#!/usr/bin/env python3
"""Join reviewed pilot decisions to evidence and calculate action-level scores."""

import csv
import json
import math
from pathlib import Path


RELEASE_DIR = Path(__file__).resolve().parents[1]
DECISIONS_PATH = RELEASE_DIR / "data" / "pilot" / "pilot_match_decisions.csv"
RECORDS_PATH = RELEASE_DIR / "data" / "pilot" / "policy_records_combined.csv"
ACTIONS_PATH = RELEASE_DIR / "data" / "raw" / "current-bank-adaptation-actions.csv"
DOCUMENTS_PATH = RELEASE_DIR / "data" / "policy_documents.csv"
MATCHES_PATH = RELEASE_DIR / "data" / "pilot" / "policy_action_matches.csv"
SCORES_PATH = RELEASE_DIR / "data" / "pilot" / "action_policy_scores.csv"

PILOT = {
    "c40_0046": {
        "relevance": "low",
        "summary": "Brazilian policy prioritizes coastal and marine resilience, protected areas, and restoration, but the reviewed records do not commit to coastal protection infrastructure.",
        "caveat": "Do not interpret general coastal policy or ecosystem restoration as a seawall or protective-structure commitment.",
    },
    "c40_0048": {
        "relevance": "high",
        "summary": "Federal policy directly supports urban drainage and rainwater-management works through disaster-prevention resources, a national structural-risk target, and municipal adaptation solutions.",
        "caveat": "The records establish policy support and programmed resources, not proof that local drainage upgrades have been delivered.",
    },
    "c40_0049": {
        "relevance": "medium",
        "summary": "Policy supports and monitors temporary accommodation for climate-affected and displaced people, but does not specify construction and maintenance of resilient hazard shelters.",
        "caveat": "Temporary accommodation is a partial functional match; resilient design, location, operations, and maintenance are not established.",
    },
    "c40_0051": {
        "relevance": "none",
        "summary": "No reviewed policy record meaningfully commits to public shade structures or tree shade in heat hotspots.",
        "caveat": "The absence of a match in this corpus does not prove that no Brazilian policy outside the selected documents addresses public shading.",
    },
    "ipcc_0086": {
        "relevance": "high",
        "summary": "The Strategy explicitly adopts ecosystem-based adaptation, supported by a quantified biodiversity target and actions for restoration, connectivity, climate refuges, and conservation units.",
        "caveat": "The evidence demonstrates policy alignment; it does not establish implementation progress or ecological outcomes.",
    },
}

RELATION_WEIGHT = {
    "commits": 1.0,
    "targets": 0.85,
    "funds": 0.85,
    "governs": 0.65,
    "monitors": 0.65,
    "prioritizes": 0.55,
    "identifies": 0.35,
    "contextualizes": 0.20,
    "references": 0.20,
    "restates": 0.10,
}
EXPLICITNESS_WEIGHT = {"explicit": 1.0, "inferred": 0.6}
CONFIDENCE_WEIGHT = {"high": 1.0, "medium": 0.65, "low": 0.35}
RELEVANCE_CAP = {"high": 100.0, "medium": 65.0, "low": 32.0, "none": 0.0}


