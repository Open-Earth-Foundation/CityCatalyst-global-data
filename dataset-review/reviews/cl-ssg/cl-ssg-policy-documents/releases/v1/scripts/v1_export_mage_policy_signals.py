#!/usr/bin/env python3
"""Export validated match findings to the two Mage S3 ingestion contracts.

Produces:
  * output/action_policy_signals.csv -- action-linked evidence for
    ``cl_ssg_action_policy_signals_to_modelled``.
  * output/policy_signals.json -- generic evidence records for
    ``cl_ssg_policy_signals_to_modelled``.

Only positive findings are exported.  A ``relevance: none`` match is a useful
coverage decision but is not a policy-signal evidence row.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from v1_common import V1


CSV_FIELDS = [
    "action_id", "location_scope", "region_code", "communal_code",
    "doc_relevance", "primitive_type", "primitive_relation",
    "signal_confidence", "explicitness", "document_type", "document_name",
    "relevance_note", "evidence_text", "page",
]


def _clean(value: object) -> str:
    return "" if value is None else str(value).strip()


def _territory_codes(document: dict) -> tuple[str, str]:
    """Return two-digit region and five-digit comuna code from registry metadata."""
    region = _clean(document.get("region_code")).zfill(2)
    territory = _clean(document.get("territory_code"))
    parts = territory.split("_")
    commune = ""
    if len(parts) == 3 and parts[0] == "3" and parts[2] not in {"", "00"}:
        commune = parts[2].zfill(5)
    return region, commune


def _scope(value: object) -> str:
    scope = _clean(value).lower()
    if scope in {"communal", "commune", "city", "municipality"}:
        return "municipal"
    if scope in {"region", "regional"}:
        return "regional"
    if scope in {"country", "national"}:
        return "national"
    return scope or "unspecified"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--findings-dir", type=Path, default=V1 / "data" / "policy_action_signals")
    ap.add_argument("--registry", type=Path, default=V1 / "data" / "registry" / "source_documents.json")
    ap.add_argument("--output-dir", type=Path, default=V1 / "output")
    args = ap.parse_args()

    registry_payload = json.loads(args.registry.read_text(encoding="utf-8"))
    documents = {
        row["source_document_id"]: row
        for row in registry_payload["source_documents"]
    }

    csv_rows: list[dict[str, object]] = []
    json_rows: list[dict[str, object]] = []
    seen: set[tuple[object, ...]] = set()
    skipped_documents: set[str] = set()

    for path in sorted(args.findings_dir.glob("*/*.json")):
        finding_set = json.loads(path.read_text(encoding="utf-8"))
        doc_id = _clean(finding_set.get("source_document_id"))
        document = documents.get(doc_id)
        if not document:
            skipped_documents.add(doc_id or str(path))
            continue
        region_code, communal_code = _territory_codes(document)
        location_scope = _scope(document.get("source_level") or finding_set.get("source_level"))
        action_id = _clean(finding_set.get("action_id"))
        action_name = _clean(finding_set.get("action_name"))
        gpc_reference = _clean(finding_set.get("action_gpc_reference"))
        document_name = _clean(document.get("source_name") or finding_set.get("source_name"))
        document_type = _clean(document.get("document_type") or finding_set.get("document_type"))
        doc_relevance = _clean(finding_set.get("relevance")) or "none"

        for finding in finding_set.get("findings", []):
            evidence_text = _clean(finding.get("evidence_text"))
            page = finding.get("page") or 0
            key = (
                action_id, location_scope, region_code, communal_code, document_name,
                page, _clean(finding.get("primitive_type")),
                _clean(finding.get("primitive_relation")), evidence_text,
            )
            if not evidence_text or key in seen:
                continue
            seen.add(key)
            note = _clean(finding.get("relevance_note"))
            csv_rows.append({
                "action_id": action_id,
                "location_scope": location_scope,
                "region_code": region_code,
                "communal_code": communal_code,
                "doc_relevance": doc_relevance,
                "primitive_type": _clean(finding.get("primitive_type")),
                "primitive_relation": _clean(finding.get("primitive_relation")),
                "signal_confidence": _clean(finding.get("signal_confidence")),
                "explicitness": _clean(finding.get("explicitness")),
                "document_type": document_type,
                "document_name": document_name,
                "relevance_note": note,
                "evidence_text": evidence_text,
                "page": page,
            })
            # The generic Mage pipeline accepts a list of records (or a wrapper
            # containing ``policy_signals``) and normalises these fields.
            json_rows.append({
                "source_document_id": doc_id,
                "action_id": action_id,
                "location_scope": location_scope,
                "region_code": region_code,
                "commune_code": communal_code or None,
                "signal_type": _clean(finding.get("primitive_type")) or "unspecified",
                "signal_relation": _clean(finding.get("primitive_relation")) or "unspecified",
                "signal_strength": _clean(finding.get("signal_confidence")) or "low",
                "signal_subject": action_name or "unspecified",
                "gpc_sector": gpc_reference or None,
                "signal_summary": note or None,
                "key_numeric": None,
                "evidence_anchors": [{
                    "evidence_text": evidence_text,
                    "page": page,
                    "section": _clean(finding.get("section")) or None,
                    "explicitness": _clean(finding.get("explicitness")) or None,
                }],
            })

    csv_rows.sort(key=lambda r: tuple(str(r[field]) for field in CSV_FIELDS))
    json_rows.sort(key=lambda r: (
        str(r["action_id"]), str(r["source_document_id"]),
        str(r["evidence_anchors"][0]["page"]), str(r["evidence_anchors"][0]["evidence_text"]),
    ))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "action_policy_signals.csv"
    json_path = args.output_dir / "policy_signals.json"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(csv_rows)
    json_path.write_text(
        json.dumps({"policy_signals": json_rows}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(csv_rows)} CSV evidence rows -> {csv_path}")
    print(f"wrote {len(json_rows)} JSON policy signals -> {json_path}")
    if skipped_documents:
        print("skipped unknown registry documents: " + ", ".join(sorted(skipped_documents)))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
