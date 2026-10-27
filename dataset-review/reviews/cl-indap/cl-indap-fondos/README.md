# Instituto de Desarrollo Agropecuario (Chile) — INDAP fomento programs (cl-indap)

INDAP (the rural-development agency of MINAGRI) runs the standing instruments through which Chilean smallholder and family farming is financed: technical-advisory and investment programs (PRODESAL, PDTI, SAT, Alianzas Productivas, PDI, Riego), the climate-explicit Transición a la Agricultura Sostenible (TAS), and short/long-term credit lines. This entry adds the **AFOLU agricultural-finance** slice the inventory was missing — no INDAP/MINAGRI line existed despite AFOLU being a core GPC sector, and INDAP was the single largest cluster of recurring opportunities in the legacy `cl-ssg/cl-ssg-finance` snapshot (34 rows). **This review sources from INDAP's own program pages, not from that snapshot** — the SSG CSV is a discovery signal only (every INDAP row in it has `source_url = "No especificado"`).

This is a **started review**: Step 1 (provenance/access/license) and Step 3 (recurrence screen) are verified against primary sources (live search 2026-06-18); the extraction notebook and `data/` release are not yet built (see Status).

## Canonical sources

INDAP publishes each instrument as a permanent "ficha" under its services platform, and runs the recurring competitive layer through a dedicated Concursos section. These pages — not the SSG CSV — are the authoritative origin.

- Services platform index (one ficha per program): https://www.indap.gob.cl/plataforma-de-servicios
- Concursos de Programas de Fomento (the recurring competitive layer): https://www.indap.gob.cl/concursos and https://www.indap.gob.cl/concursos/todos-los-concursos
- Per-program fichas (verified live):
  - TAS — Transición a la Agricultura Sostenible: https://www.indap.gob.cl/tas and https://www.indap.gob.cl/plataforma-de-servicios/transicion-la-agricultura-sostenible-tas
  - PRODESAL — Programa de Desarrollo Local: https://www.indap.gob.cl/plataforma-de-servicios/programa-de-desarrollo-local-prodesal
  - PDTI — Programa de Desarrollo Territorial Indígena (convenio INDAP–CONADI): https://www.indap.gob.cl/plataforma-de-servicios/programa-de-desarrollo-territorial-indigena-indap-conadi-pdti
  - PAP — Programa de Alianzas Productivas: https://www.indap.gob.cl/plataforma-de-servicios/programa-de-alianzas-productivas-pap
  - PDI — Programa Desarrollo de Inversiones: https://www.indap.gob.cl/plataforma-de-servicios/programa-desarrollo-de-inversiones-pdi
  - SAT, Riego (intrapredial/asociativo), SIRSD-S, Bono Legal de Aguas, Créditos: further fichas under the same `/plataforma-de-servicios/` path and enumerated in the Concursos listing.
- Cross-reference fichas (eligibility/dates in a second-source structured form): ChileAtiende, e.g. TAS https://www.chileatiende.gob.cl/fichas/118433 and PDTI https://www.chileatiende.gob.cl/fichas/1720
- Authoritative rules/amounts per cycle live in each program's **Bases** (Resolución Exenta / Norma Técnica), e.g. the PRODESAL Norma Técnica resolution on `indap.gob.cl/sites/...`.

## Why we use it

This dataset fills the **AFOLU / agriculture** finance gap. INDAP is the principal national channel for smallholder and rural-community climate-relevant investment (irrigation, soil, sustainable-production transition), and it was absent from the current inventory.

The legacy snapshot identified this as the highest-volume recurring cluster: 34 of its 43 recurring rows were INDAP programs. This review has the largest expected payoff per dataset reviewed.

The city relevance is strong through two pathways: INDAP is a general **enabler** for smallholder finance, and for PRODESAL and PDTI specifically, the city has a **municipal-delivery** role. PRODESAL and PDTI are executed *by municipalities* under convenio, so the city is an active implementer, not just a referrer.

## License

Public government information (verified 2026-06-18). INDAP (`indap.gob.cl`) is a public service administering public funds under MINAGRI; program facts (name, eligible actor, instrument, amounts, dates, financiable activities, links) are public information under the **Ley de Transparencia (Ley 20.285)**, and each cycle's rules are **Resoluciones Exentas** — official administrative acts, inherently public. No restrictive aggregator terms apply (unlike `fondos.gob.cl`). Standard public-info treatment: capture, attribute to INDAP, obtain legal confirmation before large-scale redistribution inside a product; do not label "open licence" downstream.

## Spatial and temporal scope

National (all regions), delivered regionally and at the comuna level through INDAP area offices and municipal convenios. The fomento programs are **standing** (permanent instruments with an annual budget and an annual Concursos de Fomento round); TAS runs in **two-year cycles** with annual postulation windows (second cycle opened 13–26 Oct 2025). Status of any given call is therefore time-sensitive and must be captured with an as-of date per release.

## Recurrence classification (the field the inventory needs)

Per the requirement to distinguish what is *expected to recur*, each program carries a `recurrence` value:

