# Inclusion / Exclusion Rules (Stage 1 Draft)

## Purpose
Define conservative screening logic for high-recall candidate collection.

## Guiding Principle
**Recall > Precision** in early stages.

## Inclusion (Candidate-Level)
Include as candidate when any one condition is met:
1. Mentions InP + crystal growth, bulk growth, boule growth, or related growth process terms.
2. Mentions polycrystalline InP synthesis, precursor synthesis, or feedstock preparation possibly linked to crystal growth.
3. Appears in references of a seed item and plausibly connected to InP growth/synthesis.
4. Patent/paper metadata suggests relevance but abstract is incomplete.

## Exclusion (Only with Clear Evidence)
Exclude only when at least one is explicitly true:
1. Not about InP material at all.
2. Solely about downstream device performance with no growth/synthesis/process relevance.
3. Duplicate of an already captured record (after dedup process).
4. Non-technical item with no usable scientific or patent evidence.

## Required Fields for Every Decision
- `raw_evidence`
- `candidate_judgement`
- `confidence`

If evidence is insufficient: mark judgement as `uncertain`.

## Prohibited in Stage 1
- Claiming full-text conclusions without full-text access.
- Using unstated assumptions as decision evidence.
