#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> int:
    failures: list[str] = []
    inventory = json.loads((ROOT / "sanitized_object_inventory.json").read_text(encoding="utf-8"))

    expected = {
        "sanitized": True,
        "internal_sandbox_ids_omitted": True,
        "classification": "approval_activation_blocked_active_lock_assignee_mismatch",
        "manual_lock_resolution_reported": True,
        "manual_lock_resolution_visible_in_current_session": False,
        "approval_attempt_count": 2,
        "final_list_reopen_confirmed_single_version_1_pending": True,
        "approved": False,
        "activated": False,
        "version_2_created": False,
        "assay_created": False,
        "sample_created": False,
        "test_created": False,
        "runtime_export_created": False,
        "representative_values_entered": False,
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
            failures.append(f"incorrect blocked-gate evidence: {key}")

    objects = inventory.get("objects")
    if not isinstance(objects, list) or len(objects) != 2:
        failures.append("sanitized inventory must contain exactly the worksheet and Version 1")
    elif any(key == "id" or key.endswith("_id") for item in objects for key in item):
        failures.append("sanitized inventory contains an internal QBench ID")

    if (ROOT / "runtime_export_sha256.txt").read_text(encoding="utf-8").strip() != (
        "not_available_phase_1_approval_gate"
    ):
        failures.append("runtime export hash sentinel is incorrect")

    required_markers = {
        "approval_activation_results.md": "approval_activation_blocked_active_lock_assignee_mismatch",
        "assay_assignment_results.md": "not_run_phase_1_approval_gate",
        "test_instantiation_results.md": "not_run_phase_1_approval_gate",
        "runtime_export_results.md": "not_run_phase_1_approval_gate",
        "representative_value_persistence.md": "not_run_phase_1_approval_gate",
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
    print("- Phase 1 approval blocked by active lock/assignee mismatch")
    print("- no Assay, Sample, Test, runtime export, or representative values")
    print("- zero token, API, PATCH, live, Publish, QC Review, or Pass/Fail actions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
