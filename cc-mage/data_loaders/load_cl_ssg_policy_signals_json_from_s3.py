import json
from os import path
from typing import Any

import boto3
from mage_ai.io.config import ConfigFileLoader
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


def _resolve_aws_client_kwargs(config_loader: ConfigFileLoader) -> dict:
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

    kwargs = {"region_name": region_name}
    if aws_access_key_id and aws_secret_access_key:
        kwargs["aws_access_key_id"] = aws_access_key_id
        kwargs["aws_secret_access_key"] = aws_secret_access_key
    if aws_session_token:
        kwargs["aws_session_token"] = aws_session_token
    return kwargs


def _extract_records(payload: Any) -> list[dict]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("policy_signals", "signals", "items", "data", "rows"):
            value = payload.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
        return [payload]
    return []


@data_loader
def load_cl_ssg_policy_signals_json_from_s3(*args, **kwargs) -> DataFrame:
    config_path = path.join(get_repo_path(), "io_config.yaml")
    source_bucket = str(kwargs.get("source_bucket", "test-global-api")).strip()
    policy_signals_key = str(
        kwargs.get(
            "policy_signals_key",
            "raw_data/cl-ssg/cl-ssg-policy-documents/releases/2026/synthesis/policy_signals.json",
        )
    ).strip("/")

    config_loader = ConfigFileLoader(config_path, "default")
    s3_client = boto3.client("s3", **_resolve_aws_client_kwargs(config_loader))
    response = s3_client.get_object(Bucket=source_bucket, Key=policy_signals_key)
    payload = json.loads(response["Body"].read().decode("utf-8"))
    records = _extract_records(payload)

    df = DataFrame(records)
    print(f"Loaded {len(df)} policy signal records from s3://{source_bucket}/{policy_signals_key}")
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
