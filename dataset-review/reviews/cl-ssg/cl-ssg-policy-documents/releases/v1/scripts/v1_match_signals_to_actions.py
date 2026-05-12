#!/usr/bin/env python3
"""
Deterministic matcher: profiled policy signals × profiled actions.

Reads (defaults under this release ``v1/``):

- ``data/derived/actions_profiled.csv``
- ``data/derived/signals_profiled.csv``

Writes:

- ``data/policy_action_alignment/_index.csv``
- ``data/policy_action_alignment/<source_document_id>/<action_id>.json``

Subcommands: ``match``, ``status``, ``verify``.

Usage (from ``v1/``):

.. code-block:: bash

   python3 scripts/v1_match_signals_to_actions.py match
   python3 scripts/v1_match_signals_to_actions.py match --force
   python3 scripts/v1_match_signals_to_actions.py status
   python3 scripts/v1_match_signals_to_actions.py verify

No LLM calls; CSV rows are the sole contract.

Pair-level gate: a signal–action pair is kept only if there is channel
primary/family overlap, or both ``outcome_primary_match`` and
``intervention_primary_match`` (outcome-only alignments are rejected).
Default ``--min-score`` is ``0.45``. ``policy_score`` aggregates with
``max(scores) + 0.04 * min(n-1, 5)`` (capped at 1.0), not a saturating
product.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import shutil
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

# Release root (parent of ``scripts/``).
V1_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ACTIONS_CSV = V1_ROOT / "data" / "derived" / "actions_profiled.csv"
DEFAULT_SIGNALS_CSV = V1_ROOT / "data" / "derived" / "signals_profiled.csv"
DEFAULT_OUTPUT_DIR = V1_ROOT / "data" / "policy_action_alignment"

LOG = logging.getLogger(__name__)

OUTCOME_FAMILIES: dict[str, tuple[str, ...]] = {
    "emissions": (
        "emissions_efficiency",
        "emissions_fuel_switch",
        "emissions_modal_shift",
        "emissions_demand_reduction",
        "emissions_waste_diversion",
    ),
    "sequestration": ("carbon_sequestration",),
    "transport_continuity": ("transport_continuity",),
    "resilience": ("resilience_water", "resilience_flood", "resilience_other"),
    "enabling": ("enabling",),
}

CHANNEL_FAMILIES: dict[str, tuple[str, ...]] = {
    "transport": (
        "bike_infrastructure",
        "bike_sharing",
        "public_bus",
        "public_rail",
        "freight",
        "urban_form_tod",
        "congestion_pricing",
        "transit_general",
    ),
    "waste": (
        "landfill",
        "mbt_eco_park",
        "recycling_collection",
        "organic_composting",
        "construction_demolition_waste",
        "waste_regulation",
    ),
    "energy_supply": (
        "solar_pv",
        "solar_thermal",
        "wind",
        "biogas",
        "hydro",
        "renewable_general",
    ),
    "energy_demand": (
        "street_lighting",
        "building_residential",
        "building_institutional_public",
        "building_commercial",
        "building_industrial",
        "industrial_process",
        "water_heating",
    ),
    "land": (
        "forest",
        "peatland",
        "wetland_coastal",
        "urban_green",
        "agricultural_soil",
        "livestock",
        "fire_mgmt",
        "biochar",
    ),
    "cross_cutting": (
        "financial_incentive_scheme",
        "regulation_standard",
        "capacity_building",
        "mrv_planning",
        "not_applicable",
    ),
}

RELATION_TIE_ORDER: tuple[str, ...] = (
    "supports",
    "targets",
    "funds",
    "prioritizes",
    "monitors",
    "governs",
    "contextualizes",
    "references",
)

CONFIDENCE_WEIGHT: dict[tuple[str, str], float] = {
    ("high", "high"): 1.0,
    ("high", "medium"): 0.85,
    ("medium", "high"): 0.85,
    ("medium", "medium"): 0.75,
    ("high", "low"): 0.5,
    ("low", "high"): 0.5,
    ("medium", "low"): 0.4,
    ("low", "medium"): 0.4,
    ("low", "low"): 0.3,
}

ALLOWED_CLIMATE_RELEVANCE = frozenset({"mitigation", "mixed"})


def _norm_confidence(raw: str | None) -> str:
    s = (raw or "").strip().lower()
    if s in ("high", "medium", "low"):
        return s
    return "medium"


def _non_empty(s: str | None) -> bool:
    return bool((s or "").strip())


def _channel_na(ch: str | None) -> bool:
    """True if channel should not participate in channel matching."""
    v = (ch or "").strip().lower()
    return not v or v == "not_applicable"


def build_outcome_family_index() -> dict[str, str]:
    m: dict[str, str] = {}
    for fam, vals in OUTCOME_FAMILIES.items():
        for v in vals:
            m[v] = fam
    return m


def build_channel_family_index() -> dict[str, str]:
    m: dict[str, str] = {}
    for fam, vals in CHANNEL_FAMILIES.items():
        for v in vals:
            m[v] = fam
    return m


OUTCOME_TO_FAMILY = build_outcome_family_index()
CHANNEL_TO_FAMILY = build_channel_family_index()


@dataclass(frozen=True)
class MatchDimensions:
    outcome_primary_match: bool
    outcome_secondary_match: bool
    outcome_family_match: bool
    intervention_primary_match: bool
    channel_primary_match: bool
    channel_family_match: bool


def compute_match_dimensions(
    action: Mapping[str, str],
    signal: Mapping[str, str],
) -> MatchDimensions:
    ao = (action.get("primary_outcome") or "").strip()
    aos = (action.get("secondary_outcome") or "").strip()
    so = (signal.get("primary_outcome") or "").strip()
    sos = (signal.get("secondary_outcome") or "").strip()

    outcome_primary_match = (
        _non_empty(ao) and _non_empty(so) and ao == so
    )
    outcome_secondary_match = (
        (_non_empty(ao) and _non_empty(sos) and ao == sos)
        or (_non_empty(aos) and _non_empty(so) and aos == so)
    )
    outcome_family_match = False
    if _non_empty(ao) and _non_empty(so):
        fa, fs = OUTCOME_TO_FAMILY.get(ao), OUTCOME_TO_FAMILY.get(so)
        if fa is not None and fs is not None and fa == fs:
            outcome_family_match = True

    pi_a = (action.get("primary_intervention") or "").strip()
    pi_s = (signal.get("primary_intervention") or "").strip()
    intervention_primary_match = (
        _non_empty(pi_a) and _non_empty(pi_s) and pi_a == pi_s
    )

    ch_a = (action.get("primary_channel") or "").strip()
    ch_s = (signal.get("primary_channel") or "").strip()
    channel_primary_match = False
    channel_family_match = False
    if not _channel_na(ch_a) and not _channel_na(ch_s):
        channel_primary_match = ch_a == ch_s
        if not channel_primary_match:
            fa, fs = CHANNEL_TO_FAMILY.get(ch_a), CHANNEL_TO_FAMILY.get(ch_s)
            if fa is not None and fs is not None and fa == fs:
                channel_family_match = True

    return MatchDimensions(
        outcome_primary_match=outcome_primary_match,
        outcome_secondary_match=outcome_secondary_match,
        outcome_family_match=outcome_family_match,
        intervention_primary_match=intervention_primary_match,
        channel_primary_match=channel_primary_match,
        channel_family_match=channel_family_match,
    )


def base_match_score(dim: MatchDimensions) -> float:
    """Facet-weighted score before signal-type and confidence modifiers."""
    score = 0.0
    if dim.outcome_primary_match:
        score += 0.40
    elif dim.outcome_family_match:
        score += 0.15
    if dim.outcome_secondary_match:
        score += 0.10
    if dim.intervention_primary_match:
        score += 0.15
    if dim.channel_primary_match:
        score += 0.30
    elif dim.channel_family_match:
        score += 0.10
    if dim.intervention_primary_match and dim.channel_primary_match:
        score += 0.05
    return min(score, 1.0)


def passes_meaningful_match_bridge(dim: MatchDimensions) -> bool:
    """
    True if the pair has enough delivery/procedure overlap to count.

    Requires at least one of: channel primary match, channel family match,
    or (intervention primary AND outcome primary).
    """
    return (
        dim.channel_primary_match
        or dim.channel_family_match
        or (dim.intervention_primary_match and dim.outcome_primary_match)
    )


def signal_type_modifier(signal_type: str) -> float:
    st = (signal_type or "").strip().lower()
    if st in {"risk", "context", "actor", "timeline"}:
        return 0.4
    if st in {"monitoring", "governance"}:
        return 0.7
    return 1.0


def confidence_weight(action_conf: str, signal_conf: str) -> float:
    return CONFIDENCE_WEIGHT.get(
        (_norm_confidence(action_conf), _norm_confidence(signal_conf)),
        0.5,
    )


def outcome_match_for_relation(dim: MatchDimensions) -> bool:
    return (
        dim.outcome_primary_match
        or dim.outcome_secondary_match
        or dim.outcome_family_match
    )


def derive_relation_type(signal_type: str, dim: MatchDimensions) -> str:
    st = (signal_type or "").strip().lower() or "other"
    outcome_yes = outcome_match_for_relation(dim)

    if st == "funding":
        return "funds"
    if st == "monitoring":
        return "monitors"
    if st == "governance":
        return "governs"
    if st == "action":
        return "supports"
    if st == "target":
        return "targets" if outcome_yes else "supports"
    if st in ("sector", "sector_priority"):
        return "prioritizes" if outcome_yes else "supports"
    if st in ("risk", "context"):
        return "contextualizes" if outcome_yes else "supports"
    if st in ("actor", "timeline"):
        return "references" if outcome_yes else "supports"
    return "supports"


def dimension_contributions(dim: MatchDimensions) -> tuple[float, float, float]:
    """(outcome_dim, intervention_dim, channel_dim) pre-modifier weights."""
    if dim.outcome_primary_match:
        outcome_base = 0.40
    elif dim.outcome_family_match:
        outcome_base = 0.15
    else:
        outcome_base = 0.0
    outcome_dim = outcome_base + (0.10 if dim.outcome_secondary_match else 0.0)
    intervention_dim = 0.15 if dim.intervention_primary_match else 0.0
    if dim.channel_primary_match:
        channel_dim = 0.30
    elif dim.channel_family_match:
        channel_dim = 0.10
    else:
        channel_dim = 0.0
    return outcome_dim, intervention_dim, channel_dim


def _r6(x: float) -> float:
    return round(float(x), 6)


def max_plus_bonus_policy_score(match_scores: Sequence[float]) -> float:
    """
    Aggregate policy score: strongest single match plus a small bonus for
    additional supporting signals (capped at +0.20 for five extras).
    """
    if not match_scores:
        return 0.0
    vals = [max(0.0, min(1.0, float(x))) for x in match_scores]
    top = max(vals)
    n = len(vals)
    bonus = 0.04 * min(n - 1, 5)
    return _r6(min(1.0, top + bonus))


def top_relation_type(relations: Sequence[str]) -> str:
    if not relations:
        return "supports"
    counts = Counter(relations)
    best_c = max(counts.values())
    candidates = [r for r, c in counts.items() if c == best_c]
    for pref in RELATION_TIE_ORDER:
        if pref in candidates:
            return pref
    return candidates[0]


def build_explanation(
    matched: Sequence[Mapping[str, Any]],
    source_level: str,
    match_count: int,
) -> str:
    if not matched:
        return ""
    top = max(matched, key=lambda m: float(m.get("match_score", 0.0)))
    label = str(top.get("signal_label", ""))[:80]
    st = top.get("signal_type", "")
    rel = top.get("relation_type", "")
    sc = float(top.get("match_score", 0.0))
    return (
        f"Top-matching signal: {label} (signal_type={st}, "
        f"relation={rel}, score={sc:.2f}). {match_count} total signals "
        f"matched at {source_level} level."
    )


def filter_signals(rows: Iterable[Mapping[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for r in rows:
        cr = (r.get("climate_relevance") or "").strip().lower()
        if cr not in ALLOWED_CLIMATE_RELEVANCE:
            continue
        if not _non_empty(r.get("primary_outcome")):
            continue
        out.append(dict(r))
    return out


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def parse_atom_ids(cell: str | None) -> list[str]:
    if not cell:
        return []
    return [p.strip() for p in str(cell).split(";") if p.strip()]


def score_signal_action_pair(
    action: Mapping[str, str],
    signal: Mapping[str, str],
    min_score: float,
) -> dict[str, Any] | None:
    dim = compute_match_dimensions(action, signal)
    raw = base_match_score(dim)
    raw *= signal_type_modifier(str(signal.get("signal_type", "")))
    raw *= confidence_weight(
        str(action.get("confidence", "")),
        str(signal.get("confidence", "")),
    )
    final = min(max(raw, 0.0), 1.0)
    if not passes_meaningful_match_bridge(dim):
        return None
    if final < min_score:
        return None
    rel = derive_relation_type(str(signal.get("signal_type", "")), dim)
    md = {
        "outcome_primary_match": dim.outcome_primary_match,
        "outcome_secondary_match": dim.outcome_secondary_match,
        "outcome_family_match": dim.outcome_family_match,
        "intervention_primary_match": dim.intervention_primary_match,
        "channel_primary_match": dim.channel_primary_match,
        "channel_family_match": dim.channel_family_match,
    }
    return {
        "match_dimensions": md,
        "final_match_score": final,
        "relation_type": rel,
        "dimension_tuple": dimension_contributions(dim),
    }


def derive_match_quality(
    policy_score: float,
    dimension_scores: Mapping[str, float],
) -> str:
    """Coarse bucket for downstream filtering."""
    out = float(dimension_scores.get("outcome", 0.0))
    ch = float(dimension_scores.get("channel", 0.0))
    ps = float(policy_score)
    if ps >= 0.75 and ch >= 0.20 and out >= 0.30:
        return "strong"
    if ps >= 0.55:
        return "moderate"
    return "weak"


def aggregate_pair_card(
    action: Mapping[str, str],
    policy_meta: Mapping[str, str],
    scored_matches: list[dict[str, Any]],
    computed_at: str,
) -> dict[str, Any]:
    scores = [float(m["final_match_score"]) for m in scored_matches]
    policy_score = max_plus_bonus_policy_score(scores)
    outcome_dim = _r6(max(m["dimension_tuple"][0] for m in scored_matches))
    intervention_dim = _r6(max(m["dimension_tuple"][1] for m in scored_matches))
    channel_dim = _r6(max(m["dimension_tuple"][2] for m in scored_matches))
    dim_scores: dict[str, float] = {
        "outcome": outcome_dim,
        "intervention": intervention_dim,
        "channel": channel_dim,
    }
    match_quality = derive_match_quality(float(policy_score), dim_scores)
    rels = [str(m["relation_type"]) for m in scored_matches]
    top_rel = top_relation_type(rels)
    source_level = str(policy_meta.get("source_level", "") or "")
    explanation = build_explanation(
        [
            {
                "signal_label": sm["signal_label"],
                "signal_type": sm["signal_type"],
                "relation_type": sm["relation_type"],
                "match_score": sm["match_score"],
            }
            for sm in scored_matches
        ],
        source_level,
        len(scored_matches),
    )
    matched_signals: list[dict[str, Any]] = []
    for m in scored_matches:
        matched_signals.append(
            {
                "policy_signal_id": m["policy_signal_id"],
                "signal_type": m["signal_type"],
                "signal_label": m["signal_label"],
                "supporting_atom_ids": m["supporting_atom_ids"],
                "match_dimensions": m["match_dimensions"],
                "match_score": _r6(float(m["match_score"])),
                "relation_type": m["relation_type"],
                "confidence": m["confidence"],
            }
        )
    return {
        "schema_version": "1.0.0",
        "action_id": action.get("action_id", ""),
        "action_name": action.get("action_name", ""),
        "action_gpc_reference": action.get("gpc_reference", ""),
        "source_document_id": policy_meta.get("source_document_id", ""),
        "source_name": policy_meta.get("source_name", ""),
        "source_level": policy_meta.get("source_level", ""),
        "region_code": policy_meta.get("region_code", ""),
        "communal_code": policy_meta.get("communal_code", ""),
        "document_type": policy_meta.get("document_type", ""),
        "matched_signals": matched_signals,
        "dimension_scores": dim_scores,
        "policy_score": float(policy_score),
        "match_quality": match_quality,
        "match_count": len(scored_matches),
        "top_relation_type": top_rel,
        "explanation": explanation,
        "computed_at": computed_at,
    }


def compute_alignment(
    actions: Sequence[Mapping[str, str]],
    signals: Sequence[Mapping[str, str]],
    *,
    min_score: float,
    only_action: str | None,
    only_policy: str | None,
) -> dict[tuple[str, str], dict[str, Any]]:
    """
    Returns map (source_document_id, action_id) -> score card dict.
    """
    sig_rows = filter_signals(signals)
    computed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )
    cards: dict[tuple[str, str], dict[str, Any]] = {}

    for action in actions:
        aid = (action.get("action_id") or "").strip()
        if only_action and aid != only_action.strip():
            continue
        if not _non_empty(action.get("primary_outcome")):
            LOG.warning("Skipping action %s: empty primary_outcome", aid)
            continue

        for sig in sig_rows:
            pid = (sig.get("source_document_id") or "").strip()
            if only_policy and pid != only_policy.strip():
                continue
            scored = score_signal_action_pair(action, sig, min_score)
            if scored is None:
                continue
            key = (pid, aid)
            entry = {
                "policy_signal_id": sig.get("policy_signal_id", ""),
                "signal_type": sig.get("signal_type", ""),
                "signal_label": sig.get("signal_label", ""),
                "supporting_atom_ids": parse_atom_ids(sig.get("supporting_atom_ids")),
                "match_dimensions": scored["match_dimensions"],
                "match_score": scored["final_match_score"],
                "relation_type": scored["relation_type"],
                "confidence": _norm_confidence(sig.get("confidence")),
                "final_match_score": scored["final_match_score"],
                "dimension_tuple": scored["dimension_tuple"],
            }
            if key not in cards:
                cards[key] = {"matches": [], "policy_meta": {}}
            cards[key]["matches"].append(entry)
            cards[key]["policy_meta"] = {
                "source_document_id": pid,
                "source_name": sig.get("source_name", ""),
                "source_level": sig.get("source_level", ""),
                "region_code": sig.get("region_code", ""),
                "communal_code": sig.get("communal_code", ""),
                "document_type": sig.get("document_type", ""),
            }

    result: dict[tuple[str, str], dict[str, Any]] = {}
    for key, payload in cards.items():
        matches = sorted(
            payload["matches"],
            key=lambda m: float(m["final_match_score"]),
            reverse=True,
        )
        pid, aid = key
        action_row = next(
            (a for a in actions if (a.get("action_id") or "").strip() == aid),
            {},
        )
        result[key] = aggregate_pair_card(
            action_row,
            payload["policy_meta"],
            matches,
            computed_at,
        )
    return result


def write_alignment(
    cards: Mapping[tuple[str, str], dict[str, Any]],
    output_dir: Path,
    *,
    force: bool,
) -> list[dict[str, str]]:
    if force and output_dir.is_dir():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    index_rows: list[dict[str, str]] = []
    for (pid, aid), card in sorted(cards.items()):
        sub = output_dir / pid
        sub.mkdir(parents=True, exist_ok=True)
        out_path = sub / f"{aid}.json"
        out_path.write_text(
            json.dumps(card, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        index_rows.append(
            {
                "source_document_id": pid,
                "action_id": aid,
                "policy_score": f"{float(card['policy_score']):.6f}",
                "match_count": str(card["match_count"]),
                "top_relation_type": str(card["top_relation_type"]),
                "source_level": str(card.get("source_level", "")),
                "region_code": str(card.get("region_code", "")),
                "communal_code": str(card.get("communal_code", "")),
            }
        )
    index_path = output_dir / "_index.csv"
    with open(index_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "source_document_id",
                "action_id",
                "policy_score",
                "match_count",
                "top_relation_type",
                "source_level",
                "region_code",
                "communal_code",
            ],
        )
        w.writeheader()
        w.writerows(sorted(index_rows, key=lambda r: (r["source_document_id"], r["action_id"])))
    return list(index_rows)


def cmd_match(args: argparse.Namespace) -> int:
    actions_path: Path = args.actions_csv
    signals_path: Path = args.signals_csv
    output_dir: Path = args.output_dir
    if not actions_path.is_file():
        LOG.error("Actions CSV not found: %s", actions_path)
        return 1
    if not signals_path.is_file():
        LOG.error("Signals CSV not found: %s", signals_path)
        return 1
    actions = load_csv_rows(actions_path)
    signals = load_csv_rows(signals_path)
    cards = compute_alignment(
        actions,
        signals,
        min_score=float(args.min_score),
        only_action=args.only_action,
        only_policy=args.only_policy,
    )
    write_alignment(cards, output_dir, force=bool(args.force))
    LOG.info("Wrote %s (policy, action) score cards to %s", len(cards), output_dir)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    actions_path: Path = args.actions_csv
    signals_path: Path = args.signals_csv
    if not actions_path.is_file() or not signals_path.is_file():
        LOG.error("Missing CSV input(s)")
        return 1
    actions = load_csv_rows(actions_path)
    signals = load_csv_rows(signals_path)
    cards = compute_alignment(
        actions,
        signals,
        min_score=float(args.min_score),
        only_action=None,
        only_policy=None,
    )
    policies = sorted({p for p, _ in cards})
    act_ids = sorted({a for _, a in cards})
    all_actions = sorted({(r.get("action_id") or "").strip() for r in actions if r.get("action_id")})
    matched_actions = {a for _, a in cards}
    unmatched = sorted(set(all_actions) - matched_actions)

    print("=== Actions × policies coverage (matched pairs) ===")
    header = ["action_id"] + policies
    print(",".join(header))
    for aid in all_actions[:50]:  # truncate wide matrix in console
        row = [aid] + ["1" if (p, aid) in cards else "0" for p in policies]
        print(",".join(row))
    if len(all_actions) > 50:
        print(f"... ({len(all_actions)} actions total; matrix truncated for display)")

    print("\n=== Per-policy ===")
    for p in policies:
        pairs = [(a, cards[(p, a)]) for a in act_ids if (p, a) in cards]
        if not pairs:
            continue
        best_a, best_c = max(pairs, key=lambda t: float(t[1]["policy_score"]))
        print(
            f"  {p}: actions_matched={len(pairs)} "
            f"top_action={best_a} policy_score={float(best_c['policy_score']):.3f}"
        )

    print("\n=== Per-action ===")
    for a in sorted(matched_actions)[:30]:
        pols = [p for p in policies if (p, a) in cards]
        best_p, best_c = max(
            ((p, cards[(p, a)]) for p in pols),
            key=lambda t: float(t[1]["policy_score"]),
        )
        print(
            f"  {a}: policies_matched={len(pols)} "
            f"top_policy={best_p} policy_score={float(best_c['policy_score']):.3f}"
        )
    if len(matched_actions) > 30:
        print(f"... ({len(matched_actions)} matched actions shown truncated)")

    if unmatched:
        print(f"\nActions with zero matches across all policies: {len(unmatched)}")
        print("  sample:", ", ".join(unmatched[:20]))
    return 0


def _load_json_card(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _float_close(a: float, b: float, tol: float = 1e-5) -> bool:
    return abs(a - b) <= tol


def cmd_verify(args: argparse.Namespace) -> int:
    actions_path: Path = args.actions_csv
    signals_path: Path = args.signals_csv
    output_dir: Path = args.output_dir
    if not output_dir.is_dir():
        LOG.error("Output dir missing: %s", output_dir)
        return 1
    actions = load_csv_rows(actions_path)
    signals = load_csv_rows(signals_path)
    expected = compute_alignment(
        actions,
        signals,
        min_score=float(args.min_score),
        only_action=None,
        only_policy=None,
    )
    drift = 0
    missing_files = 0
    extra_files = 0
    expected_keys = set(expected.keys())
    on_disk: set[tuple[str, str]] = set()
    for jpath in sorted(output_dir.glob("*/*.json")):
        if jpath.parent.name.startswith("_"):
            continue
        pid = jpath.parent.name
        aid = jpath.stem
        on_disk.add((pid, aid))
        key = (pid, aid)
        if key not in expected:
            LOG.warning("Extra on disk (no longer matches from CSV): %s", jpath)
            extra_files += 1
            continue
        disk = _load_json_card(jpath)
        exp = expected[key]
        if disk.get("match_count") != exp.get("match_count"):
            LOG.error("match_count drift %s %s: disk=%s expected=%s", pid, aid, disk.get("match_count"), exp.get("match_count"))
            drift += 1
        elif not _float_close(float(disk.get("policy_score", -1)), float(exp.get("policy_score", -2))):
            LOG.error("policy_score drift %s %s: disk=%s expected=%s", pid, aid, disk.get("policy_score"), exp.get("policy_score"))
            drift += 1
        elif disk.get("match_quality") != exp.get("match_quality"):
            LOG.error(
                "match_quality drift %s %s: disk=%s expected=%s",
                pid,
                aid,
                disk.get("match_quality"),
                exp.get("match_quality"),
            )
            drift += 1
        else:
            ds = disk.get("matched_signals") or []
            es = exp.get("matched_signals") or []
            if len(ds) != len(es):
                LOG.error("matched_signals len drift %s %s", pid, aid)
                drift += 1

    for key in sorted(expected_keys - on_disk):
        LOG.error("Missing JSON on disk for expected pair: %s", key)
        missing_files += 1

    print(
        f"verify: expected_pairs={len(expected)} on_disk={len(on_disk)} "
        f"drift_fields={drift} missing_json={missing_files} extra_json={extra_files}"
    )
    return 1 if drift or missing_files or extra_files else 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Match profiled signals to profiled actions.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_io(ap: argparse.ArgumentParser) -> None:
        ap.add_argument(
            "--actions-csv",
            type=Path,
            default=DEFAULT_ACTIONS_CSV,
            help="Actions profiled CSV",
        )
        ap.add_argument(
            "--signals-csv",
            type=Path,
            default=DEFAULT_SIGNALS_CSV,
            help="Signals profiled CSV",
        )
        ap.add_argument(
            "--output-dir",
            type=Path,
            default=DEFAULT_OUTPUT_DIR,
            help="Alignment output directory",
        )
        ap.add_argument(
            "--min-score",
            type=float,
            default=0.45,
            help="Minimum final match score to keep a signal on a card (default 0.45)",
        )

    pm = sub.add_parser("match", help="Compute alignment and write JSON + index")
    add_io(pm)
    pm.add_argument("--only-action", default=None, help="Limit to one action_id")
    pm.add_argument("--only-policy", default=None, help="Limit to one source_document_id")
    pm.add_argument(
        "--force",
        action="store_true",
        help="Delete output-dir entirely before writing (removes stale JSON)",
    )
    pm.set_defaults(func=cmd_match)

    ps = sub.add_parser("status", help="Print coverage summaries from CSVs")
    add_io(ps)
    ps.set_defaults(func=cmd_status)

    pv = sub.add_parser("verify", help="Compare on-disk JSONs to CSV recomputation")
    add_io(pv)
    pv.set_defaults(func=cmd_verify)

    return p


def main(argv: Sequence[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
