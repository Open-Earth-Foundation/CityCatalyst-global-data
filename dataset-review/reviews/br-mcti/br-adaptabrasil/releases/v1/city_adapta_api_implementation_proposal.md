# City Adapta Risk API Implementation Proposal (manager-ready)

## Executive summary

Build a city-first AdaptaBrasil API that serves both:

1. Current product expectations (`sector`, `risk`, `risk_component`), and
2. Full future-safe hierarchy (`impact_chain_*`, `base_indicator`).

Recommendation: implement a star-like serving model with one fact table and two dimensions, then expose one primary city route with level-based output controls.
<!-- Amanda comment: This recommendation should be aligned with the proposed v1 simplification (single wide fact table) to avoid conflicting direction in the document. -->

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
<!-- Amanda comment: Given this is a dedicated dataset with one primary city-first API use case, we should prefer a single wide/flat serving table in v1 instead of fully normalizing into multiple dimensions. Rationale: simpler ingestion/upserts, fewer joins, faster delivery, and easier maintenance while the contract is still evolving. -->

### Table 1: `dim_adapta_hierarchy`
Source: `adapta_indicator_hierarchy_modeled_en.csv`

Columns:
- `hierarchy_pk` (surrogate key, bigint)
- `sector_id`, `sector_name`
- `risk_id`, `risk_name`
- `risk_component_id`, `risk_component_name` (nullable)
- `impact_chain_id_1`, `impact_chain_name_1` (nullable)
- `impact_chain_id_2`, `impact_chain_name_2` (nullable)
- `impact_chain_id_3`, `impact_chain_name_3` (nullable)
- `base_indicator_id`, `base_indicator_name`
- `base_indicator_level` (int)
- `is_component_structural_null` (boolean default false)
- `source_release` (text, e.g. `v1`)
- `is_active` (boolean default true)

Constraints/indexes:
- Unique on full hierarchy IDs.
- Unique on full hierarchy names (for ingestion matching when IDs are absent in value payloads).
- Indexes on `sector_id`, `risk_id`, `base_indicator_id`.

---

### Table 2: `dim_adapta_indicator_metadata`
Source: `adapta_indicators_ids.csv`

Columns:
- `indicator_id` (PK; matches source `id`)
- `name`, `title`, `shortname`
- `level`
- `simple_description`, `complete_description`
- `equation`
- `measurement_unit`
- `climate_hazard`
- `years`, `years_description` (json/text)
- `scenarios` (json/text)
- `pessimist` (numeric/int as provided)
- `geometrytype`
- `legend`
- `menu_structure` (json/text)
- `raw_record` (jsonb/text for lossless provenance)

Indexes:
- PK on `indicator_id`.
- Optional full-text/search indexes on `name`, `title`.

---

### Table 3: `modelled.city_adapta_risk_fact`
Primary serving table for API responses.

Columns:
- **City/time**
  - `city_id` (internal key)
<!-- Amanda comment: Rename `city_id` to `actor_id` to align with existing city identity conventions (`actor_id`/`locode`). -->
  - `city_name`
  - `country_code` (default `BR`)
  - `timeframe` (int or text; e.g. `2020`, `2030`, `2050`)
  - `scenario` (text; e.g. `current`, `optimistic`, `pessimistic`)
  - `scenario_family` (nullable; `SSP`/`RCP`/`SWL`)
- **Hierarchy**
  - `hierarchy_pk` (FK to `dim_adapta_hierarchy`)
  - denormalized IDs optional for query speed: `sector_id`, `risk_id`, `risk_component_id`, `base_indicator_id`
- **Values**
  - `risk_value_numeric`, `risk_value_string`
  - `risk_component_value_numeric`, `risk_component_value_string` (nullable)
  - `impact_chain_1_value_numeric`, `impact_chain_1_value_string` (nullable)
  - `impact_chain_2_value_numeric`, `impact_chain_2_value_string` (nullable)
  - `impact_chain_3_value_numeric`, `impact_chain_3_value_string` (nullable)
  - `base_indicator_value_numeric`, `base_indicator_value_string`
- **Null/data quality semantics**
  - `value_status` (`ok`, `data_unavailable`)
  - `null_type` (`none`, `structural_null`, `data_gap_null`)
<!-- Amanda comment: To keep v1 simpler, we could store only `null_type` and derive `value_status` in the API response layer. -->
- **Provenance**
  - `source_dataset` (e.g. `br-mcti/adaptabrasil`)
  - `release_version` (e.g. `v1`)
  - `source_vintage` (text)
  - `spatial_support_level` (`municipal`, `state`, `subsystem`, `asset`)
  - `ingested_at`, `updated_at`
<!-- Amanda comment: For this phase, we can ignore records that are not `municipal` level. -->
<!-- Amanda comment: We can use our new tables for provenance fields:
  - `release_id` (FK to `modelled.dataset_release.release_id`; primary traceability key)
  - `created_at` (`TIMESTAMPTZ`, default `NOW()`)
  - `updated_at` (`TIMESTAMPTZ`, default `NOW()`, updated on upsert)
  - optionally keep `source_dataset` and `release_version` as display fields only
  - `release_id` should be populated via join to `modelled.dataset_release` using pipeline `release_version`
