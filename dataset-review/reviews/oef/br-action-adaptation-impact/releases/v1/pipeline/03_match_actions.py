"""Stage 3: validate action-to-indicator proposals and build mapping tables."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import (
    INPUT, MAPPING_COLUMNS, OUTPUT, REFERENCE, ROOT, SCREENING_COLUMNS,
    read_csv, require, split_ids, stable_id, write_csv,
)


MAPPING_INDICATORS = ["mapping_id", "indicator_id"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(INPUT / "mapping_proposals.csv"))
    parser.add_argument("--run-id", default="all_sector_mapping")
    args = parser.parse_args()

    proposal_path = Path(args.input)
    proposals = read_csv(proposal_path if proposal_path.is_absolute() else ROOT / proposal_path)
    actions = {row["action_id"]: row for row in read_csv(REFERENCE / "actions.csv")}
    indicator_rows = read_csv(REFERENCE / "indicators.csv")
    indicators = {
        (row["sector"], row["component"], row["indicator_id"])
        for row in indicator_rows
    }
    proposal_keys = [
        (row["action_id"], row["sector"], row["component"])
        for row in proposals
    ]
    expected_keys = {
        (action_id, sector, component)
        for action_id in actions
        for sector in {row["sector"] for row in indicator_rows}
        for component in {"vulnerability", "exposure"}
    }
    require(len(proposal_keys) == len(set(proposal_keys)),
            "Duplicate action-sector-component in mapping proposals")
    require(set(proposal_keys) == expected_keys,
            "Mapping proposals do not cover the complete action-sector-component matrix")
    sources = {row["source_id"]: row for row in read_csv(REFERENCE / "sector_sources.csv")}
    screenable_sources = {}
    for source in sources.values():
        if source["review_status"] != "rejected" and source["access_status"] == "retrieved":
            screenable_sources.setdefault(source["sector"], set()).add(source["source_id"])
    parameters = json.loads((ROOT / "schemas" / "score_parameters.json").read_text())

    mappings = []
    mapping_indicators = []
    screening = []
    for proposal in proposals:
        action_id = proposal["action_id"]
        require(action_id in actions, f"Unknown action: {action_id}")
        mapping_id = stable_id("map", action_id, proposal["sector"], proposal["component"])
        indicator_ids = split_ids(proposal["indicator_ids"])
        source_ids = split_ids(proposal["screened_source_ids"])
        eligibility = proposal["proposed_eligibility"]

        require(eligibility in {"eligible", "not_eligible", "review_required"},
                f"Invalid eligibility: {mapping_id}")
        require(eligibility != "eligible" or indicator_ids,
                f"Eligible mapping has no indicator: {mapping_id}")
        require(eligibility != "not_eligible" or not indicator_ids,
                f"Ineligible mapping has indicators: {mapping_id}")
        require(
            proposal["screening_status"] in {"not_started", "complete", "not_required"},
            f"Invalid screening status: {mapping_id}",
        )
        if eligibility == "not_eligible":
            require(proposal["screening_status"] == "not_required" and not source_ids,
                    f"Ineligible mapping must not have screening: {mapping_id}")
        elif eligibility == "review_required":
            require(proposal["screening_status"] != "complete" and not source_ids,
                    f"Unresolved mapping must not have completed screening: {mapping_id}")
        elif proposal["screening_status"] == "complete":
            expected_sources = screenable_sources.get(proposal["sector"], set())
            require(expected_sources,
                    f"Complete screening requires retrieved sector sources: {mapping_id}")
            require(
                set(source_ids) == expected_sources,
                f"Complete screening does not cover the retrieved sector sources: {mapping_id}",
            )
        else:
            require(not source_ids,
                    f"Incomplete screening must not list screened sources: {mapping_id}")

        for indicator_id in indicator_ids:
            require((proposal["sector"], proposal["component"], indicator_id) in indicators,
                    f"Invalid indicator {indicator_id}: {mapping_id}")
            mapping_indicators.append({"mapping_id": mapping_id, "indicator_id": indicator_id})
        for source_id in source_ids:
            source = sources.get(source_id)
            require(source and source["sector"] == proposal["sector"],
                    f"Invalid screened source {source_id}: {mapping_id}")
            require(source["access_status"] == "retrieved"
                    and source["review_status"] != "rejected",
                    f"Screened source is not available for proposed assessment: {source_id}")
            screening.append({
                "mapping_id": mapping_id,
                "source_id": source_id,
                "screening_status": "screened",
                "evidence_record_count": "0",
                "review_status": "proposed",
                "reviewed_by": "", "reviewed_at": "", "review_note": "",
            })

        not_applicable = eligibility == "not_eligible"
        mappings.append({
            "mapping_id": mapping_id,
            "action_id": action_id,
            "sector": proposal["sector"],
            "component": proposal["component"],
            "eligibility": eligibility,
            "eligibility_rationale": proposal["eligibility_rationale"],
            "screening_status": proposal["screening_status"],
            "effectiveness_class": "not_applicable" if not_applicable else "not_assessed",
            "source_sufficiency": "not_applicable" if not_applicable else "not_assessed",
            "time_horizon": actions[action_id]["time_horizon"] or "unknown",
            "maladaptation_flag": "false",
            "parameters_version": parameters["parameters_version"],
            "evidence_review_status": "not_applicable" if not_applicable else "not_started",
            "match_run_id": args.run_id,
            "assessment_basis": "not_applicable" if not_applicable else "not_assessed",
            "review_status": proposal["review_status"],
            "reviewed_by": proposal["reviewed_by"],
            "reviewed_at": proposal["reviewed_at"],
            "review_note": proposal["review_note"],
        })

    write_csv(OUTPUT / "mappings.csv", MAPPING_COLUMNS, mappings)
    write_csv(OUTPUT / "mapping_indicators.csv", MAPPING_INDICATORS, mapping_indicators)
    write_csv(OUTPUT / "screening.csv", SCREENING_COLUMNS, screening)
    print(json.dumps({
        "mappings": len(mappings),
        "mapping_indicators": len(mapping_indicators),
        "screening_records": len(screening),
    }))


if __name__ == "__main__":
    main()
