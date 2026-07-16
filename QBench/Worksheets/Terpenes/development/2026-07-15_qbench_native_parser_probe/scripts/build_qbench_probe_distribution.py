"""Build deterministic Prompt 4.6 Stage 0 distributions and manifest."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from build_probe_worksheet_candidate import OUTPUT_PATH as WORKSHEET_PATH
from build_probe_worksheet_candidate import render_candidate


REPO_ROOT = Path(__file__).resolve().parents[6]
PACKAGE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = PACKAGE_DIR / "src"
DIST_DIR = PACKAGE_DIR / "dist"
FIXTURE_DIR = PACKAGE_DIR / "tests/fixtures"
SOURCE_FIXTURE = REPO_ROOT / "QBench/Worksheets/Terpenes/source/Output_redacted_fixture.txt"
ANALYTE_CONFIG = REPO_ROOT / "QBench/Worksheets/Terpenes/development/2026-07-14_config_parser_foundation/config/terpenes_analytes.json"
LIMITS_PATH = PACKAGE_DIR / "config/qbench_probe_limits.json"
MANIFEST_PATH = DIST_DIR / "qbench_probe_manifest.json"
FILE_PARSER_IMPORT_URL = "https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js"


SCRIPT_MAP = {
    "qbench_runtime_no_write_probe_v1.js": "qbench_runtime_no_write_probe.js",
    "qbench_batch_context_probe_v1.js": "qbench_batch_context_probe.js",
    "qbench_attachment_context_probe_v1.js": "qbench_attachment_context_probe.js",
    "qbench_scalar_patch_probe_v1.js": "qbench_scalar_patch_probe.js",
    "qbench_range_patch_probe_v1.js": "qbench_range_patch_probe.js",
    "qbench_two_block_patch_probe_v1.js": "qbench_two_block_patch_probe.js",
    "qbench_failure_patch_probe_v1.js": "qbench_failure_patch_probe.js",
}


STAGE_WRAPPERS = {
    "qbench_scalar_patch_probe_v1.js": ("3", "QBenchScalarPatchProbe.execute(service, context.batchId)"),
    "qbench_range_patch_probe_v1.js": ("4", "QBenchRangePatchProbe.execute(service, QBenchRangePatchProbe.buildRequest(context.batchId, \"one_dimensional\"))"),
    "qbench_two_block_patch_probe_v1.js": ("5", "QBenchTwoBlockPatchProbe.execute(service, QBenchTwoBlockPatchProbe.buildRequest(context.batchId))"),
    "qbench_failure_patch_probe_v1.js": ("6", "QBenchFailurePatchProbe.execute(service, QBenchFailurePatchProbe.buildMixedValidityRequest(context.batchId))"),
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def browser_config() -> dict[str, Any]:
    source = read_json(ANALYTE_CONFIG)

    def channel(value: dict[str, Any]) -> dict[str, Any]:
        keys = [
            "order",
            "internal_key",
            "worksheet_label",
            "labsolutions_compound_id",
            "labsolutions_compound_name",
            "reportable",
            "retain_for_audit",
            "aliases",
        ]
        return {key: value[key] for key in keys if key in value}

    return {
        "reporting_mode": "quantitative_only",
        "quantitation": {
            "source_table": "Compound Results(Ch1)",
            "source_field": "Conc.",
        },
        "audit_only_channels": [channel(value) for value in source["audit_only_channels"]],
        "internal_reportable_channels": [channel(value) for value in source["internal_reportable_channels"]],
    }


def import_header() -> str:
    return (
        '"use strict";\n\n'
        f'importScripts("{FILE_PARSER_IMPORT_URL}");\n\n'
    )


def stage_wrapper(stage: str, expression: str) -> str:
    return f'''\n\nrun(async () => {{
  try {{
    const context = globalThis.QBenchProbeRuntimeContext;
    if (!context || context.authorized_stage !== "{stage}") throw new Error("CONTROLLED_STAGE_AUTHORIZATION_REQUIRED");
    if (typeof QBBatchService !== "function") throw new Error("EXACT_QBJS_IMPORT_REQUIRED");
    const service = new QBBatchService();
    await {expression};
    QB.success();
  }} catch (_error) {{
    QB.error("CONTROLLED_STAGE_ERROR");
  }}
}});\n'''


def build_distributions() -> None:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    WORKSHEET_PATH.write_text(render_candidate(), encoding="utf-8", newline="\n")
    shutil.copyfile(SOURCE_FIXTURE, FIXTURE_DIR / "Output_redacted_fixture.txt")

    config = browser_config()
    limits = read_json(LIMITS_PATH)
    core = (SRC_DIR / "qbench_browser_parser_core.js").read_text(encoding="utf-8")

    for output_name, source_name in SCRIPT_MAP.items():
        source = (SRC_DIR / source_name).read_text(encoding="utf-8")
        if output_name == "qbench_runtime_no_write_probe_v1.js":
            content = (
                import_header()
                + core
                + "\nconst QBenchProbeConfig = Object.freeze("
                + json.dumps(config, ensure_ascii=False, sort_keys=True)
                + ");\nconst QBenchProbeLimits = Object.freeze("
                + json.dumps(limits, ensure_ascii=False, sort_keys=True)
                + ");\n\n"
                + source
            )
        else:
            content = import_header() + source
            if output_name in STAGE_WRAPPERS:
                stage, expression = STAGE_WRAPPERS[output_name]
                content += stage_wrapper(stage, expression)
        (DIST_DIR / output_name).write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")

    expected_values = {
        "expected_no_write_summary.json": {
            "compound_result_rows": 24,
            "dimethylacetamide_audit_rows": 1,
            "extension_accepted": ".txt",
            "file_count": 1,
            "peak_table_rows": 34,
            "reportable_channels": 23,
            "web_crypto_available": False,
        },
        "expected_scalar_patch.json": {
            "batchId": "SANITIZED_BATCH_CONTEXT",
            "data": {
                "probe_number": {"value": 1.25},
                "probe_text": {"value": "sandbox_probe"},
            },
        },
        "expected_range_patch.json": {
            "batchId": "SANITIZED_BATCH_CONTEXT",
            "data": {"probe_small_range": {"value": [1.25, 2.5, 3.75]}},
        },
        "expected_two_block_patch.json": {
            "batchId": "SANITIZED_BATCH_CONTEXT",
            "data": {
                "probe_block_a_ae": {"value": [index + 0.25 for index in range(31)]},
                "probe_block_ah_be": {"value": [index + 100.25 for index in range(24)]},
            },
        },
    }
    for name, value in expected_values.items():
        (FIXTURE_DIR / name).write_text(json_text(value), encoding="utf-8", newline="\n")


def build_manifest() -> dict[str, Any]:
    artifacts = []
    for path in sorted(PACKAGE_DIR.rglob("*")):
        if not path.is_file() or path == MANIFEST_PATH or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        artifacts.append({"path": repo_relative(path), "sha256": sha256_file(path)})
    return {
        "artifact_hashes": artifacts,
        "controlled_dependency_hashes": {
            "prompt_3_test_candidate": "90686b980882b221008f281be33984dc5232e2f3d2632300db3f4a27b529640a",
            "prompt_4_batch_candidate_canonical_lf": "e5c80b1213396cab4932e267fd786c6986c933d4b404f11daa5c5aba0629758e",
            "prompt_4_5_source_fixture": "ed796c690b972ca08f1976b1d8f7355d3e5140e73ffa912c441d6185a093283b",
        },
        "manifest_self_hash": {"included": False, "reason": "Self-hash omitted to avoid recursive content."},
        "package": "2026-07-15_qbench_native_parser_probe",
        "prompt": "Prompt 4.6",
        "qbench_native_status": "blocked",
        "qbench_sandbox_probe_status": "stage_2b_completed_attachment_job_success_console_not_persisted_batch_context_unresolved",
        "schema_version": 1,
        "stage_1_initial_attempt": {
            "cause_status": "array_like_collection_confirmed_specific_constructor_not_logged",
            "controlled_fixture_file_count": 1,
            "observed_controlled_error": "UNEXPECTED_PARSE_ERROR",
            "parser_active": False,
            "parser_version_status": "DRAFT",
            "result": "failed_safely_runtime_file_collection_compatibility",
            "runtime_data_modified": False,
            "transient_qbench_error_notification": True,
            "worksheet_service_invoked": False,
        },
        "stage_1_retry_result": {
            "assay_set": False,
            "compound_result_row_count": 24,
            "controlled_fixture_file_count": 1,
            "dimethylacetamide_audit_row_count": 1,
            "evidence_reference": "stage_1_corrected_preview_sanitized_console_2026-07-15",
            "file_collection_kind": "array_like",
            "file_extension": ".txt",
            "parser_active": False,
            "parser_version_status": "DRAFT",
            "peak_table_row_count": 34,
            "qb_success_reached": True,
            "reportable_channel_count": 23,
            "result": "passed",
            "runtime_data_modified": False,
            "trigger_set": False,
            "web_crypto_available": True,
            "worksheet_service_invoked": False,
        },
        "stage_2a_result": {
            "assay_set": False,
            "batch_context_status": "not_available_in_preview_runtime",
            "candidate_paths": {
                "QB.attachment": {"present": False, "value_type": "undefined"},
                "QB.batch": {"present": False, "value_type": "undefined"},
                "QB.context": {"present": False, "value_type": "undefined"},
                "QB.currentBatch": {"present": False, "value_type": "undefined"},
                "QB.fileParserContext": {"present": False, "value_type": "undefined"},
            },
            "controlled_fixture_file_count_indicator": 1,
            "documented_or_observed": "observed_absent",
            "evidence_reference": "stage_2a_existing_preview_sanitized_console_2026-07-15",
            "file_metadata_logged": False,
            "full_qb_object_serialized": False,
            "parser_active": False,
            "parser_version_status": "DRAFT",
            "preview_output_group_count_observed": 2,
            "preview_rerun_by_codex": False,
            "result": "completed",
            "runtime_data_modified": False,
            "safe_property_path": None,
            "security_or_session_value_dereferenced": False,
            "trigger_set": False,
            "value_type": None,
            "worksheet_service_invoked": False,
        },
        "stage_2b_result": {
            "assay_set": False,
            "attachment_added": True,
            "attachment_remains_as_evidence": True,
            "batch_context_status": "unresolved_console_output_not_persisted",
            "batch_name": "ZZZ_SANDBOX_ONLY_TERPENES_CONTEXT_PROBE_2026-07-16",
            "controlled_fixture_name": "Output_redacted_fixture.txt",
            "evidence_reference": "stage_2b_attachment_job_history_2026-07-15",
            "filename_match": "exact_equal",
            "full_qb_object_serialized": False,
            "job_history_recorded": True,
            "job_history_status": "SUCCESS",
            "job_trigger": "Attachment Added To Batch",
            "parser_active_after_stage": False,
            "parser_name": "ZZZ_SANDBOX_ONLY_Terpenes_Attachment_Context_Probe_2026-07-16",
            "parser_version_active_within_disabled_parser": True,
            "parser_version_status": "APPROVED",
            "preview_rerun_by_codex": False,
            "property_path_observed": None,
            "property_value_type_observed": None,
            "qbench_console_lines_persisted_in_history": False,
            "result": "completed_inconclusive_batch_context",
            "runtime_attachment_modified": True,
            "security_or_session_value_dereferenced": False,
            "trigger_set": True,
            "trigger_scope": "Batch attachment exact filename",
            "worksheet_or_results_data_modified": False,
            "worksheet_service_invoked": False,
        },
        "scope_controls": {
            "authorized_attachment_added": True,
            "production_modified": False,
            "qbench_configuration_modified": True,
            "qbench_configuration_draft_modified": True,
            "qbench_modified": True,
            "qbench_runtime_data_modified": True,
            "terpenes_result_outcome_artifact_introduced": False,
            "worksheet_or_results_runtime_data_modified": False,
            "prompt_5_started": False,
        },
        "stage_statuses": {
            "stage_0_repository_preparation": "passed",
            "stage_1_no_write_runtime": "passed",
            "stage_2_batch_context": "unresolved_after_stage_2b_console_not_persisted",
            "stage_2a_preview_batch_context": "not_available_in_preview_runtime",
            "stage_2b_attachment_trigger": "completed_job_success_console_not_persisted",
            "stage_3_scalar_patch": "not_run",
            "stage_4_range_patch": "not_run",
            "stage_5_two_block_patch": "not_run",
            "stage_6_failure_behavior": "not_run",
            "stage_7_terpenes_fixture_probe": "not_run",
        },
        "test_counts": {
            "prompt_2_python": 27,
            "prompt_3_python": 50,
            "prompt_4_canonical_lf_python": 39,
            "prompt_4_5_javascript": 143,
            "prompt_4_5_python": 13,
            "prompt_4_6_javascript": 48,
            "prompt_4_6_python": 17,
            "total": 337,
        },
    }


def main() -> None:
    build_distributions()
    MANIFEST_PATH.write_text(json_text(build_manifest()), encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": "ok",
                "manifest": repo_relative(MANIFEST_PATH),
                "artifact_count": len(build_manifest()["artifact_hashes"]),
                "fixture_sha256": sha256_file(FIXTURE_DIR / "Output_redacted_fixture.txt"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