def read_csv(path: Path, encoding: str = "utf-8") -> list[dict]:
    with path.open(encoding=encoding, newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def grade(score: float) -> str:
    if score >= 66:
        return "strong"
    if score >= 33:
        return "medium"
    if score > 0:
        return "weak"
    return "none"


def main() -> None:
    records = {row["record_id"]: row for row in read_csv(RECORDS_PATH)}
    actions = {
        row["ActionID"]: row for row in read_csv(ACTIONS_PATH, encoding="utf-8-sig")
    }
    documents = {
        row["doc_id"]: row for row in read_csv(DOCUMENTS_PATH, encoding="utf-8-sig")
    }
    decisions = read_csv(DECISIONS_PATH)

    assert set(PILOT).issubset(actions)
    assert all(row["ActionID"] in PILOT for row in decisions)
    assert all(row["record_id"] in records for row in decisions)
    assert len({(row["ActionID"], row["record_id"]) for row in decisions}) == len(decisions)

    matches = []
    for decision in decisions:
        record = records[decision["record_id"]]
        assert decision["relationship"] in RELATION_WEIGHT
        assert decision["explicitness"] in EXPLICITNESS_WEIGHT
        assert decision["match_confidence"] in CONFIDENCE_WEIGHT
        assert decision["match_relevance"] in {"high", "medium", "low"}
        strength = (
            RELATION_WEIGHT[decision["relationship"]]
            * EXPLICITNESS_WEIGHT[decision["explicitness"]]
            * CONFIDENCE_WEIGHT[decision["match_confidence"]]
        )
        matches.append(
            {
                **decision,
                "document_id": record["document_id"],
                "record_type": record["record_type"],
                "source_native_id": record["source_native_id"],
                "evidence_text_pt": record["source_text_pt"],
                "evidence_text_en": record["source_text_en"],
                "supporting_resources_en": record["resources_en"],
                "supporting_indicators_en": record["indicators_en"],
                "pdf_page_start": record["pdf_page_start"],
                "pdf_page_end": record["pdf_page_end"],
                "evidence_strength": f"{strength:.4f}",
                "review_status": "pilot_proposed",
            }
        )

    match_fields = [
        "ActionID", "record_id", "document_id", "record_type", "source_native_id",
        "relationship", "match_relevance", "explicitness", "match_confidence",
        "evidence_strength", "evidence_text_pt", "evidence_text_en",
        "supporting_resources_en", "supporting_indicators_en", "pdf_page_start",
        "pdf_page_end", "match_rationale_en", "review_status",
    ]
    write_csv(MATCHES_PATH, matches, match_fields)

    scores = []
    for action_id, assessment in PILOT.items():
        action_matches = [row for row in matches if row["ActionID"] == action_id]
        total_strength = sum(float(row["evidence_strength"]) for row in action_matches)
        uncapped = 100 * (1 - math.exp(-total_strength / 2))
        score = min(uncapped, RELEVANCE_CAP[assessment["relevance"]])
        strongest = max(
            action_matches,
            key=lambda row: float(row["evidence_strength"]),
            default=None,
        )
        matched_evidence = []
        for match in action_matches:
            document = documents[match["document_id"]]
            page_start = int(match["pdf_page_start"])
            page_end = int(match["pdf_page_end"])
            page_label = (
                f"PDF p. {page_start}"
                if page_start == page_end
                else f"PDF pp. {page_start}-{page_end}"
            )
            matched_evidence.append(
                {
                    "document_id": match["document_id"],
                    "document_name": document["document"],
                    "record_id": match["record_id"],
                    "relationship": match["relationship"],
                    "extract_en": match["evidence_text_en"],
                    "extract_pt": match["evidence_text_pt"],
                    "page_start": page_start,
                    "page_end": page_end,
                    "citation": f"{document['document']}, {page_label}",
                    "source_url": document["url_public_mirror"],
                }
            )
        scores.append(
            {
                "ActionID": action_id,
                "ActionName": actions[action_id]["ActionName"],
                "overall_relevance": assessment["relevance"],
                "alignment_score": f"{score:.1f}",
                "alignment_grade": grade(score),
                "strongest_relationship": strongest["relationship"] if strongest else "none",
                "accepted_evidence_count": len(action_matches),
                "supporting_document_count": len(
                    {row["document_id"] for row in action_matches}
                ),
                "matched_evidence": json.dumps(
                    matched_evidence, ensure_ascii=False, separators=(",", ":")
                ),
                "summary_en": assessment["summary"],
                "key_caveat_en": assessment["caveat"],
                "rubric_version": "pilot-0.1.0",
                "review_status": "pilot_proposed",
            }
        )

    score_fields = [
        "ActionID", "ActionName", "overall_relevance", "alignment_score",
        "alignment_grade", "strongest_relationship", "accepted_evidence_count",
        "supporting_document_count", "matched_evidence", "summary_en", "key_caveat_en",
        "rubric_version", "review_status",
    ]
    write_csv(SCORES_PATH, scores, score_fields)
    print(json.dumps({"matches": len(matches), "scores": len(scores)}, indent=2))


if __name__ == "__main__":
    main()
