from dotenv import load_dotenv
load_dotenv()

import json
from pathlib import Path

from src.source_loader import load_sources
from src.classifier import classify_sources
from src.evidence_analyzer import analyze_evidence
from src.decision_agent import run_decision_agent
from src.source_finder import find_candidates
from src.memo_generator import generate_memos


def search_for_missing_sources(decision_path="data/decision.json") -> None:
    decision = json.loads(Path(decision_path).read_text(encoding="utf-8"))
    missing = decision.get("missing_categories", [])

    if not missing:
        print("No category gaps found. Skipping source search.")
        return

    print("\n--- Evidence gaps found. Searching for candidate sources ---\n")

    for category in missing:
        print(f"\nSearching for: {category}")
        candidates = find_candidates(category)

        if not candidates:
            print(f"  No candidates found for {category}.")
            continue

        print(f"  Found {len(candidates)} candidate(s):\n")
        for i, c in enumerate(candidates, 1):
            print(f"  [{i}] {c.get('title', 'Untitled')}")
            print(f"      {c.get('url', 'No URL')}")
            print(f"      {c.get('description', '')}\n")

    print("  IMPORTANT: Review these manually. Read the actual article before")
    print("  adding it to data/sources.csv. Do not add a source you have not read.\n")


def main():
    print("\nStep 1: Loading and validating sources...")
    load_sources("data/sources.csv")

    print("\nStep 2: Classifying and scoring sources...")
    classify_sources("data/sources.csv", "data/signals.csv")

    print("\nStep 3: Analyzing evidence quality and mixed signals...")
    analyze_evidence("data/signals.csv", "data/evidence_summary.json")

    print("\nStep 4: Running decision agent...")
    run_decision_agent("data/evidence_summary.json", "data/decision.json")

    print("\nStep 4b: Searching for candidate sources to fill evidence gaps...")
    search_for_missing_sources("data/decision.json")

    print("\nStep 5: Generating justified report outputs...")
    generate_memos("data/signals.csv", "data/decision.json")

    print("\nDone. Check the reports/ folder.")


if __name__ == "__main__":
    main()
