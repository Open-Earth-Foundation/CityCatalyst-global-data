# Pipeline Design Patterns

## Standard Block Flow

Every production pipeline follows the same structural pattern. Understanding this flow makes it easier to read an unfamiliar pipeline and to know where a problem is likely to originate.

```
data_loader (Python)          reads source file from S3 (files stage)
  └── data_exporter (Python)  writes to raw_data staging table (if_exists='replace')
        └── transformer (SQL) joins, cleans, and maps staging → modelled shape
              └── data_exporter (SQL) → modelled.* table (release-scoped delete + insert)
                    └── data_exporter (SQL) drops the raw_data staging table(s) — final cleanup
```

Deviations from this pattern should be deliberate and documented. If a pipeline skips the staging step, or writes to modelled from Python rather than SQL, that decision should be explained in a comment.

---

## Multiple Sources — Integrate in the Pipeline, Not Before Upload

Each source dataset is cleaned and analysed **on its own**, at the review stage, and uploaded **independently** to its own S3 path under the naming convention (`raw_data/<publisher_key>/<dataset_key>/release/<version>/…`). **Never pre-aggregate several sources into one combined file before upload.**

The reason is updatability: if ten sources are merged into a single uploaded artifact, refreshing one source means regenerating and re-uploading the whole blob, and the provenance of each row is muddied. Keeping one upload per source means any single dataset can be re-cleaned and re-uploaded on its own cadence without touching the others.

When a modelled table draws on several sources, the **integration happens inside the pipeline**, and **each source gets its own ingestion block** — not one block that loops over every source. Per-source blocks make the DAG self-documenting, let a single source fail/retry in isolation, and show exactly which sources feed the table.

```
load_<source_a>_staging (py, reads its S3 file)  ┐
load_<source_b>_staging (py, reads its S3 file)  ├─→ merge_<dataset> (transformer: align + union) → export → modelled.*
load_<source_c>_staging (py, reads its S3 file)  ┘
```

Keep the per-source loaders **thin**: read that source's S3 file, tag it with its `source_dataset`, return the raw frame. When the cleaning is uniform across sources, put that single shared transform in the **merge/integration block** (which receives all the per-source frames), rather than repeating it in every loader — this avoids duplicating logic while still giving each source its own ingestion block. A source with a genuinely different shape (e.g. a multi-locale triple) does its source-specific shaping in its own loader; that is the point of per-source blocks.

Do **not** collapse the sources into a single looping loader. The small amount of per-block boilerplate is the cost of an explicit, restartable DAG, and it is worth paying.

---

## Idempotency

A pipeline is idempotent if running it multiple times produces the same result as running it once. This is the single most important design constraint — without it, a re-run (whether triggered accidentally, as a retry, or to reload a release) corrupts the data.

### Staging tables — use `replace`

Python data exporters writing to `raw_data.*_staging` tables should always use `if_exists='replace'`. Staging tables are intermediate and disposable — replacing them on every run is correct and safe.

```python
loader.export(
    df,
    schema_name,   # 'raw_data'
    table_name,    # e.g. 'ct_onroad_staging'
    index=False,
    if_exists='replace',
)
```

### Modelled tables — default: release-scoped `DELETE` then `INSERT`

A plain `INSERT` with `export_write_policy: append` creates duplicate rows on re-run — the most common source of data duplication in the repo. There are two idempotent ways to fix it, and the choice matters:

**Default (full-refresh per release): delete the release's rows, then insert.** Because most pipelines are full refresh per release, the cleanest idempotent write is to clear the current release and rebuild it. This is the only pattern that also removes **stale rows** — records that existed in a previous run but are no longer in the source (a dropped row, a changed natural key). An upsert silently leaves those behind; a scoped delete does not.

