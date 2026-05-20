#!/usr/bin/env python3
"""Import RIS records into data/papers_master.csv (skeleton)."""

from pathlib import Path
import csv
import sys

PAPERS_CSV = Path("data/papers_master.csv")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/import_ris.py <input.ris>")
        return 1

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Input not found: {input_path}")
        return 1

    # TODO: parse RIS records.
    # Stage 1 skeleton only: no parsing logic yet.
    with PAPERS_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        _ = writer

    print(f"[skeleton] Ready to import RIS from: {input_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
