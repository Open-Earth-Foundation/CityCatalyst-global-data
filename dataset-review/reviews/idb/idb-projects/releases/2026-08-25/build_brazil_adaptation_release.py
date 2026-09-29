"""Build the IDB Projects Dataset Brazil adaptation research release."""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import date

import pandas as pd


RESOURCE_ID = "814b7b54-477a-4c25-b3bf-6be05412069d"
RAW = "sample/idb_projects_brazil_api.json"
PROJECT_OUT = "data/idb_brazil_adaptation_projects.csv"
MAPPING_OUT = "data/idb_brazil_adaptation_projects_to_actions.csv"
ACTION_BANK = "../../../../br-bndes/br-bndes-operacoes-financiamento/releases/2026-09-01/sample/adaptation_action_bank_icb_oef_v13.csv"
RETRIEVED_AT = "2026-09-24"
RAW_SHA256 = "85573a16161be62e49784a50c85a2560c53b9a5ea92f4d8a66c709ebcaa4dcc8"

ADAPTATION_SUBSECTORS = {
    "CLIMATE CHANGE ADAPTATION POLICY",
    "INTEGRATED DISASTER RISK MANAGEMENT",
    "IMMEDIATE RESPONSE TO EMERGENCY",
    "URBAN DRAINAGE",
}

EXPLICIT_CLIMATE = re.compile(
    r"climate[- ](?:change[- ]?)?(?:adapt|resilien|risk|vulnerab)|"
    r"adaptation (?:and|to|finance|policy)|resilien(?:ce|t) to climate|climatic resilien",
    re.I,
)
HAZARD_EVIDENCE = re.compile(
    r"flood(?:ing)?|landslide|drought|disaster risk|early warning|stormwater|storm water|"
    r"urban drainage|erosion control|resilient reconstruction",
    re.I,
)

# The objective mentions adaptation only as the title of a general IDB strategy; the operation itself is a mitigation project.
SCREEN_EXCLUSIONS = {"BR-G1006"}

RENAME = {
    "_id": "datastore_record_id",
    "oper_num": "project_id",
    "oper_nm": "project_name",
    "apprvl_dt": "approval_date",
    "sign_dt": "signing_date",
    "cntry_cd": "country_code",
    "cntry_nm": "country_name",
    "publc_sts_nm": "public_status",
    "sector_cd": "sector_code",
    "sector_nm": "sector_name",
    "subsector_cd": "subsector_code",
    "subsector_nm": "subsector_name",
    "oper_typ_cd": "operation_type_code",
    "opertyp_nm": "operation_type_name",
    "objtv": "objective",
    "orig_apprvd_useq_amnt": "original_approved_amount_usd",
    "totl_cost_orig": "original_total_cost_usd",
    "loc_cntrprt": "local_counterpart_amount_usd",
    "lending_typ_nm": "lending_type_name",
    "modality_cd": "modality_code",
    "modality_nm": "modality_name",
    "facility_typ_cd": "facility_type_code",
    "facility_typ_nm": "facility_type_name",
    "envmntl_clssfctn_cd": "environmental_classification_code",
    "envmntl_clssfctn_nm": "environmental_classification_name",
    "lending_instrmnt_cd": "lending_instrument_code",
    "lending_instrmnt_nm": "lending_instrument_name",
    "lending_typ_cd": "lending_type_code",
    "sts_cd": "internal_status_code",
}

