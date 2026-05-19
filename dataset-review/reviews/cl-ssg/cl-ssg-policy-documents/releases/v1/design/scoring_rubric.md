# Scoring rubric

Rubric version: `0.1.0`. Owner: amanda. Last updated: 2026-05-16.

## Goal

For a given Chilean city and a given climate action, produce:

- `score_raw`: a continuous strength score in `[0, 1)` after saturation
- `score_bucket`: one of `strong | medium | weak | none`
- `top_evidence`: a ranked, deduplicated list of the strongest underlying findings, with citations back to source document, page, and section

The score must be inspectable. Every score traces back to a finite list of findings, each with verbatim evidence_text, source_document_id, page, and the weights used.

## Inputs to the score

Each `(city, action)` score is computed over the set of findings F:

```
F(city, action) = {
  finding f
    : there exists a row (city_code = city, source_document_id = d) in city_applicable_policies.csv
      and f belongs to the action_findings file at action_findings/d/action.json
      and f passed verbatim and schema validation
}
```

i.e. only findings on documents that apply to the city are counted.

## Per-finding strength

For each finding f, compute:

```
finding_strength(f) =
    proximity_weight(f.source_level)
  * confidence_weight(f.signal_confidence)
  * relation_weight(f.primitive_relation)
  * explicitness_weight(f.explicitness)
```

Multiplicative form is intentional. A low-confidence, low-proximity, restating finding should not stack to a strong score just because there are many of them.

### proximity_weight (by source_level + document_type)

Driven from `city_applicable_policies.csv`, which sets `proximity_weight` for the `(city, document)` row. The default weights:

| Document class                                   | source_level   | document_type        | proximity_weight |
|--------------------------------------------------|----------------|----------------------|------------------|
| PACCC (municipal climate action plan)            | municipal      | paccc                | 1.00             |
| Direct communal plan (e.g. PRAS for that comuna) | communal       | environmental_program| 1.00             |
| Intercommunal plan covering this comuna          | intercommunal  | territorial_plan     | 0.85             |
| Regional PARCC for this city's region            | regional       | parcc                | 0.70             |
| Regional territorial plan for this region        | regional       | territorial_plan     | 0.55             |
| National sector mitigation plan                  | national       | sector_plan          | 0.50             |
| ECLP (national long-term strategy)               | national       | framework            | 0.35             |
| NDC (national commitment)                        | national       | framework            | 0.30             |
| Other national framework                         | national       | framework            | 0.30             |
| Other national territorial plan                  | national       | territorial_plan     | 0.25             |

Notes:

- A document whose `document_status` is not `final` (i.e. `draft`, `consultation`, `portal_only`, `flipbook_only`) is multiplied by 0.7 on the row's `proximity_weight`. This is a soft penalty for non-final instruments without dropping their evidence entirely.
- Placeholder documents (`document_status = placeholder`) are excluded at the applicability step and never reach scoring.
- The weights are intentionally separated by `(source_level, document_type)`. A regional territorial plan is not as strong as a regional PARCC for action-mapping purposes, because territorial plans rarely commit to operational measures.

### confidence_weight (by signal_confidence)

| signal_confidence | weight |
|-------------------|--------|
| high              | 1.00   |
| medium            | 0.60   |
| low               | 0.30   |

`signal_confidence` is set by the extraction model with these definitions (preserved from the prototype):

- `high`: passage explicitly and unambiguously addresses the action
- `medium`: passage addresses the action's theme but the link requires interpretation
- `low`: passage is tangentially related and the link may be coincidental

### relation_weight (by primitive_relation)

| primitive_relation | weight | rationale                                                                 |
|--------------------|--------|---------------------------------------------------------------------------|
| commits            | 1.00   | Explicit commitment to take the action.                                   |
| targets            | 1.00   | Quantified or dated target tied to the action.                            |
| funds              | 1.00   | Funding line or financing mechanism tied to the action.                   |
| monitors           | 0.80   | MRV indicator or review cycle tied to the action.                         |
| governs            | 0.80   | Lead body or instrument assigned to the action.                           |
| prioritizes        | 0.70   | Names the action's theme as a priority without committing to the action.  |
| identifies         | 0.50   | Names a relevant risk, gap, or enabling condition.                        |
| references        | 0.40   | Points to another instrument that addresses the action.                   |
| contextualizes     | 0.40   | Background or framing relevant to the action.                             |
| restates          | 0.30   | Restates a higher-level commitment without adding regional substance.     |

