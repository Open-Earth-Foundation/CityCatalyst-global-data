# Agent Context — CityCatalyst Global Data

This file gives an AI agent the working knowledge needed to reason about this repo correctly.
Read this alongside `ARCHITECTURE.md` for system design, and `dataset_review/catalog/index.yaml`
for the current dataset registry.

---

## What this repo actually does

This repo ingests emissions and activity data from external publishers, transforms it, and loads
it into the GlobalAPI — a PostgreSQL database that powers city-level GHG inventory reporting.

There are two distinct halves that must stay in sync:
- `dataset_review/` — *before* a pipeline exists: methodology, scoring, and sector mappings
- `cc-mage/` — the Mage.ai pipelines that actually move and transform the data

A pipeline should not be built without a corresponding dataset review. The review is the source
of truth for how data maps to the target schema.

---

## Identity mappings you must get right

These are the most common source of mistakes in SQL and Python:

| Identifier | What it is | Where it appears |
|------------|-----------|-----------------|
| `actor_id` | UN/LOCODE city code (e.g. `BR SAO`) | `modelled.emissions`, `modelled.emissions_factor` |
| `locode` | Same as `actor_id` — the city's primary key | `modelled.city_polygon` |
| `city_id` | GeoHash of the city centroid — NOT the primary key | `modelled.city_polygon`, some staging tables |
| `datasource_name` | Short string key linking emissions back to a publisher | All `modelled` tables — must match `publisher_datasource.datasource_name` exactly |
| `gpc_reference_number` | GPC sector ref (e.g. `II.1.1`) | `modelled.emissions`, `modelled.ghgi_methodology` |
| `gpcmethod_id` | UUID linking an emission record to a methodology | FK between `emissions`, `activity_subcategory`, `ghgi_methodology` |

When writing SQL that joins across tables, always use `actor_id` / `locode` for city identity —
never `city_id`. When referencing datasets, `datasource_name` must be an exact string match.

---

## How dataset_review and cc-mage connect

```
dataset_review/catalog/index.yaml        ← find the current version + review path
    └── review/<publisher>/<dataset>/<version>/
            ├── methodology.md           ← understand the data structure and assumptions
            ├── data_scoring.md          ← understand data quality limitations
            └── mapping/                 ← sector mapping drives the staging SQL transform
                    └── <source>_to_gpc.csv

cc-mage/pipelines/<pipeline_name>/
    └── metadata.yaml                    ← references variables (S3 path, year, gas)
```

The mapping CSV in `dataset_review` is what drives the `gpc_reference_number` values that
end up in `modelled.emissions`. If the mapping is wrong or missing, the pipeline will load
data under incorrect GPC reference numbers.

---

## Critical constraints

**Do not rename `cc-mage/`** — the folder name is baked into Mage.ai's project configuration.
Renaming it breaks the Docker setup entirely.

**Do not delete version folders in `dataset_review/`** — old versions must be preserved.
When a dataset is updated, create a new version folder alongside the old one. The catalog
`current_version` field (or `production_approved_release`) is what determines which is active.

**Pipeline `metadata.yaml` descriptions are unreliable** — descriptions may be `null` or
outdated. Do not use them to understand what a pipeline does. Read the blocks directly.

**Staging tables are temporary by design** — `raw_data.*_staging` tables are intermediate.
Do not treat them as a data source for other pipelines or reporting.

---

## Things that look similar but are different

**Some publishers have two pipeline patterns:**
- File-based — reads from S3 files, standard `extract → stage → modelled` flow. These are
  the authoritative pipelines for production ingestion.
- API-based — pulls from the publisher's API directly for a specific city. Used for ad-hoc
  or pilot city work, not production ingestion.

When in doubt about which pattern a pipeline uses, read its block code rather than the
`metadata.yaml` description.

**`transformer` vs `data_exporter` blocks in Mage:**
- A `transformer` block transforms data and passes it downstream — it does not write to the DB.
- A `data_exporter` block writes to the DB (or S3) and is a terminal node in the DAG.
- SQL blocks that load into `modelled.*` are always `data_exporter` type.

**`emissions_factor` vs `formula_input`:**
- `emissions_factor` — standard EF used in `emissions = activity × EF` calculations.
- `formula_input` — parameters for more complex calculations where the simple formula doesn't
  apply (e.g. waste composition factors, biological treatment parameters).

---

## Anti-patterns to avoid

- **Don't write `SELECT *` in staging SQL** — always select explicit columns so schema changes
  don't silently propagate downstream.
- **Don't create a new pipeline without a dataset review** — the methodology and mapping must
  exist in `dataset_review/` first.
- **Don't hardcode S3 paths in block code** — S3 bucket and file paths belong in pipeline
  `variables` in `metadata.yaml`, not in block logic.
- **Don't use `city_id` as the city join key** — use `actor_id` / `locode`.
- **Don't assume the `datasource_name` string** — look it up in `modelled.publisher_datasource`
  or the existing pipeline SQL to get the exact value used.
- **Don't add new `modelled` tables without a corresponding `db_create_table` block** —
  schema changes should be tracked there so they can be replayed.
