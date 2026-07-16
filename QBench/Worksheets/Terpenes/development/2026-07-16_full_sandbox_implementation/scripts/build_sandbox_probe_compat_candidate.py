"""Overlay the Prompt 4.6 probe on a native QBench worksheet export."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[6]
PACKAGE_DIR = Path(__file__).resolve().parents[1]
SOURCE_PATH = REPO_ROOT / (
    "QBench/Rescans/2026-07-04/Worksheets/Terpenes/"
    "terpenes__id_43__worksheet_export_spreadsheet__active__2026-07-04.json"
)
OUTPUT_PATH = PACKAGE_DIR / "sandbox_probe_worksheet_compatibility_candidate.json"
SHEET = "Sheet1"
COLUMN_COUNT = 57

NAMED_TARGETS = {
    "probe_text": "Sheet1!B96",
    "probe_number": "Sheet1!C96",
    "probe_isnumber": "Sheet1!D96",
    "probe_count": "Sheet1!E96",
    "probe_sentinel": "Sheet1!F96",
    "probe_small_range": "Sheet1!B94:D94",
    "probe_small_range_count": "Sheet1!E94",
    "probe_small_matrix": "Sheet1!B92:C93",
    "probe_small_matrix_count": "Sheet1!E93",
    "probe_block_a_ae": "Sheet1!A89:AE89",
    "probe_gap_af": "Sheet1!AF89",
    "probe_gap_ag": "Sheet1!AG89",
    "probe_block_ah_be": "Sheet1!AH89:BE89",
    "probe_block_a_ae_count": "Sheet1!A90",
    "probe_block_ah_be_count": "Sheet1!AH90",
}

FORMULAS = {
    "D96": "=ISNUMBER(C96)",
    "E96": "=COUNT(C96)",
    "F96": '="UNCHANGED"',
    "E94": "=COUNT(B94:D94)",
    "E93": "=COUNT(B92:C93)",
    "AF89": '="AF_UNCHANGED"',
    "AG89": '="AG_UNCHANGED"',
    "A90": "=COUNT(A89:AE89)",
    "AH90": "=COUNT(AH89:BE89)",
}


def column_letter(index: int) -> str:
    value = index
    result = ""
    while value:
        value, remainder = divmod(value - 1, 26)
        result = chr(65 + remainder) + result
    return result


def parse_cell(address: str) -> tuple[int, int]:
    letters = "".join(character for character in address if character.isalpha())
    row = int("".join(character for character in address if character.isdigit()))
    column = 0
    for character in letters:
        column = column * 26 + ord(character.upper()) - 64
    return row, column


def set_value(data: list[list[Any]], address: str, value: Any) -> None:
    row, column = parse_cell(address)
    data[row - 1][column - 1] = value


def build_named_cells() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "cell": target,
            "display_name": name.replace("_", " ").title(),
            "export": True,
        }
        for name, target in NAMED_TARGETS.items()
    }


def build_candidate() -> dict[str, Any]:
    candidate = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    worksheet = candidate["config"]["worksheets"][0]
    if worksheet["worksheetName"] != SHEET:
        raise ValueError(f"Unexpected source worksheet: {worksheet['worksheetName']}")

    data = copy.deepcopy(worksheet["data"])
    for row in data:
        row.extend([""] * (COLUMN_COUNT - len(row)))
    for address, formula in FORMULAS.items():
        set_value(data, address, formula)

    columns = copy.deepcopy(worksheet["columns"])
    while len(columns) < COLUMN_COUNT:
        columns.append({"type": "text", "width": 110})

    cells = copy.deepcopy(worksheet["cells"])
    for row in range(89, 97):
        for column in range(1, COLUMN_COUNT + 1):
            address = f"{column_letter(column)}{row}"
            cells[address] = {
                "colElement": {},
                "element": {},
                "readonly": address in FORMULAS,
                "type": "text",
                "width": 110,
                "x": column - 1,
            }

    worksheet["data"] = data
    worksheet["columns"] = columns
    worksheet["cells"] = cells
    worksheet["tableWidth"] = max(int(worksheet.get("tableWidth", 0)), 2200)
    candidate["data"] = {SHEET: copy.deepcopy(data)}
    candidate["qb_config"]["kvstore_config"] = {}
    candidate["qb_config"]["named_cells"] = build_named_cells()
    candidate["qb_config"]["portal_export_range"] = ""
    candidate["qb_config"]["report_export_range"] = ""
    return candidate


def main() -> None:
    OUTPUT_PATH.write_text(
        json.dumps(build_candidate(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": "ok",
                "output": str(OUTPUT_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
                "source_schema_preserved": True,
                "worksheet_name": SHEET,
                "named_cell_count": len(NAMED_TARGETS),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
