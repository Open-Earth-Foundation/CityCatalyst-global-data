# Chile BIP investment initiatives — climate-relevant subset (cl-bip-projects)

Public-investment initiatives (proyectos, programas, estudios básicos) registered in Chile's **Banco Integrado de Proyectos (BIP)**, the project registry of the **Sistema Nacional de Inversiones (SNI)**, administered by the **Ministerio de Desarrollo Social y Familia (MDSF)**. This entry sources the data **directly from the official open-data bulk release (BIDAT)** rather than from third-party curation, and scopes it to climate-relevant initiatives.

## Relationship to cl-ssg-projects

`reviews/cl-ssg/cl-ssg-projects` is a climate-relevant subset of the same BIP universe, but obtained by extracting **per-project FICHA IDI PDFs** from the BIP Consulta tool and parsing them (a multi-step PDF→JSON→table pipeline). This entry exists to remove that dependency: the same underlying data is published in bulk (RData/CSV) under an explicit open licence, so it can be ingested directly and refreshed without scraping or PDF parsing. Treat `cl-ssg-projects` as the legacy PDF-derived view and this as the canonical-source view.

## Canonical sources

- **BIDAT (Banco Integrado de Datos)** — open-data portal: https://bidat.gob.cl/directorio/Inversi%C3%B3n%20p%C3%BAblica/evaluacion-social-de-inversiones
  - *Iniciativas de inversión del BIP, histórica* (RData): https://bidat.gob.cl/details/ficha/dataset/proyectos-de-inversion-rdata
  - *Iniciativas de inversión del BIP, por años* (annual CSV, latest cut 31-03-2026): https://bidat.gob.cl/details/ficha/dataset/registro-de-proyectos-de-inversion
- **SNI Datos Abiertos**: https://sni.gob.cl/datosabiertos/
- **BIP Data** (download portal): https://bipdata.ministeriodesarrollosocial.gob.cl/acerca/descarga
- **BIP Consulta** (public per-project lookup + Excel export, no login): https://bip.ministeriodesarrollosocial.gob.cl/bip2-consulta/

## Access

- **Bulk download — open, no account.** Historical (RData) and annual (CSV) bases are published on BIDAT/SNI Datos Abiertos in open formats. This is the intended ingestion path.
- **BIP Consulta — open, no account.** Per-project FICHA IDI consultation with Excel export and currency conversion. This is where the `cl-ssg-projects` PDFs came from.
- **Full BIP platform** (`bip2-trabajo`) — requires institutional credentials issued by MDSF/regional SEREMI; needed only for *registering/editing* initiatives, not for reading.

## License

**Creative Commons Attribution 4.0 (CC BY 4.0)** — stated on the BIDAT historical dataset page (published 2024-01-01): https://creativecommons.org/licenses/by/4.0/deed.es. Reuse and redistribution permitted with attribution. Portal terms of use: https://bidat.gob.cl/terminos-de-uso. Evidence tag: license **verified** (explicit CC BY 4.0 on the canonical bulk dataset) — a stronger footing than the SSG PDFs, which carried no embedded licence.

## Why we use it

- **Direct, licensed, refreshable** — replaces the SSG PDF-scraping pipeline with an open bulk download under CC BY 4.0.
- **Comprehensive project universe** — every public investment initiative seeking State financing, with sector/subsector, location (region/comuna), financing source, cost, stage, RATE evaluation result, and formulating institution.
- **Climate signal** — transport, water, environment, housing/urban, and energy initiatives map to GPC sectors; the climate-relevant subset supports project↔mitigation-action matching (see `cl-ssg-legal-signals` actions library).

## Spatial and temporal scope

National, delivered to regions/comunas. Bulk data covers **all initiatives 2009–present** (annual cuts; historical base). This entry's scope is the **climate-relevant subset** of that universe (climate relevance applied as a downstream classification, mirroring the SSG intent but sourced from BIDAT).

## Record structure (FICHA IDI)

Each initiative carries: `código BIP` (unique correlative id), `nombre`, `tipología` (proyecto / programa / estudio básico), `sector` / `subsector`, `etapa actual` (perfil / prefactibilidad / diseño / ejecución), `RATE` evaluation result (e.g. RS), `región` / `comuna`, `fuente financiera` (F.N.D.R. / Sectorial / Empresa / Municipal), `costo total`, and `institución formuladora`. The bulk tables expose these as columns directly — no PDF parsing required.

## Current release

**v1** (`releases/v1/review.md`) — **scaffold only**: source, access, licence and structure documented; the RData/CSV bulk files are **not yet downloaded** into the repo. Next step is to fetch a release cut from BIDAT, apply the climate-relevance filter, and commit the resulting table + a `data/` sample. Evidence tags: provenance/scope **verified**; license **verified**; data contents **not yet captured**.

## Refresh

To produce a data release: download the latest annual CSV (or historical RData) from BIDAT, filter to climate-relevant sectors/subsectors, and commit the table under `releases/v1/data/` with `source_url` provenance and the BIDAT cut date. Re-run when a new annual cut is published.
