"""Write transformed rows to raw_data.action_policy_signals_staging."""
from os import path

from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def load_action_policy_signals_staging(df: DataFrame, **kwargs) -> DataFrame:
    if df is None or df.empty:
        print("No rows to stage.")
        return df

    config_loader = ConfigFileLoader(path.join(get_repo_path(), "io_config.yaml"), "default")
    with Postgres.with_config(config_loader) as loader:
        loader.export(
            df,
            "raw_data",
            "action_policy_signals_staging",
            index=False,
            if_exists="replace",
        )

    print(f"Staged {len(df)} rows into raw_data.action_policy_signals_staging.")
    return df
