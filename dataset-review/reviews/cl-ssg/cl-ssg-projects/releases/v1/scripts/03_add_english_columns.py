"""
Flatten the parsed FICHA IDI JSON corpus into a single bilingual (ES + EN)
CSV table — one row per etapa.

Closed-vocabulary fields (sector, etapa, fuente, RATE codes, ubicación tipo,
SEIA, etc.) are translated to English. Open free-text fields (justificación,
descripción, indicadores) are kept verbatim in Spanish; their column names
end in ``_es`` to signal that. When ``--translations-cache`` is supplied,
parallel ``_en`` columns are filled from the cache (OpenAI translations).

Usage
-----
    # default: writes data/derived/ficha_idi_table_translated.csv
    python scripts/03_add_english_columns.py

    # custom paths
    python scripts/03_add_english_columns.py \
        --json-dir releases/v1/corpus/parsed \
        --output   releases/v1/data/derived/ficha_idi_table_translated.csv

The CSV is UTF-8 with BOM so Excel recognises the encoding correctly.
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
INPUTS = DATA / "inputs"
DERIVED = DATA / "derived"
CORPUS = ROOT / "corpus"
DEFAULT_JSON_DIR = CORPUS / "parsed"
DEFAULT_OUTPUT = DERIVED / "ficha_idi_table_translated.csv"


# ---------------------------------------------------------------------------
# Translation dictionaries
# ---------------------------------------------------------------------------

TIPOLOGIA = {
    "PROYECTO":       "Project (works/infrastructure)",
    "PROGRAMA":       "Programme (transfer/activities)",
    "ESTUDIO BÁSICO": "Basic study",
}

ETAPA_ACTUAL = {
    "PERFIL":          "Concept",
    "PREFACTIBILIDAD": "Pre-feasibility",
    "FACTIBILIDAD":    "Feasibility",
    "DISEÑO":          "Design",
    "EJECUCION":       "Execution",
}

POSTULA_A = ETAPA_ACTUAL  # same vocabulary

SITUACION = {
    "NUEVA":    "New request",
    "ARRASTRE": "Continuing (multi-year)",
}

COMPONENTE_ANALISIS = {
    "NACIONAL":      "National",
    "REGIONAL":      "Regional",
    "INTERREGIONAL": "Inter-regional",
    "MULTIREGIONAL": "Multi-regional",
}

SEIA = {
    "NO CORRESPONDE": "Not applicable",
    "DECLARACION":    "Environmental Impact Declaration filed",
    "ESTUDIO":        "Environmental Impact Study filed",
    "EIA":            "EIA filed",
    "NO INGRESA":     "Not entered into SEIA",
}

UBIC_TIPO = {
    "REGION":           "Region",
    "PROVINCIA":        "Province",
    "COMUNA":           "Municipality",
    "INTERREGIONAL":    "Inter-regional",
    "MULTIREGIONAL":    "Multi-regional",
    "MULTIPROVINCIAL":  "Multi-province",
    "MULTICOMUNAL":     "Multi-municipality",
    "NACIONAL":         "National",
}

TIPO_RELACION = {
    "COMPLEMENTARIO": "Complementary",
    "SUSTITUTO":      "Replaces",
    "DEPENDE_DE":     "Depends on",
}

RATE_CODE = {
    "RS": "RS — Recommended (approved)",
    "FI": "FI — Missing information",
    "OT": "OT — Technically objected",
    "RE": "RE — Re-evaluation needed",
    "IN": "IN — Non-compliant",
}

ADMISIBILIDAD = {
    "Si": "Yes",
    "No": "No",
}

SECTOR = {
    "RECURSOS HÍDRICOS":                   "Water Resources",
    "RECURSOS HIDRICOS":                   "Water Resources",
    "RECURSOS NATURALES Y MEDIO AMBIENTE": "Natural Resources & Environment",
    "ENERGÍA":                             "Energy",
    "ENERGIA":                             "Energy",
    "TRANSPORTE":                          "Transport",
    "VIVIENDA Y DESARROLLO URBANO":        "Housing & Urban Development",
    "MULTISECTORIAL":                      "Multi-sectoral",
    "MINERÍA":                             "Mining",
    "MINERIA":                             "Mining",
}

# Subsector translations — handful of common ones; unmapped fall through.
SUBSECTOR = {
    "AGUAS LLUVIAS":                          "Stormwater",
    "AGUA POTABLE":                           "Drinking water",
    "DEFENSAS FLUVIALES,MARITIMAS Y CAUCES NATURALES": "Riverine, marine and natural-channel defences",
    "EVACUACION DE AGUAS LLUVIAS":            "Stormwater drainage",
    "MEDIO AMBIENTE":                         "Environment",
    "AGRICULTURA":                            "Agriculture",
    "ALUMBRADO PUBLICO":                      "Public lighting",
    "AUTOGENERACION":                         "Self-generation",
    "TRANSPORTE URBANO,VIALIDAD PEATONAL":    "Urban transport / pedestrian roads",
    "TRANSPORTE FERROVIARIO":                 "Rail transport",
    "TRANSPORTE CAMINERO":                    "Road transport",
    "DESARROLLO URBANO":                      "Urban development",
    "INTERSUBSECTORIAL MINERIA":              "Cross-cutting mining",
    "INTERSUBSECTORIAL MULTISECTOR":          "Cross-cutting multi-sectoral",
    "ADMINISTRACION MINERIA":                 "Mining administration",
    "HIDROCARBUROS":                          "Hydrocarbons",
}

FUENTE = {
    "F.N.D.R.":  "FNDR (Regional Development Fund)",
    "FNDR":      "FNDR (Regional Development Fund)",
    "SECTORIAL": "Sectoral (line-ministry budget)",
    "MUNICIPAL": "Municipal",
    "EMPRESA":   "State enterprise",
    "PRIVADO":   "Private",
}

ASIGNACION = {
    "OBRAS CIVILES":              "Civil works",
    "CONSULTORÍAS":               "Consulting",
    "CONSULTORIAS":               "Consulting",
    "GASTOS ADMINISTRATIVOS":     "Administrative expenses",
    "CONTRATACIÓN DEL PROGRAMA":  "Programme contracting",
    "CONTRATACION DEL PROGRAMA":  "Programme contracting",
    "EQUIPAMIENTO":               "Equipment",
    "TERRENOS COMPRA":            "Land acquisition",
    "OTROS GASTOS":               "Other expenses",
    "EQUIPOS":                    "Equipment",
    "VEHICULOS":                  "Vehicles",
}

MES = {
    "ene": "Jan", "feb": "Feb", "mar": "Mar", "abr": "Apr", "may": "May", "jun": "Jun",
    "jul": "Jul", "ago": "Aug", "sep": "Sep", "oct": "Oct", "nov": "Nov", "dic": "Dec",
}

TEMPLATE_VARIANT = {
    "PROYECTO":       "PROYECTO (works template)",
    "PROGRAMA":       "PROGRAMA (programme template)",
    "STUB":           "STUB (empty placeholder)",
    "ESTUDIO_BASICO": "Basic study template",
}


def t(d: dict, key, fallback_label: str | None = None) -> str:
    """Translate a closed-vocabulary value via dict ``d``.

    If unmapped, return the original value with a parenthetical hint that the
    translation wasn't recognised.
    """
    if key is None or key == "":
        return ""
    if key in d:
        return d[key]
    if fallback_label:
        return f"{key} ({fallback_label})"
    return f"{key} (untranslated)"


def join_list(xs, sep=" | ", limit=None):
    if not xs:
        return ""
    out = [str(x) for x in xs if x not in (None, "")]
    if limit is not None and len(out) > limit:
        out = out[:limit] + [f"… (+{len(xs) - limit} more)"]
    return sep.join(out)


# Translation cache lookup helpers ------------------------------------------

def tx(cache: dict[str, str] | None, value: str | None) -> str:
    """Return the cached English translation of ``value`` if available, else ''."""
    if not cache or not value:
        return ""
    return cache.get(value.strip(), "")


def tx_list(cache: dict[str, str] | None, items, sep=" | "):
    """Translate each item in a list using the cache, then join."""
    if not cache or not items:
        return ""
    out = []
    for x in items:
        if isinstance(x, str) and x.strip():
            t = cache.get(x.strip(), "")
            out.append(t if t else f"[untranslated: {x.strip()[:40]}…]")
    return sep.join(out)


# ---------------------------------------------------------------------------
# Row builder
# ---------------------------------------------------------------------------

COLUMNS = [
    # ── Identifiers
    "source_pdf",
    "bip_code",
    "etapa_index",
    # ── Document metadata
    "template_variant",
    "template_version",
    "parser_version",
    "n_etapas_in_pdf",
    # ── What is it
    "project_name",
    "project_type",
    "descriptor",
    "current_stage",
    "applies_for_stage",
    "request_status",
    # ── When
    "budget_year",
    "request_creation_date",
    "request_last_modified_date",
    "sni_submission_date",
    "sni_entry_date",
    "admissibility",
    # ── Sector / classification
    "sector",
    "subsector",
    "sector_subsector_raw_es",
    "analysis_level",
    "environmental_assessment_status",
    "indigenous_development_area",
    "linked_project_code",
    "linked_project_relationship",
    # ── Where
    "location_level",
    "location_name",
    "location_raw_es",
    "electoral_district",
    "senate_constituency",
    # ── Why & what (free text — kept Spanish; _en columns appear next to them
    #    when --translations-cache is provided, see add_en_columns())
    "justification_es",
    "description_es",
    "purpose_es",
    "purpose_indicators_es",
    "components_es",
    "component_indicators_es",
    # ── Beneficiaries
    "beneficiaries_male",
    "beneficiaries_female",
    "beneficiaries_total",
    # ── Duration
    "duration_months",
    "schedule_summary",
    # ── Cost & financing
    "total_cost_M_CLP_thousands",
    "total_cost_CLP",
    "total_cost_USD_estimate",
    "exchange_rate_CLP_per_USD",
    "budget_year_factor",
    "n_funding_sources",
    "funding_sources",
    "funding_breakdown",
    "in_kind_contributions",
    # ── Implementation
    "lead_agency",
    "financing_institutions",
    "technical_institutions",
    "responsible_officer_name",
    "responsible_officer_institution",
    "responsible_officer_role",
    "responsible_officer_phone",
    "responsible_officer_email",
    # ── Review / approval
    "review_result_code",
    "review_date",
    "review_institution",
    "n_review_passes",
    "conclusions_es",
    "admissibility_status",
    "n_admissibility_observations",
    # ── Budget execution
    "n_budget_history_request_rows",
    "n_budget_history_execution_rows",
    # ── Warnings
    "warning_multi_etapa_identical_blocks",
    "warning_nombre_extraction_failed",
]


def schedule_summary(aportes_directos):
    """Return a compact string describing start/end across line items."""
    if not aportes_directos:
        return ""
    starts, ends, durs = [], [], []
    for a in aportes_directos:
        i = a.get("inicio") or {}
        e = a.get("termino") or {}
        if i.get("mes") and i.get("anio_relativo"):
            starts.append(f"{MES.get(i['mes'], i['mes'])} Yr{i['anio_relativo']}")
        if e.get("mes") and e.get("anio_relativo"):
            ends.append(f"{MES.get(e['mes'], e['mes'])} Yr{e['anio_relativo']}")
        if a.get("duracion_meses"):
            durs.append(a["duracion_meses"])
    if not starts and not ends:
        return ""
    earliest = starts[0] if starts else ""
    latest   = ends[-1] if ends else ""
    return f"{earliest} → {latest}".strip(" →")


# Columns that get a parallel _en sibling when a translation cache is provided.
ES_COLUMNS_TO_TRANSLATE = [
    "sector_subsector_raw_es",
    "location_raw_es",
    "justification_es",
    "description_es",
    "purpose_es",
    "purpose_indicators_es",
    "components_es",
    "component_indicators_es",
    "conclusions_es",
]


def add_en_columns(columns: list[str]) -> list[str]:
    """Insert <name>_en immediately after each <name>_es column."""
    out = []
    for c in columns:
        out.append(c)
        if c in ES_COLUMNS_TO_TRANSLATE:
            out.append(c.replace("_es", "_en"))
    return out


def build_row(record: dict, etapa: dict, cache: dict | None = None) -> dict:
    doc = record["document"]
    extr = record["extraction"]
    src = extr["source_pdf"]
    warn_codes = {w["code"] for w in extr.get("warnings", [])}

    h = etapa["header"]
    ini = etapa["iniciativa"]
    clas = etapa["clasificacion"]
    ubic = etapa["ubicacion"]
    vinc = etapa["vinculacion"]
    nar = etapa["narrative"]
    sf = etapa["solicitud_financiamiento"]
    pi = etapa["programacion_inversion"]
    rr = etapa.get("resumen_resultados") or {}
    rr_ind = (rr.get("indicadores") or {})
    inst = etapa.get("instituciones_participantes") or {}
    fr = etapa.get("funcionario_responsable") or {}
    ra = etapa.get("resultado_analisis") or []
    obs = etapa.get("observaciones_admisibilidad") or {}
    hp = etapa.get("historial_presupuesto") or {}

    # --- monetary conversion ---
    cost_M = sf.get("totales", {}).get("costo_total")
    rate_clp = sf.get("tipo_cambio_clp_per_usd")
    cost_CLP = cost_M * 1000 if isinstance(cost_M, int) else None
    cost_USD = round(cost_CLP / rate_clp, 2) if (cost_CLP and rate_clp) else None

    # --- funding breakdown ---
    fb_pieces = []
    sources = []
    for r in sf.get("rows", []):
        f = t(FUENTE, r.get("fuente"), "fuente")
        a = t(ASIGNACION, r.get("asignacion_presupuestaria"), "asignación")
        ct = r.get("costo_total") or 0
        fb_pieces.append(f"{f} / {a}: {ct:,} M$")
        sources.append(f)
    funding_breakdown = "  ;  ".join(fb_pieces)
    n_sources = len({s for s in sources})

    # --- in-kind / otros aportes ---
    in_kind = []
    for o in pi.get("otros_aportes", []):
        f = o.get("fuente", "")
        ai = (o.get("aporte_indirecto") or {}).get("M$")
        ct = (o.get("costo_total_etapa_programada") or {}).get("M$")
        in_kind.append(f"{f}: indirect={ai or 0:,} M$, total_etapa={ct or 0:,} M$")
    in_kind_str = "  ;  ".join(in_kind)

    # --- linked project ---
    linked = vinc.get("proyecto_relacionado") or {}
    linked_code = linked.get("codigo") or ""
    linked_rel  = t(TIPO_RELACION, linked.get("tipo_relacion")) if linked else ""

    # --- review history ---
    last_review = ra[0] if ra else {}
    review_code = t(RATE_CODE, (ini.get("rate") or {}).get("resultado") or last_review.get("rate"))
    review_date = (ini.get("rate") or {}).get("fecha") or last_review.get("fecha") or ""
    review_inst = (ini.get("rate") or {}).get("institucion") or last_review.get("institucion_analisis") or ""

    # --- beneficiaries ---
    bd = (rr.get("beneficiarios_directos") or {})

    row = {
        "source_pdf":                src.get("filename", ""),
        "bip_code":                  ini.get("codigo_bip", ""),
        "etapa_index":               etapa.get("etapa_index", 0),

        "template_variant":          t(TEMPLATE_VARIANT, doc.get("template_variant")),
        "template_version":          doc.get("template_version") or "",
        "parser_version":            extr.get("parser_version", ""),
        "n_etapas_in_pdf":           doc.get("n_etapas_in_pdf", 0),

        "project_name":              ini.get("nombre", ""),
        "project_type":              t(TIPOLOGIA, ini.get("tipologia")),
        "descriptor":                ini.get("descriptor") or "",
        "current_stage":             t(ETAPA_ACTUAL, clas.get("etapa_actual")),
        "applies_for_stage":         t(POSTULA_A, h.get("postula_a")),
        "request_status":            t(SITUACION, clas.get("situacion_solicitud")),

        "budget_year":               h.get("proceso_presupuestario") or "",
        "request_creation_date":     doc.get("fecha_creacion_solicitud") or "",
        "request_last_modified_date":doc.get("fecha_ultima_modificacion") or "",
        "sni_submission_date":       h.get("fecha_postulacion_sni") or "",
        "sni_entry_date":            h.get("fecha_ingreso_sni") or "",
        "admissibility":             t(ADMISIBILIDAD, h.get("admisibilidad")),

        "sector":                    t(SECTOR, clas.get("sector"), "sector"),
        "subsector":                 t(SUBSECTOR, clas.get("subsector"), "subsector"),
        "sector_subsector_raw_es":   clas.get("sector_subsector_raw") or "",
        "analysis_level":            t(COMPONENTE_ANALISIS, clas.get("componente_analisis")),
        "environmental_assessment_status": t(SEIA, clas.get("seia")),
        "indigenous_development_area": (
            "Yes" if clas.get("area_desarrollo_indigena") is True
            else ("No" if clas.get("area_desarrollo_indigena") is False else "")
        ),
        "linked_project_code":       linked_code,
        "linked_project_relationship": linked_rel,

        "location_level":            t(UBIC_TIPO, ubic.get("tipo")),
        "location_name":             ubic.get("nombre") or "",
        "location_raw_es":           ubic.get("raw") or "",
        "electoral_district":        ubic.get("distrito") or "",
        "senate_constituency":       ubic.get("circunscripcion") or "",

        "justification_es":          nar.get("justificacion") or "",
        "description_es":            nar.get("descripcion_etapa") or "",
        "purpose_es":                rr_ind.get("proposito") or "",
        "purpose_indicators_es":     join_list(rr_ind.get("indicadores_proposito", [])),
        "components_es":             join_list(rr_ind.get("componentes", [])),
        "component_indicators_es":   join_list(rr_ind.get("indicadores_componentes", [])),

        "beneficiaries_male":        bd.get("hombres") if bd else "",
        "beneficiaries_female":      bd.get("mujeres") if bd else "",
        "beneficiaries_total":       bd.get("total") if bd else "",

        "duration_months":           rr.get("duracion_meses") if rr else "",
        "schedule_summary":          schedule_summary(pi.get("aportes_directos") or []),

        "total_cost_M_CLP_thousands": cost_M if cost_M is not None else "",
        "total_cost_CLP":            cost_CLP if cost_CLP is not None else "",
        "total_cost_USD_estimate":   cost_USD if cost_USD is not None else "",
        "exchange_rate_CLP_per_USD": rate_clp if rate_clp is not None else "",
        "budget_year_factor":        (sf.get("moneda_presupuesto") or {}).get("factor") or "",
        "n_funding_sources":         n_sources,
        "funding_sources":           join_list(sorted(set(sources))),
        "funding_breakdown":         funding_breakdown,
        "in_kind_contributions":     in_kind_str,

        "lead_agency":               inst.get("institucion_formuladora") or "",
        "financing_institutions":    join_list(inst.get("instituciones_financieras") or []),
        "technical_institutions":    join_list(inst.get("instituciones_tecnicas") or []),
        "responsible_officer_name":  fr.get("nombre") or "",
        "responsible_officer_institution": fr.get("institucion") or "",
        "responsible_officer_role":  fr.get("cargo") or "",
        "responsible_officer_phone": fr.get("fono") or "",
        "responsible_officer_email": fr.get("correo_electronico") or "",

        "review_result_code":        review_code,
        "review_date":               review_date,
        "review_institution":        review_inst,
        "n_review_passes":           len(ra),
        "conclusions_es":            etapa.get("conclusiones_analisis") or "",
        "admissibility_status":      ("Admitted" if obs.get("admitido") is True
                                     else ("Not admitted" if obs.get("admitido") is False else "")),
        "n_admissibility_observations": len(obs.get("observaciones") or []) if obs else 0,

        "n_budget_history_request_rows":   len(hp.get("solicitudes_financiamiento") or []) if hp else 0,
        "n_budget_history_execution_rows": len(hp.get("ejecucion_presupuestaria") or []) if hp else 0,

        "warning_multi_etapa_identical_blocks": "yes" if "multi_etapa_identical_blocks" in warn_codes else "",
        "warning_nombre_extraction_failed":     "yes" if "nombre_extraction_failed" in warn_codes else "",
    }

    # When a translation cache is supplied, populate _en columns alongside _es.
    if cache is not None:
        row["sector_subsector_raw_en"] = tx(cache, clas.get("sector_subsector_raw"))
        row["location_raw_en"]         = tx(cache, ubic.get("raw"))
        row["justification_en"]        = tx(cache, nar.get("justificacion"))
        row["description_en"]          = tx(cache, nar.get("descripcion_etapa"))
        row["purpose_en"]              = tx(cache, rr_ind.get("proposito"))
        row["purpose_indicators_en"]   = tx_list(cache, rr_ind.get("indicadores_proposito") or [])
        row["components_en"]           = tx_list(cache, rr_ind.get("componentes") or [])
        row["component_indicators_en"] = tx_list(cache, rr_ind.get("indicadores_componentes") or [])
        row["conclusions_en"]          = tx(cache, etapa.get("conclusiones_analisis"))

    return row


def stub_row(record: dict, columns: list[str]) -> dict:
    """For STUB PDFs we still emit one row so consumers see the file exists."""
    src = record["extraction"]["source_pdf"]
    doc = record["document"]
    extr = record["extraction"]
    return {col: "" for col in columns} | {
        "source_pdf":       src.get("filename", ""),
        "etapa_index":      "",
        "template_variant": t(TEMPLATE_VARIANT, doc.get("template_variant")),
        "template_version": doc.get("template_version") or "",
        "parser_version":   extr.get("parser_version", ""),
        "n_etapas_in_pdf":  0,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json-dir", type=Path, default=DEFAULT_JSON_DIR)
    ap.add_argument("--output",   type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--include-stubs", action="store_true",
                    help="Emit a row for STUB PDFs too (default: skip).")
    ap.add_argument("--translations-cache", type=Path, default=None,
                    help="Optional path to a {spanish: english} JSON cache "
                         "produced by scripts/04_translate_narrative.py. When supplied, "
                         "the CSV gains an _en column next to each _es column.")
    args = ap.parse_args()

    cache: dict | None = None
    if args.translations_cache:
        if not args.translations_cache.exists():
            print(f"ERROR: translations cache not found: {args.translations_cache}", file=sys.stderr)
            return 1
        cache = json.loads(args.translations_cache.read_text())
        print(f"Loaded {len(cache):,} translations from {args.translations_cache}")

    columns = add_en_columns(COLUMNS) if cache is not None else COLUMNS

    paths = sorted(glob.glob(str(args.json_dir / "*.json")))
    if not paths:
        print(f"ERROR: no JSON files in {args.json_dir}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    n_files = 0
    n_etapas_written = 0
    n_stubs = 0

    # Open with utf-8-sig so Excel auto-detects the encoding.
    with open(args.output, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=columns, quoting=csv.QUOTE_MINIMAL,
                           extrasaction="ignore")
        w.writeheader()
        for p in paths:
            try:
                d = json.loads(Path(p).read_text())
            except Exception as e:
                print(f"  skip {Path(p).name}: {e}", file=sys.stderr)
                continue
            n_files += 1
            etapas = d.get("etapas") or []
            if not etapas:
                n_stubs += 1
                if args.include_stubs:
                    w.writerow(stub_row(d, columns))
                continue
            for e in etapas:
                w.writerow(build_row(d, e, cache))
                n_etapas_written += 1

    print(f"Wrote {args.output}")
    print(f"  files read       : {n_files}")
    print(f"  etapa rows written: {n_etapas_written}")
    print(f"  stubs            : {n_stubs}{'  (skipped)' if not args.include_stubs else '  (included)'}")
    print(f"  columns          : {len(columns)}{'  (incl. _en translations)' if cache is not None else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
