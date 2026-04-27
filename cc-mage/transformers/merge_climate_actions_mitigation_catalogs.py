"""Concatenate C40, iCARE, and IPCC mitigation dataframes (EN-base + *_i18n) for staging."""

import pandas as pd
from pandas import DataFrame

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def merge_climate_actions_mitigation_catalogs(
    c40_mitigation: DataFrame,
    icare_mitigation: DataFrame,
    ipcc_mitigation: DataFrame,
    *args,
    **kwargs,
) -> DataFrame:
    """
    Union the three publisher extracts. Each upstream row is already EN-shaped with
    ``*_i18n`` JSON text columns. Adds ``mitigation_source`` (``c40`` | ``icare`` | ``ipcc``).
    """
    labeled = [
        c40_mitigation.assign(mitigation_source="c40"),
        icare_mitigation.assign(mitigation_source="icare"),
        ipcc_mitigation.assign(mitigation_source="ipcc"),
    ]
    out = pd.concat(labeled, ignore_index=True, sort=False)
    return out.fillna("")


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
    assert not output.empty, "Expected non-empty merged dataframe"
    assert "mitigation_source" in output.columns
    assert set(output["mitigation_source"].unique()) <= {"c40", "icare", "ipcc"}
    assert "src_action_id" in output.columns