`restates` is deliberately weak: if a PARCC simply repeats an NDC target, the regional document is not adding evidence of regional implementation.

### explicitness_weight (by explicitness)

| explicitness | weight |
|--------------|--------|
| explicit     | 1.00   |
| inferred     | 0.60   |

`explicit` means the passage directly addresses the action by name or by a clearly synonymous description. `inferred` means the connection requires interpretation. If `explicitness` is missing on a finding, treat it as `explicit` (the more conservative default given the verbatim-substring requirement).

## Aggregation: saturating sum

Per-finding strengths are summed and passed through a saturation function to produce a raw, uncapped score:

```
sum_strength(city, action)        = sum_{f in F(city, action)} finding_strength(f)

score_raw_uncapped(city, action)  = 1 - exp(-sum_strength(city, action) / K)
```

`K` is the saturation constant. Default: `K = 4.0` (raised from 2.0 in v0.2.0).

Properties of this shape (with `K = 4.0`):

- 1 strong commit finding (strength `1.0`) -> `score_raw_uncapped ~ 0.22`
- 2 strong commit findings -> `score_raw_uncapped ~ 0.39`
- 4 strong commit findings -> `score_raw_uncapped ~ 0.63`
- 8 strong commit findings -> `score_raw_uncapped ~ 0.86`
- 16 strong commit findings -> `score_raw_uncapped ~ 0.98`
- 5 medium-confidence boilerplate `commits` findings on a regional PARCC (each `0.49*0.6*1.0*1.0 = 0.294`, sum `1.47`) -> `score_raw_uncapped ~ 0.31` (now bucketed `weak`, was `medium`+ at K=2.0)

i.e. saturation now requires roughly twice the evidence to reach the same bucket as v0.1.0. This makes "5 medium findings on broad atoms" no longer enough to bucket as `strong`.

## Relevance cap (v0.2.0)

The matcher returns a per-(action, doc) `relevance` grade — its overall judgement of how much the document says about the action. This grade is now authoritative as a ceiling on `score_raw`. The intuition: the matcher is reading the full atoms list and making a judgement; if it says the doc only tangentially touches the action, the rubric should not promote that to `strong` just because boilerplate atoms repeated across sections.

Compute the city-action `best_relevance` as the strongest `relevance` value across all applicable docs that returned at least one finding, using this order: `none < low < medium < high`. The cap table:

| best_relevance | cap on `score_raw` | resulting bucket ceiling |
|----------------|--------------------|--------------------------|
| `none`         | 0.00               | `none`                   |
| `low`          | 0.32               | `weak`                   |
| `medium`       | 0.65               | `medium`                 |
| `high`         | 1.00 (uncapped)    | `strong`                 |

Final score:

```
score_raw(city, action) = min(score_raw_uncapped, cap(best_relevance))
```

Why the cap goes by `best_relevance` across applicable docs, not by individual doc: a city's alignment for an action is the strongest expression of that alignment in any applicable policy. If a PACCC has a `high`-relevance commitment, that's the alignment fact, even if national-level docs only contextualise. Conversely, if every applicable doc only mentions the action tangentially, accumulating those tangents should not invent a strong alignment.

## Bucket thresholds (unchanged from 0.1.0)

| score_raw    | score_bucket |
|--------------|--------------|
| `>= 0.66`    | strong       |
| `>= 0.33`    | medium       |
| `> 0.0`      | weak         |
| `== 0.0`     | none         |

Aligned to the saturating curve and the relevance cap so (at K=4.0):

