"""Build the project<->action link rows for raw_data.finance_project_action_staging.

Parallel branch to merge_finance_project (both read the same per-source loaders). Emits one row
per (project, action, mapping_source) so a project can carry SEVERAL matches -- the reason the
match moved out of finance_project into modelled.finance_project_action (mirrors
finance_opportunity_action). The modelled SQL derives project_id the same way as finance_project
(MD5(source_project_id-release_id)) and joins finance_project to stay FK-safe.

Matches by source:
  - BIP (cl-ssg): per-project matches file (codigo_bip, action_id, label); keep strong/goal_aligned.
  - GCF / FPA / CONAF: small grain crosswalks (fp_id / clasificacion / objetivo_manejo -> actions).
Confidence maps high->strong, medium->goal_aligned; off-list confidence is dropped (no link row).
"""
import re
import unicodedata

import pandas as pd

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer

BIP = "cl-ssg/cl-ssg-projects"
GCF = "gcf/gcf-projects"
FPA = "cl-mma/cl-mma-fpa-awards"
CONAF = "cl-conaf/cl-conaf-bn-awards"

CONFIDENCE = {"high": "strong", "medium": "goal_aligned"}

# grain -> list of (action_id, source_confidence). GCF keyed on raw fp_id; FPA/CONAF on folded grain.
GCF_ACTIONS = {
    "FP189": [("c40_0023", "high")], "FP120": [("ipcc_0052", "high")], "FP017": [("icare_0012", "medium")],
}
FPA_ACTIONS = {
    "economia circular y gestion de residuos": [("c40_0037", "high")],
    "punto verde": [("c40_0037", "high")],
    "eficiencia hidrica y energetica": [("c40_0016", "medium")],
    "eficiencia energetica": [("c40_0016", "medium")],
    "humedales urbanos": [("ipcc_0060", "high")],
    "invernadero y compostaje": [("icare_0064", "medium")],
    "sistema fotovoltaico offgrid": [("icare_0012", "high")],
    "sistema fotovoltaico ongrid": [("icare_0012", "high")],
    "sistema solar termico": [("icare_0016", "high")],
    "valoracion y conservacion de la biodiversidad": [("ipcc_0053", "medium")],
    "areas verdes comunitarias": [("c40_0042", "high")],
}
CONAF_ACTIONS = {  # several actions per objetivo -> several links per project
    "produccion maderera": [("ipcc_0054", "high"), ("ipcc_0071", "medium"), ("ipcc_0053", "medium")],
    "produccion no maderera": [("ipcc_0054", "high"), ("ipcc_0053", "medium")],
    "bosque preservacion y formaciones xerofiticas de alto valor ecologico":
        [("ipcc_0052", "high"), ("ipcc_0053", "medium")],
}
GRAIN = {  # source -> (grain column, crosswalk, mapping_source, fold-the-grain?)
    GCF: ("fp_id", GCF_ACTIONS, "gcf-crosswalk", False),
    FPA: ("clasificacion", FPA_ACTIONS, "fpa-crosswalk", True),
    CONAF: ("objetivo_manejo", CONAF_ACTIONS, "conaf-crosswalk", True),
}
SRC_ID = {GCF: "fp_id", FPA: "folio", CONAF: "award_id"}
OUT_COLS = ["source_dataset", "source_project_id", "action_id", "mapping_source", "confidence", "rationale"]


def _fold(s):
    s = "".join(c for c in unicodedata.normalize("NFKD", str(s or "")) if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def _frame_source(df):
    return df["_source_dataset"].iloc[0] if df is not None and len(df) else None


@transformer
def transform_finance_project_action(*frames, **kwargs):
    proj_frames, matches_df = [], None
    for df in frames:
        if df is None or not len(df):
            continue
        cols = set(df.columns)
        if "_source_dataset" not in cols and {"codigo_bip", "action_id", "label"} <= cols:
            matches_df = df
        elif "_source_dataset" in cols:
            proj_frames.append(df)

    rows = []
    # BIP per-project matches (multiple actions per project allowed)
    if matches_df is not None:
        m = matches_df.where(pd.notna(matches_df), None)
        for _, r in m.iterrows():
            lab = (r.get("label") or "").strip()
            code = (r.get("codigo_bip") or "").strip()
            aid = (r.get("action_id") or "").strip()
            if lab in ("strong", "goal_aligned") and code and aid:
                rows.append({"source_dataset": BIP, "source_project_id": code, "action_id": aid,
                             "mapping_source": "ssg-match", "confidence": lab, "rationale": None})

    # grain crosswalks (GCF / FPA / CONAF)
    for df in proj_frames:
        sd = _frame_source(df)
        if sd not in GRAIN:
            continue
        gcol, table, msrc, fold = GRAIN[sd]
        idcol = SRC_ID[sd]
        df = df.where(pd.notna(df), None)
        for _, r in df.iterrows():
            spid = (r.get(idcol) or "").strip()
            key = _fold(r.get(gcol)) if fold else (r.get(gcol) or "").strip()
            if not spid:
                continue
            for aid, conf in table.get(key, []):
                lab = CONFIDENCE.get(conf)
                if lab:
                    rows.append({"source_dataset": sd, "source_project_id": spid, "action_id": aid,
                                 "mapping_source": msrc, "confidence": lab, "rationale": None})

    out = pd.DataFrame(rows, columns=OUT_COLS)
    out = out.drop_duplicates(subset=["source_dataset", "source_project_id", "action_id", "mapping_source"]).reset_index(drop=True)
    print(f"finance_project_action: {len(out)} project-action links")
    for sd, g in out.groupby("source_dataset"):
        print(f"  {sd}: {len(g)} links, {g['source_project_id'].nunique()} projects, {g['action_id'].nunique()} actions")
    return out
