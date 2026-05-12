# Framework Synthesis Rubric

How the synthesis stage should assemble a per-document `policy_summary`
from atoms extracted from a Chilean national framework document — the
NDC, the Estrategia Climática de Largo Plazo (ECLP), and the Ley Marco
de Cambio Climático (LMCC, Ley 21.455).

## Family characteristics

- `family`: `framework`
- `source_level`: `national`
- `region_code` and `communal_code` empty.
- Spanish source language.
- Strategic and legal in tone. Yields fewer atoms per page than sector
  plans — most pages carry framing, principles, and pathway language
  rather than discrete measures.
- Frameworks set commitments. They rarely commit to operational
  measures themselves.

## Signal volume targets

For a typical national framework (NDC, ECLP, LMCC), expect to produce:

- **sector** (sector / sector_priority): 5–12 signals
- **action**: 2–5 signals
- **target**: 10–20 signals
- **funding**: 1–3 signals
- **monitoring**: 3–6 signals
- **governance**: 4–10 signals
- **risk**: 2–5 signals
- **context**: 4–8 signals

**Total: 30–50** `policy_signals` — frameworks are dense on principles
and targets, lighter on operational actions. Aim upper half when the
extracted atoms support it.

## Mitigation emphasis

- NDC: `mixed` (mitigation and adaptation both, with explicit numerical
  mitigation commitments).
- ECLP: `mixed` (sector pathways for both; mitigation pathways are
  numerically denser).
- LMCC: `secondary` (the law establishes instruments for both, but
  mitigation is encoded through the instrument hierarchy rather than
  through specific commitments).

## Atom selection priority

Frameworks are sparse on the operational atoms (action, funding,
monitoring) and dense on context, sector_priority, and target atoms.
Selection caps:

| primitive_type | cap |
| --- | --- |
| target | 20 |
| sector_priority | 15 |
| context | 12 |
| governance | 10 |
| risk | 6 |
| action | 5 |
| funding | 3 |
| monitoring | 5 |

Prefer quantitative targets and explicit governance mandates over
strategic narrative.

## Policy summary assembly

### `priority_sectors`

Frameworks name many priority sectors as part of pathway language.
Take atoms with `primitive_type: sector_priority`; cap at 15. ECLP
will produce the most. NDC produces fewer but they are higher-level.
LMCC produces almost none (it does not declare priority sectors,
only the instrument hierarchy).

### `headline_targets`

This is the most important section for a framework. The headline
commitments — carbon neutrality year, emissions reduction percent,
sector budgets — go here. Cap at 20.

Always quantitative when possible: NDC and ECLP both quantify their
top-line commitments. Populate `raw_value_numeric` and `raw_unit`
for every entry that has a number in the source.

For the ECLP, sub-targets per sector pathway also belong in
`headline_targets`. Tag each with the appropriate `sector` so
alignment scoring can join.

### `named_actions`

Frameworks rarely commit to operational actions themselves. Limit
this array to atoms that genuinely state "the framework will do X"
rather than "the framework requires sector plans to do X". The
latter is a `governance` mandate, not a framework action.

### `governance`

For frameworks, `governance` is critical. The LMCC defines the
instrument hierarchy and the bodies (Comité Científico, Equipo
Técnico Interministerial, CCMA, CORECC). Capture them in
`supporting_bodies` with the lead body being the relevant
ministry or the cross-government coordinator (Ministerio del
Medio Ambiente for environmental coordination).

For the LMCC specifically, list every named instrument the law
creates (NDC, ECLP, sector plans, PARCC, PACCC, reportes) under
`supporting_bodies` as instruments rather than bodies if you want
to keep the audit trail clean — the synthesis prompt should
distinguish bodies and instruments by context.

### `funding`

Frameworks rarely identify funding. Populate sparingly. If the
framework names an aggregate national climate budget, capture it.

### `monitoring`

Capture the framework's review cycle (NDC quinquennial, ECLP
periodic). Indicators are usually delegated to sector plans, so this
section will be small.

### `risks_identified`

Frameworks identify climate risks at national level. Take risk
atoms; cap at 6.

### `coverage_notes`

Worth recording for frameworks:

- the framework's vintage and most recent update
- whether the framework's mitigation commitments have been
  incorporated by reference into operational instruments
- any sector pathways the framework names that are not yet covered
  by a sector plan in the corpus

## Common failure modes

- Synthesis treats ECLP pathway language as named actions. Pathway
  language is `sector_priority` or `target`. Operational actions
  live in sector plans, not in the ECLP.
- Synthesis duplicates the same headline target across NDC and ECLP
  summaries. Both restate it; both should record it as their own
  `headline_target` because they are independent documents.
- Synthesis under-credits the LMCC because it does not commit to
  operational actions. Don't try to fix this by inflating
  `named_actions`. The LMCC's value is in `governance` and the
  instrument hierarchy.
- Synthesis populates `funding` with aspirational language (the
  ECLP frequently mentions "necesidades de financiamiento" without
  identifying funding). Aspirational financing is `unknown` or
  `proposal_only`, not `identified`.

## Acceptance criteria

1. `headline_targets` is densely populated with quantitative entries
   (NDC and ECLP especially).
2. `governance` accurately reflects the framework's mandate and
   instrument hierarchy.
3. `named_actions` is short or empty (frameworks do not commit to
   operational measures themselves).
4. Restated targets across frameworks are not flagged as
   restatements at this stage — synthesis-stage cross-document
   linking happens later.
