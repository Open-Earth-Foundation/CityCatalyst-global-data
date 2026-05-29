---
name: scaffold-mage-pipeline
description: Scaffold a new Mage pipeline (folder + metadata + standard block stubs). Use when the user asks to create, add, or scaffold a new pipeline, or to fork a versioned pipeline (_v<year>).
---

# scaffold-mage-pipeline

Generate the standard Mage pipeline folder + metadata + block stubs.

## Workflow

### Step 1 — Pick a name

Follow `engineering-standards/naming-conventions.md`:

```
<prefix>_<sector>_<source>[_v<year>]
```

Examples:
- `ghgi_ippu_climatetrace_v2026`
- `ccra_floods_climateraltm_v2025`
- `dq_ghgi_uniqueness`

### Step 2 — Folder structure

```
cc-mage/pipelines/<name>/
└── metadata.yaml

cc-mage/data_loaders/load_<source>.py
cc-mage/transformers/cleaning_<source>.py
cc-mage/transformers/transformation_<source>.py
cc-mage/data_exporters/<source>_staging.py
cc-mage/transformers/<source>_lookup.sql       # optional
cc-mage/transformers/locode_transformation.sql
cc-mage/data_exporters/update_<source>_emissions.sql
cc-mage/data_exporters/update_<source>_sector_activity.sql
cc-mage/data_exporters/update_<source>_emission_factor.sql
```

(Reuse existing block files when possible — Mage blocks are global to the project.)

### Step 3 — `metadata.yaml`

```yaml
name: <name>
type: python
description: |
  Ingest <source> <sector> data into modelled.* tables.
  Source: <publisher URL>. Release: <version>.
created_at: '<ISO timestamp>'

variables:
  bucket_name: test-global-api
  release_version: '<version>'
  source_path: 's3://<bucket>/<key>'
  datasource_name: '<exact match in publisher_datasource>'

blocks:
  - uuid: load_<source>
    type: data_loader
    upstream_blocks: []
    downstream_blocks: [cleaning_<source>]

  - uuid: cleaning_<source>
    type: transformer
    upstream_blocks: [load_<source>]
    downstream_blocks: [transformation_<source>]

  - uuid: transformation_<source>
    type: transformer
    upstream_blocks: [cleaning_<source>]
    downstream_blocks: [<source>_staging]

  - uuid: <source>_staging
    type: data_exporter
    upstream_blocks: [transformation_<source>]
    downstream_blocks: [locode_transformation]

  - uuid: locode_transformation
    type: transformer
    language: sql
    upstream_blocks: [<source>_staging]
    downstream_blocks:
      - update_<source>_emissions
      - update_<source>_sector_activity
      - update_<source>_emission_factor

  - uuid: update_<source>_emissions
    type: data_exporter
    language: sql
    configuration:
      use_raw_sql: true
      export_write_policy: append
    upstream_blocks: [locode_transformation]

  - uuid: update_<source>_sector_activity
    type: data_exporter
    language: sql
    configuration:
      use_raw_sql: true
      export_write_policy: append
    upstream_blocks: [locode_transformation]

  - uuid: update_<source>_emission_factor
    type: data_exporter
    language: sql
    configuration:
      use_raw_sql: true
      export_write_policy: append
    upstream_blocks: [locode_transformation]
```

### Step 4 — Block stubs

For each block, follow `mage-blocks-python.mdc` / `mage-blocks-sql.mdc`. Mandatory:

- Top-of-file docstring (block name + brief).
- Real `@test` decorators (schema + uniqueness + plausibility — not just `assert output is not None`).
- For SQL: `INSERT … ON CONFLICT … DO UPDATE` (idempotent UPSERT into `modelled.*`).

### Step 5 — Catalog + review

Use `add-publisher` (if new publisher) or `add-dataset-release` (if new release). Set `production_approved: false` initially.

### Step 6 — Local smoke run

```bash
docker compose up -d
# UI at http://localhost:6789 — run the pipeline against a small subset
```

Capture the row counts from the staging table and the modelled write — paste into the PR description.

### Step 7 — Document

Run `docs-after-change`. Update `dataset-review/reviews/<publisher>/<dataset>/README.md` to mention the new pipeline.

## Checklist

- [ ] Naming follows `naming-conventions.md`.
- [ ] `metadata.yaml.description` is non-null.
- [ ] All variables declared (no hardcoded bucket / path / version).
- [ ] Block files exist; tests are real (Layer 2+).
- [ ] SQL exporters use `INSERT … ON CONFLICT … DO UPDATE`.
- [ ] Catalog and review updated.
- [ ] Local smoke run captured (row counts in PR body).
