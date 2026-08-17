#!/usr/bin/env python3
"""Extract the nine additional Plano Clima adaptation plans.

The extractor preserves Portuguese as the authoritative evidence, separates every
source-defined action identifier (including actions shared by several targets), and
retains physical PDF-page locators. It intentionally mirrors the record structure
used by ``policy_extraction.ipynb`` for the first seven sectoral/thematic plans.
"""

from __future__ import annotations

import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import pdfplumber


RELEASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = RELEASE_DIR / "sample" / "raw"
SAMPLE_DIR = RELEASE_DIR / "sample"
SCHEMA_PATH = RELEASE_DIR / "schemas" / "policy_record.schema.json"


CONFIGS = {
    "br-secadp-agricultura-pecuaria-2026": {
        "file": "br-secadp-agricultura-pecuaria-2026.pdf",
        "output": "agriculture_livestock_policy_records.jsonl",
        "policy_pages": range(43, 63),
        "indicator_pages": range(80, 82),
        "detail_pages": range(65, 78),
        "expected": (3, 8, 18),
    },
    "br-secadp-agricultura-familiar-2026": {
        "file": "br-secadp-agricultura-familiar-2026.pdf",
        "output": "family_farming_policy_records.jsonl",
        "policy_pages": range(30, 52),
        "indicator_pages": range(58, 73),
        "expected": (3, 87, 96),
    },
    "br-secadp-industria-mineracao-2026": {
        "file": "br-secadp-industria-mineracao-2026.pdf",
        "output": "industry_mining_policy_records.jsonl",
        "policy_pages": range(39, 48),
        "indicator_pages": range(52, 54),
        "expected": (3, 7, 23),
    },
    "br-secadp-igualdade-racial-2026": {
        "file": "br-secadp-igualdade-racial-2026.pdf",
        "output": "racial_equality_policy_records.jsonl",
        "policy_pages": range(31, 45),
        "indicator_pages": [49],
        "expected": (3, 7, 23),
    },
    "br-secadp-oceano-zona-costeira-2026": {
        "file": "br-secadp-oceano-zona-costeira-2026.pdf",
        "output": "ocean_coastal_zone_policy_records.jsonl",
        "policy_pages": range(43, 58),
        "indicator_pages": range(62, 65),
        "expected": (4, 20, 23),
    },
    "br-secadp-povos-comunidades-tradicionais-2026": {
        "file": "br-secadp-povos-comunidades-tradicionais-2026.pdf",
        "output": "traditional_peoples_communities_policy_records.jsonl",
        "policy_pages": range(26, 53),
        "indicator_pages": range(56, 59),
        "expected": (3, 9, 40),
    },
    "br-secadp-povos-indigenas-2026": {
        "file": "br-secadp-povos-indigenas-2026.pdf",
        "output": "indigenous_peoples_policy_records.jsonl",
        "policy_pages": range(32, 49),
        "indicator_pages": range(53, 55),
        "expected": (4, 17, 67),
    },
    "br-secadp-transportes-2026": {
        "file": "br-secadp-transportes-2026.pdf",
        "output": "transport_policy_records.jsonl",
        "policy_pages": range(57, 70),
        "indicator_pages": range(77, 83),
        "expected": (4, 33, 58),
    },
    "br-secadp-turismo-2026": {
        "file": "br-secadp-turismo-2026.pdf",
        "output": "tourism_policy_records.jsonl",
        "policy_pages": range(37, 51),
        "indicator_pages": range(55, 59),
        "expected": (3, 17, 47),
    },
}


ACTION_TOKEN = re.compile(
    r"(?<![A-Za-z0-9])A\s*(\d+)\s*\.?\s*M\s*(\d+)"
    r"(?:\s*[-–]\s*M?\s*(\d+))?\s*[.:-]?",
    re.IGNORECASE,
)
TARGET_TOKEN = re.compile(r"(?<![A-Za-z0-9])M\s*(\d+)\s*\.", re.IGNORECASE)
OBJECTIVE_TOKEN = re.compile(r"\b(O\d+)\.\s*", re.IGNORECASE)
OBJECTIVE_TEXT = re.compile(
    r"\b(O\d+)\.\s*(.+?)(?=\s+(?:Plano Plurianual\s*/|"
    r"Metas(?: relacionadas)?\s+Ações|Plano Clima Adaptação|O\d+\.)|$)",
    re.IGNORECASE,
)


