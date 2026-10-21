---
name: add-dataset-release
description: Add a new release of an existing dataset. Preserves old releases. Use when the user asks to bump a dataset version, add a new yearly release, or update production_approved status.
---

# add-dataset-release

When a publisher ships an updated dataset (e.g. v2025 → v2026), add a **new** release folder alongside the old one.

## Workflow

### Step 1 — Add the new release folder

```
dataset-review/reviews/<publisher>/<dataset-id>/releases/<new-version>/
├── review.yaml
└── sample/      # optional tiny sample
```

**Do not delete** `releases/<old-version>/`. We preserve all releases.

### Step 2 — Fill `review.yaml`

Copy the previous release's `review.yaml` and update:

- `dataset.coverage.value` if the geographic scope changed.
- `key_attributes` if the schema changed (and document the diff in a `schema_changes:` block).
- `integration.notes` for pipeline impact.
- `production_ready: pending_validation` (start cautious).

### Step 3 — Update `catalog/index.yaml`

Inside the dataset entry's `releases:` list:

1. Add the new release. Set `is_latest: true`.
2. Flip the previous release's `is_latest: false`.
3. **Do not change** `production_approved` on the old release.

```yaml
releases:
  - version: '2026'
    production_approved: false
    is_latest: true
    license: { spdx: '...', url: '...' }
    pipeline_name: null
    data_quality: null
    urls: { source: '...', methodology: '...' }

  - version: '2025'
    production_approved: true
    is_latest: false              # was true; flip to false
    license: { spdx: '...', url: '...' }
    pipeline_name: ghgi_<…>_v2025
    data_quality: { layer_2_passed: true, layer_3_passed: true, notes: '…' }
    urls: { source: '...', methodology: '...' }
```

### Step 4 — Pipeline plan

If the new release requires pipeline changes:

- Use the `scaffold-mage-pipeline` skill to clone the previous pipeline as `_v<new>` (e.g. `ghgi_ippu_climatetrace_v2026`).
- Keep both pipelines runnable until the new one is `production_approved`.

### Step 5 — Promotion (later, separate PR)

When the new release passes Layers 2 + 3 in `engineering-standards/data-quality-and-validation.md`:

1. Set `production_approved: true` on the new release.
2. Fill `pipeline_name` and `data_quality`.
3. Optionally retire the old release: `production_approved: false`. Do **not** delete files.

### Step 6 — Document

Run the `docs-after-change` skill (especially update the dataset README).

## Anti-patterns

- Deleting the old release folder.
- Adding a new release without flipping the old `is_latest`.
- Setting `production_approved: true` in the same PR as the file additions — split into two PRs (one for "add", one for "promote") so review focuses on the right thing.
- Sharing a single pipeline across releases — fork the pipeline (`_v<year>`) so old data can still be regenerated.
