# Climate policy: the general model

This is the country-agnostic backbone for the climate-policy topic. It fixes the grains, data moments, vocabulary, and gates that every country page in this folder instantiates, so the country pages can be read side by side and a tool built on one can generalise to another. The governing principle throughout: **the structure is universal; the country-specific labels are *values* inside these fields, not new structure.** Moving to another country adds values (an instrument name, a scale code, a territory scheme), not new concepts.

This page is about **what the data is**, not how it is processed. Extraction, decomposition, matching, and scoring methods change with tooling and context windows; the grains, vocabulary, and applicability logic below are the durable contract those methods build against. Read this page for the shared model; read a country page for how that country fills it in.

## Country pages in this folder

- `cl-climate-policy.md` — Chile: a unitary state whose framework law (LMCC) mandates a nested instrument cascade — the **inheritance** case.
- `br-climate-policy.md` — Brazil: a federation with autonomous states and municipalities and a sparse subnational climate layer — the **enumeration** case.

Each page follows the same section order, so the same question is found in the same place across countries.

## The two grains: document and signal

A policy dataset has two levels of record, and mixing them is the main source of confusion.

- **Document** — one row per instrument: its title, governance actor, territorial scale, type, status, and link. This grain answers *what exists and where to get it*.
- **Signal** — one row per policy statement read out of a document, tagged by what kind of statement it is. This grain answers *what the instrument actually says*.

A document is inert until decomposed into signals: "we have the plan" is not "the plan commits to X." The document grain is the manifest; the signal grain carries all the analytical weight. They relate by document id.

## The three data moments

One policy system produces data at three moments. Keep them separate.

1. **Inventory** — what documents *exist*: the catalogue of instruments that could bear on a city, one row per document. "What's out there, at what scale, by whom, where do I get it?"
2. **Signals** — what the documents *say*: the policy statements read out of each document. "What does this instrument commit to, target, fund, monitor?"
3. **Coverage** — which documents *apply* to a given city, and how strongly. "What is the policy environment *for this city*?"

Inventory and signals relate by document. Coverage relates the document set to a jurisdiction by the country's applicability rule (below), not by a shared key.

## Applicability: a country-provided strategy

Coverage — turning a document universe into a city-specific view — is the one place countries genuinely differ in *structure*, not just values. Two strategies seen so far:

- **Inheritance** (e.g. Chile). A framework law mandates an instrument at each scale, so a city's applicable set is a clean scale rule: national → all, regional → matching region, communal → the named commune. Coverage is derivable.
- **Enumeration** (e.g. Brazil). Federal autonomy means subnational instruments are voluntary and uneven; a city's set must be *looked up*, and the presence or absence of an instrument at each level is itself first-class data.

Two elements are needed regardless of strategy:

- **Status conditions weight, not just presence.** A draft or consultation document binds less than a final one; status is a first-class field.
- **Non-climate instruments can carry climate signal.** Master plans, sanitation, mobility, and disaster-risk instruments often hold binding climate-relevant commitments even where no climate plan exists. Both strategies need a standing category for these; enumeration countries need it heavily.

The applicability rule is therefore a value a country page supplies — the model fixes that coverage must be computable and status-weighted, not the specific rule.

## The signal vocabulary (the payload)

Every signal is a policy statement tagged by **what kind of statement it is**, from a closed set. This is the domain's shared language for "what a policy document can say," and it is stable across countries and across extraction methods:

- **action** — a named intervention or measure the instrument sets out to do.
- **target** — a quantified or dated goal.
- **funding** — a financing pathway or mechanism named for delivery.
- **monitoring** — an MRV, indicator, reporting, or verification commitment.
- **governance** — an assignment of responsibility, mandate, or legal duty.
- **sector_priority** — a stated sector priority without a specific action yet.
- **sector** — a sector scoping or classification statement.
- **risk** — an identified hazard, vulnerability, or climate risk.
- **context** — framing or background that sets up the above.

Two properties travel with every signal, because they govern how much it counts independent of any scoring formula:

- **explicitness** — *explicit* (the document says it) vs *inferred* (read between the lines).
- **commitment strength** — binding (commits / targets / funds) vs soft (prioritises / identifies / contextualises / restates).

And one discipline: **verbatim grounding** — every signal traces to an exact quote (with page/section), so a claim about what a policy says is always checkable against the policy. The principle is durable; the mechanism that enforces it is not fixed here.

## The inventory field contract

The durable field set for the document grain. Names are illustrative; the *fields* are the contract.

| Field | What it holds | Why it's load-bearing |
|---|---|---|
| `source_document_id` | stable id | join key to every signal |
| `source_name` | official title (original language) | identity |
| `source_url` | link / host | where to look (may be portal or placeholder) |
| `source_level` | scale (country's set) | drives applicability |
| `document_type` | instrument type (incl. non-climate carriers) | places it in the stack; expected implementation detail |
| `document_status` | final / draft / consultation / placeholder / … | conditions signal weight |
| `territory_code` | machine-readable scale + territory (country scheme) | the applicability join |
| `publisher` | governance actor | mandate/sector signal |
| `access_type` | how retrievable (pdf / portal / …) | whether it's a real artifact yet |

The five that do the structural work everywhere: **level · type · status · territory_code · publisher.**

## What makes a signal strong (the gates)

Whatever the scoring method, a (city, action) signal is stronger when more of these hold:

- **Locality** — from an instrument closer to the city.
- **Explicitness** — the document names the action, not merely implies it.
- **Commitment** — it commits/targets/funds rather than prioritises/contextualises.
- **Status** — final rather than draft/consultation.
- **Specificity** — carries a delivery actor, timeline, or funding pathway.

These change *value* by document and country, not *structure* — which is what lets a signal map generalise by swapping instrument names and scale codes, not concepts.

## Why this generalises

Because the model is fixed and only the values move, a tool built on one country re-points to another by swapping data, not code: the coverage view, the signal index, and any alignment score keep their logic in config and data. The two country pages so far prove the seam — Chile and Brazil share every grain, vocabulary term, and gate, and differ only in instrument names, scale codes, territory schemes, and the applicability strategy (inheritance vs enumeration). That portability is the reason to keep this general page separate from the country pages: it is the contract they agree to.

## See also

- Country pages: `cl-climate-policy.md`, `br-climate-policy.md` (this folder).
- Sibling topic and shape template: `../climate-finance/overview.md` and its country pages — this folder mirrors their structure (general model + country instantiations).
- Chile signals work in practice: `dataset-review/reviews/cl-ssg/cl-ssg-policy-documents/`.
- Repo-wide terms cross-listed in `../glossary.md`; house prose conventions in `../writing-style.md`.
