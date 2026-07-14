from __future__ import annotations

import importlib.util
import json
import unittest
from decimal import Decimal
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = BASE_DIR / "scripts"
FIXTURE_DIR = BASE_DIR / "tests" / "fixtures"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


builder = load_module("build_terpenes_batch_worksheet", SCRIPTS_DIR / "build_terpenes_batch_worksheet.py")
validator = load_module("validate_terpenes_batch_worksheet", SCRIPTS_DIR / "validate_terpenes_batch_worksheet.py")
reference = load_module("reference_terpenes_batch_logic", SCRIPTS_DIR / "reference_terpenes_batch_logic.py")


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class TerpenesBatchWorksheetCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.candidate, cls.manifest, cls.candidate_text, cls.manifest_text = builder.build_outputs()
        cls.worksheets = {ws["worksheetName"]: ws for ws in cls.candidate["config"]["worksheets"]}
        cls.named_cells = cls.candidate["qb_config"]["named_cells"]
        cls.valid_rows = load_fixture("valid_unknown_import_rows.json")
        cls.qc_fixture = load_fixture("valid_qc_review_rows.json")
        cls.invalid_cases = load_fixture("invalid_batch_cases.json")

    def publish_row(self, row_name: str = "valid_unknown_row") -> dict:
        source = dict(self.valid_rows[row_name])
        source["df"] = source.pop("qbench_df")
        source["unit_confirmed"] = source["unit_confirmed"]
        source["preparation_values_confirmed"] = source["preparation_values_confirmed"]
        source["compound_results_complete"] = source["compound_results_complete"]
        return source

    def test_static_validator_passes(self) -> None:
        summary = validator.validate_candidate()
        self.assertEqual(summary["status"], "ok")
        self.assertEqual(summary["formula_count"], self.manifest["generated_candidate"]["formula_count"])
        self.assertEqual(summary["named_cell_count"], self.manifest["generated_candidate"]["named_cell_count"])

    def test_generator_is_deterministic_in_memory(self) -> None:
        first = builder.build_outputs()
        second = builder.build_outputs()
        self.assertEqual(first[2], second[2])
        self.assertEqual(first[3], second[3])

    def test_dist_files_match_generator_output(self) -> None:
        self.assertEqual(builder.CANDIDATE_PATH.read_text(encoding="utf-8"), self.candidate_text)
        self.assertEqual(builder.MANIFEST_PATH.read_text(encoding="utf-8"), self.manifest_text)

    def test_exact_tabs_and_ids(self) -> None:
        self.assertEqual(list(self.worksheets), ["Run Setup", "Instrument Import", "QC Review", "Publish"])
        source = json.loads(builder.SOURCE_ACTIVE_EXPORT.read_text(encoding="utf-8"))
        self.assertEqual(self.worksheets["Publish"]["worksheetId"], source["config"]["worksheets"][0]["worksheetId"])
        self.assertEqual(self.worksheets["Run Setup"]["worksheetId"], builder.RUN_SETUP_WORKSHEET_ID)
        self.assertEqual(self.worksheets["Instrument Import"]["worksheetId"], builder.INSTRUMENT_IMPORT_WORKSHEET_ID)
        self.assertEqual(self.worksheets["QC Review"]["worksheetId"], builder.QC_REVIEW_WORKSHEET_ID)

    def test_publish_capacity_and_placeholders_are_preserved(self) -> None:
        source = json.loads(builder.SOURCE_ACTIVE_EXPORT.read_text(encoding="utf-8"))
        placeholders = builder.source_publish_placeholders(source)
        publish = self.worksheets["Publish"]["data"]
        self.assertEqual(len(publish) - 1, len(placeholders))
        self.assertEqual(len(placeholders), 86)
        for index, placeholder in enumerate(placeholders, start=2):
            self.assertEqual(publish[index - 1][0], placeholder["test_id"])
            self.assertEqual(publish[index - 1][2], placeholder["product_matrix"])

    def test_import_and_publish_analytes_are_prompt2_order(self) -> None:
        analytes = json.loads(builder.PROMPT2_CONFIG_FILES[0].read_text(encoding="utf-8"))
        expected = [
            row["worksheet_label"]
            for row in sorted(analytes["internal_reportable_channels"], key=lambda item: item["order"])
        ]
        self.assertEqual(self.worksheets["Instrument Import"]["data"][0][33:56], expected)
        self.assertEqual(self.worksheets["Publish"]["data"][0][3:26], expected)
        self.assertEqual(len(expected), 23)

    def test_dimethylacetamide_is_audit_only(self) -> None:
        import_headers = self.worksheets["Instrument Import"]["data"][0]
        publish_headers = self.worksheets["Publish"]["data"][0]
        self.assertIn("dimethylacetamide_conc", import_headers)
        self.assertIn("Dimethylacetamide Conc.", publish_headers)
        self.assertNotIn("Dimethylacetamide", publish_headers[3:26])

    def test_named_cells_include_required_ranges(self) -> None:
        self.assertEqual(self.named_cells["terpenes_batch_import_table"]["cell"], "Instrument Import!A1:BE201")
        self.assertEqual(self.named_cells["terpenes_batch_import_analytes"]["cell"], "Instrument Import!AH2:BD201")
        self.assertEqual(self.named_cells["terpenes_batch_publish_table"]["cell"], "Publish!A1:BD87")
        self.assertEqual(self.named_cells["terpenes_batch_publish_instrument_conc"]["cell"], "Publish!D2:Z87")
        self.assertEqual(self.named_cells["batch_qc_disposition"]["cell"], "QC Review!B12")
        self.assertEqual(self.named_cells["batch_publish_ready"]["cell"], "QC Review!B15")
        self.assertEqual(self.named_cells["bracketing_ccv_criterion_status"]["cell"], "QC Review!B3")

    def test_default_release_gates_are_closed(self) -> None:
        run_setup = self.worksheets["Run Setup"]["data"]
        qc = self.worksheets["QC Review"]["data"]
        self.assertEqual(run_setup[3][1], "Terpenes")
        self.assertEqual(run_setup[16][1], "")
        self.assertIn("Analytical batch ID required", run_setup[24][1])
        self.assertEqual(qc[2][1], "decision_required")
        self.assertEqual(qc[3][1], "")
        self.assertIn('decision_required', qc[4][1])
        self.assertEqual(qc[11][1], "Hold")
        self.assertIn('$B$12="Accepted"', qc[14][1])

    def test_publish_row_prerequisites_do_not_depend_on_batch_publish_ready(self) -> None:
        publish = self.worksheets["Publish"]["data"]
        for row_number in range(2, 88):
            prereq_formula = publish[row_number - 1][53]
            ready_formula = publish[row_number - 1][54]
            self.assertNotIn("'QC Review'!$B$15=TRUE", prereq_formula)
            self.assertIn(f"BB{row_number}=TRUE", ready_formula)
            self.assertIn("'QC Review'!$B$15=TRUE", ready_formula)

    def test_batch_publish_ready_does_not_depend_on_row_publish_ready(self) -> None:
        batch_formula = self.worksheets["QC Review"]["data"][14][1]
        self.assertNotIn("Publish!BC", batch_formula)
        self.assertIn("Publish!BB", self.worksheets["QC Review"]["data"][8][1])

    def test_no_final_sample_calculation_or_blocked_formula_text(self) -> None:
        formula_text = "\n".join(validator.formulas(self.candidate))
        for forbidden in ["IFERROR", "VALUE(", "Conc. %", "Norm Conc.", "/1000", "/10", "<LOQ"]:
            self.assertNotIn(forbidden, formula_text)

    def test_no_outcome_artifacts_in_candidate_json(self) -> None:
        validator.validate_no_forbidden_artifacts(self.candidate)

    def test_kvstore_config_is_empty(self) -> None:
        self.assertEqual(self.candidate["qb_config"]["kvstore_config"], {})

    def test_import_row_validates_clean_unknown(self) -> None:
        row = dict(self.valid_rows["valid_unknown_row"])
        self.assertEqual(reference.import_row_message(row), "Import row valid")
        self.assertEqual(reference.import_validation_status(row), "Valid")

    def test_import_row_accepts_numeric_zero_and_negative_analyte(self) -> None:
        zero_row = dict(self.valid_rows["valid_all_zero_unknown_row"])
        self.assertEqual(reference.import_row_message(zero_row), "Import row valid")
        negative = dict(self.valid_rows["valid_unknown_row"])
        negative["analyte_values"] = [-1] + [1] * 22
        self.assertEqual(reference.import_row_message(negative), "Import row valid")

    def test_strict_numeric_recognition(self) -> None:
        self.assertTrue(reference.is_strict_number(0))
        self.assertTrue(reference.is_strict_number(Decimal("1.25")))
        self.assertFalse(reference.is_strict_number("10"))
        self.assertFalse(reference.is_strict_number(True))
        self.assertFalse(reference.is_strict_number(""))

    def test_valid_publish_row_prerequisites(self) -> None:
        row = self.publish_row()
        duplicates: set[str] = set()
        self.assertTrue(reference.row_prerequisites_complete(row, duplicates))
        self.assertEqual(reference.publish_row_message(row, duplicates), "Ready for transfer")
        self.assertEqual(reference.publish_ready(True, True), "TRUE")
        self.assertEqual(reference.publish_ready(True, False), "FALSE")

    def test_invalid_publish_cases(self) -> None:
        for case in self.invalid_cases["invalid_publish_cases"]:
            with self.subTest(case=case["name"]):
                if "import_updates" in case:
                    import_row = dict(self.valid_rows["valid_unknown_row"])
                    import_row.update(case["import_updates"])
                    self.assertEqual(reference.import_row_message(import_row), case["expected_import_message"])
                    continue
                row = self.publish_row()
                row.update(case.get("updates", {}))
                duplicate_ids = set(case.get("duplicate_ids", []))
                self.assertEqual(reference.publish_row_message(row, duplicate_ids), case["expected_message"])

    def test_all_zero_publish_row_is_valid(self) -> None:
        row = self.publish_row("valid_all_zero_unknown_row")
        self.assertTrue(reference.row_prerequisites_complete(row, set()))

    def test_duplicate_detection(self) -> None:
        duplicates = reference.duplicate_test_ids(["TR-1", "TR-2", "TR-1", "", "TR-3", "TR-2"])
        self.assertEqual(duplicates, {"TR-1", "TR-2"})

    def test_qc_boundary_cases(self) -> None:
        for case in self.qc_fixture["boundary_cases"]:
            with self.subTest(case=case["name"]):
                if case["kind"] == "minimum":
                    result = reference.evaluate_minimum(case["value"], Decimal(str(case["limit"])))
                elif case["kind"] == "maximum":
                    result = reference.evaluate_maximum(case["value"], Decimal(str(case["limit"])))
                elif case["kind"] == "range":
                    result = reference.evaluate_range(
                        case["value"],
                        Decimal(str(case["minimum"])),
                        Decimal(str(case["maximum"])),
                    )
                else:
                    result = reference.bracketing_ccv_evaluation(
                        case["value"],
                        case["criterion_status"],
                        case["window"],
                    )
                self.assertEqual(result, case["expected"])

    def test_qc_configuration_completeness(self) -> None:
        self.assertFalse(
            reference.qc_configuration_complete(
                bracketing_ccv_criterion_status="decision_required",
                bracketing_ccv_accuracy_percent_window="",
            )
        )
        self.assertTrue(
            reference.qc_configuration_complete(
                bracketing_ccv_criterion_status="confirmed",
                bracketing_ccv_accuracy_percent_window=15,
            )
        )
        self.assertFalse(
            reference.qc_configuration_complete(
                bracketing_ccv_criterion_status="confirmed",
                bracketing_ccv_accuracy_percent_window=15,
                lcs_criterion_status="decision_required",
            )
        )

    def test_overall_qc_evaluation_cases(self) -> None:
        for case in self.qc_fixture["overall_cases"]:
            with self.subTest(case=case["name"]):
                self.assertEqual(
                    reference.overall_analyte_qc_evaluation(case["evaluations"]),
                    case["expected"],
                )

    def test_batch_publish_ready_positive_case(self) -> None:
        self.assertTrue(
            reference.batch_publish_ready(
                qc_configuration_is_complete=True,
                integration_review_is_complete=True,
                qc_data_is_complete=True,
                qc_review_is_complete=True,
                all_publish_rows_are_valid=True,
                duplicate_test_id_count=0,
                batch_qc_disposition="Accepted",
                batch_qc_reviewer="Reviewer",
                batch_qc_reviewed_at="2026-07-14",
            )
        )

    def test_batch_gate_invalid_cases(self) -> None:
        base = {
            "qc_configuration_is_complete": True,
            "integration_review_is_complete": True,
            "qc_data_is_complete": True,
            "qc_review_is_complete": True,
            "all_publish_rows_are_valid": True,
            "duplicate_test_id_count": 0,
            "batch_qc_disposition": "Accepted",
            "batch_qc_reviewer": "Reviewer",
            "batch_qc_reviewed_at": "2026-07-14",
        }
        for case in self.invalid_cases["batch_gate_cases"]:
            with self.subTest(case=case["name"]):
                if "qc_configuration" in case:
                    self.assertEqual(
                        reference.qc_configuration_complete(**case["qc_configuration"]),
                        case["expected_configuration_complete"],
                    )
                    continue
                values = {**base, **case.get("updates", {})}
                self.assertEqual(reference.batch_publish_ready(**values), case["expected_ready"])
                self.assertEqual(reference.batch_publish_message(**values), case["expected_message"])

    def test_batch_publish_requires_accepted_disposition(self) -> None:
        for disposition in ["Hold", "Rejected"]:
            with self.subTest(disposition=disposition):
                self.assertFalse(
                    reference.batch_publish_ready(
                        qc_configuration_is_complete=True,
                        integration_review_is_complete=True,
                        qc_data_is_complete=True,
                        qc_review_is_complete=True,
                        all_publish_rows_are_valid=True,
                        duplicate_test_id_count=0,
                        batch_qc_disposition=disposition,
                        batch_qc_reviewer="Reviewer",
                        batch_qc_reviewed_at="2026-07-14",
                    )
                )

    def test_manifest_records_dependencies_and_scope(self) -> None:
        self.assertEqual(
            self.manifest["source_active_export"]["sha256"],
            builder.sha256_file(builder.SOURCE_ACTIVE_EXPORT),
        )
        self.assertFalse(self.manifest["scope_controls"]["test_worksheet_candidate_modified"])
        self.assertFalse(self.manifest["scope_controls"]["active_or_raw_qbench_export_modified"])
        self.assertFalse(self.manifest["scope_controls"]["prompt5_started"])

    def test_internal_metadata_is_synchronized(self) -> None:
        validator.validate_synchronized_data(self.candidate)
        validator.validate_internal_metadata(self.candidate)


if __name__ == "__main__":
    unittest.main()
