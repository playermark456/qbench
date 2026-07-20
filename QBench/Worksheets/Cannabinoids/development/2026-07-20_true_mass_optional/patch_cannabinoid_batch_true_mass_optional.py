#!/usr/bin/env python3
"""Add optional True Mass per Unit column AH to a QBench Cannabinoid Potency Batch worksheet export."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HEADER = "True Mass per Unit"
FIELD = "true_mass_per_unit"
FIRST_TEST_ROW = 62
COLUMN_INDEX = 33  # AH, zero-based


def ensure_cell(data: list[list[object]], row: int, col: int, value: object) -> None:
    while len(data) <= row:
        data.append([])
    while len(data[row]) <= col:
        data[row].append(None)
    data[row][col] = value


def formula(test_index: int) -> str:
    ref = f'${{tests[{test_index}].additional_fields[\'{FIELD}\'].value}}'
    return f'=IF(OR("{ref}"="",LOWER("{ref}")="none"),"",IFERROR(VALUE("{ref}"),""))'


def patch(doc: dict) -> dict:
    out = copy.deepcopy(doc)
    worksheets = out.get("config", {}).get("worksheets", [])
    if len(worksheets) != 1:
        raise ValueError("Expected exactly one batch worksheet")
    ws = worksheets[0]
    data = ws["data"]

    ensure_cell(data, 0, COLUMN_INDEX, HEADER)

    # Preserve blank non-Test rows. Populate Test rows using the row-to-tests[] mapping
    # already used by this batch worksheet. The first test row is row 62.
    test_index = 0
    for excel_row in range(FIRST_TEST_ROW, len(data) + 1):
        row_index = excel_row - 1
        first_cell = data[row_index][0] if data[row_index] else None
        if isinstance(first_cell, str) and "${tests[" in first_cell:
            ensure_cell(data, row_index, COLUMN_INDEX, formula(test_index))
            test_index += 1
        else:
            ensure_cell(data, row_index, COLUMN_INDEX, "")

    # Add matching cell configuration without making the field required or read-only.
    cells = ws.setdefault("cells", {})
    for excel_row in range(1, len(data) + 1):
        address = f"AH{excel_row}"
        existing = copy.deepcopy(cells.get(f"AG{excel_row}", {"readonly": False, "type": "text", "width": 137}))
        existing["readonly"] = False
        existing["type"] = "text"
        existing["width"] = 137
        cells[address] = existing

    out.setdefault("data", {})[ws["worksheetName"]] = copy.deepcopy(data)
    return out


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: patch_cannabinoid_batch_true_mass_optional.py input.json output.json")
    source = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8-sig"))
    result = patch(source)
    Path(sys.argv[2]).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
