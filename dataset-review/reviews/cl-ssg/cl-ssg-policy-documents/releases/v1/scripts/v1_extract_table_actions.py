#!/usr/bin/env python3
"""Supplement atom files with verbatim actions found in policy tables.

This deliberately does not use an LLM.  It identifies action names in two
common PDF-to-text patterns: measure cards (``Nombre de Medida`` / ``Nombre
iniciativa``) and numbered action tables (``N° / Nombre Medida``).  Each
accepted value is copied directly from the source markdown, resolved with the
same verifier used by the main atomizer, and appended only when no existing
action starts at the same source offset.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import v1_common as ef

V1 = Path(__file__).resolve().parents[1]
MARKDOWN_DIR = V1 / "data" / "markdown"
ATOMS_DIR = V1 / "data" / "atoms"

PAGE_RE = re.compile(r"(?=<!-- page_break: \d+ -->)")
CARD_LABEL_RE = re.compile(
    r"(?i)(?:\d+\.\s*)?Nombre\s+(?:de\s+)?(?:la\s+)?(?:medida|iniciativa)\s*(.*)$"
)
ROW_RE = re.compile(r"(?m)^\s*(\d{1,3})\s{2,}(.{16,500}?)(?:\s{2,}|$)")
TABLE_CUE_RE = re.compile(
    r"(?i)ficha\s+de\s+medida|lista\s+larga\s+de\s+medidas|"
    r"nombre\s+(?:de\s+)?(?:la\s+)?medida|nombre\s+iniciativa|"
    r"acciones\s+y\s+asignación|matriz\s+de\s+acciones"
)


def clean_candidate(value: str) -> str:
    """Keep a compact, literal action name; reject labels and table debris."""
    value = value.strip()
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"^(?:Descripción|Código|N°)\s*[:.\-]*\s*", "", value, flags=re.I)
    if len(value) < 12 or len(value) > 360:
        return ""
    if re.fullmatch(r"[\d\W_]+", value):
        return ""
    label_check = re.sub(r"^\d+(?:\.\d+)*\.\s*", "", value).lower()
    if label_check.startswith((
        "objetivo", "fuente", "financiamiento", "responsables", "tipo de medida",
        "unidad técnica", "lineamiento", "descripción", "indicador", "meta",
    )):
        return ""
    if len(value.split()) < 3:
        return ""
    return value


def candidates(text: str) -> list[str]:
    found: list[str] = []
    for page in PAGE_RE.split(text):
        if not TABLE_CUE_RE.search(page):
            continue
        lines = page.splitlines()
        for index, line in enumerate(lines):
            match = CARD_LABEL_RE.search(line)
            if not match:
                continue
            # Tables often leave a large visual gap between the field label and
            # its value.  Prefer the text after the label; otherwise take the
            # next substantive line, which remains an exact source substring.
            item = clean_candidate(match.group(1))
            if not item:
                for following in lines[index + 1:index + 4]:
                    item = clean_candidate(following)
                    if item:
                        break
            if item:
                found.append(item)
        # Numbered measure rows are only considered on pages explicitly marked
        # as lists/matrices/fichas, avoiding ordinary numbered prose.
        for match in ROW_RE.finditer(page):
            item = clean_candidate(match.group(2))
            if item:
                found.append(item)
    return list(dict.fromkeys(found))


def next_atom_number(atoms: list[dict]) -> int:
    numbers = []
    for atom in atoms:
        tail = str(atom.get("atom_id", "")).rsplit("_a_", 1)
        if len(tail) == 2 and tail[1].isdigit():
            numbers.append(int(tail[1]))
    return max(numbers, default=-1) + 1


def supplement(doc_id: str, *, markdown_dir: Path, atoms_dir: Path) -> tuple[int, int]:
    document = ef.load_document(markdown_dir, doc_id)
    atom_path = atoms_dir / f"{doc_id}.jsonl"
    atoms = (
        [json.loads(line) for line in atom_path.read_text(encoding="utf-8").splitlines() if line]
        if atom_path.exists()
        else []
    )
    action_offsets = {
        atom.get("evidence_offset")
        for atom in atoms
        if atom.get("primitive_type") == "action" and atom.get("evidence_offset") is not None
    }
    sequence = next_atom_number(atoms)
    added = 0
    unresolved = 0
    for candidate in candidates(document.text):
        offset = document.find_verbatim(candidate)
        if offset is None:
            unresolved += 1
            continue
        if offset in action_offsets:
            continue
        atom = {
            "schema_version": "1.0.0",
            "atom_id": f"{doc_id}_a_{sequence:04d}",
            "source_document_id": doc_id,
            "primitive_type": "action",
            "evidence_text": candidate,
            "evidence_offset": offset,
            "atom_summary": f"Table-listed action: {candidate}",
            "sector_tags": ["cross_cutting"],
            "applicability_scope": "",
            "measure_type": "unknown",
            "explicitness": "explicit",
            "primitive_relation_hint": "commits",
            "extraction_metadata": {"method": "deterministic_table_action_v1"},
        }
        page = document.page_for_offset(offset)
        if page is not None:
            atom["page"] = page
        section = document.section_for_offset(offset)
        if section:
            atom["section"] = section
        atoms.append(atom)
        action_offsets.add(offset)
        sequence += 1
        added += 1
    atom_path.write_text(
        "".join(json.dumps(atom, ensure_ascii=False) + "\n" for atom in atoms),
        encoding="utf-8",
    )
    return added, unresolved


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", action="append", required=True)
    parser.add_argument("--markdown-dir", type=Path, default=MARKDOWN_DIR)
    parser.add_argument("--atoms-dir", type=Path, default=ATOMS_DIR)
    args = parser.parse_args()
    for doc_id in args.doc:
        added, unresolved = supplement(doc_id, markdown_dir=args.markdown_dir, atoms_dir=args.atoms_dir)
        print(f"{doc_id}: added={added} unresolved={unresolved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
