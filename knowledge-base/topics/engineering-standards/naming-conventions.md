# Naming Conventions

## General Principles

- **snake_case everywhere** — all file names, folder names, S3 paths, database objects, and Python code use underscores. No spaces, no camelCase, no mixed conventions.
- **Descriptive over short** — names should communicate what something is without needing to open it. Avoid single-letter variables or cryptic shorthand outside of approved abbreviations.
- **Abbreviations are acceptable** where they are well understood.
- **Consistency over cleverness** — when in doubt, follow the closest existing pattern rather than inventing a new one.

### Migration

These conventions apply to all new work. Existing code and data objects that do not conform should be migrated opportunistically when touched as part of other work, not as a dedicated migration exercise.

---

## Repository Names

Repository names use **kebab-case** (hyphens). This is the one exception to the snake_case rule, following standard GitHub convention.

| Type | Pattern | Example |
|---|---|---|
| Project repo | `project-<topic>` | `project-stationary-energy` |
| Main pipeline repo | existing name | — |
| Shared library / tool | `<name>-<purpose>` | `climate-data-utils` |

---

## S3 Paths & File Names

All folder names and file names within S3 use **snake_case**. The structure mirrors the 4-stage architecture.

### Stage folder structure

```
<stage>/
  <publisher-slug>/
    <dataset-slug>/
      release/
        <release-version>/
            <file_name>.parquet   (or source extension for files stage)
```

### Naming patterns for stage files

Use these slug conventions in every stage path:

- `publisher-slug`: canonical lower-case kebab-case publisher identifier.
  - Pattern: `<country-or-scope>-<publisher>`
  - Examples: `cl-ine`, `ocha-rolac`, `uncece`
- `dataset-slug`: canonical lower-case kebab-case dataset identifier under a publisher.
  - Pattern: `<publisher-slug>-<dataset>`
  - Examples: `cl-ine-censo`, `cl-ocha-ab`, `uncece-unlocode`
- `publisher_key`: `publisher-slug` converted for S3/file paths by replacing `-` with `_`.
  - Examples: `cl_ine`, `ocha_rolac`, `uncece`
- `dataset_key`: `dataset-slug` converted for S3/file paths by replacing `-` with `_`.
  - Examples: `cl_ine_censo`, `cl_ocha_ab`, `uncece_unlocode`
- `file_name`: must start with `dataset_key`, then domain.
  - Pattern: `<dataset_key>_<domain>.<ext>`
  - Examples: `cl_ine_censo_stationary_energy.csv`, `uncece_unlocode_city_reference.parquet`

| Stage | Pattern | Example |
|---|---|---|
| `files` | `files/<publisher_key>/<dataset_key>/release/<release-version>/<dataset_key>_<domain>.<ext>` | `files/cl_ine/cl_ine_censo/release/v1/cl_ine_censo_stationary_energy.csv` |
| `raw_data` | `raw_data/<publisher_key>/<dataset_key>/release/<release-version>/<dataset_key>_<domain>.parquet` | `raw_data/cl_ine/cl_ine_censo/release/v1/cl_ine_censo_stationary_energy.parquet` |
| `modelled` | `modelled/<publisher_key>/<dataset_key>/release/<release-version>/<dataset_key>_<domain>.parquet` | `modelled/cl_ine/cl_ine_censo/release/v1/cl_ine_censo_stationary_energy.parquet` |
| `reporting` | `reporting/<publisher_key>/<dataset_key>/release/<release-version>/<dataset_key>_<domain>.parquet` | `reporting/cl_ine/cl_ine_censo/release/v1/cl_ine_censo_city_emissions_summary.parquet` |

### Rules
- Keep canonical `publisher-slug` and `dataset-slug` stable; derive S3/path segments by replacing `-` with `_` (`publisher_key`, `dataset_key`).
- In S3 paths and file names, use only snake_case segments (`publisher_key`, `dataset_key`, and `<domain>`).
- No release versions or years in `file_name` — put versioning only in `release/<release-version>/`.

---

## Database Objects

### Schemas

Schemas map to the architecture stages and should not be repurposed.

| Schema | Purpose |
|---|---|
| `raw_data` | Transformed source data, not yet modelled |
| `modelled` | Data modelled to GPC standards |

### Tables

