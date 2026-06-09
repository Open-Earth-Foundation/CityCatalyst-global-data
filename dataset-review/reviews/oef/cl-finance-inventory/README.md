# OEF — Chile climate-finance inventory (exploratory)

An OEF working workspace that unions the six vetted Chile climate-finance source reviews into a single inventory and develops an action **financing-availability (coverage)** indicator on top of it — explicitly a *coverage* signal, not fundability (see `methodology.md` §0). Deliberately kept **pre-Mage**: this is for exploratory analysis before anything is productionised.

## Structure

Follows the standard review layout — dataset root holds `README.md` + the hub `methodology.md`; artefacts live under `releases/<version>/`:

```
cl-finance-inventory/
├── README.md            (this file)
├── methodology.md       (working hub methodology — schema + coverage indicator design)
└── releases/v1/
    ├── harmonize.ipynb              unions the six source CSVs → data/chile_finance_inventory.csv
    ├── extract_inventory.ipynb      programmatic extraction harness (one reusable prompt)
    ├── chile_finance_explore.ipynb  supply-side profiling
    ├── chile_financing_coverage.ipynb  action coverage_level classifier
    ├── review.md                    release epistemic contract
    └── data/
        ├── chile_finance_inventory.csv      harmonized inventory (78 rows)
        └── financing_coverage_by_action.csv 102 actions × coverage_level
```

`extract_inventory.ipynb` writes `data/extracted_inventory.csv` **only on a live run** (real `FETCH` + `MODEL_CALL`); in offline-demo mode it prints a DEMO warning and writes nothing, so it never disagrees with the curated inventory.

What each piece does:

- `releases/v1/harmonize.ipynb` — reads the six source-review CSVs and writes `data/chile_finance_inventory.csv` (78 rows: cl-mma 55, cl-minenergia 6, cl-subdere 4, cl-minvu 4, cl-gore 4, cl-corfo 5). Re-run after any source release.
- `releases/v1/extract_inventory.ipynb` — **programmatic extraction harness**: fetches the reviewed source pages and extracts rows with one reusable prompt (`EXTRACTION_PROMPT`) → `data/extracted_inventory.csv`. The reproducible replacement for hand-curation — plug in a live `FETCH`/`MODEL_CALL`; ships a deterministic offline stub. MMA uses the deterministic parser; messy sources flow through the prompt; CORFO/fondos.gob.cl need a JS fetch.
- `releases/v1/chile_finance_explore.ipynb` — supply-side profiling (sector, actor, recurrence, specificity, usability).
- `releases/v1/chile_financing_coverage.ipynb` — classifies the ClimateView `current_actions` set into a `coverage_level` (sector-specific / broad-only / none) → `data/financing_coverage_by_action.csv`. **Coverage, not fundability** (methodology §0): a *where-to-look* + gap map reflecting what we have catalogued (availability bias), not the probability of securing finance.
- `methodology.md` (dataset root) — the hub working methodology.

## Inputs (authoritative; not duplicated here)

The per-source reviews keep provenance, license, parsing, and recurrence detail:

- `dataset-review/reviews/cl-mma/cl-mma-fondos`
- `dataset-review/reviews/cl-minenergia/cl-minenergia-fondos`
- `dataset-review/reviews/cl-subdere/cl-subdere-fondos`
- `dataset-review/reviews/cl-minvu/cl-minvu-fondos`
- `dataset-review/reviews/cl-gore/cl-gore-fndr` (regional tier)
- `dataset-review/reviews/cl-corfo/cl-corfo-finance` (firm-facing debt/blended)

These six are grouped logically as the `chile-finance` collection (`dataset-review/collections/collection.yaml`).

## Scope and status

Research / exploratory — not production-approved, not in a pipeline. The inventory is a derived convenience table; for any licensing or caveat question, defer to the source review. Refresh: re-run `releases/v1/harmonize.ipynb` (sources → inventory), then the explore / coverage notebooks.

## Status & roadmap (where this stands)

**Usable now — a city-facing funding reference.** The inventory (78 verified channels across six institutions) carries the fields an app would surface per opportunity: name, funder, eligible actor, instrument type, amount note, status, recurrence, GPC sector, and a live `source_url`. A city can browse "what funding exists for this kind of action", and the coverage indicator can power a "which actions have a funding route" view. This part is real and deliverable.

**What it is NOT yet — a fundability metric.** What we built is honestly a *financing-availability (coverage)* signal — does a sector-appropriate, usable, city-accessible channel exist — not *fundability* (does this action tend to secure finance). It carries an availability bias (it reflects what we have catalogued; unreviewed sectors look like gaps). See `methodology.md` §0.

**Before surfacing in an app, mind three things:**
- **Research-grade.** Not production-approved, not in a Mage pipeline. Promote first.
- **Licensing per source.** Ranges from "public info, no explicit reuse grant" (ministries) to CORFO `CC BY-NC-ND 3.0` and AgenciaSE all-rights-reserved. As an attributed directory of public facts this is likely fine, but confirm with legal before redistributing in a product. Authority lives in each source review.
- **Snapshot + partial scope.** Point-in-time (2026-06-08), refreshable via each review's "Extraction & refresh" prompt. Strong core, not complete national scope — known gaps: agriculture (INDAP), transport (Min. Transportes), multilateral and private/blended beyond CORFO.

**Roadmap to a real fundability metric** (in priority order):
1. **Action-actor inference** — read coverage against *who implements the action* (CORFO showed industry's "gap" is an actor gap, not a supply gap); this is the biggest lever and gets action-level resolution.
2. **Revealed fundability** — mine award/adjudication history (what actually got funded, how often, at what size); we already touched this in the recurrence work.
3. Then the remaining facets: **adequacy** (amount vs project cost), **competitiveness** (award odds), **capacity** (ability to apply).

In one line: the **supply side is done and useful; the demand/outcome side that turns "available" into "fundable" is the remaining work.**

## How it fits the repo flow

discover (`dataset-discovery/needs/2026-06-cl-finance-opportunities`) → review (the six `cl-*` source datasets) → **this OEF exploratory layer** → (later) Mage pipeline + `catalog`/`knowledge-base` promotion once the methodology stabilises.
