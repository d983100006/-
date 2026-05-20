#!/usr/bin/env python3
"""Build summary reports from master CSVs (skeleton)."""

from pathlib import Path
import csv

PAPERS_CSV = Path("data/papers_master.csv")
PATENTS_CSV = Path("data/patents_master.csv")
REPORTS_DIR = Path("reports")
SUMMARY_MD = REPORTS_DIR / "stage_summary.md"


def count_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8") as f:
        return max(sum(1 for _ in csv.reader(f)) - 1, 0)


def main() -> int:
    for path in (PAPERS_CSV, PATENTS_CSV):
        if not path.exists():
            print(f"Missing required file: {path}")
            return 1

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    papers_n = count_rows(PAPERS_CSV)
    patents_n = count_rows(PATENTS_CSV)

    SUMMARY_MD.write_text(
        "\n".join(
            [
                "# Stage Summary (Skeleton)",
                "",
                f"- Papers records: {papers_n}",
                f"- Patents records: {patents_n}",
                "",
                "No technical conclusions in Stage 1.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"[skeleton] Wrote report: {SUMMARY_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
