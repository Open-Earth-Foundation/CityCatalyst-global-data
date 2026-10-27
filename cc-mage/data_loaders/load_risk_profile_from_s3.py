"""Stream the Adapta Brasil risk profile Parquet file into PostgreSQL."""

from os import path

import duckdb
from mage_ai.io.config import ConfigFileLoader, ConfigKey
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


STAGING_COLUMNS = (
    ("actor_id", "TEXT"),
    ("city_name", "TEXT"),
    ("country_code", "TEXT"),
    ("timeframe", "BIGINT"),
    ("scenario", "TEXT"),
    ("scenario_family", "TEXT"),
    ("sector_id", "BIGINT"),
    ("sector_name", "TEXT"),
    ("risk_id", "BIGINT"),
    ("risk_name", "TEXT"),
    ("risk_component_id", "BIGINT"),
    ("risk_component_name", "TEXT"),
    ("impact_chain_id_1", "BIGINT"),
    ("impact_chain_name_1", "TEXT"),
    ("impact_chain_id_2", "BIGINT"),
    ("impact_chain_name_2", "TEXT"),
    ("impact_chain_id_3", "BIGINT"),
    ("impact_chain_name_3", "TEXT"),
    ("base_indicator_id", "BIGINT"),
    ("base_indicator_name", "TEXT"),
    ("base_indicator_level", "BIGINT"),
    ("risk_value_numeric", "DOUBLE PRECISION"),
    ("risk_value_string", "TEXT"),
    ("risk_component_value_numeric", "DOUBLE PRECISION"),
    ("risk_component_value_string", "TEXT"),
    ("impact_chain_1_value_numeric", "DOUBLE PRECISION"),
    ("impact_chain_1_value_string", "TEXT"),
    ("impact_chain_2_value_numeric", "DOUBLE PRECISION"),
    ("impact_chain_2_value_string", "TEXT"),
    ("impact_chain_3_value_numeric", "DOUBLE PRECISION"),
    ("impact_chain_3_value_string", "TEXT"),
    ("base_indicator_value_numeric", "DOUBLE PRECISION"),
    ("base_indicator_value_string", "TEXT"),
    ("null_type", "TEXT"),
    ("release_id", "TEXT"),
    ("source_dataset", "TEXT"),
    ("release_version", "TEXT"),
    ("source_vintage", "TEXT"),
    ("spatial_support_level", "TEXT"),
    ("created_at", "TIMESTAMP WITH TIME ZONE"),
    ("updated_at", "TIMESTAMP WITH TIME ZONE"),
)


def _sql_literal(value: object) -> str:
    """Return a DuckDB string literal without exposing credentials to logs."""
    return "'" + str(value).replace("'", "''") + "'"


def _configure_s3(connection: duckdb.DuckDBPyConnection, config: ConfigFileLoader) -> None:
    access_key = config[ConfigKey.AWS_ACCESS_KEY_ID]
    secret_key = config[ConfigKey.AWS_SECRET_ACCESS_KEY]
    session_token = config[ConfigKey.AWS_SESSION_TOKEN]
    region = config[ConfigKey.AWS_REGION] or "us-east-1"

    if access_key and secret_key:
        options = [
            "TYPE s3",
            "PROVIDER config",
            f"KEY_ID {_sql_literal(access_key)}",
            f"SECRET {_sql_literal(secret_key)}",
            f"REGION {_sql_literal(region)}",
        ]
        if session_token:
            options.append(f"SESSION_TOKEN {_sql_literal(session_token)}")
    else:
        connection.execute("LOAD aws")
        options = [
            "TYPE s3",
            "PROVIDER credential_chain",
            f"REGION {_sql_literal(region)}",
        ]

    connection.execute(
        "CREATE SECRET adapta_s3 (\n    " + ",\n    ".join(options) + "\n)"
    )


def _configure_postgres(
    connection: duckdb.DuckDBPyConnection, config: ConfigFileLoader
) -> None:
    port = int(config[ConfigKey.POSTGRES_PORT] or 5432)
    options = [
        "TYPE postgres",
        f"HOST {_sql_literal(config[ConfigKey.POSTGRES_HOST])}",
        f"PORT {port}",
        f"DATABASE {_sql_literal(config[ConfigKey.POSTGRES_DBNAME])}",
        f"USER {_sql_literal(config[ConfigKey.POSTGRES_USER])}",
        f"PASSWORD {_sql_literal(config[ConfigKey.POSTGRES_PASSWORD])}",
    ]
    connection.execute(
        "CREATE SECRET ccglobal_postgres (\n    "
        + ",\n    ".join(options)
        + "\n)"
    )
    connection.execute(
        "ATTACH '' AS ccglobal (TYPE POSTGRES, SECRET ccglobal_postgres)"
    )


@data_loader
def load_from_s3_bucket(*args, **kwargs):
    """Replace the risk profile staging table without materialising a DataFrame."""
    bucket_name = kwargs["bucket_name"]
    object_key = kwargs["object_key"]
    memory_limit = kwargs.get("duckdb_memory_limit", "1GB")
    threads = int(kwargs.get("duckdb_threads", 2))
    if threads < 1:
        raise ValueError("duckdb_threads must be at least 1")

    s3_uri = f"s3://{bucket_name}/{object_key.lstrip('/')}"
    config = ConfigFileLoader(path.join(get_repo_path(), "io_config.yaml"), "default")

    connection = duckdb.connect()
    try:
        connection.execute("LOAD httpfs")
        connection.execute("LOAD postgres")
        connection.execute(f"SET memory_limit = {_sql_literal(memory_limit)}")
        connection.execute(f"SET threads = {threads}")
        connection.execute("SET preserve_insertion_order = false")
        _configure_s3(connection, config)
        _configure_postgres(connection, config)

        parquet_columns = tuple(
            row[0]
            for row in connection.execute(
                f"DESCRIBE SELECT * FROM read_parquet({_sql_literal(s3_uri)})"
            ).fetchall()
        )
        expected_columns = tuple(name for name, _ in STAGING_COLUMNS)
        if parquet_columns != expected_columns:
            raise ValueError(
                "Adapta Brasil Parquet columns do not match the staging schema. "
                f"Expected {expected_columns}, received {parquet_columns}."
            )

        column_definitions = ",\n    ".join(
            f'"{name}" {column_type}' for name, column_type in STAGING_COLUMNS
        )

        connection.execute("BEGIN")
        try:
            connection.execute(
                "DROP TABLE IF EXISTS ccglobal.raw_data.risk_profile_staging"
            )
            connection.execute(
                "CREATE TABLE ccglobal.raw_data.risk_profile_staging (\n"
                f"    {column_definitions}\n"
                ")"
            )
            result = connection.execute(
                "COPY ccglobal.raw_data.risk_profile_staging "
                f"FROM {_sql_literal(s3_uri)} (FORMAT PARQUET)"
            ).fetchone()
            connection.execute("COMMIT")
        except Exception:
            connection.execute("ROLLBACK")
            raise
    finally:
        connection.close()

    row_count = int(result[0]) if result else 0
    print(
        f"Staged {row_count} Adapta Brasil risk profile rows from {s3_uri} "
        "using DuckDB PostgreSQL binary COPY."
    )
    return DataFrame([{"row_count": row_count, "source": s3_uri}])


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
    assert not output.empty, "The output summary is empty"
    assert output["row_count"].iloc[0] > 0, (
        "No Adapta Brasil risk profile rows were staged"
    )
