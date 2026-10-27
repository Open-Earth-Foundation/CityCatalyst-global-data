import json
from typing import Any

from pandas import DataFrame

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


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
        region_code = str(row["region_code"]).strip()
        province_code = str(row["province_code"]).strip()
        commune_code = str(row["commune_code_2018"]).strip()
        region_name = str(row["region_name"]).strip()
        province_name = str(row["province_name"]).strip()
        commune_name = str(row["commune_name"]).strip()

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
            if parts[0] == "1":
                location_scope = location_scope or "national"
                location_name = location_name or "Chile"
            elif parts[0] == "2" and parts[1] not in ("", "00"):
                location_scope = location_scope or "region"
                location_code = parts[1]
            elif parts[0] == "3" and parts[2] not in ("", "00"):
                location_scope = location_scope or "commune"
                location_code = parts[2]

    if location_code:
        location_code = location_code.lstrip("_")
        for key in ("commune_code_2018", "province_code", "region_code"):
            matched = location_maps[key].get(location_code)
            if matched:
                code, name, inferred_scope, region_code = matched
                return code, location_name or name, location_scope or inferred_scope, region_code

    if location_name:
        lookup_key = location_name.lower()
        for key in ("commune_name", "province_name", "region_name"):
            matched = location_maps[key].get(lookup_key)
            if matched:
                code, name, inferred_scope, region_code = matched
                return code, name, location_scope or inferred_scope, region_code

    if (location_scope or "").lower() in ("national", "country"):
        return "CL", location_name or "Chile", "national", None

    return location_code, location_name or "Unknown", location_scope or "unspecified", None


def _normalize_scope(value: str | None) -> str:
    scope = (value or "").strip().lower()
    if scope in ("national", "country"):
        return "national"
    if scope in ("region", "regional"):
        return "region"
    if scope in ("commune", "comuna", "communal", "city", "municipal", "municipality"):
        return "commune"
    return scope or "unspecified"


@transformer
def transform(policy_signals_df: DataFrame, local_codes_df: DataFrame, *args, **kwargs) -> DataFrame:
    location_maps = _build_location_maps(local_codes_df)
    rows: list[dict[str, Any]] = []

    for _, source_row in policy_signals_df.iterrows():
        record = source_row.to_dict()
        location_code, location_name, location_scope, region_code = _resolve_location(record, location_maps)
        scope_normalized = _normalize_scope(location_scope)
        location_scope = scope_normalized

        if scope_normalized == "national":
            location_code = "CL"
        elif scope_normalized == "region":
            region_for_code = (region_code or "").strip()
            if region_for_code:
                location_code = f"CL{region_for_code.zfill(2)}"
            elif location_code:
                location_code = f"CL{str(location_code).zfill(2)}"
        elif scope_normalized == "commune":
            location_code = None

        rows.append(
            {
                "location_code": location_code,
                "location_name": location_name,
                "location_scope": location_scope,
                "signal_type": _string_value(record.get("signal_type") or record.get("type")) or "unspecified",
                "signal_relation": _string_value(
                    record.get("signal_relation") or record.get("relation") or record.get("operator")
                )
                or "unspecified",
                "signal_strength": _string_value(record.get("signal_strength") or record.get("strength")),
                "signal_subject": _string_value(record.get("signal_subject") or record.get("subject") or record.get("title"))
                or "unspecified",
                "gpc_sector": _string_value(record.get("gpc_sector") or record.get("gpc_reference_number")),
                "signal_summary": _string_value(record.get("signal_summary") or record.get("summary")),
                "key_numeric": _safe_json(record.get("key_numeric") or record.get("numeric_values")),
                "evidence_anchors": _safe_json(
                    record.get("evidence_anchors") or record.get("evidence") or record.get("anchors")
                ),
                "_region_code": region_code,
            }
        )

    output = DataFrame(rows)
    print(f"Transformed {len(output)} policy signal rows with location normalization.")
    return output


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