def normalise(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalise_pdf_cell(value: str | None) -> str:
    """Join line-wrap hyphenation while retaining genuine source punctuation."""
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", value or "")
    return normalise(text)


def match_text(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"^M\s*\d+\s*\.?\s*", "", value, flags=re.IGNORECASE)
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def deadline_from_text(value: str) -> str | None:
    years = re.findall(r"\b20\d{2}\b", value or "")
    return max(years) if years else None


def record(
    *,
    record_id: str,
    document_id: str,
    record_type: str,
    native_id: str | None,
    parent_id: str | None,
    source_text: str,
    page: int,
    deadline: str | None = None,
    resources: list[str] | None = None,
    indicators: list[str] | None = None,
    notes: list[str] | None = None,
    related_objectives: list[str] | None = None,
    review_note: str | None = None,
    section_or_table: str | None = None,
) -> dict:
    return {
        "schema_version": "0.2.0",
        "record_id": record_id,
        "document_id": document_id,
        "record_type": record_type,
        "source_native_id": native_id,
        "parent_record_id": parent_id,
        "source_text": source_text,
        "analysis_summary_en": None,
        "deadline": deadline,
        "responsible_institutions": [],
        "resources": resources or [],
        "financing_evidence": [],
        "cost_evidence": [],
        "co_benefit_evidence": [],
        "indicators": indicators or [],
        "monitoring_frequency": None,
        "source_notes": notes or [],
        "related_objective_ids": related_objectives or [],
        "pdf_page_start": page,
        "pdf_page_end": page,
        "printed_page": str(page),
        "section_or_table": section_or_table,
        "evidence_status": "verified",
        "review_status": "proposed",
        "review_note": review_note,
    }


def header_index(table: list[list[str | None]], kind: str) -> int | None:
    for index, row in enumerate(table[:4]):
        header = match_text(" | ".join(cell or "" for cell in row))
        if kind == "policy" and "acoes" in header and "recurso" in header:
            return index
        if kind == "indicator" and "indicador" in header and "periodicidade" in header:
            return index
        if kind == "detail" and ("acao" in header or "acoes" in header) and "descricao" in header and "orgao" in header:
            return index
    return None


def target_parts(cell: str) -> list[tuple[str, str]]:
    text = normalise_pdf_cell(cell)
    matches = list(TARGET_TOKEN.finditer(text))
    if not matches:
        leading = re.match(r"^M\s*(\d+)\s+(.+)", text, flags=re.IGNORECASE)
        return [(f"M{int(leading.group(1))}", leading.group(2).strip())] if leading else []
    parts = []
    for index, found in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        parts.append((f"M{int(found.group(1))}", text[found.end() : end].strip(" .")))
    return parts


def action_parts(cell: str) -> list[tuple[str, str, list[str]]]:
    text = normalise_pdf_cell(cell)
    matches = list(ACTION_TOKEN.finditer(text))
    parts = []
    for index, found in enumerate(matches):
        action_number, target_start, target_end = found.groups()
        native_id = f"A{int(action_number)}.M{int(target_start)}"
        target_numbers = list(
            range(int(target_start), int(target_end) + 1)
            if target_end
            else [int(target_start)]
        )
        if target_end:
            native_id += f"-M{int(target_end)}"
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        wording = text[found.end() : end].strip(" .:-")
        parts.append((native_id, wording, [f"M{number}" for number in target_numbers]))
    return parts


def action_record_id(document_id: str, native_id: str) -> str:
    suffix = native_id.lower().replace(".", "-")
    return f"{document_id}:{suffix}"


def append_unique(values: list[str], value: str | None) -> None:
    value = normalise_pdf_cell(value)
    if value and value not in values:
        values.append(value)


def objective_context(page: pdfplumber.page.Page, table_top: float) -> str | None:
    candidates = []
    for hit in page.search(r"\bO\d+\.", regex=True, case=False):
        if hit["top"] <= table_top + 20:
            match = OBJECTIVE_TOKEN.search(hit["text"])
            if match:
                candidates.append((hit["top"], match.group(1).upper()))
    return max(candidates)[1] if candidates else None


def closest_target(target_text: str, targets: dict[str, dict]) -> tuple[str, float]:
    needle = match_text(target_text)
    scores = []
    for target_id, target in targets.items():
        candidate = match_text(target["source_text"])
        if needle == candidate:
            return target_id, 1.0
        scores.append((SequenceMatcher(None, needle, candidate).ratio(), target_id))
    score, target_id = max(scores)
    return target_id, score


def validate_record(item: dict, schema: dict) -> list[str]:
    errors = []
    missing = set(schema["required"]) - set(item)
    extra = set(item) - set(schema["properties"])
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")
    if extra:
        errors.append(f"unexpected fields: {sorted(extra)}")
    if item.get("schema_version") != "0.2.0":
        errors.append("invalid schema_version")
    if item.get("record_type") not in schema["properties"]["record_type"]["enum"]:
        errors.append("invalid record_type")
    if item.get("evidence_status") not in schema["properties"]["evidence_status"]["enum"]:
        errors.append("invalid evidence_status")
    if item.get("review_status") not in schema["properties"]["review_status"]["enum"]:
        errors.append("invalid review_status")
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
        value = item.get(field)
        if not isinstance(value, list) or any(not isinstance(entry, str) or not entry for entry in value):
            errors.append(f"invalid {field}")
        elif len(value) != len(set(value)):
            errors.append(f"duplicate {field}")
    for field in ("pdf_page_start", "pdf_page_end"):
        if not isinstance(item.get(field), int) or item[field] < 1:
            errors.append(f"invalid {field}")
    return errors


def extract_document(document_id: str, config: dict, schema: dict) -> dict:
    path = RAW_DIR / config["file"]
    records: dict[str, dict] = {}
    targets: dict[str, dict] = {}
    actions: dict[str, dict] = {}
    objective_wording: dict[str, tuple[str, int, list[str]]] = {}
    rejected_action_cells: list[tuple[int, str]] = []
    current_objective: str | None = None

    with pdfplumber.open(path) as pdf:
        # Extract objective wording once, independently of table geometry.
        for page_number in config["policy_pages"]:
            page_text = normalise(pdf.pages[page_number - 1].extract_text())
            for found in OBJECTIVE_TEXT.finditer(page_text):
                objective_id = found.group(1).upper()
                wording = re.sub(r"\s+Metas$", "", found.group(2)).strip(" .")
                if 20 <= len(wording) <= 1200:
                    objective_wording.setdefault(
                        objective_id,
                        (wording, page_number, sorted(set(re.findall(r"\bON\d+\b", page_text)))),
                    )

        for objective_id, (wording, page_number, related) in objective_wording.items():
            item = record(
                record_id=f"{document_id}:{objective_id.lower()}",
                document_id=document_id,
                record_type="objective",
                native_id=objective_id,
                parent_id=None,
                source_text=wording,
                page=page_number,
                related_objectives=related,
                section_or_table="Objetivos setoriais ou temáticos / Metas / Ações",
            )
            records[item["record_id"]] = item

        # Extract targets and split every source-defined action token in policy tables.
        for page_number in config["policy_pages"]:
            page = pdf.pages[page_number - 1]
            for found_table in page.find_tables():
                table = found_table.extract()
                start = header_index(table, "policy")
                if start is None:
                    continue
                prefix = " ".join(
                    normalise_pdf_cell(cell)
                    for row in table[:start]
                    for cell in row
                    if cell
                )
                prefix_objective = OBJECTIVE_TOKEN.search(prefix)
                table_objective = (
                    prefix_objective.group(1).upper()
                    if prefix_objective
                    else objective_context(page, found_table.bbox[1])
                )
                if table_objective:
                    current_objective = table_objective
                current_targets: list[str] = []

                for row in table[start + 1 :]:
                    if len(row) < 2:
                        continue
                    if row[0]:
                        parsed_targets = target_parts(row[0])
                        if parsed_targets:
                            current_targets = [native for native, _ in parsed_targets]
                        for native_id, wording in parsed_targets:
                            target_id = f"{document_id}:{native_id.lower()}"
                            parent_id = (
                                f"{document_id}:{current_objective.lower()}"
                                if current_objective and f"{document_id}:{current_objective.lower()}" in records
                                else None
                            )
                            if target_id not in targets:
                                target = record(
                                    record_id=target_id,
                                    document_id=document_id,
                                    record_type="target",
                                    native_id=native_id,
                                    parent_id=parent_id,
                                    source_text=wording,
                                    page=page_number,
                                    deadline=deadline_from_text(wording),
                                    section_or_table="Metas / Ações / Fonte do recurso",
                                    review_note=(
                                        None
                                        if parent_id
                                        else "No single sector/thematic objective was assigned automatically; review the source table heading."
                                    ),
                                )
                                targets[target_id] = target
                                records[target_id] = target
                            else:
                                targets[target_id]["pdf_page_end"] = max(
                                    targets[target_id]["pdf_page_end"], page_number
                                )

                    action_cell = row[1] or ""
                    parsed_actions = action_parts(action_cell)
                    if action_cell and not parsed_actions and match_text(action_cell) not in {"acoes", "acao"}:
                        rejected_action_cells.append((page_number, normalise_pdf_cell(action_cell)))
                    description = row[2] if len(row) >= 4 else None
                    resource_text = row[-1] if len(row) >= 3 else None

                    for native_id, wording, linked_targets in parsed_actions:
                        action_id = action_record_id(document_id, native_id)
                        parent_native = linked_targets[0] if linked_targets else (current_targets[0] if current_targets else None)
                        parent_id = f"{document_id}:{parent_native.lower()}" if parent_native else None
                        range_note = None
                        if len(linked_targets) > 1:
                            range_note = (
                                f"The source links this action to targets {', '.join(linked_targets)}; "
                                f"parent_record_id uses {linked_targets[0]} and the full source range is retained in source_native_id."
                            )
                        if action_id not in actions:
                            action = record(
                                record_id=action_id,
                                document_id=document_id,
                                record_type="action",
                                native_id=native_id,
                                parent_id=parent_id,
                                source_text=wording,
                                page=page_number,
                                deadline=deadline_from_text(wording),
                                resources=[normalise_pdf_cell(resource_text)] if normalise_pdf_cell(resource_text) else [],
                                notes=[normalise_pdf_cell(description)] if normalise_pdf_cell(description) else [],
                                review_note=range_note,
                                section_or_table="Metas / Ações / Fonte do recurso",
                            )
                            actions[action_id] = action
                            records[action_id] = action
                        else:
                            existing = actions[action_id]
                            if wording and wording != existing["source_text"] and wording not in existing["source_text"]:
                                existing["source_text"] = normalise(f"{existing['source_text']} {wording}")
                                existing["review_note"] = normalise(
                                    f"{existing.get('review_note') or ''} The source action continues across table rows or pages; fragments are joined in page order."
                                )
                            append_unique(existing["resources"], resource_text)
                            append_unique(existing["source_notes"], description)
                            existing["pdf_page_end"] = max(existing["pdf_page_end"], page_number)

        # Attach target indicators and frequencies. Some tables omit target IDs;
        # those rows are matched back to exact/fuzzy target wording conservatively.
        unmatched_indicator_rows = []
        for page_number in config["indicator_pages"]:
            page = pdf.pages[page_number - 1]
            for table in page.extract_tables():
                start = header_index(table, "indicator")
                if start is None:
                    continue
                for row in table[start + 1 :]:
                    if len(row) < 2 or not row[0]:
                        continue
                    header_like = match_text(" ".join(cell or "" for cell in row))
                    if "indicadores das metas" in header_like or header_like in {"metas", "meta"}:
                        continue
                    parsed = target_parts(row[0])
                    target_ids = [f"{document_id}:{native.lower()}" for native, _ in parsed]
                    if not target_ids:
                        target_id, score = closest_target(normalise_pdf_cell(row[0]), targets)
                        if score < 0.78:
                            unmatched_indicator_rows.append((page_number, score, normalise_pdf_cell(row[0])))
                            continue
                        target_ids = [target_id]
                    for target_id in target_ids:
                        if target_id not in targets:
                            unmatched_indicator_rows.append((page_number, 0.0, normalise_pdf_cell(row[0])))
                            continue
                        target = targets[target_id]
                        append_unique(target["indicators"], row[1])
                        frequency = normalise_pdf_cell(row[-1]) if len(row) >= 3 else ""
                        if frequency:
                            target["monitoring_frequency"] = frequency
                        if len(row) == 4 and row[2]:
                            append_unique(target["source_notes"], f"Fórmula de cálculo: {normalise_pdf_cell(row[2])}")

        # Agriculture and livestock uniquely provides an action-detail table with
        # action-level descriptions, indicators, institutions and execution dates.
        missing_detail_actions = []
        for page_number in config.get("detail_pages", []):
            for table in pdf.pages[page_number - 1].extract_tables():
                start = header_index(table, "detail")
                if start is None:
                    continue
                for row in table[start + 1 :]:
                    if len(row) < 5 or not row[0]:
                        continue
                    parsed = action_parts(row[0])
                    if not parsed:
                        continue
                    for native_id, _, _ in parsed:
                        action_id = action_record_id(document_id, native_id)
                        if action_id not in actions:
                            missing_detail_actions.append((page_number, native_id))
                            continue
                        action = actions[action_id]
                        append_unique(action["source_notes"], row[1])
                        append_unique(action["indicators"], row[2])
                        append_unique(action["responsible_institutions"], row[3])
                        timing = normalise_pdf_cell(row[4])
                        if timing:
                            append_unique(action["source_notes"], f"Prazo de execução e observações: {timing}")
                            action["deadline"] = deadline_from_text(timing) or action["deadline"]
                        action["pdf_page_end"] = max(action["pdf_page_end"], page_number)

    expected_objectives, expected_targets, expected_actions = config["expected"]
    counts = {
        "objectives": sum(item["record_type"] == "objective" for item in records.values()),
        "targets": len(targets),
        "actions": len(actions),
    }
    assert counts == {
        "objectives": expected_objectives,
        "targets": expected_targets,
        "actions": expected_actions,
    }, f"{document_id}: count mismatch {counts}"
    assert not rejected_action_cells, f"{document_id}: unparsed action cells {rejected_action_cells[:5]}"
    assert not unmatched_indicator_rows, f"{document_id}: unmatched indicator rows {unmatched_indicator_rows[:5]}"
    assert not missing_detail_actions, f"{document_id}: unmatched action details {missing_detail_actions[:5]}"
    targets_without_indicators = [target["source_native_id"] for target in targets.values() if not target["indicators"]]
    targets_without_frequency = [target["source_native_id"] for target in targets.values() if not target["monitoring_frequency"]]
    assert not targets_without_indicators, f"{document_id}: targets without indicators {targets_without_indicators}"
    assert not targets_without_frequency, f"{document_id}: targets without frequency {targets_without_frequency}"
    assert all(action["parent_record_id"] in targets for action in actions.values()), f"{document_id}: actions without target parent"

    ordered = sorted(
        records.values(),
        key=lambda item: (
            item["pdf_page_start"],
            {"objective": 0, "target": 1, "action": 2}.get(item["record_type"], 3),
            item["record_id"],
        ),
    )
    errors = [
        f"{item['record_id']}: {error}"
        for item in ordered
        for error in validate_record(item, schema)
    ]
    assert not errors, errors[:10]
    assert len(ordered) == len({item["record_id"] for item in ordered})

    output_path = SAMPLE_DIR / config["output"]
    output_path.write_text(
        "\n".join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in ordered) + "\n",
        encoding="utf-8",
    )
    return {
        **counts,
        "records": len(ordered),
        "targets_with_indicators": sum(bool(item["indicators"]) for item in targets.values()),
        "actions_with_structured_institutions": sum(bool(item["responsible_institutions"]) for item in actions.values()),
        "output": str(output_path.relative_to(RELEASE_DIR)),
    }


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    results = {
        document_id: extract_document(document_id, config, schema)
        for document_id, config in CONFIGS.items()
    }
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
