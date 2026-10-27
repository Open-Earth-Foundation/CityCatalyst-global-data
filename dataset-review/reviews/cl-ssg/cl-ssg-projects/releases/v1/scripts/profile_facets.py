"""
Profile climate actions or projects with structured outcome + intervention facets.

Calls OpenAI with structured JSON output (enforced schema) to assign:
- primary_outcome, secondary_outcome (controlled vocab, 10 values, multi-value)
- primary_intervention, secondary_intervention (controlled vocab, 7 values)
- climate_relevance (projects only, 5 values)
- confidence (high/medium/low) + reasoning

Modes
-----
    python scripts/profile_facets.py --mode actions
    python scripts/profile_facets.py --mode projects

Inputs (defaults)
-----------------
    actions  -> data/inputs/actions.csv
    projects -> data/inputs/projects.csv

Environment
-------------
    ``OPENAI_API_KEY`` is required. If unset, the script loads ``.env`` at the
    release root (``releases/v1/.env``) when present; existing environment
    variables are not overwritten.

Outputs
-------
    actions  -> data/derived/actions_profiled.csv
    projects -> data/derived/projects_profiled.csv

Each output CSV contains the original columns plus:
    primary_outcome, secondary_outcome,
    primary_intervention, secondary_intervention,
    confidence, reasoning,
    (climate_relevance for projects only)

Resume: if the output already exists, only rows missing primary_outcome are
profiled. Use --refresh to re-profile everything.

Smoke test first:
    python scripts/profile_facets.py --mode actions --limit 10
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import os
import signal
import sys
import time
from collections import defaultdict
from pathlib import Path

try:
    from openai import AsyncOpenAI
except ImportError:
    print("openai not installed. Install with: pip install openai>=1.82.0",
          file=sys.stderr)
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
INPUTS = ROOT / "data" / "inputs"
DERIVED = ROOT / "data" / "derived"


def load_dotenv_release(path: Path) -> None:
    """Load KEY=VALUE lines from ``path`` into ``os.environ`` if not already set."""
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

DEFAULT_INPUTS = {
    "actions":  INPUTS / "actions.csv",
    "projects": INPUTS / "projects.csv",
}
DEFAULT_OUTPUTS = {
    "actions":  DERIVED / "actions_profiled.csv",
    "projects": DERIVED / "projects_profiled.csv",
}
# In projects mode we enrich each row's narrative from the bilingual ES+EN table
# (one row per etapa), joined by codigo_bip -> bip_code.
TRANSLATED_TABLE = DERIVED / "ficha_idi_table_translated.csv"

ID_COLUMN = {
    "actions":  "action_id",
    "projects": "codigo_bip",
}

NEW_FACET_COLUMNS = [
    "primary_outcome",
    "secondary_outcome",
    "primary_intervention",
    "secondary_intervention",
    "confidence",
    "reasoning",
]


# ---------------------------------------------------------------------------
# Controlled vocabularies
# ---------------------------------------------------------------------------

OUTCOME_VALUES = [
    "emissions_efficiency",
    "emissions_fuel_switch",
    "emissions_modal_shift",
    "emissions_demand_reduction",
    "emissions_waste_diversion",
    "carbon_sequestration",
    "transport_continuity",
    "resilience_water",
    "resilience_flood",
    "resilience_other",
    "enabling",
]

# 5-value canonical intervention vocab — aligns with actions.json intervention_type.
INTERVENTION_VALUES = [
    "infrastructure",
    "program",
    "regulatory",
    "planning",
    "financial",
]

CLIMATE_RELEVANCE_VALUES = [
    "mitigation",
    "adaptation",
    "mixed",
    "unclear",
    "not_climate",
]


SHARED_SYSTEM_PROMPT = """You classify climate actions or projects along structured facets for downstream matching.

DOMAIN: Climate action library curated for Chilean cities, organized by GPC inventory subsectors (I = stationary energy, II = transport, III = waste, IV = industrial processes, V = AFOLU/land use). The action library is mitigation-only.

