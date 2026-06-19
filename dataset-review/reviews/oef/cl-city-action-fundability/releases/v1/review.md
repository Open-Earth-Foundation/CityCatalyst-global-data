# Review — oef/cl-city-action-fundability, release v1

## Scope and status

Research / exploratory OEF release (not production-approved, not in a pipeline). A **derived** product consolidating the former `cl-finance-inventory` and `cl-action-fundability` releases into one. It carries two linked layers — a harmonized **finance inventory** + **coverage** indicator (Part A), and a four-layer **fundability model** + the traceable **`finance_db`** fixture (Part B) — built by the notebooks here; methodology in `../methodology.md`. The per-source reviews remain authoritative for provenance, licence and per-fund caveats.

Outputs: `data/chile_finance_inventory.csv` (99 funds, 10 sources), `data/financing_coverage_by_action.csv` (102 actions × coverage_level), `data/fundability_scored.csv` (345 comunas × 102 actions), `data/action_coverage_matrix.csv` (102-action gap dashboard), and `finance_db/*.csv` (the funder/opportunity/project/action + funding-link fixture).

## What this release supports

- "Across ten Chilean public + firm-facing sources, there are 99 climate-relevant funding channels." — the harmonized inventory.
- "For a climate action, whether a *dedicated*, currently-usable, city-accessible channel exists." — a **coverage** label (sector-specific / broad-only / none).
- "For a comuna and an action, how hard it is to fund/deliver and by what route, with named funds and precedent." — the fundability model's route bucket + `financial_feasibility` score + annotation.
- "The real scale and the three access routes (competitive / public-investment / intermediated-multilateral) of the repo's finance data, end to end and traceable to source." — the `finance_db` fixture.

## What this release does NOT support

- "This action is fundable / likely to secure finance." — NO. Coverage is **availability**, not award probability (Part A §A0); the model is a **categorisation**, not a funding probability (Part B §B0). Of the five facets of real fundability, only supply + partial access + capacity are measured.
- "A ranking of comunas." — NO. The model orders actions *within* a comuna; cross-comuna difficulty is out of scope (§B0).
- "Action ranking within a sector (coverage)." — NO. Coverage is essentially sector-determined (§A3).
- "A complete picture of Chilean climate finance." — NO. International funders (GCF/IDB/World Bank/UNDP-SGP) appear in `finance_db` as intermediated, `city_can_apply = no`; adequacy (amounts) and award odds are not built.
- "Authoritative licence/amounts." — NO; defer to each source review. Amounts are sparse and mixed-unit; do not rank on money.

## Using it downstream

- Treat coverage as a **where-to-look + gap map**, not a score; read `coverage_level` with the availability-bias caveat.
- Use the model output as an **annotation** on ranked actions (bucket + named funds + precedent), feeding HIAP Feasibility as a third leg — never Impact or Alignment.
- The decisive interpretation rule (from CORFO + operator-facing transport/agriculture funds): coverage must be read against **who implements the action** — the industry/transport gap is an actor gap, not a supply gap.
- Rebuild order after any source change: `01_finance_inventory.ipynb` → `02_fundability_model.ipynb` → `build_finance_db.py`. Each notebook passes restart-and-run-all; the build script is deterministic.

## Notes on non-obvious fields

- `specificity` (sector-specific | broad) — broad funds are capped at "Moderate" in the coverage classifier; a control, not a quality judgement.
- `coverage_level` (sector-specific | broad-only | none) — the headline label; `none` is a true gap (currently empty because broad municipal funds cover almost everything).
- `route` / `access_route` / `city_can_apply` (in `finance_db`) — make the access path explicit so the "a city cannot apply directly" signal is never lost (see `finance_db/README.md`).
- `match_confidence` (on `finance_db/actions.csv`) — quote a benchmark only where `strong` (21 actions).
- `fund_access` (in the scored output) — a weak substring heuristic pending the curated `access_tier` (§B5).

## Traceability

Inputs: the ten `../../cl-*/.../releases/v1/data/*.csv` supply CSVs, `../../climateview/.../current_actions.csv`, the SINIM/Censo/SSG layers, and the CONAF/FPA/GCF award reviews. Derivation + validation: the two release notebooks + `build_finance_db.py` (each restart-and-run-all / deterministic rebuild passes). Source provenance and licences: the per-source review READMEs (authoritative). Methodology and decision log: `../methodology.md`.
