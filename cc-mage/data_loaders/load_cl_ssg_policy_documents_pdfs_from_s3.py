from os import path

import boto3
from botocore.exceptions import ClientError
from mage_ai.io.config import ConfigFileLoader
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


def _resolve_aws_client_kwargs(config_loader: ConfigFileLoader) -> dict:
    """Build boto3 client kwargs from io_config and environment variables."""
    import os

    config_dict = {}
    if hasattr(config_loader, "config") and isinstance(config_loader.config, dict):
        config_dict = config_loader.config
    elif hasattr(config_loader, "settings") and isinstance(config_loader.settings, dict):
        config_dict = config_loader.settings

    aws_access_key_id = config_dict.get("AWS_ACCESS_KEY_ID") or os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = config_dict.get("AWS_SECRET_ACCESS_KEY") or os.getenv(
        "AWS_SECRET_ACCESS_KEY"
    )
    aws_session_token = config_dict.get("AWS_SESSION_TOKEN") or os.getenv("AWS_SESSION_TOKEN")
    region_name = config_dict.get("AWS_REGION") or os.getenv("AWS_REGION") or "us-east-1"

    kwargs: dict = {"region_name": region_name}
    if aws_access_key_id and aws_secret_access_key:
        kwargs["aws_access_key_id"] = aws_access_key_id
        kwargs["aws_secret_access_key"] = aws_secret_access_key
    if aws_session_token:
        kwargs["aws_session_token"] = aws_session_token
    return kwargs


@data_loader
def load_cl_ssg_policy_documents_pdfs_from_s3(*args, **kwargs) -> DataFrame:
    """
    List PDF object keys under an S3 prefix for cl-ssg-policy-documents (raw_data).

    Returns one row per PDF:
      - document_stem — filename without .pdf (used for output markdown basename)
      - s3_uri — full s3:// URI for the source PDF

    Pipeline variables / kwargs:
      - source_bucket — default test-global-api
      - source_prefix — e.g. raw_data/cl-ssg/cl-ssg-policy-documents/releases/2026
        (no leading slash; trailing slash optional)
    """
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    source_bucket = str(kwargs.get("source_bucket", "test-global-api")).strip()
    source_prefix = str(
        kwargs.get(
            "source_prefix",
            "raw_data/cl-ssg/cl-ssg-policy-documents/releases/2026",
        )
    ).strip().strip("/")

    if not source_bucket or not source_prefix:
        print("Missing source_bucket or source_prefix; returning empty frame.")
        return DataFrame(columns=["document_stem", "s3_uri"])

    config_loader = ConfigFileLoader(config_path, config_profile)
    s3_client = boto3.client("s3", **_resolve_aws_client_kwargs(config_loader))

    prefix = f"{source_prefix}/"
    paginator = s3_client.get_paginator("list_objects_v2")
    rows: list[dict[str, str]] = []

    try:
        for page in paginator.paginate(Bucket=source_bucket, Prefix=prefix):
            for obj in page.get("Contents") or []:
                key = obj.get("Key") or ""
                if not key or key.endswith("/"):
                    continue
                lower = key.lower()
                if not lower.endswith(".pdf"):
                    continue
                base = key.rsplit("/", 1)[-1]
                if not base.lower().endswith(".pdf"):
                    continue
                stem = base[: -len(".pdf")]
                if not stem:
                    continue
                rows.append(
                    {
                        "document_stem": stem,
                        "s3_uri": f"s3://{source_bucket}/{key}",
                    }
                )
    except ClientError as exc:
        print(f"S3 list failed for s3://{source_bucket}/{prefix}: {exc}")
        return DataFrame(columns=["document_stem", "s3_uri"])

    rows.sort(key=lambda r: r["document_stem"])
    df = DataFrame(rows)
    print(f"Listed {len(df)} PDFs under s3://{source_bucket}/{prefix}")
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
