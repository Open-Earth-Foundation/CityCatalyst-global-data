# Territorial Plan Thin Synthesis Rubric

How the synthesis stage should assemble a per-document `policy_summary`
from atoms extracted from a Chilean territorial planning instrument
(Política Nacional de Desarrollo Urbano / Rural / Ordenamiento
Territorial, Estrategia Regional de Desarrollo, Plan Regional de
Ordenamiento Territorial, Plan Regulador, PLADECO, Plan Comunal de
Emergencia, Plan Comunal para la Reducción del Riesgo de Desastres).

These documents are mostly contextual for climate-action alignment.
They constrain or enable city action through land use, zoning, and
development strategy, but they rarely commit to climate measures
directly. The synthesis is deliberately thin.

## Family characteristics

- `family`: `territorial_plan`
- `source_level`: varies — national, regional, intercommunal,
  communal. Read from registry.
- Spanish source language.
- Most atoms will be `primitive_type: context` or `sector_priority`.
  `action` atoms exist mainly in PLADECOs and risk-reduction plans.

## Signal volume targets

Territorial instruments are **thin** for climate-specific signals:

- Prefer **sector**, **context**, and **risk** signals; fewer discrete
  **action** / **target** objects than PARCCs or sector plans.
- **Total: 8–20** `policy_signals` (hard cap mindset). Do not inflate
  count beyond what atoms substantiate.

## Mitigation emphasis

- `absent` is the expected value for most territorial plans.
- `secondary` only when the document explicitly commits to a
  mitigation-relevant measure (e.g. a PLADECO with a public-transport
  electrification commitment, or a zoning rule that mandates green
  infrastructure with measurable mitigation effect).
- `primary` is not expected and should be flagged in `coverage_notes`
  if it occurs.

If the document has zero atoms with `measure_type` in {`mitigation`,
`transversal`}, set `mitigation_emphasis: absent` and write a brief
`coverage_notes` explaining what the document does cover (zoning,
emergency response, regional development strategy, etc.). Empty
arrays are acceptable in this case.

## Atom selection priority

Cap total summary content at 15–20 entries combined across all
arrays. Prefer:

1. Atoms with `measure_type` in {`mitigation`, `transversal`}.
2. Atoms whose `_section` indicates climate-relevant content
   (sustainability, resilience, infraestructura verde, transporte,
   energía, riesgo climático).
3. Atoms with quantitative evidence over qualitative.

## Policy summary assembly

### `priority_sectors`

Take all atoms with `primitive_type: sector_priority` whose sector
bears on climate or risk. Cap at 6.

### `headline_targets`

Rare for territorial plans. Populate only if the document carries
explicit numerical commitments with mitigation relevance (e.g. "30%
de áreas verdes" with a known emissions co-benefit).

### `named_actions`

Cap at 5. Only mitigation or transversal-with-mitigation entries
under mitigation focus. Skip every non-climate operational measure.

### `governance`

Optional. Populate only when the document names a body specifically
responsible for the climate-relevant content.

### `funding`

Almost always empty for territorial plans. Populate only when a
specific funding line is named for a climate-relevant measure.

### `monitoring`

Almost always empty.

### `risks_identified`

Plan Comunal de Emergencia and Plan Comunal para la Reducción del
Riesgo de Desastres can produce useful risk atoms even under
mitigation focus. Cap at 6.

### `coverage_notes`

Always populate. Worth recording:

- what kind of territorial instrument this is (zoning, development,
  emergency, risk reduction)
- why mitigation content is sparse or absent in this document
- any non-climate signal that downstream alignment scoring should
  know about (e.g. a zoning rule that constrains where
  electrification infrastructure can be sited)

## Common failure modes

- Synthesis pads `named_actions` with non-climate zoning rules to
  avoid an empty array. Do not pad. An empty array with
  `mitigation_emphasis: absent` is correct for most of these
  documents.
- Synthesis treats land-use rules as actions. Zoning rules are
  context unless the document explicitly commits to a measure with
  a target.
- Synthesis populates territorial codes inconsistently. Take
  `region_code` and `communal_code` from the registry.

## Acceptance criteria

1. Total entries across all arrays is at most 20.
2. `mitigation_emphasis` is correctly `absent` for most entries.
3. `coverage_notes` is populated and explains the document's role
   even when most arrays are empty.
4. No padding of `named_actions` with non-climate content.
