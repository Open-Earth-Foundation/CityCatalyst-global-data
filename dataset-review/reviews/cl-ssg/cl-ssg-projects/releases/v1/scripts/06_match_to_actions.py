"""
Match Chilean SNI/BIP projects to climate-action library entries.

Faceted approach:
1. GPC taxonomy filter — projects' (sector, subsector) maps to a set of GPC
   subsectors via data/inputs/gpc_mapping_v1.csv. Only actions in matching
   GPC subsectors (or matching GPC sector when subsector misses) are surfaced.
2. Climate-relevance routing — projects with these climate_relevance values
   are routed to sentinel labels rather than competing for matches:
     not_climate            -> skip_not_climate
     adaptation             -> library_gap_adaptation
     (primary_outcome=transport_continuity, regardless of relevance)
                            -> library_gap_transport_continuity
3. Facet overlap — for the remaining candidates, compute set overlap of
   {primary_outcome, secondary_outcome}, {primary_intervention,
   secondary_intervention}, and delivery {primary_channel, secondary_channel}
   (falls back to legacy ``primary_scope`` / ``secondary_scope`` if present).
   Assign a label:
     strong              outcome overlap AND intervention overlap > 0
     compatible_context  outcome overlap only (right goal, different lever)
     goal_aligned        outcome match against an outcome-action
                          (action_role=outcome from actions.json)
     wrong_scope         intervention overlap only (wrong goal)
     unrelated           no overlap
4. TF-IDF tiebreaker — bilingual cosine (Spanish + English on both sides)
   orders candidates within the same label tier. Action Spanish text comes
   from actions.json's description_i18n.es via the rebuild step.

Inputs
------
data/derived/projects_profiled.csv
data/derived/actions_profiled.csv    (rebuilt from actions.json via
                                      scripts/rebuild_actions_profiled.py)
data/inputs/gpc_mapping_v1.csv
data/derived/ficha_idi_table_translated.csv   (narrative for TF-IDF input)

Output
------
data/derived/project_action_matches.csv — one row per (project, candidate)
pair for matched projects (rank 1..N), plus a single sentinel row (rank=0)
per project for sentinel-routed projects (adaptation / transport_continuity /
not_climate / unmatched_taxonomy).

Usage
-----
    python scripts/06_match_to_actions.py
    python scripts/06_match_to_actions.py --top-n 3
"""

from __future__ import annotations

import argparse
import ast
import csv
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
INPUTS = DATA / "inputs"
DERIVED = DATA / "derived"

PROJECTS_CSV   = DERIVED / "projects_profiled.csv"
ACTIONS_CSV    = DERIVED / "actions_profiled.csv"
GPC_CSV        = INPUTS / "gpc_mapping_v1.csv"
TRANSLATED_CSV = DERIVED / "ficha_idi_table_translated.csv"
OUT_CSV        = DERIVED / "project_action_matches.csv"

DEFAULT_TOP_N = 5


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_csv(p: Path) -> list[dict]:
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def values_set(row: dict, primary_col: str, secondary_col: str) -> set[str]:
    s = set()
    for c in (primary_col, secondary_col):
        v = (row.get(c) or "").strip()
        if v:
            s.add(v)
    return s


def channel_values_set(row: dict) -> set[str]:
    """Delivery-channel facet (where the intervention lands), not IPCC emissions scope."""
    ch = values_set(row, "primary_channel", "secondary_channel")
    if ch:
        return ch
    return values_set(row, "primary_scope", "secondary_scope")


def parse_set_literal(s: str) -> set[str]:
    try:
        v = ast.literal_eval(s) if s.strip() else set()
        return set(v) if isinstance(v, (set, list, tuple)) else set()
    except Exception:
        return set()


def load_gpc_lookup() -> dict[tuple[str, str], dict]:
    rows = load_csv(GPC_CSV)
    lookup = {}
    for g in rows:
        sectors = parse_set_literal(g.get("gpc_sector_array", ""))
        subsectors = parse_set_literal(g.get("gpc_subsector_array", ""))
        lookup[(g["sector"], g["subsector"])] = {
            "gpc_sectors": sectors,
            "gpc_subsectors": subsectors,
            "is_cross_sector": g.get("is_cross_sector", "False") == "True",
        }
    return lookup


# Defensive remap: handles legacy 7-value intervention names if any rows in
# projects_profiled.csv predate the canonical-vocab migration. Idempotent for
# data already in canonical 5-value form.
_LEGACY_INTERVENTION_REMAP = {
    "infrastructure_build":    "infrastructure",
    "infrastructure_retrofit": "infrastructure",
    "tech_deployment":         "infrastructure",
    "program_capacity":        "program",
    "policy_regulation":       "regulatory",
    "planning_assessment":     "planning",
    "financial_incentive":     "financial",
}


