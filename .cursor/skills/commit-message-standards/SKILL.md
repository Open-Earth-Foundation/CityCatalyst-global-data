---
name: commit-message-standards
description: Generate Conventional Commits messages for global-data. Pairs with pull-request-standards.
---

# commit-message-standards — global-data

Conventional Commits, ≤72 chars per line, imperative summary.

```
<type>(<scope>): <imperative summary>

<body — explain WHY, wrap at 72>

<footer — Refs: ON-####>
```

Recommended `<scope>`:
- `pipeline` — Mage pipeline (added / changed / removed).
- `mage` — Mage project / docker / config.
- `catalog` — `dataset-review/catalog/*`.
- `review` — `dataset-review/reviews/*`.
- `kb` — `knowledge-base/*`.
- `standards` — `engineering-standards/*`.
- `ci`, `docker`, `chore`, `docs`.

Examples:

```
feat(pipeline): add ghgi_ippu_climatetrace v2026 release

Pipeline mirrors v2025 with the new bucket layout. Updates
catalog entry to set v2026 as production_approved with a
data_quality summary.

Refs: ON-5712
```

```
fix(catalog): drop duplicate eurostat dataset id

The 2025 release was registered twice with slightly different
slugs, causing collections/collection.yaml to point at the wrong
release. Keep `eu-eurostat-energy-2025`, remove the typo entry.
```

```
docs(standards): clarify Layer 2 schema check expectations
```

Anti-patterns: `wip`, `update`, `fixed bug`, `cleanup`. Always state the WHY in the body when it isn't obvious from the diff.
