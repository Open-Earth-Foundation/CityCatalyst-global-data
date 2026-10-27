"""Tests for source-text resolution used by atom validation."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

V1 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(V1 / "scripts"))

from v1_common import Document  # noqa: E402


class DocumentVerbatimTests(unittest.TestCase):
    def test_resolves_pdf_line_wrap_hyphens_to_the_original_offset(self) -> None:
        text = "Una medida evita perju-\ndicar a la comunidad."
        document = Document("fixture", text)

        self.assertEqual(
            document.find_verbatim("Una medida evita perjudicar a la comunidad."),
            0,
        )

    def test_does_not_accept_a_non_verbatim_rephrase(self) -> None:
        document = Document("fixture", "La comuna implementará una ciclovía.")

        self.assertIsNone(document.find_verbatim("La ciudad implementará una ciclovía."))


if __name__ == "__main__":
    unittest.main()
