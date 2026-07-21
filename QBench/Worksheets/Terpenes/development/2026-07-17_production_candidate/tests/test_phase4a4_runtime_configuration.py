from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parents[1]
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

import build_phase3_candidates as phase3_builder
import build_phase3_candidates_v3 as v3_builder
import validate_phase3_candidates as phase3_validator
import validate_phase3_candidates_v2 as v2_validator
import validate_phase4a4_v3 as v3_validator


class Phase4A4RuntimeConfigurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = v3_builder.load_profile()
        cls.candidate = v3_builder.build_candidate(cls.profile)

    def mutated_spec_value(self, row_index: int, value: str):
        candidate = copy.deepcopy(self.candidate)
        specifications = v3_validator.worksheet(candidate, "Specifications")
        specifications["data"][row_index][20] = value
        candidate["data"]["Specifications"] = copy.deepcopy(specifications["data"])
        return candidate

    def test_unresolved_u2_fails(self):
        with self.assertRaisesRegex(AssertionError, "unresolved configuration marker"):
            v3_validator.validate_runtime_configuration(
                self.mutated_spec_value(1, v3_builder.UNRESOLVED), self.profile
            )

    def test_unresolved_u4_fails(self):
        with self.assertRaisesRegex(AssertionError, "unresolved configuration marker"):
            v3_validator.validate_runtime_configuration(
                self.mutated_spec_value(3, v3_builder.UNRESOLVED), self.profile
            )

    def test_blank_u2_fails(self):
        with self.assertRaisesRegex(AssertionError, "U2 store binding is unresolved"):
            v3_validator.validate_runtime_configuration(self.mutated_spec_value(1, ""), self.profile)

    def test_blank_matrix_source_fails(self):
        profile = copy.deepcopy(self.profile)
        profile["matrix_source"] = ""
        with self.assertRaisesRegex(AssertionError, "matrix_source must be resolved"):
            v3_builder.validate_profile(profile)

    def test_static_one_matrix_hardcoding_fails(self):
        candidate = self.mutated_spec_value(3, "SBX_ONLY_RUNTIME_MATRIX_V2")
        with self.assertRaisesRegex(AssertionError, "fixed matrix"):
            v3_validator.validate_runtime_configuration(candidate, self.profile)

    def test_valid_environment_binding_passes(self):
        result = v3_validator.validate_runtime_configuration(self.candidate, self.profile)
        self.assertEqual(result["unresolved_markers"], 0)

    def test_valid_dynamic_matrix_reference_passes(self):
        self.assertEqual(
            v3_validator.worksheet(self.candidate, "Specifications")["data"][3][20],
            v3_builder.DYNAMIC_MATRIX_SOURCE,
        )
        self.assertEqual(
            v3_validator.worksheet(self.candidate, "Data")["data"][1][2],
            v3_builder.DYNAMIC_MATRIX_SOURCE,
        )

    def test_exact_43_writable_destinations_remain_unchanged(self):
        destinations = v3_validator.exact_destination_contract(self.candidate)
        v2 = v3_validator.load_json(v3_validator.V2_PATH)
        expected = {k: v for k, v in v2["qb_config"]["named_cells"].items() if k != "report_results"}
        self.assertEqual(destinations, expected)

    def test_renderer_compatibility_still_passes(self):
        historical = v3_validator.load_json(phase3_validator.HISTORICAL_TEST_PATH)
        result = v2_validator.validate_renderer_contract(
            self.candidate,
            historical,
            {"Report": "Report", "Data": "Data", "Specifications": "Specifications"},
            "Test v3",
        )
        self.assertEqual(result["formula_count"], 309)

    def test_scientific_vectors_still_pass(self):
        result = phase3_validator.validate_vectors()
        self.assertGreater(result["rows"], 0)


if __name__ == "__main__":
    unittest.main()
