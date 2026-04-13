import os
from os import path
from urllib.parse import urlparse

import boto3
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


def _resolve_aws_client_kwargs(config_loader: ConfigFileLoader) -> dict:
    config_dict = {}
    if hasattr(config_loader, "config") and isinstance(config_loader.config, dict):
        config_dict = config_loader.config
    elif hasattr(config_loader, "settings") and isinstance(config_loader.settings, dict):
        config_dict = config_loader.settings

    aws_access_key_id = config_dict.get("AWS_ACCESS_KEY_ID") or os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = (
        config_dict.get("AWS_SECRET_ACCESS_KEY") or os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    aws_session_token = config_dict.get("AWS_SESSION_TOKEN") or os.getenv("AWS_SESSION_TOKEN")
    region_name = config_dict.get("AWS_REGION") or os.getenv("AWS_REGION") or "us-east-1"

    kwargs = {"region_name": region_name}
    if aws_access_key_id and aws_secret_access_key:
        kwargs["aws_access_key_id"] = aws_access_key_id
        kwargs["aws_secret_access_key"] = aws_secret_access_key
    if aws_session_token:
        kwargs["aws_session_token"] = aws_session_token
    return kwargs


def _parse_s3_uri(s3_uri: str) -> tuple[str, str]:
    parsed = urlparse(s3_uri)
    if parsed.scheme != "s3" or not parsed.netloc or not parsed.path:
        raise ValueError(f"Invalid S3 URI: {s3_uri}")
    return parsed.netloc, parsed.path.lstrip("/")


@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> DataFrame:
    """Read synthesis JSON from S3 URIs and persist an enriched staging table."""
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    config_loader = ConfigFileLoader(config_path, config_profile)
    table_name = kwargs.get("enriched_table_name", "world_bank_project_synthesis_enriched_staging")

    if df is None or df.empty:
        print("No synthesis rows to enrich from S3.")
        return df

    s3_client = boto3.client("s3", **_resolve_aws_client_kwargs(config_loader))
    enriched = df.copy()
    if "synthesis_json" not in enriched.columns:
        enriched["synthesis_json"] = None

    for idx, row in enriched.iterrows():
        s3_uri = row.get("synthesis_s3_uri")
        if not s3_uri:
            continue
        try:
            bucket, key = _parse_s3_uri(str(s3_uri))
            obj = s3_client.get_object(Bucket=bucket, Key=key)
            enriched.at[idx, "synthesis_json"] = obj["Body"].read().decode("utf-8")
        except Exception as exc:
            print(f"Unable to enrich synthesis JSON for {s3_uri}: {exc}")

    with Postgres.with_config(config_loader) as loader:
        loader.export(
            enriched,
            "raw_data",
            table_name,
            index=False,
            if_exists="replace",
        )

    return enriched
