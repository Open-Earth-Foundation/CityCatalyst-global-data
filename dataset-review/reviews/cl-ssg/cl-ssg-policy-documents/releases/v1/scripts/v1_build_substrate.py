#!/usr/bin/env python3
"""Build v1 substrate artifacts from confirmed PDF mappings.

Dependencies (install in your environment):
  pip install pymupdf pymupdf4llm pyyaml

This script is fully self-contained under `v1/`:
  - root anchor: V1_ROOT = Path(__file__).resolve().parent.parent
  - mapping CSV: v1/data/source_pdf_map.csv
  - registry: v1/data/registry/source_documents.json
  - outputs: v1/data/markdown/<source_document_id>/
  - source PDFs: paths in mapping CSV are resolved as V1-relative
    (e.g. `policy-pdf/Plan_de_Mitigación_Sector_Agricultura.pdf`)

This script implements Stage 1 of the v1 pipeline:
  - convert: PDF -> page-marked markdown + section/skip map
  - inspect: human-readable summary for one source_document_id
  - verify: consistency + sha drift checks for generated artifacts
  - map: rebuild proposed PDF suggestions for unmapped IDs
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

V1_ROOT = Path(__file__).resolve().parent.parent
LOW_TEXT_THRESHOLD = 50
FRONT_MATTER_SECTION = "[front matter]"
RUNNING_HEADER_SINGLE_WORDS = {"annex", "anexo", "page", "pagina", "página", "capitulo", "capítulo"}
CHUNK_SIZE_PAGES = 20
MAP_PROTECTED_STATUSES = {"confirmed", "missing_source"}

SKIP_PATTERNS_DEFAULT: list[tuple[str, str]] = [
    ("procurement", r"\bprocurement\b|\badquisiciones?\b"),
    ("financial_mgmt", r"\bfinancial management\b|\bgesti[oó]n financiera\b"),
    ("legal", r"\blegal covenants?\b|\bconvenios? legales?\b|\bdisposiciones? legales?\b"),
    ("safeguard", r"\bsafeguard policies?\b|\bsalvaguardas?\b"),
    (
        "annex_admin",
        r"\b(annex|anexo)\s+\d+\b.*(procurement|financial|implementation arrangements|gender|"
        r"safeguard|fiduciary|adquisiciones|gesti[oó]n financiera|salvaguardas?|g[eé]nero|fiduciario)",
    ),
    ("toc", r"\btable of contents\b|\b[ií]ndice\b|\btabla de contenidos?\b"),
    ("abbreviations", r"\babbreviations?\b|\bacronyms?\b|\babreviaturas?\b|\bsiglas?\b|\bacr[oó]nimos?\b"),
    ("glossary", r"\bglossary\b|\bglosario\b"),
    ("references", r"\breferences?\b|\bbibliography\b|\bbibliograf[ií]a\b|\breferencias?\b"),
    ("gender_annex", r"\bgender action plan\b|\bplan de acci[oó]n de g[eé]nero\b"),
]


@dataclass
class PageInfo:
    page: int
    markdown: str
    char_count: int
    word_count: int
    is_low_text: bool
    headings: list[str]
    current_section: str
    skip: bool
    skip_reason: str | None


@dataclass
class ConvertResult:
    source_document_id: str
    pages: int
    skipped: int
    top_skip_reason: str
    low_text_pages: list[int]
    status: str


def load_fitz():
    try:
        import fitz as pymupdf  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("PyMuPDF is required. Install with: pip install pymupdf") from exc
    return pymupdf


def load_pymupdf4llm():
    try:
        import pymupdf4llm  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("pymupdf4llm is required. Install with: pip install pymupdf4llm") from exc
    return pymupdf4llm


def resolve_root(root_arg: str | None) -> Path:
    return Path(root_arg).resolve() if root_arg else V1_ROOT


def resolve_under_root(root: Path, path_value: str) -> Path:
    candidate = Path(path_value)
    return candidate if candidate.is_absolute() else root / candidate


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(65536)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def load_registry(registry_path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    docs = payload.get("source_documents", [])
    return {doc["source_document_id"]: doc for doc in docs if isinstance(doc, dict) and doc.get("source_document_id")}


def read_rows(map_csv: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with map_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append({k: (v or "").strip() for k, v in row.items() if k})
    return rows


def read_confirmed_rows(map_csv: Path, only: str | None = None) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_rows(map_csv):
        source_id = row.get("source_document_id", "")
        status = row.get("status", "")
        if status != "confirmed":
            continue
        if only and source_id != only:
            continue
        rows.append(
            {
                "source_document_id": source_id,
                "proposed_pdf_path": row.get("proposed_pdf_path", ""),
                "status": status,
            }
        )
    return rows


def load_patterns_file(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".json"}:
        payload = json.loads(text)
    else:
        try:
            import yaml  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("YAML patterns require PyYAML. Install with: pip install pyyaml") from exc
        payload = yaml.safe_load(text)
    if not isinstance(payload, list):
        raise ValueError("Pattern file must be a list of [name, regex] entries.")
    patterns: list[tuple[str, str]] = []
    for idx, item in enumerate(payload):
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise ValueError(f"Invalid pattern at index {idx}; expected [name, regex].")
        name, pattern = item
        if not isinstance(name, str) or not isinstance(pattern, str):
            raise ValueError(f"Invalid pattern at index {idx}; name/regex must be strings.")
        patterns.append((name, pattern))
    return patterns


def compile_skip_patterns(
    skip_patterns_path: Path | None,
    extra_skip_patterns_path: Path | None,
    no_skip_patterns: bool,
) -> list[tuple[str, re.Pattern[str]]]:
    if no_skip_patterns:
        return []
    raw_patterns = list(SKIP_PATTERNS_DEFAULT)
    if skip_patterns_path:
        raw_patterns = load_patterns_file(skip_patterns_path)
    if extra_skip_patterns_path:
        raw_patterns.extend(load_patterns_file(extra_skip_patterns_path))
    compiled: list[tuple[str, re.Pattern[str]]] = []
    for name, pattern in raw_patterns:
        compiled.append((name, re.compile(pattern, flags=re.IGNORECASE)))
    return compiled


def extract_heading_lines(page_markdown: str) -> list[str]:
    heading_lines: list[str] = []
    for line in page_markdown.splitlines():
        match = re.match(r"^#{1,4}\s+(.+)$", line.strip())
        if match:
            text = match.group(1).strip()
            if text:
                heading_lines.append(text)
    return heading_lines


def join_multiline_headings(heading_lines: list[str]) -> list[str]:
    if not heading_lines:
        return []
    combined: list[str] = []
    current = heading_lines[0]
    for idx in range(1, len(heading_lines)):
        prev = heading_lines[idx - 1]
        nxt = heading_lines[idx]
        if prev.endswith(("-", ":", "(", "—")):
            current = f"{current.rstrip('-: (—')} {nxt}".strip()
        elif re.match(r"^[a-záéíóúñü]", nxt):
            current = f"{current} {nxt}".strip()
        else:
            combined.append(current.strip())
            current = nxt
    combined.append(current.strip())
    return combined


def is_qualifying_heading(heading: str) -> bool:
    words = [word for word in re.split(r"\s+", heading.strip()) if word]
    if len(words) < 2:
        return False
    if len(words) == 1 and words[0].casefold() in RUNNING_HEADER_SINGLE_WORDS:
        return False
    return True


def update_current_section(current_section: str, page_headings: list[str]) -> str:
    new_section = current_section
    for heading in page_headings:
        if is_qualifying_heading(heading):
            new_section = heading
    return new_section


def match_skip_reason(current_section: str, patterns: list[tuple[str, re.Pattern[str]]]) -> str | None:
    for name, pattern in patterns:
        if pattern.search(current_section):
            return name
    return None


def split_markdown_pages(markdown_text: str) -> list[tuple[int, str]]:
    pattern = re.compile(r"<!--\s*page_break:\s*(\d+)\s*-->")
    matches = list(pattern.finditer(markdown_text))
    if not matches:
        return []
    chunks: list[tuple[int, str]] = []
    for idx, match in enumerate(matches):
        page = int(match.group(1))
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(markdown_text)
        page_text = markdown_text[start:end].lstrip("\n")
        chunks.append((page, page_text))
    return chunks


def markdown_from_doc_chunk(
    pymupdf4llm: Any,
    doc: Any,
    pages_zero_based: list[int],
) -> str:
    try:
        return pymupdf4llm.to_markdown(doc, pages=pages_zero_based)
    except TypeError:
        return pymupdf4llm.to_markdown(doc, page_numbers=pages_zero_based)


def extract_pdf_markdown_pages(pdf_path: Path) -> tuple[list[tuple[int, str]], int, str]:
    fitz = load_fitz()
    pymupdf4llm = load_pymupdf4llm()
    doc = fitz.open(pdf_path)
    try:
        if doc.is_encrypted and not doc.authenticate(""):
            return [], 0, "encrypted"
        page_count = doc.page_count
        chunks: list[tuple[int, str]] = []
        for chunk_start in range(0, page_count, CHUNK_SIZE_PAGES):
            chunk_end = min(chunk_start + CHUNK_SIZE_PAGES, page_count)
            page_ids = list(range(chunk_start, chunk_end))
            chunk_markdown = markdown_from_doc_chunk(pymupdf4llm, doc, page_ids)
            chunk_pages = split_markdown_pages(chunk_markdown)
            chunk_has_text = any(text.strip() for _, text in chunk_pages)
            if not chunk_pages or not chunk_has_text:
                # Some pymupdf4llm versions return chunk markdown without page markers.
                # Others emit page markers but blank page content.
                # Fall back to single-page conversion to avoid silently writing blank pages.
                for page_zero in page_ids:
                    page_markdown = markdown_from_doc_chunk(pymupdf4llm, doc, [page_zero])
                    single_page_chunks = split_markdown_pages(page_markdown)
                    if single_page_chunks:
                        chunks.append((page_zero + 1, single_page_chunks[0][1]))
                    else:
                        chunks.append((page_zero + 1, page_markdown.strip()))
                continue
            chunks.extend(chunk_pages)
        chunks.sort(key=lambda item: item[0])
        dedup: dict[int, str] = {}
        for page, text in chunks:
            dedup[page] = text
        ordered = [(page, dedup.get(page, "")) for page in range(1, page_count + 1)]
        return ordered, page_count, ""
    finally:
        doc.close()


def build_page_infos(
    page_markdown: list[tuple[int, str]],
    patterns: list[tuple[str, re.Pattern[str]]],
) -> list[PageInfo]:
    infos: list[PageInfo] = []
    current_section = FRONT_MATTER_SECTION
    for page, markdown in page_markdown:
        heading_lines = extract_heading_lines(markdown)
        headings = join_multiline_headings(heading_lines)
        current_section = update_current_section(current_section, headings)
        skip_reason = match_skip_reason(current_section, patterns)
        char_count = len(markdown)
        word_count = len(re.findall(r"\S+", markdown))
        infos.append(
            PageInfo(
                page=page,
                markdown=markdown,
                char_count=char_count,
                word_count=word_count,
                is_low_text=char_count < LOW_TEXT_THRESHOLD,
                headings=headings,
                current_section=current_section,
                skip=skip_reason is not None,
                skip_reason=skip_reason,
            )
        )
    return infos


def write_document_md(path: Path, pages: list[PageInfo]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for info in pages:
            handle.write(f"<!-- page_break: {info.page} -->\n")
            if info.markdown:
                handle.write(info.markdown.rstrip() + "\n")
            handle.write("\n")


def write_pages_jsonl(path: Path, pages: list[PageInfo]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for info in pages:
            row = {
                "page": info.page,
                "char_count": info.char_count,
                "word_count": info.word_count,
                "is_low_text": info.is_low_text,
                "headings": info.headings,
                "current_section": info.current_section,
                "skip": info.skip,
                "skip_reason": info.skip_reason,
            }
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_section_map(source_document_id: str, pages: list[PageInfo]) -> dict[str, Any]:
    skip_counts: dict[str, int] = {}
    payload_pages: list[dict[str, Any]] = []
    skipped = 0
    for info in pages:
        if info.skip and info.skip_reason:
            skipped += 1
            skip_counts[info.skip_reason] = skip_counts.get(info.skip_reason, 0) + 1
        payload_pages.append(
            {
                "page": info.page,
                "current_section": info.current_section,
                "skip": info.skip,
                "skip_reason": info.skip_reason,
            }
        )
    return {
        "source_document_id": source_document_id,
        "pages": payload_pages,
        "skip_stats": {
            "total_pages": len(pages),
            "skipped_pages": skipped,
            "skip_reasons": skip_counts,
        },
    }


def build_document_json(
    source_document_id: str,
    source_doc: dict[str, Any],
    pdf_rel_path: str,
    pdf_sha256: str,
    pages: list[PageInfo],
    tool_version: str,
    skip_patterns_used: list[tuple[str, str]],
) -> dict[str, Any]:
    return {
        "source_document_id": source_document_id,
        "source_name": source_doc.get("source_name", ""),
        "pdf_path": pdf_rel_path,
        "pdf_sha256": pdf_sha256,
        "page_count": len(pages),
        "char_count_total": sum(p.char_count for p in pages),
        "low_text_pages": [p.page for p in pages if p.is_low_text],
        "language_hint": source_doc.get("language", "es") or "es",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "tool": tool_version,
        "skip_patterns_used": [{"name": name, "regex": regex} for name, regex in skip_patterns_used],
    }


def is_idempotent(output_doc_json: Path, pdf_sha256: str) -> bool:
    if not output_doc_json.exists():
        return False
    try:
        payload = json.loads(output_doc_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return payload.get("pdf_sha256") == pdf_sha256


def count_page_breaks(markdown_path: Path) -> int:
    if not markdown_path.exists():
        return 0
    text = markdown_path.read_text(encoding="utf-8")
    return len(re.findall(r"<!--\s*page_break:\s*\d+\s*-->", text))


def slug_tokens(value: str) -> set[str]:
    normalized = unicodedata.normalize("NFKD", value.casefold())
    ascii_text = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return set(token for token in re.split(r"[^a-z0-9]+", ascii_text) if token)


def suggest_pdf_path(source_document_id: str, policy_pdf_root: Path) -> str:
    source_tokens = slug_tokens(source_document_id)
    if not source_tokens:
        return ""
    best_score = 0
    best_path = ""
    for pdf_path in sorted(policy_pdf_root.iterdir()) if policy_pdf_root.exists() else []:
        if not pdf_path.is_file() or pdf_path.suffix.casefold() != ".pdf":
            continue
        overlap = len(source_tokens & slug_tokens(pdf_path.stem))
        if overlap > best_score:
            best_score = overlap
            best_path = f"policy-pdf/{pdf_path.name}"
    return best_path


def command_convert(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    map_csv = resolve_under_root(root, args.map_csv)
    registry_path = root / "data/registry/source_documents.json"
    markdown_root = root / "data/markdown"

    if not map_csv.exists():
        print(f"Mapping file not found: {map_csv}", file=sys.stderr)
        return 1

    patterns_compiled = compile_skip_patterns(
        skip_patterns_path=resolve_under_root(root, args.skip_patterns) if args.skip_patterns else None,
        extra_skip_patterns_path=resolve_under_root(root, args.extra_skip_patterns) if args.extra_skip_patterns else None,
        no_skip_patterns=args.no_skip_patterns,
    )
    patterns_used = [(name, pattern.pattern) for name, pattern in patterns_compiled]
    registry = load_registry(registry_path)
    confirmed_rows = read_confirmed_rows(map_csv, only=args.only)
    if not confirmed_rows:
        print("No confirmed rows found.")
        return 0

    results: list[ConvertResult] = []
    processed = 0
    skipped_idempotent = 0
    failed = 0

    for row in confirmed_rows:
        source_id = row["source_document_id"]
        source_doc = registry.get(source_id, {})
        rel_pdf = row["proposed_pdf_path"]
        pdf_path = (root / rel_pdf).resolve() if rel_pdf else root / ""
        if not rel_pdf or not pdf_path.exists() or not pdf_path.is_file():
            failed += 1
            results.append(ConvertResult(source_id, 0, 0, "-", [], "missing_pdf"))
            continue

        pdf_sha = sha256_file(pdf_path)
        doc_dir = markdown_root / source_id
        doc_json_path = doc_dir / "document.json"
        if not args.force and is_idempotent(doc_json_path, pdf_sha):
            payload = json.loads(doc_json_path.read_text(encoding="utf-8"))
            skip_stats = json.loads((doc_dir / "section_map.json").read_text(encoding="utf-8")).get("skip_stats", {})
            skipped_idempotent += 1
            results.append(
                ConvertResult(
                    source_document_id=source_id,
                    pages=int(payload.get("page_count", 0)),
                    skipped=int(skip_stats.get("skipped_pages", 0)),
                    top_skip_reason=top_skip_reason(skip_stats.get("skip_reasons", {})),
                    low_text_pages=list(payload.get("low_text_pages", [])),
                    status="skipped_idempotent",
                )
            )
            continue

        pages_md, page_count, error = extract_pdf_markdown_pages(pdf_path)
        if error == "encrypted":
            results.append(ConvertResult(source_id, 0, 0, "-", [], "encrypted"))
            continue
        if error:
            failed += 1
            results.append(ConvertResult(source_id, 0, 0, "-", [], "failed"))
            continue
        if page_count != len(pages_md):
            failed += 1
            results.append(ConvertResult(source_id, 0, 0, "-", [], "page_count_mismatch"))
            continue

        page_infos = build_page_infos(pages_md, patterns_compiled)
        section_map = build_section_map(source_id, page_infos)
        doc_json = build_document_json(
            source_document_id=source_id,
            source_doc=source_doc,
            pdf_rel_path=rel_pdf,
            pdf_sha256=pdf_sha,
            pages=page_infos,
            tool_version=f"pymupdf4llm {getattr(load_pymupdf4llm(), '__version__', 'unknown')}",
            skip_patterns_used=patterns_used,
        )

        doc_dir.mkdir(parents=True, exist_ok=True)
        write_document_md(doc_dir / "document.md", page_infos)
        write_pages_jsonl(doc_dir / "pages.jsonl", page_infos)
        (doc_dir / "section_map.json").write_text(
            json.dumps(section_map, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (doc_dir / "document.json").write_text(
            json.dumps(doc_json, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        processed += 1
        results.append(
            ConvertResult(
                source_document_id=source_id,
                pages=doc_json["page_count"],
                skipped=section_map["skip_stats"]["skipped_pages"],
                top_skip_reason=top_skip_reason(section_map["skip_stats"]["skip_reasons"]),
                low_text_pages=doc_json["low_text_pages"],
                status="processed",
            )
        )

    print("| source_document_id | pages | skipped | top_skip_reason | low_text_pages |")
    print("|---|---:|---:|---|---|")
    for result in sorted(results, key=lambda item: item.source_document_id):
        low_text = ",".join(str(p) for p in result.low_text_pages) if result.low_text_pages else "-"
        print(
            f"| {result.source_document_id} | {result.pages} | {result.skipped} | "
            f"{result.top_skip_reason} | {low_text} |"
        )
    print("")
    print(f"Processed: {processed}")
    print(f"Skipped idempotent: {skipped_idempotent}")
    print(f"Failed: {failed}")
    return 1 if failed > 0 else 0


def top_skip_reason(skip_reasons: dict[str, int]) -> str:
    if not skip_reasons:
        return "-"
    return sorted(skip_reasons.items(), key=lambda item: (-item[1], item[0]))[0][0]


def command_inspect(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    source_id = args.source_document_id
    doc_dir = root / "data/markdown" / source_id
    doc_json_path = doc_dir / "document.json"
    section_map_path = doc_dir / "section_map.json"
    if not doc_json_path.exists() or not section_map_path.exists():
        print(f"Missing substrate for {source_id} under {doc_dir}", file=sys.stderr)
        return 1

    doc_json = json.loads(doc_json_path.read_text(encoding="utf-8"))
    section_map = json.loads(section_map_path.read_text(encoding="utf-8"))
    skip_stats = section_map.get("skip_stats", {})
    print(f"source_document_id: {source_id}")
    print(f"page_count: {doc_json.get('page_count', 0)}")
    print(f"char_count_total: {doc_json.get('char_count_total', 0)}")
    print(f"skipped_pages: {skip_stats.get('skipped_pages', 0)}")
    print("skip_reasons:")
    for reason, count in sorted((skip_stats.get("skip_reasons", {}) or {}).items(), key=lambda item: (-item[1], item[0])):
        print(f"- {reason}: {count}")
    print("")
    print("| page | skip_reason | current_section |")
    print("|---:|---|---|")
    for page in section_map.get("pages", []):
        if page.get("skip"):
            print(f"| {page.get('page')} | {page.get('skip_reason') or '-'} | {page.get('current_section') or '-'} |")
    return 0


def command_verify(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    markdown_root = root / "data/markdown"
    failures: list[str] = []
    if not markdown_root.exists():
        print("No data/markdown directory to verify.")
        return 0
    for doc_dir in sorted(path for path in markdown_root.iterdir() if path.is_dir()):
        source_id = doc_dir.name
        doc_json_path = doc_dir / "document.json"
        doc_md_path = doc_dir / "document.md"
        pages_jsonl_path = doc_dir / "pages.jsonl"
        section_map_path = doc_dir / "section_map.json"
        if not doc_json_path.exists():
            failures.append(f"{source_id}: missing document.json")
            continue
        try:
            doc_json = json.loads(doc_json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"{source_id}: invalid document.json ({exc})")
            continue
        page_count = int(doc_json.get("page_count", 0))
        pdf_rel = doc_json.get("pdf_path", "")
        pdf_path = (root / pdf_rel).resolve() if isinstance(pdf_rel, str) else root / ""
        if not pdf_path.exists():
            failures.append(f"{source_id}: missing pdf for sha check ({pdf_rel})")
        else:
            sha = sha256_file(pdf_path)
            if sha != doc_json.get("pdf_sha256"):
                failures.append(f"{source_id}: pdf_sha256 drift")

        if count_page_breaks(doc_md_path) != page_count:
            failures.append(f"{source_id}: document.md page breaks != page_count")

        if not pages_jsonl_path.exists():
            failures.append(f"{source_id}: missing pages.jsonl")
        else:
            lines = [line for line in pages_jsonl_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            if len(lines) != page_count:
                failures.append(f"{source_id}: pages.jsonl lines != page_count")

        if not section_map_path.exists():
            failures.append(f"{source_id}: missing section_map.json")
        else:
            section_map = json.loads(section_map_path.read_text(encoding="utf-8"))
            if len(section_map.get("pages", [])) != page_count:
                failures.append(f"{source_id}: section_map pages != page_count")

    if failures:
        print("Verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Verification passed.")
    return 0


def command_map(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    map_csv = resolve_under_root(root, args.map_csv)
    policy_pdf_root = root / "policy-pdf"
    if not map_csv.exists():
        print(f"Mapping file not found: {map_csv}", file=sys.stderr)
        return 1
    if not policy_pdf_root.exists():
        print(f"Policy PDF directory not found: {policy_pdf_root}", file=sys.stderr)
        return 1

    rows = read_rows(map_csv)
    if not rows:
        print("No mapping rows found.")
        return 0

    updated = 0
    for row in rows:
        status = row.get("status", "")
        if status in MAP_PROTECTED_STATUSES:
            continue
        source_id = row.get("source_document_id", "")
        if not source_id:
            continue
        suggestion = suggest_pdf_path(source_id, policy_pdf_root)
        if not suggestion:
            continue
        existing = row.get("proposed_pdf_path", "")
        if existing and not args.overwrite_proposed:
            continue
        row["proposed_pdf_path"] = suggestion
        updated += 1

    with map_csv.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = ["source_document_id", "proposed_pdf_path", "confidence", "status"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})

    print(f"Updated proposed_pdf_path suggestions: {updated}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build/inspect/verify/map v1 substrate artifacts.")
    parser.add_argument("--root", type=str, default=str(V1_ROOT), help="Override v1 root directory.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    convert_parser = subparsers.add_parser("convert", help="Build substrate for confirmed map rows.")
    convert_parser.add_argument("--only", type=str, default=None, help="Only process one source_document_id.")
    convert_parser.add_argument(
        "--map-csv",
        type=str,
        default=str(V1_ROOT / "data/source_pdf_map.csv"),
        help="Path to source PDF mapping CSV (defaults to v1/data/source_pdf_map.csv).",
    )
    convert_parser.add_argument("--skip-patterns", type=str, default=None, help="JSON/YAML list replacing defaults.")
    convert_parser.add_argument(
        "--extra-skip-patterns",
        type=str,
        default=None,
        help="JSON/YAML list appended to defaults.",
    )
    convert_parser.add_argument("--no-skip-patterns", action="store_true", help="Disable all skip pattern matching.")
    convert_parser.add_argument("--force", action="store_true", help="Ignore idempotency check and rebuild.")

    inspect_parser = subparsers.add_parser("inspect", help="Inspect one substrate output directory.")
    inspect_parser.add_argument("source_document_id", type=str)

    verify_parser = subparsers.add_parser("verify", help="Verify existing substrate outputs.")
    verify_parser.add_argument(
        "--map-csv",
        type=str,
        default=str(V1_ROOT / "data/source_pdf_map.csv"),
        help="Unused placeholder for CLI symmetry.",
    )

    map_parser = subparsers.add_parser(
        "map",
        help="Rebuild proposed PDF suggestions for unmapped IDs without touching confirmed/missing_source rows.",
    )
    map_parser.add_argument(
        "--map-csv",
        type=str,
        default=str(V1_ROOT / "data/source_pdf_map.csv"),
        help="Path to source PDF mapping CSV (defaults to v1/data/source_pdf_map.csv).",
    )
    map_parser.add_argument(
        "--overwrite-proposed",
        action="store_true",
        help="Also overwrite existing proposed_pdf_path values on non-protected rows.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "convert":
        return command_convert(args)
    if args.command == "inspect":
        return command_inspect(args)
    if args.command == "verify":
        return command_verify(args)
    if args.command == "map":
        return command_map(args)
    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
