#!/usr/bin/env python3
"""Translate Portuguese policy-record fields into reviewable English.

Translations are stored separately from source extraction so Portuguese evidence
is never overwritten. The script is resumable: accepted records already present
in the output JSONL are skipped.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

RELEASE_DIR = Path(__file__).resolve().parents[1]
SAMPLE_DIR = RELEASE_DIR / "sample"
OUTPUT_PATH = RELEASE_DIR / "data" / "translations" / "policy_record_translations.jsonl"
DEFAULT_MODEL = "gpt-4.1-mini"
DEFAULT_BATCH_SIZE = 8

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
)

TRANSLATED_FIELDS = (
    "source_text",
    "resources",
    "financing_evidence",
    "cost_evidence",
    "co_benefit_evidence",
    "indicators",
    "monitoring_frequency",
    "source_notes",
    "section_or_table",
)

# Argos sometimes localizes or reverses Brazilian policy acronyms. Preserve the
# source acronyms so records remain traceable to the official documents.
ACRONYM_EQUIVALENTS = {
    "GEE": ("GHG",),
    "CAF": ("FCA",),
    "EEI": ("EIS",),
    "CVU": ("UCRC", "UVC"),
    "PD&I": ("RD&I",),
    "ODS": ("SDGs", "SDG", "SDS"),
    "PEM": ("SEM",),
    "OIT": ("ILO",),
    "IDHM": ("MHDI",),
    "TI": ("ITs", "IT"),
    "PAC": ("CAP",),
    "SNASMDS": ("SNASSMDS",),
    "IST": ("STIs", "STI"),
    "ONG": ("NGOs", "NGO"),
    "PAA": ("AAP",),
    "SAN": ("FNS",),
    "FMM": ("MMF",),
    "RDT": ("DDR",),
}

AUDITED_SOURCE_TEXT_OVERRIDES = {
    "br-secadp-agricultura-familiar-2026:m2": "Increase PRONAF credit operations for eligible goods and services for irrigation, water-storage and drainage works by 9% per year, strengthening family farming in addressing climate change, by 2035.",
    "br-secadp-agricultura-familiar-2026:a1-m20": "Expand access to the Family Farming Registry (CAF) by adding new registrations and conducting outreach drives for Indigenous Peoples, Quilombolas, traditional communities, extractivist communities, and family farmers in remote regions, ensuring their access to public policies.",
    "br-secadp-agricultura-familiar-2026:a1-m64": "Create and make available, in partnership with education and research institutions, a multichannel chatbot (WhatsApp, Telegram and web) that uses the farmer's location (municipality or postal code—CEP) to provide weekly weather forecasts, information on extreme events, and technical guidance adapted to the regional agricultural calendar.",
    "br-secadp-agricultura-pecuaria-2026:m8": "Expand the diversity of the genetic base of crops and breeds (genetic resources) with adaptive capacity to climate change by 2035.",
    "br-secadp-biodiversidade-2026:a5-m1": "Implement the National Early Warning, Early Detection and Rapid Response Programme for Invasive Alien Species (PNADPRR) in federal conservation units and create post-extreme-weather-event monitoring protocols for Invasive Alien Species (EEI) in federal conservation units (UC).",
    "br-secadp-igualdade-racial-2026:a1-m6": "Monitor, together with the ministries responsible for implementation, the actions under Axis 8—Environment, Guarantee of the Right to the City and Valuing Territories—of the Plano Juventude Negra Viva.",
    "br-secadp-povos-comunidades-tradicionais-2026:a7-m1": "Establish emergency-assistance mechanisms and social-protection instruments for communities whose traditional livelihoods have been compromised by extreme weather events, including basic food baskets, financial assistance, and Primary Health Care.",
    "br-secadp-povos-comunidades-tradicionais-2026:a2-m6": "Establish primary healthcare measures specifically for vulnerable and marginalized populations, with emphasis on rural, forest and waterside populations (Indigenous Peoples, Quilombolas, Traditional Peoples and Communities), people experiencing homelessness, and migrants.",
    "br-secadp-povos-comunidades-tradicionais-2026:o2": "Ensure preventive and emergency access to healthcare for Traditional Peoples and Communities in their territories.",
    "br-secadp-povos-indigenas-2026:a1-m5": "Identify Indigenous villages that do not have a continuous supply of safe, good-quality drinking water.",
    "br-secadp-povos-indigenas-2026:a1-m17": "Identify Indigenous Lands that have no energy or communications source, and Indigenous Lands with access to electricity, classified by source type.",
    "br-secadp-povos-indigenas-2026:a2-m16": "Establish prioritization criteria for developing forest-restoration actions in Indigenous Lands (TI).",
    "br-secadp-povos-indigenas-2026:a3-m1": "Incorporate climate education into the political-pedagogical projects of 30 Indigenous schools.",
    "br-secadp-riscos-desastres-2026:o2": "Reduce disaster-related damage and losses, taking account of priority disaster types and areas in the country, by promoting non-structural actions (measures and instruments) and structural response and recovery actions (works and structures) in the context of climate change.",
    "br-secadp-riscos-desastres-2026:m4": "Improve and expand disaster-preparedness actions to reduce damage and losses.",
    "br-secadp-riscos-desastres-2026:a1-m4": "Develop a Contingency Plan module in S2iD 4.0 (system implemented and operational / 2027 / Sedec-MIDR).",
    "br-secadp-riscos-desastres-2026:a8-m4": "Conduct a study assessing the appropriateness and feasibility of emergency transfers of resources for mitigation and preparedness, including mobilization of financial, human and material resources to reduce disaster-related damage and losses (study published, with a regulatory proposal if applicable / 2031 / Sedec-MIDR).",
    "br-secadp-riscos-desastres-2026:a6-m9": "Provide training on disaster damage assessment (training available, with guidance material / 2027 / Sedec-MIDR).",
    "br-secadp-saude-2026:m26": "Reduce unplanned interruptions of health information systems caused by environmental or climate-related problems to zero and maintain them at zero by 2027.",
    "br-secadp-seguranca-alimentar-2026:a2-m10": "Set targets for PAA implementing bodies to purchase food from Traditional Peoples and Communities (PCTs).",
    "br-secadp-seguranca-alimentar-2026:a2-m11": "Set targets for PAA implementing bodies to provide food in the territories and to the populations most vulnerable to climate change.",
    "br-secadp-transportes-2026:a1-m15": "Prioritize financing for shallow-draft vessels using FMM resources.",
    "br-secadp-transportes-2026:a1-m16": "Develop, with other stakeholders, a public policy for financing sustainable infrastructure projects or projects related to responses to adverse climate events using FMM resources.",
    "br-secadp-turismo-2026:a1-m1": "Assess the sustainable-tourism and climate-resilience knowledge and skills needs of professionals and local communities, identifying priority areas for each tourism region.",
}

SYSTEM_PROMPT = """You translate Brazilian federal climate-policy records from Portuguese to English.

