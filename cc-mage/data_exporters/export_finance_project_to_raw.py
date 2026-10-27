"""Write the unioned project frame to raw_data.finance_project_staging (replace; staging is throwaway)."""
from os import path

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# Names Mage's Postgres export mangles (e.g. status -> _status), which then breaks the modelled SQL.
# finance_project has none today, but guard so a future column is caught with a clear message.
RESERVED_COLUMN_NAMES = {
    "status", "order", "group", "user", "type", "end", "table", "column",
    "select", "from", "where", "limit", "offset", "default", "references",
    "primary", "unique", "constraint", "check", "desc", "asc",
}


@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    bad = sorted(c for c in df.columns if c.lower() in RESERVED_COLUMN_NAMES)
    if bad:
        raise ValueError(
            f"Reserved column name(s) {bad} will be mangled by Mage's Postgres export "
            f"(e.g. status -> _status), breaking the modelled SQL. Rename them in the transformer."
        )
    config_path = path.join(get_repo_path(), "io_config.yaml")
    with Postgres.with_config(ConfigFileLoader(config_path, "default")) as loader:
        loader.export(df, "raw_data", "finance_project_staging", index=False, if_exists="replace")
