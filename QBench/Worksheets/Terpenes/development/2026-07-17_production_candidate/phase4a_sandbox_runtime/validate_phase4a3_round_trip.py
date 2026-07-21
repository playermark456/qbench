#!/usr/bin/env python3
"""Validate an old-Sandbox worksheet Export Spreadsheet round trip.

The embedded worksheet ``data`` arrays are authoritative for formulas. QBench's
duplicate top-level ``data`` object is an evaluated display cache after save.
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


class RoundTripMismatch(AssertionError):
    """A non-normalizable worksheet round-trip difference."""


def _fail(message: str) -> None:
    raise RoundTripMismatch(message)


def _dimensions(grid: list[list[Any]]) -> tuple[int, int]:
    rows = len(grid)
    columns = max((len(row) for row in grid), default=0)
    return rows, columns


def _is_formula(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("=")


def _assert_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        _fail(f"{label} differs")


def compare_round_trip(candidate: dict[str, Any], exported: dict[str, Any]) -> dict[str, Any]:
    """Compare a candidate with a saved QBench export.

    Allowed normalization is limited to the generated namespace, editor
    minimum/viewport fields, and evaluated top-level formula-cache cells.
    """

    _assert_equal(list(exported), list(candidate), "top-level key order")

    candidate_config = deepcopy(candidate["config"])
    exported_config = deepcopy(exported["config"])
    candidate_worksheets = candidate_config.pop("worksheets")
    exported_worksheets = exported_config.pop("worksheets")
    candidate_config.pop("namespace", None)
    exported_config.pop("namespace", None)
    _assert_equal(exported_config, candidate_config, "config outside allowed normalization")

    if len(exported_worksheets) != len(candidate_worksheets):
        _fail("worksheet count differs")

    candidate_names = [worksheet["worksheetName"] for worksheet in candidate_worksheets]
    exported_names = [worksheet["worksheetName"] for worksheet in exported_worksheets]
    _assert_equal(exported_names, candidate_names, "worksheet tab names or order")
    _assert_equal(list(exported["data"]), list(candidate["data"]), "top-level data tab order")
    _assert_equal(exported["qb_config"], candidate["qb_config"], "named cells or QBench config")

    normalized_min_dimensions = 0
    normalized_viewports = 0
    embedded_formula_count = 0
    top_level_formula_cache_count = 0
    nonformula_top_level_count = 0

    for candidate_ws, exported_ws in zip(candidate_worksheets, exported_worksheets):
        name = candidate_ws["worksheetName"]
        candidate_grid = candidate_ws["data"]
        exported_grid = exported_ws["data"]

        _assert_equal(exported_grid, candidate_grid, f"{name} embedded worksheet data")
        _assert_equal(_dimensions(exported_grid), _dimensions(candidate_grid), f"{name} embedded dimensions")

        candidate_ws_remainder = deepcopy(candidate_ws)
        exported_ws_remainder = deepcopy(exported_ws)
        for key in ("data", "minDimensions", "tableWidth", "tableHeight"):
            candidate_ws_remainder.pop(key, None)
            exported_ws_remainder.pop(key, None)
        _assert_equal(
            exported_ws_remainder,
            candidate_ws_remainder,
            f"{name} rows, columns, cells, styles, metadata, protection, or number formats",
        )

        expected_minimum = candidate_ws["minDimensions"]
        actual_minimum = exported_ws["minDimensions"]
        if actual_minimum != expected_minimum:
            if actual_minimum != [1, 1]:
                _fail(f"{name} minDimensions changed to an unsupported value")
            normalized_min_dimensions += 1

        for key in ("tableWidth", "tableHeight"):
            expected_viewport = candidate_ws[key]
            actual_viewport = exported_ws[key]
            if actual_viewport != expected_viewport:
                if isinstance(actual_viewport, bool) or not isinstance(actual_viewport, (int, float)) or actual_viewport <= 0:
                    _fail(f"{name} {key} is not a valid normalized editor viewport")
                normalized_viewports += 1

        candidate_top = candidate["data"][name]
        exported_top = exported["data"][name]
        _assert_equal(_dimensions(exported_top), _dimensions(candidate_top), f"{name} top-level data dimensions")
        _assert_equal(_dimensions(candidate_top), _dimensions(candidate_grid), f"{name} candidate data mirrors")

        for row_index, (candidate_row, exported_row, embedded_row) in enumerate(
            zip(candidate_top, exported_top, candidate_grid)
        ):
            if len(exported_row) != len(candidate_row):
                _fail(f"{name} top-level row {row_index + 1} width differs")
            for column_index, (candidate_value, exported_value, embedded_value) in enumerate(
                zip(candidate_row, exported_row, embedded_row)
            ):
                if _is_formula(embedded_value):
                    embedded_formula_count += 1
                    if candidate_value != embedded_value:
                        _fail(f"{name} candidate formula mirror differs at row {row_index + 1}, column {column_index + 1}")
                    if exported_value != candidate_value:
                        if isinstance(exported_value, (dict, list)):
                            _fail(f"{name} formula cache is not a scalar at row {row_index + 1}, column {column_index + 1}")
                        top_level_formula_cache_count += 1
                else:
                    nonformula_top_level_count += 1
                    if exported_value != candidate_value:
                        _fail(f"{name} non-formula top-level value differs at row {row_index + 1}, column {column_index + 1}")

    return {
        "classification": "passed_with_expected_qbench_normalization",
        "authoritative_formula_representation": "config.worksheets[*].data",
        "top_level_data_representation": "qbench_evaluated_display_cache",
        "normalized_min_dimensions": normalized_min_dimensions,
        "normalized_viewport_fields": normalized_viewports,
        "embedded_formula_count": embedded_formula_count,
        "top_level_formula_cache_values": top_level_formula_cache_count,
        "nonformula_top_level_values_compared": nonformula_top_level_count,
        "worksheet_count": len(candidate_worksheets),
        "named_definition_count": len(candidate["qb_config"]["named_cells"]),
    }


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def main() -> None:
    runtime_dir = Path(__file__).resolve().parent
    candidate_dir = runtime_dir.parent / "production_candidates"
    audit_dir = runtime_dir.parent / "audit"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--candidate",
        type=Path,
        default=candidate_dir / "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v2.json",
    )
    parser.add_argument(
        "--export",
        type=Path,
        default=audit_dir / "phase4a2_test_v2_saved_reopened_export_spreadsheet.json",
    )
    args = parser.parse_args()
    result = compare_round_trip(load_json(args.candidate), load_json(args.export))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
