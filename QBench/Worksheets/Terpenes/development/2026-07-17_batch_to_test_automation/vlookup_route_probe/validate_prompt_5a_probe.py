#!/usr/bin/env python3
"""Validate the Prompt 5A per-Test VLOOKUP routing-probe evidence."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent

REQUIRED_FILES = {
    "README.md",
    "named_cell_mapping.csv",
    "routing_evidence.json",
    "sandbox_change_log.md",
    "sandbox_cleanup_plan.md",
    "sandbox_object_inventory.csv",
    "sandbox_routing_result.md",
    "sanitized_automation_configuration.json",
    "validate_prompt_5a_probe.py",
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    present = {path.name for path in HERE.iterdir() if path.is_file()}
    missing = sorted(REQUIRED_FILES - present)
    assert not missing, f"missing required files: {missing}"

    evidence = load_json(HERE / "routing_evidence.json")
    config = load_json(HERE / "sanitized_automation_configuration.json")

    assert evidence["classification"] == "per_test_vlookup_error"
    assert evidence["environment"]["hostname_verified_before_mutations"] == (
        "ait-sandbox.qbench.net"
    )
    assert evidence["environment"]["live_qbench_accessed"] is False
    assert evidence["execution"]["trigger_count"] == 1
    assert evidence["execution"]["task_created_automation_history_entries"] == 1
    assert evidence["execution"]["automation_history_status"] == "Success"
    assert evidence["execution"]["final_automation_active"] is False
    assert evidence["scope_controls"]["configured_terpenes_mapping_fields"] == 0
    assert evidence["scope_controls"]["pass_fail_created"] is False

    expected_rows = [(290, 101), (291, 202), (292, 303)]
    observed_rows = [
        (row["synthetic_qbench_test_id"], row["probe_value"])
        for row in evidence["batch_table"]["rows"]
    ]
    assert observed_rows == expected_rows
    assert evidence["source_expression"] == "=VLOOKUP({{test.id}}, A2:B4, 2)"

    observations = evidence["test_observations_after_reopen"]
    assert len(observations) == 3
    for observation, (test_id, expected_value) in zip(observations, expected_rows):
        assert observation["synthetic_qbench_test_id"] == test_id
        assert observation["expected_route_probe"] == expected_value
        assert observation["observed_route_probe"] is None
        assert observation["route_probe_native_numeric"] is False
        assert observation["observed_qbench_test_id_display"] == test_id
        assert observation["observed_route_probe_sentinel"] == "UNCHANGED"
        assert observation["other_worksheet_field_changed"] is False

    assert set(evidence["secondary_guard_probes"].values()) == {
        "not_run_routing_did_not_pass"
    }

    assert config["requested_name_length"] == 53
    assert config["saved_name_length"] == 47
    assert config["trigger"] == {"event": "Data Modified", "data_type": "Batch"}
    assert len(config["conditions"]) == 1
    assert len(config["actions"]) == 1
    assert config["actions"][0]["source_expression"] == evidence["source_expression"]
    assert config["activation"]["final_active"] is False

    export_paths = {}
    for raw_export in evidence["raw_exports"]:
        path = HERE / raw_export["path"]
        assert path.is_file(), f"missing raw export: {path}"
        assert sha256(path) == raw_export["sha256"], f"hash mismatch: {path}"
        export_paths[path.name] = path

    batch_path = export_paths[
        "SBX_ONLY_TERPENES_2026_07_17_VLOOKUP_ROUTE_BATCH_WS__raw_export_spreadsheet.json"
    ]
    test_path = export_paths[
        "SBX_ONLY_TERPENES_2026_07_17_VLOOKUP_ROUTE_TEST_WS__raw_export_spreadsheet.json"
    ]
    batch_book = load_json(batch_path)
    test_book = load_json(test_path)

    batch_sheet = batch_book["config"]["worksheets"][0]
    assert batch_sheet["data"][0][:2] == ["Test ID", "Probe Value"]
    assert all(
        value == ""
        for row in batch_sheet["data"][1:]
        for value in row
    )

    test_sheet = test_book["config"]["worksheets"][0]
    assert test_sheet["data"][0][:2] == ["route_probe", ""]
    assert test_sheet["data"][1][:2] == ["qbench_test_id_display", "${test.id}"]
    assert test_sheet["data"][2][:2] == ["route_probe_sentinel", '=\"UNCHANGED\"']
    assert test_sheet["cells"]["B2"]["readonly"] is True
    assert test_sheet["cells"]["B3"]["readonly"] is True
    assert "B1" not in test_sheet["cells"] or (
        test_sheet["cells"]["B1"].get("readonly") is not True
    )
    assert test_book["data"]["Sheet1"][2][1] == "UNCHANGED"
    assert test_book["qb_config"].get("named_cells") in (None, {})

    with (HERE / "named_cell_mapping.csv").open(
        "r", encoding="utf-8", newline=""
    ) as handle:
        mappings = list(csv.DictReader(handle))
    assert [row["system_name"] for row in mappings] == [
        "route_probe",
        "qbench_test_id_display",
        "route_probe_sentinel",
    ]
    assert [row["cell"] for row in mappings] == ["B1", "B2", "B3"]
    assert all(row["observed_in_post_run_export"] == "false" for row in mappings)

    with (HERE / "sandbox_object_inventory.csv").open(
        "r", encoding="utf-8", newline=""
    ) as handle:
        objects = list(csv.DictReader(handle))
    assert len(objects) == 11
    assert sum(row["object_type"] == "Test" for row in objects) == 3
    assert sum(row["object_type"] == "Sample" for row in objects) == 3
    automation = next(row for row in objects if row["object_type"] == "Automation")
    assert automation["final_status"] == "Inactive"

    print(
        "Prompt 5A probe validation passed: exact raw exports and hashes verified; "
        "3 synthetic Test mappings checked; one trigger; final inactive state; "
        "missing named-cell setup fault confirmed; classification per_test_vlookup_error."
    )


if __name__ == "__main__":
    main()
