from io import BytesIO
from os import path
import os
from urllib.parse import urlparse

import boto3
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
    aws_secret_access_key = config_dict.get("AWS_SECRET_ACCESS_KEY") or os.getenv("AWS_SECRET_ACCESS_KEY")
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
    """Split an S3 URI into bucket and object key."""
    parsed = urlparse(s3_uri)
    if parsed.scheme != "s3" or not parsed.netloc or not parsed.path:
        raise ValueError(f"Invalid S3 URI: {s3_uri}")
    return parsed.netloc, parsed.path.lstrip("/")


def _pdf_to_markdown(pdf_bytes: bytes, title: str) -> str:
    """Extract plain text from each PDF page with page_break markers."""
    reader = PdfReader(BytesIO(pdf_bytes))
    sections: list[str] = [f"# {title}"]
    for idx, page in enumerate(reader.pages, start=1):
        page_text = (page.extract_text() or "").strip()
        normalized = "\n".join(line.rstrip() for line in page_text.splitlines()) if page_text else ""
        if normalized:
            sections.append(f"<!-- page_break: {idx} -->\n\n{normalized}")
        else:
            # Preserve page sequence even when text extraction yields empty content.
            sections.append(f"<!-- page_break: {idx} -->")
    return "\n\n".join(sections).strip() + "\n"


@data_exporter
def export_data_to_s3(df: DataFrame, **kwargs) -> DataFrame:
    """
    Convert PDF files listed in `s3_uri` into Markdown and upload them to S3.
    """
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    destination_bucket = kwargs.get("destination_bucket", "test-global-api")
    destination_prefix = kwargs.get(
        "destination_prefix",
        "raw_data/world_bank/world_bank_projects/documents",
    ).strip("/")

    if df is None or df.empty:
        print("No documents available for markdown conversion.")
        return DataFrame(columns=["source_project_id", "s3_uri", "markdown_s3_uri", "status"])

    config_loader = ConfigFileLoader(config_path, config_profile)
    s3_client = boto3.client("s3", **_resolve_aws_client_kwargs(config_loader))
    output_rows = []
    converted = 0
    failed = 0

    for _, row in df.iterrows():
        source_project_id = str(row.get("source_project_id", "")).strip()
        s3_uri = row.get("s3_uri")
        markdown_s3_uri = None
        status = "failed"

        if not source_project_id or not s3_uri:
            failed += 1
            output_rows.append(
                {
                    "source_project_id": source_project_id,
                    "s3_uri": s3_uri,
                    "markdown_s3_uri": markdown_s3_uri,
                    "status": "missing_input",
                }
            )
            continue

        try:
            source_bucket, source_key = _parse_s3_uri(s3_uri)
            object_name = source_key.rsplit("/", 1)[-1]
            document_stem = object_name.rsplit(".", 1)[0]
            markdown_key = f"{destination_prefix}/{source_project_id}/{document_stem}.md"

            source_obj = s3_client.get_object(Bucket=source_bucket, Key=source_key)
            pdf_bytes = source_obj["Body"].read()
            markdown_body = _pdf_to_markdown(pdf_bytes, title=document_stem)

            s3_client.put_object(
                Bucket=destination_bucket,
                Key=markdown_key,
                Body=markdown_body.encode("utf-8"),
                ContentType="text/markdown",
            )
            markdown_s3_uri = f"s3://{destination_bucket}/{markdown_key}"
            status = "converted"
            converted += 1
        except Exception as exc:
            failed += 1
            print(
                f"Failed to convert source_project_id={source_project_id} "
                f"s3_uri={s3_uri}: {exc}"
            )

        output_rows.append(
            {
                "source_project_id": source_project_id,
                "s3_uri": s3_uri,
                "markdown_s3_uri": markdown_s3_uri,
                "status": status,
            }
        )

    print(
        "World Bank markdown conversion complete: "
        f"converted={converted}, failed={failed}, total={len(df)}"
    )
    return DataFrame(output_rows)
