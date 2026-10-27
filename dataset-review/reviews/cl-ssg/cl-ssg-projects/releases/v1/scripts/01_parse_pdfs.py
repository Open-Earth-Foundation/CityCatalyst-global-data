"""
Chile SNI/BIP — Reporte Ficha IDI parser.

Reads a "Reporte Ficha IDI" PDF and emits JSON conforming to
ficha_idi.schema.v1.0.0.json.

Usage as a CLI:
    python scripts/01_parse_pdfs.py <pdf_path> [-o output.json] [--validate]

Usage as a library:
    from parse_module import parse_ficha
    record = parse_ficha("path/to/file.pdf")     # -> dict (JSON-serialisable)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

PARSER_VERSION = "ficha_idi_parser/1.0.2"
SCHEMA_VERSION = "1.0.0"
STUB_SIZE_THRESHOLD = 30_000   # bytes; the canonical "null" stubs are 28k
STUB_TEXT_THRESHOLD = 500      # chars in pdftotext output


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def strip_accents(s: str | None) -> str:
    if not s:
        return ""
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))


def pdftotext(path: str | Path, layout: bool = True) -> str:
    args = ["pdftotext"]
    if layout:
        args.append("-layout")
    args.extend([str(path), "-"])
    res = subprocess.run(args, capture_output=True, text=True, check=False)
    return res.stdout or ""


def sha256_of(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def pdf_pagecount(path: str | Path) -> int | None:
    res = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, check=False)
    m = re.search(r"^Pages:\s+(\d+)", res.stdout, re.M)
    return int(m.group(1)) if m else None


def pdf_producer(path: str | Path) -> str | None:
    res = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, check=False)
    m = re.search(r"^Producer:\s+(.+)$", res.stdout, re.M)
    return m.group(1).strip() if m else None


def parse_int(s) -> int | None:
    """'90.000' or '  90.000  ' → 90000. Accepts thousands separator '.', ',' or spaces."""
    if s is None:
        return None
    if isinstance(s, int):
        return s
    s = re.sub(r"[\s.,]", "", str(s).strip())
    if s in ("", "-"):
        return None
    try:
        return int(s)
    except ValueError:
        return None


def parse_float(s) -> float | None:
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return float(s)
    s = str(s).strip()
    if s in ("", "-"):
        return None
    # Spanish decimal: '163.432' = 163.432 already (period is decimal here, NOT thousands).
    # But '90.000' may be either 90000 or 90.000 depending on context; we don't call this
    # for amounts in M$ — those go through parse_int.
    s = s.replace(",", ".")
    # If the only period is at position len-4 it's likely a thousands sep; we keep as float.
    try:
        return float(s)
    except ValueError:
        return None


def parse_date(s: str | None) -> str | None:
    """Spanish DD/MM/YYYY → ISO YYYY-MM-DD."""
    if not s:
        return None
    s = s.strip()
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def first(pat: str, text: str, group: int = 1, flags=re.I | re.M | re.S) -> str | None:
    m = re.search(pat, text, flags)
    if not m:
        return None
    val = m.group(group)
    return val.strip() if val else None


def normalize_ws(s: str | None) -> str | None:
    if s is None:
        return None
    s = re.sub(r"\d{1,2}/\d{1,2}/\d{4}\s+Versi[oó]n\s+[\d.]+\s+P[áa]gina\s+\d+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s or None


# ---------------------------------------------------------------------------
# Variant detection
# ---------------------------------------------------------------------------

def detect_template_version(text: str) -> str | None:
    m = re.search(r"Versi[oó]n\s+(\d+\.\d+)", text)
    return m.group(1) if m else None


def detect_template_variant(text: str, size_bytes: int) -> str:
    if size_bytes < STUB_SIZE_THRESHOLD and len(text.strip()) < STUB_TEXT_THRESHOLD:
        return "STUB"
    if "PROCESO PRESUPUESTARIO null" in text:
        return "STUB"
    tip = first(r"TIPOLOG[ÍI]A\s*:\s*(PROYECTO|PROGRAMA|ESTUDIO B[ÁA]SICO)", text)
    if tip == "ESTUDIO BÁSICO":
        return "ESTUDIO_BASICO"
    if tip == "PROGRAMA":
        return "PROGRAMA"
    if tip == "PROYECTO":
        return "PROYECTO"
    # No tipologia found → treat as STUB
    return "STUB"


def split_etapas(text: str) -> list[str]:
    """A multi-etapa PDF prints 'REPORTE FICHA IDI' twice. Split on that header."""
    parts = re.split(r"(?=^[\s ]*REPORTE FICHA[- ]IDI)", text, flags=re.M)
    return [p for p in parts if "REPORTE FICHA" in p]


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

def parse_header(text: str) -> dict:
    proceso = first(r"PROCESO PRESUPUESTARIO\s+(\d{4})", text)
    proceso_year = int(proceso) if proceso else None

    postula = first(r"POSTULA A\s+(EJECUCION|EJECUCI[OÓ]N|PERFIL|PREFACTIBILIDAD|FACTIBILIDAD|DISE[ÑN]O)", text)
    if postula:
        postula = postula.replace("EJECUCIÓN", "EJECUCION").replace("DISEÑO", "DISEÑO")

    fp = first(r"Fecha Postulaci[oó]n SNI\s*:\s*([0-9/\-]+)", text)
    fi = first(r"Fecha Ingreso SNI\s*:\s*([0-9/\-]+)", text)

    adm = first(r"Admisibilidad\s*:\s*(Si|No)", text)
    return {
        "proceso_presupuestario": proceso_year,
        "postula_a": postula,
        "fecha_postulacion_sni": parse_date(fp),
        "fecha_ingreso_sni": parse_date(fi),
        "admisibilidad": adm,
    }


# ---------------------------------------------------------------------------
# Iniciativa (section 1)
# ---------------------------------------------------------------------------

def parse_iniciativa(text: str) -> dict:
    tip = first(r"TIPOLOG[ÍI]A\s*:\s*(PROYECTO|PROGRAMA|ESTUDIO B[ÁA]SICO)", text)
    bip = first(r"C[ÓO]DIGO BIP\s*:\s*(\d+\-\d+)", text)

    nombre = None
    m = re.search(r"NOMBRE(?:\s+IDI)?\s*:\s*(.+?)\s*DESCRIPTOR", text, re.I | re.S)
    if m and m.group(1).strip():
        nombre = normalize_ws(m.group(1))
    else:
        # Fallback A: PROYECTO files where label/value are on different lines and the
        # value sits below the DESCRIPTOR row, prefixed by a stand-alone colon.
        m2 = re.search(
            r"NOMBRE(?:\s+IDI)?\s*\n.*?DESCRIPTOR\s*:?\s*\n\s*:\s*(.+?)(?:\n\s*\n|\n\s*SIN DESCRIPTORES|\n\s*RATE)",
            text, re.I | re.S,
        )
        if m2:
            nombre = normalize_ws(m2.group(1))

    if not nombre:
        # Fallback B: 'NOMBRE IDI' label has no colon on its own line; the value lives
        # on a colon-prefixed line elsewhere in section 1. Pick the longest such
        # candidate (descriptor values like 'PRU' / 'SUBTÍTULO 33' are short).
        sec1 = re.search(r"NOMBRE(?:\s+IDI)?\b(.+?)RATE\s*=", text, re.I | re.S)
        if sec1:
            block = sec1.group(1)
            value_lines = re.findall(
                r"^\s+:\s+([A-ZÁÉÍÓÚÑ0-9][^\n]*?)\s*$", block, re.M
            )
            candidates = [v.strip() for v in value_lines
                          if len(v.strip()) > 12
                          and v.strip().upper() != "SIN DESCRIPTORES"]
            if candidates:
                nombre = normalize_ws(max(candidates, key=len))

    descriptor = None
    # Stop the descriptor capture at: a stand-alone colon-prefixed line (which is the
    # NOMBRE value bleeding in via two-column layout), a blank line, RATE =, or the
    # next numbered section. The new '\n\s+:\s+' guard fixes the case where descriptor
    # was swallowing the leaked nombre value plus the trailing RATE code.
    md = re.search(
        r"DESCRIPTOR\s*:\s*(.+?)(?:\n\s+:\s+|\n\s*\n|\n\s*RATE\s*=|\n\s*\d+\.\s*ETAPA ACTUAL)",
        text, re.I | re.S,
    )
    if md:
        descriptor = normalize_ws(md.group(1))
    if descriptor and "SIN DESCRIPTORES" in descriptor.upper():
        descriptor = None

    # The RATE column header appears at the top of section 1; the 2-letter code
    # and date sit beneath it but separated by several intervening label lines.
    # Bound the search to avoid false-matching a RATE table further down.
    rate_resultado = None
    rate_fecha = None
    rh = re.search(r"\bRATE\b", text)
    if rh:
        window = text[rh.end(): rh.end() + 800]
        cm = re.search(r"\n\s+(RS|FI|OT|RE|IN)\b", window)
        if cm:
            rate_resultado = cm.group(1)
            tail = window[cm.end():]
            dm = re.search(r"\n\s+(\d{1,2}/\d{1,2}/\d{4})", tail[:200])
            if dm:
                rate_fecha = parse_date(dm.group(1))

    return {
        "tipologia": tip,
        "codigo_bip": bip,
        "nombre": nombre,
        "descriptor": descriptor,
        "rate": {
            "resultado": rate_resultado,
            "fecha": rate_fecha,
            "institucion": None,
        },
    }


# ---------------------------------------------------------------------------
# Sections 2-9 (etapa, sector, location, etc.)
# ---------------------------------------------------------------------------

def parse_classification_and_location(text: str) -> tuple[dict, dict, dict]:
    # ------- etapa actual -------
    etapa = first(r"ETAPA ACTUAL\s*:\s*([A-ZÁÉÍÓÚÑ ]+?)(?:\s{2,}|$)", text)
    if not etapa:
        # PROGRAMA two-column layout
        etapa = first(
            r"ETAPA ACTUAL.{0,400}?\b(PERFIL|PREFACTIBILIDAD|DISE[ÑN]O|FACTIBILIDAD|EJECUCI[OÓ]N)\b",
            text,
        )
    if etapa:
        etapa = etapa.replace("EJECUCIÓN", "EJECUCION").upper().strip()
        if etapa not in ("PERFIL", "PREFACTIBILIDAD", "FACTIBILIDAD", "DISEÑO", "EJECUCION"):
            etapa = None

    # ------- sector / subsector -------
    sector_raw = None
    m = re.search(r"SECTOR/SUBSECTOR\s*:\s*(.+?)(?:\n\s*(?:4\.|LOC\.|COMP\.|DISTRITO))", text, re.I | re.S)
    if m and m.group(1).strip():
        sector_raw = normalize_ws(m.group(1))
    if not sector_raw:
        # Two-column PROGRAMA layout: value is split across lines around the label
        lines = text.splitlines()
        for i, ln in enumerate(lines):
            if re.search(r"3\.\s*SECTOR/SUBSECTOR", ln):
                before = lines[i - 1] if i > 0 else ""
                bm = re.search(r":\s*([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ ,\-/]+)$", before)
                p1 = bm.group(1).strip() if bm else ""
                p2 = ""
                for j in range(i + 1, min(i + 5, len(lines))):
                    tail = lines[j].strip()
                    if not tail or tail == ":" or re.match(r"^\d+\.", tail):
                        continue
                    if re.match(r"^[/A-ZÁÉÍÓÚÑ]", tail):
                        p2 = tail
                        break
                combined = re.sub(r"\s+", " ", f"{p1} {p2}").strip(" /")
                sector_raw = combined or None
                break
    sector = subsector = None
    if sector_raw and "/" in sector_raw:
        a, b = sector_raw.split("/", 1)
        sector, subsector = a.strip(), b.strip()
    elif sector_raw:
        sector = sector_raw

    # ------- componente análisis -------
    comp = first(r"COMP\.\s*DE AN[ÁA]LISIS\s*:\s*(\w+)", text)
    if not comp:
        comp = first(r"COMP\.\s*DE AN[ÁA]LISIS.{0,200}?\b(NACIONAL|REGIONAL|INTERREGIONAL|MULTIREGIONAL)\b", text)
    if comp:
        comp = comp.upper()
        if comp not in ("NACIONAL", "REGIONAL", "INTERREGIONAL", "MULTIREGIONAL"):
            comp = None

    # ------- SEIA -------
    seia = first(r"\bSEIA\s*:\s*(NO CORRESPONDE|DECLARACION|ESTUDIO|EIA|NO INGRESA)", text)
    if not seia:
        seia = first(r"\bSEIA\b.{0,300}?\b(NO CORRESPONDE|DECLARACI[OÓ]N|ESTUDIO|EIA|NO INGRESA)\b", text)
        if seia:
            seia = seia.replace("DECLARACIÓN", "DECLARACION")

    # ------- ADI -------
    adi_raw = first(r"[ÁA]REA DE DESARROLLO IND[ÍI]GENA\s*:\s*(\S+)", text)
    if adi_raw is None:
        ad_indigena = None
    else:
        ad_indigena = adi_raw.upper().startswith("SI") or adi_raw.upper() == "SÍ"

    # ------- situación de la solicitud -------
    sit = first(r"SITUACI[ÓO]N DE LA SOLICITUD\s*:\s*(NUEVA|ARRASTE|ARRASTRE)", text)
    if sit == "ARRASTE":
        sit = "ARRASTRE"

    clas = {
        "etapa_actual": etapa,
        "sector": sector,
        "subsector": subsector,
        "sector_subsector_raw": sector_raw,
        "componente_analisis": comp,
        "seia": seia,
        "area_desarrollo_indigena": ad_indigena,
        "situacion_solicitud": sit,
    }

    # ------- ubicación -------
    raw = first(r"LOC\.\s*GEOGR[ÁA]FICA\s*:\s*(.+?)(?:\s{2,}5\.|\n)", text)
    if not raw:
        m3 = re.search(r"LOC\.\s*GEOGR[ÁA]FICA(.{0,400})", text, re.I | re.S)
        if m3:
            window = m3.group(1)
            mw = re.search(
                r"\b((?:REGIONES DE|REGION DE|REGION DEL|REGION|COMUNAS DE|COMUNA DE|PROVINCIA DE|"
                r"MULTIPROVINCIAL|MULTICOMUNAL|MULTIREGIONAL|INTERREGIONAL|NACIONAL)"
                r"\s+[A-ZÁÉÍÓÚÑ ]+?)(?:\s{2,}|\n|$)",
                window,
            )
            if mw:
                raw = normalize_ws(mw.group(1))
    raw = normalize_ws(raw)

    tipo = nombre = None
    if raw:
        u = raw.upper()
        if u.startswith("REGIONES DE"):
            tipo, nombre = "MULTIREGIONAL", raw[12:].strip()
        elif u.startswith("REGION DE") or u.startswith("REGION DEL") or u.startswith("REGION "):
            tipo = "REGION"
            nombre = re.sub(r"^REGION\s+(?:DE|DEL)?\s*", "", raw, flags=re.I).strip()
        elif u.startswith("COMUNAS DE"):
            tipo, nombre = "MULTICOMUNAL", raw[11:].strip()
        elif u.startswith("COMUNA DE"):
            tipo, nombre = "COMUNA", raw[10:].strip()
        elif u.startswith("PROVINCIA DE"):
            tipo, nombre = "PROVINCIA", raw[13:].strip()
        elif u in ("INTERREGIONAL", "MULTIREGIONAL", "NACIONAL", "MULTIPROVINCIAL", "MULTICOMUNAL"):
            tipo, nombre = u, None

    distrito = first(r"\bDISTRITO\s*:\s*(\S+)", text)
    circunscripcion = first(r"CIRCUNSCRIPCI[ÓO]N\s*:\s*([^\n]+?)(?:\s{2,}|$)", text)
    if circunscripcion:
        circunscripcion = normalize_ws(circunscripcion)

    ubic = {
        "raw": raw,
        "tipo": tipo,
        "nombre": nombre,
        "distrito": distrito,
        "circunscripcion": circunscripcion,
    }

    # ------- proyecto relacionado -------
    pr = first(r"PROYECTO REL(?:AC)?\.\s*:\s*(\d+)\s*\(([A-ZÁÉÍÓÚÑ ]+)\)", text, group=0)
    proyecto_relacionado = None
    if pr:
        m_pr = re.search(r"(\d+)\s*\(([A-ZÁÉÍÓÚÑ ]+)\)", pr)
        if m_pr:
            tipo_rel = m_pr.group(2).strip().upper()
            if tipo_rel not in ("COMPLEMENTARIO", "SUSTITUTO", "DEPENDE_DE"):
                tipo_rel = None
            proyecto_relacionado = {"codigo": m_pr.group(1), "tipo_relacion": tipo_rel}
    vinc = {"proyecto_relacionado": proyecto_relacionado}

    return clas, ubic, vinc


# ---------------------------------------------------------------------------
# Sections 10, 11 — narrative
# ---------------------------------------------------------------------------

def parse_narrative(text: str) -> dict:
    just = re.search(
        r"\d+\.\s*JUSTIFICACI[ÓO]N DEL (?:PROYECTO|PROGRAMA|ESTUDIO)\.?\s*\n(.+?)\n\s*\d+\.\s*DESCRIPCI[ÓO]N",
        text, re.I | re.S,
    )
    desc = re.search(
        r"\d+\.\s*DESCRIPCI[ÓO]N DE (?:LA ETAPA|LAS ACTIVIDADES).+?\n(.+?)\n\s*\d+\.\s*CORRESPONDE A UN [ÁA]REA",
        text, re.I | re.S,
    )
    return {
        "justificacion": normalize_ws(just.group(1)) if just else None,
        "descripcion_etapa": normalize_ws(desc.group(1)) if desc else None,
    }


# ---------------------------------------------------------------------------
# Section 14/15 — solicitud de financiamiento
# ---------------------------------------------------------------------------

EMPTY_FINANCING = {
    "moneda_presupuesto": {"year": None, "factor": None},
    "tipo_cambio_clp_per_usd": None,
    "rows": [],
    "totales": {
        "pagado_al_inicio_periodo": None,
        "solicitado_periodo_actual": None,
        "solicitado_periodos_siguientes": None,
        "costo_total": None,
    },
}


def parse_financiamiento(text: str) -> dict:
    m = re.search(
        r"SOLICITUD DE FINANCIAMIENTO(.+?)(?:Moneda Presupuesto|\d+\.\s*PROGRAMACI[ÓO]N|FECHA CREACI[ÓO]N)",
        text, re.I | re.S,
    )
    if not m:
        return _empty(EMPTY_FINANCING)
    block = m.group(1)

    rows = []
    row_re = re.compile(
        r"^\s*([A-ZÁÉÍÓÚÑ\.\-]+(?:\s+[A-ZÁÉÍÓÚÑ\.\-]+)*?)\s{2,}"     # fuente
        r"([A-ZÁÉÍÓÚÑ ()\-,]+?)\s{2,}"                                # asignación
        r"(M\$|MUS\$|US\$)\s+"                                         # moneda
        r"([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)\s*$",          # 4 numeric cols
        re.M,
    )
    for mo in row_re.finditer(block):
        fuente, asig, moneda, p1, p2, p3, p4 = mo.groups()
        if fuente.strip().upper().startswith("TOTAL"):
            continue
        rows.append({
            "fuente": fuente.strip(),
            "asignacion_presupuestaria": asig.strip(),
            "moneda": "MUS$" if "US" in moneda else "M$",
            "pagado_al_inicio_periodo": parse_int(p1),
            "solicitado_periodo_actual": parse_int(p2),
            "solicitado_periodos_siguientes": parse_int(p3),
            "costo_total": parse_int(p4) or 0,
        })

    tot = re.search(r"Total\s*_?\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)", block)
    totales = {
        "pagado_al_inicio_periodo": parse_int(tot.group(1)) if tot else None,
        "solicitado_periodo_actual": parse_int(tot.group(2)) if tot else None,
        "solicitado_periodos_siguientes": parse_int(tot.group(3)) if tot else None,
        "costo_total": parse_int(tot.group(4)) if tot else None,
    }

    fact_m = re.search(r"Moneda Presupuesto\s+(\d{4})\s*/\s*Factor:\s*([\d.,]+)", text)
    moneda_p = {
        "year": int(fact_m.group(1)) if fact_m else None,
        "factor": parse_float(fact_m.group(2)) if fact_m else None,
    }
    tc_m = re.search(r"Tipo de Cambio:\s*\$?([\d.,]+)\s*/\s*\$?US", text)
    tc = parse_float(tc_m.group(1)) if tc_m else None

    return {
        "moneda_presupuesto": moneda_p,
        "tipo_cambio_clp_per_usd": tc,
        "rows": rows,
        "totales": totales,
    }


# ---------------------------------------------------------------------------
# Section 15/16 — programación de la inversión
# ---------------------------------------------------------------------------

EMPTY_PROGRAMACION = {
    "aportes_directos": [],
    "otros_aportes": [],
    "totales": {
        "monto_directo_total": {"M$": None, "MUS$": None},
        "costo_total_etapa_programada": {"M$": None, "MUS$": None},
    },
}


def _money(m: str | None, mus: str | None) -> dict:
    return {"M$": parse_int(m), "MUS$": parse_float(mus)}


def parse_programacion(text: str) -> dict:
    m = re.search(
        r"PROGRAMACI[ÓO]N DE LA INVERSI[ÓO]N(.+?)(?:\d+\.\s*REGISTRO DE INGRESO|17\.\s*REGISTRO|FECHA CREACI[ÓO]N)",
        text, re.I | re.S,
    )
    if not m:
        return _empty(EMPTY_PROGRAMACION)
    block = m.group(1)

    # Aportes Directos block
    ap_m = re.search(r"Aportes Directos(.+?)(?:Otros Aportes|TOTAL\s|17\.|REGISTRO)", block, re.I | re.S)
    aportes = []
    if ap_m:
        ap_block = ap_m.group(1)
        row_re = re.compile(
            r"^\s*([A-ZÁÉÍÓÚÑ ()\-,]+?)\s{2,}"
            r"(\d+)\s+Meses\s+"
            r"(ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)\s*/\s*A[ñn]o\s*(\d+)\s+"
            r"(ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)\s*/\s*A[ñn]o\s*(\d+)\s+"
            r"([\d.,]+)?\s*([\d.,]+)?\s*$",
            re.M,
        )
        for mo in row_re.finditer(ap_block):
            asig, dur, im, ia, tm, ta, monto1, monto2 = mo.groups()
            aportes.append({
                "asignacion_presupuestaria": asig.strip(),
                "duracion_meses": int(dur),
                "inicio": {"mes": im, "anio_relativo": int(ia)},
                "termino": {"mes": tm, "anio_relativo": int(ta)},
                "monto": _money(monto1, monto2),
            })

    # Otros Aportes block (rows like "APORTE BENEFICIARIOS  40.000  ...")
    ot_m = re.search(r"Otros Aportes(.+?)(?:REGISTRO DE INGRESO|17\.|18\.)", block, re.I | re.S)
    otros = []
    if ot_m:
        ot_block = ot_m.group(1)
        row_re = re.compile(
            r"^\s*([A-ZÁÉÍÓÚÑ ()\-,]+?)\s{2,}([\d.,]+)\s*([\d.,]+)?\s*$",
            re.M,
        )
        for mo in row_re.finditer(ot_block):
            fuente, ai, ct = mo.groups()
            f = fuente.strip()
            if f.upper().startswith("FUENTE") or f.upper().startswith("TOTAL"):
                continue
            otros.append({
                "fuente": f,
                "aporte_indirecto": _money(ai, None),
                "costo_total_etapa_programada": _money(ct, None),
            })

    # Totales — TOTAL line in Aportes Directos
    tot_m = re.search(r"^\s*TOTAL\s+([\d.,]+)\s*([\d.,]+)?\s*$", block, re.M)
    monto_directo = _money(tot_m.group(1) if tot_m else None,
                           tot_m.group(2) if tot_m else None)
    cte_m = re.search(r"costo total etapa programada.*?([\d.,]+)", block, re.I | re.S)
    cte = _money(cte_m.group(1) if cte_m else None, None)

    return {
        "aportes_directos": aportes,
        "otros_aportes": otros,
        "totales": {
            "monto_directo_total": monto_directo,
            "costo_total_etapa_programada": cte,
        },
    }


# ---------------------------------------------------------------------------
# Sections 16/17 — REGISTRO DE INGRESO EN EL S.N.I.
# ---------------------------------------------------------------------------

def parse_registro_sni(text: str) -> list:
    m = re.search(
        r"REGISTRO DE INGRESO EN EL S\.?N\.?I(.+?)(?:\d+\.\s*RESULTADO|\d+\.\s*CONCLUSIONES|\d+\.\s*INSTITUCIONES|FECHA CREACI[ÓO]N|$)",
        text, re.I | re.S,
    )
    if not m:
        return []
    block = m.group(1)
    rows = []
    row_re = re.compile(
        r"^\s*([A-ZÁÉÍÓÚÑ ]+?)\s{2,}([0-9/]+)\s{2,}([A-ZÁÉÍÓÚÑ \-,()0-9]+?)\s*$",
        re.M,
    )
    for mo in row_re.finditer(block):
        rec, fecha, inst = mo.groups()
        if rec.strip().upper() in ("RECEPCION", "RECEPCIÓN"):
            continue
        rows.append({
            "recepcion": rec.strip(),
            "fecha": parse_date(fecha),
            "institucion_responsable": inst.strip(),
        })
    return rows


# ---------------------------------------------------------------------------
# Sections 17/18 — RESULTADO DEL ANÁLISIS
# ---------------------------------------------------------------------------

def parse_resultado_analisis(text: str) -> list:
    m = re.search(
        r"RESULTADO DEL AN[ÁA]LISIS(?: T[ÉE]CNICO ECON[ÓO]MICO)?(.+?)(?:\d+\.\s*CONCLUSIONES|\d+\.\s*INSTITUCIONES|\d+\.\s*RESUMEN|\d+\.\s*HISTORIAL|\d+\.\s*FUNCIONARIO|\d+\.\s*OBSERVACIONES|FECHA CREACI[ÓO]N|$)",
        text, re.I | re.S,
    )
    if not m:
        return []
    block = m.group(1)
    rows = []
    row_re = re.compile(
        r"^\s*(RS|FI|OT|RE|IN)\s{2,}([A-ZÁÉÍÓÚÑ ()\-,]+?)\s{2,}([0-9/]+)\s{2,}([A-ZÁÉÍÓÚÑ \-,()]+?)\s*$",
        re.M,
    )
    for mo in row_re.finditer(block):
        rate, resultado, fecha, inst = mo.groups()
        rows.append({
            "rate": rate,
            "resultado": resultado.strip(),
            "fecha": parse_date(fecha),
            "institucion_analisis": inst.strip(),
        })
    return rows


# ---------------------------------------------------------------------------
# Section 18/19 — CONCLUSIONES DEL ANÁLISIS (free text)
# ---------------------------------------------------------------------------

def parse_conclusiones(text: str) -> str | None:
    m = re.search(
        r"\d+\.\s*CONCLUSIONES DEL AN[ÁA]LISIS\s*:?\s*(.+?)(?:\d+\.\s*INSTITUCIONES|\d+\.\s*RESUMEN|\d+\.\s*HISTORIAL|\d+\.\s*FUNCIONARIO|\d+\.\s*OBSERVACIONES|$)",
        text, re.I | re.S,
    )
    if not m:
        return None
    return normalize_ws(m.group(1))


# ---------------------------------------------------------------------------
# Section 19/20 — INSTITUCIONES QUE PARTICIPAN
# ---------------------------------------------------------------------------

def parse_instituciones(text: str) -> dict | None:
    m = re.search(
        r"\d+\.\s*INSTITUCIONES QUE PARTICIPAN EN LA EJECUCI[ÓO]N DEL (?:PROYECTO|PROGRAMA)\s*(.+?)"
        r"(?:\d+\.\s*RESUMEN|\d+\.\s*HISTORIAL|\d+\.\s*FUNCIONARIO|\d+\.\s*OBSERVACIONES|$)",
        text, re.I | re.S,
    )
    if not m:
        return None
    block = m.group(1)
    formuladora = first(r"Instituci[oó]n Formuladora de la Etapa\s+(.+?)(?:\n\s*\n|\n\s*Instituciones)", block, flags=re.I | re.S)
    financieras = first(r"Instituciones Financieras\s+(.+?)(?:\n\s*\n|\n\s*Instituciones)", block, flags=re.I | re.S)
    tecnicas = first(r"Instituciones T[ée]cnicas\s+(.+?)(?:\n\s*\n|$)", block, flags=re.I | re.S)
    fin_list = [s.strip() for s in re.split(r"\n+", financieras) if s.strip()] if financieras else None
    tec_list = [s.strip() for s in re.split(r"\n+", tecnicas) if s.strip()] if tecnicas else None
    return {
        "institucion_formuladora": normalize_ws(formuladora),
        "instituciones_financieras": fin_list,
        "instituciones_tecnicas": tec_list,
    }


# ---------------------------------------------------------------------------
# Section 20/23 — RESUMEN DE LOS RESULTADOS
# ---------------------------------------------------------------------------

def parse_resumen(text: str) -> dict | None:
    m = re.search(
        r"\d+\.\s*RESUMEN DE LOS RESULTADOS DEL (?:PROYECTO|PROGRAMA)\s*(.+?)"
        r"(?:\d+\.\s*HISTORIAL|\d+\.\s*FUNCIONARIO|\d+\.\s*OBSERVACIONES|$)",
        text, re.I | re.S,
    )
    if not m:
        return None
    block = m.group(1)

    fecha = parse_date(first(r"Fecha de la Informaci[oó]n\s+([0-9/]+)", block))
    duracion = parse_int(first(r"Duraci[oó]n\s+(\d+)\s*Meses", block))

    h = parse_int(first(r"Hombres\s*:\s*([\d.,]+)", block))
    mu = parse_int(first(r"Mujeres\s*:\s*([\d.,]+)", block))
    tot = parse_int(first(r"Total\s*:\s*([\d.,]+)", block))

    proposito = normalize_ws(first(r"Prop[oó]sito\s+(.+?)(?:\n\s*Indicadores de Prop[oó]sito|\n\s*Componentes|$)",
                                   block, flags=re.I | re.S))
    indic_prop = _parse_list_items(first(r"Indicadores de Prop[oó]sito\s+(.+?)(?:\n\s*Componentes|\n\s*Indicadores de Componentes|$)",
                                         block, flags=re.I | re.S))
    componentes = _parse_list_items(first(r"\n\s*Componentes\s+(.+?)(?:\n\s*Indicadores de Componentes|$)",
                                          block, flags=re.I | re.S))
    indic_comp = _parse_list_items(first(r"Indicadores de Componentes\s+(.+?)$",
                                         block, flags=re.I | re.S))

    return {
        "fecha_de_la_informacion": fecha,
        "duracion_meses": duracion,
        "beneficiarios_directos": {"hombres": h, "mujeres": mu, "total": tot},
        "indicadores": {
            "proposito": proposito,
            "indicadores_proposito": indic_prop,
            "componentes": componentes,
            "indicadores_componentes": indic_comp,
        },
    }


def _parse_list_items(s: str | None) -> list[str]:
    """Parse a list-like FICHA section into items.

    Accepts items separated by any of the markers used in FICHA IDI documents:

      ``1.``  ``1 -``  ``1)``  ``- ``  ``• ``

    The marker must sit at item boundary — start-of-string, newline, or after at
    least three spaces — so we don't break paragraphs that happen to contain
    ``"- "`` or ``"32.5"`` mid-sentence. Single-paragraph values become a list of
    length one (which is the correct behaviour for ``Indicadores de Propósito``
    when the FICHA prints a single block of prose).
    """
    if not s:
        return []
    items = re.split(
        r"(?:^|\n|\s{3,})\s*(?:\d+\s*[.\-)]\s+|[\-•]\s+)",
        s,
    )
    return [normalize_ws(x) for x in items if x and x.strip()]


# ---------------------------------------------------------------------------
# Section 21/24 — HISTORIAL DE PRESUPUESTO
# ---------------------------------------------------------------------------

def parse_historial(text: str) -> dict | None:
    m = re.search(
        r"\d+\.\s*HISTORIAL DE PRESUPUESTO DEL (?:PROYECTO|PROGRAMA) PARA LA ETAPA SELECCIONADA\s*(.+?)"
        r"(?:\d+\.\s*FUNCIONARIO|\d+\.\s*OBSERVACIONES|$)",
        text, re.I | re.S,
    )
    if not m:
        return None
    block = m.group(1)

    a_m = re.search(r"A\.\s*Solicitudes de Financiamiento(.+?)(?:B\.\s*Ejecuci[oó]n|$)", block, re.I | re.S)
    b_m = re.search(r"B\.\s*Ejecuci[oó]n Presupuestaria(.+?)$", block, re.I | re.S)

    solicitudes = []
    if a_m:
        sa = a_m.group(1)
        row_re = re.compile(
            r"^\s*(\d{4})\s+(RS|FI|OT|RE|IN)?\s*([\d.,\-]*)\s+([\d.,\-]*)\s+([\d.,\-]*)\s+([\d.,\-]*)\s+([\d.,\-]*)\s+([\d.,\-]*)\s+([\d.,\-]*)\s*$",
            re.M,
        )
        for mo in row_re.finditer(sa):
            anio, rate, p1, p2, p3, p4, p5, p6, p7 = mo.groups()
            solicitudes.append({
                "anio_idi": int(anio),
                "rate": rate or None,
                "pagado_anios_anteriores_M$": parse_int(p1),
                "solicitado_anio_M$": parse_int(p2),
                "solicitado_anio_MUS$": parse_float(p3),
                "solicitado_anios_siguientes_M$": parse_int(p4),
                "solicitado_anios_siguientes_MUS$": parse_float(p5),
                "costo_total_M$": parse_int(p6),
                "costo_total_MUS$": parse_float(p7),
            })

    ejecucion = []
    if b_m:
        eb = b_m.group(1)
        row_re = re.compile(
            r"^\s*(\d{4})\s+([A-ZÁÉÍÓÚÑ\.\-]+)\s+(RS|FI|OT|RE|IN)?\s*(M\$|MUS\$|US\$)?\s*([\d.,\-]+)\s+([\d.,\-]+)\s*$",
            re.M,
        )
        for mo in row_re.finditer(eb):
            anio, fuente, rate, mon, mv, gt = mo.groups()
            ejecucion.append({
                "anio_asignacion": int(anio),
                "fuente": fuente.strip(),
                "rate": rate or None,
                "moneda": ("MUS$" if mon and "US" in mon else "M$") if mon else None,
                "monto_vigente": parse_float(mv),
                "gasto_total": parse_float(gt),
            })

    if not solicitudes and not ejecucion:
        return None
    return {
        "solicitudes_financiamiento": solicitudes,
        "ejecucion_presupuestaria": ejecucion,
    }


# ---------------------------------------------------------------------------
# Section 22/25 — FUNCIONARIO RESPONSABLE
# ---------------------------------------------------------------------------

def parse_funcionario(text: str) -> dict | None:
    m = re.search(
        r"\d+\.\s*FUNCIONARIO RESPONSABLE\s*(.+?)"
        r"(?:\d+\.\s*OBSERVACIONES|$)",
        text, re.I | re.S,
    )
    if not m:
        return None
    block = m.group(1)
    # Cheap guard: the section is meaningful only when an email is present. This
    # also avoids catastrophic backtracking that the previous 5-field lazy regex
    # exhibited on lines missing the @ anchor.
    if "@" not in block:
        return None
    email_re = re.compile(r"[\w\.\-]+@[\w\.\-]+")
    sep = re.compile(r"\s{2,}")
    for line in block.splitlines():
        ln = line.rstrip()
        if "@" not in ln or not email_re.search(ln):
            continue
        parts = [p for p in sep.split(ln.strip()) if p]
        if len(parts) < 5:
            continue
        # The PDF prints exactly 5 fields per row: Nombre, Institución, Cargo,
        # Fono, Correo. If pdftotext gave us extra fragments we glue them back
        # into the middle (Institución + Cargo are most prone to extra splits).
        nombre, *middle, fono, correo = parts
        if nombre.lower() == "nombre":
            continue
        if not email_re.fullmatch(correo):
            continue
        # middle has at least 2 elements (institución, cargo); collapse anything
        # extra into cargo so we don't lose data.
        if len(middle) < 2:
            continue
        institucion = middle[0]
        cargo = " ".join(middle[1:]) if len(middle) > 1 else None
        return {
            "nombre": nombre,
            "institucion": institucion,
            "cargo": cargo,
            "fono": fono,
            "correo_electronico": correo,
        }
    return None


# ---------------------------------------------------------------------------
# Section 26 (or 19) — OBSERVACIONES DE [NO] ADMISIBILIDAD
# ---------------------------------------------------------------------------

def parse_observaciones(text: str) -> dict | None:
    m = re.search(
        r"\d+\.\s*OBSERVACIONES DE (NO )?ADMISIBILIDAD\s*:?\s*(.+?)$",
        text, re.I | re.S,
    )
    if not m:
        return None
    no_flag = m.group(1) is not None
    block = m.group(2)

    # Split into preamble + numbered observations
    parts = re.split(r"\n\s*(\d+)\.\s*", block, maxsplit=0)
    preamble = normalize_ws(parts[0]) if parts and parts[0].strip() else None
    observaciones = []
    for i in range(1, len(parts) - 1, 2):
        try:
            num = int(parts[i])
        except ValueError:
            continue
        texto = normalize_ws(parts[i + 1])
        if texto:
            observaciones.append({"numero": num, "texto": texto})

    if preamble is None and not observaciones:
        return None
    return {
        "admitido": not no_flag,
        "preamble": preamble,
        "observaciones": observaciones,
    }


# ---------------------------------------------------------------------------
# Stub helpers
# ---------------------------------------------------------------------------

def _empty(template: dict) -> dict:
    """Deep copy of a template constant (avoid mutation of module-level dict)."""
    return json.loads(json.dumps(template))


# ---------------------------------------------------------------------------
# Top-level: parse a single etapa block
# ---------------------------------------------------------------------------

def parse_etapa(etapa_text: str, etapa_index: int) -> dict:
    iniciativa = parse_iniciativa(etapa_text)
    clasificacion, ubicacion, vinculacion = parse_classification_and_location(etapa_text)
    narrative = parse_narrative(etapa_text)
    return {
        "etapa_index": etapa_index,
        "header": parse_header(etapa_text),
        "iniciativa": iniciativa,
        "clasificacion": clasificacion,
        "ubicacion": ubicacion,
        "vinculacion": vinculacion,
        "narrative": narrative,
        "solicitud_financiamiento": parse_financiamiento(etapa_text),
        "programacion_inversion": parse_programacion(etapa_text),
        "registro_sni": parse_registro_sni(etapa_text),
        "resultado_analisis": parse_resultado_analisis(etapa_text),
        "conclusiones_analisis": parse_conclusiones(etapa_text),
        "instituciones_participantes": parse_instituciones(etapa_text),
        "resumen_resultados": parse_resumen(etapa_text),
        "historial_presupuesto": parse_historial(etapa_text),
        "funcionario_responsable": parse_funcionario(etapa_text),
        "observaciones_admisibilidad": parse_observaciones(etapa_text),
        "georreferenciacion_section_present": bool(re.search(r"\d+\.\s*GEORREFERENCIACI[ÓO]N", etapa_text)),
        "extras": [],
    }


# ---------------------------------------------------------------------------
# Top-level: parse a PDF
# ---------------------------------------------------------------------------

def parse_ficha(pdf_path: str | Path) -> dict:
    pdf_path = Path(pdf_path)
    text = pdftotext(pdf_path, layout=True)
    size_bytes = pdf_path.stat().st_size

    template_variant = detect_template_variant(text, size_bytes)
    template_version = detect_template_version(text)

    fc = parse_date(first(r"FECHA CREACI[ÓO]N SOLICITUD\s*:\s*([0-9/]+)", text))
    fm = parse_date(first(r"FECHA [ÚU]LTIMA MODIFICACI[ÓO]N\s*:\s*([0-9/]+)", text))

    warnings: list[dict] = []

    if template_variant == "STUB":
        etapas = []
    else:
        etapa_blocks = split_etapas(text)

        # Detect byte-identical multi-etapa duplication. About 1.7% of the corpus
        # ships the FICHA twice in the same PDF; downstream consumers usually want
        # to dedupe.
        if len(etapa_blocks) >= 2:
            normalized_blocks = [normalize_ws(b) or "" for b in etapa_blocks]
            if len(set(normalized_blocks)) == 1:
                warnings.append({
                    "code": "multi_etapa_identical_blocks",
                    "message": (
                        f"PDF contains {len(etapa_blocks)} FICHA blocks that are "
                        "textually identical after whitespace normalisation; "
                        "downstream consumers may want to deduplicate."
                    ),
                    "section": None,
                })

        etapas = [parse_etapa(b, i) for i, b in enumerate(etapa_blocks)]

        # Surface unrecoverable nombre extraction failures so schema-validation
        # errors carry a self-explanatory cause.
        for i, e in enumerate(etapas):
            if e["iniciativa"]["nombre"] is None:
                warnings.append({
                    "code": "nombre_extraction_failed",
                    "message": (
                        "iniciativa.nombre could not be extracted from section 1; "
                        "the two-column layout did not match any known pattern."
                    ),
                    "section": "1",
                })

    return {
        "$schema_version": SCHEMA_VERSION,
        "extraction": {
            "parser_version": PARSER_VERSION,
            "parsed_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "source_pdf": {
                "filename": pdf_path.name,
                "size_bytes": size_bytes,
                "n_pages": pdf_pagecount(pdf_path) or 1,
                "sha256": sha256_of(pdf_path),
                "producer": pdf_producer(pdf_path),
            },
            "warnings": warnings,
        },
        "document": {
            "report_type": "FICHA-IDI",
            "template_variant": template_variant,
            "template_version": template_version,
            "n_etapas_in_pdf": len(etapas),
            "fecha_creacion_solicitud": fc,
            "fecha_ultima_modificacion": fm,
        },
        "etapas": etapas,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _validate(record: dict, schema_path: Path) -> list[str]:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return ["jsonschema not installed; skipped validation"]
    with open(schema_path) as f:
        schema = json.load(f)
    v = Draft202012Validator(schema)
    return [f"{'/'.join(str(p) for p in e.absolute_path)}: {e.message}"
            for e in sorted(v.iter_errors(record), key=lambda e: list(e.path))]


def main():
    ap = argparse.ArgumentParser(description="Parse a Reporte Ficha IDI PDF to JSON.")
    ap.add_argument("pdf", help="Path to PDF file")
    ap.add_argument("-o", "--output", help="Output JSON path (default: stdout)")
    ap.add_argument("--validate", action="store_true",
                    help="Validate output against ficha_idi.schema.v1.0.0.json")
    ap.add_argument("--schema", default=None,
                    help="Path to schema (default: ../schemas/ficha_idi.schema.v1.0.0.json)")
    args = ap.parse_args()

    record = parse_ficha(args.pdf)

    if args.validate:
        schema_path = Path(args.schema) if args.schema else (
            Path(__file__).resolve().parent.parent / "schemas" / "ficha_idi.schema.v1.0.0.json"
        )
        errors = _validate(record, schema_path)
        if errors:
            sys.stderr.write(f"VALIDATION FAILED ({len(errors)} errors):\n")
            for e in errors[:30]:
                sys.stderr.write(f"  - {e}\n")
            sys.exit(2)

    out = json.dumps(record, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(out)
    else:
        print(out)


if __name__ == "__main__":
    main()
