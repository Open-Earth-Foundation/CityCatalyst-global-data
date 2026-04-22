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
- **Scenario ID ambiguity.** The scenario number needed to call the projections API is not exposed in the metadata, and inspection of the web app suggests optimistic and pessimistic projections may be served from the same `scenario_id`. Possibly the optimistic/pessimistic distinction is encoded elsewhere (the `pessimist` 0/1 column in the indicator response is a candidate) rather than via `scenario_id`. Needs validation before production ingestion.

## Serving strategy recommendation (API vs DB)

For an app that consumes AdaptaBrasil data primarily by **city**, the recommended pattern is to ingest Adapta API data into our database and serve from modeled tables, rather than querying the public API directly at runtime.

- The Adapta API is mostly **indicator-centric** (Brazil-wide payloads per indicator), while the app access pattern is **city-centric** (all indicators for one city).
- Runtime API usage would still require effectively full extraction and heavy reshape logic on demand.
- A DB-first pipeline lets us keep a stable semantic model (`sector`, `risk`, `risk_component`, `impact_chain_*`, `base_indicator`) and app-ready contracts.
- Because the source API is active, run a **daily full-refresh** ingestion and replace serving tables atomically to keep data synchronized.
- Start with full replacement for simplicity and reliability; optimize to incremental refresh only if runtime/cost constraints require it.

## Next steps

1. **Validate the scenario API.** The web app appears to serve optimistic and pessimistic projections from the same `scenario_id`, and the scenario parameter isn't exposed in indicator metadata. Confirm how the switch works via direct API testing and raise with MCTI if it looks like a bug. Blocks the final ingestion schema.
2. **Review the methodology documents.** Pull the official MCTI methodology and capture advantages '/methodolgy' (subnational resolution, standardized impact-chain framework, CCRA alignment) and limitations (infrastructure sectors without municipal resolution, scenario coverage, vintage). All review insights to be a markdown in the same directory.
3. **Design the city adatpa risk API table.** Define the `global-api` table schema and API route around a city access pattern. The current expectation is to expose `sector`, `risk`, and `risk_component`; however, prefer including the full modeled structure now (including impact-chain and base-indicator fields) if implementation effort is similar, to avoid future requirement gaps and rework.
4. **Write the knowledge-base markdown.** Explain what AdaptaBrasil measures, how to interpret a score, and how to trace from a risk score to its driver indicators. Depends on #2 for framing and on #1 for any projections content.
