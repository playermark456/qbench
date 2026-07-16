#!/usr/bin/env python3
"""Validate the sanitized Prompt 4.6B scalar-patch evidence package."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "qbench_scalar_patch_probe.js"
FIXTURE = ROOT / "tests" / "fixtures" / "expected_scalar_patch_payload.json"
ATTEMPT1_FIXTURE = ROOT / "tests" / "fixtures" / "attempt_1_nested_scalar_patch_payload.json"
RESULT = ROOT / "docs" / "sandbox_scalar_patch_result.md"


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    attempt1_fixture = json.loads(ATTEMPT1_FIXTURE.read_text(encoding="utf-8"))
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
    assert fixture["data"]["probe_text"] == "sandbox_probe"
    assert fixture["data"]["probe_number"] == 1.25
    assert isinstance(fixture["data"]["probe_number"], float)
    assert '{ value: "sandbox_probe" }' not in source
    assert "{ value: 1.25 }" not in source

    assert attempt1_fixture["batchId"] == "<runtime-only synthetic Batch context>"
    assert attempt1_fixture["data"]["probe_text"] == {"value": "sandbox_probe"}
    assert attempt1_fixture["data"]["probe_number"] == {"value": 1.25}

    required_result_markers = (
        "accepted_callback_but_noop_nested_value_shape",
        "accepted_callback_but_noop_direct_scalar_shape",
        "patch_callback = success",
        "zero changed cells",
        "second silent no-op",
        "Range/matrix testing did not start",
        "Prompt 5 did not start",
        "Production `ait.qbench.net` was not accessed or changed",
    )
    for marker in required_result_markers:
        assert marker in result, marker

    assert not re.search(r"\b(?:Batch|parser|attachment|worksheet-version) ID\s*[:#]?\s*\d+\b", result, re.I)
    print("scalar patch evidence validation: ok (direct values, no nested wrappers)")


if __name__ == "__main__":
    main()