ACTION_RULES = [
    (
        "c40_0048",
        "direct",
        re.compile(r"urban drainage|macrodrainage|drenurbs|drainage.{0,120}(?:flood|storm)|flood control|flood risk|control of flood damage|control of flooding zones", re.I),
        "The project text explicitly names urban drainage, macrodrainage or flood-control infrastructure.",
    ),
    (
        "icare_0184",
        "component",
        re.compile(r"slope stabili", re.I),
        "The project text explicitly names slope stabilisation as one component.",
    ),
    (
        "icare_0183",
        "component",
        re.compile(r"early warning", re.I),
        "The project text explicitly includes early-warning capacity as one component.",
    ),
    (
        "icare_0171",
        "component",
        re.compile(r"hydrometeorolog|hydrological monitoring|forecasting and monitoring", re.I),
        "The project text explicitly includes hydrometeorological forecasting or monitoring.",
    ),
    (
        "icare_0169",
        "related",
        re.compile(r"(?=.*emergency)(?=.*(?:flood|landslide|disaster|humanitarian|drought))|humanitarian (?:aid|assistance|needs)|flood victims", re.I | re.S),
        "The operation supports hazard-related emergency response or humanitarian assistance; this is related to, but does not prove funding for, a municipal preparedness plan.",
    ),
    (
        "icare_0172",
        "component",
        re.compile(r"disaster risk management policy|risk reduction plan|climate action plan|climate governance|climate mainstreaming", re.I),
        "The operation supports climate or disaster-risk planning and governance as part of a broader programme.",
    ),
    (
        "ipcc_0092",
        "component",
        re.compile(r"recovery credit|post-disaster financial|compensation payments|reconstruction after", re.I),
        "The project text names post-disaster finance, compensation or reconstruction support.",
    ),
    (
        "ipcc_0090",
        "direct",
        re.compile(r"crop insurance|garantia-safra|crop guarantee", re.I),
        "The operation explicitly concerns climate-risk insurance or crop-loss compensation for farmers.",
    ),
    (
        "ipcc_0096",
        "component",
        re.compile(r"(?=.*(?:farm|agricultur|livestock|coffee|productive value chain))(?=.*(?:climate adaptation|climate resilience|adaptation to climate))", re.I | re.S),
        "The objective explicitly links agriculture or rural production to climate adaptation or resilience.",
    ),
    (
        "ipcc_0101",
        "component",
        re.compile(r"(?=.*(?:water supply|sanitation|water security))(?=.*(?:climate resilience|climate adaptation|adaptation to climate|drought))", re.I | re.S),
        "The objective explicitly links water or sanitation infrastructure to drought, adaptation or climate resilience.",
    ),
    (
        "ipcc_0087",
        "component",
        re.compile(r"(?=.*(?:transport infrastructure|transport network|electrical grid|education infrastructure|school infrastructure))(?=.*climate resil)", re.I | re.S),
        "The project explicitly links public infrastructure to climate resilience, but the operation may include non-retrofit activities.",
    ),
    (
        "icare_0180",
        "component",
        re.compile(r"green-blue infrastructure|blue-green infrastructure", re.I),
        "The objective explicitly includes green-blue infrastructure.",
    ),
    (
        "icare_0170",
        "component",
        re.compile(r"relocat|resettl|high-risk areas", re.I),
        "The project text names relocation, resettlement or rehabilitation of high-risk areas as one component.",
    ),
    (
        "icare_0186",
        "component",
        re.compile(r"coastal.{0,120}(?:climate resilience|disaster risk)|(?:climate resilience|disaster risk).{0,120}coastal", re.I),
        "The objective links coastal management to climate resilience or disaster-risk reduction.",
    ),
    (
        "ipcc_0103",
        "component",
        re.compile(r"climate governance|climate mainstreaming|adaptation finance|(?=.*institutional planning)(?=.*(?:climate polic|adaptation target|plano clima))", re.I | re.S),
        "The operation strengthens institutional climate governance or adaptation-finance capacity.",
    ),
    (
        "new0001",
        "component",
        re.compile(r"(?=.*(?:rural population|traditional communities|indigenous|small holder farmers))(?=.*(?:climate adaptation|climate resilience|adaptation to climate))", re.I | re.S),
        "The objective links vulnerable rural or traditional communities to climate-resilient livelihoods or services.",
    ),
]


def load_source() -> pd.DataFrame:
    assert hashlib.sha256(open(RAW, "rb").read()).hexdigest() == RAW_SHA256
    payload = json.load(open(RAW, encoding="utf-8"))
    assert payload["success"] is True
    assert payload["result"]["total"] == 1750
    records = payload["result"]["records"]
    assert len(records) == 1750
    return pd.DataFrame(records).fillna("")


def screening_terms(text: str, subsector: str) -> str:
    terms = []
    if subsector in ADAPTATION_SUBSECTORS:
        terms.append("adaptation_or_disaster_subsector")
    if EXPLICIT_CLIMATE.search(text):
        terms.append("explicit_climate_adaptation_or_resilience")
    if HAZARD_EVIDENCE.search(text):
        terms.append("explicit_hazard_or_risk_reduction")
    return ";".join(terms)


