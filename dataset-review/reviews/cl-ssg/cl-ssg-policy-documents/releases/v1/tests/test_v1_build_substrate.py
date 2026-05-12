from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "v1_build_substrate.py"
spec = importlib.util.spec_from_file_location("v1_build_substrate", SCRIPT_PATH)
v1_build_substrate = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = v1_build_substrate
spec.loader.exec_module(v1_build_substrate)


def test_procurement_heading_marks_skip() -> None:
    pages = [
        (1, "# Overview\nBody"),
        (2, "No heading carry section"),
        (3, "# Procurement Procedures\nBody"),
        (4, "continuation"),
        (5, "# Implementation Plan\nBody"),
    ]
    patterns = v1_build_substrate.compile_skip_patterns(None, None, no_skip_patterns=False)
    infos = v1_build_substrate.build_page_infos(pages, patterns)
    by_page = {info.page: info for info in infos}
    assert by_page[3].skip is True
    assert by_page[3].skip_reason == "procurement"


def test_page_without_heading_inherits_previous_section() -> None:
    pages = [(1, "# Implementation Plan\ntext"), (2, "No heading here")]
    infos = v1_build_substrate.build_page_infos(pages, [])
    assert infos[1].current_section == "Implementation Plan"


def test_single_word_annex_does_not_update_current_section() -> None:
    pages = [(1, "# Background Context\ntext"), (2, "# Annex\ntext")]
    infos = v1_build_substrate.build_page_infos(pages, [])
    assert infos[1].current_section == "Background Context"


def test_two_word_heading_updates_current_section() -> None:
    pages = [(1, "# Background Context\ntext"), (2, "# Annex 1\ntext")]
    infos = v1_build_substrate.build_page_infos(pages, [])
    assert infos[1].current_section == "Annex 1"


def test_annex_admin_requires_annex_and_tail_keyword() -> None:
    patterns = v1_build_substrate.compile_skip_patterns(None, None, no_skip_patterns=False)
    assert (
        v1_build_substrate.match_skip_reason("Annex 1 - Detailed Project Description", patterns) is None
    )
    assert (
        v1_build_substrate.match_skip_reason("Annex 5 - Procurement Procedures", patterns)
        == "annex_admin"
    )


def test_idempotent_rerun_matching_sha_no_changes(tmp_path: Path) -> None:
    doc_json = tmp_path / "document.json"
    sha = "abc123"
    doc_json.write_text(json.dumps({"pdf_sha256": sha}), encoding="utf-8")
    assert v1_build_substrate.is_idempotent(doc_json, sha) is True


def test_force_rerun_ignores_idempotency(tmp_path: Path) -> None:
    root = tmp_path
    (root / "data/registry").mkdir(parents=True, exist_ok=True)
    (root / "data").mkdir(parents=True, exist_ok=True)
    (root / "policy-pdf").mkdir(parents=True, exist_ok=True)
    (root / "data/registry/source_documents.json").write_text(
        json.dumps({"source_documents": [{"source_document_id": "doc1", "source_name": "Doc One"}]}),
        encoding="utf-8",
    )
    (root / "data/source_pdf_map.csv").write_text(
        "source_document_id,proposed_pdf_path,confidence,status\n"
        "doc1,policy-pdf/doc1.pdf,high,confirmed\n",
        encoding="utf-8",
    )
    (root / "policy-pdf/doc1.pdf").write_bytes(b"fake-pdf")
    out_dir = root / "data/markdown/doc1"
    out_dir.mkdir(parents=True, exist_ok=True)
    sha = v1_build_substrate.sha256_file(root / "policy-pdf/doc1.pdf")
    (out_dir / "document.json").write_text(json.dumps({"pdf_sha256": sha, "page_count": 1}), encoding="utf-8")
    (out_dir / "section_map.json").write_text(
        json.dumps({"skip_stats": {"skipped_pages": 0, "skip_reasons": {}}, "pages": [{"page": 1}]}),
        encoding="utf-8",
    )

    original_extract = v1_build_substrate.extract_pdf_markdown_pages
    original_load_fit = v1_build_substrate.load_fitz
    original_load_llm = v1_build_substrate.load_pymupdf4llm
    try:
        v1_build_substrate.extract_pdf_markdown_pages = lambda _: ([(1, "# Heading\ntext")], 1, "")
        v1_build_substrate.load_fitz = lambda: object()
        v1_build_substrate.load_pymupdf4llm = lambda: type("L", (), {"__version__": "test"})()
        parser = v1_build_substrate.build_parser()
        args = parser.parse_args(["--root", str(root), "convert", "--force"])
        code = v1_build_substrate.command_convert(args)
        assert code == 0
        payload = json.loads((out_dir / "document.json").read_text(encoding="utf-8"))
        assert payload["char_count_total"] > 0
    finally:
        v1_build_substrate.extract_pdf_markdown_pages = original_extract
        v1_build_substrate.load_fitz = original_load_fit
        v1_build_substrate.load_pymupdf4llm = original_load_llm


def test_inspect_missing_source_document_id_nonzero(tmp_path: Path, capsys) -> None:
    parser = v1_build_substrate.build_parser()
    args = parser.parse_args(["--root", str(tmp_path), "inspect", "missing_doc"])
    code = v1_build_substrate.command_inspect(args)
    captured = capsys.readouterr()
    assert code == 1
    assert "Missing substrate for missing_doc" in captured.err


