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
)

TRANSLATED_FIELDS = (
    "source_text",
    "resources",
    "indicators",
    "monitoring_frequency",
    "source_notes",
    "section_or_table",
)

SYSTEM_PROMPT = """You translate Brazilian federal climate-policy records from Portuguese to English.

Requirements:
- Translate faithfully and completely. Do not summarize, explain, improve, or add information.
- Preserve identifiers, acronyms, programme names, institution names, numbers, years, percentages, and units.
- Preserve list length and item order exactly.
- Use clear policy English. Translate generic administrative terms, but retain official proper names in Portuguese where translating the name could create ambiguity.
- Return only a JSON object with a `translations` array.
- Each output item must contain exactly: record_id, source_text_en, resources_en, indicators_en, monitoring_frequency_en, source_notes_en, section_or_table_en.
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
    assert len(records) == 549, f"Expected 549 Portuguese-source records, found {len(records)}"
    return records


def input_payload(record: dict) -> dict:
    return {
        "record_id": record["record_id"],
        "source_text": record["source_text"],
        "resources": record.get("resources") or [],
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

    for record_id, row in existing.items():
        source = source_by_id[record_id]
        translated = {
            "record_id": record_id,
            **{f"{field}_en": row[f"{field}_en"] for field in TRANSLATED_FIELDS},
        }
        validate_translation(source, translated)

    if args.validate_only:
        print(json.dumps({"valid_translations": len(existing), "expected": len(records)}, indent=2))
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

    pending = [record for record in records if record["record_id"] not in existing]
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
                    "total_complete": len(existing) + min(start + len(batch), len(pending)),
                }
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
