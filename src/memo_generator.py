import json
from pathlib import Path

import pandas as pd
from anthropic import Anthropic


MODEL = "claude-sonnet-4-6"


def load_prompt(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def parse_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])


def call_claude(prompt: str, payload: dict) -> dict:
    client = Anthropic()

    with client.messages.stream(
        model=MODEL,
        max_tokens=32000,
        temperature=0,
        system=prompt,
        messages=[
            {
                "role": "user",
                "content": json.dumps(payload, indent=2),
            }
        ],
    ) as stream:
        response = stream.get_final_message()

    return parse_json(response.content[0].text)


def write_report(path: str, markdown: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(markdown, encoding="utf-8")
    print(f"Wrote report: {path}")


def generate_gap_report(decision: dict, output_path="reports/evidence_gap_report.md") -> None:
    lines = [
        "# Evidence Gap Report",
        "",
        decision["reasoning_summary"],
        "",
        "## Missing Categories",
        *[f"- {cat}" for cat in decision["missing_categories"]],
        "",
        "## Recommended Next Sources",
        *[f"- {src}" for src in decision["recommended_next_sources"]],
    ]

    write_report(output_path, "\n".join(lines))


def generate_memos(
    signals_path="data/signals.csv",
    decision_path="data/decision.json",
) -> None:
    signals_df = pd.read_csv(signals_path).fillna("")
    decision = json.loads(Path(decision_path).read_text(encoding="utf-8"))

    payload = {
        "decision": decision,
        "signals": signals_df.to_dict(orient="records"),
        "instruction": "Return JSON only with key report_markdown.",
    }

    if decision["decision"] == "evidence_gap_report_only":
        generate_gap_report(decision)
        return

    if decision["policy_memo_allowed"]:
        prompt = load_prompt("prompts/generate_policy_memo.md")
        result = call_claude(prompt, payload)
        write_report("reports/policy_memo.md", result["report_markdown"])

    if decision["client_brief_allowed"]:
        prompt = load_prompt("prompts/generate_client_brief.md")
        result = call_claude(prompt, payload)
        write_report("reports/client_brief.md", result["report_markdown"])

    if not decision["policy_memo_allowed"] and not decision["client_brief_allowed"]:
        generate_gap_report(decision)


if __name__ == "__main__":
    generate_memos()
