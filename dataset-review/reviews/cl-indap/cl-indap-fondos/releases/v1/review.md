# Review — cl-indap-fondos, release v1

## Scope and status

Research release (not production-approved). The AFOLU agricultural-finance slice missing from the Chile finance inventory: INDAP's standing fomento programs. Snapshot hand-curated from official INDAP program fichas (`indap.gob.cl/plataforma-de-servicios`) captured 2026-06-18 — **not** from the legacy `cl-ssg/cl-ssg-finance` CSV, which was used only to discover that INDAP was missing. Output: `data/cl_indap_fondos_v1.csv` — 9 rows, one per distinct program (the legacy CSV's 34 INDAP rows collapse to these once budget-subtitle duplicates are removed). Dataset-level facts (sources, license, parsing) are in the README one level up.

## What this data supports

All five core claims about INDAP's role are supported by the nine programs captured here.

The data shows INDAP's standing, recurring climate-relevant finance for smallholder and family farming. All nine programs in the release are marked `afolu` and are sourced from permanent INDAP fichas — they are not discovery signals or one-off calls.

INDAP has an explicitly climate-focused program. TAS (Transición a la Agricultura Sostenible) is built around agroecología, climate resilience and water scarcity, with year-1 incentives up to 95% / CLP 450,000 and year-2 incentives up to 90% / CLP 3,500,000.

Soil and water are directly financed. SIRSD-S finances up to 90% of soil-recovery and erosion-control works (Ley 20.412), and the Riego program co-finances on-farm irrigation.

A city can be the delivery vehicle, not just a referrer. PRODESAL and PDTI are executed *by municipalities* under convenio — the city is an active implementer.

Each program carries a recurrence expectation. The `recurrence` field distinguishes `biennial-cycle` (TAS), `annual` (SIRSD-S, Riego, SAT, PAP, PDI), and `ongoing` (PRODESAL, PDTI, créditos).

## What this data does not support

Do not read these figures as final per-project amounts. Most `amount_clp` are null because amounts are co-financing percentages and ceilings set per cycle in each program's Norma Técnica / concurso bases, not flat project-level figures. Read `amount_note` to understand the structure, and confirm against the bases before any city relies on a figure.

PRODESAL and PDTI do not make the municipality the beneficiary. The beneficiary is the smallholder or indigenous community; the municipality is the executor. Model the city as `implementer`.

TAS is not permanently open or available. It runs in two-year cycles; the second cycle's window (13–29 Oct 2025) is closed as of 2026-06-18. The `recurrence` field marks this as `biennial-cycle`, and the `status` is `closed`.

PRODESAL, PDTI, SAT, PAP, and PDI are not climate funds, though they support climate outcomes. PRODESAL and PDTI carry an explicit climate-adaptation mandate but are general extension programs (`specificity = broad`, `climate_relevance = climate-adjacent`); SAT, PAP, PDI, and créditos are `indirect`. Only TAS, SIRSD-S, and Riego carry `climate_relevance = explicit`.

## Using it downstream

- For fundability scoring, the three `explicit` AFOLU programs (TAS, SIRSD-S, Riego) are the strong matches; the `adjacent`/`indirect` ones support breadth but should be down-weighted by `climate_relevance` and `specificity`.
- Treat `recurrence` as a first-class field: surface `annual`/`ongoing` programs as standing availability, but a TAS row must carry its cycle/window, never a flat "recurring".
- Exact adequacy (amount vs project cost) must be checked against each program's Norma Técnica PDF (linked from the ficha) before a city acts.

## Mapping to actions

`data/cl_indap_fondos_to_actions.csv` (built by the release notebook `cl_indap_fondos_review.ipynb`, Block 5) links each program to the city action list, one row per (program, action) pair, with confidence tags and rationale; quantities stay at the program grain (link, don't attribute). Coverage: 7 of 9 programs map, reaching 6 AFOLU actions — TAS → regenerative/agroecological agriculture (`icare_0045`, high) is the one strong link; the rest are medium/low (PRODESAL, PDTI, SAT are broad municipal-delivered or advisory instruments, medium by convention; PAP, PDI are indirect/low). Two programs are `none`: **Riego** (no on-farm irrigation / agricultural water-efficiency action exists) and **créditos** (a finance lever, not an intervention).

Two taxonomy gaps surfaced and matter more than anything in the data: there is **no soil-conservation / restore-degraded-agricultural-soils action**, so SIRSD-S — the cleanest AFOLU instrument — has only partial homes (`ipcc_0067` crop nutrient, `icare_0045` regenerative, both medium); and there is **no agricultural-irrigation action**, leaving Riego unmappable. All medium/low/none rows are agent drafts and **await human adjudication**. Use the mapping as a link only: an award or amount on a program contributes revealed-demand weight to its mapped actions, never split across them.

## Notes on non-obvious fields

- `amount_clp` null is expected — benefits are co-financing %+ceilings, not single project figures; structure is in `amount_note`.
- `recurrence` vocabulary: `annual` (yearly concurso), `ongoing` (rolling/permanent, e.g. PRODESAL solicitud todo el año and créditos), `biennial-cycle` (TAS).
- `detail_level = detailed` rows (TAS, SIRSD-S, PRODESAL, PDTI) were read from the live ficha; `index` rows (Riego, SAT, PAP, PDI, créditos) carry verified program identity + source_url but amounts pending the bases.

## Traceability

Sources (captured 2026-06-18): INDAP fichas for TAS, SIRSD-S and PRODESAL (read in full), plus the Nuestros Programas menu and Concursos de Fomento listing for the remaining program slugs; ChileAtiende ficha 118433 (TAS) corroborating amounts. Statutory bases: Ley 20.412 (SIRSD-S), Ley Orgánica INDAP 18.910. Per-cycle amounts beyond TAS/SIRSD-S are **unverified** — confirm against each Norma Técnica PDF. Refresh steps in the README.
