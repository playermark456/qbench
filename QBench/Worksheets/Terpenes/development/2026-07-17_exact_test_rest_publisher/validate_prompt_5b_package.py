#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[4]

REQUIRED = {
    "README.md",
    "requirements.txt",
    ".env.example",
    "terpenes_publisher.py",
    "src/terpenes_publisher/__init__.py",
    "src/terpenes_publisher/core.py",
    "tests/test_publisher.py",
    "config/publisher_config.json",
    "config/field_mapping.csv",
    "config/field_mapping_scalar_candidate.csv",
    "docs/api_contract.md",
    "docs/security_model.md",
    "docs/publish_gate.md",
    "docs/field_mapping.md",
    "docs/destination_contract_results.md",
    "docs/atomicity_results.md",
    "docs/rollback_contract.md",
    "docs/idempotency_contract.md",
    "docs/sandbox_success_results.md",
    "docs/sandbox_failure_results.md",
    "docs/live_promotion_gap_analysis.md",
    "fixtures/README.md",
    "fixtures/sanitized_audit_example.json",
    "sandbox_destination_proof/expected_destination_contract.csv",
    "sandbox_destination_proof/failed_runtime_provenance.json",
    "sandbox_destination_proof/pre_import_baseline.md",
    "sandbox_destination_proof/sanitized_destination_contract_evidence.json",
    "sandbox_destination_proof/sanitized_object_inventory.json",
    "native_test_worksheet_probe/README.md",
    "native_test_worksheet_probe/native_probe_configuration.md",
    "native_test_worksheet_probe/native_probe_results.md",
    "native_test_worksheet_probe/sanitized_object_inventory.json",
    "native_test_worksheet_probe/raw_export_sha256.txt",
    "native_test_worksheet_probe/sandbox_cleanup_plan.md",
    "native_43_field_rebuild/README.md",
    "native_43_field_rebuild/stage1_results.md",
    "native_43_field_rebuild/stage2_definition_results.md",
    "native_43_field_rebuild/stage3_instantiation_results.md",
    "native_43_field_rebuild/expected_contract.csv",
    "native_43_field_rebuild/raw_definition_sha256.txt",
    "native_43_field_rebuild/sanitized_object_inventory.json",
    "native_43_field_rebuild/sandbox_cleanup_plan.md",
    "native_43_field_rebuild/scalar_candidate_mapping.md",
    "native_43_field_rebuild/scalar_stage1_results.md",
    "native_43_field_rebuild/scalar_stage2_definition_results.md",
    "native_43_field_rebuild/scalar_stage3_instantiation_results.md",
    "native_43_field_rebuild/scalar_raw_export_sha256.txt",
    "native_43_field_rebuild/scalar_sanitized_object_inventory.json",
    "native_43_field_rebuild/scalar_sandbox_cleanup_plan.md",
    "native_43_field_rebuild/named_cell_persistence_diagnostic/README.md",
    "native_43_field_rebuild/named_cell_persistence_diagnostic/probe_a_unique_control.md",
    "native_43_field_rebuild/named_cell_persistence_diagnostic/probe_b_analyte_name.md",
    "native_43_field_rebuild/named_cell_persistence_diagnostic/probe_c_duplicate_name.md",
    "native_43_field_rebuild/named_cell_persistence_diagnostic/sanitized_object_inventory.json",
    "native_43_field_rebuild/named_cell_persistence_diagnostic/sandbox_cleanup_plan.md",
    "json_import_rebuild/README.md",
    "json_import_rebuild/SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE.json",
    "json_import_rebuild/candidate_validation.md",
    "json_import_rebuild/candidate_sha256.txt",
    "json_import_rebuild/compare_structures.py",
    "json_import_rebuild/structural_comparison.json",
    "json_import_rebuild/structural_comparison.md",
    "json_import_rebuild/source/2026-07-17_SBX_ONLY_TERPENES_NATIVE_SCALAR_43_FIELD_BASE_working_native_export_spreadsheet.json",
    "json_import_rebuild/failed_candidate/SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE_failed_collapsed_grid.json",
    "json_import_rebuild/source/.gitattributes",
    "json_import_rebuild/failed_candidate/.gitattributes",
    "json_import_rebuild/compare_address_formats.py",
    "json_import_rebuild/address_format_comparison.json",
    "json_import_rebuild/address_format_comparison.md",
    "json_import_rebuild/prior_qualified_candidate/.gitattributes",
    "json_import_rebuild/prior_qualified_candidate/SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE_qualified_addresses.json",
    "json_import_rebuild/generate_candidate.py",
    "json_import_rebuild/import_results.md",
    "json_import_rebuild/round_trip_results.md",
    "json_import_rebuild/sanitized_object_inventory.json",
    "json_import_rebuild/sandbox_cleanup_plan.md",
    "json_import_rebuild/validate_candidate.py",
    "json_import_rebuild/round_trip/.gitattributes",
    "json_import_rebuild/round_trip/SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE_v1_DRAFT_saved_reopened_export_spreadsheet.json",
    "json_import_rebuild/round_trip/saved_draft_round_trip_evidence.json",
    "json_import_rebuild/round_trip/semantic_comparison.md",
    "json_import_rebuild/round_trip/validate_round_trip.py",
    "json_import_rebuild/runtime_instantiation/README.md",
    "json_import_rebuild/runtime_instantiation/approval_activation_results.md",
    "json_import_rebuild/runtime_instantiation/assay_assignment_results.md",
    "json_import_rebuild/runtime_instantiation/test_instantiation_results.md",
    "json_import_rebuild/runtime_instantiation/runtime_export_results.md",
    "json_import_rebuild/runtime_instantiation/representative_value_persistence.md",
    "json_import_rebuild/runtime_instantiation/runtime_export_sha256.txt",
    "json_import_rebuild/runtime_instantiation/runtime_export_sanitized.csv",
    "json_import_rebuild/runtime_instantiation/sanitized_object_inventory.json",
    "json_import_rebuild/runtime_instantiation/sandbox_cleanup_plan.md",
    "json_import_rebuild/runtime_instantiation/validate_runtime_instantiation.py",
    "read_only_api_confirmation/README.md",
    "read_only_api_confirmation/preflight_plan.md",
    "read_only_api_confirmation/oauth_endpoint_discovery.md",
    "read_only_api_confirmation/oauth_endpoint_sources.csv",
    "read_only_api_confirmation/oauth_404_root_cause.md",
    "read_only_api_confirmation/oauth_result_sanitized.md",
    "read_only_api_confirmation/object_identity_results.md",
    "read_only_api_confirmation/worksheet_get_results.md",
    "read_only_api_confirmation/worksheet_contract_results.md",
    "read_only_api_confirmation/field_key_comparison.csv",
    "read_only_api_confirmation/request_ledger_sanitized.json",
    "read_only_api_confirmation/raw_response_sha256.txt",
    "read_only_api_confirmation/sanitized_object_inventory.json",
    "read_only_api_confirmation/next_patch_phase_gate.md",
    "read_only_api_confirmation/run_summary_sanitized.json",
    "read_only_api_confirmation/run_read_only_confirmation.py",
    "read_only_api_confirmation/validate_read_only_api_confirmation.py",
    "prompt_5b_manifest.json",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    failures: list[str] = []
    for relative in sorted(REQUIRED):
        if not (ROOT / relative).is_file():
            failures.append(f"missing required file: {relative}")

    with (ROOT / "config/field_mapping.csv").open("r", encoding="utf-8", newline="") as handle:
        mapping = list(csv.DictReader(handle))
    if len(mapping) != 43:
        failures.append("mapping does not contain exactly 43 rows")
    if [int(row["sequence"]) for row in mapping] != list(range(1, 44)):
        failures.append("mapping sequence is not exactly 1..43")
    destinations = [row["destination_named_cell"] for row in mapping]
    cells = [row["destination_cell"] for row in mapping]
    if len(set(destinations)) != 43 or len(set(cells)) != 43:
        failures.append("mapping destinations are not unique")
    if any("pass_fail" in value.lower() or "pass-fail" in value.lower() for value in destinations):
        failures.append("mapping contains Pass/Fail")
    if any("dimethylacetamide" in value.lower() for value in destinations):
        failures.append("mapping incorrectly contains Dimethylacetamide")
    if any(row["status"] != "unverified_saved_sandbox_destination" for row in mapping):
        failures.append("mapping claims unearned Sandbox destination verification")
    with (ROOT / "native_43_field_rebuild/expected_contract.csv").open(
        "r", encoding="utf-8", newline=""
    ) as handle:
        rebuild_expected = list(csv.DictReader(handle))
    if rebuild_expected != mapping:
        failures.append("native rebuild expected contract is not an exact 43-row mapping copy")

    with (ROOT / "config/field_mapping_scalar_candidate.csv").open(
        "r", encoding="utf-8", newline=""
    ) as handle:
        scalar_candidate = list(csv.DictReader(handle))
    if len(scalar_candidate) != 43:
        failures.append("scalar candidate does not contain exactly 43 rows")
    candidate_names = [row["destination_named_cell"] for row in scalar_candidate]
    candidate_cells = [row["destination_cell"] for row in scalar_candidate]
    expected_analyte_names = [f"terpenes_instrument_conc_{index:02d}" for index in range(1, 24)]
    expected_analyte_cells = [f"Data!{chr(ord('D') + index)}2" for index in range(23)]
    if candidate_names[:23] != expected_analyte_names:
        failures.append("scalar candidate analyte names are not exactly numbered 01..23")
    if sum(name.startswith("terpenes_instrument_conc_") for name in candidate_names) != 23:
        failures.append("scalar candidate does not contain exactly 23 analytes")
    if candidate_cells[:23] != expected_analyte_cells:
        failures.append("scalar candidate analyte cells are not exactly Data!D2:Z2")
    if len(set(candidate_names)) != 43:
        failures.append("scalar candidate destination names are not unique")
    if len(set(candidate_cells)) != 43:
        failures.append("scalar candidate destination addresses are not unique")
    if any("[" in name or "]" in name for name in candidate_names):
        failures.append("scalar candidate contains a bracketed destination name")
    if any("pass_fail" in name.lower() or "pass-fail" in name.lower() for name in candidate_names):
        failures.append("scalar candidate contains Pass/Fail")
    if any("dimethylacetamide" in name.lower() for name in candidate_names):
        failures.append("scalar candidate incorrectly contains Dimethylacetamide")
    if any("peak_table" in name.lower() or "peak table" in name.lower() for name in candidate_names):
        failures.append("scalar candidate incorrectly contains Peak Table reportable data")
    for index, (current, candidate) in enumerate(zip(mapping, scalar_candidate, strict=True)):
        expected = dict(current)
        if index < 23:
            expected["destination_named_cell"] = expected_analyte_names[index]
        if candidate != expected:
            failures.append(f"scalar candidate changed a non-name mapping field at sequence {index + 1}")

    config = json.loads((ROOT / "config/publisher_config.json").read_text(encoding="utf-8"))
    if config.get("destination_contract_proven") is not False:
        failures.append("destination contract must remain unproven")
    if config.get("destination_contract_proof_file") or config.get("destination_contract_proof_sha256"):
        failures.append("unearned destination proof lock is configured")
    if config.get("token_endpoint_contract_proven") is not True:
        failures.append("authoritative OAuth token endpoint is not marked proven")
    if config.get("token_path") != "/qbench/api/v2/auth/token":
        failures.append("authoritative OAuth token path is not exact")
    if config.get("required_batch_display_name_prefix") != "SBX_ONLY_":
        failures.append("synthetic Batch display-name prefix is not enforced")
    if config.get("atomicity_classification") != "api_patch_unresolved":
        failures.append("atomicity must remain api_patch_unresolved")
    if config.get("expected_assay_ids") or config.get("expected_assay_names") or config.get("expected_workflows"):
        failures.append("unverified Sandbox workflow identifiers are configured")

    core = (ROOT / "src/terpenes_publisher/core.py").read_text(encoding="utf-8")
    for required_text in (
        'ALLOWED_BASE_URL = "https://ait-sandbox.qbench.net"',
        "/qbench/api/v1/batch/",
        "/qbench/api/v1/test/",
        'AUTHORITATIVE_TOKEN_PATH = "/qbench/api/v2/auth/token"',
        'JWT_BEARER_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:jwt-bearer"',
        '"Content-Type": f"multipart/form-data; boundary={boundary}"',
        "saved_destination_contract_not_proven_before_token_request",
        "api_patch_atomic",
        "PUBLISH REVIEWED TERPENES BATCH",
    ):
        if required_text not in core:
            failures.append(f"core contract text missing: {required_text}")
    if "https://ait.qbench.net" in core:
        failures.append("live QBench URL appears in executable code")

    env_lines = (ROOT / ".env.example").read_text(encoding="utf-8").splitlines()
    if env_lines != ["QBENCH_BASE_URL=", "QBENCH_CLIENT_ID=", "QBENCH_CLIENT_SECRET="]:
        failures.append("sample environment file must contain blank variable names only")
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    for pattern in (
        ".env",
        ".env.*",
        "*.secret",
        "*.secrets",
        "qbench_sandbox_token*",
        "*object_ids.local.json",
        "native_test_worksheet_probe/*saved_reopened_export_spreadsheet.json",
        "native_test_worksheet_probe/*instantiated_export_spreadsheet.*",
        "native_43_field_rebuild/*saved_reopened_export_spreadsheet.json",
        "native_43_field_rebuild/*instantiated_export_spreadsheet.*",
        "native_43_field_rebuild/*object_ids.local.json",
    ):
        if pattern not in gitignore:
            failures.append(f"root .gitignore missing secret pattern: {pattern}")

    evidence = json.loads(
        (ROOT / "sandbox_destination_proof/sanitized_destination_contract_evidence.json").read_text(
            encoding="utf-8"
        )
    )
    if evidence.get("saved_worksheet_definition_contract") != "passed_43_of_43":
        failures.append("saved Worksheet definition classification is incorrect")
    if evidence.get("direct_existing_test_instantiation", {}).get("classification") != "failed_blank_default_5x5":
        failures.append("direct existing-Test classification is incorrect")
    normal_classification = "normal_assay_test_instantiation_failed_blank_default"
    if evidence.get("normal_assay_test_instantiation", {}).get("classification") != normal_classification:
        failures.append("normal Assay Test-instantiation classification is incorrect")
    if evidence.get("classification") != normal_classification:
        failures.append("final destination-contract classification is incorrect")
    if evidence.get("destination_contract_proven") is not False:
        failures.append("sanitized evidence must keep destination_contract_proven false")
    if any(evidence.get("security", {}).get(key) is not False for key in (
        "credentials_displayed",
        "oauth_token_requested",
        "qbench_rest_api_requested",
        "patch_requested",
        "live_qbench_accessed",
        "pass_fail_artifact_introduced",
    )):
        failures.append("sanitized evidence security controls are not all false")

    inventory = json.loads(
        (ROOT / "sandbox_destination_proof/sanitized_object_inventory.json").read_text(
            encoding="utf-8"
        )
    )
    if inventory.get("sanitized") is not True or inventory.get("internal_sandbox_ids_omitted") is not True:
        failures.append("object inventory is not marked sanitized with internal IDs omitted")
    inventory_objects = inventory.get("objects", [])
    if len(inventory_objects) != 8:
        failures.append("object inventory does not contain the eight authorized proof objects")
    if any(key == "id" or key.endswith("_id") for item in inventory_objects for key in item):
        failures.append("tracked object inventory contains an internal Sandbox ID")
    if inventory.get("analytical_results_entered") is not False:
        failures.append("object inventory claims analytical results were entered")
    if inventory.get("pass_fail_artifact_introduced") is not False:
        failures.append("object inventory claims a Pass/Fail artifact")

    native_inventory = json.loads(
        (ROOT / "native_test_worksheet_probe/sanitized_object_inventory.json").read_text(
            encoding="utf-8"
        )
    )
    native_classification = "native_test_worksheet_instantiation_passed"
    if native_inventory.get("classification") != native_classification:
        failures.append("native probe inventory classification is incorrect")
    if native_inventory.get("sanitized") is not True or native_inventory.get(
        "internal_sandbox_ids_omitted"
    ) is not True:
        failures.append("native probe inventory is not sanitized")
    native_objects = native_inventory.get("objects", [])
    if len(native_objects) != 6:
        failures.append("native probe inventory does not contain six authorized objects")
    if any(key == "id" or key.endswith("_id") for item in native_objects for key in item):
        failures.append("tracked native probe inventory contains an internal Sandbox ID")
    for key in (
        "worksheet_association_persisted",
        "native_definition_instantiated",
        "exact_manual_probe_persisted",
        "blank_baseline_restored",
    ):
        if native_inventory.get(key) is not True:
            failures.append(f"native probe inventory does not prove {key}")
    for key in (
        "analytical_results_entered",
        "pass_fail_artifact_introduced",
        "credentials_displayed",
        "oauth_token_requested",
        "qbench_rest_api_requested",
        "patch_requested",
        "live_qbench_accessed",
    ):
        if native_inventory.get(key) is not False:
            failures.append(f"native probe safety control is not false: {key}")

    native_results = (ROOT / "native_test_worksheet_probe/native_probe_results.md").read_text(
        encoding="utf-8"
    )
    for required_text in (
        native_classification,
        "old_sandbox_test_worksheet_engine = operational_for_native_definitions",
        "imported_prompt3_test_worksheet = compatibility_failure",
        "sandbox_native_test_probe",
        "a43cb9779e03d401e5b43d69df6169a1236b51e45dd805bd9aee7353109f8b24",
        "a72835d464d17a858c5d9a3fc88b31eae69c512f517cb1083c85f0cd32d73e9e",
    ):
        if required_text not in native_results:
            failures.append(f"native probe results missing: {required_text}")

    raw_hashes = (ROOT / "native_test_worksheet_probe/raw_export_sha256.txt").read_text(
        encoding="utf-8"
    )
    for expected_hash in (
        "a43cb9779e03d401e5b43d69df6169a1236b51e45dd805bd9aee7353109f8b24",
        "a72835d464d17a858c5d9a3fc88b31eae69c512f517cb1083c85f0cd32d73e9e",
    ):
        if expected_hash not in raw_hashes:
            failures.append(f"native raw-export hash evidence missing: {expected_hash}")

    rebuild_classification = "native_minimal_destination_probe_failed"
    rebuild_inventory = json.loads(
        (ROOT / "native_43_field_rebuild/sanitized_object_inventory.json").read_text(
            encoding="utf-8"
        )
    )
    if rebuild_inventory.get("classification") != rebuild_classification:
        failures.append("native 43-field rebuild classification is incorrect")
    if rebuild_inventory.get("sanitized") is not True or rebuild_inventory.get(
        "internal_sandbox_ids_omitted"
    ) is not True:
        failures.append("native 43-field rebuild inventory is not sanitized")
    rebuild_objects = rebuild_inventory.get("objects", [])
    if len(rebuild_objects) != 2:
        failures.append("native 43-field rebuild inventory does not contain two objects")
    if any(key == "id" or key.endswith("_id") for item in rebuild_objects for key in item):
        failures.append("tracked native 43-field rebuild inventory contains an internal Sandbox ID")
    rebuild_phase1 = rebuild_inventory.get("phase_1", {})
    expected_phase1 = {
        "expected_destinations": 7,
        "persisted_destinations": 4,
        "missing_destinations": 3,
        "indexed_bracket_names_persisted": False,
        "scalar_names_persisted": True,
        "diagnostic_underscore_names_removed": True,
        "export_download_file_created": False,
    }
    for key, expected in expected_phase1.items():
        if rebuild_phase1.get(key) != expected:
            failures.append(f"native 43-field Phase 1 evidence is incorrect: {key}")
    if rebuild_inventory.get("phase_2_skipped") is not True or rebuild_inventory.get(
        "phase_3_skipped"
    ) is not True:
        failures.append("native 43-field rebuild did not preserve the Phase 1 stop gate")
    for key in (
        "assay_created",
        "sample_created",
        "test_created",
        "analytical_results_entered",
        "pass_fail_artifact_introduced",
        "credentials_displayed",
        "oauth_token_requested",
        "qbench_rest_api_requested",
        "patch_requested",
        "live_qbench_accessed",
    ):
        if rebuild_inventory.get(key) is not False:
            failures.append(f"native 43-field rebuild safety control is not false: {key}")
    rebuild_raw_hashes = (ROOT / "native_43_field_rebuild/raw_definition_sha256.txt").read_text(
        encoding="utf-8"
    )
    for required_text in (
        "version_2_raw_export=NOT_CREATED",
        "phase_1_export_download=NOT_PRODUCED_BY_QBENCH_EXPORT_SPREADSHEET_ACTION",
        "reason=native_minimal_destination_probe_failed_before_version_2",
    ):
        if required_text not in rebuild_raw_hashes:
            failures.append(f"native 43-field raw-export stop evidence missing: {required_text}")

    scalar_classification = "native_scalar_minimal_destination_probe_failed"
    scalar_inventory = json.loads(
        (ROOT / "native_43_field_rebuild/scalar_sanitized_object_inventory.json").read_text(
            encoding="utf-8"
        )
    )
    if scalar_inventory.get("classification") != scalar_classification:
        failures.append("native scalar rebuild classification is incorrect")
    if scalar_inventory.get("sanitized") is not True or scalar_inventory.get(
        "internal_sandbox_ids_omitted"
    ) is not True:
        failures.append("native scalar rebuild inventory is not sanitized")
    scalar_objects = scalar_inventory.get("objects", [])
    if len(scalar_objects) != 2:
        failures.append("native scalar rebuild inventory does not contain two objects")
    if any(key == "id" or key.endswith("_id") for item in scalar_objects for key in item):
        failures.append("tracked native scalar rebuild inventory contains an internal Sandbox ID")
    scalar_phase1 = scalar_inventory.get("phase_1a", {})
    for key, expected in {
        "expected_destinations": 7,
        "persisted_destinations": 0,
        "missing_destinations": 7,
        "renamed_destinations": 0,
        "duplicated_destinations": 0,
        "formula_owned_destinations": 0,
        "export_spreadsheet_run": False,
        "export_download_file_created": False,
    }.items():
        if scalar_phase1.get(key) != expected:
            failures.append(f"native scalar Phase 1A evidence is incorrect: {key}")
    for key in ("phase_1b_skipped", "phase_2_skipped", "phase_3_skipped"):
        if scalar_inventory.get(key) is not True:
            failures.append(f"native scalar rebuild did not preserve stop gate: {key}")
    for key in (
        "assay_created",
        "sample_created",
        "test_created",
        "analytical_results_entered",
        "pass_fail_artifact_introduced",
        "credentials_displayed",
        "oauth_token_requested",
        "qbench_rest_api_requested",
        "patch_requested",
        "live_qbench_accessed",
    ):
        if scalar_inventory.get(key) is not False:
            failures.append(f"native scalar rebuild safety control is not false: {key}")
    scalar_raw_hashes = (ROOT / "native_43_field_rebuild/scalar_raw_export_sha256.txt").read_text(
        encoding="utf-8"
    )
    for required_text in (
        "phase_1_export_spreadsheet=NOT_RUN",
        "phase_1_sha256=NOT_AVAILABLE",
        "version_2_raw_export=NOT_CREATED",
    ):
        if required_text not in scalar_raw_hashes:
            failures.append(f"native scalar raw-export stop evidence missing: {required_text}")

    diagnostic_classification = "codex_named_cell_save_control_failed"
    diagnostic_inventory = json.loads(
        (
            ROOT
            / "native_43_field_rebuild/named_cell_persistence_diagnostic/sanitized_object_inventory.json"
        ).read_text(encoding="utf-8")
    )
    if diagnostic_inventory.get("classification") != diagnostic_classification:
        failures.append("named-cell persistence diagnostic classification is incorrect")
    for key, expected in {
        "manual_named_cell_persistence_control": "passed",
        "qbench_native_named_cell_persistence": "operational",
        "codex_browser_named_cell_save_control": "failed",
        "browser_control_authoritative": False,
    }.items():
        if diagnostic_inventory.get(key) != expected:
            failures.append(f"named-cell persistence correction is incorrect: {key}")
    if diagnostic_inventory.get("sanitized") is not True or diagnostic_inventory.get(
        "internal_sandbox_ids_omitted"
    ) is not True:
        failures.append("named-cell persistence diagnostic inventory is not sanitized")
    diagnostic_objects = diagnostic_inventory.get("objects", [])
    if len(diagnostic_objects) != 2:
        failures.append("named-cell persistence diagnostic inventory does not contain two objects")
    if any(key == "id" or key.endswith("_id") for item in diagnostic_objects for key in item):
        failures.append("tracked named-cell diagnostic inventory contains an internal Sandbox ID")
    probe_a = diagnostic_inventory.get("probe_a", {})
    expected_probe_a = {
        "classification": "unique_named_cell_control_failed",
        "grid_rows": 6,
        "grid_columns": 5,
        "system_name": "terpenes_named_cell_unique_control_20260717",
        "cell": "B2",
        "display_name": "Unique persistence control",
        "exportable": True,
        "named_cell_add_control_used": True,
        "row_visibly_committed_before_save": True,
        "grid_persisted_after_reopen": True,
        "label_persisted_after_reopen": True,
        "named_cell_persisted_after_reopen": False,
        "visible_validation_message": None,
    }
    for key, expected in expected_probe_a.items():
        if probe_a.get(key) != expected:
            failures.append(f"named-cell Probe A evidence is incorrect: {key}")
    manual_control = diagnostic_inventory.get("manual_control", {})
    for key, expected in {
        "worksheet": "SBX_ONLY_TERPENES_2026_07_17_NATIVE_SCALAR_43_FIELD_BASE",
        "version": "1 - Native Scalar 43 Field Base v1 - DRAFT",
        "version_row_visibly_present": True,
        "system_name": "sdf",
        "cell": "A1",
        "display_name": "",
        "exportable": True,
        "save_draft_used": True,
        "persisted_after_refresh": True,
        "visible_to_codex_after_exact_reopen": True,
    }.items():
        if manual_control.get(key) != expected:
            failures.append(f"manual named-cell control evidence is incorrect: {key}")
    codex_control = diagnostic_inventory.get("codex_save_control", {})
    for key, expected in {
        "system_name": "terpenes_codex_save_control_20260717",
        "cell": "B2",
        "display_name": "Codex save control",
        "exportable": True,
        "row_visibly_complete_before_save": True,
        "save_draft_used": True,
        "save_as_new_version_used": False,
        "persisted_after_refresh_and_exact_reopen": False,
        "manual_control_remained_after_reopen": True,
        "deleted_after_success": False,
        "cleanup_not_applicable_because_control_absent": True,
    }.items():
        if codex_control.get(key) != expected:
            failures.append(f"Codex save-control evidence is incorrect: {key}")
    for key in ("probe_b_run", "probe_b_nozero_run", "probe_c_run"):
        if diagnostic_inventory.get(key) is not False:
            failures.append(f"named-cell diagnostic incorrectly claims probe ran: {key}")
    if diagnostic_inventory.get("further_worksheet_construction_allowed") is not False:
        failures.append("named-cell diagnostic incorrectly permits further worksheet construction")
    for key in (
        "assay_created",
        "sample_created",
        "test_created",
        "analytical_results_entered",
        "pass_fail_artifact_introduced",
        "credentials_read_or_displayed",
        "oauth_token_requested",
        "qbench_rest_api_requested",
        "patch_requested",
        "live_qbench_accessed",
    ):
        if diagnostic_inventory.get(key) is not False:
            failures.append(f"named-cell diagnostic safety control is not false: {key}")

    version_control_classification = "codex_named_cell_save_control_failed"
    version_control_inventory = json.loads(
        (
            ROOT
            / "native_43_field_rebuild/version_creation_diagnostic/sanitized_object_inventory.json"
        ).read_text(encoding="utf-8")
    )
    if version_control_inventory.get("classification") != version_control_classification:
        failures.append("version-creation control classification is incorrect")
    for key, expected in {
        "historical_classification": "version_created_named_cell_missing",
        "manual_named_cell_persistence_control": "passed",
        "qbench_native_named_cell_persistence": "operational",
        "codex_browser_named_cell_save_control": "failed",
        "browser_control_authoritative": False,
    }.items():
        if version_control_inventory.get(key) != expected:
            failures.append(f"version-creation correction is incorrect: {key}")
    if version_control_inventory.get("sanitized") is not True or version_control_inventory.get(
        "internal_sandbox_ids_omitted"
    ) is not True:
        failures.append("version-creation control inventory is not sanitized")
    if len(version_control_inventory.get("objects", [])) != 2:
        failures.append("version-creation control inventory does not contain two objects")
    if any(
        key == "id" or key.endswith("_id")
        for item in version_control_inventory.get("objects", [])
        for key in item
    ):
        failures.append("version-creation control inventory contains an internal Sandbox ID")
    for key, expected in {
        "version_row_visibly_present": True,
        "grid_rows_after_reopen": 6,
        "grid_columns_after_reopen": 5,
        "a1_after_reopen": "Version creation control",
        "b2_after_reopen": "",
        "named_cell_rows_before_create": 1,
        "named_cell_rows_after_reopen": 0,
        "destination_contract_proven": False,
    }.items():
        if version_control_inventory.get(key) != expected:
            failures.append(f"version-creation control evidence is incorrect: {key}")
    for key in (
        "assay_created",
        "sample_created",
        "test_created",
        "analytical_results_entered",
        "pass_fail_artifact_introduced",
        "credentials_displayed",
        "oauth_token_requested",
        "qbench_rest_api_requested",
        "patch_requested",
        "live_qbench_accessed",
    ):
        if version_control_inventory.get(key) is not False:
            failures.append(f"version-creation control safety control is not false: {key}")

    json_import_classification = (
        "runtime_instantiation_passed_pending_read_only_api_confirmation"
    )
    approval_procedure_correction = (
        "approval_attempt_procedural_error_unnecessary_lock_handling"
    )
    json_candidate_path = (
        ROOT
        / "json_import_rebuild/SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE.json"
    )
    expected_json_candidate_hash = (
        "e5ef20a5cec574dc292ed679867e01313233c92ceda9ef863bf98dd8d4485b80"
    )
    if digest(json_candidate_path) != expected_json_candidate_hash:
        failures.append("generated JSON candidate hash is incorrect")
    candidate_validation = subprocess.run(
        [sys.executable, str(ROOT / "json_import_rebuild/validate_candidate.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if candidate_validation.returncode != 0:
        failures.append(
            "generated JSON candidate validator failed: "
            + candidate_validation.stdout.replace("\n", " ").strip()
        )
    round_trip_path = ROOT / (
        "json_import_rebuild/round_trip/"
        "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE_v1_DRAFT_"
        "saved_reopened_export_spreadsheet.json"
    )
    expected_round_trip_hash = (
        "3589f2ace8afb96db96d4da638e9effc86bda404e03f97b85fca0e43aa349912"
    )
    if digest(round_trip_path) != expected_round_trip_hash:
        failures.append("saved/reopened round-trip export hash is incorrect")
    round_trip_validation = subprocess.run(
        [
            sys.executable,
            str(ROOT / "json_import_rebuild/round_trip/validate_round_trip.py"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if round_trip_validation.returncode != 0:
        failures.append(
            "saved/reopened round-trip validator failed: "
            + round_trip_validation.stdout.replace("\n", " ").strip()
        )
    round_trip_evidence = json.loads(
        (
            ROOT
            / "json_import_rebuild/round_trip/saved_draft_round_trip_evidence.json"
        ).read_text(encoding="utf-8")
    )
    for key, expected in {
        "sanitized": True,
        "internal_sandbox_ids_omitted": True,
        "worksheet": "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE",
        "version": "JSON Scalar 43 Field Base v1",
        "version_state": "DRAFT",
        "version_row_visibly_present": True,
        "grid_before_refresh": "40x26",
        "grid_after_refresh_and_list_reopen": "40x26",
        "named_cells_before_refresh": 43,
        "named_cells_after_refresh_and_list_reopen": 43,
        "unqualified_named_cells_after_refresh_and_list_reopen": 43,
        "qualified_named_cells_after_refresh_and_list_reopen": 0,
        "blank_destinations_after_refresh_and_list_reopen": 43,
        "writable_destinations_after_refresh_and_list_reopen": 43,
        "formula_owned_destinations": 0,
        "exportable_destinations": 43,
        "a2_mapping_present": False,
        "round_trip_export_sha256": expected_round_trip_hash,
        "json_import_saved_definition_contract": "passed_43_of_43",
        "json_import_round_trip": "passed",
        "destination_contract_proven": json_import_classification,
        "runtime_test_worksheet_contract": "passed_43_of_43",
        "runtime_representative_value_persistence": "passed",
        "final_blank_destinations": 43,
        "atomicity_classification": "api_patch_unresolved",
        "analyte_patch_key_contract": "unresolved",
    }.items():
        if round_trip_evidence.get(key) != expected:
            failures.append(f"round-trip evidence is incorrect: {key}")
    for key in (
        "candidate_promoted",
        "analytical_results_entered",
        "credentials_read_or_displayed",
        "oauth_token_requested",
        "qbench_rest_api_requested",
        "patch_requested",
        "live_qbench_accessed",
        "pass_fail_artifact_introduced",
    ):
        if round_trip_evidence.get(key) is not False:
            failures.append(f"round-trip safety control is not false: {key}")
    for key in ("approved", "activated", "assay_created", "sample_created", "test_created"):
        if round_trip_evidence.get(key) is not True:
            failures.append(f"round-trip current lifecycle evidence is not true: {key}")
    json_inventory = json.loads(
        (ROOT / "json_import_rebuild/sanitized_object_inventory.json").read_text(
            encoding="utf-8"
        )
    )
    for key, expected in {
        "sanitized": True,
        "internal_sandbox_ids_omitted": True,
        "classification": json_import_classification,
        "candidate_sha256": expected_json_candidate_hash,
        "qualified_address_save_error": "Invalid cell definition Data!D2 for field name terpenes_instrument_conc_01",
        "logical_address_example": "Data!D2",
        "old_sandbox_json_cell_example": "D2",
        "json_unqualified_named_cells": 43,
        "json_qualified_named_cells": 0,
        "a2_mapping_present": False,
        "first_analyte_json_cell": "D2",
        "grid_rows": 40,
        "grid_columns": 26,
        "required_anchor_count": 28,
        "named_cells": 43,
        "destination_validation": "passed_43_of_43",
        "corrected_version": "JSON Scalar 43 Field Base v1",
        "corrected_version_state": "APPROVED and ACTIVE",
        "round_trip_sha256": expected_round_trip_hash,
        "json_import_saved_definition_contract": "passed_43_of_43",
        "json_import_round_trip": "passed",
        "approval_activation_classification": "passed_43_of_43",
        "approval_procedure_correction": approval_procedure_correction,
        "direct_approval_without_lock_required": True,
        "approved": True,
        "activated": True,
        "version_2_created": False,
        "assay_created": True,
        "assay_association_persisted": True,
        "sample_created": True,
        "test_created": True,
        "runtime_grid_before_reopen": "40x26",
        "runtime_grid_after_reopen": "40x26",
        "runtime_export_sha256": "f7c702dd3ecac694c32b3aa686cca6cd4928198b7bda45f4d8e030e65d681bfe",
        "runtime_test_worksheet_contract": "passed_43_of_43",
        "runtime_representative_value_persistence": "passed",
        "representative_values_cleared": True,
        "final_blank_destinations": 43,
        "destination_contract_proven": json_import_classification,
        "atomicity_classification": "api_patch_unresolved",
        "analyte_patch_key_contract": "unresolved",
        "pass_fail_artifact_introduced": False,
        "credentials_read_or_displayed": False,
        "oauth_token_requested": False,
        "qbench_rest_api_requested": False,
        "patch_requested": False,
        "live_qbench_accessed": False,
        "publish_or_qc_review_performed": False,
    }.items():
        if json_inventory.get(key) != expected:
            failures.append(f"JSON import evidence is incorrect: {key}")
    json_objects = json_inventory.get("objects", [])
    if len(json_objects) != 6:
        failures.append("JSON import sanitized inventory must contain six object descriptions")
    if any(key == "id" or key.endswith("_id") for item in json_objects for key in item):
        failures.append("JSON import inventory contains an internal Sandbox ID")

    runtime_validation = subprocess.run(
        [
            sys.executable,
            str(
                ROOT
                / "json_import_rebuild/runtime_instantiation/validate_runtime_instantiation.py"
            ),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if runtime_validation.returncode != 0:
        failures.append(
            "runtime-instantiation evidence validator failed: "
            + runtime_validation.stdout.replace("\n", " ").strip()
        )

    read_only_validation = subprocess.run(
        [
            sys.executable,
            str(
                ROOT
                / "read_only_api_confirmation/validate_read_only_api_confirmation.py"
            ),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if read_only_validation.returncode != 0:
        failures.append(
            "read-only API evidence validator failed: "
            + read_only_validation.stdout.replace("\n", " ").strip()
        )

    manifest = json.loads((ROOT / "prompt_5b_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("atomicity_classification") != "api_patch_unresolved":
        failures.append("manifest atomicity classification is incorrect")
    if manifest.get("sandbox", {}).get("api_requests_attempted") != 1:
        failures.append("manifest Sandbox API-request count is incorrect")
    if manifest.get("sandbox", {}).get("token_requests_attempted") != 1:
        failures.append("manifest token-request count is incorrect")
    if manifest.get("sandbox", {}).get("hostname_runtime_api_verified") is not True:
        failures.append("manifest exact Sandbox runtime origin was not verified")
    if manifest.get("sandbox", {}).get("exact_test_membership") != "not_run_oauth_failed":
        failures.append("manifest exact-Test API membership state is incorrect")
    if manifest.get("status") != "read_only_api_authoritative_oauth_400_controlled_stop":
        failures.append("manifest controlled-stop status is incorrect")
    if manifest.get("mapping", {}).get("saved_worksheet_definition_contract") != "passed_43_of_43":
        failures.append("manifest saved-definition classification is incorrect")
    if manifest.get("mapping", {}).get("direct_existing_test_instantiation") != "failed_blank_default_5x5":
        failures.append("manifest direct existing-Test classification is incorrect")
    if manifest.get("mapping", {}).get("normal_assay_test_instantiation") != "passed":
        failures.append("manifest normal Assay Test classification is incorrect")
    if (
        manifest.get("mapping", {}).get("destination_contract_classification")
        != json_import_classification
    ):
        failures.append("manifest current destination classification is incorrect")
    if manifest.get("mapping", {}).get("runtime_gate_classification") != "passed_43_of_43":
        failures.append("manifest runtime gate classification is incorrect")
    native_manifest = manifest.get("native_test_worksheet_probe", {})
    if native_manifest.get("classification") != native_classification:
        failures.append("manifest native probe classification is incorrect")
    if native_manifest.get("old_sandbox_test_worksheet_engine") != "operational_for_native_definitions":
        failures.append("manifest native worksheet engine conclusion is incorrect")
    if native_manifest.get("imported_prompt3_test_worksheet") != "compatibility_failure":
        failures.append("manifest Prompt 3 compatibility conclusion is incorrect")
    if native_manifest.get("blank_baseline_restored") is not True:
        failures.append("manifest does not record restored native blank baseline")
    rebuild_manifest = manifest.get("native_43_field_rebuild", {})
    if rebuild_manifest.get("classification") != rebuild_classification:
        failures.append("manifest native 43-field rebuild classification is incorrect")
    if rebuild_manifest.get("phase_1_expected_destinations") != 7 or rebuild_manifest.get(
        "phase_1_persisted_destinations"
    ) != 4 or rebuild_manifest.get("phase_1_missing_destinations") != 3:
        failures.append("manifest native 43-field Phase 1 counts are incorrect")
    if rebuild_manifest.get("indexed_bracket_names_persisted") is not False:
        failures.append("manifest incorrectly claims bracketed names persisted")
    if rebuild_manifest.get("version_2_created") is not False:
        failures.append("manifest incorrectly claims Version 2 exists")
    if rebuild_manifest.get("export_spreadsheet_download_produced") is not False:
        failures.append("manifest incorrectly claims a rebuild export download")
    scalar_manifest = manifest.get("native_scalar_43_field_rebuild", {})
    if scalar_manifest.get("classification") != scalar_classification:
        failures.append("manifest native scalar rebuild classification is incorrect")
    if scalar_manifest.get("phase_1_expected_destinations") != 7 or scalar_manifest.get(
        "phase_1_persisted_destinations"
    ) != 0 or scalar_manifest.get("phase_1_missing_destinations") != 7:
        failures.append("manifest native scalar Phase 1A counts are incorrect")
    if scalar_manifest.get("version_1_state") != "Draft":
        failures.append("manifest native scalar Version 1 state is incorrect")
    if scalar_manifest.get("version_2_created") is not False:
        failures.append("manifest incorrectly claims native scalar Version 2 exists")
    if scalar_manifest.get("export_spreadsheet_run") is not False:
        failures.append("manifest incorrectly claims a native scalar export action")
    diagnostic_manifest = manifest.get("named_cell_persistence_diagnostic", {})
    if diagnostic_manifest.get("classification") != version_control_classification:
        failures.append("manifest named-cell diagnostic classification is incorrect")
    for key, expected in {
        "manual_named_cell_persistence_control": "passed",
        "qbench_native_named_cell_persistence": "operational",
        "codex_browser_named_cell_save_control": "failed",
        "browser_control_authoritative": False,
        "manual_control_system_name": "sdf",
        "manual_control_cell": "A1",
        "manual_control_version_row_visibly_present": True,
        "manual_control_display_name": "",
        "manual_control_exportable": True,
        "manual_control_visible_after_exact_reopen": True,
        "codex_control_system_name": "terpenes_codex_save_control_20260717",
        "codex_control_cell": "B2",
        "codex_control_display_name": "Codex save control",
        "codex_control_exportable": True,
        "codex_control_row_complete_before_save": True,
        "save_draft_used": True,
        "save_as_new_version_used": False,
        "both_rows_survived_refresh_and_reopen": False,
        "manual_control_remains": True,
        "codex_control_deleted_after_success": False,
        "cleanup_not_applicable_because_control_absent": True,
    }.items():
        if diagnostic_manifest.get(key) != expected:
            failures.append(f"manifest named-cell correction is incorrect: {key}")
    if diagnostic_manifest.get("probe_a_classification") != "unique_named_cell_control_failed":
        failures.append("manifest named-cell Probe A classification is incorrect")
    if diagnostic_manifest.get("row_visibly_committed_before_save") is not True:
        failures.append("manifest does not record the visibly committed Probe A row")
    if diagnostic_manifest.get("named_cell_persisted_after_reopen") is not False:
        failures.append("manifest incorrectly claims the Probe A named cell persisted")
    if any(diagnostic_manifest.get(key) is not False for key in (
        "probe_b_run", "probe_b_nozero_run", "probe_c_run", "further_worksheet_construction_allowed"
    )):
        failures.append("manifest does not preserve the Probe A stop gate")
    version_control_manifest = manifest.get("version_creation_diagnostic", {})
    if version_control_manifest.get("classification") != version_control_classification:
        failures.append("manifest version-creation diagnostic classification is incorrect")
    for key, expected in {
        "historical_classification": "version_created_named_cell_missing",
        "manual_named_cell_persistence_control": "passed",
        "qbench_native_named_cell_persistence": "operational",
        "codex_browser_named_cell_save_control": "failed",
        "browser_control_authoritative": False,
    }.items():
        if version_control_manifest.get(key) != expected:
            failures.append(f"manifest version-creation correction is incorrect: {key}")
    for key, expected in {
        "version_state": "Draft",
        "version_row_visibly_present": True,
        "grid_rows": 6,
        "grid_columns": 5,
        "a1": "Version creation control",
        "b2": "",
        "named_cell_rows_before_create": 1,
        "named_cell_rows_after_reopen": 0,
        "destination_contract_proven": False,
    }.items():
        if version_control_manifest.get(key) != expected:
            failures.append(f"manifest version-creation diagnostic is incorrect: {key}")
    json_manifest = manifest.get("json_import_rebuild", {})
    for key, expected in {
        "classification": json_import_classification,
        "implementation_path": "native_export_legacy_envelope_correction",
        "manual_named_cell_entry": False,
        "working_native_export_sha256": "d86e05122bc9a7fc4b6937e5582d9ff469f15c234e606fc0c5bbdd7d7c3659e5",
        "qualified_address_candidate_sha256": "54a65e029b9f1a038a21428cf40727896130db86041fafcc2d0bdf868e7fe35b",
        "qualified_address_render_result": "passed_40x26_grid_and_43_named_cells",
        "qualified_address_save_result": "rejected_sheet_qualified_cell_definition",
        "qualified_address_save_error": "Invalid cell definition Data!D2 for field name terpenes_instrument_conc_01",
        "candidate_sha256": expected_json_candidate_hash,
        "candidate_local_validation": "passed",
        "candidate_envelope": "legacy_table_config_qb_config",
        "logical_address_representation": "Data!D2",
        "old_sandbox_json_cell_representation": "D2",
        "json_named_cell_representation": "unqualified_independent_scalar_cells",
        "json_unqualified_named_cells": 43,
        "json_qualified_named_cells": 0,
        "a2_mapping_present": False,
        "first_analyte_json_cell": "D2",
        "worksheet_tabs": ["Data"],
        "grid_rows": 40,
        "grid_columns": 26,
        "required_anchor_count": 28,
        "non_empty_cell_count": 30,
        "named_cells": 43,
        "analyte_named_cells": 23,
        "analyte_naming": "terpenes_instrument_conc_01_through_23",
        "analyte_logical_cells": "Data!D2:Z2",
        "analyte_json_cells": "D2:Z2",
        "missing_destinations": 0,
        "renamed_destinations": 0,
        "duplicated_destinations": 0,
        "formula_owned_destinations": 0,
        "address_only_difference_count": 43,
        "rendered_worksheet_structure_unchanged": True,
        "worksheet": "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE",
        "worksheet_state": "json_scalar_43_field_base_v1_approved_active",
        "config_style_reference_type": "absent",
        "config_style_candidate_type": "absent",
        "corrected_upload_attempted": True,
        "corrected_candidate_attached": True,
        "corrected_import_submitted": True,
        "corrected_draft_version_created": True,
        "corrected_version": "JSON Scalar 43 Field Base v1",
        "corrected_version_state": "APPROVED and ACTIVE",
        "corrected_version_row_visibly_present": True,
        "grid_before_refresh": "40x26",
        "grid_after_refresh_and_list_reopen": "40x26",
        "imported_named_cells_before_refresh": 43,
        "imported_named_cells_after_reopen": 43,
        "round_trip_export_created": True,
        "round_trip_sha256": expected_round_trip_hash,
        "semantic_round_trip_run": True,
        "semantic_round_trip_result": "passed_after_normalizing_only_qbench_regenerated_renderer_uuid",
        "json_import_saved_definition_contract": "passed_43_of_43",
        "json_import_round_trip": "passed",
        "destination_contract_proven": json_import_classification,
        "atomicity_classification": "api_patch_unresolved",
        "analyte_patch_key_contract": "unresolved",
        "approval_activation_classification": "passed_43_of_43",
        "approval_procedure_correction": approval_procedure_correction,
        "status_progression": ["DRAFT", "PENDING", "APPROVED", "ACTIVE"],
        "approval_attempted": True,
        "approval_error": "This worksheet cannot be modified because it is currently locked.",
        "direct_approval_without_lock_required": True,
        "manual_approval_verified": True,
        "final_list_reopen_confirmed_single_version_1_approved_active": True,
        "candidate_promoted": False,
        "approved": True,
        "activated": True,
    }.items():
        if json_manifest.get(key) != expected:
            failures.append(f"manifest JSON import evidence is incorrect: {key}")
    runtime_manifest = manifest.get("runtime_instantiation", {})
    for key, expected in {
        "classification": json_import_classification,
        "worksheet": "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE",
        "version": "JSON Scalar 43 Field Base v1",
        "initial_status": "DRAFT",
        "final_status": "APPROVED and ACTIVE",
        "approval_procedure_correction": approval_procedure_correction,
        "approved_active_definition": "passed_43_of_43",
        "assay_assignment": "passed",
        "sample_creation": "passed",
        "test_creation": "passed",
        "runtime_grid_before_reopen": "40x26",
        "runtime_grid_after_reopen": "40x26",
        "blank_default_grid_appeared": False,
        "runtime_test_worksheet_contract": "passed_43_of_43",
        "runtime_representative_value_persistence": "passed",
        "b22_b23_remained_blank": True,
        "representative_values_cleared": True,
        "final_blank_destinations": 43,
        "runtime_export_filename": "json_import_rebuild/runtime_instantiation/SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_RUNTIME_TEST_WORKSHEET_export_data.csv",
        "runtime_export_sha256": "f7c702dd3ecac694c32b3aa686cca6cd4928198b7bda45f4d8e030e65d681bfe",
        "final_list_reopen_confirmed_single_version_1_approved_active": True,
    }.items():
        if runtime_manifest.get(key) != expected:
            failures.append(f"manifest runtime-instantiation evidence is incorrect: {key}")
    for key in (
        "version_2_created",
        "credentials_read_or_displayed",
        "oauth_token_requested",
        "qbench_rest_api_requested",
        "patch_requested",
        "live_qbench_accessed",
        "publish_or_qc_review_performed",
        "pass_fail_artifact_introduced",
    ):
        if runtime_manifest.get(key) is not False:
            failures.append(f"manifest runtime safety control is not false: {key}")

    read_only_manifest = manifest.get("read_only_api_confirmation", {})
    for key, expected in {
        "classification": "oauth_authoritative_endpoint_http_400_controlled_stop",
        "origin_preflight": "passed_exact_sandbox_origin",
        "allowed_origin": "https://ait-sandbox.qbench.net",
        "credential_loading": "passed_without_display",
        "historical_token_endpoint_template": "/qbench/api/v1/oauth/token",
        "authoritative_token_endpoint_template": "/qbench/api/v2/auth/token",
        "token_post_requests": 2,
        "historical_token_http_status": 404,
        "authoritative_retry_http_status": 400,
        "token_response_content_type": "application/json",
        "oauth_result": "failed_authoritative_endpoint_http_400",
        "token_returned": False,
        "get_requests": 0,
        "read_only_api_identity": "not_run_oauth_failed",
        "read_only_api_worksheet_contract": "not_run_oauth_failed",
        "destination_contract_proven": json_import_classification,
        "analyte_patch_key_contract": "unresolved",
        "atomicity_classification": "api_patch_unresolved",
        "patch_requests": 0,
        "put_requests": 0,
        "delete_requests": 0,
        "non_token_post_requests": 0,
        "objects_changed": 0,
        "analytical_results_changed": False,
        "live_qbench_accessed": False,
        "publish_or_qc_review_performed": False,
        "pass_fail_artifact_introduced": False,
        "credentials_token_or_authorization_committed_or_displayed": False,
        "assertion_committed_or_displayed_by_runner": False,
        "swagger_assertion_transient_tool_output_control_failed": True,
    }.items():
        if read_only_manifest.get(key) != expected:
            failures.append(f"manifest read-only API evidence is incorrect: {key}")
    if read_only_manifest.get("field_key_classification_counts") != {
        "observed_exact": 0,
        "missing": 0,
        "renamed": 0,
        "duplicated": 0,
        "present_but_unreadable": 0,
        "not_exposed_by_get_contract": 43,
    }:
        failures.append("manifest read-only field-key counts are incorrect")
    expected_sandbox_objects = [
        "SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF",
        "SBX_ONLY_TERPENES_API_DESTINATION_PROOF_V2",
        "SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF_TEST",
        "SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF_SAMPLE",
        "SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_ASSAY",
        "SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_ASSAY_SAMPLE",
        "SBX_ONLY_TERPENES_2026_07_17_NATIVE_TEST_WS_PROBE",
        "Native Test Worksheet Probe v1",
        "Native Test Worksheet Probe v2",
        "SBX_ONLY_TERPENES_2026_07_17_NATIVE_TEST_WS_ASSAY",
        "SBX_ONLY_TERPENES_2026_07_17_NATIVE_TEST_WS_SAMPLE",
        "fresh Test created only from SBX_ONLY_TERPENES_2026_07_17_NATIVE_TEST_WS_ASSAY",
        "SBX_ONLY_TERPENES_2026_07_17_NATIVE_43_FIELD_BASE",
        "Native 43 Field Base v1",
        "SBX_ONLY_TERPENES_2026_07_17_NATIVE_SCALAR_43_FIELD_BASE",
        "Native Scalar 43 Field Base v1",
        "SBX_ONLY_TERPENES_2026_07_17_NAMED_CELL_UNIQUE_CONTROL",
        "Named Cell Unique Control v1",
        "SBX_ONLY_TERPENES_2026_07_17_VERSION_CREATION_CONTROL",
        "Version Creation Control v1",
        "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE",
        "JSON Scalar 43 Field Base v1",
        "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_ASSAY",
        "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_RUNTIME_SAMPLE",
        "fresh Test created only from SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_ASSAY",
    ]
    if manifest.get("sandbox", {}).get("objects_created_or_changed") != expected_sandbox_objects:
        failures.append("manifest Sandbox mutations are not the exact authorized proof objects")
    for item in manifest.get("generated_files", []):
        relative = item.get("path")
        path = ROOT / str(relative)
        if not path.is_file():
            failures.append(f"manifest file missing: {relative}")
        elif digest(path) != item.get("sha256"):
            failures.append(f"manifest hash mismatch: {relative}")

    if failures:
        print("Prompt 5B package validation FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Prompt 5B package validation PASSED")
    print("- 43 ordered non-Pass/Fail destinations")
    print("- saved Worksheet definition passed 43/43")
    print("- historical direct and original Assay Test probes classified blank default 5x5")
    print("- native UI-built Assay Test instantiation passed with exact persistence")
    print("- old Sandbox engine operational; imported Prompt 3 compatibility failure")
    print("- exact native 43-field rebuild stopped at Phase 1 with 4/7 persisted")
    print("- native scalar candidate validated at 43 mappings and 23 exact analytes")
    print("- native scalar saved/reopened Phase 1A stopped at 0/7; no promotion or runtime")
    print("- historical unique one-cell Probe A failed; Probes B/C not run")
    print("- user manual sdf/A1 persistence control passed")
    print("- QBench native named-cell persistence operational")
    print("- historical Codex B2 save control failed while sdf remained")
    print("- failed newer-envelope import classified wrong-target and collapsed-renderer")
    print("- qualified-address native envelope rendered 40x26 with 43 named cells")
    print("- qualified-address Save As New Version rejected by old one-tab validator")
    print("- unqualified-address JSON candidate passed local 43/43 validation")
    print("- exactly 43 address strings changed; rendered structure unchanged")
    print("- saved definition and raw round trip passed 43/43")
    print("- exact Version 1 is APPROVED and ACTIVE; direct approval required no review lock")
    print("- normal isolated Assay/Sample/Test instantiation passed with a 40x26 runtime grid")
    print("- runtime CSV contains exactly 43 blank destinations")
    print("- representative values persisted, controlled cells stayed blank, and all five probes were cleared")
    print("- sanitized eight-object inventory contains no internal Sandbox IDs")
    print("- sanitized six-object native inventory contains no internal Sandbox IDs")
    print("- exact Sandbox-only executable allowlist")
    print("- atomicity remains api_patch_unresolved")
    print("- historical wrong-path token POST preserved as HTTP 404")
    print("- one authoritative-route token retry returned HTTP 400; zero GET requests")
    print("- zero PATCH, PUT, DELETE, non-token POST, object changes, or result changes")
    print(f"- {len(manifest['generated_files'])} generated-file hashes verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