Requirements:
- Translate faithfully and completely. Do not summarize, explain, improve, or add information.
- Preserve identifiers, acronyms, programme names, institution names, numbers, years, percentages, and units.
- Preserve list length and item order exactly.
- Use clear policy English. Translate generic administrative terms, but retain official proper names in Portuguese where translating the name could create ambiguity.
- Return only a JSON object with a `translations` array.
- Each output item must contain exactly: record_id, source_text_en, resources_en, financing_evidence_en, cost_evidence_en, co_benefit_evidence_en, indicators_en, monitoring_frequency_en, source_notes_en, section_or_table_en.
- String inputs produce string outputs. Array inputs produce arrays with the same number of items.
- Empty strings and empty arrays remain empty.
"""


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def canonical_records() -> list[dict]:
    records = []
    for filename in CANONICAL_FILES:
        records.extend(read_jsonl(SAMPLE_DIR / filename))
    record_ids = [record["record_id"] for record in records]
    assert len(record_ids) == len(set(record_ids)), "Canonical record IDs are not unique"
    return records


def input_payload(record: dict) -> dict:
    return {
        "record_id": record["record_id"],
        "source_text": record["source_text"],
        "resources": record.get("resources") or [],
        "financing_evidence": record.get("financing_evidence") or [],
        "cost_evidence": record.get("cost_evidence") or [],
        "co_benefit_evidence": record.get("co_benefit_evidence") or [],
        "indicators": record.get("indicators") or [],
        "monitoring_frequency": record.get("monitoring_frequency") or "",
        "source_notes": record.get("source_notes") or [],
        "section_or_table": record.get("section_or_table") or "",
    }


def load_existing() -> dict[str, dict]:
    if not OUTPUT_PATH.exists():
        return {}
    return {row["record_id"]: row for row in read_jsonl(OUTPUT_PATH)}


def digit_tokens(value: object) -> list[str]:
    text = json.dumps(value, ensure_ascii=False).translate(
        str.maketrans({"²": "2", "³": "3"})
    )
    return [
        token.replace(",", ".")
        for token in re.findall(r"\d+(?:[.,]\d+)?", text)
    ]


def validate_translation(source: dict, translated: dict) -> None:
    required = {
        "record_id",
        "source_text_en",
        "resources_en",
        "financing_evidence_en",
        "cost_evidence_en",
        "co_benefit_evidence_en",
        "indicators_en",
        "monitoring_frequency_en",
        "source_notes_en",
        "section_or_table_en",
    }
    assert set(translated) == required, f"{source['record_id']}: unexpected translation fields"
    assert translated["record_id"] == source["record_id"]

    for field in TRANSLATED_FIELDS:
        output_field = f"{field}_en"
        source_value = source[field]
        output_value = translated[output_field]
        assert isinstance(output_value, type(source_value)), (
            f"{source['record_id']}: {output_field} changed type"
        )
        if isinstance(source_value, list):
            assert len(output_value) == len(source_value), (
                f"{source['record_id']}: {output_field} changed list length"
            )
        if source_value:
            assert output_value, f"{source['record_id']}: {output_field} is unexpectedly empty"
        assert digit_tokens(output_value) == digit_tokens(source_value), (
            f"{source['record_id']}: {output_field} changed numeric content "
            f"{digit_tokens(source_value)} -> {digit_tokens(output_value)}"
        )


def translate_openai_batch(client: object, model: str, records: list[dict]) -> list[dict]:
    payload = [input_payload(record) for record in records]
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": "Translate these records:\n" + json.dumps(payload, ensure_ascii=False),
            },
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    result = json.loads(response.choices[0].message.content or "{}")
    translations = result.get("translations")
    assert isinstance(translations, list), "Response has no translations array"
    assert len(translations) == len(records), "Response record count differs from request"

    by_id = {item["record_id"]: item for item in translations}
    assert len(by_id) == len(records), "Response contains duplicate record IDs"
    ordered = [by_id[record["record_id"]] for record in records]
    for record, translation in zip(payload, ordered):
        validate_translation(record, translation)
    return ordered


def load_argos_translator(package_dir: Path) -> object:
    from argostranslate import package, settings, translate

    settings.package_data_dir = package_dir
    settings.package_dirs = [package_dir]
    translate.load_installed_languages()
    installed = translate.get_installed_languages()
    source = next(language for language in installed if language.code == "pt")
    target = next(language for language in installed if language.code == "en")
    return source.get_translation(target)


def translate_argos_batch(translator: object, records: list[dict]) -> list[dict]:
    translated_rows = []
    for record in records:
        source = input_payload(record)

        def translate_text(text: str) -> str:
            numbers: list[str] = []

            def mask(match: re.Match) -> str:
                numbers.append(match.group(0))
                return f" ZXNUMBER{len(numbers) - 1}XZ "

            masked = re.sub(r"\d+(?:[.,]\d+)?", mask, text)
            output = translator.translate(masked)
            for index, number in enumerate(numbers):
                placeholder = f"ZXNUMBER{index}XZ"
                if placeholder not in output:
                    # A numeric value must never disappear during translation.
                    # Translating the surrounding fragments separately is a safe fallback.
                    fragments = re.split(r"(\d+(?:[.,]\d+)?)", text)
                    return "".join(
                        fragment
                        if re.fullmatch(r"\d+(?:[.,]\d+)?", fragment)
                        else translator.translate(fragment)
                        for fragment in fragments
                    )
                output = output.replace(placeholder, number)
            return re.sub(r"\s+([.,;:%)])", r"\1", output).strip()

        def translate_value(value: object) -> object:
            if isinstance(value, list):
                return [translate_text(item) for item in value]
            return translate_text(value) if value else ""

        translated = {
            "record_id": record["record_id"],
            **{
                f"{field}_en": translate_value(source[field])
                for field in TRANSLATED_FIELDS
            },
        }
        validate_translation(source, translated)
        translated_rows.append(translated)
    return translated_rows


def append_translations(rows: list[dict], model: str, status: str) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    with OUTPUT_PATH.open("a", encoding="utf-8") as handle:
        for row in rows:
            output = {
                "schema_version": "1.0.0",
                "record_id": row["record_id"],
                "source_language": "pt",
                "target_language": "en",
                "translation_status": status,
                "translation_model": model,
                "translated_at": timestamp,
                **{key: value for key, value in row.items() if key != "record_id"},
            }
            handle.write(json.dumps(output, ensure_ascii=False, sort_keys=True) + "\n")


def preserve_source_acronyms(source_value: object, translated_value: object) -> object:
    if isinstance(source_value, list):
        return [
            preserve_source_acronyms(source_item, translated_item)
            for source_item, translated_item in zip(source_value, translated_value)
        ]
    if not source_value or not translated_value:
        return translated_value
    output = translated_value
    if "ODS" in source_value:
        output = re.sub(r"\b(\d+)\s+(?:SDG|SDS)\b", r"ODS \1", output)
    for source_acronym, translated_acronyms in ACRONYM_EQUIVALENTS.items():
        if source_acronym not in source_value or source_acronym in output:
            continue
        for translated_acronym in translated_acronyms:
            output = re.sub(
                rf"(?<![A-Za-z]){re.escape(translated_acronym)}(?![A-Za-z])",
                source_acronym,
                output,
            )
    return output


def apply_audited_corrections(record: dict, translation: dict) -> dict:
    source = input_payload(record)
    corrected = dict(translation)
    for field in TRANSLATED_FIELDS:
        corrected[f"{field}_en"] = preserve_source_acronyms(
            source[field], corrected[f"{field}_en"]
        )
    if record["record_id"] in AUDITED_SOURCE_TEXT_OVERRIDES:
        corrected["source_text_en"] = AUDITED_SOURCE_TEXT_OVERRIDES[record["record_id"]]
    validate_translation(
        source,
        {
            "record_id": record["record_id"],
            **{f"{field}_en": corrected[f"{field}_en"] for field in TRANSLATED_FIELDS},
        },
    )
    return corrected


def compact_translations(records: list[dict]) -> None:
    """Keep one complete, most-recent translation per canonical record."""
    translations = load_existing()
    record_order = [record["record_id"] for record in records]
    missing = [record_id for record_id in record_order if record_id not in translations]
    assert not missing, f"Missing translations after generation: {missing[:5]}"
    rows = [
        apply_audited_corrections(record, translations[record["record_id"]])
        for record in records
    ]
    temporary_path = OUTPUT_PATH.with_suffix(".jsonl.tmp")
    with temporary_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    temporary_path.replace(OUTPUT_PATH)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=("openai", "argos"), default="openai")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--argos-package-dir", type=Path)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    records = canonical_records()
    source_by_id = {record["record_id"]: input_payload(record) for record in records}
    existing = load_existing()

    complete_existing = {
        record_id: row
        for record_id, row in existing.items()
        if all(f"{field}_en" in row for field in TRANSLATED_FIELDS)
    }

    for record_id, row in complete_existing.items():
        source = source_by_id[record_id]
        translated = {
            "record_id": record_id,
            **{f"{field}_en": row[f"{field}_en"] for field in TRANSLATED_FIELDS},
        }
        validate_translation(source, translated)

    if args.validate_only:
        print(
            json.dumps(
                {"valid_translations": len(complete_existing), "expected": len(records)},
                indent=2,
            )
        )
        return

    if args.backend == "openai":
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Set OPENAI_API_KEY before running translation")
        translator = OpenAI(api_key=api_key)
        model = args.model
        status = "generated"
    else:
        if not args.argos_package_dir:
            raise RuntimeError("--argos-package-dir is required for the Argos backend")
        translator = load_argos_translator(args.argos_package_dir)
        model = "argos-translate-pt_en-1.9"
        status = "machine_translated"

    pending = [
        record for record in records if record["record_id"] not in complete_existing
    ]
    if args.limit is not None:
        pending = pending[: args.limit]

    for start in range(0, len(pending), args.batch_size):
        batch = pending[start : start + args.batch_size]
        if args.backend == "openai":
            translated = translate_openai_batch(translator, model, batch)
        else:
            translated = translate_argos_batch(translator, batch)
        append_translations(translated, model, status)
        print(
            json.dumps(
                {
                    "translated": min(start + len(batch), len(pending)),
                    "this_run": len(pending),
                    "total_complete": len(complete_existing)
                    + min(start + len(batch), len(pending)),
                }
            ),
            flush=True,
        )

    if args.limit is None:
        compact_translations(records)


if __name__ == "__main__":
    main()
