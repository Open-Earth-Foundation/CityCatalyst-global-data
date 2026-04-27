#!/usr/bin/env python3
"""
Regenerate C40 benchmark calibration artifacts from the source workbook.

Outputs:
- data/c40_city_year_subsector_values.csv
- data/c40_subsector_per_capita_stats.csv
- data/c40_initial_threshold_calibration.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


DEFAULT_SELECTED_SUBSECTORS = [
    "I.1.1",
    "I.2.1",
    "II.1.1",
    "III.1.1",
    "III.4.1",
    "I.4.1",
    "IV.1",
]


def build_base_dataframe(workbook_path: Path) -> pd.DataFrame:
    df = pd.read_excel(workbook_path, sheet_name="C40 database with percapita")
    df = df.rename(
        columns={
            "City name": "city_name",
            "Country": "country",
            "gpc_reference_number": "gpc_reference_number",
            "year": "year",
            "total": "total_tco2e",
            "Population": "population",
            "Per capita value": "per_capita_tco2e",
        }
    )

    for column in ["total_tco2e", "population", "per_capita_tco2e", "year"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df[
        [
            "city_name",
            "country",
            "gpc_reference_number",
            "year",
            "total_tco2e",
            "population",
            "per_capita_tco2e",
        ]
    ].dropna(subset=["gpc_reference_number"])


def build_subsector_stats(base_df: pd.DataFrame) -> pd.DataFrame:
    stats_df = (
        base_df.groupby("gpc_reference_number")["per_capita_tco2e"]
        .agg(
            count="count",
            mean="mean",
            median="median",
            min="min",
            max="max",
            std="std",
            p05=lambda s: s.quantile(0.05),
            p25=lambda s: s.quantile(0.25),
            p75=lambda s: s.quantile(0.75),
            p95=lambda s: s.quantile(0.95),
        )
        .reset_index()
    )
    stats_df["sector_prefix"] = stats_df["gpc_reference_number"].astype(str).str.extract(
        r"^(I{1,3}|IV|V|VI)\."
    )
    return stats_df


def build_initial_calibration(
    base_df: pd.DataFrame, selected_subsectors: list[str]
) -> pd.DataFrame:
    rows = []
    for gpc in selected_subsectors:
        series = base_df.loc[
            base_df["gpc_reference_number"] == gpc, "per_capita_tco2e"
        ].dropna()
        if series.empty:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        rows.append(
            {
                "gpc_reference_number": gpc,
                "count": int(series.count()),
                "median_per_capita_tco2e": series.median(),
                "p05_per_capita_tco2e": series.quantile(0.05),
                "p95_per_capita_tco2e": series.quantile(0.95),
                "iqr_low_suggested": q1 - 1.5 * iqr,
                "iqr_high_suggested": q3 + 1.5 * iqr,
                "note": "Use as soft-flag context; investigate before asserting error.",
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regenerate C40 benchmark calibration CSV artifacts."
    )
    parser.add_argument(
        "--workbook",
        required=True,
        help="Absolute path to C40 workbook (.xlsx).",
    )
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).parent / "data"),
        help="Directory where output CSV files will be written.",
    )
    args = parser.parse_args()

    workbook_path = Path(args.workbook).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    base_df = build_base_dataframe(workbook_path)
    stats_df = build_subsector_stats(base_df)
    calibration_df = build_initial_calibration(base_df, DEFAULT_SELECTED_SUBSECTORS)

    base_df.to_csv(output_dir / "c40_city_year_subsector_values.csv", index=False)
    stats_df.to_csv(output_dir / "c40_subsector_per_capita_stats.csv", index=False)
    calibration_df.to_csv(output_dir / "c40_initial_threshold_calibration.csv", index=False)

    print("Wrote:")
    print(output_dir / "c40_city_year_subsector_values.csv")
    print(output_dir / "c40_subsector_per_capita_stats.csv")
    print(output_dir / "c40_initial_threshold_calibration.csv")


if __name__ == "__main__":
    main()
