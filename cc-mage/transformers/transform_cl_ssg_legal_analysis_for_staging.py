"""Normalize legal analysis dataframe column names for ``raw_data`` staging export."""
from __future__ import annotations

from pandas import DataFrame

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer


def _normalize_legal_analysis_columns(out: DataFrame) -> DataFrame:
    """Align CSV shapes with ``load_cl_ssg_legal_signals_modelled.sql`` staging expectations.

    Supports:

    - **Pipeline / DB shape** (already): ``src_action_id``, ``country_code``,
      ``ownership_description_en`` / ``_es``, ``restrictions_description_en`` / ``_es``,
      ``legal_justification_en`` / ``_es``, ``sector`` → ``gpc_sector``.
    - **Review / export shape** (alternate): ``action_id`` → ``src_action_id``;
      default ``country_code`` ``CL``; English in ``ownership_description`` /
      ``restrictions_description`` renamed to ``*_en``; Spanish in
      ``legal_justification`` renamed to ``legal_justification_es`` when
      ``legal_justification_en`` is present.
    """
    if "src_action_id" not in out.columns and "action_id" in out.columns:
        out = out.rename(columns={"action_id": "src_action_id"})
    if "country_code" not in out.columns:
        out["country_code"] = "CL"

    if "ownership_description_en" not in out.columns and "ownership_description" in out.columns:
        out = out.rename(columns={"ownership_description": "ownership_description_en"})
    if (
        "restrictions_description_en" not in out.columns
        and "restrictions_description" in out.columns
    ):
        out = out.rename(columns={"restrictions_description": "restrictions_description_en"})

    if (
        "legal_justification_es" not in out.columns
        and "legal_justification" in out.columns
        and "legal_justification_en" in out.columns
    ):
        out = out.rename(columns={"legal_justification": "legal_justification_es"})

    if "sector" in out.columns and "gpc_sector" not in out.columns:
        out = out.rename(columns={"sector": "gpc_sector"})
    return out


@transformer
def transform_cl_ssg_legal_analysis_for_staging(df: DataFrame, *args, **kwargs) -> DataFrame:
    """Rename columns for staging SQL and strip string fields."""
    if df is None or df.empty:
        print("No legal analysis rows to transform.")
        return df

    out = df.copy()
    out = _normalize_legal_analysis_columns(out)

    for col in out.columns:
        if out[col].dtype == object:
            out[col] = out[col].astype(str).str.strip()
            out[col] = out[col].replace({"nan": ""})
    return out
