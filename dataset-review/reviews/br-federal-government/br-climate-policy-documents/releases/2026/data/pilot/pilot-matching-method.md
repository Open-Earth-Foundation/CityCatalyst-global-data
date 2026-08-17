# Seven-action matching pilot

## Purpose

Test whether extracted policy records provide defensible evidence about seven varied adaptation actions. The score measures **policy alignment**, not implementation, funding certainty, or effectiveness.

## Pilot actions

| Action | Why selected |
|---|---|
| `ipcc_0096` Climate resilience in farming and fisheries | Tests direct targets, finance, and sector practices across farming and aquaculture. |
| `ipcc_0091` Livelihood diversification | Tests a partial match where income and productive-inclusion measures do not fully match fisheries-specific diversification. |
| `icare_0145` Healthcare system resilience | Tests direct system, infrastructure, workforce, and continuity-of-care evidence for extreme events. |
| `c40_0051` Public shading | Tests a legitimate no-match result. |
| `ipcc_0099` Water capture and storage | Tests quantified technology deployment and implementation commitments. |
| `ipcc_0100` Efficient water use and demand | Tests cross-sector irrigation, reuse, aquaculture, and industrial-demand measures. |
| `c40_0056` Watershed protection and management | Tests restoration, source protection, governance, and implementation evidence. |

## Evidence decisions

Each accepted pair receives:

- `relationship`: `commits`, `targets`, `funds`, `governs`, `monitors`, `prioritizes`, `identifies`, `contextualizes`, `references`, or `restates`;
- `match_relevance`: `high`, `medium`, or `low`;
- `explicitness`: whether the policy-to-action connection is direct or inferred;
- `match_confidence`: confidence in the evidence classification;
- a concise English rationale.

No evidence row is created when there is no meaningful match. Portuguese remains the authoritative quotation; English supports review.

## Scoring

Each evidence row receives:

`relation weight × explicitness weight × confidence weight`

| Dimension | Weights |
|---|---|
| Relationship | commits `1.00`; targets/funds `0.85`; governs/monitors `0.65`; prioritizes `0.55`; identifies `0.35`; contextualizes/references `0.20`; restates `0.10` |
| Explicitness | explicit `1.00`; inferred `0.60` |
| Confidence | high `1.00`; medium `0.65`; low `0.35` |

Evidence is aggregated with `100 × (1 − exp(−sum / 2))`. This limits the effect of repeated evidence.

The overall relevance judgment caps the score:

| Relevance | Cap |
|---|---:|
| high | 100 |
| medium | 65 |
| low | 32 |
| none | 0 |

Grades are `strong ≥ 66`, `medium ≥ 33`, `weak > 0`, and `none = 0`.

Duplicate national targets are excluded. Related objectives, targets, and actions may all explain a match, but repeated wording must not be counted as independent evidence.
