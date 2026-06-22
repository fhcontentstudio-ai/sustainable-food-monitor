import json
from pathlib import Path


POLICY_REQUIRED = {"policy_regulation", "market_demand", "investment"}
CLIENT_REQUIRED = {"market_demand", "consumer_adoption", "corporate_strategy"}


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def decide(summary: dict) -> dict:
    source_count = summary["source_count"]
    avg_quality = summary["average_evidence_quality_score"]
    avg_conf = summary["average_confidence_score"]
    categories = set(summary["categories_present"])
    missing = summary["missing_categories"]
    mixed_flags = summary["mixed_signal_flags"]

    policy_allowed = POLICY_REQUIRED.issubset(categories)
    client_allowed = CLIENT_REQUIRED.issubset(categories)

    confidence_cap = "high"
    reasons = []

    if source_count < 8:
        decision = "evidence_gap_report_only"
        confidence_cap = "none"
        reasons.append("Fewer than 8 sources; too little evidence for a credible memo.")
    elif source_count < 10:
        decision = "generate_limited_report"
        confidence_cap = "low"
        reasons.append("Only 8-9 sources; report must be limited.")
    elif avg_quality < 3.0:
        decision = "generate_limited_report"
        confidence_cap = "low"
        reasons.append("Average evidence quality is below 3.0.")
    elif avg_conf < 3.0:
        decision = "generate_limited_report"
        confidence_cap = "low"
        reasons.append("Average confidence is below 3.0.")
    elif len(categories) < 4:
        decision = "generate_limited_report"
        confidence_cap = "low_to_moderate"
        reasons.append("Fewer than 4 core categories are represented.")
    elif policy_allowed and client_allowed:
        decision = "generate_full_policy_memo_and_client_brief"
        reasons.append("Evidence supports both policy and client outputs.")
    elif policy_allowed:
        decision = "generate_policy_memo_only"
        reasons.append("Evidence supports policy memo, but not client brief.")
    elif client_allowed:
        decision = "generate_client_brief_only"
        reasons.append("Evidence supports client brief, but not policy memo.")
    else:
        decision = "generate_limited_report"
        confidence_cap = "low_to_moderate"
        reasons.append("Evidence is usable but lacks required categories for full outputs.")

    if mixed_flags and confidence_cap == "high":
        confidence_cap = "moderate"
        reasons.append("Mixed signals require a more cautious conclusion.")

    recommended = [f"Collect more sources for: {cat}" for cat in missing]

    return {
        "decision": decision,
        "policy_memo_allowed": policy_allowed and decision != "evidence_gap_report_only",
        "client_brief_allowed": client_allowed and decision != "evidence_gap_report_only",
        "confidence_cap": confidence_cap,
        "reasoning_summary": " ".join(reasons),
        "missing_categories": missing,
        "contradictions_to_include": bool(mixed_flags),
        "recommended_next_sources": recommended,
        "required_disclaimer": (
            "This output is directional and limited by the current evidence base."
            if confidence_cap in ["low", "low_to_moderate", "moderate"]
            else ""
        ),
    }


def run_decision_agent(
    evidence_path="data/evidence_summary.json",
    output_path="data/decision.json",
) -> dict:
    summary = load_json(evidence_path)
    decision = decide(summary)

    Path(output_path).write_text(json.dumps(decision, indent=2), encoding="utf-8")
    print(f"Wrote decision to {output_path}: {decision['decision']}")

    return decision


if __name__ == "__main__":
    run_decision_agent()
