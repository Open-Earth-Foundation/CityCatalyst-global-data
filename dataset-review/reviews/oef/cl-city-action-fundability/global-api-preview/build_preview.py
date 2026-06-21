#!/usr/bin/env python3
"""
Preview build for the global-api Chile climate-finance design.

Reads the v1 finance_db fixture CSVs and constructs a SQLite database that
mirrors the proposed global-api tables:
    finance_opportunity   (base table)
    finance_project       (base table, co-finance folded into funding_sources JSON)
    finance_action        (VIEW: demands banded from action attrs + benchmark roll-up)
    city_finance_profile  (Phase 2 table, from the scored fixture's autonomy/capacity)

Then emits example API responses (JSON) so the data shapes are visible before
any migration is written. This is a PREVIEW: ids/coverage mirror the fixture.
"""
import csv, json, sqlite3, re, unicodedata
from pathlib import Path
from statistics import median

BASE = Path("/sessions/jolly-dazzling-ritchie/mnt/CityCatalyst-global-data/"
            "dataset-review/reviews/oef/cl-city-action-fundability/releases/v1")
DATA = BASE / "data"
FDB = BASE / "finance_db"
OUT = Path("/sessions/jolly-dazzling-ritchie/mnt/outputs/finance_preview")
OUT.mkdir(parents=True, exist_ok=True)
DB = Path("/tmp/finance_preview.db")

# ---------- helpers ----------------------------------------------------------
def rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

def num(v):
    if v is None or v == "" or str(v).lower() == "nan":
        return None
    try:
        f = float(v)
        return int(f) if f.is_integer() else f
    except ValueError:
        return None

def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

def city_application(city_can_apply):
    t = (city_can_apply or "").lower()
    if "facilitat" in t: return "facilitated"
    if "intermediat" in t or t.startswith("no"): return "intermediated"
    if t.startswith("yes") or "direct" in t: return "direct"
    return None

def channel_descriptor(route_text):
    t = (route_text or "").lower()
    if "public investment" in t or "bip" in t or "sni" in t: return "public investment"
    if "intermediat" in t or "multilateral" in t: return "intermediated multilateral"
    if "competitive" in t or "concurso" in t or t.startswith("route a"): return "competitive fund"
    return route_text or None

# preparation_complexity banding from intervention_type (methodology B3)
PREP = {"regulatory": 0.2, "planning": 0.5, "program": 0.5, "financial": 0.5,
        "infrastructure": 0.8}
def preparation_complexity(intervention_type, capital_intensity):
    base = PREP.get((intervention_type or "").lower())
    if base is None:
        return None
    if base == 0.8 and (capital_intensity or 0) >= 0.8:
        return 0.9
    return base

def city_archetype(aut, cap):
    if aut is None or cap is None: return None
    hi_a, hi_c = aut >= 0.5, cap >= 0.5
    return {(True, True): "self-starter", (False, True): "capable-but-cash-tight",
            (True, False): "funded-but-thin", (False, False): "needs-full-support"}[(hi_a, hi_c)]

# ---------- load -------------------------------------------------------------
opps = rows(FDB / "opportunities.csv")
projs = rows(FDB / "projects.csv")
pfund = rows(FDB / "project_funding.csv")
acts = rows(FDB / "actions.csv")
scored = rows(DATA / "fundability_scored.csv")
inv = rows(DATA / "chile_finance_inventory.csv")

# inventory lookup for dates/amount, keyed (source_dataset_prefix, normalized name)
inv_lk = {}
for r in inv:
    inv_lk[(r["source_dataset"], norm(r["program_name"]))] = r

def inv_match(opp):
    prefix = opp["source_dataset"].split("/")[0]
    return inv_lk.get((prefix, norm(opp["opportunity_name"])))

# ---------- build sqlite -----------------------------------------------------
con = sqlite3.connect(DB)
con.execute("DROP TABLE IF EXISTS finance_opportunity")
con.execute("DROP TABLE IF EXISTS finance_project")
con.execute("DROP TABLE IF EXISTS city_finance_profile")
con.execute("DROP TABLE IF EXISTS finance_action_base")
con.execute("DROP VIEW  IF EXISTS finance_action")

