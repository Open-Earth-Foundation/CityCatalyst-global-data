"""Integrate the per-source finance frames into one row-per-opportunity staging frame.

Each upstream loader hands in its source's raw rows tagged with `_source_dataset`. The
cleaning is uniform across sources, so it lives here (once): align heterogeneous columns to
the audited superset, normalize controlled vocabularies to canonical bases (multi-valued ones
to JSON arrays), keep verbatim detail, stash unmodeled columns in source_extras, union, dedupe.
"""
import json
import re
import unicodedata

import pandas as pd

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

# review column -> superset column. Inlined (Mage blocks have no __file__; no local-repo reads).
SYNONYMS = {
    "fund_name": "opportunity_name", "program": "opportunity_name", "program_name": "opportunity_name",
    "funder_institution": "funder_name", "funder_name": "funder_name", "funder": "funder_name",
    "provider": "provider",
    "instrument_type": "instrument", "instrument": "instrument",
    "gpc_sectors": "gpc_sectors", "program_gpc_sector": "gpc_sectors",
    "thematic_lines": "thematic_lines",
    "eligible_actor": "eligible_actor", "eligible_actor_detail": "eligible_actor_detail",
    "access_pathway": "access_pathway",          # consumed for city_application, not a column
    "open_date": "open_date", "close_date": "close_date",
    # staging avoids the reserved word status (Mage renames it to _status); SQL maps it back
    "status": "opportunity_status", "status_as_of": "status_as_of",
    "recurrence": "recurrence",
    "amount_clp": "amount", "amount_note": "amount_note",
    "climate_relevance": "climate_relevance", "climate_relevance_norm": "climate_relevance",
    "program_climate_relevance": "climate_relevance",
    "specificity": "specificity",
    "source_url": "source_url", "resolucion_url": "legal_basis_url",
    "notes": "notes",
}
SUPERSET = list(dict.fromkeys(SYNONYMS.values()))
# folded into data_quality_flags (incl. detail_level = extraction completeness)
DQ_COLS = {"amount_suspect", "status_section_conflict", "detail_level"}
# dropped from the model: program_family, lifecycle, next_call_estimate. Their source columns are
# not mapped, so they ride along untouched in source_extras (nothing lost).

CLIMATE_SYN = {"explicit_adjacent": "climate_adjacent"}

# eligible_actor: ordered keyword -> canonical actor (all matches kept; full text -> detail)
ELIGIBLE_RULES = [
    ("municipal", "municipality"), ("comuna", "municipality"), ("alcalde", "municipality"),
    ("regional government", "regional_government"), ("gore", "regional_government"),
    ("indigen", "indigenous_community"), ("indígen", "indigenous_community"),
    ("household", "household"), ("hogar", "household"),
    ("landowner", "private_firm"), ("propietario", "private_firm"),
    ("operator", "operator"), ("operador", "operator"),
    ("firm", "private_firm"), ("sme", "private_firm"), ("empresa", "private_firm"),
    ("entrepreneur", "private_firm"), ("developer", "private_firm"), ("concesionario", "private_firm"),
    ("universit", "research_university"), ("research", "research_university"), ("investigador", "research_university"),
    ("non-profit", "ngo"), ("ngo", "ngo"),
    ("cooperativ", "community_org"), ("comité", "community_org"), ("comite", "community_org"),
    ("community", "community_org"), ("comunidad", "community_org"), ("junta", "community_org"),
    ("citizen", "community_org"), ("organiza", "community_org"), ("usuarios de agua", "community_org"),
    ("school", "public_agency"), ("sostenedor", "public_agency"), ("public agency", "public_agency"),
    ("public_agency", "public_agency"), ("public services", "public_agency"), ("mandante", "public_agency"),
    ("unspecified", "unspecified"),
]


