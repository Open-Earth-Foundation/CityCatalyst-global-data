# Review — oef/cl-finance-inventory, release v1

## Scope and status

Research / exploratory OEF release (not production-approved, not in a pipeline). A **derived** product: `data/chile_finance_inventory.csv` unions the six vetted Chile climate-finance source reviews (cl-mma, cl-minenergia, cl-subdere, cl-minvu, cl-gore, cl-corfo — 78 fund rows) into one common schema, plus an action **financing-availability (coverage)** indicator (`data/financing_coverage_by_action.csv`) over the ClimateView `current_actions` set, and a programmatic extraction harness. Built by the notebooks in this release; methodology in `../methodology.md`. The per-source reviews remain authoritative for provenance, licence, and per-fund caveats.

## What this data supports

- "Across six Chilean public + firm-facing sources, there are ~78 climate-relevant funding channels spanning environment/waste, energy, municipal infrastructure, urban/green, regional FNDR, and firm debt/blended." — supported by the harmonized inventory.
- "For a given climate action, whether a *dedicated* (sector-specific), currently-usable, city-accessible funding channel exists." — supported as a **coverage** label (sector-specific / broad-only / none).
- "Which sectors have only broad/general-purpose coverage (a gap) — e.g. transport, industry." — supported as a gap map.
- "A reproducible way to re-derive the inventory from source pages." — supported by `extract_inventory.ipynb` (one reusable prompt) + `harmonize.ipynb`.

## What this data does not support

- "This action is fundable / likely to secure finance." — NO. This is **availability/coverage**, not fundability (methodology §0); it reflects what we have catalogued (availability bias), not award probability. Five of five facets of real fundability (supply, access, adequacy, competitiveness, capacity) — only supply + partial access are measured.
- "Action ranking within a sector." — NO. Coverage is essentially sector-determined; within-sector order is not meaningful (methodology §5).
- "A complete picture of Chilean climate finance." — NO. National public + CORFO core only; INDAP/agriculture, Min. Transportes, SERVIU, the multilateral tier and private/blended beyond CORFO are not yet in (see the SSG gap analysis).
- "Authoritative licence/amounts." — NO; defer to each source review. Amounts are sparse and mixed-unit (CLP/UF/US$/%); do not rank on money.
- "`extracted_inventory.csv` is a live extract." — NO; it is the offline-stub demo output proving the harness. A live run needs a real `FETCH`/`MODEL_CALL` (+ JS fetch for CORFO/fondos.gob.cl).

## Using it downstream

- Treat as a **city-facing where-to-look map + gap map**, not a score. Read `coverage_level` with the availability-bias caveat.
- For true "what gets funded in practice", the deferred next step is a **revealed** signal from award/adjudication history (methodology §0).
- The decisive interpretation rule (from adding CORFO): coverage must be read against **who implements the action** — industry's gap is an actor gap, not a supply gap. Action-actor inference is the real next improvement, not more sources.
- Rebuild order after any source change: `harmonize.ipynb` → `chile_financing_coverage.ipynb` (and `chile_finance_explore.ipynb`).

## Notes on non-obvious fields

- `specificity` (sector-specific | broad) — broad funds are capped at "Moderate" in the coverage classifier; a control, not a quality judgement.
- `climate_relevance_norm` (explicit | adjacent | indirect) — normalized from each source's free-text relevance.
- `coverage_level` (sector-specific | broad-only | none) — the headline label; `none` is a true gap (currently empty because broad municipal funds cover almost everything).
- `detail_level` (detailed | index) — index rows are leads pending live-call confirmation.

## Traceability

Inputs: the six `../../cl-*/.../releases/v1/data/*.csv` source CSVs + `../../climateview/.../current_actions.csv`. Derivation + validation: the four notebooks in this release (each restart-and-run-all passes). Source provenance and licences: the per-source review READMEs (authoritative). Methodology and decision log: `../methodology.md`.
