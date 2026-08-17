#!/usr/bin/env python3
"""Add source-only financing, cost, and co-benefit evidence to canonical records.

The enrichment is deliberately conservative:
- evidence values are copied verbatim from the record's source fields;
- financing evidence may name a programme or mechanism but does not imply funding;
- cost evidence requires an explicit currency amount tied to the record;
- co-benefit evidence requires explicit benefit/co-benefit wording;
- no thematic benefit category is inferred from an action description.
"""

import json
import re
from pathlib import Path


RELEASE_DIR = Path(__file__).resolve().parents[1]
SAMPLE_DIR = RELEASE_DIR / "sample"
SCHEMA_PATH = RELEASE_DIR / "schemas" / "policy_record.schema.json"

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

FINANCING_PATTERN = re.compile(
    r"(?:recursos? financeiros?|fontes? de financiamento|financiamento|"
    r"linhas? de cr[eé]dito|\bcr[eé]dito\b|\bfundo\b|n[aã]o or[cç]ament[aá]rio|"
    r"\bprograma\s+\d{4}\b|\ba[cç][aã]o\s+[0-9A-Z]{2,}\b|"
    r"\bentrega\s+\d+\b|medida institucional)",
    re.IGNORECASE,
)
COST_PATTERN = re.compile(
    r"(?:(?:custo|or[cç]amento|valor estimado)[^.\n]{0,120}(?:R\$|US\$|USD|BRL)\s*[0-9]|"
    r"(?:R\$|US\$|USD|BRL)\s*[0-9][^.\n]{0,120}(?:custo|or[cç]amento|valor estimado))",
    re.IGNORECASE,
)
COBENEFIT_PATTERN = re.compile(
    r"(?:co-?benefit|cobenef[ií]c|benef[ií]cios?\s+para\b|gerando\s+benef[ií]cios?\b)",
    re.IGNORECASE,
)


CONTEXT_RECORDS = {
    "biodiversity_policy_records.jsonl": {
        "schema_version": "0.2.0",
        "record_id": "br-secadp-biodiversidade-2026:context-cobenefits",
        "document_id": "br-secadp-biodiversidade-2026",
        "record_type": "context",
        "source_native_id": None,
        "parent_record_id": None,
        "source_text": (
            "Outrossim, é importante considerar que as estratégias planejadas devem evitar os "
            "riscos de má adaptação, e as ações elencadas devem fomentar a justiça distributiva, "
            "a integração territorial e os cobenefícios sociais e ecológicos, incluindo saberes "
            "tradicionais, indígenas e pequena agricultura familiar."
        ),
        "analysis_summary_en": None,
        "deadline": None,
        "responsible_institutions": [],
        "resources": [],
        "financing_evidence": [],
        "cost_evidence": [],
        "co_benefit_evidence": [],
        "indicators": [],
        "monitoring_frequency": None,
        "source_notes": [],
        "related_objective_ids": [],
        "pdf_page_start": 35,
        "pdf_page_end": 35,
        "printed_page": "35",
        "section_or_table": "3. Plano de Ação",
        "evidence_status": "verified",
        "review_status": "proposed",
        "review_note": "Document-level guidance; it is not assigned to every individual action.",
    },
    "energy_policy_records.jsonl": {
        "schema_version": "0.2.0",
        "record_id": "br-secadp-energia-2026:context-cobenefits",
        "document_id": "br-secadp-energia-2026",
        "record_type": "context",
        "source_native_id": None,
        "parent_record_id": None,
        "source_text": (
            "Ademais, a ENA orienta esse processo à transparência, à articulação entre diferentes "
            "níveis de governo, à integração entre planos, programas e ações do setor, além da busca "
            "por cobenefícios entre adaptação e mitigação das emissões de GEE."
        ),
        "analysis_summary_en": None,
        "deadline": None,
        "responsible_institutions": [],
        "resources": [],
        "financing_evidence": [],
        "cost_evidence": [],
        "co_benefit_evidence": [],
        "indicators": [],
        "monitoring_frequency": None,
        "source_notes": [],
        "related_objective_ids": [],
        "pdf_page_start": 46,
        "pdf_page_end": 46,
        "printed_page": "46",
        "section_or_table": "3.1. Objetivos",
        "evidence_status": "verified",
        "review_status": "proposed",
        "review_note": "Document-level guidance; it is not assigned to every individual action.",
    },
    "disaster_risk_policy_records.jsonl": {
        "schema_version": "0.2.0",
        "record_id": "br-secadp-riscos-desastres-2026:context-cobenefits",
        "document_id": "br-secadp-riscos-desastres-2026",
        "record_type": "context",
        "source_native_id": None,
        "parent_record_id": None,
        "source_text": (
            "Tais medidas são de extrema importância para aumentar a segurança diante de desastres "
            "relacionados a água, como secas e inundações, além de outros cobenefícios ambientais "
            "e sociais."
        ),
        "analysis_summary_en": None,
        "deadline": None,
        "responsible_institutions": [],
        "resources": [],
        "financing_evidence": [],
        "cost_evidence": [],
        "co_benefit_evidence": [],
        "indicators": [],
        "monitoring_frequency": None,
        "source_notes": [
            "The preceding source paragraph discusses ecosystem-based adaptation measures."
        ],
        "related_objective_ids": [],
        "pdf_page_start": 44,
        "pdf_page_end": 44,
        "printed_page": "44",
        "section_or_table": "Ampla implementação de medidas de adaptação baseadas em ecossistemas",
        "evidence_status": "verified",
        "review_status": "proposed",
        "review_note": "Document-level context; it is not assigned to every individual action.",
    },
    "ndc_adaptation_policy_records.jsonl": {
        "schema_version": "0.2.0",
        "record_id": "br-ndc-2024:context-co-benefit-list",
        "document_id": "br-ndc-2024",
        "record_type": "context",
        "source_native_id": None,
        "parent_record_id": None,
        "source_text": (
            "Linking sectoral mitigation and adaptation policies with other public policies should "
            "generate, in addition to reducing emissions, co-benefits such as: biodiversity "
            "conservation, provision of ecosystem services, reduction of atmospheric pollution, "
            "generation of employment and income, reduction of social and regional inequalities, "
            "promotion of food security, energy security and water security, guarantee of the "
            "rights of traditional peoples and communities and indigenous peoples."
        ),
        "analysis_summary_en": None,
        "deadline": None,
        "responsible_institutions": [],
        "resources": [],
        "financing_evidence": [],
        "cost_evidence": [],
        "co_benefit_evidence": [],
        "indicators": [],
        "monitoring_frequency": None,
        "source_notes": [],
        "related_objective_ids": [],
        "pdf_page_start": 37,
        "pdf_page_end": 37,
        "printed_page": "37",
        "section_or_table": "5. Assumptions and methodological approaches",
        "evidence_status": "verified",
        "review_status": "proposed",
        "review_note": "Document-level policy statement; it is not assigned to every individual action.",
    },
}


