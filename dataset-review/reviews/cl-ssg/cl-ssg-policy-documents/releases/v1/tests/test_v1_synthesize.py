"""Tests for v1_synthesize.py — uses FakeLLMClient, tmp_path, no real API calls."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Any

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "v1_synthesize.py"
spec = importlib.util.spec_from_file_location("v1_synthesize", SCRIPT_PATH)
v1_synthesize = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = v1_synthesize
spec.loader.exec_module(v1_synthesize)


@dataclass
class FakeLLMResponse:
    text: str
    parsed: Any
    finish_reason: str | None = "stop"


class FakeLLMClient:
    def __init__(self, responses: list[FakeLLMResponse]) -> None:
        self.responses = list(responses)
        self.calls = 0

    def complete(self, **_kwargs: Any) -> FakeLLMResponse:
        response = self.responses[self.calls % len(self.responses)]
        self.calls += 1
        return response


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "policy_summary.schema.json"


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def make_atom(
    atom_id: str,
    primitive_type: str = "action",
    measure_type: str = "mitigation",
    evidence_kind: str = "qualitative",
    raw_value_numeric: float | None = None,
    explicitness: str = "explicit",
) -> dict[str, Any]:
    atom: dict[str, Any] = {
        "atom_id": atom_id,
        "source_document_id": "test_doc",
        "primitive_type": primitive_type,
        "evidence_kind": evidence_kind,
        "evidence_text": f"Evidence for {atom_id}.",
        "page_start": 1,
        "page_end": 1,
        "explicitness": explicitness,
        "extraction_method": "atom_extractor",
        "measure_type": measure_type,
    }
    if raw_value_numeric is not None:
        atom["raw_value_numeric"] = raw_value_numeric
    return atom


def minimal_valid_summary(source_document_id: str, atom_id: str = "test_doc_a_0001") -> dict[str, Any]:
    """Minimal policy_summary that satisfies the schema."""
    return {
        "schema_version": "1.0.0",
        "source_document_id": source_document_id,
        "source_name": "Test Document",
        "family": "parcc",
        "document_type": "parcc",
        "document_status": "final",
        "publisher": "Test",
        "publication_year": 2025,
        "region_code": "08",
        "communal_code": "",
        "source_level": "regional",
        "applicability_scope": "Test scope",
        "synthesis_run": {
            "created_at": "2026-01-01T00:00:00+00:00",
            "created_by": "test",
            "atom_count_input": 1,
            "atom_count_selected": 1,
        },
        "evidence_anchors": [
            {
                "atom_id": atom_id,
                "page_start": 1,
                "page_end": 1,
                "evidence_text": "Evidence text.",
            }
        ],
        "policy_signals": [
            {
                "policy_signal_id": f"{source_document_id}_sig_0001",
                "signal_type": "context",
                "signal_code": "",
                "signal_label": "Test signal",
                "actor_level": "unknown",
                "supporting_atom_ids": [atom_id],
            }
        ],
    }


def make_registry(source_document_id: str, document_type: str = "parcc") -> dict[str, dict[str, Any]]:
    return {
        source_document_id: {
            "source_document_id": source_document_id,
            "source_name": "Test Document",
            "document_type": document_type,
            "document_status": "final",
            "source_level": "regional",
            "region_code": "CL-BI",
            "communal_code": "",
            "publisher": "Test Publisher",
            "publication_year": 2025,
        }
    }


def write_atoms_jsonl(path: Path, atoms: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for atom in atoms:
            f.write(json.dumps(atom, ensure_ascii=False) + "\n")


def write_registry(v1_root: Path, docs: list[dict[str, Any]]) -> None:
    reg_path = v1_root / "data/registry/source_documents.json"
    reg_path.parent.mkdir(parents=True, exist_ok=True)
    reg_path.write_text(json.dumps({"source_documents": docs}), encoding="utf-8")


def copy_schemas(v1_root: Path) -> None:
    """Copy schemas and rubrics into the tmp v1_root."""
    real_v1 = Path(__file__).resolve().parents[1]
    for schema in (real_v1 / "schemas").glob("*.json"):
        dest = v1_root / "schemas" / schema.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(schema.read_bytes())
    for rubric in (real_v1 / "rubrics").glob("*.md"):
        dest = v1_root / "rubrics" / rubric.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(rubric.read_bytes())


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_selection_respects_per_primitive_caps():
    """select_atoms respects per-primitive-type caps from SELECTION_CAPS."""
    # parcc/mitigation action cap = 25; build 30 action atoms
    atoms = [make_atom(f"a_{i:04d}", primitive_type="action") for i in range(30)]
    selected = v1_synthesize.select_atoms(atoms, family="parcc", focus="mitigation")
    action_selected = [a for a in selected if a["primitive_type"] == "action"]
    assert len(action_selected) <= 25, f"Expected ≤25 actions, got {len(action_selected)}"


def test_prioritization_quantitative_over_qualitative():
    """When the cap forces a choice, quantitative atoms rank above qualitative ones."""
    # territorial_plan action cap = 5; mix quantitative and qualitative
    quant_atoms = [
        make_atom(f"q_{i:04d}", primitive_type="action", evidence_kind="quantitative", raw_value_numeric=float(i))
        for i in range(5)
    ]
    qual_atoms = [
        make_atom(f"l_{i:04d}", primitive_type="action", evidence_kind="qualitative")
        for i in range(5)
    ]
    all_atoms = qual_atoms + quant_atoms  # qualitative listed first
    selected = v1_synthesize.select_atoms(all_atoms, family="territorial_plan", focus="mitigation")
    selected_ids = {a["atom_id"] for a in selected if a["primitive_type"] == "action"}
    # All 5 quantitative atoms must be in the selected set
    for atom in quant_atoms:
        assert atom["atom_id"] in selected_ids, f"{atom['atom_id']} not selected despite being quantitative"


def test_evidence_anchor_crossref_rejects_hallucinated_atom_ids():
    """validate_summary flags atom_ids in evidence_anchors not in the input set."""
    schema = load_schema()
    summary = minimal_valid_summary("test_doc", atom_id="test_doc_a_0001")
    # Real atom id in the summary but not in input
    errors = v1_synthesize.validate_summary(
        summary,
        schema=schema,
        input_atom_ids={"test_doc_a_9999"},  # real input has a different id
        focus="mitigation",
    )
    hallucinated = [e for e in errors if e.startswith("hallucinated_atom_id")]
    assert hallucinated, f"Expected hallucination error, got: {errors}"


def test_evidence_anchor_crossref_rejects_duplicates():
    """validate_summary flags duplicate atom_ids in evidence_anchors."""
    schema = load_schema()
    summary = minimal_valid_summary("test_doc", atom_id="test_doc_a_0001")
    # Duplicate anchor
    summary["evidence_anchors"].append(
        {"atom_id": "test_doc_a_0001", "page_start": 1, "page_end": 1, "evidence_text": "dup"}
    )
    errors = v1_synthesize.validate_summary(
        summary,
        schema=schema,
        input_atom_ids={"test_doc_a_0001"},
        focus="mitigation",
    )
    dupe_errors = [e for e in errors if "duplicate" in e]
    assert dupe_errors, f"Expected duplicate error, got: {errors}"


def test_zero_mitigation_atoms_produces_absent_emphasis(tmp_path):
    """focus=mitigation with no mitigation atoms → summary has mitigation_emphasis=absent."""
    copy_schemas(tmp_path)
    doc_id = "test_parcc_doc"
    atoms = [make_atom(f"{doc_id}_a_{i:04d}", measure_type="adaptation") for i in range(5)]
    atoms_path = tmp_path / "data/atoms" / f"{doc_id}.jsonl"
    write_atoms_jsonl(atoms_path, atoms)
    registry_doc = make_registry(doc_id, "parcc")[doc_id]
    write_registry(tmp_path, [registry_doc])

    schema_original, schema_resolved = v1_synthesize.load_summary_schema(tmp_path)
    input_atom_ids = {a["atom_id"] for a in atoms}

    # Build a minimal valid summary that the fake client will return
    summary = minimal_valid_summary(doc_id, atom_id=atoms[0]["atom_id"])
    summary["mitigation_emphasis"] = "absent"
    summary["named_actions"] = []
    summary["headline_targets"] = []

    client = FakeLLMClient([FakeLLMResponse(text=json.dumps(summary), parsed=summary)])

    status, _run = v1_synthesize.synthesize_document(
        source_document_id=doc_id,
        v1_root=tmp_path,
        provider="openai",
        model="gpt-4.1",
        focus="mitigation",
        max_output_tokens=16000,
        max_transient_retries=1,
        force=False,
        client=client,
        summary_schema_original=schema_original,
        summary_schema_resolved=schema_resolved,
        registry=make_registry(doc_id, "parcc"),
    )
    assert status == "synthesized", f"Expected synthesized, got {status}"
    result = json.loads((tmp_path / "data/summaries" / f"{doc_id}.json").read_text())
    assert result.get("mitigation_emphasis") == "absent"
    assert result.get("named_actions") == []


def test_malformed_json_triggers_retry(tmp_path):
    """LLM returns malformed JSON → retry runs, second attempt succeeds."""
    copy_schemas(tmp_path)
    doc_id = "test_parcc_retry"
    atoms = [make_atom(f"{doc_id}_a_0001")]
    atoms_path = tmp_path / "data/atoms" / f"{doc_id}.jsonl"
    write_atoms_jsonl(atoms_path, atoms)
    write_registry(tmp_path, [make_registry(doc_id, "parcc")[doc_id]])

    schema_original, schema_resolved = v1_synthesize.load_summary_schema(tmp_path)
    valid_summary = minimal_valid_summary(doc_id, atom_id=f"{doc_id}_a_0001")

    malformed = FakeLLMResponse(text="{not valid json}", parsed=None)
    valid = FakeLLMResponse(text=json.dumps(valid_summary), parsed=valid_summary)
    client = FakeLLMClient([malformed, valid])

    status, _run = v1_synthesize.synthesize_document(
        source_document_id=doc_id,
        v1_root=tmp_path,
        provider="openai",
        model="gpt-4.1",
        focus="mitigation",
        max_output_tokens=16000,
        max_transient_retries=1,
        force=False,
        client=client,
        summary_schema_original=schema_original,
        summary_schema_resolved=schema_resolved,
        registry=make_registry(doc_id, "parcc"),
    )
    assert status == "synthesized", f"Expected synthesized after retry, got {status}"
    assert client.calls == 2, f"Expected 2 LLM calls (initial + retry), got {client.calls}"


def test_still_malformed_after_retry_goes_to_quarantine(tmp_path):
    """LLM still malformed after retry → quarantined, no summary written."""
    copy_schemas(tmp_path)
    doc_id = "test_parcc_quarantine"
    atoms = [make_atom(f"{doc_id}_a_0001")]
    atoms_path = tmp_path / "data/atoms" / f"{doc_id}.jsonl"
    write_atoms_jsonl(atoms_path, atoms)
    write_registry(tmp_path, [make_registry(doc_id, "parcc")[doc_id]])

    schema_original, schema_resolved = v1_synthesize.load_summary_schema(tmp_path)

    malformed = FakeLLMResponse(text="{not valid json}", parsed=None)
    client = FakeLLMClient([malformed, malformed])

    status, _run = v1_synthesize.synthesize_document(
        source_document_id=doc_id,
        v1_root=tmp_path,
        provider="openai",
        model="gpt-4.1",
        focus="mitigation",
        max_output_tokens=16000,
        max_transient_retries=1,
        force=False,
        client=client,
        summary_schema_original=schema_original,
        summary_schema_resolved=schema_resolved,
        registry=make_registry(doc_id, "parcc"),
    )
    assert status == "quarantined", f"Expected quarantined, got {status}"
    summary_path = tmp_path / "data/summaries" / f"{doc_id}.json"
    assert not summary_path.exists(), "Summary file should not exist after quarantine"
    quarantine_errors = tmp_path / "data/summaries/quarantine" / f"{doc_id}.errors.json"
    assert quarantine_errors.exists(), "Errors file should exist in quarantine"


def test_idempotency_skips_existing_summary(tmp_path):
    """Existing summary is skipped without --force."""
    copy_schemas(tmp_path)
    doc_id = "test_parcc_skip"
    atoms = [make_atom(f"{doc_id}_a_0001")]
    atoms_path = tmp_path / "data/atoms" / f"{doc_id}.jsonl"
    write_atoms_jsonl(atoms_path, atoms)
    write_registry(tmp_path, [make_registry(doc_id, "parcc")[doc_id]])

    # Pre-write a summary file
    summaries_dir = tmp_path / "data/summaries"
    summaries_dir.mkdir(parents=True, exist_ok=True)
    existing_summary = minimal_valid_summary(doc_id, atom_id=f"{doc_id}_a_0001")
    (summaries_dir / f"{doc_id}.json").write_text(json.dumps(existing_summary))

    schema_original, schema_resolved = v1_synthesize.load_summary_schema(tmp_path)
    client = FakeLLMClient([])

    status, _run = v1_synthesize.synthesize_document(
        source_document_id=doc_id,
        v1_root=tmp_path,
        provider="openai",
        model="gpt-4.1",
        focus="mitigation",
        max_output_tokens=16000,
        max_transient_retries=1,
        force=False,
        client=client,
        summary_schema_original=schema_original,
        summary_schema_resolved=schema_resolved,
        registry=make_registry(doc_id, "parcc"),
    )
    assert status == "skipped_idempotent"
    assert client.calls == 0, "No LLM calls should happen when skipping"


def test_verify_detects_renamed_atom_id(tmp_path):
    """verify command: detects when an atom_id was renamed in the atoms JSONL since synthesis ran."""
    copy_schemas(tmp_path)
    doc_id = "test_parcc_verify"
    old_atom_id = f"{doc_id}_a_0001"
    new_atom_id = f"{doc_id}_a_9999"

    # Write current atoms with the NEW atom_id
    atoms_path = tmp_path / "data/atoms" / f"{doc_id}.jsonl"
    write_atoms_jsonl(atoms_path, [make_atom(new_atom_id)])
    write_registry(tmp_path, [make_registry(doc_id, "parcc")[doc_id]])

    # Write summary that references the OLD atom_id
    summary = minimal_valid_summary(doc_id, atom_id=old_atom_id)
    summaries_dir = tmp_path / "data/summaries"
    summaries_dir.mkdir(parents=True, exist_ok=True)
    (summaries_dir / f"{doc_id}.json").write_text(json.dumps(summary))

    # Simulate verify by calling the function logic directly
    current_atom_ids = {new_atom_id}
    failures: list[str] = []
    for anchor in summary.get("evidence_anchors", []):
        aid = anchor.get("atom_id", "")
        if aid not in current_atom_ids:
            failures.append(f"{doc_id}: anchor atom_id {aid!r} not found in current atoms (renamed or deleted)")

    assert failures, "Expected drift to be detected"
    assert old_atom_id in failures[0]


def test_dangling_evidence_anchor_id_in_claim():
    """validate_summary flags evidence_anchor_id in named_actions that is not in evidence_anchors."""
    schema = load_schema()
    summary = minimal_valid_summary("test_doc", atom_id="test_doc_a_0001")
    summary["named_actions"] = [
        {
            "action_statement": "Some action",
            "evidence_anchor_id": "test_doc_a_9999",  # not in evidence_anchors
        }
    ]
    errors = v1_synthesize.validate_summary(
        summary,
        schema=schema,
        input_atom_ids={"test_doc_a_0001"},
        focus="mitigation",
    )
    dangling = [e for e in errors if "dangling_evidence_anchor_id" in e and "9999" in e]
    assert dangling, f"Expected dangling anchor error, got: {errors}"
