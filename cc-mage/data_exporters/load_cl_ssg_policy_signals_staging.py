from os import path

from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def load_cl_ssg_policy_signals_staging(df: DataFrame, **kwargs) -> DataFrame:
    """Write transformed policy signals to raw_data staging."""
    if df is None or df.empty:
        print("No policy signals to stage.")
        return df

    schema_name = "raw_data"
    table_name = "cl_ssg_policy_signals_staging"
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    config_loader = ConfigFileLoader(config_path, config_profile)

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
