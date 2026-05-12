"""Unit tests for profile_channel.py (message builders) — no API calls."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "profile_channel.py"
spec = importlib.util.spec_from_file_location("profile_channel", SCRIPT_PATH)
profile_channel = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = profile_channel
spec.loader.exec_module(profile_channel)


def test_signal_user_message_renders_fields() -> None:
    row = {
        "policy_signal_id": "sig_99",
        "source_document_id": "doc_z",
        "signal_type": "governance",
        "signal_label": "CORECC meets annually",
        "climate_relevance": "mitigation",
        "primary_outcome": "enabling",
        "primary_intervention": "planning",
        "reasoning": "Governance body coordinates regional climate work.",
    }
    msg = profile_channel.signal_user_message(row)
    assert "Policy signal ID: sig_99" in msg
    assert "Source document: doc_z" in msg
    assert "Signal type: governance" in msg
    assert "Climate relevance: mitigation" in msg
    assert "Primary outcome: enabling" in msg
    assert "Profiler reasoning:" in msg


def test_action_user_message_unchanged_shape() -> None:
    row = {
        "action_id": "a1",
        "action_name": "LED retrofit",
        "subsector_number": "I.4",
        "primary_outcome": "emissions_efficiency",
        "primary_intervention": "infrastructure",
        "action_role": "outcome",
        "description": "Replace lighting",
        "outcome_summary": "Lower electricity use",
    }
    msg = profile_channel.action_user_message(row)
    assert "Action ID: a1" in msg
    assert "Primary outcome: emissions_efficiency" in msg
    assert "Outcome summary: Lower electricity use" in msg


def test_needs_profiling_skips_when_channel_set() -> None:
    assert profile_channel.needs_profiling({"primary_channel": ""}) is True
    assert profile_channel.needs_profiling({"primary_channel": "solar_pv"}) is False
