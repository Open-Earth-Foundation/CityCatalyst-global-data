"""Stage 6: derive mapping inputs and build the warehouse-ready flat CSV."""

from __future__ import annotations

import json

from common import MAPPING_COLUMNS, OUTPUT, REFERENCE, ROOT, as_bool, read_csv, require, write_csv
WAREHOUSE_COLUMNS = [
    "mapping_id", "action_id", "sector", "component", "risk_id", "risk_name",
    "indicator_id", "indicator_name", "eligibility", "screening_status",
    "effectiveness_class", "source_sufficiency", "time_horizon",
    "maladaptation_flag", "parameters_version", "screened_source_count",
    "evidence_record_count", "accepted_evidence_count", "assessment_basis",
    "evidence_review_status", "mapping_review_status",
]
REVIEW_COLUMNS = [
    "mapping_id", "action_id", "action_name", "action_definition", "sector",
    "component", "eligibility", "eligibility_rationale", "mapping_indicator_ids",
    "mapping_indicator_names", "indicator_evidence_coverage", "effectiveness_class",
    "source_sufficiency", "time_horizon", "maladaptation_flag", "assessment_basis",
    "screening_status", "screened_source_count", "mapping_review_status",
    "mapping_review_note", "evidence_id", "source_id", "source_title", "source_url",
    "pdf_page", "printed_page", "quote_verbatim", "evidence_grounding_status",
    "evidence_grounding_note", "evidence_indicator_ids",
    "evidence_indicator_names", "direction", "quantified_value", "support_scope",
    "maladaptation_signal", "evidence_review_status", "evidence_review_note",
]


def grouped(rows, key):
    result = {}
    for row in rows:
        result.setdefault(row[key], []).append(row)
    return result


def effectiveness(mapping, assessment_evidence):
    if mapping["eligibility"] == "not_eligible":
        return "not_applicable"
    if (mapping["eligibility"] == "review_required"
            or mapping["screening_status"] != "complete"):
        return "not_assessed"

    positive = [
        row for row in assessment_evidence if row["direction"] in {"supports", "qualifies"}
    ]
    contradicting = [row for row in assessment_evidence if row["direction"] == "contradicts"]
    if not positive:
        return "none_demonstrated"
    if any(row["support_scope"] == "whole_action" for row in contradicting):
        return "low"
    if (all(row["direction"] == "qualifies" for row in positive)
            or all(row["support_scope"] == "partial_action" for row in positive)):
        return "low"
    whole_support_sources = {
        row["source_id"] for row in positive
        if row["direction"] == "supports" and row["support_scope"] == "whole_action"
    }
    if (len(whole_support_sources) >= 2
            and not any(row["direction"] == "qualifies" for row in positive)
            and not contradicting):
        return "high"
    return "medium"


def source_sufficiency(mapping, assessment_evidence, sources):
    if mapping["eligibility"] == "not_eligible":
        return "not_applicable"
    if (mapping["eligibility"] == "review_required"
            or mapping["screening_status"] != "complete"):
        return "not_assessed"
    positive_sources = {
        row["source_id"] for row in assessment_evidence
        if row["direction"] in {"supports", "qualifies"}
    }
    if not positive_sources:
        return "none"
    has_tier_ab = any(
        sources[source_id]["source_tier"] in {"A", "B"} for source_id in positive_sources
    )
    if len(positive_sources) >= 2 and has_tier_ab:
        return "broad"
    return "moderate" if has_tier_ab else "limited"


