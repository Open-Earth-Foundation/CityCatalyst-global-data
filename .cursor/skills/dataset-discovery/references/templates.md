# Output templates

One folder per need: `dataset-discovery/needs/<YYYY-MM-slug>/` with exactly
three files. Field-ownership rule: machine-checkable criteria live only in
search.yaml; intent and lifecycle only in need.md; results only in
candidates.yaml.

## need.md — intent and lifecycle

```yaml
---
id: 2026-06-cl-waste
title: <one line>
status: open            # open | resolved | gap_confirmed | superseded
opened: YYYY-MM-DD
requested_by: <person>
serves: <ghgi | ccra | action-prioritization | other>

outcome:
  candidates: []        # promote/investigate ids once searched
  resolution_notes: null
---

## Context
Why this came up, current proxies, prior searches, leads. No criteria here.

## Open questions
- Decisions the search surfaced that need a human answer.
```

## search.yaml — screening parameters

```yaml
need: <need id>

sector: <GPC sector / theme>
themes: []

action_taxonomy:        # only if results must map to a taxonomy/schema
  framework: <name>
  catalog_ref: <index.yaml id if tracked>

geography:
  countries: []         # or global
  required_level: <admin level below which a dataset fails, or none>

data_requirements:
  must_have: []
  nice_to_have: []
  metric_form: <acceptable forms, or any>
  temporal: <coverage + cadence needed>

constraints:            # graded — each may be null
  license: {preferred: ..., acceptable: ..., disqualifying: ...}
  access: {preferred: ..., acceptable: ..., disqualifying: ...}

screening_guidance: >
  How the use case adjusts quality bars (e.g. ordinal ranking tolerates
  uncertainty; internal consistency may outweigh accuracy).
```

## candidates.yaml — search output

```yaml
candidates:

- id: <publisher-shortname-dataset-shortname>
  name: <full name>
  publisher: <org>
  url: <primary>
  also: []              # optional supporting links
  themes: []
  coverage: <geography, unit of analysis, breadth — one or two lines>
  access: <how to get it; say "unverified" when it is>
  license: <terms; say "unverified" when it is>
  screening:
    verdict: promote | investigate | deprioritize | reject
    notes: >
      Why this verdict, written for the next person who searches this
      theme. For reject: reason + date + what would reopen it.
  added: YYYY-MM-DD
```

After promotion, collapse the entry to a stub: keep id, verdict `promoted`,
and a pointer to the `index.yaml` id. Rich structure lives in one place only.

Re-runs: append to candidates.yaml with new `added` dates, or write a dated
sibling (`candidates-YYYY-MM.yaml`) if the re-run replaces the old results.
