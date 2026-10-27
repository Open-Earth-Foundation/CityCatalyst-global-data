# CORFO (Chile) — climate finance instruments (cl-corfo-finance)

CORFO (Corporación de Fomento de la Producción) is Chile's economic-development agency, and its climate-relevant instruments fund **firms** through **loans, guarantees, co-financing and blended finance** — Crédito Verde, Programa Expande, CORFO guarantees, the green-hydrogen facility, and Innova R&D. Added because the SSG-vs-ours gap analysis showed CORFO was the single largest missing institution (45 SSG rows) and the inventory was 93% grants — CORFO fills the **debt/blended instrument** tier and the **private-firm** actor.

## Canonical sources

- CORFO programmes & calls: https://www.corfo.cl/sites/cpp/programasyconvocatorias (redirects to `corfo.gob.cl`).
- Per-instrument pages, e.g. Crédito Verde: https://www.corfo.cl/sites/cpp/convocatorias/movil/credito_verde
- Green-hydrogen fund: https://corfo.cl/sites/cpp/sala_de_prensa/nacional/19_06_2023_fondo_hidrogeno_verde

## Why we use it

- **Fills the instrument gap.** The rest of the inventory is grants; CORFO adds loans (Crédito Verde), guarantees (FOGAIN-type), blended/concessional finance (green hydrogen), and innovation co-financing — the instruments that matter for large-capital and industrial decarbonisation.
- **Covers the industry/energy supply side via the private sector** — which is where industrial-decarbonisation actions are actually implemented and financed (not by municipalities).
- Adds the `industry` GPC sector, previously a coverage gap.

## License

**Explicit licence — the first source with one.** CORFO's site carries a Creative Commons **CC BY-NC-ND 3.0** notice (`creativecommons.org/licenses/by-nc-nd/3.0/deed.es`). That is more defined than the "no licence stated" of the public-ministry sources, but it is restrictive: **NonCommercial** and **NoDerivatives**. Handling: capture and attribute the factual programme data (facts are not the copyrighted creative work), keep use non-commercial and avoid republishing derivative versions of CORFO's text; confirm with legal before any commercial or large-scale redistribution. Tag license **verified (CC BY-NC-ND 3.0)** for the site content; programme facts captured with attribution.

## Spatial and temporal scope

National (all-Chile and regional CORFO lines). Mostly **ongoing/standing** instruments (Crédito Verde, guarantees) plus annual calls (Expande) and an emerging green-hydrogen facility. Status as captured 2026-06-08.

## Interpretation warnings

- **Firm actor, not municipality.** Every CORFO instrument here targets private firms (no annual-sales cap on Crédito Verde). A municipality does **not** apply; the city role is to point local businesses / municipal enterprises here. This is why CORFO improves *supply* coverage for industry/energy but does not raise a *city's* coverage label (the actor doesn't fit) — a clean illustration that the coverage gap for industry is an **actor** gap, not a supply gap.
- **Intermediated access.** Crédito Verde and guarantees are delivered *through banks/leasing companies*, not by CORFO directly — there's a financial-intermediary step.
- **Loans/guarantees ≠ grants.** These must be repaid or are contingent; "fundability" via debt depends on the firm's bankability, a different logic from grant eligibility. Recorded in `instrument_type`.
- **Green-hydrogen facility is emerging** — a large (~US$1,000M, EIB/KfW-backed) fund phased in over time; `detail_level=index`, confirm current facility terms.
- **Guarantees and Innova are broad** (`specificity=broad`) — they enable firm credit/innovation generally, climate-relevant only for the specific project.

## Parsing notes

- The `programasyconvocatorias` listing is **JavaScript-rendered** (paginated to ~125 pages) — `web_fetch` returns a shell; enumerate with a JS-capable fetch (Chrome tools) or the per-instrument pages. v1 is hand-curated from the per-instrument pages + press (captured 2026-06-08).
- Domain redirects `corfo.cl` → `corfo.gob.cl`.
- CORFO has a documents repository (`repositoriodigital.corfo.cl`) and public reports for deeper terms.

## Extraction & refresh

**How this snapshot was produced.** CORFO's main calls list is **JavaScript-rendered** (~125 pages), so a plain fetch returns a shell — enumerate it with a JS-capable fetch (headless browser). v1 was produced from the per-instrument pages + press with the **extraction prompt** below. The committed `data/cl_corfo_programs_v1.csv` is the resulting snapshot. (The same prompt runs across all six Chile finance sources at once in the OEF harness, `reviews/oef/cl-city-action-fundability/releases/v1/extract_inventory.ipynb`, if you prefer to refresh them together.)

**Source pages for this dataset:**
- https://www.corfo.cl/sites/cpp/programasyconvocatorias  (JS-rendered list — needs a JS-capable fetch)
- https://www.corfo.cl/sites/cpp/convocatorias/movil/credito_verde
- https://corfo.cl/sites/cpp/sala_de_prensa/nacional/19_06_2023_fondo_hidrogeno_verde

**To refresh the data:** fetch each instrument page text (JS fetch for the main list), run the prompt, replace the rows in `data/cl_corfo_programs_v1.csv`. Spot-check the result against the page before committing, and update `status_as_of` / the capture date.

**Extraction prompt (copy-paste into any LLM):**

```text
You extract climate-relevant public FUNDING OPPORTUNITIES offered by Corporación de Fomento de la Producción (CORFO) from the page text below, into JSON.

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

Not yet promoted. First release **v1** in `releases/v1/`: `data/cl_corfo_programs_v1.csv` (5 instruments) + `review.md`; the extraction prompt + refresh steps live in the "Extraction & refresh" section above. Evidence tags: provenance/scope **verified**; amounts **partly verified** (Crédito Verde figures from press; others per-call); license **verified (CC BY-NC-ND 3.0)**.
