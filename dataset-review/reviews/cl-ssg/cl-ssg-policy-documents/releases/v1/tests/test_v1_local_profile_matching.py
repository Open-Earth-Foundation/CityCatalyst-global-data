from __future__ import annotations

import sys
import json
import unittest
from pathlib import Path


V1 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(V1 / "scripts"))

import v1_local_match_profiles as local_match  # noqa: E402


class LocalProfileMatchingTest(unittest.TestCase):
    def test_all_action_profiles_have_reviewed_boundaries(self):
        profiles = json.loads(
            (V1 / "data" / "registry" / "action_matching_profiles.json").read_text(encoding="utf-8")
        )["profiles"]
        self.assertEqual(len(profiles), 102)
        self.assertTrue(all(p["profile_status"] == "pilot_reviewed" for p in profiles))
        self.assertTrue(all(p.get("reviewed_rules", {}).get("direct_phrases") for p in profiles))

    def test_word_boundaries_do_not_confuse_reforestation_and_deforestation(self):
        self.assertTrue(local_match.contains_any("plan de reforestacion", ["reforestacion"]))
        self.assertFalse(local_match.contains_any("reducir la deforestacion", ["reforestacion"]))

    def test_explicit_prefix_marker_handles_spanish_inflection(self):
        text = local_match.normalize("Reducir las pérdidas eléctricas mejora la eficiencia")
        self.assertTrue(local_match.contains_any(text, ["reduci*"]))
        self.assertTrue(local_match.contains_any(text, ["eficien*"]))
        self.assertFalse(local_match.contains_any(text, ["electromov*"]))

    def test_reviewed_direct_rule_precedes_exclusion(self):
        rules = {
            "direct_phrases": ["buses electricos"],
            "exclude_phrases": ["transporte publico"],
        }
        text = local_match.normalize("Adquisición de buses eléctricos para transporte público")
        self.assertEqual(local_match.classify_reviewed(text, rules), "direct")

    def test_exclusion_blocks_an_indirect_sector_coincidence(self):
        rules = {
            "indirect_phrases": ["ciclovias"],
            "exclude_phrases": ["transporte publico limpio"],
        }
        text = local_match.normalize("Transporte público limpio, como ciclovías y vehículos eléctricos")
        self.assertIsNone(local_match.classify_reviewed(text, rules))

    def test_unreviewed_fallback_is_never_direct(self):
        profile = {"distinctive_anchors": ["paneles solares municipales"]}
        text = local_match.normalize("Instalar paneles solares municipales")
        self.assertEqual(local_match.classify_fallback(text, profile), "indirect")

    def test_measure_type_is_canonical(self):
        self.assertEqual(local_match.canonical_measure_type("mitigación."), "mitigation")
        self.assertEqual(local_match.canonical_measure_type("adaptación"), "adaptation")
        self.assertEqual(local_match.canonical_measure_type("program"), "unknown")

    def test_reviewed_false_positive_boundaries(self):
        cases = [
            ({"direct_phrases": ["recuperacion de calor"]}, "eficiencia energetica industrial"),
            ({"direct_phrases": ["cogeneracion"]}, "energia renovable"),
            ({"direct_phrases": ["tarifa horaria"]}, "gestion de la demanda"),
            ({"direct_phrases": ["captura y almacenamiento de carbono"]}, "consejos de cambio climatico ccs"),
            ({"direct_phrases": ["relleno sanitario con captura de biogas"]}, "programa de compostaje"),
            ({"direct_phrases": ["suficiencia en el consumo"]}, "reduccion del consumo de agua"),
            ({"direct_phrases": ["bioenergia con captura de carbono"]}, "captura de biogas"),
        ]
        for rules, text in cases:
            with self.subTest(text=text):
                self.assertIsNone(local_match.classify_reviewed(local_match.normalize(text), rules))


if __name__ == "__main__":
    unittest.main()
