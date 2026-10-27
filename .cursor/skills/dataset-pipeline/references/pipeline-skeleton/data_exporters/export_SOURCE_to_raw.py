"""Template — copy to cc-mage/data_exporters/export_<SOURCE>_to_raw.py.

Writes the staging frame to raw_data.<SOURCE>_staging with if_exists='replace'
(staging is throwaway; replace is idempotent).
"""
from os import path

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# Mage's export mangles reserved-word columns (status -> _status), breaking the modelled SQL.
# Fail fast with a clear message instead. Extend the set if Mage mangles a name not listed.
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
            f"(e.g. status -> _status). Rename them in the transformer to a non-reserved name."
        )

    config_path = path.join(get_repo_path(), "io_config.yaml")
    with Postgres.with_config(ConfigFileLoader(config_path, "default")) as loader:
        loader.export(df, "raw_data", "<SOURCE>_staging", index=False, if_exists="replace")
