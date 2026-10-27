# expectations.yaml — format

One file per release, in the release's `tests/` folder. Run with
`run_expectations.py`. Every section is optional; include what applies.

```yaml
table: modelled.<table>          # required — the table to validate
partition_by: source_dataset     # optional — column the profile breaks down by

structural:                      # the contract — hard fail
  primary_key: <pk_col>                        # unique + not-null
  required_not_null: [colA, colB]              # no nulls allowed
  unique:                                      # composite-key uniqueness
    - [col1, col2, col3]
  foreign_keys:                                # every value resolves in the parent
    - {column: <col>, references: "modelled.<parent>.<parent_col>"}

invariants:                      # true in reality for ANY release — hard fail
  value_sets:                                  # controlled vocabulary (nulls ignored)
    <col>: [allowed, values, here]
  ranges:                                      # numeric bounds (nulls ignored)
    <col>: {min: 0, max: 1000000}
  row_rules:                                   # raw SQL boolean; row fails only if FALSE
    - "close_date >= open_date"                # (NULL on either side = passes)
    - "amount_paid <= amount_committed"

snapshot:                        # THIS release's observed facts — regression
  row_count: {equals: 99}                      # or {min: 90, max: 110}
  distinct_count:
    <col>: 10
  group_counts:                                # exact per-value counts
    <col>: {value_a: 89, value_b: 7}
  min_non_null:                                # at least N non-null
    <col>: 6

profile:                         # descriptive only — drives validation_report.md
  categorical: [colA, colB]      # value distributions
  numeric: [amount_clp]          # min / max / avg / non-null
  dates: [open_date, close_date] # min / max / non-null
```

## Check semantics

| Section | Check | Passes when | Level |
|---|---|---|---|
| structural | `primary_key` | no duplicate and no null keys | fail |
| structural | `required_not_null` | zero nulls in the column | fail |
| structural | `unique` | no duplicate groups for the column set | fail |
| structural | `foreign_keys` | every non-null value exists in the parent | fail |
| invariants | `value_sets` | every non-null value is in the allowed list | fail |
| invariants | `ranges` | every non-null value is within [min, max] | fail |
| invariants | `row_rules` | the expression is never explicitly FALSE | fail |
| snapshot | `row_count` / `distinct_count` / `group_counts` / `min_non_null` | matches the recorded baseline | fail (re-confirm per release) |
| profile | — | always; produces the report | n/a |

## Choosing the tier

- **Will it be true next release too?** → `invariants` (value sets, ranges, relationships).
- **Is it just what we have right now?** → `snapshot` (counts) — generate it from the profile, don't hand-guess.
- **Is it the table's shape/contract?** → `structural`.

`row_rules` take any Postgres boolean expression over the row — it's trusted config, so
keep them in the YAML, not in code. Nulls make a rule pass (use `IS NOT NULL` inside the
expression if a null should fail).
