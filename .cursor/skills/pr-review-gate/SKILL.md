---
name: pr-review-gate
description: Review a global-data PR for high-impact issues only (≥7/10). Pipeline correctness, identity-key safety, idempotency, catalog hygiene.
---

# pr-review-gate — global-data

Same philosophy as the cross-repo skill: report only `impact >= 7` findings.

## Must-check list (in addition to the cross-repo defaults)

- **Identity keys** — `actor_id` / `locode` used as city key; `datasource_name` exact-match. Anything else is a bug.
- **Idempotency** — `modelled.*` SQL writes are UPSERTs (or there's an explicit reason).
- **Catalog drift** — if `production_approved: true` was set, `pipeline_name` and `data_quality` are filled.
- **Schema drift** — if a `modelled.*` table is altered, all writers are updated in the same PR (or an explicit follow-up issue is referenced).
- **Naming** — pipeline / staging / S3 paths follow `engineering-standards/naming-conventions.md`.
- **Tests** — Mage `@test` checks beyond `assert output is not None` (schema, row count, identity uniqueness, plausibility).

## Output format

Same as cross-repo:

```markdown
- file: dataset-review/catalog/index.yaml
  line: 142
  severity: 9/10
  comment: production_approved=true but data_quality is null. Either fill it or set production_approved=false.
```

If nothing ≥ 7/10 → output exactly:

```markdown
No review comments above 7/10 impact.
```

Max 5 findings. Concrete, evidence-based.
