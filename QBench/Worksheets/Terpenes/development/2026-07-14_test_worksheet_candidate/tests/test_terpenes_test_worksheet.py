from __future__ import annotations

import importlib.util
import json
import unittest
from decimal import Decimal
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = BASE_DIR / "scripts"
FIXTURE_PATH = BASE_DIR / "tests" / "fixtures" / "calculation_reference_cases.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


builder = load_module("build_terpenes_test_worksheet", SCRIPTS_DIR / "build_terpenes_test_worksheet.py")
validator = load_module("validate_terpenes_test_worksheet", SCRIPTS_DIR / "validate_terpenes_test_worksheet.py")
reference = load_module("reference_terpenes_calculations", SCRIPTS_DIR / "reference_terpenes_calculations.py")


class TerpenesTestWorksheetCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.candidate, cls.manifest, cls.candidate_text, cls.manifest_text = builder.build_outputs()
        cls.worksheets = {ws["worksheetName"]: ws for ws in cls.candidate["config"]["worksheets"]}
        cls.named_cells = cls.candidate["qb_config"]["named_cells"]
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.reference_cases = cls.fixture["cases"]

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

    def test_exact_tabs_and_no_metrc_tab(self) -> None:
        self.assertEqual([ws["worksheetName"] for ws in self.candidate["config"]["worksheets"]], ["Report", "Data", "Specifications"])
        self.assertNotIn("METRC", self.worksheets)

    def test_data_input_channel_order_is_config_order(self) -> None:
        analytes = json.loads(builder.PROMPT2_CONFIG_FILES[0].read_text(encoding="utf-8"))
        expected = [
            row["worksheet_label"]
            for row in sorted(analytes["internal_reportable_channels"], key=lambda item: item["order"])
        ]
        self.assertEqual(self.worksheets["Data"]["data"][0][3:26], expected)

    def test_named_cells_include_required_report_ranges(self) -> None:
        self.assertEqual(self.named_cells["report_header"]["cell"], "Report!A1:E1")
        self.assertEqual(self.named_cells["report_content"]["cell"], "Report!A2:E23")
        self.assertEqual(self.named_cells["report_results"]["cell"], "Report!A1:E23")

    def test_all_compatibility_named_cells_are_preserved(self) -> None:
        source_named = json.loads(builder.SOURCE_ACTIVE_EXPORT.read_text(encoding="utf-8"))["qb_config"]["named_cells"]
        self.assertEqual(len(source_named), 47)
        for name, value in source_named.items():
            self.assertEqual(self.named_cells[name], value)

    def test_default_decision_gates_block_report_release(self) -> None:
        data = self.worksheets["Data"]["data"]
        self.assertEqual(data[14][1], "capture_only_until_method_validated")
        self.assertEqual(data[16][1], "FALSE")
        self.assertEqual(data[17][1], "FALSE")
        self.assertEqual(data[18][1], "decision_required")
        self.assertEqual(data[19][1], "decision_required")
        self.assertEqual(data[20][1], "decision_required")
        self.assertEqual(data[21][1], "Hold")
        self.assertEqual(data[22][1], "FALSE")
        self.assertIn("COUNT($D$2:$Z$2)=23", data[23][1])
        self.assertIn("COUNT($D$4:$Z$4)=23", data[23][1])

    def test_controlled_below_loq_modes_are_exact(self) -> None:
        expected = ["decision_required", "display_less_than_loq", "display_numeric_result"]
        self.assertEqual(self.fixture["controlled_below_loq_reporting_modes"], expected)
        self.assertEqual(self.manifest["default_decision_gates"]["controlled_below_loq_reporting_modes"], expected)
        self.assertEqual(sorted(reference.CONTROLLED_BELOW_LOQ_REPORTING_MODES), sorted(expected))

    def test_report_result_formulas_are_gated_by_reporting_ready(self) -> None:
        report = self.worksheets["Report"]["data"]
        for row in report[1:]:
            for formula in row[1:]:
                self.assertTrue(formula.startswith('=IF(DATA!$B$26'))

    def test_no_forbidden_outcome_tokens_in_candidate_json(self) -> None:
        validator.validate_no_forbidden_artifacts(self.candidate)

    def test_formula_layers_exist_for_all_23_channels(self) -> None:
        data = self.worksheets["Data"]["data"]
        for col in range(4, 27):
            label = builder.col_letter(col)
            self.assertTrue(
                data[2][col - 1].startswith(
                    f'=IF({label}2="","",IF(ISNUMBER({label}2)<>TRUE,"",IF($B$25<>TRUE'
                )
            )
            self.assertIn(f"{label}3*$B$13/$B$12/1000", data[3][col - 1])
            self.assertEqual(
                data[4][col - 1],
                f'=IF({label}4="","",IF(ISNUMBER({label}4)<>TRUE,"",{label}4/10))',
            )
            self.assertIn("Review Required", data[5][col - 1])

    def test_all_23_instrument_input_formulas_have_isnumber_guards(self) -> None:
        data = self.worksheets["Data"]["data"]
        for col in range(4, 27):
            label = builder.col_letter(col)
            effective_formula = data[2][col - 1]
            mgg_formula = data[3][col - 1]
            percent_formula = data[4][col - 1]
            qualifier_formula = data[5][col - 1]
            guard = f"ISNUMBER({label}2)<>TRUE"
            self.assertIn(f'IF({guard},""', effective_formula)
            self.assertLess(effective_formula.index(guard), effective_formula.index(f"{label}2*"))
            self.assertIn(f'IF({guard},"Review Required"', qualifier_formula)
            self.assertIn(f"ISNUMBER({label}3)<>TRUE", mgg_formula)
            self.assertIn(f"ISNUMBER({label}4)<>TRUE", percent_formula)

    def test_formula_text_does_not_coerce_or_hide_text_inputs(self) -> None:
        formula_text = "\n".join(validator.formulas(self.candidate))
        self.assertNotIn("IFERROR", formula_text)
        self.assertNotIn("VALUE(", formula_text)

    def test_total_ocimene_sums_only_cis_and_trans_ocimene(self) -> None:
        spec = self.worksheets["Specifications"]["data"]
        self.assertEqual(spec[27][3], '=IF(COUNT(D11,D14)=2,SUM(D11,D14),"")')
        self.assertEqual(spec[27][4], '=IF(COUNT(E11,E14)=2,SUM(E11,E14),"")')

    def test_total_nerolidol_sums_only_cis_and_trans_nerolidol(self) -> None:
        spec = self.worksheets["Specifications"]["data"]
        self.assertEqual(spec[28][3], '=IF(COUNT(D23,D24)=2,SUM(D23,D24),"")')
        self.assertEqual(spec[28][4], '=IF(COUNT(E23,E24)=2,SUM(E23,E24),"")')

    def test_total_terpenes_sums_internal_channels_once(self) -> None:
        spec = self.worksheets["Specifications"]["data"]
        self.assertIn("SUM(D5:D27)", spec[29][3])
        self.assertIn("SUM(E5:E27)", spec[29][4])
        self.assertNotIn("D28", spec[29][3])
        self.assertNotIn("E29", spec[29][4])

    def test_kvstore_config_is_empty(self) -> None:
        self.assertEqual(self.candidate["qb_config"]["kvstore_config"], {})

    def test_formula_cells_readonly_and_instrument_inputs_writable(self) -> None:
        data_cells = self.worksheets["Data"]["cells"]
        for col in range(4, 27):
            self.assertIs(data_cells[f"{builder.col_letter(col)}2"]["readonly"], False)
            for row in [3, 4, 5, 6]:
                self.assertIs(data_cells[f"{builder.col_letter(col)}{row}"]["readonly"], True)

    def test_reference_calculation_fixture_cases(self) -> None:
        for case in self.reference_cases:
            with self.subTest(case=case["name"]):
                result = reference.calculate_result(
                    conc_ug_ml=case["conc_ug_ml"],
                    final_volume_ml=case["final_volume_ml"],
                    sample_mass_g=case["sample_mass_g"],
                    df_application_mode=case["df_application_mode"],
                    df=case["df"] or None,
                )
                self.assertEqual(result["effective_concentration_ug_ml"], Decimal(case["expected_effective_concentration_ug_ml"]))
                self.assertEqual(result["result_mg_g"], Decimal(case["expected_mg_g"]))
                self.assertEqual(result["result_percent"], Decimal(case["expected_percent"]))

    def test_zero_sample_mass_blocks_reference_calculation(self) -> None:
        with self.assertRaises(reference.CalculationBlocked):
            reference.calculate_result(
                conc_ug_ml="10",
                final_volume_ml="10",
                sample_mass_g="0",
                df_application_mode="already_applied_by_labsolutions",
            )

    def test_zero_final_volume_blocks_reference_calculation(self) -> None:
        with self.assertRaises(reference.CalculationBlocked):
            reference.calculate_result(
                conc_ug_ml="10",
                final_volume_ml="0",
                sample_mass_g="1",
                df_application_mode="already_applied_by_labsolutions",
            )

    def test_unconfirmed_unit_blocks_calculation_readiness(self) -> None:
        ready = reference.calculation_ready(
            labsolutions_conc_unit="ug/mL",
            labsolutions_conc_unit_confirmed=False,
            preparation_values_confirmed=True,
            sample_mass_g="1",
            final_volume_ml="10",
            df_application_mode="already_applied_by_labsolutions",
        )
        self.assertFalse(ready)

    def test_unresolved_dilution_mode_blocks_calculation_readiness(self) -> None:
        ready = reference.calculation_ready(
            labsolutions_conc_unit="ug/mL",
            labsolutions_conc_unit_confirmed=True,
            preparation_values_confirmed=True,
            sample_mass_g="1",
            final_volume_ml="10",
            df_application_mode="capture_only_until_method_validated",
        )
        self.assertFalse(ready)

    def test_nonnumeric_preparation_inputs_block_calculation_readiness(self) -> None:
        base = {
            "labsolutions_conc_unit": "ug/mL",
            "labsolutions_conc_unit_confirmed": True,
            "preparation_values_confirmed": True,
            "sample_mass_g": "1",
            "final_volume_ml": "10",
            "df_application_mode": "already_applied_by_labsolutions",
        }
        cases = [
            {"sample_mass_g": "abc"},
            {"sample_mass_g": "1 g"},
            {"final_volume_ml": "abc"},
            {"final_volume_ml": "10 mL"},
            {"sample_mass_g": "0"},
            {"sample_mass_g": "-1"},
            {"final_volume_ml": "0"},
            {"final_volume_ml": "-10"},
        ]
        for override in cases:
            with self.subTest(override=override):
                values = {**base, **override}
                self.assertFalse(reference.calculation_ready(**values))

    def test_applicable_df_must_be_numeric_positive_for_calculation(self) -> None:
        base = {
            "labsolutions_conc_unit": "ug/mL",
            "labsolutions_conc_unit_confirmed": True,
            "preparation_values_confirmed": True,
            "sample_mass_g": "1",
            "final_volume_ml": "10",
            "df_application_mode": "apply_in_qbench",
        }
        for df in ["abc", "", "0", "-2"]:
            with self.subTest(df=df):
                self.assertFalse(reference.calculation_ready(**base, df=df))

    def test_captured_df_not_required_when_already_applied(self) -> None:
        self.assertTrue(
            reference.calculation_ready(
                labsolutions_conc_unit="ug/mL",
                labsolutions_conc_unit_confirmed=True,
                preparation_values_confirmed=True,
                sample_mass_g="1",
                final_volume_ml="10",
                df_application_mode="already_applied_by_labsolutions",
                df="",
            )
        )

    def test_hold_disposition_blocks_reporting(self) -> None:
        self.assertFalse(
            reference.reporting_ready(
                calculation_is_ready=True,
                analytical_results_are_complete=True,
                batch_qc_disposition="Hold",
                publish_ready=True,
                below_loq_reporting_mode="display_numeric_result",
                loq_source_status="confirmed",
                mu_source_status="confirmed",
            )
        )

    def test_rejected_disposition_blocks_reporting(self) -> None:
        self.assertFalse(
            reference.reporting_ready(
                calculation_is_ready=True,
                analytical_results_are_complete=True,
                batch_qc_disposition="Rejected",
                publish_ready=True,
                below_loq_reporting_mode="display_numeric_result",
                loq_source_status="confirmed",
                mu_source_status="confirmed",
            )
        )

    def test_publish_ready_false_blocks_reporting(self) -> None:
        self.assertFalse(
            reference.reporting_ready(
                calculation_is_ready=True,
                analytical_results_are_complete=True,
                batch_qc_disposition="Accepted",
                publish_ready=False,
                below_loq_reporting_mode="display_numeric_result",
                loq_source_status="confirmed",
                mu_source_status="confirmed",
            )
        )

    def test_invalid_below_loq_modes_block_reporting(self) -> None:
        for mode in ["decision_required", *self.fixture["invalid_below_loq_reporting_modes"]]:
            with self.subTest(mode=mode):
                self.assertFalse(
                    reference.reporting_ready(
                        calculation_is_ready=True,
                        analytical_results_are_complete=True,
                        batch_qc_disposition="Accepted",
                        publish_ready=True,
                        below_loq_reporting_mode=mode,
                        loq_source_status="confirmed",
                        mu_source_status="confirmed",
                    )
                )

    def test_supported_below_loq_modes_can_release_when_other_gates_are_met(self) -> None:
        for mode in ["display_less_than_loq", "display_numeric_result"]:
            with self.subTest(mode=mode):
                self.assertTrue(
                    reference.reporting_ready(
                        calculation_is_ready=True,
                        analytical_results_are_complete=True,
                        batch_qc_disposition="Accepted",
                        publish_ready=True,
                        below_loq_reporting_mode=mode,
                        loq_source_status="confirmed",
                        mu_source_status="confirmed",
                    )
                )

    def test_incomplete_analytical_results_block_reporting(self) -> None:
        self.assertFalse(
            reference.reporting_ready(
                calculation_is_ready=True,
                analytical_results_are_complete=False,
                batch_qc_disposition="Accepted",
                publish_ready=True,
                below_loq_reporting_mode="display_numeric_result",
                loq_source_status="confirmed",
                mu_source_status="confirmed",
            )
        )

    def test_no_double_application_of_dilution(self) -> None:
        result = reference.calculate_result(
            conc_ug_ml="10",
            final_volume_ml="10",
            sample_mass_g="1",
            df_application_mode="already_applied_by_labsolutions",
            df="2",
        )
        self.assertEqual(result["result_mg_g"], Decimal("0.1"))

    def test_no_formula_uses_blocked_labsolutions_fields(self) -> None:
        formula_text = "\n".join(validator.formulas(self.candidate))
        self.assertNotIn("Conc. %", formula_text)
        self.assertNotIn("Norm Conc.", formula_text)

    def test_report_display_supports_both_below_loq_modes(self) -> None:
        self.assertEqual(
            reference.report_display_value(
                reporting_is_ready=True,
                qualifier="<LOQ",
                below_loq_reporting_mode="display_less_than_loq",
                numerical_result="0.004",
            ),
            "<LOQ",
        )
        self.assertEqual(
            reference.report_display_value(
                reporting_is_ready=True,
                qualifier="<LOQ",
                below_loq_reporting_mode="display_numeric_result",
                numerical_result="0.004",
            ),
            Decimal("0.004"),
        )

    def test_report_display_suppresses_nonreport_qualifiers(self) -> None:
        for qualifier in ["Hold", "Review Required", ""]:
            with self.subTest(qualifier=qualifier):
                self.assertEqual(
                    reference.report_display_value(
                        reporting_is_ready=True,
                        qualifier=qualifier,
                        below_loq_reporting_mode="display_numeric_result",
                        numerical_result="0.004",
                    ),
                    "",
                )

    def test_analytical_results_complete_requires_23_numeric_inputs_and_results(self) -> None:
        self.assertTrue(reference.analytical_results_complete([0] * 23, [Decimal("0")] * 23))
        self.assertFalse(reference.analytical_results_complete([1] * 22, [Decimal("1")] * 23))
        self.assertFalse(reference.analytical_results_complete([1] * 23, [Decimal("1")] * 22))
        self.assertFalse(reference.analytical_results_complete([1] * 22 + ["abc"], [Decimal("1")] * 23))
        self.assertFalse(reference.analytical_results_complete([1] * 23, [Decimal("1")] * 22 + ["text"]))
        self.assertFalse(reference.analytical_results_complete(["1"] * 23, [Decimal("1")] * 23))

    def test_nonnumeric_instrument_inputs_blank_calculations_and_require_review(self) -> None:
        for instrument_conc in ["abc", "10 ug/mL", "N/A"]:
            with self.subTest(instrument_conc=instrument_conc):
                effective = reference.effective_concentration_or_blank(
                    instrument_conc=instrument_conc,
                    calculation_is_ready=True,
                    df_application_mode="already_applied_by_labsolutions",
                )
                mgg = reference.result_mg_g_or_blank(
                    effective_concentration=effective,
                    final_volume_ml=Decimal("10"),
                    sample_mass_g=Decimal("1"),
                    calculation_is_ready=True,
                )
                percent = reference.result_percent_or_blank(mgg)
                qualifier = reference.qualifier_for_instrument_input(
                    instrument_conc=instrument_conc,
                    calculation_is_ready=True,
                    result_mg_g=mgg,
                )
                self.assertEqual(effective, "")
                self.assertEqual(mgg, "")
                self.assertEqual(percent, "")
                self.assertEqual(qualifier, "Review Required")
                self.assertFalse(
                    reference.analytical_results_complete(
                        [Decimal("1")] * 22 + [instrument_conc],
                        [Decimal("0.01")] * 23,
                    )
                )

    def test_blank_instrument_input_stays_blank(self) -> None:
        effective = reference.effective_concentration_or_blank(
            instrument_conc="",
            calculation_is_ready=True,
            df_application_mode="already_applied_by_labsolutions",
        )
        mgg = reference.result_mg_g_or_blank(
            effective_concentration=effective,
            final_volume_ml=Decimal("10"),
            sample_mass_g=Decimal("1"),
            calculation_is_ready=True,
        )
        self.assertEqual(effective, "")
        self.assertEqual(mgg, "")
        self.assertEqual(reference.result_percent_or_blank(mgg), "")
        self.assertEqual(reference.qualifier_for_instrument_input(instrument_conc="", calculation_is_ready=True), "")
        self.assertFalse(reference.analytical_results_complete([Decimal("1")] * 22 + [""], [Decimal("1")] * 23))

    def test_numeric_zero_positive_and_negative_inputs_remain_numeric(self) -> None:
        cases = [
            (0, Decimal("0"), Decimal("0"), Decimal("0")),
            (Decimal("10"), Decimal("10"), Decimal("0.1"), Decimal("0.01")),
            (Decimal("-1"), Decimal("-1"), Decimal("-0.01"), Decimal("-0.001")),
        ]
        for instrument_conc, expected_effective, expected_mgg, expected_percent in cases:
            with self.subTest(instrument_conc=instrument_conc):
                effective = reference.effective_concentration_or_blank(
                    instrument_conc=instrument_conc,
                    calculation_is_ready=True,
                    df_application_mode="already_applied_by_labsolutions",
                )
                mgg = reference.result_mg_g_or_blank(
                    effective_concentration=effective,
                    final_volume_ml=Decimal("10"),
                    sample_mass_g=Decimal("1"),
                    calculation_is_ready=True,
                )
                percent = reference.result_percent_or_blank(mgg)
                self.assertEqual(effective, expected_effective)
                self.assertEqual(mgg, expected_mgg)
                self.assertEqual(percent, expected_percent)
                self.assertEqual(
                    reference.qualifier_for_instrument_input(
                        instrument_conc=instrument_conc,
                        calculation_is_ready=True,
                        result_mg_g=mgg,
                    ),
                    "Reported",
                )
        self.assertTrue(reference.analytical_results_complete([0] * 23, [Decimal("0")] * 23))

    def test_numeric_looking_text_input_is_not_silently_accepted(self) -> None:
        effective = reference.effective_concentration_or_blank(
            instrument_conc="10",
            calculation_is_ready=True,
            df_application_mode="already_applied_by_labsolutions",
        )
        self.assertEqual(effective, "")
        self.assertEqual(
            reference.qualifier_for_instrument_input(instrument_conc="10", calculation_is_ready=True),
            "Review Required",
        )

    def test_numerical_and_display_layers_are_separate(self) -> None:
        report_formulas = [
            value
            for row in self.worksheets["Report"]["data"][1:]
            for value in row[1:]
        ]
        self.assertTrue(all('DATA!$B$19="display_less_than_loq"' in formula or "<LOQ" not in formula for formula in report_formulas))
        self.assertTrue(all("Hold" not in formula for formula in report_formulas))
        self.assertTrue(all("Review Required" not in formula for formula in report_formulas))
        self.assertTrue(any("<LOQ" in formula for formula in self.worksheets["Data"]["data"][5][3:26]))

    def test_manifest_records_source_hash(self) -> None:
        self.assertEqual(
            self.manifest["source_active_export"]["sha256"],
            builder.sha256_file(builder.SOURCE_ACTIVE_EXPORT),
        )

    def test_reference_rollups(self) -> None:
        values = {
            "cisocimene": "0.010",
            "transocimene": "0.015",
            "cisnerolidol": "0.020",
            "transnerolidol": "0.005",
        }
        self.assertEqual(reference.sum_components(values, ["cisocimene", "transocimene"]), Decimal("0.025"))
        self.assertEqual(reference.sum_components(values, ["cisnerolidol", "transnerolidol"]), Decimal("0.025"))

    def test_partial_ocimene_rollup_is_blank(self) -> None:
        values = {"cisocimene": "0.010"}
        self.assertIsNone(reference.complete_sum_components(values, ["cisocimene", "transocimene"]))

    def test_partial_nerolidol_rollup_is_blank(self) -> None:
        values = {"transnerolidol": "0.005"}
        self.assertIsNone(reference.complete_sum_components(values, ["cisnerolidol", "transnerolidol"]))

    def test_reference_total_terpenes_uses_internal_channels_once(self) -> None:
        internal_keys = [f"k{index}" for index in range(23)]
        values = {key: "1" for key in internal_keys}
        self.assertEqual(reference.total_terpenes(values, internal_keys), Decimal("23"))

    def test_partial_total_terpenes_is_blank(self) -> None:
        internal_keys = [f"k{index}" for index in range(23)]
        values = {key: "1" for key in internal_keys[:-1]}
        self.assertIsNone(reference.complete_total_terpenes(values, internal_keys))

    def test_complete_total_terpenes_sums_23_channels_once(self) -> None:
        internal_keys = [f"k{index}" for index in range(23)]
        values = {key: "1" for key in internal_keys}
        self.assertEqual(reference.complete_total_terpenes(values, internal_keys), Decimal("23"))


if __name__ == "__main__":
    unittest.main()