con.execute("""CREATE TABLE finance_opportunity(
  source_opportunity_id TEXT, opportunity_name TEXT, funder_name TEXT, funder_level TEXT,
  funder_channel TEXT, instrument TEXT, gpc_sectors TEXT, eligible_actor TEXT,
  city_application TEXT, funding_channel TEXT, access_tier TEXT, open_date TEXT, close_date TEXT,
  status TEXT, status_as_of TEXT, recurrence TEXT, amount_clp REAL, amount_note TEXT,
  climate_relevance TEXT, specificity TEXT, source_url TEXT, country_code TEXT,
  source_dataset TEXT)""")

def classify(name, source_dataset, city_app):
    """Re-derive (funding_channel, access_tier, city_application) since the v1 fixture
    flattened every opportunity to 'Route A — competitive fund'. Production reads this
    straight from the source reviews; here it is a name/source heuristic.
    access_tier (methodology B5): competitive | BIP-SNI-gated | intermediated."""
    n, sd = name.lower(), source_dataset.lower()
    if "8%" in n:                                   # FNDR 8% is a competitive activity subvention
        return "competitive fund", "competitive", city_app or "direct"
    if any(k in n for k in ("fndr", "fril", "frpd")) or "gore" in sd:
        return "public investment", "BIP-SNI-gated", "direct"   # city formulates, passes the gate
    if "subdere" in sd:                             # PMU/PMB/PMR/FRC municipal infrastructure via SNI
        return "public investment", "BIP-SNI-gated", "direct"
    if city_app == "intermediated" or "mtt" in sd:  # operator-facing transport subsidy
        return "intermediated", "intermediated", "intermediated"
    return "competitive fund", "competitive", city_app or "direct"

for o in opps:
    m = inv_match(o) or {}
    channel, tier, city_app = classify(o["opportunity_name"], o["source_dataset"],
                                       city_application(o.get("city_can_apply")))
    con.execute("INSERT INTO finance_opportunity VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
        o["opportunity_id"], o["opportunity_name"], o["funder_name"], None,
        channel, o["instrument"], o["gpc_sectors"], o["eligible_actor"],
        city_app, channel, tier,
        m.get("open_date") or None, m.get("close_date") or None,
        o["status"], m.get("status_as_of") or None, o["recurrence"],
        num(m.get("amount_clp")), o.get("amount_note") or None,
        o["climate_relevance"], o["specificity"], o["source_url"], "CL", o["source_dataset"]))

# project funding grouped -> JSON
funding_by_proj = {}
for f in pfund:
    funding_by_proj.setdefault(f["project_id"], []).append({
        "source_label": f["source_label"] or None,
        "source_opportunity_id": f["opportunity_id"] or None,
        "amount": num(f["amount"]), "amount_unit": f["amount_unit"] or None,
        "paid_amount": num(f["paid_amount"]), "cycle": num(f["cycle"])})

con.execute("""CREATE TABLE finance_project(
  source_project_id TEXT, action_id TEXT, project_name TEXT, sector TEXT,
  jurisdiction TEXT, actor_id TEXT, lifecycle_stage TEXT, evaluation_verdict TEXT,
  cost_total REAL, amount_committed REAL, amount_paid REAL, amount_unit TEXT,
  duration_months REAL, beneficiaries_total INTEGER, owner_formulator TEXT,
  match_label TEXT, funding_channel TEXT, funding_sources TEXT,
  country_code TEXT, source_dataset TEXT)""")
for p in projs:
    con.execute("INSERT INTO finance_project VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
        p["project_id"], p["action_id"] or None, p["project_name"], p["sector"],
        p["jurisdiction"] or None, None, p["lifecycle_stage"] or None,
        p["evaluation_verdict"] or None, num(p["cost_total"]), num(p["amount_committed"]),
        num(p["amount_paid"]), p["amount_unit"] or None, num(p["duration_months"]),
        num(p["beneficiaries_total"]), p["owner_formulator"] or None, p["match_label"] or None,
        channel_descriptor(p.get("route")),
        json.dumps(funding_by_proj.get(p["project_id"], []), ensure_ascii=False),
        "CL", p["source_dataset"]))