-->

Logical uniqueness:
- (`city_id`, `timeframe`, `scenario`, `hierarchy_pk`)
<!-- Amanda comment: If we rename `city_id` to `actor_id`, update logical uniqueness and all indexes below to use `actor_id` consistently. -->

Critical indexes:
- (`city_id`, `timeframe`, `scenario`)
- (`city_id`, `sector_id`)
- (`city_id`, `risk_id`)
- (`city_id`, `timeframe`, `scenario`, `risk_component_id`)

---

## Ingestion and transformation design

## Pipeline steps

1. Load hierarchy from `adapta_indicator_hierarchy_modeled_en.csv` into `dim_adapta_hierarchy`.
2. Load indicator dictionary from `adapta_indicators_ids.csv` into `dim_adapta_indicator_metadata`.
<!-- Amanda comment: Before these steps, we should ingest AdaptaBrasil data directly from the API only, land raw payloads into `raw_data`, and run this ingestion weekly to keep data synchronized with source updates. -->
<!-- Amanda comment: If we proceed with a flat-table v1, these dimension-loading steps should be revised to avoid implying a mandatory 3-table implementation. -->
3. Load value payloads (sample/full extract) into staging.
4. Resolve hierarchy for each value row:
   - join by full name path:
     - `sector_name`, `risk_name`, `risk_component_name`,
     - `impact_chain_name_1`, `impact_chain_name_2`, `impact_chain_name_3`,
     - `base_indicator_name`.
5. Assign null semantics:
   - `structural_null` if component fields empty and base indicator numeric exists.
   - `data_gap_null` if base indicator numeric is empty and string is `Data unavailable`.
6. Upsert into `city_adapta_risk_fact`.
7. Run validation checks + publish.

## Why full-path matching is required

`base_indicator_name` is not globally unique across all sectors/risks. Use full hierarchy path keys to avoid incorrect ID mapping.

---

## API routes proposal

## 1) Primary city endpoint (recommended default)
`GET /v1/cities/{cityId}/climate-risk/adapta`

Query params:
- `timeframe` (optional; default current configured year)
- `scenario` (optional; default current)
- `sector` (optional; id or name)
- `risk` (optional; id or name)
- `level` (optional):
  - `summary` (default: sector/risk/risk_component)
  - `chain` (includes impact_chain levels)
  - `indicator` (full hierarchy + base indicators)
<!-- Amanda comment: Keep only two `level` options for now: `summary` and `chain`, where `chain` should return the full hierarchy/detail (no separate `indicator` level in v1). -->
- `include_metadata` (optional boolean; enrich with indicator descriptions)
- `include_nulls` (optional boolean; default true)
<!-- Amanda comment: This feels too parameter-heavy for v1. Prefer a simpler contract with only `timeframe`, `scenario`, and optional `level` (default `summary`), and defer `sector`, `risk`, `include_metadata`, and `include_nulls` to follow-up endpoints/versions if needed. -->

Response shape:
- `meta`: dataset/release/scenario/timeframe/provenance
- `data`: array of rows filtered to requested level
- each row includes `null_type` and `value_status`

---

## 2) Secondary list endpoint (UI filtering support)
`GET /v1/cities/{cityId}/climate-risk/adapta/options`
<!-- Amanda comment: For v1, we can likely skip this endpoint and keep a single city endpoint; add `/options` later only if UI filtering requires a dedicated route. -->

Returns available filters for the current city/time/scenario:
- sectors
- risks per sector
- components per risk
- available timeframes/scenarios

---

## 3) Optional dictionary endpoint (cached, low change)
`GET /v1/climate-risk/adapta/dictionary`
<!-- Amanda comment: Defer this to phase 2 unless the UI needs metadata/tooltips immediately in v1. -->

Returns hierarchy metadata + indicator definitions.
Can be served from dimensions only (no city filtering).

---

## Example API behavior (null semantics)

If a row has:
- empty `risk_component_name`
- but non-empty `base_indicator_value_numeric`

then return:
- `null_type: "structural_null"`
- `value_status: "ok"`

If a row has:
- `base_indicator_value_numeric` null
- `base_indicator_value_string = "Data unavailable"`

then return:
- `null_type: "data_gap_null"`
- `value_status: "data_unavailable"`

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
1. `dim_adapta_hierarchy` + `dim_adapta_indicator_metadata` + `city_adapta_risk_fact`,
2. Primary city endpoint with `level` parameter,
3. Explicit `structural_null` vs `data_gap_null` semantics,
4. Source-faithful scenario handling (`SSP`/`RCP`/`SWL`) without premature harmonization.
<!-- Amanda comment: is this information currently coming from the API, if not we will need to follow up with them -->

