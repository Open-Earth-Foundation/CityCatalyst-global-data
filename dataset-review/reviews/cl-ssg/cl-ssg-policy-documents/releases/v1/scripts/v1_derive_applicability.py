#!/usr/bin/env python3
"""Phase 3: derive the (city, source_document) applicability registry.

Reads:
  - releases/v1/data/registry/source_documents.json
  - releases/v1/data/registry/local_codes.csv

Writes:
  - releases/v1/data/registry/city_applicable_policies.csv
  - releases/v1/data/registry/city_applicable_policies.derivation.json  (run log)

Rules (matches releases/v1/design/scoring_rubric.md, version 0.1.0):

  national       -> applies to every commune in local_codes.csv
  regional       -> applies to every commune whose region_code matches the
                    document's region_code
  intercommunal  -> v0 fallback: if region_code != "00", applies to every
                    commune in that region. If region_code == "00", the doc is
                    skipped with a warning (registry needs an intercommunal
                    comuna list to handle these cleanly).
  municipal      -> applies to the single commune whose code matches the
                    commune segment of the doc's territory_code (3_RR_CCCCC).

Placeholder documents are always excluded.
Low-priority documents (PRAS environmental_program) are excluded unless
--include-low-priority is passed.

Usage:
  python v1_derive_applicability.py
  python v1_derive_applicability.py --include-low-priority
  python v1_derive_applicability.py \
      --registry  /path/to/source_documents.json \
      --codes     /path/to/local_codes.csv \
      --output    /path/to/city_applicable_policies.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

RUBRIC_VERSION = "0.1.0"

# ----------------------------------------------------------------------------
# Default paths (relative to this file)
# ----------------------------------------------------------------------------

V1_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = V1_ROOT.parents[1]

DEFAULT_REGISTRY = V1_ROOT / "data" / "registry" / "source_documents.json"
DEFAULT_CODES = V1_ROOT / "data" / "registry" / "local_codes.csv"
DEFAULT_OUTPUT = V1_ROOT / "data" / "registry" / "city_applicable_policies.csv"
DEFAULT_DERIVATION_LOG = V1_ROOT / "data" / "registry" / "city_applicable_policies.derivation.json"

# ----------------------------------------------------------------------------
# Weight tables (mirror scoring_rubric.md v0.1.0)
# ----------------------------------------------------------------------------

PROXIMITY_BASE: dict[tuple[str, str], float] = {
    ("municipal",     "paccc"):                 1.00,
    ("communal",      "paccc"):                 1.00,
    ("municipal",     "environmental_program"): 1.00,
    ("communal",      "environmental_program"): 1.00,
    ("intercommunal", "territorial_plan"):      0.85,
    ("regional",      "parcc"):                 0.70,
    ("regional",      "territorial_plan"):      0.55,
    ("national",      "sector_plan"):           0.50,
    ("national",      "framework"):             0.30,
    ("national",      "territorial_plan"):      0.25,
}

# Document-specific overrides on top of the (source_level, document_type) table.
PROXIMITY_DOC_OVERRIDE: dict[str, float] = {
    "chl_eclp_2021": 0.35,   # long-term strategy is stronger than NDC framing
}

STATUS_MULTIPLIER: dict[str, float] = {
    "final":           1.00,
    "draft":           0.70,
    "consultation":    0.70,
    "portal_only":     0.70,
    "flipbook_only":   0.70,
    # placeholder -> excluded entirely (handled in caller)
}

# Low-priority documents to exclude by default. Currently the four PRAS
# environmental-program docs, by source_document_id prefix.
LOW_PRIORITY_PREFIXES = ("chl_environmental_program_",)


def is_low_priority(doc: dict) -> bool:
    sid = doc.get("source_document_id", "")
    return doc.get("review_priority") == "low" or any(
        sid.startswith(pref) for pref in LOW_PRIORITY_PREFIXES
    )


# ----------------------------------------------------------------------------
# Applicability rules
# ----------------------------------------------------------------------------

def applicability_type_for(doc: dict) -> str:
    level = doc.get("source_level")
    dtype = doc.get("document_type", "")
    if level == "national":
        if dtype == "sector_plan":
            return "national_sector"
        if dtype == "territorial_plan":
            return "national_territorial"
        return "national_framework"
    if level == "regional":
        if dtype == "territorial_plan":
            return "regional_territorial"
        return "regional"
    if level == "intercommunal":
        return "intercommunal"
    if level in ("municipal", "communal"):
        if dtype == "environmental_program":
            return "direct"
        return "communal"
    return "unknown"


def proximity_weight_base_for(doc: dict) -> float:
    sid = doc.get("source_document_id", "")
    if sid in PROXIMITY_DOC_OVERRIDE:
        return PROXIMITY_DOC_OVERRIDE[sid]
    key = (doc.get("source_level", ""), doc.get("document_type", ""))
    return PROXIMITY_BASE.get(key, 0.0)


def status_multiplier_for(doc: dict) -> float:
    return STATUS_MULTIPLIER.get(doc.get("document_status", ""), 0.0)


def commune_code_from_territory(territory_code: str) -> str | None:
    """territory_code looks like '3_RR_CCCCC' for municipal docs.
    Returns the commune code (5 digits) or None if it can't be parsed.
    """
    if not territory_code:
        return None
    parts = territory_code.split("_")
    if len(parts) != 3:
        return None
    candidate = parts[2]
    if len(candidate) == 5 and candidate.isdigit():
        return candidate
    return None


# ----------------------------------------------------------------------------
# Load inputs
# ----------------------------------------------------------------------------

def load_source_documents(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return list(data.get("source_documents", []))


def load_local_codes(path: Path) -> list[dict]:
    """Return list of commune dicts with keys: city_code, region_code, city_name."""
    out: list[dict] = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            city_code = (row.get("commune_code_2018") or "").strip()
            region_code = (row.get("region_code") or "").strip()
            city_name = (row.get("commune_name") or "").strip()
            if not city_code or not region_code:
                continue
            out.append({
                "city_code": city_code,
                "region_code": region_code,
                "city_name": city_name,
            })
    return out


# ----------------------------------------------------------------------------
# Core derivation
# ----------------------------------------------------------------------------

def derive_rows(
    documents: list[dict],
    cities: list[dict],
    include_low_priority: bool,
    keep_drafts: bool,
) -> tuple[list[dict], dict]:
    """Return (rows, derivation_log).

    rows: list of dicts ready to write to CSV.
    derivation_log: dict summarising the run (counts, skipped docs, warnings).
    """
    rows: list[dict] = []
    warnings: list[str] = []
    skipped: list[dict] = []

    docs_by_region: dict[str, list[dict]] = defaultdict(list)
    for city in cities:
        docs_by_region[city["region_code"]].append(city)
    cities_by_code: dict[str, dict] = {c["city_code"]: c for c in cities}

    for doc in documents:
        sid = doc["source_document_id"]
        status = doc.get("document_status", "")

        if status == "placeholder":
            skipped.append({"source_document_id": sid, "reason": "placeholder"})
            continue
        if not keep_drafts and status in {"draft", "consultation"}:
            # We still include drafts by default with a 0.7 multiplier; this
            # branch only triggers when the caller explicitly suppresses them.
            skipped.append({"source_document_id": sid, "reason": f"status={status} suppressed"})
            continue
        if is_low_priority(doc) and not include_low_priority:
            skipped.append({"source_document_id": sid, "reason": "review_priority=low"})
            continue

        level = doc.get("source_level")
        app_type = applicability_type_for(doc)
        weight_base = proximity_weight_base_for(doc)
        status_mult = status_multiplier_for(doc)
        weight = round(weight_base * status_mult, 4)

        common = {
            "source_document_id": sid,
            "source_level": level,
            "document_type": doc.get("document_type", ""),
            "document_status": status,
            "applicability_type": app_type,
            "proximity_weight_base": weight_base,
            "status_multiplier": status_mult,
            "proximity_weight": weight,
            "review_priority": doc.get("review_priority", ""),
            "rubric_version": RUBRIC_VERSION,
        }

        if weight_base == 0.0:
            warnings.append(
                f"{sid}: no proximity_weight_base for (level={level}, "
                f"document_type={doc.get('document_type','')}); rows will be "
                f"emitted with weight 0"
            )

        if level == "national":
            reason = f"national-scope document ({doc.get('document_type','')}) applies to all cities"
            for city in cities:
                rows.append({
                    **common,
                    "city_code": city["city_code"],
                    "region_code": city["region_code"],
                    "city_name": city["city_name"],
                    "applicability_reason": reason,
                })

        elif level == "regional":
            region = doc.get("region_code", "")
            if region in {"", "00"}:
                warnings.append(
                    f"{sid}: regional doc has region_code={region!r}; skipped"
                )
                skipped.append({"source_document_id": sid, "reason": f"regional doc missing region_code (got {region!r})"})
                continue
            cohort = docs_by_region.get(region, [])
            if not cohort:
                warnings.append(f"{sid}: no cities found for region_code={region}")
            reason = f"regional document for region {region}"
            for city in cohort:
                rows.append({
                    **common,
                    "city_code": city["city_code"],
                    "region_code": city["region_code"],
                    "city_name": city["city_name"],
                    "applicability_reason": reason,
                })

        elif level == "intercommunal":
            region = doc.get("region_code", "")
            if region in {"", "00"}:
                warnings.append(
                    f"{sid}: intercommunal doc has region_code={region!r}; "
                    f"v0 fallback cannot resolve scope (needs intercommunal_comunas in registry). Skipped."
                )
                skipped.append({"source_document_id": sid, "reason": "intercommunal scope unresolved"})
                continue
            cohort = docs_by_region.get(region, [])
            reason = f"intercommunal document (v0 fallback: all cities in region {region})"
            for city in cohort:
                rows.append({
                    **common,
                    "city_code": city["city_code"],
                    "region_code": city["region_code"],
                    "city_name": city["city_name"],
                    "applicability_reason": reason,
                })

        elif level in {"municipal", "communal"}:
            cc = commune_code_from_territory(doc.get("territory_code", ""))
            if not cc:
                warnings.append(
                    f"{sid}: municipal doc has unparseable territory_code "
                    f"{doc.get('territory_code','')!r}; skipped"
                )
                skipped.append({"source_document_id": sid, "reason": "municipal territory_code unparseable"})
                continue
            city = cities_by_code.get(cc)
            if not city:
                warnings.append(
                    f"{sid}: municipal doc references commune code {cc} not "
                    f"present in local_codes.csv; skipped"
                )
                skipped.append({"source_document_id": sid, "reason": f"commune {cc} not in local_codes"})
                continue
            reason = f"municipal document for commune {cc} ({city['city_name']})"
            rows.append({
                **common,
                "city_code": city["city_code"],
                "region_code": city["region_code"],
                "city_name": city["city_name"],
                "applicability_reason": reason,
            })

        else:
            warnings.append(f"{sid}: unknown source_level {level!r}; skipped")
            skipped.append({"source_document_id": sid, "reason": f"unknown source_level {level!r}"})

    derivation_log = {
        "rubric_version": RUBRIC_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_documents": len(documents),
        "input_cities": len(cities),
        "include_low_priority": include_low_priority,
        "keep_drafts": keep_drafts,
        "output_rows": len(rows),
        "skipped_documents": skipped,
        "warnings": warnings,
        "rows_by_applicability_type": dict(Counter(r["applicability_type"] for r in rows)),
        "rows_by_status": dict(Counter(r["document_status"] for r in rows)),
        "distinct_cities": len({r["city_code"] for r in rows}),
        "distinct_documents": len({r["source_document_id"] for r in rows}),
    }
    return rows, derivation_log


# ----------------------------------------------------------------------------
# Write outputs
# ----------------------------------------------------------------------------

CSV_COLUMNS = [
    "city_code",
    "region_code",
    "city_name",
    "source_document_id",
    "source_level",
    "document_type",
    "document_status",
    "applicability_type",
    "proximity_weight_base",
    "status_multiplier",
    "proximity_weight",
    "applicability_reason",
    "review_priority",
    "rubric_version",
]


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows_sorted = sorted(
        rows,
        key=lambda r: (r["city_code"], -float(r["proximity_weight"]), r["source_document_id"]),
    )
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for r in rows_sorted:
            writer.writerow({k: r.get(k, "") for k in CSV_COLUMNS})


def write_log(log: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Derive city x source_document applicability registry for v2")
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY,
                    help=f"path to source_documents.json (default: {DEFAULT_REGISTRY})")
    ap.add_argument("--codes", type=Path, default=DEFAULT_CODES,
                    help=f"path to local_codes.csv (default: {DEFAULT_CODES})")
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                    help=f"path to write city_applicable_policies.csv (default: {DEFAULT_OUTPUT})")
    ap.add_argument("--log", type=Path, default=DEFAULT_DERIVATION_LOG,
                    help=f"path to write derivation log JSON (default: {DEFAULT_DERIVATION_LOG})")
    ap.add_argument("--include-low-priority", action="store_true",
                    help="Include review_priority=low docs (e.g. PRAS environmental programs).")
    ap.add_argument("--drop-drafts", action="store_true",
                    help="Suppress draft and consultation docs entirely instead of applying the 0.7 status multiplier.")
    args = ap.parse_args()

    documents = load_source_documents(args.registry)
    cities = load_local_codes(args.codes)

    rows, log = derive_rows(
        documents=documents,
        cities=cities,
        include_low_priority=args.include_low_priority,
        keep_drafts=not args.drop_drafts,
    )

    write_csv(rows, args.output)
    write_log(log, args.log)

    # Summary to stderr
    print(f"wrote {args.output}  rows={log['output_rows']}", file=sys.stderr)
    print(f"  distinct_cities={log['distinct_cities']} distinct_documents={log['distinct_documents']}", file=sys.stderr)
    print(f"  by applicability_type: {log['rows_by_applicability_type']}", file=sys.stderr)
    if log["skipped_documents"]:
        print(f"  skipped {len(log['skipped_documents'])} documents:", file=sys.stderr)
        for s in log["skipped_documents"]:
            print(f"    - {s['source_document_id']}: {s['reason']}", file=sys.stderr)
    if log["warnings"]:
        print(f"  {len(log['warnings'])} warnings:", file=sys.stderr)
        for w in log["warnings"]:
            print(f"    - {w}", file=sys.stderr)
    print(f"derivation log: {args.log}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
