"""
Profile actions or projects with a `primary_channel` / `secondary_channel` facet —
the "what specifically is being affected" dimension that distinguishes
bike_infrastructure from bike_sharing, landfill from mbt_eco_park, etc.

This is a **delivery / implementation channel** (where the intervention lands),
not IPCC emissions scope (scope 1 / 2 / 3).

Adds two columns to the existing profile CSV:
- primary_channel
- secondary_channel

Doesn't touch outcome / intervention / climate_relevance / confidence / reasoning.
Skips rows that already have a primary_channel value (resume-safe).

If the input CSV still has legacy ``primary_scope`` / ``secondary_scope`` columns,
their values are copied into the channel columns on load and those legacy columns
are dropped from the rewritten file.

Modes
-----
    python scripts/profile_channel.py --mode actions
    python scripts/profile_channel.py --mode projects

Default inputs/outputs (modifies in place, backed up to .bak):
    actions  -> data/derived/actions_profiled.csv
    projects -> data/derived/projects_profiled.csv

Projects: by default profiles only rows where the matcher will actually
attempt matching (climate_relevance in {mitigation, mixed, unclear} AND
primary_outcome != transport_continuity). The rest get channel = '' (correct,
they go to sentinel routes).
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import os
import shutil
import signal
import sys
import time
from pathlib import Path

try:
    from openai import AsyncOpenAI
except ImportError:
    print("openai not installed. pip install openai>=1.82.0", file=sys.stderr)
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
INPUTS = ROOT / "data" / "inputs"
DERIVED = ROOT / "data" / "derived"

DEFAULT_INPUTS = {
    "actions":  DERIVED / "actions_profiled.csv",
    "projects": DERIVED / "projects_profiled.csv",
}
ID_COLUMN = {
    "actions":  "action_id",
    "projects": "codigo_bip",
}

NEW_COLS = ["primary_channel", "secondary_channel"]
LEGACY_SCOPE_COLS = ("primary_scope", "secondary_scope")


# ---------------------------------------------------------------------------
# Controlled vocabulary — flat list, organised in the prompt by family.
# ---------------------------------------------------------------------------

CHANNEL_VALUES = [
    # transport
    "bike_infrastructure",
    "bike_sharing",
    "public_bus",
    "public_rail",
    "freight",
    "urban_form_tod",
    "congestion_pricing",
    "transit_general",
    # waste
    "landfill",
    "mbt_eco_park",
    "recycling_collection",
    "organic_composting",
    "construction_demolition_waste",
    "waste_regulation",
    # energy supply / generation
    "solar_pv",
    "solar_thermal",
    "wind",
    "biogas",
    "hydro",
    "renewable_general",
    # energy demand / buildings / industry
    "street_lighting",
    "building_residential",
    "building_institutional_public",
    "building_commercial",
    "building_industrial",
    "industrial_process",
    "water_heating",
    # land / AFOLU
    "forest",
    "peatland",
    "wetland_coastal",
    "urban_green",
    "agricultural_soil",
    "livestock",
    "fire_mgmt",
    "biochar",
    # cross-cutting / catch-all
    "financial_incentive_scheme",
    "regulation_standard",
    "capacity_building",
    "mrv_planning",
    "not_applicable",
]


SYSTEM_PROMPT = """You assign a **delivery channel** (NOT IPCC emissions scope 1/2/3).

The channel is the "what specifically is being affected" dimension — it sub-classifies within outcome and intervention.

The action or project already has primary_outcome and primary_intervention assigned. Use those plus the description to pick the channel.

CHANNEL VOCABULARY (pick exact strings):

TRANSPORT family:
- bike_infrastructure: physical bike lanes, bike parking, ciclovías. NOT bike-sharing schemes.
- bike_sharing: bike-share programs, rental fleets, public-bike systems.
- public_bus: bus fleets, BRT, bus operations.
- public_rail: metro, light rail, commuter rail, intercity rail (passenger or maintenance of existing rail).
- freight: freight trucks, freight rail, port access for cargo.
- urban_form_tod: compact urban form, transit-oriented development, zoning for density.
- congestion_pricing: tolls, charges, vehicle restrictions on polluting vehicles.
- transit_general: generic "improve public transport" without specific mode focus.

WASTE family:
- landfill: traditional landfill construction, upgrade, closure, gas capture.
- mbt_eco_park: integrated multi-technology waste treatment plants (mechanical biological treatment, "ecoparques") — only when project text describes integrated treatment of multiple waste fractions.
- recycling_collection: recycling centers, clean points, recycling containers, neighborhood recycling.
- organic_composting: composting facilities, vermicomposters, organic waste valorization.
- construction_demolition_waste: C&D waste management specifically.
- waste_regulation: bans, mandates, fees on waste (not infrastructure).

