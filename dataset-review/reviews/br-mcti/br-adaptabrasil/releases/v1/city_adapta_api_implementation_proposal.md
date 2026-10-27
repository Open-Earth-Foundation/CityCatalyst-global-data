# City Adapta Risk API Implementation Proposal (manager-ready)

## Executive summary

Build a city-first AdaptaBrasil API for a practical v1 launch while keeping room for future expansion.

1. Current product expectations (`sector`, `risk`, `risk_component`), and
2. Full hierarchy detail when needed (`impact_chain_*`, `base_indicator`).

Recommendation: implement a single wide serving table for v1, then expose one primary city route with level-based output controls (`summary` and `chain`).

This approach minimizes rework, preserves source semantics, and handles known hierarchy/data-quality edge cases already observed in the release files.

---

## Inputs reviewed and what they imply

### 1) `data/adapta_indicator_hierarchy_modeled_en.csv`
- Best semantic backbone for API serving.
- Contains stable IDs and names for:
  - `sector`, `risk`, `risk_component`, `impact_chain_1..3`, `base_indicator`.
- Shows branch-specific structure where `risk_component` can be empty (structural hierarchy choice, not always data error).

### 2) `data/adapta_indicator_hierarchy.csv`
- Raw PT hierarchy by positional levels (`nome_nivel_*`, `id_nivel_*`).
- Useful as lineage/reference, but modeled_en is better for API contracts.

### 3) `data/adapta_indicators_ids.csv`
- Large metadata dictionary (`id` key) with descriptions, equations, units, scenario/time hints.
- Should be a dimension table for enrichment (avoid repeating long text in fact rows).

### 4) `data/adapta_sample_data_one_city.csv`
- Confirms value payload shape for serving:
  - city/time/scenario + hierarchy names + numeric/class values.
- Confirms two null types:
  - **structural null**: component fields empty but valid indicator value present.
  - **data-gap null**: indicator value missing + `Data unavailable`.

---

## API design goals

- City-first access pattern (app retrieves all risk data for one city quickly).
- Backward-compatible summary output while exposing full hierarchy now.
- Explicit null semantics so clients do not misinterpret empty component fields.
- Scenario and vintage transparency (do not over-harmonize `SSP`, `RCP`, `SWL`).

## Non-goals (phase 1)

- No forced cross-sector scenario normalization.
- No semantic rewriting of source hierarchy.
- No heavy analytical endpoints beyond city retrieval and filtering.

---

## Proposed data model

## Schema: `global_api`

### Table 1 (v1): `modelled.city_adapta_risk_fact`
Primary serving table for API responses (single wide/flat table for v1).

Columns:
- **City/time**
  - `actor_id` (UN/LOCODE city key)
  - `city_name`
  - `country_code` (default `BR`)
  - `timeframe` (int or text; e.g. `2020`, `2030`, `2050`)
  - `scenario` (text; source-faithful values)
  - `scenario_family` (nullable; e.g. `SSP`, `RCP`, `SWL` when available from source API)
- **Hierarchy (IDs and names in-table)**
  - `sector_id`, `sector_name`
  - `risk_id`, `risk_name`
  - `risk_component_id`, `risk_component_name` (nullable)
  - `impact_chain_id_1`, `impact_chain_name_1` (nullable)
  - `impact_chain_id_2`, `impact_chain_name_2` (nullable)
  - `impact_chain_id_3`, `impact_chain_name_3` (nullable)
  - `base_indicator_id`, `base_indicator_name`
  - `base_indicator_level` (nullable int)
- **Values**
  - `risk_value_numeric`, `risk_value_string`
  - `risk_component_value_numeric`, `risk_component_value_string` (nullable)
  - `impact_chain_1_value_numeric`, `impact_chain_1_value_string` (nullable)
  - `impact_chain_2_value_numeric`, `impact_chain_2_value_string` (nullable)
  - `impact_chain_3_value_numeric`, `impact_chain_3_value_string` (nullable)
  - `base_indicator_value_numeric`, `base_indicator_value_string`
- **Null/data quality semantics**
  - `null_type` (`none`, `structural_null`, `data_gap_null`)
  - `value_status` is derived in API responses from `null_type` for v1
