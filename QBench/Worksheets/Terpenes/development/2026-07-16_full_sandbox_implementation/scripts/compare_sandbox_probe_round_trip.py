"""Compare the saved old-Sandbox Probe export with the imported candidate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


PACKAGE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATE = (
    PACKAGE_DIR
    / "dist/qbench_runtime_probe_batch_ws_candidate__ait_sandbox_runtime.json"
)
DEFAULT_EXPORT = (
    PACKAGE_DIR
    / "round_trip/2026-07-16_ait-sandbox_ws_id_62_version_1_draft_export_spreadsheet.json"
)
EXPECTED_FORMULAS = {
    "B4": "=ISNUMBER(B3)",
    "B5": "=COUNT(B3)",
    "B6": '="UNCHANGED"',
    "B9": "=COUNT(B8:D8)",
    "B13": "=COUNT(B11:C12)",
    "AF16": '="AF_UNCHANGED"',
    "AG16": '="AG_UNCHANGED"',
    "A17": "=COUNT(A16:AE16)",
    "AH17": "=COUNT(AH16:BE16)",
}
EXPECTED_EVALUATED_VALUES = {
    "B4": "false",
    "B5": "0",
    "B6": "UNCHANGED",
    "B9": "0",
    "B13": "0",
    "AF16": "AF_UNCHANGED",
    "AG16": "AG_UNCHANGED",
    "A17": "0",
    "AH17": "0",
}
RUNTIME_CONFIG_KEYS = {
    "namespace",
    "allowDeleteWorksheet",
    "allowMoveWorksheet",
    "allowRenameWorksheet",
    "style",
}
RUNTIME_WORKSHEET_KEYS = {
    "tableWidth",
    "tableHeight",
    "minDimensions",
    "style",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def cell_indexes(address: str) -> tuple[int, int]:
    letters = "".join(character for character in address if character.isalpha())
    row = int("".join(character for character in address if character.isdigit()))
    column = 0
    for character in letters:
        column = column * 26 + ord(character.upper()) - 64
    return row - 1, column - 1


def cell_value(data: list[list[Any]], address: str) -> Any:
    row, column = cell_indexes(address)
    return data[row][column]


def normalized_config(config: dict[str, Any]) -> dict[str, Any]:
    normalized = copy.deepcopy(config)
    for key in RUNTIME_CONFIG_KEYS:
        normalized.pop(key, None)
    for worksheet in normalized.get("worksheets", []):
        for key in RUNTIME_WORKSHEET_KEYS:
            worksheet.pop(key, None)
    return normalized


def matrix_differences(
    candidate: list[list[Any]], exported: list[list[Any]]
) -> dict[str, tuple[Any, Any]]:
    differences: dict[str, tuple[Any, Any]] = {}
    row_count = min(len(candidate), len(exported))
    for row_index in range(row_count):
        column_count = min(len(candidate[row_index]), len(exported[row_index]))
        for column_index in range(column_count):
            before = candidate[row_index][column_index]
            after = exported[row_index][column_index]
            if before != after:
                number = column_index + 1
                letters = ""
                while number:
                    number, remainder = divmod(number - 1, 26)
                    letters = chr(65 + remainder) + letters
                differences[f"{letters}{row_index + 1}"] = (before, after)
    return differences


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, default=DEFAULT_CANDIDATE)
    parser.add_argument("--export", dest="export_path", type=Path, default=DEFAULT_EXPORT)
    args = parser.parse_args()

    candidate = load_json(args.candidate)
    exported = load_json(args.export_path)
    errors: list[str] = []

    if list(candidate) != list(exported):
        errors.append("top-level keys changed")

    candidate_worksheets = candidate.get("config", {}).get("worksheets", [])
    exported_worksheets = exported.get("config", {}).get("worksheets", [])
    if len(candidate_worksheets) != 1 or len(exported_worksheets) != 1:
        errors.append("candidate and export must each contain exactly one worksheet")
        candidate_ws: dict[str, Any] = {}
        exported_ws: dict[str, Any] = {}
    else:
        candidate_ws = candidate_worksheets[0]
        exported_ws = exported_worksheets[0]

    exported_matrix = exported_ws.get("data", [])
    if exported_ws.get("worksheetName") != "Probe":
        errors.append("saved export worksheet is not named Probe")
    if len(exported_matrix) != 17 or any(len(row) != 57 for row in exported_matrix):
        errors.append("saved export is not a 17-row by 57-column matrix")

    if normalized_config(candidate.get("config", {})) != normalized_config(
        exported.get("config", {})
    ):
        errors.append("non-runtime worksheet configuration changed")
    if candidate.get("qb_config") != exported.get("qb_config"):
        errors.append("named-cell configuration changed")
    if candidate_ws.get("data") != exported_ws.get("data"):
        errors.append("worksheet data or formulas changed")
    if candidate_ws.get("cells") != exported_ws.get("cells"):
        errors.append("cell writable/read-only configuration changed")

    formula_cells = {
        address: cell_value(exported_matrix, address)
        for address in EXPECTED_FORMULAS
        if exported_matrix
    }
    if formula_cells != EXPECTED_FORMULAS:
        errors.append("one or more required formulas changed")
    formula_count = sum(
        1
        for row in exported_matrix
        for value in row
        if isinstance(value, str) and value.startswith("=")
    )
    if formula_count != 9:
        errors.append(f"saved export contains {formula_count} formulas instead of 9")

    candidate_cache = candidate.get("data", {}).get("Probe", [])
    exported_cache = exported.get("data", {}).get("Probe", [])
    cache_differences = matrix_differences(candidate_cache, exported_cache)
    expected_cache_differences = {
        address: (EXPECTED_FORMULAS[address], EXPECTED_EVALUATED_VALUES[address])
        for address in EXPECTED_FORMULAS
    }
    if cache_differences != expected_cache_differences:
        errors.append("top-level evaluated-data differences were not the expected nine formulas")

    named_cells = exported.get("qb_config", {}).get("named_cells", {})
    if len(named_cells) != 15:
        errors.append("saved export does not contain exactly 15 named cells")

    serialized_export = json.dumps(exported)
    for forbidden in ("STD 1", "System Suitability", "Sheet1!B96", "pass_fail"):
        if forbidden in serialized_export:
            errors.append(f"forbidden legacy value found: {forbidden}")

    candidate_config = candidate.get("config", {})
    exported_config = exported.get("config", {})
    candidate_ws_config = candidate_ws
    exported_ws_config = exported_ws
    runtime_normalizations = {
        "namespace": {
            "candidate": candidate_config.get("namespace"),
            "export": exported_config.get("namespace"),
        },
        "worksheet_management": {
            key: {
                "candidate": candidate_config.get(key),
                "export": exported_config.get(key),
            }
            for key in (
                "allowDeleteWorksheet",
                "allowMoveWorksheet",
                "allowRenameWorksheet",
            )
        },
        "table_viewport": {
            key: {
                "candidate": candidate_ws_config.get(key),
                "export": exported_ws_config.get(key),
            }
            for key in ("tableWidth", "tableHeight", "minDimensions")
        },
        "empty_style_objects_added": {
            "config": "style" not in candidate_config and not exported_config.get("style"),
            "worksheet": "style" not in candidate_ws_config
            and not exported_ws_config.get("style"),
        },
        "top_level_formula_cache_evaluated": sorted(cache_differences),
    }

    result = {
        "status": "ok" if not errors else "failed",
        "semantic_round_trip_match": not errors,
        "candidate_sha256": sha256(args.candidate),
        "saved_export_sha256": sha256(args.export_path),
        "worksheet": exported_ws.get("worksheetName"),
        "rows": len(exported_matrix),
        "columns": len(exported_matrix[0]) if exported_matrix else 0,
        "named_cells": len(named_cells),
        "formulas": formula_count,
        "runtime_normalizations": runtime_normalizations,
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
