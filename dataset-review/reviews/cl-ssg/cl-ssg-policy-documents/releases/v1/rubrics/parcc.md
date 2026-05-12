# PARCC Synthesis Rubric

How the synthesis stage should assemble a per-document `policy_summary`
from atoms extracted from a Chilean Plan de Acción Regional de Cambio
Climático.

This rubric is consumed by `scripts/v1_synthesize.py`. The atom
extractor does not read this file; it stays family-agnostic.

## Family characteristics

- `family`: `parcc`
- `source_level`: `regional`
- `region_code` is populated from the registry; `communal_code` is
  empty unless the source document names a specific comuna.
- Spanish source language; `evidence_text` stays in Spanish.
- Adaptation-dominant. Most named measures are adaptation. Mitigation
  measures exist (transport electrification, public-building energy
  efficiency, waste/methane, urban tree cover) but are typically a
  minority of the document's content.
- Frequently restate national NDC and ECLP commitments. Treat
  restatements as context anchors, not as local commitments.

## Signal volume targets

For a typical PARCC, expect to produce:

- **sector** (sector / sector_priority): 4–8 signals
- **action**: 12–25 signals
- **target**: 5–10 signals
- **funding**: 3–6 signals
- **monitoring**: 5–10 signals
- **governance**: 2–5 signals
- **risk**: 5–12 signals
- **context**: 2–5 signals

**Total: 40–70** `policy_signals` for a full regional PARCC when atoms
support it — aim for the **upper half** of the range. Do not merge
distinct facts to stay under count; one substantive atom can justify
multiple signals when it carries separable claims (e.g. target vs
implementation pathway).

## Mitigation emphasis

For PARCCs, set `mitigation_emphasis` to:

- `secondary` when the PARCC includes named mitigation measures or
  sub-targets but the document is structured around adaptation.
- `mixed` when mitigation and adaptation framing are roughly balanced
  (rare for PARCCs but possible — e.g. region-with-large-port).
- `absent` when the document yields no mitigation atoms after focus
  filtering. Set `coverage_notes` accordingly.
- `primary` would not be expected for a PARCC and should be flagged
  in `coverage_notes` for review.

## Atom selection priority

When focus is `mitigation`:

1. Atoms with `measure_type` in {`mitigation`, `transversal`} take
   precedence.
2. Among those, prefer `evidence_kind: quantitative` first, then
   `qualitative`, then `categorical`.
3. Among those, prefer `explicitness: explicit` over `inferred`.
4. Among those, prefer atoms whose `_doc_type` is `parcc` (as opposed
   to atoms restating national framework material — those are
   useful as context but should not crowd out local commitments).

Atoms with `measure_type: adaptation` are still loaded but only
contribute to `risks_identified` and (when relevant)
`priority_sectors` rationale. They do not appear in `named_actions`
or `headline_targets` under mitigation focus.

## Policy summary assembly

### `priority_sectors`

Take all atoms with `primitive_type: sector_priority`. Cap at 8.
Prefer atoms whose sector is one of the climate-mitigation-relevant
sectors: `energia`, `transporte`, `infraestructura`,
`ciudades_asentamientos`, `residuos`, `bosques_silvicultura`,
`agricultura`, `industria`. Keep `multi_sector` if the document
explicitly names it.

For each entry, populate `rationale` with a one-sentence English
restatement of why the source names this sector as a priority.

### `headline_targets`

Take all atoms with `primitive_type: target` that have
`measure_type` in {`mitigation`, `transversal`}. Cap at 10. Prefer
quantitative atoms with parsed `raw_value_numeric` over text-only
targets.

For each entry, copy `target_value_text`, `raw_value_numeric`,
`raw_unit`, `timeline`, and `sector` directly from the atom. Set
`scope` to `"Región <name>"` (the regional applicability is implicit
for PARCCs; spell it out for downstream alignment).

### `named_actions`

Take atoms with `primitive_type: action` and `measure_type` in
{`mitigation`, `transversal`}. Cap at 25. Prefer atoms whose
`readiness_status` is `active_plan_measure` over `proposal` or
`conceptual`.

For each entry, populate `action_statement`, `sector`, `theme`,
`measure_type`, `responsible_actor`, `timeline`, `funding_status`,
`funding_source`, `monitoring_indicator`, `readiness_status`, and
`explicitness` directly from the atom or atoms supporting it. When
multiple atoms describe the same action (one carrying the verb, one
the actor, one the timeline), merge them into one `named_actions`
entry and reference all supporting `atom_id`s in
`evidence_anchors`.

### `governance`

Take atoms with `primitive_type: governance`. Identify the lead body
(usually CORECC or the equivalent regional climate committee) and
list supporting bodies. Cap supporting_bodies at 6.

### `funding`

Take atoms with `primitive_type: funding`. List named funding lines
(FNDR, sectorial transfers, GEF, international cooperation). If the
document names an aggregate budget for the PARCC as a whole,
populate `total_amount_text`, `raw_value_numeric`, `raw_unit`.

### `monitoring`

Take atoms with `primitive_type: monitoring`. List the indicators and
verification methods named at PARCC level (not per-action indicators
— those belong on the action entries). Populate `review_cycle` if the
document states one.

### `risks_identified`

Take atoms with `primitive_type: risk`. Cap at 12. Even under
mitigation focus, capture the named regional climate risks because
they explain why certain mitigation actions are framed as transversal
or co-beneficial. Each entry needs `risk_label` and the regional
scope.

### `evidence_anchors`

Every `atom_id` referenced anywhere in the summary appears once in
`evidence_anchors` with its `page_start`, `page_end`, and
`evidence_text`. The anchor list is the audit thread for the
summary.

### `coverage_notes`

Free text. Worth recording for PARCCs:

- whether the document is final, draft, or in consultation
- whether the PARCC explicitly restates NDC/ECLP and to what extent
- whether mitigation measures are concentrated in one sector or
  spread across many
- any region-specific framing that downstream alignment scoring
  should know (e.g. coastal region with adaptation-led framing
  may yield few mitigation actions, and that's expected)

## Common failure modes

- Synthesis treats restated national targets as PARCC commitments.
  Defense: when an atom's notes flag a restatement, treat it as
  context, not as a `headline_target`.
- Synthesis credits a PARCC for measures that are sector plan
  responsibilities (e.g. national rail electrification appearing in
  a regional PARCC). Defense: prefer atoms whose `responsible_actor`
  is a regional body (Gobierno Regional, SEREMI) over a national
  ministry.
- Synthesis collapses many small PARCC actions into a generic
  "regional measures" entry. Defense: keep `named_actions` granular
  even at the cost of repetition; alignment scoring needs the
  granularity.
- Synthesis produces empty `headline_targets` because the PARCC has
  none and is mostly text-framed adaptation. Defense: leave the
  array empty and note in `coverage_notes` that the PARCC is text-
  framed.

## Acceptance criteria

Before declaring a PARCC summary complete:

1. Every claim is anchored to an `atom_id` in `evidence_anchors`.
2. `mitigation_emphasis` matches the actual content (no "primary"
   PARCCs without strong evidence).
3. `named_actions` only contains mitigation or transversal-with-
   mitigation entries under mitigation focus.
4. `priority_sectors` does not duplicate entries from
   `named_actions`.
5. Numeric fields in `headline_targets` are populated when the
   underlying atom is quantitative.
