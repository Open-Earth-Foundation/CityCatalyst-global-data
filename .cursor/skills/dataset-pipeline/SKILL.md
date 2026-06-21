---
name: dataset-pipeline
description: >
  Build the Mage pipeline that ships a vetted dataset into the modelled
  database — the third stage after discover → review. Use whenever the user
  wants to build/create a pipeline, ship or promote a reviewed dataset to
  production, load a cleaned dataset into modelled.*, register a dataset in
  the catalog, upload source/cleaned data to S3, or "wire up the pipeline for
  <dataset>". Orchestrates the stage and defers the how-to to
  knowledge-base/topics/engineering-standards/; it does not restate those
  standards.
---

# Dataset Pipeline (build)

Take a dataset that has passed `dataset-review` and ship it to production: a
catalog entry, the data in S3, a Mage pipeline that lands it in `modelled.*`,
and the definition-of-done met. The hard thinking was done in review — this
stage is disciplined assembly, so the bar is **clean, idempotent, minimal**.

The conventions already exist and are authoritative; this skill sequences the
work and points at them. Do **not** copy their content into pipeline code or
into this skill:

- `knowledge-base/topics/engineering-standards/pipeline-design-patterns.md` — the standard block flow, multi-source integration, idempotency (release-scoped delete+insert), deterministic identity, lookups (inline/S3, no local files), reserved-word & SQL-comment gotchas, staging cleanup, minimal-code.
- `…/naming-conventions.md` — snake_case, the `files/` vs `raw_data/` S3 stages, block names.
- `…/data-quality-and-validation.md` — the `@test` layers.
- `…/definition-of-done.md` — the gating checklist.
- `ARCHITECTURE.md` — the modelled schema and stage map.

## Checkpoints — work in increments

Run as five steps, **stopping after each to show what you did and let the
human decide to continue**. The skill owns the legwork (entry drafting, command
generation, skeleton wiring, test scaffolding); the human owns the judgment
calls (license, production approval, the second-reviewer sign-off).

**Human-run handoffs — the agent must explicitly prompt for these and wait; it
cannot do them itself.** These need the user's machine, credentials, or Mage
instance:

- **S3 uploads** (Step 2) — the agent has no AWS credentials. It generates the
  `aws s3 cp` commands and must **stop and ask the user to run them**. The pipeline
  reads its data from S3, so it cannot run until this is done.
- **Running the pipeline** in Mage (Step 4) — runs in the user's environment, not
  the agent's. The agent must prompt the user to trigger the run and report back.
- **Activating the API trigger** (Step 5) and holding its token — the agent writes
  `triggers.yaml`, the user syncs/activates it in Mage and owns the endpoint token.
- **Setting `production_approved: true`** and the second-reviewer sign-off (Step 4).

Always surface these as an explicit "your turn — please run X, then tell me the
result" prompt, never assume they happened.

### Step 1 — Catalog entry (always first)

**This is the first step, always.** The pipeline reads each dataset's identity
(publisher, name, version → `dataset_id` / `release_id`) from the catalog, so
nothing downstream is correct until the catalog is. Before anything else, make
sure **every dataset the pipeline touches has an entry** in
`dataset-review/catalog/index.yaml`:

- A **single-source** pipeline: add/update that one dataset's entry.
- A **multi-source** pipeline: confirm **all** source datasets have entries (they
  normally exist already from the dataset-review stage) — the pipeline will fail or
  mis-key if a source is missing from the catalog.

Use `references/catalog-entry.md` and fill every field the definition-of-done
requires for a release.

- **Do not set `themes`.** Themes are owned by `dataset-review/collections/`, not
  the index — leave them out of the entry.
- A new release appends to `releases` with the next `version_number` and flips
  the previous one to `is_latest: false`.
- `production_approved: true` is a human decision, set only after Step 4.

### Step 2 — S3 upload

Put the data in the two S3 stages with `references/s3-upload.md` (snake_case
paths per naming-conventions):

- **`files/`** — the original source file(s), as retrieved.
- **`raw_data/`** — the cleaned, tidy release data the loader will read.

