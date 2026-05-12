# Sector Plan Synthesis Rubric

How the synthesis stage should assemble a per-document `policy_summary`
from atoms extracted from a Chilean national sector mitigation plan
(Plan de Mitigación Sector — energía, agricultura, ciudades,
infraestructura, salud, transporte, minería).

## Family characteristics

- `family`: `sector_plan`
- `source_level`: `national`
- `region_code` and `communal_code` are empty.
- Spanish source language.
- Mitigation-dominant by design (these are the operational mitigation
  instruments under the LMCC framework). Most named measures are
  `measure_type: mitigation`.
- Single-sector focus. The sector is fixed by the document via this
  mapping:

| `source_document_id` | locked `sector` |
| --- | --- |
| `chl_energia_sector_plan` | `energia` |
| `chl_agricultura_sector_plan` | `agricultura` |
| `chl_ciudades_sector_plan_2025` | `ciudades_asentamientos` |
| `chl_infraestructura_sector_plan_2025` | `infraestructura` |
| `chl_salud_sector_plan_2024` | `salud` |
| `chl_transporte_sector_plan_2025` | `transporte` |
| `chl_mineria_sector_plan` | `mineria` |

The Salud sector plan is adaptation-leaning despite the family name.
For Salud, set `mitigation_emphasis: secondary` or `absent` and
expect most measures to carry `measure_type: adaptation` or
`transversal`.

## Signal volume targets

For a typical national sector mitigation plan, expect to produce:

- **sector** (sector / sector_priority): 1–3 signals (sector is locked by document)
- **action**: 25–40 signals
- **target**: 10–20 signals
- **funding**: 5–10 signals
- **monitoring**: 10–20 signals
- **governance**: 4–8 signals
- **risk**: 1–4 signals
- **context**: 2–5 signals

**Total: 60–100** `policy_signals` when atoms support it — aim for the
**upper half**. Prefer one signal per measurable commitment or named
measure; split targets and actions when they are distinct evidence units.

## Mitigation emphasis

For sector plans, set `mitigation_emphasis` to:

- `primary` for the six mitigation-led plans (Energia, Agricultura,
  Ciudades, Infraestructura, Transporte, Mineria).
- `secondary` for Salud.
- `mixed` if the document clearly straddles (rare).

## Atom selection priority

Sector plans are dense and structured. Selection caps:

| primitive_type | cap |
| --- | --- |
| target | 25 |
| action | 40 |
| funding | 20 |
| monitoring | 20 |
| governance | 15 |
| sector_priority | 10 |
| risk | 10 |
| context | 8 |

Within each type, prefer:

1. `evidence_kind: quantitative` over qualitative
2. atoms with `raw_value_numeric` populated
3. `readiness_status: active_plan_measure` over `proposal`
4. `explicitness: explicit` over `inferred`

## Policy summary assembly

### `priority_sectors`

Sector plans usually do not declare priority sectors — the document
is the sector's plan. Populate this array only if the plan names
internal sub-sectors as priority axes (e.g. Transporte sector plan
naming public transport, freight, and aviation as separate axes).

### `headline_targets`

Sector plans carry the densest `target` content. Take all
quantitative target atoms; cap at 25. Always populate
`raw_value_numeric` and `raw_unit` for quantitative entries. Set
`sector` to the document's locked sector. Set `scope` to `"Chile"`.

If the plan's headline target is a single sector-wide emissions
reduction figure (e.g. "X MtCO2e al 2030"), that target should be
the first entry.

### `named_actions`

Sector plans present each measure as a named card. Take atoms with
`primitive_type: action`. Cap at 40. Each `named_actions` entry
should reflect one source measure card; merge atoms describing the
same measure (action + target + actor + timeline + monitoring) into
one entry referencing all supporting atom_ids.

Do not split one card into multiple `named_actions` entries unless
the card describes genuinely distinct interventions.

`responsible_actor` is usually the lead ministry (Ministerio de
Energía, Ministerio de Agricultura, etc.) or a specific service
(SUBTRANS, MOP, CONAF). Populate from the atom.

### `governance`

Identify the lead ministry as `lead_body`. Inter-ministerial
committees, working groups, and the Comité Asesor go in
`supporting_bodies`. Most sector plans cite the LMCC's governance
hierarchy — capture it concisely; do not enumerate every reference.

### `funding`

Take all funding atoms. Sector plans frequently name multiple
financing channels (presupuesto sectorial, transferencias, fondos
internacionales). List them in `named_funding_lines`. If the plan
names an aggregate budget, populate the total fields.

### `monitoring`

Sector plans typically have a plan-level MRV section. Take its
indicators and verification methods. Populate `review_cycle` from
the atom (usually annual or biennial reporting cycles).

### `risks_identified`

Most sector plans have a brief sector-context section that names
sector-specific climate risks. Capture them; cap at 8.

### `coverage_notes`

For sector plans, worth recording:

- whether the plan is the first, second, or update of an earlier
  sector plan
- whether the plan covers the full sector or only specific
  sub-sectors
- whether targets are stated as absolute (MtCO2e) or relative (%)
- whether the plan articulates a clear linkage to the ECLP
  pathway for the sector

## Common failure modes

- Synthesis lifts ECLP pathway language into `named_actions`. Sector
  plans often cite ECLP pathways as context. Restated pathway
  language belongs in `coverage_notes` or a `context`-derived
  observation, not in `named_actions`.
- Synthesis treats Salud measures as mitigation when they are
  adaptation. Trust the atom's `measure_type` field; do not force
  Salud measures into mitigation just because the family is "sector
  plan".
- Synthesis loses individual measure granularity by summarizing a
  set of related measures into one entry. Alignment scoring needs
  the named, per-measure granularity preserved.
- Synthesis populates `region_code` because a measure mentions a
  region in passing. Sector plans are national; leave
  `region_code` and `communal_code` empty on the summary.

## Acceptance criteria

1. `mitigation_emphasis` matches the document and the atom mix.
2. Every quantitative target in `headline_targets` has
   `raw_value_numeric` and `raw_unit`.
3. `named_actions` contains the major numbered measures from the
   plan; small support tasks should not crowd them out.
4. The locked sector is consistent across `priority_sectors`,
   `headline_targets`, and `named_actions`.
