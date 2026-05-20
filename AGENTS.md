# AGENTS.md

## Scope
This file applies to the entire repository.

## Stage 1 Rules (Scoping & Data Collection Setup)
- Primary objective in Stage 1 is **recall > precision**.
- Do **not** exclude candidates too early.
- Do **not** claim or imply full-text reading unless full text is actually available and read.
- Do **not** use common sense as a substitute for evidence.
- Every judgement must preserve:
  - raw evidence
  - candidate judgement
  - confidence
- `heating_method` must use exactly one of:
  - `induction`
  - `resistance`
  - `mixed`
  - `unclear`
  - `not_applicable`
- If evidence is insufficient, mark as `uncertain`.

## Current Task Constraints
- Stage 1 repository setup only.
- No external search in this stage.
- No technical conclusions in this stage.
