from __future__ import annotations

import json
import math
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_PATH = (
    ROOT
    / "production_candidates"
    / "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v4_binding_fix.json"
)
MU_UNRESOLVED = "MU UNRESOLVED"


def used_component(raw: float | None) -> float:
    if raw is None or not isinstance(raw, (int, float)) or raw <= 0:
        return 0.0
    return float(raw)


def conditional_component_mu(used: float, lookup: float | None) -> float | str:
    if used == 0:
        return ""
    if not isinstance(lookup, (int, float)):
        return MU_UNRESOLVED
    return float(lookup)


def combined_mu(
    used_1: float,
    used_2: float,
    mu_1: float | str,
    mu_2: float | str,
) -> float | str:
    total = used_1 + used_2
    if total <= 0:
        return ""
    if used_1 > 0 and used_2 == 0:
        return mu_1 if isinstance(mu_1, float) else MU_UNRESOLVED
    if used_1 == 0 and used_2 > 0:
        return mu_2 if isinstance(mu_2, float) else MU_UNRESOLVED
    if not isinstance(mu_1, float) or not isinstance(mu_2, float):
        return MU_UNRESOLVED
    return 100 * math.sqrt((used_1 * mu_1 / 100) ** 2 + (used_2 * mu_2 / 100) ** 2) / total


class Phase4A6FConditionalComponentMUTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        candidate = json.loads(CANDIDATE_PATH.read_text(encoding="utf-8"))
        cls.specifications = candidate["data"]["Specifications"]

    def test_candidate_formulas_gate_component_mu_on_positive_used_values(self) -> None:
        expected_gates = {
            "O19": (18, 14, "M19=0", '"Nerolidol 1","MU"'),
            "P19": (18, 15, "N19=0", '"Nerolidol 2","MU"'),
            "O20": (19, 14, "M20=0", '"Ocimene 1","MU"'),
            "P20": (19, 15, "N20=0", '"Ocimene 2","MU"'),
        }
        for cell, (row, column, zero_gate, lookup_key) in expected_gates.items():
            with self.subTest(cell=cell):
                formula = self.specifications[row][column]
                self.assertIn(f'IF({zero_gate},"",', formula)
                self.assertIn(lookup_key, formula)

    def test_blank_raw_component_keeps_mu_blank(self) -> None:
        used = used_component(None)
        self.assertEqual(used, 0)
        self.assertEqual(conditional_component_mu(used, 4), "")

    def test_zero_raw_component_keeps_mu_blank(self) -> None:
        used = used_component(0)
        self.assertEqual(used, 0)
        self.assertEqual(conditional_component_mu(used, 4), "")

    def test_negative_raw_component_keeps_mu_blank(self) -> None:
        used = used_component(-2.5)
        self.assertEqual(used, 0)
        self.assertEqual(conditional_component_mu(used, 11), "")

    def test_positive_component_resolves_mu(self) -> None:
        used = used_component(3.25)
        self.assertEqual(used, 3.25)
        self.assertEqual(conditional_component_mu(used, 4), 4)

    def test_positive_component_with_missing_mu_is_unresolved(self) -> None:
        used = used_component(3.25)
        mu = conditional_component_mu(used, None)
        self.assertEqual(mu, MU_UNRESOLVED)
        self.assertEqual(combined_mu(used, 0, mu, ""), MU_UNRESOLVED)

    def test_one_positive_and_one_nonpositive_component_uses_positive_mu(self) -> None:
        used_1 = used_component(12.5)
        used_2 = used_component(-2.5)
        mu_1 = conditional_component_mu(used_1, 7)
        mu_2 = conditional_component_mu(used_2, 11)
        self.assertEqual(combined_mu(used_1, used_2, mu_1, mu_2), 7)

    def test_two_positive_components_use_independent_relative_propagation(self) -> None:
        used_1 = used_component(3.25)
        used_2 = used_component(9.75)
        mu_1 = conditional_component_mu(used_1, 4)
        mu_2 = conditional_component_mu(used_2, 8)
        actual = combined_mu(used_1, used_2, mu_1, mu_2)
        self.assertIsInstance(actual, float)
        self.assertAlmostEqual(actual, 6.08276253029822, places=14)


if __name__ == "__main__":
    unittest.main()
