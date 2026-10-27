# Review — oef/cl-city-action-fundability, release v1

## Scope and status

**Implemented** OEF release. A **derived** product consolidating the former `cl-finance-inventory` and `cl-action-fundability` releases into one. It carries two linked layers — a harmonized **finance inventory** + **coverage** indicator (Part A) and a four-layer **fundability model** (Part B) — built by the notebooks here; methodology in `../methodology.md`. The model is now in production in `CityCatalyst/global-api` (modelled tables + the `city_action_financial_feasibility` score function + the `climate-finance` API) and `cc-mage` (load pipelines); see `implementation.md` → As-built. The per-source reviews remain authoritative for provenance, licence and per-fund caveats.

Outputs (analysis record): `data/chile_finance_inventory.csv` (99 funds, 10 sources — now `modelled.finance_opportunity`), `data/financing_coverage_by_action.csv` (102 actions × coverage_level), `data/action_coverage_matrix.csv` (102-action gap dashboard), and `tests/expectations_*.yaml` (post-load checks for the modelled tables). The prototyping fixtures (`finance_db/*.csv`, `fundability_scored.csv`, the SQLite preview) were removed once the real tables landed.

## What this release supports

- "Across ten Chilean public + firm-facing sources, there are 99 climate-relevant funding channels." — the harmonized inventory.
- "For a climate action, whether a *dedicated*, currently-usable, city-accessible channel exists." — a **coverage** label (sector-specific / broad-only / none).
- "For a comuna and an action, how hard it is to fund/deliver and by what route, with named funds and precedent." — the fundability model's route bucket + `financial_feasibility` score + annotation.
- "The real scale and the three access routes (competitive / public-investment / intermediated-multilateral) of the repo's finance data, end to end and traceable to source." — the modelled `finance_opportunity` / `finance_project` tables.

## What this release does NOT support

- "This action is fundable / likely to secure finance." — NO. Coverage is **availability**, not award probability; the model is a **categorisation**, not a funding probability. Of the five facets of real fundability, only supply + partial access + capacity are measured.
- "A ranking of comunas." — NO. The model orders actions *within* a comuna; cross-comuna difficulty is out of scope.
- "Action ranking within a sector (coverage)." — NO. Coverage is essentially sector-determined.
- "A complete picture of Chilean climate finance." — NO. International funders (GCF/IDB/World Bank/UNDP-SGP) appear in the modelled tables as intermediated (`city_application` excludes `direct`); adequacy (amounts) and award odds are not built.
- "Authoritative licence/amounts." — NO; defer to each source review. Amounts are sparse and mixed-unit; do not rank on money.

## Using it downstream

- Treat coverage as a **where-to-look + gap map**, not a score; read `coverage_level` with the availability-bias caveat.
- Use the model output as an **annotation** on ranked actions (bucket + named funds + precedent), feeding HIAP Feasibility as a third leg — never Impact or Alignment.
- The decisive interpretation rule (from CORFO + operator-facing transport/agriculture funds): coverage must be read against **who implements the action** — the industry/transport gap is an actor gap, not a supply gap.
- Rebuild order (analysis) after any source change: `01_finance_inventory.ipynb` → `02_fundability_model.ipynb`; each passes restart-and-run-all. Production refresh is the `cc-mage` pipelines (see the As-built summary), not these notebooks.

## Notes on non-obvious fields

- `specificity` (sector-specific | broad) — broad funds are capped at "Moderate" in the coverage classifier; a control, not a quality judgement.
- `coverage_level` (sector-specific | broad-only | none) — the headline label; `none` is a true gap (currently empty because broad municipal funds cover almost everything).
- `funding_channel` / `access_tier` / `city_application` (on `modelled.finance_opportunity`) — make the access path explicit so the "a city cannot apply directly" signal is never lost.
- `confidence` (on `modelled.finance_project_action`) — quote a benchmark only where `strong`.
- `fund_access` (in the scored output) — a weak substring heuristic pending the curated `access_tier` (see `methodology.md` → *Status and what's next*).

## Traceability

Inputs: the ten `../../cl-*/.../releases/v1/data/*.csv` supply CSVs, `../../climateview/.../current_actions.csv`, the SINIM/Censo/SSG layers, and the CONAF/FPA/GCF award reviews. Derivation + validation: the two release notebooks (each restart-and-run-all passes), and the post-load `tests/expectations_*.yaml` against the modelled tables. Source provenance and licences: the per-source review READMEs (authoritative). Methodology and decision log: `../methodology.md`.
