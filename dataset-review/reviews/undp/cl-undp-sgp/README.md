# GEF Small Grants Programme — Chile (cl-undp-sgp)

Community-scale environmental grants made under the **GEF Small Grants Programme (SGP)**, implemented by **UNDP** and funded by the **Global Environment Facility (GEF)**: small grants (standard ceiling **up to US$50,000**) direct to CBOs, NGOs, and indigenous/community organisations for biodiversity, land-degradation, climate-change, and chemicals-and-waste projects. This entry adds the **multilateral / community-enabler** slice that need `2026-06-cl-finance-opportunities` flagged as gap 3 ("Multilateral / bilateral tier — flagged in v1, never ingested"), and which `gaps.md` named as *the most directly city/community-accessible* multilateral source.

It is **dual-layer**: the programme itself is a **supply** instrument (an enabler/intermediated funding channel a city can point local organisations to), and the SGP project database is an **awards / revealed-fundability** archive (one row per funded community project) — the repo's **second awards dataset after `cl-conaf-bn-awards`**, and the first to carry waste / biodiversity / community-energy precedent. See the climate-finance concepts note for the supply vs awards distinction.

> **Status: discovery scaffold (not built, not promoted).** This README captures canonical sources, scope, licence, and the build plan. No `releases/` yet. Headline finding: the SGP portal *country snapshot* shows the programme closed in 2012, but that snapshot is **stale** — Chile is one of 11 countries **re-included in GEF-8** and the programme is **live again under OP8 (2025–2029)**, with a confirmed **PPD Chile 2025 grant round (submission deadline 31 October 2025**, 2-year projects). So this is **both** a *live, recurring supply channel* and a *historical precedent archive* (260 projects, 1994–2012). That dual nature is the reason it's worth a review (see Interpretation warnings).

## Canonical sources

- SGP Chile country page (legacy snapshot 1994–2012, areas of work, documents): https://sgp.undp.org/component/countrypages/?view=countrypage&country=35&Itemid=271
- UNDP Chile — PPD / SGP OP8 programme & 2025 call (live channel): https://www.undp.org/es/chile (search "Programa de Pequeñas Donaciones"); 2025 round FAQ: https://www.undp.org/sites/g/files/zskgke326/files/2025-08/respuestas_preguntas-frecuentes-ppd-2025_0.pdf
- All Chile projects (the awards archive): https://sgp.undp.org/spacial-itemid-projects-landing-page/spacial-itemid-project-search-results.html?view=allprojects&CountryID[0]=CHI&from_country_page=1
- Active Chile projects only: same URL with `&pstatus=cue`
- Programme rules (ceiling, eligibility, how to apply): https://sgp.undp.org/about-us-157/grant-eligibility.html and https://sgp.undp.org/about-us-157/how-to-apply.html
- GEF programme context + Operational Phase 8: https://www.thegef.org/what-we-do/topics/gef-small-grants-program and https://www.thegef.org/projects-operations/projects/11285

## Why we use it

- Fills the **multilateral / community-enabler** gap absent from finance-inventory v1: the inventory is entirely national/regional public funders; SGP is the first international, community-facing channel.
- **Second awards layer.** It attacks the fundability model's worst coverage hole — *75 / 102 actions have no award precedent* (currently AFOLU-only, all from CONAF). SGP awards extend revealed precedent into **waste**, **biodiversity / nature-based AFOLU**, and **community energy**.
- Explicit climate + environment relevance: SGP focal areas map to GPC sectors — Biodiversity & Land Degradation → `afolu`; Climate Change (mitigation) → `afolu` / `stationary_energy` / cross; Chemicals & Waste → `waste`. (Climate Change *Adaptation* projects are present in the Chile portfolio but **out of scope** for this review per current finance-workstream focus.)

## License

GEF/UNDP is a multilateral public body; SGP programme facts and project records are published for public information on the SGP portal. Standard public-info treatment: capture and attribute to "UNDP GEF Small Grants Programme". **Two checks before redistribution:** (i) confirm the SGP portal terms of use carry no restrictive aggregator clause (the data is presented as public monitoring output — "Quality assured data from SGP's annual monitoring process, 2024" — but verify); (ii) the per-project records may name grantee organisations and contacts — treat any personal data the same way `cl-conaf-bn-awards` does (strip before commit). Licence evidence tag: **to verify** at build.

## Spatial and temporal scope

Two eras:

- **Legacy programme 1994–2012** — per the portal snapshot (source: SGP annual monitoring, 2024): **260 total projects** (257 GEF + 3 non-GEF); **US$ 7,024,145** GEF grant amount; US$ 472,138 co-financing in cash; US$ 5,312,939 in kind. Areas of work: Biodiversity, Chemicals & Waste, Climate Change, Climate Change Adaptation, Land Degradation, Multifocal. This is the **awards archive**.
- **OP8 programme 2025–2029** — reactivated under GEF-8; a Chile grant round ran in 2025 (submission deadline 31 Oct 2025, 2-year projects). This is the **live supply** line; project counts/amounts will accrue as OP8 reports.

