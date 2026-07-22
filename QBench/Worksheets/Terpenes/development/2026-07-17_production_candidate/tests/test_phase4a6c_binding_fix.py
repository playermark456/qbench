from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parents[1]
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

import build_phase3_candidates_v4 as v4_builder
import build_phase4a6c_binding_fix as binding_builder
import validate_phase4a6c_binding_fix as binding_validator


class Phase4A6CBindingFixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = v4_builder.load_profile()
        cls.original = binding_validator.load_json(binding_builder.ORIGINAL_PATH)
        cls.corrected = binding_builder.build_candidate(profile=cls.profile)

    def test_exact_two_path_binding_delta_passes(self):
        result = binding_validator.validate_exact_delta(
            self.original, self.corrected, self.profile
        )
        self.assertEqual(
            result["binding_fix_delta"], "passed_exact_store_binding_only"
        )
        self.assertEqual(len(result["changed_paths"]), 2)

    def test_formula_change_fails(self):
        broken = copy.deepcopy(self.corrected)
        specifications = next(
            sheet
            for sheet in broken["config"]["worksheets"]
            if sheet["worksheetName"] == "Specifications"
        )
        specifications["data"][3][5] += " "
        with self.assertRaisesRegex(AssertionError, "outside the exact U2 mirror"):
            binding_validator.validate_exact_delta(self.original, broken, self.profile)

    def test_third_nonformula_change_fails(self):
        broken = copy.deepcopy(self.corrected)
        broken["config"]["worksheets"][0]["tableHeight"] += 1
        with self.assertRaisesRegex(AssertionError, "outside the exact U2 mirror"):
            binding_validator.validate_exact_delta(self.original, broken, self.profile)

    def test_original_binding_cannot_be_reused(self):
        broken_profile = copy.deepcopy(self.profile)
        broken_profile["kv_store_binding"] = self.original["data"]["Specifications"][1][20]
        with self.assertRaisesRegex(AssertionError, "still equals the original TEST binding"):
            binding_validator.validate_exact_delta(
                self.original, self.corrected, broken_profile
            )


if __name__ == "__main__":
    unittest.main()
