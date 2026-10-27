# NOTE: ``bip_database.csv`` is an external manual-labeling dependency and is
# intentionally not tracked in this repository.
"""
Rebuild utility (optional): one row per climate-relevant project
(``codigo_bip``), joining ``bip_database.csv`` (manual climate flag + comment)
with ``data/derived/ficha_idi_table.csv`` (rich extracted FICHA fields).

The canonical projects table used by the rest of the release is
``data/inputs/projects.csv`` — externally sourced, not produced by this
pipeline. Run this script only when you need to regenerate from
``bip_database.csv``; it is not part of the regular pipeline.

Output: ``releases/v1/data/derived/projects_rebuilt.csv``

Conventions
-----------
- One row per ``codigo_bip``. When multiple etapas exist for the same project,
  we keep the *latest* (highest ``proceso_presupuestario``) etapa's fields.
- ``codigo_bip`` is normalised to ``"<numeric>-<suffix>"``. ``bip_database``
  has just the numeric part — we add ``-0`` if no suffix is present.
- Projects flagged in ``bip_database`` but missing from ``ficha_idi_table``
  (the PDF is not in our parsed sample) get ``has_ficha_data = False``. They
  carry the bip_database fields only — no narrative, no extracted budget.
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
INPUTS = DATA / "inputs"
DERIVED = DATA / "derived"
DB = INPUTS / "bip_database.csv"
FT = DERIVED / "ficha_idi_table.csv"
OUT = DERIVED / "projects_rebuilt.csv"


def numeric(s: str | None) -> str:
    if not s:
        return ""
    m = re.match(r"(\d+)", str(s))
    return m.group(1) if m else ""


def normalise_bip(s: str | None) -> str:
    n = numeric(s)
    if not n:
        return ""
    if "-" in str(s):
        return str(s)
    return f"{n}-0"


def main():
    if not DB.exists():
        print(
            "bip_database.csv not found. This file is the manual climate-relevance "
            "labeling input and is not tracked in the repo. Either provide it or "
            "skip this step — data/inputs/projects.csv may already exist from an external source."
        )
        raise SystemExit(1)

    db_rows = list(csv.DictReader(open(DB, newline="")))
    ft_rows = list(csv.DictReader(open(FT, newline="")))

    # Group ficha rows by numeric codigo_bip; pick latest etapa per project.
    by_code: dict[str, list[dict]] = defaultdict(list)
    for r in ft_rows:
        by_code[numeric(r["codigo_bip"])].append(r)

    def pick_latest(rows: list[dict]) -> dict:
        def year(r):
            try:
                return int(r.get("proceso_presupuestario") or 0)
            except (ValueError, TypeError):
                return 0
        # Prefer non-stub, non-duplicate, latest year
        rows = sorted(
            rows,
            key=lambda r: (
                r.get("template_variant") != "STUB",
                r.get("multi_etapa_duplicate") != "True",
                year(r),
            ),
            reverse=True,
        )
        return rows[0]

    out_cols = [
        # ----- identity -----
        "codigo_bip",                     # canonical "<num>-<suffix>"
        "codigo_bip_numeric",             # just the numeric part
        "nombre",                         # project name (from FICHA when available, else bip_database DESCRIPCIÓN)
        "tipologia",                      # PROYECTO / PROGRAMA / ESTUDIO BÁSICO
        "descriptor",
        # ----- status / lifecycle -----
        "etapa_actual",
        "rate_resultado",
        "ano_postulacion",                # latest budget year on record
        "n_etapas_total",                 # how many etapas the project went through
        # ----- classification -----
        "sector",
        "subsector",
        "sector_en",                      # joined from gpc_mapping later
        "subsector_en",
        # ----- location -----
        "region",
        "comuna",
        "provincia",
        "ubicacion_tipo",
        "ubicacion_nombre",
        # ----- narrative (the matching corpus) -----
        "justificacion",
        "descripcion_etapa",
        "componentes_text",
        "proposito",
        # ----- finance -----
        "costo_total_M_CLP",
        "costo_total_USD",
        "duracion_meses",
        "fuentes_financiamiento",
        "institucion_formuladora",
        # ----- contact -----
        "funcionario_correo",
        # ----- climate flagging (from bip_database) -----
        "is_climate_relevant",
        "climate_classification_es",
        # ----- data quality -----
        "has_ficha_data",                 # False when project flagged in bip_database but no parsed JSON
        "source_pdf_filename",
    ]

    rows_out = []
    for db in db_rows:
        num = numeric(db["CÓDIGO BIP"])
        if not num:
            continue
        ft_candidates = by_code.get(num, [])
        has_ficha = bool(ft_candidates)
        ft = pick_latest(ft_candidates) if has_ficha else {}

        # --- IDs ---
        codigo = ft.get("codigo_bip") or f"{num}-0"

        # --- name: prefer FICHA, fall back to bip_database DESCRIPCIÓN ---
        nombre = ft.get("nombre") or (db.get("DESCRIPCIÓN", "").split(" Año y Etapa")[0]).strip()

        # --- year ---
        ano = ft.get("proceso_presupuestario") or db.get("AÑO POSTULACIÓN", "")

        # --- sector/subsector: prefer FICHA (already parsed), fall back to bip_database raw ---
        sector = ft.get("sector") or db.get("SECTOR", "")
        subsector = ft.get("subsector") or db.get("SUB SECTOR", "")

        rows_out.append({
            "codigo_bip":             codigo,
            "codigo_bip_numeric":     num,
            "nombre":                 nombre,
            "tipologia":              ft.get("tipologia") or db.get("TIPOLOGÍA", ""),
            "descriptor":             ft.get("descriptor", ""),
            "etapa_actual":           ft.get("etapa_actual") or db.get("ETAPA ACTUAL", ""),
            "rate_resultado":         ft.get("rate_resultado") or db.get("RATE", ""),
            "ano_postulacion":        ano,
            "n_etapas_total":         len(ft_candidates),
            "sector":                 sector,
            "subsector":              subsector,
            "sector_en":              "",  # filled later from gpc_mapping
            "subsector_en":           "",
            "region":                 ft.get("region", ""),
            "comuna":                 ft.get("comuna", ""),
            "provincia":              ft.get("provincia", ""),
            "ubicacion_tipo":         ft.get("ubicacion_tipo", ""),
            "ubicacion_nombre":       ft.get("ubicacion_nombre", ""),
            "justificacion":          ft.get("justificacion", ""),
            "descripcion_etapa":      ft.get("descripcion_etapa", ""),
            "componentes_text":       ft.get("componentes_text", ""),
            "proposito":              ft.get("proposito", ""),
            "costo_total_M_CLP":      ft.get("costo_total_M_CLP", ""),
            "costo_total_USD":        ft.get("costo_total_USD", ""),
            "duracion_meses":         ft.get("duracion_meses", ""),
            "fuentes_financiamiento": ft.get("fuentes_financiamiento", ""),
            "institucion_formuladora": ft.get("institucion_formuladora", "") or db.get("INSTITUCIÓN FORMULADORA", ""),
            "funcionario_correo":     ft.get("funcionario_correo", ""),
            "is_climate_relevant":    db.get("considerar_en_bd_climatica", "").upper() == "SI",
            "climate_classification_es": db.get("comentario_clasificacion", ""),
            "has_ficha_data":         has_ficha,
            "source_pdf_filename":    ft.get("source_pdf_filename", ""),
        })

    # Join in sector_en / subsector_en from gpc_mapping
    gpc = list(csv.DictReader(open(INPUTS / "gpc_mapping_v1.csv", newline="")))
    en_lookup = {(g["sector"], g["subsector"]): (g["sector_en"], g["subsector_en"]) for g in gpc}
    for r in rows_out:
        s_en, ss_en = en_lookup.get((r["sector"], r["subsector"]), ("", ""))
        r["sector_en"] = s_en
        r["subsector_en"] = ss_en

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_cols)
        w.writeheader()
        w.writerows(rows_out)
    print(f"wrote {OUT}  rows={len(rows_out)}")
    print(f"  with FICHA data:    {sum(1 for r in rows_out if r['has_ficha_data'])}")
    print(f"  bip_database only:  {sum(1 for r in rows_out if not r['has_ficha_data'])}")
    print(f"  with sector_en:     {sum(1 for r in rows_out if r['sector_en'])}")


if __name__ == "__main__":
    main()
