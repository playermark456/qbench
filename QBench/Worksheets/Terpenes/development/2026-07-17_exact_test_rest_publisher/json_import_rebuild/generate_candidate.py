from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "config" / "field_mapping_scalar_candidate.csv"
OUTPUT_PATH = Path(__file__).resolve().parent / (
    "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE.json"
)

NAMESPACE = "fba1ba1a-6b6b-4101-be22-b4ef4935f65c"
WORKSHEET_ID = "148d340f-a118-495e-ac94-e9df7ab115a2"
ROWS = 40
COLS = 26


def column_name(index: int) -> str:
    value = index + 1
    result = ""
    while value:
        value, remainder = divmod(value - 1, 26)
        result = chr(65 + remainder) + result
    return result


with MAPPING_PATH.open(newline="", encoding="utf-8") as handle:
    mapping = list(csv.DictReader(handle))

if len(mapping) != 43:
    raise SystemExit(f"expected 43 mapping rows, found {len(mapping)}")

named_cells = {}
target_addresses = set()
for row in mapping:
    system_name = row["destination_named_cell"]
    address = row["destination_cell"]
    named_cells[system_name] = {
        "cell": address,
        "display_name": row["source_header"],
        "export": True,
    }
    target_addresses.add(address.split("!", 1)[1])

blank_grid = [["" for _ in range(COLS)] for _ in range(ROWS)]
cells = {}
for row_number in range(1, ROWS + 1):
    for column_index in range(COLS):
        address = f"{column_name(column_index)}{row_number}"
        cells[address] = {
            "readonly": address not in target_addresses,
            "type": "text",
            "width": 130,
            "x": column_index,
        }

worksheet = {
    "allowComments": False,
    "allowDeleteColumn": True,
    "allowDeleteRow": True,
    "allowInsertColumn": True,
    "allowInsertRow": True,
    "allowRenameColumn": False,
    "cache": {},
    "cells": cells,
    "columnDrag": True,
    "columnResize": True,
    "columnSorting": False,
    "columns": [{"type": "text", "width": 130} for _ in range(COLS)],
    "comments": {},
    "csvFileName": "worksheet_data",
    "filters": False,
    "freezeColumnControl": True,
    "freezeColumns": [],
    "freezeRowControl": True,
    "freezeRows": [],
    "mergeCells": {},
    "meta": {},
    "minDimensions": [1, 1],
    "resize": "vertical",
    "rowDrag": True,
    "rowResize": True,
    "rows": [{"height": 28} for _ in range(ROWS)],
    "tableHeight": 350,
    "tableOverflow": True,
    "tableWidth": 1588,
    "worksheetId": WORKSHEET_ID,
    "worksheetName": "Data",
    "data": blank_grid,
    "style": {},
}

candidate = {
    "config": {
        "allowDeleteWorksheet": True,
        "allowMoveWorksheet": True,
        "allowRenameWorksheet": True,
        "application": "QBench",
        "autoCasting": False,
        "bar": True,
        "entityId": "SPREADSHEET_EDITOR",
        "namespace": NAMESPACE,
        "plugins": {"conditionalFormatting": {"rules": []}},
        "qbConfigs": {
            "generalSpreadsheetSettings": {
                "enableSpreadsheetCustomization": False,
                "allowTabEditing": True,
                "showToolbar": True,
            },
            "reportSpreadsheetSettings": {"enableReportBorders": False},
        },
        "tabs": {
            "allowCreate": True,
            "allowChangePosition": True,
            "animation": True,
            "position": "top",
            "maxWidth": "-50px",
        },
        "style": None,
        "worksheets": [worksheet],
    },
    "qb_config": {
        "named_cells": named_cells,
        "kvstore_config": {},
        "portal_export_range": "",
        "report_export_range": "",
    },
    "data": {"Data": [row[:] for row in blank_grid]},
}

OUTPUT_PATH.write_text(
    json.dumps(candidate, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
print(OUTPUT_PATH)