```sql
-- 1) clear only THIS release's rows (never a global DELETE / TRUNCATE)
DELETE FROM modelled.emissions
WHERE release_id = MD5(CONCAT_WS('-', '{{ datasource_name }}', '{{ dataset_name }}', '{{ release_version }}'))::UUID;

-- 2) insert the current release fresh
INSERT INTO modelled.emissions (emissions_id, actor_id, ..., release_id)
SELECT ...
FROM raw_data.ct_onroad_staging;
```

The `DELETE` **must** be scoped to the release (or the dataset's own rows) via a `WHERE` on `release_id` or `datasource_name` — never an unscoped `DELETE`/`TRUNCATE`, which would wipe other releases or datasets sharing the table. Deterministic ids (`release_id`, row PK) make the delete-and-reinsert land on exactly the same keys each run.

### Deterministic identity — hash stable slugs, not descriptive URLs

Identity ids are MD5s of **stable identifiers only**:

```
dataset_id = MD5(datasource_name · dataset_name)
release_id = MD5(datasource_name · dataset_name · version_label)
row PK     = MD5(source_natural_key · release_id)
```

Do **not** include `dataset_url` (or any other descriptive, mutable, or nullable field) in an identity hash. `dataset_url` is *where to verify the data* — it can change when a publisher moves a page, and it is `null` for derived datasets with no single source; folding it into the key makes the identity fragile and breaks the link between `dataset_release` and `publisher_datasource` if it ever changes. Keep it as a stored column, out of the hash. (Some older pipelines hash `dataset_url` in — that is the pattern to correct, carefully, since changing it re-keys already-loaded data.)

**Alternative (`ON CONFLICT DO UPDATE`): only when you can't scope a delete.** Use an upsert when the table is co-populated such that no single predicate isolates this run's rows (e.g. several sources interleaved on a shared key you don't own), or when you deliberately want to preserve rows not present in the current source. Be aware this does **not** remove stale rows.

```sql
INSERT INTO modelled.emissions (emissions_id, ...) SELECT ...
ON CONFLICT (emissions_id) DO UPDATE SET emissions_value = EXCLUDED.emissions_value, ...;
```

**What to do with existing pipelines that use plain append:** when touching one as part of other work, convert it to the release-scoped delete+insert (or `ON CONFLICT` where a delete can't be scoped). Do not leave a plain append in a pipeline you have otherwise reviewed.

---

## Parameters Over Hardcoding

Pipelines process multiple releases of the same dataset over time. Any value that changes between releases — the source file path, the release year, the S3 key — must be a pipeline variable, not hardcoded in block logic.

Variables are defined in `metadata.yaml` under the `variables` key and accessed in blocks via `kwargs`:

```yaml
# metadata.yaml
variables:
  release_version: "2024"
  source_path: "files/cl_ine/cl_ine_censo/release/2024/cl_ine_censo_demographics.csv"
```

```python
# In a block
release_version = kwargs['release_version']
source_path = kwargs['source_path']
```

At minimum, every pipeline should parameterise:

- `release_version` — matches the version label in the catalog release entry
- `source_path` or `source_url` — where to retrieve the source data from S3 or the web

This enables re-runs to be triggered programmatically using the information in the catalog, and makes it clear exactly which release a given pipeline run processed.

---

## Full Refresh vs Incremental

Most pipelines in this repo are **full refresh per release** — they load all data for a given release version in a single run, parameterised by `release_version`. This is the default pattern and should be used unless there is a specific reason to do otherwise.

A full refresh pipeline:
- Replaces the staging table entirely on each run (`if_exists='replace'`)
- Upserts into modelled tables (idempotent by design)
- Can be re-run safely any number of times for the same release

An incremental pipeline — one that only processes new or changed records — is only appropriate when the source data is genuinely too large to reload in full, or when the source provides a reliable change feed. If you are considering an incremental approach, discuss it with the team first. The added complexity (tracking state, handling late arrivals, managing deletions) is rarely justified for the data volumes we work with.

---

## Logging

Mage captures block output and makes it visible in the pipeline run UI. Use this rather than relying on `print()` statements scattered through block code.

For structured information about what a block processed, return or print clearly labelled output at the end of the block:

```python
print(f"Loaded {len(df)} rows for release {release_version}")
print(f"Unique locodes: {df['actor_id'].nunique()}")
```

For Layer 3 plausibility flags (see [Data Quality & Validation](./data-quality-and-validation.md)), log the flag clearly so it is visible in the run output:

```python
yoy_change = (current_total - previous_total) / previous_total
if abs(yoy_change) > 0.30:
    print(f"[FLAG] Year-over-year emissions change is {yoy_change:.1%} — investigate before approving")
```

Avoid using logging as a substitute for comments. If something in the code needs explanation, explain it inline. Logs are for runtime information about data; comments are for reasoning about code.

---

## Error Handling

Mage propagates unhandled exceptions as block failures and stops the pipeline. This is the correct default behaviour for structural errors — do not silently swallow exceptions.

The right place to handle errors explicitly is at the data loading step, where failures have a clear and recoverable cause:

```python
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
except requests.HTTPError as e:
    raise ValueError(f"Failed to fetch source data from {url}: {e}")
except requests.Timeout:
    raise ValueError(f"Request timed out fetching {url} — check source availability")
```

Re-raise as a descriptive `ValueError` rather than letting the raw exception propagate — it makes the run log easier to diagnose.

Do not use try/except to mask failures and allow the pipeline to continue with incomplete data. A pipeline that silently produces partial output is worse than one that fails loudly.

---

## Lookups and Mappings as Data

A pipeline often needs a mapping: source column → modelled column, raw category → canonical value, code → label. Treat a **large or frequently-edited** lookup as data, not a code literal — but **never read it from a local repo file inside a block.** Mage executes block code with `exec()`, so `__file__` is undefined and there is no reliable repo-relative path; we also deliberately keep pipelines free of local-file dependencies (the only inputs a block reads are S3 for data and GitHub for the catalog).

So a mapping lives in exactly one of two places:

- **Inline in the block** — for small, stable maps (roughly ≤ a few dozen rows that change rarely). A `dict` literal is fine and clearest.
- **In S3 (or GitHub), read like any other input** — for genuinely large or often-changed lookups, upload the CSV to S3 and read it the same way the block reads its data (`S3.with_config(...).load(...)`), or fetch it from GitHub raw (as the catalog block does for `index.yaml`). This keeps "a mapping is data you can edit without touching code" *and* the no-local-files rule.

```python
# large/changing lookup as data — read from S3, not a repo path
field_map = S3.with_config(ConfigFileLoader(config_path, "default")).load(bucket, "raw_data/<...>/field_map.csv")
lookup = dict(zip(field_map["source_field"], field_map["modelled_field"]))
```

The line to draw: **a lookup table is data; control flow is code.** A many-row correspondence (category crosswalks, code→name tables) is data — inline if small, S3 if large. A handful of `if/elif` branches encoding genuine logic (e.g. "if access is via the BIP gate, the tier is gated") is control flow and stays inline. What you must *not* do is `pd.read_csv(Path(__file__)... )` against the repo — that breaks under Mage and reintroduces a local-file dependency.

---

## Reserved Column Names

Mage's Postgres exporter **renames reserved-word columns** when it auto-creates a staging table — `status` becomes `_status`, `order` becomes `_order`, etc. The modelled SQL then fails with `column s.status does not exist` (hint: "did you mean `s._status`"). Quoting does not help, because the column was genuinely renamed.

Fix it at the source, in your control: **do not name a staging/dataframe column with a reserved word.** Rename it to something descriptive and safe in the transformer (`status` → `opportunity_status`, `order` → `sort_order`), and map it back to the real column in the modelled `INSERT`. Add a fail-fast guard in the export-to-raw block so a reserved name is caught with a clear message rather than a cryptic `UndefinedColumn` later:

```python
RESERVED_COLUMN_NAMES = {"status", "order", "group", "user", "type", "end", ...}
bad = sorted(c for c in df.columns if c.lower() in RESERVED_COLUMN_NAMES)
if bad:
    raise ValueError(f"Reserved column name(s) {bad} will be mangled by Mage's export; rename them.")
```

Common offenders: `status`, `order`, `group`, `user`, `type`, `end`, `table`, `column`, `default`, `references`, `desc`, `asc`. Extend the set when you hit a new one.

## SQL Block Comments

Mage pre-processes a raw-SQL block by tracking quote/statement state and splitting on `;` — **and it does this through `--` comments too, not just live SQL.** Two failure modes, same root cause:

- A **`;` in a comment** cuts the statement early — `-- see x.md); the rest…` runs `the rest…` as its own query (`syntax error at or near "the"`).
- An **apostrophe in a comment** (`dataset's`, `releases'`, `if_exists='replace'`) looks like an opening string quote, so the real `;` is treated as inside a string and the statement never terminates (`syntax error at end of input`).

So in SQL blocks, keep comments **plain ASCII prose**:

- **No apostrophes** — write `dataset` not `dataset's`, `the pipeline` not `pipeline's`, `via replace` not `if_exists='replace'`.
- **No `;`** — reword with `—`, `.`, or `,`.
- Short, on their own line, above the statement they describe. **No commented-out SQL** left in the block.

When in doubt, a comment that contains only letters, spaces, and `. , - ( ) /` is safe; `'`, `"`, and `;` are not.

**This is enforced, not just advised.** `cc-mage/scripts/lint_sql_comments.py` fails on any `--` comment containing `'`, `"`, or `;`; it runs as a pre-commit hook on changed `.sql` files (`.pre-commit-config.yaml`). Run it directly any time: `python cc-mage/scripts/lint_sql_comments.py <files-or-dir>`.

---

## Guiding Principles

- **Idempotency is not optional.** A pipeline that cannot be safely re-run will eventually corrupt production data. Design for re-runs from the start.
- **Staging tables are throwaway — and dropped at the end.** They exist only to support the SQL transform step; do not read from them in other pipelines or use them for reporting. The pipeline's final block is a SQL exporter that `DROP TABLE IF EXISTS` each `raw_data` staging table it created, so `raw_data` doesn't accumulate clutter. They're recreated by the next run (`if_exists='replace'`), so dropping is safe.
- **Parameters belong in `metadata.yaml`, not in block code.** Block code should be release-agnostic; releases are distinguished by variables.
- **The block DAG is documentation.** A well-structured pipeline communicates its intent through its block names and connections. Name blocks clearly and keep each block focused on one responsibility.
- **Lookups are data, logic is code — but no local-file reads.** Small/stable maps inline; large/changing maps in S3 (read like data); never a repo-relative CSV read inside a block (Mage has no `__file__`). Only genuine control flow stays in code.
- **A block reads only S3 and GitHub.** Source data from S3, the catalog/index from GitHub raw, Mage's own `io_config.yaml` via `get_repo_path()`. No other local-repo file dependencies.
- **Never hand-edit a data file.** Source CSVs/extracts are fixed in the extraction/cleaning *code* or by refetching with new rules — never by editing the file. A manual edit is invisible, unrepeatable, and lost on the next refresh. (Pipeline *code* and *config* like the catalog are edited normally; raw/source *data* is not.)
- **Country-agnostic vocabulary.** Structural fields and their canonical values are universal; a country's own terms are *values/detail*, not the model. Use `gated`, not `BIP-SNI-gated`; `regional`, not `GORE`. The local specifics live in a detail column, a note, or `source_extras`.
- **Multi-valued fields are arrays.** If a field can legitimately hold several values (sectors, eligible actors, access modes), model it as a JSONB array — don't collapse to a primary value or stuff a delimited string. Singular-by-nature fields stay scalar.
- **The complexity is in the domain, not the code.** The problems here are intricate, but a well-understood problem yields simple code. Prefer the smallest block that is correct and readable over defensive scaffolding. If a block is hard to read, the understanding is not finished yet — clarify the model, then write the simple version.
