"""Build a lossless, deliberately unverified seed from the reviewed v1 inventory.

This script copies source claims exactly and adds only deterministic bookkeeping.
It does not infer programme families, call status, geography, or action eligibility.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
INPUT = REPO / "dataset-review/reviews/oef/cl-city-action-fundability/releases/v1/data/chile_finance_inventory.csv"
OUTPUT = HERE / "data.csv"
SOURCES_OUTPUT = HERE / "sources.yaml"
OVERRIDES = HERE / "references/verified-record-overrides.csv"
ADDITIONS = HERE / "references/research-additions.json"
APPLICANT_MAP = HERE / "references/applicant-class-map.csv"
FUNDING_MODE_MAP = HERE / "references/funding-mode-map.csv"
ROUTE_OVERRIDES = HERE / "references/route-profile-overrides.csv"

ROUTE_SCOPE = {"sector-specific": "targeted", "broad": "general", "": "unknown"}
THEME_ALIASES = {"buildings": "stationary_energy"}
ROUTE_PROFILE_FIELDS = ("route_scope", "funds_what", "applicant_class", "municipality_eligible", "themes_norm")

SOURCE_FIELDS = [
    "source_dataset", "funder_institution", "program_name", "program_family",
    "eligible_actor", "instrument_type", "amount_clp", "amount_note", "open_date",
    "close_date", "status", "recurrence", "specificity", "climate_relevance",
    "climate_relevance_norm", "gpc_sectors", "access_pathway", "detail_level",
    "status_as_of", "source_url", "notes",
]

OUTPUT_FIELDS = [
    "record_id", "seed_row_number", "country_code", "record_scope",
    "program_family_id", "call_id", "geography_id", "source_dataset",
    "funder_institution", "program_name", "program_family", "eligible_actor",
    "instrument_type", "amount_clp", "amount_note", "open_date", "close_date",
    "status_claim", "normalized_status", "recurrence", "specificity",
    "climate_relevance", "climate_relevance_norm", "gpc_sectors", "access_pathway",
    "detail_level", "status_as_of_claim", "source_url", "notes_claim",
    "route_scope", "funds_what", "applicant_class", "municipality_eligible",
    "themes_norm",
    "verification_status", "verified_as_of", "evidence_level",
    "current_display_eligible", "reconciliation_disposition", "reconciles_to",
    "verification_notes",
]


def record_id(row: dict[str, str]) -> str:
    natural = "|".join((row["source_dataset"], row["program_name"], row["source_url"]))
    return "seed-" + hashlib.sha256(natural.encode("utf-8")).hexdigest()[:16]


def read_lookup(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    lookup = {row[key]: row for row in rows}
    if len(lookup) != len(rows):
        raise ValueError(f"Duplicate {key} in {path.name}")
    return lookup


def normalise_themes(raw: str) -> str:
    """Map the seed's sector vocabulary onto the action-sector vocabulary.

    cross_sector is preserved rather than replaced by a guessed list; resolving it
    needs primary evidence, and the gap is tracked in collection.md.
    """
    if not raw:
        return "[]"
    try:
        tags = json.loads(raw) if raw.startswith("[") else [raw]
    except json.JSONDecodeError:
        tags = [raw]
    seen: list[str] = []
    for tag in tags:
        mapped = THEME_ALIASES.get(tag, tag)
        if mapped and mapped not in seen:
            seen.append(mapped)
    return json.dumps(seen)


def route_profile(row: dict[str, str], applicants: dict, modes: dict) -> dict[str, str]:
    """Derive the four route fields from source-stated values via auditable lookups."""
    actor = applicants.get(row["eligible_actor"])
    if actor is None:
        raise ValueError(f"eligible_actor not in applicant-class-map.csv: {row['eligible_actor']!r}")
    mode = modes.get(row["instrument_type"])
    if mode is None:
        raise ValueError(f"instrument_type not in funding-mode-map.csv: {row['instrument_type']!r}")
    funds_what = mode["funds_what"]
    # An enabling platform buys readiness, whatever its nominal instrument mix says.
    if row["record_scope"] == "enabling_platform":
        funds_what = "preparation"
    return {
        "route_scope": ROUTE_SCOPE.get(row["specificity"], "unknown"),
        "funds_what": funds_what,
        "applicant_class": actor["applicant_class"],
        "municipality_eligible": actor["municipality_eligible"],
        "themes_norm": normalise_themes(row["gpc_sectors"]),
    }


def main() -> None:
    with INPUT.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 99:
        raise ValueError(f"Expected the reviewed 99-row seed, found {len(rows)}")
    if set(rows[0]) != set(SOURCE_FIELDS):
        raise ValueError("Seed columns changed; review the transformation before rebuilding")

    with OVERRIDES.open(newline="", encoding="utf-8-sig") as handle:
        override_rows = list(csv.DictReader(handle))
    overrides = {row["program_name"]: row for row in override_rows}
    if len(overrides) != len(override_rows):
        raise ValueError("Duplicate program_name in verified-record-overrides.csv")
    missing_override_targets = set(overrides) - {row["program_name"] for row in rows}
    if missing_override_targets:
        raise ValueError(f"Override targets absent from seed: {sorted(missing_override_targets)}")

    applicants = read_lookup(APPLICANT_MAP, "eligible_actor")
    modes = read_lookup(FUNDING_MODE_MAP, "instrument_type")
    with ROUTE_OVERRIDES.open(newline="", encoding="utf-8-sig") as handle:
        route_overrides: dict[str, dict[str, str]] = {}
        for entry in csv.DictReader(handle):
            if entry["field"] not in ROUTE_PROFILE_FIELDS:
                raise ValueError(f"route-profile-overrides.csv targets unknown field {entry['field']!r}")
            route_overrides.setdefault(entry["program_name"], {})[entry["field"]] = entry["value"]

    output = []
    for number, source in enumerate(rows, start=1):
        row = {
            "record_id": record_id(source),
            "seed_row_number": str(number),
            "country_code": "CL",
            "record_scope": "seed_unspecified",
            "program_family_id": "",
            "call_id": "",
            "geography_id": "",
            "source_dataset": source["source_dataset"],
            "funder_institution": source["funder_institution"],
            "program_name": source["program_name"],
            "program_family": source["program_family"],
            "eligible_actor": source["eligible_actor"],
            "instrument_type": source["instrument_type"],
            "amount_clp": source["amount_clp"],
            "amount_note": source["amount_note"],
            "open_date": source["open_date"],
            "close_date": source["close_date"],
            "status_claim": source["status"],
            "normalized_status": "",
            "recurrence": source["recurrence"],
            "specificity": source["specificity"],
            "climate_relevance": source["climate_relevance"],
            "climate_relevance_norm": source["climate_relevance_norm"],
            "gpc_sectors": source["gpc_sectors"],
            "access_pathway": source["access_pathway"],
            "detail_level": source["detail_level"],
            "status_as_of_claim": source["status_as_of"],
            "source_url": source["source_url"],
            "notes_claim": source["notes"],
            "verification_status": "seed_not_reverified",
            "verified_as_of": "",
            "evidence_level": "seed_only",
            "current_display_eligible": "false",
            "reconciliation_disposition": "carried_forward_as_seed",
            "reconciles_to": "",
            "verification_notes": "Preserved verbatim from the reviewed v1 inventory; primary source not rechecked in this compile yet.",
        }
        if source["program_name"] in overrides:
            override = overrides[source["program_name"]]
            for field in (
                "record_scope", "program_family_id", "call_id", "normalized_status",
                "verification_status", "verified_as_of", "evidence_level",
                "current_display_eligible", "reconciliation_disposition", "reconciles_to",
                "verification_notes",
            ):
                row[field] = override[field]
        # Derived after the verification override, because record_scope feeds funds_what.
        row.update(route_profile(row, applicants, modes))
        row.update(route_overrides.get(row["program_name"], {}))
        output.append(row)

    ids = [row["record_id"] for row in output]

    additions = json.loads(ADDITIONS.read_text(encoding="utf-8"))
    for addition in additions:
        unknown_fields = set(addition) - set(OUTPUT_FIELDS)
        if unknown_fields:
            raise ValueError(f"Unknown addition fields: {sorted(unknown_fields)}")
        row = {field: "" for field in OUTPUT_FIELDS}
        row.update(addition)
        row["record_id"] = "research-" + hashlib.sha256(
            "|".join((row["source_dataset"], row["program_name"], row["source_url"])).encode("utf-8")
        ).hexdigest()[:16]
        row["seed_row_number"] = ""
        row["country_code"] = "CL"
        row.update(route_profile(row, applicants, modes))
        row.update(route_overrides.get(row["program_name"], {}))
        output.append(row)

    unused = set(route_overrides) - {row["program_name"] for row in output}
    if unused:
        raise ValueError(f"route-profile-overrides.csv targets absent from data: {sorted(unused)}")

    ids = [row["record_id"] for row in output]
    if len(ids) != len(set(ids)):
        raise ValueError("Deterministic record_id collision")
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(output)

    source_registry = []
    seen_urls = set()
    for row in output:
        url = row["source_url"]
        if url in seen_urls:
            continue
        seen_urls.add(url)
        checked_rows = [candidate for candidate in output if candidate["source_url"] == url and candidate["verification_status"] != "seed_not_reverified"]
        checked = bool(checked_rows)
        source_registry.append({
            "id": "seed-url-" + hashlib.sha256(url.encode("utf-8")).hexdigest()[:12],
            "source": row["funder_institution"],
            "kind": checked_rows[0]["evidence_level"] if checked else "seed-url-unclassified",
            "url": url,
            "last_fetched": "2026-08-16" if checked else None,
            "yields": "Primary evidence for checked seed record(s)." if checked else "One or more inherited seed claims; not re-fetched in this compile yet.",
            "notes": "Checked in the first verification batch." if checked else "Registry seed only; do not treat the linked claim as reverified.",
        })

    source_registry.extend([
        {
            "id": "fpr-2026-bases",
            "source": "Ministerio del Medio Ambiente",
            "kind": "call-bases-pdf",
            "url": "https://fondos.mma.gob.cl/wp-content/uploads/2025/09/Bases_Fondo_para_el_Reciclaje_2026.pdf",
            "last_fetched": "2026-08-16",
            "yields": "Applicant types, fixed amount, co-finance, activity lines and eligible cost categories.",
            "notes": "Terms source; current usability is overridden by the later revocation linked on the call page.",
        },
        {
            "id": "sni-transport-current",
            "source": "Sistema Nacional de Inversiones",
            "kind": "official-sector-guidance",
            "url": "https://sni.gob.cl/formulacion-de-iniciativas/transporte/",
            "last_fetched": "2026-08-16",
            "yields": "Current transport-sector formulation routes, including cycleway requirements and methodology.",
            "notes": "Confirms a project-formulation route, not availability of an award or call.",
        },
        {
            "id": "dipres-2026-regional-investment-budget",
            "source": "Dirección de Presupuestos",
            "kind": "official-budget-pdf",
            "url": "https://www.dipres.gob.cl/597/articles-397464_doc_pdf.pdf",
            "last_fetched": "2026-08-16",
            "yields": "2026 regional investment budget allocations including FNDR by region.",
            "notes": "Confirms budgeted route scale; does not prove eligibility of a particular action.",
        },
        {
            "id": "dtpr-rtc-2026-processes",
            "source": "División de Transporte Público Regional",
            "kind": "regional-call-index",
            "url": "https://dtpr.mtt.gob.cl/WEBRTC/Procesos.aspx?a=2026",
            "last_fetched": "2026-08-16",
            "yields": "Region-specific 2026 Renueva tu Colectivo processes and dates.",
            "notes": "Must be extracted into regional call rows; the national seed row is not a single current call.",
        },
        {
            "id": "conaf-fcbn-2026-bases",
            "source": "Corporación Nacional Forestal",
            "kind": "call-bases-pdf",
            "url": "https://concursolbn.conaf.cl/ayuda/2026/Bases_administrativas_2026_completas.pdf",
            "last_fetched": "2026-08-16",
            "yields": "2026 call identity, applicant classes, administrative requirements and annual-call structure.",
            "notes": "The separate official call index records the extended 31 July 2026 deadline.",
        },
        {
            "id": "conaf-fcbn-2026-call-index",
            "source": "Corporación Nacional Forestal",
            "kind": "official-call-index",
            "url": "https://concursolbn.conaf.cl/login/bases.php/1000",
            "last_fetched": "2026-08-16",
            "yields": "2026 bases links and extension of applications to 31 July 2026.",
            "notes": "Establishes that the 2026 call is closed on the compile verification date.",
        },
        {
            "id": "mop-ssr-law-and-route",
            "source": "Ministerio de Obras Públicas — Servicios Sanitarios Rurales",
            "kind": "official-programme-page",
            "url": "https://ssr.mop.gob.cl/ley-20-998/",
            "last_fetched": "2026-08-16",
            "yields": "Operator role, state technical assistance and public infrastructure-investment function.",
            "notes": "Confirms a public-investment system, not an open municipal grant.",
        },
        {
            "id": "mop-2026-investment-programme",
            "source": "Ministerio de Obras Públicas",
            "kind": "official-investment-programme-pdf",
            "url": "https://planeamiento.mop.gob.cl/uploads/sites/12/2024/05/programa_anual_de_inversiones_2026-1.pdf",
            "last_fetched": "2026-08-16",
            "yields": "Named 2026 SSR investment projects, BIP identifiers, stages, regions and programmed amounts.",
            "notes": "Useful as project precedent and route evidence; not an application call catalogue.",
        },
    ])
    with SOURCES_OUTPUT.open("w", encoding="utf-8") as handle:
        json.dump({"sources": source_registry}, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(f"wrote {len(rows)} lossless seed records plus {len(additions)} researched additions to {OUTPUT}")
    print(f"wrote {len(source_registry)} registered sources to {SOURCES_OUTPUT}")


if __name__ == "__main__":
    main()
