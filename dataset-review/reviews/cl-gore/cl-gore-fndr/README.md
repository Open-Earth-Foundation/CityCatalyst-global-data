# Gobiernos Regionales (Chile) — FNDR regional funds (cl-gore-fndr)

The regional-tier funding that Chilean municipalities access through their Gobierno Regional: the Fondo Nacional de Desarrollo Regional (FNDR) and its instruments — regional investment (Glosa 03 / SNI), FRIL (minor communal works), the 8% activity subvención (with an environmental line), and FRPD (productivity/investment). This is the **regional tier** of need `2026-06-cl-finance-opportunities` — explicitly deferred in the original national-first scope, now added because GORE/FNDR is the single largest channel of municipality-accessible public investment.

## Canonical sources

- SUBDERE — FNDR framing (Glosa 03): https://www.subdere.gov.cl/content/glosa-03-provisi%C3%B3n-fondo-nacional-de-desarrollo-regional-fndr
- Each of the 16 Gobiernos Regionales runs its own calls of the same instruments on its own site (e.g. `gobiernosantiago.cl/fndr/`, `goremaule.cl`, `goreloslagos.cl/fondos_concursables/`, `fndr8.gorearaucania.cl`) and via `fondos.gob.cl` (cite the GORE page, not the restricted aggregator).
- FNDR investment projects run through the Sistema Nacional de Inversiones (SNI / BIP) and require a "Recomendación Satisfactoria (RS)".

## Why we use it

- **The biggest regional channel.** FNDR is how a large share of public infrastructure actually gets funded in the regions; FRIL specifically is the municipal small-works fund — both are highly city-accessible.
- Adds the **regional tier** the national-only inventory was missing, and tests the schema's `tier` concept (recorded in `notes`).
- The 8% line includes an explicit **Medio Ambiente y educación ambiental** stream.

## License

Public information of State bodies under the Ley de Transparencia (GOREs and SUBDERE are public services; their sites carry Transparencia links, no restrictive terms-of-use, no all-rights-reserved notice — verified 2026-06-08 on the GORE/SUBDERE pages). No affirmative open-data licence stated. Handling: capture and attribute the programme facts; tag license **partly verified** (public-info verified; explicit reuse grant unanswered). Same posture as `cl-mma` / `cl-subdere` / `cl-minvu`. Note: do not source these from `fondos.gob.cl` (restricted) — use the GORE/SUBDERE pages.

## Spatial and temporal scope

National in structure, **regional in delivery**: 16 Gobiernos Regionales each run their own calls of the same instruments, with region-specific amounts, dates, and (for the 8%) lines. Curated here at the *instrument* level, one row per instrument, not per region. FNDR/FRIL operate on the annual budget; the 8% is annual (2026 calls ran early 2026). Status as captured 2026-06-08.

## Interpretation warnings

- **Regional tier — amounts and dates vary by GORE.** A single row stands for 16 regional variants. The `amount_note` figures are illustrative (e.g. FRIL ≤ ~CLP 180M; FRPD up to ~CLP 300M in Arica); confirm with the specific GORE.
- **Mostly broad funds.** FNDR investment, FRIL, and FRPD fund almost any regional/municipal project — `specificity=broad`, so they are capped at Moderate in the fundability score (the over-matching control). They are valuable for the city-facing reference but must not inflate scoring.
- **Eligible actor differs by instrument.** FRIL and FNDR investment = municipality/region; the 8% Medio Ambiente line = **NGOs, not municipalities**; FRPD = firms/legal persons. Read `eligible_actor` per row.
- **FNDR investment is not a quick grant.** Projects need SNI evaluation and an RS recommendation — a real lead time, not an open application window.
- **The 8% environment line funds activities, not infrastructure** (6-month activities, ≤ ~CLP 30M, max 2 per org) — useful for environmental education/community works, not capital projects.

## Parsing notes

- No single portal; v1 is **hand-curated** at instrument level from SUBDERE + representative GORE pages (captured 2026-06-08), one row per instrument with `source_url` provenance.
- To extend to per-region granularity, the 16 GORE sites + their `fondos.gob.cl` fichas are the index sources; the 8% is the most standardised (same glosa across regions).
- FRPD/8% specifics (amounts, dates, lines) live in each GORE's Resolución/bases — parse those for detail beyond the instrument summary.
- `detail_level=index` for FRPD (region-dependent specifics pending).

## Extraction & refresh

**How this snapshot was produced.** One row per FNDR *instrument* (the same instrument is delivered by all 16 GOREs). Rows are produced from the SUBDERE + representative GORE pages with the **extraction prompt** below; amounts are illustrative (vary by region). The committed `data/cl_gore_fndr_programs_v1.csv` is the resulting snapshot. (The same prompt runs across all six Chile finance sources at once in the OEF harness, `reviews/oef/cl-city-action-fundability/releases/v1/extract_inventory.ipynb`, if you prefer to refresh them together.)

**Source pages for this dataset:**
- https://www.subdere.gov.cl/content/glosa-03-provision-fondo-nacional-de-desarrollo-regional-fndr
- GORE sites, e.g. gobiernosantiago.cl/fndr/, goremaule.cl (FNDR 8%), gorearica (FRPD)

**To refresh the data:** fetch the SUBDERE/GORE page text, run the prompt, replace the rows in `data/cl_gore_fndr_programs_v1.csv`. Spot-check the result against the page before committing, and update `status_as_of` / the capture date.

**Extraction prompt (copy-paste into any LLM):**

```text
You extract climate-relevant public FUNDING OPPORTUNITIES offered by Gobiernos Regionales (FNDR) from the page text below, into JSON.

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

Not yet promoted. First release **v1** in `releases/v1/`: `data/cl_gore_fndr_programs_v1.csv` (4 instruments) + `review.md`; the extraction prompt + refresh steps live in the "Extraction & refresh" section above. Evidence tags: provenance/scope **verified**; amounts **illustrative/region-varying**; license **partly verified**.