def clean_projects(raw: pd.DataFrame) -> pd.DataFrame:
    text = raw[["oper_nm", "objtv", "subsector_nm"]].agg(" | ".join, axis=1)
    terms = [screening_terms(t, s) for t, s in zip(text, raw["subsector_nm"])]
    selected_mask = pd.Series(terms).ne("") & ~raw["oper_num"].isin(SCREEN_EXCLUSIONS)
    selected = raw.loc[selected_mask].copy().reset_index(drop=True)
    selected_terms = [value for value, keep in zip(terms, selected_mask) if keep]
    clean = selected.rename(columns=RENAME)[list(RENAME.values())].copy()
    for column in ["approval_date", "signing_date"]:
        parsed = pd.to_datetime(clean[column], errors="coerce")
        clean[column] = parsed.dt.strftime("%Y-%m-%d").fillna("")
    for column in ["original_approved_amount_usd", "original_total_cost_usd", "local_counterpart_amount_usd"]:
        clean[column] = pd.to_numeric(clean[column], errors="coerce")
    clean["adaptation_screen_terms"] = selected_terms
    clean["adaptation_screen_confidence"] = [
        "high" if "explicit_climate_adaptation_or_resilience" in value or selected.iloc[i]["subsector_nm"] == "CLIMATE CHANGE ADAPTATION POLICY" else "medium"
        for i, value in enumerate(selected_terms)
    ]
    clean["source_resource_id"] = RESOURCE_ID
    clean["source_retrieved_at"] = RETRIEVED_AT
    clean["source_language"] = "English"
    clean["translation_status"] = "source_english_no_portuguese_fields"
    return clean


def build_mapping(projects: pd.DataFrame) -> pd.DataFrame:
    action_bank = pd.read_csv(ACTION_BANK, header=1, dtype=str, keep_default_na=False)
    action_names = action_bank.set_index("ID")["Action"]
    rows = []
    for project in projects.itertuples(index=False):
        # Do not let a broad subsector label create an action-level claim. Project name and objective are the mapping evidence.
        text = " | ".join([project.project_name, project.objective])
        matches = []
        for action_id, match_type, pattern, rationale in ACTION_RULES:
            if pattern.search(text):
                matches.append((action_id, match_type, rationale))
        if not matches:
            rows.append(
                {
                    "project_id": project.project_id,
                    "project_name": project.project_name,
                    "action_id": "",
                    "action_name": "",
                    "match_type": "none",
                    "mapping_confidence": "none",
                    "adjudication_status": "not_mapped",
                    "rationale": "Adaptation relevance is screened in, but the project text does not support a specific action-bank link without additional project documents.",
                }
            )
            continue
        for action_id, match_type, rationale in matches:
            rows.append(
                {
                    "project_id": project.project_id,
                    "project_name": project.project_name,
                    "action_id": action_id,
                    "action_name": action_names.get(action_id, ""),
                    "match_type": match_type,
                    "mapping_confidence": "medium",
                    "adjudication_status": "pending",
                    "rationale": rationale,
                }
            )
    mapping = pd.DataFrame(rows)
    assert mapping.loc[mapping["action_id"].ne(""), "action_name"].ne("").all()
    assert not mapping.duplicated(["project_id", "action_id"]).any()
    assert set(mapping["project_id"]) == set(projects["project_id"])
    assert set(mapping["mapping_confidence"]) <= {"medium", "none"}
    return mapping


def validate(raw: pd.DataFrame, projects: pd.DataFrame, mapping: pd.DataFrame) -> None:
    assert raw.shape == (1750, 29)
    assert projects.shape[0] == 63
    assert projects["project_id"].is_unique
    assert projects["country_code"].eq("BR").all()
    assert projects["public_status"].value_counts().to_dict() == {"Implementation": 29, "Closed": 28, "Preparation": 4, "Cancelled": 2}
    assert projects["approval_date"].eq("").sum() == 4
    assert projects["adaptation_screen_confidence"].value_counts().to_dict() == {"high": 33, "medium": 30}
    assert projects["translation_status"].eq("source_english_no_portuguese_fields").all()
    assert projects["original_approved_amount_usd"].notna().all()
    assert projects["original_approved_amount_usd"].ge(0).all()
    assert not projects.duplicated().any()
    assert set(mapping["project_id"]) == set(projects["project_id"])


def main() -> None:
    raw = load_source()
    projects = clean_projects(raw)
    mapping = build_mapping(projects)
    validate(raw, projects, mapping)
    os.makedirs("data", exist_ok=True)
    projects.to_csv(PROJECT_OUT, index=False, encoding="utf-8")
    mapping.to_csv(MAPPING_OUT, index=False, encoding="utf-8")
    mapped = mapping.loc[mapping["action_id"].ne(""), "project_id"].nunique()
    print(
        f"wrote {len(projects)} projects and {len(mapping)} mapping rows; "
        f"{mapped}/{len(projects)} projects mapped to {mapping['action_id'].replace('', pd.NA).nunique()} actions"
    )


if __name__ == "__main__":
    main()