def remap_intervention(value: str) -> str:
    v = (value or "").strip()
    return _LEGACY_INTERVENTION_REMAP.get(v, v)


def load_actions() -> list[dict]:
    rows = load_csv(ACTIONS_CSV)
    for r in rows:
        r["_outcomes"] = values_set(r, "primary_outcome", "secondary_outcome")
        r["_interventions"] = values_set(r, "primary_intervention", "secondary_intervention")
        r["_channels"] = channel_values_set(r)
        r["_action_role"] = (r.get("action_role") or "").strip()
        sn = (r.get("subsector_number") or "").strip()
        r["_gpc_sector"] = sn.split(".")[0] if sn else ""
        r["_gpc_subsector"] = sn
    return rows


def load_projects() -> list[dict]:
    rows = load_csv(PROJECTS_CSV)
    for r in rows:
        pi = remap_intervention(r.get("primary_intervention"))
        si = remap_intervention(r.get("secondary_intervention"))
        if si and si == pi:
            si = ""
        r["primary_intervention"] = pi
        r["secondary_intervention"] = si
        r["_outcomes"] = values_set(r, "primary_outcome", "secondary_outcome")
        r["_interventions"] = values_set(r, "primary_intervention", "secondary_intervention")
        r["_channels"] = channel_values_set(r)
    return rows


# ---------------------------------------------------------------------------
# Translated narrative join (for TF-IDF input)
# ---------------------------------------------------------------------------

_NARRATIVE_FIELDS_FOR_SCORE = [
    "justification_es", "description_es", "purpose_es", "components_es",
    "conclusions_es", "purpose_indicators_es",
]


def _narrative_score(r: dict) -> int:
    return sum(1 for f in _NARRATIVE_FIELDS_FOR_SCORE if (r.get(f) or "").strip())


def _parse_int(s: str) -> int:
    try:
        return int(s)
    except (TypeError, ValueError):
        return 0


def load_translated_lookup() -> dict[str, dict]:
    """codigo_bip -> best etapa row. Non-STUB, max narrative, latest budget_year."""
    if not TRANSLATED_CSV.exists():
        return {}
    by_bip: dict[str, list[dict]] = defaultdict(list)
    for r in load_csv(TRANSLATED_CSV):
        code = (r.get("bip_code") or "").strip()
        if code:
            by_bip[code].append(r)
    chosen = {}
    for code, cands in by_bip.items():
        ranked = sorted(cands, key=lambda r: (
            r.get("template_variant") != "STUB",
            _narrative_score(r),
            _parse_int(r.get("budget_year", "")),
        ), reverse=True)
        chosen[code] = ranked[0]
    return chosen


# ---------------------------------------------------------------------------
# Text builders + TF-IDF
# ---------------------------------------------------------------------------

def _strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if not unicodedata.combining(c))


def normalise(s: str) -> str:
    s = _strip_accents(s or "").lower()
    s = re.sub(r"[^\w\s]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def project_text(p: dict, translated: dict[str, dict]) -> str:
    t = translated.get((p.get("codigo_bip") or "").strip(), {})
    parts = [
        p.get("nombre", ""),
        p.get("descriptor", ""),
        p.get("climate_classification_es", ""),
    ]
    for en, es in [
        ("justification_en", "justification_es"),
        ("description_en", "description_es"),
        ("purpose_en", "purpose_es"),
        ("components_en", "components_es"),
        ("conclusions_en", "conclusions_es"),
    ]:
        text = (t.get(en) or "").strip() or (t.get(es) or "").strip()
        if text:
            parts.append(text)
    return normalise(" ".join(parts))


def action_text(a: dict) -> str:
    """Bilingual action text — English description + Spanish translation from
    actions.json — so cosine bridges Spanish project narrative with English
    action descriptions."""
    return normalise(
        f"{a.get('action_name','')} "
        f"{a.get('description','')} "
        f"{a.get('outcome_summary','')} "
        f"{a.get('description_es','')}"
    )


def build_tfidf_similarity(projects: list[dict], actions: list[dict],
                            translated: dict[str, dict]):
    """Return (proj_idx_by_bip, action_idx_by_id, sim_matrix)."""
    proj_texts = [project_text(p, translated) for p in projects]
    action_texts_ = [action_text(a) for a in actions]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_df=0.95)
    vectorizer.fit(proj_texts + action_texts_)
    proj_vecs = vectorizer.transform(proj_texts)
    action_vecs = vectorizer.transform(action_texts_)
    sim = cosine_similarity(proj_vecs, action_vecs)
    proj_idx = {(p.get("codigo_bip") or "").strip(): i for i, p in enumerate(projects)}
    action_idx = {a["action_id"]: i for i, a in enumerate(actions)}
    return proj_idx, action_idx, sim


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------

