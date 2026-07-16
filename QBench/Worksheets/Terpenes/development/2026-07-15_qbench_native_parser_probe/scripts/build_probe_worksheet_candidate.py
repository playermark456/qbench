"""Build the deterministic nonproduction Prompt 4.6 probe worksheet."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[6]
PACKAGE_DIR = Path(__file__).resolve().parents[1]
SOURCE_EXPORT = REPO_ROOT / "QBench/Rescans/2026-07-04/Worksheets/Terpenes/terpenes__id_43__worksheet_export_spreadsheet__active__2026-07-04.json"
OUTPUT_PATH = PACKAGE_DIR / "dist/qbench_runtime_probe_batch_ws_candidate.json"
PROBE_WORKSHEET_ID = "8e7e1a62-04fa-4f1d-9fd7-461000000001"
PROBE_NAME = "Probe"
ROW_COUNT = 17
COLUMN_COUNT = 57


NAMED_TARGETS = {
    "probe_text": "Probe!B2",
    "probe_number": "Probe!B3",
    "probe_isnumber": "Probe!B4",
    "probe_count": "Probe!B5",
    "probe_sentinel": "Probe!B6",
    "probe_small_range": "Probe!B8:D8",
    "probe_small_range_count": "Probe!B9",
    "probe_small_matrix": "Probe!B11:C12",
    "probe_small_matrix_count": "Probe!B13",
    "probe_block_a_ae": "Probe!A16:AE16",
    "probe_gap_af": "Probe!AF16",
    "probe_gap_ag": "Probe!AG16",
    "probe_block_ah_be": "Probe!AH16:BE16",
    "probe_block_a_ae_count": "Probe!A17",
    "probe_block_ah_be_count": "Probe!AH17",
}


FORMULAS = {
    "B4": "=ISNUMBER(B3)",
    "B5": "=COUNT(B3)",
    "B6": '=\"UNCHANGED\"',
    "B9": "=COUNT(B8:D8)",
    "B13": "=COUNT(B11:C12)",
    "AF16": '=\"AF_UNCHANGED\"',
    "AG16": '=\"AG_UNCHANGED\"',
    "A17": "=COUNT(A16:AE16)",
    "AH17": "=COUNT(AH16:BE16)",
}


def column_letter(index: int) -> str:
    value = index
    output = ""
    while value:
        value, remainder = divmod(value - 1, 26)
        output = chr(65 + remainder) + output
    return output


def cell_ref(row: int, column: int) -> str:
    return f"{column_letter(column)}{row}"


def parse_cell(cell: str) -> tuple[int, int]:
    letters = "".join(character for character in cell if character.isalpha())
    row = int("".join(character for character in cell if character.isdigit()))
    column = 0
    for character in letters:
        column = column * 26 + ord(character.upper()) - 64
    return row, column


def range_cells(start: str, end: str) -> set[str]:
    start_row, start_column = parse_cell(start)
    end_row, end_column = parse_cell(end)
    return {
        cell_ref(row, column)
        for row in range(start_row, end_row + 1)
        for column in range(start_column, end_column + 1)
    }


def writable_cells() -> set[str]:
    cells = {"B2", "B3"}
    cells.update(range_cells("B8", "D8"))
    cells.update(range_cells("B11", "C12"))
    cells.update(range_cells("A16", "AE16"))
    cells.update(range_cells("AH16", "BE16"))
    return cells


def build_data() -> list[list[Any]]:
    data: list[list[Any]] = [[""] * COLUMN_COUNT for _ in range(ROW_COUNT)]
    labels = {
        "A1": "Prompt 4.6 disposable QBench runtime probe",
        "A2": "Text input",
        "A3": "Number input",
        "A4": "Number type check",
        "A5": "Number count",
        "A6": "Scalar sentinel",
        "A8": "Small range",
        "A9": "Small range numeric count",
        "A11": "Small matrix",
        "A13": "Small matrix numeric count",
    }
    for address, value in {**labels, **FORMULAS}.items():
        row, column = parse_cell(address)
        data[row - 1][column - 1] = value
    return data


def build_named_cells() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "cell": target,
            "display_name": name.replace("_", " ").title(),
            "export": True,
        }
        for name, target in NAMED_TARGETS.items()
    }


def build_cells() -> dict[str, dict[str, Any]]:
    writable = writable_cells()
    cells: dict[str, dict[str, Any]] = {}
    for row in range(1, ROW_COUNT + 1):
        for column in range(1, COLUMN_COUNT + 1):
            address = cell_ref(row, column)
            cells[address] = {
                "readonly": address not in writable,
                "type": "text",
                "width": 130 if column <= 33 else 110,
                "x": column - 1,
            }
    return cells


def build_candidate() -> dict[str, Any]:
    source = json.loads(SOURCE_EXPORT.read_text(encoding="utf-8"))
    candidate = copy.deepcopy(source)
    candidate["qb_config"]["kvstore_config"] = {}
    candidate["qb_config"]["named_cells"] = build_named_cells()
    candidate["qb_config"]["portal_export_range"] = ""
    candidate["qb_config"]["report_export_range"] = ""
    plugins = candidate["config"].get("plugins", {})
    if isinstance(plugins.get("conditionalFormatting"), dict):
        plugins["conditionalFormatting"]["rules"] = []

    worksheet = copy.deepcopy(source["config"]["worksheets"][0])
    data = build_data()
    worksheet.update(
        {
            "worksheetName": PROBE_NAME,
            "worksheetId": PROBE_WORKSHEET_ID,
            "cache": {},
            "comments": {},
            "mergeCells": {},
            "meta": {},
            "filters": False,
            "freezeColumns": [],
            "freezeRows": [],
            "csvFileName": "",
            "data": data,
            "columns": [{"type": "text", "width": 130 if column <= 33 else 110} for column in range(1, COLUMN_COUNT + 1)],
            "rows": [{"height": 28} for _row in range(ROW_COUNT)],
            "minDimensions": [COLUMN_COUNT, ROW_COUNT],
            "style": {},
            "cells": build_cells(),
            "tableWidth": 2200,
            "tableHeight": 720,
        }
    )
    candidate["config"]["allowDeleteWorksheet"] = False
    candidate["config"]["allowMoveWorksheet"] = False
    candidate["config"]["allowRenameWorksheet"] = False
    candidate["config"]["worksheets"] = [worksheet]
    candidate["data"] = {PROBE_NAME: data}
    return candidate


def render_candidate() -> str:
    return json.dumps(build_candidate(), ensure_ascii=False, indent=2) + "\n"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_candidate(), encoding="utf-8", newline="\n")
    print(json.dumps({"status": "ok", "output": str(OUTPUT_PATH.relative_to(REPO_ROOT)).replace("\\", "/"), "worksheet_id": PROBE_WORKSHEET_ID, "named_cell_count": len(NAMED_TARGETS)}, indent=2))


if __name__ == "__main__":
    main()
