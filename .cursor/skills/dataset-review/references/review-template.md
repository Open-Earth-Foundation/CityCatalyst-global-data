# review.md — the release's epistemic contract

**Formatting:** prose is never hard-wrapped — one line per paragraph/bullet, soft-wrap in the editor (older entries may still be hard-wrapped; don't copy that). Follow the house writing style in `knowledge-base/topics/writing-style.md`: lead each section with plain-language prose, reserve bullets for genuine lists, keep paths out of prose and collect them in a References block at the end of the section.

One per release, in the release folder: what this release's data **can and
cannot support**. Written for the analyst who will quote the data without
reading the methodology. Worked example:
`reviews/ipcc/ipcc-ar6-spm7-mitigation-potentials/releases/2023/review.md`.

Claims change between releases (coverage, adjudications), which is why this
is release-level; dataset-level facts (license, provenance, parsing) stay in
the review README one level up. Don't duplicate between the two.

## Sections

```markdown
# Review — <dataset>, release <version>

## Scope and status
What artifacts this release contains, which notebooks produced them,
research vs production-approved.

## Visual summary
A short prose digest of what the notebook's charts show — the shape of the
data in a few sentences, with a pointer to run the notebook for the rendered
charts. Charts are not saved as image files or embedded here; the precise
numbers belong in tables in the sections below. Optional when there are no
meaningful aggregates; recommended for awards/outcomes datasets.

## What this data supports
Open with a sentence or two naming what the claims are mostly about and where
the load-bearing caveat sits, then give the claims. Each claim is a literal
sentence someone could lift into a report; a claim with a condition is prose
(the condition keeps it honest), not a packed bullet. This is the heart of
the document.

## What this data does not support
Open with a line on the overclaim pattern to watch for, then the anti-claims.
Each anti-claim is a prose sentence with its one-line why; write the
overclaims you can already see coming. Reasoning goes in prose, not bullets.

## Using it downstream
Translation rules: tiers vs ranks, which sibling datasets to pair with,
artifacts to handle explicitly.

## Benchmark values a city can use
REQUIRED for awards/outcomes datasets (anything recording funded projects,
adjudications, or executed investments); optional elsewhere. State which
concrete values a city could reuse to **understand, replicate, generalise,
or take learnings from** what got funded — typical award/cost size, unit
rates (e.g. per ha, per unit), co-finance share, delivery channel, timing
lags, and where the route is proven. Give real figures (median + range) from
this release, grouped by the use ("to understand / to replicate / to
generalise"). Label them comparator priors, not guarantees, and carry the
unit and granularity caveat (e.g. region-level, one cycle, UTM not CLP).

## Notes on non-obvious fields
ONLY fields someone could plausibly misread by looking at the data
(flags, sentinel semantics, intentional many-to-many). Never a full
data dictionary — people can open the csv; explaining `sector` adds
text, not information.

## Traceability
Source DOIs, local-only input dependencies, adjudication record.
```

Phrase claims and anti-claims as concrete example sentences, not abstract
principles — overclaiming happens in sentences, so the defense should be
sentence-shaped.
