#!/usr/bin/env python3
"""Validate the sanitized Prompt 4.6B scalar-patch evidence package."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "qbench_scalar_patch_probe.js"
FIXTURE = ROOT / "tests" / "fixtures" / "expected_scalar_patch_payload.json"
ATTEMPT1_FIXTURE = ROOT / "tests" / "fixtures" / "attempt_1_nested_scalar_patch_payload.json"
TRIGGER_FIXTURE = ROOT / "tests" / "fixtures" / "SBX_ONLY_TERPENES_SCALAR_PATCH_TRIGGER_01.txt"
CONTROLLED_FIXTURE = ROOT.parent.parent / "source" / "Output_redacted_fixture.txt"
RESULT = ROOT / "docs" / "sandbox_scalar_patch_result.md"


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    attempt1_fixture = json.loads(ATTEMPT1_FIXTURE.read_text(encoding="utf-8"))
    trigger_fixture = TRIGGER_FIXTURE.read_bytes()
    controlled_fixture = CONTROLLED_FIXTURE.read_bytes()
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

    assert trigger_fixture == controlled_fixture
    assert len(trigger_fixture) == 8692
    assert hashlib.sha256(trigger_fixture).hexdigest() == (
        "ed796c690b972ca08f1976b1d8f7355d3e5140e73ffa912c441d6185a093283b"
    )

    required_result_markers = (
        "accepted_callback_but_noop_nested_value_shape",
        "accepted_callback_but_noop_direct_scalar_shape",
        "manual_persistence_result = manual_persistence_passed",
        "batch_assignment_result = batch_assignment_verified",
        "runtime_mode_diagnostic_initial_attempt = blocked",
        "runtime_mode_diagnostic = attachment_trigger_runtime_stalled",
        "code_parser_patchworksheet_status = blocked_old_sandbox_runtime_stall",
        "qbench_code_parser_write_status = blocked",
        "qbench_sandbox_scalar_probe_status = blocked_runtime_stall",
        "recommended_next_route = no_code_file_parser_with_normalized_tsv",
        "SBX_ONLY_TERPENES_SCALAR_PATCH_TRIGGER_01.txt",
        "ed796c690b972ca08f1976b1d8f7355d3e5140e73ffa912c441d6185a093283b",
        "File Parser Results status: not created",
        "Callback result: not reached",
        "exactly one File Parser Results job was created",
        "job remained `IN_PROGRESS`",
        "neither the success nor error callback was observable",
        "awaits a Promise that settles only when the",
        "awaited execution did not settle",
        "attachment_trigger_runtime_stalled",
        "The old ait-sandbox.qbench.net File Parser attachment runtime did not complete the controlled patchWorksheet request and cannot currently be used as a reliable Spreadsheet Worksheet writer.",
        "does not state that `patchWorksheet` is universally",
        "Raw LabSolutions ASCII",
        "controlled local Prompt 4.5 parser/adapter",
        "normalized tab-delimited wide-row file",
        "QBench No-Code File Parser",
        "Batch Instrument Import worksheet",
        "only `A:AE` and `AH:BE`",
        "`AF` and `AG` untouched",
        "The exact trigger is inert because the parser is inactive",
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
    print(
        "scalar patch evidence validation: ok "
        "(two Preview no-ops, manual persistence passed, attachment runtime stall blocked safely)"
    )


if __name__ == "__main__":
    main()
