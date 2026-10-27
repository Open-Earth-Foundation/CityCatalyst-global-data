---
name: dataset-test
description: >
  Validate and profile a dataset after a pipeline has loaded it into the modelled
  database. Use when the user wants to test/validate loaded data, check a modelled
  table, write or run data expectations, check nulls / value sets / ranges, produce a
  data-quality or validation report, or "say something about the data". The post-load
  layer that complements Mage's in-pipeline @test checks; runs against the live DB.
---

# Dataset Test (post-load validation + profiling)

After `dataset-pipeline` lands a dataset in `modelled.*`, confirm what actually
landed and **say something about it**. This is the layer Mage's in-pipeline `@test`
can't cover: it runs against the live database, so it catches what the SQL transform,
the FK constraints, and the load did to the data.

It produces two things from one run: a **pass/fail gate** and a **`validation_report.md`** —
the statement about the data (counts, null rates, value distributions, ranges) that
becomes the review's evidence and the regression baseline.

Lightweight by design (no Great Expectations / dbt): a declarative `expectations.yaml`
per release + one shared runner. See `data-quality-and-validation.md` for the Layer
1/2/3 philosophy this implements against the DB.

## The three tiers (in `expectations.yaml`)

- **structural** — the contract: PK unique/not-null, required-not-null columns,
  composite uniqueness, FKs resolve. Hard fail. Generic to any table.
- **invariants** — what's true *in reality, for any release*: value sets (controlled
  vocabularies), numeric ranges, row rules (e.g. `close_date >= open_date`). Hard fail.
  These are domain knowledge and survive across releases — the durable guardrails.
- **snapshot** — *this* release's observed facts: row count, distinct counts, group
  counts. A regression catch; re-confirmed each release (like the DoD's data-quality
  scores, never copied forward blindly).

## The loop (how the pieces feed each other)

1. Author `structural` + `invariants` by hand, from the review's claims + domain truth.
2. Run the runner → it validates those **and profiles** the table, writing
   `validation_report.md`. The profile *is* the snapshot: read it, then commit the
   `snapshot` block (now regression-locked).
3. Re-runs validate all three and regenerate the profile, so drift is a diff.

So the process states facts about the data (the report), those facts become the
review's evidence and the baseline, and the invariants encode what must always hold.
Validation feeds back into the review — closing discover → review → pipeline → test.

## Checkpoints

### Step 1 — Author expectations
Create `expectations.yaml` in the release's `tests/` folder (next to `review.md`).
Fill `structural` and `invariants` from the review and domain knowledge; leave
`snapshot` for Step 3. Schema + examples in `references/expectations-schema.md`.

### Step 2 — Run it (human-run — needs the DB)
The runner connects to the local global-api DB via `.env`, so **the user runs it**
(the agent has no DB access). Prompt them:
```
DATABASE_URL=postgresql://… python <skill>/references/run_expectations.py path/to/expectations.yaml
```
`--dry-run` prints the SQL without a DB (agent can use this to sanity-check). The agent
reviews the printed report / `validation_report.md` with the user.

### Step 3 — Read the profile, lock the snapshot, feed the review
From the report: commit the `snapshot` block (the observed counts), fix any real
failures (e.g. a null in a should-never-be-null column → a pipeline fix), and carry the
data statements into the dataset's `review.md` evidence. A failing check is a finding to
act on, not a number to silence.

## Failure handling (per data-quality-and-validation.md)
- **structural / invariants** → hard fail. Fix the data or the pipeline; don't weaken
  the expectation to make it pass.
- **snapshot** → fails on change; re-confirm the new number is correct, then update it.
- **profile** → never fails; it's the statement. Investigate anything surprising and
  record the conclusion (documentation, not rejection).

## References
- `references/run_expectations.py` — the generic runner (validate + profile + report).
- `references/expectations-schema.md` — the `expectations.yaml` format and check types.
- `references/check_source_urls.py` — liveness check: HEAD/GETs each distinct `source_url` and
  flags rows missing a URL or pointing to a dead page. Network-dependent, so run it manually
  (locally), not as a gate. Use it whenever a dataset must link out to real pages.
