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

    manifest = json.loads((ROOT / "prompt_5b_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("atomicity_classification") != "api_patch_unresolved":
        failures.append("manifest atomicity classification is incorrect")
    if manifest.get("sandbox", {}).get("api_requests_attempted") != 0:
        failures.append("manifest claims a Sandbox API request")
    if manifest.get("sandbox", {}).get("token_requests_attempted") != 0:
        failures.append("manifest claims a token request")
    if manifest.get("status") != "normal_assay_test_instantiation_failed_blank_default_pre_token_controlled_stop":
        failures.append("manifest controlled-stop status is incorrect")
    if manifest.get("mapping", {}).get("saved_worksheet_definition_contract") != "passed_43_of_43":
        failures.append("manifest saved-definition classification is incorrect")
    if manifest.get("mapping", {}).get("direct_existing_test_instantiation") != "failed_blank_default_5x5":
        failures.append("manifest direct existing-Test classification is incorrect")
    if manifest.get("mapping", {}).get("normal_assay_test_instantiation") != normal_classification:
        failures.append("manifest normal Assay Test classification is incorrect")
    expected_sandbox_objects = [
        "SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF",
        "SBX_ONLY_TERPENES_API_DESTINATION_PROOF_V2",
        "SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF_TEST",
        "SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF_SAMPLE",
        "SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_ASSAY",
        "SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_ASSAY_SAMPLE",
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
    print("- sanitized eight-object inventory contains no internal Sandbox IDs")
    print("- exact Sandbox-only executable allowlist")
    print("- atomicity remains api_patch_unresolved")
    print("- zero token/API requests and exact authorized Sandbox proof objects only")
    print(f"- {len(manifest['generated_files'])} generated-file hashes verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
