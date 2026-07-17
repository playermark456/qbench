#!/usr/bin/env python3
"""Build the corrected legacy JSON import from the working native export."""
from __future__ import annotations

import copy
import csv
import json
import re
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = (
    HERE
    / "source"
    / "2026-07-17_SBX_ONLY_TERPENES_NATIVE_SCALAR_43_FIELD_BASE_working_native_export_spreadsheet.json"
)
MAPPING = ROOT / "config" / "field_mapping_scalar_candidate.csv"
OUTPUT = HERE / "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE.json"
ROWS = 40
COLS = 26
CANDIDATE_RENDERER_UUID = "051174c5-a7da-4b6d-afc5-0c2addc1a900"
UUID_PATTERN = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
    re.IGNORECASE,
)


def split_address(address: str) -> tuple[int, int]:
    sheet, local = address.split("!", 1)
    if sheet != "Data":
        raise ValueError(f"expected Data-qualified address, found {address}")
    letters = "".join(character for character in local if character.isalpha())
    digits = "".join(character for character in local if character.isdigit())
    column = 0
    for character in letters:
        column = column * 26 + ord(character.upper()) - 64
    return int(digits) - 1, column - 1


def load_mapping() -> list[dict[str, str]]:
    with MAPPING.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 43:
        raise ValueError(f"expected 43 mapping rows, found {len(rows)}")
    return rows


def replace_source_renderer_uuid(item: Any, source_uuid: str) -> Any:
    if isinstance(item, dict):
        return {
            key: replace_source_renderer_uuid(value, source_uuid)
            for key, value in item.items()
        }
    if isinstance(item, list):
        return [replace_source_renderer_uuid(value, source_uuid) for value in item]
    if isinstance(item, str):
        return item.replace(source_uuid, CANDIDATE_RENDERER_UUID)
    return item


def build_candidate() -> dict[str, Any]:
    source = json.loads(SOURCE.read_text(encoding="utf-8-sig"))
    if set(source) != {"table_config", "qb_config"}:
        raise ValueError("working native export is not the exact legacy envelope")

    table = source.get("table_config", {})
    grid = table.get("cell_settings", [])
    if len(grid) != ROWS or any(len(row) != COLS for row in grid):
        raise ValueError("working native export is not an exact 40x26 matrix")
    if len(table.get("default_settings", {}).get("rowHeights", [])) != ROWS:
        raise ValueError("working native export does not have 40 native row settings")
    if len(table.get("default_settings", {}).get("colWidths", [])) != COLS:
        raise ValueError("working native export does not have 26 native column settings")

    source_named = source.get("qb_config", {}).get("named_cells", {})
    if set(source_named) != {"sdf"} or source_named["sdf"].get("cell") != "A1":
        raise ValueError("working native export does not contain only sdf / A1")

    source_uuids = set(UUID_PATTERN.findall(json.dumps(source)))
    if len(source_uuids) != 1:
        raise ValueError(
            f"expected exactly one source renderer UUID, found {len(source_uuids)}"
        )
    source_uuid = next(iter(source_uuids))
    candidate = replace_source_renderer_uuid(copy.deepcopy(source), source_uuid)
    grid = candidate["table_config"]["cell_settings"]
    mapping = load_mapping()

    anchors: dict[tuple[int, int], str] = {
        (0, 0): "Terpenes JSON scalar 43-field base",
        (11, 0): "Preparation and calculation inputs",
        (21, 0): "Controlled disposition",
        (27, 0): "Source and audit metadata",
        (39, 0): "End of worksheet",
    }
    for offset, row in enumerate(mapping[:23], start=3):
        anchors[(0, offset)] = row["source_header"]
    for (row_index, column_index), value in anchors.items():
        grid[row_index][column_index]["value"] = value

    named_cells: dict[str, dict[str, Any]] = {}
    for row in mapping:
        address = row["destination_cell"]
        row_index, column_index = split_address(address)
        cell = grid[row_index][column_index]
        cell["value"] = ""
        metadata = cell.get("meta_data")
        if not isinstance(metadata, dict):
            raise ValueError(f"native metadata missing at {address}")
        lowered_keys = {str(key).lower() for key in metadata}
        if "formula" in lowered_keys or "readonly" in lowered_keys:
            raise ValueError(f"native destination metadata is not writable at {address}")
        named_cells[row["destination_named_cell"]] = {
            "cell": address,
            "display_name": row["source_header"],
            "export": True,
        }

    candidate["qb_config"]["named_cells"] = named_cells
    return candidate


def main() -> None:
    candidate = build_candidate()
    OUTPUT.write_text(
        json.dumps(candidate, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()
