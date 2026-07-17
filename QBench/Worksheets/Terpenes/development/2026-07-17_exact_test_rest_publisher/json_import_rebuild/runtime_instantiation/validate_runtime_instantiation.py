#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RAW_SHA256 = "f7c702dd3ecac694c32b3aa686cca6cd4928198b7bda45f4d8e030e65d681bfe"
EXPECTED_DESTINATIONS = [
    "Batch QC Disposition",
    "Detector ID",
    "Detector Name",
    "DF",
    "DF Application Mode",
    "Final Volume",
    "Imported At",
    "Instrument Name",
    "LabSolutions Conc. Unit",
    "Unit Confirmed",
    "Parser Version",
    "Preparation Values Confirmed",
    "Publish Ready",
    "Sample Mass",
    "Source Batch ID",
    "Source Data File",
    "Source File Hash",
    "Source Instrument File",
    "Source Method File",
    "Source Sequence File",
    "alpha-Pinene",
    "Camphene",
    "beta-Myrcene",
    "beta-Pinene",
    "Delta-3-carene",
    "alpha-Terpinene",
    "cis-Ocimene",
    "d-Limonene",
    "p-Cymene",
    "trans-Ocimene",
    "Eucalyptol",
    "gamma-Terpinene",
    "Terpinolene",
    "Linalool",
    "Isopulegol",
    "Geraniol",
    "beta-Caryophyllene",
    "alpha-Humulene",
    "cis-Nerolidol",
    "trans-Nerolidol",
    "Guaiol",
    "Caryophyllene Oxide",
    "alpha-Bisabolol",
]


def main() -> int:
    failures: list[str] = []
    inventory = json.loads((ROOT / "sanitized_object_inventory.json").read_text(encoding="utf-8"))

    expected = {
        "sanitized": True,
        "internal_sandbox_ids_omitted": True,
        "classification": "approval_attempt_procedural_error_unnecessary_lock_handling",
        "manual_approval_reported": True,
        "manual_approval_verified": True,
        "direct_approval_without_lock_required": True,
        "approved": True,
        "activated": True,
        "worksheet_record_activated": True,
        "approved_active_definition": "passed_43_of_43",
        "version_2_created": False,
        "assay_created": True,
        "assay_association_persisted": True,
        "sample_created": True,
        "test_created": True,
        "runtime_grid_before_reopen": "40x26",
        "runtime_grid_after_reopen": "40x26",
        "blank_default_grid_appeared": False,
        "runtime_export_created": True,
        "runtime_export_sha256": RAW_SHA256,
        "runtime_test_worksheet_contract": "passed_43_of_43",
        "representative_values_entered": True,
        "representative_values_persisted": True,
        "runtime_representative_value_persistence": "passed",
        "b22_b23_remained_blank": True,
        "representative_values_cleared": True,
        "final_blank_destinations": 43,
        "destination_contract_proven": "runtime_instantiation_passed_pending_read_only_api_confirmation",
        "atomicity_classification": "api_patch_unresolved",
        "analyte_patch_key_contract": "unresolved",
        "credentials_read_or_displayed": False,
        "oauth_token_requested": False,
        "qbench_rest_api_requested": False,
        "patch_requested": False,
        "live_qbench_accessed": False,
        "publish_or_qc_review_performed": False,
        "pass_fail_artifact_introduced": False,
    }
    for key, value in expected.items():
        if inventory.get(key) != value:
            failures.append(f"incorrect runtime evidence: {key}")

    objects = inventory.get("objects")
    if not isinstance(objects, list) or len(objects) != 5:
        failures.append("sanitized inventory must contain exactly five task-created object descriptions")
    elif any(key == "id" or key.endswith("_id") for item in objects for key in item):
        failures.append("sanitized inventory contains an internal QBench ID")

    if (ROOT / "runtime_export_sha256.txt").read_text(encoding="utf-8").strip() != RAW_SHA256:
        failures.append("runtime export SHA-256 evidence is incorrect")

    with (ROOT / "runtime_export_sanitized.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if len(rows) != 2:
        failures.append("sanitized runtime export must contain one header and one data row")
    else:
        if rows[0] != EXPECTED_DESTINATIONS:
            failures.append("sanitized runtime export destination headers are not the exact ordered 43")
        if len(rows[1]) != 43 or any(rows[1]):
            failures.append("sanitized runtime export destination row is not 43/43 blank")

    required_markers = {
        "approval_activation_results.md": "approved_active_definition=passed_43_of_43",
        "assay_assignment_results.md": "Status: **`passed`**",
        "test_instantiation_results.md": "normal_assay_test_instantiation=passed",
        "runtime_export_results.md": "runtime_test_worksheet_contract=passed_43_of_43",
        "representative_value_persistence.md": "runtime_representative_value_persistence=passed",
    }
    for name, marker in required_markers.items():
        if marker not in (ROOT / name).read_text(encoding="utf-8"):
            failures.append(f"missing classification marker in {name}")

    if failures:
        print("Runtime-instantiation evidence validation FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Runtime-instantiation evidence validation PASSED")
    print("- Approved/Active Version 1 definition passed 43/43; no Version 2")
    print("- normal Assay-created Test retained the full 40x26 runtime grid")
    print("- runtime export contract passed 43/43 and final baseline is blank")
    print("- representative values persisted, B22/B23 stayed blank, then all five were cleared")
    print("- zero credential, token, API, PATCH, live, Publish, QC Review, or Pass/Fail actions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