- **Plural names** — tables represent collections of records: `emissions`, `cities`, `data_sources`.
- Pattern: `<entity>` or `<domain>_<entity>` for disambiguation.
- Avoid prefixing with the schema name — the schema already provides that context.

```
modelled.city_emissions
modelled.activity_data
reporting.emissions_summary
reporting.city_overview
```

### Columns

- Always **snake_case**.
- **Include units in column names** for any measured quantity there should be a column with units as well
- **Boolean columns** use `is_` or `has_` prefix: `is_active`, `has_geospatial_data`.
- **Foreign keys** use the referenced table name with `_id` suffix: `city_id`, `data_source_id`.
- **City identifiers** use `locode` as the standard column name: `locode`.
- **Timestamps** follow the `_at` convention: `created_at`, `updated_at`.
- **Reporting year** uses `reporting_year` (not `year` alone, which is ambiguous in climate data).

```sql
-- Good
city_id          VARCHAR
locode           VARCHAR
reporting_year   INTEGER
emissions        NUMERIC
emissions_units  VARCHAR
is_verified      BOOLEAN
created_at       TIMESTAMP

-- Avoid
city             VARCHAR   -- ambiguous, is this the name or the id?
year             INTEGER   -- too generic
emissions        NUMERIC   -- missing units
verified         BOOLEAN   -- missing is_ prefix
```

### Views

Views follow the same table naming conventions with a `_v` suffix to distinguish them from base tables: `city_emissions_v`.

---

## Python Code

Follow [PEP 8](https://pep8.org/) as the baseline. Key rules:

| Element | Convention | Example |
|---|---|---|
| Modules / files | `snake_case` | `emissions_transformer.py` |
| Functions | `snake_case` | `calculate_co2e_emissions()` |
| Variables | `snake_case` | `reporting_year` |
| Classes | `PascalCase` | `EmissionsTransformer` |
| Constants | `UPPER_SNAKE_CASE` | `DEFAULT_REPORTING_YEAR` |

- Function names should describe what they do: `transform_raw_to_modelled()`, not `process()`.
- Avoid single-letter variable names outside of short loop counters (`i`, `j`).
- Configuration values and environment-specific values should be constants or loaded from config, never hardcoded inline.

---

## Mage Pipelines

Mage pipeline and block names use **snake_case**.

### Pipeline naming

| Element | Pattern | Example |
|---|---|---|
| Pipeline (standard) | `<prefix>_<source>_<description>` | `ghgi_carbon_monitor`, `ccra_br_risk_assessment` |
| Pipeline (versioned) | `<prefix>_<source>_<description>_v<n>` | `ghgi_ct_onroad_v2025` |
| Data loader block | `load_<source>_<description>` | `load_ct_oil_gas_refining` |
| Transformer block | `transform_<description>` | `transform_emissions_to_co2e` |
| Data exporter block | `export_<destination>_<description>` | `export_s3_modelled_stationary` |

### Pipeline versioning

Pipelines are versioned when the processing logic changes significantly enough that it cannot be handled by parameters alone — for example, when a source changes its methodology, schema, or sector structure between releases.

Most data releases do not require a new pipeline version. A single pipeline handles multiple releases via parameters (release year, source path, etc.), and the catalog records which pipeline and parameters were used for each release.

Create a new pipeline version (`_v2`, `_v3`) when:
- The source schema changes in a way that breaks the existing pipeline
- The methodology changes significantly enough that the old logic would produce incorrect results for old releases if rerun
- The transformation logic requires a fundamentally different approach

Do not create a new pipeline version for:
- A new data year using the same structure and methodology
- Minor fixes or improvements that apply equally to all releases
- Configuration or parameter changes

When a new pipeline version is created, the previous version is **not deleted**. It remains in the main repo and can be used to rerun older releases. The catalog entry for each release records which pipeline version was used for that release.

### Pipeline parameters and catalog linkage

Pipelines should be designed to accept the key inputs for a given release as parameters rather than hardcoding them. This enables reruns to be triggered programmatically — for example, via the Mage API — using the information stored in the catalog.

At minimum, a parameterised pipeline should accept:
- `release_version` — the version label from the catalog release entry
- `source_url` or `source_path` — where to retrieve the source data

The catalog release entry records `pipeline_name` and `pipeline_version` for each release, creating a complete chain: catalog → pipeline → data in the database.

