# Ministerio del Medio Ambiente (Chile) — MMA competitive funds portal (fondos.mma.gob.cl)

MMA's own portal for its competitive environmental funds: the Fondo de Protección Ambiental (FPA) and the Fondo para el Reciclaje (FPR), plus the Recambio de Calefactores programme and special territorial calls. This entry covers the portal as a *live, authoritative source* for the environment slice of the Chile climate-finance inventory (need `2026-06-cl-finance-opportunities`). It exists because the national aggregator `fondos.gob.cl` is unusable as a stored/redistributed source (restrictive terms — see that candidate's reject note); MMA's own pages are the authoritative origin for these funds and carry no such restriction. Scope here is MMA funds only; MINVU, Min. Energía and SUBDERE programmes are separate per-institution reviews.

## Canonical sources

- Portal root: https://fondos.mma.gob.cl/ — index of open / in-evaluation / awarded funds, with a category filter and `?page=N` pagination.
- FPA hub: https://fondos.mma.gob.cl/fpa/ ; "what it is": https://fondos.mma.gob.cl/que-es-fpa/ ; general rules: https://fondos.mma.gob.cl/wp-content/uploads/2019/12/Bases_Generales-fpa.pdf
- FPR hub: https://fondos.mma.gob.cl/fpr/ ; FPR historical archive: https://fondoreciclaje.mma.gob.cl/
- Per-fund ficha pattern: `https://fondos.mma.gob.cl/<fund-slug>/` (e.g. `/fpa-2026-proyectos-sustentables-ciudadanos/`, `/fpr-2026-fondo-para-el-reciclaje/`).
- Per-fund the authoritative documents are the **Resolución Exenta** (approves the bases) and the results Resolución — linked as PDFs from each ficha under "Documentos a descargar".
- Applications themselves happen on the restricted aggregator (`fondos.gob.cl`); only descriptive/authoritative content is sourced from MMA.

## Why we use it

- Authoritative, current source for the **environment** category of need `2026-06-cl-finance-opportunities` (FPA, FPR, heater replacement) — the slice that dominates the live "Medio Ambiente" funds on the national portal.
- Intended to refresh/replace the environment rows of the static 2023 inventory `cl-ssg/cl-ssg-finance` (sibling catalog entry) with link-backed, status-verifiable records.
- Unlike `fondos.gob.cl`, it keeps a **historical archive** (awarded FPA/FPR 2020–2025), useful for recurrence/next-call estimation in the fundability work.
- Each ficha is semi-structured (an "Antecedentes Generales" table) so eligibility, amount, thematic lines, and dates are extractable per fund.

## License

No terms-of-use or reuse licence is published on `fondos.mma.gob.cl` (verified 2026-06-08: portal footers, the FPA "qué es" page, and a live ficha carry no "Aviso Legal" / "Términos y Condiciones"; none found by search). Content is public information of a State body under the **Ley de Transparencia (Law 20.285)**, and each fund's rules and awards are **Resoluciones Exentas** — official administrative acts, inherently public. No affirmative open-data licence (e.g. Creative Commons) is stated.

- **Verified:** no restrictive terms apply here (contrast `fondos.gob.cl`, whose ToU forbids copying/redistribution/mirroring); the underlying program facts are public administrative records.
- **Inferred / unanswered:** there is no explicit *grant* of reuse/redistribution rights. Treat program data as public-information facts, attribute to MMA, and obtain a legal confirmation before large-scale redistribution inside a product. Do **not** state this source as "open licence" downstream.

## Spatial and temporal scope

National (Chile), with regionally-targeted special calls (e.g. Rapa Nui; Alto del Carmen humedales/biodiversidad). FPA and FPR are **annual** competitions; the portal shows the current cycle plus an awarded-funds archive back to 2020. As of 2026-06-08 there were no FPA/FPR calls open (the FPA 2026 lines opened Aug 2025 and closed Oct 2025; FPR 2026 closed Nov 2025) — the funds are in their post-award/convenio phase. Status is therefore time-sensitive and must be re-checked per release.

## Interpretation warnings

