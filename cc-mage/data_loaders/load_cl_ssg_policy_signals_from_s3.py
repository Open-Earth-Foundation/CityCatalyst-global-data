import json
from os import path
from typing import Any

import boto3
import pandas as pd
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


def _read_json_from_s3(s3_client, bucket: str, key: str) -> Any:
    response = s3_client.get_object(Bucket=bucket, Key=key)
    body = response["Body"].read().decode("utf-8")
    return json.loads(body)


def _read_csv_from_s3(s3_client, bucket: str, key: str) -> DataFrame:
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(response["Body"], dtype=str).fillna("")


def _string_value(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _safe_json(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            return json.loads(text)
        except Exception:
            return {"value": text}
    if isinstance(value, (int, float, bool)):
        return value
    return {"value": str(value)}


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


def _build_location_maps(local_codes_df: DataFrame) -> dict[str, dict[str, tuple[str, str, str, str]]]:
    maps = {
        "region_code": {},
        "province_code": {},
        "commune_code_2018": {},
        "region_name": {},
        "province_name": {},
        "commune_name": {},
    }

    for _, row in local_codes_df.iterrows():
        region_code = row["region_code"].strip()
        province_code = row["province_code"].strip()
        commune_code = row["commune_code_2018"].strip()
        region_name = row["region_name"].strip()
        province_name = row["province_name"].strip()
        commune_name = row["commune_name"].strip()

        maps["region_code"][region_code] = (region_code, region_name, "region", region_code)
        maps["province_code"][province_code] = (province_code, province_name, "province", region_code)
        maps["commune_code_2018"][commune_code] = (commune_code, commune_name, "commune", region_code)
        maps["region_name"][region_name.lower()] = (region_code, region_name, "region", region_code)
        maps["province_name"][province_name.lower()] = (province_code, province_name, "province", region_code)
        maps["commune_name"][commune_name.lower()] = (commune_code, commune_name, "commune", region_code)

    return maps


def _resolve_location(
    record: dict, location_maps: dict[str, dict[str, tuple[str, str, str, str]]]
) -> tuple[str | None, str, str, str | None]:
    location_scope = _string_value(record.get("location_scope") or record.get("scale"))
    location_code = _string_value(
        record.get("location_code")
        or record.get("region_code")
        or record.get("province_code")
        or record.get("commune_code_2018")
        or record.get("commune_code")
    )
    location_name = _string_value(
        record.get("location_name")
        or record.get("location")
        or record.get("territory_name")
        or record.get("jurisdiction_name")
    )

    territory_code = _string_value(record.get("territory_code") or record.get("territory_id"))
    if territory_code and not location_code:
        parts = [segment.strip("_") for segment in territory_code.split("_")]
        if len(parts) == 3:
            scale = parts[0]
            region = parts[1]
            commune = parts[2]
            if scale == "1":
                location_scope = location_scope or "national"
                location_name = location_name or "Chile"
                location_code = None
            elif scale == "2" and region not in ("", "00"):
                location_code = region
                location_scope = location_scope or "region"
            elif scale == "3" and commune not in ("", "00"):
                location_code = commune
                location_scope = location_scope or "commune"

    if location_code:
        location_code = location_code.lstrip("_")
        for key in ("commune_code_2018", "province_code", "region_code"):
            matched = location_maps[key].get(location_code)
            if matched:
                code, name, inferred_scope = matched
                return code, location_name or name, location_scope or inferred_scope, region_code

    if location_name:
        lookup_key = location_name.lower()
        for key in ("commune_name", "province_name", "region_name"):
            matched = location_maps[key].get(lookup_key)
            if matched:
                code, name, inferred_scope = matched
                return code, name, location_scope or inferred_scope, region_code

    if (location_scope or "").lower() in ("national", "country"):
        return "CL", location_name or "Chile", "national", None

    return location_code, location_name or "Unknown", location_scope or "unspecified", None


def _normalize_record(
    record: dict, location_maps: dict[str, dict[str, tuple[str, str, str, str]]]
) -> dict[str, Any]:
    location_code, location_name, location_scope, region_code = _resolve_location(record, location_maps)
    scope_normalized = (location_scope or "").strip().lower()

    if scope_normalized in ("national", "country"):
        location_code = "CL"
    elif scope_normalized == "region":
        if location_code:
            location_code = f"CL{str(location_code).zfill(2)}"
    elif scope_normalized in ("commune", "comuna"):
        # Export step resolves city locode from modelled.city_polygon.
        location_code = None

    signal_type = _string_value(record.get("signal_type") or record.get("type")) or "unspecified"
    signal_relation = (
        _string_value(record.get("signal_relation") or record.get("relation") or record.get("operator"))
        or "unspecified"
    )
    signal_subject = (
        _string_value(record.get("signal_subject") or record.get("subject") or record.get("title"))
        or "unspecified"
    )

    return {
        "location_code": location_code,
        "location_name": location_name,
        "location_scope": location_scope,
        "signal_type": signal_type,
        "signal_relation": signal_relation,
        "signal_strength": _string_value(record.get("signal_strength") or record.get("strength")),
        "signal_subject": signal_subject,
        "gpc_sector": _string_value(record.get("gpc_sector") or record.get("gpc_reference_number")),
        "signal_summary": _string_value(record.get("signal_summary") or record.get("summary")),
        "key_numeric": _safe_json(record.get("key_numeric") or record.get("numeric_values")),
        "evidence_anchors": _safe_json(
            record.get("evidence_anchors") or record.get("evidence") or record.get("anchors")
        ),
        "_region_code": region_code,
    }


@data_loader
def load_cl_ssg_policy_signals_from_s3(*args, **kwargs) -> DataFrame:
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    source_bucket = str(kwargs.get("source_bucket", "test-global-api")).strip()
    policy_signals_key = str(
        kwargs.get(
            "policy_signals_key",
            "raw_data/cl-ssg/cl-ssg-policy-documents/releases/2026/synthesis/policy_signals.json",
        )
    ).strip("/")
    local_codes_key = str(
        kwargs.get(
            "local_codes_key",
            "raw_data/cl-ssg/cl-ssg-policy-documents/releases/2026/local_codes.csv",
        )
    ).strip("/")

    config_loader = ConfigFileLoader(config_path, config_profile)
    s3_client = boto3.client("s3", **_resolve_aws_client_kwargs(config_loader))

    payload = _read_json_from_s3(s3_client, source_bucket, policy_signals_key)
    local_codes_df = _read_csv_from_s3(s3_client, source_bucket, local_codes_key)
    location_maps = _build_location_maps(local_codes_df)

    records = _extract_records(payload)
    normalized = [_normalize_record(record, location_maps) for record in records]
    df = DataFrame(normalized)

    print(
        "Loaded "
        f"{len(df)} policy signals from s3://{source_bucket}/{policy_signals_key} "
        f"with location map s3://{source_bucket}/{local_codes_key}."
    )
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