OUTCOME VOCABULARY (pick exact strings):
- emissions_efficiency: less energy or material per unit of activity (e.g., building efficiency standards, industrial heat recovery, efficient furnaces, LED retrofit)
- emissions_fuel_switch: replace high-carbon energy source with low-carbon (e.g., zero-emission bus fleets, fleet electrification, renewable energy supply, biogas displacing fossil fuel)
- emissions_modal_shift: shift activity from high-carbon mode to low-carbon. ONLY for projects that EXPAND or CREATE low-carbon mode capacity (new bike lanes, new metro line construction, new BRT, new transit-oriented development). Do NOT use for maintenance, equipment replacement, or operational continuity of EXISTING low-carbon modes — those go to transport_continuity.
- transport_continuity: maintain, repair, or replace existing low-carbon transport infrastructure or operational assets — keeps an existing low-carbon mode running but doesn't shift modes or expand capacity. Examples: metro signaling replacement, rail track maintenance, station equipment upgrade, port access rail repair, transit ticket-machine procurement, rolling-stock minor equipment, bridge replacement on an existing rail line. Includes "REPOSICION / CONSERVACION / MEJORAMIENTO" projects on existing rail, metro, bus, or transit assets.
- emissions_demand_reduction: reduce the activity or material demand itself (e.g., compact urban form, single-use material bans, behavior-change campaigns)
- emissions_waste_diversion: divert waste from high-emission disposal, including methane capture (e.g., landfill gas capture, biogas at WWTP, recycling, composting)
- carbon_sequestration: store atmospheric carbon in soils, vegetation, or wetlands (e.g., afforestation, peatland restoration, urban tree planting, coastal wetlands)
- resilience_water: water security, sanitation reliability, drought adaptation (mostly projects — no actions in current library)
- resilience_flood: fluvial / pluvial / stormwater flood adaptation (mostly projects — no actions)
- resilience_other: slope/landslide, coastal, heat, other adaptation (mostly projects — no actions)
- enabling: capacity-building, governance, planning, finance, MRV — doesn't directly change emissions or resilience (e.g., payment-for-environmental-services schemes, regulatory frameworks, baseline studies)

INTERVENTION VOCABULARY (pick exact strings):
- infrastructure: physical asset work — new construction OR upgrade/replacement of existing assets, OR procurement and rollout of specific technology (vehicle fleets, solar panels, sensors). Covers bike lanes, new parks, building retrofits, treatment plants, equipment procurement, fleet electrification.
- program: training, technical assistance, education, awareness campaigns, capacity-building.
- regulatory: standards, mandates, bans, zoning, permits enforced by an authority.
- planning: studies, design, baseline-setting, MRV, master plans, feasibility analysis.
- financial: subsidies, grants, taxes, rebates, payments-for-services, financial incentives.

