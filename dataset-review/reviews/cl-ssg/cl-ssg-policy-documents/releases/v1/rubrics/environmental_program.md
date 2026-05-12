# Environmental Program Synthesis Rubric

How the synthesis stage should assemble a per-document `policy_summary`
from atoms extracted from a Chilean Programa para la Recuperación
Ambiental y Social (PRAS).

PRAS are zone-specific environmental remediation programs for declared
zonas saturadas. They are action-rich and locally scoped. Many
commitments target environmental quality and health outcomes that
overlap with mitigation indirectly (industrial emission reductions,
energy efficiency, transport electrification in industrial zones).

## Family characteristics

- `family`: `environmental_program`
- `source_level`: usually `intercommunal` or `municipal`. Read from
  registry.
- Spanish source language.
- Mix of mitigation, adaptation, environmental quality, and health
  outcomes. `measure_type: transversal` is common.
- Frequently more advanced in execution than climate plans of similar
  vintage. `readiness_status: active_plan_measure` is more common
  than for PARCCs.

## Signal volume targets

For a typical PRAS (zona saturada / recuperación ambiental y social),
expect to produce:

- **sector** (sector / sector_priority): 3–6 signals
- **action**: 20–35 signals
- **target**: 5–10 signals
- **funding**: 5–10 signals
- **monitoring**: 8–15 signals
- **governance**: 4–8 signals
- **risk**: 3–6 signals
- **context**: 2–5 signals

**Total: 50–80** `policy_signals` when atoms support it — PRAS are
action-rich; aim for the **upper half** of the range.

## Mitigation emphasis

- `secondary` for most PRAS. Mitigation co-benefits are real but the
  document's lens is environmental quality.
- `mixed` if the PRAS explicitly frames specific compromisos as
  climate measures.
- `absent` if the PRAS yields zero mitigation-relevant compromisos
  after focus filtering. Set `coverage_notes` accordingly.

## Atom selection priority

Selection caps:

| primitive_type | cap |
| --- | --- |
| action | 25 |
| target | 10 |
| sector_priority | 8 |
| governance | 8 |
| monitoring | 10 |
| funding | 10 |
| risk | 6 |
| context | 5 |

Within each type, prefer:

1. atoms with `measure_type` in {`mitigation`, `transversal`}
2. atoms with `readiness_status: active_plan_measure`
3. quantitative over qualitative

## Policy summary assembly

### `priority_sectors`

PRAS organize compromisos under named ejes (aire, agua, suelo, salud,
social, productivo). Take atoms with `primitive_type: sector_priority`
whose sector is in the PRAS-extended vocabulary (`calidad_aire`,
`agua`, `suelo`, `salud`, `social_comunidad`, `industria`, plus the
climate sectors). Cap at 6.

### `headline_targets`

PRAS targets are often environmental quality thresholds (PM2.5
target, SO2 reduction). Capture them; cap at 10. Quantitative when
possible.

### `named_actions`

This is the densest section for PRAS. Take all atoms with
`primitive_type: action` and `measure_type` in {`mitigation`,
`transversal`}. Cap at 25.

For each entry, populate the action_statement, sector,
responsible_actor (usually a SEREMI, ministry, or service),
funding_status, and readiness_status. PRAS typically have an
identified funding source per compromiso — capture it.

### `governance`

Identify the Comité de Recuperación Ambiental (or zone-specific
equivalent) as `lead_body`. List the SEREMIs, municipalities, and
multi-stakeholder mesas in `supporting_bodies`. PRAS governance is
multi-actor by design.

### `funding`

PRAS frequently have a per-compromiso budget. Aggregate the named
funding lines and, if the document states a total program budget,
populate the total fields.

### `monitoring`

PRAS have a seguimiento platform (often a public dashboard) and
defined indicators per eje. Capture them.

### `risks_identified`

PRAS document the contamination risks that justified the zone's
declaration. Capture them; cap at 6. Even under mitigation focus,
risk context is useful for understanding why specific compromisos
exist.

### `coverage_notes`

Worth recording:

- which zone the PRAS covers (Quintero–Puchuncaví, Coronel, Huasco,
  Tocopilla)
- whether the PRAS spans multiple comunas
- the contamination types that drove the zone's declaration
- whether the program is in implementation, monitoring, or wind-down
  phase

## Common failure modes

- Synthesis forces every compromiso into mitigation. Many PRAS
  compromisos are environmental quality measures with transversal
  climate effects — `transversal` is the right `measure_type`.
- Synthesis loses zone-specific detail by populating
  `applicability_scope` generically. PRAS scope is the named zone;
  alignment scoring needs that specificity.
- Synthesis double-counts when an action carries both an
  environmental quality target and a co-benefit framing. Pick one
  primary framing per `named_actions` entry.
- Synthesis credits PRAS compromisos to national ministries when
  the actual implementer is the regional SEREMI. Take
  `responsible_actor` from the atom, not from the ministry the
  SEREMI reports to.

## Acceptance criteria

1. `mitigation_emphasis` reflects the actual mitigation co-benefit
   density of the PRAS.
2. `applicability_scope` names the specific zone, not just the
   region.
3. `named_actions` preserves the per-compromiso granularity needed
   for downstream alignment scoring.
4. `funding_status` is `identified` only where the PRAS names a
   specific channel.
