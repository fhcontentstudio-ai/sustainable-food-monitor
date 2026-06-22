import json
from pathlib import Path

import pandas as pd
from anthropic import Anthropic

from src.source_loader import load_sources


MODEL = "claude-sonnet-4-6"

SIGNAL_COLUMNS = [
    "signal_id",
    "source_id",
    "date",
    "source_title",
    "geography",
    "sector_segment",
    "signal_category",
    "signal_direction",
    "mechanism_type",
    "behavioral_mechanism",
    "norm_type",
    "framing_type",
    "time_horizon",
    "economic_impact_score",
    "policy_risk_score",
    "consumer_adoption_score",
    "investment_relevance_score",
    "evidence_quality_score",
    "confidence_score",
    "strategic_implication",
]


def load_prompt(path="prompts/classify_and_score_source.md") -> str:
    return Path(path).read_text(encoding="utf-8")


def parse_json(text: str) -> dict:
    """Parse strict JSON, with a small fallback if the model adds extra text."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])


def call_claude(prompt: str, source_row: dict) -> dict:
    client = Anthropic()

    user_payload = {
        "instruction": "Classify and score this source. Return JSON only.",
        "source": source_row,
    }

    response = client.messages.create(
        model=MODEL,
        max_tokens=1200,
        temperature=0,
        system=prompt,
        messages=[
            {
                "role": "user",
                "content": json.dumps(user_payload, indent=2),
            }
        ],
    )

    return parse_json(response.content[0].text)


def classify_sources(
    sources_path="data/sources.csv",
    output_path="data/signals.csv",
) -> pd.DataFrame:
    sources_df = load_sources(sources_path)
    prompt = load_prompt()
    rows = []

    for idx, source in sources_df.iterrows():
        source_dict = source.to_dict()
        result = call_claude(prompt, source_dict)

        row = {
            "signal_id": f"SIG{idx + 1:03d}",
            "source_id": source_dict["source_id"],
            "date": source_dict["date"],
            "source_title": source_dict["source_title"],
            "geography": result.get("geography", source_dict["geography"]),
            "sector_segment": result.get("sector_segment", source_dict["sector_segment"]),
            "signal_category": result.get("signal_category", ""),
            "signal_direction": result.get("signal_direction", ""),
            "mechanism_type": result.get("mechanism_type", ""),
            "behavioral_mechanism": result.get("behavioral_mechanism", "null"),
            "norm_type": result.get("norm_type", "null"),
            "framing_type": result.get("framing_type", "null"),
            "time_horizon": result.get("time_horizon", "ongoing"),
            "economic_impact_score": result.get("economic_impact_score", 0),
            "policy_risk_score": result.get("policy_risk_score", 0),
            "consumer_adoption_score": result.get("consumer_adoption_score", 0),
            "investment_relevance_score": result.get("investment_relevance_score", 0),
            "evidence_quality_score": result.get("evidence_quality_score", 0),
            "confidence_score": result.get("confidence_score", 0),
            "strategic_implication": result.get("strategic_implication", ""),
        }

        rows.append(row)
        print(f"Classified {row['source_id']} -> {row['signal_category']} [{row['mechanism_type']}]")

    signals_df = pd.DataFrame(rows, columns=SIGNAL_COLUMNS)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    signals_df.to_csv(output_path, index=False)

    print(f"Wrote {len(signals_df)} signals to {output_path}")
    return signals_df


if __name__ == "__main__":
    classify_sources()
