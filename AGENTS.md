# Agent Context — CityCatalyst Global Data

This file gives an AI agent the working knowledge needed to reason about this repo correctly.
Read this alongside `ARCHITECTURE.md` for system design, `dataset-review/catalog/index.yaml`
for the current dataset registry, and `engineering-standards/` for team conventions and the
definition of done.

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

Always use `actor_id` / `locode` for city identity — never `city_id`. When referencing
datasets, `datasource_name` must be an exact string match.

---

## Critical constraints

**Do not rename `cc-mage/`** — the folder name is baked into Mage.ai's project configuration.
Renaming it breaks the Docker setup entirely.

**Do not delete release folders in `dataset-review/reviews/`** — old releases must be preserved.
When a dataset is updated, create a new release folder alongside the old one. The catalog
`production_approved_release` field is what determines which release is currently active.

**Staging tables are temporary by design** — `raw_data.*_staging` tables are intermediate.
Do not treat them as a data source for other pipelines or reporting.

**Do not use `city_id` as the city join key** — use `actor_id` / `locode`.

---

## Things that look similar but are different

**`emissions_factor` vs `formula_input`:**
- `emissions_factor` — standard EF used in `emissions = activity × EF` calculations.
- `formula_input` — parameters for more complex calculations where the simple formula doesn't
  apply (e.g. waste composition factors, biological treatment parameters).

**Some publishers have two pipeline patterns:**
- File-based — reads from S3, standard `extract → stage → modelled` flow. Authoritative for production.
- API-based — pulls directly from the publisher API for a specific city. Ad-hoc only, not production ingestion.

When in doubt about which pattern a pipeline uses, read its block code — `metadata.yaml`
descriptions may be outdated.
