---
name: simplify-after-change
description: Simplify only the files touched in this change. Preserve behaviour. No new dependencies.
---

# simplify-after-change — global-data

Same philosophy as the cross-repo skill. Apply only to:

1. files edited in this change, or
2. the currently open file(s).

Do not refactor unrelated modules.

## Specifically for Mage blocks

- Remove leftover Jupyter-style `display(df)` / `df.head()` calls.
- Inline single-use helpers if they live next to the only caller and don't aid readability.
- Replace `inplace=True` chains with explicit assignment.
- Drop unused `kwargs` reads.
- Drop `@test` blocks that only assert `output is not None` — replace with a real schema/uniqueness check (or delete and file a follow-up issue).

## Non-negotiables

- Preserve identity-key handling (`locode` / `actor_id`, `datasource_name`).
- Preserve idempotency of `modelled.*` writes.
- Preserve logging at INFO+ levels.
- Do not introduce new deps in `cc-mage/requirements.txt`.

## Output

Bullet-list what you simplified and why.
