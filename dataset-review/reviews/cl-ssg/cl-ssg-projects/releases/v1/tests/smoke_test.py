"""
Smoke test for the FICHA IDI extraction pipeline.

What this script does
---------------------
1.  Loads ficha_idi.schema.v1.0.0.json and validates every parsed JSON in the
    --json-dir against it.
2.  Computes content-quality metrics across the corpus:
       - schema pass / fail rate
       - top 5 failure patterns (path + message)
       - per-template-variant counts (PROYECTO / PROGRAMA / STUB / ESTUDIO_BASICO)
       - per-sector counts
       - parser_version distribution (catches stale outputs)
       - rate at which key fields are populated:
            iniciativa.nombre, sector, ubicacion.tipo,
            solicitud_financiamiento.rows, programacion_inversion.aportes_directos,
            resumen_resultados.indicadores.componentes,
            resumen_resultados.indicadores.indicadores_proposito,
            funcionario_responsable
       - warning counts (multi_etapa_identical_blocks, nombre_extraction_failed)
3.  Optionally compares the metrics to a JSON baseline (--baseline) and flags
    regressions (any metric that got measurably worse).
4.  Exits 0 on success, 1 if any schema failures, 2 if --baseline is given and
    a regression is detected. Suitable as a pre-commit / CI gate.

Usage
-----
    # Default — validate the standard corpus/parsed directory
    python tests/smoke_test.py

    # Custom location
    python tests/smoke_test.py --json-dir corpus/parsed

    # Save current metrics as the baseline for future regression checks
    python tests/smoke_test.py --save-baseline tests/baseline.json

    # Run with regression check
    python tests/smoke_test.py --baseline tests/baseline.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable

DEFAULT_SCHEMA = Path(__file__).resolve().parent.parent / "schemas" / "ficha_idi.schema.v1.0.0.json"
DEFAULT_JSON_DIR = Path(__file__).resolve().parent.parent / "corpus" / "parsed"

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
DIM = "\033[2m"
BOLD = "\033[1m"
END = "\033[0m"


# ---------------------------------------------------------------------------
# Worker: validate one file and extract its metric contributions
# ---------------------------------------------------------------------------

def _check_file(args) -> dict:
    path_str, schema = args
    from jsonschema import Draft202012Validator
    v = Draft202012Validator(schema)
    out = {
        "path": path_str,
        "errors": [],
        "metrics": {},
    }
    try:
        d = json.loads(Path(path_str).read_text())
    except Exception as e:
        out["errors"].append({"key": "<json_load>", "message": str(e)[:160]})
        return out

    for e in v.iter_errors(d):
        out["errors"].append({
            "key": "/".join(str(x) for x in e.absolute_path) or "<root>",
            "message": e.message[:200],
        })

    # Collect everything we care about for the per-corpus rollup.
    parser_version = d.get("extraction", {}).get("parser_version")
    template_variant = d.get("document", {}).get("template_variant")
    template_version = d.get("document", {}).get("template_version")
    n_etapas = d.get("document", {}).get("n_etapas_in_pdf", 0)
    warnings = [w["code"] for w in d.get("extraction", {}).get("warnings", [])]
    filename = d.get("extraction", {}).get("source_pdf", {}).get("filename") or ""
    sector = filename.split("_")[0] if "_" in filename else ""
    if sector and not Path(path_str).name.startswith(sector):
        # Files in corpus/parsed/ are named '<sector>__<basename>.json'
        sector = Path(path_str).name.split("__")[0]

    etapa_metrics = []
    for e in d.get("etapas", []):
        ini = e.get("iniciativa") or {}
        clas = e.get("clasificacion") or {}
        ubic = e.get("ubicacion") or {}
        sf = (e.get("solicitud_financiamiento") or {}).get("rows") or []
        ad = (e.get("programacion_inversion") or {}).get("aportes_directos") or []
        rr = e.get("resumen_resultados") or {}
        ind = (rr.get("indicadores") or {})
        etapa_metrics.append({
            "nombre": bool(ini.get("nombre")),
            "sector": bool(clas.get("sector")),
            "ubicacion_tipo": bool(ubic.get("tipo")),
            "fin_rows": len(sf),
            "aportes_directos": len(ad),
            "componentes": bool(ind.get("componentes")),
            "indicadores_proposito": bool(ind.get("indicadores_proposito")),
            "funcionario": bool(e.get("funcionario_responsable")),
        })

    out["metrics"] = {
        "parser_version": parser_version,
        "template_variant": template_variant,
        "template_version": template_version,
        "n_etapas": n_etapas,
        "warnings": warnings,
        "sector": sector,
        "etapa_metrics": etapa_metrics,
    }
    return out


# ---------------------------------------------------------------------------
# Aggregator
# ---------------------------------------------------------------------------

def aggregate(results: Iterable[dict]) -> dict:
    n_files = 0
    n_valid = 0
    n_invalid = 0
    err_pattern = Counter()
    err_examples: dict[tuple, str] = {}
    parser_versions = Counter()
    template_variants = Counter()
    template_versions = Counter()
    sectors = Counter()
    warning_counts = Counter()
    n_etapas = 0
    etapa_pop = Counter()  # etapa-level "populated" tallies

    for r in results:
        n_files += 1
        if r["errors"]:
            n_invalid += 1
            for e in r["errors"][:1]:
                key = (e["key"], e["message"])
                err_pattern[key] += 1
                err_examples.setdefault(key, Path(r["path"]).name)
        else:
            n_valid += 1
        m = r.get("metrics") or {}
        parser_versions[m.get("parser_version")] += 1
        template_variants[m.get("template_variant")] += 1
        template_versions[m.get("template_version")] += 1
        sectors[m.get("sector") or "<unknown>"] += 1
        for w in m.get("warnings", []):
            warning_counts[w] += 1
        for em in m.get("etapa_metrics", []):
            n_etapas += 1
            for k in ("nombre", "sector", "ubicacion_tipo", "componentes",
                      "indicadores_proposito", "funcionario"):
                if em.get(k):
                    etapa_pop[k] += 1
            if em.get("fin_rows", 0) > 0:
                etapa_pop["any_financing_row"] += 1
            if em.get("aportes_directos", 0) > 0:
                etapa_pop["any_aporte_directo"] += 1

    return {
        "n_files": n_files,
        "n_valid": n_valid,
        "n_invalid": n_invalid,
        "err_pattern_top": [
            {"path": k[0], "message": k[1], "count": c, "example": err_examples[k]}
            for k, c in err_pattern.most_common(5)
        ],
        "parser_versions": dict(parser_versions),
        "template_variants": dict(template_variants),
        "template_versions": dict(template_versions),
        "sectors": dict(sectors),
        "warnings": dict(warning_counts),
        "n_etapas": n_etapas,
        "etapa_populated": dict(etapa_pop),
    }


# ---------------------------------------------------------------------------
# Pretty-printer
# ---------------------------------------------------------------------------

def fmt_pct(num: int, denom: int) -> str:
    if denom == 0:
        return "—"
    return f"{100*num/denom:5.1f}%"


def print_report(metrics: dict, color: bool = True) -> None:
    def C(s, code): return f"{code}{s}{END}" if color else s

    n = metrics["n_files"]
    print(C(f"\n=== FICHA IDI smoke test — {n} JSON files ===\n", BOLD))

    pass_pct = 100 * metrics["n_valid"] / n if n else 0
    pass_color = GREEN if pass_pct == 100 else (YELLOW if pass_pct >= 99 else RED)
    fraction = f"{metrics['n_valid']}/{n}"
    print(f"schema validation: {C(fraction, pass_color)} ({pass_pct:.2f}% pass)")
    if metrics["n_invalid"]:
        print(C(f"  ⚠  {metrics['n_invalid']} files failed validation", YELLOW))
        for e in metrics["err_pattern_top"]:
            print(f"     {e['count']:4d}×  {e['path']}: {e['message'][:80]}")
            print(f"           example → {e['example']}")

    print()
    print(C("parser version distribution:", BOLD))
    for v, c in sorted(metrics["parser_versions"].items(), key=lambda kv: -kv[1]):
        print(f"  {v or '<missing>':35s} {c}")

    print()
    print(C("template variants:", BOLD))
    for v, c in sorted(metrics["template_variants"].items(), key=lambda kv: -kv[1]):
        print(f"  {v or '<missing>':25s} {c}")

    print()
    print(C("template versions:", BOLD))
    for v, c in sorted(metrics["template_versions"].items(), key=lambda kv: -kv[1]):
        print(f"  {v or '<missing>':25s} {c}")

    print()
    print(C("sector breakdown:", BOLD))
    for s, c in sorted(metrics["sectors"].items(), key=lambda kv: -kv[1]):
        print(f"  {s:25s} {c}")

    n_etapas = metrics["n_etapas"]
    print()
    print(C(f"etapa-level field population ({n_etapas} etapas):", BOLD))
    pop = metrics["etapa_populated"]
    rows = [
        ("iniciativa.nombre",                     pop.get("nombre", 0)),
        ("clasificacion.sector",                  pop.get("sector", 0)),
        ("ubicacion.tipo",                        pop.get("ubicacion_tipo", 0)),
        ("solicitud_financiamiento.rows ≥ 1",     pop.get("any_financing_row", 0)),
        ("programacion_inversion.aportes_directos ≥ 1",
                                                 pop.get("any_aporte_directo", 0)),
        ("resumen.indicadores.componentes",       pop.get("componentes", 0)),
        ("resumen.indicadores.indicadores_proposito",
                                                 pop.get("indicadores_proposito", 0)),
        ("funcionario_responsable",               pop.get("funcionario", 0)),
    ]
    for label, count in rows:
        print(f"  {label:48s} {count:5d}  ({fmt_pct(count, n_etapas)})")

    print()
    print(C("warnings emitted:", BOLD))
    if not metrics["warnings"]:
        print("  (none)")
    else:
        for w, c in sorted(metrics["warnings"].items(), key=lambda kv: -kv[1]):
            print(f"  {w:40s} {c}")
    print()


# ---------------------------------------------------------------------------
# Baseline / regression detection
# ---------------------------------------------------------------------------

CRITICAL_KEYS = {
    "n_valid",
    "etapa_populated.nombre",
    "etapa_populated.sector",
    "etapa_populated.ubicacion_tipo",
    "etapa_populated.any_financing_row",
    "etapa_populated.any_aporte_directo",
    "etapa_populated.componentes",
    "etapa_populated.indicadores_proposito",
    "etapa_populated.funcionario",
}


def _flatten(d: dict, prefix: str = "") -> dict:
    out = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(_flatten(v, key))
        elif isinstance(v, (int, float)):
            out[key] = v
    return out


def diff_against_baseline(current: dict, baseline: dict) -> list[str]:
    cur_flat = _flatten(current)
    base_flat = _flatten(baseline)
    regressions = []
    for k in CRITICAL_KEYS:
        c = cur_flat.get(k, 0)
        b = base_flat.get(k, 0)
        if c < b:
            regressions.append(f"REGRESSION  {k}: {b} → {c}  ({c - b:+d})")
        elif c > b:
            regressions.append(f"improved    {k}: {b} → {c}  ({c - b:+d})")
    # Schema invalid regression: increase is bad
    c_inv = cur_flat.get("n_invalid", 0)
    b_inv = base_flat.get("n_invalid", 0)
    if c_inv > b_inv:
        regressions.append(f"REGRESSION  n_invalid: {b_inv} → {c_inv}  ({c_inv - b_inv:+d})")
    return regressions


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json-dir", type=Path, default=DEFAULT_JSON_DIR,
                    help=f"Directory of parsed JSON files (default: {DEFAULT_JSON_DIR})")
    ap.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA,
                    help=f"Path to JSON Schema (default: {DEFAULT_SCHEMA})")
    ap.add_argument("--processes", type=int, default=8)
    ap.add_argument("--baseline", type=Path, default=None,
                    help="Path to baseline metrics JSON; flag regressions against it.")
    ap.add_argument("--save-baseline", type=Path, default=None,
                    help="Save current metrics to this path (for future --baseline runs).")
    ap.add_argument("--no-color", action="store_true")
    ap.add_argument("--metrics-out", type=Path, default=None,
                    help="Optional path to write the full metrics dict as JSON.")
    args = ap.parse_args()

    if not args.schema.exists():
        print(f"ERROR: schema not found: {args.schema}", file=sys.stderr)
        return 1
    if not args.json_dir.exists():
        print(f"ERROR: json dir not found: {args.json_dir}", file=sys.stderr)
        return 1

    schema = json.loads(args.schema.read_text())
    paths = sorted(str(p) for p in args.json_dir.glob("*.json"))
    if not paths:
        print(f"ERROR: no JSON files found in {args.json_dir}", file=sys.stderr)
        return 1

    print(f"Validating {len(paths)} files against {args.schema.name}…")
    work = [(p, schema) for p in paths]
    results: list[dict] = []
    with ProcessPoolExecutor(max_workers=args.processes) as ex:
        for r in ex.map(_check_file, work, chunksize=20):
            results.append(r)

    metrics = aggregate(results)
    print_report(metrics, color=not args.no_color)

    if args.metrics_out:
        args.metrics_out.write_text(json.dumps(metrics, indent=2))
        print(f"metrics written to {args.metrics_out}")

    if args.save_baseline:
        args.save_baseline.parent.mkdir(parents=True, exist_ok=True)
        args.save_baseline.write_text(json.dumps(metrics, indent=2))
        print(f"baseline saved to {args.save_baseline}")

    rc = 0
    if metrics["n_invalid"] > 0:
        rc = 1
        print(f"FAIL  schema-invalid files: {metrics['n_invalid']}", file=sys.stderr)

    if args.baseline and args.baseline.exists():
        baseline = json.loads(args.baseline.read_text())
        diffs = diff_against_baseline(metrics, baseline)
        print(f"\n=== regression check vs {args.baseline.name} ===")
        if not diffs:
            print("  metrics unchanged.")
        else:
            for d in diffs:
                print(f"  {d}")
        if any(d.startswith("REGRESSION") for d in diffs):
            rc = max(rc, 2)
            print("FAIL  regression vs baseline", file=sys.stderr)

    if rc == 0:
        ok = f"{GREEN}OK{END}" if not args.no_color else "OK"
        print(f"\n{ok}  all checks passed.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
