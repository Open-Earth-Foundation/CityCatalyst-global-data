# Green Climate Fund — projects (gcf-projects)

Project-level records of **Green Climate Fund (GCF)**-funded climate programmes, from the **GCF Projects API** (`http://api.gcfund.org/v1/projects`). Global coverage, one row per Funded Activity (FP), with the country/ies, accredited entity, GCF financing, result areas, status and approval date. This is the single GCF review — the **Chile slice lives here as a filter** (`countries = Chile`), not as a separate dataset.

## Where this sits (layer & level)

**Awards/Projects layer, multilateral level, intermediated access** — see `knowledge-base/topics/climate-finance/cl-climate-finance.md` ("Funder levels"). GCF is *not* a Supply/opportunity (application) source: a city cannot apply to GCF directly, so there is no open-call catalogue. These are **projects that got funded**, reached only through a national gatekeeper plus an Accredited Entity. So for GCF, "opportunity (application)" and "projects happening" collapse into this one projects layer.

For Chile the access chain is: **NDA = Ministerio de Hacienda** (Sustainable Finance Office) → an **Accredited Entity** (IDB, CAF, FAO, IFC, or the Chilean direct-access AE **FYNSA**) → GCF Board. Tag every Chile row `access_pathway = intermediated`.

## Why we use it

- Source of GCF-funded **mitigation** projects (adaptation is out of scope — see below), with a repeatable API ingestion path.
- The non-ODA-gated multilateral Chile can actually access (unlike the DAC-gated city facilities), and it carries a genuinely city-facing programme — **FP189 E-Mobility for Sustainable Cities** (electric buses/EV fleets).
- Global portfolio enables cross-country comparison; the `countries` field makes the Chile slice a filter.

## Access & license

Public API (`http://api.gcfund.org/v1/projects`, JSON). Verified from the catalog notebook (2026-06): a single `requests.get` returns the **whole list, about 336 funded projects** (no pagination needed), with fields `ProjectsID, ApprovedRef (FP id), ProjectName, Theme (Mitigation / Adaptation / Cross-cutting), Sector, Countries (nested, ISO3), Entities (the accredited entity), Funding, ResultAreas, TotalGCFFunding, TotalValue, Status, ApprovalDate, DateClosing`. The Chile slice is a client-side filter on the nested `Countries` (ISO3 = CHL). An interactive single fetch can time out on the tool layer, but the plain API call in a notebook returns quickly. Also the **GCF Open Data Library** (`https://data.greenclimate.fund/`) and per-country pages. Public GCF programme info; confirm GCF terms-and-conditions before redistribution.

## Scope: mitigation only

We cover mitigation actions, so adaptation-only FPs are flagged out of scope (not taxonomy gaps) — e.g. Chile's **FP254** (resilient water infrastructure) is `in_scope = no`.

## Chile slice + action mapping (verified 2026-06-18)

`releases/v1/data/gcf_chile_slice.csv` — the 8 Chile entries (7 FPs + 1 readiness), hand-verified from the GCF Chile country page as a first cut pending an API pull. `releases/v1/data/gcf_chile_to_actions.csv` + `gcf_chile_analysis.ipynb` map each to the city action list at the FP grain (restart-and-run-all passes, chart inline). **3 of 8 in-scope FPs map**: FP189 → zero-emission bus fleets (`c40_0023`, high); FP120 REDD+ → reduce deforestation (`ipcc_0052`, high); FP017 solar → solar generation (`icare_0012`, medium). The rest are `none`: finance vehicles (FP151/152 Subnational Climate Fund, FP149 FI facility) are instruments not interventions; FP254 is adaptation (out of scope); the FAO readiness grant is capacity. **These are approved/under-implementation programmes, not open calls** (`application_status` per row); GCF's apply route (project cycle) is continuous/rolling.

## Interpretation warnings

- **Multi-country FP financing is not a Chile figure** — FP189's US$450M etc. are programme totals across countries; `chile_scope` flags single- vs multi-country.
- **Awarded/approved ≠ disbursed**; every Chile row is intermediated by an AE — the city is a beneficiary/partner, not the recipient.
- Mapping is link-don't-attribute at FP grain; medium/none rows await human adjudication.

## Status

This review is **self-contained** and is the one with real committed Chile data. `releases/v1/` holds `data/gcf_chile_slice.csv` (the project dataset, 8 entries hand-verified from the GCF Chile country page), `data/gcf_chile_to_actions.csv` (the crosswalk), `gcf_chile_analysis.ipynb`, `review.md` and `review.yaml`. To refresh from the API: a single `requests.get('http://api.gcfund.org/v1/projects')` returns the full ~336-project list, filter `Countries` ISO3 = CHL, then map on **`ResultAreas`** (e.g. "Energy generation and access", "Transport", "Forests and land use") — the same classification-grain approach as the FPA `clasificacion`. Production: **pending validation**. The discovery candidate `gcf-chile` (need `2026-06-cl-international-climate-finance`) is promoted here.
