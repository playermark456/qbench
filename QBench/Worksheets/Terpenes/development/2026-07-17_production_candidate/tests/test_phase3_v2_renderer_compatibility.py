from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_DIR))

import build_phase3_candidates as phase3  # noqa: E402
import build_phase3_candidates_v2 as v2_builder  # noqa: E402
import validate_phase3_candidates as phase3_validator  # noqa: E402
import validate_phase3_candidates_v2 as v2_validator  # noqa: E402


class Phase3V2RendererCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_candidate, cls.batch_candidate = v2_builder.build_candidates()
        cls.historical_test = json.loads(phase3_validator.HISTORICAL_TEST_PATH.read_text(encoding="utf-8"))
        cls.historical_batch = json.loads(phase3_validator.HISTORICAL_BATCH_PATH.read_text(encoding="utf-8"))
        cls.test_tabs = {"Report": "Report", "Data": "Data", "Specifications": "Specifications"}
        cls.batch_tabs = {
            "Run Setup": "Run Setup",
            "Instrument Import": "Instrument Import",
            "QC Review": "Batch Review",
            "Publish": "Test Transfer",
        }

    def test_failed_v1_files_remain_byte_identical(self) -> None:
        expected = {
            phase3.TEST_OUTPUT: "275c8058cd597cfc688121bbdf50d1189897a088f455ff9e00e79a3fdf781a44",
            phase3.BATCH_OUTPUT: "7c96c9e8bb300f5886a4f66971c6c22c3ae72ee9225134f737d6601a0bbc55b2",
        }
        for path, digest in expected.items():
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)

    def test_historical_namespace_and_worksheet_ids_are_preserved(self) -> None:
        v2_validator.validate_identity(self.test_candidate, self.historical_test, self.test_tabs, "Test")
        v2_validator.validate_identity(self.batch_candidate, self.historical_batch, self.batch_tabs, "Batch")

    def test_root_config_and_worksheet_key_shapes_are_preserved(self) -> None:
        for candidate, historical, mapping in (
            (self.test_candidate, self.historical_test, self.test_tabs),
            (self.batch_candidate, self.historical_batch, self.batch_tabs),
        ):
            self.assertEqual(list(candidate), list(historical))
            self.assertEqual(list(candidate["config"]), list(historical["config"]))
            candidate_sheets = v2_validator.worksheet_map(candidate)
            historical_sheets = v2_validator.worksheet_map(historical)
            for historical_name, candidate_name in mapping.items():
                self.assertEqual(list(candidate_sheets[candidate_name]), list(historical_sheets[historical_name]))

    def test_cell_entry_shapes_and_readonly_types_are_preserved(self) -> None:
        for candidate, historical, mapping in (
            (self.test_candidate, self.historical_test, self.test_tabs),
            (self.batch_candidate, self.historical_batch, self.batch_tabs),
        ):
            candidate_sheets = v2_validator.worksheet_map(candidate)
            historical_sheets = v2_validator.worksheet_map(historical)
            for historical_name, candidate_name in mapping.items():
                candidate_shapes = {tuple(value) for value in candidate_sheets[candidate_name]["cells"].values()}
                historical_shapes = {tuple(value) for value in historical_sheets[historical_name]["cells"].values()}
                self.assertEqual(candidate_shapes, historical_shapes)
                self.assertTrue(all(isinstance(value["readonly"], bool) for value in candidate_sheets[candidate_name]["cells"].values()))

    def test_rows_columns_and_min_dimensions_use_historical_representation(self) -> None:
        for candidate in (self.test_candidate, self.batch_candidate):
            for worksheet in candidate["config"]["worksheets"]:
                rows = len(worksheet["data"])
                cols = max(map(len, worksheet["data"]))
                self.assertEqual(worksheet["minDimensions"], [cols, rows])
                self.assertEqual(len(worksheet["rows"]), rows)
                self.assertEqual(len(worksheet["columns"]), cols)
                self.assertTrue(all(set(value) == {"height"} for value in worksheet["rows"]))
                self.assertTrue(all(set(value) == {"type", "width"} for value in worksheet["columns"]))

    def test_top_level_data_is_an_exact_mirror(self) -> None:
        for candidate in (self.test_candidate, self.batch_candidate):
            self.assertEqual(
                list(candidate["data"]),
                [worksheet["worksheetName"] for worksheet in candidate["config"]["worksheets"]],
            )
            for worksheet in candidate["config"]["worksheets"]:
                self.assertEqual(candidate["data"][worksheet["worksheetName"]], worksheet["data"])

    def test_formulas_remain_plain_strings_and_formula_cells_are_readonly(self) -> None:
        for candidate in (self.test_candidate, self.batch_candidate):
            sheets = v2_validator.worksheet_map(candidate)
            for sheet_name, reference, formula in phase3_validator.formulas(candidate):
                self.assertIsInstance(formula, str)
                self.assertTrue(formula.startswith("="))
                self.assertIs(sheets[sheet_name]["cells"][reference]["readonly"], True)

    def test_style_indexes_use_historical_integer_serialization(self) -> None:
        for candidate in (self.test_candidate, self.batch_candidate):
            for worksheet in candidate["config"]["worksheets"]:
                self.assertTrue(all(isinstance(key, str) for key in worksheet["style"]))
                self.assertTrue(all(isinstance(value, int) for value in worksheet["style"].values()))

    def test_named_cells_use_historical_entry_serialization(self) -> None:
        for candidate in (self.test_candidate, self.batch_candidate):
            shapes = {tuple(value) for value in candidate["qb_config"]["named_cells"].values()}
            self.assertEqual(shapes, {("cell", "display_name", "export")})

    def test_test_scientific_and_destination_contract_passes(self) -> None:
        result = phase3_validator.validate_test_candidate(self.test_candidate)
        self.assertEqual(result["named_cells"], 44)
        self.assertEqual(result["writable_destinations"], 43)

    def test_batch_scientific_and_transfer_contract_passes(self) -> None:
        result = phase3_validator.validate_batch_candidate(self.batch_candidate)
        self.assertEqual(result["af_ag_formula_rows"], 200)

    def test_all_calculation_vectors_pass(self) -> None:
        result = phase3_validator.validate_vectors()
        self.assertEqual(result["rows"], 41)

    def test_full_renderer_contract_passes_for_both_candidates(self) -> None:
        v2_validator.validate_renderer_contract(self.test_candidate, self.historical_test, self.test_tabs, "Test")
        v2_validator.validate_renderer_contract(self.batch_candidate, self.historical_batch, self.batch_tabs, "Batch")


if __name__ == "__main__":
    unittest.main()
