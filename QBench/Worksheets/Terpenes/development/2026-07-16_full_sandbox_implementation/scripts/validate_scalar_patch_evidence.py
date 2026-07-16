#!/usr/bin/env python3
"""Validate the sanitized Prompt 4.6B scalar-patch evidence package."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "qbench_scalar_patch_probe.js"
FIXTURE = ROOT / "tests" / "fixtures" / "expected_scalar_patch_payload.json"
RESULT = ROOT / "docs" / "sandbox_scalar_patch_result.md"


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    result = RESULT.read_text(encoding="utf-8")

    assert source.count("service.patchWorksheet(") == 1
    for forbidden in (
        "updateWorksheet",
        "QBBatchService.update(",
        "fetch(",
        "XMLHttpRequest",
        "https://ait.qbench.net",
    ):
        assert forbidden not in source, forbidden

    assert not re.search(r"batchId\s*[:=]\s*\d+", source)
    assert set(fixture) == {"batchId", "data", "success", "error"}
    assert fixture["batchId"] == "<runtime-only synthetic Batch context>"
    assert set(fixture["data"]) == {"probe_text", "probe_number"}
    assert fixture["data"]["probe_text"] == {"value": "sandbox_probe"}
    assert fixture["data"]["probe_number"] == {"value": 1.25}
    assert isinstance(fixture["data"]["probe_number"]["value"], float)

    required_result_markers = (
        "failed_safely_success_callback_without_persisted_cell_changes",
        "patch_callback = success",
        "All 969",
        "silent no-op compatibility failure",
        "range/matrix testing did",
        "not start. Prompt 5 did not start",
        "Prompt 5 did not start",
        "Production\n`ait.qbench.net` was not accessed or changed",
    )
    for marker in required_result_markers:
        assert marker in result, marker

    assert not re.search(r"\b(?:Batch|parser|attachment|worksheet-version) ID\s*[:#]?\s*\d+\b", result, re.I)
    print("scalar patch evidence validation: ok")


if __name__ == "__main__":
    main()
