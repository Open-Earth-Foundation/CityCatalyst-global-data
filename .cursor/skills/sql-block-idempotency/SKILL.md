---
name: sql-block-idempotency
description: Audit a SQL data_exporter block for idempotency (UPSERT semantics, no destructive truncates). Use when reviewing or writing a SQL block targeting modelled.*.
---

# sql-block-idempotency

`modelled.*` writes must be idempotent — re-running the pipeline must produce the same final state.

## Required pattern

```sql
INSERT INTO modelled.<table> (<cols>, created_at, updated_at)
SELECT <…>, NOW(), NOW()
FROM <staging>
ON CONFLICT (<unique_key_cols>)
DO UPDATE SET
    <non_key_col_a> = EXCLUDED.<non_key_col_a>,
    <non_key_col_b> = EXCLUDED.<non_key_col_b>,
    updated_at      = NOW();
```

## Audit checklist

- [ ] `INSERT INTO modelled.<table>` — no `DELETE` / `TRUNCATE` of `modelled.*`.
- [ ] `ON CONFLICT (<unique key>) DO UPDATE` present.
- [ ] Conflict columns match a real unique constraint (`SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint WHERE conrelid = 'modelled.<table>'::regclass`).
- [ ] `created_at` only set on insert (`NOW()` initially, kept on update via `EXCLUDED.created_at` only if you want it preserved — usually leave the existing value alone, so don't list `created_at` in DO UPDATE SET).
- [ ] `updated_at = NOW()` in DO UPDATE SET.
- [ ] `release_id` set on every write (mandatory for `modelled.*` per `data-model-design.md`).
- [ ] `datasource_name` is the exact-match value, not a `LIKE` pattern.

## Anti-patterns

- `DELETE FROM modelled.<table> WHERE datasource_name = '…'; INSERT …` — destroys provenance and breaks foreign keys.
- `TRUNCATE modelled.<table>` — never. This isn't staging.
- `INSERT … ON CONFLICT DO NOTHING` for fact tables — silently drops updated values.
- Missing `release_id` — orphans the row from its dataset release.

## Fix recipe

If you find a destructive pattern:

1. Identify the table's unique key (`pg_constraint`).
2. Rewrite as `INSERT … ON CONFLICT … DO UPDATE`.
3. Add a smoke `@test` block that runs the same input twice and asserts the row count is unchanged.
4. Note the change in the PR body — this is a behavioural change worth flagging.
