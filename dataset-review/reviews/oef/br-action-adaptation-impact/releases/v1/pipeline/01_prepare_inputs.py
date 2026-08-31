"""Stage 1: prepare the stable action, indicator, document and source inputs."""

from __future__ import annotations

import json
from pathlib import Path

from common import (
    ARCHIVE, DOCUMENT_COLUMNS, INPUT, REFERENCE, read_csv, require,
    require_unique, split_ids, stable_id, write_csv,
)


ACTIONS = [
    "action_id", "action_name", "action_definition", "action_subcategory",
    "action_type", "time_horizon",
]
INDICATORS = [
    "sector", "component", "risk_id", "risk_name", "indicator_id",
    "indicator_name", "indicator_level", "pathway",
]
SOURCES = [
    "source_id", "sector", "document_id", "scope", "title", "publisher",
    "publication_year", "canonical_url", "source_tier", "access_status",
    "retrieved_at", "review_status", "reviewed_by", "reviewed_at", "review_note",
]
MAPPING_PROPOSALS = [
    "eligibility_id", "action_id", "action_name", "sector", "component",
    "proposed_eligibility", "indicator_ids", "indicator_names",
    "eligibility_rationale", "screening_status", "screened_source_ids",
    "review_status", "reviewed_by", "reviewed_at", "review_note",
]
EVIDENCE_PROPOSALS = [
    "schema_version", "evidence_id", "action_id", "action_name", "sector",
    "component", "source_id", "source_title", "pdf_page", "printed_page",
    "quote_verbatim", "quote_language", "indicator_ids_addressed",
    "indicator_names_addressed", "direction", "quantified_value",
    "support_scope", "maladaptation_signal", "extraction_run_id",
    "review_status", "reviewed_by", "reviewed_at", "review_note",
]
COMPONENTS = ("vulnerability", "exposure")


def moved_path(value: str, folder: str) -> str:
    return f"data/documents/{folder}/{Path(value).name}" if value else ""


def prepare_mapping_proposals(
    actions: list[dict[str, str]], indicators: list[dict[str, str]]
) -> int:
    """Maintain one review row for every action × sector × component pair."""
    path = INPUT / "mapping_proposals.csv"
    seed = path if path.exists() else ARCHIVE / "water_resources_pilot_eligibility_review.csv"
    existing = read_csv(seed) if seed.exists() else []
    existing_by_key = {
        (row["action_id"], row["sector"], row["component"]): row
        for row in existing
    }
    require(
        len(existing_by_key) == len(existing),
        "Duplicate action-sector-component in mapping proposals",
    )

    action_by_id = {row["action_id"]: row for row in actions}
    sectors = sorted({row["sector"] for row in indicators})
    valid_keys = {
        (action_id, sector, component)
        for action_id in action_by_id
        for sector in sectors
        for component in COMPONENTS
    }
    unexpected = set(existing_by_key) - valid_keys
    require(not unexpected, f"Unexpected mapping proposal keys: {sorted(unexpected)}")

    proposals = []
    for sector in sectors:
        for action in actions:
            for component in COMPONENTS:
                key = (action["action_id"], sector, component)
                proposal = dict(existing_by_key.get(key, {}))
                if not proposal:
                    proposal = {
                        "proposed_eligibility": "review_required",
                        "indicator_ids": "",
                        "indicator_names": "",
                        "eligibility_rationale": (
                            "Awaiting review of the action's primary mechanism against "
                            "this sector-component's terminal indicators."
                        ),
                        "screening_status": "not_started",
                        "screened_source_ids": "",
                        "review_status": "proposed",
                        "reviewed_by": "",
                        "reviewed_at": "",
                        "review_note": "",
                    }
                proposal.update({
                    "eligibility_id": stable_id(
                        "elig", action["action_id"], sector, component
                    ),
                    "action_id": action["action_id"],
                    "action_name": action["action_name"],
                    "sector": sector,
                    "component": component,
                })
                proposals.append(proposal)

    write_csv(path, MAPPING_PROPOSALS, proposals)
    return len(proposals)


def prepare_evidence_proposals() -> int:
    """Move the pilot evidence into the active contract and preserve later edits."""
    path = INPUT / "evidence_proposals.csv"
    seed = path if path.exists() else ARCHIVE / "water_resources_pilot_evidence_review.csv"
    proposals = read_csv(seed) if seed.exists() else []
    require_unique(proposals, "evidence_id", "evidence proposals")
    for proposal in proposals:
        proposal["schema_version"] = "0.3.0"
    write_csv(path, EVIDENCE_PROPOSALS, proposals)
    return len(proposals)


