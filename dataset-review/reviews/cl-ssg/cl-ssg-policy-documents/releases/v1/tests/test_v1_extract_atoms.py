from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "v1_extract_atoms.py"
spec = importlib.util.spec_from_file_location("v1_extract_atoms", SCRIPT_PATH)
v1_extract_atoms = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = v1_extract_atoms
spec.loader.exec_module(v1_extract_atoms)


class FakeValidator:
    def __init__(self, required: list[str]) -> None:
        self.required = required

    def iter_errors(self, atom):
        for key in self.required:
            if key not in atom:
                yield type("Err", (), {"message": f"'{key}' is a required property"})()


class FakeLLMClient:
    def __init__(self, responses):
        self.responses = responses
        self.calls = 0

    def complete(self, **_kwargs):
        response = self.responses[self.calls]
        self.calls += 1
        return response


def minimal_valid_atom(source_document_id: str, *, evidence_text: str, page_start: int = 1, page_end: int = 1):
    return {
        "atom_id": "tmp_a_0001",
        "source_document_id": source_document_id,
        "primitive_type": "action",
        "evidence_kind": "qualitative",
        "evidence_text": evidence_text,
        "page_start": page_start,
        "page_end": page_end,
        "explicitness": "explicit",
        "extraction_method": "atom_extractor",
    }


def test_batches_respect_section_boundaries() -> None:
    pages = [
        {"page": 1, "current_section": "A", "skip": False},
        {"page": 2, "current_section": "A", "skip": False},
        {"page": 3, "current_section": "B", "skip": False},
    ]
    batches = v1_extract_atoms.build_batches(pages)
    assert len(batches) == 2
    assert batches[0].pages == [1, 2]
    assert batches[1].pages == [3]


def test_batch_caps_at_four_pages() -> None:
    pages = [{"page": i, "current_section": "A", "skip": False} for i in range(1, 7)]
    batches = v1_extract_atoms.build_batches(pages)
    assert [batch.pages for batch in batches] == [[1, 2, 3, 4], [5, 6]]


def test_skipped_pages_break_contiguity() -> None:
    pages = [
        {"page": 1, "current_section": "A", "skip": False},
        {"page": 2, "current_section": "A", "skip": True},
        {"page": 3, "current_section": "A", "skip": False},
    ]
    batches = v1_extract_atoms.build_batches(pages)
    assert [batch.pages for batch in batches] == [[1], [3]]


def test_parse_response_bare_array() -> None:
    atoms, warning = v1_extract_atoms.parse_response_atoms([{"atom_id": "a"}])
    assert len(atoms) == 1
    assert warning is None


def test_parse_response_atoms_envelope() -> None:
    atoms, warning = v1_extract_atoms.parse_response_atoms({"atoms": [{"atom_id": "a"}]})
    assert len(atoms) == 1
    assert warning == "model_returned_envelope_shape_unwrapped_atoms"


def test_parse_response_extra_envelope_raises() -> None:
    try:
        v1_extract_atoms.parse_response_atoms({"foo": [{"atom_id": "a"}], "bar": True})
        raised = False
    except ValueError:
        raised = True
    assert raised is True


def test_evidence_paraphrase_rejected() -> None:
    atom = minimal_valid_atom("doc1", evidence_text="paraphrased sentence")
    valid, reason = v1_extract_atoms.validate_atom(
        atom,
        atom_validator=FakeValidator(
            [
                "atom_id",
                "source_document_id",
                "primitive_type",
                "evidence_kind",
                "evidence_text",
                "page_start",
                "page_end",
                "explicitness",
                "extraction_method",
            ]
        ),
        page_count=1,
        document_pages={1: "original sentence"},
        low_text_by_page={1: False},
    )
    assert valid is False
    assert reason == "evidence_not_verbatim"


