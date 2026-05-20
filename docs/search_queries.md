# Search Query Strategy (Stage 1 Template)

## Objective
Maximize recall of candidate records related to:
- InP bulk single crystal growth
- polycrystalline InP synthesis

## Query Design Principles
1. Use broad boolean families before narrowing.
2. Include synonym and variant spellings.
3. Separate paper and patent query versions.
4. Track each query version and source DB.

## Core Concept Buckets
- Material terms: InP, indium phosphide
- Single crystal terms: single crystal, bulk crystal, boule, ingot, Bridgman, VGF, LEC, CZ
- Polycrystal terms: polycrystalline, poly-InP, precursor, synthesis, feedstock
- Process-control terms: thermal field, heating, pressure control, encapsulation

## Query Logging Template
For each query run, record:
- query_id
- target database
- query string
- date
- filters used
- results count
- notes

## Citation Expansion
For each seed item:
1. export references
2. normalize cited metadata
3. map to existing records if present
4. add missing records as new candidates
