#!/usr/bin/env python3
"""Audit completeness and source alignment of policy-record translations."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from translate_policy_records import (
    CANONICAL_FILES,
    OUTPUT_PATH,
    SAMPLE_DIR,
    TRANSLATED_FIELDS,
    digit_tokens,
    input_payload,
    read_jsonl,
)


PORTUGUESE_MARKERS = {
    "ação", "ações", "adaptação", "ampliar", "aos", "das", "desenvolvimento",
    "em", "fortalecer", "gestão", "mudança", "para", "por", "promover", "que",
}
ENGLISH_MARKERS = {
    "action", "actions", "adaptation", "and", "climate", "development", "for",
    "management", "of", "promote", "strengthen", "the", "to", "with",
}
GLOSSARY = (
    (re.compile(r"adapta", re.I), ("adapt",)),
    (
        re.compile(r"mudan(?:ça|ças) (?:do )?clima", re.I),
        ("climate change", "climate-resilient"),
    ),
    (re.compile(r"climátic", re.I), ("climat", "weather")),
    (re.compile(r"\brisc", re.I), ("risk",)),
    (re.compile(r"resili", re.I), ("resili",)),
    (re.compile(r"vulner", re.I), ("vulner",)),
    (re.compile(r"incênd|queimad", re.I), ("fire", "burn", "wildfire")),
    (re.compile(r"inunda|alagament", re.I), ("flood",)),
    (re.compile(r"seca|estiagem", re.I), ("drought", "dry")),
    (re.compile(r"\bágua|\bhídric", re.I), ("water", "hydro", "água")),
    (re.compile(r"saúde", re.I), ("health",)),
    (re.compile(r"agricult", re.I), ("agric", "farm")),
    (re.compile(r"indígen", re.I), ("indigenous",)),
    (re.compile(r"turismo|turístic", re.I), ("touris",)),
    (re.compile(r"transport", re.I), ("transport",)),
    (re.compile(r"biodivers", re.I), ("biodivers",)),
)
ACRONYM_RE = re.compile(r"(?<![\w-])[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{2,}(?:\+)?(?![\w-])")
ACRONYM_STOP = {"DA", "DAS", "DE", "DO", "DOS", "E", "EM", "NA", "NAS", "NO", "NOS"}


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-záéíóúâêôãõç]+", text.casefold()))


def main() -> None:
    source_records = []
    for filename in CANONICAL_FILES:
        source_records.extend(read_jsonl(SAMPLE_DIR / filename))
    source_by_id = {record["record_id"]: input_payload(record) for record in source_records}
    translations = read_jsonl(OUTPUT_PATH)
    translation_by_id = {row["record_id"]: row for row in translations}

    critical: list[dict] = []
    warnings: list[dict] = []
    source_ids = set(source_by_id)
    translated_ids = set(translation_by_id)
    for record_id in sorted(source_ids - translated_ids):
        critical.append({"record_id": record_id, "issue": "missing_translation_record"})
    for record_id in sorted(translated_ids - source_ids):
        critical.append({"record_id": record_id, "issue": "unexpected_translation_record"})

    for record_id in sorted(source_ids & translated_ids):
        source = source_by_id[record_id]
        translated = translation_by_id[record_id]
        for field in TRANSLATED_FIELDS:
            output_field = f"{field}_en"
            if output_field not in translated:
                critical.append({"record_id": record_id, "field": output_field, "issue": "missing_field"})
                continue
            source_value = source[field]
            output_value = translated[output_field]
            if type(output_value) is not type(source_value):
                critical.append({"record_id": record_id, "field": output_field, "issue": "type_changed"})
                continue
            if isinstance(source_value, list) and len(source_value) != len(output_value):
                critical.append({"record_id": record_id, "field": output_field, "issue": "list_length_changed"})
            if source_value and not output_value:
                critical.append({"record_id": record_id, "field": output_field, "issue": "translation_blank"})
            if digit_tokens(source_value) != digit_tokens(output_value):
                critical.append({"record_id": record_id, "field": output_field, "issue": "numeric_content_changed"})

        source_text = source["source_text"]
        english_text = translated.get("source_text_en", "")
        if not english_text:
            continue
        if "ZXNUMBER" in english_text:
            critical.append({"record_id": record_id, "field": "source_text_en", "issue": "numeric_placeholder_leaked"})
        source_words = tokens(source_text)
        english_words = tokens(english_text)
        pt_score = len(english_words & PORTUGUESE_MARKERS)
        en_score = len(english_words & ENGLISH_MARKERS)
        if len(english_words) >= 8 and pt_score >= 3 and pt_score > en_score:
            warnings.append({"record_id": record_id, "issue": "target_may_still_be_portuguese"})
        source_letters = len(re.findall(r"[A-Za-zÀ-ÿ]", source_text))
        english_letters = len(re.findall(r"[A-Za-z]", english_text))
        if source_letters >= 30:
            ratio = english_letters / source_letters
            if ratio < 0.45 or ratio > 2.2:
                warnings.append({"record_id": record_id, "issue": "unusual_length_ratio", "ratio": round(ratio, 3)})
            if source_text.casefold() == english_text.casefold():
                warnings.append({"record_id": record_id, "issue": "translation_unchanged"})
        for pattern, expected_terms in GLOSSARY:
            if pattern.search(source_text) and not any(term in english_text.casefold() for term in expected_terms):
                warnings.append({"record_id": record_id, "issue": "glossary_concept_missing", "source_pattern": pattern.pattern})
        source_acronyms = {value for value in ACRONYM_RE.findall(source_text) if value not in ACRONYM_STOP}
        for acronym in sorted(source_acronyms):
            if acronym not in english_text:
                warnings.append({"record_id": record_id, "issue": "acronym_missing", "acronym": acronym})

    report = {
        "source_records": len(source_records),
        "translation_rows": len(translations),
        "unique_translation_records": len(translation_by_id),
        "critical_issue_count": len(critical),
        "warning_count": len(warnings),
        "critical_by_issue": dict(Counter(item["issue"] for item in critical)),
        "warnings_by_issue": dict(Counter(item["issue"] for item in warnings)),
        "critical_examples": critical[:25],
        "warning_examples": warnings[:50],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(1 if critical else 0)


if __name__ == "__main__":
    main()
