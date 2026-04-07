## What this PR does

<!-- Brief description of the change and why -->

## Type of change

- [ ] New pipeline (first production deployment of a dataset)
- [ ] New release (existing pipeline, new data version)
- [ ] Bug fix / improvement to existing pipeline
- [ ] Catalog / documentation update
- [ ] Other (describe above)

---

## Definition of Done

Complete the relevant checklist below. Tick items that apply and strike through items that don't (~~like this~~).

### For new pipelines

- [ ] Pipeline name follows `<prefix>_<source>_<description>` convention
- [ ] Block names follow `load_`, `transform_`, `export_` patterns
- [ ] `metadata.yaml` has a `description` and release inputs defined as `variables`
- [ ] Layer 2 `@test` decorators on all Python blocks
- [ ] `ON CONFLICT DO UPDATE` on all SQL blocks writing to `modelled.*`
- [ ] No hardcoded S3 paths or credentials in block code
- [ ] Mapping and transformation decisions commented inline
- [ ] `methodology_url` set to the source's methodology documentation
- [ ] `internal_review_url` set to OEF's Notion review page
- [ ] Catalog entry complete: `production_approved`, `is_latest`, `pipeline_name`, `data_quality` scores, `retrieved_at`
- [ ] Reviewed by a second team member

### For new releases

- [ ] New release entry appended with incremented `version_number`
- [ ] Previous release set to `is_latest: false`
- [ ] `data_quality` scores reviewed (not copied forward without re-evaluation)
- [ ] License confirmed for this release
- [ ] `methodology_url` and `internal_review_url` updated if methodology changed
- [ ] Pipeline variables updated and run end-to-end without errors
- [ ] Any Layer 3 flags investigated and documented
