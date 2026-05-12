#!/usr/bin/env python3
"""Stage-3 synthesis: select atoms, call LLM, write policy_summary JSON.

Dependencies (install in your environment):
  pip install jsonschema google-genai openai

Usage:
  python v1/scripts/v1_synthesize.py synthesize
  python v1/scripts/v1_synthesize.py synthesize --only chl_parcc_biobio_2025
  python v1/scripts/v1_synthesize.py synthesize --provider openai --model gpt-4.1 --focus mitigation
  python v1/scripts/v1_synthesize.py synthesize --force
  python v1/scripts/v1_synthesize.py status
  python v1/scripts/v1_synthesize.py verify
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
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

LOGGER = logging.getLogger("v1_synthesize")

V1_ROOT = Path(__file__).resolve().parent.parent
GEMINI_DEFAULT_MODEL = "gemini-2.5-pro"
OPENAI_DEFAULT_MODEL = "gpt-4.1"

FAMILY_RUBRIC: dict[str, str] = {
    "parcc": "v1/rubrics/parcc.md",
    "paccc": "v1/rubrics/parcc.md",
    "sector_plan": "v1/rubrics/sector_plan.md",
    "framework": "v1/rubrics/framework.md",
    "territorial_plan": "v1/rubrics/territorial_plan_thin.md",
    "environmental_program": "v1/rubrics/environmental_program.md",
}

# Diagnostic minimum signal counts (non-blocking). Keys match `family` from registry mapping.
SIGNAL_MIN_PER_FAMILY: dict[str, int] = {
    "parcc": 30,
    "paccc": 30,
    "sector_plan": 40,
    "framework": 25,
    "territorial_plan": 5,
    "environmental_program": 35,
    "other": 5,
}

# Map family to OUTPUT CONTRACT volume text (paccc reuses parcc).
_SIGNAL_VOLUME_CONTRACT_KEY: dict[str, str] = {
    "paccc": "parcc",
}

SIGNAL_VOLUME_CONTRACT_BY_FAMILY: dict[str, str] = {
    "parcc": (
        "Expected total policy_signals for this family: **40–70** (aim upper half when atoms support it).\n"
        "Per-type mix (typical PARCC): sector 4–8, action 12–25, target 5–10, funding 3–6, "
        "monitoring 5–10, governance 2–5, risk 5–12, context 2–5."
    ),
    "sector_plan": (
        "Expected total policy_signals for this family: **60–100** (aim upper half when atoms support it).\n"
        "Per-type mix (typical sector plan): sector 1–3 (sector is locked in document), action 25–40, "
        "target 10–20, funding 5–10, monitoring 10–20, governance 4–8, risk 1–4, context 2–5."
    ),
    "framework": (
        "Expected total policy_signals for this family: **30–50** (aim upper half when atoms support it).\n"
        "Per-type mix (typical framework): sector 5–12, action 2–5, target 10–20, funding 1–3, "
        "monitoring 3–6, governance 4–10, risk 2–5, context 4–8."
    ),
    "territorial_plan": (
        "Expected total policy_signals for this family: **10–20** (thin instrument; cap total).\n"
        "Mostly sector + context + risk; fewer discrete actions/targets than sector plans."
    ),
    "environmental_program": (
        "Expected total policy_signals for this family: **50–80** (aim upper half when atoms support it).\n"
        "Per-type mix (typical PRAS): sector 3–6, action 20–35, target 5–10, funding 5–10, "
        "monitoring 8–15, governance 4–8, risk 3–6, context 2–5."
    ),
    "other": (
        "Expected total policy_signals: use judgment from atom density; prefer high recall over consolidation."
    ),
}

# Backstop selection caps per (family, focus="mitigation").
# For adaptation, swap priority to adaptation atoms; for "all", use 1.5× the mitigation cap.
SELECTION_CAPS: dict[tuple[str, str], dict[str, int]] = {
    ("parcc", "mitigation"): {
        "target": 10,
        "action": 25,
        "sector_priority": 8,
        "monitoring": 8,
        "governance": 6,
        "funding": 5,
        "risk": 12,
        "context": 6,
        "actor": 8,
        "timeline": 6,
    },
    ("sector_plan", "mitigation"): {
        "target": 25,
        "action": 40,
        "sector_priority": 10,
        "monitoring": 20,
        "funding": 20,
        "governance": 15,
        "risk": 10,
        "context": 8,
        "actor": 10,
        "timeline": 10,
    },
    ("framework", "mitigation"): {
        "target": 20,
        "sector_priority": 15,
        "context": 12,
        "governance": 10,
        "risk": 6,
        "action": 5,
        "funding": 3,
        "monitoring": 5,
        "actor": 5,
        "timeline": 5,
    },
    ("territorial_plan", "mitigation"): {
        "target": 3,
        "action": 5,
        "sector_priority": 4,
        "monitoring": 2,
        "governance": 2,
        "funding": 2,
        "risk": 4,
        "context": 3,
        "actor": 2,
        "timeline": 2,
    },
    ("environmental_program", "mitigation"): {
        "target": 10,
        "action": 25,
        "sector_priority": 6,
        "monitoring": 10,
        "governance": 8,
        "funding": 10,
        "risk": 6,
        "context": 5,
        "actor": 8,
        "timeline": 5,
    },
}

_DOC_STATUS_WEIGHT: dict[str, int] = {
    "final": 4,
    "draft": 3,
    "consultation": 2,
    "proposal": 1,
    "placeholder": 0,
    "unknown": 2,
}
_EVIDENCE_KIND_WEIGHT: dict[str, int] = {
    "quantitative": 2,
    "qualitative": 1,
    "categorical": 0,
}
_EXPLICITNESS_WEIGHT: dict[str, int] = {
    "explicit": 1,
    "inferred": 0,
}

ATOM_PROMPT_FIELDS = [
    "atom_id",
    "primitive_type",
    "evidence_kind",
    "evidence_text",
    "page_start",
    "page_end",
    "plain_language_summary",
    "sector",
    "theme",
    "measure_type",
    "action_statement",
    "target_value_text",
    "raw_value_numeric",
    "raw_unit",
    "timeline",
    "responsible_actor",
    "supporting_actors",
    "funding_source",
    "funding_amount",
    "monitoring_indicator",
    "verification_method",
    "review_cycle",
    "readiness_status",
    "explicitness",
    "applicability_scope",
    "region_code",
    "communal_code",
    "notes",
]


class ModelConfigurationError(RuntimeError):
    """Raised when a provider model is invalid or retired."""


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


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def transient_backoff(attempt: int) -> int:
    return min(15 * (2**attempt), 240)


def strip_markdown_json_fence(raw: str) -> str:
    text = raw.strip()
    match = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else text


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_atoms_jsonl(path: Path) -> list[dict[str, Any]]:
    atoms: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            atoms.append(json.loads(line))
    return atoms


def strip_formats(node: Any) -> Any:
    if isinstance(node, dict):
        return {k: strip_formats(v) for k, v in node.items() if k != "format" and not k.startswith("$")}
    if isinstance(node, list):
        return [strip_formats(item) for item in node]
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


def simplify_for_structured_output(node: Any) -> Any:
    allowed = {
        "type", "properties", "required", "items", "enum",
        "minimum", "maximum", "minItems", "maxItems",
        "minLength", "maxLength", "description",
    }
    if isinstance(node, dict):
        out: dict[str, Any] = {}
        for key, value in node.items():
            if key == "properties" and isinstance(value, dict):
                out[key] = {k: simplify_for_structured_output(v) for k, v in value.items()}
                continue
            if key in allowed:
                out[key] = simplify_for_structured_output(value)
        return out
    if isinstance(node, list):
        return [simplify_for_structured_output(item) for item in node]
    return node


def load_summary_schema(v1_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return (original_schema, structured_output_ready_schema)."""
    schema = load_json(v1_root / "schemas/policy_summary.schema.json")
    resolved = resolve_refs(copy.deepcopy(schema), schema)
    resolved = strip_formats(resolved)
    for meta_key in ("title", "description", "$schema", "$id"):
        resolved.pop(meta_key, None)
    resolved = simplify_for_structured_output(resolved)
    return schema, resolved


