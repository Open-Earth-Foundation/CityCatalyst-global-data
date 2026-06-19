# Corporación Nacional Forestal (Chile) — native-forest finance (cl-conaf)

The forestry / nature-based funding CONAF administers under the Ley de Bosque Nativo (Ley 20.283): the Fondo de Conservación, Recuperación y Manejo Sustentable del Bosque Nativo (the bonificación concurso) and the adjacent Fondo de Investigación del Bosque Nativo. This entry adds the **AFOLU / nature-based** slice that need `2026-06-cl-finance-opportunities` was missing — v1 had no CONAF/MINAGRI line at all despite AFOLU being a core GPC sector with both mitigation (forest carbon) and adaptation (soil, water, fire) relevance (gap 2 in the need's `gaps.md`).

## Canonical sources

CONAF runs its own programme pages and a dedicated application portal:

- CONAF programme page: https://www.conaf.cl/manejo-de-ecosistemas/bosque-nativo/fondo-de-conservacion-y-manejo-sustentable-del-bosque-nativo/
- 2026 call announcement (dates, total fund): https://www.conaf.cl/abiertas-postulaciones-al-fondo-de-conservacion-de-la-ley-de-bosque-nativo-20-283/ and https://www.conaf.cl/conaf-lanza-fondo-con-casi-7-mil-millones-para-impulsar-el-manejo-sustentable-del-bosque-nativo/
- Application portal + bases: https://concursolbn.conaf.cl/ (`/login/bases.php`, `/login/guia.php`).
- Research line (adjacent): Fondo de Investigación del Bosque Nativo, XVII concurso 2026.

## Why we use it

- Fills the **afolu / nature-based** gap, absent from v1 — the inventory had no forestry, urban-greening, or fire/soil-conservation finance beyond MINVU's urban parks.
- Explicit climate line: native-forest conservation, regeneration, fire-prevention (cortafuegos) and soil conservation are mitigation + adaptation relevant; maps to `gpc_sector = afolu`.
- Time-sensitive and live: the 2026 concurso is open with a near-term deadline (see below), making it the most actionable new entry.

## License

Public government information (verified 2026-06-16): CONAF (`conaf.cl`, `concursolbn.conaf.cl`) is a public-interest body administering public funds; programme facts (name, eligible actor, amounts, dates, financiable activities, links) are public information. Standard public-info treatment: capture and attribute. No restrictive aggregator terms in play.

## Spatial and temporal scope

National (all regions with native forest / xerophytic formations of high ecological value). The bonificación concurso is **annual**; the **2026 cycle is open now with applications closing at noon on 1 July 2026 and results announced late August 2026** — a real, dated cycle of exactly the kind the SSG 2023 set lacked. Status as captured 2026-06-16.

## Interpretation warnings

- **TIME-SENSITIVE.** The 2026 window closes noon 1 Jul 2026. A city-facing row must show `status = open` + this close date, not a generic "recurring" — and the row goes stale within weeks; re-verify before surfacing.
- **Eligible actor is the forest landowner, not "the municipality" by default.** Two lines: pequeños propietarios (small owners, whom CONAF accompanies through the whole process) and otros interesados. A municipality qualifies only as a landowner of eligible native forest; otherwise the city's role is to facilitate local owners. Tag `eligible_actor`; broad-capture keeps the row.
- **Per-hectare bonificación, not a project grant ceiling.** The total 2026 fund is ~CLP 6.98 bn across all awards; the per-applicant benefit is a per-hectare bonificación (literal C cap ~10 UTM/ha). `amount_clp` is null with the structure in `amount_note` — don't read the fund total as a per-project figure.
- **Research line is not a city fund.** The Fondo de Investigación del Bosque Nativo (XVII concurso 2026) is recorded as `climate-adjacent` / `index` context — eligible actor is research/universities, not a city finance opportunity. Kept tagged so it isn't mistaken for an applicable grant.

## Parsing notes

- v1 is **hand-curated** from the CONAF programme/announcement pages (captured 2026-06-16), one row per fund line, `source_url` per row — same pattern as the other Chile finance sources.
- The live application portal `concursolbn.conaf.cl` holds the bases (PDF) with the literales (a/b/c), per-ha rates and exact requirements — the authoritative place to confirm amounts before any city acts.
- The 2026 total-fund figure and dates come from the CONAF launch announcement; the per-ha caps (e.g. 10 UTM/ha, literal C) come from press coverage of the bases — confirm the precise table against the official bases PDF at portal.

## Extraction & refresh

Hand-curated from the source pages below using the OEF extraction prompt (see `reviews/oef/cl-city-action-fundability/releases/v1/extract_inventory.ipynb`, or the per-source prompt in `reviews/cl-minenergia/cl-minenergia-fondos/README.md`). To refresh: re-read each `source_url` and the portal bases, re-run the prompt, replace rows in `data/cl_conaf_programs_v1.csv`, spot-check, and update `status` / `status_as_of` (this fund's status changes each cycle — refresh at least annually around the April launch).

Source pages (captured 2026-06-16): conaf.cl programme + 2026 launch pages, concursolbn.conaf.cl portal, Fondo de Investigación del Bosque Nativo XVII concurso 2026.

## Current approved release

Not yet promoted (awaiting sign-off). First release **v1** in `releases/v1/`: `data/cl_conaf_programs_v1.csv` (2 lines — the bonificación concurso + the research fund) + `review.md`. Evidence tags: provenance/scope **verified** (live search 2026-06-16); 2026 dates and total fund **verified**; per-ha caps (10 UTM/ha literal C) **partly verified** (from press, confirm against bases PDF); eligibility (small owners + others; municipalities as landowners) **verified**; license **verified** (public government info).