def label_for(outcome_overlap: int, intervention_overlap: int,
              action_role: str, channel_mismatch: bool) -> str:
    # Outcome-actions describe a goal, not a specific lever — they have no
    # intervention_type from actions.json. Match them on outcome only.
    if action_role == "outcome":
        return "goal_aligned" if outcome_overlap else "unrelated"
    # Channel mismatch downgrades strong to compatible_context. Only fires when
    # BOTH sides have populated delivery channels that don't overlap. Missing
    # channel on either side is treated as "unknown" and doesn't downgrade.
    if outcome_overlap and intervention_overlap and not channel_mismatch:
        return "strong"
    if outcome_overlap and intervention_overlap and channel_mismatch:
        return "compatible_context"
    if outcome_overlap:
        return "compatible_context"
    if intervention_overlap:
        return "wrong_scope"
    return "unrelated"


LABEL_RANK = {
    "strong": 5,
    "compatible_context": 4,
    "goal_aligned": 3,
    "wrong_scope": 2,
    "unrelated": 1,
}


def match_project(project: dict, actions: list[dict],
                  gpc_lookup: dict[tuple, dict],
                  proj_idx: dict[str, int],
                  action_idx: dict[str, int],
                  sim) -> list[dict]:
    """Ranked candidate list with overlap details + label. Ranking key:
    label tier → total facet overlap → TF-IDF cosine."""
    key = (project.get("sector", ""), project.get("subsector", ""))
    gpc = gpc_lookup.get(key, {})
    gpc_subsectors = gpc.get("gpc_subsectors", set())
    gpc_sectors = gpc.get("gpc_sectors", set())

    pi = proj_idx.get((project.get("codigo_bip") or "").strip())

    proj_channels = project.get("_channels", set())

    candidates = []
    for a in actions:
        sub_hit = a["_gpc_subsector"] in gpc_subsectors
        sec_hit = a["_gpc_sector"] in gpc_sectors
        if not (sub_hit or sec_hit):
            continue
        o_ov = len(project["_outcomes"] & a["_outcomes"])
        i_ov = len(project["_interventions"] & a["_interventions"])
        # Channel mismatch only fires when both sides have populated channels AND
        # there's zero overlap. Empty channel on either side -> no penalty.
        act_channels = a.get("_channels", set())
        channel_shared = sorted(proj_channels & act_channels)
        channel_mismatch = bool(proj_channels) and bool(act_channels) and not channel_shared
        lbl = label_for(o_ov, i_ov, a["_action_role"], channel_mismatch)
        ai = action_idx.get(a["action_id"])
        tfidf = float(sim[pi, ai]) if (pi is not None and ai is not None) else 0.0
        candidates.append({
            "action_id":         a["action_id"],
            "action_name":       a["action_name"],
            "action_role":       a["_action_role"],
            "action_subsector":  a["_gpc_subsector"],
            "outcome_overlap":   o_ov,
            "intervention_overlap": i_ov,
            "channel_overlap":   len(channel_shared),
            "outcome_shared":    sorted(project["_outcomes"] & a["_outcomes"]),
            "intervention_shared": sorted(project["_interventions"] & a["_interventions"]),
            "channel_shared":    channel_shared,
            "channel_mismatch":  channel_mismatch,
            "tfidf_score":       round(tfidf, 4),
            "subsector_hit":     sub_hit,
            "sector_hit":        sec_hit,
            "label":             lbl,
        })
    # Within tier, prefer more facet overlap (incl. channel), then TF-IDF.
    candidates.sort(key=lambda c: (
        LABEL_RANK[c["label"]],
        c["outcome_overlap"] + c["intervention_overlap"] + c["channel_overlap"],
        c["channel_overlap"],
        c["tfidf_score"],
    ), reverse=True)
    return candidates


