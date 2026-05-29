---
name: definition-of-done-check
description: Run the engineering-standards Definition of Done checklist against a pipeline or release. Use before promoting production_approved=true, or when the user asks "is this ready for prod?".
---

# definition-of-done-check

Authoritative checklist lives in `engineering-standards/definition-of-done.md`. This skill is the agent's runner.

## When to use

- Before flipping `production_approved: true` on a dataset release.
- Before merging a "promote pipeline" PR.
- When asked "is `<pipeline>` ready for prod?".

## Run order

### A. New pipeline

- [ ] Pipeline name follows `naming-conventions.md`.
- [ ] `metadata.yaml.description` is non-null and matches the README.
- [ ] All variables in `metadata.yaml.variables` (no hardcoded values).
- [ ] Layer 2 tests present on every transformer and exporter (schema, row counts, identity uniqueness).
- [ ] Layer 3 tests present where ranges are knowable (plausibility flags).
- [ ] Catalog entry exists in `catalog/index.yaml`, `production_approved: true`, `pipeline_name` and `data_quality` non-null.
- [ ] `dataset-review/reviews/<publisher>/<dataset>/README.md` mentions the pipeline.
- [ ] Notion methodology page linked from `urls` in catalog.
- [ ] Peer review in PR (CTO sign-off).

### B. New release of existing pipeline

- [ ] New release folder added under `reviews/<publisher>/<dataset>/releases/<version>/`.
- [ ] Old release `is_latest: false` flipped.
- [ ] If the schema changed, `review.yaml` includes a `schema_changes:` block.
- [ ] Pipeline forked as `_v<year>` (old still runnable).
- [ ] Layer 2 + 3 tests pass on a real run against the new release.
- [ ] PR includes row counts from a successful local run.

## Output

Run silently if everything passes. Otherwise output:

```markdown
- [ ] <check that failed>
  - reason: <evidence from file>
  - fix: <minimal action>
```

If 5+ checks fail, also recommend splitting into a smaller PR.
