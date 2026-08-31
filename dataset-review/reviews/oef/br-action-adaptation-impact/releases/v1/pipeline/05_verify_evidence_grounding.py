"""Stage 5: verify every evidence quote against its cited extracted PDF page."""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher

from common import OUTPUT, REFERENCE, ROOT, read_csv, require, write_csv


EVIDENCE_COLUMNS = [
    "schema_version", "evidence_id", "mapping_id", "source_id", "pdf_page",
    "printed_page", "quote_verbatim", "quote_language", "grounding_status",
    "grounding_note", "direction", "quantified_value", "support_scope",
    "maladaptation_signal", "extraction_run_id", "review_status",
    "reviewed_by", "reviewed_at", "review_note",
]
VALID_REVIEW_STATUSES = {"proposed", "needs_review", "accepted", "rejected"}


def normalized_words(value: str) -> list[str]:
    """Normalize punctuation, Unicode and line-break hyphenation for comparison."""
    value = unicodedata.normalize("NFKC", value).replace("\u00ad", "")
    value = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", value)
    return re.sub(r"[^\w]+", " ", value.casefold()).split()


def extracted_pages(text: str) -> dict[int, str]:
    """Read the page markers written by Stage 2."""
    parts = re.split(r"(?m)^## PDF page (\d+)\s*$", text)
    return {int(parts[index]): parts[index + 1] for index in range(1, len(parts), 2)}


def grounding_result(quote: str, page_text: str) -> tuple[str, str]:
    quote_words = normalized_words(quote)
    page_words = normalized_words(page_text)
    require(bool(quote_words), "Evidence quote is empty")
    require(bool(page_words), "Cited PDF page has no extracted text")

    quote_text = " ".join(quote_words)
    page_text_normalized = " ".join(page_words)
    if quote_text in page_text_normalized:
        return "verified_exact", "Normalized quote occurs on the cited PDF page."

    matcher = SequenceMatcher(None, quote_words, page_words, autojunk=False)
    blocks = matcher.get_matching_blocks()
    ordered_coverage = sum(block.size for block in blocks) / len(quote_words)
    if ordered_coverage >= 0.95:
        return (
            "verified_ordered",
            f"Ordered token coverage on the cited PDF page is {ordered_coverage:.1%}.",
        )

    quote_counts = Counter(quote_words)
    page_counts = Counter(page_words)
    token_coverage = sum(
        min(count, page_counts[word]) for word, count in quote_counts.items()
    ) / len(quote_words)
    longest_block = max(block.size for block in blocks)
    minimum_anchor = min(5, max(2, len(quote_words) // 4))

    layout_match = (
        longest_block >= minimum_anchor
        and (token_coverage >= 0.98 or ordered_coverage >= 0.90)
    )
    require(
        layout_match,
        "Quote is not sufficiently present on the cited PDF page "
        f"(ordered coverage {ordered_coverage:.1%}, token coverage "
        f"{token_coverage:.1%}, longest ordered block {longest_block} words)",
    )
    return (
        "layout_match",
        "Quote text is present but PDF columns or tables changed its extraction order; "
        f"ordered coverage is {ordered_coverage:.1%} and token coverage is "
        f"{token_coverage:.1%}. Confirm visually during evidence review.",
    )


def main() -> None:
    path = OUTPUT / "evidence.csv"
    evidence = read_csv(path)
    sources = {
        row["source_id"]: row
        for row in read_csv(REFERENCE / "sector_sources.csv")
    }
    documents = {
        row["document_id"]: row
        for row in read_csv(REFERENCE / "documents.csv")
    }
    page_cache: dict[str, dict[int, str]] = {}
    counts = {"verified_exact": 0, "verified_ordered": 0, "layout_match": 0}

    for row in evidence:
        evidence_id = row["evidence_id"]
        require(
            row["review_status"] in VALID_REVIEW_STATUSES,
            f"Invalid evidence review status: {evidence_id}",
        )
        source = sources.get(row["source_id"])
        require(source is not None, f"Unknown evidence source: {evidence_id}")
        document = documents.get(source["document_id"])
        require(document is not None, f"Unknown evidence document: {evidence_id}")
        require(document["text_file"], f"Evidence document has no extracted text: {evidence_id}")

        if document["document_id"] not in page_cache:
            text_path = ROOT / document["text_file"]
            require(text_path.exists(), f"Extracted document text is missing: {evidence_id}")
            page_cache[document["document_id"]] = extracted_pages(
                text_path.read_text(encoding="utf-8")
            )
        page = int(row["pdf_page"])
        page_text = page_cache[document["document_id"]].get(page, "")
        try:
            status, note = grounding_result(row["quote_verbatim"], page_text)
        except ValueError as error:
            raise ValueError(f"Evidence grounding failed for {evidence_id}: {error}") from error

        row["grounding_status"] = status
        row["grounding_note"] = note
        if status == "layout_match" and row["review_status"] == "proposed":
            row["review_status"] = "needs_review"
        counts[status] += 1

    write_csv(path, EVIDENCE_COLUMNS, evidence)
    print(json.dumps({"evidence": len(evidence), **counts, "status": "valid"}))


if __name__ == "__main__":
    main()
