"""OEF Chile city-action fundability v3 city profile: bare S3 read.

The uploaded CSV is the reviewed 345-comuna join of the INE-derived capacity tier and
SUBDERE SIM/BEP autonomy. Shaping here is intentionally limited to source tagging;
locode resolution and the modelled-table projection live in
transformers/transform_city_finance_profile.py.
"""
from os import path

import pandas as pd
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from mage_ai.settings.repo import get_repo_path

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

SOURCE = "oef/cl-city-action-fundability"
REQUIRED_COLUMNS = {
    "comuna_cut",
    "autonomy",
    "capacity",
    "city_archetype",
    "capacity_basis",
    "autonomy_basis",
    "autonomy_source_vintage",
}


@data_loader
def load_data(*args, **kwargs):
    bucket = kwargs.get("source_bucket", "test-global-api")
    version = kwargs.get("source_release_version", "v3")
    key = (
        "raw_data/oef/cl_city_action_fundability/"
        f"release/{version}/cl_city_action_fundability.csv"
    )
    config_path = path.join(get_repo_path(), "io_config.yaml")
    df = S3.with_config(ConfigFileLoader(config_path, "default")).load(
        bucket, key, dtype=str
    )
    df["_source_dataset"] = SOURCE
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, "city-profile S3 loader returned no frame"
    missing = REQUIRED_COLUMNS - set(output.columns)
    assert not missing, f"city-profile upload missing columns: {sorted(missing)}"
    assert len(output) == 345, f"expected 345 uploaded comunas, got {len(output)}"

    cut = output["comuna_cut"].astype(str).str.strip().str.zfill(5)
    assert cut.str.fullmatch(r"\d{5}").all(), "comuna_cut must be five digits"
    assert cut.is_unique, "uploaded comuna_cut is not unique"

    for column in ("autonomy", "capacity"):
        values = pd.to_numeric(output[column], errors="coerce")
        assert values.notna().all(), f"{column} contains non-numeric or null values"
        assert values.between(0, 1).all(), f"{column} outside [0,1]"

    assert output["_source_dataset"].eq(SOURCE).all(), "unexpected source identity"