def caps_for(family: str, focus: str) -> dict[str, int]:
    """Derive per-primitive selection caps for (family, focus)."""
    mit_caps = SELECTION_CAPS.get((family, "mitigation"), {})
    if focus == "mitigation":
        return dict(mit_caps)
    if focus == "adaptation":
        # Mirror: swap mitigation-emphasis primitives
        return {k: v for k, v in mit_caps.items()}
    # focus == "all": use ceiling(1.5 × mitigation cap) per type
    return {k: max(1, int(v * 1.5)) for k, v in mit_caps.items()}


def _atom_priority_key(atom: dict[str, Any], focus: str) -> tuple[int, int, int, int, int]:
    """Composite sort key (all descending — negate for sort)."""
    doc_status = atom.get("doc_status", atom.get("_doc_status", "unknown"))
    status_w = _DOC_STATUS_WEIGHT.get(str(doc_status), 2)
    measure_type = atom.get("measure_type", "unknown")
    if focus in ("mitigation", "all"):
        focus_w = 2 if measure_type == "mitigation" else (1 if measure_type == "transversal" else 0)
    else:
        focus_w = 2 if measure_type == "adaptation" else (1 if measure_type == "transversal" else 0)
    evidence_kind = atom.get("evidence_kind", "qualitative")
    ev_w = _EVIDENCE_KIND_WEIGHT.get(str(evidence_kind), 0)
    numeric_w = 1 if atom.get("raw_value_numeric") is not None else 0
    explicitness = atom.get("explicitness", "inferred")
    exp_w = _EXPLICITNESS_WEIGHT.get(str(explicitness), 0)
    return (status_w, focus_w, ev_w, numeric_w, exp_w)


def select_atoms(
    atoms: list[dict[str, Any]],
    family: str,
    focus: str,
) -> list[dict[str, Any]]:
    """Select and rank atoms per family rubric caps. Pure function."""
    caps = caps_for(family, focus)
    by_type: dict[str, list[dict[str, Any]]] = {}
    for atom in atoms:
        ptype = str(atom.get("primitive_type", "context"))
        by_type.setdefault(ptype, []).append(atom)

    selected: list[dict[str, Any]] = []
    for ptype, group in by_type.items():
        cap = caps.get(ptype)
        if cap is None:
            # Uncapped primitive types — take all
            ranked = sorted(group, key=lambda a: _atom_priority_key(a, focus), reverse=True)
        else:
            ranked = sorted(group, key=lambda a: _atom_priority_key(a, focus), reverse=True)[:cap]
        selected.extend(ranked)
    return selected