- `strong` requires `best_relevance = high` from at least one applicable doc, plus roughly 4+ strong commit findings (or many medium ones).
- `medium` requires `best_relevance = high` or `medium` plus some evidence; or many medium findings under a `high` cap.
- `weak` means at least some applicable evidence, with the matcher's `best_relevance` no higher than `low`.
- `none` means every applicable doc returned `relevance=none` or had no findings.

Thresholds will be re-calibrated against the held-out eval set once we have city-level scores across multiple regions.

## Deduplication of findings before scoring

A single passage can be flagged in multiple findings (e.g. once as `action/commits` and once as `target/targets` if it contains both a commitment and a number). For scoring:

- We do NOT deduplicate across `primitive_type` for the same `(source_document_id, page, evidence_text)` — those are intentionally distinct contributions.
- We DO deduplicate within `(source_document_id, page, evidence_text, primitive_type, primitive_relation)`. Identical findings emitted twice by the model count once.

## Handling restatements explicitly

If a regional or municipal document restates a national commitment verbatim or near-verbatim:

1. The model is instructed to set `primitive_relation = restates` and lower `signal_confidence`.
2. The finding optionally carries `restatement_of` pointing back to the source instrument.
3. The relation_weight of 0.30 ensures restatements add little to the score.
4. When computing `top_evidence`, restating findings are only surfaced if there are fewer than N higher-strength findings available.

This means a city with a PARCC that only repeats the NDC will score lower than a city with a PARCC that adds its own regional commitments, which matches the intended evidentiary hierarchy.

## Worked example

City: Arica (region_code=15). Action: `ipcc_0053` (afforestation, reforestation, forest ecosystem restoration).

Applicable documents for Arica include (truncated):

| doc                              | source_level | document_type        | proximity_weight |
|----------------------------------|--------------|----------------------|------------------|
| chl_parcc_arica                  | regional     | parcc                | 0.70 (draft -> 0.49) |
| chl_agricultura_sector_plan      | national     | sector_plan          | 0.50             |
| chl_eclp_2021                    | national     | framework            | 0.35             |
| chl_ndc                          | national     | framework            | 0.30             |

Suppose extraction yields, on `chl_parcc_arica`, two `action/commits` findings with `signal_confidence=high, explicitness=explicit` for related afforestation measures, plus one `governance/governs` finding describing the GORE as lead body.

```
f1: 0.49 * 1.0 * 1.0 * 1.0 = 0.490
f2: 0.49 * 1.0 * 1.0 * 1.0 = 0.490
f3: 0.49 * 1.0 * 0.8 * 1.0 = 0.392

sum_strength = 1.372
score_raw    = 1 - exp(-1.372 / 2.0) = 1 - 0.504 = 0.496
score_bucket = medium
```

If we also pick up a strong `target/targets` finding on the same PARCC with the regional 30% forest cover commitment (strength 0.49), the score climbs:

```
sum_strength = 1.862
score_raw    = 1 - exp(-1.862 / 2.0) = 1 - 0.394 = 0.606
score_bucket = medium (just below 0.66)
```

A PACCC for Arica with a single explicit commitment would land at:

```
sum_strength contribution = 1.00
score_raw climbs above 0.66 -> strong
```

This illustrates the intended ordering: local implementation evidence dominates national context, and the bucket boundaries roughly correspond to "credible regional commitment" (medium) vs "explicit local commitment" (strong).

## Versioning

Every row in `data/policy_score/<run>/scores.jsonl` carries `rubric_version`. The scorer refuses to merge results across versions. Bump the version on any change to:

- weight tables
- saturation function shape or `K`
- bucket thresholds
- deduplication rules
- treatment of `document_status`

## Calibration plan

1. Run extraction over the existing 27 viable documents x a small `actions.csv` subset (e.g. 10 representative actions).
2. Score 3-5 manually selected cities, including one Metropolitana city, one with a real PARCC final, and one with only national coverage.
3. Compare the score buckets to a manual judgement made independently from the same evidence files.
4. Tune `K` and the bucket thresholds, not the per-finding weights, unless the weights produce obvious ordering mistakes.
5. Lock `rubric_version = 1.0.0` once buckets agree with manual judgement on the calibration set.
