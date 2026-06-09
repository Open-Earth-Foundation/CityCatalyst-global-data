# Definition of Done

## Purpose

This checklist gates what it means for a pipeline to be production-ready. It is not a bureaucratic sign-off process — it is a shared standard that protects the team from shipping incomplete work and protects downstream users from unreliable data.

There are two versions of the checklist: one for a **new pipeline** (first time a dataset goes to production) and a shorter one for a **new release** of an existing pipeline. Both must be completed before data is considered production-approved in the catalog.

---

## New Pipeline Checklist

Use this when a dataset is being shipped to production for the first time.

### Naming & Structure

- [ ] Pipeline name follows the `<prefix>_<source>_<description>` convention (see [Naming Conventions](./naming-conventions.md))
- [ ] All block names follow the `load_`, `transform_`, `export_` naming patterns
- [ ] Pipeline `metadata.yaml` has a `description` field that clearly states what the pipeline does, what dataset it processes, and which stages it operates across
- [ ] Release-specific inputs (`release_version`, `source_url` or `source_path`) are defined as `variables` in `metadata.yaml`, not hardcoded in block logic

### Data Quality

- [ ] Layer 2 structural checks are implemented as `@test` decorators on all Python blocks (see [Data Quality & Validation](./data-quality-and-validation.md))
- [ ] At minimum: output is not null, expected columns are present, no nulls in required fields, row count is non-zero
- [ ] Layer 3 plausibility checks are implemented where applicable and output flags to logs rather than hard failures
- [ ] Pipeline has been run end-to-end against real data without errors

### Code

- [ ] All mapping and transformation decisions are commented inline with the reasoning (not just what the code does, but why)
- [ ] No hardcoded environment-specific values (paths, credentials, bucket names) — these come from config or pipeline variables
- [ ] No leftover debug code, print statements used for development, or commented-out blocks

### Documentation & Catalog

- [ ] `methodology_url` set to the source publisher's own methodology documentation
- [ ] OEF internal review exists in Notion and `internal_review_url` is set in the catalog release entry
- [ ] Dataset catalog entry in `dataset-review/catalog/index.yaml` is complete:
  - [ ] All required dataset-level fields populated (see [Documentation & Metadata](./documentation-and-metadata.md))
  - [ ] Release entry has `production_approved: true`
  - [ ] Release entry has `is_latest: true`
  - [ ] `pipeline_name` and `pipeline_version` are set correctly
  - [ ] All six `data_quality` scores are completed for this release
  - [ ] `retrieved_at` and `released_at` are populated
  - [ ] `dataset_slug` and `dataset_name` (multilingual) are populated at dataset level
- [ ] S3 paths used by the pipeline follow the stage folder structure in the naming conventions

### Review

- [ ] A second team member has reviewed the pipeline logic and catalog entry before the release is marked `production_approved: true`

---

## New Release Checklist

Use this when an existing pipeline is being run against a new data release (same logic, new version year or updated source file).

### Catalog

- [ ] New release entry appended to the dataset's `releases` list in `index.yaml` with the next `version_number`
- [ ] Previous release updated to `is_latest: false`
- [ ] New release has `production_approved: true` and `is_latest: true`
- [ ] `pipeline_name` and `pipeline_version` correctly reflect which pipeline was used
- [ ] `data_quality` scores reviewed and updated if anything has changed — scores from the prior release must not be copied forward without re-evaluation
- [ ] License confirmed for this release — do not assume it matches the previous release
- [ ] `retrieved_at` populated

### Pipeline

- [ ] Pipeline variables updated to the new release parameters (`release_version`, `source_url`, etc.)
- [ ] Pipeline run end-to-end against the new release without errors
- [ ] Layer 2 checks pass cleanly
- [ ] Any new Layer 3 flags investigated and documented before marking production-approved

### Documentation

- [ ] If the source updated its methodology, `methodology_url` updated to the new documentation
- [ ] If OEF's analysis changed, Notion review updated and `internal_review_url` reflects the current page

---

## Guiding Principles

**Documentation is not a finishing step.** The catalog entry, methodology page, and inline comments are part of the work, not something added after. A pipeline that processes data correctly but has no methodology URL is not done.

**`production_approved: true` is a promise.** It tells downstream systems and users that this data has been reviewed, validated, and is fit for purpose. Do not set it until the full checklist is complete.

**The checklist is a floor, not a ceiling.** If something specific to a dataset warrants additional checks or documentation beyond what is listed here, add it. The checklist captures the minimum; good judgement determines the rest.
