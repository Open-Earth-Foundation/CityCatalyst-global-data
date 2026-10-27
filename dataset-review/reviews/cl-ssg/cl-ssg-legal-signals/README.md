# Chile legal signals - SSG municipal feasibility (waste sector)

Curated legal-feasibility assessment for municipal climate mitigation actions in Chile, focused on the waste sector.

## Why we use it

- Helps estimate whether a municipality can implement an action under current Chilean law.
- Combines legal basis, local governance capacity, and financing access in one score.

## Current release

- `releases/v1/`
- Scope: waste-sector actions (Spanish and English files).

## What is included in v1

- `data/Viabilidad_Municipal_Residuos_FINAL_Resumen.csv`
- `data/Viabilidad_Municipal_Residuos_FINAL_Resumen_en.csv`
- `data/Viabilidad_Municipal_Residuos_FINAL_Evaluación.csv`
- `data/Viabilidad_Municipal_Residuos_FINAL_Evaluación_en.csv`
- `methodology/Minuta_Metodologica_Residuos_FINAL.md`
- `methodology/Minuta_Metodologica_Residuos_FINAL_en.md`

## Scoring logic (simple)

- Total score (0-100) = `Legal (40%) + Governance (30%) + Financing (30%)`.
- Score interpretation:
  - `>=75`: action viable
  - `40-74`: viable with conditions
  - `<40`: low current viability

## Notes

- This release is a benchmark-style assessment, not city-specific legal advice.
- CSV exports are presentation-oriented and may need normalization before database ingestion.
