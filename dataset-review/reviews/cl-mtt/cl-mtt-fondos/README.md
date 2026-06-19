# Ministerio de Transportes y Telecomunicaciones (Chile) — transport finance for cities (cl-mtt)

The transport-sector funding MTT and its División de Transporte Público Regional (DTPR) offer to renew and decarbonise public and shared transport: the national public-transport subsidy (Fondos de Apoyo Regional, reformed 2024) for fleet renewal and zero-emission buses, plus the vehicle-renewal programmes Renueva tu Micro and Renueva tu Colectivo. This entry adds the **transportation** slice that need `2026-06-cl-finance-opportunities` had entirely missing — transport is a core GPC sector and a major municipal mitigation lever, yet no transport instrument was in the v1 inventory (the gap was named in `dataset-discovery/needs/2026-06-cl-finance-opportunities/gaps.md`, gap 1).

## Canonical sources

No single fund portal — transport finance is split across the ministry, DTPR, and the citizen-services catalogue:

- DTPR (División de Transporte Público Regional): https://dtpr.gob.cl/ — administers the regional public-transport subsidy and the renewal programmes; per-region calls run here or via the SEREMI de Transportes.
- Reform overview (new subsidy law, Aug 2024): https://www.gob.cl/noticias/nueva-ley-subsidio-transporte-publico-buses-electricos-regiones/ and MTT gestión 2022-2026 https://mtt.gob.cl/avances-mtt-2022-2026/.
- ChileAtiende fichas: Renueva tu Micro `fichas/25058`, Renueva tu Colectivo `fichas/43671` — eligibility, documents, process.
- MinEnergía electromobility platform (overlap, charging/vehicle context): https://energia.gob.cl/electromovilidad/estado-y-electromovilidad.

## Why we use it

- Fills the **transportation** GPC sector, absent from v1 — the single biggest sector hole in the inventory.
- Explicit decarbonisation line: the reformed subsidy law earmarks >=50% of regional Fondos de Apoyo Regional to operation + fleet renewal and explicitly incentivises zero-emission buses, charging infrastructure and public bicycles; 1,028 electric buses were awarded for incorporation in 2026-27.
- Maps cleanly to `gpc_sector = transportation` for scoring transport actions.

## License

Public government information (verified 2026-06-16): MTT/DTPR pages and ChileAtiende fichas are ordinary public information under the Ley de Transparencia; ChileAtiende additionally publishes a developer API and its own terms. Less restrictive than the `fondos.gob.cl` aggregator that was rejected for the inventory. Handling: capture and attribute the factual programme data (name, eligible actor, amounts, dates, links); standard public-info treatment.

## Spatial and temporal scope

National, delivered region-by-region. The big subsidy is administered per-GORE (each Gobierno Regional sets its own bases and window), so a given city's access is mediated by its region. Renueva tu Colectivo reajusta cada marzo (treat as annual); Renueva tu Micro runs periodically. Status as captured 2026-06-16.

## Interpretation warnings

- **The city is rarely the applicant.** For all three rows the eligible actor is a transport operator (bus/colectivo) or the GORE administers the funds — not the municipality. This is a textbook broad-capture case: keep the rows, tag `eligible_actor` / `access_pathway = intermediated`, and let scoring (not inclusion) handle that it's not a direct municipal grant.
- **Amounts are largely per-call / per-region.** The national subsidy's per-call amount is set in each GORE's bases (recorded `index`, amount unverified at program level). Only Renueva tu Colectivo states a programme-level figure (~CLP 6.8M special subsidy for electric replacement; ~7.7M and up to ~9M with scrappage cited regionally) — and those are approximate; confirm on ChileAtiende ficha 43671.
- **Climate relevance varies by row.** The subsidy law's zero-emission line and the colectivo EV subsidy are `explicit`; Renueva tu Micro is `climate-adjacent` (renewal toward cleaner vehicles, not exclusively zero-emission).
- **Overlap with MinEnergía.** Electromobility also appears on the MinEnergía platform; cite MTT for the transport-operator subsidies and MinEnergía for charging/vehicle-incentive context — do not double-count if both are ingested.

## Parsing notes

- No single portal to scrape: v1 is **hand-curated** from official programme pages (captured 2026-06-16), one row per programme, `source_url` per row — same pattern as `cl-minenergia`, recorded so a future maintainer doesn't look for a portal that isn't there.
- Per-region calls live on `dtpr.gob.cl/noticias` and SEREMI pages; the live "what's open in region X" status must be re-checked there, not inferred from this snapshot.
- ChileAtiende fichas are server-rendered and have a developer API — a candidate structured source if transport scope is later widened.

## Extraction & refresh

Hand-curated from the source pages below using the OEF extraction prompt (see `reviews/oef/cl-city-action-fundability/releases/v1/extract_inventory.ipynb`, or the per-source prompt in `reviews/cl-minenergia/cl-minenergia-fondos/README.md`). To refresh: re-read each `source_url`, re-run the prompt, replace rows in `data/cl_mtt_programs_v1.csv`, spot-check against the page, and update `status_as_of`.

Source pages (captured 2026-06-16): gob.cl subsidy-law note, dtpr.gob.cl, ChileAtiende fichas 25058 and 43671, mtt.gob.cl gestión 2022-2026.

## Current approved release

Not yet promoted (awaiting sign-off). First release **v1** in `releases/v1/`: `data/cl_mtt_programs_v1.csv` (3 programmes) + `review.md`. Evidence tags: provenance/scope **verified** (live search 2026-06-16); the reformed-subsidy zero-emission earmark and e-bus awards **verified**; per-call/per-region amounts **unverified** (set in GORE bases); Renueva tu Colectivo EV figure **partly verified** (approximate, region-dependent); license **verified** (public government info).
