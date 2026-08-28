# C40 High Impact Actions — Release 2026-04-24

## What changed in this release
- This release introduces a **mapping-based structure** for C40 actions.
- Instead of only keeping the original C40 action list format, this release includes a transformed file aligned with the **Transition Element Framework (TEF)** mapping schema.

## Mapping details
- Output in this release: `20260424_climate_actions_mitigation_en.csv` (17 mapped C40 mitigation actions)

## Notes on structure
- The standardized structure supports richer downstream use (e.g., subsector alignment, GPC references, timeline and investment fields).
- Compared with earlier release formats, this output keeps only maintained fields and drops non-essential descriptive fields.
- Added fields: `action_role`, `intervention_type`, `outcome_summary`, `intervention_summary`.

## Translation fix (c40_0012, c40_0035, c40_0042)
- ES/PT rows for these three actions were present but **skipped on load** because `intervention_summary` contained unquoted commas (pandas `on_bad_lines="warn"` dropped the rows).
- Result in Global API: `name_i18n` / `description_i18n` had empty `es`/`pt`, so the frontend fell back to English.
- Fix: re-quote ES/PT CSVs (and refresh name/description text) so all 17 actions load in every locale. Re-upload to S3 and re-run `action_pathways_to_modelled`.
