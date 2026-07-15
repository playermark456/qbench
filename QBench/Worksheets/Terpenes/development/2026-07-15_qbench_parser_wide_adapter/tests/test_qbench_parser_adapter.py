from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DIST_DIR = BASE_DIR / "dist"
VALIDATOR_PATH = BASE_DIR / "scripts" / "validate_qbench_parser_adapter.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_qbench_parser_adapter", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class QBenchParserAdapterTests(unittest.TestCase):
    def test_validator_passes(self) -> None:
        self.assertEqual(load_validator().validate_package()["status"], "ok")

    def test_manifest_native_status_is_blocked(self) -> None:
        manifest = load_json(DIST_DIR / "parser_adapter_manifest.json")
        self.assertEqual(manifest["qbench_native_status"], "blocked_missing_qbench_runtime_contract")

    def test_wide_row_has_57_columns(self) -> None:
        row = load_json(DIST_DIR / "Output_redacted_wide_import_row.json")
        self.assertEqual(len(row["columns"]), 57)

    def test_af_ag_are_excluded(self) -> None:
        row = load_json(DIST_DIR / "Output_redacted_wide_import_row.json")
        self.assertEqual(row["write_plan"]["excludes_formula_owned_columns"], ["AF", "AG"])

    def test_expected_counts_are_recorded(self) -> None:
        parsed = load_json(BASE_DIR / "tests" / "fixtures" / "expected_parsed_core.json")
        self.assertEqual(parsed["counts"]["compound_result_row_count"], 24)
        self.assertEqual(parsed["counts"]["peak_table_row_count"], 34)
        self.assertEqual(parsed["counts"]["reportable_compound_row_count"], 23)

    def test_publish_patch_stops_at_ax(self) -> None:
        patch = load_json(BASE_DIR / "tests" / "fixtures" / "expected_publish_patch.json")
        self.assertEqual(patch["writes"][0]["columns"][-1], "AX")
        self.assertNotIn("AY", patch["writes"][0]["columns"])
        self.assertEqual(patch["target_publish_row"], 2)
        self.assertEqual(patch["range"], "Publish!D2:AX2")

    def test_no_native_candidate_file_when_blocked(self) -> None:
        self.assertFalse((DIST_DIR / "terpenes_qbench_file_parser_candidate_v1.js").exists())

    def test_prompt4_hashes_record_raw_and_canonical(self) -> None:
        manifest = load_json(DIST_DIR / "parser_adapter_manifest.json")
        candidate = manifest["prompt4_candidate_hashes"]["candidate"]
        self.assertEqual(candidate["raw_sha256"], "f779d0175a7aec09eb5f57a778fde91cccf07bb7078a9573132547ee158da151")
        self.assertEqual(candidate["canonical_lf_sha256"], "e5c80b1213396cab4932e267fd786c6986c933d4b404f11daa5c5aba0629758e")

    def test_source_row_identity_contract_is_context_independent(self) -> None:
        manifest = load_json(DIST_DIR / "parser_adapter_manifest.json")
        self.assertTrue(manifest["source_row_identity"]["source_derived_only"])
        self.assertIn("qbench_test_id", manifest["source_row_identity"]["qbench_context_excluded"])
        self.assertFalse(manifest["source_row_identity"]["assignment_hash_used_for_duplicate_detection"])

    def test_review_and_publish_contracts_are_recorded(self) -> None:
        manifest = load_json(DIST_DIR / "parser_adapter_manifest.json")
        contract = manifest["reviewed_publish_contract"]
        self.assertEqual(contract["labsolutions_conc_unit_required_exact"], "ug/mL")
        self.assertEqual(contract["review_evidence_key"], "source_row_hash")
        self.assertEqual(contract["publish_row_mapping_key"], "qbench_test_id")
        self.assertTrue(contract["multi_row_preview_atomic"])

    def test_sandbox_evidence_does_not_claim_untracked_records(self) -> None:
        manifest = load_json(DIST_DIR / "parser_adapter_manifest.json")
        for record in manifest["sandbox_evidence"].values():
            self.assertEqual(record["status"], "not_recorded_in_repository")
            self.assertIsNone(record["path"])
            self.assertIsNone(record["sha256"])


if __name__ == "__main__":
    unittest.main()
