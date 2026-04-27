# Calibration Policy — C40 Benchmark Context (2024)

## Purpose

Define a consistent policy for converting benchmark distributions into QA rules
for outlier flagging in city emissions data.

This policy is for **plausibility/consistency flags** (soft flags), not for
structural validation failures (hard fails).

## Core rule design

- Use per-capita distributions by `gpc_reference_number` as the default baseline.
- Calibrate low/high soft flags from empirical C40 distributions.
- Keep all calibrated thresholds traceable to a release artifact in
  `releases/2024/data/`.

## Threshold strategy by sample size

1. `count >= 100`
   - Use p05 (low) and p95 (high) bounds as primary soft-flag thresholds.
   - Rationale: enough sample support for percentile-based context.

2. `30 <= count < 100`
   - Use p05/p95 with caution.
   - Add review note that bounds are moderate-confidence and should be revisited
     as more coverage is added.

3. `count < 30`
   - Do not activate strict numeric low/high thresholds by default.
   - Prefer contextual rules (for example, zero-value checks, boundary checks,
     industrial profile pairing checks).
   - If numeric thresholds are used, mark as provisional.

## When to use IQR fences

- Use IQR fences (`Q1 - 1.5*IQR`, `Q3 + 1.5*IQR`) as diagnostic context, not as
  default production bounds.
- Use IQR particularly for subsectors with heavy skew or long right tails
  (common in energy industries and industrial process categories).
- If p95 is clearly too permissive for review goals, compare p95 vs IQR-high and
  document the selected policy for that subsector.

## Recommended severity mapping

- `hard_fail`
  - Structural/data-integrity defects (schema mismatch, required nulls, invalid
    keys, impossible negatives in non-sink sectors).
- `soft_flag`
  - Calibrated low/high percentile bounds.
  - Contextual interpretation checks (boundary effects, expected profile pairing).

## Escalation guidance for repeated flags

- First occurrence: flag and require investigation note.
- Repeated occurrence (same city/subsector across releases):
  - escalate to targeted source-method review.
  - consider updating benchmark stratification (for example, climate zone,
    city-size group, or regional cohorts).

## Recalibration triggers

Recalibrate thresholds when any of the following occurs:

- New major source release is added to the benchmark base.
- Distribution shift >20% in median for a calibrated subsector.
- Large increase in city coverage (for example, +25% records for a subsector).
- Methodological change in normalization inputs (population source, sector scope).

## Output requirements for rule provenance

Each calibrated rule should include:

- `source_stat` (for example `p95_of_ii1_1_per_capita_tco2e`)
- release version (`2024` currently)
- source file reference in `releases/2024/data/`
- explicit `recommended_action`

This keeps QA-agent output explainable and suitable for MCP context responses.