**One dataset per upload — never pre-aggregate.** If the pipeline integrates
several sources, upload each on its own path; the union happens in the pipeline
(Step 3), not in a combined file. This keeps any single source independently
refreshable.

Generate the `aws s3 cp` commands and present them for the human to run; do not
execute them. **Stop here and explicitly ask the user to run the uploads** (after
`aws sts get-caller-identity`) — the pipeline cannot read its data until they have.
Wait for the user to confirm before moving to Step 3/4.

### Step 3 — Build the pipeline

Copy `references/pipeline-skeleton/` to `cc-mage/pipelines/<pipeline_name>/` and
fill it in. The standard flow is: per-source ingestion block(s) → merge/transform
→ export-to-raw → modelled → drop-staging, with a parallel catalog branch that
registers each source's release from `index.yaml`. The `cl_finance_opportunity_to_modelled`
pipeline is the worked reference. Keep that shape unless a deviation is deliberate and commented.

- Name `<prefix>_<source>_<description>`; blocks `load_` / `export_` / `transform_`.
- The only pipeline variables are release-varying **infra** values (e.g. `source_bucket`,
  `source_release_version`). Dataset/publisher **identity is read from the catalog**
  (next bullet) — never hardcoded or held as per-dataset variables.
- Staging write uses `if_exists='replace'`; the modelled write **deletes this
  release's rows then inserts** (scoped `DELETE WHERE release_id = …`, never
  global) so stale rows don't linger, with deterministic MD5 ids. Use
  `ON CONFLICT DO UPDATE` only when a delete can't be scoped. (Idempotency is
  not optional.)
- **Register a `publisher_datasource` + `dataset_release` for every source
  dataset, and read their identity from `dataset-review/catalog/index.yaml`** —
  do not hand-maintain per-dataset variables. A block reads the catalog for the
  pipeline's source ids, computes the ids (`dataset_id = MD5(datasource·dataset)`,
  `release_id = MD5(datasource·dataset·version)`), and upserts the registrations;
  each modelled row then carries **its own source's `release_id`** (join on the
  source key), so provenance/license/version are per-source, not lumped under one
  derived dataset. This keeps pipeline variables down to a handful.
- **A block reads only S3 (data) and GitHub (the catalog/index) — no local-repo
  files.** Mage runs blocks via `exec()`, so `__file__` is undefined; never
  `pd.read_csv(Path(__file__)…)`. A field/category mapping is inline if small, or
  in S3 (loaded like data) if large. Genuine control flow stays inline. Keep
  blocks the smallest correct version.
- **A data loader is a bare read — no transformation in the loader.** The `load_`
  block does exactly one thing: read the object from S3 and return the frame as-is
  (`S3.with_config(...).load(bucket, key)`). All shaping — deriving ids, filtering,
  renaming, slugging, casting — happens in a **downstream transformer**, never in the
  loader. This keeps loading robust: a load failure (missing key, bad path, creds) is
  cleanly separated from a transform bug, so you can see at a glance which block broke,
  and each block is independently re-runnable in the Mage UI. The worked example is
  `load_finance_opportunity_action_from_s3` (bare read) →
  `transform_finance_opportunity_action` (does the shaping). When a load "isn't
  working," first confirm the **S3 key actually exists** (the loader can only be as
  reliable as the upload in Step 2) — a bare loader makes that the obvious first check.
- **No reserved-word column names in the staging frame.** Mage's Postgres export
  renames them (`status` → `_status`), breaking the modelled SQL. Rename to a
  descriptive safe name in the transformer and map it back in the `INSERT`; the
  export-to-raw block carries a fail-fast guard for known reserved words.
- **Never hand-edit a source data file; country-agnostic vocabulary; multi-valued →
  arrays.** Fix data in the extraction code or refetch (not by editing the CSV); use
  universal values (`gated`, not `BIP-SNI-gated`) with local specifics in detail/extras;
  model genuinely multi-valued fields as JSONB arrays. (See pipeline-design-patterns.md.)
- **The pipeline's final block drops its `raw_data` staging table(s).** A SQL
  exporter (`DROP TABLE IF EXISTS raw_data.<…>_staging`) runs downstream of the
  modelled load. Staging is throwaway and recreated next run — don't leave it behind.
