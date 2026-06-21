#!/usr/bin/env python3
"""Emit example API responses from the preview DB so the data shapes are visible."""
import csv, json, sqlite3
from pathlib import Path

DB = Path("/tmp/finance_preview.db")
BASE = Path("/sessions/jolly-dazzling-ritchie/mnt/CityCatalyst-global-data/"
            "dataset-review/reviews/oef/cl-city-action-fundability/releases/v1")
OUT = Path("/sessions/jolly-dazzling-ritchie/mnt/outputs/finance_preview")
OUT.mkdir(parents=True, exist_ok=True)

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

DEMO_CUT = "01101"  # Iquique (chosen in build: most actions with precedent)
prof = dict(con.execute("SELECT * FROM city_finance_profile WHERE comuna_cut=?", (DEMO_CUT,)).fetchone())
ACTOR_ID = prof["actor_id"]

scored = {(s["comuna_cut"], s["action_id"]): s
          for s in csv.DictReader(open(BASE / "data/fundability_scored.csv"))}

BUCKET_SCORE = {  # methodology B7 (display mapping; production computes from inputs)
    "self-deliverable": 1.00, "own-budget feasible": 0.85, "needs technical assistance": 0.70,
    "needs co-finance": 0.45, "needs finance + TA / pooling": 0.25}

def n(v):
    try:
        f = float(v); return int(f) if f.is_integer() else f
    except (TypeError, ValueError):
        return None

def reachable_opps(sector):
    """COMPETITIVE funds only: sector-specific first, then broad/cross-sector (capped per B2)."""
    specific, broad = [], []
    for o in con.execute("""SELECT * FROM finance_opportunity
                            WHERE funding_channel='competitive fund'
                              AND city_application IN ('direct','facilitated')"""):
        try:
            secs = json.loads(o["gpc_sectors"])
        except Exception:
            secs = []
        if sector in secs and o["specificity"] == "sector-specific":
            specific.append(o)
        elif sector in secs or "cross_sector" in secs:
            broad.append(o)
    return specific, broad

def channels(action_id, sector):
    """Per-action route summary: competitive SUPPLY + public-investment EVIDENCE + intermediated.
    Public investment has no application form, so its availability is driven by BIP precedent."""
    spec, broad = reachable_opps(sector)
    # public investment: feeder funds (supply) + BIP precedent (evidence)
    feeders = [o["opportunity_name"] for o in
               con.execute("SELECT opportunity_name FROM finance_opportunity WHERE funding_channel='public investment'")]
    pi = con.execute("""SELECT funding_sources, jurisdiction FROM finance_project
                        WHERE action_id=? AND funding_channel='public investment'""", (action_id,)).fetchall()
    from collections import Counter
    funded_via = Counter()
    for r in pi:
        for f in json.loads(r["funding_sources"]):
            if f.get("source_label"): funded_via[f["source_label"]] += 1
    # intermediated: MTT supply + GCF evidence
    inter_supply = [dict(o) for o in con.execute(
        "SELECT * FROM finance_opportunity WHERE funding_channel='intermediated'")]
    inter_supply = [o for o in inter_supply if sector in (json.loads(o["gpc_sectors"]) or []) or "cross_sector" in (json.loads(o["gpc_sectors"]) or [])]
    gcf = con.execute("""SELECT COUNT(*) FROM finance_project
                         WHERE action_id=? AND funding_channel='intermediated multilateral'""", (action_id,)).fetchone()[0]

    ch = {
        "competitive": {
            "available": bool(spec or broad),
            "n_sector_specific": len(spec), "n_broad": len(broad),
            "access_tier": "competitive (city or enabled actor applies to a concurso)"},
        "public_investment": {
            "available": len(pi) > 0,
            "access_tier": "BIP-SNI-gated — no application form; city formulates an iniciativa, "
                           "passes the SNI/BIP gate, then draws a feeder fund",
            "feeder_funds": feeders,
            "evidence": {"n_precedent_projects": len(pi),
                         "funded_via": dict(funded_via.most_common()),
                         "example_comunas": [r["jurisdiction"] for r in pi[:5]]}},
        "intermediated": {
            "available": bool(inter_supply) or gcf > 0,
            "access_tier": "intermediated — via operator (transport subsidy) or accredited entity (multilateral)",
            "n_supply": len(inter_supply), "n_precedent_projects": gcf}}
    # honest gap: only when NO channel is open
    ch["is_real_gap"] = not (ch["competitive"]["available"] or
                             ch["public_investment"]["available"] or
                             ch["intermediated"]["available"])
    return ch