def _slim_atom(atom: dict[str, Any]) -> dict[str, Any]:
    """Return only the fields the LLM needs for synthesis."""
    return {k: atom[k] for k in ATOM_PROMPT_FIELDS if k in atom}


def require_registry_source_level(registry_doc: dict[str, Any], source_document_id: str) -> str:
    """Registry must supply source_level before synthesis (downstream filtering)."""
    sl = str(registry_doc.get("source_level") or "").strip()
    if not sl:
        raise ModelConfigurationError(
            f"registry_missing_source_level:source_document_id={source_document_id}"
        )
    return sl


def infer_applicability_scope(registry_doc: dict[str, Any]) -> str:
    """Default applicability_scope when registry does not set it."""
    raw = str(registry_doc.get("applicability_scope") or "").strip()
    if raw:
        return raw
    sl = str(registry_doc.get("source_level") or "").strip().lower()
    tn = str(registry_doc.get("territory_name") or "").strip()
    rc = str(registry_doc.get("region_code") or "").strip()
    if sl == "national":
        return tn or "Chile"
    if sl == "regional":
        if tn and tn.lower() not in ("chile", ""):
            return tn
        if rc and rc not in ("", "00"):
            return f"Región {rc}"
        return "Chile (regional)"
    if sl in ("municipal", "communal", "intercommunal"):
        parts = [p for p in (tn, f"código territorial {rc}" if rc else "") if p]
        return ", ".join(parts) if parts else sl
    return tn or sl or "Chile"


def merge_registry_into_summary(
    summary: dict[str, Any],
    registry_doc: dict[str, Any],
    *,
    source_document_id: str,
    family: str,
) -> None:
    """Overwrite envelope fields from registry (do not rely on the LLM for these).

    Precondition: ``registry_doc`` includes a non-empty ``source_level`` (validated by
    ``require_registry_source_level`` before synthesis).
    """
    summary["source_document_id"] = source_document_id
    summary["source_name"] = str(registry_doc.get("source_name") or "")
    url = str(registry_doc.get("source_url") or "").strip()
    if url:
        summary["source_url"] = url
    else:
        summary.pop("source_url", None)
    summary["family"] = family
    summary["document_type"] = str(registry_doc.get("document_type") or "")
    ds = str(registry_doc.get("document_status") or "").strip()
    summary["document_status"] = ds if ds else "unknown"
    summary["publisher"] = str(registry_doc.get("publisher") or "")
    py = registry_doc.get("publication_year")
    if py is not None and str(py).strip() != "":
        try:
            summary["publication_year"] = int(py)
        except (TypeError, ValueError):
            summary.pop("publication_year", None)
    summary["region_code"] = str(registry_doc.get("region_code") or "")
    summary["communal_code"] = str(registry_doc.get("communal_code") or "")
    summary["source_level"] = str(registry_doc.get("source_level") or "").strip()
    summary["applicability_scope"] = infer_applicability_scope(registry_doc)


def apply_signal_actor_defaults(summary: dict[str, Any], *, default_actor_level: str) -> None:
    """Fill missing policy_signal actor_level from document source_level."""
    if not default_actor_level:
        return
    sigs = summary.get("policy_signals")
    if not isinstance(sigs, list):
        return
    for sig in sigs:
        if not isinstance(sig, dict):
            continue
        current = str(sig.get("actor_level") or "").strip()
        if not current:
            sig["actor_level"] = default_actor_level


def prepare_candidate_for_validation(
    summary: dict[str, Any],
    *,
    registry_doc: dict[str, Any],
    source_document_id: str,
    family: str,
) -> None:
    merge_registry_into_summary(summary, registry_doc, source_document_id=source_document_id, family=family)
    apply_signal_actor_defaults(
        summary,
        default_actor_level=str(registry_doc.get("source_level") or "").strip(),
    )


def signal_diagnostic_flags(
    summary: dict[str, Any],
    *,
    family: str,
    atom_count_input: int,
    source_document_id: str,
) -> tuple[bool, bool]:
    """Return (low_yield_warning, low_atom_coverage_warning); log warnings (non-blocking)."""
    expected_min = SIGNAL_MIN_PER_FAMILY.get(family, SIGNAL_MIN_PER_FAMILY["other"])
    sigs = summary.get("policy_signals")
    n = len(sigs) if isinstance(sigs, list) else 0
    low_yield = n < expected_min
    if low_yield:
        LOGGER.warning(
            "Low signal yield: %d signals for %s (family=%s, expected >= %d). atom_count_input=%d.",
            n,
            source_document_id,
            family,
            expected_min,
            atom_count_input,
        )
    cited: set[str] = set()
    if isinstance(sigs, list):
        for sig in sigs:
            if not isinstance(sig, dict):
                continue
            for aid in sig.get("supporting_atom_ids") or []:
                cited.add(str(aid))
    coverage = len(cited) / max(1, atom_count_input)
    low_cov = coverage < 0.30
    if low_cov:
        LOGGER.warning(
            "Low atom coverage: only %d/%d atoms (%d%%) cited by policy_signals.",
            len(cited),
            atom_count_input,
            int(round(100 * coverage)),
        )
    return low_yield, low_cov


