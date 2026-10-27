"""Tests for v1_derive_applicability.

Run with: python -m pytest releases/v1/tests/test_v1_applicability.py -v
or:       python releases/v1/tests/test_v1_applicability.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

V1 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(V1 / "scripts"))

import v1_derive_applicability as da  # noqa: E402


# Tiny synthetic fixture so tests do not depend on the live registry
DOCS = [
    {
        "source_document_id": "ndc",
        "source_level": "national",
        "document_type": "framework",
        "document_status": "final",
        "region_code": "00",
        "territory_code": "1_00_00",
        "review_priority": "high",
    },
    {
        "source_document_id": "eclp",
        "source_level": "national",
        "document_type": "framework",
        "document_status": "final",
        "region_code": "00",
        "territory_code": "1_00_00",
        "review_priority": "high",
    },
    {
        "source_document_id": "energia_plan",
        "source_level": "national",
        "document_type": "sector_plan",
        "document_status": "final",
        "region_code": "00",
        "territory_code": "1_00_00",
        "review_priority": "high",
    },
    {
        "source_document_id": "mineria_plan_draft",
        "source_level": "national",
        "document_type": "sector_plan",
        "document_status": "draft",
        "region_code": "00",
        "territory_code": "1_00_00",
        "review_priority": "high",
    },
    {
        "source_document_id": "parcc_R1",
        "source_level": "regional",
        "document_type": "parcc",
        "document_status": "final",
        "region_code": "01",
        "territory_code": "2_01_00",
        "review_priority": "high",
    },
    {
        "source_document_id": "parcc_R2_draft",
        "source_level": "regional",
        "document_type": "parcc",
        "document_status": "draft",
        "region_code": "02",
        "territory_code": "2_02_00",
        "review_priority": "high",
    },
    {
        "source_document_id": "parcc_R3_placeholder",
        "source_level": "regional",
        "document_type": "parcc",
        "document_status": "placeholder",
        "region_code": "03",
        "territory_code": "2_03_00",
        "review_priority": "low",
    },
    {
        "source_document_id": "pras_low_priority",
        "source_level": "municipal",
        "document_type": "environmental_program",
        "document_status": "final",
        "region_code": "01",
        "territory_code": "3_01_01101",
        "review_priority": "low",
    },
    {
        "source_document_id": "intercommunal_unresolved",
        "source_level": "intercommunal",
        "document_type": "territorial_plan",
        "document_status": "final",
        "region_code": "00",
        "territory_code": "4_00_00",
        "review_priority": "medium",
    },
    {
        "source_document_id": "intercommunal_R2",
        "source_level": "intercommunal",
        "document_type": "territorial_plan",
        "document_status": "final",
        "region_code": "02",
        "territory_code": "4_02_00",
        "review_priority": "medium",
    },
    {
        "source_document_id": "regional_missing_code",
        "source_level": "regional",
        "document_type": "parcc",
        "document_status": "final",
        "region_code": "00",
        "territory_code": "2_00_00",
        "review_priority": "high",
    },
]

CITIES = [
    {"city_code": "01101", "region_code": "01", "city_name": "City1A"},
    {"city_code": "01102", "region_code": "01", "city_name": "City1B"},
    {"city_code": "02101", "region_code": "02", "city_name": "City2A"},
    {"city_code": "02102", "region_code": "02", "city_name": "City2B"},
    {"city_code": "03101", "region_code": "03", "city_name": "City3A"},
]


class DeriveApplicabilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rows, self.log = da.derive_rows(
            documents=DOCS,
            cities=CITIES,
            include_low_priority=False,
            keep_drafts=True,
        )
        self.by_city = {}
        for r in self.rows:
            self.by_city.setdefault(r["city_code"], []).append(r)
        self.by_doc = {}
        for r in self.rows:
            self.by_doc.setdefault(r["source_document_id"], []).append(r)

    # --- National docs -------------------------------------------------------

    def test_every_city_gets_every_national_doc(self) -> None:
        national_docs = {"ndc", "eclp", "energia_plan", "mineria_plan_draft"}
        for city in CITIES:
            applied = {r["source_document_id"] for r in self.by_city.get(city["city_code"], [])}
            for nd in national_docs:
                self.assertIn(
                    nd,
                    applied,
                    f"city {city['city_code']} missing national doc {nd}",
                )

    def test_eclp_uses_per_doc_override(self) -> None:
        # The synthetic 'eclp' doc id does not match the real override key
        # ('chl_eclp_2021'), so it should fall back to the framework base 0.30.
        rows = self.by_doc["eclp"]
        self.assertTrue(all(r["proximity_weight_base"] == 0.30 for r in rows))

    def test_draft_status_penalty(self) -> None:
        rows = self.by_doc["mineria_plan_draft"]
        self.assertTrue(rows)
        for r in rows:
            self.assertEqual(r["status_multiplier"], 0.70)
            self.assertAlmostEqual(r["proximity_weight"], 0.50 * 0.70, places=4)

    # --- Regional docs -------------------------------------------------------

    def test_regional_final_doc_applies_only_to_matching_region(self) -> None:
        rows = self.by_doc["parcc_R1"]
        cities_hit = {r["city_code"] for r in rows}
        self.assertEqual(cities_hit, {"01101", "01102"})
        for r in rows:
            self.assertEqual(r["applicability_type"], "regional")
            self.assertEqual(r["proximity_weight"], 0.70)

    def test_regional_draft_uses_status_multiplier(self) -> None:
        rows = self.by_doc["parcc_R2_draft"]
        cities_hit = {r["city_code"] for r in rows}
        self.assertEqual(cities_hit, {"02101", "02102"})
        for r in rows:
            self.assertEqual(r["status_multiplier"], 0.70)
            self.assertAlmostEqual(r["proximity_weight"], 0.70 * 0.70, places=4)

    def test_regional_placeholder_excluded(self) -> None:
        self.assertNotIn("parcc_R3_placeholder", self.by_doc)
        skipped_ids = {s["source_document_id"] for s in self.log["skipped_documents"]}
        self.assertIn("parcc_R3_placeholder", skipped_ids)

    def test_regional_with_missing_region_code_is_skipped(self) -> None:
        self.assertNotIn("regional_missing_code", self.by_doc)
        skipped_ids = {s["source_document_id"] for s in self.log["skipped_documents"]}
        self.assertIn("regional_missing_code", skipped_ids)

    # --- Intercommunal docs --------------------------------------------------

    def test_intercommunal_with_resolved_region_applies_to_that_region(self) -> None:
        rows = self.by_doc["intercommunal_R2"]
        cities_hit = {r["city_code"] for r in rows}
        self.assertEqual(cities_hit, {"02101", "02102"})
        for r in rows:
            self.assertEqual(r["applicability_type"], "intercommunal")
            self.assertEqual(r["proximity_weight_base"], 0.85)

    def test_intercommunal_with_region_00_is_skipped(self) -> None:
        self.assertNotIn("intercommunal_unresolved", self.by_doc)
        skipped_ids = {s["source_document_id"] for s in self.log["skipped_documents"]}
        self.assertIn("intercommunal_unresolved", skipped_ids)

    # --- Municipal / low-priority -------------------------------------------

    def test_low_priority_excluded_by_default(self) -> None:
        self.assertNotIn("pras_low_priority", self.by_doc)
        skipped_ids = {s["source_document_id"] for s in self.log["skipped_documents"]}
        self.assertIn("pras_low_priority", skipped_ids)

    def test_low_priority_included_when_flagged(self) -> None:
        rows, log = da.derive_rows(
            documents=DOCS,
            cities=CITIES,
            include_low_priority=True,
            keep_drafts=True,
        )
        by_doc = {}
        for r in rows:
            by_doc.setdefault(r["source_document_id"], []).append(r)
        self.assertIn("pras_low_priority", by_doc)
        target = by_doc["pras_low_priority"]
        self.assertEqual(len(target), 1, "PRAS doc should apply to exactly one commune")
        self.assertEqual(target[0]["city_code"], "01101")
        self.assertEqual(target[0]["applicability_type"], "direct")
        self.assertEqual(target[0]["proximity_weight"], 1.00)

    # --- Drop-drafts mode ----------------------------------------------------

    def test_drop_drafts_suppresses_draft_and_consultation(self) -> None:
        rows, log = da.derive_rows(
            documents=DOCS,
            cities=CITIES,
            include_low_priority=False,
            keep_drafts=False,
        )
        ids = {r["source_document_id"] for r in rows}
        self.assertNotIn("mineria_plan_draft", ids)
        self.assertNotIn("parcc_R2_draft", ids)

    # --- Log summary ---------------------------------------------------------

    def test_log_summary_counts(self) -> None:
        self.assertEqual(self.log["input_documents"], len(DOCS))
        self.assertEqual(self.log["input_cities"], len(CITIES))
        self.assertEqual(self.log["output_rows"], len(self.rows))
        self.assertEqual(self.log["distinct_cities"], len({r["city_code"] for r in self.rows}))
        self.assertEqual(self.log["rubric_version"], da.RUBRIC_VERSION)


# Standalone helper for territory_code parsing
class TerritoryCodeParserTests(unittest.TestCase):
    def test_parses_municipal_code(self) -> None:
        self.assertEqual(da.commune_code_from_territory("3_05_05101"), "05101")

    def test_rejects_non_5_digit_commune(self) -> None:
        self.assertIsNone(da.commune_code_from_territory("3_05_5101"))

    def test_rejects_wrong_segment_count(self) -> None:
        self.assertIsNone(da.commune_code_from_territory("3_05"))

    def test_rejects_blank(self) -> None:
        self.assertIsNone(da.commune_code_from_territory(""))


if __name__ == "__main__":
    unittest.main(verbosity=2)
