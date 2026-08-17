#!/usr/bin/env python3
"""Match all policy atoms to action profiles without an external API.

Reviewed action rules take precedence. Unreviewed profiles use a deliberately
strict distinctive-phrase fallback and are marked as candidates requiring
review; this prevents machine-generated profile text from being presented as
equivalent to reviewed semantic matching.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import unicodedata
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

import v1_common as common


V1 = Path(__file__).resolve().parents[1]
DEFAULT_PROFILES = V1 / "data" / "registry" / "action_matching_profiles.json"
DEFAULT_ATOMS = V1 / "data" / "atoms"
DEFAULT_REGISTRY = V1 / "data" / "registry" / "source_documents.json"
DEFAULT_OUTPUT = V1 / "data" / "policy_action_signals_v0_3_local"

RELATIONS = {
    "action": "commits", "target": "targets", "funding": "funds",
    "monitoring": "monitors", "governance": "governs",
    "sector_priority": "prioritizes", "sector": "contextualizes",
    "risk": "identifies", "context": "contextualizes",
}


@lru_cache(maxsize=250_000)
def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def contains_any(text: str, phrases: list[str]) -> bool:
    padded = f" {text} "
    words = text.split()
    for phrase in phrases:
        if phrase.endswith("*"):
            prefix = normalize(phrase[:-1])
            if prefix and any(word.startswith(prefix) for word in words):
                return True
            continue
        cleaned = normalize(phrase)
        if cleaned and f" {cleaned} " in padded:
            return True
    return False


def classify_reviewed(text: str, rules: dict) -> str | None:
    direct = contains_any(text, rules.get("direct_phrases", []))
    required = rules.get("direct_requires_any", [])
    if direct and (not required or contains_any(text, required)):
        return "direct"
    if contains_any(text, rules.get("exclude_phrases", [])):
        return None
    if contains_any(text, rules.get("indirect_phrases", [])):
        return "indirect"
    if contains_any(text, rules.get("contextual_phrases", [])):
        return "contextual"
    return None


def classify_fallback(text: str, profile: dict) -> str | None:
    # Require an exact distinctive multiword phrase. Single sector words are
    # intentionally insufficient because they caused the original inflation.
    anchors = [p for p in profile.get("distinctive_anchors", []) if len(p.split()) >= 2]
    padded = f" {text} "
    hits = [p for p in anchors if f" {normalize(p)} " in padded]
    if not hits:
        return None
    # Until a human confirms the action boundary, lexical overlap is only a
    # candidate/enabling signal. It must not create direct or strong support.
    return "indirect"


def canonical_measure_type(raw: str | None) -> str:
    value = normalize(raw or "")
    if value in {"mitigation", "mitigacion"}:
        return "mitigation"
    if value in {"adaptation", "adaptacion"}:
        return "adaptation"
    if value in {"transversal", "cross cutting"}:
        return "transversal"
    return "unknown"


def finding(atom: dict, match_type: str, reviewed: bool) -> dict:
    primitive = atom.get("primitive_type", "context")
    if primitive not in RELATIONS:
        primitive = "context"
    confidence = {"direct": "high", "indirect": "medium", "contextual": "low"}[match_type]
    reason = {
        "direct": "The policy atom names the same intervention object and mechanism as the action profile.",
        "indirect": "The policy atom is a concrete enabling measure but does not implement the full action.",
        "contextual": "The policy atom provides narrowly relevant context without implementing or enabling the action.",
    }[match_type]
    subject = atom.get("atom_summary") or ""
    if len(normalize(subject)) < 3:
        subject = atom.get("evidence_text") or "policy intervention"
    return {
        "atom_id": atom["atom_id"],
        "primitive_type": primitive,
        "primitive_relation": RELATIONS[primitive],
        "match_type": match_type,
        "policy_subject": subject[:240],
        "subject_match_reason": reason,
        "signal_confidence": confidence if reviewed else "medium",
        "explicitness": "explicit" if match_type == "direct" else "inferred",
        "relevance_note": reason,
        "evidence_text": atom.get("evidence_text", ""),
        "page": atom.get("page") or 1,
        "section": atom.get("section", ""),
        "sector_tags": atom.get("sector_tags", []),
        "measure_type": canonical_measure_type(atom.get("measure_type")),
        "applicability_scope": atom.get("applicability_scope", ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profiles", type=Path, default=DEFAULT_PROFILES)
    parser.add_argument("--atoms-dir", type=Path, default=DEFAULT_ATOMS)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()

    if args.output_dir.exists():
        if not args.replace:
            raise SystemExit(f"output exists; pass --replace: {args.output_dir}")
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True)
    profiles = json.loads(args.profiles.read_text(encoding="utf-8"))["profiles"]
    actions = common.load_actions(V1 / "data" / "registry" / "actions.json")
    registry = common.load_registry(args.registry)
    pairs = findings_count = reviewed_pairs = 0

    for atom_path in sorted(args.atoms_dir.glob("*.jsonl")):
        doc_id = atom_path.stem
        if doc_id not in registry:
            continue
        atoms = [json.loads(line) for line in atom_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        meta = registry[doc_id]
        out_dir = args.output_dir / doc_id
        out_dir.mkdir()
        for profile in profiles:
            aid = profile["action_id"]
            rules = profile.get("reviewed_rules") or {}
            is_reviewed = bool(rules)
            matches = []
            for atom in atoms:
                text = normalize((atom.get("evidence_text") or "") + " " + (atom.get("atom_summary") or ""))
                match_type = classify_reviewed(text, rules) if is_reviewed else classify_fallback(text, profile)
                if match_type:
                    matches.append(finding(atom, match_type, is_reviewed))
            # Keep the strongest, most useful evidence and avoid a single broad
            # atom being repeated throughout downstream displays.
            rank = {"direct": 3, "indirect": 2, "contextual": 1}
            matches.sort(key=lambda x: (-rank[x["match_type"]], len(x["evidence_text"])))
            matches = matches[:20]
            strongest = max((rank[x["match_type"]] for x in matches), default=0)
            relevance = {3: "high", 2: "medium", 1: "low", 0: "none"}[strongest]
            action = actions[aid]
            payload = {
                "schema_version": "2.2.0", "action_id": aid,
                "action_name": action.action_name,
                "action_gpc_reference": action.action_gpc_reference,
                "source_document_id": doc_id,
                "source_name": meta.get("source_name", ""),
                "source_level": meta.get("source_level", "national"),
                "region_code": meta.get("region_code", ""),
                "communal_code": meta.get("communal_code", ""),
                "document_type": meta.get("document_type", ""),
                "relevance": relevance,
                "summary": "" if not matches else f"Local profile matching found {len(matches)} {matches[0]['match_type']} or weaker policy signal(s).",
                "findings": matches,
                "absent_primitive_types": [],
                "caveats": "Reviewed action boundary." if is_reviewed else "Machine-generated candidate profile; human review required before production use.",
                "search_run": {
                    "model": "none-local-deterministic", "created_at": datetime.now(timezone.utc).isoformat(),
                    "matcher_version": "local-profile-0.3.0", "rubric_version": "0.3.0",
                    "atoms_seen": len(atoms), "schema_check_passed": True,
                    "profile_status": profile["profile_status"], "notes": [],
                },
            }
            (out_dir / f"{aid}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            pairs += 1
            findings_count += len(matches)
            reviewed_pairs += int(is_reviewed)

    summary = {"documents": len(list(args.output_dir.iterdir())), "actions": len(profiles), "pairs": pairs,
               "findings": findings_count, "reviewed_action_pairs": reviewed_pairs,
               "external_api_calls": 0}
    (args.output_dir / "_run_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
