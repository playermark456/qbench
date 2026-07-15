#!/usr/bin/env python3
"""Build deterministic Prompt 4.5 parser/adapter distribution files."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = BASE_DIR.parents[4]
DIST_DIR = BASE_DIR / "dist"
PROMPT2_DIR = REPO_ROOT / "QBench" / "Worksheets" / "Terpenes" / "development" / "2026-07-14_config_parser_foundation"
PROMPT3_DIR = REPO_ROOT / "QBench" / "Worksheets" / "Terpenes" / "development" / "2026-07-14_test_worksheet_candidate"
PROMPT4_DIR = REPO_ROOT / "QBench" / "Worksheets" / "Terpenes" / "development" / "2026-07-14_batch_worksheet_candidate"
SOURCE_FIXTURE = BASE_DIR / "tests" / "fixtures" / "Output_redacted_fixture.txt"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_lf_hash(path: Path) -> str:
    return sha256_bytes(path.read_bytes().replace(b"\r\n", b"\n"))


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def copy_distribution_sources() -> dict[str, str]:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    mapping = {
        BASE_DIR / "src" / "labsolutions_ascii_core.js": DIST_DIR / "terpenes_labsolutions_parser_core_v1.js",
        BASE_DIR / "src" / "wide_import_adapter.js": DIST_DIR / "terpenes_wide_import_adapter_v1.js",
        BASE_DIR / "src" / "reviewed_publish_adapter.js": DIST_DIR / "terpenes_reviewed_publish_adapter_v1.js",
    }
    hashes: dict[str, str] = {}
    for source, destination in mapping.items():
        shutil.copyfile(source, destination)
        hashes[rel(destination)] = sha256_file(destination)
    return hashes


def run_fixture_generation() -> dict:
    result = subprocess.run(
        [sys.executable, str(BASE_DIR / "scripts" / "generate_wide_import_fixture.py")],
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(result.stdout)


def dependency_hash(path: Path) -> dict[str, str]:
    return {
        "path": rel(path),
        "raw_sha256": sha256_file(path),
        "canonical_lf_sha256": canonical_lf_hash(path),
    }


def sandbox_record_not_recorded() -> dict[str, str | None]:
    return {
        "status": "not_recorded_in_repository",
        "path": None,
        "sha256": None,
    }


def build_manifest(distribution_hashes: dict[str, str], generation_summary: dict) -> dict:
    analytes = load_json(PROMPT2_DIR / "config" / "terpenes_analytes.json")
    limits = load_json(BASE_DIR / "config" / "parser_security_limits.json")
    generated_outputs = [
        DIST_DIR / "Output_redacted_wide_import_row.json",
        DIST_DIR / "Output_redacted_wide_import_row.tsv",
        DIST_DIR / "Output_redacted_block_A_AE.tsv",
        DIST_DIR / "Output_redacted_block_AH_BE.tsv",
    ]
    return {
        "schema_version": 1,
        "package": "2026-07-15_qbench_parser_wide_adapter",
        "prompt": "Prompt 4.5",
        "qbench_native_status": "blocked_missing_qbench_runtime_contract",
        "runtime_contract_evidence_status": "missing_exact_qbench_runtime_contract",
        "source_fixture": {
            "path": rel(SOURCE_FIXTURE),
            "sha256": sha256_file(SOURCE_FIXTURE),
        },
        "prompt2_config_hashes": [
            dependency_hash(PROMPT2_DIR / "config" / "terpenes_analytes.json"),
            dependency_hash(PROMPT2_DIR / "config" / "terpenes_qc.json"),
            dependency_hash(PROMPT2_DIR / "config" / "metrc_profiles.json"),
        ],
        "prompt3_candidate_hashes": {
            "candidate": dependency_hash(PROMPT3_DIR / "dist" / "terpenes__test_ws_id_42__candidate_v1__2026-07-14.json"),
            "manifest": dependency_hash(PROMPT3_DIR / "dist" / "candidate_manifest.json"),
        },
        "prompt4_candidate_hashes": {
            "candidate": dependency_hash(PROMPT4_DIR / "dist" / "terpenes__batch_ws_id_43__candidate_v1__2026-07-14.json"),
            "manifest": dependency_hash(PROMPT4_DIR / "dist" / "candidate_manifest.json"),
            "layout_config": dependency_hash(PROMPT4_DIR / "config" / "terpenes_batch_layout.json"),
            "import_contract_config": dependency_hash(PROMPT4_DIR / "config" / "terpenes_batch_import_contract.json"),
        },
        "distribution_hashes": distribution_hashes,
        "generated_output_hashes": {rel(path): sha256_file(path) for path in generated_outputs},
        "parser_core_output_hash": sha256_file(BASE_DIR / "tests" / "fixtures" / "expected_parsed_core.json"),
        "adapter_output_hash": sha256_file(DIST_DIR / "Output_redacted_wide_import_row.json"),
        "qbench_wrapper_output_hash": None,
        "expected_counts": {
            "compound_result_rows": generation_summary["compound_result_row_count"],
            "peak_table_rows": generation_summary["peak_table_row_count"],
            "reportable_compound_rows": generation_summary["reportable_compound_row_count"],
            "dimethylacetamide_rows": 1,
        },
        "analyte_order": [
            row["internal_key"]
            for row in sorted(analytes["internal_reportable_channels"], key=lambda item: item["order"])
        ],
        "instrument_import_ranges": {
            "full": "Instrument Import!A:BE",
            "writable_blocks": [
                "Instrument Import!A:AE",
                "Instrument Import!AH:BE",
            ],
            "formula_owned_excluded_columns": [
                "AF",
                "AG",
            ],
        },
        "publish_patch_range": "Publish!D:AX",
        "source_row_identity": {
            "source_derived_only": True,
            "qbench_context_excluded": [
                "qbench_test_id",
                "qbench_sample_id",
                "product_matrix",
                "source_batch_id",
                "reviewer_selection",
                "confirmation_flags",
            ],
            "assignment_hash_available": True,
            "assignment_hash_used_for_duplicate_detection": False,
        },
        "reviewed_publish_contract": {
            "labsolutions_conc_unit_required_exact": "ug/mL",
            "review_evidence_key": "source_row_hash",
            "required_review_evidence": {
                "explicitly_selected": True,
                "import_validation_status": "Valid",
                "import_message": "Import row valid",
            },
            "publish_row_mapping_key": "qbench_test_id",
            "sample_id_used_for_publish_row_mapping": False,
            "multi_row_preview_atomic": True,
        },
        "multi_file_orchestration": {
            "function": "buildWideImportRows(fileInputs, config, contexts, securityLimits)",
            "allowed_file_extensions": [
                ".txt",
            ],
            "duplicate_source_row_hash_rejected": True,
            "duplicate_source_file_hash_reported": True,
            "publish_selection_status_for_multiple_reviewed_injections": "decision_required",
            "automatic_averaging_or_selection": False,
        },
        "security_limits": limits,
        "test_counts": {
            "javascript_node_tests": 122,
            "python_unittest_tests": 11,
            "prompt2_unittest_tests": 27,
            "prompt3_unittest_tests": 50,
            "prompt4_unittest_tests": 39,
            "prompt4_canonical_lf_hash_gate": "passed"
        },
        "deterministic_generation": {
            "stable_inputs_only": True,
            "current_timestamps_omitted": True,
            "local_paths_omitted_from_generated_metadata": True,
            "source_file_hash": generation_summary["source_file_hash"],
            "source_row_hash": generation_summary["source_row_hash"],
        },
        "unresolved_scientific_decisions": [
            "Final LabSolutions Conc. unit confirmation remains required.",
            "Approved sample mass and final volume source remains a Sandbox/release decision.",
            "Dilution application mode remains controlled by explicit context.",
            "Below-LOQ, MU, COA, METRC, totals, and final sample result behavior remain out of Prompt 4.5 scope."
        ],
        "sandbox_evidence": {
            "test_worksheet_sandbox_validation": sandbox_record_not_recorded(),
            "batch_worksheet_sandbox_validation": sandbox_record_not_recorded(),
            "end_to_end_qbench_parser_validation": sandbox_record_not_recorded(),
        },
        "scope_controls": {
            "repository_only": True,
            "qbench_modified": False,
            "prompt2_modified": False,
            "prompt3_modified": False,
            "prompt4_modified": False,
            "test_worksheet_written": False,
            "publish_written": False,
            "qc_review_written": False,
            "pass_fail_artifact_introduced": False,
            "prompt5_started": False,
        },
    }


def main() -> None:
    generation_summary = run_fixture_generation()
    distribution_hashes = copy_distribution_sources()
    manifest = build_manifest(distribution_hashes, generation_summary)
    manifest_path = DIST_DIR / "parser_adapter_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": "ok",
        "manifest_path": rel(manifest_path),
        "qbench_native_status": manifest["qbench_native_status"],
        "source_file_hash": generation_summary["source_file_hash"],
        "source_row_hash": generation_summary["source_row_hash"],
        "counts": manifest["expected_counts"],
    }, indent=2))


if __name__ == "__main__":
    main()