def test_page_out_of_range_rejected() -> None:
    atom = minimal_valid_atom("doc1", evidence_text="x", page_start=1, page_end=3)
    valid, reason = v1_extract_atoms.validate_atom(
        atom,
        atom_validator=FakeValidator(["atom_id", "source_document_id", "primitive_type", "evidence_kind", "evidence_text", "page_start", "page_end", "explicitness", "extraction_method"]),
        page_count=2,
        document_pages={1: "x", 2: "y"},
        low_text_by_page={1: False, 2: False},
    )
    assert valid is False
    assert reason == "page_out_of_range"


def test_missing_required_field_rejected() -> None:
    atom = {
        "atom_id": "x",
        "source_document_id": "doc1",
    }
    valid, reason = v1_extract_atoms.validate_atom(
        atom,
        atom_validator=FakeValidator(["atom_id", "source_document_id", "primitive_type"]),
        page_count=1,
        document_pages={1: "x"},
        low_text_by_page={1: False},
    )
    assert valid is False
    assert reason and reason.startswith("schema_invalid:")


def test_denormalize_doc_type_and_section() -> None:
    patched = v1_extract_atoms.denormalize_atom({}, {"document_type": "parcc"}, "Section A")
    assert patched["_doc_type"] == "parcc"
    assert patched["_section"] == "Section A"


def test_resume_completed_batch_keys() -> None:
    keys = v1_extract_atoms.completed_batch_keys(
        {"batches": [{"section": "A", "page_start": 1}, {"section": "B", "page_start": 5}]}
    )
    assert ("A", 1) in keys
    assert ("B", 5) in keys