- **SQL-block comments: plain ASCII, no `'` `"` `;`, none commented-out.** Mage tracks
  quote/statement state *through* comments, so a `;` cuts the statement early and an
  apostrophe (`dataset's`, `if_exists='replace'`) makes it run to end-of-input. Write
  `dataset` not `dataset's`. **Enforced**: run `python cc-mage/scripts/lint_sql_comments.py <files>`
  before finishing any SQL block (also a pre-commit hook); fix every hit.

### Step 4 — Validate & gate

Make it production-ready against `definition-of-done.md`:

- `@test` blocks for the in-pipeline Layer-2 checks (not null, expected columns,
  required fields non-null, row count > 0); Layer-3 plausibility flags log, not fail.
- Run end-to-end against the real S3 data with no errors; report row counts and
  key cardinalities.
- **Post-load validation: invoke the `dataset-test` skill** — author the release's
  `expectations.yaml` (structural + invariants + snapshot) and have the user run the
  runner against the live DB. It writes `validation_report.md` (the data statement) and
  gates on hard failures. This is the layer the in-pipeline `@test` can't cover (FKs,
  the SQL transform, what actually landed).
- Only then: set `production_approved: true`, `is_latest: true`,
  `pipeline_name`/`pipeline_version` in the catalog, and route the second-reviewer
  sign-off to the human.

### Step 5 — Expose an API trigger

Once the pipeline runs green, give it an on-demand HTTP trigger so it can be re-run
without the UI (e.g. from a service, a scheduled job, or after a new release lands).
Add `cc-mage/pipelines/<pipeline_name>/triggers.yaml` (template in
`references/pipeline-skeleton/triggers.yaml`) with a single API trigger:

- **Name it `<pipeline_name>_api`** so the trigger is discoverable from the pipeline name.
- `schedule_type: api`, `status: active`.
- Pass release-varying values (e.g. `source_release_version`) in the POST body's
  `variables` to override the defaults for a given run.

Mage exposes the trigger as `POST /api/pipeline_schedules/<id>/pipeline_runs/<token>`;
the id/token are shown on the trigger in the Mage UI. **Human-run handoff:** the agent
adds `triggers.yaml`, but the user activates/syncs it in their Mage instance and holds
the token — the agent cannot call it. Triggering the run is the user's action.

## Failure modes (this skill's, specifically)

- **Restating the standards in code or comments.** Link to them; don't duplicate.
- **Hardcoding a release value** (path, year, bucket) in block code instead of a variable.
- **Reading a local-repo file from a block** (`pd.read_csv(Path(__file__)…)`) — Mage has no `__file__`; inline small maps, S3 for large.
- **Transforming inside a data loader** — a `load_` block must be a bare S3 read; do the shaping in a downstream transformer so load failures and transform bugs are isolated and each block is re-runnable.
- **A loader that "won't load" when the S3 key was never uploaded** — a bare loader can't fix a missing object; verify the Step 2 upload first.
- **Per-dataset identity as pipeline variables** instead of reading it from the catalog.
- **A non-idempotent modelled write** — plain `INSERT … append` duplicates on re-run; use release-scoped `DELETE` + `INSERT`.
- **An unscoped `DELETE`/`TRUNCATE`** — wipes other releases/datasets sharing the table; always scope to `release_id`.
- **Reserved-word column** in the staging frame (`status` → `_status`); **`;` inside a SQL comment** (breaks Mage's splitter).
- **Leaving staging tables behind** — the final block drops them.
- **Setting `production_approved: true` before Step 4** or without the second review.
- **Adding `themes` to the catalog entry** — that lives in collections now.

## References

- `references/catalog-entry.md` — the `index.yaml` release entry (themes omitted; `dataset_url` = source-to-verify).
- `references/s3-upload.md` — per-source upload to the two stages (`files/` + `raw_data/`), no pre-aggregation.
- `references/pipeline-skeleton/` — fill-in templates for the standard flow (catalog-driven identity, per-source ingestion, delete+insert, drop-staging) plus `triggers.yaml` (the `<pipeline_name>_api` API trigger).
