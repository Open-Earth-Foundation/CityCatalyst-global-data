# Review: c40-high-impact-actions (release 2025-12-16)

## Dataset snapshot
- File reviewed: `20251216_climate_actions_en.csv`
- Rows: 41 actions
- Columns: `ID`, `Action`, `Short name`, `Sector (Primary)`
- Coverage: mitigation + adaptation themes across Transport, Buildings, Waste, Food, Urban Planning and Design, Adaptation, Air Quality, and Ports.

## What this release is useful for now
- Provides a curated list of city climate action concepts with clear human-readable descriptions.
- Useful as a **reference library / action taxonomy seed** for discovery, curation, and expert review.
- Can support preliminary tagging and alignment work against existing action catalogs.

## Key limitations for prioritization workflows
- Current structure is not sufficient for direct HIAP prioritization scoring.
- Sector is too high-level; we need at least **subsector-level** mapping to connect actions to inventories and implementation contexts.
- Missing core prioritization attributes, including:
  - mitigation potential bucket (`very_low`, `low`, `medium`, `high`, `very_high`)
  - implementation timeline bucket (`short_<5y`, `medium_5_10y`, `long_>10y`)
  - investment cost bucket (`low`, `medium`, `high`)
- For adaptation actions, missing hazard-specific context and expected impact severity bucket.

## Recommendation
- Keep this dataset in catalog as a **reference-supporting dataset** (not yet a scoring-ready action dataset).
- Do not use it as a standalone input for ranking/prioritization until enrichment fields are added.

## Next steps
1. Run de-duplication/overlap check with the current CityCatalyst action bank.
2. Define a minimum enrichment schema for scoring readiness (subsector, mitigation/adaptation attributes, timeline, cost, confidence).
3. Annotate this release (or a derived table) with the minimum schema so it can be tested in the prioritization pipeline.