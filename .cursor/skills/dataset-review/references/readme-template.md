# Review README — house style

File: `dataset-review/reviews/<publisher>/<dataset>/README.md`. Sections in
order; omit a section only when truly empty. Live examples:
`reviews/ipcc/ipcc-ar6-spm7-mitigation-potentials/`,
`reviews/ipcc/ipcc-sr15-mitigation-feasibility/`,
`reviews/br-mcti/br-adaptabrasil/`.

**Formatting:** prose is never hard-wrapped — one line per paragraph/bullet, soft-wrap in the editor (older entries may still be hard-wrapped; don't copy that).

```markdown
# <Publisher> — <dataset name>

One-paragraph summary: what the data is, who assessed/produced it, which
version this entry covers and why that version.

## Canonical downloads
DOI/permalink list. Note alternates and what distinguishes them.

## Why we use it
Bulleted, each tied to a use case or need id. Name a complementary catalog
dataset only when the reader would actually source or join it alongside this
one (pairs with <sibling> for <axis>) — skip decorative "feeds X" mentions.

## License
The verified terms, citation requirements, redistribution status.

## Spatial and temporal scope
Geography and level; whether values are local truth or a global prior.
Time coverage, baseline, frozen-or-updated, what supersedes it.

## Interpretation warnings
What silently bites downstream use: non-additivity, uncertainty width,
stale assumptions, records that vanish under common operations, explicit
author exclusions translated into consequences for our use case.

## Parsing notes
What breaks naive ingestion: where real data starts/stops, working rows,
padding, header quirks, name hygiene, flag columns and their meaning.

## Current approved release
**<version>** (production approval is tracked in `catalog/index.yaml`).
```

Write warnings and parsing notes for the engineer and analyst who will
never read the methodology — those two sections are most of the README's
value. Keep claims tagged-by-construction: anything stated plainly here
must have been verified during the deep-dive.