| Program | Instrument | `recurrence` | Climate relevance | Evidence |
|---|---|---|---|---|
| Transición a la Agricultura Sostenible (TAS) | grant + TA | **cycle-based** (2-yr cycles, annual window) | explicit | 2nd cycle opened Oct 2025; "resiliencia frente al cambio climático" in objective |
| Riego (intrapredial / asociativo) | grant | **standing** (annual) | explicit | Permanent ficha; in annual Concursos de Fomento |
| SIRSD-S (recuperación de suelos) | grant | **standing** (annual) | explicit | Soil-conservation incentive, annual concurso |
| PRODESAL | grant + TA | **standing** (permanent) | adjacent | Permanent municipal-delivered extension program |
| PDTI (convenio INDAP–CONADI) | grant + TA | **standing** (permanent) | adjacent | Permanent municipal-delivered program |
| SAT (Servicios de Asesoría Técnica) | TA | **standing** (annual) | adjacent | Permanent ficha; annual concurso |
| Alianzas Productivas (PAP) | grant + TA | **standing** (annual) | indirect | Permanent ficha; annual concurso |
| Programa Desarrollo de Inversiones (PDI) | grant | **standing** (annual) | indirect | Permanent ficha; annual concurso |
| Asesoría Producción Sustentable de Cultivos | TA | **standing** | adjacent | Sub-line of services platform |
| Créditos corto / largo plazo | loan | **standing** (rolling) | indirect | Permanent credit lines |

Tag every captured row with this `recurrence` value; do not collapse to a flat "recurring". TAS is the one to watch — it is recurring but cycle-bound, so a city-facing row needs the cycle/window, not "ongoing".

## Interpretation warnings

**Budget-line artifacts in the legacy CSV.** The SSG data contains rows like `Subt 24… (009)`, `Subt 32 Préstamos`, `Subt 33… (002)` that are DIPRES budget-classification artifacts (subtítulo/asignación) of the same underlying programs (Alianzas, Créditos, PDI). This review deduplicates to the *program*, sourced from its INDAP ficha, so do not treat each budget line as a distinct fund.

**PRODESAL and PDTI are executed by municipalities.** INDAP transfers resources via convenio to the municipality, which hires the extension team. The city's role here is `implementer`, not `applicant` or `enabler`. Model the pathway accordingly; the ultimate `eligible_actor` and beneficiary is the smallholder or indigenous community. Capture `eligible_actor` per program to distinguish these cases from others.

**Eligibility requires prior INDAP accreditation.** Most programs require that the recipient be an established INDAP user (smallholder thresholds) and have no morose debt. A municipality is the delivery vehicle, not the beneficiary.

**Amounts are per-beneficiary incentives, not project-grant ceilings.** TAS, for example, pays up to 95% / CLP 450,000 (year 1) and up to 90% / CLP 3.5M (year 2) *per producer*. Do not read program budget totals as per-project figures; keep `amount_note` with units and the per-beneficiary structure explicit.

**Climate relevance comes from the funded works, not the program name.** TAS, Riego, and SIRSD-S are explicit (transition, water, soil); PRODESAL and PDTI are adjacent (general productive extension that *can* fund climate-resilient practices); credits and commercialization are indirect. Tag `climate_relevance` from the financiable activities, not from the program's nominal focus.

## Parsing notes

- No data is inherited from the SSG CSV — it lacks URLs, mixes budget lines with programs, and is a 2023 snapshot. Build v1 by **hand-curating from the INDAP fichas** (one row per program), `source_url` per row, same pattern as `cl-conaf/cl-conaf-fondos`.
- `indap.gob.cl` is server-rendered (fetch works without JS). Retrieval = fetch each `/plataforma-de-servicios/<slug>` ficha + the Concursos listing; the Bases/Norma Técnica PDFs hold exact amounts, percentages and accreditation thresholds.
- Spanish long-form dates and CLP amounts ("$ 3.500.000", dot thousands) — normalise to integer CLP; keep timezone notes on cierre times.
- The Concursos listing is the **index tier** (enumerate every open concurso: program, dates, region); the fichas are the **detail tier** (eligibility, instrument, financiable works). Merge on program.

## Extraction & refresh

`data/cl_indap_fondos_v1.csv` is hand-curated from the fichas above, one row per program (same pattern as `cl-conaf-fondos`). To refresh: re-read each `source_url` and its Norma Técnica PDF, update amounts, `status` and `status_as_of`. Refresh annually around the Concursos de Fomento opening, plus the TAS cycle window.

Source pages (captured 2026-06-18): `indap.gob.cl/plataforma-de-servicios`, `indap.gob.cl/concursos`, per-program fichas (TAS, PRODESAL, PDTI, PAP, PDI, SAT, Riego), ChileAtiende fichas 118433 / 1720.

## Status

**Release v1 built — not yet production-approved.** `releases/v1/` holds the review notebook `cl_indap_fondos_review.ipynb` (load → validate → aggregates → program→action mapping → coverage charts; restart-and-run-all passes), `data/cl_indap_fondos_v1.csv` (9 programs), `data/cl_indap_fondos_to_actions.csv` (the crosswalk) + `review.md`. Provenance, license and recurrence **verified** (live fetch of the INDAP fichas, 2026-06-18). TAS and SIRSD-S amounts **verified** from the ficha; the remaining per-cycle amounts are **unverified** (`detail_level = index`) pending each Norma Técnica PDF. License **partly verified** (public info — verified; affirmative reuse grant — unanswered). Next: confirm the index-row amounts, then promote via `catalog/index.yaml`.
