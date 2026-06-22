"""Integrate the four Chile project/award reviews into one row-per-project staging frame
for modelled.finance_project (design section 3.2 / 4.2).

Each upstream loader hands in its source's raw rows tagged with `_source_dataset`:
  - cl-ssg/cl-ssg-projects   (BIP / SNI public-investment projects)   + its per-project action matches
  - gcf/gcf-projects         (GCF Chile slice, intermediated multilateral)
  - cl-mma/cl-mma-fpa-awards  (FPA competitive awards)
  - cl-conaf/cl-conaf-bn-awards (CONAF Bosque Nativo competitive awards)
Plus the cl-ocha-ab locode lookup (comuna -> city locode) for actor_id.

The cleaning is uniform-ish across sources but each source has a genuinely different shape,
so the per-source shaping lives here (once), keyed on `_source_dataset`: align to the
finance_project superset, normalize controlled vocab to canonical bases, caps-normalize the
all-caps source text, assemble the i18n + funding_sources JSONB, resolve the locode, attach
the action match, union. Off-list / unmodeled is dropped (no source_extras catch-all).
"""
import json
import re
import unicodedata

import pandas as pd

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

# ---- source dataset ids (must match the loaders' _source_dataset and the catalog) ----
BIP = "cl-ssg/cl-ssg-projects"
GCF = "gcf/gcf-projects"
FPA = "cl-mma/cl-mma-fpa-awards"
CONAF = "cl-conaf/cl-conaf-bn-awards"

SUPERSET = [
    "source_project_id", "project_name", "project_name_i18n",
    "sector", "sector_i18n", "jurisdiction", "actor_id", "lifecycle_stage",
    "evaluation_verdict", "cost_total", "amount_committed", "amount_paid", "amount_unit",
    "duration_months", "owner_formulator", "funding_channel", "funding_sources",
    "country_code", "source_dataset",
]
# action matches are emitted separately into finance_project_action by
# transformers/transform_finance_project_action.py (room for multiple matches per project).

# ---- canonical vocab maps ----------------------------------------------------------
# lifecycle_stage canonical: formulated / appraised / financed / in-execution / completed
BIP_STAGE = {
    "PERFIL": "formulated", "PREFACTIBILIDAD": "appraised", "FACTIBILIDAD": "appraised",
    "DISENO": "financed", "DISEÑO": "financed", "EJECUCION": "in-execution",
    "TERMINADO": "completed",
}
GCF_STAGE = {"under implementation": "in-execution", "completed": "completed"}  # "approved ..." -> financed

CONAF_OBJETIVO_EN = {
    "PRODUCCION MADERERA": "Timber production",
    "PRODUCCION NO MADERERA": "Non-timber forest production",
    "BOSQUE PRESERVACION Y FORMACIONES XEROFITICAS DE ALTO VALOR ECOLOGICO":
        "High-ecological-value native forest and xerophytic preservation",
}

# tokens kept upper in caps-normalization; small words kept lower
KEEP_UPPER = {"LED", "RSD", "APR", "FNDR", "FRIL", "PMU", "PMB", "EFE", "RM", "RMS", "GCF",
              "FPA", "CONAF", "UTM", "CLP", "USD", "SAP", "ERP", "S.A.", "S.A", "II", "III",
              "IV", "V", "VI", "VII", "VIII", "IX", "XI", "XII", "XIII", "XIV", "XV", "ZOFRI"}
LOWER_SMALL = {"de", "del", "la", "las", "el", "los", "y", "e", "en", "para", "por", "con",
               "a", "of", "the", "and", "in", "for"}


def demojibake(s):
    """Repair the classic UTF-8-as-Latin-1 double encoding (Ã±->ñ, PÃšBLICO->PÚBLICO) without ftfy."""
    if s and any(m in s for m in ("Ã", "Â", "â€")):
        try:
            return s.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return s
    return s


