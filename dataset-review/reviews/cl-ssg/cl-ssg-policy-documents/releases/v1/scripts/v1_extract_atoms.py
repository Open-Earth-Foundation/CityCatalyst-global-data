#!/usr/bin/env python3
"""Extract Stage-2 policy atoms from v1 substrate markdown.

Dependencies (install in your environment):
  pip install jsonschema google-genai openai
"""

from __future__ import annotations

import argparse
import copy
import json
import logging
import os
import re
import sys
import time
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

LOGGER = logging.getLogger("v1_extract_atoms")

V1_ROOT = Path(__file__).resolve().parent.parent
GEMINI_DEFAULT_MODEL = "gemini-2.5-flash"
OPENAI_DEFAULT_MODEL = "gpt-4.1-mini"
TRUNCATION_PARSE_MARKERS = (
    "Unterminated string",
    "Expecting value",
    "Expecting property name",
    "Expecting ',' delimiter",
)


class ModelConfigurationError(RuntimeError):
    """Raised when a provider model is invalid/retired."""


class LLMClient(Protocol):
    def complete(
        self,
        *,
        system: str,
        user: str,
        response_schema: dict[str, Any],
        model: str,
        max_output_tokens: int,
        max_transient_retries: int,
    ) -> "LLMResponse": ...


@dataclass
class LLMResponse:
    text: str
    parsed: Any
    finish_reason: str | None


@dataclass
class Batch:
    batch_id: int
    section: str
    pages: list[int]

    @property
    def page_start(self) -> int:
        return self.pages[0]

    @property
    def page_end(self) -> int:
        return self.pages[-1]


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def transient_backoff(attempt: int) -> int:
    return min(15 * (2**attempt), 240)


def normalize_for_match(text: str) -> str:
    normalized = unicodedata.normalize("NFC", text)
    normalized = normalized.replace("\u00ad", "")
    ligatures = {"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi", "\ufb04": "ffl"}
    for src, dst in ligatures.items():
        normalized = normalized.replace(src, dst)
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
    }
    for src, dst in replacements.items():
        normalized = normalized.replace(src, dst)
    normalized = normalized.replace("|", " ")
    normalized = re.sub(r"(\*{1,2}|_{1,2})(?=\S)|(?<=\S)(\*{1,2}|_{1,2})", "", normalized)
    normalized = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", normalized, flags=re.MULTILINE)
    normalized = re.sub(r"\s+", " ", normalized).strip().lower()
    return normalized


def strip_markdown_json_fence(raw: str) -> str:
    text = raw.strip()
    match = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else text


def recover_truncated_array(text: str) -> list[dict[str, Any]] | None:
    cleaned = strip_markdown_json_fence(text)
    start = cleaned.find("[")
    if start < 0:
        return None
    decoder = json.JSONDecoder()
    idx = start + 1
    recovered: list[dict[str, Any]] = []
    while idx < len(cleaned):
        while idx < len(cleaned) and cleaned[idx] in " \t\r\n,":
            idx += 1
        if idx >= len(cleaned) or cleaned[idx] == "]":
            break
        try:
            obj, next_idx = decoder.raw_decode(cleaned, idx)
        except json.JSONDecodeError:
            break
        if isinstance(obj, dict):
            recovered.append(obj)
        idx = next_idx
    return recovered or None


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def strip_formats(node: Any) -> Any:
    if isinstance(node, dict):
        out: dict[str, Any] = {}
        for key, value in node.items():
            if key == "format" or key.startswith("$"):
                continue
            out[key] = strip_formats(value)
        return out
    if isinstance(node, list):
        return [strip_formats(item) for item in node]
    return node


def simplify_for_structured_output(node: Any) -> Any:
    """Keep only JSON-Schema features accepted by provider validators."""
    allowed = {
        "type",
        "properties",
        "required",
        "items",
        "enum",
        "minimum",
        "maximum",
        "minItems",
        "maxItems",
        "minLength",
        "maxLength",
        "description",
    }
    if isinstance(node, dict):
        out: dict[str, Any] = {}
        for key, value in node.items():
            if key == "properties" and isinstance(value, dict):
                out[key] = {prop_name: simplify_for_structured_output(prop_schema) for prop_name, prop_schema in value.items()}
                continue
            if key in allowed:
                out[key] = simplify_for_structured_output(value)
        return out
    if isinstance(node, list):
        return [simplify_for_structured_output(item) for item in node]
    return node


def resolve_refs(node: Any, root_schema: dict[str, Any]) -> Any:
    if isinstance(node, dict):
        if "$ref" in node and isinstance(node["$ref"], str):
            ref = node["$ref"]
            if not ref.startswith("#/"):
                return node
            cursor: Any = root_schema
            for part in ref[2:].split("/"):
                cursor = cursor[part]
            return resolve_refs(copy.deepcopy(cursor), root_schema)
        return {k: resolve_refs(v, root_schema) for k, v in node.items() if k != "$ref"}
    if isinstance(node, list):
        return [resolve_refs(item, root_schema) for item in node]
    return node


