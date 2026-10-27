"""Map pipeline CSV columns to action_policy_signals staging shape."""
from __future__ import annotations

import math

from pandas import DataFrame

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer

RELATION_ALIASES = {
    "action": "commits",
    "target": "targets",
    "monitor": "monitors",
    "monitoring": "monitors",
    "risk": "identifies",
}
ALLOWED_MATCH_TYPES = {"direct", "indirect", "contextual"}


def _clean(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    text = str(value).strip().strip('"')
    if text.lower() in {"", "nan", "none"}:
        return ""
    return text


def _territory_code(value: object, width: int) -> str:
    """Normalize INE region/comuna codes; repair float coercion (3304.0 → 03304)."""
    text = _clean(value)
    if not text:
        return ""
    if "." in text:
        try:
            text = str(int(float(text)))
        except ValueError:
            pass
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        try:
            text = str(int(value))
        except (ValueError, OverflowError):
            pass
    return text.zfill(width)


def _normalize_relation(value: object) -> str:
    key = _clean(value).lower()
    return RELATION_ALIASES.get(key, key or "unspecified")


def _normalize_match_type(value: object) -> str:
    key = _clean(value).lower()
    return key if key in ALLOWED_MATCH_TYPES else ""


def _lookup_tables(
    city_locodes_df: DataFrame,
) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    region_names: dict[str, str] = {}
    comuna_names: dict[str, str] = {}
    comuna_locodes: dict[str, str] = {}
    for _, row in city_locodes_df.iterrows():
        region_code = _territory_code(row.get("region_code"), 2)
        comuna_code = _territory_code(row.get("comuna_code"), 5)
        region_name = _clean(row.get("region_name"))
        comuna_name = _clean(row.get("comuna_name"))
        locode = _clean(row.get("locode"))
        if region_code and region_name and region_code not in region_names:
            region_names[region_code] = region_name
        if comuna_code and comuna_name:
            comuna_names[comuna_code] = comuna_name
        if comuna_code and locode:
            comuna_locodes[comuna_code] = locode
    return region_names, comuna_names, comuna_locodes


def _resolve_location(
    row: dict,
    region_names: dict[str, str],
    comuna_names: dict[str, str],
    comuna_locodes: dict[str, str],
) -> tuple[str, str, str]:
    scope = _clean(row.get("location_scope")).lower()
    region_code = _territory_code(row.get("region_code"), 2)
    comuna_code = _territory_code(row.get("communal_code"), 5)

    if scope == "national":
        return "national", "CL", "Chile"
    if scope == "regional":
        name = region_names.get(region_code, f"Región {region_code}")
        return "regional", region_code, name
    if scope == "municipal":
        name = comuna_names.get(comuna_code, "")
        locode = comuna_locodes.get(comuna_code, "")
        if locode:
            return "municipal", locode, name or locode
        if comuna_code:
            return "municipal", comuna_code, name or f"Comuna {comuna_code}"
    return scope or "unspecified", region_code or comuna_code or "CL", "Chile"


@transformer
def transform_action_policy_signals_for_staging(
    signals_df: DataFrame,
    city_locodes_df: DataFrame,
    *args,
    **kwargs,
) -> DataFrame:
    region_names, comuna_names, comuna_locodes = _lookup_tables(city_locodes_df)
    rows: list[dict[str, object]] = []
    municipal_with_locode = 0
    municipal_comuna_only = 0

    for _, row in signals_df.iterrows():
        evidence_text = _clean(row.get("evidence_text"))
        if len(evidence_text) <= 30:
            continue

        location_scope, location_code, location_name = _resolve_location(
            row.to_dict(), region_names, comuna_names, comuna_locodes
        )
        if location_scope == "municipal":
            comuna_code = _territory_code(row.get("communal_code"), 5)
            if location_code == comuna_locodes.get(comuna_code, ""):
                municipal_with_locode += 1
            else:
                municipal_comuna_only += 1

        page_raw = _clean(row.get("page"))
        page = int(float(page_raw)) if page_raw else 0

        rows.append(
            {
                "src_action_id": _clean(row.get("action_id")),
                "location_scope": location_scope,
                "location_code": location_code,
                "location_name": location_name,
                "signal_type": _clean(row.get("primitive_type")) or "unspecified",
                "signal_relation": _normalize_relation(row.get("primitive_relation")),
                "signal_strength": _clean(row.get("signal_confidence")) or "low",
                "explicitness": _clean(row.get("explicitness")) or "explicit",
                "document_type": _clean(row.get("document_type")),
                "document_name": _clean(row.get("document_name")),
                "doc_relevance": _clean(row.get("doc_relevance")) or "none",
                "signal_summary": _clean(row.get("relevance_note")),
                "evidence_text": evidence_text,
                "match_type": _normalize_match_type(row.get("match_type")),
                "match_reason": _clean(row.get("subject_match_reason"))
                or _clean(row.get("match_reason")),
                "page": page,
            }
        )

    out = DataFrame(rows)
    if municipal_with_locode or municipal_comuna_only:
        print(
            f"Municipal rows: {municipal_with_locode} with locode, "
            f"{municipal_comuna_only} with comuna code only (add locodes to city_locodes.csv)."
        )
    print(f"Prepared {len(out)} action policy signal rows for staging.")
    return out
