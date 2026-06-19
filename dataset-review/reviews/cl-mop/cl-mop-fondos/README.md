# Ministerio de Obras Públicas (Chile) — MOP infrastructure & water finance (cl-mop)

The recurring funding MOP channels for climate-relevant infrastructure, concentrated in **water** (rural drinking water and sanitation, basin management) and **cross-sector rural infrastructure**. Unlike the single-publisher Chile finance sources, MOP is a **family of sub-directorates**, each with its own site and program: DOH (Dirección de Obras Hidráulicas) runs Agua Potable Rural / Servicios Sanitarios Rurales; DGA (Dirección General de Aguas) runs basin/water-rights administration under the reformed Código de Aguas; DGOP (Dirección General de Obras Públicas) runs the Infraestructura para el Buen Vivir program and the development-infrastructure fund; the Dirección General de Concesiones runs the public-private (APP) infrastructure plan. This entry adds the **water/adaptation and rural-infrastructure** slice missing from the inventory. **It sources from the MOP sub-directorate pages, not from the legacy `cl-ssg/cl-ssg-finance` snapshot** — the SSG CSV is a discovery signal only (every MOP row in it has `source_url = "No especificado"`).

This is a **started review**: Step 1 (provenance/access/license) and Step 3 (recurrence screen) are verified against primary sources (live search 2026-06-18); the extraction notebook and `data/` release are not yet built (see Status).

## Canonical sources

One publisher dir (`cl-mop`), several sub-directorate origins. Source each program from its own site:

- DOH — Dirección de Obras Hidráulicas: https://doh.mop.gob.cl/
  - Servicios Sanitarios Rurales (APR/SSR): https://doh.mop.gob.cl/SSR/index.html ; program background https://doh.mop.gob.cl/2024/11/22/mop-conmemora-60-anos-del-programa-de-agua-potable-rural-apr-que-beneficia-a-mas-de-2-millones-de-personas-en-el-pais/
  - Statutory basis — Ley 20.998 (Regula los Servicios Sanitarios Rurales) + reglamento: https://www.mop.gob.cl/archivos/2023/12/Presentacion-Ley-y-Reglamento-SSR.pdf
- DGA — Dirección General de Aguas: https://dga.mop.gob.cl/ ; legislación https://dga.mop.gob.cl/legislacion/ ; Ley 21.435 (reforma Código de Aguas) https://dga.mop.gob.cl/uploads/sites/13/2023/07/ley_21435.pdf
- DGOP — Dirección General de Obras Públicas: https://dgop.mop.gob.cl/
  - Programa Infraestructura para el Buen Vivir (PIBV): https://dgop.mop.gob.cl/programa-infraestructura-para-el-buen-vivir/ and the fondo page https://dgop.mop.gob.cl/fondo-infraestructura-para-el-buen-vivir/ ; quarterly execution reports under `dgop.mop.gob.cl/uploads/...`
- DIPRES program records (budget line, evaluations) — Partida 12 (MOP), e.g. PIBV "Partida 12 Capítulo 02 Programa 14": https://www.dipres.gob.cl/597/w3-multipropertyvalues-35376-35869.html
- Concesiones — Plan de infraestructura en Asociación Público-Privada 2022–2026 (Dirección General de Concesiones), via `concesiones.mop.gob.cl` / MOP.

## Why we use it

- Fills the **water / adaptation** gap: rural drinking water and sanitation (APR/SSR) and basin management are the most directly adaptation-relevant national programs absent from the inventory, all under the `water`/`waste`/`afolu` sectors.
- APR/SSR is a genuinely large standing program (since 1964; ~2,400 systems; ~CLP 300 bn/yr) with a clear city/community pathway — rural water committees and cooperatives are the operators, and municipalities facilitate.
- Adds cross-sector rural infrastructure (PIBV) covering roads, sanitation and rural buildings in indigenous and rural territories.

## License

Public government information (verified 2026-06-18). MOP and its sub-directorates (`mop.gob.cl`, `doh.mop.gob.cl`, `dga.mop.gob.cl`, `dgop.mop.gob.cl`) are public bodies administering public funds under the **Ley de Transparencia (Ley 20.285)**; program facts, statutory bases (Ley 20.998, Ley 21.435) and budget/execution reports (DIPRES) are public. No restrictive aggregator terms. Capture, attribute to the specific sub-directorate, and obtain legal confirmation before large-scale product redistribution; do not label "open licence" downstream.

## Spatial and temporal scope

National, executed regionally (DOH/DGA regional offices) and at the comuna level. PIBV is geographically **targeted** — Arauco, Biobío, Malleco and Cautín, extended from 2024 to Los Ríos and Los Lagos. APR/SSR and DGA basin administration are national and statutory (permanent). Capture status with an as-of date per release.

## Recurrence classification (the field the inventory needs)

Per the requirement to distinguish what is *expected to recur*:

| Program | Owner | Sector | `recurrence` | Climate relevance | Evidence |
|---|---|---|---|---|---|
| Agua Potable Rural / Servicios Sanitarios Rurales (APR/SSR) | DOH | water (waste/afolu) | **standing** (permanent, statutory) | explicit | Program since 1964; Ley 20.998; ~CLP 300 bn/yr |
| Saneamiento rural | DOH | waste/water | **standing** | explicit | Part of SSR mandate (water + sanitation) |
| Conservación APRs | DOH | water | **standing** | explicit | Ongoing conservation of existing systems |
| Gestión de cuencas (Leyes 20.998 / 21.435) | DGA | afolu/water | **standing** (statutory) | explicit | Reformed Código de Aguas; PERH basin plans, water-research fund |
| Infraestructura para el Buen Vivir (PIBV) | DGOP | cross-sector | **time-boxed** (targeted, plan horizon) | adjacent | Annual budget line (Partida 12.02.14), but region-targeted + program horizon |
| Fondo de Infraestructura para el Desarrollo | DGOP | cross-sector | **time-boxed** | adjacent | Budget-line transfer fund |
| Plan APP / Concesiones 2022–2026 | DG Concesiones | energy supply / transport | **time-boxed** (defined 2022–2026 plan) | adjacent | Named multi-year plan with end date |
| Equipamiento social / Iniciativas de inversión | Dir. Arquitectura | public buildings / energy | **standing** (Subt 31 inversión) | indirect | Recurrent investment subtitle |