- **Status is not a clean field — and the section label lags.** There is no status column; it must be derived. The index section ("Fondos Abiertos / En Evaluación / Adjudicados") and ficha banners ("POSTULACIONES DESDE EL …", "resultados de adjudicación") lag reality — extraction found the FPR 2026 ficha still grouped under "Abierto" after its 30-Oct-2025 close. **Rule (validated in the notebook): the close *date* is authoritative for "can I apply now"; the section/banner give lifecycle context only, and a `status_section_conflict` flag is raised when they disagree.** Always record the as-of date.
- **Annual cycles mean "closed now" is normal, not dead.** A fund with no open call is almost always between cycles. For the inventory/fundability use, store status + a next-call estimate from the historical pattern, never a flat "recurring".
- **Money and eligibility are per-line, not per-fund.** FPA runs several parallel lines (Proyectos Sustentables Ciudadanos, Establecimientos Educacionales, Pueblos Indígenas, plus special calls), each with its own amount, eligible applicants, and dates. Treat each *line* as the opportunity, not "FPA" as a whole. Example: FPA Ciudadanos 2026 = CLP 6,000,000, eligible = non-profit private legal persons (juntas de vecinos, ONG, fundaciones — **not** municipalities); FPR 2026 = up to CLP 14,000,000, eligible = municipalities and municipal associations.
- **Eligible actor differs sharply across MMA funds** — FPA excludes municipalities as applicants; FPR is municipality-only. Capture `eligible_actor` per line (the broad-capture schema in `search.yaml` already requires this); do not generalise "MMA funds" to one actor type.
- **Full fidelity lives in the Bases PDF.** The HTML ficha gives headline fields; exact eligibility, regional restrictions, scoring, and co-financing rules are only in the Resolución Exenta / Bases PDF. For anything beyond a summary row, parse the PDF.
- **Thematic lines are the climate hook.** FPA lines (Cambio Climático y Descontaminación, Economía Circular y Gestión de Residuos, Eficiencia Energética y Energías Renovables, Ecotecnias Hídricas, Biodiversidad) and the construction annexes (Punto Verde, Invernadero, SFV off/on-grid solar, SST solar-thermal) are what justify climate tagging — use them for `gpc_sector` / `climate_relevance`, not the fund name alone.
- **Accuracy is self-disclaimed upstream.** The aggregator (where applications occur) disclaims accuracy/completeness/currency; MMA pages can also lag. Trust the Resolución Exenta over banner text where they conflict.

## Parsing notes

- Pages are server-rendered WordPress HTML (fetch works without JS — unlike `fondos.gob.cl`). Retrieval = fetch ficha HTML + linked PDFs/DOCX; paginate the index via `?page=N`.
- The core structured object is the **"Antecedentes Generales" table** per ficha: Objetivo, Tipo de Postulantes, Financiamiento, Líneas Temáticas, Inicio/Cierre Postulaciones, Web de Postulación. Parse this table first.
- Table cells contain **rich nested lists and prose** (e.g. Tipo de Postulantes lists org types inline); expect bulleted text inside a single cell, and trailing empty rows (`|  |  |`).
- **Dates are Spanish long-form** ("26 de agosto del 2025", "07 de octubre del 2025 (Hasta las 14:00 hrs. Chile continental)") and sometimes only in a banner, not the table. Normalise; keep the timezone note.
- **Amounts** are Chilean peso strings ("$ 6.000.000") — dot thousands separators; parse to integer CLP.
- "Web de Postulación" points to `fondos.gob.cl` (restricted) — keep as the application pathway, but source descriptive fields from MMA.
- Document links are stable `wp-content/uploads/YYYY/MM/...` paths (PDF for bases/results/resoluciones, DOCX for annexes). The **Resolución Exenta** is the citable legal act; prefer it as provenance.
- Historical/awarded funds are reachable via the FPA hub (`/fpa/`) and FPR hub (`/fpr/`) listings (page 1 covers 2020–2026; `?page=2` and the `fondoreciclaje.mma.gob.cl` archive hold older entries). The hub listing itself is structured enough to enumerate every concurso (name, ficha URL, "POSTULACIONES DESDE EL …" date) without opening each ficha — this is the **index tier** in the extraction.
- **Named source defect:** the FPA Rapa Nui 2026 ficha prints the amount as `$ 10.000.0000` (an extra zero). Naive parsing yields $100,000,000; intended value is $10,000,000. The notebook flags this via `amount_suspect` rather than absorbing it — confirm from the Bases PDF. Treat amount strings defensively (grouping check).
- **Two extraction tiers** (see notebook): *detailed* rows parse the full Antecedentes table (current cycle); *index* rows carry name/URL/open-date/status from the hub listing for the 2020–2025 archive. Merge on `source_url`.

## Extraction & refresh

**How this snapshot was produced.** This source has **clean, parseable HTML tables**, so it is extracted **deterministically** by the notebook `cl_mma_fondos_extract_clean.ipynb` (a two-tier parser: per-ficha 'Antecedentes Generales' tables + a hub index of every concurso). That notebook is the primary method here; the LLM prompt below is a fallback for pages the parser doesn't cover. The committed `data/cl_mma_fondos_v1.csv` is the resulting snapshot. (The same prompt runs across all six Chile finance sources at once in the OEF harness, `reviews/oef/cl-finance-inventory/releases/v1/extract_inventory.ipynb`, if you prefer to refresh them together.)

