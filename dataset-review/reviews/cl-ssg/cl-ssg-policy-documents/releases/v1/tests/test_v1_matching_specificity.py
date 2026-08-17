import sys
import unittest
import json
from collections import Counter
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import v1_match_atoms_to_action as matcher  # noqa: E402
import v1_score_city_actions as scorer  # noqa: E402


class MatcherSpecificityTest(unittest.TestCase):
    def setUp(self):
        self.atoms = {
            "a1": {
                "atom_id": "a1",
                "primitive_type": "action",
                "evidence_text": "Implementar un sistema público de bicicletas compartidas.",
                "page": 10,
                "section": "Movilidad",
            }
        }

    def finding(self, **overrides):
        finding = {
            "atom_id": "a1",
            "primitive_relation": "commits",
            "match_type": "direct",
            "policy_subject": "public bicycle-sharing system",
            "subject_match_reason": "The policy establishes the same bicycle-sharing intervention as the action.",
            "signal_confidence": "high",
            "explicitness": "explicit",
            "relevance_note": "Direct commitment to implement the action.",
        }
        finding.update(overrides)
        return finding

    def test_direct_match_preserves_high_relevance(self):
        payload = {"relevance": "high", "findings": [self.finding()]}
        findings, errors, warnings = matcher.validate_and_denormalise(payload, self.atoms)
        self.assertEqual([], errors)
        self.assertEqual("direct", findings[0]["match_type"])
        self.assertEqual("high", payload["relevance"])
        self.assertEqual([], warnings)

    def test_contradictory_direct_match_is_demoted_and_caps_relevance(self):
        payload = {
            "relevance": "high",
            "findings": [self.finding(
                subject_match_reason="Cycleways are indirectly related but do not establish bike sharing.",
                relevance_note="This is indirect enabling infrastructure.",
            )],
        }
        findings, errors, warnings = matcher.validate_and_denormalise(payload, self.atoms)
        self.assertEqual([], errors)
        self.assertEqual("indirect", findings[0]["match_type"])
        self.assertEqual("medium", payload["relevance"])
        self.assertIn("findings[0]:direct_match_demoted_to_indirect", warnings)
        self.assertIn("relevance_capped_by_match_type:high->medium", warnings)

    def test_contextual_only_caps_relevance_low(self):
        payload = {
            "relevance": "high",
            "findings": [self.finding(
                match_type="contextual",
                policy_subject="general sustainable mobility policy",
                subject_match_reason="The passage frames mobility policy but does not enable or establish bike sharing.",
            )],
        }
        _, errors, _ = matcher.validate_and_denormalise(payload, self.atoms)
        self.assertEqual([], errors)
        self.assertEqual("low", payload["relevance"])


class ScoringSpecificityTest(unittest.TestCase):
    @staticmethod
    def finding(match_type="direct", index=0):
        return {
            "atom_id": f"a{index}",
            "primitive_type": "action",
            "primitive_relation": "commits",
            "match_type": match_type,
            "policy_subject": "test subject",
            "subject_match_reason": "Specificity test evidence.",
            "signal_confidence": "high",
            "explicitness": "explicit",
            "evidence_text": f"Unique evidence passage number {index}.",
            "page": index + 1,
        }

    def score(self, findings, relevance="high"):
        index = {
            ("test_action", "test_doc"): {
                "schema_version": "2.2.0",
                "relevance": relevance,
                "findings": findings,
                "search_run": {"schema_check_passed": True},
            }
        }
        return scorer.score_city_action(
            "00000", "00", "Test", "test_action", "I.1",
            {"test_doc": 1.0}, index, None,
        )

    def test_match_type_weights(self):
        direct = scorer.finding_strength(self.finding("direct"), 1.0)
        indirect = scorer.finding_strength(self.finding("indirect"), 1.0)
        contextual = scorer.finding_strength(self.finding("contextual"), 1.0)
        self.assertEqual(1.0, direct)
        self.assertEqual(0.25, indirect)
        self.assertEqual(0.05, contextual)

    def test_indirect_evidence_cannot_create_strong_score(self):
        result = self.score([self.finding("indirect", i) for i in range(20)])
        self.assertEqual("medium", result["score_bucket"])
        self.assertTrue(result["direct_evidence_gate_applied"])
        self.assertEqual(0, result["direct_strong_evidence_count"])

    def test_direct_evidence_can_create_strong_score(self):
        result = self.score([self.finding("direct", i) for i in range(5)])
        self.assertEqual("strong", result["score_bucket"])
        self.assertFalse(result["direct_evidence_gate_applied"])
        self.assertEqual(5, result["direct_strong_evidence_count"])


class SpecificityRegressionFixtureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        v1 = Path(__file__).resolve().parents[1]
        cls.v1 = v1
        cls.fixture = json.loads(
            (v1 / "tests" / "fixtures" / "matching_specificity_regression.json").read_text()
        )
        cls.actions = json.loads((v1 / "data" / "registry" / "actions.json").read_text())
        registry_payload = json.loads(
            (v1 / "data" / "registry" / "source_documents.json").read_text()
        )
        cls.action_ids = {row["actionId"] for row in cls.actions}
        cls.doc_ids = {row["source_document_id"] for row in registry_payload["source_documents"]}

    def test_fixture_has_40_unique_stratified_cases(self):
        cases = self.fixture["cases"]
        keys = [(row["action_id"], row["source_document_id"]) for row in cases]
        self.assertEqual(40, len(cases))
        self.assertEqual(40, len(set(keys)))
        distribution = Counter(row["strongest_match_type"] for row in cases)
        self.assertGreaterEqual(distribution["direct"], 10)
        self.assertGreaterEqual(distribution["indirect"], 5)
        self.assertGreaterEqual(distribution["contextual"], 2)
        self.assertGreaterEqual(distribution["none"], 10)

    def test_fixture_references_existing_actions_documents_and_atoms(self):
        expected_relevance = {
            "direct": "high", "indirect": "medium", "contextual": "low", "none": "none"
        }
        for case in self.fixture["cases"]:
            with self.subTest(action=case["action_id"], doc=case["source_document_id"]):
                self.assertIn(case["action_id"], self.action_ids)
                self.assertIn(case["source_document_id"], self.doc_ids)
                self.assertEqual(
                    expected_relevance[case["strongest_match_type"]],
                    case["expected_relevance"],
                )
                atom_path = self.v1 / "data" / "atoms" / f"{case['source_document_id']}.jsonl"
                atoms = {
                    row["atom_id"]: row
                    for row in (json.loads(line) for line in atom_path.read_text().splitlines() if line.strip())
                }
                accepted_ids = {row["atom_id"] for row in case["accepted"]}
                rejected_ids = set(case["rejected"])
                self.assertFalse(accepted_ids & rejected_ids)
                self.assertTrue(accepted_ids | rejected_ids)
                for accepted in case["accepted"]:
                    self.assertIn(accepted["atom_id"], atoms)
                    self.assertIn(accepted["match_type"], matcher.ALLOWED_MATCH_TYPES)
                    evidence = " ".join(
                        atoms[accepted["atom_id"]].get("evidence_text", "").casefold().split()
                    )
                    expected_text = " ".join(accepted["evidence_contains"].casefold().split())
                    self.assertIn(expected_text, evidence)
                for atom_id in rejected_ids:
                    self.assertIn(atom_id, atoms)


if __name__ == "__main__":
    unittest.main()
