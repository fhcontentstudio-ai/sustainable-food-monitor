from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = [
    "source_id",
    "date",
    "source_title",
    "source_url",
    "source_type",
    "geography",
    "sector_segment",
    "source_text",
    "key_notes",
    "added_by",
]


def load_sources(path="data/sources.csv") -> pd.DataFrame:
    """Read sources.csv and validate that it has the required v1 fields."""

    csv_path = Path(path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Could not find {csv_path}")

    df = pd.read_csv(csv_path)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"sources.csv is missing required columns: {missing}")

    if df.empty:
        raise ValueError("sources.csv has no rows. Add 10-20 sources first.")

    if df["source_id"].duplicated().any():
        raise ValueError("source_id values must be unique.")

    df = df.fillna("")

    if len(df) < 8:
        print("Warning: fewer than 8 sources. Only an evidence-gap report may be justified.")

    print(f"Loaded {len(df)} sources from {csv_path}")
    return df


if __name__ == "__main__":
    load_sources()