**Source pages for this dataset:**
- https://fondos.mma.gob.cl/fpa/  (FPA hub — lists all concursos)
- https://fondos.mma.gob.cl/fpr/  (FPR hub)
- per-fund ficha pages, e.g. /fpa-2026-proyectos-sustentables-ciudadanos/

**To refresh the data:** re-run `cl_mma_fondos_extract_clean.ipynb` with its live loader (it re-fetches the fichas), or use the prompt below on a fetched ficha. Spot-check the result against the page before committing, and update `status_as_of` / the capture date.

**Extraction prompt (copy-paste into any LLM):**

```text
You extract climate-relevant public FUNDING OPPORTUNITIES offered by Ministerio del Medio Ambiente (MMA) from the page text below, into JSON.

Return a JSON list — one object per distinct fund / programme / call. Use exactly these keys:
- program             : official name of the fund/programme/call
- funder_institution  : the body that funds it
- eligible_actor      : who can apply (municipality | community/citizen org | household | indigenous community | private firm | NGO | school sostenedor | ...). If it is explicitly NOT municipalities, say so.
- instrument_type     : grant | loan | guarantee | blended | technical_assistance | subsidy | equity
- amount_note         : amount / ceiling / rate as stated, keeping units (CLP, UF, US$, %); "" if not stated
- status              : open | closed | ongoing | periodic | emerging  (prefer the close DATE over section labels)
- recurrence          : annual | ongoing | sporadic | one-off
- specificity         : "sector-specific" if it targets a defined climate sector; "broad" if general-purpose (fits many sectors)
- climate_relevance   : explicit | climate-adjacent | indirect
- gpc_sectors         : list from {stationary_energy, transportation, waste, water, afolu, industry, buildings, cross_sector}, mapped from the FUNDED WORKS (not the name)
- access_pathway      : direct application | facilitated-by-city | intermediated (via banks/AE) | ...
- detail_level        : "detailed" if amount+eligibility+dates are on the page; "index" if only the programme is identified
- source_url          : the page URL

Rules: capture FACTS only — never invent amounts or dates. An annual fund that is currently closed is still recurrence=annual. Mark general-purpose funds specificity=broad. Output ONLY the JSON list.

SOURCE_URL: <paste the source URL>
PAGE_TEXT:
{PAGE_TEXT}
```

## Current approved release

Not yet promoted (awaiting your sign-off). First release **v1** is built in `releases/v1/`:

- `cl_mma_fondos_extract_clean.ipynb` — extraction notebook (block-per-parsing-note; restart-and-run-all passes). Two tiers: *detailed* (current-cycle fichas, full Antecedentes) + *index* (full FPA/FPR hub enumeration). Field values captured from the live portal 2026-06-08; a documented live-refresh path re-fetches.
- `data/cl_mma_fondos_v1.csv` — tidy output, **55 fund lines** (45 FPA, 9 FPR, 1 Recambio programme; 7 detailed + 48 index), one row per fund *line*, with broad-capture attributes (eligible_actor, amount_clp + amount_suspect flag, open/close dates, status + lifecycle + conflict flag, **recurrence + next_call_estimate**, stream, gpc_sectors, thematic_lines, instrument_type, access_pathway, Resolución Exenta provenance, source_url, detail_level).
- `data/hub_index.json` — the enumerated FPA/FPR hub listing that feeds the index tier.
- `review.md` — the release's epistemic contract: what the data does and does not support (incl. the recurrence interpretation — annual streams reopen ~Aug–Oct; special calls do not).

Recurrence note: every line is `closed` right now because these are annual funds between cycles. `recurrence` (annual / sporadic / one-off) is derived from how many of the 7 cycles (2020–2026) each stream appears in; the FPR and three core FPA lines are `annual` (next call ~Aug–Oct 2026), while special/territorial calls are one-off. See `releases/v1/review.md` for the claim/anti-claim detail.

v1 covers the full current MMA set plus the 2020–2025 archive index. To deepen: enrich index rows by fetching their fichas; pull FPA hub `?page=2+` for pre-2020; parse Bases/Resolución PDFs for exact eligibility, regional limits, and co-financing. Production approval is tracked in `catalog/index.yaml`.

Evidence tags: provenance/access/coverage **verified** (live fetch 2026-06-08); extraction logic **verified** (assertions pass, incl. the named Rapa Nui amount defect); license **partly verified** (no restrictive terms — verified; affirmative reuse grant — unanswered).
