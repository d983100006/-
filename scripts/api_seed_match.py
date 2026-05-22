#!/usr/bin/env python3
"""Stage 3.0 seed metadata completion and API coverage check (GET-only)."""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

PAPERS_CSV = Path("data/papers_master.csv")
OUT_CSV = Path("data/api_seed_match_results.csv")
OUT_REPORT = Path("reports/api_seed_coverage_report.md")

REQUIRED_SOURCE_DATABASE = "user_seed"
REQUEST_INTERVAL_SEC = 1.2
MAX_RETRIES = 4
BACKOFF_BASE = 2.0


def normalize_doi(v: str) -> str:
    v = (v or "").strip()
    v = re.sub(r"^https?://(dx\.)?doi\.org/", "", v, flags=re.I)
    return v.strip().lower()


def req_json(url: str, headers: dict[str, str] | None = None) -> tuple[dict[str, Any] | None, str]:
    headers = headers or {}
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=30) as resp:
                code = resp.getcode()
                data = resp.read().decode("utf-8", errors="replace")
                time.sleep(REQUEST_INTERVAL_SEC)
                if code == 200:
                    return json.loads(data), "ok"
                return None, f"http_{code}"
        except urllib.error.HTTPError as e:  # type: ignore[attr-defined]
            if e.code == 429 and attempt < MAX_RETRIES - 1:
                time.sleep(BACKOFF_BASE**attempt)
                continue
            return None, f"http_{e.code}"
        except Exception as e:
            return None, f"error:{type(e).__name__}"
    return None, "rate_limited"


def query_semantic_scholar(title: str, doi: str) -> tuple[dict[str, Any], str]:
    notes = []
    result: dict[str, Any] = {}
    if doi:
        url = (
            "https://api.semanticscholar.org/graph/v1/paper/DOI:"
            + urllib.parse.quote(doi)
            + "?fields=paperId,title,citationCount,referenceCount,abstract,openAccessPdf"
        )
        data, status = req_json(url)
        notes.append(f"S2_doi:{status}")
        if data:
            result = data
    if not result and title:
        q = urllib.parse.quote(title)
        url = (
            "https://api.semanticscholar.org/graph/v1/paper/search?query="
            + q
            + "&limit=1&fields=paperId,title,citationCount,referenceCount,abstract,openAccessPdf"
        )
        data, status = req_json(url)
        notes.append(f"S2_title:{status}")
        if data and data.get("data"):
            result = data["data"][0]
    return result, ";".join(notes)


def query_openalex(title: str, doi: str) -> tuple[dict[str, Any], str]:
    notes = []
    result: dict[str, Any] = {}
    if doi:
        url = "https://api.openalex.org/works/https://doi.org/" + urllib.parse.quote(doi)
        data, status = req_json(url)
        notes.append(f"OA_doi:{status}")
        if data and data.get("id"):
            result = data
    if not result and title:
        q = urllib.parse.quote(title)
        url = f"https://api.openalex.org/works?search={q}&per-page=1"
        data, status = req_json(url)
        notes.append(f"OA_title:{status}")
        if data and data.get("results"):
            result = data["results"][0]
    return result, ";".join(notes)


