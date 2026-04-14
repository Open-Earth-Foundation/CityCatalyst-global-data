import os
from os import path
from urllib.parse import urlparse

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
    document_stem: str,
    extensions: list[str],
) -> bool:
    """Return True if any candidate atoms object exists under .../atoms/."""
    base = f"{destination_prefix}/atoms/{document_stem}_atoms"
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
def load_cl_ssg_policy_markdowns_from_s3(*args, **kwargs) -> DataFrame:
    """
    List policy markdown documents in S3 and build extraction input rows.

    Required prefixes:
    - source_prefix: markdown folder, e.g. raw_data/.../releases/2026/markdown
    - source_pdf_prefix: sibling PDF folder, e.g. raw_data/.../releases/2026

    Optional behavior:
    - skip_if_atoms_exist=true skips markdowns that already have atoms objects.
    - max_markdown_kb or max_markdown_bytes caps markdown size before enqueueing.
    """
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    source_bucket = str(kwargs.get("source_bucket", "test-global-api")).strip()
    source_prefix = str(
        kwargs.get(
            "source_prefix",
            "raw_data/cl-ssg/cl-ssg-policy-documents/releases/2026/markdown",
        )
    ).strip("/")
    source_pdf_prefix = str(
        kwargs.get(
            "source_pdf_prefix",
            "raw_data/cl-ssg/cl-ssg-policy-documents/releases/2026",
        )
    ).strip("/")
    destination_bucket = str(kwargs.get("destination_bucket", "test-global-api")).strip()
    destination_prefix = str(
        kwargs.get(
            "destination_prefix",
            "raw_data/cl-ssg/cl-ssg-policy-documents/releases/2026/markdown",
        )
    ).strip("/")
    skip_if_atoms_exist = bool(kwargs.get("skip_if_atoms_exist", True))
    atoms_file_extension = str(kwargs.get("atoms_file_extension", "jsonl")).strip(".").lower()
    if not atoms_file_extension:
        atoms_file_extension = "jsonl"
    check_legacy_ndjson = bool(kwargs.get("check_legacy_ndjson", True))
    atoms_extensions = [atoms_file_extension]
    if check_legacy_ndjson and atoms_file_extension == "jsonl" and "ndjson" not in atoms_extensions:
        atoms_extensions.append("ndjson")

    if not source_bucket or not source_prefix:
        print("Missing source_bucket or source_prefix; returning empty frame.")
        return DataFrame(columns=["document_stem", "markdown_s3_uri", "pdf_s3_uri"])

    config_loader = ConfigFileLoader(config_path, config_profile)
    s3_client = boto3.client("s3", **_resolve_aws_client_kwargs(config_loader))

    rows: list[dict[str, str]] = []
    paginator = s3_client.get_paginator("list_objects_v2")
    for page_data in paginator.paginate(Bucket=source_bucket, Prefix=f"{source_prefix}/"):
        for obj in page_data.get("Contents") or []:
            key = (obj.get("Key") or "").strip()
            if not key or key.endswith("/") or not key.lower().endswith(".md"):
                continue
            stem = key.rsplit("/", 1)[-1][:-3]
            if not stem:
                continue
            rows.append(
                {
                    "document_stem": stem,
                    "markdown_s3_uri": f"s3://{source_bucket}/{key}",
                    "pdf_s3_uri": f"s3://{source_bucket}/{source_pdf_prefix}/{stem}.pdf",
                }
            )

    df = DataFrame(rows)
    if df.empty:
        print(f"No markdown files found under s3://{source_bucket}/{source_prefix}/")
        return DataFrame(columns=["document_stem", "markdown_s3_uri", "pdf_s3_uri"])

    max_markdown_bytes = _resolve_max_markdown_bytes(kwargs)
    if max_markdown_bytes is not None:
        before = len(df)
        keep_idx: list[int] = []
        skipped_missing = 0
        skipped_large = 0
        for idx, row in df.iterrows():
            uri = str(row["markdown_s3_uri"])
            size = _markdown_size_bytes(s3_client, uri)
            if size is None:
                skipped_missing += 1
                continue
            if size > max_markdown_bytes:
                skipped_large += 1
                continue
            keep_idx.append(idx)
        df = df.loc[keep_idx].reset_index(drop=True) if keep_idx else df.iloc[0:0].copy()
        print(
            f"Markdown size filter (<={max_markdown_bytes} bytes): "
            f"skipped_large={skipped_large}, missing={skipped_missing}, kept={len(df)} (of {before})."
        )

    initial_count = len(df)
    if skip_if_atoms_exist and not df.empty:
        def _needs_processing(row) -> bool:
            return not _atoms_object_exists(
                s3_client,
                destination_bucket,
                destination_prefix,
                str(row["document_stem"]).strip(),
                atoms_extensions,
            )

        mask = df.apply(_needs_processing, axis=1)
        skipped = int((~mask).sum())
        df = df[mask].reset_index(drop=True)
        print(
            f"Skip existing atoms: {skipped} already processed, "
            f"{len(df)} pending (of {initial_count} markdown files)."
        )

    df = df.sort_values("document_stem").reset_index(drop=True)
    print(f"Loaded {len(df)} policy markdown candidates from s3://{source_bucket}/{source_prefix}/")
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
