# SUBDERE (Chile) — municipal investment funds (cl-subdere)

The Subsecretaría de Desarrollo Regional y Administrativo's municipal investment programmes relevant to climate action: PMU, PMB, the Programa de Prevención y Mitigación de Riesgos, and the Fondo de Recuperación de Ciudades. These are the backbone of how Chilean municipalities actually fund local infrastructure. Covers the municipal-infrastructure slice of need `2026-06-cl-finance-opportunities`.

## Canonical sources

- SUBDERE programme pages: https://www.subdere.gov.cl/programas (División de Municipalidades / Departamento de Inversión Local).
- Applications run through `subdereenlinea.gov.cl` (open, continuous).
- A project repository ("Banco de Proyectos", `bancodeproyectos.subdere.gob.cl`) supports PMU/PMB applications.
- Several also appear as fichas on the restricted national aggregator `fondos.gob.cl` (cite the SUBDERE page, not the aggregator).

## Why we use it

- These are the **largest, most-used municipal funding channels** — in 2022 PMU + PMB + PTRAC + PRBIPE moved ~CLP 222 billion across 2,811 projects. For a city-facing reference they are the realistic backbone.
- PMB specifically funds **sanitation, solid waste, waste valorization, and electrification** — direct water/waste/energy relevance (`gpc_sectors`).
- PMU is continuous (rolling all year), so it is almost always "available now" — useful, but see the broad-fund warning.

## License

Public information of a State body under the Ley de Transparencia (verified 2026-06-08: SUBDERE is a public service; pages carry Transparencia links, no restrictive terms-of-use and no all-rights-reserved notice). No affirmative open-data licence is stated. Handling: capture and attribute the programme facts; tag license **partly verified** (public-info verified; explicit reuse grant unanswered). This is the same posture as `cl-mma`, and unlike the restricted `fondos.gob.cl` aggregator or the AgenciaSE foundation.

## Spatial and temporal scope

National, delivered to municipalities. PMU and PMB are **continuous/rolling** (apply any time, funded subject to budget), not annual concursos. Availability is therefore effectively "open" but budget-gated. Status as captured 2026-06-08.

## Interpretation warnings

- **PMU and PMB are broad funds — the over-matching risk.** They fund almost any municipal infrastructure, so in any action↔fund matching they will match nearly everything and inflate scores. `specificity=broad` flags this: include them in the city-facing reference, but down-weight them in the fundability score (this is exactly the failure mode that broke the SSG scoring).
- **"Rolling/continuous" ≠ guaranteed money.** PMU/PMB accept applications all year but fund subject to the annual budget; an application is not an award. Don't read `status=open` as "funds available on demand".
- **Eligible actor is the municipality** (PMB also municipal associations) — these are genuinely city-applicant funds, unlike FPA (community orgs) or Casa Solar (households).
- **Climate relevance is mostly adjacent, not explicit.** PMU/FRC are general infrastructure; PMB has the clearest direct hooks (waste/water/energy); PMR is adaptation (risk). Read `climate_relevance` per row and tag the action's sector via the funded works, not the programme name.

## Parsing notes

- No single parseable fund portal; v1 is **hand-curated** from SUBDERE programme pages (captured 2026-06-08), one row per programme with `source_url` provenance.
- **Access caveat:** `subdere.gov.cl` was slow/timed out during capture; some fields (PMR, FRC current calls/amounts) are `detail_level=index` pending a successful fetch. Re-fetch to enrich.
- SUBDERE programme URLs are percent-encoded (accented path segments) — handle encoding when fetching.
- The detailed PMU/PMB procedures live in SUBDERE PDF manuals (linked from the programme pages) — parse those for eligibility/scoring detail.

## Extraction & refresh

**How this snapshot was produced.** The SUBDERE programme pages are thin and the detailed amounts live in PDF manuals; the site can also be slow. Rows are produced from the page text with the **extraction prompt** below (PMR/FRC are index-level pending a fuller fetch). The committed `data/cl_subdere_programs_v1.csv` is the resulting snapshot. (The same prompt runs across all six Chile finance sources at once in the OEF harness, `reviews/oef/cl-finance-inventory/releases/v1/extract_inventory.ipynb`, if you prefer to refresh them together.)

**Source pages for this dataset:**
- https://www.subdere.gov.cl/programas  (PMU, PMB, PMR, FRC)

**To refresh the data:** fetch the programmes page text, run the prompt, replace the rows in `data/cl_subdere_programs_v1.csv`. Spot-check the result against the page before committing, and update `status_as_of` / the capture date.

**Extraction prompt (copy-paste into any LLM):**

```text
You extract climate-relevant public FUNDING OPPORTUNITIES offered by Subsecretaría de Desarrollo Regional y Administrativo (SUBDERE) from the page text below, into JSON.

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

Not yet promoted. First release **v1** in `releases/v1/`: `data/cl_subdere_programs_v1.csv` (4 programmes) + `review.md`. Evidence tags: provenance/scope **verified**; amounts **unverified** (per-project, budget-dependent — not stated at programme level); license **partly verified**.
