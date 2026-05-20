# Decision Questions (for Later Extraction Stages)

> Stage 1 note: questions are defined now, but no technical conclusions are made yet.

## Crystal Growth Method
- What growth method is described?
- Is method description from raw evidence or inferred?
- Confidence level?

## Thermal Field / Heating
- Which heating method is indicated?
- Allowed labels:
  - `induction`
  - `resistance`
  - `mixed`
  - `unclear`
  - `not_applicable`
- If insufficient evidence, mark `uncertain`.

## Pressure / Atmosphere Control
- Is pressure control described?
- What parameters are explicit vs missing?
- Confidence level?

## Polycrystalline InP Synthesis
- Is polycrystal synthesis route described?
- Inputs/intermediates/process controls explicit?
- Confidence level?

## Safety Design
- Are safety mechanisms or safeguards described?
- Is evidence from patent claims, specification, or paper text?
- Confidence level?

## Evidence Discipline
For every answer:
- Keep `raw_evidence` text snippet or source pointer.
- Keep `candidate_judgement`.
- Keep `confidence`.
- Do not claim full-text-derived conclusions without full text.