MULTI-VALUE RULE — use the REMOVAL TEST: Imagine removing the supposed secondary value's activities from the action. Would the action still achieve its primary climate goal as a real, fundable action on its own?
- If YES (the action stands on its own without the secondary content), the secondary content is supporting/enabling, NOT a second value. Set secondary_outcome=null and secondary_intervention=null. Be conservative — when in doubt, leave secondary null.
- If NO (the action wouldn't be a real climate action without that second component), the secondary value is substantive. Assign it.

Worked examples (apply the removal test in your head):
- "Zero-emission bus fleet procurement, with eco-driving training and maintenance programs": REMOVE the training -> "adopt zero-emission bus fleets" is still a real, fundable action. Training is supporting/enabling, not a second intervention. -> primary_outcome=emissions_fuel_switch, secondary_outcome=null. primary_intervention=infrastructure, secondary_intervention=null.
- "Retrofit residential buildings for energy efficiency, with rebates for high-efficiency appliances": REMOVE the rebates -> "retrofit buildings for efficiency" is still a real action, BUT the rebates fundamentally shape who retrofits and at what scale, and are described as a co-equal component. -> primary_intervention=infrastructure, secondary_intervention=financial.
- "Stormwater detention park with afforestation": REMOVE the afforestation -> "build a detention basin" is one real action. REMOVE the basin -> "plant trees on this site" is another real action. Both stand on their own as distinct physical components. -> primary_outcome=resilience_flood, secondary_outcome=carbon_sequestration.
- "Bike lane construction; also improves air quality and public health": REMOVE the air-quality framing -> bike lane construction is still a real action. Air quality is a co-benefit, not a second outcome. -> primary_outcome=emissions_modal_shift, primary_intervention=infrastructure, secondary_outcome=null.
- "Efficiency standards for new buildings; includes solar-ready wiring requirements": REMOVE the solar-ready clause -> the standards are still a real action. Solar-ready wiring is incidental. -> primary_intervention=regulatory, secondary_intervention=null.
- "Construction of metro line 3" (NEW metro line): primary_outcome=emissions_modal_shift, primary_intervention=infrastructure. This expands low-carbon capacity.
- "Replacement of metro signaling system on existing line" (REPOSICION SISTEMA CONTROL DE TRENES): primary_outcome=transport_continuity, primary_intervention=infrastructure. The signaling replacement keeps the existing metro running but doesn't shift anyone to it.
- "Procurement of ticket vending machines for metro" (ADQUISICION MAQUINAS DE AUTOSERVICIO METRO): primary_outcome=transport_continuity, primary_intervention=infrastructure. Operational equipment replacement.
- "Bike lane construction" (CONSTRUCCION CICLOVIA): primary_outcome=emissions_modal_shift, primary_intervention=infrastructure. New low-carbon mode capacity.

CONFIDENCE:
- high: BOTH facets are unambiguous AND you had NO judgment call about a possible secondary value (even one you ultimately decided against). Reserve high for the cleanest, single-facet, no-debate cases.
- medium: you considered adding a secondary value and decided one way or the other, OR there was real judgment in picking between two plausible primary values.
- low: source text is too vague to classify confidently.

REASONING: one or two sentences. Cite specific language from the source where possible. No filler.

Output ONLY a JSON object matching the schema. No preamble.
"""

PROJECT_EXTRA_PROMPT = """

PROJECT MODE — Additional facet:

climate_relevance (pick exact string):
- mitigation: project's primary climate outcome is emissions reduction or sequestration
- adaptation: project's primary climate outcome is resilience (water/flood/other). The action library is mitigation-only, so this label flags an expected library gap.
- mixed: project has substantively distinct mitigation AND adaptation components
- unclear: project passed an upstream climate screen but its climate connection is weak or indirect
- not_climate: project doesn't appear to be a climate action at all. Leave outcomes/interventions null and explain in reasoning.

When climate_relevance is mitigation/adaptation, primary_outcome MUST be from the corresponding family:
- mitigation -> emissions_*, carbon_sequestration, transport_continuity, or enabling
- adaptation -> resilience_*
When mixed, primary_outcome is the more prominent component, secondary is the other family.
When unclear, classify best-guess outcomes and mark confidence=low.
When not_climate, set primary_outcome=null and primary_intervention=null.
"""


# ---------------------------------------------------------------------------
# Message construction
# ---------------------------------------------------------------------------

def action_user_message(row: dict) -> str:
    return (
        f"Action ID: {row.get('action_id', '')}\n"
        f"Action name: {row.get('action_name', '')}\n"
        f"GPC subsector: {row.get('subsector_number', '')}\n"
        f"Description: {row.get('description', '')}\n"
    )


# Narrative fields we use to score "fullness" when picking the best etapa per
# codigo_bip from the translated (one-row-per-etapa) table.
_NARRATIVE_FIELDS_FOR_SCORE = [
    "justification_es", "description_es", "purpose_es", "components_es",
    "conclusions_es", "purpose_indicators_es", "component_indicators_es",
]


def _narrative_score(r: dict) -> int:
    return sum(1 for f in _NARRATIVE_FIELDS_FOR_SCORE if (r.get(f) or "").strip())


def _parse_int(s: str) -> int:
    try:
        return int(s)
    except (TypeError, ValueError):
        return 0


def load_translated_narrative(path: Path) -> dict[str, dict]:
    """Return {bip_code: row} from the bilingual table, picking the best etapa per project.

    "Best" = non-STUB, non-duplicate, then the etapa with the most populated
    narrative fields, then the latest budget_year. Same logic the eval enricher
    uses. Returns an empty dict if the file doesn't exist (so projects mode
    still works on bare projects.csv).
    """
    if not path.exists():
        print(f"warning: translated narrative table not found at {path}; "
              f"profiling will use only projects.csv fields", file=sys.stderr)
        return {}
    by_bip: dict[str, list[dict]] = defaultdict(list)
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            code = (r.get("bip_code") or "").strip()
            if code:
                by_bip[code].append(r)
    chosen: dict[str, dict] = {}
    for code, candidates in by_bip.items():
        ranked = sorted(
            candidates,
            key=lambda r: (
                r.get("template_variant") != "STUB",
                r.get("warning_multi_etapa_identical_blocks", "") != "True",
                _narrative_score(r),
                _parse_int(r.get("budget_year", "")),
            ),
            reverse=True,
        )
        chosen[code] = ranked[0]
    return chosen


def project_user_message(row: dict, translated: dict[str, dict] | None = None) -> str:
    parts = [
        f"Project name: {row.get('nombre', '')}",
        f"Descriptor: {row.get('descriptor', '')}",
        f"Sector / subsector: {row.get('sector', '')} / {row.get('subsector', '')}",
        f"Climate classification (upstream): {row.get('climate_classification_es', '')}",
    ]

    # Pull narrative + extras from the translated table if joined. Falls back to
    # projects.csv's Spanish-only narrative when nothing is joined.
    t = (translated or {}).get((row.get("codigo_bip") or "").strip(), {})

    # Core narrative: prefer the (cleaner) translated table's EN, then its ES,
    # then projects.csv's plain Spanish.
    for label, en_key, es_key, fallback_key in [
        ("justificacion",     "justification_en",  "justification_es",  "justificacion"),
        ("descripcion_etapa", "description_en",    "description_es",    "descripcion_etapa"),
        ("proposito",         "purpose_en",        "purpose_es",        "proposito"),
        ("componentes",       "components_en",     "components_es",     "componentes_text"),
    ]:
        text = ((t.get(en_key) or "").strip()
                or (t.get(es_key) or "").strip()
                or (row.get(fallback_key) or "").strip())
        if text:
            parts.append(f"{label}: {text[:2000]}")

    # Bonus fields from the translated table that aren't in projects.csv.
    # Use ES for conclusions/indicators (their EN translations are still argos-quality).
    extras = [
        ("conclusions",          (t.get("conclusions_es") or "").strip()),
        ("purpose_indicators",   (t.get("purpose_indicators_es") or "").strip()),
        ("component_indicators", (t.get("component_indicators_es") or "").strip()),
        ("funding_breakdown",    (t.get("funding_breakdown") or "").strip()),
        ("environmental_assessment_status",
                                 (t.get("environmental_assessment_status") or "").strip()),
    ]
    for label, text in extras:
        if text:
            parts.append(f"{label}: {text[:1500]}")
    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# JSON schema for structured outputs
# ---------------------------------------------------------------------------

def make_schema(mode: str) -> dict:
    outcome_schema = {
        "type": ["string", "null"],
        "enum": OUTCOME_VALUES + [None],
    }
    intervention_schema = {
        "type": ["string", "null"],
        "enum": INTERVENTION_VALUES + [None],
    }
    props = {
        "primary_outcome": outcome_schema,
        "secondary_outcome": outcome_schema,
        "primary_intervention": intervention_schema,
        "secondary_intervention": intervention_schema,
        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
        "reasoning": {"type": "string"},
    }
    required = [
        "primary_outcome", "secondary_outcome",
        "primary_intervention", "secondary_intervention",
        "confidence", "reasoning",
    ]
    if mode == "projects":
        props = {
            "climate_relevance": {"type": "string", "enum": CLIMATE_RELEVANCE_VALUES},
            **props,
        }
        required = ["climate_relevance"] + required

    return {
        "type": "object",
        "properties": props,
        "required": required,
        "additionalProperties": False,
    }


# ---------------------------------------------------------------------------
# OpenAI call
# ---------------------------------------------------------------------------

async def profile_row(client, model, system_prompt, schema, user_message):
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "facets",
                "schema": schema,
                "strict": True,
            },
        },
    )
    return json.loads(response.choices[0].message.content)


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def write_output(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    tmp.replace(path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def run(args) -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not set", file=sys.stderr)
        return 1
    client = AsyncOpenAI()

    input_path = args.input or DEFAULT_INPUTS[args.mode]
    output_path = args.output or DEFAULT_OUTPUTS[args.mode]
    id_col = ID_COLUMN[args.mode]

    if not input_path.exists():
        print(f"input not found: {input_path}", file=sys.stderr)
        return 1

    with open(input_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        in_fields = list(reader.fieldnames or [])
        rows = list(reader)

    extra_cols = NEW_FACET_COLUMNS.copy()
    if args.mode == "projects":
        extra_cols = ["climate_relevance"] + extra_cols
    out_fields = in_fields + [c for c in extra_cols if c not in in_fields]

    # Resume from existing output if present
    if output_path.exists() and not args.refresh:
        with open(output_path, encoding="utf-8-sig", newline="") as f:
            existing = {r[id_col]: r for r in csv.DictReader(f)}
        for r in rows:
            cached = existing.get(r[id_col])
            if cached and (cached.get("primary_outcome") or "").strip():
                for c in extra_cols:
                    r[c] = cached.get(c, "")

    todo = [r for r in rows if not (r.get("primary_outcome") or "").strip()]
    if args.limit is not None:
        todo = todo[:args.limit]

    print(f"input:  {input_path}")
    print(f"output: {output_path}")
    print(f"total rows: {len(rows)}  already profiled: {len(rows) - len(todo)}  "
          f"to do this run: {len(todo)}")

    if not todo:
        write_output(output_path, out_fields, rows)
        print("Nothing to profile.")
        return 0

    # In projects mode, load the translated table once and use it to enrich
    # each project's user message with the richer per-etapa narrative.
    if args.mode == "projects":
        translated = load_translated_narrative(TRANSLATED_TABLE)
        joined = sum(1 for r in rows
                     if (r.get("codigo_bip") or "").strip() in translated)
        print(f"translated narrative joined for {joined}/{len(rows)} projects "
              f"(from {TRANSLATED_TABLE.name})")
        msg_fn = lambda r: project_user_message(r, translated)
    else:
        msg_fn = action_user_message

    # Rough cost estimate (gpt-4o-mini pricing)
    system_prompt = SHARED_SYSTEM_PROMPT + (PROJECT_EXTRA_PROMPT if args.mode == "projects" else "")
    sys_tokens = len(system_prompt) * 0.3
    sample_in = sum(len(msg_fn(r)) for r in todo[:min(20, len(todo))]) / max(1, min(20, len(todo)))
    est_in = (sys_tokens + sample_in * 0.3) * len(todo)
    est_out = 200 * len(todo)
    print(f"estimated cost ({args.model}): "
          f"${est_in / 1_000_000 * 0.150 + est_out / 1_000_000 * 0.600:.2f}")

    schema = make_schema(args.mode)
    sem = asyncio.Semaphore(args.concurrency)
    interrupted = {"flag": False}

    def on_int(sig, frame):
        interrupted["flag"] = True
        print("\nInterrupt — finishing in-flight, then saving.")
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
                result = await profile_row(client, args.model, system_prompt,
                                           schema, msg_fn(row))
                for k, v in result.items():
                    row[k] = "" if v is None else v
            except Exception as e:
                print(f"  FAILED {row.get(id_col)}: {e}", file=sys.stderr)
                row["primary_outcome"] = ""
                row["reasoning"] = f"[error] {str(e)[:160]}"
        done += 1
        if done % args.save_every == 0:
            async with save_lock:
                write_output(output_path, out_fields, rows)
                elapsed = time.time() - t0
                rate = done / max(elapsed, 0.001)
                remaining = len(todo) - done
                eta_min = remaining / max(rate, 0.001) / 60
                print(f"  [{done}/{len(todo)}]  {rate:.1f}/s  ETA {eta_min:.1f}min")

    await asyncio.gather(*[worker(r) for r in todo])
    write_output(output_path, out_fields, rows)
    print(f"\nDone. wrote {output_path}")
    return 0 if not interrupted["flag"] else 130


def main():
    load_dotenv_release(ROOT / ".env")
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", required=True, choices=["actions", "projects"],
                    help="Profile the action library or the projects table.")
    ap.add_argument("--input", type=Path, default=None,
                    help="Override input CSV path.")
    ap.add_argument("--output", type=Path, default=None,
                    help="Override output CSV path.")
    ap.add_argument("--model", default="gpt-4o-mini",
                    help="OpenAI model (default: gpt-4o-mini).")
    ap.add_argument("--concurrency", type=int, default=8,
                    help="Concurrent API calls (default: 8).")
    ap.add_argument("--save-every", type=int, default=20,
                    help="Save output every N completions (default: 20).")
    ap.add_argument("--limit", type=int, default=None,
                    help="Profile at most N rows (smoke test).")
    ap.add_argument("--refresh", action="store_true",
                    help="Re-profile all rows, ignoring cached output.")
    args = ap.parse_args()
    sys.exit(asyncio.run(run(args)))


if __name__ == "__main__":
    main()
