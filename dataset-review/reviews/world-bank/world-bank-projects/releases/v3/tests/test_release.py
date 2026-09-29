import json
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]


def test_cleaned_release_invariants():
    data = pd.read_csv(BASE / "data/world_bank_brazil_adaptation_projects.csv")
    source_path = BASE / "sample/world_bank_projects_brazil_api.json"
    if source_path.exists():
        source = json.loads(source_path.read_text())
        assert len(source["projects"]) == len(set(source["projects"])) == 566
    assert len(data) == 55
    assert data["project_id"].notna().all()
    assert data["project_id"].is_unique
    assert set(data["country_code"]) == {"BR"}
    assert set(data["organization_names_translation_status"]) == {"source_legal_names_not_translated"}
    assert data["lifecycle_status"].value_counts().to_dict() == {
        "Closed": 26,
        "Active": 22,
        "Pipeline": 5,
        "Dropped": 2,
    }
    assert int(data["total_commitment_amount_usd"].fillna(0).sum()) == 8_679_030_000
    assert data["adaptation_finance_amount_usd"].isna().all()
    assert not data["has_disbursement_data"].any()


def test_translation_pairing():
    data = pd.read_csv(BASE / "data/world_bank_brazil_adaptation_projects.csv")
    translated = data[data["project_name_translation_status"] == "human_translated_from_portuguese_source"]
    assert translated["project_id"].tolist() == ["P170682"]
    assert translated["project_name_pt"].notna().all()
    assert data.loc[data["project_id"] != "P170682", "project_name_pt"].isna().all()


def test_mapping_completeness_and_conservatism():
    data = pd.read_csv(BASE / "data/world_bank_brazil_adaptation_projects.csv")
    mapping = pd.read_csv(BASE / "data/world_bank_brazil_adaptation_projects_to_actions.csv")
    assert len(mapping) == len(data) == 55
    assert mapping["project_id"].is_unique
    assert set(mapping["project_id"]) == set(data["project_id"])
    assert mapping["action_id"].notna().sum() == 9
    assert mapping.loc[mapping["action_id"].notna(), "action_name"].notna().all()
    assert set(mapping["action_id"].dropna()) == {
        "c40_0048",
        "icare_0183",
        "ipcc_0087",
        "ipcc_0096",
        "ipcc_0101",
    }
    assert mapping["allocated_amount_usd"].isna().all()
    assert set(mapping.loc[mapping["action_id"].notna(), "confidence"]) == {"medium"}
