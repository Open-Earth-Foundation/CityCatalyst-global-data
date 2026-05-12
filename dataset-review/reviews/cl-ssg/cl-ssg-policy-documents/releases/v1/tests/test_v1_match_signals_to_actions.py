"""Unit tests for v1_match_signals_to_actions.py — deterministic matcher, no I/O."""

from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path

import pytest

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "v1_match_signals_to_actions.py"
spec = importlib.util.spec_from_file_location("v1_match_signals_to_actions", SCRIPT_PATH)
m = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = m
spec.loader.exec_module(m)

V1_ROOT = Path(__file__).resolve().parents[1]


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def _base_action(
    action_id: str = "icare_test_1",
    primary_outcome: str = "emissions_fuel_switch",
    primary_channel: str = "solar_pv",
    primary_intervention: str = "infrastructure",
    confidence: str = "high",
) -> dict[str, str]:
    return {
        "action_id": action_id,
        "action_name": "Test action",
        "description": "",
        "gpc_reference": "I.2",
        "primary_outcome": primary_outcome,
        "secondary_outcome": "",
        "primary_intervention": primary_intervention,
        "secondary_intervention": "",
        "confidence": confidence,
        "primary_channel": primary_channel,
        "secondary_channel": "",
    }


def _base_signal(
    policy_signal_id: str = "pol_sig_1",
    signal_type: str = "action",
    climate_relevance: str = "mitigation",
    primary_outcome: str = "emissions_fuel_switch",
    primary_channel: str = "solar_pv",
    primary_intervention: str = "infrastructure",
    confidence: str = "high",
) -> dict[str, str]:
    return {
        "policy_signal_id": policy_signal_id,
        "source_document_id": "pol_test",
        "source_name": "Test Policy",
        "source_level": "regional",
        "region_code": "08",
        "communal_code": "",
        "signal_type": signal_type,
        "signal_code": "x",
        "signal_label": "Solar expansion in public buildings",
        "actor_level": "regional",
        "supporting_atom_ids": "atom_a;atom_b",
        "document_type": "parcc",
        "climate_relevance": climate_relevance,
        "primary_outcome": primary_outcome,
        "secondary_outcome": "",
        "primary_intervention": primary_intervention,
        "secondary_intervention": "",
        "confidence": confidence,
        "primary_channel": primary_channel,
        "secondary_channel": "",
    }


def test_exact_primary_outcome_and_channel_high_score() -> None:
    action = _base_action()
    sig = _base_signal(signal_type="action")
    r = m.score_signal_action_pair(action, sig, 0.45)
    assert r is not None
    assert r["final_match_score"] >= 0.70
    assert r["relation_type"] == "supports"


def test_outcome_only_pair_rejected_by_bridge_gate() -> None:
    """Same primary outcome but no channel overlap and no intervention+outcome bridge."""
    action = _base_action(
        primary_outcome="emissions_efficiency",
        primary_channel="building_institutional_public",
        primary_intervention="regulatory",
    )
    sig = _base_signal(
        primary_outcome="emissions_efficiency",
        primary_channel="agricultural_soil",
        primary_intervention="planning",
    )
    assert m.score_signal_action_pair(action, sig, 0.01) is None


def test_intervention_channel_primary_synergy_bonus() -> None:
    dim = m.compute_match_dimensions(
        _base_action(),
        _base_signal(),
    )
    assert dim.intervention_primary_match and dim.channel_primary_match
    assert pytest.approx(m.base_match_score(dim), rel=1e-9) == 0.9


def test_only_outcome_family_lower_base_score() -> None:
    action = _base_action(
        primary_outcome="emissions_efficiency",
        primary_channel="landfill",
        primary_intervention="regulatory",
    )
    sig = _base_signal(
        primary_outcome="emissions_demand_reduction",
        primary_channel="solar_pv",
        primary_intervention="planning",
    )
    dim = m.compute_match_dimensions(action, sig)
    assert dim.outcome_family_match
    assert not dim.outcome_primary_match
    assert m.base_match_score(dim) == 0.15


def test_outcome_plus_channel_family_accepted() -> None:
    """Primary outcome match + channel family (no primary channel), passes gate."""
    action = _base_action(
        primary_outcome="emissions_fuel_switch",
        primary_channel="solar_pv",
        primary_intervention="infrastructure",
    )
    sig = _base_signal(
        primary_outcome="emissions_fuel_switch",
        primary_channel="wind",
        primary_intervention="infrastructure",
    )
    r = m.score_signal_action_pair(action, sig, 0.45)
    assert r is not None
    dim = m.compute_match_dimensions(action, sig)
    assert dim.channel_family_match and not dim.channel_primary_match


def test_outcome_intervention_primary_gate_without_channel() -> None:
    """Clause (c): intervention_primary AND outcome_primary, different channel families."""
    action = _base_action(
        primary_outcome="emissions_fuel_switch",
        primary_channel="landfill",
        primary_intervention="infrastructure",
    )
    sig = _base_signal(
        primary_outcome="emissions_fuel_switch",
        primary_channel="solar_pv",
        primary_intervention="infrastructure",
    )
    dim = m.compute_match_dimensions(action, sig)
    assert dim.outcome_primary_match and dim.intervention_primary_match
    assert not dim.channel_family_match and not dim.channel_primary_match
    assert m.passes_meaningful_match_bridge(dim)
    r = m.score_signal_action_pair(action, sig, 0.45)
    assert r is not None


