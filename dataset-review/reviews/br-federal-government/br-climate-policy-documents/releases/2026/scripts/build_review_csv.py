#!/usr/bin/env python3
"""Build the complete bilingual review CSV from canonical per-document JSONL files."""

import csv
import json
from pathlib import Path


RELEASE_DIR = Path(__file__).resolve().parents[1]
SAMPLE_DIR = RELEASE_DIR / "sample"
OUTPUT_PATH = RELEASE_DIR / "data" / "pilot" / "policy_records_combined.csv"
TRANSLATIONS_PATH = RELEASE_DIR / "data" / "translations" / "policy_record_translations.jsonl"

CANONICAL_FILES = (
    "national_adaptation_strategy_policy_records.jsonl",
    "climate_plan_summary_adaptation_policy_records.jsonl",
    "biodiversity_policy_records.jsonl",
    "cities_policy_records.jsonl",
    "energy_policy_records.jsonl",
    "water_resources_policy_records.jsonl",
    "disaster_risk_policy_records.jsonl",
    "health_policy_records.jsonl",
    "food_nutrition_security_policy_records.jsonl",
    "agriculture_livestock_policy_records.jsonl",
    "family_farming_policy_records.jsonl",
    "industry_mining_policy_records.jsonl",
    "racial_equality_policy_records.jsonl",
    "ocean_coastal_zone_policy_records.jsonl",
    "traditional_peoples_communities_policy_records.jsonl",
    "indigenous_peoples_policy_records.jsonl",
    "transport_policy_records.jsonl",
    "tourism_policy_records.jsonl",
    "ndc_adaptation_policy_records.jsonl",
)

FIELDNAMES = (
    "record_id",
    "document_id",
    "record_type",
    "source_native_id",
    "parent_record_id",
    "source_language",
    "translation_status",
    "source_text_pt",
    "source_text_en",
    "resources_pt",
    "resources_en",
    "financing_evidence_pt",
    "financing_evidence_en",
    "cost_evidence_pt",
    "cost_evidence_en",
    "co_benefit_evidence_pt",
    "co_benefit_evidence_en",
    "indicators_pt",
    "indicators_en",
    "monitoring_frequency_pt",
    "monitoring_frequency_en",
    "source_notes_pt",
    "source_notes_en",
    "section_or_table_pt",
    "section_or_table_en",
    "responsible_institutions",
    "deadline",
    "related_objective_ids",
    "pdf_page_start",
    "pdf_page_end",
    "printed_page",
    "evidence_status",
    "review_status",
    "review_note",
    "schema_version",
)


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def array_cell(value: object) -> str:
    """Preserve list boundaries and punctuation in a CSV cell."""
    return json.dumps(value or [], ensure_ascii=False)


def review_row(record: dict, translations: dict[str, dict]) -> dict:
    source_is_english = record["document_id"] == "br-ndc-2024"
    official_english = record.get("analysis_summary_en")
    generated = translations.get(record["record_id"], {})

    if source_is_english:
        source_language = "en"
        translation_status = "source_english"
    elif official_english:
        source_language = "pt"
        translation_status = (
            "official_companion_plus_generated_fields" if generated else "official_companion"
        )
    elif generated:
        source_language = "pt"
        translation_status = generated["translation_status"]
    else:
        source_language = "pt"
        translation_status = "not_available"

    return {
        "record_id": record["record_id"],
        "document_id": record["document_id"],
        "record_type": record["record_type"],
        "source_native_id": record.get("source_native_id"),
        "parent_record_id": record.get("parent_record_id"),
        "source_language": source_language,
        "translation_status": translation_status,
        "source_text_pt": "" if source_is_english else record["source_text"],
        "source_text_en": (
            record["source_text"]
            if source_is_english
            else (official_english or generated.get("source_text_en", ""))
        ),
        "resources_pt": array_cell([] if source_is_english else record.get("resources")),
        "resources_en": array_cell(
            record.get("resources") if source_is_english else generated.get("resources_en")
        ),
        "financing_evidence_pt": array_cell(
            [] if source_is_english else record.get("financing_evidence")
        ),
        "financing_evidence_en": array_cell(
            record.get("financing_evidence")
            if source_is_english
            else generated.get("financing_evidence_en")
        ),
        "cost_evidence_pt": array_cell(
            [] if source_is_english else record.get("cost_evidence")
        ),
        "cost_evidence_en": array_cell(
            record.get("cost_evidence")
            if source_is_english
            else generated.get("cost_evidence_en")
        ),
        "co_benefit_evidence_pt": array_cell(
            [] if source_is_english else record.get("co_benefit_evidence")
        ),
        "co_benefit_evidence_en": array_cell(
            record.get("co_benefit_evidence")
            if source_is_english
            else generated.get("co_benefit_evidence_en")
        ),
        "indicators_pt": array_cell([] if source_is_english else record.get("indicators")),
        "indicators_en": array_cell(
            record.get("indicators") if source_is_english else generated.get("indicators_en")
        ),
        "monitoring_frequency_pt": "" if source_is_english else (record.get("monitoring_frequency") or ""),
        "monitoring_frequency_en": (
            (record.get("monitoring_frequency") or "")
            if source_is_english
            else generated.get("monitoring_frequency_en", "")
        ),
        "source_notes_pt": array_cell([] if source_is_english else record.get("source_notes")),
        "source_notes_en": array_cell(
            record.get("source_notes") if source_is_english else generated.get("source_notes_en")
        ),
        "section_or_table_pt": "" if source_is_english else (record.get("section_or_table") or ""),
        "section_or_table_en": (
            (record.get("section_or_table") or "")
            if source_is_english
            else generated.get("section_or_table_en", "")
        ),
        "responsible_institutions": array_cell(record.get("responsible_institutions")),
        "deadline": record.get("deadline"),
        "related_objective_ids": array_cell(record.get("related_objective_ids")),
        "pdf_page_start": record["pdf_page_start"],
        "pdf_page_end": record["pdf_page_end"],
        "printed_page": record.get("printed_page"),
        "evidence_status": record["evidence_status"],
        "review_status": record["review_status"],
        "review_note": record.get("review_note"),
        "schema_version": record["schema_version"],
    }


def main() -> None:
    translations = {}
    if TRANSLATIONS_PATH.exists():
        translations = {
            row["record_id"]: row for row in read_jsonl(TRANSLATIONS_PATH)
        }

    records = []
    for filename in CANONICAL_FILES:
        records.extend(read_jsonl(SAMPLE_DIR / filename))

    record_ids = [record["record_id"] for record in records]
    assert len(record_ids) == len(set(record_ids)), "Canonical record IDs are not unique"

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(review_row(record, translations) for record in records)

    print(
        json.dumps(
            {
                "output": str(OUTPUT_PATH.relative_to(RELEASE_DIR)),
                "records": len(records),
                "columns": len(FIELDNAMES),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
