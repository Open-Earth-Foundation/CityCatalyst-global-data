# Ministerio de Energía (Chile) — municipal energy funding programmes (cl-minenergia)

The energy-transition funding the Ministry of Energy and its implementing agency offer to (or through) Chilean municipalities: Comuna Energética, Asistencia Técnica para Municipios, Parque Solar Comunitario, Casa Solar, the Fondo de Acceso a la Energía (FAE), and Mejor Escuela. This entry covers the **municipally-relevant subset** of Min. Energía / AgenciaSE funding for the energy slice of need `2026-06-cl-finance-opportunities`. Scope was deliberately narrowed (Amanda, 2026-06-08) to programmes a municipality can apply to, run, or facilitate — excluding the many AgenciaSE courses, seals, and B2B mobility programmes.

## Canonical sources

Unlike MMA, there is **no single fund portal** — the programmes live across a ministry, a foundation, and per-programme microsites:

- Ministry policy + financing finder: https://energia.gob.cl/servicios-online/financiamiento-disponible (and `pfinanciamiento.minenergia.cl`).
- Agencia de Sostenibilidad Energética (AgenciaSE) — implementer; weekly open-calls bulletin: https://www.agenciase.org/convocatorias/ (the "convocatorias abiertas al <date>" posts give a live Nombre/Tipo/Cierre table).
- Per-programme: Comuna Energética `comunaenergetica.cl`, Casa Solar `casasolar.cl`, FAE `chileatiende.gob.cl/fichas/36666...` + `energia.gob.cl/fae`, Mejor Escuela `mejorescuela.cl`.
- Applications for several run through the restricted national aggregator `fondos.gob.cl`.

## Why we use it

- Adds the **energy** slice to the inventory (need `2026-06-cl-finance-opportunities`) — mitigation-relevant (EE / ERNC) programmes that complement MMA's environment funds with little overlap.
- Several are genuinely municipal: Comuna Energética and Asistencia Técnica have municipalities as the direct applicant; Parque Solar Comunitario and Casa Solar run through the comuna; Mejor Escuela reaches municipal school sostenedores.
- Maps cleanly to `gpc_sector = stationary_energy`, useful for scoring energy actions.

## License

Mixed, and a step more cautious than MMA (verified 2026-06-08):

- Ministry pages (`energia.gob.cl`) and ChileAtiende fichas are ordinary public information (Ley de Transparencia); ChileAtiende additionally publishes a developer API and its own terms.
- **AgenciaSE is a "Fundación de derecho privado, sin fines de lucro"** — its sites (`agenciase.org`, `comunaenergetica.cl`, `casasolar.cl`) carry an explicit **"© Todos los derechos"** notice and a privacy policy, i.e. all-rights-reserved, not an open licence. AgenciaSE is nonetheless a Transparency-subject body (regulated org FU014) administering public funds, so the underlying programme facts (name, eligible actor, amount, dates, links) are public-interest facts.
- **Handling:** capture and attribute the factual programme data; do not reproduce large verbatim text from AgenciaSE sites; obtain a legal confirmation before redistributing AgenciaSE content at scale. Not the hard prohibition that disqualified `fondos.gob.cl`, but tag license **partly verified / unanswered** for the affirmative reuse grant.

## Spatial and temporal scope

National, delivered comuna-by-comuna (enrolment or per-comuna calls). These are mostly **standing programmes**, not annual concursos with fixed cycles — availability is per-comuna and rolling (Casa Solar, Comuna Energética) or sporadic (FAE: last call closed 2024-07-20). Re-check the AgenciaSE bulletin for what is open in a given week. Status as captured 2026-06-08.

## Interpretation warnings

- **Programmes, not annual concursos.** Don't expect MMA-style fixed open/close cycles. Most are "ventanilla abierta" / rolling / per-comuna; status is genuinely point-in-time — read `status_as_of` and re-check the AgenciaSE bulletin.
- **Eligible actor is not uniformly "municipality."** Comuna Energética / Asistencia Técnica = municipality applies; Casa Solar = households (municipally facilitated); FAE = community-role orgs (indigenous communities, juntas de vecinos, NGOs, bomberos) explicitly **not** municipalities; Parque Solar = via municipality; Mejor Escuela = school sostenedor. Read `eligible_actor` per row; do not generalise.
- **Several are enabling, not cash.** Comuna Energética and Asistencia Técnica are mostly technical assistance / certification with co-financing windows attached — not a direct grant. `instrument_type` records this.
- **FAE is dormant.** Created 2014 as a pilot; the most recent call closed July 2024. Treat as `recurrence=sporadic`, not reliably annual.
- **Implementer ≠ funder.** Money is public (Min. Energía), but delivery and most web content are AgenciaSE (a private-law foundation) — relevant for both citation and licence.

## Parsing notes

- No single portal to scrape: v1 is **hand-curated** from the official programme pages (captured 2026-06-08), one row per programme, with `source_url` provenance per row. This differs from `cl-mma` (single parseable portal); recorded so a future maintainer doesn't look for a portal that isn't there.
- The one harvestable live list is the AgenciaSE weekly bulletin (`agenciase.org/.../convocatorias-abiertas-al-<date>`), a markdown/HTML table of Nombre / Tipo / Cierre — use the latest dated post for current open calls.
- The Ministry financing finder (`energia.gob.cl/servicios-online/financiamiento-disponible`) is server-rendered and paginated (`?page=N`) — a candidate index source if scope is later widened beyond municipal.
- AgenciaSE assets are served from a DigitalOcean Spaces bucket (`agenciase.sfo3.digitaloceanspaces.com`); programme microsites are WordPress.

## Extraction & refresh

**How this snapshot was produced.** There is no single portal — the programmes live across AgenciaSE microsites (mostly server-rendered WordPress). Each page is fetched and turned into rows by the **extraction prompt** below. The committed `data/cl_minenergia_programs_v1.csv` is the resulting snapshot. (The same prompt runs across all six Chile finance sources at once in the OEF harness, `reviews/oef/cl-city-action-fundability/releases/v1/extract_inventory.ipynb`, if you prefer to refresh them together.)

**Source pages for this dataset:**
- https://www.comunaenergetica.cl/sobre-comuna-energetica/
- https://www.casasolar.cl/
- https://www.chileatiende.gob.cl/fichas/36666-fondo-de-acceso-a-la-energia-fae
- https://www.mejorescuela.cl/
- https://www.agenciase.org/convocatorias/

**To refresh the data:** fetch each source page's text, run the prompt, replace the rows in `data/cl_minenergia_programs_v1.csv`. Spot-check the result against the page before committing, and update `status_as_of` / the capture date.

**Extraction prompt (copy-paste into any LLM):**

```text
You extract climate-relevant public FUNDING OPPORTUNITIES offered by Ministerio de Energía / Agencia de Sostenibilidad Energética (AgenciaSE) from the page text below, into JSON.

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

Not yet promoted (awaiting sign-off). First release **v1** in `releases/v1/`: `data/cl_minenergia_programs_v1.csv` (6 municipally-relevant programmes) + `review.md` (epistemic contract). Evidence tags: provenance/scope **verified** (live fetch 2026-06-08); per-programme amounts mostly **unverified** (program-level pages rarely state a single figure — would come from each call's bases); license **partly verified** (Ministry public-info verified; AgenciaSE affirmative reuse grant unanswered).
