# IPCC Climate Actions — Release 2026-04-24

## What changed in this release
- This release introduces a **mapping-based structure** for IPCC actions.
- Instead of only keeping the original IPCC action list format, this release includes a transformed file aligned with the **Transition Element Framework (TEF)** mapping schema.

## Mapping details
- Source file: `meed-data/actions/final-transformation/action_to_tef_mapping_final.csv`
- Filter applied: `publisher_id = ipcc`
- Output in this release: `20260424_climate_actions_mitigation_en.csv` (36 mapped IPCC mitigation actions)

## Notes on structure
- The standardized structure supports richer downstream use (e.g., subsector alignment, GPC references, timeline and investment fields).
- Compared with earlier release formats, this output keeps only maintained fields and drops non-essential descriptive fields.
- Added fields: `action_role`, `intervention_type`, `outcome_summary`, `intervention_summary`.
