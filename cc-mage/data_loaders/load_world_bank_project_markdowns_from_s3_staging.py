import os
from os import path
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


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


def _s3_bucket_key(s3_uri: str) -> tuple[str, str]:
    parsed = urlparse(s3_uri)
    if parsed.scheme != "s3" or not parsed.netloc or not parsed.path:
        raise ValueError(f"Invalid S3 URI: {s3_uri}")
    return parsed.netloc, parsed.path.lstrip("/")


def _markdown_size_bytes(s3_client, s3_uri: str) -> int | None:
    """Return ContentLength or None if object is missing."""
    bucket, key = _s3_bucket_key(s3_uri)
    try:
        resp = s3_client.head_object(Bucket=bucket, Key=key)
        return int(resp.get("ContentLength") or 0)
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code in ("404", "NoSuchKey", "NotFound"):
            return None
        raise


def _resolve_max_markdown_bytes(kwargs: dict) -> int | None:
    """Inclusive max markdown size in bytes; None means no size filter."""
    if kwargs.get("max_markdown_bytes") is not None:
        return int(kwargs["max_markdown_bytes"])
    if kwargs.get("max_markdown_kb") is not None:
        return int(float(kwargs["max_markdown_kb"]) * 1024)
    return None


def _atoms_object_exists(
    s3_client,
    bucket: str,
    destination_prefix: str,
    source_project_id: str,
    document_stem: str,
    extensions: list[str],
) -> bool:
    """Return True if any candidate atoms object exists under .../atoms/."""
    base = f"{destination_prefix}/{source_project_id}/atoms/{document_stem}_atoms"
    for ext in extensions:
        key = f"{base}.{ext}"
        try:
            s3_client.head_object(Bucket=bucket, Key=key)
            return True
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code in ("404", "NoSuchKey", "NotFound"):
                continue
            raise
    return False


@data_loader
def load_world_bank_project_markdowns_from_s3_staging(*args, **kwargs) -> DataFrame:
    """
    Build markdown S3 URIs from staged World Bank document records.

    By default, skips rows whose atom extraction output already exists in S3
    (same path convention as load_world_bank_project_markdown_atoms_to_s3).
    Set skip_if_atoms_exist=false to reprocess everything.

    Optional kwargs:
    - source_project_id — when set, restrict to that project_id.
    - max_markdown_kb or max_markdown_bytes — only enqueue markdown whose S3
      object size is at most this (inclusive). Larger files are skipped.
    """
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    table_name = kwargs.get("table_name", "world_bank_project_documents_staging")
    source_name = kwargs.get("source_name", "world_bank")
    country_code = kwargs.get("country_code")
    destination_bucket = kwargs.get("destination_bucket", "test-global-api")
    destination_prefix = kwargs.get(
        "destination_prefix",
        "raw_data/world_bank/world_bank_projects/documents",
    ).strip("/")
    source_project_id = kwargs.get("source_project_id")
    skip_if_atoms_exist = bool(kwargs.get("skip_if_atoms_exist", True))
    atoms_file_extension = str(kwargs.get("atoms_file_extension", "jsonl")).strip(".").lower()
    if not atoms_file_extension:
        atoms_file_extension = "jsonl"
    check_legacy_ndjson = bool(kwargs.get("check_legacy_ndjson", True))
    atoms_extensions = [atoms_file_extension]
    if check_legacy_ndjson and atoms_file_extension == "jsonl" and "ndjson" not in atoms_extensions:
        atoms_extensions.append("ndjson")

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
      COALESCE(document_id::TEXT, '') AS document_id,
      COALESCE(document_type::TEXT, 'unknown') AS doc_type,
      s3_uri::TEXT AS pdf_s3_uri
    FROM raw_data.{table_name}
    WHERE project_id IS NOT NULL
      AND s3_uri IS NOT NULL
      {source_filter}
      {country_filter}
      {project_filter}
    ORDER BY project_id, document_id
    """

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        df = loader.load(query)

    if df.empty:
        print("No staged World Bank PDFs found for markdown atom extraction.")
        return DataFrame(
            columns=[
                "source_project_id",
                "document_id",
                "doc_type",
                "pdf_s3_uri",
                "markdown_s3_uri",
                "document_stem",
            ]
        )

    def _document_stem(row) -> str:
        doc_id = str(row["document_id"]).strip()
        if doc_id:
            return doc_id
        parsed = urlparse(str(row["pdf_s3_uri"]))
        pdf_name = parsed.path.rsplit("/", 1)[-1]
        return pdf_name.rsplit(".", 1)[0]

    def _build_markdown_uri(row) -> str:
        document_stem = row["document_stem"]
        return (
            f"s3://{destination_bucket}/"
            f"{destination_prefix}/{row['source_project_id']}/{document_stem}.md"
        )

    df["document_stem"] = df.apply(_document_stem, axis=1)
    df["markdown_s3_uri"] = df.apply(_build_markdown_uri, axis=1)

    max_markdown_bytes = _resolve_max_markdown_bytes(kwargs)
    config_loader = ConfigFileLoader(config_path, config_profile)
    need_s3 = bool(skip_if_atoms_exist or max_markdown_bytes is not None)
    s3_client = None
    if need_s3 and not df.empty:
        s3_client = boto3.client("s3", **_resolve_aws_client_kwargs(config_loader))

    if max_markdown_bytes is not None and s3_client is not None:
        before = len(df)
        skipped_missing = 0
        skipped_large = 0
        keep_idx: list[int] = []
        for idx, row in df.iterrows():
            uri = str(row["markdown_s3_uri"])
            size = _markdown_size_bytes(s3_client, uri)
            if size is None:
                skipped_missing += 1
                print(f"Skip (markdown not in S3): {uri}")
                continue
            if size > max_markdown_bytes:
                skipped_large += 1
                stem = str(row.get("document_stem", ""))
                print(
                    f"Skip (markdown {size} bytes > max {max_markdown_bytes}): "
                    f"{row.get('source_project_id')}/{stem}"
                )
                continue
            keep_idx.append(idx)
        df = df.loc[keep_idx].reset_index(drop=True) if keep_idx else df.iloc[0:0].copy()
        print(
            f"Markdown size filter (<={max_markdown_bytes} bytes): "
            f"skipped_large={skipped_large}, missing={skipped_missing}, "
            f"kept={len(df)} (of {before})."
        )

    initial_count = len(df)
    if skip_if_atoms_exist and not df.empty:
        if s3_client is None:
            s3_client = boto3.client("s3", **_resolve_aws_client_kwargs(config_loader))

        def _needs_processing(row) -> bool:
            return not _atoms_object_exists(
                s3_client,
                destination_bucket,
                destination_prefix,
                str(row["source_project_id"]).strip(),
                str(row["document_stem"]).strip(),
                atoms_extensions,
            )

        mask = df.apply(_needs_processing, axis=1)
        skipped = int((~mask).sum())
        df = df[mask].reset_index(drop=True)
        print(
            f"Skip existing atoms: {skipped} already processed, "
            f"{len(df)} pending (of {initial_count} staged)."
        )
    elif not df.empty:
        print(f"Loaded {len(df)} markdown candidates from raw_data.{table_name}.")

    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
