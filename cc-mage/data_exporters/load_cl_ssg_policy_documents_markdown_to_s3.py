from io import BytesIO
from os import path
import os
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError
from mage_ai.io.config import ConfigFileLoader
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame
from pypdf import PdfReader

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


def _resolve_aws_client_kwargs(config_loader: ConfigFileLoader) -> dict:
    """Build boto3 client kwargs from io_config and environment variables."""
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


def _parse_s3_uri(s3_uri: str) -> tuple[str, str]:
    """Split an S3 URI into bucket and object key."""
    parsed = urlparse(s3_uri)
    if parsed.scheme != "s3" or not parsed.netloc or not parsed.path:
        raise ValueError(f"Invalid S3 URI: {s3_uri}")
    return parsed.netloc, parsed.path.lstrip("/")


def _pdf_to_markdown(pdf_bytes: bytes, title: str) -> str:
    """Extract plain text from each PDF page with page_break markers (same as World Bank pipeline)."""
    reader = PdfReader(BytesIO(pdf_bytes))
    sections: list[str] = [f"# {title}"]
    for idx, page in enumerate(reader.pages, start=1):
        page_text = (page.extract_text() or "").strip()
        normalized = "\n".join(line.rstrip() for line in page_text.splitlines()) if page_text else ""
        if normalized:
            sections.append(f"<!-- page_break: {idx} -->\n\n{normalized}")
        else:
            sections.append(f"<!-- page_break: {idx} -->")
    return "\n\n".join(sections).strip() + "\n"


def _markdown_exists(s3_client, bucket: str, key: str) -> bool:
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") in ("404", "NoSuchKey", "NotFound"):
            return False
        raise


@data_exporter
def export_data_to_s3(df: DataFrame, **kwargs) -> DataFrame:
    """
    Download each PDF from s3_uri, convert to Markdown (pypdf text extraction), upload to S3.

    Input columns: document_stem, s3_uri

    Output columns: document_stem, s3_uri, markdown_s3_uri, status

    Kwargs:
      - destination_bucket — default test-global-api
      - destination_prefix — e.g. raw_data/cl-ssg/cl-ssg-policy-documents/releases/2026/markdown
      - skip_if_markdown_exists — if true, skip upload when destination .md already exists
    """
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    destination_bucket = str(kwargs.get("destination_bucket", "test-global-api")).strip()
    destination_prefix = str(
        kwargs.get(
            "destination_prefix",
            "raw_data/cl-ssg/cl-ssg-policy-documents/releases/2026/markdown",
        )
    ).strip().strip("/")
    skip_if_markdown_exists = bool(kwargs.get("skip_if_markdown_exists", True))

    if df is None or df.empty:
        print("No PDF rows to convert to markdown.")
        return DataFrame(columns=["document_stem", "s3_uri", "markdown_s3_uri", "status"])

    config_loader = ConfigFileLoader(config_path, config_profile)
    s3_client = boto3.client("s3", **_resolve_aws_client_kwargs(config_loader))
    output_rows: list[dict] = []
    converted = 0
    failed = 0
    skipped = 0

    for _, row in df.iterrows():
        document_stem = str(row.get("document_stem", "")).strip()
        s3_uri = row.get("s3_uri")
        markdown_s3_uri = None
        status = "failed"

        if not document_stem or not s3_uri:
            failed += 1
            output_rows.append(
                {
                    "document_stem": document_stem,
                    "s3_uri": s3_uri,
                    "markdown_s3_uri": markdown_s3_uri,
                    "status": "missing_input",
                }
            )
            continue

        markdown_key = f"{destination_prefix}/{document_stem}.md"

        try:
            if skip_if_markdown_exists and _markdown_exists(
                s3_client, destination_bucket, markdown_key
            ):
                markdown_s3_uri = f"s3://{destination_bucket}/{markdown_key}"
                status = "skipped_exists"
                skipped += 1
                output_rows.append(
                    {
                        "document_stem": document_stem,
                        "s3_uri": s3_uri,
                        "markdown_s3_uri": markdown_s3_uri,
                        "status": status,
                    }
                )
                continue

            source_bucket, source_key = _parse_s3_uri(str(s3_uri))
            source_obj = s3_client.get_object(Bucket=source_bucket, Key=source_key)
            pdf_bytes = source_obj["Body"].read()
            markdown_body = _pdf_to_markdown(pdf_bytes, title=document_stem)

            s3_client.put_object(
                Bucket=destination_bucket,
                Key=markdown_key,
                Body=markdown_body.encode("utf-8"),
                ContentType="text/markdown; charset=utf-8",
            )
            markdown_s3_uri = f"s3://{destination_bucket}/{markdown_key}"
            status = "converted"
            converted += 1
        except Exception as exc:
            failed += 1
            print(f"Failed document_stem={document_stem} s3_uri={s3_uri}: {exc}")

        output_rows.append(
            {
                "document_stem": document_stem,
                "s3_uri": s3_uri,
                "markdown_s3_uri": markdown_s3_uri,
                "status": status,
            }
        )

    print(
        "cl-ssg policy documents markdown: "
        f"converted={converted}, skipped={skipped}, failed={failed}, total={len(df)}"
    )
    return DataFrame(output_rows)
