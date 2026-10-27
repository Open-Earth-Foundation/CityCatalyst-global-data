# Review — cl-subdere-fondos, release v1

## Scope and status

Research release (not production-approved). SUBDERE's climate-relevant municipal investment programmes for need `2026-06-cl-finance-opportunities`: PMU, PMB, Prevención y Mitigación de Riesgos (PMR), Fondo de Recuperación de Ciudades (FRC). Hand-curated from SUBDERE programme pages, captured 2026-06-08 (see "Extraction & refresh" in the README). Output: `data/cl_subdere_programs_v1.csv` (4 rows). Dataset-level facts (sources, license, parsing) in the README one level up.

## What this data supports

- "Chilean municipalities can fund local infrastructure continuously through SUBDERE's PMU and PMB, applying any time via subdereenlinea.gov.cl." — supported; both `recurrence=ongoing (rolling)`, `eligible_actor=municipality`.
- "PMB can fund sanitation, solid-waste, waste-valorization and electrification projects." — supported from the SUBDERE/DIPRES descriptions (`gpc_sectors = water, waste, stationary_energy`).
- "SUBDERE municipal investment is large-scale (≈CLP 222bn across 2,811 projects in 2022, PMU+PMB+others)." — supported as context (not per-fund).
- "A municipality can pursue climate-risk works through the Programa de Prevención y Mitigación de Riesgos." — supported as adaptation-relevant (detail/amount pending; `detail_level=index`).

## What this data does not support

- "PMU/PMB being open means money is available on request." — NO. Applications are continuous but funded subject to the annual budget; `status=open` means the window is open, not that an award is assured.
- "These are climate funds." — mostly NO. PMU and FRC are general municipal infrastructure (`climate_relevance=climate-adjacent`); only PMB (waste/water/energy) and PMR (risk) have direct hooks. Tag the action by the funded works, not the programme.
- "PMU/PMB are good signals of action-specific fundability." — use with care: they are `specificity=broad` and will match almost any action. They must be down-weighted in scoring or they inflate everything (the documented SSG failure mode).
- "Programme X awards CLP N." — unsupported; amounts are per-project and budget-dependent, not stated at programme level (`amount_note`).

## Using it downstream

- In the fundability score, treat PMU/PMB as broad/always-on context: they raise baseline fundability for almost any municipal action, so cap or down-weight their contribution; reserve "Strong" matches for sector-specific funds (e.g. MMA FPR for waste, Min. Energía for energy).
- For the city-facing reference these are high-value (municipality applies directly, usually open) — surface them, but label them general-purpose.
- Pairs with `cl-mma` (environment/waste), `cl-minenergia` (energy), `cl-minvu` (urban/green) for full municipal coverage.
- `detail_level=index` rows (PMR, FRC) are leads — confirm current calls/amounts on SUBDERE before presenting.

## Notes on non-obvious fields

- `specificity=broad` — flag that the fund matches across many sectors; a scoring control, not a quality judgement.
- `recurrence=ongoing (rolling)` — continuous intake, not an annual cycle; different from MMA's annual concursos and from MINVU's April/September windows.
- `amount_note` carries the reason `amount_clp`-type figures are absent (per-project, budget-dependent).
- `detail_level=index` — programme identified; specifics pending a successful SUBDERE fetch (site was slow at capture).

## Traceability

Sources (captured 2026-06-08): subdere.gov.cl programme pages (PMU, PMB), DIPRES/ACHM PMB documentation, SUBDERE press (2022 investment figures); applications via subdereenlinea.gov.cl. Extraction prompt + refresh steps are in the README ("Extraction & refresh"); the committed `data/` CSV is the snapshot (the same prompt also runs in the OEF harness). Access caveat: subdere.gov.cl timed out during capture — PMR/FRC rows are index-level pending re-fetch.