# finance_action: base (stands in for action_pathway demands) + benchmark roll-up
con.execute("""CREATE TABLE finance_action_base(
  action_id TEXT, action_name TEXT, sector TEXT, intervention_type TEXT,
  capital_intensity REAL, preparation_complexity REAL, country_code TEXT)""")
for a in acts:
    cap = num(a["capital_demand"])
    con.execute("INSERT INTO finance_action_base VALUES (?,?,?,?,?,?,?)", (
        a["action_id"], a["action_name"], a["sector"], a["archetype"],
        cap, preparation_complexity(a["archetype"], cap), "CL"))

# benchmark roll-up from finance_project (strong/goal_aligned only) -> temp table
con.execute("DROP TABLE IF EXISTS _bench")
con.execute("CREATE TABLE _bench(action_id TEXT, bench_n_projects INT, "
            "bench_duration_median_months REAL, bench_duration_n INT, "
            "bench_cost_median_mmclp REAL, bench_cost_n INT, match_confidence TEXT)")
by_action = {}
for p in projs:
    if (p["match_label"] or "") in ("strong", "goal_aligned") and p["action_id"]:
        by_action.setdefault(p["action_id"], []).append(p)
for aid, ps in by_action.items():
    durs = [num(x["duration_months"]) for x in ps if num(x["duration_months"]) not in (None, 0)]
    costs = [num(x["cost_total"]) for x in ps if num(x["cost_total"]) is not None]
    labels = [x["match_label"] for x in ps]
    dom = max(set(labels), key=labels.count)
    con.execute("INSERT INTO _bench VALUES (?,?,?,?,?,?,?)", (
        aid, len(ps), round(median(durs), 1) if durs else None, len(durs),
        round(median(costs), 1) if costs else None, len(costs), dom))

con.execute("""CREATE VIEW finance_action AS
  SELECT b.action_id, b.action_name, b.sector, b.intervention_type,
         b.capital_intensity, b.preparation_complexity,
         k.bench_n_projects, k.bench_duration_median_months, k.bench_duration_n,
         k.bench_cost_median_mmclp, k.bench_cost_n, k.match_confidence,
         b.country_code
  FROM finance_action_base b LEFT JOIN _bench k ON k.action_id = b.action_id""")

# city_finance_profile from scored fixture (distinct comuna)
con.execute("""CREATE TABLE city_finance_profile(
  actor_id TEXT, comuna_cut TEXT, comuna_name TEXT, autonomy REAL, capacity REAL,
  city_archetype TEXT, country_code TEXT)""")
seen = {}
for s in scored:
    cut = s["comuna_cut"]
    if cut in seen: continue
    seen[cut] = 1
    aut, cap = num(s["autonomy"]), num(s["capacity"])
    # actor_id unresolved in fixture -> placeholder shows the production join point
    con.execute("INSERT INTO city_finance_profile VALUES (?,?,?,?,?,?,?)", (
        f"CL-COMUNA-{cut}", cut, s["comuna"], aut, cap, city_archetype(aut, cap), "CL"))

con.commit()

# scored lookup for the demo (route/fund_access/score come from methodology run)
scored_lk = {(s["comuna_cut"], s["action_id"]): s for s in scored}

# choose a demo comuna: most actions with existing-project precedent
from collections import Counter
prec = Counter()
for s in scored:
    if num(s["n_existing_projects"]):
        prec[(s["comuna_cut"], s["comuna"])] += 1
(demo_cut, demo_name), _ = prec.most_common(1)[0]
print(f"DEMO city: {demo_name} ({demo_cut})")

# counts
for t in ["finance_opportunity", "finance_project", "finance_action", "city_finance_profile"]:
    n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"  {t:22s} {n:>6d} rows")
dated = con.execute("SELECT COUNT(*) FROM finance_opportunity WHERE close_date IS NOT NULL").fetchone()[0]
print(f"  opportunities with close_date: {dated}")

con.close()
print("DB ->", DB)
