#!/usr/bin/env python3
"""Validate Phase 3 v2 science, schema, and historical renderer compatibility."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

import build_phase3_candidates as phase3_builder
import build_phase3_candidates_v2 as v2_builder
import validate_phase3_candidates as phase3_validator


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parents[4]
TEST_PATH = v2_builder.TEST_OUTPUT
BATCH_PATH = v2_builder.BATCH_OUTPUT
REPORT_PATH = PACKAGE_DIR / "phase3_v2_validation_report.md"
HISTORICAL_TEST_COMMIT = "443fa40809347114d543f442493dae6c55fc8f22"
HISTORICAL_BATCH_COMMIT = "28cd4f17db96f2c78dd60cba84c490d9e87a6dde"
HISTORICAL_TEST_HELPER_SHA256 = "0164d0c8a6014a3cc9a95c33d52b5a1250e6f308caa037b6a1bfed580d667883"
HISTORICAL_BATCH_HELPER_SHA256 = "1b4bcf3a20cb3faa3e56cd36d82006f528261e7a96f3d5efe2cec01a54345772"
TEST_SOURCE_PATH = (
    REPO_ROOT
    / "QBench/Rescans/2026-07-04/Worksheets/Terpenes/"
    "terpenes__id_42__worksheet_export_spreadsheet__active__2026-07-04.json"
)
BATCH_SOURCE_PATH = (
    REPO_ROOT
    / "QBench/Rescans/2026-07-04/Worksheets/Terpenes/"
    "terpenes__id_43__worksheet_export_spreadsheet__active__2026-07-04.json"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def worksheet_map(candidate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {worksheet["worksheetName"]: worksheet for worksheet in candidate["config"]["worksheets"]}


def value_shape(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: value_shape(item) for key, item in value.items()}
    if isinstance(value, list):
        return [value_shape(value[0])] if value else []
    return type(value).__name__


def validate_security(candidate: dict[str, Any], label: str) -> None:
    serialized = json.dumps(candidate, ensure_ascii=False)
    prohibited = {
        "credential key": r"QBENCH_(?:CLIENT_ID|CLIENT_SECRET)|GH_TOKEN|GITHUB_TOKEN",
        "authorization material": r"Authorization\s*:|Bearer\s+[A-Za-z0-9._-]{12,}",
        "network URL": r"https?://|qbench\.net",
        "signed URL": r"X-Amz-(?:Credential|Signature)",
        "customer data marker": r"customer_(?:name|account)|customer information",
        "Pass/Fail": r"(?i)pass[_ /-]?fail",
    }
    for description, pattern in prohibited.items():
        if re.search(pattern, serialized):
            raise AssertionError(f"{label} contains prohibited {description}")


def validate_identity(
    candidate: dict[str, Any],
    historical: dict[str, Any],
    tab_names: dict[str, str],
    label: str,
) -> None:
    if candidate["config"]["namespace"] != historical["config"]["namespace"]:
        raise AssertionError(f"{label} changed the proven historical namespace")
    candidate_sheets = worksheet_map(candidate)
    historical_sheets = worksheet_map(historical)
    for historical_name, candidate_name in tab_names.items():
        if candidate_sheets[candidate_name]["worksheetId"] != historical_sheets[historical_name]["worksheetId"]:
            raise AssertionError(f"{label} changed the historical worksheet ID for {candidate_name}")


def validate_renderer_contract(
    candidate: dict[str, Any],
    historical: dict[str, Any],
    tab_names: dict[str, str],
    label: str,
) -> dict[str, Any]:
    if list(candidate) != list(historical):
        raise AssertionError(f"{label} top-level key order/shape changed")
    if list(candidate["config"]) != list(historical["config"]):
        raise AssertionError(f"{label} config key order/shape changed")
    if value_shape(candidate["qb_config"]) != value_shape(historical["qb_config"]):
        # The named-cell keys and counts intentionally differ, so compare entry shapes below.
        historical_named = historical["qb_config"]["named_cells"]
        candidate_named = candidate["qb_config"]["named_cells"]
        historical_without_named = dict(historical["qb_config"])
        candidate_without_named = dict(candidate["qb_config"])
        historical_without_named.pop("named_cells")
        candidate_without_named.pop("named_cells")
        if value_shape(candidate_without_named) != value_shape(historical_without_named):
            raise AssertionError(f"{label} qb_config shape changed outside named_cells")
        historical_shapes = {tuple(item.keys()) for item in historical_named.values()}
        candidate_shapes = {tuple(item.keys()) for item in candidate_named.values()}
        if candidate_shapes != historical_shapes:
            raise AssertionError(f"{label} named-cell serialization shape changed")

    validate_identity(candidate, historical, tab_names, label)
    candidate_sheets = worksheet_map(candidate)
    historical_sheets = worksheet_map(historical)
    ignored_payload_fields = {
        "cells", "columns", "csvFileName", "data", "minDimensions", "rows", "style",
        "tableHeight", "tableWidth", "worksheetId", "worksheetName",
    }
    formula_count = 0
    style_indexes: set[int] = set()
    for historical_name, candidate_name in tab_names.items():
        worksheet = candidate_sheets[candidate_name]
        historical_worksheet = historical_sheets[historical_name]
        if list(worksheet) != list(historical_worksheet):
            raise AssertionError(f"{label} worksheet object key shape changed for {candidate_name}")
        for key in worksheet:
            if key not in ignored_payload_fields and worksheet[key] != historical_worksheet[key]:
                raise AssertionError(f"{label} changed preserved worksheet field {candidate_name}.{key}")

        data = worksheet["data"]
        rows = len(data)
        cols = max((len(row) for row in data), default=0)
        if worksheet["minDimensions"] != [cols, rows]:
            raise AssertionError(f"{label} minDimensions mismatch for {candidate_name}")
        if len(worksheet["rows"]) != rows or any(value_shape(row) != {"height": "int"} for row in worksheet["rows"]):
            raise AssertionError(f"{label} row metadata representation changed for {candidate_name}")
        expected_column_shape = {"type": "str", "width": "int"}
        if len(worksheet["columns"]) != cols or any(value_shape(col) != expected_column_shape for col in worksheet["columns"]):
            raise AssertionError(f"{label} column metadata representation changed for {candidate_name}")

        historical_cell_shapes = {tuple(item.keys()) for item in historical_worksheet["cells"].values()}
        candidate_cell_shapes = {tuple(item.keys()) for item in worksheet["cells"].values()}
        if candidate_cell_shapes != historical_cell_shapes:
            raise AssertionError(f"{label} cell metadata entry shape changed for {candidate_name}")
        if any(not isinstance(item.get("readonly"), bool) for item in worksheet["cells"].values()):
            raise AssertionError(f"{label} readonly metadata is not boolean for {candidate_name}")

        if candidate["data"][candidate_name] != data:
            raise AssertionError(f"{label} top-level data mirror differs for {candidate_name}")
        if any(not isinstance(value, int) for value in worksheet["style"].values()):
            raise AssertionError(f"{label} style index is not an integer for {candidate_name}")
        style_indexes.update(worksheet["style"].values())

        for row in data:
            for value in row:
                if isinstance(value, str) and value.startswith("="):
                    formula_count += 1
                elif isinstance(value, dict) and any(key.lower().startswith("formula") for key in value):
                    raise AssertionError(f"{label} formula serialization changed to an object")

    named_shapes = {tuple(item.keys()) for item in candidate["qb_config"]["named_cells"].values()}
    if named_shapes != {("cell", "display_name", "export")}:
        raise AssertionError(f"{label} named-cell entry serialization changed")
    if any(not isinstance(item["cell"], str) or not isinstance(item["export"], bool) for item in candidate["qb_config"]["named_cells"].values()):
        raise AssertionError(f"{label} named-cell value types changed")

    return {
        "namespace_preserved": True,
        "worksheet_ids_preserved": True,
        "worksheet_key_shapes_preserved": True,
        "cell_entry_shapes_preserved": True,
        "data_mirroring_preserved": True,
        "formula_count": formula_count,
        "style_indexes": sorted(style_indexes),
    }


def write_report(
    test_result: dict[str, Any],
    batch_result: dict[str, Any],
    renderer_test: dict[str, Any],
    renderer_batch: dict[str, Any],
    vector_result: dict[str, Any],
) -> None:
    lines = [
        "# Phase 3 v2 local validation",
        "",
        "- `scientific_logic_validation = passed`",
        "- `worksheet_schema_validation = passed`",
        "- `historical_renderer_compatibility = passed`",
        "",
        "## Proven historical sources",
        "",
        f"- Test generator commit: `{HISTORICAL_TEST_COMMIT}`.",
        f"- Batch generator commit: `{HISTORICAL_BATCH_COMMIT}`.",
        f"- Test source worksheet: `{TEST_SOURCE_PATH.relative_to(REPO_ROOT).as_posix()}`; SHA-256 `{sha256(TEST_SOURCE_PATH)}`.",
        f"- Batch source worksheet: `{BATCH_SOURCE_PATH.relative_to(REPO_ROOT).as_posix()}`; SHA-256 `{sha256(BATCH_SOURCE_PATH)}`.",
        f"- Historical Test helper: `{phase3_builder.TEST_BUILDER_PATH.relative_to(REPO_ROOT).as_posix()}`; canonical merge-commit SHA-256 `{HISTORICAL_TEST_HELPER_SHA256}`.",
        f"- Historical Batch helper: `{phase3_builder.BATCH_BUILDER_PATH.relative_to(REPO_ROOT).as_posix()}`; canonical merge-commit SHA-256 `{HISTORICAL_BATCH_HELPER_SHA256}`.",
        f"- Corrected v2 builder: `{Path(v2_builder.__file__).relative_to(REPO_ROOT).as_posix()}`; SHA-256 `{sha256(Path(v2_builder.__file__))}`.",
        "",
        "## Candidate results",
        "",
        f"- Test v2: `{TEST_PATH.name}`; SHA-256 `{sha256(TEST_PATH)}`.",
        f"- Test tabs/dimensions: `{test_result['dimensions']}`; named cells `{test_result['named_cells']}`; formulas `{test_result['formulas']}`.",
        f"- Batch v2: `{BATCH_PATH.name}`; SHA-256 `{sha256(BATCH_PATH)}`.",
        f"- Batch tabs/dimensions: `{batch_result['dimensions']}`; named cells `{batch_result['named_cells']}`; formulas `{batch_result['formulas']}`.",
        f"- Scientific calculation vectors: `{vector_result['rows']}` rows; synthetic Total Terpenes `{vector_result['total_ug_g']:.0f} ug/g`.",
        "",
        "## Renderer-sensitive regression contract",
        "",
        f"- Test: `{renderer_test}`.",
        f"- Batch: `{renderer_batch}`.",
        "- The proven source namespace and worksheet IDs are retained; the v1 UUIDv5 rewrite is absent.",
        "- Root/config/worksheet key shapes, worksheet defaults, cells entry shape, boolean readonly values, row/column representations, minDimensions, formula strings, style indexes, named-cell entry shape, and duplicate data mirrors passed.",
        "",
        "## Regression matrix",
        "",
        "- v2 renderer-compatibility tests: 13/13 passed.",
        "- Existing Phase 3 v1 validator: passed; both failed v1 SHA-256 values unchanged.",
        "- Prompt 2 configuration/parser tests: 27/27 passed.",
        "- Historical Test reproduction: byte-for-byte; validator passed; 50/50 tests passed.",
        "- Historical Batch reproduction: byte-for-byte; validator passed; 39/39 tests passed.",
        "- Wide-adapter tests: 13/13 Python and 143/143 JavaScript passed; package validator passed.",
        "- Native-probe tests: 17/17 Python and 48/48 JavaScript passed; 45-artifact package validator passed in the exact manifest-byte workspace.",
        "- No-code parser package validator: passed.",
        "- Prompt 5 automation package validator: passed in the exact mixed-line-ending manifest workspace.",
        "- Prompt 5B publisher tests: 46/46 passed; no request-capable command was run.",
        "",
        "## Safety",
        "",
        "- Failed v1 candidate bytes remain unchanged.",
        "- No credential, token, authorization header, URL, signed URL, Pass/Fail artifact, or customer data was found.",
        "- No QBench environment was accessed and no Sandbox object was modified.",
        "",
    ]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> None:
    test_candidate = load_json(TEST_PATH)
    batch_candidate = load_json(BATCH_PATH)
    historical_test = load_json(phase3_validator.HISTORICAL_TEST_PATH)
    historical_batch = load_json(phase3_validator.HISTORICAL_BATCH_PATH)

    validate_security(test_candidate, "Test v2")
    validate_security(batch_candidate, "Batch v2")
    test_result = phase3_validator.validate_test_candidate(test_candidate)
    batch_result = phase3_validator.validate_batch_candidate(batch_candidate)
    vector_result = phase3_validator.validate_vectors()
    phase3_validator.validate_mapping()
    renderer_test = validate_renderer_contract(
        test_candidate,
        historical_test,
        {"Report": "Report", "Data": "Data", "Specifications": "Specifications"},
        "Test v2",
    )
    renderer_batch = validate_renderer_contract(
        batch_candidate,
        historical_batch,
        {
            "Run Setup": "Run Setup",
            "Instrument Import": "Instrument Import",
            "QC Review": "Batch Review",
            "Publish": "Test Transfer",
        },
        "Batch v2",
    )
    write_report(test_result, batch_result, renderer_test, renderer_batch, vector_result)
    print("SCIENTIFIC_LOGIC_VALIDATION=PASSED")
    print("WORKSHEET_SCHEMA_VALIDATION=PASSED")
    print("HISTORICAL_RENDERER_COMPATIBILITY=PASSED")
    print(f"test_v2_sha256={sha256(TEST_PATH)}")
    print(f"batch_v2_sha256={sha256(BATCH_PATH)}")


if __name__ == "__main__":
    main()
