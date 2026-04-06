# Pipeline Design Patterns

## Standard Block Flow

Every production pipeline follows the same structural pattern. Understanding this flow makes it easier to read an unfamiliar pipeline and to know where a problem is likely to originate.

```
data_loader (Python)          reads source file from S3 (files stage)
  └── data_exporter (Python)  writes to raw_data staging table (if_exists='replace')
        └── transformer (SQL) joins, cleans, and maps staging → modelled shape
              └── data_exporter (SQL) → modelled.* table (ON CONFLICT DO UPDATE)
```

Deviations from this pattern should be deliberate and documented. If a pipeline skips the staging step, or writes to modelled from Python rather than SQL, that decision should be explained in a comment.

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

### Modelled tables — use `ON CONFLICT DO UPDATE`

SQL blocks writing to `modelled.*` tables must use an upsert pattern. A plain `INSERT` with `export_write_policy: append` will create duplicate rows if the pipeline is re-run. This is the most common source of data duplication in the repo.

```sql
INSERT INTO modelled.emissions (
    emissions_id,
    actor_id,
    gpc_reference_number,
    emissions_value,
    emissions_units,
    reporting_year,
    datasource_name,
    gpcmethod_id
)
SELECT ...
FROM raw_data.ct_onroad_staging
ON CONFLICT (emissions_id)
DO UPDATE SET
    emissions_value    = EXCLUDED.emissions_value,
    emissions_units    = EXCLUDED.emissions_units,
    reporting_year     = EXCLUDED.reporting_year,
    datasource_name    = EXCLUDED.datasource_name,
    gpcmethod_id       = EXCLUDED.gpcmethod_id;
```

The conflict target should be the table's primary key. For `modelled.emissions` this is `emissions_id`. For `modelled.emissions_factor` it is `emissionfactor_id`. Check the schema in [`ARCHITECTURE.md`](../ARCHITECTURE.md) if unsure.

**What to do with existing pipelines that use plain append:** When touching a pipeline as part of other work, add the `ON CONFLICT` clause opportunistically. Do not leave a plain append in a pipeline you have otherwise reviewed and updated.

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

## Guiding Principles

- **Idempotency is not optional.** A pipeline that cannot be safely re-run will eventually corrupt production data. Design for re-runs from the start.
- **Staging tables are throwaway.** They exist only to support the SQL transform step. Do not read from them in other pipelines or use them for reporting.
- **Parameters belong in `metadata.yaml`, not in block code.** Block code should be release-agnostic; releases are distinguished by variables.
- **The block DAG is documentation.** A well-structured pipeline communicates its intent through its block names and connections. Name blocks clearly and keep each block focused on one responsibility.
