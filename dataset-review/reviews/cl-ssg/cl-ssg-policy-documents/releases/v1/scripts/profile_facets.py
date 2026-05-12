"""
Profile climate actions or policy signals with structured outcome + intervention facets.

Calls OpenAI with structured JSON output (enforced schema) to assign:
- primary_outcome, secondary_outcome (controlled vocab, multi-value)
- primary_intervention, secondary_intervention (controlled vocab)
- climate_relevance (signals mode only, 5 values)
- confidence (high/medium/low) + reasoning

Modes
-----
    python scripts/profile_facets.py --mode actions
    python scripts/profile_facets.py --mode signals

Inputs (defaults)
-----------------
    actions  -> data/input/actions.json
    signals  -> data/summaries/   (directory — one JSON per document)

Environment
-------------
    ``OPENAI_API_KEY`` is required. If unset, the script loads ``.env`` at the
    release root (``v1/.env``) when present; existing environment variables
    are not overwritten.

Outputs
-------
    actions  -> data/derived/actions_profiled.csv
    signals  -> data/derived/signals_profiled.csv

Each output CSV contains the original columns plus:
    primary_outcome, secondary_outcome,
    primary_intervention, secondary_intervention,
    confidence, reasoning,
    (climate_relevance for signals only)

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
from pathlib import Path

try:
    from openai import AsyncOpenAI
except ImportError:
    print("openai not installed. Install with: pip install openai>=1.82.0",
          file=sys.stderr)
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
INPUTS = ROOT / "data" / "input"
DERIVED = ROOT / "data" / "derived"
SUMMARIES = ROOT / "data" / "summaries"
ATOMS = ROOT / "data" / "atoms"

DEFAULT_INPUTS: dict[str, Path] = {
    "actions": INPUTS / "actions.json",
    "signals": SUMMARIES,
}
DEFAULT_OUTPUTS = {
    "actions": DERIVED / "actions_profiled.csv",
    "signals": DERIVED / "signals_profiled.csv",
}

ID_COLUMN = {
    "actions": "action_id",
    "signals": "policy_signal_id",
}

NEW_FACET_COLUMNS = [
    "primary_outcome",
    "secondary_outcome",
    "primary_intervention",
    "secondary_intervention",
    "confidence",
    "reasoning",
]

_ATOM_BY_ID_CACHE: dict[str, dict] | None = None


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

SIGNAL_EXTRA_PROMPT = """

SIGNAL MODE — Additional facet:

climate_relevance (pick exact string):
- mitigation: signal's primary climate framing is emissions reduction
  or sequestration. Use for sector priorities, named measures,
  quantified targets, and funding pathways framed around mitigation.
- adaptation: signal's primary climate framing is resilience or
  hazard adaptation. PARCC signals are often adaptation-led.
- mixed: signal substantively covers both mitigation and adaptation
  distinctly.
- unclear: signal is climate-related but the framing is too generic
  to classify (e.g. broad reference to "cambio climático" without
  further specificity).
- not_climate: signal doesn't appear to be a climate signal at all
  (territorial planning signals can sometimes be borderline).

When climate_relevance is mitigation/adaptation, primary_outcome
MUST be from the corresponding family. When mixed, primary_outcome
is the more prominent component and secondary the other family.
When unclear, classify best-guess and mark confidence=low.
When not_climate, set primary_outcome=null and primary_intervention=null.

Signal-specific guidance:
- Signals with signal_type=sector or sector_priority typically map
  to outcome=enabling unless they explicitly name a measure.
- Signals with signal_type=target should map to outcome based on
  what's being targeted (emissions, resilience, etc.).
- Signals with signal_type=funding typically map to
  intervention=financial.
- Signals with signal_type=governance typically map to
  intervention=planning or regulatory.
- National framework signals (NDC, ECLP) often legitimately map to
  outcome=enabling — they set the stage rather than commit to specific
  physical actions.
"""


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_actions_json(path: Path) -> list[dict]:
    """Read actions.json and return flattened row dicts for profiling."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError(f"actions.json must be a JSON array, got {type(raw)}")
    rows: list[dict] = []
    for obj in raw:
        if not isinstance(obj, dict):
            continue
        em = obj.get("emissions") or {}
        if not isinstance(em, dict):
            em = {}
        gpc_list = em.get("gpc_reference_number") or []
        if isinstance(gpc_list, list):
            gpc_str = "; ".join(str(x) for x in gpc_list)
        else:
            gpc_str = str(gpc_list) if gpc_list else ""
        subn = em.get("subsector_number", "")
        secn = em.get("sector_number", "")
        rows.append(
            {
                "action_id": str(obj.get("actionId", "") or ""),
                "action_name": str(obj.get("actionName", "") or ""),
                "description": str(obj.get("description", "") or ""),
                "intervention_summary": str(obj.get("intervention_summary") or ""),
                "outcome_summary": str(obj.get("outcome_summary") or ""),
                "intervention_type_input": str(obj.get("intervention_type") or ""),
                "action_role": str(obj.get("action_role") or ""),
                "subsector_number": "" if subn is None else str(subn),
                "sector_number": "" if secn is None else str(secn),
                "gpc_reference": gpc_str,
            }
        )
    return rows


