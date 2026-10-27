# INDAP fomento awards / beneficiaries (cl-indap-awards)

The "who actually got funded" companion to the supply-side review `cl-indap/cl-indap-fondos`: the awarded projects and beneficiary nóminas of INDAP's fomento programs (TAS, SIRSD-S, Riego, PDI, PRODESAL, PDTI, PAP and the rest). This is the **awards / revealed-fundability** layer for agriculture — the AFOLU analogue of `cl-conaf/cl-conaf-bn-awards` — answering "what gets funded, where, how often, at what size?" rather than "what is available". It records *outcomes* (selected applications), kept strictly separate from the supply review, which records the *program*.

This review has a **proof-of-pipeline release** (`releases/v1/`): a single concurso harvested end-to-end to fix the method, schema and PII handling before any wider harvest. The honest finding is that this layer *exists, is public, and is machine-extractable*, but assembling it is a consolidation-and-de-identification job, not a one-file download. Two empirical facts shape the work: the Concursos channel publishes **calls (llamados) richly but results (resultados) sparsely** — of 370 listed concursos, the visible entries are openings, while winners appear on separate "Resultados" pages — and each results page links **per-province Resolución Exenta PDFs** that contain the awarded list **with RUT and full name** (PII), so de-identification is mandatory.

## Canonical sources

INDAP discloses winners through two distinct channels; a real awards dataset draws on both.

- **Concurso results pages** — per-call lists of selected projects / planes de manejo, published under the Concursos section as each cycle resolves. Index: https://www.indap.gob.cl/concursos/todos-los-concursos ; example result page: https://www.indap.gob.cl/concursos/todos-los-concursos/resultados-de-los-concursos-territoriales-programa-sirsd-s-region-del (SIRSD-S Biobío concursos 4–7 2025). PDI/Riego special calls publish equivalents. Investment-program results also surface via GORE co-financed rounds (e.g. GORE Los Ríos + INDAP, 3er Concurso de Inversión 2025, ~CLP 1,466 M across 171 projects).
- **Transparencia activa (Ley 20.285)** — the systematic, amount-bearing channel: the *Programas de Subsidios y Otros Beneficios* index (https://transparencia.indap.cl/2010/subsidio_programas.html) and the monthly *Nómina de Beneficiarios de Programas Sociales en Ejecución* listings on `transparencia.indap.cl`, by program and region. These carry the beneficiary, the program, the region and the amount.
- Application/results back-end for investment lines: https://inversiones.indap.cl/ (postulation + selection).

## Access

No documented bulk API or single export. The concurso results are HTML/PDF pages, fragmented per call and region, and several are posted only as "available at the Agencia de Área / Dirección Regional" — so online coverage is uneven and some cycles resolve only offline. The transparencia nóminas are **monthly HTML pages** split by program and region, which makes a multi-year, multi-program series a stitch-many-pages exercise. Building v1 therefore means enumerating the relevant program/region/month pages, parsing each, and unioning — closer to the MMA hub-enumeration pattern than to a clean CONAF-style download. Expect a manual or semi-automated harvest, captured with an as-of date.

## License

Public-interest government information — INDAP is a public body administering public funds, so program and award facts are public. **But the nóminas identify individual beneficiaries** (natural persons, often with RUT and amount), so reuse is governed by Chile's data-protection rules, not plain public-info reuse — the same constraint that applies to the CONAF awards export. Decision for this dataset (mirroring `cl-conaf-bn-awards`): **strip or aggregate personal identifiers before any commit or redistribution**; commit only de-identified derivatives (program × region × cycle × amount), never raw beneficiary rows. No explicit open licence (e.g. CC BY) is attached to either channel. Evidence tags: program/award-fact reuse **verified** (public); PII handling **decided here** (de-identify before commit).

## Spatial and temporal scope

National, resolvable to **region** and (for some concurso results) **comuna**, by program and cycle. Temporal coverage depends on the harvest: concurso results exist per call (annual for most programs; per 2-yr cycle for TAS), and transparencia nóminas run monthly back several years. The achievable series is "awards by program × region × cycle", with comuna where the result page provides it.

## Interpretation warnings

These mirror the CONAF awards caveats and add INDAP-specific ones; write them into the dataset when built.

- **Awarded is not paid.** Selection (adjudicación) precedes execution and the actual incentive payment; an award row is "committed", not "disbursed". The two-stage TAS structure (year-1 capital, year-2 inversiones) makes this especially visible.
- **The beneficiary is the smallholder, but PRODESAL/PDTI run through municipal execution.** For municipal-delivered programs the *executor* is the comuna while the *beneficiary* is the AFC user — don't read the executor as the awardee, and don't read the awardee as the city.
- **Amounts mix units and co-financing.** Figures may be CLP or percentages of co-financed cost; capture the unit and whether it is the INDAP contribution or the total project cost. Cross-check against the program's known ceilings (the supply review's `amount_note`).
- **Coverage is uneven by channel.** Transparencia nóminas are comprehensive but coarse; concurso results are richer but patchy. State which channel each row came from; do not present a partial harvest as the full awarded set.
- **No municipality is the awardee.** As with CONAF, awardees are private AFC users/organizations; the city's relevance is enabler/implementer, not recipient.

## Parsing notes

- Transparencia pages are per-program, per-region, **per-month** HTML tables — enumerate the index first (`/2010/subsidio_programas.html` pattern), then harvest the monthly nómina pages; expect repeated monthly rows for continuing beneficiaries.
- Concurso result pages vary in format (HTML lists, embedded PDFs, "see regional office" stubs); treat as a two-tier harvest (detailed where the list is online; index where only the call/result is named).
- Spanish long-form dates and CLP amounts (dot thousands); normalise. Keep `programa`, `region`, `comuna` (where present), `cycle`, `amount`, `amount_unit`, `channel`, `source_url`, `as_of`.
- PII columns (beneficiary name, RUT, contact) are dropped/aggregated at load — commit only de-identified derivatives.

## Relationship to other datasets

- `cl-indap/cl-indap-fondos` — the supply side (what each program is). This is its awards side; join on the program, not a shared key.
- `cl-conaf/cl-conaf-bn-awards` — the sibling AFOLU awards dataset (forestry); same supply-vs-awards split, same PII discipline.
- `cl-mdsfam/cl-bip-projects` — the public-investment outcomes pipeline; **no record overlap** (private AFC applicants vs public bodies). Relate only at the (comuna/region, sector) aggregate level.

## Status

**Proof-of-pipeline release built — not production-approved.** `releases/v1/` holds a single-concurso de-identified sample (`data/cl_indap_awards_sirsds_biobio2025_arauco_sample.csv`, 96 awarded planes, RUT + name dropped) + `review.md`. Provenance, access path and the PII decision **verified and applied** (2026-06-18); the parse reproduces the resolución's declared control total (CLP 80,033,236 / 96 planes) exactly, which is the data-quality gate. Raw PII PDFs are **not committed**. Next increment: the other three Biobío 2025 SIRSD-S resoluciones (REx 020905/020907/020908), then other regions and the TAS/PDI investment concursos; switch flowed-text parsing to a table-aware PDF extractor (pdfplumber) for the full harvest. Then promote via `catalog/index.yaml`.
