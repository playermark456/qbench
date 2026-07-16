"""Python validation tests for the Prompt 4.6 controlled probe package."""

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PACKAGE_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import build_probe_worksheet_candidate as worksheet_builder  # noqa: E402
import build_qbench_probe_distribution as distribution_builder  # noqa: E402
import validate_qbench_probe_package as validator  # noqa: E402


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generated_hashes() -> dict[str, str]:
    paths = [
        *sorted((PACKAGE_DIR / "dist").glob("*")),
        *sorted((PACKAGE_DIR / "tests/fixtures").glob("*")),
    ]
    return {path.relative_to(PACKAGE_DIR).as_posix(): file_hash(path) for path in paths if path.is_file()}


class QBenchProbePackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        distribution_builder.main()

    def test_static_validator_passes(self) -> None:
        summary = validator.validate_package()
        self.assertEqual(summary["status"], "ok")
        self.assertTrue(summary["qbench_configuration_draft_modified"])
        self.assertTrue(summary["qbench_modified"])
        self.assertFalse(summary["qbench_runtime_data_modified"])
        self.assertEqual(summary["stage_1_status"], "incomplete_retry_pending")

    def test_worksheet_generator_is_byte_identical(self) -> None:
        output = PACKAGE_DIR / "dist/qbench_runtime_probe_batch_ws_candidate.json"
        self.assertEqual(output.read_text(encoding="utf-8"), worksheet_builder.render_candidate())

    def test_generators_are_byte_identical_across_two_runs(self) -> None:
        distribution_builder.main()
        first = generated_hashes()
        distribution_builder.main()
        second = generated_hashes()
        self.assertEqual(first, second)

    def test_worksheet_has_one_probe_tab(self) -> None:
        workbook = json.loads(worksheet_builder.render_candidate())
        worksheets = workbook["config"]["worksheets"]
        self.assertEqual([worksheet["worksheetName"] for worksheet in worksheets], ["Probe"])
        self.assertEqual(worksheets[0]["worksheetId"], worksheet_builder.PROBE_WORKSHEET_ID)

    def test_required_named_cells_are_exact_and_unique(self) -> None:
        workbook = worksheet_builder.build_candidate()
        named = workbook["qb_config"]["named_cells"]
        self.assertEqual(set(named), set(worksheet_builder.NAMED_TARGETS))
        self.assertEqual(len(named), 15)

    def test_formula_cells_are_read_only(self) -> None:
        worksheet = worksheet_builder.build_candidate()["config"]["worksheets"][0]
        for address in worksheet_builder.FORMULAS:
            self.assertTrue(worksheet["cells"][address]["readonly"], address)

    def test_controlled_input_cells_are_writable(self) -> None:
        worksheet = worksheet_builder.build_candidate()["config"]["worksheets"][0]
        for address in worksheet_builder.writable_cells():
            self.assertFalse(worksheet["cells"][address]["readonly"], address)

    def test_worksheet_has_no_report_or_key_value_configuration(self) -> None:
        workbook = worksheet_builder.build_candidate()
        self.assertEqual(workbook["qb_config"]["kvstore_config"], {})
        self.assertEqual(workbook["qb_config"]["report_export_range"], "")
        self.assertEqual(workbook["qb_config"]["portal_export_range"], "")

    def test_controlled_fixture_copy_hash_matches(self) -> None:
        fixture = PACKAGE_DIR / "tests/fixtures/Output_redacted_fixture.txt"
        self.assertEqual(file_hash(fixture), "ed796c690b972ca08f1976b1d8f7355d3e5140e73ffa912c441d6185a093283b")

    def test_stage_7_distribution_is_absent(self) -> None:
        self.assertFalse((PACKAGE_DIR / "dist/terpenes_qbench_file_parser_sandbox_probe_v1.js").exists())

    def test_manifest_marks_stage_1_incomplete_and_later_stages_not_run(self) -> None:
        manifest = json.loads((PACKAGE_DIR / "dist/qbench_probe_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["stage_statuses"]["stage_0_repository_preparation"], "passed")
        self.assertEqual(manifest["stage_statuses"]["stage_1_no_write_runtime"], "incomplete_retry_pending")
        self.assertTrue(all(
            status == "not_run"
            for stage, status in manifest["stage_statuses"].items()
            if stage not in {"stage_0_repository_preparation", "stage_1_no_write_runtime"}
        ))

    def test_manifest_records_only_the_authorized_qbench_draft_change(self) -> None:
        manifest = json.loads((PACKAGE_DIR / "dist/qbench_probe_manifest.json").read_text(encoding="utf-8"))
        self.assertTrue(manifest["scope_controls"]["qbench_configuration_draft_modified"])
        self.assertTrue(manifest["scope_controls"]["qbench_modified"])
        self.assertFalse(manifest["scope_controls"]["qbench_runtime_data_modified"])
        self.assertFalse(manifest["scope_controls"]["production_modified"])
        self.assertFalse(manifest["scope_controls"]["prompt_5_started"])

    def test_manifest_records_initial_stage_1_attempt_as_failed_safely(self) -> None:
        manifest = json.loads((PACKAGE_DIR / "dist/qbench_probe_manifest.json").read_text(encoding="utf-8"))
        attempt = manifest["stage_1_initial_attempt"]
        self.assertEqual(attempt["result"], "failed_safely_runtime_file_collection_compatibility")
        self.assertEqual(attempt["observed_controlled_error"], "UNEXPECTED_PARSE_ERROR")
        self.assertEqual(attempt["controlled_fixture_file_count"], 1)
        self.assertEqual(attempt["cause_status"], "file_collection_compatibility_hypothesis_not_proven")
        self.assertFalse(attempt["runtime_data_modified"])
        self.assertFalse(attempt["worksheet_service_invoked"])

    def test_stage_1_source_has_array_like_normalization_and_stable_codes(self) -> None:
        source = (PACKAGE_DIR / "src/qbench_runtime_no_write_probe.js").read_text(encoding="utf-8")
        for token in [
            "fileCollectionKind",
            "normalizeFileCollection",
            "files.item(0)",
            "CONTROLLED_FILE_COLLECTION_ERROR",
            "CONTROLLED_FILE_COUNT_ERROR",
            "CONTROLLED_FILE_OBJECT_ERROR",
            "CONTROLLED_FILE_NAME_ERROR",
            "CONTROLLED_FILE_READ_ERROR",
            "failed step =",
        ]:
            self.assertIn(token, source)
        self.assertNotIn("Array.from", source)

    def test_exact_file_parser_url_is_recorded_without_guessing_qbjs_url(self) -> None:
        contract = json.loads((PACKAGE_DIR / "config/qbench_probe_contract.json").read_text(encoding="utf-8"))
        self.assertEqual(contract["current_tenant_imports"]["file_parser_js"]["url"], distribution_builder.FILE_PARSER_IMPORT_URL)
        self.assertIsNone(contract["current_tenant_imports"]["qbjs_js"]["url"])

    def test_expected_payload_fixtures_are_valid_json(self) -> None:
        for path in sorted((PACKAGE_DIR / "tests/fixtures").glob("expected_*.json")):
            self.assertIsInstance(json.loads(path.read_text(encoding="utf-8")), dict)


if __name__ == "__main__":
    unittest.main()