def query_crossref(title: str, doi: str) -> tuple[dict[str, Any], str]:
    notes = []
    result: dict[str, Any] = {}
    if doi:
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
        data, status = req_json(url, headers={"User-Agent": "seed-check/1.0 (mailto:stage3@example.com)"})
        notes.append(f"CR_doi:{status}")
        if data and data.get("message"):
            result = data["message"]
    if not result and title:
        q = urllib.parse.quote(title)
        url = f"https://api.crossref.org/works?query.title={q}&rows=1"
        data, status = req_json(url, headers={"User-Agent": "seed-check/1.0 (mailto:stage3@example.com)"})
        notes.append(f"CR_title:{status}")
        items = (data or {}).get("message", {}).get("items", [])
        if items:
            result = items[0]
    return result, ";".join(notes)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()

    with PAPERS_CSV.open("r", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r.get("source_database") == REQUIRED_SOURCE_DATABASE]

    out_rows = []
    for r in rows:
        title = (r.get("title") or "").strip()
        doi_seed = normalize_doi(r.get("doi") or "")

        s2, n1 = query_semantic_scholar(title, doi_seed)
        oa, n2 = query_openalex(title, doi_seed)
        cr, n3 = query_crossref(title, doi_seed)

        api_sources = []
        if s2:
            api_sources.append("semantic_scholar")
        if oa:
            api_sources.append("openalex")
        if cr:
            api_sources.append("crossref")

        matched_title = s2.get("title") or oa.get("display_name") or ((cr.get("title") or [""])[0] if cr else "")
        citation_count = s2.get("citationCount")
        if citation_count is None:
            citation_count = oa.get("cited_by_count")
        reference_count = s2.get("referenceCount")
        if reference_count is None:
            reference_count = oa.get("referenced_works_count")

        abstract_available = "yes" if (s2.get("abstract") or oa.get("abstract_inverted_index") or cr.get("abstract")) else "no"
        open_access_pdf_url = ""
        if s2.get("openAccessPdf") and isinstance(s2["openAccessPdf"], dict):
            open_access_pdf_url = s2["openAccessPdf"].get("url", "")
        if not open_access_pdf_url:
            open_access_pdf_url = ((oa.get("open_access") or {}).get("oa_url") if oa else "") or ""

        crossref_doi = normalize_doi(cr.get("DOI", "")) if cr else ""
        match_confidence = "high" if doi_seed and (crossref_doi == doi_seed or (oa.get("doi", "").lower().endswith(doi_seed))) else ("medium" if api_sources else "uncertain")

        out_rows.append(
            {
                "record_id": r.get("record_id", ""),
                "user_index": r.get("user_index", ""),
                "title": title,
                "doi_seed": doi_seed,
                "semantic_scholar_id": s2.get("paperId", "") if s2 else "",
                "openalex_id": oa.get("id", "") if oa else "",
                "crossref_doi": crossref_doi,
                "matched_title": matched_title,
                "match_confidence": match_confidence,
                "api_found": "yes" if api_sources else "no",
                "api_sources_found": ";".join(api_sources),
                "citation_count": citation_count if citation_count is not None else "",
                "reference_count": reference_count if reference_count is not None else "",
                "abstract_available": abstract_available,
                "open_access_pdf_url": open_access_pdf_url,
                "metadata_notes": ";".join(x for x in [n1, n2, n3] if x),
            }
        )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = list(out_rows[0].keys()) if out_rows else []
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)

    total = len(out_rows)
    api_found_n = sum(1 for x in out_rows if x["api_found"] == "yes")
    s2_n = sum(1 for x in out_rows if "semantic_scholar" in x["api_sources_found"])
    oa_n = sum(1 for x in out_rows if "openalex" in x["api_sources_found"])
    cr_n = sum(1 for x in out_rows if "crossref" in x["api_sources_found"])
    not_found = [x for x in out_rows if x["api_found"] == "no"]
    cand_doi = [x for x in out_rows if not x["doi_seed"] and x["crossref_doi"]]
    missing_doi_url = [x for x in out_rows if (not x["doi_seed"] and not x["crossref_doi"]) or not x["open_access_pdf_url"]]
    ref_expand = [x for x in out_rows if x["api_found"] == "yes" and str(x["reference_count"]).strip() not in ("", "0")]

    lines = [
        "# API Seed Coverage Report (Stage 3.0)",
        "",
        f"- Seed records processed: {total}",
        f"- API matched records: {api_found_n}/{total}",
        f"- Semantic Scholar matched: {s2_n}",
        f"- OpenAlex matched: {oa_n}",
        f"- Crossref matched: {cr_n}",
        "",
        "## Unmatched records",
    ]
    lines += [f"- {x['record_id']} ({x['title']})" for x in not_found] or ["- None"]
    lines += ["", "## Candidate DOI supplements (do not overwrite seed DOI)"]
    lines += [f"- {x['record_id']}: candidate DOI `{x['crossref_doi']}`" for x in cand_doi] or ["- None"]
    lines += ["", "## Still missing DOI / URL"]
    lines += [f"- {x['record_id']}: doi_seed={x['doi_seed'] or 'N/A'}, oa_pdf_url={'yes' if x['open_access_pdf_url'] else 'no'}" for x in missing_doi_url] or ["- None"]
    lines += ["", "## Suggested for reference expansion"]
    lines += [f"- {x['record_id']} ({x['reference_count']} references; sources={x['api_sources_found']})" for x in ref_expand] or ["- None"]
    lines += ["", "No final technical conclusions in this stage."]

    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote: {OUT_CSV}")
    print(f"Wrote: {OUT_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
