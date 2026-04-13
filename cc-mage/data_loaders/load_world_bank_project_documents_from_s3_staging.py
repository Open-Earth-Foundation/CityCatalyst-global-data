from os import path

from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_world_bank_project_documents_from_s3_staging(*args, **kwargs) -> DataFrame:
    """
    Load World Bank project document PDF S3 URIs from raw_data.<table_name>.

    Optional kwargs: source_project_id — when set, restrict to that project_id.
    """
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    table_name = kwargs.get("table_name", "world_bank_projects_staging")
    source_name = kwargs.get("source_name", "world_bank")
    country_code = kwargs.get("country_code")
    source_project_id = kwargs.get("source_project_id")

    source_filter = ""
    if source_name:
        safe_source_name = str(source_name).replace("'", "").strip()
        source_filter = f"AND source_name = '{safe_source_name}'"

    country_filter = ""
    if country_code:
        safe_country_code = str(country_code).replace("'", "").strip().upper()
        country_filter = f"AND UPPER(country_code) = '{safe_country_code}'"

    project_filter = ""
    if source_project_id:
        safe_project_id = str(source_project_id).replace("'", "").strip()
        project_filter = f"AND project_id = '{safe_project_id}'"

    query = f"""
    SELECT
      project_id::TEXT AS source_project_id,
      s3_uri::TEXT AS s3_uri
    FROM raw_data.{table_name}
    WHERE project_id IS NOT NULL
      AND s3_uri IS NOT NULL
      {source_filter}
      {country_filter}
      {project_filter}
    ORDER BY project_id
    """

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        df = loader.load(query)

    print(f"Loaded {len(df)} rows from raw_data.{table_name}.")
    return df


@test
def test_output(output, *args) -> None:
    """Validate block output exists."""
    assert output is not None, "The output is undefined"
