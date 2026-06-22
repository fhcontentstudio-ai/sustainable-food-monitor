import json
from pathlib import Path

import pandas as pd


CORE_CATEGORIES = {
    "market_demand",
    "investment",
    "policy_regulation",
    "consumer_adoption",
    "corporate_strategy",
    "macroeconomic_context",
}

SEGMENT_GROUPS = {
    "plant_based_foods": [
        "plant_based_meat",
        "plant_based_dairy",
        "foodservice",
        "retail_cpg",
    ],
    "alternative_protein": [
        "alternative_protein_general",
        "cultivated_meat",
        "fermentation",
    ],
}


def load_signals(path="data/signals.csv") -> pd.DataFrame:
    csv_path = Path(path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Could not find {csv_path}. Run classifier.py first.")

    df = pd.read_csv(csv_path).fillna("")

    if df.empty:
        raise ValueError("signals.csv has no rows.")

    return df


def score_summary(df: pd.DataFrame) -> dict:
    return {
        "source_count": len(df),
        "average_evidence_quality_score": round(df["evidence_quality_score"].mean(), 2),
        "average_confidence_score": round(df["confidence_score"].mean(), 2),
        "high_impact_signal_count": int((df["economic_impact_score"] >= 4).sum()),
        "high_policy_risk_signal_count": int((df["policy_risk_score"] >= 4).sum()),
        "categories_present": sorted(df["signal_category"].dropna().unique().tolist()),
        "geographies_present": sorted(df["geography"].dropna().unique().tolist()),
    }


def find_missing_categories(df: pd.DataFrame) -> list:
    categories_present = set(df["signal_category"].dropna().unique())
    return sorted(list(CORE_CATEGORIES - categories_present))


def find_mixed_signals(df: pd.DataFrame) -> list:
    flags = []

    confident = df[
        (df["confidence_score"] >= 3)
        & (
            (df["economic_impact_score"] >= 3)
            | (df["policy_risk_score"] >= 3)
            | (df["consumer_adoption_score"] >= 3)
            | (df["investment_relevance_score"] >= 3)
        )
    ]

    for group_name, segments in SEGMENT_GROUPS.items():
        group_df = confident[confident["sector_segment"].isin(segments)]

        positives = group_df[group_df["signal_direction"] == "positive"]
        negatives = group_df[group_df["signal_direction"] == "negative"]

        if not positives.empty and not negatives.empty:
            flags.append(
                {
                    "type": "mixed_signal",
                    "sector_group": group_name,
                    "description": f"{group_name} has both positive and negative high-confidence signals.",
                    "positive_source_ids": positives["source_id"].head(3).tolist(),
                    "negative_source_ids": negatives["source_id"].head(3).tolist(),
                    "memo_instruction": "Avoid one-directional claims; describe the sector as mixed or segment-specific.",
                }
            )

    return flags


def analyze_evidence(
    signals_path="data/signals.csv",
    output_path="data/evidence_summary.json",
) -> dict:
    df = load_signals(signals_path)

    summary = score_summary(df)
    summary["missing_categories"] = find_missing_categories(df)
    summary["mixed_signal_flags"] = find_mixed_signals(df)

    missing = ", ".join(summary["missing_categories"]) or "none"
    summary["overall_evidence_summary"] = (
        f"Evidence base includes {summary['source_count']} sources. "
        f"Missing categories: {missing}. "
        f"Mixed signal flags: {len(summary['mixed_signal_flags'])}."
    )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Wrote evidence summary to {output_path}")
    return summary


if __name__ == "__main__":
    analyze_evidence()
