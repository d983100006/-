# InP Growth Public Data Research Repository

This repository is for staged research on:
- InP bulk single crystal growth
- polycrystalline InP synthesis

## Stage Plan

### Stage 1 (current)
Repository and workflow scaffolding only:
- data structure and CSV schemas
- screening and judgement rules
- search strategy templates
- import and deduplication script skeletons
- report-building skeleton

**Constraints for Stage 1**
- No external searching.
- No technical conclusions.

### Stage 2+
- Broad retrieval of candidate papers and patents
- citation expansion from seed references
- structured extraction after full-text PDFs are available
- decision brief drafting for executive audience

## Repository Layout

- `AGENTS.md`: operating rules for all contributors/agents
- `data/`: master datasets and relation tables
- `docs/`: inclusion rules, query plans, decision questions
- `scripts/`: import, deduplication, report skeleton scripts
- `reports/`: generated outputs and guidance

## Data Governance Principles

- Prioritize recall in early-stage collection.
- Avoid premature exclusion.
- Preserve evidence trail for each judgement.
- Keep uncertainty explicit.