def opp_view(o):
    return {"opportunity_name": o["opportunity_name"], "funder_name": o["funder_name"],
            "instrument": o["instrument"], "specificity": o["specificity"],
            "city_application": o["city_application"], "funding_channel": o["funding_channel"],
            "status": o["status"], "recurrence": o["recurrence"],
            "open_date": o["open_date"], "close_date": o["close_date"],
            "amount_clp": o["amount_clp"], "source_url": o["source_url"]}

def precedent(action_id, scope, comuna_name):
    q = "SELECT * FROM finance_project WHERE action_id=?"
    args = [action_id]
    if scope == "comuna":
        q += " AND UPPER(jurisdiction)=UPPER(?)"; args.append(comuna_name)
    rows = con.execute(q + " ORDER BY cost_total DESC NULLS LAST LIMIT 5", args).fetchall()
    return rows

def proj_view(p):
    fs = json.loads(p["funding_sources"]) if p["funding_sources"] else []
    return {"project_name": p["project_name"], "jurisdiction": p["jurisdiction"],
            "lifecycle_stage": p["lifecycle_stage"], "cost_total": p["cost_total"],
            "amount_unit": p["amount_unit"], "duration_months": p["duration_months"],
            "funding_channel": p["funding_channel"], "match_label": p["match_label"],
            "funding_sources": fs}

def action_block(action_id):
    a = con.execute("SELECT * FROM finance_action WHERE action_id=?", (action_id,)).fetchone()
    s = scored.get((DEMO_CUT, action_id))
    if not a or not s:
        return None
    sector = a["sector"]
    specific, broad = reachable_opps(sector)
    route = s["route"]
    return {
        "action_id": action_id, "action_name": a["action_name"], "sector": sector,
        "financial_feasibility": n(s["financial_feasibility"]),
        "route": route,
        "reason": reason(route, a, prof, len(specific), len(broad)),
        "inputs": {
            "action": {"intervention_type": a["intervention_type"],
                       "capital_intensity": a["capital_intensity"],
                       "preparation_complexity": a["preparation_complexity"]},
            "city": {"autonomy": prof["autonomy"], "capacity": prof["capacity"],
                     "archetype": prof["city_archetype"]},
            "finance": {"fund_access": s["fund_access"],
                        "n_reachable_sector_specific": len(specific),
                        "n_reachable_broad": len(broad)},
            "evidence": {"n_existing_projects": n(s["n_existing_projects"]),
                         "benchmark_duration_median_months": a["bench_duration_median_months"],
                         "benchmark_match_confidence": a["match_confidence"]}},
        "channels": channels(action_id, sector),
        "links": {
            "opportunities": f"/api/v1/cities/{ACTOR_ID}/climate-finance/opportunities?action_id={action_id}",
            "projects": f"/api/v1/cities/{ACTOR_ID}/climate-finance/projects?action_id={action_id}"}}

def reason(route, a, prof, n_specific, n_broad):
    it = a["intervention_type"]; ci = a["capital_intensity"]
    funds = f"{n_specific} sector-specific + {n_broad} broad reachable fund(s)"
    if route == "self-deliverable":
        return f"Low-capital {it} action (capital_intensity {ci}); self-deliverable regardless of city finances."
    if route == "own-budget feasible":
        return f"Capital action within reach of this city's autonomy ({prof['autonomy']}); own-budget feasible."
    if route == "needs technical assistance":
        return f"{it.capitalize()} action whose preparation demand exceeds this city's capacity ({prof['capacity']}); needs TA."
    if route == "needs co-finance":
        return f"Capital-intensive {it} action beyond this city's autonomy; needs external co-finance. {funds} in sector."
    return (f"High capital + preparation demand against a low-autonomy/low-capacity city; "
            f"needs external finance plus technical assistance / pooling. {funds} in sector.")

META = {"actor_id": ACTOR_ID, "comuna": prof["comuna_name"], "comuna_cut": DEMO_CUT, "country_code": "CL",
        "release": {"version_label": "v1", "released_at": "2026-06-19",
                    "source_dataset": "oef/cl-city-action-fundability"},
        "methodology": {"status": "working", "city_layer": "profiled",
                        "caveats": ["not a probability of securing funding",
                                    "coverage reflects what is catalogued, not real-world award behaviour"]}}

# ---- 1. feasibility: up to 2 actions per route ------------------------------
from collections import Counter
picks, per_route = [], Counter()
for (cut, aid), s in sorted(scored.items()):
    if cut != DEMO_CUT:
        continue
    r = s["route"]
    if per_route[r] < 2:
        per_route[r] += 1; picks.append(aid)
feas = {"meta": META, "data": [b for aid in picks if (b := action_block(aid))]}
json.dump(feas, open(OUT / "example_1_feasibility.json", "w"), indent=2, ensure_ascii=False)
seen_routes = set(per_route)

