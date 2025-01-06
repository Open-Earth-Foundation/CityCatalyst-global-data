from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    schema_name = 'raw_data'  # Specify the name of the schema to export data to
    table_name = 'br_city_polygon'  # Specify the name of the table to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    chunk_size = 100  # You can adjust this number based on your needs and system memory

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        for start in range(0, len(df), chunk_size):
            chunk = df.iloc[start:start + chunk_size]
            if_exist_policy = 'replace' if start == 0 else 'append'
            loader.export(
                chunk,
                schema_name,
                table_name,
                index=False,
                if_exists=if_exist_policy,  # Replace on first chunk, append subsequently
            )