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
    Write Chile INE Census 2024 attribute staging data to
    raw_data.cl_ine_censo_staging. Replaces the staging table on each run.

    Schema: locode, region_nombre, attribute_type, attribute_value,
            attribute_units, attribute_category
    """
    schema_name = 'raw_data'
    table_name  = 'cl_ine_censo_staging'
    config_path    = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,
            if_exists='replace',
        )
