---
name: dataset-review
description: >
  Deep-dive review of a dataset for CityCatalyst: verify access and license,
  profile the actual data, read the methodology, run the fit-for-purpose
  check, and draft the review entry in dataset-review/reviews/. Use whenever
  the user wants to review, assess, vet, or "go deeper into" a dataset;
  promote a discovery candidate; check whether a dataset is fit for purpose;
  or create/update an entry under dataset-review/ — even if they just say
  "let's look at this dataset properly". Follows dataset-discovery in the
  pipeline: discover → review → pipeline.
---

# Dataset Review (deep-dive)

Take a dataset — usually a `promote` candidate from `dataset-discovery/` —
and turn claims into verified findings: what's actually in the data, what
the methodology means for our use, what the license really says, and whether
it's fit for purpose. Output is a review entry in
`dataset-review/reviews/<publisher>/<dataset>/` in the house style.

The work is exploratory; the deliverable is not. Don't script the path —
contract the destination: by the end, every question in
`references/deep-dive-checklist.md` has an answer tagged **verified**,
**inferred**, or **unanswered**. Never present an inferred or skimmed answer
as verified — confident summaries of unread docs are this skill's main
failure mode, and the tags are the defense.

## Checkpoints — work in increments

Run as a sequence of steps, **stopping after each one to present findings
and let the user decide to continue**. The human owns judgment calls (fit
verdict, what goes in warnings, promotion); the skill owns legwork (fetching,
profiling, cross-checking). If the user explicitly asks for an end-to-end
run, do all steps but still present per-step findings in the final report.

### Step 1 — Provenance, access, license

Fetch the authoritative metadata record (publisher page, DOI record, data
catalog entry), not blogs about it. Establish: canonical download(s) and
versions, license **as stated in actual terms** (a landing-page "open" claim
is inferred, not verified), citation requirements, update cadence or frozen
status. If multiple published versions exist, identify which is canonical
for us and why.

Files often can't be fetched directly from this environment — asking the
user to download and drop the file in is a normal step, not a failure.

### Step 2 — Profile the data

Open the real file. Establish structure (sheets/tables/layers), actual
columns and units, the real row count vs claimed coverage, and — most
valuable — the **quirks a pipeline would trip on**: working-notes rows,
phantom padding, trailing spaces, inline section headers, truncated labels,
sentinel values, files that are exports of office tools rather than data
products. Use the data plugin's explore/profile skills where available.
Every quirk found here is a parsing note in the README.

### Step 3 — Methodology

Read the methodology documentation (figure captions, methods sections,
technical annexes — primary sources). Establish: what the values actually
measure, against what baseline, with what uncertainty, and what the authors
explicitly exclude or warn about. Translate each into a concrete
implication for *our* use case — "non-additive" matters differently for
ranking than for inventory. Author-stated caveats are gold: collect them.

### Step 4 — Fit-for-purpose check

Score against the originating need's `search.yaml` (or elicit criteria if
the review wasn't triggered by a discovery need): each must-have,
constraint, and the screening guidance, each marked pass/fail/conditional
with evidence. By now this should be nearly mechanical — if it requires
fresh research, steps 1–3 missed something.

Also check the catalog for *sibling datasets by theme* — complements and
overlaps (e.g. a feasibility dataset pairing with a potentials dataset).
Search index.yaml by theme keywords, not just by the publisher you expect;
adjacent datasets under other publishers are easy to miss.

### Step 5 — Write the review entry

Create `reviews/<publisher>/<dataset>/README.md` (house style and section
guide in `references/readme-template.md`; good live examples:
`reviews/ipcc/ipcc-ar6-spm7-mitigation-potentials/`,
`reviews/ipcc/ipcc-sr15-mitigation-feasibility/`) and place files in
`releases/<version>/`. Version naming: the publisher's version or release
year/date — match the publisher's own framing.

File placement convention inside a release: `data/` is committed to git and
holds only what helps someone understand the dataset later (cleaned outputs,
mappings, and the canonical raw when genuinely small — single-digit MB);
`sample/` is gitignored (see repo .gitignore) and holds large files and
working outputs. Large raws go in `sample/` with re-download instructions
(URL/DOI + retrieval steps) in the README so the notebook can be re-run
from a fresh clone. Notebooks sit at the release root.

The README's most valuable sections are **interpretation warnings** (what
silently bites downstream use) and **parsing notes** (what breaks naive
ingestion) — write both for the engineer and analyst who will never read
the methodology themselves.

### Phase B — Extraction notebook (after the README exists)

Turn the README's parsing notes into working, validated code. Method and
block-by-block skeleton in `references/notebook-template.md`. The core
discipline: **parsing notes ↔ cleaning blocks stay 1:1** — if cleaning needs
a step the README doesn't mention, add the parsing note first; if the
notebook discovers a new data fact (e.g. source-side rounding residues),
it flows back into the README. Fit analysis is limited to the questions the
need raises — that limit is what keeps notebooks from sprawling.

### Phase C — Mapping (when the need requires a taxonomy/schema link)

Produce a crosswalk csv in the release `data/` linking the dataset's units
to the target taxonomy (TEF, GPC, locodes), in the house mapping schema.
Method in `references/mapping-method.md`. Core principles: **link, don't
attribute** (values stay at source granularity — never split a quantity
across mapped targets); keep unmapped entries with `mapping_confidence:
none` and a rationale; agent drafts with confidence tags, **human
adjudicates the mediums and lows**; record the adjudication date and
adjudicator in the notebook findings.

### Phase D — review.md (close out the release)

Write the release's epistemic contract: what the data can and cannot
support, as literal claim/anti-claim sentences with conditions. Template in
`references/review-template.md`. This is the document downstream analysts
read instead of the methodology — most of its content falls out of phases
A–C (author caveats → anti-claims, fit analysis → claim conditions, mapping
coverage → downstream rules), so write it last, when those are known.
It is then a living document within the release: whenever a new artifact
(another mapping, a new analysis cell) changes what the data can support,
update review.md in the same change.

Phase split criterion (for future maintainers): a phase becomes its own
skill only when it's routinely run without the others AND its reference
file outgrows this skill. Until then, one skill keeps the README ↔ notebook
↔ mapping ↔ review.md loop in one place.

### Step 6 — Promotion mechanics (on user approval)

Add/update the `catalog/index.yaml` entry; if the review came from a
discovery need, collapse the candidate to a `promoted` stub and update the
need's outcome. Never delete old release folders — new releases sit
alongside old ones; `production_approved` in the catalog decides what's
active.

## Hard rules

- Evidence tags are mandatory: verified / inferred / unanswered. License
  and methodology claims must be verified from primary sources before the
  README states them plainly.
- `dataset-review/` follows publisher/dataset/version structure strictly.
  Keep markdown minimal: per review folder, the only markdown is `README.md`
  and the release `review.md` — plus, where a review acts as the hub for a
  cross-cutting working methodology, a single `methodology.md` at that
  review's root. No other ad-hoc markdown. Working/WIP methodology lives in
  that `methodology.md` (clearly marked working), NOT in
  `knowledge-base/topics/`, which is reserved for landed reference; promote a
  consolidated version to topics only once the method stabilises.
- The review records what the data *is*, including flaws — fit problems go
  in warnings, not silently dropped. A negative review (not fit) is a valid
  outcome; record it rather than abandoning the entry.
- Markdown formatting: do NOT hard-wrap prose at a fixed column width. Write each paragraph and each bullet as a single long line and let the editor soft-wrap. (This bullet is one line — follow its example. Code blocks and tables keep their natural structure; existing wrapped files can be left alone or unwrapped when touched.)