- **Provenance**
  - `release_id` (FK to `modelled.dataset_release.release_id`)
  - `source_dataset` (display field; e.g. `br-mcti/adaptabrasil`)
  - `release_version` (display field; e.g. `v1`)
  - `source_vintage` (text)
  - `spatial_support_level` (`municipal`, `state`, `subsystem`, `asset`)
  - `created_at` (`TIMESTAMPTZ`, default `NOW()`)
  - `updated_at` (`TIMESTAMPTZ`, default `NOW()`, updated on upsert)

Logical uniqueness:
- (`actor_id`, `timeframe`, `scenario`, `base_indicator_id`, `risk_component_id`, `impact_chain_id_1`, `impact_chain_id_2`, `impact_chain_id_3`)

Critical indexes:
- (`actor_id`, `timeframe`, `scenario`)
- (`actor_id`, `sector_id`)
- (`actor_id`, `risk_id`)
- (`actor_id`, `timeframe`, `scenario`, `risk_component_id`)

Future note (phase 2):
- If API contracts stabilize and reuse grows, split hierarchy and metadata into dimensions to reduce duplication.

---

## Ingestion and transformation design

## Pipeline steps

1. Ingest AdaptaBrasil directly from source API on a weekly schedule.
2. Land raw payloads into `raw_data` for reproducibility and audit.
3. Transform raw payloads into staging with normalized hierarchy fields.
4. Keep only records with `spatial_support_level = municipal` for v1 serving.
5. Resolve hierarchy values using full path keys (`sector` -> `risk` -> `risk_component` -> `impact_chain_*` -> `base_indicator`) to avoid collisions.
6. Assign null semantics:
   - `structural_null` if component fields empty and base indicator numeric exists.
   - `data_gap_null` if base indicator numeric is empty and string is `Data unavailable`.
7. Upsert into `modelled.city_adapta_risk_fact`.
8. Run validation checks + publish.

## Why full-path matching is required

`base_indicator_name` is not globally unique across all sectors/risks. Use full hierarchy path keys to avoid incorrect ID mapping.

---

## API routes proposal

## Primary city endpoint (v1)
`GET /v1/cities/{actorId}/climate-risk/adapta`

Query params:
- `timeframe` (optional; default current configured year)
- `scenario` (optional; default current)
- `level` (optional):
  - `summary` (default: sector/risk/risk_component)
  - `chain` (full hierarchy detail including impact chains and base indicators)

Response shape:
- `meta`: dataset/release/scenario/timeframe/provenance
- `data`: array of rows filtered to requested level
- each row includes `null_type`; `value_status` is derived in the response layer

---

## Deferred endpoints (phase 2)

The following routes are deferred unless UI needs force earlier delivery:
- `GET /v1/cities/{actorId}/climate-risk/adapta/options`
- `GET /v1/climate-risk/adapta/dictionary`

---

## Example API behavior (null semantics)

If a row has:
- empty `risk_component_name`
- but non-empty `base_indicator_value_numeric`

then return:
- `null_type: "structural_null"`
- `value_status: "ok"` (derived in API layer)

If a row has:
- `base_indicator_value_numeric` null
- `base_indicator_value_string = "Data unavailable"`

then return:
- `null_type: "data_gap_null"`
- `value_status: "data_unavailable"` (derived in API layer)

---

## Governance and versioning

- Version API path (`/v1/...`) and keep release provenance fields in payload.
- Add `methodology_version`, `source_vintage`, `scenario_family` in metadata blocks.
- Treat hierarchy changes as data-version events (not breaking API changes unless contract changes).

---

## Risks and mitigations

- **Risk:** hierarchy join mismatches from name drift.
  - **Mitigation:** strict normalization and full-path matching + unmatched-row audit table.

- **Risk:** scenario inconsistency across sectors (SSP/RCP/SWL).
  - **Mitigation:** preserve source scenario fields; avoid forced harmonization in phase 1.

- **Risk:** misinterpretation of blank components as missing values.
  - **Mitigation:** enforce `null_type` and document semantics in API spec.

---

## Decision request

Approve implementation with:
1. A single wide v1 serving table: `modelled.city_adapta_risk_fact`,
2. A single city endpoint with a minimal parameter set (`timeframe`, `scenario`, `level`),
3. Explicit `structural_null` vs `data_gap_null` semantics,
4. Source-faithful scenario handling (`SSP`/`RCP`/`SWL`) without premature harmonization,
5. Weekly API ingestion into `raw_data` and municipal-level filtering for v1,
6. Follow-up verification on scenario-family field availability from source API.

