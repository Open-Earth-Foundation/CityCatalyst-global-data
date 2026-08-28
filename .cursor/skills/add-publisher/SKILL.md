---
name: add-publisher
description: Add a new data publisher and its first dataset review. Creates folder skeleton, README, and catalog entry. Use when the user asks to onboard a publisher, add a new data source, or register a new dataset publisher.
---

# add-publisher

Onboard a new publisher (e.g. EU Eurostat, ClimateTRACE, EDGAR) into `dataset-review/`.

## Workflow

### Step 1 — Pick slugs

- `<publisher>` slug: short, lowercase, kebab-case (`eurostat`, `climatetrace`, `edgar`, `world-bank`).
- `<dataset-id>` slug: `<publisher>-<dataset-name>` (`eurostat-energy`, `climatetrace-onroad`).

### Step 2 — Folder skeleton

```
dataset-review/reviews/<publisher>/<dataset-id>/
├── README.md
└── releases/<version>/
    ├── review.yaml
    └── sample/                  # (optional) tiny sample data, NOT prod data
```

### Step 3 — `README.md` (per dataset)

```md
# <Dataset Human Name>

Source: <Publisher Human Name> · License: <SPDX or "see source">

## What it is
1–3 sentences describing the dataset (coverage, themes, granularity).

## Why we want it
Bullet list — discovery, finance signal, geographic coverage, methodological reference, etc.

## Releases

- `releases/<version>/` — see [`review.yaml`](releases/<version>/review.yaml). Status: <pending_validation|production_ready>.

## Open questions
Bullet list of things to check during integration (e.g. units, deduplication, license clauses).
```

### Step 4 — `releases/<version>/review.yaml`

```yaml
publisher:
  name: <Publisher Human Name>
  short_name: <publisher>
  url: '<homepage>'

dataset:
  id: <dataset-id>
  name: <Dataset Human Name>
  description: <one sentence>
  source_format: csv|json|geojson|parquet|api
  api_endpoint: '<url if api>'
  coverage:
    type: country|global|city
    value: '<countries / "global" / specific city>'

themes:
  - climate
  - <…>

key_attributes:
  - name: <field>
    type: string|int|float|datetime
    description: <…>

integration:
  recommended_pattern: file_based | api_based
  notes: |
    <how to ingest into raw_data and modelled>

license:
  spdx: '<SPDX id or "custom">'
  url: '<license URL>'
  redistribution_allowed: yes|no|conditional

production_ready: pending_validation
```

### Step 5 — Catalog entry

Append to `dataset-review/catalog/index.yaml`:

```yaml
- id: <dataset-id>
  name: <Dataset Human Name>
  publisher: <publisher>
  coverage: { type: country|global|city, value: '<…>' }
  themes: [...]
  update_frequency: annual|quarterly|monthly|adhoc
  priority: high|medium|low
  releases:
    - version: '<version>'
      production_approved: false      # always start false
      is_latest: true
      license: { spdx: '<…>', url: '<…>' }
      pipeline_name: null              # filled when production_approved=true
      data_quality: null
      urls: { source: '<…>', methodology: '<…>' }
```

### Step 6 — Document

- Run the `docs-after-change` skill.
- If the dataset belongs in a thematic collection, add the id under `dataset-review/collections/collection.yaml`.

## Checklist

- [ ] Folder created under `reviews/<publisher>/<dataset-id>/`.
- [ ] README explains what + why + open questions.
- [ ] `releases/<version>/review.yaml` filled (no nulls in required fields).
- [ ] `catalog/index.yaml` appended (`production_approved: false`).
- [ ] `collections/collection.yaml` updated if applicable.
- [ ] No production data committed under `sample/` — tiny excerpts only.
