#!/usr/bin/env python3
"""Validate Prompt 4.5 parser/adapter package artifacts."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DIST_DIR = BASE_DIR / "dist"


class ValidationError(ValueError):
    pass


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate_package() -> dict:
    manifest = load_json(DIST_DIR / "parser_adapter_manifest.json")
    row = load_json(DIST_DIR / "Output_redacted_wide_import_row.json")
    parsed = load_json(BASE_DIR / "tests" / "fixtures" / "expected_parsed_core.json")
    patch = load_json(BASE_DIR / "tests" / "fixtures" / "expected_publish_patch.json")

    require(manifest["qbench_native_status"] == "blocked_missing_qbench_runtime_contract", "QBench native status must be blocked.")
    require(parsed["counts"]["compound_result_row_count"] == 24, "Expected 24 Compound Results rows.")
    require(parsed["counts"]["peak_table_row_count"] == 34, "Expected 34 Peak Table rows.")
    require(parsed["counts"]["reportable_compound_row_count"] == 23, "Expected 23 reportable rows.")
    require(len(row["columns"]) == 57, "Wide row must contain exactly 57 A:BE columns.")
    require(row["write_plan"]["excludes_formula_owned_columns"] == ["AF", "AG"], "AF/AG must be excluded.")
    require(all(col["js_type"] == "number" for col in row["columns"] if col["column"] >= "AH" and col["column"] <= "BD"), "AH:BD values must be numbers.")
    require(patch["status"] == "ok", "Expected publish preview patch to be valid.")
    require(patch["range"] == "Publish!D2:AX2", "Publish preview range must be D:AX.")
    require(all(col not in patch["writes"][0]["columns"] for col in ["AY", "AZ", "BA", "BB", "BC", "BD"]), "Publish formula/control columns must not be written.")

    text_blobs = [
        path.read_text(encoding="utf-8")
        for path in [
            BASE_DIR / "src" / "labsolutions_ascii_core.js",
            BASE_DIR / "src" / "wide_import_adapter.js",
            BASE_DIR / "src" / "reviewed_publish_adapter.js",
        ]
    ]
    combined = "\n".join(text_blobs)
    require("Claim Met" not in combined and "Claim Not Met" not in combined, "No label-claim conclusion may be introduced.")
    require(not re.search(r"\beval\s*\(", combined), "eval must not be used.")
    require(not re.search(r"\bnew\s+Function\b|\bFunction\s*\(", combined), "Function constructor must not be used.")
    require("fetch(" not in combined and "XMLHttpRequest" not in combined, "Arbitrary network APIs must not be used.")
    require("localStorage" not in combined and "cookie" not in combined.lower(), "Credential/browser storage access must not be used.")
    template = (BASE_DIR / "src" / "qbench_file_parser_entry.template.js").read_text(encoding="utf-8")
    require("INTEGRATION_BLOCKER" in template, "QBench template must retain integration blockers.")
    require("C:\\Users" not in json.dumps(row), "Local machine paths must not appear in generated wide row.")
    generated_surface = "\n".join([
        json.dumps(row),
        json.dumps(patch),
        (DIST_DIR / "Output_redacted_wide_import_row.tsv").read_text(encoding="utf-8"),
    ])
    require("pass_fail" not in generated_surface.lower(), "Generated surfaces must not expose pass_fail.")
    require("Pass/Fail" not in generated_surface, "Generated surfaces must not expose Pass/Fail.")

    return {
        "status": "ok",
        "qbench_native_status": manifest["qbench_native_status"],
        "counts": parsed["counts"],
        "wide_column_count": len(row["columns"]),
        "write_plan_blocks": len(row["write_plan"]["blocks"]),
        "publish_patch_range": patch["range"],
    }


class ParserAdapterArtifactTests(unittest.TestCase):
    def test_package_artifacts_validate(self) -> None:
        self.assertEqual(validate_package()["status"], "ok")

    def test_expected_files_exist(self) -> None:
        for relative in [
            "README.md",
            "docs/qbench_parser_api_evidence.md",
            "docs/qbench_parser_runtime_contract.md",
            "docs/wide_import_row_mapping.md",
            "docs/reviewed_import_to_publish_mapping.md",
            "docs/qbench_parser_sandbox_installation.md",
            "docs/qbench_parser_sandbox_validation_checklist.md",
            "docs/parser_limitations_and_blockers.md",
            "dist/terpenes_labsolutions_parser_core_v1.js",
            "dist/terpenes_wide_import_adapter_v1.js",
            "dist/terpenes_reviewed_publish_adapter_v1.js",
            "dist/Output_redacted_wide_import_row.json",
            "dist/Output_redacted_wide_import_row.tsv",
            "dist/Output_redacted_block_A_AE.tsv",
            "dist/Output_redacted_block_AH_BE.tsv",
            "dist/parser_adapter_manifest.json",
        ]:
            self.assertTrue((BASE_DIR / relative).is_file(), relative)

    def test_final_qbench_candidate_not_created_when_blocked(self) -> None:
        self.assertFalse((DIST_DIR / "terpenes_qbench_file_parser_candidate_v1.js").exists())

    def test_tsv_blocks_exclude_formula_columns(self) -> None:
        block_a = (DIST_DIR / "Output_redacted_block_A_AE.tsv").read_text(encoding="utf-8")
        block_b = (DIST_DIR / "Output_redacted_block_AH_BE.tsv").read_text(encoding="utf-8")
        self.assertNotIn("Import Validation Status", block_a)
        self.assertNotIn("Import Message", block_a)
        self.assertNotIn("Import Validation Status", block_b)
        self.assertNotIn("Import Message", block_b)

    def test_manifest_records_prompt4_raw_and_canonical_hashes(self) -> None:
        manifest = load_json(DIST_DIR / "parser_adapter_manifest.json")
        candidate = manifest["prompt4_candidate_hashes"]["candidate"]
        self.assertEqual(candidate["raw_sha256"], "f779d0175a7aec09eb5f57a778fde91cccf07bb7078a9573132547ee158da151")
        self.assertEqual(candidate["canonical_lf_sha256"], "e5c80b1213396cab4932e267fd786c6986c933d4b404f11daa5c5aba0629758e")

    def test_publish_patch_has_no_late_formula_columns(self) -> None:
        patch = load_json(BASE_DIR / "tests" / "fixtures" / "expected_publish_patch.json")
        self.assertEqual(patch["writes"][0]["columns"][-1], "AX")
        self.assertNotIn("AY", patch["writes"][0]["columns"])

    def test_numerical_values_are_numbers(self) -> None:
        row = load_json(DIST_DIR / "Output_redacted_wide_import_row.json")
        number_columns = [col for col in row["columns"] if col["js_type"] == "number"]
        self.assertGreaterEqual(len(number_columns), 31)
        self.assertTrue(any(col["value"] == 0 for col in number_columns))

    def test_scope_controls(self) -> None:
        manifest = load_json(DIST_DIR / "parser_adapter_manifest.json")
        self.assertFalse(manifest["scope_controls"]["test_worksheet_written"])
        self.assertFalse(manifest["scope_controls"]["publish_written"])
        self.assertFalse(manifest["scope_controls"]["qc_review_written"])
        self.assertFalse(manifest["scope_controls"]["pass_fail_artifact_introduced"])
        self.assertFalse(manifest["scope_controls"]["prompt5_started"])


def main() -> None:
    try:
        print(json.dumps(validate_package(), indent=2))
    except ValidationError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2))
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
