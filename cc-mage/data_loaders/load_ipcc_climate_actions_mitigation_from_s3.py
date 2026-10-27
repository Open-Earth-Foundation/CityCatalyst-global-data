"""IPCC mitigation actions: S3 triple (en/es/pt) → EN-base table with ``*_i18n`` JSON columns."""

import json
from os import path
from typing import Dict

import pandas as pd
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

_I18N_SOURCE_COLUMNS = (
    "action_name",
    "description",
    "outcome_summary",
    "intervention_summary",
)


def _load_csv(s3: S3, bucket: str, key: str) -> DataFrame:
    return s3.load(bucket, key, dtype=str, engine="python", on_bad_lines="warn").fillna("")


def _object_keys_for_locales(prefix: str) -> Dict[str, str]:
    base = prefix.strip().rstrip("/")
    return {lang: f"{base}_{lang}.csv" for lang in ("en", "es", "pt")}


def _cell_str(val) -> str:
    if val is None or val == "":
        return ""
    try:
        if pd.isna(val):
            return ""
    except TypeError:
        pass
    return str(val)


def _merge_locales_to_en_base(dfs: Dict[str, DataFrame]) -> DataFrame:
    df_en = dfs["en"].copy()
    df_es = dfs["es"][["src_action_id", *_I18N_SOURCE_COLUMNS]].copy()
    df_pt = dfs["pt"][["src_action_id", *_I18N_SOURCE_COLUMNS]].copy()

    for col in _I18N_SOURCE_COLUMNS:
        df_es = df_es.rename(columns={col: f"{col}_locale_es"})
        df_pt = df_pt.rename(columns={col: f"{col}_locale_pt"})

    merged = df_en.merge(df_es, on="src_action_id", how="left").merge(df_pt, on="src_action_id", how="left")

    for col in _I18N_SOURCE_COLUMNS:
        es_c = f"{col}_locale_es"
        pt_c = f"{col}_locale_pt"
        merged[es_c] = merged[es_c].fillna("")
        merged[pt_c] = merged[pt_c].fillna("")
        merged[f"{col}_i18n"] = [
            json.dumps(
                {"en": _cell_str(e), "es": _cell_str(s), "pt": _cell_str(p)},
                ensure_ascii=False,
            )
            for e, s, p in zip(merged[col], merged[es_c], merged[pt_c], strict=True)
        ]
        merged = merged.drop(columns=[col, es_c, pt_c])

    return merged


@data_loader
def load_ipcc_climate_actions_mitigation_from_s3(*args, **kwargs) -> DataFrame:
    """
    Read IPCC mitigation CSVs (en, es, pt) and return a single table keyed off EN.

    Same shape as the C40 / iCARE mitigation loaders: EN structural columns plus
    ``*_i18n`` JSON columns for ``action_name``, ``description``, ``outcome_summary``,
    ``intervention_summary``.

    Pipeline variables (``pipelines/action_pathways_to_modelled/metadata.yaml``):

    - ``source_bucket`` — S3 bucket (shared with other loaders in the pipeline)
    - ``ipcc_mitigation_s3_key_prefix`` — key prefix, e.g.
      ``files/ipcc/ipcc_climate_actions/release/2026-04-24/climate_actions_mitigation``
    """
    config_path = path.join(get_repo_path(), "io_config.yaml")
    bucket = str(kwargs["source_bucket"]).strip()
    key_prefix = str(kwargs["ipcc_mitigation_s3_key_prefix"]).strip()
    keys = _object_keys_for_locales(key_prefix)
    s3 = S3.with_config(ConfigFileLoader(config_path, "default"))
    dfs = {lang: _load_csv(s3, bucket, k) for lang, k in keys.items()}
    return _merge_locales_to_en_base(dfs)


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
    assert not output.empty, "Expected non-empty dataframe"
    assert "src_action_id" in output.columns
    for col in _I18N_SOURCE_COLUMNS:
        json_col = f"{col}_i18n"
        assert json_col in output.columns, f"missing {json_col}"
        sample = json.loads(output.iloc[0][json_col])
        assert set(sample.keys()) == {"en", "es", "pt"}, json_col
