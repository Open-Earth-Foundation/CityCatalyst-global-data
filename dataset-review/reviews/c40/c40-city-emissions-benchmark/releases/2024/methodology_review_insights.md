# Methodology Review Insights — C40 Benchmark Context (2024)

## Purpose

Capture methodological notes for using C40-aligned sources as context for
benchmarking sector values and identifying outliers in city emissions data.

## Scope of this release

- Sector interpretation context for GPC-aligned city emissions values.
- Context is used for QA interpretation, not as authoritative truth labels.
- Intended for both human review and machine-assisted DQ checks.

## Source data ingested for calibration

- Source workbook: `C40 GPC Inventory DB (reformatted).xlsx`
- Sheets used:
  - `C40 database` (17,108 rows)
  - `C40 database with percapita` (17,108 rows)
  - `Pivot Table 1` (reference summary by subsector)
- Distinct GPC references observed: 52
- Derived artifacts saved in `releases/2024/data/` for reproducible threshold tuning.
- Initial calibrated soft-flag thresholds implemented for:
  - `I.1.1`, `I.2.1`, `II.1.1`, `III.1.1`, `III.4.1`, `I.4.1`, `IV.1`
  - using p05/p95 per-capita bounds from C40 distributions.
- Calibration decision rules documented in `calibration_policy.md`.
- Recalibration command and output artifacts documented in `data/README.md`.

## Initial methodology notes

- Emissions values are estimates and may differ across credible methodologies.
- Context thresholds should produce investigation flags, not automatic rejection.
- Sector-specific interpretation is required; cross-sector comparisons can be
  misleading without normalization.

## Validation principles

- Structural issues remain hard-fail checks in pipeline validation.
- Plausibility and consistency checks are soft flags requiring review notes.
- Any accepted anomaly must include documented reasoning.

## Open items

- Confirm license/reuse constraints for all benchmark source references.
- Add release-specific references and URLs used to set threshold bands.
- Document calibration approach for city-size and climate stratification.
- Decide final percentile policy (for example p05/p95 vs IQR fences) per subsector.