def test_low_text_pages_threshold() -> None:
    pages = [(1, "# Intro\nshort"), (2, "# Background Section\n" + ("a" * 100))]
    infos = v1_build_substrate.build_page_infos(pages, [])
    low = [item.page for item in infos if item.is_low_text]
    assert low == [1]


def test_extract_pdf_markdown_pages_falls_back_when_chunk_has_no_markers() -> None:
    class FakeDoc:
        def __init__(self) -> None:
            self.is_encrypted = False
            self.page_count = 2

        def authenticate(self, _password: str) -> bool:
            return True

        def close(self) -> None:
            return None

    class FakeFitz:
        @staticmethod
        def open(_path):
            return FakeDoc()

    original_load_fit = v1_build_substrate.load_fitz
    original_load_llm = v1_build_substrate.load_pymupdf4llm
    original_markdown_from_doc_chunk = v1_build_substrate.markdown_from_doc_chunk
    try:
        v1_build_substrate.load_fitz = lambda: FakeFitz()
        v1_build_substrate.load_pymupdf4llm = lambda: object()

        def fake_markdown_from_doc_chunk(_llm, _doc, pages_zero_based):
            if pages_zero_based == [0, 1]:
                return "no page markers in chunk output"
            if pages_zero_based == [0]:
                return "content page one"
            if pages_zero_based == [1]:
                return "content page two"
            return ""

        v1_build_substrate.markdown_from_doc_chunk = fake_markdown_from_doc_chunk
        pages, page_count, error = v1_build_substrate.extract_pdf_markdown_pages(Path("fake.pdf"))
        assert error == ""
        assert page_count == 2
        assert pages == [(1, "content page one"), (2, "content page two")]
    finally:
        v1_build_substrate.load_fitz = original_load_fit
        v1_build_substrate.load_pymupdf4llm = original_load_llm
        v1_build_substrate.markdown_from_doc_chunk = original_markdown_from_doc_chunk


def test_extract_pdf_markdown_pages_falls_back_when_chunk_markers_are_blank() -> None:
    class FakeDoc:
        def __init__(self) -> None:
            self.is_encrypted = False
            self.page_count = 2

        def authenticate(self, _password: str) -> bool:
            return True

        def close(self) -> None:
            return None

    class FakeFitz:
        @staticmethod
        def open(_path):
            return FakeDoc()

    original_load_fit = v1_build_substrate.load_fitz
    original_load_llm = v1_build_substrate.load_pymupdf4llm
    original_markdown_from_doc_chunk = v1_build_substrate.markdown_from_doc_chunk
    try:
        v1_build_substrate.load_fitz = lambda: FakeFitz()
        v1_build_substrate.load_pymupdf4llm = lambda: object()

        def fake_markdown_from_doc_chunk(_llm, _doc, pages_zero_based):
            if pages_zero_based == [0, 1]:
                return "<!-- page_break: 1 -->\n\n<!-- page_break: 2 -->\n"
            if pages_zero_based == [0]:
                return "recovered page one"
            if pages_zero_based == [1]:
                return "recovered page two"
            return ""

        v1_build_substrate.markdown_from_doc_chunk = fake_markdown_from_doc_chunk
        pages, page_count, error = v1_build_substrate.extract_pdf_markdown_pages(Path("fake.pdf"))
        assert error == ""
        assert page_count == 2
        assert pages == [(1, "recovered page one"), (2, "recovered page two")]
    finally:
        v1_build_substrate.load_fitz = original_load_fit
        v1_build_substrate.load_pymupdf4llm = original_load_llm
        v1_build_substrate.markdown_from_doc_chunk = original_markdown_from_doc_chunk


def test_parser_defaults_to_v1_local_paths() -> None:
    parser = v1_build_substrate.build_parser()
    args = parser.parse_args(["convert"])
    assert Path(args.root) == v1_build_substrate.V1_ROOT
    assert Path(args.map_csv) == v1_build_substrate.V1_ROOT / "data/source_pdf_map.csv"


def test_map_does_not_touch_confirmed_or_missing_source(tmp_path: Path) -> None:
    root = tmp_path
    (root / "data").mkdir(parents=True, exist_ok=True)
    (root / "policy-pdf").mkdir(parents=True, exist_ok=True)
    (root / "policy-pdf/Plan_de_Mitigación_Sector_Agricultura.pdf").write_bytes(b"fake-pdf")
    map_csv = root / "data/source_pdf_map.csv"
    map_csv.write_text(
        (
            "source_document_id,proposed_pdf_path,confidence,status\n"
            "doc_confirmed,policy-pdf/keep.pdf,high,confirmed\n"
            "doc_missing,policy-pdf/keep2.pdf,high,missing_source\n"
            "chl_agricultura_sector_plan,,high,proposed\n"
        ),
        encoding="utf-8",
    )
    parser = v1_build_substrate.build_parser()
    args = parser.parse_args(["--root", str(root), "map"])
    code = v1_build_substrate.command_map(args)
    assert code == 0
    rows = v1_build_substrate.read_rows(map_csv)
    by_id = {row["source_document_id"]: row for row in rows}
    assert by_id["doc_confirmed"]["proposed_pdf_path"] == "policy-pdf/keep.pdf"
    assert by_id["doc_missing"]["proposed_pdf_path"] == "policy-pdf/keep2.pdf"
    assert by_id["chl_agricultura_sector_plan"]["proposed_pdf_path"].startswith("policy-pdf/")
