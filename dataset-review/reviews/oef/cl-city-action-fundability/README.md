# OEF — Chile city-action fundability (cl-city-action-fundability)

The consolidated OEF product for *how a Chilean comuna can pay for a climate action*. It brings the supply side (a harmonized finance inventory + a financing-availability indicator) and the model side (a four-layer fundability model) into one folder, and is now implemented in production (modelled tables + score function + `climate-finance` API). **It supersedes and replaces the former `cl-finance-inventory` and `cl-action-fundability` reviews** — everything they did lives here, refreshed.

It is an OEF model and curation, not a new external source: it unions and scores already-reviewed datasets and re-grants nothing. It is the data side of the financial-feasibility workstream for MEED+ HIAP, feeding that tool's Feasibility pillar.

## What it produces

1. **A finance inventory** — the ten vetted Chile climate-finance supply reviews harmonized into one fund table (99 funds), plus an action **financing-availability (coverage)** label. This is the FINANCE/supply layer.
2. **A fundability model** — combines four layers (action catalog, SIM/BEP fiscal autonomy + census-derived municipal capacity, the finance inventory, the projects pipeline) into a per `(action × comuna)` route/effort bucket + a 0–1 `financial_feasibility` score + the funds that fit. Not a funding probability, not a comuna ranking.
3. **The production implementation** — the model landed as real modelled tables, a read-time score function, and the `climate-finance` API in `CityCatalyst/global-api`, loaded by `cc-mage` pipelines (see **Status** below; full object/endpoint list in `releases/v1/implementation.md` → As-built). The earlier traceable `finance_db` CSV fixture that prototyped this has been removed.

## Inputs (authoritative upstream, not duplicated here)

| Layer | Source review(s) | Role |
| --- | --- | --- |
| Action (what) | `reviews/cl-ssg/cl-ssg-projects` (actions catalog, 102) | capital intensity; formulation demand; self-financeability |
| City (who) | `reviews/cl-subdere/cl-subdere-sim-bep` (autonomy, from v3) + `reviews/oef/cl-municipal-capacity-tier` (capacity, from v3) | fiscal autonomy and delivery capacity (the 2×2) |
| Finance (route) | the ten `cl-*/cl-*-fondos` supply reviews (harmonized here) | usable, municipality-eligible funds + access pathway |
| Projects (evidence) | `reviews/cl-ssg/cl-ssg-projects`; CONAF / FPA / GCF awards | calibration, precedent, benchmarks |

The ten supply reviews behind the inventory: `cl-mma`, `cl-minenergia`, `cl-subdere`, `cl-minvu`, `cl-gore`, `cl-corfo`, `cl-conaf`, `cl-mtt`, `cl-indap`, `cl-mop` (grouped as the `chile-finance` collection). Each remains authoritative for its own provenance, licence, parsing and recurrence detail.

## Structure (analysis + methodology record)

```
cl-city-action-fundability/
├── README.md                 (this file)
├── methodology.md            (the shareable overview: how the fundability score works + the v2 matching contract)
├── releases/v1/                     the release implemented in production
│   ├── implementation.md            the production design (tables, score function, API) + As-built summary
│   ├── 01_finance_inventory.ipynb   supply layer: harmonize 10 sources → inventory + coverage
│   ├── 02_fundability_model.ipynb   the four-layer model (autonomy/capacity formulas, the score)
│   ├── extract_inventory.ipynb      reproducible extraction harness (one reusable prompt; refresh source rows)
│   ├── review.md                    release epistemic contract
│   ├── data/
│   │   ├── chile_finance_inventory.csv         99 funds, harmonized (now productionised as finance_opportunity)
│   │   ├── financing_coverage_by_action.csv    102 actions × coverage_level
│   │   └── action_coverage_matrix.csv          102 actions × gap dashboard
│   └── tests/                       post-load expectations for the modelled tables
└── releases/v2/                     research: route-derived action matching, not in production
    ├── 01_opportunity_action_links.ipynb  build, validation and charts
    ├── review.md                    release epistemic contract
    └── data/
        ├── chile_finance_inventory.csv        100 opportunities (99 v1 records + 1 verified local call)
        ├── action_delivery_mode.csv           input: what each of the 102 actions takes to deliver
        ├── action_opportunity_mapping.csv     input: 21 hand-judged rows (16 whole/part, 4 preparation, 1 reviewed-no-match)
        └── finance_opportunity_action.csv     200 links, 180 derived and 20 reviewed
└── releases/v3/                     research: commercially reusable city-profile inputs, not in production
    ├── 01_city_profile_v3.ipynb      join the two reviewed axes and band the archetype
    ├── review.md                     release epistemic contract
    ├── data/
    │   └── city_finance_profile.csv         345 comunas × capacity, autonomy, archetype + provenance
    └── sample/                       the three consultant source files (gitignored)
```

