#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
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
    if config.get("token_endpoint_contract_proven") is not False or config.get("token_path"):
        failures.append("unproven OAuth token endpoint is configured")
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
        '"grant_type": "client_credentials"',
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

    diagnostic_classification = "native_named_cell_save_environment_or_procedure_blocked"
    diagnostic_inventory = json.loads(
        (
            ROOT
            / "native_43_field_rebuild/named_cell_persistence_diagnostic/sanitized_object_inventory.json"
        ).read_text(encoding="utf-8")
    )
    if diagnostic_inventory.get("classification") != diagnostic_classification:
        failures.append("named-cell persistence diagnostic classification is incorrect")
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

    manifest = json.loads((ROOT / "prompt_5b_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("atomicity_classification") != "api_patch_unresolved":
        failures.append("manifest atomicity classification is incorrect")
    if manifest.get("sandbox", {}).get("api_requests_attempted") != 0:
        failures.append("manifest claims a Sandbox API request")
    if manifest.get("sandbox", {}).get("token_requests_attempted") != 0:
        failures.append("manifest claims a token request")
    if manifest.get("status") != "native_named_cell_save_environment_or_procedure_blocked_pre_token_stop":
        failures.append("manifest controlled-stop status is incorrect")
    if manifest.get("mapping", {}).get("saved_worksheet_definition_contract") != "passed_43_of_43":
        failures.append("manifest saved-definition classification is incorrect")
    if manifest.get("mapping", {}).get("direct_existing_test_instantiation") != "failed_blank_default_5x5":
        failures.append("manifest direct existing-Test classification is incorrect")
    if manifest.get("mapping", {}).get("normal_assay_test_instantiation") != normal_classification:
        failures.append("manifest normal Assay Test classification is incorrect")
    if manifest.get("mapping", {}).get("destination_contract_classification") != diagnostic_classification:
        failures.append("manifest current destination classification is incorrect")
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
    if diagnostic_manifest.get("classification") != diagnostic_classification:
        failures.append("manifest named-cell diagnostic classification is incorrect")
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
    print("- direct and normal Assay Test instantiations classified blank default 5x5")
    print("- native UI-built Assay Test instantiation passed with exact persistence")
    print("- old Sandbox engine operational; imported Prompt 3 compatibility failure")
    print("- exact native 43-field rebuild stopped at Phase 1 with 4/7 persisted")
    print("- native scalar candidate validated at 43 mappings and 23 exact analytes")
    print("- native scalar saved/reopened Phase 1A stopped at 0/7; no promotion or runtime")
    print("- unique one-cell Probe A failed after explicit UI commit; Probes B/C not run")
    print("- native named-cell worksheet construction blocked for QBench support review")
    print("- sanitized eight-object inventory contains no internal Sandbox IDs")
    print("- sanitized six-object native inventory contains no internal Sandbox IDs")
    print("- exact Sandbox-only executable allowlist")
    print("- atomicity remains api_patch_unresolved")
    print("- zero token/API requests and exact authorized Sandbox objects only")
    print(f"- {len(manifest['generated_files'])} generated-file hashes verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
