#!/usr/bin/env python3
"""
Per-city deterministic aggregator: policy–action alignment cards → locality-weighted rankings.

Reads matcher outputs and registry/local catalog; no LLM calls.

Usage (from ``releases/v1`` parent, or with ``--root``):

.. code-block:: bash

   python3 v1/scripts/v1_aggregate_per_city.py aggregate
   python3 v1/scripts/v1_aggregate_per_city.py status
   python3 v1/scripts/v1_aggregate_per_city.py inspect 08101
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence

V1_ROOT = Path(__file__).resolve().parent.parent


def resolve_paths(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    """Return (v1_root, alignment_dir, output_dir)."""
    root = Path(args.root).resolve() if getattr(args, "root", None) else V1_ROOT
    ad = getattr(args, "alignment_dir", None) or root / "data/policy_action_alignment"
    od = getattr(args, "output_dir", None) or root / "data/city_action_alignment"
    return root, Path(ad), Path(od)


LOG = logging.getLogger(__name__)

WEIGHT_BY_LEVEL: dict[str, float] = {
    "national": 1.0,
    "intercommunal": 1.5,
    "regional": 2.0,
    "municipal": 3.0,
    "other": 0.5,
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

LOCAL_LEVELS = frozenset({"regional", "intercommunal", "municipal"})


def norm_region(code: str | None) -> str:
    s = (code or "").strip()
    if not s:
        return ""
    if s.isdigit():
        return s.zfill(2)
    return s


def norm_commune(code: str | None) -> str:
    s = (code or "").strip()
    if not s:
        return ""
    if s.isdigit():
        return s.zfill(5)
    return s


def parse_communal_codes(raw: str | None) -> set[str]:
    if not raw:
        return set()
    parts = str(raw).replace(";", ",").split(",")
    return {norm_commune(p) for p in parts if norm_commune(p)}


def weight_for_level(source_level: str | None) -> float:
    sl = (source_level or "").strip().lower()
    return WEIGHT_BY_LEVEL.get(sl, WEIGHT_BY_LEVEL["other"])


def registry_row_included(doc: Mapping[str, Any]) -> bool:
    if str(doc.get("document_status", "")).lower() == "placeholder":
        return False
    if str(doc.get("access_type", "")).lower() == "placeholder":
        return False
    return True


def policy_applies_to_commune(
    doc: Mapping[str, Any],
    commune_code: str,
    region_code: str,
) -> bool:
    """True if this registry policy is territorially applicable to the commune."""
    if not registry_row_included(doc):
        return False
    sl = (doc.get("source_level") or "").strip().lower()
    cc = norm_commune(commune_code)
    rc = norm_region(region_code)
    doc_rc = norm_region(str(doc.get("region_code", "") or ""))
    codes = parse_communal_codes(str(doc.get("communal_code", "") or ""))

    if sl == "national":
        return True
    if sl == "regional":
        return bool(doc_rc) and doc_rc == rc
    if sl == "municipal":
        return cc in codes if codes else False
    if sl == "intercommunal":
        if cc and cc in codes:
            return True
        if doc_rc and doc_rc == rc:
            return True
        return False
    # unknown / other / paccc-style: include broadly (weighted down)
    return True


def top_relation_from_supporting(relations: Sequence[str]) -> str:
    if not relations:
        return "supports"
    counts = Counter(relations)
    best = max(counts.values())
    candidates = [r for r, c in counts.items() if c == best]
    for pref in RELATION_TIE_ORDER:
        if pref in candidates:
            return pref
    return candidates[0]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_registry(path: Path) -> dict[str, dict[str, Any]]:
    data = load_json(path)
    rows = data.get("source_documents") or []
    return {str(r["source_document_id"]): dict(r) for r in rows if isinstance(r, dict) and r.get("source_document_id")}


def load_alignment_cards(alignment_dir: Path) -> list[dict[str, Any]]:
    index_path = alignment_dir / "_index.csv"
    if not index_path.is_file():
        return []
    out: list[dict[str, Any]] = []
    with open(index_path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            pid = (row.get("source_document_id") or "").strip()
            aid = (row.get("action_id") or "").strip()
            if not pid or not aid:
                continue
            jpath = alignment_dir / pid / f"{aid}.json"
            if not jpath.is_file():
                LOG.warning("Missing score card: %s", jpath)
                continue
            card = load_json(jpath)
            if not isinstance(card, dict):
                continue
            card["_path"] = str(jpath)
            out.append(card)
    return out


def load_actions_index(path: Path) -> dict[str, dict[str, str]]:
    if not path.is_file():
        return {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    return {(r.get("action_id") or "").strip(): dict(r) for r in rows if (r.get("action_id") or "").strip()}


def load_communes(path: Path) -> list[dict[str, str]]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def applicable_policies_for_commune(
    registry_by_id: dict[str, dict[str, Any]],
    commune_code: str,
    region_code: str,
) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for pid, doc in sorted(registry_by_id.items(), key=lambda x: x[0]):
        if policy_applies_to_commune(doc, commune_code, region_code):
            items.append(
                {
                    "source_document_id": pid,
                    "source_level": str(doc.get("source_level", "") or ""),
                    "source_name": str(doc.get("source_name", "") or ""),
                }
            )
    return items


def build_supporting_entries(
    cards: Sequence[Mapping[str, Any]],
    applicable_ids: set[str],
    _registry_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for card in cards:
        pid = str(card.get("source_document_id", "") or "")
        if pid not in applicable_ids:
            continue
        sl = str(card.get("source_level", "") or "").strip().lower()
        w = weight_for_level(sl)
        ps = float(card.get("policy_score", 0.0) or 0.0)
        wc = round(ps * w, 6)
        rows.append(
            {
                "source_document_id": pid,
                "source_level": str(card.get("source_level", "") or ""),
                "policy_score": ps,
                "match_count": int(card.get("match_count", 0) or 0),
                "top_relation_type": str(card.get("top_relation_type", "") or "supports"),
                "match_quality": str(card.get("match_quality", "") or "weak"),
                "weight": w,
                "weighted_contribution": wc,
            }
        )
    rows.sort(key=lambda r: float(r["weighted_contribution"]), reverse=True)
    return rows


def compute_city_score(supporting: Sequence[Mapping[str, Any]]) -> float:
    if not supporting:
        return 0.0
    wsum = sum(float(s["weight"]) for s in supporting)
    if wsum <= 0:
        return 0.0
    weighted = sum(float(s["policy_score"]) * float(s["weight"]) for s in supporting)
    return round(weighted / wsum, 6)


def has_local_evidence(supporting: Sequence[Mapping[str, Any]]) -> bool:
    for s in supporting:
        if (s.get("source_level") or "").strip().lower() in LOCAL_LEVELS:
            return True
    return False


def render_explanation(
    commune_name: str,
    supporting: Sequence[Mapping[str, Any]],
    applicable_count: int,
    has_local: bool,
    registry_by_id: dict[str, dict[str, Any]],
) -> str:
    n = len(supporting)
    if n == 0:
        return ""
    top = max(supporting, key=lambda s: float(s.get("policy_score", 0.0)))
    pid = str(top.get("source_document_id", ""))
    pname = str(registry_by_id.get(pid, {}).get("source_name", "") or top.get("policy_name", "") or pid)
    lvl = str(top.get("source_level", ""))
    sc = float(top.get("policy_score", 0.0))
    base = (
        f"Action backed by {n} of {applicable_count} applicable policies for {commune_name}. "
        f"Strongest: {pname} ({lvl}, score {sc:.2f})."
    )
    if has_local:
        locals_ = [
            s
            for s in supporting
            if (s.get("source_level") or "").strip().lower() in LOCAL_LEVELS
        ]
        pick = max(locals_, key=lambda s: float(s.get("weight", 0)) * float(s.get("policy_score", 0)))
        lp = str(pick.get("source_document_id", ""))
        lname = str(registry_by_id.get(lp, {}).get("source_name", "") or pick.get("policy_name", "") or lp)
        llvl = str(pick.get("source_level", ""))
        base += f" Local evidence from {lname} ({llvl})."
    return base


def aggregate_one_city(
    commune: Mapping[str, str],
    all_cards: Sequence[Mapping[str, Any]],
    registry_by_id: dict[str, dict[str, Any]],
    actions_by_id: dict[str, dict[str, str]],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, str]]]:
    """
    Returns (city_summary, per_action_payloads, index_rows).
    per_action_payloads only includes actions with >=1 supporting policy.
    """
    cc = norm_commune(commune.get("commune_code_2018", ""))
    rc = norm_region(commune.get("region_code", ""))
    cname = str(commune.get("commune_name", "") or "")
    rname = str(commune.get("region_name", "") or "")

    applicable = applicable_policies_for_commune(registry_by_id, cc, rc)
    applicable_ids = {p["source_document_id"] for p in applicable}

    by_action: dict[str, list[dict[str, Any]]] = {}
    for card in all_cards:
        aid = str(card.get("action_id", "") or "")
        if not aid:
            continue
        pid = str(card.get("source_document_id", "") or "")
        if pid not in applicable_ids:
            continue
        by_action.setdefault(aid, []).append(card)

    scored: list[tuple[str, float, list[dict[str, Any]], list[dict[str, Any]]]] = []
    for aid, cards in by_action.items():
        sup = build_supporting_entries(cards, applicable_ids, registry_by_id)
        if not sup:
            continue
        cs = compute_city_score(sup)
        scored.append((aid, cs, sup, cards))

    scored.sort(key=lambda t: t[1], reverse=True)

    action_total = len(actions_by_id) if actions_by_id else len({str(c.get("action_id")) for c in all_cards})
    with_matches = len(scored)
    top_actions = []
    for aid, cs, _, _ in scored[:10]:
        row = actions_by_id.get(aid, {})
        top_actions.append(
            {
                "action_id": aid,
                "action_name": str(row.get("action_name", "") or ""),
                "city_score": cs,
            }
        )

    summary = {
        "commune_code": cc,
        "commune_name": cname,
        "region_code": rc,
        "region_name": rname,
        "applicable_policies": [{"source_document_id": p["source_document_id"], "source_level": p["source_level"]} for p in applicable],
        "action_count_with_matches": with_matches,
        "action_count_total": action_total,
        "top_actions": top_actions,
    }

    payloads: list[dict[str, Any]] = []
    index_rows: list[dict[str, str]] = []
    for aid, cs, sup, _cards in scored:
        row = actions_by_id.get(aid, {})
        hl = has_local_evidence(sup)
        top_rel = top_relation_from_supporting(
            [str(s.get("top_relation_type", "supports")) for s in sup]
        )
        expl = render_explanation(cname, sup, len(applicable), hl, registry_by_id)
        payload = {
            "schema_version": "1.0.0",
            "commune_code": cc,
            "commune_name": cname,
            "region_code": rc,
            "region_name": rname,
            "action_id": aid,
            "action_name": str(row.get("action_name", "") or ""),
            "applicable_policies": summary["applicable_policies"],
            "supporting_policies": sup,
            "city_score": cs,
            "supporting_policy_count": len(sup),
            "applicable_policy_count": len(applicable),
            "has_local_evidence": hl,
            "top_relation_type": top_rel,
            "explanation": expl,
        }
        payloads.append(payload)
        index_rows.append(
            {
                "commune_code": cc,
                "commune_name": cname,
                "region_code": rc,
                "action_id": aid,
                "city_score": f"{cs:.6f}",
                "applicable_policy_count": str(len(applicable)),
                "supporting_policy_count": str(len(sup)),
                "top_relation_type": top_rel,
                "has_local_evidence": "1" if hl else "0",
            }
        )

    return summary, payloads, index_rows


def cmd_aggregate(args: argparse.Namespace) -> int:
    v1_root, alignment_dir, out_dir = resolve_paths(args)
    if not alignment_dir.is_dir():
        LOG.error("Alignment dir missing: %s", alignment_dir)
        return 1
    registry_path = v1_root / "data" / "registry" / "source_documents.json"
    local_path = v1_root / "data" / "registry" / "local_codes.csv"
    actions_path = v1_root / "data" / "derived" / "actions_profiled.csv"

    registry_by_id = load_registry(registry_path)
    all_cards = load_alignment_cards(alignment_dir)
    actions_by_id = load_actions_index(actions_path)
    communes = load_communes(local_path)

    if args.force and out_dir.is_dir():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    top_n = int(args.top_n) if args.top_n is not None and int(args.top_n) > 0 else None
    min_score = float(args.min_city_score)

    filter_cc = norm_commune(args.only_city) if args.only_city else None
    filter_rc = norm_region(args.only_region) if args.only_region else None

    all_index: list[dict[str, str]] = []
    cities_done = 0

    for commune in communes:
        cc = norm_commune(commune.get("commune_code_2018", ""))
        rc = norm_region(commune.get("region_code", ""))
        if filter_cc and cc != filter_cc:
            continue
        if filter_rc and rc != filter_rc:
            continue

        summary, payloads, index_rows = aggregate_one_city(commune, all_cards, registry_by_id, actions_by_id)
        cities_done += 1

        sub = out_dir / cc
        sub.mkdir(parents=True, exist_ok=True)
        (sub / "_city_summary.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        written = 0
        for payload in payloads:
            if float(payload["city_score"]) < min_score:
                continue
            if top_n is not None and written >= top_n:
                break
            aid = payload["action_id"]
            (sub / f"{aid}.json").write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            matching = next((r for r in index_rows if r["action_id"] == aid), None)
            if matching:
                all_index.append(matching)
            written += 1

    idx_path = out_dir / "_index.csv"
    with open(idx_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "commune_code",
                "commune_name",
                "region_code",
                "action_id",
                "city_score",
                "applicable_policy_count",
                "supporting_policy_count",
                "top_relation_type",
                "has_local_evidence",
            ],
        )
        w.writeheader()
        w.writerows(sorted(all_index, key=lambda r: (r["commune_code"], -float(r["city_score"]))))

    LOG.info("Processed %s cities; wrote index %s", cities_done, idx_path)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    _root, _align, out_dir = resolve_paths(args)
    if not out_dir.is_dir():
        print("No output directory; run aggregate first.")
        return 0

    summaries = sorted(out_dir.glob("*/_city_summary.json"))
    print(f"Total cities with output: {len(summaries)}")
    if not summaries:
        return 0

    app_counts: list[int] = []
    sup_ratios: list[float] = []
    top3_counter: Counter[str] = Counter()
    zero_match_cities: list[str] = []

    for sp in summaries:
        d = load_json(sp)
        app_counts.append(len(d.get("applicable_policies") or []))
        wm = int(d.get("action_count_with_matches", 0) or 0)
        tot = int(d.get("action_count_total", 0) or 1)
        sup_ratios.append(wm / tot)
        for ta in (d.get("top_actions") or [])[:3]:
            aid = str(ta.get("action_id", ""))
            if aid:
                top3_counter[aid] += 1
        if wm == 0:
            zero_match_cities.append(str(d.get("commune_code", "")))

    print(f"Average applicable policies per city: {sum(app_counts) / len(app_counts):.1f}")
    print(f"Average action match rate (with_matches / total): {sum(sup_ratios) / len(sup_ratios):.3f}")
    print("Top-3 action frequency (how many cities list each action in top 3):")
    for aid, c in top3_counter.most_common(15):
        print(f"  {aid}: {c}")
    print(f"Cities with zero matched actions: {len(zero_match_cities)}")
    if zero_match_cities[:10]:
        print("  sample:", ", ".join(zero_match_cities[:10]))
    return 0


def cmd_inspect(args: argparse.Namespace) -> int:
    _root, _align, out_dir = resolve_paths(args)
    code = norm_commune(args.commune_code)
    sp = out_dir / code / "_city_summary.json"
    if not sp.is_file():
        print(f"No output for commune {code}. Run: aggregate --only-city {code}")
        return 1
    d = load_json(sp)
    print(f"=== {d.get('commune_name')} ({code}) region {d.get('region_code')} ===")
    print(f"Applicable policies ({len(d.get('applicable_policies') or [])}):")
    for p in (d.get("applicable_policies") or [])[:25]:
        print(f"  - {p.get('source_document_id')} [{p.get('source_level')}]")
    if len(d.get("applicable_policies") or []) > 25:
        print("  ...")
    print("\nTop 10 actions by city_score:")
    for i, ta in enumerate((d.get("top_actions") or [])[:10], 1):
        aid = ta.get("action_id")
        jpath = out_dir / code / f"{aid}.json"
        expl = ""
        if jpath.is_file():
            aj = load_json(jpath)
            expl = str(aj.get("explanation", ""))[:200]
        print(f"  {i}. {aid}  score={float(ta.get('city_score', 0)):.3f}  {ta.get('action_name', '')[:60]}")
        if expl:
            print(f"      {expl}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Per-city policy–action ranking from alignment cards.")
    p.add_argument("--root", type=str, default=None, help="Override v1 root (default: parent of scripts/)")
    p.add_argument(
        "--alignment-dir",
        type=Path,
        default=None,
        help="policy_action_alignment directory (default: <root>/data/policy_action_alignment)",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="city_action_alignment output directory (default: <root>/data/city_action_alignment)",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    agg = sub.add_parser("aggregate", help="Build per-city outputs")
    agg.add_argument("--only-city", type=str, default=None, help="Single commune_code_2018")
    agg.add_argument("--only-region", type=str, default=None, help="All communes in region_code")
    agg.add_argument("--top-n", type=int, default=None, help="Max action JSONs per city (default: all)")
    agg.add_argument("--min-city-score", type=float, default=0.0, help="Minimum city_score to write action file")
    agg.add_argument("--force", action="store_true", help="Delete output-dir before writing")
    agg.set_defaults(func=cmd_aggregate)

    st = sub.add_parser("status", help="Summary stats over aggregate output")
    st.set_defaults(func=cmd_status)

    ins = sub.add_parser("inspect", help="Print one city's summary + top actions")
    ins.add_argument("commune_code", type=str, help="Commune code e.g. 08101")
    ins.set_defaults(func=cmd_inspect)

    return p


def main(argv: Sequence[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
