# Review — cl-mop-fondos, release v1

## Scope and status

Research release (not production-approved). The water/adaptation and rural-infrastructure slice missing from the Chile finance inventory: the recurring funding MOP channels through its sub-directorates. Snapshot hand-curated from the MOP sub-directorate sites (DOH, DGA, DGOP, Concesiones, Arquitectura) captured 2026-06-18 — **not** from the legacy `cl-ssg/cl-ssg-finance` CSV, which was used only as a discovery signal. Output: `data/cl_mop_fondos_v1.csv` — 7 rows across 5 sub-directorates. Dataset-level facts (sources, license, parsing) are in the README one level up.

## What this data supports

- "MOP runs a large, permanent rural water-security program." — supported; APR/SSR (DOH) operates ~2,422 systems for ~2.27M people, since 1964, under Ley 20.998, at roughly CLP 300 bn/yr.
- "Water and sanitation are directly funded." — supported; APR/SSR covers new systems, expansion and sanitation, with a conservation line for existing systems.
- "There is cross-sector rural infrastructure money." — supported; Infraestructura para el Buen Vivir (DGOP) funds roads, rural sanitation, water systems and rural buildings.
- "Each program carries a recurrence expectation." — supported; `recurrence` separates `ongoing` (APR/SSR, conservation, DGA basin administration, Arquitectura inversión) from `time-boxed` (PIBV, the development-infrastructure fund, the 2022–2026 APP plan).

## What this data does not support

- "MOP is one fund a city applies to." — NO. It is four+ different instruments across sub-directorates: DOH grants to water committees, DGA statutory administration, DGOP budget transfers, Concesiones PPP. Model each separately with its `provider`.
- "DGA's basin line is a competitive grant." — NO. It is statutory water-rights administration plus PERH basin plans and a water-research fund created by Ley 21.435 — `access_pathway = statutory/intermediated`, not a city application channel.
- "APR/SSR pays the municipality." — NO. The operator/beneficiary is the rural water committee or cooperative (`community_org`); the city facilitates. The ~CLP 300 bn/yr is a program aggregate, not a per-project figure.
- "Infraestructura para el Buen Vivir is available anywhere." — NO. It is geographically gated (Arauco, Biobío, Malleco, Cautín; from 2024 Los Ríos & Los Lagos). Surfacing it elsewhere is wrong.
- "These are permanent, open funds." — only some. APR/SSR, conservation, DGA and Arquitectura inversión are `ongoing`; PIBV, the infra fund and the APP plan are `time-boxed` (program horizon / 2022–2026), and several flow through the SNI/BIP gate rather than as an open call.

## Using it downstream

- For fundability scoring, the `explicit` water programs (APR/SSR, conservation, DGA cuencas) are the strong adaptation matches; PIBV and the infra fund are `adjacent` and should carry their territorial/time-box caveats; Arquitectura is `indirect`.
- Where `access_pathway` is `statutory`/`intermediated` or routed through SNI/BIP, relate to public-investment formulation rather than modelling a competitive concurso.
- Amounts here are program aggregates or budget lines; per-project figures come from SNI/BIP formulation and DIPRES/MOP execution reports — confirm before a city relies on a number.
- Awards / who-won do not live in this supply dataset and have no MOP-specific awards companion. APR/SSR and DGOP/Arquitectura outcomes are public-investment records in `cl-mdsfam/cl-bip-projects` (with construction-contract awards on Mercado Público / the MOP licitaciones visor); the Concesiones awarded portfolio is at `concesiones.mop.gob.cl`. See the README's "Awards / who won" section.

## Mapping to actions

`data/cl_mop_fondos_to_actions.csv` (built by the release notebook `cl_mop_fondos_review.ipynb`, Block 5) links each program to the city action list. The result is itself the finding: **7 of 8 programs map to `none`**. Only the Dirección de Arquitectura program reaches an action (`c40_0017` retrofit municipal buildings, medium; `c40_0012` institutional standards, low). APR/SSR, conservación, saneamiento and DGA cuencas — the climate-explicit core — map to nothing because the **action list is mitigation-only and contains no water-supply / water-security / adaptation action**; PIBV, the infra fund and the Concesiones plan are broad multi-sector finance vehicles that only resolve at project grain.

This is a property of the target taxonomy, not a weakness of MOP finance: coverage is low because MOP's value is adaptation/water and the action spine is mitigation. The unreached-target finding belongs upstream with whoever owns the action list — the missing water-security and rural-sanitation archetypes are the blocker. All rows are agent drafts and **await human adjudication**.

## Notes on non-obvious fields

- `amount_clp` null is expected — values are program aggregates or budget lines, not project ceilings; structure is in `amount_note`.
- `recurrence` vocabulary: `ongoing` (permanent/statutory) vs `time-boxed` (program horizon or named multi-year plan). The time-boxed flag is the load-bearing one — PIBV and the APP plan must not be surfaced as permanent.
- `provider` carries the sub-directorate (DOH / DGA / DGOP / DGC / DA); `funder_institution` is MOP for all.
- `detail_level = detailed` rows (APR/SSR, PIBV) were read from live source/searches; `index` rows carry verified identity + source_url with amounts pending DIPRES/laws.

## Traceability

Sources (captured 2026-06-18): DOH (`doh.mop.gob.cl`, /SSR/) and the 60-años APR background; DGA legislación (`dga.mop.gob.cl/legislacion/`, Ley 21.435) and the Water Transition Program announcement; DGOP PIBV program page (`dgop.mop.gob.cl`) and DIPRES Partida 12.02.14 records; Concesiones APP plan 2022–2026; Dirección de Arquitectura. Statutory bases Ley 20.998 and Ley 21.435. Per-program amounts and the Concesiones/Arquitectura rows are **unverified** at value level — confirm against DIPRES execution reports and the laws. Refresh steps in the README.