def slug(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")[:120]


def city_application(access_pathway, eligible_actor):
    """Multi-valued: a fund can be e.g. direct or facilitated. Returns a list."""
    t = f"{access_pathway} {eligible_actor}".lower()
    modes = []
    if "direct" in t or "applies directly" in t or t.strip().startswith("yes"):
        modes.append("direct")
    if "facilitat" in t or "enabl" in t or "owner" in t or "household" in t:
        modes.append("facilitated")
    if "intermediat" in t or "operator" in t or "accredited" in t:
        modes.append("intermediated")
    return modes or ["direct"]


def classify_channel_tier(name, source_dataset):
    """Heuristic — production should read this from the source review. Country-agnostic values."""
    n, sd = str(name).lower(), source_dataset.lower()
    if "8%" in n:
        return "competitive fund", "competitive"
    if any(k in n for k in ("fndr", "fril", "frpd")) or "gore" in sd or "subdere" in sd:
        return "public investment", "gated"   # CL specifics (BIP/SNI) noted in the review, not the value
    if "mtt" in sd:
        return "intermediated", "intermediated"
    return "competitive fund", "competitive"


def _base(raw):
    """The canonical token before any qualifier: grant (capital transfer) -> grant."""
    head = re.split(r"\s*[(/;+]", str(raw), 1)[0].strip().lower()
    return re.sub(r"[\s\-]+", "_", head)


def _norm(raw, syn=None):
    """Return (canonical_base, verbatim) — verbatim kept only when it carried more than the base."""
    if raw is None or str(raw).strip() == "":
        return None, None
    base = (syn or {}).get(_base(raw), _base(raw))
    verbatim = raw if re.sub(r"[\s\-]+", "_", str(raw).strip().lower()) != base else None
    return base, verbatim


def _norm_eligible(raw):
    """All actors by keyword (multi-valued -> list); full text preserved in eligible_actor_detail."""
    if raw is None or str(raw).strip() == "":
        return None, None
    t = str(raw).lower()
    actors = []
    for kw, canon in ELIGIBLE_RULES:
        if kw in t and canon not in actors:
            actors.append(canon)
    if not actors:
        return ["unspecified"], raw
    detail = raw if t.strip() not in actors else None
    return actors, detail


def _align_row(r, source_dataset):
    out = {c: None for c in SUPERSET}
    dq, extras = {}, {}
    for col, val in r.items():
        if col == "_source_dataset" or val is None or str(val).strip() == "":
            continue
        if col in SYNONYMS:
            tgt = SYNONYMS[col]
            if out.get(tgt) in (None, ""):
                out[tgt] = val
        elif col in DQ_COLS:
            dq[col] = val
        else:
            extras[col] = val                       # nothing lost: unmodeled cols -> source_extras
    out["source_dataset"] = source_dataset
    out["country_code"] = "CL"
    out["source_opportunity_id"] = f"{source_dataset.split('/')[0]}-{slug(out['opportunity_name'])}"
    # city_application is multi-valued (JSON array); derive from access_pathway, then drop the raw pathway
    out["city_application"] = json.dumps(city_application(out.get("access_pathway"), out.get("eligible_actor")))
    access_pathway = out.pop("access_pathway", None)
    if access_pathway:
        extras["access_pathway_verbatim"] = access_pathway
    ch, tier = classify_channel_tier(out["opportunity_name"], source_dataset)
    out["funding_channel"] = out["funder_channel"] = ch
    out["access_tier"] = tier
    # normalise single-value controlled vocabularies to a canonical base; keep the verbatim
    for field, syn in (("instrument", None), ("recurrence", None), ("opportunity_status", None),
                       ("climate_relevance", CLIMATE_SYN)):
        canon, verbatim = _norm(out.get(field), syn)
        out[field] = canon
        if verbatim:
            extras[f"{field}_verbatim"] = verbatim
    # eligible_actor is multi-valued -> JSON array; full verbose text -> eligible_actor_detail
    actors, ea_verbatim = _norm_eligible(out.get("eligible_actor"))
    out["eligible_actor"] = json.dumps(actors) if actors else None
    if ea_verbatim and not out.get("eligible_actor_detail"):
        out["eligible_actor_detail"] = ea_verbatim
    if out.get("amount"):
        out["amount_currency"] = "CLP"          # source amounts are CLP; explicit for multi-currency
    out["data_quality_flags"] = json.dumps(dq) if dq else None
    out["source_extras"] = json.dumps(extras, ensure_ascii=False) if extras else None
    return out


@transformer
def merge_finance_opportunity(*frames, **kwargs):
    rows = []
    for df in frames:
        df = df.where(pd.notna(df), None)
        source_dataset = df["_source_dataset"].iloc[0] if len(df) else None
        for _, r in df.iterrows():
            rows.append(_align_row(r, source_dataset))

    result = pd.DataFrame(rows)
    before = len(result)
    result = result.drop_duplicates(subset=["source_opportunity_id"], keep="first").reset_index(drop=True)
    print(f"finance_opportunity: {len(result)} rows from {result['source_dataset'].nunique()} sources "
          f"({before - len(result)} duplicate fund rows collapsed)")
    return result


@test
def test_output(output, *args) -> None:
    assert output is not None and len(output) > 0, "no opportunities integrated"
    for col in ("source_opportunity_id", "opportunity_name", "source_dataset"):
        assert col in output.columns and output[col].notna().all(), f"missing/empty required column {col}"
    assert output["source_opportunity_id"].is_unique, "source_opportunity_id not unique"