Flag the two DGOP items and the Concesiones plan as **time-boxed** — they have a program horizon and should not be surfaced as permanent. APR/SSR and DGA basin management are the permanent, climate-explicit anchors.

## Interpretation warnings

- **MOP is not one fund — split by sub-directorate.** A naive "MOP" row hides four very different instruments (DOH grants to water committees, DGA statutory administration, DGOP budget transfers, Concesiones PPP). Model each program separately with its owning sub-directorate; keep `provider`/`funder` distinct.
- **DGA's line is statutory administration, not a competitive fund.** The CSV's `Aplicación Leyes 20.998 y 21.435` is basin/water-rights governance and a water-research fund created by the reform — not a grant a city applies to. Tag as `access_pathway = statutory/intermediated`, climate-explicit but not a direct city application channel.
- **APR/SSR beneficiary is the rural water committee/cooperative, with the city as facilitator.** Eligible operators are `comités`/`cooperativas` de agua potable rural; the municipality facilitates and may co-formulate. Tag `eligible_actor = community_org` + city `enabler`/`facilitator`, not "municipality applies".
- **PIBV is geographically gated.** Surfacing it for a comuna outside the named provinces/regions is wrong; carry the eligible-territory list and check before showing the row.
- **Much MOP money flows through the SNI/BIP gate (Route B), not as a direct call.** Several of these are budget transfers to formulated investment projects, not open competitive funds — model the pathway as public-investment financing, not a "concurso".
- **Climate relevance from funded works.** APR/SSR, saneamiento and cuencas are explicit (water security/adaptation); PIBV and the infra fund are adjacent (cross-sector rural works that can be climate-relevant); Arquitectura equipment is indirect.

## Parsing notes

- No data is inherited from the SSG CSV — it lacks URLs, mixes sub-directorates and budget subtitles, and is a 2023 snapshot. Build v1 by **hand-curating from the sub-directorate pages**, one row per program, `source_url` and `provider` (sub-directorate) per row.
- Sites are server-rendered (fetch works without JS). Statutory detail and amounts live in the laws (Ley 20.998, Ley 21.435) and DIPRES program/evaluation PDFs and DGOP quarterly execution reports — cite those for amounts.
- Budget-subtitle names in the CSV (`Subt 31 Iniciativas de Inversión`, `asignación 001 A otros ejecutores`) are DIPRES classification artifacts; resolve to the named program.
- Spanish long-form dates, CLP amounts (dot thousands) — normalise; keep an as-of date because APR/SSR figures are reported per budget year.

## Extraction & refresh

`data/cl_mop_fondos_v1.csv` is hand-curated from the sub-directorate pages above, one row per program with its `provider`. To refresh: re-read each `source_url` plus the relevant DIPRES execution report / law, update amounts, `status` and `status_as_of`. Refresh annually with the budget year.

Source pages (captured 2026-06-18): `doh.mop.gob.cl` (+ /SSR/), `dga.mop.gob.cl` (+ /legislacion/), `dgop.mop.gob.cl` (PIBV + fondo), DIPRES Partida 12 records, Concesiones APP plan 2022–2026, Ley 20.998 and Ley 21.435.

## Awards / who won

Unlike INDAP (and CONAF), MOP has no single beneficiary nómina to harvest — the "who won and how much" for these programs flows through other systems, so there is no `cl-mop-awards` companion to build here. Rural water (APR/SSR) and most DGOP/Arquitectura investment is formulated and tracked as public investment, so its awards are the **SNI/BIP project records** already covered by `cl-mdsfam/cl-bip-projects`, with the construction-contract awards on **Mercado Público** and the MOP licitaciones visor. The Concesiones plan is the exception with its own structured disclosure: the **awarded-concessions portfolio** (concessionaire, investment amount, status) at `concesiones.mop.gob.cl/concesiones/cartera-de-proyectos/`. So for MOP, point the awards question at BIP + procurement + the Concesiones portfolio rather than expecting a fund-by-fund winners list.

References: `cl-mdsfam/cl-bip-projects`; https://www.mop.gob.cl/visordelicitaciones/ ; https://concesiones.mop.gob.cl/concesiones/cartera-de-proyectos/

## Status

**Release v1 built — not yet production-approved.** `releases/v1/` holds the review notebook `cl_mop_fondos_review.ipynb` (load → validate → aggregates → program→action mapping → coverage charts; restart-and-run-all passes), `data/cl_mop_fondos_v1.csv` (7 programs across 5 sub-directorates), `data/cl_mop_fondos_to_actions.csv` (the crosswalk) + `review.md`. Provenance, sub-directorate structure and recurrence **verified** (2026-06-18); APR/SSR and PIBV facts **verified** from source; per-program amounts and the Concesiones/Arquitectura rows **unverified** (`detail_level = index`) pending DIPRES execution reports and the laws. License **partly verified** (public info — verified; affirmative reuse grant — unanswered). Next: confirm index-row amounts, then promote via `catalog/index.yaml`.
