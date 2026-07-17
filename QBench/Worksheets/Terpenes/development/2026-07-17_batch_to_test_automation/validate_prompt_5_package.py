#!/usr/bin/env python3
"""Validate the sanitized Prompt 5 blocker/evidence package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]

REQUIRED_FILES = {
    "README.md",
    "automation_configuration.md",
    "automation_mapping.csv",
    "batch_publish_gate.md",
    "test_matching_contract.md",
    "idempotency_contract.md",
    "sandbox_object_inventory.csv",
    "sandbox_success_results.md",
    "sandbox_failure_results.md",
    "sandbox_duplicate_results.md",
    "sandbox_change_log.md",
    "sandbox_cleanup_plan.md",
    "live_promotion_gap_analysis.md",
    "sanitized_automation_configuration.json",
    "validate_prompt_5_package.py",
    "prompt_5_manifest.json",
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

    manifest = load_json(HERE / "prompt_5_manifest.json")
    config = load_json(HERE / "sanitized_automation_configuration.json")

    assert manifest["status"] == "blocked_stop_condition_before_activation"
    assert manifest["environment"]["sandbox_hostname_verified"] == "ait-sandbox.qbench.net"
    assert manifest["environment"]["live_qbench_accessed"] is False
    assert manifest["sandbox_internal_object_ids_included"] is False
    assert manifest["validation"]["test_worksheet_writes"] == 0
    assert manifest["validation"]["pass_fail_artifact_created"] is False

    assert config["active"] is False
    assert config["conditions"] == []
    assert config["actions"] == []
    assert config["capability_observation"]["exact_test_id_target_selector"] is False
    assert config["capability_observation"]["match_cardinality_guard"] is False
    assert "internal_id" not in config

    with (HERE / "automation_mapping.csv").open("r", encoding="utf-8", newline="") as handle:
        mappings = list(csv.DictReader(handle))
    assert len(mappings) == 43, f"expected 43 mapping rows, found {len(mappings)}"
    assert [int(row["sequence"]) for row in mappings] == list(range(1, 44))
    assert all(row["status"] == "intended_not_configured" for row in mappings)

    test_path = REPO / manifest["source_artifacts"][0]["path"]
    batch_path = REPO / manifest["source_artifacts"][1]["path"]
    test_book = load_json(test_path)
    batch_book = load_json(batch_path)

    test_names = test_book["qb_config"]["named_cells"]
    batch_names = batch_book["qb_config"]["named_cells"]
    for row in mappings:
        destination = row["destination_named_cell"].split("[", 1)[0]
        assert destination in test_names, f"missing Test named cell: {destination}"
        assert row["source_named_range"] in batch_names, (
            f"missing Batch named range: {row['source_named_range']}"
        )

    data_sheet = next(
        sheet for sheet in test_book["config"]["worksheets"]
        if sheet["worksheetName"] == "Data"
    )
    for column in "DEFGHIJKLMNOPQRSTUVWXYZ":
        assert data_sheet["cells"][f"{column}2"]["readonly"] is False
        for row_number in range(3, 7):
            assert data_sheet["cells"][f"{column}{row_number}"]["readonly"] is True
            value = data_sheet["data"][row_number - 1][ord(column) - ord("A")]
            assert isinstance(value, str) and value.startswith("=")

    for source in manifest["source_artifacts"]:
        source_path = REPO / source["path"]
        assert sha256(source_path) == source["sha256"], f"hash mismatch: {source['path']}"

    print(
        "Prompt 5 package validation passed: "
        "16 required files, 43 intended mappings, source hashes verified, "
        "automation inactive with zero saved conditions/actions, zero Test writes."
    )


if __name__ == "__main__":
    main()
