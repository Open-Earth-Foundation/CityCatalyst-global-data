#!/usr/bin/env python3
"""Build the World Bank Brazil adaptation-screen release from official API responses.

The screen is deliberately not a climate-finance attribution. It combines reproducible
Projects API full-text queries with explicit title terms, then assigns only conservative
action links. Run with ``--refresh`` to retrieve fresh API evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
SAMPLE = HERE / "sample"
DATA = HERE / "data"
API = "https://search.worldbank.org/api/v2/projects"
COUNTRY_URL = f"{API}?format=json&rows=1000&os=0&countrycode=BR"
QUERY_TERMS = {
    "adaptation": "adaptation",
    "climate_resilience": '"climate resilience"',
    "disaster_risk": '"disaster risk"',
    "flood": "flood",
    "drought": "drought",
    "landslide": "landslide",
    "early_warning": '"early warning"',
}
TITLE_RE = re.compile(
    r"adaptation|climat(?:e|ic)|resilien|flood|drought|disaster|landslide|"
    r"early warning|water security|drainage|forest fire|climate-smart",
    re.I,
)
PT_TITLE_TRANSLATIONS = {
    "P170682": "Urban Resilience Credit Line in Southern Brazil",
}
ACTION_BANK = (
    HERE
    / "../../../../br-bndes/br-bndes-operacoes-financiamento/releases/2026-09-01/"
    / "sample/adaptation_action_bank_icb_oef_v13.csv"
).resolve()


def fetch_json(url: str, path: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "CityCatalyst dataset review"})
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = response.read()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def load_projects(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    projects = payload.get("projects", {})
    if isinstance(projects, dict):
        return list(projects.values())
    return list(projects)


def money(value):
    if value in (None, ""):
        return pd.NA
    text = str(value).replace(",", "").strip()
    return pd.NA if not text else int(float(text))


def scalar(value):
    """Unwrap API list/list-like scalar fields without evaluating arbitrary text."""
    if isinstance(value, list):
        return value[0] if len(value) == 1 else " | ".join(map(str, value))
    text = "" if value is None else str(value).strip()
    match = re.fullmatch(r"\['([^']+)'\]", text)
    return match.group(1) if match else text


def date(value):
    if value in (None, ""):
        return ""
    return pd.to_datetime(value, errors="coerce", utc=True).date().isoformat()


def sector(record: dict, n: int, field: str):
    value = record.get(f"sector{n}") or {}
    return value.get(field, "")


def parse_theme(value):
    if not value or value == "!$!0":
        return ("", "")
    parts = str(value).split("!$!")
    name = parts[0]
    percent = parts[1] if len(parts) > 1 and parts[1].isdigit() else ""
    return name, percent


def build(refresh: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    SAMPLE.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    country_path = SAMPLE / "world_bank_projects_brazil_api.json"
    if refresh or not country_path.exists():
        fetch_json(COUNTRY_URL, country_path)

    query_hits: dict[str, set[str]] = {}
    for label, term in QUERY_TERMS.items():
        path = SAMPLE / f"query_{label}.json"
        url = f"{API}?format=json&rows=1000&os=0&countrycode=BR&qterm={urllib.parse.quote(term)}"
        if refresh or not path.exists():
            fetch_json(url, path)
        for record in load_projects(path):
            query_hits.setdefault(record["id"], set()).add(label)

    source = {record["id"]: record for record in load_projects(country_path)}
    selected_ids = []
    for project_id, record in source.items():
        title = record.get("project_name") or ""
        if len(query_hits.get(project_id, set())) >= 2 or TITLE_RE.search(title):
            selected_ids.append(project_id)

    rows = []
    for project_id in sorted(selected_ids):
        record = source[project_id]
        original_title = record.get("project_name") or ""
        translated = project_id in PT_TITLE_TRANSLATIONS
        hits = sorted(query_hits.get(project_id, set()))
        title_explicit = bool(TITLE_RE.search(original_title))
        theme1, theme1_percent = parse_theme(record.get("theme1"))
        major_themes = sorted(
            {x.get("name", "") for x in (record.get("mjtheme_namecode") or []) if x.get("name")}
        )
        status = record.get("status") or ""
        approved = status in {"Active", "Closed"} and bool(record.get("boardapprovaldate"))
        rows.append(
            {
                "project_id": project_id,
                "project_name": PT_TITLE_TRANSLATIONS.get(project_id, original_title),
                "project_name_pt": original_title if translated else "",
                "project_name_translation_status": (
                    "human_translated_from_portuguese_source" if translated else "source_english"
                ),
                "country_code": scalar(record.get("countrycode")),
                "country_name": scalar(record.get("countryshortname") or record.get("countryname")),
                "region_name": scalar(record.get("regionname")),
                "lifecycle_status": status,
                "has_board_approval_evidence": approved,
                "board_approval_date": date(record.get("boardapprovaldate")),
                "closing_date": date(record.get("closingdate")),
                "closing_date_semantics": "planned_or_recorded_closing_date_not_completion_evidence",
                "has_disbursement_data": False,
                "lending_instrument": record.get("lendinginstr", ""),
                "lending_instrument_type_code": record.get("lendinginstrtype", ""),
                "product_line_code": record.get("prodline", ""),
                "product_line_name": record.get("prodlinetext", ""),
                "product_line_type_code": record.get("productlinetype", ""),
                "borrower_name": record.get("borrower", ""),
                "implementing_agency_name": record.get("impagency", ""),
                "organization_names_translation_status": "source_legal_names_not_translated",
                "primary_sector_name": sector(record, 1, "Name"),
                "primary_sector_percent": sector(record, 1, "Percent"),
                "secondary_sector_name": sector(record, 2, "Name"),
                "secondary_sector_percent": sector(record, 2, "Percent"),
                "tertiary_sector_name": sector(record, 3, "Name"),
                "tertiary_sector_percent": sector(record, 3, "Percent"),
                "primary_theme_name": theme1,
                "primary_theme_percent": theme1_percent,
                "major_theme_names": " | ".join(major_themes),
                "total_commitment_amount_usd": money(record.get("totalcommamt")),
                "project_cost_usd": money(record.get("lendprojectcost")),
                "ibrd_commitment_amount_usd": money(record.get("ibrdcommamt")),
                "ida_commitment_amount_usd": money(record.get("idacommamt")),
                "grant_amount_usd": money(record.get("grantamt")),
                "environmental_assessment_category_code": record.get("envassesmentcategorycode", ""),
                "project_url": record.get("url", ""),
                "official_api_query_matches": " | ".join(hits),
                "adaptation_screen_evidence": (
                    "explicit_project_title" if title_explicit else "multiple_official_api_query_matches"
                ),
                "adaptation_screen_confidence": "high" if title_explicit or len(hits) >= 3 else "medium",
                "adaptation_finance_amount_usd": pd.NA,
                "adaptation_finance_amount_status": "not_reported_do_not_infer_from_project_commitment",
                "source_retrieved_date": "2026-09-25",
            }
        )

    projects = pd.DataFrame(rows).sort_values("project_id").reset_index(drop=True)
    projects.to_csv(DATA / "world_bank_brazil_adaptation_projects.csv", index=False)
    mappings = build_mappings(projects)
    mappings.to_csv(DATA / "world_bank_brazil_adaptation_projects_to_actions.csv", index=False)
    return projects, mappings


def build_mappings(projects: pd.DataFrame) -> pd.DataFrame:
    bank = pd.read_csv(ACTION_BANK, header=1)
    action_names = dict(zip(bank["ID"], bank["Action"]))
    rows = []
    for project in projects.to_dict("records"):
        title = project["project_name"].lower()
        action_id = ""
        relation = "none"
        rationale = "No action-level link is supported by the project-level API metadata."
        if "early warning" in title or ("forest fire" in title and "warning" in title):
            action_id, relation = "icare_0183", "direct"
            rationale = "The project title explicitly identifies an early-warning system."
        elif "flood" in title and any(x in title for x in ["prevention", "reduction", "urban flood"]):
            action_id, relation = "c40_0048", "component"
            rationale = "The title identifies flood prevention/reduction; drainage is a plausible component, not the whole project."
        elif "water security" in title:
            action_id, relation = "ipcc_0101", "component"
            rationale = "The title identifies water security; the link is limited to a possible resilient water/sanitation component."
        elif "resilient road" in title or "road asset management" in title:
            action_id, relation = "ipcc_0087", "component"
            rationale = "The title identifies resilient road assets, a public-infrastructure component."
        elif "climate-smart agriculture" in title:
            action_id, relation = "ipcc_0096", "direct"
            rationale = "The title explicitly identifies climate-smart agriculture."
        rows.append(
            {
                "project_id": project["project_id"],
                "project_name": project["project_name"],
                "action_id": action_id,
                "action_name": action_names.get(action_id, ""),
                "relationship": relation,
                "confidence": "medium" if action_id else "none",
                "mapping_status": "pending_human_adjudication" if action_id else "not_mapped_insufficient_evidence",
                "mapping_rationale": rationale,
                "allocated_amount_usd": pd.NA,
                "amount_allocation_status": "not_allocated_project_metadata_has_no_component_amount",
            }
        )
    return pd.DataFrame(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="retrieve official API responses again")
    args = parser.parse_args()
    project_data, mapping_data = build(args.refresh)
    print(f"projects={len(project_data)} mappings={len(mapping_data)}")
    print(project_data["lifecycle_status"].value_counts().sort_index().to_dict())
    print(f"mapped={mapping_data['action_id'].ne('').sum()} none={mapping_data['action_id'].eq('').sum()}")
    for file in sorted(SAMPLE.glob("*.json")):
        print(f"sha256 {file.name} {sha256(file)}")
