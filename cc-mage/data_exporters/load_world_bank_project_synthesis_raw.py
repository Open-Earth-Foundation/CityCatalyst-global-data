from os import path

from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> DataFrame:
    """Persist synthesis JSON output rows into a raw_data staging table."""
    schema_name = "raw_data"
    table_name = kwargs.get("table_name", "world_bank_project_synthesis_staging")
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    config_loader = ConfigFileLoader(config_path, config_profile)

    if df is None or df.empty:
        print("No synthesis rows to stage.")
        return df

    # Keep legacy staging schema stable; enrichment step reads S3 JSON explicitly.
    stage_df = df.copy()
    if "status" in stage_df.columns and "_status" not in stage_df.columns:
        stage_df["_status"] = stage_df["status"]
    stage_columns = ["source_project_id", "atoms_count", "synthesis_s3_uri", "_status"]
    for column in stage_columns:
        if column not in stage_df.columns:
            stage_df[column] = None
    stage_df = stage_df[stage_columns]

    with Postgres.with_config(config_loader) as loader:
        loader.export(
            stage_df,
            schema_name,
            table_name,
            index=False,
            if_exists="replace",
        )
    return df
