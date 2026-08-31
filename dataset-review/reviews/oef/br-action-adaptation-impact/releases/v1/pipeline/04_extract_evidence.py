"""Stage 4: validate page-located evidence proposed for eligible mappings."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import (
    INPUT, OUTPUT, REFERENCE, ROOT, SCREENING_COLUMNS, as_bool, read_csv,
    require, require_unique, split_ids, write_csv,
)
EVIDENCE = [
    "schema_version", "evidence_id", "mapping_id", "source_id", "pdf_page",
    "printed_page", "quote_verbatim", "quote_language", "direction",
    "quantified_value", "support_scope", "maladaptation_signal",
    "extraction_run_id", "review_status",
    "reviewed_by", "reviewed_at", "review_note",
]
EVIDENCE_INDICATORS = ["evidence_id", "indicator_id"]


def input_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(INPUT / "evidence_proposals.csv"))
    args = parser.parse_args()

    proposals = read_csv(input_path(args.input))
    require_unique(proposals, "evidence_id", "evidence proposals")
    mappings = read_csv(OUTPUT / "mappings.csv")
    mapping_by_pair = {
        (row["action_id"], row["sector"], row["component"]): row for row in mappings
    }
    mapping_indicator_ids = {}
    for row in read_csv(OUTPUT / "mapping_indicators.csv"):
        mapping_indicator_ids.setdefault(row["mapping_id"], set()).add(row["indicator_id"])
    sources = {row["source_id"]: row for row in read_csv(REFERENCE / "sector_sources.csv")}
    documents = {row["document_id"]: row for row in read_csv(REFERENCE / "documents.csv")}
    indicator_keys = {
        (row["sector"], row["component"], row["indicator_id"])
        for row in read_csv(REFERENCE / "indicators.csv")
    }
    screening = read_csv(OUTPUT / "screening.csv")
    screened_pairs = {(row["mapping_id"], row["source_id"]) for row in screening}

    evidence = []
    evidence_indicators = []
    for proposal in proposals:
        require(proposal["direction"] in {"supports", "qualifies", "contradicts"},
                f"Invalid evidence direction: {proposal['evidence_id']}")
        require(proposal["support_scope"] in {"whole_action", "partial_action"},
                f"Invalid evidence support scope: {proposal['evidence_id']}")
        mapping = mapping_by_pair.get(
            (proposal["action_id"], proposal["sector"], proposal["component"])
        )
        require(mapping is not None, f"No mapping for evidence {proposal['evidence_id']}")
        require(mapping["eligibility"] == "eligible",
                f"Evidence attached to non-eligible mapping: {proposal['evidence_id']}")
        source = sources.get(proposal["source_id"])
        require(source and source["access_status"] == "retrieved"
                and source["review_status"] != "rejected",
                f"Evidence source is not available for proposed assessment: {proposal['source_id']}")
        require((mapping["mapping_id"], proposal["source_id"]) in screened_pairs,
                f"Evidence source was not screened: {proposal['evidence_id']}")

        document = documents[source["document_id"]]
        require(document["extraction_status"] == "processed" and document["text_file"],
                f"Document text has not been extracted: {document['document_id']}")
        page = int(proposal["pdf_page"])
        require(1 <= page <= int(document["page_count"]),
                f"Evidence page is outside PDF: {proposal['evidence_id']}")

        evidence.append({
            "schema_version": "0.3.0",
            "evidence_id": proposal["evidence_id"],
            "mapping_id": mapping["mapping_id"],
            "source_id": proposal["source_id"],
            "pdf_page": proposal["pdf_page"],
            "printed_page": proposal["printed_page"],
            "quote_verbatim": proposal["quote_verbatim"],
            "quote_language": proposal["quote_language"],
            "direction": proposal["direction"],
            "quantified_value": proposal.get("quantified_value", ""),
            "support_scope": proposal["support_scope"],
            "maladaptation_signal": str(as_bool(proposal["maladaptation_signal"])).lower(),
            "extraction_run_id": proposal["extraction_run_id"],
            "review_status": proposal["review_status"],
            "reviewed_by": proposal["reviewed_by"],
            "reviewed_at": proposal["reviewed_at"],
            "review_note": proposal["review_note"],
        })
        addressed_indicator_ids = split_ids(proposal["indicator_ids_addressed"])
        require(
            set(addressed_indicator_ids)
            & mapping_indicator_ids.get(mapping["mapping_id"], set()),
            f"Evidence does not address a linked mapping indicator: {proposal['evidence_id']}",
        )
        for indicator_id in addressed_indicator_ids:
            require((mapping["sector"], mapping["component"], indicator_id) in indicator_keys,
                    f"Invalid evidence indicator {indicator_id}: {proposal['evidence_id']}")
            evidence_indicators.append({
                "evidence_id": proposal["evidence_id"],
                "indicator_id": indicator_id,
            })

    counts = {}
    for row in evidence:
        key = (row["mapping_id"], row["source_id"])
        counts[key] = counts.get(key, 0) + 1
    for row in screening:
        row["evidence_record_count"] = str(counts.get((row["mapping_id"], row["source_id"]), 0))

    write_csv(OUTPUT / "evidence.csv", EVIDENCE, evidence)
    write_csv(OUTPUT / "evidence_indicators.csv", EVIDENCE_INDICATORS, evidence_indicators)
    write_csv(OUTPUT / "screening.csv", SCREENING_COLUMNS, screening)
    print(json.dumps({"evidence": len(evidence), "evidence_indicators": len(evidence_indicators)}))


if __name__ == "__main__":
    main()