def load_atom_schema(v1_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    schema = load_json(v1_root / "schemas/atoms.schema.json")
    resolved = resolve_refs(copy.deepcopy(schema), schema)
    resolved = strip_formats(resolved)
    # Keep only the atom item contract fields for structured-output schema.
    for meta_key in ("title", "description"):
        resolved.pop(meta_key, None)
    resolved = simplify_for_structured_output(resolved)
    return schema, resolved


def atom_required_shape_reference(schema: dict[str, Any]) -> str:
    props = schema.get("properties", {})
    defs = schema.get("$defs", {})
    required = schema.get("required", [])
    lines = ["REQUIRED FIELDS: " + ", ".join(required)]
    enum_fields = [
        "primitive_type",
        "evidence_kind",
        "measure_type",
        "explicitness",
        "readiness_status",
        "extraction_method",
    ]
    for field in enum_fields:
        enum_values: list[str] = []
        ref = props.get(field, {}).get("$ref")
        if isinstance(ref, str) and ref.startswith("#/$defs/"):
            def_name = ref.split("/")[-1]
            enum_values = defs.get(def_name, {}).get("enum", [])
        if enum_values:
            lines.append(f"{field}: {', '.join(enum_values)}")
    return "\n".join(lines)


def build_system_prompt(v1_root: Path, atom_schema: dict[str, Any]) -> str:
    extraction_rules = (v1_root / "schemas/extraction_rules.md").read_text(encoding="utf-8")
    output_contract = (
        "OUTPUT CONTRACT\n"
        "You output a single JSON array of atoms and nothing else. No prose, no markdown fences, no envelope.\n"
        "The first character of your response must be '[' and the last must be ']'."
    )
    shape_ref = atom_required_shape_reference(atom_schema)
    return extraction_rules + "\n\n" + output_contract + "\n\n" + shape_ref


def parse_document_pages(document_md_path: Path) -> dict[int, str]:
    text = document_md_path.read_text(encoding="utf-8")
    pattern = re.compile(r"<!--\s*page_break:\s*(\d+)\s*-->")
    matches = list(pattern.finditer(text))
    out: dict[int, str] = {}
    for idx, match in enumerate(matches):
        page = int(match.group(1))
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        out[page] = text[start:end].lstrip("\n")
    return out


def parse_pages_spec(spec: str, page_count: int) -> set[int]:
    pages: set[int] = set()
    for part in (item.strip() for item in spec.split(",") if item.strip()):
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            start, end = int(start_text), int(end_text)
            if start > end:
                start, end = end, start
            for page in range(start, end + 1):
                if 1 <= page <= page_count:
                    pages.add(page)
        else:
            page = int(part)
            if 1 <= page <= page_count:
                pages.add(page)
    return pages


def build_batches(
    section_pages: list[dict[str, Any]],
    *,
    max_pages_per_batch: int = 4,
    selected_pages: set[int] | None = None,
) -> list[Batch]:
    kept = [p for p in section_pages if not p.get("skip")]
    if selected_pages is not None:
        kept = [p for p in kept if int(p["page"]) in selected_pages]
    kept.sort(key=lambda item: int(item["page"]))
    batches: list[Batch] = []
    current_pages: list[int] = []
    current_section = ""
    batch_id = 0
    for page_obj in kept:
        page = int(page_obj["page"])
        section = str(page_obj.get("current_section", "[front matter]"))
        start_new = False
        if not current_pages:
            start_new = True
        elif len(current_pages) >= max_pages_per_batch:
            start_new = True
        elif section != current_section:
            start_new = True
        elif page != current_pages[-1] + 1:
            start_new = True
        if start_new:
            if current_pages:
                batch_id += 1
                batches.append(Batch(batch_id=batch_id, section=current_section, pages=current_pages))
            current_pages = [page]
            current_section = section
        else:
            current_pages.append(page)
    if current_pages:
        batch_id += 1
        batches.append(Batch(batch_id=batch_id, section=current_section, pages=current_pages))
    return batches


def doc_short_id(source_document_id: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", source_document_id.lower()).strip("_")[:40]


def build_user_prompt(
    *,
    source_document_id: str,
    registry_doc: dict[str, Any],
    batch: Batch,
    page_texts: dict[int, str],
) -> str:
    page_blocks = []
    for page in batch.pages:
        page_blocks.append(f"<<<PAGE {page}>>>\n{page_texts.get(page, '')}")
    return (
        "SOURCE DOCUMENT\n"
        f"source_document_id: {source_document_id}\n"
        f"source_name: {registry_doc.get('source_name', '')}\n"
        f"document_type: {registry_doc.get('document_type', '')}\n"
        f"source_level: {registry_doc.get('source_level', '')}\n"
        f"region_code: {registry_doc.get('region_code', '')}\n"
        f"communal_code: {registry_doc.get('communal_code', '')}\n"
        f"publisher: {registry_doc.get('publisher', '')}\n"
        f"publication_year: {registry_doc.get('publication_year', '')}\n\n"
        "BATCH\n"
        f"section: {batch.section}\n"
        f"pages: {batch.page_start}-{batch.page_end}\n\n"
        "EXTRACTION TASK\n"
        "Extract atoms from the page text below following the extraction rules above. "
        "Return ONLY a JSON array of atoms. "
        f"Use atom_id of the form \"{doc_short_id(source_document_id)}_a_<NNNN>\" where NNNN is zero-padded "
        "and unique within this document; numbering can continue across batches because the harness will dedupe "
        "and renumber if needed.\n\n"
        "Set extraction_method = \"atom_extractor\" on every atom.\n\n"
        "OUTPUT VOLUME RULE\n"
        "Return at most 15 atoms per batch. If the cited pages contain more than 15 atom-worthy facts, prioritize "
        "the most substantive: explicit actions, quantified targets, named actors, and named funding lines over "
        "generic context.\n\n"
        "PAGE TEXT (page-tagged)\n"
        + "\n".join(page_blocks)
    )


def parse_pages_jsonl(path: Path) -> dict[int, dict[str, Any]]:
    out: dict[int, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        out[int(row["page"])] = row
    return out


def build_verbatim_source(document_pages: dict[int, str], page_start: int, page_end: int) -> str:
    raw = "\n".join(document_pages.get(page, "") for page in range(page_start, page_end + 1))
    raw = re.sub(r"<!--\s*page_break:\s*\d+\s*-->", "", raw)
    return raw


def parse_response_atoms(parsed: Any) -> tuple[list[dict[str, Any]], str | None]:
    warning: str | None = None
    if isinstance(parsed, list):
        if all(isinstance(item, dict) for item in parsed):
            return parsed, warning
        raise ValueError("response array must contain objects")
    if isinstance(parsed, dict):
        if "atoms" in parsed and isinstance(parsed["atoms"], list):
            warning = "model_returned_envelope_shape_unwrapped_atoms"
            atoms = parsed["atoms"]
            if all(isinstance(item, dict) for item in atoms):
                return atoms, warning
            raise ValueError("atoms envelope contains non-object entries")
        if all(not isinstance(v, (list, dict)) for v in parsed.values()):
            return [parsed], "model_returned_single_object_wrapped"
        raise ValueError("dict response missing atoms array")
    raise ValueError("response must be a JSON object or array")


def parse_response_atoms_text(raw_text: str) -> tuple[list[dict[str, Any]], str | None]:
    parsed = json.loads(strip_markdown_json_fence(raw_text))
    return parse_response_atoms(parsed)


def extract_atom_validator(schema: dict[str, Any]):
    try:
        import jsonschema
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("jsonschema is required. Install with: pip install jsonschema") from exc
    return jsonschema.Draft202012Validator(schema)


def normalize_rejection_reason(prefix: str, err: Exception | str) -> str:
    message = str(err).replace("\n", " ").strip()
    return f"{prefix}:{message}" if message else prefix


def validate_atom(
    atom: dict[str, Any],
    *,
    atom_validator: Any,
    page_count: int,
    document_pages: dict[int, str],
    low_text_by_page: dict[int, bool],
) -> tuple[bool, str | None]:
    schema_errors = list(atom_validator.iter_errors(atom))
    if schema_errors:
        return False, normalize_rejection_reason("schema_invalid", schema_errors[0].message)
    page_start = atom.get("page_start")
    page_end = atom.get("page_end")
    if not isinstance(page_start, int) or not isinstance(page_end, int):
        return False, "page_out_of_range"
    if page_start < 1 or page_end < page_start or page_end > page_count:
        return False, "page_out_of_range"
    if all(low_text_by_page.get(page, False) for page in range(page_start, page_end + 1)):
        return False, "low_text_pages_in_span"
    normalized_evidence = normalize_for_match(str(atom.get("evidence_text", "")))
    normalized_source = normalize_for_match(build_verbatim_source(document_pages, page_start, page_end))
    if not normalized_evidence or normalized_evidence not in normalized_source:
        return False, "evidence_not_verbatim"
    return True, None


def denormalize_atom(atom: dict[str, Any], registry_doc: dict[str, Any], section: str) -> dict[str, Any]:
    patched = dict(atom)
    if "_doc_type" not in patched:
        patched["_doc_type"] = registry_doc.get("document_type", "")
    if "_section" not in patched:
        patched["_section"] = section
    return patched


def completed_batch_keys(run_payload: dict[str, Any]) -> set[tuple[str, int]]:
    keys: set[tuple[str, int]] = set()
    for batch in run_payload.get("batches", []):
        section = str(batch.get("section", ""))
        page_start = int(batch.get("page_start", 0))
        if section and page_start:
            keys.add((section, page_start))
    return keys


def renumber_atom_ids(source_document_id: str, atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    short_id = doc_short_id(source_document_id)
    for idx, atom in enumerate(atoms, start=1):
        patched = dict(atom)
        patched["atom_id"] = f"{short_id}_a_{idx:04d}"
        out.append(patched)
    return out


def load_existing_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def jsonl_line_count(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def merge_atoms_by_id(
    original_accepted: list[dict[str, Any]],
    retry_accepted: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    accepted_by_id: dict[str, dict[str, Any]] = {}
    no_id_atoms: list[dict[str, Any]] = []
    for atom in original_accepted:
        atom_id = atom.get("atom_id")
        if atom_id:
            accepted_by_id[str(atom_id)] = atom
        else:
            no_id_atoms.append(atom)
    for atom in retry_accepted:
        atom_id = atom.get("atom_id")
        if atom_id:
            accepted_by_id[str(atom_id)] = atom
        else:
            no_id_atoms.append(atom)
    return list(accepted_by_id.values()) + no_id_atoms


def assign_sequential_atom_ids(
    source_document_id: str,
    atoms: list[dict[str, Any]],
    start_index: int,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    short_id = doc_short_id(source_document_id)
    for offset, atom in enumerate(atoms, start=1):
        patched = dict(atom)
        patched["atom_id"] = f"{short_id}_a_{start_index + offset:04d}"
        out.append(patched)
    return out


class GeminiClient:
    def __init__(self, api_key: str | None = None) -> None:
        key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY (or GOOGLE_API_KEY) is required for gemini provider")
        try:
            from google import genai
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("google-genai SDK is not installed") from exc
        self.genai = genai
        self.client = genai.Client(api_key=key)
        self._sleep = time.sleep

    def complete(
        self,
        *,
        system: str,
        user: str,
        response_schema: dict[str, Any],
        model: str,
        max_output_tokens: int,
        max_transient_retries: int,
    ) -> LLMResponse:
        config_obj = self.genai.types.GenerateContentConfig(
            temperature=0.0,
            max_output_tokens=max_output_tokens,
            response_mime_type="application/json",
            # Wrap top-level array to avoid SDK/provider issues with array-root schemas.
            response_schema={"type": "object", "required": ["atoms"], "properties": {"atoms": response_schema}},
        )
        last_exc: Exception | None = None
        for attempt in range(max_transient_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=f"{system}\n\n{user}",
                    config=config_obj,
                )
                text = (getattr(response, "text", "") or "").strip()
                try:
                    parsed = json.loads(text) if text else {}
                except json.JSONDecodeError:
                    parsed = None
                finish_reason = str(getattr(getattr(response, "candidates", [None])[0], "finish_reason", "") or None)
                return LLMResponse(text=text, parsed=parsed, finish_reason=finish_reason)
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                status_code = getattr(exc, "status_code", None)
                if status_code == 404:
                    raise ModelConfigurationError(f"gemini_model_not_found:{model}") from exc
                is_transient = status_code in {408, 429, 500, 502, 503, 504}
                if not is_transient or attempt >= max_transient_retries:
                    break
                wait = transient_backoff(attempt)
                LOGGER.warning("gemini transient retry %s/%s in %ss", attempt + 1, max_transient_retries, wait)
                self._sleep(wait)
        assert last_exc is not None
        raise last_exc


class OpenAIClient:
    def __init__(self, api_key: str | None = None) -> None:
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY is required for openai provider")
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("openai SDK is not installed") from exc
        self.client = OpenAI(api_key=key)
        self._sleep = time.sleep

    def complete(
        self,
        *,
        system: str,
        user: str,
        response_schema: dict[str, Any],
        model: str,
        max_output_tokens: int,
        max_transient_retries: int,
    ) -> LLMResponse:
        try:
            import openai
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("openai SDK is not installed") from exc
        # Responses API expects a flat json_schema object on text.format (name/schema at top level),
        # not the legacy Chat Completions nested {"json_schema": {...}} envelope.
        text_format: dict[str, Any] = {
            "type": "json_schema",
            "name": "atoms_wrapper",
            # Strict mode requires additionalProperties:false on every object; our inlined atom schema
            # is not fully strict-normalized, so keep this loose for reliable extraction.
            "strict": False,
            "schema": {
                "type": "object",
                "additionalProperties": False,
                "required": ["atoms"],
                "properties": {"atoms": response_schema},
            },
        }
        last_exc: Exception | None = None
        for attempt in range(max_transient_retries + 1):
            try:
                response = self.client.responses.create(
                    model=model,
                    input=[
                        {"role": "system", "content": [{"type": "input_text", "text": system}]},
                        {"role": "user", "content": [{"type": "input_text", "text": user}]},
                    ],
                    text={"format": text_format},
                    max_output_tokens=max_output_tokens,
                    temperature=0.0,
                )
                text = getattr(response, "output_text", "") or ""
                try:
                    parsed = json.loads(text) if text else {}
                except json.JSONDecodeError:
                    parsed = None
                finish_reason = getattr(response, "finish_reason", None)
                return LLMResponse(text=text, parsed=parsed, finish_reason=finish_reason)
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                status_code = getattr(exc, "status_code", None)
                if status_code == 404:
                    raise ModelConfigurationError(f"openai_model_not_found:{model}") from exc
                transient = isinstance(
                    exc,
                    tuple(
                        cls
                        for cls in (
                            openai.RateLimitError,
                            getattr(openai, "APIConnectionError", None),
                            getattr(openai, "APITimeoutError", None),
                            getattr(openai, "InternalServerError", None),
                        )
                        if cls is not None
                    ),
                )
                if not transient or attempt >= max_transient_retries:
                    break
                wait = transient_backoff(attempt)
                LOGGER.warning("openai transient retry %s/%s in %ss", attempt + 1, max_transient_retries, wait)
                self._sleep(wait)
        assert last_exc is not None
        raise last_exc


def create_client(provider: str) -> LLMClient:
    if provider == "gemini":
        return GeminiClient()
    if provider == "openai":
        return OpenAIClient()
    raise ValueError(f"Unsupported provider: {provider}")


def model_for_provider(provider: str, override: str | None) -> str:
    if override:
        return override
    if provider == "gemini":
        return GEMINI_DEFAULT_MODEL
    if provider == "openai":
        return OPENAI_DEFAULT_MODEL
    raise ValueError(f"Unsupported provider: {provider}")


def usable_substrate_reason(document_json: dict[str, Any]) -> str | None:
    page_count = int(document_json.get("page_count", 0) or 0)
    char_count_total = int(document_json.get("char_count_total", 0) or 0)
    low_text_pages = document_json.get("low_text_pages", []) or []
    if document_json.get("status") == "encrypted" or document_json.get("encrypted") is True:
        return "encrypted"
    if page_count <= 1 or char_count_total == 0:
        return "no_prechunk"
    if isinstance(low_text_pages, list) and len(low_text_pages) == page_count:
        return "no_prechunk"
    return None


def is_truncation_parse_error(exc: Exception, parsed_text: str) -> bool:
    if not isinstance(exc, json.JSONDecodeError):
        return False
    if not any(marker in str(exc) for marker in TRUNCATION_PARSE_MARKERS):
        return False
    return exc.pos >= max(0, len(parsed_text) - 16)


def build_verbatim_retry_prompt(
    *,
    rejected_verbatim: list[dict[str, Any]],
    attempted_atoms: list[dict[str, Any]],
    document_pages: dict[int, str],
) -> str:
    details: list[dict[str, Any]] = []
    cited_pages: set[int] = set()
    for rej in rejected_verbatim:
        atom_index = int(rej.get("atom_index", -1))
        if atom_index < 0 or atom_index >= len(attempted_atoms):
            continue
        atom = attempted_atoms[atom_index]
        p_start = atom.get("page_start")
        p_end = atom.get("page_end")
        if isinstance(p_start, int) and isinstance(p_end, int):
            for page in range(p_start, p_end + 1):
                cited_pages.add(page)
        details.append(
            {
                "atom_id": atom.get("atom_id"),
                "page_range": f"{atom.get('page_start')}-{atom.get('page_end')}",
                "attempted_evidence_text": atom.get("evidence_text", ""),
            }
        )
    page_text = "\n".join(f"<<<PAGE {p}>>>\n{document_pages.get(p, '')}" for p in sorted(cited_pages))
    return (
        "PREVIOUS BATCH HAD VERBATIM MISMATCHES\n"
        "The following atoms were rejected because their evidence_text did not appear verbatim in the cited pages:\n"
        f"{json.dumps(details, ensure_ascii=False, indent=2)}\n\n"
        "The actual page text for the cited pages is below. For each rejected atom, find the shortest verbatim sentence "
        "on the cited page that supports the row and use that exact text - copied character-for-character including markdown "
        "formatting (pipes, asterisks, accents) - as evidence_text. Do not paraphrase, do not strip formatting.\n\n"
        f"{page_text}\n\n"
        "Return ONLY a JSON array of corrected atoms. Use the same atom_ids as before."
    )


def process_document(
    *,
    source_document_id: str,
    v1_root: Path,
    provider: str,
    model: str,
    max_output_tokens: int,
    request_throttle_seconds: float,
    max_transient_retries: int,
    pages_override: str | None,
    force: bool,
    resume: bool,
    dry_run: bool,
    client: LLMClient | None,
    atom_schema_original: dict[str, Any],
    atom_schema_resolved: dict[str, Any],
    registry: dict[str, dict[str, Any]],
) -> tuple[str, dict[str, Any] | None]:
    markdown_dir = v1_root / "data/markdown" / source_document_id
    document_json_path = markdown_dir / "document.json"
    section_map_path = markdown_dir / "section_map.json"
    pages_jsonl_path = markdown_dir / "pages.jsonl"
    document_md_path = markdown_dir / "document.md"
    atoms_dir = v1_root / "data/atoms"
    atoms_jsonl_path = atoms_dir / f"{source_document_id}.jsonl"
    run_json_path = atoms_dir / f"{source_document_id}.run.json"

    if not (document_json_path.exists() and section_map_path.exists() and pages_jsonl_path.exists() and document_md_path.exists()):
        LOGGER.info("%s skipped: missing substrate artifacts", source_document_id)
        return "skipped_missing_substrate", None

    if run_json_path.exists() and not force and not resume:
        existing_run = load_json(run_json_path)
        if int(existing_run.get("totals", {}).get("batches", 0)) > 0:
            LOGGER.info("%s skipped: already completed (use --force/--resume)", source_document_id)
            return "skipped_idempotent", None

    document_json = load_json(document_json_path)
    reason = usable_substrate_reason(document_json)
    if reason:
        LOGGER.info("%s skipped: %s", source_document_id, reason)
        return f"skipped_{reason}", None

    section_map = load_json(section_map_path)
    section_pages = section_map.get("pages", [])
    if not section_pages:
        LOGGER.info("%s skipped: section_map has no pages", source_document_id)
        return "skipped_empty", None

    page_count = int(document_json.get("page_count", 0))
    selected_pages = parse_pages_spec(pages_override, page_count) if pages_override else None
    batches = build_batches(section_pages, selected_pages=selected_pages)
    if not batches:
        LOGGER.info("%s skipped: all pages are skipped", source_document_id)
        return "skipped_all_pages_skipped", None

    page_metadata = parse_pages_jsonl(pages_jsonl_path)
    low_text_by_page = {page: bool(row.get("is_low_text")) for page, row in page_metadata.items()}
    document_pages = parse_document_pages(document_md_path)
    registry_doc = registry.get(source_document_id, {})
    system_prompt = build_system_prompt(v1_root, atom_schema_original)
    atom_validator = extract_atom_validator(atom_schema_original)

    prior_run = load_json(run_json_path) if (resume and run_json_path.exists()) else {}
    done_keys = completed_batch_keys(prior_run) if resume else set()
    existing_line_count = jsonl_line_count(atoms_jsonl_path) if resume else 0
    next_atom_index = existing_line_count
    batch_records: list[dict[str, Any]] = list(prior_run.get("batches", [])) if resume else []
    skipped_pages_total = sum(1 for page in section_pages if page.get("skip"))
    started_at = prior_run.get("started_at", iso_now()) if resume else iso_now()

    if dry_run:
        first = batches[0]
        first_prompt = build_user_prompt(
            source_document_id=source_document_id,
            registry_doc=registry_doc,
            batch=first,
            page_texts=document_pages,
        )
        print(f"[dry-run] source_document_id={source_document_id} batches={len(batches)} first_input_chars={len(first_prompt)}")
        return "dry_run", None

    assert client is not None
    if force and not resume:
        if atoms_jsonl_path.exists():
            atoms_jsonl_path.unlink()
        if run_json_path.exists():
            run_json_path.unlink()
    for batch in batches:
        if (batch.section, batch.page_start) in done_keys:
            continue
        user_prompt = build_user_prompt(
            source_document_id=source_document_id,
            registry_doc=registry_doc,
            batch=batch,
            page_texts=document_pages,
        )
        input_chars = len(user_prompt)
        batch_start = time.time()
        finish_reason = None
        rejected: list[dict[str, Any]] = []
        returned_atoms: list[dict[str, Any]] = []
        batch_notes: list[str] = []
        try:
            response = client.complete(
                system=system_prompt,
                user=user_prompt,
                response_schema={"type": "array", "items": atom_schema_resolved},
                model=model,
                max_output_tokens=max_output_tokens,
                max_transient_retries=max_transient_retries,
            )
            finish_reason = response.finish_reason
            if response.parsed is None:
                try:
                    returned_atoms, shape_warning = parse_response_atoms_text(response.text)
                except json.JSONDecodeError as parse_exc:
                    if is_truncation_parse_error(parse_exc, strip_markdown_json_fence(response.text)):
                        recovered = recover_truncated_array(response.text)
                        if recovered is not None:
                            returned_atoms, shape_warning = parse_response_atoms(recovered)
                            batch_notes = [
                                f"salvaged_truncated: original len={len(response.text)}, recovered {len(recovered)} atoms"
                            ]
                        else:
                            raise ValueError("json_parse_unrecoverable") from parse_exc
                    else:
                        raise ValueError("json_parse_unrecoverable") from parse_exc
            else:
                returned_atoms, shape_warning = parse_response_atoms(response.parsed)
            if shape_warning:
                LOGGER.warning("%s batch %s: %s", source_document_id, batch.batch_id, shape_warning)
        except Exception as exc:  # noqa: BLE001
            duration = round(time.time() - batch_start, 2)
            reason_text = "json_parse_unrecoverable" if str(exc) == "json_parse_unrecoverable" else normalize_rejection_reason("batch_error", exc)
            batch_records.append(
                {
                    "batch_id": batch.batch_id,
                    "section": batch.section,
                    "page_start": batch.page_start,
                    "page_end": batch.page_end,
                    "page_count": len(batch.pages),
                    "atoms_returned": 0,
                    "atoms_accepted": 0,
                    "atoms_rejected": [{"reason": reason_text, "atom_index": -1}],
                    "duration_seconds": duration,
                    "input_chars": input_chars,
                    "finish_reason": finish_reason or "ERROR",
                }
            )
            continue

        batch_accepted: list[dict[str, Any]] = []
        for idx, atom in enumerate(returned_atoms):
            patched = denormalize_atom(atom, registry_doc, batch.section)
            valid, reason_text = validate_atom(
                patched,
                atom_validator=atom_validator,
                page_count=page_count,
                document_pages=document_pages,
                low_text_by_page=low_text_by_page,
            )
            if not valid:
                rejected.append(
                    {
                        "reason": reason_text,
                        "atom_index": idx,
                        "atom_id": patched.get("atom_id"),
                        "page_start": patched.get("page_start"),
                        "attempted_evidence_text": patched.get("evidence_text", ""),
                    }
                )
                continue
            batch_accepted.append(patched)
        rejected_verbatim = [row for row in rejected if row.get("reason") == "evidence_not_verbatim"]
        if (
            returned_atoms
            and len(batch_accepted) > 0
            and len(rejected_verbatim) / len(returned_atoms) > 0.5
        ):
            retry_prompt = build_verbatim_retry_prompt(
                rejected_verbatim=rejected_verbatim,
                attempted_atoms=returned_atoms,
                document_pages=document_pages,
            )
            try:
                retry_response = client.complete(
                    system=system_prompt,
                    user=retry_prompt,
                    response_schema={"type": "array", "items": atom_schema_resolved},
                    model=model,
                    max_output_tokens=max_output_tokens,
                    max_transient_retries=max_transient_retries,
                )
                retry_atoms, retry_warning = parse_response_atoms(retry_response.parsed)
                if retry_warning:
                    LOGGER.warning("%s batch %s retry: %s", source_document_id, batch.batch_id, retry_warning)
                retry_accepted: list[dict[str, Any]] = []
                for atom in retry_atoms:
                    patched = denormalize_atom(atom, registry_doc, batch.section)
                    valid, reason_text = validate_atom(
                        patched,
                        atom_validator=atom_validator,
                        page_count=page_count,
                        document_pages=document_pages,
                        low_text_by_page=low_text_by_page,
                    )
                    if not valid:
                        continue
                    retry_accepted.append(patched)
                if retry_accepted:
                    retry_ids = {atom.get("atom_id") for atom in retry_accepted if atom.get("atom_id")}
                    if retry_ids:
                        rejected = [r for r in rejected if r.get("atom_id") not in retry_ids]
                    merged_batch_accepted = merge_atoms_by_id(batch_accepted, retry_accepted)
                    recovered = len([atom for atom in retry_accepted if atom.get("atom_id") in retry_ids])
                    batch_accepted = merged_batch_accepted
                    batch_notes.append(f"verbatim_retry: {recovered} atoms recovered of {len(rejected_verbatim)} originally rejected")
            except Exception as exc:  # noqa: BLE001
                batch_notes.append(normalize_rejection_reason("verbatim_retry_failed", exc))
        batch_accepted = assign_sequential_atom_ids(source_document_id, batch_accepted, next_atom_index)
        lines_before = jsonl_line_count(atoms_jsonl_path)
        append_jsonl(atoms_jsonl_path, batch_accepted)
        lines_after = jsonl_line_count(atoms_jsonl_path)
        line_gain = lines_after - lines_before
        if line_gain != len(batch_accepted):
            raise RuntimeError(
                f"jsonl_write_mismatch: batch={batch.batch_id} expected_gain={len(batch_accepted)} actual_gain={line_gain}"
            )
        next_atom_index += len(batch_accepted)
        if returned_atoms and (len(rejected) / len(returned_atoms)) > 0.5:
            LOGGER.warning(
                "%s batch %s high verbatim/schema rejection rate: %s/%s",
                source_document_id,
                batch.batch_id,
                len(rejected),
                len(returned_atoms),
            )
        duration = round(time.time() - batch_start, 2)
        batch_records.append(
            {
                "batch_id": batch.batch_id,
                "section": batch.section,
                "page_start": batch.page_start,
                "page_end": batch.page_end,
                "page_count": len(batch.pages),
                "atoms_returned": len(returned_atoms),
                "atoms_accepted": len(batch_accepted),
                "atoms_rejected": rejected,
                "duration_seconds": duration,
                "input_chars": input_chars,
                "finish_reason": finish_reason or "STOP",
                "notes": batch_notes,
            }
        )
        if request_throttle_seconds > 0:
            time.sleep(request_throttle_seconds)
    totals_accepted = sum(int(batch.get("atoms_accepted", 0)) for batch in batch_records)
    jsonl_lines = jsonl_line_count(atoms_jsonl_path)
    if jsonl_lines != totals_accepted:
        breakdown = [
            {
                "batch_id": batch.get("batch_id"),
                "page_start": batch.get("page_start"),
                "page_end": batch.get("page_end"),
                "atoms_accepted": batch.get("atoms_accepted", 0),
                "atoms_rejected": len(batch.get("atoms_rejected", [])),
            }
            for batch in batch_records
        ]
        LOGGER.error(
            "%s totals mismatch: jsonl_lines=%s totals_accepted=%s breakdown=%s",
            source_document_id,
            jsonl_lines,
            totals_accepted,
            json.dumps(breakdown, ensure_ascii=False),
        )
        raise RuntimeError(
            f"totals_mismatch: source_document_id={source_document_id} jsonl_lines={jsonl_lines} totals_accepted={totals_accepted}"
        )
    totals_rejected = sum(len(batch.get("atoms_rejected", [])) for batch in batch_records)
    run_payload = {
        "source_document_id": source_document_id,
        "started_at": started_at,
        "completed_at": iso_now(),
        "provider": provider,
        "model": model,
        "batches": batch_records,
        "totals": {
            "atoms_accepted": totals_accepted,
            "atoms_rejected": totals_rejected,
            "batches": len(batch_records),
            "skipped_pages": skipped_pages_total,
        },
    }
    write_json(run_json_path, run_payload)
    return "processed", run_payload


def command_extract(args: argparse.Namespace) -> int:
    v1_root = Path(args.root).resolve() if args.root else V1_ROOT
    markdown_root = v1_root / "data/markdown"
    if not markdown_root.exists():
        LOGGER.error("Missing markdown substrate directory: %s", markdown_root)
        return 1
    atom_schema_original, atom_schema_resolved = load_atom_schema(v1_root)
    registry_payload = load_json(v1_root / "data/registry/source_documents.json")
    registry = {row["source_document_id"]: row for row in registry_payload.get("source_documents", [])}

    provider = args.provider
    model = model_for_provider(provider, args.model)
    max_tokens = int(args.max_output_tokens or (24000 if provider == "gemini" else 16000))
    source_ids = sorted(path.name for path in markdown_root.iterdir() if path.is_dir())
    if args.only:
        source_ids = [doc_id for doc_id in source_ids if doc_id == args.only]
    if not source_ids:
        LOGGER.info("No documents matched.")
        return 0

    client = None if args.dry_run else create_client(provider)
    any_processed = False
    for source_document_id in source_ids:
        status, _run = process_document(
            source_document_id=source_document_id,
            v1_root=v1_root,
            provider=provider,
            model=model,
            max_output_tokens=max_tokens,
            request_throttle_seconds=float(args.request_throttle_seconds),
            max_transient_retries=int(args.max_transient_retries),
            pages_override=args.pages,
            force=bool(args.force),
            resume=bool(args.resume),
            dry_run=bool(args.dry_run),
            client=client,
            atom_schema_original=atom_schema_original,
            atom_schema_resolved=atom_schema_resolved,
            registry=registry,
        )
        LOGGER.info("%s -> %s", source_document_id, status)
        if status == "processed":
            any_processed = True
    if args.dry_run:
        return 0
    return 0 if any_processed or args.only else 0


def command_status(args: argparse.Namespace) -> int:
    v1_root = Path(args.root).resolve() if args.root else V1_ROOT
    atoms_root = v1_root / "data/atoms"
    print("| source_document_id | batches | atoms_accepted | atoms_rejected | last_run |")
    print("|---|---:|---:|---:|---|")
    if not atoms_root.exists():
        return 0
    run_files = sorted(atoms_root.glob("*.run.json"))
    for run_file in run_files:
        payload = load_json(run_file)
        totals = payload.get("totals", {})
        last_run = payload.get("completed_at", "")
        print(
            f"| {payload.get('source_document_id', run_file.stem.replace('.run', ''))} "
            f"| {int(totals.get('batches', 0))} | {int(totals.get('atoms_accepted', 0))} "
            f"| {int(totals.get('atoms_rejected', 0))} | {last_run} |"
        )
    return 0


def command_verify(args: argparse.Namespace) -> int:
    v1_root = Path(args.root).resolve() if args.root else V1_ROOT
    atoms_root = v1_root / "data/atoms"
    markdown_root = v1_root / "data/markdown"
    if not atoms_root.exists():
        LOGGER.info("No atoms directory to verify.")
        return 0
    atom_schema_original, _atom_schema_resolved = load_atom_schema(v1_root)
    atom_validator = extract_atom_validator(atom_schema_original)
    failures: list[str] = []
    for jsonl_path in sorted(atoms_root.glob("*.jsonl")):
        source_document_id = jsonl_path.stem
        markdown_dir = markdown_root / source_document_id
        if not markdown_dir.exists():
            failures.append(f"{source_document_id}: missing markdown substrate")
            continue
        doc_json = load_json(markdown_dir / "document.json")
        page_count = int(doc_json.get("page_count", 0))
        document_pages = parse_document_pages(markdown_dir / "document.md")
        low_text_by_page = {p: bool(row.get("is_low_text")) for p, row in parse_pages_jsonl(markdown_dir / "pages.jsonl").items()}
        rows = load_existing_jsonl(jsonl_path)
        for idx, atom in enumerate(rows):
            valid, reason = validate_atom(
                atom,
                atom_validator=atom_validator,
                page_count=page_count,
                document_pages=document_pages,
                low_text_by_page=low_text_by_page,
            )
            if not valid:
                failures.append(f"{source_document_id}: row {idx} -> {reason}")
    if failures:
        print("Verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Verification passed.")
    return 0


def command_reconcile_run(args: argparse.Namespace) -> int:
    v1_root = Path(args.root).resolve() if args.root else V1_ROOT
    atoms_root = v1_root / "data/atoms"
    if not args.only:
        LOGGER.error("reconcile-run requires --only <source_document_id>")
        return 2
    source_document_id = args.only
    run_path = atoms_root / f"{source_document_id}.run.json"
    jsonl_path = atoms_root / f"{source_document_id}.jsonl"
    if not run_path.exists():
        LOGGER.error("Missing run file: %s", run_path)
        return 1
    run_payload = load_json(run_path)
    batches = run_payload.get("batches", [])
    sum_batch_accepted = sum(int(batch.get("atoms_accepted", 0)) for batch in batches)
    sum_batch_rejected = sum(len(batch.get("atoms_rejected", [])) for batch in batches)
    totals = run_payload.get("totals", {})
    totals_accepted = int(totals.get("atoms_accepted", 0))
    totals_rejected = int(totals.get("atoms_rejected", 0))
    jsonl_lines = jsonl_line_count(jsonl_path)

    print(f"source_document_id: {source_document_id}")
    print(f"sum(batch.atoms_accepted): {sum_batch_accepted}")
    print(f"run.totals.atoms_accepted: {totals_accepted}")
    print(f"jsonl_lines: {jsonl_lines}")
    print(f"sum(batch.atoms_rejected): {sum_batch_rejected}")
    print(f"run.totals.atoms_rejected: {totals_rejected}")
    if sum_batch_accepted != totals_accepted or totals_accepted != jsonl_lines:
        print("discrepancy: yes")
        print("| batch_id | page_start | page_end | atoms_accepted | atoms_rejected | notes |")
        print("|---:|---:|---:|---:|---:|---|")
        for batch in batches:
            notes = "; ".join(str(n) for n in batch.get("notes", []))
            print(
                f"| {int(batch.get('batch_id', 0))} "
                f"| {int(batch.get('page_start', 0))} "
                f"| {int(batch.get('page_end', 0))} "
                f"| {int(batch.get('atoms_accepted', 0))} "
                f"| {len(batch.get('atoms_rejected', []))} "
                f"| {notes} |"
            )
        return 1
    print("discrepancy: no")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Stage-2 atom extraction from v1 substrate.")
    parser.add_argument("--root", type=str, default=str(V1_ROOT), help="Override v1 root directory.")
    parser.add_argument("--verbose", action="store_true", help="Enable DEBUG logging.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract_parser = subparsers.add_parser("extract", help="Extract atoms from v1/data/markdown.")
    extract_parser.add_argument("--only", type=str, default=None)
    extract_parser.add_argument("--provider", choices=["gemini", "openai"], default="gemini")
    extract_parser.add_argument("--model", type=str, default=None)
    extract_parser.add_argument("--resume", action="store_true")
    extract_parser.add_argument("--dry-run", action="store_true")
    extract_parser.add_argument("--max-output-tokens", type=int, default=None)
    extract_parser.add_argument("--request-throttle-seconds", type=float, default=0.0)
    extract_parser.add_argument("--max-transient-retries", type=int, default=5)
    extract_parser.add_argument("--pages", type=str, default=None, help='Page selection override, e.g. "1-30,45-60".')
    extract_parser.add_argument("--force", action="store_true")

    subparsers.add_parser("status", help="Print extraction run status table.")
    subparsers.add_parser("verify", help="Verify existing atoms against substrate.")
    reconcile_parser = subparsers.add_parser("reconcile-run", help="Reconcile run.json totals with JSONL line counts.")
    reconcile_parser.add_argument("--only", type=str, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try:
        if args.command == "extract":
            return command_extract(args)
        if args.command == "status":
            return command_status(args)
        if args.command == "verify":
            return command_verify(args)
        if args.command == "reconcile-run":
            return command_reconcile_run(args)
        parser.error(f"Unknown command: {args.command}")
    except ModelConfigurationError as exc:
        LOGGER.error("%s", exc)
        if "gemini_model_not_found" in str(exc):
            LOGGER.error(
                "Gemini model not found. Try --model gemini-2.5-flash "
                "or another valid Gemini model available to your account."
            )
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())

