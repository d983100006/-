#!/usr/bin/env python3
"""Deduplicate records across papers/patents masters (skeleton)."""

from pathlib import Path
import csv

PAPERS_CSV = Path("data/papers_master.csv")
PATENTS_CSV = Path("data/patents_master.csv")
EXCLUDED_CSV = Path("data/excluded_records.csv")


def main() -> int:
    for path in (PAPERS_CSV, PATENTS_CSV, EXCLUDED_CSV):
        if not path.exists():
            print(f"Missing required file: {path}")
            return 1

    # TODO:
    # 1) normalize title/doi/patent_number keys
    # 2) identify exact + fuzzy duplicates
    # 3) keep highest-evidence canonical record
    # 4) append suppressed duplicates to excluded_records with reason="duplicate"

    with PAPERS_CSV.open("r", encoding="utf-8") as f:
        papers_count = sum(1 for _ in csv.reader(f)) - 1
    with PATENTS_CSV.open("r", encoding="utf-8") as f:
        patents_count = sum(1 for _ in csv.reader(f)) - 1

    print(f"[skeleton] papers={max(papers_count,0)} patents={max(patents_count,0)}")
    print("[skeleton] Dedup logic not implemented yet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
