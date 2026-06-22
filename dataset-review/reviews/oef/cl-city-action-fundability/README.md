# OEF — Chile city-action fundability (cl-city-action-fundability)

The consolidated OEF product for *how a Chilean comuna can pay for a climate action*. It brings the supply side (a harmonized finance inventory + a financing-availability indicator) and the model side (a four-layer fundability model) into one folder, and is now implemented in production (modelled tables + score function + `climate-finance` API). **It supersedes and replaces the former `cl-finance-inventory` and `cl-action-fundability` reviews** — everything they did lives here, refreshed.

It is an OEF model and curation, not a new external source: it unions and scores already-reviewed datasets and re-grants nothing. It is the data side of the financial-feasibility workstream for MEED+ HIAP, feeding that tool's Feasibility pillar.

## What it produces

1. **A finance inventory** — the ten vetted Chile climate-finance supply reviews harmonized into one fund table (99 funds), plus an action **financing-availability (coverage)** label. This is the FINANCE/supply layer.
2. **A fundability model** — combines four layers (action catalog, SINIM/Censo municipal capacity, the finance inventory, the projects pipeline) into a per `(action × comuna)` route/effort bucket + a 0–1 `financial_feasibility` score + the funds that fit. Not a funding probability, not a comuna ranking.
3. **The production implementation** — the model landed as real modelled tables, a read-time score function, and the `climate-finance` API in `CityCatalyst/global-api`, loaded by `cc-mage` pipelines (see **Status** below; full object/endpoint list in `releases/v1/implementation.md` → As-built). The earlier traceable `finance_db` CSV fixture that prototyped this has been removed.

## Inputs (authoritative upstream, not duplicated here)

| Layer | Source review(s) | Role |
| --- | --- | --- |
| Action (what) | `reviews/cl-ssg/cl-ssg-projects` (actions catalog, 102) | capital intensity; formulation demand; self-financeability |
| City (who) | `reviews/cl-subdere/cl-subdere-sinim` + `reviews/cl-ine/cl-ine-censo` | fiscal autonomy and delivery capacity (the 2×2) |
| Finance (route) | the ten `cl-*/cl-*-fondos` supply reviews (harmonized here) | usable, municipality-eligible funds + access pathway |
| Projects (evidence) | `reviews/cl-ssg/cl-ssg-projects`; CONAF / FPA / GCF awards | calibration, precedent, benchmarks |

The ten supply reviews behind the inventory: `cl-mma`, `cl-minenergia`, `cl-subdere`, `cl-minvu`, `cl-gore`, `cl-corfo`, `cl-conaf`, `cl-mtt`, `cl-indap`, `cl-mop` (grouped as the `chile-finance` collection). Each remains authoritative for its own provenance, licence, parsing and recurrence detail.

## Structure (analysis + methodology record)

```
cl-city-action-fundability/
├── README.md                 (this file)
├── methodology.md            (the shareable overview: how the fundability score works)
└── releases/v1/
    ├── implementation.md            the production design (tables, score function, API) + As-built summary
    ├── 01_finance_inventory.ipynb   supply layer: harmonize 10 sources → inventory + coverage
    ├── 02_fundability_model.ipynb   the four-layer model (autonomy/capacity formulas, the score)
    ├── extract_inventory.ipynb      reproducible extraction harness (one reusable prompt; refresh source rows)
    ├── review.md                    release epistemic contract
    ├── data/
    │   ├── chile_finance_inventory.csv         99 funds, harmonized (now productionised as finance_opportunity)
    │   ├── financing_coverage_by_action.csv    102 actions × coverage_level
    │   └── action_coverage_matrix.csv          102 actions × gap dashboard
    └── tests/                       post-load expectations for the modelled tables
```

The exploratory fixtures used to *design* the schema — the SQLite `finance_preview.db`, the `finance_db/` CSVs, the precomputed `fundability_scored.csv`, the preview example JSONs and `build_*` scripts — were removed once the real tables landed (the implementation supersedes them). Refresh of the analysis: re-run `01` after any source release, then `02`.

## Provenance & licence

Authority lives upstream; this product inherits the **most restrictive upstream licence** and re-grants nothing. The binding constraint is **SINIM** (non-commercial + attribution clear; commercial unresolved pending SUBDERE clearance). Finance sources add per-source terms (e.g. CORFO `CC BY-NC-ND`). Treat outputs as non-commercial + attribution until the SINIM clearance lands, and check each input review before redistributing.

## Status

**Implemented in production.** The four-layer model is built end to end in `CityCatalyst/global-api` (modelled tables + the score function + the API) and `cc-mage` (the load pipelines). See `releases/v1/implementation.md` → **As-built** for the authoritative object/pipeline/endpoint list.

- **Tables / function:** `finance_opportunity` (+`_action`), `finance_project` (+`_action`), `city_finance_profile`, and the read-time score `modelled.city_action_financial_feasibility(...)` — Alembic `9f3c1a7b2e10`, `a4f1c9d72b3e`, `b8e2f5a1c9d4`, `c3f9a7e1d2b8`.
- **Pipelines:** `cl_finance_opportunity_to_modelled`, `cl_finance_project_to_modelled`, `cl_city_finance_profile_to_modelled`.
- **Endpoints:** `climate-finance/opportunities`, `.../feasibility`, `.../actions/{action_id}`, `.../projects`.

This folder is now the analysis + methodology record behind that implementation. Remaining methodology caveat: the curated `access_tier` that will replace the current "direct" substring heuristic (see `methodology.md` → *Status and what's next*), pending SINIM commercial-licence clearance.
