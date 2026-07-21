from __future__ import annotations

import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "phase4a_sandbox_runtime"
sys.path.insert(0, str(RUNTIME_DIR))

from validate_phase4a3_round_trip import RoundTripMismatch, compare_round_trip  # noqa: E402


def load_candidate() -> dict:
    path = ROOT / "production_candidates" / "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v2.json"
    return json.loads(path.read_text(encoding="utf-8-sig"))


def observed_qbench_normalization(candidate: dict) -> dict:
    exported = deepcopy(candidate)
    exported["config"]["namespace"] = "qbench-generated-namespace"
    embedded_by_name = {
        worksheet["worksheetName"]: worksheet["data"]
        for worksheet in exported["config"]["worksheets"]
    }
    for worksheet in exported["config"]["worksheets"]:
        worksheet["minDimensions"] = [1, 1]
        worksheet["tableWidth"] = 1954
        worksheet["tableHeight"] = 350
    for name, grid in exported["data"].items():
        embedded = embedded_by_name[name]
        for row_index, row in enumerate(grid):
            for column_index, value in enumerate(row):
                if isinstance(embedded[row_index][column_index], str) and embedded[row_index][column_index].startswith("="):
                    row[column_index] = "0" if "SUM(" in value or "+" in value else ""
    return exported


class Phase4A3RoundTripNormalizationTests(unittest.TestCase):
    def test_observed_qbench_normalization_passes(self) -> None:
        candidate = load_candidate()
        result = compare_round_trip(candidate, observed_qbench_normalization(candidate))
        self.assertEqual(result["classification"], "passed_with_expected_qbench_normalization")
        self.assertEqual(result["worksheet_count"], 3)
        self.assertEqual(result["embedded_formula_count"], 309)
        self.assertEqual(result["top_level_formula_cache_values"], 309)
        self.assertEqual(result["named_definition_count"], 44)

    def test_embedded_formula_change_still_fails(self) -> None:
        candidate = load_candidate()
        exported = observed_qbench_normalization(candidate)
        exported["config"]["worksheets"][0]["data"][1][1] = "=1"
        with self.assertRaisesRegex(RoundTripMismatch, "embedded worksheet data differs"):
            compare_round_trip(candidate, exported)

    def test_nonformula_top_level_change_still_fails(self) -> None:
        candidate = load_candidate()
        exported = observed_qbench_normalization(candidate)
        exported["data"]["Report"][0][0] = "Changed header"
        with self.assertRaisesRegex(RoundTripMismatch, "non-formula top-level value differs"):
            compare_round_trip(candidate, exported)


if __name__ == "__main__":
    unittest.main()
