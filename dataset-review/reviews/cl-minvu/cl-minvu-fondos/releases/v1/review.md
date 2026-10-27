# Review — cl-minvu-fondos, release v1

## Scope and status

Research release (not production-approved). MINVU's climate-relevant urban / green-space programmes for need `2026-06-cl-finance-opportunities`: Programa Concursable de Espacios Públicos, Parques Urbanos, Pavimentación Participativa, Programa de Recuperación de Barrios (Quiero Mi Barrio). Hand-curated from MINVU "Ciudad" pages, captured 2026-06-08 (see "Extraction & refresh" in the README). Output: `data/cl_minvu_programs_v1.csv` (4 rows). Dataset-level facts in the README one level up.

## What this data supports

- "A Chilean municipality can fund green public space and rainwater works through MINVU's Programa Concursable de Espacios Públicos (Regular ≤ UF 30,000; Especial ≤ UF 6,000), applying through the regional SEREMI." — supported (amounts read from the page; `eligible_actor=municipality`).
- "Espacios Públicos has two annual windows — a Regular call around April and a Special call around September." — supported (`recurrence=annual`).
- "Urban parks delivery (construction + conservation) targets green-area-deficit, vulnerable areas as a climate-resilience measure." — supported as relevance; construction is SEREMI-prioritised, not an open competition.

## What this data does not support

- "Parques Urbanos construction is an open competitive fund a city applies to and wins." — NO. Construction is SEREMI-prioritised by deficit/population/vulnerability; only the conservation line is competitive.
- "The current Espacios Públicos call is 2023–2024." — NO; that's page lag. The cadence is annual; confirm the current Resolución Exenta with the SEREMI.
- "Espacios Públicos awards CLP N." — figures are in **UF** and bundle design+execution; convert at use, don't store a fixed peso amount.
- "All MINVU city programmes are climate funds." — NO. Espacios Públicos / Parques Urbanos are explicit (green/rainwater/heat); Pavimentación Participativa and Quiero Mi Barrio are adjacent (mobility / neighbourhood). Tag by funded works.

## Using it downstream

- For fundability scoring these are the **adaptation / urban-green** matches (urban heat, stormwater, green space) — sector-specific enough (Espacios Públicos, Parques Urbanos) to support "Strong" matches for the right actions, unlike the broad SUBDERE funds.
- Timing matters: Espacios Públicos is annual (April/September), so for a closed-now action it's "reliably annual" rather than "open" — combine `status` with `recurrence` as in `cl-mma`.
- Pairs with `cl-subdere` (broad municipal infra), `cl-mma` (environment), `cl-minenergia` (energy) for full municipal coverage.

## Notes on non-obvious fields

- `amount_note` holds UF figures for Espacios Públicos (UF, not CLP; design+execution bundled); other rows have no programme-level amount.
- `recurrence=annual` (Espacios Públicos, Pavimentación) vs `ongoing` (Parques construction, Quiero Mi Barrio) — read alongside `status`.
- `detail_level=index` — programme identified; per-call specifics pending the detail page / current Resolución Exenta.
- `climate_relevance` distinguishes explicit (green/rainwater) from adjacent (mobility/neighbourhood).

## Traceability

Sources (captured 2026-06-08): minvu.gob.cl "Ciudad" pages — Espacios Públicos (`/beneficio/ciudad/programa-concursable-de-espacios-publicos/`), Parques Urbanos, Pavimentación Participativa, Recuperación de Barrios; governing norm DS 312/2016. Extraction prompt + refresh steps are in the README ("Extraction & refresh"); the committed `data/` CSV is the snapshot (the same prompt also runs in the OEF harness). Per-call detail (dates, amounts, eligibility) lives in each SEREMI Resolución Exenta.