ENERGY SUPPLY family:
- solar_pv: photovoltaic panels, solar electricity.
- solar_thermal: solar water heating, solar thermal.
- wind: wind turbines, wind farms.
- biogas: biogas digesters, gas capture from waste/sludge.
- hydro: hydroelectric, small hydro.
- renewable_general: mixed/multi-renewable planning, microgrids, integrated planning.

ENERGY DEMAND / BUILDINGS / INDUSTRY family:
- street_lighting: public LED, solar street lighting, alumbrado público.
- building_residential: housing energy efficiency, residential retrofits, thermal subsidies for homes.
- building_institutional_public: schools, hospitals, government buildings.
- building_commercial: commercial / office building efficiency.
- building_industrial: industrial facility energy efficiency standards.
- industrial_process: industrial process emissions (steel, cement, manufacturing process changes).
- water_heating: solar/heat-pump water heating specifically.

LAND family:
- forest: afforestation, reforestation, sustainable forest management, deforestation reduction.
- peatland: peatland restoration / protection.
- wetland_coastal: mangroves, coastal wetlands, salt marsh restoration.
- urban_green: urban parks, green corridors, green spaces (climate role: heat + sequestration + sometimes flood).
- agricultural_soil: soil carbon, crop management, fertiliser practices.
- livestock: livestock methane, manure management, enteric fermentation.
- fire_mgmt: forest/grassland fire management.
- biochar: biochar production.

CROSS-CUTTING family (use only if no domain-specific channel fits):
- financial_incentive_scheme: payment-for-services, subsidies as the primary mechanism.
- regulation_standard: standards-setting / mandates with no specific physical delivery surface.
- capacity_building: training, awareness, technical assistance.
- mrv_planning: monitoring, reporting, verification, baseline studies, plans.
- not_applicable: project doesn't fit any channel; use sparingly.