def source_values(record: dict) -> list[str]:
    values = [record.get("source_text", "")]
    values.extend(record.get("resources") or [])
    values.extend(record.get("source_notes") or [])
    return [value for value in values if value]


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def validate_record(record: dict, schema: dict) -> None:
    missing = set(schema["required"]) - set(record)
    extra = set(record) - set(schema["properties"])
    if missing or extra:
        raise ValueError(
            f"{record.get('record_id')}: missing={sorted(missing)} extra={sorted(extra)}"
        )
    if record["schema_version"] != schema["properties"]["schema_version"]["const"]:
        raise ValueError(f"{record['record_id']}: invalid schema_version")
    for field in ("record_type", "evidence_status", "review_status"):
        if record[field] not in schema["properties"][field]["enum"]:
            raise ValueError(f"{record['record_id']}: invalid {field}")
    if not isinstance(record["source_text"], str) or not record["source_text"]:
        raise ValueError(f"{record['record_id']}: invalid source_text")
    for field in ("pdf_page_start", "pdf_page_end"):
        if not isinstance(record[field], int) or record[field] < 1:
            raise ValueError(f"{record['record_id']}: invalid {field}")
    for field in (
        "responsible_institutions",
        "resources",
        "financing_evidence",
        "cost_evidence",
        "co_benefit_evidence",
        "indicators",
        "source_notes",
        "related_objective_ids",
    ):
        value = record[field]
        if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
            raise ValueError(f"{record['record_id']}: invalid {field}")
        if len(value) != len(set(value)):
            raise ValueError(f"{record['record_id']}: duplicate {field}")


def enrich(record: dict) -> dict:
    record["schema_version"] = "0.2.0"
    values = source_values(record)
    resources = record.get("resources") or []

    financing = list(resources)
    financing.extend(value for value in values if FINANCING_PATTERN.search(value))
    record["financing_evidence"] = unique(financing)
    record["cost_evidence"] = unique(
        value for value in values if COST_PATTERN.search(value)
    )
    record["co_benefit_evidence"] = unique(
        value for value in [record.get("source_text", ""), *(record.get("source_notes") or [])]
        if value and COBENEFIT_PATTERN.search(value)
    )
    return record


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    totals = {
        "records": 0,
        "with_financing_evidence": 0,
        "with_cost_evidence": 0,
        "with_co_benefit_evidence": 0,
        "context_records_added": 0,
    }

    for filename in CANONICAL_FILES:
        path = SAMPLE_DIR / filename
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
        context = CONTEXT_RECORDS.get(filename)
        if context and not any(item["record_id"] == context["record_id"] for item in records):
            records.append(context)
            totals["context_records_added"] += 1

        records = [enrich(record) for record in records]
        for record in records:
            validate_record(record, schema)
        path.write_text(
            "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records),
            encoding="utf-8",
        )

        totals["records"] += len(records)
        totals["with_financing_evidence"] += sum(bool(r["financing_evidence"]) for r in records)
        totals["with_cost_evidence"] += sum(bool(r["cost_evidence"]) for r in records)
        totals["with_co_benefit_evidence"] += sum(bool(r["co_benefit_evidence"]) for r in records)

    print(json.dumps(totals, indent=2))


if __name__ == "__main__":
    main()
