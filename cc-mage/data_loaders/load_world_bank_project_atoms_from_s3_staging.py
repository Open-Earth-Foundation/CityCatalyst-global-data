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
def load_world_bank_project_atoms_from_s3_staging(*args, **kwargs) -> DataFrame:
    """
    Load project-level catalog rows for World Bank projects that have staged documents.

    Optional kwargs:
    - source_project_id: restrict to a single World Bank project.
    - country_code: optional two-letter country code filter.
    """
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    source_name = kwargs.get("source_name", "world_bank")
    country_code = kwargs.get("country_code")
    source_project_id = kwargs.get("source_project_id")

    source_filter = ""
    if source_name:
        safe_source_name = str(source_name).replace("'", "").strip()
        source_filter = (
            f"AND (d.source_name = '{safe_source_name}' "
            f"OR p.source_name = '{safe_source_name}')"
        )

    country_filter = ""
    if country_code:
        safe_country_code = str(country_code).replace("'", "").strip().upper()
        country_filter = (
            f"AND UPPER(COALESCE(p.country_code::TEXT, d.country_code::TEXT, '')) "
            f"= '{safe_country_code}'"
        )

    project_filter = ""
    if source_project_id:
        safe_project_id = str(source_project_id).replace("'", "").strip()
        project_filter = f"AND d.project_id::TEXT = '{safe_project_id}'"

    query = f"""
    SELECT DISTINCT
      d.project_id::TEXT AS source_project_id,
      p.project_name::TEXT AS project_name,
      COALESCE(p.source_name::TEXT, d.source_name::TEXT, 'world_bank') AS source_name,
      p.country_name::TEXT AS country,
      COALESCE(p.country_code::TEXT, d.country_code::TEXT) AS country_code,
      p.sector_name::TEXT AS sector,
      p.project_status::TEXT AS status,
      p.total_commitment_amount::FLOAT AS total_commitment_amount,
      p.approval_at::DATE AS approval_date,
      p.closing_at::DATE AS closing_date
    FROM raw_data.world_bank_project_documents_staging d
    LEFT JOIN modelled.project_portfolio p
      ON p.source_project_id::TEXT = d.project_id::TEXT
    WHERE d.project_id IS NOT NULL
      {source_filter}
      {country_filter}
      {project_filter}
    ORDER BY source_project_id
    """

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        df = loader.load(query)

    print(f"Loaded {len(df)} candidate project(s) for synthesis.")
    return df


@test
def test_output(output, *args) -> None:
    """Validate block output exists."""
    assert output is not None, "The output is undefined"
