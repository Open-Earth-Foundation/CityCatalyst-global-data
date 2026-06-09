---
name: dataset-discovery
description: >
  Find and triage candidate datasets for CityCatalyst data needs. Use whenever
  the user wants to find, source, scout, or search for data; mentions a data
  gap; asks what data exists for a sector, theme, or geography; or wants to
  open, update, or resolve a data need — even if they never say "search" or
  "discovery". Also use when deciding whether a dataset someone suggested is
  worth a full review. Produces a need folder in dataset-discovery/needs/
  containing need.md, search.yaml, and candidates.yaml.
---

# Dataset Discovery

Turn a vague data need into a structured search, hunt for candidate datasets,
screen them against explicit criteria, and record the results so the team
never re-searches the same ground. This skill owns everything *before* a
dataset is confident enough to enter `dataset-review/` — it writes only to
`dataset-discovery/`, never to the catalog or reviews.

The pipeline this feeds: **discover → review → pipeline**. The framing that
keeps the two folders distinct: dataset-review is organized by the *answer*
(datasets, versioned); dataset-discovery is organized by the *question*
(needs, dated). Promotion out of discovery means a human or the
dataset-review process creates the `catalog/index.yaml` entry and `reviews/`
folder; this skill's job ends at a well-evidenced recommendation.

## Output contract

One folder per need: `dataset-discovery/needs/<YYYY-MM-slug>/` containing
exactly three files (formats in `references/templates.md`):

Prose in these files is never hard-wrapped — one line per paragraph/bullet, soft-wrap in the editor.

- `need.md` — intent and lifecycle: who asked, why, status
  (`open | resolved | gap_confirmed | superseded`), open questions, outcome.
- `search.yaml` — every machine-checkable criterion: geography, must-haves,
  graded constraints, taxonomy to map to. This parameterizes screening.
- `candidates.yaml` — the search output: candidates with verdicts and evidence.

Field-ownership rule (prevents drift): anything a screening check could read
lives in search.yaml and nowhere else; need.md holds the human why, never the
criteria. No other files go in a need folder — samples, screenshots, and
scratch from the hunt stay out of git entirely. Re-runs of a search append to
or date-suffix candidates files; they never spawn new structure.

## Workflow

### 1. Elicit the need

Don't search on a vague ask. The questions that most change where you'd
search, in rough order of leverage: what the data will be *used for* (the use
case sets the quality bar — e.g. ordinal ranking tolerates wide uncertainty
that inventory work cannot), geography and the minimum admin level below
which a dataset fails, which taxonomy or schema results must map to,
must-have vs nice-to-have variables, and license/access constraints.

Write the answers into need.md (intent) and search.yaml (criteria). Most
fields are optional — a five-line search.yaml that exists beats a thorough
one the user abandons. Mark unknowns explicitly and move on, but ask before
assuming on the two answers that routinely reverse the search target: the
use case, and whether a constraint is a hard filter or a preference.

Constraints are *graded* (preferred / acceptable / disqualifying), not
binary. When the catalog has nothing for a domain (greenfield), loosen them —
reviewing a commercial source to map the landscape is legitimate.

### 2. Check our own records first

Before any web search, check `dataset-review/catalog/index.yaml`, prior need
folders in `dataset-discovery/needs/`, and `knowledge-base/topics/data-sources/`
for the same theme or geography. Past finds, rejected candidates (with
reasons), and confirmed gaps are the most specific knowledge we have — this
step regularly answers part of the need outright and prevents re-investigating
dead ends.

### 3. Search

Read the relevant playbook in `knowledge-base/topics/data-sources/` for the
need's domain (pick by theme; if none exists, note that, rely on general
search, and seed a playbook from what the run teaches). Useful general
pattern: official/multilateral sources first (consistent methodology, clear
licensing), then NGO/research compendia, then national sources for
geographic context.

Expect dead ends. "Promising but needs manual portal digging" and "publisher
must be contacted" are legitimate outcomes — record them as open questions or
`investigate` verdicts rather than guessing or overstating access.

### 4. Screen

Apply `references/screening-criteria.md`, parameterized by search.yaml — the
must-haves and graded constraints *are* the kill-list for this run. Cheap
disqualifiers first (license, admin level, scope); expensive checks
(methodology consistency, mapping cost) only on survivors.

### 5. Record

Write candidates.yaml (verdicts: `promote | investigate | deprioritize |
reject`). Every candidate carries evidence links and screening notes
explaining the verdict — the notes are what stop a future searcher repeating
your work, so write them for that reader. Never delete a rejected candidate;
keep it with a one-line reason and date.

Update need.md: list promote/investigate ids under `outcome`, and fold
anything the search taught back into the open questions (searches routinely
surface decisions the elicitation missed — route them to the user, don't
bury them). If nothing adequate exists, set status to `gap_confirmed` with
notes — a confirmed gap is a valuable result, not a failure, and gap_confirmed
needs are the watch-list for any future horizon scanning.

### 6. Verify before reporting

Spot-check each candidate's central claims — does the access method, license,
and metric actually match what the publisher states? Verify by fetching the
source where feasible; where not, mark the claim unverified in the candidate
entry. Never present an unverified claim as checked.

## Improving this skill

After each run, ask: did this teach a *reusable* lesson? Route it by the
"how vs what" test, and resist creating files:

- A fact about a *specific dataset/publisher* (a portal quirk, a hidden
  sheet, a licensing term, where a figure's data really lives) → the
  **dataset's own docs** in `dataset-review/` (its README parsing/provenance
  notes), not the knowledge base. The lesson rides with the dataset it's about.
- General *"how something works"* knowledge that holds independent of any one
  dataset and that multiple tasks would reference → `knowledge-base/topics/`
  — but keep it a concise, high-level reference, added deliberately during a
  consolidation pass, never auto-appended per run. `knowledge-base/` is not a
  dumping ground for per-dataset findings.

Most lessons aren't reusable — don't pad anything. Method (this skill +
references) stays generic.
