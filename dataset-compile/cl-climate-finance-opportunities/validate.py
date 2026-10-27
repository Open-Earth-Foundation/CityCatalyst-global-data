"""Structural and no-loss checks for the Chile opportunity compile."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SEED = REPO / "dataset-review/reviews/oef/cl-city-action-fundability/releases/v1/data/chile_finance_inventory.csv"
DATA = HERE / "data.csv"

COPY_MAP = {
    "source_dataset": "source_dataset", "funder_institution": "funder_institution",
    "program_name": "program_name", "program_family": "program_family",
    "eligible_actor": "eligible_actor", "instrument_type": "instrument_type",
    "amount_clp": "amount_clp", "amount_note": "amount_note", "open_date": "open_date",
    "close_date": "close_date", "status": "status_claim", "recurrence": "recurrence",
    "specificity": "specificity", "climate_relevance": "climate_relevance",
    "climate_relevance_norm": "climate_relevance_norm", "gpc_sectors": "gpc_sectors",
    "access_pathway": "access_pathway", "detail_level": "detail_level",
    "status_as_of": "status_as_of_claim", "source_url": "source_url", "notes": "notes_claim",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    seed = read_csv(SEED)
    data = read_csv(DATA)
    schema = json.loads((HERE / "schema.json").read_text(encoding="utf-8"))
    sources = json.loads((HERE / "sources.yaml").read_text(encoding="utf-8"))["sources"]

    assert len(seed) == 99, f"reviewed seed changed: {len(seed)} rows"
    assert len(data) >= len(seed), "seed rows were lost"
    assert len({row["record_id"] for row in data}) == len(data), "duplicate record_id"
    assert [field["name"] for field in schema["fields"]] == list(data[0]), "schema/data field drift"

    for index, (before, after) in enumerate(zip(seed, data[:len(seed)], strict=True), start=1):
        assert after["seed_row_number"] == str(index), f"seed ordering drift at row {index}"
        for seed_field, compiled_field in COPY_MAP.items():
            assert before[seed_field] == after[compiled_field], (
                f"seed claim changed at row {index}: {seed_field} -> {compiled_field}"
            )

    for addition in data[len(seed):]:
        assert addition["seed_row_number"] == "", "research addition has a seed row number"
        assert addition["reconciliation_disposition"] == "newly_discovered", (
            "post-seed record is not explicitly identified as newly discovered"
        )
        assert addition["verification_status"] != "seed_not_reverified", (
            "new discovery lacks primary-source verification"
        )

    registered_urls = {source["url"] for source in sources}
    assert all(row["source_url"] in registered_urls for row in data), "data source URL absent from sources.yaml"
    assert len({source["id"] for source in sources}) == len(sources), "duplicate source registry id"
    assert all(row["current_display_eligible"] == "false" for row in data), (
        "display eligibility must remain false until the downstream rule is documented and reviewed"
    )
    assert all(
        row["normalized_status"] == "" for row in data
        if row["verification_status"] == "seed_not_reverified"
    ), "unverified seed row received a normalized status"

    # Route profile: controlled vocabularies, complete lookups, nothing inferred.
    applicants = read_csv(HERE / "references/applicant-class-map.csv")
    modes = read_csv(HERE / "references/funding-mode-map.csv")
    applicant_by_actor = {row["eligible_actor"]: row for row in applicants}
    mode_by_instrument = {row["instrument_type"]: row for row in modes}

    assert len(applicant_by_actor) == len(applicants), "duplicate eligible_actor in applicant-class-map.csv"
    assert len(mode_by_instrument) == len(modes), "duplicate instrument_type in funding-mode-map.csv"
    assert {row["eligible_actor"] for row in data} <= set(applicant_by_actor), "eligible_actor missing from the applicant lookup"
    assert {row["instrument_type"] for row in data} <= set(mode_by_instrument), "instrument_type missing from the funding-mode lookup"
    assert not set(applicant_by_actor) - {row["eligible_actor"] for row in data}, "applicant lookup carries rows no record uses"
    assert not set(mode_by_instrument) - {row["instrument_type"] for row in data}, "funding-mode lookup carries rows no record uses"

    vocabularies = {
        "route_scope": {"targeted", "general", "unknown"},
        "funds_what": {"asset", "equipment", "practice", "preparation", "credit", "unknown"},
        "applicant_class": {"municipality", "public_agency", "community_org", "indigenous_community", "producer", "firm", "operator", "household", "research", "unknown"},
        "municipality_eligible": {"yes", "no", "implementer", "unknown"},
    }
    for field, allowed in vocabularies.items():
        found = {row[field] for row in data}
        assert found <= allowed, f"{field} outside its controlled vocabulary: {sorted(found - allowed)}"

    for row in data:
        actor = applicant_by_actor[row["eligible_actor"]]
        assert row["applicant_class"] == actor["applicant_class"], f"applicant_class drifted from the lookup: {row['program_name']}"
        assert row["municipality_eligible"] == actor["municipality_eligible"], f"municipality_eligible drifted from the lookup: {row['program_name']}"
        # An unrecorded applicant must never acquire a class, and never a city-eligibility answer.
        if row["eligible_actor"] == "unspecified":
            assert row["applicant_class"] == "unknown", f"invented an applicant class: {row['program_name']}"
            assert row["municipality_eligible"] == "unknown", f"invented city eligibility: {row['program_name']}"
        themes = json.loads(row["themes_norm"])
        assert isinstance(themes, list), f"themes_norm is not a list: {row['program_name']}"
        assert "buildings" not in themes, f"themes_norm kept an unmapped alias: {row['program_name']}"
        assert len(themes) == len(set(themes)), f"duplicate theme: {row['program_name']}"
        if row["record_scope"] == "enabling_platform":
            assert row["funds_what"] == "preparation", f"enabling platform must fund preparation: {row['program_name']}"

    dispositions = Counter(row["reconciliation_disposition"] for row in data)
    assert sum(dispositions.values()) == len(data), "reconciliation does not account for every compiled row"
    print(json.dumps({
        "seed_rows": len(seed),
        "compiled_rows": len(data),
        "newly_discovered_rows": len(data) - len(seed),
        "unique_record_ids": len({row["record_id"] for row in data}),
        "registered_sources": len(sources),
        "reverified_records": sum(row["verification_status"] != "seed_not_reverified" for row in data),
        "display_eligible_records": sum(row["current_display_eligible"] == "true" for row in data),
        "reconciliation": dispositions,
    }, default=dict, indent=2))


if __name__ == "__main__":
    main()