def load_atom_by_id(atoms_dir: Path, *, use_cache: bool = True) -> dict[str, dict]:
    """Build atom_id -> atom dict from all v1/data/atoms/*.jsonl."""
    global _ATOM_BY_ID_CACHE
    if use_cache and _ATOM_BY_ID_CACHE is not None:
        return _ATOM_BY_ID_CACHE
    m: dict[str, dict] = {}
    if not atoms_dir.is_dir():
        _ATOM_BY_ID_CACHE = m
        return m
    for p in sorted(atoms_dir.glob("*.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                a = json.loads(line)
            except json.JSONDecodeError:
                continue
            aid = a.get("atom_id")
            if aid:
                m[str(aid)] = a
    if use_cache:
        _ATOM_BY_ID_CACHE = m
    return m


def load_signal_rows_from_summaries(summaries_dir: Path) -> list[dict]:
    """Walk summaries/*.json and emit one row per policy_signals[] entry."""
    rows: list[dict] = []
    if not summaries_dir.is_dir():
        return rows
    for path in sorted(summaries_dir.glob("*.json")):
        if path.name.endswith(".run.json"):
            continue
        try:
            summary = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(summary, dict):
            continue
        signals = summary.get("policy_signals") or []
        if not isinstance(signals, list):
            continue
        sid = str(summary.get("source_document_id", "") or "")
        sname = str(summary.get("source_name", "") or "")
        slevel = str(summary.get("source_level", "") or "")
        rcode = str(summary.get("region_code", "") or "")
        ccode = str(summary.get("communal_code", "") or "")
        dtype = str(summary.get("document_type", "") or "")
        for sig in signals:
            if not isinstance(sig, dict):
                continue
            aids = sig.get("supporting_atom_ids") or []
            if isinstance(aids, list):
                aids_joined = ";".join(str(x) for x in aids)
            else:
                aids_joined = str(aids) if aids else ""
            rows.append(
                {
                    "policy_signal_id": str(sig.get("policy_signal_id", "") or ""),
                    "source_document_id": sid,
                    "source_name": sname,
                    "source_level": slevel,
                    "region_code": rcode,
                    "communal_code": ccode,
                    "signal_type": str(sig.get("signal_type", "") or ""),
                    "signal_code": str(sig.get("signal_code") or ""),
                    "signal_label": str(sig.get("signal_label", "") or ""),
                    "actor_level": str(sig.get("actor_level", "") or ""),
                    "supporting_atom_ids": aids_joined,
                    "document_type": dtype,
                }
            )
    return rows


def load_rows_actions_mode(input_path: Path) -> tuple[list[dict], list[str]]:
    """Load action rows from JSON or CSV; return (rows, base_fieldnames order)."""
    suffix = input_path.suffix.lower()
    if suffix == ".json":
        rows = load_actions_json(input_path)
        if not rows:
            return [], []
        base_fields = list(rows[0].keys())
        return rows, base_fields
    with open(input_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        in_fields = list(reader.fieldnames or [])
        rows = list(reader)
    return rows, in_fields


# ---------------------------------------------------------------------------
# Message construction
# ---------------------------------------------------------------------------

def action_user_message(row: dict) -> str:
    return (
        f"Action ID: {row.get('action_id', '')}\n"
        f"Action name: {row.get('action_name', '')}\n"
        f"GPC subsector: {row.get('subsector_number', '')} ({row.get('gpc_reference', '')})\n"
        f"Intervention type (input): {row.get('intervention_type_input', '')}\n"
        f"Action role: {row.get('action_role', '')}\n"
        f"Description: {row.get('description', '')}\n"
        f"Outcome summary: {row.get('outcome_summary', '')}\n"
    )


def signal_user_message(row: dict, atom_by_id: dict[str, dict]) -> str:
    ev: list[str] = []
    raw_ids = row.get("supporting_atom_ids") or ""
    for aid in str(raw_ids).split(";"):
        aid = aid.strip()
        if not aid:
            continue
        a = atom_by_id.get(aid)
        if not a:
            continue
        pref = a.get("page_reference", "") or "?"
        etext = str(a.get("evidence_text", "") or "")[:400]
        ev.append(f"  [p. {pref}] {etext}")
        if len(ev) >= 3:
            break
    ev_block = "\n".join(ev) if ev else "  (no matching atoms in lookup)"
    return (
        f"Policy signal ID: {row.get('policy_signal_id', '')}\n"
        f"Source document: {row.get('source_document_id', '')} ({row.get('document_type', '')})\n"
        f"Actor level: {row.get('actor_level', '')}\n"
        f"Signal type: {row.get('signal_type', '')}\n"
        f"Signal code: {row.get('signal_code', '')}\n"
        f"Signal label: {row.get('signal_label', '')}\n"
        f"\nSupporting evidence (verbatim from policy document):\n"
        f"{ev_block}\n"
    )


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
    if mode == "signals":
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

    atom_by_id: dict[str, dict] = {}
    if args.mode == "signals":
        if not input_path.exists():
            print(f"input not found: {input_path}", file=sys.stderr)
            return 1
        if not input_path.is_dir():
            print(f"signals mode expects summaries directory: {input_path}", file=sys.stderr)
            return 1
        rows = load_signal_rows_from_summaries(input_path)
        atom_by_id = load_atom_by_id(ATOMS, use_cache=True)
        base_fields = [
            "policy_signal_id",
            "source_document_id",
            "source_name",
            "source_level",
            "region_code",
            "communal_code",
            "signal_type",
            "signal_code",
            "signal_label",
            "actor_level",
            "supporting_atom_ids",
            "document_type",
        ]
        if not rows:
            print("No policy_signals found in any summary JSON (nothing to profile).")
            extra_cols = NEW_FACET_COLUMNS.copy()
            extra_cols = ["climate_relevance"] + extra_cols
            out_fields = base_fields + [c for c in extra_cols if c not in base_fields]
            write_output(output_path, out_fields, rows)
            return 0
    else:
        if not input_path.exists():
            print(f"input not found: {input_path}", file=sys.stderr)
            return 1
        rows, in_fields = load_rows_actions_mode(input_path)
        if not rows:
            print("No rows in input.", file=sys.stderr)
            return 1
        base_fields = in_fields

    extra_cols = NEW_FACET_COLUMNS.copy()
    if args.mode == "signals":
        extra_cols = ["climate_relevance"] + extra_cols
    out_fields = list(base_fields) + [c for c in extra_cols if c not in base_fields]

    for r in rows:
        for c in extra_cols:
            r.setdefault(c, "")

    # Resume from existing output if present
    if output_path.exists() and not args.refresh:
        with open(output_path, encoding="utf-8-sig", newline="") as f:
            existing = {r[id_col]: r for r in csv.DictReader(f)}
        for r in rows:
            cached = existing.get(r.get(id_col, ""))
            if cached and (cached.get("primary_outcome") or "").strip():
                for c in extra_cols:
                    r[c] = cached.get(c, "")

    todo = [r for r in rows if not (r.get("primary_outcome") or "").strip()]
    if args.limit is not None:
        todo = todo[: args.limit]

    print(f"input:  {input_path}")
    print(f"output: {output_path}")
    print(f"total rows: {len(rows)}  already profiled: {len(rows) - len(todo)}  "
          f"to do this run: {len(todo)}")

    if not todo:
        write_output(output_path, out_fields, rows)
        print("Nothing to profile.")
        return 0

    if args.mode == "signals":
        msg_fn = lambda r: signal_user_message(r, atom_by_id)
        def _has_resolved_atom(r: dict) -> bool:
            for part in str(r.get("supporting_atom_ids", "")).split(";"):
                aid = part.strip()
                if aid and aid in atom_by_id:
                    return True
            return False

        joined = sum(1 for r in todo if _has_resolved_atom(r))
        print(f"signals with ≥1 resolved atom in lookup: {joined}/{len(todo)}")
    else:
        msg_fn = action_user_message

    system_prompt = SHARED_SYSTEM_PROMPT + (SIGNAL_EXTRA_PROMPT if args.mode == "signals" else "")

    # Rough cost estimate (gpt-4o-mini pricing)
    sys_tokens = len(system_prompt) * 0.3
    sample_in = sum(len(msg_fn(r)) for r in todo[: min(20, len(todo))]) / max(1, min(20, len(todo)))
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
    ap.add_argument("--mode", required=True, choices=["actions", "signals"],
                    help="Profile the action library or policy signals from summaries.")
    ap.add_argument("--input", type=Path, default=None,
                    help="Override input path (CSV/JSON for actions; directory for signals).")
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