RULES:
1. PRIMARY channel is the dominant focus. Be specific — pick the narrowest channel that fits.
2. SECONDARY channel ONLY if the source genuinely covers two distinct channels (use the REMOVAL TEST: would the action still exist as a real action without the secondary channel?). Otherwise null.
3. If the project is maintenance/replacement of existing transport assets (REPOSICION/CONSERVACION on metro/rail/bus), still pick the transport channel (public_rail / public_bus / freight) — the matcher will handle the maintenance routing elsewhere.
4. Output JSON only. No preamble.
"""


def make_schema() -> dict:
    enum_with_null = CHANNEL_VALUES + [None]
    return {
        "type": "object",
        "properties": {
            "primary_channel":   {"type": ["string", "null"], "enum": enum_with_null},
            "secondary_channel": {"type": ["string", "null"], "enum": enum_with_null},
            "reasoning":         {"type": "string"},
        },
        "required": ["primary_channel", "secondary_channel", "reasoning"],
        "additionalProperties": False,
    }


def action_user_message(row: dict) -> str:
    return (
        f"Action ID: {row.get('action_id','')}\n"
        f"Action name: {row.get('action_name','')}\n"
        f"GPC subsector: {row.get('subsector_number','')}\n"
        f"Primary outcome: {row.get('primary_outcome','')}\n"
        f"Primary intervention: {row.get('primary_intervention','')}\n"
        f"Action role: {row.get('action_role','')}\n"
        f"Description: {row.get('description','')}\n"
        f"Outcome summary: {row.get('outcome_summary','')}\n"
    )


def project_user_message(row: dict) -> str:
    return (
        f"Project: {row.get('nombre','')}\n"
        f"Descriptor: {row.get('descriptor','')}\n"
        f"Sector / subsector: {row.get('sector','')} / {row.get('subsector','')}\n"
        f"Climate classification (upstream): {row.get('climate_classification_es','')}\n"
        f"Climate relevance (auto): {row.get('climate_relevance','')}\n"
        f"Primary outcome: {row.get('primary_outcome','')}\n"
        f"Primary intervention: {row.get('primary_intervention','')}\n"
        f"Profiler reasoning: {(row.get('reasoning') or '')[:600]}\n"
    )


def needs_profiling(mode: str, row: dict) -> bool:
    if (row.get("primary_channel") or "").strip():
        return False
    if mode == "actions":
        return True
    # projects: skip rows that route to sentinel labels
    cr = (row.get("climate_relevance") or "").strip()
    po = (row.get("primary_outcome") or "").strip()
    if cr in {"adaptation", "not_climate"}:
        return False
    if po == "transport_continuity":
        return False
    return True


async def profile_row(client, model, sys_prompt, schema, user_msg):
    resp = await client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": sys_prompt},
                  {"role": "user",   "content": user_msg}],
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "channel_profile", "schema": schema, "strict": True},
        },
    )
    return json.loads(resp.choices[0].message.content)


def load_dotenv_release(path: Path) -> None:
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        if "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def write_output(path: Path, fields: list[str], rows: list[dict]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    tmp.replace(path)


def migrate_legacy_scope_columns(rows: list[dict]) -> None:
    """Copy legacy primary_scope/secondary_scope into channel columns when needed."""
    for r in rows:
        for c in NEW_COLS:
            r.setdefault(c, "")
        if (r.get("primary_channel") or "").strip():
            continue
        ps = (r.get("primary_scope") or "").strip()
        if not ps:
            continue
        r["primary_channel"] = ps
        r["secondary_channel"] = (r.get("secondary_scope") or "").strip()


def build_out_fields(in_fields: list[str]) -> list[str]:
    out = [f for f in in_fields if f not in LEGACY_SCOPE_COLS]
    for c in NEW_COLS:
        if c not in out:
            out.append(c)
    return out


async def run(args) -> int:
    load_dotenv_release(ROOT / ".env")
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not set", file=sys.stderr)
        return 1
    client = AsyncOpenAI()

    input_path = args.input or DEFAULT_INPUTS[args.mode]
    if not input_path.exists():
        print(f"input not found: {input_path}", file=sys.stderr)
        return 1

    with open(input_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        in_fields = list(reader.fieldnames or [])
        rows = list(reader)

    migrate_legacy_scope_columns(rows)
    out_fields = build_out_fields(in_fields)

    todo = [r for r in rows if needs_profiling(args.mode, r)]
    if args.limit is not None:
        todo = todo[:args.limit]
    print(f"input: {input_path}")
    print(f"rows total: {len(rows)}  to profile: {len(todo)}")
    if not todo:
        # Still backup + write so newly-added columns persist
        bak = input_path.with_suffix(input_path.suffix + ".bak")
        if not bak.exists():
            shutil.copy2(input_path, bak)
        write_output(input_path, out_fields, rows)
        print("Nothing to profile (columns ensured).")
        return 0

    msg_fn = action_user_message if args.mode == "actions" else project_user_message
    schema = make_schema()

    sys_tokens = len(SYSTEM_PROMPT) * 0.3
    sample = sum(len(msg_fn(r)) for r in todo[:min(20, len(todo))]) / max(1, min(20, len(todo)))
    est_in = (sys_tokens + sample * 0.3) * len(todo)
    est_out = 80 * len(todo)
    print(f"estimated cost ({args.model}): "
          f"${est_in/1e6*0.150 + est_out/1e6*0.600:.2f}")

    bak = input_path.with_suffix(input_path.suffix + ".bak")
    if not bak.exists():
        shutil.copy2(input_path, bak)
        print(f"backup: {bak}")

    sem = asyncio.Semaphore(args.concurrency)
    interrupted = {"flag": False}

    def on_int(sig, frame):
        interrupted["flag"] = True
        print("\nInterrupt — saving and exiting.")
    signal.signal(signal.SIGINT, on_int)

    t0 = time.time()
    done = 0
    save_lock = asyncio.Lock()

    async def worker(row):
        nonlocal done
        if interrupted["flag"]:
            return
        async with sem:
            if interrupted["flag"]:
                return
            try:
                result = await profile_row(client, args.model, SYSTEM_PROMPT, schema, msg_fn(row))
                row["primary_channel"] = result.get("primary_channel") or ""
                row["secondary_channel"] = result.get("secondary_channel") or ""
            except Exception as e:
                print(f"  FAILED {row.get(ID_COLUMN[args.mode])}: {e}", file=sys.stderr)
                row["primary_channel"] = ""
                row["secondary_channel"] = ""
        done += 1
        if done % args.save_every == 0:
            async with save_lock:
                write_output(input_path, out_fields, rows)
                rate = done / max(time.time() - t0, 0.001)
                remaining = len(todo) - done
                eta = remaining / max(rate, 0.001) / 60
                print(f"  [{done}/{len(todo)}]  {rate:.1f}/s  ETA {eta:.1f}min")

    await asyncio.gather(*[worker(r) for r in todo])
    write_output(input_path, out_fields, rows)
    print(f"\nDone. wrote {input_path}")
    return 0 if not interrupted["flag"] else 130


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", required=True, choices=["actions", "projects"])
    ap.add_argument("--input", type=Path, default=None)
    ap.add_argument("--model", default="gpt-4o-mini")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--save-every", type=int, default=50)
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    sys.exit(asyncio.run(run(args)))


if __name__ == "__main__":
    main()
