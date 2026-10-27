# AdaptaBrasil indicator hierarchy — levels

The raw hierarchy has up to 6 positional levels, but we now also maintain a modeled semantic view:
- PT: `data/adapta_indicator_hierarchy_modeled.csv`
- EN: `data/adapta_indicator_hierarchy_modeled_en.csv`

In this modeled view, semantics are stable (`sector`, `risk`, `risk_component`, `impact_chain_*`, `base_indicator`) and the base indicator is always the deepest non-empty node from the raw path.

- **Modeled `sector` (raw L1).** Strategic sector (Recursos hídricos, Biodiversidade, Desastres geo-hidrológicos, Segurança alimentar, Segurança energética, Saúde, Infraestrutura, etc.).
- **Modeled `risk` (raw L2).** Named risk / impact-chain root within each sector (e.g., Risco de estresse hídrico, Integridade do bioma, Deslizamento de terra).
- **Modeled `risk_component` (usually raw L3).** Standardized to Ameaça / Exposição / Vulnerabilidade (Hazard / Exposure / Vulnerability) when applicable.
- **Modeled `impact_chain_1..3` (raw L4-L6 where applicable).** Intermediate branch levels between `risk_component` and the leaf.
- **Modeled `base_indicator` (dynamic leaf).** Always the deepest non-empty node in the original path (can be raw L3, L4, L5, or L6).

**Key takeaway:** the modeled files are the preferred semantic layer for downstream use. Key off `sector` + `risk` + `risk_component` + `base_indicator`; use `impact_chain_*` only as optional intermediate context.

## Methodology framing — impact chain

AdaptaBrasil follows the **impact chain (cadeia de impacto)** methodology (GIZ Vulnerability Sourcebook / IPCC AR5 lineage). The hierarchy *is* the impact chain, read bottom-up:

raw indicator (leaf) → thematic group → IPCC component (Hazard / Exposure / Vulnerability) → composite risk index (L2) → strategic sector (L1)

Each non-leaf node is a weighted aggregation of its children, so an L2 risk score is the roll-up of all L6 leaves beneath it. The `/api/info` endpoint with `nextlevel` / `lastlevel` exposes how children compose into a parent.

## Observations and caveats

- **`risk_component` is not always populated.** In most chains it is standardized to Ameaça/Exposição/Vulnerabilidade (Hazard/Exposure/Vulnerability), but some direct-leaf cases skip this split and map directly to `base_indicator` (e.g., Energy Security indicators such as solar, hydropower, wind potential, and cooling demand). Treat `risk_component` as "present when IPCC decomposition applies," not as a mandatory field.
- **Not all sectors resolve to municipality.** Infrastructure-related sectors are missing city-level aggregation — their indicators typically resolve at asset, basin, or state level because the underlying assets don't obey municipal boundaries.
- **Scenarios vs indicator metadata.** Indicator metadata lists projection years but does **not** attach the `scenario_id` required by the municipio map endpoint for each indicator/year. The platform still exposes a finite set of candidate scenario ids (see `data/adapta_scenarios_extracted.csv`), so a discovery pass must try those ids against each indicator and future year. That brute-force sweep is slow, stresses the public API (timeouts, intermittent `403`s), and in practice needed throttling and restarts. The exhaustive probe is logged in `sample/indicators/adapta_request_coverage.csv` (**14,708** rows, including duplicate rows from reruns; **~3.7k** distinct `(indicator_id, year, scenario)` URLs when deduplicated).
- **Reference allowlist.** For ongoing downloads or ingestion, use `data/indicator_scenario_combination.csv` instead of exercising the full Cartesian grid: it keeps only combinations that returned HTTP **200** with a non-empty municipal row count. The file has **1,184** rows; after deduplication by `(indicator_id, year, scenario)` there are **~543** distinct combinations (the extra rows mirror the same rerun duplication pattern as the coverage log). That is roughly **~12×** fewer HTTP rows to replay than the **14,708**-row coverage log, and far fewer than naively hitting every scenario for every indicator.

## Serving strategy recommendation (API vs DB)

For an app that consumes AdaptaBrasil data primarily by **city**, the recommended pattern is to ingest Adapta API data into our database and serve from modeled tables, rather than querying the public API directly at runtime.

- The Adapta API is mostly **indicator-centric** (Brazil-wide payloads per indicator), while the app access pattern is **city-centric** (all indicators for one city).
- Runtime API usage would still require effectively full extraction and heavy reshape logic on demand.
- A DB-first pipeline lets us keep a stable semantic model (`sector`, `risk`, `risk_component`, `impact_chain_*`, `base_indicator`) and app-ready contracts.
- Because the source API is active, run a **daily full-refresh** ingestion and replace serving tables atomically to keep data synchronized.
- Start with full replacement for simplicity and reliability; optimize to incremental refresh only if runtime/cost constraints require it.