#!/usr/bin/env python3
"""Stage 1: extract action-agnostic atoms from one source document.

For each document this script produces:
  - releases/v1/data/atoms/<source_document_id>.jsonl   one atom per line
  - releases/v1/data/atoms/<source_document_id>.meta.json  run metadata

Large documents are split into section-boundary chunks (~50k tokens each) and
atomized chunk-by-chunk to stay inside gpt-4.1-mini's 32k-token output limit
and to make recall more reliable. Atoms are renumbered in document order
after all chunks return.

Usage:
  # Dry run — print chunk plan and one chunk's prompt prefix without API calls
  python v1_extract_atoms.py --doc chl_parcc_arica --dry-run

  # Real run
  python v1_extract_atoms.py --doc chl_parcc_arica

  # Re-validate an existing atoms file (deterministic, no API call)
  python v1_extract_atoms.py --validate releases/v1/data/atoms/chl_parcc_arica.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

# Reuse Document / page-resolver / template helpers
import v1_common as ef  # noqa: N812 — keeping `ef` alias for now to minimise diff

SCHEMA_VERSION = "1.0.0"
EXTRACTOR_VERSION = "0.1.0"
DEFAULT_MODEL = "gpt-4.1-mini"
DEFAULT_CHUNK_TOKEN_BUDGET = 50_000   # target input tokens per chunk
DEFAULT_CHUNK_CHAR_BUDGET = DEFAULT_CHUNK_TOKEN_BUDGET * 4   # rough chars-per-token estimate

V1 = Path(__file__).resolve().parents[1]
DEFAULT_MARKDOWN_DIR = V1 / "data" / "markdown"
DEFAULT_REGISTRY = V1 / "data" / "registry" / "source_documents.json"
DEFAULT_OUTPUT_DIR = V1 / "data" / "atoms"
ATOMIZE_SYSTEM_PATH = V1 / "prompts" / "atomize_system.md"
ATOMIZE_USER_PATH = V1 / "prompts" / "atomize_user.md.j2"

ALLOWED_PRIMITIVE_TYPES = {
    "action", "target", "funding", "monitoring", "governance",
    "sector_priority", "sector", "risk", "context",
}
ALLOWED_RELATION_HINTS = {
    "commits", "targets", "funds", "monitors", "governs", "prioritizes",
    "identifies", "contextualizes", "restates", "references",
}
ALLOWED_MEASURE_TYPES = {"mitigation", "adaptation", "transversal", "unknown"}
ALLOWED_EXPLICITNESS = {"explicit", "inferred"}

SECTION_BREAK_RE = re.compile(r"^(##+)\s+(.+?)$", re.MULTILINE)


# ----------------------------------------------------------------------------
# Chunking
# ----------------------------------------------------------------------------

@dataclass
class Chunk:
    index: int           # 0-based
    start_offset: int    # char offset in full doc
    end_offset: int      # exclusive
    text: str            # the chunk content (may include leading section headings)


def plan_chunks(text: str, char_budget: int = DEFAULT_CHUNK_CHAR_BUDGET) -> list[Chunk]:
    """Split the doc into chunks of at most ~char_budget chars at ## section
    boundaries. If a single section is larger than the budget, the chunk
    containing it is allowed to overflow rather than split mid-section.
    """
    if len(text) <= char_budget:
        return [Chunk(index=0, start_offset=0, end_offset=len(text), text=text)]

    # Identify ## section break offsets
    breaks = [m.start() for m in SECTION_BREAK_RE.finditer(text)]
    if not breaks or breaks[0] != 0:
        breaks = [0] + breaks
    breaks.append(len(text))

    chunks: list[Chunk] = []
    chunk_start = 0
    cursor = 0
    while cursor < len(breaks) - 1:
        # Try to extend until we exceed budget
        next_cursor = cursor
        while next_cursor + 1 < len(breaks) and (breaks[next_cursor + 1] - chunk_start) <= char_budget:
            next_cursor += 1
        if next_cursor == cursor:
            # Even one section exceeds the budget; include it as its own chunk
            next_cursor = cursor + 1
        chunk_end = breaks[next_cursor]
        chunks.append(
            Chunk(
                index=len(chunks),
                start_offset=chunk_start,
                end_offset=chunk_end,
                text=text[chunk_start:chunk_end],
            )
        )
        chunk_start = chunk_end
        cursor = next_cursor
    return chunks


# ----------------------------------------------------------------------------
# Prompt assembly
# ----------------------------------------------------------------------------

def load_atomize_system() -> str:
    return ATOMIZE_SYSTEM_PATH.read_text(encoding="utf-8")


def load_atomize_user() -> str:
    return ATOMIZE_USER_PATH.read_text(encoding="utf-8")


def build_user_prompt(doc_meta: dict, chunk: Chunk, total_chunks: int) -> str:
    chunk_label = (
        "single-chunk document (chunk 1 of 1)"
        if total_chunks == 1
        else f"chunk {chunk.index + 1} of {total_chunks} "
             f"(character offsets {chunk.start_offset}..{chunk.end_offset} of the full document)"
    )
    return ef.render_template(
        load_atomize_user(),
        {
            "source_document_id": doc_meta.get("source_document_id", ""),
            "source_name": doc_meta.get("source_name", ""),
            "source_level": doc_meta.get("source_level", ""),
            "region_code": doc_meta.get("region_code", ""),
            "document_type": doc_meta.get("document_type", ""),
            "chunk_label": chunk_label,
            "document_markdown": chunk.text,
        },
    )


# ----------------------------------------------------------------------------
# LLM call
# ----------------------------------------------------------------------------

def call_atomize(system_prompt: str, user_prompt: str, model: str) -> tuple[dict, dict]:
    try:
        from openai import OpenAI  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Install openai: pip install 'openai>=1.40'") from exc

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY environment variable")

    client = OpenAI(api_key=api_key)
    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    duration = time.time() - start
    text = response.choices[0].message.content or ""
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    payload = json.loads(text)
    usage = getattr(response, "usage", None)
    usage_dict = {"duration_seconds": round(duration, 2)}
    if usage is not None:
        usage_dict["input_tokens"] = getattr(usage, "prompt_tokens", None)
        usage_dict["output_tokens"] = getattr(usage, "completion_tokens", None)
        details = getattr(usage, "prompt_tokens_details", None)
        if details is not None:
            usage_dict["cached_input_tokens"] = getattr(details, "cached_tokens", None)
        details_out = getattr(usage, "completion_tokens_details", None)
        if details_out is not None:
            usage_dict["reasoning_tokens"] = getattr(details_out, "reasoning_tokens", None)
        # Detect output truncation via finish_reason if available
        try:
            finish = response.choices[0].finish_reason
            usage_dict["finish_reason"] = finish
        except Exception:
            pass
    return payload, usage_dict


# ----------------------------------------------------------------------------
# Atom normalisation and validation
# ----------------------------------------------------------------------------

def normalize_atom(raw: dict) -> dict | None:
    """Return a normalised atom dict, or None if the raw record is unusable."""
    primitive_type = raw.get("primitive_type")
    if primitive_type not in ALLOWED_PRIMITIVE_TYPES:
        return None
    evidence_text = (raw.get("evidence_text") or "").strip()
    if len(evidence_text) < 5:
        return None
    atom = {
        "schema_version": SCHEMA_VERSION,
        "primitive_type": primitive_type,
        "evidence_text": evidence_text,
        "atom_summary": (raw.get("atom_summary") or "").strip(),
        "sector_tags": list(raw.get("sector_tags") or []),
        "applicability_scope": (raw.get("applicability_scope") or "").strip(),
    }
    mt = raw.get("measure_type")
    if mt in ALLOWED_MEASURE_TYPES:
        atom["measure_type"] = mt
    ex = raw.get("explicitness")
    if ex in ALLOWED_EXPLICITNESS:
        atom["explicitness"] = ex
    hint = raw.get("primitive_relation_hint")
    if hint in ALLOWED_RELATION_HINTS:
        atom["primitive_relation_hint"] = hint
    return atom


def assign_offsets_and_ids(
    atoms: list[dict],
    document: ef.Document,
    doc_id: str,
) -> tuple[list[dict], list[str]]:
    """Return (good_atoms_with_ids, dropped_reasons).

    For each atom:
      - resolve the verbatim offset; drop if not found
      - resolve page + section from the offset
      - sort by offset (document order)
      - assign atom_id = <doc_id>_a_NNNN
    """
    resolved: list[dict] = []
    dropped: list[str] = []
    for atom in atoms:
        offset = document.find_verbatim(atom["evidence_text"])
        if offset is None:
            dropped.append(f"verbatim_not_found:{atom['evidence_text'][:80]!r}")
            continue
        atom["evidence_offset"] = offset
        page = document.page_for_offset(offset)
        if page is not None:
            atom["page"] = page
        section = document.section_for_offset(offset)
        if section:
            atom["section"] = section
        resolved.append(atom)

    resolved.sort(key=lambda a: a["evidence_offset"])

    final: list[dict] = []
    seen: set[tuple] = set()  # (primitive_type, evidence_offset) for dedupe
    for i, atom in enumerate(resolved):
        key = (atom["primitive_type"], atom["evidence_offset"], atom["evidence_text"])
        if key in seen:
            dropped.append(f"duplicate:{atom['atom_summary'][:60]!r}")
            continue
        seen.add(key)
        atom["atom_id"] = f"{doc_id}_a_{len(final):04d}"
        atom["source_document_id"] = doc_id
        final.append(atom)
    return final, dropped


# ----------------------------------------------------------------------------
# Per-doc entry point
# ----------------------------------------------------------------------------

def atomize_document(
    doc_id: str,
    doc_meta: dict,
    markdown_dir: Path,
    model: str = DEFAULT_MODEL,
    char_budget: int = DEFAULT_CHUNK_CHAR_BUDGET,
) -> tuple[list[dict], dict]:
    document = ef.load_document(markdown_dir, doc_id)
    chunks = plan_chunks(document.text, char_budget=char_budget)
    system_prompt = load_atomize_system()

    raw_atoms: list[dict] = []
    chunk_logs: list[dict] = []
    for chunk in chunks:
        print(
            f"atomizing {doc_id}: chunk {chunk.index + 1}/{len(chunks)} "
            f"({chunk.end_offset - chunk.start_offset:,} chars)",
            file=sys.stderr,
            flush=True,
        )
        user_prompt = build_user_prompt(doc_meta, chunk, total_chunks=len(chunks))
        payload, usage = call_atomize(system_prompt, user_prompt, model=model)
        chunk_atoms_raw = payload.get("atoms") or []
        for raw in chunk_atoms_raw:
            norm = normalize_atom(raw)
            if norm is None:
                continue
            norm.setdefault("extraction_metadata", {})
            norm["extraction_metadata"]["chunk_index"] = chunk.index
            norm["extraction_metadata"]["model"] = model
            norm["extraction_metadata"]["created_at"] = datetime.now(timezone.utc).isoformat()
            norm["extraction_metadata"]["extractor_version"] = EXTRACTOR_VERSION
            raw_atoms.append(norm)
        chunk_logs.append({
            "chunk_index": chunk.index,
            "start_offset": chunk.start_offset,
            "end_offset": chunk.end_offset,
            "chars": chunk.end_offset - chunk.start_offset,
            "raw_atoms": len(chunk_atoms_raw),
            "kept_atoms": sum(
                1 for raw in chunk_atoms_raw if normalize_atom(raw) is not None
            ),
            **usage,
        })
        print(
            f"completed {doc_id}: chunk {chunk.index + 1}/{len(chunks)} "
            f"atoms={len(chunk_atoms_raw)}",
            file=sys.stderr,
            flush=True,
        )

    atoms, dropped = assign_offsets_and_ids(raw_atoms, document, doc_id)

    meta = {
        "schema_version": SCHEMA_VERSION,
        "source_document_id": doc_id,
        "model": model,
        "extractor_version": EXTRACTOR_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "document_chars": len(document.text),
        "chunks": chunk_logs,
        "total_raw_atoms": len(raw_atoms),
        "kept_atoms": len(atoms),
        "dropped_count": len(dropped),
        "dropped_reasons_sample": dropped[:20],
        "total_input_tokens": sum(c.get("input_tokens") or 0 for c in chunk_logs),
        "total_output_tokens": sum(c.get("output_tokens") or 0 for c in chunk_logs),
        "total_cached_input_tokens": sum(c.get("cached_input_tokens") or 0 for c in chunk_logs),
        "duration_seconds": round(sum(c.get("duration_seconds") or 0.0 for c in chunk_logs), 2),
    }
    return atoms, meta


# ----------------------------------------------------------------------------
# I/O
# ----------------------------------------------------------------------------

def write_atoms(atoms: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for atom in atoms:
            f.write(json.dumps(atom, ensure_ascii=False) + "\n")


def write_meta(meta: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")


def load_atoms(path: Path) -> list[dict]:
    atoms = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            atoms.append(json.loads(line))
    return atoms


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Stage 1: extract action-agnostic atoms")
    ap.add_argument("--doc", help="source_document_id")
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    ap.add_argument("--markdown-dir", type=Path, default=DEFAULT_MARKDOWN_DIR)
    ap.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--char-budget", type=int, default=DEFAULT_CHUNK_CHAR_BUDGET,
                    help=f"Per-chunk char budget for chunking (default: {DEFAULT_CHUNK_CHAR_BUDGET}).")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print chunk plan + first chunk's prompt offsets, no API call.")
    ap.add_argument("--validate", help="Path to an existing atoms.jsonl to re-validate against the doc.")
    args = ap.parse_args()

    if args.validate:
        path = Path(args.validate)
        atoms = load_atoms(path)
        doc_id = atoms[0]["source_document_id"] if atoms else path.stem
        document = ef.load_document(args.markdown_dir, doc_id)
        bad = []
        for a in atoms:
            off = document.find_verbatim(a["evidence_text"])
            if off is None:
                bad.append(a["atom_id"])
        print(f"{len(atoms)} atoms; {len(bad)} fail verbatim check")
        for b in bad[:20]:
            print(f"  - {b}")
        return 0 if not bad else 2

    if not args.doc:
        ap.print_help()
        return 1

    registry = ef.load_registry(args.registry)
    if args.doc not in registry:
        print(f"unknown source_document_id {args.doc!r}", file=sys.stderr)
        return 1
    doc_meta = dict(registry[args.doc])
    doc_meta["source_document_id"] = args.doc
    document = ef.load_document(args.markdown_dir, args.doc)

    if args.dry_run:
        chunks = plan_chunks(document.text, char_budget=args.char_budget)
        print(f"document chars: {len(document.text):,}")
        print(f"planned chunks: {len(chunks)}")
        for c in chunks:
            print(f"  chunk {c.index+1}/{len(chunks)} offsets={c.start_offset:9d}..{c.end_offset:9d}  chars={c.end_offset-c.start_offset:,}")
        system_prompt = load_atomize_system()
        user_prompt = build_user_prompt(doc_meta, chunks[0], total_chunks=len(chunks))
        print()
        print(f"system prompt chars: {len(system_prompt):,}")
        print(f"chunk-1 user prompt chars: {len(user_prompt):,}")
        return 0

    atoms, meta = atomize_document(
        doc_id=args.doc,
        doc_meta=doc_meta,
        markdown_dir=args.markdown_dir,
        model=args.model,
        char_budget=args.char_budget,
    )

    out_jsonl = args.output_dir / f"{args.doc}.jsonl"
    out_meta = args.output_dir / f"{args.doc}.meta.json"
    write_atoms(atoms, out_jsonl)
    write_meta(meta, out_meta)

    print(
        f"wrote {out_jsonl}  atoms={len(atoms)} chunks={len(meta['chunks'])} "
        f"in={meta['total_input_tokens']:,} out={meta['total_output_tokens']:,} "
        f"duration={meta['duration_seconds']}s",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