def main() -> None:
    mappings = read_csv(OUTPUT / "mappings.csv")
    mapping_indicators = read_csv(OUTPUT / "mapping_indicators.csv")
    screening = read_csv(OUTPUT / "screening.csv")
    evidence = read_csv(OUTPUT / "evidence.csv")
    for row in evidence:
        require(
            row.get("grounding_status") in {
                "verified_exact", "verified_ordered", "layout_match",
            },
            f"Evidence has not passed grounding verification: {row['evidence_id']}",
        )
    indicators = read_csv(REFERENCE / "indicators.csv")
    sources = {row["source_id"]: row for row in read_csv(REFERENCE / "sector_sources.csv")}
    actions = {row["action_id"]: row for row in read_csv(REFERENCE / "actions.csv")}
    evidence_indicators = read_csv(OUTPUT / "evidence_indicators.csv")

    evidence_by_mapping = grouped(evidence, "mapping_id")
    screening_by_mapping = grouped(screening, "mapping_id")
    indicator_ids_by_mapping = grouped(mapping_indicators, "mapping_id")
    indicator_by_key = {
        (row["sector"], row["component"], row["indicator_id"]): row for row in indicators
    }
    evidence_indicator_ids = grouped(evidence_indicators, "evidence_id")
    basis_evidence_by_mapping = {}

    for mapping in mappings:
        evidence_rows = evidence_by_mapping.get(mapping["mapping_id"], [])
        screening_rows = screening_by_mapping.get(mapping["mapping_id"], [])
        accepted = [row for row in evidence_rows if row["review_status"] == "accepted"]
        evidence_resolved = all(row["review_status"] in {"accepted", "rejected"} for row in evidence_rows)
        screening_accepted = (
            mapping["screening_status"] == "complete"
            and bool(screening_rows)
            and all(row["review_status"] == "accepted" for row in screening_rows)
            and all(
                sources[row["source_id"]]["review_status"] == "accepted"
                for row in screening_rows
            )
        )

        if mapping["eligibility"] == "not_eligible":
            mapping["evidence_review_status"] = "not_applicable"
        elif not evidence_rows:
            if mapping["screening_status"] != "complete":
                mapping["evidence_review_status"] = "not_started"
            else:
                mapping["evidence_review_status"] = (
                    "complete" if screening_accepted else "pending"
                )
        else:
            mapping["evidence_review_status"] = "complete" if evidence_resolved else "pending"

        final_basis = screening_accepted and evidence_resolved
        assessment_evidence = (
            accepted if final_basis
            else [row for row in evidence_rows if row["review_status"] != "rejected"]
        )
        basis_evidence_by_mapping[mapping["mapping_id"]] = assessment_evidence
        if mapping["eligibility"] == "not_eligible":
            mapping["assessment_basis"] = "not_applicable"
        elif mapping["eligibility"] == "review_required":
            mapping["assessment_basis"] = "awaiting_eligibility_review"
        else:
            mapping["assessment_basis"] = (
                "accepted_evidence" if final_basis else "proposed_evidence"
            )

        mapping["effectiveness_class"] = effectiveness(mapping, assessment_evidence)
        mapping["source_sufficiency"] = source_sufficiency(
            mapping, assessment_evidence, sources
        )
        mapping["maladaptation_flag"] = str(any(
            as_bool(row["maladaptation_signal"]) for row in assessment_evidence
        )).lower()
        if (any(row["direction"] == "contradicts" for row in assessment_evidence)
                and mapping["review_status"] == "proposed"):
            mapping["review_status"] = "needs_review"
            if not mapping["review_note"]:
                mapping["review_note"] = "Contradicting evidence requires confirmation."

    write_csv(OUTPUT / "mappings.csv", MAPPING_COLUMNS, mappings)

    warehouse_rows = []
    for mapping in mappings:
        mapping_id = mapping["mapping_id"]
        links = indicator_ids_by_mapping.get(mapping_id, []) or [{"indicator_id": ""}]
        screening_rows = screening_by_mapping.get(mapping_id, [])
        evidence_rows = evidence_by_mapping.get(mapping_id, [])
        for link in links:
            indicator_id = link["indicator_id"]
            indicator = indicator_by_key.get(
                (mapping["sector"], mapping["component"], indicator_id), {}
            )
            warehouse_rows.append({
                "mapping_id": mapping_id,
                "action_id": mapping["action_id"],
                "sector": mapping["sector"],
                "component": mapping["component"],
                "risk_id": indicator.get("risk_id", ""),
                "risk_name": indicator.get("risk_name", ""),
                "indicator_id": indicator_id,
                "indicator_name": indicator.get("indicator_name", ""),
                "eligibility": mapping["eligibility"],
                "screening_status": mapping["screening_status"],
                "effectiveness_class": mapping["effectiveness_class"],
                "source_sufficiency": mapping["source_sufficiency"],
                "time_horizon": mapping["time_horizon"],
                "maladaptation_flag": mapping["maladaptation_flag"],
                "parameters_version": mapping["parameters_version"],
                "screened_source_count": len(screening_rows),
                "evidence_record_count": len(evidence_rows),
                "accepted_evidence_count": sum(
                    row["review_status"] == "accepted" for row in evidence_rows
                ),
                "assessment_basis": mapping["assessment_basis"],
                "evidence_review_status": mapping["evidence_review_status"],
                "mapping_review_status": mapping["review_status"],
            })

    review_rows = []
    for mapping in mappings:
        mapping_id = mapping["mapping_id"]
        action = actions[mapping["action_id"]]
        mapping_links = indicator_ids_by_mapping.get(mapping_id, [])
        mapping_ids = [row["indicator_id"] for row in mapping_links]
        mapping_names = [
            indicator_by_key[(mapping["sector"], mapping["component"], indicator_id)]["indicator_name"]
            for indicator_id in mapping_ids
        ]
        addressed_ids = {
            link["indicator_id"]
            for evidence_row in basis_evidence_by_mapping[mapping_id]
            for link in evidence_indicator_ids.get(evidence_row["evidence_id"], [])
        }
        missing_ids = [indicator_id for indicator_id in mapping_ids if indicator_id not in addressed_ids]
        if mapping["eligibility"] == "not_eligible":
            indicator_coverage = "not_applicable"
        elif mapping["eligibility"] == "review_required":
            indicator_coverage = "not_assessed"
        elif len(missing_ids) == len(mapping_ids):
            indicator_coverage = (
                f"none (0/{len(mapping_ids)}; missing {' | '.join(missing_ids)})"
            )
        elif missing_ids:
            indicator_coverage = (
                f"partial ({len(mapping_ids) - len(missing_ids)}/{len(mapping_ids)}; "
                f"missing {' | '.join(missing_ids)})"
            )
        else:
            indicator_coverage = f"complete ({len(mapping_ids)}/{len(mapping_ids)})"
        screening_rows = screening_by_mapping.get(mapping_id, [])
        linked_evidence = evidence_by_mapping.get(mapping_id, []) or [{}]
        for evidence_row in linked_evidence:
            source = sources.get(evidence_row.get("source_id", ""), {})
            evidence_links = evidence_indicator_ids.get(evidence_row.get("evidence_id", ""), [])
            evidence_ids = [row["indicator_id"] for row in evidence_links]
            evidence_names = [
                indicator_by_key[(mapping["sector"], mapping["component"], indicator_id)]["indicator_name"]
                for indicator_id in evidence_ids
            ]
            review_rows.append({
                "mapping_id": mapping_id,
                "action_id": mapping["action_id"],
                "action_name": action["action_name"],
                "action_definition": action["action_definition"],
                "sector": mapping["sector"],
                "component": mapping["component"],
                "eligibility": mapping["eligibility"],
                "eligibility_rationale": mapping["eligibility_rationale"],
                "mapping_indicator_ids": " | ".join(mapping_ids),
                "mapping_indicator_names": " | ".join(mapping_names),
                "indicator_evidence_coverage": indicator_coverage,
                "effectiveness_class": mapping["effectiveness_class"],
                "source_sufficiency": mapping["source_sufficiency"],
                "time_horizon": mapping["time_horizon"],
                "maladaptation_flag": mapping["maladaptation_flag"],
                "assessment_basis": mapping["assessment_basis"],
                "screening_status": mapping["screening_status"],
                "screened_source_count": len(screening_rows),
                "mapping_review_status": mapping["review_status"],
                "mapping_review_note": mapping["review_note"],
                "evidence_id": evidence_row.get("evidence_id", ""),
                "source_id": evidence_row.get("source_id", ""),
                "source_title": source.get("title", ""),
                "source_url": source.get("canonical_url", ""),
                "pdf_page": evidence_row.get("pdf_page", ""),
                "printed_page": evidence_row.get("printed_page", ""),
                "quote_verbatim": evidence_row.get("quote_verbatim", ""),
                "evidence_grounding_status": evidence_row.get("grounding_status", ""),
                "evidence_grounding_note": evidence_row.get("grounding_note", ""),
                "evidence_indicator_ids": " | ".join(evidence_ids),
                "evidence_indicator_names": " | ".join(evidence_names),
                "direction": evidence_row.get("direction", ""),
                "quantified_value": evidence_row.get("quantified_value", ""),
                "support_scope": evidence_row.get("support_scope", ""),
                "maladaptation_signal": evidence_row.get("maladaptation_signal", ""),
                "evidence_review_status": evidence_row.get("review_status", ""),
                "evidence_review_note": evidence_row.get("review_note", ""),
            })

    require(len({row["mapping_id"] for row in mappings}) == len(mappings), "Duplicate mapping ID")
    for mapping in mappings:
        count = len(indicator_ids_by_mapping.get(mapping["mapping_id"], []))
        require(mapping["eligibility"] != "eligible" or count > 0,
                f"Eligible mapping has no indicator: {mapping['mapping_id']}")
        require(mapping["eligibility"] != "not_eligible" or count == 0,
                f"Ineligible mapping has indicators: {mapping['mapping_id']}")

    output_path = OUTPUT / "action_risk_mapping.csv"
    review_path = OUTPUT / "assessment_evidence_review.csv"
    write_csv(output_path, WAREHOUSE_COLUMNS, warehouse_rows)
    write_csv(review_path, REVIEW_COLUMNS, review_rows)
    print(json.dumps({
        "warehouse_file": str(output_path.relative_to(ROOT)),
        "review_file": str(review_path.relative_to(ROOT)),
        "mappings": len(mappings),
        "warehouse_rows": len(warehouse_rows),
        "review_rows": len(review_rows),
        "status": "valid",
    }))


if __name__ == "__main__":
    main()
