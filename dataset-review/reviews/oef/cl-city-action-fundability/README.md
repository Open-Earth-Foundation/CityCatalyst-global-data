# OEF — Chile city-action fundability (cl-city-action-fundability)

The consolidated OEF product for *how a Chilean comuna can pay for a climate action*. It brings the supply side (a harmonized finance inventory + a financing-availability indicator) and the model side (a four-layer fundability model + a traceable `finance_db` fixture) into one folder. **It supersedes and replaces the former `cl-finance-inventory` and `cl-action-fundability` reviews** — everything they did lives here, refreshed.

It is an OEF model and curation, not a new external source: it unions and scores already-reviewed datasets and re-grants nothing. It is the data side of the financial-feasibility workstream for MEED+ HIAP, feeding that tool's Feasibility pillar.

## What it produces

1. **A finance inventory** — the ten vetted Chile climate-finance supply reviews harmonized into one fund table (99 funds), plus an action **financing-availability (coverage)** label. This is the FINANCE/supply layer.
2. **A fundability model** — combines four layers (action catalog, SINIM/Censo municipal capacity, the finance inventory, the projects pipeline) into a per `(action × comuna)` route/effort bucket + a 0–1 `financial_feasibility` score + the funds that fit. Not a funding probability, not a comuna ranking.
3. **`finance_db`** — a traceable "database" of CSVs (funder · opportunity · project · action + a `project_funding` link) populated from the repo's real data, so the model's use cases can be tested and the real scale (and the three access **routes**) is visible. See `releases/v1/finance_db/README.md`.

## Inputs (authoritative upstream, not duplicated here)

| Layer | Source review(s) | Role |
| --- | --- | --- |
| Action (what) | `reviews/cl-ssg/cl-ssg-projects` (actions catalog, 102) | capital intensity; formulation demand; self-financeability |
| City (who) | `reviews/cl-subdere/cl-subdere-sinim` + `reviews/cl-ine/cl-ine-censo` | fiscal autonomy and delivery capacity (the 2×2) |
| Finance (route) | the ten `cl-*/cl-*-fondos` supply reviews (harmonized here) | usable, municipality-eligible funds + access pathway |
| Projects (evidence) | `reviews/cl-ssg/cl-ssg-projects`; CONAF / FPA / GCF awards | calibration, precedent, benchmarks |

The ten supply reviews behind the inventory: `cl-mma`, `cl-minenergia`, `cl-subdere`, `cl-minvu`, `cl-gore`, `cl-corfo`, `cl-conaf`, `cl-mtt`, `cl-indap`, `cl-mop` (grouped as the `chile-finance` collection). Each remains authoritative for its own provenance, licence, parsing and recurrence detail.

## Structure (the lean release)

```
cl-city-action-fundability/
├── README.md                 (this file)
├── methodology.md            (the hub: Part A supply & coverage · Part B fundability model)
└── releases/v1/
    ├── 01_finance_inventory.ipynb   supply layer: harmonize 10 sources → inventory + coverage
    ├── 02_fundability_model.ipynb   the four-layer model + the coverage matrix
    ├── extract_inventory.ipynb      reproducible extraction harness (one reusable prompt; refresh source rows)
    ├── build_finance_db.py          regenerates the finance_db fixture deterministically
    ├── review.md                    release epistemic contract
    ├── data/
    │   ├── chile_finance_inventory.csv         99 funds, harmonized
    │   ├── financing_coverage_by_action.csv    102 actions × coverage_level
    │   ├── fundability_scored.csv              345 comunas × 102 actions
    │   └── action_coverage_matrix.csv          102 actions × gap dashboard
    └── finance_db/                  the traceable fixture (CSVs + queries + walkthrough + its own README)
```

Refresh: re-run `01` after any source release (sources → inventory + coverage), then `02` (model + matrix), then `build_finance_db.py` (fixture). `extract_inventory.ipynb` is the reproducible extraction harness the source reviews point at — one reusable prompt to re-derive fund rows from the source pages (live `FETCH`/`MODEL_CALL`; ships an offline stub).

## Provenance & licence

Authority lives upstream; this product inherits the **most restrictive upstream licence** and re-grants nothing. The binding constraint is **SINIM** (non-commercial + attribution clear; commercial unresolved pending SUBDERE clearance). Finance sources add per-source terms (e.g. CORFO `CC BY-NC-ND`). Treat outputs as non-commercial + attribution until the SINIM clearance lands, and check each input review before redistributing.

## Status

Research / exploratory — not production-approved, not in a Mage pipeline. The four-layer logic, route buckets and score are implemented and validated on a full national run (345 comunas × 102 actions). Promotion prerequisites: the SINIM commercial-licence clearance, a settled capacity-cut definition, and the curated `access_tier` that replaces the current "direct" substring heuristic (see `methodology.md` Part B §5). Promotion path: this OEF layer → Mage pipeline → `catalog` / `knowledge-base` once the methodology stabilises.