Geographic resolution is **project-level (community/locality)**; whether records resolve to comuna or only to region must be confirmed when the project list is extracted (the CONAF awards set, by comparison, resolves only to region).

## Interpretation warnings

- **The portal close-year (2012) is stale — don't read it as "dead".** The SGP country snapshot still shows the legacy programme closing in 2012, but Chile was re-included in GEF-8 and a **PPD Chile 2025 round ran (deadline 31 Oct 2025)**. Treat the 260-project figure as the *legacy archive*, and carry a *separate live OP8 line*. Tag the legacy rows `status = closed (legacy)` and the OP8 line `status = recurring (OP8)`.
- **Two record sets, don't merge them.** The 1994–2012 archive and the OP8 (2025–) awards are different programme eras; keep an `era` / `operational_phase` field so they aren't conflated in counts or amounts.
- **OP8 cadence still firming up.** A 2025 Chile round is confirmed; whether it repeats annually through 2029 and the exact OP8 grant ceiling for Chile should be confirmed against the live UNDP Chile call before surfacing a "next deadline".
- **Not municipality-eligible.** Grantees are CBOs, NGOs, and community/indigenous organisations — not the municipality. In the fundability FINANCE layer (which counts only the 26 municipality-eligible funds) SGP is **city-as-enabler / intermediated**: it adds a *route option and precedent*, not to the municipal-eligible supply count. Tag `eligible_actor` and `access_pathway = intermediated` deliberately.
- **Grant ceiling is per-project, not a fund total.** Standard SGP grants are up to US$50,000 (strategic projects can be larger); don't read the US$7.0M country total as a project size.
- **Co-financing inflates headline value.** The US$7.0M GEF figure is separate from the ~US$5.8M co-financing; keep GEF grant, cash co-finance, and in-kind co-finance in distinct fields.

## Parsing notes

- The SGP portal is **JavaScript-rendered** — a plain HTTP fetch of the project-search page returns an empty shell. The country *snapshot* page does render server-side (used for the figures above), but the **per-project list needs a JS-capable retrieval** (Claude-in-Chrome / a rendered scrape), not WebFetch. This is the main extraction cost and the reason this is scoped as a build task, not a hand-curate.
- A back-end DB admin link is exposed on the country page footer (`/intranet/admin.cfm`) — **not** a usable data source (auth-walled, internal); ignore it.
- Expect per-project fields: title, grantee org, focal area, GEF grant, co-financing, status, start/end, locality. Map focal area → `gpc_sectors`; flag adaptation-only projects for exclusion.

## How this would be produced (build plan)

1. **Supply row(s)** — hand-curate the *programme* as inventory rows: the **OP8 live line** (`status = recurring`, standard SGP grant, 2025 round = precedent for cadence) and optionally a legacy line for context. Same pattern as the other `*-fondos` reviews. Feeds `oef/cl-city-action-fundability` as an enabler/intermediated, non-municipality-eligible channel.
2. **Awards layer** — extract the Chile project list (~260 rows) via a JS-capable fetch of the all-projects URL; de-identify any grantee personal data; map focal area → GPC sector; emit `releases/v1/data/cl_undp_sgp_awards_projects.csv` + an `extract_clean.ipynb`, mirroring `cl-conaf-bn-awards`. Drop adaptation-only rows or tag them `out_of_scope`.
3. **Validate** — assert row count vs the portal's 260, US$ totals reconcile to the snapshot (7.0M GEF), no PII committed, focal-area → sector mapping complete.

## Relationship to other datasets

- **`oef/cl-city-action-fundability`**: receives the SGP supply row(s) (enabler/intermediated tier).
- **`cl-conaf/cl-conaf-bn-awards`**: the sibling awards dataset (CONAF Bosque Nativo). SGP is the second awards layer; both are private/community applicant universes, so relate to the BIP public-investment pipeline only at the (region/comuna, sector) aggregate level.
- **`gcf/gcf-projects`, `idb/idb-projects`, `world-bank/world-bank-projects`**: adjacent multilateral reviews; SGP is the community-scale, most city-accessible end of that tier.
- **Discovery need** `dataset-discovery/needs/2026-06-cl-finance-opportunities`: this review answers gap 3; promote the `gcf-chile`/multilateral candidate note to reference `cl-undp-sgp` once built.

## Current approved release

None — discovery scaffold. First release will be **v1** in `releases/v1/` (supply rows + the ~260-row de-identified awards CSV + `extract_clean.ipynb` + `review.md`). Evidence tags so far: legacy-archive figures (260 projects, US$7.0M, 1994–2012) **verified** (portal, SGP 2024 monitoring, captured 2026-06-17); OP8 reactivation + 2025 Chile round (deadline 31 Oct 2025) **verified** (GEF-8 country list + UNDP Chile 2025 call); OP8 cadence through 2029 and exact Chile grant ceiling **to confirm**; per-project geographic resolution, licence terms, and PII content **to verify** at build.
