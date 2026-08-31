"""Stage 2: extract every retrieved PDF into page-marked text."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone

from common import DOCUMENT_COLUMNS, REFERENCE, ROOT, read_csv, require, write_csv


def file_hash(path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--document")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    path = REFERENCE / "documents.csv"
    documents = read_csv(path)
    processed = 0
    skipped = 0

    for document in documents:
        if args.document and document["document_id"] != args.document:
            continue
        if document["retrieval_status"] != "downloaded" or not document["local_pdf"]:
            skipped += 1
            continue

        pdf = ROOT / document["local_pdf"]
        text_file = ROOT / (document["text_file"] or f"data/documents/text/{document['document_id']}.md")
        actual_hash = file_hash(pdf)
        require(not document["sha256"] or document["sha256"] == actual_hash,
                f"PDF hash changed: {document['document_id']}")
        if not args.force and text_file.exists() and document["extraction_status"] == "processed":
            skipped += 1
            continue

        info = subprocess.run(["pdfinfo", str(pdf)], check=True, capture_output=True, text=True).stdout
        page_count = int(re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE).group(1))
        raw_text = subprocess.run(
            ["pdftotext", "-layout", str(pdf), "-"], check=True, capture_output=True
        ).stdout.decode("utf-8", errors="replace")
        pages = raw_text.split("\f")
        if len(pages) > page_count and not pages[-1].strip():
            pages.pop()
        pages.extend([""] * (page_count - len(pages)))
        require(len(pages) == page_count, f"Page split failed: {document['document_id']}")

        header = [
            f"# {document['document_title']}", "",
            f"- Document ID: `{document['document_id']}`",
            f"- Source PDF: `{document['local_pdf']}`",
            f"- SHA-256: `{actual_hash}`",
            f"- Physical PDF pages: {page_count}",
            "- Extraction: Poppler pdftotext (-layout)", "", "---", "",
        ]
        body = []
        for number, page_text in enumerate(pages, start=1):
            body.extend([f"## PDF page {number}", "", page_text.rstrip(), ""])
        text_file.parent.mkdir(parents=True, exist_ok=True)
        text_file.write_text("\n".join(header + body).rstrip() + "\n", encoding="utf-8")

        document.update({
            "sha256": actual_hash,
            "page_count": str(page_count),
            "text_file": str(text_file.relative_to(ROOT)),
            "extraction_status": "processed",
            "extracted_page_count": str(page_count),
            "pages_with_text": str(sum(len(page.strip()) > 20 for page in pages)),
            "text_characters": str(sum(len(page) for page in pages)),
            "extraction_tool": "Poppler pdftotext (-layout)",
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            "extraction_note": "",
        })
        processed += 1

    if args.document:
        require(any(row["document_id"] == args.document for row in documents),
                f"Unknown document: {args.document}")
    write_csv(path, DOCUMENT_COLUMNS, documents)
    print(json.dumps({"processed": processed, "skipped": skipped}))


if __name__ == "__main__":
    main()
