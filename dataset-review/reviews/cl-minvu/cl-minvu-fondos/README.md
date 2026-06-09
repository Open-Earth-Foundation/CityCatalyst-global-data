# MINVU (Chile) — urban / green-space funding programmes (cl-minvu)

The Ministerio de Vivienda y Urbanismo's city programmes relevant to climate action: the Programa Concursable de Espacios Públicos, Parques Urbanos, Pavimentación Participativa, and the Programa de Recuperación de Barrios (Quiero Mi Barrio). Covers the urban / green-space / adaptation slice of need `2026-06-cl-finance-opportunities`.

## Canonical sources

- MINVU "Ciudad" benefit pages: https://www.minvu.gob.cl/beneficios/ciudad/ (Espacios Públicos, Parques Urbanos, Pavimentación Participativa, Recuperación de Barrios, Vialidad Urbana, Pequeñas Localidades).
- Calls are issued **per region by the SEREMI MINVU via Resolución Exenta** and published in national/regional press; municipalities apply through the SEREMI / SECPLA.
- Governing norm for Espacios Públicos: DS 312 (V. y U.), 2016.

## Why we use it

- Adds the **urban green-space / adaptation** dimension — the clearest hooks for urban-heat, stormwater, and resilience actions that MMA/energy/SUBDERE don't cover directly.
- Espacios Públicos and Parques Urbanos explicitly fund green areas, rainwater (aguas lluvias) solutions, and resilient public space; the National Urban Parks Policy names "environment, resilience and climate change" as an axis.
- Municipalities are the applicant (the alcalde presents), so these are genuinely city-actionable.

## License

Public information of a State body under the Ley de Transparencia (verified 2026-06-08: minvu.gob.cl carries Transparencia links and a Política de Privacidad, no restrictive terms-of-use, no all-rights-reserved notice). No affirmative open-data licence stated. Handling: capture and attribute programme facts; tag license **partly verified** (public-info verified; explicit reuse grant unanswered). Same posture as `cl-mma` / `cl-subdere`.

## Spatial and temporal scope

National, delivered region-by-region through SEREMI MINVU. Espacios Públicos has a clear **annual cadence**: the Llamado Regular opens ~April, the Llamado Especial ~September. Parques Urbanos construction is SEREMI-prioritised (not openly competitive); a newer conservation line is competitive. Status as captured 2026-06-08.

## Interpretation warnings

- **Espacios Públicos is annual, not rolling.** Two windows a year (Regular ~April, Especial ~September); `recurrence=annual`. A city must time applications — unlike SUBDERE's continuous PMU/PMB.
- **Page lag.** The Espacios Públicos page still headlines the 2023–2024 call; the cadence is annual, so treat the displayed call as illustrative and confirm the current Resolución Exenta with the regional SEREMI.
- **Parques Urbanos construction is not a competition you "win".** It is SEREMI-prioritised by green-area deficit / population / vulnerability; only the conservation line is competitive. Don't present construction as an open call.
- **Amounts are in UF, and bundle design+execution.** Espacios Públicos Regular ≤ UF 30,000 (design + execution), Especial ≤ UF 6,000 (execution of finished designs). Convert UF→CLP at use; don't store a fixed peso figure.
- **Climate relevance varies.** Espacios Públicos / Parques Urbanos = explicit (green/rainwater/heat); Pavimentación Participativa and Quiero Mi Barrio = adjacent (mobility / neighbourhood) — tag by the funded works.

## Parsing notes

- No single fund portal; v1 is **hand-curated** from MINVU "Ciudad" benefit pages (captured 2026-06-08), one row per programme with `source_url` provenance.
- minvu.gob.cl is server-rendered WordPress; the `/beneficios/<x>/` index pages are thin (link to a `/beneficio/ciudad/<x>/` detail page) — follow to the detail page for fields.
- Per-call specifics (dates, exact amounts, eligibility) live in each SEREMI's **Resolución Exenta** and the DS 312 norm — parse those for detail beyond the programme summary.
- `detail_level=index` rows (Parques Urbanos, Pavimentación, Quiero Mi Barrio) are programme-level; enrich from the detail page / current call.

## Extraction & refresh

**How this snapshot was produced.** MINVU 'Ciudad' index pages are thin (they link to a detail page); per-call specifics live in each SEREMI's Resolución Exenta PDF. Programme-level rows are produced from the detail pages with the **extraction prompt** below. The committed `data/cl_minvu_programs_v1.csv` is the resulting snapshot. (The same prompt runs across all six Chile finance sources at once in the OEF harness, `reviews/oef/cl-finance-inventory/releases/v1/extract_inventory.ipynb`, if you prefer to refresh them together.)

**Source pages for this dataset:**
- https://www.minvu.gob.cl/beneficios/ciudad/  (+ each /beneficio/ciudad/<x>/ detail page)

**To refresh the data:** fetch the detail page text, run the prompt, replace the rows in `data/cl_minvu_programs_v1.csv`. Spot-check the result against the page before committing, and update `status_as_of` / the capture date.

**Extraction prompt (copy-paste into any LLM):**

```text
You extract climate-relevant public FUNDING OPPORTUNITIES offered by Ministerio de Vivienda y Urbanismo (MINVU) from the page text below, into JSON.

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

Not yet promoted. First release **v1** in `releases/v1/`: `data/cl_minvu_programs_v1.csv` (4 programmes) + `review.md`. Evidence tags: provenance/scope **verified**; Espacios Públicos amounts **verified** (UF figures from the page); other amounts/dates **unverified** (per-call); license **partly verified**.