def main() -> None:
    active_reference_paths = {
        "actions": REFERENCE / "actions.csv",
        "indicators": REFERENCE / "indicators.csv",
        "documents": REFERENCE / "documents.csv",
        "sector_sources": REFERENCE / "sector_sources.csv",
    }
    if all(path.exists() for path in active_reference_paths.values()):
        actions = read_csv(active_reference_paths["actions"])
        indicators = read_csv(active_reference_paths["indicators"])
        documents = read_csv(active_reference_paths["documents"])
        sources = read_csv(active_reference_paths["sector_sources"])

        require_unique(actions, "action_id", "actions")
        require_unique(documents, "document_id", "documents")
        require_unique(sources, "source_id", "sector sources")
        indicator_keys = {
            (row["sector"], row["component"], row["indicator_id"])
            for row in indicators
        }
        require(len(indicator_keys) == len(indicators), "Duplicate indicator key")
        document_ids = {row["document_id"] for row in documents}
        for source in sources:
            require(
                not source["document_id"] or source["document_id"] in document_ids,
                f"Unknown document for source {source['source_id']}",
            )

        mapping_proposal_count = prepare_mapping_proposals(actions, indicators)
        evidence_proposal_count = prepare_evidence_proposals()
        print(json.dumps({
            "actions": len(actions),
            "indicators": len(indicators),
            "documents": len(documents),
            "sector_sources": len(sources),
            "mapping_proposals": mapping_proposal_count,
            "evidence_proposals": evidence_proposal_count,
        }))
        return

    actions = read_csv(ARCHIVE / "action_catalog.csv")
    indicators = read_csv(ARCHIVE / "indicator_framework.csv")
    manifest = read_csv(ARCHIVE / "document_processing_manifest.csv")
    source_register = read_csv(ARCHIVE / "source_register.csv")

    require_unique(actions, "action_id", "actions")
    require_unique(manifest, "candidate_document_id", "documents")
    require_unique(source_register, "source_id", "sector sources")
    indicator_keys = {
        (row["sector"], row["component"], row["indicator_id"]) for row in indicators
    }
    require(len(indicator_keys) == len(indicators), "Duplicate indicator key")

    documents = []
    for row in manifest:
        documents.append({
            "document_id": row["candidate_document_id"],
            "document_title": row["document_title"],
            "retrieval_status": row["pdf_download_status"],
            "local_pdf": moved_path(row["local_pdf"], "raw"),
            "sha256": row["sha256"],
            "page_count": row["pdf_page_count"],
            "text_file": moved_path(row["text_file"], "text"),
            "extraction_status": row["processing_status"],
            "extracted_page_count": row["extracted_page_count"],
            "pages_with_text": row["pages_with_text"],
            "text_characters": row["text_characters"],
            "extraction_tool": row["extraction_tool"],
            "extracted_at": row["processed_at"],
            "extraction_note": row["processing_note"],
        })

    document_by_pdf = {
        Path(row["local_pdf"]).name: row["document_id"]
        for row in documents if row["local_pdf"]
    }
    document_by_source = {}
    for row in manifest:
        for source_id in split_ids(row["workbook_source_ids"]):
            require(
                source_id not in document_by_source
                or document_by_source[source_id] == row["candidate_document_id"],
                f"Source {source_id} maps to multiple documents",
            )
            document_by_source[source_id] = row["candidate_document_id"]

    sources = []
    for row in source_register:
        pdf_name = Path(row["local_pdf"]).name if row["local_pdf"] else ""
        document_id = document_by_pdf.get(pdf_name) or document_by_source.get(row["source_id"], "")
        require(
            row["review_status"] != "accepted"
            or (row["access_status"] == "retrieved" and document_id),
            f"Accepted source {row['source_id']} is not tied to a retrieved document",
        )
        sources.append({
            "source_id": row["source_id"],
            "sector": row["sector"],
            "document_id": document_id,
            "scope": row["scope"],
            "title": row["title"],
            "publisher": row["publisher"],
            "publication_year": row["publication_year"],
            "canonical_url": row["canonical_url"],
            "source_tier": row["source_tier"],
            "access_status": row["access_status"],
            "retrieved_at": row["retrieved_at"],
            "review_status": row["review_status"],
            "reviewed_by": row["reviewed_by"],
            "reviewed_at": row["reviewed_at"],
            "review_note": row["review_note"],
        })

    write_csv(REFERENCE / "actions.csv", ACTIONS, actions)
    write_csv(REFERENCE / "indicators.csv", INDICATORS, indicators)
    write_csv(REFERENCE / "documents.csv", DOCUMENT_COLUMNS, documents)
    write_csv(REFERENCE / "sector_sources.csv", SOURCES, sources)
    mapping_proposal_count = prepare_mapping_proposals(actions, indicators)
    evidence_proposal_count = prepare_evidence_proposals()
    print(json.dumps({
        "actions": len(actions),
        "indicators": len(indicators),
        "documents": len(documents),
        "sector_sources": len(sources),
        "mapping_proposals": mapping_proposal_count,
        "evidence_proposals": evidence_proposal_count,
    }))


if __name__ == "__main__":
    main()
