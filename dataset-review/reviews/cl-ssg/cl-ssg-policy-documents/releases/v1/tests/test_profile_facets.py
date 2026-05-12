"""Unit tests for profile_facets.py (loaders, messages, schema) — no API calls."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "profile_facets.py"
spec = importlib.util.spec_from_file_location("profile_facets", SCRIPT_PATH)
profile_facets = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = profile_facets
spec.loader.exec_module(profile_facets)

V1_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def _reset_atom_cache() -> None:
    profile_facets._ATOM_BY_ID_CACHE = None
    yield
    profile_facets._ATOM_BY_ID_CACHE = None


def test_load_actions_json_flattens_emissions() -> None:
    path = V1_ROOT / "data" / "input" / "actions.json"
    if not path.exists():
        return
    rows = profile_facets.load_actions_json(path)
    assert len(rows) >= 1
    first = rows[0]
    assert "action_id" in first and first["action_id"]
    assert "action_name" in first
    assert "subsector_number" in first
    assert "sector_number" in first
    assert "gpc_reference" in first
    assert "intervention_type_input" in first
    assert "outcome_summary" in first


def test_load_signal_rows_across_summaries(tmp_path: Path) -> None:
    summ = tmp_path / "data" / "summaries"
    summ.mkdir(parents=True)
    (summ / "doc_a.json").write_text(
        json.dumps(
            {
                "source_document_id": "doc_a",
                "source_name": "Doc A",
                "source_level": "regional",
                "region_code": "08",
                "communal_code": "",
                "document_type": "parcc",
                "policy_signals": [
                    {
                        "policy_signal_id": "sig_a_1",
                        "signal_type": "target",
                        "signal_code": "T1",
                        "signal_label": "Reduce emissions 40%",
                        "actor_level": "regional",
                        "supporting_atom_ids": ["doc_a_a_0001"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (summ / "doc_b.json").write_text(
        json.dumps(
            {
                "source_document_id": "doc_b",
                "source_name": "Doc B",
                "source_level": "national",
                "region_code": "",
                "communal_code": "",
                "document_type": "framework",
                "policy_signals": [
                    {
                        "policy_signal_id": "sig_b_1",
                        "signal_type": "sector",
                        "signal_code": "",
                        "signal_label": "Energy sector priority",
                        "actor_level": "national",
                        "supporting_atom_ids": [],
                    },
                    {
                        "policy_signal_id": "sig_b_2",
                        "signal_type": "funding",
                        "signal_code": "FVC",
                        "signal_label": "Green Climate Fund",
                        "actor_level": "national",
                        "supporting_atom_ids": ["x"],
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    rows = profile_facets.load_signal_rows_from_summaries(summ)
    assert len(rows) == 3
    ids = {r["policy_signal_id"] for r in rows}
    assert ids == {"sig_a_1", "sig_b_1", "sig_b_2"}
    ra = next(r for r in rows if r["policy_signal_id"] == "sig_a_1")
    assert ra["source_document_id"] == "doc_a"
    assert ra["supporting_atom_ids"] == "doc_a_a_0001"


def test_signal_user_message_includes_atom_evidence(tmp_path: Path) -> None:
    atoms = tmp_path / "data" / "atoms"
    atoms.mkdir(parents=True)
    (atoms / "doc_a.jsonl").write_text(
        json.dumps(
            {
                "atom_id": "doc_a_a_0001",
                "evidence_text": "Verbatim evidence line one.",
                "page_reference": "12-14",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    profile_facets._ATOM_BY_ID_CACHE = None
    atom_by_id = profile_facets.load_atom_by_id(atoms, use_cache=False)
    row = {
        "policy_signal_id": "sig_1",
        "source_document_id": "doc_a",
        "document_type": "parcc",
        "actor_level": "regional",
        "signal_type": "target",
        "signal_code": "T",
        "signal_label": "Cut 50%",
        "supporting_atom_ids": "doc_a_a_0001",
    }
    msg = profile_facets.signal_user_message(row, atom_by_id)
    assert "Policy signal ID: sig_1" in msg
    assert "Source document: doc_a (parcc)" in msg
    assert "Signal type: target" in msg
    assert "Verbatim evidence" in msg
    assert "[p. 12-14]" in msg


def test_action_user_message_includes_required_fields() -> None:
    row = {
        "action_id": "x_001",
        "action_name": "Test action",
        "subsector_number": "II.1",
        "gpc_reference": "II.1; II.2",
        "intervention_type_input": "infrastructure",
        "action_role": "outcome",
        "description": "Desc here",
        "outcome_summary": "Outcome here",
    }
    msg = profile_facets.action_user_message(row)
    assert "Action ID: x_001" in msg
    assert "GPC subsector: II.1 (II.1; II.2)" in msg
    assert "Intervention type (input): infrastructure" in msg
    assert "Action role: outcome" in msg
    assert "Outcome summary: Outcome here" in msg


def test_make_schema_signals_includes_climate_relevance() -> None:
    schema = profile_facets.make_schema("signals")
    assert "climate_relevance" in schema["properties"]
    assert "climate_relevance" in schema["required"]
    assert "primary_outcome" in schema["required"]


def test_make_schema_actions_has_no_climate_relevance() -> None:
    schema = profile_facets.make_schema("actions")
    assert "climate_relevance" not in schema["properties"]