def test_dry_run_writes_nothing(tmp_path: Path) -> None:
    v1_root = tmp_path
    doc_id = "doc1"
    doc_dir = v1_root / "data/markdown" / doc_id
    doc_dir.mkdir(parents=True, exist_ok=True)
    (v1_root / "data/registry").mkdir(parents=True, exist_ok=True)
    (v1_root / "schemas").mkdir(parents=True, exist_ok=True)
    (v1_root / "schemas/extraction_rules.md").write_text("rules", encoding="utf-8")
    (v1_root / "schemas/atoms.schema.json").write_text(
        json.dumps(
            {
                "type": "object",
                "required": ["atom_id", "source_document_id", "primitive_type", "evidence_kind", "evidence_text", "page_start", "page_end", "explicitness", "extraction_method"],
                "properties": {
                    "atom_id": {"type": "string"},
                    "source_document_id": {"type": "string"},
                    "primitive_type": {"type": "string"},
                    "evidence_kind": {"type": "string"},
                    "evidence_text": {"type": "string"},
                    "page_start": {"type": "integer"},
                    "page_end": {"type": "integer"},
                    "explicitness": {"type": "string"},
                    "extraction_method": {"type": "string"},
                },
                "$defs": {},
            }
        ),
        encoding="utf-8",
    )
    (v1_root / "data/registry/source_documents.json").write_text(
        json.dumps({"source_documents": [{"source_document_id": doc_id, "document_type": "parcc"}]}),
        encoding="utf-8",
    )
    (doc_dir / "document.json").write_text(json.dumps({"page_count": 2, "char_count_total": 100, "low_text_pages": []}), encoding="utf-8")
    (doc_dir / "section_map.json").write_text(json.dumps({"pages": [{"page": 1, "current_section": "A", "skip": False}, {"page": 2, "current_section": "A", "skip": False}]}), encoding="utf-8")
    (doc_dir / "pages.jsonl").write_text(
        "\n".join(
            [
                json.dumps({"page": 1, "is_low_text": False}),
                json.dumps({"page": 2, "is_low_text": False}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (doc_dir / "document.md").write_text("<!-- page_break: 1 -->\ntext\n<!-- page_break: 2 -->\nmore\n", encoding="utf-8")

    atom_schema, atom_resolved = v1_extract_atoms.load_atom_schema(v1_root)
    status, _ = v1_extract_atoms.process_document(
        source_document_id=doc_id,
        v1_root=v1_root,
        provider="gemini",
        model="gemini-2.5-flash",
        max_output_tokens=1000,
        request_throttle_seconds=0.0,
        max_transient_retries=1,
        pages_override=None,
        force=False,
        resume=False,
        dry_run=True,
        client=None,
        atom_schema_original=atom_schema,
        atom_schema_resolved=atom_resolved,
        registry={doc_id: {"source_document_id": doc_id, "document_type": "parcc"}},
    )
    assert status == "dry_run"
    assert not (v1_root / "data/atoms" / f"{doc_id}.jsonl").exists()


def test_one_page_document_skipped_no_prechunk() -> None:
    reason = v1_extract_atoms.usable_substrate_reason({"page_count": 1, "char_count_total": 8, "low_text_pages": [1]})
    assert reason == "no_prechunk"


def test_normalize_strips_markdown_table_pipes() -> None:
    value = v1_extract_atoms.normalize_for_match("| a | b | c |")
    assert value == "a b c"


def test_normalize_strips_markdown_emphasis_markers() -> None:
    value = v1_extract_atoms.normalize_for_match("**Energia** _M1_")
    assert value == "energia m1"


def test_normalize_leaves_bare_text() -> None:
    value = v1_extract_atoms.normalize_for_match("Energia M1 2030")
    assert value == "energia m1 2030"


def test_normalize_markdown_table_phrase_matches_plain_phrase() -> None:
    substrate = "| **Energía** | _M1_ | **2030** |"
    evidence = "Energía M1 2030"
    assert v1_extract_atoms.normalize_for_match(evidence) in v1_extract_atoms.normalize_for_match(substrate)


def test_recover_truncated_array_recovers_complete_objects() -> None:
    raw = '[{"atom_id":"a1"},{"atom_id":"a2"},{"atom_id":"a3","evidence_text":"unterminated'
    recovered = v1_extract_atoms.recover_truncated_array(raw)
    assert recovered == [{"atom_id": "a1"}, {"atom_id": "a2"}]


def test_recover_truncated_array_no_complete_object_returns_none() -> None:
    raw = '[{"atom_id":"a1","evidence_text":"unterminated'
    recovered = v1_extract_atoms.recover_truncated_array(raw)
    assert recovered is None


def test_verbatim_retry_fires_once_when_over_half_rejected(tmp_path: Path) -> None:
    v1_root = tmp_path
    doc_id = "doc_retry"
    doc_dir = v1_root / "data/markdown" / doc_id
    doc_dir.mkdir(parents=True, exist_ok=True)
    (v1_root / "data/registry").mkdir(parents=True, exist_ok=True)
    (v1_root / "schemas").mkdir(parents=True, exist_ok=True)
    (v1_root / "schemas/extraction_rules.md").write_text("rules", encoding="utf-8")
    atom_schema_payload = {
        "type": "object",
        "required": [
            "atom_id",
            "source_document_id",
            "primitive_type",
            "evidence_kind",
            "evidence_text",
            "page_start",
            "page_end",
            "explicitness",
            "extraction_method",
        ],
        "properties": {
            "atom_id": {"type": "string"},
            "source_document_id": {"type": "string"},
            "primitive_type": {"type": "string"},
            "evidence_kind": {"type": "string"},
            "evidence_text": {"type": "string"},
            "page_start": {"type": "integer"},
            "page_end": {"type": "integer"},
            "explicitness": {"type": "string"},
            "extraction_method": {"type": "string"},
            "_doc_type": {"type": "string"},
            "_section": {"type": "string"},
        },
        "$defs": {},
    }
    (v1_root / "schemas/atoms.schema.json").write_text(json.dumps(atom_schema_payload), encoding="utf-8")
    (v1_root / "data/registry/source_documents.json").write_text(
        json.dumps({"source_documents": [{"source_document_id": doc_id, "document_type": "parcc"}]}),
        encoding="utf-8",
    )
    (doc_dir / "document.json").write_text(json.dumps({"page_count": 1, "char_count_total": 100, "low_text_pages": []}), encoding="utf-8")
    (doc_dir / "section_map.json").write_text(
        json.dumps({"pages": [{"page": 1, "current_section": "A", "skip": False}]}),
        encoding="utf-8",
    )
    (doc_dir / "pages.jsonl").write_text(json.dumps({"page": 1, "is_low_text": False}) + "\n", encoding="utf-8")
    (doc_dir / "document.md").write_text("<!-- page_break: 1 -->\nExact sentence one.\nExact sentence two.\n", encoding="utf-8")

    first_batch_atoms = [
        minimal_valid_atom(doc_id, evidence_text="Exact sentence one."),
        minimal_valid_atom(doc_id, evidence_text="Paraphrased not present"),
        minimal_valid_atom(doc_id, evidence_text="Also missing"),
    ]
    first_batch_atoms[0]["atom_id"] = "doc_retry_a_0001"
    first_batch_atoms[1]["atom_id"] = "doc_retry_a_0002"
    first_batch_atoms[2]["atom_id"] = "doc_retry_a_0003"

    retry_atoms = [
        minimal_valid_atom(doc_id, evidence_text="Exact sentence two."),
    ]
    retry_atoms[0]["atom_id"] = "doc_retry_a_0002"

    fake = FakeLLMClient(
        [
            v1_extract_atoms.LLMResponse(text=json.dumps(first_batch_atoms), parsed=first_batch_atoms, finish_reason="STOP"),
            v1_extract_atoms.LLMResponse(text=json.dumps(retry_atoms), parsed=retry_atoms, finish_reason="STOP"),
        ]
    )
    atom_schema, atom_resolved = v1_extract_atoms.load_atom_schema(v1_root)
    status, run_payload = v1_extract_atoms.process_document(
        source_document_id=doc_id,
        v1_root=v1_root,
        provider="gemini",
        model="gemini-2.5-flash",
        max_output_tokens=2000,
        request_throttle_seconds=0.0,
        max_transient_retries=1,
        pages_override=None,
        force=True,
        resume=False,
        dry_run=False,
        client=fake,
        atom_schema_original=atom_schema,
        atom_schema_resolved=atom_resolved,
        registry={doc_id: {"source_document_id": doc_id, "document_type": "parcc"}},
    )
    assert status == "processed"
    assert fake.calls == 2
    assert run_payload is not None
    notes = run_payload["batches"][0].get("notes", [])
    assert any("verbatim_retry:" in note for note in notes)


def setup_single_page_doc(tmp_path: Path, doc_id: str, page_text: str = "e1\ne2\ne3\ne4\ne5\ne6\ne7\ne8\ne9\ne10\n") -> tuple[Path, dict]:
    v1_root = tmp_path
    doc_dir = v1_root / "data/markdown" / doc_id
    doc_dir.mkdir(parents=True, exist_ok=True)
    (v1_root / "data/registry").mkdir(parents=True, exist_ok=True)
    (v1_root / "schemas").mkdir(parents=True, exist_ok=True)
    (v1_root / "schemas/extraction_rules.md").write_text("rules", encoding="utf-8")
    atom_schema_payload = {
        "type": "object",
        "required": [
            "atom_id",
            "source_document_id",
            "primitive_type",
            "evidence_kind",
            "evidence_text",
            "page_start",
            "page_end",
            "explicitness",
            "extraction_method",
        ],
        "properties": {
            "atom_id": {"type": "string"},
            "source_document_id": {"type": "string"},
            "primitive_type": {"type": "string"},
            "evidence_kind": {"type": "string"},
            "evidence_text": {"type": "string"},
            "page_start": {"type": "integer"},
            "page_end": {"type": "integer"},
            "explicitness": {"type": "string"},
            "extraction_method": {"type": "string"},
            "_doc_type": {"type": "string"},
            "_section": {"type": "string"},
        },
        "$defs": {},
    }
    (v1_root / "schemas/atoms.schema.json").write_text(json.dumps(atom_schema_payload), encoding="utf-8")
    (v1_root / "data/registry/source_documents.json").write_text(
        json.dumps({"source_documents": [{"source_document_id": doc_id, "document_type": "parcc"}]}),
        encoding="utf-8",
    )
    (doc_dir / "document.json").write_text(json.dumps({"page_count": 2, "char_count_total": 100, "low_text_pages": []}), encoding="utf-8")
    (doc_dir / "section_map.json").write_text(
        json.dumps({"pages": [{"page": 1, "current_section": "A", "skip": False}, {"page": 2, "current_section": "A", "skip": True}]}),
        encoding="utf-8",
    )
    (doc_dir / "pages.jsonl").write_text(
        "\n".join([json.dumps({"page": 1, "is_low_text": False}), json.dumps({"page": 2, "is_low_text": False})]) + "\n",
        encoding="utf-8",
    )
    (doc_dir / "document.md").write_text(f"<!-- page_break: 1 -->\n{page_text}\n<!-- page_break: 2 -->\nignored\n", encoding="utf-8")
    atom_schema, atom_resolved = v1_extract_atoms.load_atom_schema(v1_root)
    return v1_root, {
        "atom_schema": atom_schema,
        "atom_resolved": atom_resolved,
        "registry": {doc_id: {"source_document_id": doc_id, "document_type": "parcc"}},
    }


def run_process(v1_root: Path, doc_id: str, fake: FakeLLMClient, ctx: dict) -> tuple[str, dict | None]:
    return v1_extract_atoms.process_document(
        source_document_id=doc_id,
        v1_root=v1_root,
        provider="gemini",
        model="gemini-2.5-flash",
        max_output_tokens=2000,
        request_throttle_seconds=0.0,
        max_transient_retries=1,
        pages_override=None,
        force=True,
        resume=False,
        dry_run=False,
        client=fake,
        atom_schema_original=ctx["atom_schema"],
        atom_schema_resolved=ctx["atom_resolved"],
        registry=ctx["registry"],
    )


def test_write_path_first_pass_only_counts_match(tmp_path: Path) -> None:
    doc_id = "doc_first_pass"
    v1_root, ctx = setup_single_page_doc(tmp_path, doc_id)
    atoms = []
    for idx in range(1, 11):
        atom = minimal_valid_atom(doc_id, evidence_text=f"e{idx}")
        atom["atom_id"] = f"{doc_id}_a_{idx:04d}"
        atoms.append(atom)
    fake = FakeLLMClient([v1_extract_atoms.LLMResponse(text=json.dumps(atoms), parsed=atoms, finish_reason="STOP")])
    status, run_payload = run_process(v1_root, doc_id, fake, ctx)
    assert status == "processed"
    assert run_payload is not None
    assert run_payload["totals"]["atoms_accepted"] == 10
    jsonl_path = v1_root / "data/atoms" / f"{doc_id}.jsonl"
    assert v1_extract_atoms.jsonl_line_count(jsonl_path) == 10


def test_write_path_retry_only_recovers_atoms(tmp_path: Path) -> None:
    doc_id = "doc_retry_only"
    v1_root, ctx = setup_single_page_doc(tmp_path, doc_id)
    first_pass = []
    for idx in range(1, 9):
        atom = minimal_valid_atom(doc_id, evidence_text=f"missing{idx}")
        atom["atom_id"] = f"{doc_id}_a_{idx:04d}"
        first_pass.append(atom)
    retry_pass = []
    for idx in range(1, 9):
        atom = minimal_valid_atom(doc_id, evidence_text=f"e{idx}")
        atom["atom_id"] = f"{doc_id}_a_{idx:04d}"
        retry_pass.append(atom)
    fake = FakeLLMClient(
        [
            v1_extract_atoms.LLMResponse(text=json.dumps(first_pass), parsed=first_pass, finish_reason="STOP"),
            v1_extract_atoms.LLMResponse(text=json.dumps(retry_pass), parsed=retry_pass, finish_reason="STOP"),
        ]
    )
    status, run_payload = run_process(v1_root, doc_id, fake, ctx)
    assert status == "processed"
    assert run_payload is not None
    assert run_payload["totals"]["atoms_accepted"] == 8
    jsonl_path = v1_root / "data/atoms" / f"{doc_id}.jsonl"
    assert v1_extract_atoms.jsonl_line_count(jsonl_path) == 8


def test_retry_merge_by_id_replaces_and_extends(tmp_path: Path) -> None:
    doc_id = "doc_merge"
    page_text = "e1\ne2\ne3\ne3r\ne4\ne4r\ne5\ne6\n"
    v1_root, ctx = setup_single_page_doc(tmp_path, doc_id, page_text=page_text)
    first = []
    for atom_id, text in [("a1", "e1"), ("a2", "e2"), ("a3", "e3"), ("a4", "e4"), ("a5", "e5"), ("a6", "missing6"), ("a7", "missing7"), ("a8", "missing8"), ("a9", "missing9"), ("a10", "missing10")]:
        atom = minimal_valid_atom(doc_id, evidence_text=text)
        atom["atom_id"] = atom_id
        first.append(atom)
    retry = []
    for atom_id, text in [("a3", "e3r"), ("a4", "e4r"), ("a6", "e6")]:
        atom = minimal_valid_atom(doc_id, evidence_text=text)
        atom["atom_id"] = atom_id
        retry.append(atom)
    fake = FakeLLMClient(
        [
            v1_extract_atoms.LLMResponse(text=json.dumps(first), parsed=first, finish_reason="STOP"),
            v1_extract_atoms.LLMResponse(text=json.dumps(retry), parsed=retry, finish_reason="STOP"),
        ]
    )
    status, run_payload = run_process(v1_root, doc_id, fake, ctx)
    assert status == "processed"
    assert run_payload is not None
    assert run_payload["totals"]["atoms_accepted"] == 6
    rows = v1_extract_atoms.load_existing_jsonl(v1_root / "data/atoms" / f"{doc_id}.jsonl")
    evidence_set = {row["evidence_text"] for row in rows}
    assert len(rows) == 6
    assert "e3r" in evidence_set
    assert "e4r" in evidence_set
    assert "e6" in evidence_set
    assert "e3" not in evidence_set
    assert "e4" not in evidence_set


def test_end_of_run_assertion_fails_when_writer_drops_rows(tmp_path: Path) -> None:
    doc_id = "doc_writer_drop"
    v1_root, ctx = setup_single_page_doc(tmp_path, doc_id)
    atoms = []
    for idx in range(1, 4):
        atom = minimal_valid_atom(doc_id, evidence_text=f"e{idx}")
        atom["atom_id"] = f"{doc_id}_a_{idx:04d}"
        atoms.append(atom)
    fake = FakeLLMClient([v1_extract_atoms.LLMResponse(text=json.dumps(atoms), parsed=atoms, finish_reason="STOP")])

    original_append = v1_extract_atoms.append_jsonl

    def dropping_append(path: Path, rows):
        keep = rows[:-1] if rows else rows
        return original_append(path, keep)

    v1_extract_atoms.append_jsonl = dropping_append
    try:
        try:
            run_process(v1_root, doc_id, fake, ctx)
            raised = False
        except RuntimeError as exc:
            raised = "jsonl_write_mismatch" in str(exc)
    finally:
        v1_extract_atoms.append_jsonl = original_append
    assert raised is True
