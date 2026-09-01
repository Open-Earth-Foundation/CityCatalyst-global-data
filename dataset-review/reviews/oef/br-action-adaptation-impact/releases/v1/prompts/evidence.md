# Component evidence

Prompt version: `1.2.0`

Review the supplied candidate PDF pages for evidence about one action, sector, risk
and component. The action has already received direct indicator claims. Eligibility
is fixed in this stage: evidence cannot create or broaden an eligible link.

Use only the supplied page text. Do not use outside knowledge, invent a quotation or
combine words from separate passages.

## Evidence rule

Record a passage only when it says something substantive about the action mechanism's
effect on at least one supplied direct indicator **in the named sector-risk context**.

The quote must establish all three of the following:

1. the relevant action mechanism or a clear operational equivalent;
2. an effect on the exact indicator, or on an unambiguous operational equivalent; and
3. relevance to the named sector and risk.

The sector or risk name does not have to appear verbatim when the passage's subject
makes the context unambiguous. For example, a passage about preventing electricity
outages can support an energy-security access indicator. A general passage about
relocation cannot support an energy-security exposure indicator unless it also
connects relocation to energy access, energy users or energy assets.

- `supports`: the passage supports the expected effect.
- `qualifies`: the passage supports the effect only under stated conditions, or only for
  part of the action.
- `contradicts`: the passage describes failure, harm, rebound or an effect opposing the
  expected mechanism.

Use `whole_action` only when the passage addresses the action's central mechanism.
Otherwise use `partial_action`.

## Effectiveness signal

For every retained evidence passage, assign one `outcome_signal`. This is an input to
the runner's deterministic component-level effectiveness rule; it is not a separate
indicator-level effectiveness assessment.

- `strong_or_quantified`: the passage reports a strong positive outcome or quantifies
  the relevant positive outcome. A number is relevant only when it measures the effect
  on the supplied indicator or an unambiguous operational equivalent.
- `moderate_or_conditional`: the passage reports a moderate positive outcome, or says
  the outcome depends on stated conditions or context.
- `explicitly_limited`: the passage explicitly describes the positive outcome as small,
  weak, minor or otherwise limited.
- `strength_not_demonstrated`: the passage supports the direction of effect, but does
  not demonstrate whether the outcome is strong, moderate or explicitly limited.
- `not_applicable`: use only for `contradicts` evidence, where no positive effectiveness
  level applies.

The final component output uses only:

- `High effectiveness` when the mechanism and indicator relationship are direct and
  the retained evidence demonstrates a strong or relevant quantified outcome;
- `Medium effectiveness` when the mechanism and indicator relationship are direct and
  the retained evidence demonstrates a moderate, conditional or context-dependent
  outcome;
- `Low effectiveness` when the mechanism and indicator relationship are direct and the
  retained evidence explicitly demonstrates a limited outcome;
- `No demonstrated effectiveness` when no relevant positive evidence demonstrates one
  of the three levels above.

Do not interpret scientific confidence, evidence certainty or agreement as outcome
strength. For example, “high confidence” does not by itself mean High effectiveness.
Do not use Low effectiveness for uncertainty, missing quantification, partial document
coverage or absence of evidence. Use `strength_not_demonstrated` instead.

A broad mention of climate risk, resilience, a hazard, the action type, or the
indicator outside the named sector-risk context is not enough. Do not treat
recommendations, definitions or descriptions of need as demonstrated effectiveness
unless they explicitly state the relevant effect.

Every quotation must be verbatim and come from one supplied source and physical PDF
page. Link it only to direct indicators that the passage actually addresses.

Return one screening result for every supplied source, including sources where no
relevant evidence was found. Do not assign the final component effectiveness category;
the runner derives it from the validated evidence and `outcome_signal` values. Follow
the supplied JSON schema exactly.
