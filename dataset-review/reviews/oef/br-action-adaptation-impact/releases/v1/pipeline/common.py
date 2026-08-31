"""Small shared helpers for the numbered CSV pipeline."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive" / "working"
INPUT = ROOT / "data" / "input"
REFERENCE = ROOT / "data" / "reference"
OUTPUT = ROOT / "data" / "output"

DOCUMENT_COLUMNS = [
    "document_id", "document_title", "retrieval_status", "local_pdf", "sha256",
    "page_count", "text_file", "extraction_status", "extracted_page_count",
    "pages_with_text", "text_characters", "extraction_tool", "extracted_at",
    "extraction_note",
]
MAPPING_COLUMNS = [
    "mapping_id", "action_id", "sector", "component", "eligibility",
    "eligibility_rationale", "screening_status", "effectiveness_class",
    "source_sufficiency", "time_horizon", "maladaptation_flag",
    "parameters_version", "evidence_review_status", "match_run_id",
    "assessment_basis", "review_status", "reviewed_by", "reviewed_at", "review_note",
]
SCREENING_COLUMNS = [
    "mapping_id", "source_id", "screening_status", "evidence_record_count",
    "review_status", "reviewed_by", "reviewed_at", "review_note",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, columns: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def split_ids(value: str) -> list[str]:
    return list(dict.fromkeys(item.strip() for item in value.split("|") if item.strip()))


def as_bool(value: object) -> bool:
    if value in (True, "true", "1", 1):
        return True
    if value in (False, "false", "0", "", 0, None):
        return False
    raise ValueError(f"Invalid boolean: {value}")


def stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:16]
    return f"{prefix}_{digest}"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def require_unique(rows: list[dict[str, str]], key: str, label: str) -> None:
    values = [row[key] for row in rows]
    require(len(values) == len(set(values)), f"Duplicate {key} in {label}")
