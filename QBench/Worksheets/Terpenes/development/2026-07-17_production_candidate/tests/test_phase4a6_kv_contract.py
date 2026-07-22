from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parents[1]
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

import build_phase3_candidates_v4 as v4_builder
import validate_phase3_candidates as phase3_validator
import validate_phase3_candidates_v2 as v2_validator
import validate_phase4a6_v4 as v4_validator


class Phase4A6KeyValueContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = {
            "kv_store_binding": "SBX_ONLY_SYNTHETIC_STORE_BINDING",
            "kv_store_binding_classification": "another_non_secret_visible_identifier",
            "scope_key": "Terpenes",
            "matrix_binding_mode": "dynamic_test_matrix_reference",
            "matrix_source": "${test.sample.product_matrix}",
            "matrix_source_cell": "Data!C2",
            "result_unit": "ug/g",
        }
        cls.candidate = v4_builder.build_candidate(cls.profile)

    def test_old_six_argument_v3_signature_fails(self):
        call = 'GET_KVSTORE_VALUE($U$2,$U$3,A2,$U$4,$U$5,"LOQ")'
        with self.assertRaisesRegex(AssertionError, "exactly five arguments"):
            v4_validator.validate_lookup_call(call)

    def test_swapped_analyte_matrix_order_fails(self):
        call = 'GET_KVSTORE_VALUE($U$2,$U$3,A2,$U$4,"LOQ")'
        with self.assertRaisesRegex(AssertionError, "store, scope, matrix, analyte, field"):
            v4_validator.validate_lookup_call(call)

    def test_added_result_unit_level_fails(self):
        call = 'GET_KVSTORE_VALUE($U$2,$U$3,$U$4,A2,$U$5,"LOQ")'
        with self.assertRaisesRegex(AssertionError, "exactly five arguments"):
            v4_validator.validate_lookup_call(call)

    def test_mu_percent_terminal_field_fails(self):
        call = 'GET_KVSTORE_VALUE($U$2,$U$3,$U$4,A2,"MU%")'
        with self.assertRaisesRegex(AssertionError, "terminal field must be LOQ or MU"):
            v4_validator.validate_lookup_call(call)

    def test_five_argument_loq_form_passes(self):
        self.assertEqual(
            v4_validator.validate_lookup_call(
                'GET_KVSTORE_VALUE($U$2,$U$3,$U$4,A2,"LOQ")'
            ),
            ("A2", "LOQ"),
        )

    def test_five_argument_mu_form_passes(self):
        self.assertEqual(
            v4_validator.validate_lookup_call(
                'GET_KVSTORE_VALUE($U$2,$U$3,$U$4,"Ocimene 1","MU")'
            ),
            ('"Ocimene 1"', "MU"),
        )

    def test_renderer_compatibility_remains_passed(self):
        historical = v4_validator.load_json(phase3_validator.HISTORICAL_TEST_PATH)
        result = v2_validator.validate_renderer_contract(
            self.candidate,
            historical,
            {"Report": "Report", "Data": "Data", "Specifications": "Specifications"},
            "Test v4 fixture",
        )
        self.assertEqual(result["formula_count"], 309)

    def test_all_scientific_vectors_remain_passed(self):
        result = phase3_validator.validate_vectors()
        self.assertGreater(result["rows"], 0)

    def test_dynamic_spreadsheet_deployment_guard_passes(self):
        contract = v4_validator.load_json(v4_validator.DEPLOYMENT_CONTRACT_PATH)
        result = v4_validator.validate_deployment_contract(contract)
        self.assertEqual(result["worksheet_json_contract"], "passed")
        self.assertEqual(result["qbench_shell_type"], "dynamic_spreadsheet")
        self.assertEqual(
            result["sandbox_runtime_contract"],
            "blocked_version_2_definition_preview_blank_loq_mu",
        )

    def test_regular_spreadsheet_is_rejected_as_deployment_shell(self):
        contract = copy.deepcopy(v4_validator.load_json(v4_validator.DEPLOYMENT_CONTRACT_PATH))
        contract["qbench_shell_type"] = "spreadsheet"
        with self.assertRaisesRegex(AssertionError, "requires dynamic_spreadsheet"):
            v4_validator.validate_deployment_contract(contract)


if __name__ == "__main__":
    unittest.main()
