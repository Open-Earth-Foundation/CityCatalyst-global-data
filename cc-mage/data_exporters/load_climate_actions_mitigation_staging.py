from os import path

from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def load_climate_actions_mitigation_staging(df: DataFrame, **kwargs) -> DataFrame:
    """
    Replace ``raw_data.climate_actions_mitigation_staging`` with the merged C40 / iCARE / IPCC
    mitigation catalog (EN-base columns plus ``*_i18n`` JSON strings and ``mitigation_source``).
    """
    if df is None or df.empty:
        print("No climate-actions mitigation rows to stage.")
        return df

    schema_name = "raw_data"
    table_name = "climate_actions_mitigation_staging"
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_loader = ConfigFileLoader(config_path, "default")

    with Postgres.with_config(config_loader) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,
            if_exists="replace",
        )

    print(f"Staged {len(df)} rows into {schema_name}.{table_name}.")
    return df