def _signal_volume_contract_text(family: str) -> str:
    key = _SIGNAL_VOLUME_CONTRACT_KEY.get(family, family)
    return SIGNAL_VOLUME_CONTRACT_BY_FAMILY.get(key, SIGNAL_VOLUME_CONTRACT_BY_FAMILY["other"])


def summary_shape_reference(schema: dict[str, Any]) -> str:
    """Produce a condensed shape reference for the system prompt."""
    props = schema.get("properties", {})
    lines = ["POLICY_SUMMARY TOP-LEVEL FIELDS AND KEY SUBSTRUCTURE"]
    for field, sub in props.items():
        if field == "evidence_anchors":
            lines.append(
                "evidence_anchors: array of {atom_id, page_start, page_end, page_reference, evidence_text}"
            )
        elif field == "synthesis_run":
            lines.append("synthesis_run: {created_at, created_by, atom_count_input, atom_count_selected, ...}")
        elif sub.get("type") == "array":
            item_props = sub.get("items", {}).get("properties", {})
            req = sub.get("items", {}).get("required", [])
            lines.append(f"{field}: array of {{{', '.join(item_props.keys())}}} required={req}")
        elif sub.get("type") == "object":
            obj_props = list(sub.get("properties", {}).keys())
            lines.append(f"{field}: object {{{', '.join(obj_props)}}}")
        else:
            lines.append(f"{field}: {sub.get('type', 'any')}")
    return "\n".join(lines)


def build_system_prompt(v1_root: Path, family: str, summary_schema: dict[str, Any]) -> str:
    rubric_rel = FAMILY_RUBRIC[family]
    # Rubric paths are relative to the v1 root's *parent parent* (repo root) but
    # in practice they live at v1_root / rubrics/<family>.md
    rubric_path = v1_root / "rubrics" / Path(rubric_rel).name
    rubric_text = rubric_path.read_text(encoding="utf-8")

    volume_lines = _signal_volume_contract_text(family)
    output_contract = (
        "OUTPUT CONTRACT\n"
        "You output a single JSON object conforming to the policy_summary schema and nothing else. "
        "No prose, no markdown fences. The first character of your response must be '{' and the last must be '}'.\n\n"
        "**Primary deliverable — `policy_signals[]`:** This array is the canonical structured output for downstream "
        "pipelines (profiling, matching). Produce **one signal per meaningful unit of evidence** supported by the "
        "selected atoms. Do **not** consolidate distinct facts into one signal to reduce count. Example: a quantified "
        "target and a related implementation measure should be **separate** signals (e.g. `target` + `action`), not merged.\n\n"
        "**Expected signal counts for this document family:**\n"
        "- parcc / paccc: total **40–70** signals\n"
        "- sector_plan: total **60–100** signals\n"
        "- framework: total **30–50** signals\n"
        "- territorial_plan: total **10–20** signals (capped)\n"
        "- environmental_program: total **50–80** signals\n\n"
        "Aim for the **upper half** of the expected total when the atoms support it.\n\n"
        "**Family-specific mix (guidance):**\n"
        f"{volume_lines}\n\n"
        "**Secondary (human-readable) grouped arrays:** After `policy_signals[]` and `evidence_anchors`, you may "
        "**optionally** populate priority_sectors, headline_targets, named_actions, governance, funding, monitoring, "
        "and risks_identified as a readable view **derived from** the signals. These grouped arrays are **not** the "
        "primary output — leave them empty or sparse if time/token budget is tight.\n\n"
        "Every `evidence_anchor_id` in grouped arrays must reference an `atom_id` present in `evidence_anchors`. "
        "Every `supporting_atom_id` in `policy_signals[]` must appear in `evidence_anchors` with the same verbatim "
        "`evidence_text` as the atom. Do not invent atom_ids; use only SELECTED ATOMS."
    )
    shape_ref = summary_shape_reference(summary_schema)
    return rubric_text + "\n\n" + output_contract + "\n\n" + shape_ref


def build_user_prompt(
    *,
    source_document_id: str,
    registry_doc: dict[str, Any],
    focus: str,
    selected_atoms: list[dict[str, Any]],
) -> str:
    catalog_block = (
        "CATALOG\n"
        f"source_document_id: {source_document_id}\n"
        f"source_name: {registry_doc.get('source_name', '')}\n"
        f"document_type: {registry_doc.get('document_type', '')}\n"
        f"document_status: {registry_doc.get('document_status', '')}\n"
        f"source_level: {registry_doc.get('source_level', '')}\n"
        f"region_code: {registry_doc.get('region_code', '')}\n"
        f"communal_code: {registry_doc.get('communal_code', '')}\n"
        f"publisher: {registry_doc.get('publisher', '')}\n"
        f"publication_year: {registry_doc.get('publication_year', '')}"
    )
    focus_block = f"FOCUS\n{focus}"
    slim_atoms = [_slim_atom(a) for a in selected_atoms]
    atoms_block = "SELECTED ATOMS\n" + json.dumps(slim_atoms, ensure_ascii=False, indent=2)
    task_block = (
        "TASK\n"
        "1) **policy_signals[] (primary):** Build a dense list of signals — one per substantive fact or commitment "
        "you can ground in SELECTED ATOMS (targets, actions, sector priorities, funding, governance, monitoring, risks, context). "
        "Meet the family signal-count targets in the OUTPUT CONTRACT; prefer high recall over merging. "
        "Each signal: policy_signal_id (unique, pattern <source_document_id>_sig_<NNNN>), signal_type, signal_label, "
        "signal_code (or empty string), actor_level (override only when the signal clearly names a different jurisdictional level; "
        "otherwise match the document), supporting_atom_ids (non-empty; only atom_ids from SELECTED ATOMS).\n"
        "2) **evidence_anchors:** Include every atom_id referenced by any grouped array **or** any policy_signals[].supporting_atom_ids, "
        "once each, with page_start, page_end, page_reference, evidence_text copied verbatim from the atom.\n"
        "3) **Grouped arrays (optional):** If you populate them, derive from signals; each evidence_anchor_id must exist in evidence_anchors.\n\n"
        "Return ONLY the JSON object."
    )
    return "\n\n".join([catalog_block, focus_block, atoms_block, task_block])


