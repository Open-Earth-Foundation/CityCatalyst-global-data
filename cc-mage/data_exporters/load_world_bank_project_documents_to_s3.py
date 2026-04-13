from io import BytesIO
from os import path
import os

import boto3
import requests
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


def _session() -> requests.Session:
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=1.2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _resolve_aws_client_kwargs(config_loader: ConfigFileLoader) -> dict:
    """
    Resolve AWS credentials from Mage io_config loader and env vars.
    """
    config_dict = {}
    if hasattr(config_loader, "config") and isinstance(config_loader.config, dict):
        config_dict = config_loader.config
    elif hasattr(config_loader, "settings") and isinstance(config_loader.settings, dict):
        config_dict = config_loader.settings

    aws_access_key_id = (
        config_dict.get("AWS_ACCESS_KEY_ID")
        or os.getenv("AWS_ACCESS_KEY_ID")
    )
    aws_secret_access_key = (
        config_dict.get("AWS_SECRET_ACCESS_KEY")
        or os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    aws_session_token = (
        config_dict.get("AWS_SESSION_TOKEN")
        or os.getenv("AWS_SESSION_TOKEN")
    )
    region_name = config_dict.get("AWS_REGION") or os.getenv("AWS_REGION") or "us-east-1"

    kwargs = {"region_name": region_name}
    if aws_access_key_id and aws_secret_access_key:
        kwargs["aws_access_key_id"] = aws_access_key_id
        kwargs["aws_secret_access_key"] = aws_secret_access_key
    if aws_session_token:
        kwargs["aws_session_token"] = aws_session_token
    return kwargs


@data_exporter
def export_data_to_s3(df: DataFrame, **kwargs) -> DataFrame:
    """
    Download PDFs from pdf_url and upload to S3 using s3_object_key.
    """
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    bucket_name = kwargs.get("s3_bucket", "test-global-api")
    timeout_seconds = int(kwargs.get("download_timeout_seconds", 90))
    table_name = kwargs.get("table_name", "world_bank_project_documents_staging")
    country_code = kwargs.get("country_code")
    session = _session()

    # Keep this block simple and stable: always read from staging table.
    country_filter = ""
    if country_code:
        safe_country_code = str(country_code).replace("'", "").strip().upper()
        country_filter = f"AND UPPER(country_code) = '{safe_country_code}'"
    query = f"""
    SELECT
      project_id,
      document_id AS doc_id,
      document_type AS doc_type,
      s3_object_key AS s3_pdf_key,
      source_name AS funder,
      source_document_url AS source_url,
      pdf_url,
      s3_object_key
    FROM raw_data.{table_name}
    WHERE pdf_url IS NOT NULL
      AND s3_object_key IS NOT NULL
      {country_filter}
    """
    config_loader = ConfigFileLoader(config_path, config_profile)
    with Postgres.with_config(config_loader) as loader:
        df = loader.load(query)
    print(f"Loaded {len(df)} rows from raw_data.{table_name} for S3 upload.")

    if df.empty:
        print("No rows available for S3 upload after fallback query.")
        return DataFrame(
            columns=[
                "project_id",
                "doc_id",
                "doc_type",
                "s3_pdf_key",
                "funder",
                "source_url",
                "pdf_url",
                "s3_object_key",
            ]
        )

    uploaded = 0
    failed = 0

    s3_client = boto3.client("s3", **_resolve_aws_client_kwargs(config_loader))
    for _, row in df.iterrows():
        pdf_url = row.get("pdf_url")
        object_key = row.get("s3_object_key")

        if not pdf_url or not object_key:
            failed += 1
            continue

        try:
            response = session.get(pdf_url, timeout=timeout_seconds)
            response.raise_for_status()
            file_bytes = BytesIO(response.content)
            s3_client.upload_fileobj(
                Fileobj=file_bytes,
                Bucket=bucket_name,
                Key=object_key,
                ExtraArgs={"ContentType": "application/pdf"},
            )
            uploaded += 1
        except Exception as exc:
            failed += 1
            print(f"Failed to upload {pdf_url} -> s3://{bucket_name}/{object_key}: {exc}")

    print(
        f"World Bank document upload complete: uploaded={uploaded}, failed={failed}, "
        f"total={len(df)}"
    )
    return df
