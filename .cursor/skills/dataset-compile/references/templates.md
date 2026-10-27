# dataset-compile templates

Generic skeletons for the four files in `dataset-compile/<slug>/`. Replace the
placeholder domain (ROLLUP, facet fields, categories) with the dataset's own.
The worked instance is `dataset-compile/mn-climate-awards/`.

## schema.json

```json
{
  "$schema_notes": "One-line description of the dataset, its rollup dimension, and its facet axes. State it's a compiled staging dataset, not an ingested external one.",
  "dataset": "<slug>",
  "title": "<human title>",
  "status": "compile",
  "grain": "one row per <record>",
  "primary_key": "id",
  "scope": {
    "in_scope": "which ROLLUP values / sources / time range are covered",
    "not_yet_in_scope": "what's deliberately left out",
    "complete_when": "the bar for 'done' — every source-record present, all derived fields computed by rule"
  },
  "field_provenance_legend": {
    "sourced": "read directly from a primary source (verifiable against source_url)",
    "derived": "assigned by judgment, NOT in the source — lower-trust until a rule is defined",
    "derived-by-rule": "computed by an explicit auditable lookup/rule (references/*), reproducible",
    "meta": "bookkeeping about the record"
  },
  "fields": [
    {"name": "id", "type": "string", "source": "meta"},
    {"name": "<rollup>", "type": "enum(...)", "source": "derived", "role": "rollup index"},
    {"name": "<facet_1>", "type": "string", "source": "sourced"},
    {"name": "<facet_2>", "type": "string", "source": "sourced"},
    {"name": "<value>", "type": "number|null", "source": "sourced"},
    {"name": "region_or_group", "type": "enum(...)", "source": "derived-by-rule", "notes": "via references/<lookup>.csv"},
    {"name": "verified", "type": "boolean", "source": "meta"},
    {"name": "source_url", "type": "string", "source": "sourced"},
    {"name": "source_title", "type": "string", "source": "sourced"},
    {"name": "notes", "type": "string", "source": "meta"}
  ],
  "promotion_path": "compile -> dataset-review (lock scope, derived->rule, fill gaps, complete provenance) -> catalog + pipeline."
}
```

## collection.md

```markdown
# <slug> — collection notes

Provenance and method for the compiled dataset in this folder. Staging dataset:
manufactured from public sources, not ingested, not yet vetted through dataset-review.

## What this is
<one paragraph: the records, the rollup dimension, the facet axes, and what it's for>

## How it was collected
1. Navigated by <reference map in knowledge-base>.
2. Targeted search per source category.
3. Fetched primary sources (see sources.yaml).
4. Extracted records; structured into schema.json.
5. Verified against control totals where available.

## Provenance is a gradient
List which fields are `derived` / `derived-by-rule` and why they're lower-trust.
Everything else is read from source.

## Verification status
Per source: what reconciled (against which published total), what is single-source,
what is null because only an aggregate is public.

## Insights — what the data says
<distributions, magnitudes, funnels, concentration — the findings the records reveal>

## Known gaps (the to-proper checklist)
<what's missing before promotion: derived->rule, unfilled sources, thin rollup values>

## Refresh model
No feed. Refresh = re-run the compile against sources.yaml and diff.

## Promotion
Graduates into dataset-review when scope is locked, derived fields are rules,
gaps are filled, and provenance is complete.
```

## sources.yaml

```yaml
# Source registry. No external feed exists; this list IS the refresh mechanism.
sources:
  - id: <short-id>
    rollup: <rollup value>
    source: <publisher / program>
    kind: <news-release | pdf-table | registry-page | committee-report | ...>
    url: <primary source url>
    local_copy: raw/<file>            # if a binary had to be downloaded
    last_fetched: YYYY-MM-DD
    yields: <what records/fields this source produced>
    notes: <quirks, blockers, verification note>
```

## references/<lookup>.csv (for derived-by-rule fields)

```csv
key,value,basis,confidence
<place-or-entity>,<assigned group/tier>,<county/rule basis>,<high|med|default|review>
```

One row per distinct key. Flag genuine edge cases `review` rather than silently
asserting. This is what turns a `derived` field into `derived-by-rule`: the rule
lives in one auditable place, correct it here and re-apply.
```