def clean_text(s):
    """demojibake + strip the BIP administrative suffix + whitespace; no case change."""
    if s is None or str(s).strip() == "" or str(s).lower() == "nan":
        return None
    t = demojibake(str(s))
    t = re.sub(r"\s*A[ñn]o y Etapa a Financiar:.*$", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s+\d{4}-(?:EJECUCION|DISE[ÑN]O|PERFIL|PREFACTIBILIDAD|FACTIBILIDAD)\s*$", "", t)
    t = re.sub(r"\s{2,}", " ", t).strip(" \t,.-")
    return t or None


def title_case(s):
    """Caps-normalize: title-case only all-caps source text; keep mixed-case text as-is."""
    t = clean_text(s)
    if t is None:
        return None
    letters = [c for c in t if c.isalpha()]
    if letters and not all(c.isupper() for c in letters):
        return t  # already mixed case (e.g. FPA creative titles) -> leave alone
    out = []
    for i, w in enumerate(t.split()):
        u = re.sub(r"[.,]", "", w).upper()
        if u in KEEP_UPPER or re.fullmatch(r"[IVX]{2,}", u):
            out.append(w.upper())
        elif w.lower() in LOWER_SMALL and i != 0:
            out.append(w.lower())
        else:
            out.append(w.capitalize())
    return " ".join(out)


def numstr(v):
    """Numeric value as a clean text token for the text staging frame (the SQL casts it)."""
    n = num(v)
    if n is None:
        return None
    return str(int(n)) if float(n).is_integer() else str(n)


def comuna_clean(s):
    """BIP comuna sometimes carries a ' - REGION ...' suffix; keep just the comuna name."""
    t = clean_text(s)
    if not t:
        return None
    return re.split(r"\s+-\s+", t)[0].strip()


def deacc(s):
    return "".join(c for c in unicodedata.normalize("NFKD", str(s or "")) if not unicodedata.combining(c))


def slug(s):
    s = deacc(s)
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")[:120]


def num(v):
    if v is None or str(v).strip() in ("", "nan", "None"):
        return None
    try:
        f = float(str(v).replace(",", ""))
        return f
    except ValueError:
        return None


def i18n(es, en):
    """Build a {es, en} dict, omitting empty members. Returns JSON text or None."""
    d = {}
    if es:
        d["es"] = es
    if en:
        d["en"] = en
    return json.dumps(d, ensure_ascii=False) if d else None


def base_en(en, es):
    """The displayed base value is ENGLISH; fall back to the source language only if no en yet."""
    return en or es


def build_locode_lookup(df):
    """comuna_code (CL+CUT) and normalized comuna_name -> locode."""
    by_code, by_name = {}, {}
    if df is None or not len(df):
        return by_code, by_name
    for _, r in df.iterrows():
        loc = (r.get("locode") or None)
        if not loc or str(loc).strip() in ("", "None", "nan"):
            continue
        loc = str(loc).strip()
        code = str(r.get("comuna_code") or "").strip()
        if code:
            by_code[code] = loc
        nm = deacc(r.get("comuna_name") or "").upper().strip()
        if nm:
            by_name[nm] = loc
    return by_code, by_name


# ---- per-source row shaping --------------------------------------------------------
def _bip(r, by_name):
    code = (r.get("codigo_bip") or "").strip()
    name_es, name_en = title_case(r.get("nombre")), clean_text(r.get("nombre_en"))
    sector_es, sector_en = title_case(r.get("sector")), clean_text(r.get("sector_en"))
    comuna = comuna_clean(r.get("comuna"))
    fuentes = clean_text(r.get("fuentes_financiamiento"))
    fs = []
    if fuentes:
        fs.append({"source_label": fuentes, "funder_name": fuentes,
                   "source_opportunity_id": None, "amount": None,
                   "amount_unit": "CLP_millions", "paid_amount": None,
                   "cycle": (r.get("ano_postulacion") or None)})
    return {
        "source_project_id": code,
        "project_name": base_en(name_en, name_es),
        "project_name_i18n": i18n(name_es, name_en),
        "sector": base_en(sector_en, sector_es),
        "sector_i18n": i18n(sector_es, sector_en),
        "jurisdiction": title_case(comuna) if comuna else title_case(r.get("region")),
        "actor_id": by_name.get(deacc(comuna).upper().strip()) if comuna else None,
        "lifecycle_stage": BIP_STAGE.get(deacc(r.get("etapa_actual") or "").upper().strip()),
        "evaluation_verdict": clean_text(r.get("rate_resultado")),
        "cost_total": numstr(r.get("costo_total_M_CLP")),
        "amount_committed": None, "amount_paid": None,
        "amount_unit": "CLP_millions" if num(r.get("costo_total_M_CLP")) is not None else None,
        "duration_months": numstr(r.get("duracion_meses")),
        "owner_formulator": title_case(r.get("institucion_formuladora")),
        "funding_channel": "public investment",
        "funding_sources": json.dumps(fs, ensure_ascii=False) if fs else None,
    }


def _gcf(r):
    name = clean_text(r.get("title"))           # GCF is natively English
    sect = clean_text(r.get("gpc_sector"))
    ae = clean_text(r.get("accredited_entity"))
    fs = [{"source_label": ae or "GCF", "funder_name": "Green Climate Fund",
           "source_opportunity_id": None, "amount": None, "amount_unit": "USD",
           "paid_amount": None, "cycle": None}]
    return {
        "source_project_id": (r.get("fp_id") or "").strip(),
        "project_name": name, "project_name_i18n": i18n(name, name),
        "sector": sect, "sector_i18n": i18n(sect, sect),
        "jurisdiction": clean_text(r.get("chile_scope")) or "Chile",
        "actor_id": None,
        "lifecycle_stage": GCF_STAGE.get((r.get("status") or "").strip().lower(), "financed"),
        "evaluation_verdict": None,
        "cost_total": None, "amount_committed": None, "amount_paid": None, "amount_unit": None,
        "duration_months": None,
        "owner_formulator": ae,
        "funding_channel": "intermediated multilateral",
        "funding_sources": json.dumps(fs, ensure_ascii=False),
    }


def _fpa(r, by_code):
    name_es, name_en = clean_text(r.get("nombre_proyecto")), clean_text(r.get("nombre_proyecto_en"))
    sect = clean_text(r.get("gpc_sector"))      # GPC token, already English
    cut = (r.get("comuna_cut") or "").strip()
    monto = num(r.get("monto_clp"))
    fs = [{"source_label": clean_text(r.get("concurso")) or f"FPA {r.get('concurso_year') or ''}".strip(),
           "funder_name": "MMA Fondo de Proteccion Ambiental",
           "source_opportunity_id": None, "amount": monto, "amount_unit": "CLP",
           "paid_amount": None, "cycle": (r.get("concurso_year") or None)}]
    return {
        "source_project_id": (r.get("folio") or "").strip(),
        "project_name": base_en(name_en, name_es),
        "project_name_i18n": i18n(name_es, name_en),
        "sector": sect, "sector_i18n": i18n(sect, sect),
        "jurisdiction": title_case(r.get("comuna")),
        "actor_id": by_code.get(f"CL{cut.zfill(5)}") if cut else None,  # CUT padded to 5 digits
        "lifecycle_stage": "financed",
        "evaluation_verdict": None,
        "cost_total": None, "amount_committed": numstr(r.get("monto_clp")), "amount_paid": None,
        "amount_unit": "CLP" if monto is not None else None,
        "duration_months": None,
        "owner_formulator": title_case(r.get("organizacion")),
        "funding_channel": "competitive fund",
        "funding_sources": json.dumps(fs, ensure_ascii=False),
    }


def _conaf(r):
    obj = (r.get("objetivo_manejo") or "").strip().upper()
    concurso = clean_text(r.get("concurso")) or "Bosque Nativo"
    region = title_case(r.get("region"))
    ingreso = (r.get("numero_ingreso") or "").strip()
    name_es = f"{title_case(obj)} - Bosque Nativo {concurso}" + (f" ({region})" if region else "") + (f" #{ingreso}" if ingreso else "")
    name_en = f"{CONAF_OBJETIVO_EN.get(obj, title_case(obj))} - Native Forest {concurso}" + (f" ({region})" if region else "") + (f" #{ingreso}" if ingreso else "")
    monto = num(r.get("monto_total_utm"))
    bono = (r.get("tiene_bonificacion_saff") or "").strip().lower()
    stage = "in-execution" if bono == "si" or num(r.get("numero_bonos")) else "financed"
    fs = [{"source_label": f"Bosque Nativo {concurso}",
           "funder_name": "CONAF Fondo de Conservacion y Manejo Sustentable del Bosque Nativo",
           "source_opportunity_id": None, "amount": monto, "amount_unit": "UTM",
           "paid_amount": None, "cycle": (r.get("ano") or None)}]
    return {
        "source_project_id": (r.get("award_id") or "").strip(),
        "project_name": name_en, "project_name_i18n": i18n(name_es, name_en),
        "sector": "afolu", "sector_i18n": i18n("afolu", "afolu"),
        "jurisdiction": region,
        "actor_id": None,
        "lifecycle_stage": stage,
        "evaluation_verdict": None,
        "cost_total": None, "amount_committed": numstr(r.get("monto_total_utm")), "amount_paid": None,
        "amount_unit": "UTM" if monto is not None else None,
        "duration_months": None,
        "owner_formulator": title_case(r.get("presenter_type")),
        "funding_channel": "competitive fund",
        "funding_sources": json.dumps(fs, ensure_ascii=False),
    }


SHAPERS = {BIP: _bip, GCF: _gcf, FPA: _fpa, CONAF: _conaf}


def _frame_source(df):
    return df["_source_dataset"].iloc[0] if df is not None and len(df) else None


@transformer
def merge_finance_project(*frames, **kwargs):
    # project frames are tagged _source_dataset; the locode lookup frame is identified by its
    # columns. (Action matches are handled in the separate finance_project_action branch, so any
    # match frame passed here is ignored.)
    proj_frames, locode_df = [], None
    for df in frames:
        if df is None or not len(df):
            continue
        cols = set(df.columns)
        if "locode" in cols and "comuna_code" in cols:
            locode_df = df
        elif "_source_dataset" in cols:
            proj_frames.append(df)

    by_code, by_name = build_locode_lookup(locode_df)

    rows = []
    for df in proj_frames:
        sd = _frame_source(df)
        shaper = SHAPERS.get(sd)
        if shaper is None:
            print(f"[WARN] no shaper for source {sd}; skipping {len(df)} rows")
            continue
        df = df.where(pd.notna(df), None)
        for _, r in df.iterrows():
            r = r.to_dict()
            out = shaper(r, by_name) if sd == BIP else (shaper(r, by_code) if sd == FPA else shaper(r))
            if not out.get("source_project_id") or not out.get("project_name"):
                continue  # drop rows with no natural key or no name
            out["country_code"] = "CL"
            out["source_dataset"] = sd
            for c in SUPERSET:
                out.setdefault(c, None)
            rows.append(out)

    result = pd.DataFrame(rows, columns=SUPERSET)
    before = len(result)
    result = result.drop_duplicates(subset=["source_dataset", "source_project_id"], keep="first").reset_index(drop=True)
    n_actor = result["actor_id"].notna().sum()
    print(f"finance_project: {len(result)} rows from {result['source_dataset'].nunique()} sources "
          f"({before - len(result)} dup keys dropped); actor_id on {n_actor}")
    for sd, g in result.groupby("source_dataset"):
        print(f"  {sd}: {len(g)} rows")
    return result


@test
def test_output(output, *args) -> None:
    assert output is not None and len(output) > 0, "no projects integrated"
    for col in ("source_project_id", "project_name", "source_dataset"):
        assert output[col].notna().all(), f"missing/empty required column {col}"
    assert not output.duplicated(subset=["source_dataset", "source_project_id"]).any(), "dup natural keys"
