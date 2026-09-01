# Indicator eligibility

Prompt version: `1.0.0`

Assess whether an action is linked to each supplied terminal risk indicator. This stage
uses only the action definition and risk framework. Do not use evidence documents and
do not assess effectiveness.

## Reasoning order

1. Interpret the action as a whole and identify its primary implementation mechanism.
2. Identify the condition, system, resource, population, user or activity changed by
   that mechanism.
3. Compare that change with each indicator, keeping vulnerability and exposure
   separate.
4. Assign exactly one link claim to every supplied indicator.

Do not begin with shared words between the action and indicator names.

## Link claims

- `direct`: the primary mechanism directly changes the exact condition measured by the
  indicator, without an unsupported intermediate assumption. This is the only eligible
  relationship.
- `indirect`: the indicator could change later through a secondary effect, co-benefit or
  another intervention. This is recorded but is not eligible.
- `no_link`: the action has no credible relationship to the indicator.
- `unclear`: the supplied action definition or indicator meaning is insufficient to
  distinguish direct from indirect. Human review is required.

Sector terminology, a shared hazard, general resilience language or evidence that an
intervention can work does not make a link direct. A sector mechanism must be central
to the action or explicitly implemented by it.

Planning, monitoring, research, awareness, coordination, governance or finance is
direct only when the indicator measures that same function. It is indirect when the
indicator measures a later physical or social outcome.

For exposure, `direct` requires a direct change to the exact exposed population, asset,
area, activity or user quantity. Explicit relocation or resettlement can directly change
an exposed-population indicator. General protection or resilience does not by itself
change exposure.

Return a concise rationale for `direct`, `indirect` and `unclear`. The rationale for
`no_link` must be an empty string. Do not use speculative wording to justify a direct
claim. Follow the supplied JSON schema exactly.
