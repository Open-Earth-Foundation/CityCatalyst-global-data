#!/usr/bin/env python3
"""Stage 2: match one action against the atoms of one source document.

Given:
  - releases/v1/data/atoms/<source_document_id>.jsonl  (from stage 1)
  - one action from releases/v1/data/registry/actions.json

Produces:
  - releases/v1/data/policy_action_signals/<source_document_id>/<action_id>.json
    Each finding references an atom_id; evidence_text + page are denormalised
    from the atom for downstream convenience.

The atoms block is identical across all actions on the same document, so
prefix caching kicks in when many pairs share a doc. The batch runner
orders pairs by document for this reason.

Usage:
  # Dry run (no API call)
  python v1_match_atoms_to_action.py --action ipcc_0053 --doc chl_parcc_arica --dry-run

  # Real run
  python v1_match_atoms_to_action.py --action ipcc_0053 --doc chl_parcc_arica

  # Re-validate an existing finding file (deterministic)
  python v1_match_atoms_to_action.py --validate releases/v1/data/policy_action_signals/chl_parcc_arica/ipcc_0053.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import v1_common as ef  # noqa: N812 — keeping `ef` alias for now to minimise diff
import v1_extract_atoms as atoms_mod

FINDINGS_SCHEMA_VERSION = "2.1.0"
MATCHER_VERSION = "0.1.0"
RUBRIC_VERSION = "0.1.0"
DEFAULT_MODEL = "gpt-4.1-mini"
ATOM_EVIDENCE_TRUNCATE = 600   # chars of evidence_text per atom in the prompt

V1 = Path(__file__).resolve().parents[1]
DEFAULT_ATOMS_DIR = V1 / "data" / "atoms"
DEFAULT_OUTPUT_DIR = V1 / "data" / "policy_action_signals"
MATCH_SYSTEM_PATH = V1 / "prompts" / "match_system.md"
MATCH_USER_PATH = V1 / "prompts" / "match_user.md.j2"

ALLOWED_RELATIONS = {
    "commits", "targets", "funds", "monitors", "governs", "prioritizes",
    "identifies", "contextualizes", "restates", "references",
}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
ALLOWED_RELEVANCE = {"high", "medium", "low", "none"}
ALLOWED_EXPLICITNESS = {"explicit", "inferred"}

# Model-error auto-correction: when the model conflates primitive_type with
# primitive_relation and writes e.g. relation="action", remap to the default
# relation associated with that primitive_type.
TYPE_TO_DEFAULT_RELATION: dict[str, str] = {
    "action":          "commits",
    "target":          "targets",
    "funding":         "funds",
    "monitoring":      "monitors",
    "governance":      "governs",
    "sector_priority": "prioritizes",
    "sector":          "contextualizes",
    "risk":            "identifies",
    "context":         "contextualizes",
}


def repair_primitive_relation(raw: str | None, atom: dict) -> tuple[str | None, bool]:
    """Return (relation, was_repaired). If the model used a primitive_type
    value where a primitive_relation belongs, swap in the default relation
    for that type (using the atom's primitive_type as the fallback)."""
    if raw in ALLOWED_RELATIONS:
        return raw, False
    # If the model wrote a primitive_type-shaped string, use the corresponding default
    if raw in TYPE_TO_DEFAULT_RELATION:
        return TYPE_TO_DEFAULT_RELATION[raw], True
    # Else fall back to whatever the atom's primitive_type suggests
    fallback = TYPE_TO_DEFAULT_RELATION.get(atom.get("primitive_type", ""))
    if fallback:
        return fallback, True
    return raw, False


# ----------------------------------------------------------------------------
# Atoms loading + compact block formatting
# ----------------------------------------------------------------------------

def truncate_text(text: str, n: int = ATOM_EVIDENCE_TRUNCATE) -> str:
    if len(text) <= n:
        return text
    return text[:n].rstrip() + "..."


def atom_to_compact(atom: dict) -> dict:
    """Compact representation sent to the matcher. Keeps the fields the
    matcher needs to judge relevance and drops verbose extraction metadata.
    """
    out = {
        "atom_id": atom["atom_id"],
        "primitive_type": atom["primitive_type"],
        "page": atom.get("page"),
        "section": atom.get("section", ""),
        "atom_summary": atom.get("atom_summary", ""),
        "sector_tags": atom.get("sector_tags", []),
        "evidence_text": truncate_text(atom.get("evidence_text", "")),
    }
    for k in ("measure_type", "explicitness", "primitive_relation_hint", "applicability_scope"):
        v = atom.get(k)
        if v:
            out[k] = v
    return out


def atoms_block(atoms: list[dict]) -> str:
    """One compact-atom JSON object per line — JSONL inside the prompt."""
    return "\n".join(json.dumps(atom_to_compact(a), ensure_ascii=False) for a in atoms)


# ----------------------------------------------------------------------------
# Prompt assembly
# ----------------------------------------------------------------------------

def load_match_system() -> str:
    return MATCH_SYSTEM_PATH.read_text(encoding="utf-8")


def load_match_user() -> str:
    return MATCH_USER_PATH.read_text(encoding="utf-8")


def build_match_user_prompt(
    action: "ef.Action",
    doc_meta: dict,
    atoms: list[dict],
) -> str:
    return ef.render_template(
        load_match_user(),
        {
            "source_document_id": doc_meta.get("source_document_id", ""),
            "source_name": doc_meta.get("source_name", ""),
            "source_level": doc_meta.get("source_level", ""),
            "region_code": doc_meta.get("region_code", ""),
            "document_type": doc_meta.get("document_type", ""),
            "atoms_block": atoms_block(atoms),
            "action_id": action.action_id,
            "action_name": action.action_name,
            "action_gpc_reference": action.action_gpc_reference,
            "action_description": action.description,
            "action_intervention_summary": action.intervention_summary,
            "action_outcome_summary": action.outcome_summary,
        },
    )


# ----------------------------------------------------------------------------
# LLM call
# ----------------------------------------------------------------------------

def call_match(system_prompt: str, user_prompt: str, model: str) -> tuple[dict, dict]:
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
    return payload, usage_dict


# ----------------------------------------------------------------------------
# Validation + denormalisation
# ----------------------------------------------------------------------------

def validate_and_denormalise(
    payload: dict,
    atoms_by_id: dict[str, dict],
) -> tuple[list[dict], list[str], list[str]]:
    """Return (findings_with_evidence, errors, warnings).

    findings_with_evidence: each finding gets evidence_text + page + section
                            copied in from the referenced atom for convenience.
    errors: list of error tags.
    warnings: list of warning tags.
    """
    findings = payload.get("findings") or []
    errors: list[str] = []
    warnings: list[str] = []
    out: list[dict] = []
    seen_atom_ids: set[str] = set()

    if payload.get("relevance") not in ALLOWED_RELEVANCE:
        errors.append(f"invalid_relevance:{payload.get('relevance')}")

    for i, f in enumerate(findings):
        prefix = f"findings[{i}]"
        atom_id = f.get("atom_id")
        if not atom_id:
            errors.append(f"{prefix}:missing_atom_id")
            continue
        if atom_id in seen_atom_ids:
            warnings.append(f"{prefix}:duplicate_atom_id:{atom_id}")
            continue
        atom = atoms_by_id.get(atom_id)
        if atom is None:
            errors.append(f"{prefix}:atom_id_not_in_index:{atom_id}")
            continue

        relation_raw = f.get("primitive_relation")
        relation, repaired = repair_primitive_relation(relation_raw, atom)
        if repaired:
            warnings.append(
                f"{prefix}:primitive_relation_repaired:{relation_raw}->{relation}"
            )
        if relation not in ALLOWED_RELATIONS:
            errors.append(f"{prefix}:invalid_primitive_relation:{relation_raw}")
        conf = f.get("signal_confidence")
        if conf not in ALLOWED_CONFIDENCE:
            errors.append(f"{prefix}:invalid_signal_confidence:{conf}")
        explicitness = f.get("explicitness")
        if explicitness and explicitness not in ALLOWED_EXPLICITNESS:
            warnings.append(f"{prefix}:invalid_explicitness:{explicitness}")
        seen_atom_ids.add(atom_id)

        out.append({
            "atom_id": atom_id,
            "primitive_type": atom["primitive_type"],
            "primitive_relation": relation,
            "signal_confidence": conf,
            "explicitness": explicitness or atom.get("explicitness", "explicit"),
            "relevance_note": (f.get("relevance_note") or "").strip(),
            "evidence_text": atom.get("evidence_text", ""),
            "page": atom.get("page"),
            "section": atom.get("section", ""),
            "sector_tags": atom.get("sector_tags", []),
            "applicability_scope": atom.get("applicability_scope", ""),
        })

    # Sanity grades
    relevance = payload.get("relevance")
    if relevance == "none" and out:
        warnings.append("relevance_none_but_findings_present")
    if relevance in {"high", "medium"} and not out:
        warnings.append(f"relevance_{relevance}_but_no_findings")

    return out, errors, warnings


# ----------------------------------------------------------------------------
# Per-pair entry point (importable by batch runner)
# ----------------------------------------------------------------------------

def match_pair(
    action: "ef.Action",
    doc_id: str,
    doc_meta: dict,
    atoms_dir: Path,
    model: str = DEFAULT_MODEL,
) -> dict:
    atoms_path = atoms_dir / f"{doc_id}.jsonl"
    if not atoms_path.exists():
        raise FileNotFoundError(f"No atoms file for {doc_id} at {atoms_path}; run stage 1 first.")
    atoms = atoms_mod.load_atoms(atoms_path)
    atoms_by_id = {a["atom_id"]: a for a in atoms}

    system_prompt = load_match_system()
    user_prompt = build_match_user_prompt(action, doc_meta, atoms)
    payload, usage = call_match(system_prompt, user_prompt, model=model)

    findings, errors, warnings = validate_and_denormalise(payload, atoms_by_id)

    out: dict = {
        "schema_version": FINDINGS_SCHEMA_VERSION,
        "action_id": action.action_id,
        "action_name": action.action_name,
        "action_gpc_reference": action.action_gpc_reference,
        "source_document_id": doc_id,
        "source_name": doc_meta.get("source_name", ""),
        "source_level": doc_meta.get("source_level", ""),
        "region_code": doc_meta.get("region_code", ""),
        "communal_code": doc_meta.get("communal_code", ""),
        "document_type": doc_meta.get("document_type", ""),
        "relevance": payload.get("relevance", "none"),
        "summary": payload.get("summary", ""),
        "absent_primitive_types": payload.get("absent_primitive_types", []),
        "caveats": payload.get("caveats", ""),
        "findings": findings,
        "search_run": {
            "model": model,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "matcher_version": MATCHER_VERSION,
            "rubric_version": RUBRIC_VERSION,
            "input_tokens": usage.get("input_tokens"),
            "cached_input_tokens": usage.get("cached_input_tokens"),
            "output_tokens": usage.get("output_tokens"),
            "duration_seconds": usage.get("duration_seconds"),
            "atoms_seen": len(atoms),
            "schema_check_passed": not errors,
            "notes": errors + [f"warning:{w}" for w in warnings],
        },
    }
    return out


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def output_path(output_dir: Path, doc_id: str, action_id: str) -> Path:
    return output_dir / doc_id / f"{action_id}.json"


def main() -> int:
    ap = argparse.ArgumentParser(description="Stage 2: match action against doc atoms")
    ap.add_argument("--action", help="action_id")
    ap.add_argument("--doc", help="source_document_id")
    ap.add_argument("--actions", type=Path, default=ef.DEFAULT_ACTIONS_JSON,
                    help="Path to actions.json (or legacy actions_profiled.csv).")
    ap.add_argument("--registry", type=Path, default=ef.DEFAULT_REGISTRY)
    ap.add_argument("--atoms-dir", type=Path, default=DEFAULT_ATOMS_DIR)
    ap.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--validate", help="Path to an existing findings JSON to validate against the atoms")
    ap.add_argument("--repair-corpus", help="Path to a directory of already-emitted findings files. Apply primitive_relation auto-correction in place. No LLM calls.")
    args = ap.parse_args()

    if args.repair_corpus:
        root = Path(args.repair_corpus)
        repaired_files = 0
        repaired_findings = 0
        for p in sorted(root.rglob("*.json")):
            if p.name == "failed.jsonl":
                continue
            payload = json.loads(p.read_text(encoding="utf-8"))
            findings = payload.get("findings") or []
            file_repaired = 0
            for f in findings:
                rel_raw = f.get("primitive_relation")
                # mini-atom for repair_primitive_relation
                atom = {"primitive_type": f.get("primitive_type", "")}
                rel, was_repaired = repair_primitive_relation(rel_raw, atom)
                if was_repaired:
                    f["primitive_relation"] = rel
                    file_repaired += 1
            if file_repaired:
                run = payload.setdefault("search_run", {})
                run["primitive_relation_repaired_in_place"] = (
                    run.get("primitive_relation_repaired_in_place", 0) + file_repaired
                )
                # Re-evaluate schema_check_passed: count remaining invalid relations
                still_invalid = sum(
                    1 for f in findings if f.get("primitive_relation") not in ALLOWED_RELATIONS
                )
                run["schema_check_passed"] = still_invalid == 0
                p.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
                repaired_files += 1
                repaired_findings += file_repaired
        print(f"repaired {repaired_findings} findings across {repaired_files} files under {root}")
        return 0

    if args.validate:
        path = Path(args.validate)
        payload = json.loads(path.read_text(encoding="utf-8"))
        doc_id = payload.get("source_document_id") or path.parent.name
        atoms_path = args.atoms_dir / f"{doc_id}.jsonl"
        atoms = atoms_mod.load_atoms(atoms_path)
        atoms_by_id = {a["atom_id"]: a for a in atoms}
        bad_ids = [f["atom_id"] for f in payload.get("findings") or [] if f.get("atom_id") not in atoms_by_id]
        print(f"findings: {len(payload.get('findings') or [])}; atoms missing: {len(bad_ids)}")
        for b in bad_ids[:10]:
            print(f"  - missing atom_id: {b}")
        return 0 if not bad_ids else 2

    if not args.action or not args.doc:
        ap.print_help()
        return 1

    actions = ef.load_actions(args.actions)
    if args.action not in actions:
        print(f"unknown action_id {args.action!r}", file=sys.stderr)
        return 1
    registry = ef.load_registry(args.registry)
    if args.doc not in registry:
        print(f"unknown source_document_id {args.doc!r}", file=sys.stderr)
        return 1

    action = actions[args.action]
    doc_meta = dict(registry[args.doc])
    doc_meta["source_document_id"] = args.doc
    atoms_path = args.atoms_dir / f"{args.doc}.jsonl"
    if not atoms_path.exists():
        print(f"no atoms file for {args.doc} at {atoms_path}", file=sys.stderr)
        print("run stage 1 first: python v2_extract_atoms.py --doc " + args.doc, file=sys.stderr)
        return 1
    atoms = atoms_mod.load_atoms(atoms_path)

    if args.dry_run:
        system_prompt = load_match_system()
        user_prompt = build_match_user_prompt(action, doc_meta, atoms)
        print(f"atoms_seen     : {len(atoms)}")
        print(f"system chars   : {len(system_prompt):,}")
        print(f"user chars     : {len(user_prompt):,}  (~{len(user_prompt)//4:,} estimated tokens)")
        # Show structural offsets to confirm cache-friendly ordering
        for label in ("DOCUMENT METADATA", "ATOMS", "ACTION", "TASK"):
            print(f"  {label:18s} offset={user_prompt.find(label):9d}")
        return 0

    payload = match_pair(
        action=action,
        doc_id=args.doc,
        doc_meta=doc_meta,
        atoms_dir=args.atoms_dir,
        model=args.model,
    )

    out = output_path(args.output_dir, args.doc, args.action)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {out}", file=sys.stderr)
    return 0 if payload["search_run"]["schema_check_passed"] else 2


if __name__ == "__main__":
    sys.exit(main())
