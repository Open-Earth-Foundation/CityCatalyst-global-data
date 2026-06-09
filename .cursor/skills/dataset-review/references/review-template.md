# review.md — the release's epistemic contract

**Formatting:** prose is never hard-wrapped — one line per paragraph/bullet, soft-wrap in the editor (older entries may still be hard-wrapped; don't copy that).

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

## What this data supports
Claim TEMPLATES with validity conditions — literal sentences someone could
lift into a report, each with the condition that keeps it honest.
This is the heart of the document.

## What this data does not support
Anti-claims, each with a one-line why. Write the overclaims you can
already see coming.

## Using it downstream
Translation rules: tiers vs ranks, which sibling datasets to pair with,
artifacts to handle explicitly.

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