def test_adaptation_signal_filtered_out() -> None:
    action = _base_action()
    sig = _base_signal(climate_relevance="adaptation")
    cards = m.compute_alignment([action], [sig], min_score=0.01, only_action=None, only_policy=None)
    assert cards == {}


def test_monitoring_modifier_vs_action_type() -> None:
    action = _base_action()
    sig_action = _base_signal(signal_type="action", policy_signal_id="s1")
    sig_mon = _base_signal(signal_type="monitoring", policy_signal_id="s2")
    ra = m.score_signal_action_pair(action, sig_action, 0.01)
    rm = m.score_signal_action_pair(action, sig_mon, 0.01)
    assert ra is not None and rm is not None
    assert pytest.approx(rm["final_match_score"], rel=1e-6) == ra["final_match_score"] * 0.7
    assert rm["relation_type"] == "monitors"


def test_max_plus_bonus_strong_plus_weak_supports() -> None:
    scores = [0.85] + [0.45] * 6
    assert m.max_plus_bonus_policy_score(scores) == 1.0


def test_max_plus_bonus_six_weak_only() -> None:
    assert pytest.approx(m.max_plus_bonus_policy_score([0.45] * 6), rel=1e-9) == 0.65


def test_zero_matches_no_card(tmp_path: Path) -> None:
    action = _base_action(primary_outcome="enabling", primary_channel="mrv_planning")
    sig = _base_signal(
        primary_outcome="carbon_sequestration",
        primary_channel="peatland",
    )
    cards = m.compute_alignment([action], [sig], min_score=0.95, only_action=None, only_policy=None)
    assert cards == {}


def test_high_medium_confidence_weight() -> None:
    action = _base_action(confidence="high")
    sig = _base_signal(confidence="medium")
    dim = m.compute_match_dimensions(action, sig)
    raw = m.base_match_score(dim) * m.signal_type_modifier(sig["signal_type"])
    expected = raw * m.confidence_weight("high", "medium")
    r = m.score_signal_action_pair(action, sig, 0.01)
    assert r is not None
    assert pytest.approx(r["final_match_score"], rel=1e-5) == expected


def test_top_relation_tie_break_supports_wins() -> None:
    action = _base_action()
    sigs = [
        _base_signal(policy_signal_id="a1", signal_type="action"),
        _base_signal(policy_signal_id="a2", signal_type="action"),
        _base_signal(
            policy_signal_id="a3",
            signal_type="sector_priority",
        ),
    ]
    cards = m.compute_alignment([action], sigs, min_score=0.01, only_action=None, only_policy=None)
    key = ("pol_test", "icare_test_1")
    assert key in cards
    assert cards[key]["top_relation_type"] == "supports"
    assert cards[key]["match_count"] == 3


def test_match_quality_labels() -> None:
    assert m.derive_match_quality(0.76, {"outcome": 0.4, "channel": 0.3, "intervention": 0.0}) == "strong"
    assert m.derive_match_quality(0.75, {"outcome": 0.4, "channel": 0.19, "intervention": 0.0}) == "moderate"
    assert m.derive_match_quality(0.60, {"outcome": 0.1, "channel": 0.0, "intervention": 0.0}) == "moderate"
    assert m.derive_match_quality(0.54, {"outcome": 0.5, "channel": 0.5, "intervention": 0.15}) == "weak"


def test_match_writes_json(tmp_path: Path) -> None:
    actions_f = tmp_path / "actions.csv"
    signals_f = tmp_path / "signals.csv"
    af = list(_base_action().keys())
    sf = list(_base_signal().keys())
    _write_csv(actions_f, af, [_base_action()])
    _write_csv(signals_f, sf, [_base_signal()])
    out = tmp_path / "align"
    assert (
        m.main(
            [
                "match",
                "--actions-csv",
                str(actions_f),
                "--signals-csv",
                str(signals_f),
                "--output-dir",
                str(out),
            ]
        )
        == 0
    )
    jpath = out / "pol_test" / "icare_test_1.json"
    assert jpath.is_file()
    data = json.loads(jpath.read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.0.0"
    assert data["action_gpc_reference"] == "I.2"
    assert len(data["matched_signals"]) == 1
    assert data["matched_signals"][0]["supporting_atom_ids"] == ["atom_a", "atom_b"]
    assert data["match_quality"] in ("strong", "moderate", "weak")


def test_verify_detects_drift(tmp_path: Path) -> None:
    actions_f = tmp_path / "actions.csv"
    signals_f = tmp_path / "signals.csv"
    _write_csv(actions_f, list(_base_action().keys()), [_base_action()])
    _write_csv(signals_f, list(_base_signal().keys()), [_base_signal()])
    out = tmp_path / "align"
    assert m.main(["match", "--actions-csv", str(actions_f), "--signals-csv", str(signals_f), "--output-dir", str(out)]) == 0
    _write_csv(
        signals_f,
        list(_base_signal().keys()),
        [_base_signal(primary_outcome="carbon_sequestration", primary_channel="forest")],
    )
    assert m.main(["verify", "--actions-csv", str(actions_f), "--signals-csv", str(signals_f), "--output-dir", str(out)]) != 0


def test_live_release_csvs_smoke() -> None:
    a_path = V1_ROOT / "data" / "derived" / "actions_profiled.csv"
    s_path = V1_ROOT / "data" / "derived" / "signals_profiled.csv"
    if not a_path.is_file() or not s_path.is_file():
        return
    actions = m.load_csv_rows(a_path)
    signals = m.load_csv_rows(s_path)
    cards = m.compute_alignment(actions, signals, min_score=0.45, only_action=None, only_policy=None)
    assert len(cards) >= 1