def build_correction_prompt(errors: list[str], original_output: str) -> str:
    return (
        "CORRECTION REQUIRED\n"
        "The previous response had the following validation errors:\n"
        + "\n".join(f"- {e}" for e in errors)
        + "\n\nOriginal response:\n"
        + original_output
        + "\n\nPlease return a corrected JSON object that fixes all of these errors. "
        "Return ONLY the corrected JSON object."
    )


def parse_summary_response(raw: str) -> dict[str, Any]:
    """Parse LLM response to dict, stripping markdown fences."""
    cleaned = strip_markdown_json_fence(raw)
    return json.loads(cleaned)


def validate_summary(
    summary: dict[str, Any],
    *,
    schema: dict[str, Any],
    input_atom_ids: set[str],
    focus: str,
) -> list[str]:
    """Run all validation checks. Returns list of error strings (empty = valid)."""
    try:
        import jsonschema
    except ImportError as exc:
        raise RuntimeError("jsonschema is required. Install with: pip install jsonschema") from exc

    errors: list[str] = []

    # 1. JSON Schema validation
    validator = jsonschema.Draft202012Validator(schema)
    schema_errors = list(validator.iter_errors(summary))
    for err in schema_errors:
        errors.append(f"schema:{err.json_path}:{err.message}")

    # 2. Build anchor lookup
    anchors = summary.get("evidence_anchors", [])
    anchor_ids: set[str] = set()
    seen_ids: list[str] = []
    for anchor in anchors:
        aid = anchor.get("atom_id", "")
        seen_ids.append(aid)
        anchor_ids.add(aid)

    # 3. evidence_anchors uniqueness
    if len(seen_ids) != len(set(seen_ids)):
        from collections import Counter
        counts = Counter(seen_ids)
        dupes = [aid for aid, cnt in counts.items() if cnt > 1]
        errors.append(f"evidence_anchors_duplicate_atom_ids:{dupes}")

    # 4. atom_id existence: every anchor atom_id must be from input
    for aid in anchor_ids:
        if aid not in input_atom_ids:
            errors.append(f"hallucinated_atom_id:{aid}")

    # 5. Cross-reference: every evidence_anchor_id in claim arrays must be in evidence_anchors
    claim_fields = [
        "priority_sectors",
        "headline_targets",
        "named_actions",
        "risks_identified",
    ]
    for field in claim_fields:
        items = summary.get(field) or []
        for item in items:
            ref = item.get("evidence_anchor_id")
            if ref and ref not in anchor_ids:
                errors.append(f"dangling_evidence_anchor_id:{field}:{ref}")

    for singular_field in ("governance", "funding", "monitoring"):
        obj = summary.get(singular_field) or {}
        ref = obj.get("evidence_anchor_id")
        if ref and ref not in anchor_ids:
            errors.append(f"dangling_evidence_anchor_id:{singular_field}:{ref}")

    # policy_signals: unique ids; supporting_atom_ids ⊆ input and ⊆ evidence_anchors
    sigs = summary.get("policy_signals")
    if isinstance(sigs, list):
        seen_pid: set[str] = set()
        for idx, sig in enumerate(sigs):
            if not isinstance(sig, dict):
                errors.append(f"policy_signals:{idx}:not_object")
                continue
            pid = str(sig.get("policy_signal_id", "") or "")
            if pid in seen_pid:
                errors.append(f"policy_signals:duplicate_policy_signal_id:{pid}")
            if pid:
                seen_pid.add(pid)
            aids = sig.get("supporting_atom_ids")
            if not isinstance(aids, list):
                errors.append(f"policy_signals:{pid or idx}:supporting_atom_ids_invalid")
                continue
            for atom_id in aids:
                aid = str(atom_id)
                if aid not in input_atom_ids:
                    errors.append(f"policy_signal_supporting_unknown_atom:{pid}:{aid}")
                if aid not in anchor_ids:
                    errors.append(f"policy_signal_supporting_not_in_evidence_anchors:{pid}:{aid}")
    elif sigs is not None:
        errors.append("policy_signals:not_array")

    # 6. mitigation_emphasis sanity
    if focus == "mitigation":
        mit_emphasis = summary.get("mitigation_emphasis")
        if mit_emphasis not in (None, "absent") and not anchor_ids:
            errors.append(
                f"mitigation_emphasis_sanity:no_anchors_but_emphasis_is_{mit_emphasis}"
            )

    return errors