# choose a focus action from REAL precedent: most strong/goal_aligned projects,
# that also has reachable funds and is non-transport for a clean story.
cands = con.execute("""SELECT action_id, COUNT(*) c FROM finance_project
  WHERE action_id IS NOT NULL AND match_label IN ('strong','goal_aligned')
  GROUP BY action_id ORDER BY c DESC""").fetchall()
focus = None
for row in cands:
    fa = con.execute("SELECT * FROM finance_action WHERE action_id=?", (row["action_id"],)).fetchone()
    if not fa or (DEMO_CUT, row["action_id"]) not in scored:
        continue
    spec, broad = reachable_opps(fa["sector"])
    if (spec or broad) and fa["sector"] != "transportation":
        focus = row["action_id"]; break
focus = focus or cands[0]["action_id"]
fa = con.execute("SELECT * FROM finance_action WHERE action_id=?", (focus,)).fetchone()
focus_sector = fa["sector"]
spec, broad = reachable_opps(focus_sector)
opps = spec + broad

# ---- 2. opportunities for the focus action ----------------------------------
opp_json = {"meta": {**META, "filter": {"action_id": focus, "sector": focus_sector,
            "n_sector_specific": len(spec), "n_broad": len(broad),
            "note": "reachable = national/regional supply matching the action's sector a municipality can access; sector-specific listed first"}},
            "data": [opp_view(o) for o in opps[:8]]}
json.dump(opp_json, open(OUT / "example_2_opportunities.json", "w"), indent=2, ensure_ascii=False)

# ---- 3. projects (precedent) for the focus action, sector scope -------------
proj_rows = precedent(focus, "sector", prof["comuna_name"])
proj_json = {"meta": {**META, "filter": {"action_id": focus, "scope": "sector",
             "note": "scope=comuna restricts to this city; scope=sector shows national precedent"}},
             "data": [proj_view(p) for p in proj_rows]}
json.dump(proj_json, open(OUT / "example_3_projects.json", "w"), indent=2, ensure_ascii=False)

# ---- 4. action drill-down (composed) ----------------------------------------
detail = {"meta": META, "data": {**action_block(focus),
          "benchmark": {"n_projects": fa["bench_n_projects"],
                        "duration_median_months": fa["bench_duration_median_months"],
                        "cost_median_mmclp": fa["bench_cost_median_mmclp"],
                        "match_confidence": fa["match_confidence"]},
          "reachable_opportunities": [opp_view(o) for o in opps[:5]],
          "precedent_projects": [proj_view(p) for p in proj_rows[:3]]}}
json.dump(detail, open(OUT / "example_4_action_detail.json", "w"), indent=2, ensure_ascii=False)

# ---- 5. channels contrast: BIP-evidenced action vs a transport action -------
def first_action(sector_pred):
    for row in cands:
        fa2 = con.execute("SELECT * FROM finance_action WHERE action_id=?", (row["action_id"],)).fetchone()
        if fa2 and sector_pred(fa2["sector"]) and (DEMO_CUT, row["action_id"]) in scored:
            return row["action_id"], fa2
    return None, None

# a transport action (where competitive municipal supply is the classic "gap")
t_aid = next((aid for (cut, aid) in scored
              if cut == DEMO_CUT
              and (r := con.execute("SELECT sector FROM finance_action WHERE action_id=?", (aid,)).fetchone())
              and r["sector"] == "transportation"), None)
contrast = {"meta": {**META, "note": "how each action's funding channels resolve — "
            "public investment is signalled by BIP precedent, not by an application form, "
            "so it stops reading as a gap"},
            "data": []}
for aid in [focus, t_aid]:
    if not aid:
        continue
    a2 = con.execute("SELECT * FROM finance_action WHERE action_id=?", (aid,)).fetchone()
    contrast["data"].append({"action_id": aid, "action_name": a2["action_name"],
                             "sector": a2["sector"], "channels": channels(aid, a2["sector"])})
json.dump(contrast, open(OUT / "example_5_channels.json", "w"), indent=2, ensure_ascii=False)

# schema dump
with open(OUT / "schema.sql", "w") as f:
    for r in con.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL AND name NOT LIKE '\\_%' ESCAPE '\\' ORDER BY type DESC, name"):
        f.write(r["sql"] + ";\n\n")

print("focus action:", focus, "-", fa["action_name"], "| sector:", focus_sector)
print("reachable opportunities:", len(opps), "| precedent projects (sector):", len(proj_rows))
print("feasibility actions shown:", len(feas["data"]), "routes:", sorted(seen_routes))
print("files:", *[p.name for p in sorted(OUT.glob("*"))])
con.close()
