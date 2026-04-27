# Data Notes

This folder contains derived benchmark artifacts produced from the source workbook:
`C40 GPC Inventory DB (reformatted).xlsx`.

## Included files

- `c40_city_year_subsector_values.csv`
  - Normalized city-year-subsector records extracted from the C40 workbook.
  - Key columns: `city_name`, `country`, `gpc_reference_number`, `year`,
    `total_tco2e`, `population`, `per_capita_tco2e`.

- `c40_subsector_per_capita_stats.csv`
  - Distribution stats by `gpc_reference_number` (count, median, p05, p95, IQR context).
  - Used as benchmark evidence for plausibility checks.

- `c40_initial_threshold_calibration.csv`
  - Starter threshold bands for selected subsectors.
  - Designed for soft-flag QA checks and iterative calibration.

## Re-run calibration

From repo root, run:

`python dataset-review/reviews/c40/c40-city-emissions-benchmark/releases/2024/recalibrate_from_workbook.py --workbook "/Users/admin/Downloads/C40 GPC Inventory DB (reformatted).xlsx"`

If needed, set a different output location with `--output-dir`.
