from __future__ import annotations

import copy
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = BASE_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


parser_mod = load_module("parse_labsolutions_ascii", SCRIPTS_DIR / "parse_labsolutions_ascii.py")
validator_mod = load_module("validate_terpenes_config", SCRIPTS_DIR / "validate_terpenes_config.py")


class TerpenesParserConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.analytes = parser_mod.load_json(BASE_DIR / "config" / "terpenes_analytes.json")
        self.qc = parser_mod.load_json(BASE_DIR / "config" / "terpenes_qc.json")
        self.metrc = parser_mod.load_json(BASE_DIR / "config" / "metrc_profiles.json")
        self.fixture = BASE_DIR / "fixtures" / "labsolutions_ascii" / "Output_redacted_fixture.txt"

    def test_fixture_counts_and_audit_retention(self) -> None:
        parsed = parser_mod.parse_file(self.fixture, self.analytes)

        self.assertEqual(len(parsed["sections_present"]), 8)
        self.assertEqual(len(parsed["Compound Results(Ch1)"]), 24)
        self.assertEqual(len(parsed["normalized_reportable_compound_results"]), 23)
        self.assertEqual(len(parsed["Peak Table(Ch1)"]), 34)

        non_reportable = parsed["audit_non_reportable_compounds"]
        self.assertEqual([row["source_name"] for row in non_reportable], ["Dimethylacetamide"])
        reportable_names = {row["source_name"] for row in parsed["normalized_reportable_compound_results"]}
        self.assertNotIn("Dimethylacetamide", reportable_names)

    def test_every_reportable_channel_maps_to_one_internal_key(self) -> None:
        parsed = parser_mod.parse_file(self.fixture, self.analytes)
        internal_keys = [row["internal_key"] for row in parsed["normalized_reportable_compound_results"]]
        configured_keys = [row["internal_key"] for row in self.analytes["internal_reportable_channels"]]

        self.assertEqual(len(internal_keys), 23)
        self.assertEqual(len(set(internal_keys)), 23)
        self.assertEqual(set(internal_keys), set(configured_keys))

    def test_parser_preserves_source_conc_and_both_result_unit_slots(self) -> None:
        parsed = parser_mod.parse_file(self.fixture, self.analytes)
        first = parsed["normalized_reportable_compound_results"][0]

        self.assertEqual(first["potency_source_field"], "Conc.")
        self.assertIn("labsolutions_conc", first)
        self.assertIn("result_mg_g", first)
        self.assertIn("result_percent", first)
        self.assertIn("normalized_conc_percent_not_potency", first)
        self.assertIn("norm_conc_not_potency", first)

    def test_blocked_potency_fields_fail_validation(self) -> None:
        bad = copy.deepcopy(self.analytes)
        bad["quantitation"]["source_field"] = "Conc. %"

        with self.assertRaises(parser_mod.TerpenesConfigError):
            parser_mod.validate_analyte_config(bad)

        bad = copy.deepcopy(self.analytes)
        bad["quantitation"]["source_field"] = "Norm Conc."
        with self.assertRaises(parser_mod.TerpenesConfigError):
            parser_mod.validate_analyte_config(bad)

    def test_duplicate_internal_keys_fail_validation(self) -> None:
        bad = copy.deepcopy(self.analytes)
        bad["internal_reportable_channels"][1]["internal_key"] = bad["internal_reportable_channels"][0]["internal_key"]

        with self.assertRaises(parser_mod.TerpenesConfigError):
            parser_mod.validate_analyte_config(bad)

    def test_conflicting_aliases_fail_validation(self) -> None:
        bad = copy.deepcopy(self.analytes)
        bad["internal_reportable_channels"][1]["aliases"].append("alpha-Pinene")

        with self.assertRaises(parser_mod.TerpenesConfigError):
            parser_mod.validate_analyte_config(bad)

    def test_missing_required_metrc_mapping_fails_validation(self) -> None:
        bad = copy.deepcopy(self.metrc)
        bad["metrc_mappings"] = [
            row for row in bad["metrc_mappings"] if row["internal_key"] != "apinene"
        ]

        with self.assertRaises(validator_mod.ConfigValidationError):
            validator_mod.validate_metrc_config(bad, self.analytes)

    def test_forbidden_result_outcome_tokens_fail_validation(self) -> None:
        bad = copy.deepcopy(self.metrc)
        bad["report_fields"] = ["Pass"]

        with self.assertRaises(validator_mod.ConfigValidationError):
            validator_mod.validate_no_forbidden_result_artifacts(self.analytes, self.qc, bad)

        bad = copy.deepcopy(self.metrc)
        bad["named_cells"] = ["pass_fail"]
        with self.assertRaises(validator_mod.ConfigValidationError):
            validator_mod.validate_no_forbidden_result_artifacts(self.analytes, self.qc, bad)

    def test_batch_qc_dispositions_and_publish_ready_logic(self) -> None:
        validator_mod.validate_qc_config(self.qc)
        self.assertEqual(self.qc["batch_qc_disposition_values"], ["Accepted", "Hold", "Rejected"])

        self.assertTrue(
            validator_mod.publish_ready_allowed(
                self.qc,
                batch_qc_disposition="Accepted",
                required_analytical_fields_complete=True,
                required_audit_fields_complete=True,
            )
        )
        for disposition in ["Hold", "Rejected"]:
            self.assertFalse(
                validator_mod.publish_ready_allowed(
                    self.qc,
                    batch_qc_disposition=disposition,
                    required_analytical_fields_complete=True,
                    required_audit_fields_complete=True,
                )
            )
        self.assertFalse(
            validator_mod.publish_ready_allowed(
                self.qc,
                batch_qc_disposition="Accepted",
                required_analytical_fields_complete=False,
                required_audit_fields_complete=True,
            )
        )

    def test_metrc_structural_outcome_column_policy_is_blank_and_not_in_include(self) -> None:
        validator_mod.validate_metrc_config(self.metrc, self.analytes)

        bad = copy.deepcopy(self.metrc)
        policy = bad["schema_outcome_column_policy"]["if_required_by_external_schema"]
        policy["include_formula_depends_on_column"] = True
        with self.assertRaises(validator_mod.ConfigValidationError):
            validator_mod.validate_metrc_config(bad, self.analytes)

        bad = copy.deepcopy(self.metrc)
        policy = bad["schema_outcome_column_policy"]["if_required_by_external_schema"]
        policy["output_value"] = "Reported"
        with self.assertRaises(validator_mod.ConfigValidationError):
            validator_mod.validate_metrc_config(bad, self.analytes)

    def test_no_silent_other_terpenes_mapping(self) -> None:
        validator_mod.validate_metrc_config(self.metrc, self.analytes)

        bad = copy.deepcopy(self.metrc)
        bad["metrc_mappings"][0]["metrc_target_analyte_label"] = "Other Terpenes"
        with self.assertRaises(validator_mod.ConfigValidationError):
            validator_mod.validate_metrc_config(bad, self.analytes)

    def test_full_bundle_validation_cli_logic(self) -> None:
        summary = validator_mod.validate_bundle(BASE_DIR)

        self.assertEqual(summary["status"], "ok")
        self.assertEqual(summary["reporting_mode"], "quantitative_only")
        self.assertEqual(summary["reportable_channel_count"], 23)
        self.assertEqual(summary["default_coa_measurand_count"], 21)
        self.assertEqual(summary["metrc_profile_count"], 9)

    def test_cli_parser_writes_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            parsed = parser_mod.parse_file(self.fixture, self.analytes)
            parser_mod.write_csv(
                output_dir / "labsolutions_normalized_reportable_results_fixture.csv",
                parsed["normalized_reportable_compound_results"],
            )

            self.assertTrue((output_dir / "labsolutions_normalized_reportable_results_fixture.csv").is_file())


if __name__ == "__main__":
    unittest.main()