Neither city axis is defined in this folder. Capacity lives in `reviews/oef/cl-municipal-capacity-tier` and derives from INE Censo 2024 under CC BY-SA 4.0. Autonomy lives in `reviews/cl-subdere/cl-subdere-sim-bep` and is recalculated from SUBDERE's public budget-execution workbook, with CC0 applied by Chile's national open-data default. Release v3 consumes both tables unchanged and asserts an exact 345-CUT join.

The exploratory fixtures used to *design* the schema — the SQLite `finance_preview.db`, the `finance_db/` CSVs, the precomputed `fundability_scored.csv`, the preview example JSONs and `build_*` scripts — were removed once the real tables landed (the implementation supersedes them). Refresh of the analysis: re-run `01` after any source release, then `02`.

## Provenance & licence

Authority lives upstream; this product inherits the **most restrictive upstream licence** and re-grants nothing. The **v3 city-profile inputs permit commercial use**: capacity inherits INE's CC BY-SA 4.0 attribution/share-alike conditions, while SIM/BEP autonomy uses CC0 under Chile's government-wide open-data default (the workbook does not print a resource-specific licence). This clears the city layer, not automatically the whole fundability product: finance sources retain their own terms, including CORFO `CC BY-NC-ND`. Check every upstream review before redistributing a combined output.

The v3 release contains no SINIM-derived city data. In the configured database used for verification, Mage run 170 replaced the retired SINIM-backed rows with the OEF v3 release and confirmed that no retired-source rows remained.

## Status

**Implemented in production.** The four-layer model is built end to end in `CityCatalyst/global-api` (modelled tables + the score function + the API) and `cc-mage` (the load pipelines). See `releases/v1/implementation.md` → **As-built** for the authoritative object/pipeline/endpoint list.

- **Tables / function:** `finance_opportunity` (+`_action`), `finance_project` (+`_action`), `city_finance_profile`, and the read-time score `modelled.city_action_financial_feasibility(...)` — Alembic `9f3c1a7b2e10`, `a4f1c9d72b3e`, `b8e2f5a1c9d4`, `c3f9a7e1d2b8`.
- **Pipelines:** `cl_finance_opportunity_to_modelled`, `cl_finance_project_to_modelled`, `cl_city_finance_profile_to_modelled`.
- **Endpoints:** `climate-finance/opportunities`, `.../feasibility`, `.../actions/{action_id}`, `.../projects`.

This folder is now the analysis + methodology record behind that implementation. The principal remaining methodology caveat is the curated `access_tier` that will replace the current "direct" substring heuristic (see `methodology.md` → *Status and what's next*).

**Release v3 remains unpromoted research, but its replacement pipeline has been run successfully in the configured environment.** It replaces both city axes without iterating the release number: capacity comes from `cl-municipal-capacity-tier`, and autonomy comes from `cl-subdere-sim-bep`. Their 345 CUT codes join exactly, with no nulls. Relative to the former city-profile output, four comunas change archetype; Padre Hurtado's large source disagreement and Natales' threshold-edge result still require adjudication. The T4 band (0.10 provisional) and T1 evidence gate also remain open. Mage run 170 loaded 341 locode-resolved v3 rows and atomically removed all retired SINIM-backed database rows. No database schema migration is required. Details in `releases/v3/review.md`.

**Release v2 is research and is not in production.** It rebuilds the action matching so that how specifically a fund matches an action follows from how specific the fund is, which makes 180 of its 200 links derived rather than asserted and shrinks the hand-maintained judgement to 21 rows. Coverage, city eligibility and current availability are three separate gates. Because every opportunity currently fails the availability gate, v2 ships zero displayable links on purpose; v1 remains what the modelled tables and the finance API serve. Its headline finding is that no action requiring municipal capital is without a route, and that 48 of 102 actions are funded in Chile but not for the city. Details in `releases/v2/review.md`; the contract in `methodology.md` → *Action-to-opportunity matching*.

## Parsing notes

Three things break naive ingestion of this folder. All three are properties of the inputs rather than of the analysis, so they bite any consumer of the release data.

- **Join on action id, never action name.** The ClimateView action catalogue carries source-side spelling errors and trailing spaces in `action_name` (for example `"Optmize waste management systems "`). Both are preserved as published in the v2 crosswalk and links, with only the surrounding whitespace stripped, so a name join silently drops rows that an id join keeps.
- **Opportunity ids are derived, not stored upstream.** `source_opportunity_id` is a deterministic slug of the source dataset and programme name (accents stripped, non-alphanumeric runs collapsed to a hyphen). The compile's own `record_id` is a content hash and is not the join key.
- **Inventory `status` is mixed provenance.** It is normalised where the v2 compile reverified a record and is otherwise the seed's original claim carried forward from v1, so it must not be read as a uniformly current status. `verification_status` on the compile is what distinguishes the two.
