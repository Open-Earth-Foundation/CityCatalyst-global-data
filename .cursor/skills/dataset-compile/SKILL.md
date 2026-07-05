---
name: dataset-compile
description: >
  Manufacture a structured staging dataset by compiling many public sources
  (award lists, registries, reports, portals) into schema'd, provenance-flagged,
  verified records — for cases where no single external dataset exists to adopt.
  Use whenever the user wants to compile, harvest, scrape, assemble, or "go
  collect examples/records" from scattered public sources; build a dataset that
  doesn't exist yet; or turn many announcements into one queryable table — even
  if they never say "compile". Sibling to dataset-discovery: discovery *finds*
  an existing dataset, compile *builds* one. Writes only to
  dataset-compile/<slug>/, never the knowledge base or the catalog.
---

# Dataset Compile (manufacture)

Some datasets you need don't exist as a single publisher's file — they're
scattered across dozens of public pages (award announcements, priority lists,
recipient tables, PDFs). This skill compiles that scatter into one structured,
provenance-tracked, verified staging dataset, ready to promote into
`dataset-review`.

It is the sibling entry point to `dataset-discovery` in the pipeline
**(discover | compile) -> review -> pipeline -> test**. Discovery finds and
triages a dataset that already exists externally; compile assembles one that
doesn't, from many sources. Both hand off to review. This skill writes **only**
to `dataset-compile/`, never to `knowledge-base/` (that's reference context) or
`dataset-review/catalog/` (that's for vetted external datasets).

The worked reference instance is `dataset-compile/mn-climate-awards/` (Minnesota
climate-finance awards, indexed by funding "route"). The method below is generic;
that folder is one set of values.

## What makes this different from an ingested dataset

An ingested dataset has one publisher, one license, and a feed to poll — it
belongs in `dataset-discovery` -> `dataset-review`. A compiled dataset is
**authored**: no single source, synthesised across many, and it changes as your
research proceeds, not as an upstream feed updates. That's why it gets its own
lane and its own provenance discipline (below), and why it's a *staging*
dataset — not knowledge, not yet a vetted dataset.

## Output contract

One folder per dataset: `dataset-compile/<slug>/` containing:

- `schema.json` — the contract: grain, primary key, scope, and **every field
  tagged `sourced` / `derived` / `derived-by-rule` / `meta`** (see provenance).
- `data.csv` — one row per record, flat and diff-friendly. Schema lives in
  `schema.json`, not here.
- `collection.md` — provenance & method: how it was compiled, the verification
  status, an insights section, and the to-proper gap checklist.
- `sources.yaml` — the source registry. Since there's no feed, **this list IS
  the refresh mechanism**; each entry carries a `last_fetched` date.
- `raw/` — source files that had to be downloaded (e.g. PDFs). Kept for
  re-parsing; URL-fetch-via-code may be unavailable, so a local copy matters.
- `references/` — optional deterministic lookups the derived-by-rule fields use
  (e.g. a place -> region map), kept auditable and separate from `data.csv`.

Skeletons for each are in `references/templates.md`.

## The core design: rollup index + facet axes

Pick one **rollup dimension** that is the natural parent of the records and that
determines their shape — in the reference instance it's the funding *route*,
because the route dictates what a fundable application must contain. Then keep a
small set of **facet fields** so the data backs a general `get_<records>(params)`
query and generalises to a second domain as new rows, not a rebuild. The rollup
is a derived parent tag layered on top of the facets, never a replacement for
them. Expect the rollup to be **lopsided** — some values richly enumerable,
others thin. That lopsidedness is a *finding*, not a gap: it tells you where the
reachable, documented records actually are.

## Workflow

### 1. Frame

Decide the grain (what is one row?), the rollup dimension, the facet fields, and
the query the dataset should answer. Write these into `schema.json` first — the
schema is the contract, and framing it up front stops the compile from drifting.

### 2. Navigate by an existing reference, don't compile blind

Check `knowledge-base/` for a map of the domain that says *where the records
live* — the reference instance was steered entirely by a landscape doc that
listed each route's award-list sources. If no such map exists, note it, rely on
general search, and consider seeding one. Reference context navigates; it is not
the data.

### 3. Compile

Search per source category -> fetch the primary source -> extract records.
Prefer primary tables/PDFs over summaries. For PDFs, download to `raw/` and parse
locally (`pdftotext -layout`, then regex/column logic); a bad fetch is often a
fetch artifact, not a bad file. Expect dead ends and thin routes — record them,
don't invent rows to fill them.

### 4. Structure + tag provenance

Map each record into the schema. For every field, decide its provenance and tag
it (next section). This is the discipline that keeps judgment from masquerading
as fact.

### 5. Verify — reconcile to control totals

The strongest QA available: if a source publishes an aggregate (a totals row, a
published count, subtotals per group), parse the rows and **check your sums tie
to it**. In the reference instance the 18 grant line-items reconciled to two
published subtotals, and 135 loan rows tied exactly (per group) to a totals-by-
part table — that's what makes those figures trustworthy. Where no control total
exists, cross-check individual rows against the source and mark the rest
`verified: false`. Never present an unverified figure as checked.

### 6. Insights pass

Compute what the data says (distributions, magnitudes, funnels, concentration)
and write it into `collection.md`. The compiled records usually reveal structure
the prose reference couldn't — capture it.

### 7. Record provenance

Fill `collection.md` (method, verification status, gaps) and `sources.yaml`
(every source + `last_fetched`). These are what let someone else re-run or trust
the compile.

## Provenance discipline (the load-bearing rule)

Every field in `schema.json` is tagged:

- `sourced` — read directly from a primary source (verifiable against a URL).
- `derived` — assigned by judgment, not stated in the source. Lower-trust; the
  main work remaining before promotion is turning these into rules.
- `derived-by-rule` — computed by an explicit, auditable lookup or rule (e.g. a
  `references/*.csv` map), not per-row judgment. Reproducible and correctable in
  one place. Promote `derived` fields to this whenever you can.
- `meta` — bookkeeping (ids, verified flag, free-text notes).

Keep `schema.json` (contract) separate from `data.csv` (values), keep
derived-by-rule inputs in `references/` so they're auditable, and treat
`sources.yaml` as the refresh mechanism.

## Where it sits & promotion

Compile is pre-review staging. It graduates into `dataset-review` when: scope is
locked, `derived` fields are computed by rule, gaps are filled from primary
sources, and provenance is complete. Review then creates the catalog entry and,
downstream, the pipeline into production. Don't put a compiled file in the
knowledge base (it's not prose reference) or the catalog (it's not a vetted
external dataset) — the compile lane is exactly the missing middle.

## Improving this skill

After a run, route lessons by the "how vs what" test:

- A fact about a *specific source* (a portal quirk, a PDF's column layout, where
  a figure really lives) -> the dataset's own `collection.md` / `sources.yaml`.
- General *"where records of type X live"* knowledge that any future compile
  would reuse -> `knowledge-base/` as a concise reference map, added
  deliberately, never auto-appended per run.

The method (this file + `references/`) stays generic. Most lessons aren't
reusable — don't pad it.