class GeminiClient:
    def __init__(self, api_key: str | None = None) -> None:
        key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY (or GOOGLE_API_KEY) is required for gemini provider")
        try:
            from google import genai
        except ImportError as exc:
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
            response_schema=response_schema,
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
                finish_reason = str(
                    getattr(getattr(response, "candidates", [None])[0], "finish_reason", "") or None
                )
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
        except ImportError as exc:
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
        except ImportError as exc:
            raise RuntimeError("openai SDK is not installed") from exc
        text_format: dict[str, Any] = {
            "type": "json_schema",
            "name": "policy_summary",
            "strict": False,
            "schema": response_schema,
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


def family_for_document_type(document_type: str) -> str | None:
    """Map document_type from registry to a family key."""
    return FAMILY_RUBRIC.get(document_type.lower()) and document_type.lower()


def synthesize_document(
    *,
    source_document_id: str,
    v1_root: Path,
    provider: str,
    model: str,
    focus: str,
    max_output_tokens: int,
    max_transient_retries: int,
    force: bool,
    client: LLMClient,
    summary_schema_original: dict[str, Any],
    summary_schema_resolved: dict[str, Any],
    registry: dict[str, dict[str, Any]],
) -> tuple[str, dict[str, Any] | None]:
    """Run synthesis for one document. Returns (status, run_payload)."""
    atoms_path = v1_root / "data/atoms" / f"{source_document_id}.jsonl"
    summaries_dir = v1_root / "data/summaries"
    summary_path = summaries_dir / f"{source_document_id}.json"
    run_path = summaries_dir / f"{source_document_id}.run.json"
    quarantine_dir = summaries_dir / "quarantine"

    # Idempotency check
    if summary_path.exists() and not force:
        LOGGER.info("%s skipped: summary already exists (use --force)", source_document_id)
        return "skipped_idempotent", None

    # Atoms presence check
    if not atoms_path.exists():
        LOGGER.info("%s skipped: no atoms file", source_document_id)
        return "skipped_no_atoms", None

    atoms = load_atoms_jsonl(atoms_path)
    atom_count_input = len(atoms)

    # Family resolution
    registry_doc = registry.get(source_document_id, {})
    document_type = str(registry_doc.get("document_type", ""))
    family = family_for_document_type(document_type)
    if family is None or family not in FAMILY_RUBRIC:
        LOGGER.error("%s skipped: unmapped document_type=%r", source_document_id, document_type)
        return "skipped_unmapped_family", None

    # Data quality gate: downstream filtering requires registry source_level
    require_registry_source_level(registry_doc, source_document_id)

    rubric_rel = FAMILY_RUBRIC[family]
    started_at = iso_now()

    # Atom selection
    selected_atoms = select_atoms(atoms, family, focus)
    atom_count_selected = len(selected_atoms)

    selection_by_primitive: dict[str, int] = {}
    for atom in selected_atoms:
        ptype = str(atom.get("primitive_type", "context"))
        selection_by_primitive[ptype] = selection_by_primitive.get(ptype, 0) + 1

    notes_parts: list[str] = []
    if atom_count_input < 10:
        notes_parts.append(f"thin_atom_set:only_{atom_count_input}_atoms")

    # Check for zero mitigation atoms under focus=mitigation
    mit_atoms = [
        a for a in selected_atoms
        if a.get("measure_type") in ("mitigation", "transversal")
    ] if focus == "mitigation" else selected_atoms
    zero_mitigation = focus == "mitigation" and len(mit_atoms) == 0

    system_prompt = build_system_prompt(v1_root, family, summary_schema_original)
    user_prompt = build_user_prompt(
        source_document_id=source_document_id,
        registry_doc=registry_doc,
        focus=focus,
        selected_atoms=selected_atoms,
    )
    input_chars = len(system_prompt) + len(user_prompt)
    input_atom_ids = {str(a["atom_id"]) for a in atoms if "atom_id" in a}

    call_start = time.time()
    raw_text: str = ""
    validation_errors: list[str] = []
    summary_obj: dict[str, Any] | None = None

    # --- First LLM call ---
    try:
        response = client.complete(
            system=system_prompt,
            user=user_prompt,
            response_schema=summary_schema_resolved,
            model=model,
            max_output_tokens=max_output_tokens,
            max_transient_retries=max_transient_retries,
        )
        raw_text = response.text or ""
    except Exception as exc:  # noqa: BLE001
        LOGGER.error("%s LLM call failed: %s", source_document_id, exc)
        return "error_llm", None

    try:
        candidate = response.parsed if response.parsed and isinstance(response.parsed, dict) else parse_summary_response(raw_text)
    except (json.JSONDecodeError, ValueError) as exc:
        LOGGER.warning("%s parse failed on first attempt: %s", source_document_id, exc)
        candidate = None
        validation_errors = [f"json_parse_error:{exc}"]

    if candidate is not None:
        prepare_candidate_for_validation(
            candidate,
            registry_doc=registry_doc,
            source_document_id=source_document_id,
            family=family,
        )
        validation_errors = validate_summary(
            candidate,
            schema=summary_schema_original,
            input_atom_ids=input_atom_ids,
            focus=focus,
        )

    # --- One corrective retry ---
    if validation_errors:
        LOGGER.info("%s validation errors on first attempt (%d), retrying", source_document_id, len(validation_errors))
        correction_prompt = build_correction_prompt(validation_errors, raw_text)
        try:
            retry_response = client.complete(
                system=system_prompt,
                user=correction_prompt,
                response_schema=summary_schema_resolved,
                model=model,
                max_output_tokens=max_output_tokens,
                max_transient_retries=max_transient_retries,
            )
            retry_text = retry_response.text or ""
            try:
                retry_candidate = (
                    retry_response.parsed
                    if retry_response.parsed and isinstance(retry_response.parsed, dict)
                    else parse_summary_response(retry_text)
                )
                prepare_candidate_for_validation(
                    retry_candidate,
                    registry_doc=registry_doc,
                    source_document_id=source_document_id,
                    family=family,
                )
                retry_errors = validate_summary(
                    retry_candidate,
                    schema=summary_schema_original,
                    input_atom_ids=input_atom_ids,
                    focus=focus,
                )
                if not retry_errors:
                    candidate = retry_candidate
                    validation_errors = []
                    notes_parts.append("corrective_retry_succeeded")
                else:
                    validation_errors = retry_errors
                    notes_parts.append(f"corrective_retry_still_invalid:{len(retry_errors)}_errors")
            except (json.JSONDecodeError, ValueError) as exc2:
                validation_errors = [f"retry_json_parse_error:{exc2}"]
                notes_parts.append("corrective_retry_parse_failed")
        except Exception as exc:  # noqa: BLE001
            LOGGER.error("%s retry LLM call failed: %s", source_document_id, exc)
            validation_errors.append(f"retry_llm_error:{exc}")

    duration_seconds = round(time.time() - call_start, 2)
    completed_at = iso_now()

    run_payload: dict[str, Any] = {
        "source_document_id": source_document_id,
        "started_at": started_at,
        "completed_at": completed_at,
        "provider": provider,
        "model": model,
        "rubric_path": rubric_rel,
        "focus": focus,
        "atom_count_input": atom_count_input,
        "atom_count_selected": atom_count_selected,
        "selection_by_primitive": selection_by_primitive,
        "duration_seconds": duration_seconds,
        "input_chars": input_chars,
        "validation_errors": validation_errors,
        "notes": "; ".join(notes_parts) if notes_parts else "",
    }

    if validation_errors or candidate is None:
        # Quarantine
        quarantine_dir.mkdir(parents=True, exist_ok=True)
        attempt_path = quarantine_dir / f"{source_document_id}.attempt.json"
        errors_path = quarantine_dir / f"{source_document_id}.errors.json"
        write_json(attempt_path, candidate if candidate else {"raw": raw_text})
        write_json(errors_path, {"validation_errors": validation_errors, "run": run_payload})
        LOGGER.warning(
            "%s quarantined after validation failure: %d errors",
            source_document_id,
            len(validation_errors),
        )
        write_json(run_path, run_payload)
        return "quarantined", run_payload

    low_yield, low_cov = signal_diagnostic_flags(
        candidate,
        family=family,
        atom_count_input=atom_count_input,
        source_document_id=source_document_id,
    )
    run_payload["low_yield_warning"] = low_yield
    run_payload["low_atom_coverage_warning"] = low_cov

    # Inject synthesis_run metadata into summary
    candidate["synthesis_run"] = {
        "created_at": started_at,
        "created_by": f"v1_synthesize/{model}",
        "provider": provider,
        "model": model,
        "rubric_path": rubric_rel,
        "focus": focus,
        "atom_count_input": atom_count_input,
        "atom_count_selected": atom_count_selected,
        "notes": "; ".join(notes_parts) if notes_parts else "",
    }
    if low_yield:
        candidate["synthesis_run"]["low_yield_warning"] = True
    if low_cov:
        candidate["synthesis_run"]["low_atom_coverage_warning"] = True

    if zero_mitigation:
        candidate.setdefault("mitigation_emphasis", "absent")
        candidate.setdefault("named_actions", [])
        candidate.setdefault("headline_targets", [])
        candidate.setdefault(
            "coverage_notes",
            "No mitigation or transversal atoms found in the selected set for this document.",
        )

    if atom_count_input < 10:
        existing_notes = candidate.get("coverage_notes", "")
        thin_note = f"Thin atom set: only {atom_count_input} atoms extracted from this document."
        candidate["coverage_notes"] = (thin_note + " " + existing_notes).strip()

    write_json(summary_path, candidate)
    write_json(run_path, run_payload)
    n_signals = len(candidate.get("policy_signals") or [])
    LOGGER.info(
        "%s synthesized: %d atoms selected, %d anchors, %d policy_signals",
        source_document_id,
        atom_count_selected,
        len(candidate.get("evidence_anchors", [])),
        n_signals,
    )
    return "synthesized", run_payload


def command_synthesize(args: argparse.Namespace) -> int:
    v1_root = Path(args.root).resolve() if args.root else V1_ROOT
    atoms_dir = v1_root / "data/atoms"
    if not atoms_dir.exists():
        LOGGER.error("Missing atoms directory: %s", atoms_dir)
        return 1

    summary_schema_original, summary_schema_resolved = load_summary_schema(v1_root)
    registry_payload = load_json(v1_root / "data/registry/source_documents.json")
    registry = {row["source_document_id"]: row for row in registry_payload.get("source_documents", [])}

    provider = args.provider
    model = model_for_provider(provider, args.model)
    focus = args.focus
    max_tokens = int(args.max_output_tokens or 16000)

    # Discover source document IDs from atoms/*.jsonl
    if args.only:
        source_ids = [doc_id.strip() for doc_id in args.only.split(",")]
    else:
        source_ids = sorted(p.stem for p in atoms_dir.glob("*.jsonl"))

    if not source_ids:
        LOGGER.info("No atom files found.")
        return 0

    client = create_client(provider)
    counts: dict[str, int] = {}
    for source_document_id in source_ids:
        try:
            status, _run = synthesize_document(
                source_document_id=source_document_id,
                v1_root=v1_root,
                provider=provider,
                model=model,
                focus=focus,
                max_output_tokens=max_tokens,
                max_transient_retries=int(args.max_transient_retries),
                force=bool(args.force),
                client=client,
                summary_schema_original=summary_schema_original,
                summary_schema_resolved=summary_schema_resolved,
                registry=registry,
            )
        except ModelConfigurationError as exc:
            LOGGER.error("%s -> %s", source_document_id, exc)
            counts["registry_configuration_error"] = counts.get("registry_configuration_error", 0) + 1
            continue
        LOGGER.info("%s -> %s", source_document_id, status)
        counts[status] = counts.get(status, 0) + 1

    LOGGER.info("Done: %s", counts)
    return 0


def command_status(args: argparse.Namespace) -> int:
    v1_root = Path(args.root).resolve() if args.root else V1_ROOT
    summaries_dir = v1_root / "data/summaries"
    atoms_dir = v1_root / "data/atoms"

    print("| source_document_id | family | atoms_input | atoms_selected | mit_emphasis | headline_targets | named_actions |")
    print("|---|---|---:|---:|---|---:|---:|")

    if not summaries_dir.exists():
        return 0

    run_files = sorted(summaries_dir.glob("*.run.json"))
    for run_file in run_files:
        run_data = load_json(run_file)
        doc_id = run_data.get("source_document_id", run_file.stem.replace(".run", ""))
        family = FAMILY_RUBRIC.get(
            str(run_data.get("rubric_path", "")).split("/")[-1].replace(".md", ""), "?"
        )
        # Read summary if it exists
        summary_path = summaries_dir / f"{doc_id}.json"
        mit_emphasis = "?"
        n_targets = "?"
        n_actions = "?"
        if summary_path.exists():
            summary = load_json(summary_path)
            mit_emphasis = summary.get("mitigation_emphasis", "?")
            n_targets = str(len(summary.get("headline_targets") or []))
            n_actions = str(len(summary.get("named_actions") or []))
        print(
            f"| {doc_id} "
            f"| {run_data.get('rubric_path', '?').split('/')[-1].replace('.md', '')} "
            f"| {run_data.get('atom_count_input', '?')} "
            f"| {run_data.get('atom_count_selected', '?')} "
            f"| {mit_emphasis} "
            f"| {n_targets} "
            f"| {n_actions} |"
        )
    return 0


def command_verify(args: argparse.Namespace) -> int:
    """Re-check every existing summary's evidence_anchors against the current atoms JSONL."""
    v1_root = Path(args.root).resolve() if args.root else V1_ROOT
    summaries_dir = v1_root / "data/summaries"
    atoms_dir = v1_root / "data/atoms"

    if not summaries_dir.exists():
        LOGGER.info("No summaries directory to verify.")
        return 0

    failures: list[str] = []
    summary_files = sorted(summaries_dir.glob("*.json"))
    for summary_path in summary_files:
        if summary_path.name.endswith(".run.json"):
            continue
        doc_id = summary_path.stem
        atoms_path = atoms_dir / f"{doc_id}.jsonl"
        if not atoms_path.exists():
            failures.append(f"{doc_id}: atoms file missing (drift — cannot verify)")
            continue
        current_atom_ids = {
            str(json.loads(line)["atom_id"])
            for line in atoms_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        summary = load_json(summary_path)
        for anchor in summary.get("evidence_anchors", []):
            aid = anchor.get("atom_id", "")
            if aid not in current_atom_ids:
                failures.append(f"{doc_id}: anchor atom_id {aid!r} not found in current atoms (renamed or deleted)")

    if failures:
        print("Verify failed:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("Verify passed.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Stage-3 synthesis: atoms → policy_summary JSON.")
    parser.add_argument("--root", type=str, default=None, help="Override v1 root directory.")
    parser.add_argument("--verbose", action="store_true", help="Enable DEBUG logging.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    synth = subparsers.add_parser("synthesize", help="Synthesize policy_summary from atoms.")
    synth.add_argument("--only", type=str, default=None, help="Comma-separated source_document_ids.")
    synth.add_argument("--provider", choices=["gemini", "openai"], default="openai")
    synth.add_argument("--model", type=str, default=None)
    synth.add_argument("--focus", choices=["mitigation", "adaptation", "all"], default="mitigation")
    synth.add_argument("--force", action="store_true", help="Re-synthesize even if summary exists.")
    synth.add_argument("--max-output-tokens", type=int, default=None)
    synth.add_argument("--max-transient-retries", type=int, default=5)

    subparsers.add_parser("status", help="Print synthesis status table.")
    subparsers.add_parser("verify", help="Re-check evidence_anchors against current atoms.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    try:
        if args.command == "synthesize":
            return command_synthesize(args)
        if args.command == "status":
            return command_status(args)
        if args.command == "verify":
            return command_verify(args)
        parser.error(f"Unknown command: {args.command}")
    except ModelConfigurationError as exc:
        LOGGER.error("%s", exc)
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