def sentinel_row(p: dict, label: str, cr: str) -> dict:
    return {
        "codigo_bip":          p["codigo_bip"],
        "nombre":              p.get("nombre", ""),
        "climate_relevance":   cr,
        "rank":                0,
        "action_id":           "",
        "action_name":         "",
        "action_role":         "",
        "label":               label,
        "outcome_overlap":     0,
        "intervention_overlap": 0,
        "channel_overlap":     0,
        "tfidf_score":         0.0,
        "outcome_shared":      "",
        "intervention_shared": "",
        "channel_shared":      "",
        "project_outcomes":    " | ".join(sorted(p["_outcomes"])),
        "project_interventions": " | ".join(sorted(p["_interventions"])),
        "project_channels":    " | ".join(sorted(p.get("_channels", set()))),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top-n", type=int, default=DEFAULT_TOP_N,
                    help=f"Candidate rows per matched project (default: {DEFAULT_TOP_N}).")
    ap.add_argument("--out", type=Path, default=OUT_CSV,
                    help=f"Output CSV path (default: {OUT_CSV}).")
    args = ap.parse_args()

    print("loading...")
    gpc = load_gpc_lookup()
    actions = load_actions()
    projects = load_projects()
    translated = load_translated_lookup()
    print(f"  {len(gpc)} GPC mappings, {len(actions)} actions, "
          f"{len(projects)} projects, {len(translated)} translated narratives")

    print("building TF-IDF similarity matrix...")
    proj_idx, action_idx, sim = build_tfidf_similarity(projects, actions, translated)
    print(f"  shape={sim.shape}  nonzero={(sim>0).sum()}\n")

    per_project_route = Counter()
    per_project_best_label = Counter()
    candidate_label_totals = Counter()
    library_gap_by_sector = Counter()
    project_with_strong = 0

    out_rows = []
    for p in projects:
        cr = (p.get("climate_relevance") or "").strip()

        if cr == "not_climate":
            out_rows.append(sentinel_row(p, "skip_not_climate", cr))
            per_project_route["skip_not_climate"] += 1
            per_project_best_label["skip_not_climate"] += 1
            continue

        if cr == "adaptation":
            out_rows.append(sentinel_row(p, "library_gap_adaptation", cr))
            per_project_route["library_gap_adaptation"] += 1
            per_project_best_label["library_gap_adaptation"] += 1
            library_gap_by_sector[p.get("sector", "")] += 1
            continue

        if (p.get("primary_outcome") or "").strip() == "transport_continuity":
            out_rows.append(sentinel_row(p, "library_gap_transport_continuity", cr))
            per_project_route["library_gap_transport_continuity"] += 1
            per_project_best_label["library_gap_transport_continuity"] += 1
            continue

        cands = match_project(p, actions, gpc, proj_idx, action_idx, sim)
        if not cands:
            out_rows.append(sentinel_row(p, "unmatched_taxonomy", cr))
            per_project_route["unmatched_taxonomy"] += 1
            per_project_best_label["unmatched_taxonomy"] += 1
            continue

        per_project_route["matched"] += 1
        best = cands[0]["label"]
        per_project_best_label[best] += 1
        if best == "strong":
            project_with_strong += 1
        for c in cands[:args.top_n]:
            candidate_label_totals[c["label"]] += 1
            out_rows.append({
                "codigo_bip":          p["codigo_bip"],
                "nombre":              p.get("nombre", ""),
                "climate_relevance":   cr,
                "rank":                cands.index(c) + 1,
                "action_id":           c["action_id"],
                "action_name":         c["action_name"],
                "action_role":         c["action_role"],
                "label":               c["label"],
                "outcome_overlap":     c["outcome_overlap"],
                "intervention_overlap": c["intervention_overlap"],
                "channel_overlap":     c["channel_overlap"],
                "tfidf_score":         c["tfidf_score"],
                "outcome_shared":      " | ".join(c["outcome_shared"]),
                "intervention_shared": " | ".join(c["intervention_shared"]),
                "channel_shared":      " | ".join(c["channel_shared"]),
                "project_outcomes":    " | ".join(sorted(p["_outcomes"])),
                "project_interventions": " | ".join(sorted(p["_interventions"])),
                "project_channels":    " | ".join(sorted(p.get("_channels", set()))),
            })

    fields = ["codigo_bip", "nombre", "climate_relevance", "rank",
              "action_id", "action_name", "action_role", "label",
              "outcome_overlap", "intervention_overlap", "channel_overlap",
              "tfidf_score",
              "outcome_shared", "intervention_shared", "channel_shared",
              "project_outcomes", "project_interventions", "project_channels"]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)
    print(f"wrote {args.out}  rows={len(out_rows)}\n")

    n = len(projects)
    print("=" * 70 + "\nPROJECT ROUTING\n" + "=" * 70)
    for k, v in per_project_route.most_common():
        print(f"  {k}: {v}  ({100 * v / n:.1f}%)")

    print("\n" + "=" * 70 + "\nBEST-CANDIDATE LABEL PER PROJECT\n" + "=" * 70)
    for k, v in per_project_best_label.most_common():
        print(f"  {k}: {v}  ({100 * v / n:.1f}%)")

    print(f"\nProjects with at least one STRONG match:  {project_with_strong}  "
          f"({100 * project_with_strong / n:.1f}%)")

    print("\n" + "=" * 70 + f"\nALL CANDIDATE LABELS (top {args.top_n} per matched project)\n" + "=" * 70)
    for k, v in candidate_label_totals.most_common():
        print(f"  {k}: {v}")

    print("\n" + "=" * 70 + "\nADAPTATION LIBRARY-GAPS BY SECTOR\n" + "=" * 70)
    for k, v in library_gap_by_sector.most_common(10):
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
