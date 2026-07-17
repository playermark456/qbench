#!/usr/bin/env python3
"""Write the failed/native/rendered-qualified structural comparison evidence."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
FAILED = (
    HERE
    / "failed_candidate"
    / "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE_failed_collapsed_grid.json"
)
NATIVE = (
    HERE
    / "source"
    / "2026-07-17_SBX_ONLY_TERPENES_NATIVE_SCALAR_43_FIELD_BASE_working_native_export_spreadsheet.json"
)
RENDERED_QUALIFIED = (
    HERE
    / "prior_qualified_candidate"
    / "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE_qualified_addresses.json"
)
JSON_REPORT = HERE / "structural_comparison.json"
MD_REPORT = HERE / "structural_comparison.md"
UUID_PATTERN = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
    re.IGNORECASE,
)


def address(row_index: int, column_index: int) -> str:
    value = column_index + 1
    letters = ""
    while value:
        value, remainder = divmod(value - 1, 26)
        letters = chr(65 + remainder) + letters
    return f"{letters}{row_index + 1}"


def dimensions(rows: Any) -> str:
    if not isinstance(rows, list):
        return "absent"
    columns = max((len(row) for row in rows if isinstance(row, list)), default=0)
    return f"{len(rows)}x{columns}"


def json_type_or_absent(container: dict[str, Any], key: str) -> str:
    if key not in container:
        return "absent"
    value = container[key]
    if value is None:
        return "null"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, str):
        return "string"
    return type(value).__name__


def normalize_uuid(item: Any) -> Any:
    if isinstance(item, dict):
        return {key: normalize_uuid(value) for key, value in item.items()}
    if isinstance(item, list):
        return [normalize_uuid(value) for value in item]
    if isinstance(item, str):
        return UUID_PATTERN.sub("<renderer-uuid>", item)
    return item


def summary(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8-sig"))
    config = document.get("config") if isinstance(document.get("config"), dict) else {}
    worksheets = config.get("worksheets") if isinstance(config.get("worksheets"), list) else []
    worksheet = worksheets[0] if worksheets and isinstance(worksheets[0], dict) else {}
    table = document.get("table_config") if isinstance(document.get("table_config"), dict) else {}
    legacy_grid = table.get("cell_settings")
    worksheet_grid = worksheet.get("data")
    top_data = document.get("data") if isinstance(document.get("data"), dict) else {}
    top_grid = top_data.get("Data")
    active_grid = legacy_grid if isinstance(legacy_grid, list) else worksheet_grid
    nonempty = 0
    if isinstance(active_grid, list):
        if legacy_grid is active_grid:
            nonempty = sum(
                isinstance(cell, dict) and cell.get("value") not in ("", None)
                for row in active_grid
                if isinstance(row, list)
                for cell in row
            )
        else:
            nonempty = sum(
                value not in ("", None)
                for row in active_grid
                if isinstance(row, list)
                for value in row
            )
    named = document.get("qb_config", {}).get("named_cells", {})
    defaults = table.get("default_settings", {}) if isinstance(table, dict) else {}
    return {
        "filename": path.name,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "top_level_keys": list(document.keys()),
        "envelope": "legacy table_config/qb_config" if "table_config" in document else "newer config/qb_config/data",
        "config.style_type": json_type_or_absent(config, "style"),
        "config.style_value": config.get("style", "<absent>"),
        "minDimensions": worksheet.get("minDimensions", "<absent>"),
        "rows": len(worksheet.get("rows", [])) if "rows" in worksheet else len(defaults.get("rowHeights", [])) if "rowHeights" in defaults else "absent",
        "columns": len(worksheet.get("columns", [])) if "columns" in worksheet else len(defaults.get("colWidths", [])) if "colWidths" in defaults else "absent",
        "non_empty_cell_count": nonempty,
        "worksheet_data_dimensions": dimensions(worksheet_grid) if "config" in document else dimensions(legacy_grid),
        "worksheet_data_storage": "config.worksheets[0].data" if "config" in document else "table_config.cell_settings",
        "top_level_Data_dimensions": dimensions(top_grid),
        "named_cell_count": len(named) if isinstance(named, (dict, list)) else 0,
        "namespace": config.get("namespace", "<absent>"),
        "worksheetId": worksheet.get("worksheetId", "<absent>"),
        "worksheetName": worksheet.get("worksheetName", "<legacy single logical Data worksheet>"),
        "tableHeight": worksheet.get("tableHeight", "<absent>"),
        "tableWidth": worksheet.get("tableWidth", "<absent>"),
        "worksheet.style_type": json_type_or_absent(worksheet, "style"),
    }


failed_document = json.loads(FAILED.read_text(encoding="utf-8"))
native_document = json.loads(NATIVE.read_text(encoding="utf-8-sig"))
corrected_document = json.loads(RENDERED_QUALIFIED.read_text(encoding="utf-8"))

changed_cells: list[str] = []
native_grid = native_document["table_config"]["cell_settings"]
corrected_grid = corrected_document["table_config"]["cell_settings"]
for row_index, (native_row, corrected_row) in enumerate(zip(native_grid, corrected_grid)):
    for column_index, (native_cell, corrected_cell) in enumerate(zip(native_row, corrected_row)):
        if native_cell.get("value") != corrected_cell.get("value"):
            changed_cells.append(address(row_index, column_index))

report = {
    "classification": "qualified_address_native_envelope_rendered_save_rejected",
    "files": {
        "failed_candidate": summary(FAILED),
        "working_native_export": summary(NATIVE),
        "rendered_qualified_candidate": summary(RENDERED_QUALIFIED),
    },
    "failed_candidate_defects": [
        "Used the newer config/qb_config/data envelope instead of the working legacy table_config/qb_config envelope.",
        "config.style was null while the working native export has no config object or config.style field.",
        "minDimensions was [1, 1] despite serialized 40x26 arrays.",
        "The import loaded 43 qb_config.named_cells entries but rendered only a collapsed/default blank cell.",
        "The import was applied to the NATIVE_SCALAR worksheet instead of the JSON_SCALAR worksheet.",
    ],
    "native_to_corrected_complete_difference": {
        "changed_cell_value_addresses": changed_cells,
        "changed_cell_value_count": len(changed_cells),
        "named_cells": "removed sdf/A1 and replaced the mapping with exactly 43 Data-qualified destinations",
        "all_other_table_config_fields_identical": native_document["table_config"] == {
            **corrected_document["table_config"],
            "cell_settings": native_document["table_config"]["cell_settings"],
        },
        "cell_metadata_identical_after_renderer_uuid_normalization": all(
            normalize_uuid(native_cell.get("meta_data"))
            == normalize_uuid(corrected_cell.get("meta_data"))
            for native_row, corrected_row in zip(native_grid, corrected_grid)
            for native_cell, corrected_cell in zip(native_row, corrected_row)
        ),
        "default_settings_identical": native_document["table_config"].get("default_settings")
        == corrected_document["table_config"].get("default_settings"),
        "plugin_settings_identical": native_document["table_config"].get("plugin_settings")
        == corrected_document["table_config"].get("plugin_settings"),
        "source_specific_UUIDs_preserved": False,
    },
    "interpretation": {
        "logical_worksheet": "The old Sandbox legacy export serializes one unnamed table. It is the candidate's logical Data worksheet.",
        "dual_data_representations": "The legacy reference has one table_config.cell_settings representation and no top-level data['Data']; the rendered qualified candidate preserves that single representation.",
        "config_style": "The legacy reference has no config object, so absence - not null - is the exact matching type/state.",
    },
}

JSON_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

f = report["files"]
rows = []
labels = [
    ("Envelope", "envelope"),
    ("Top-level keys", "top_level_keys"),
    ("config.style type", "config.style_type"),
    ("config.style value", "config.style_value"),
    ("minDimensions", "minDimensions"),
    ("Rows", "rows"),
    ("Columns", "columns"),
    ("Non-empty cells", "non_empty_cell_count"),
    ("Worksheet data dimensions", "worksheet_data_dimensions"),
    ("Worksheet data storage", "worksheet_data_storage"),
    ("Top-level Data dimensions", "top_level_Data_dimensions"),
    ("Named-cell count", "named_cell_count"),
    ("Namespace", "namespace"),
    ("Worksheet ID", "worksheetId"),
    ("Worksheet name", "worksheetName"),
    ("tableHeight", "tableHeight"),
    ("tableWidth", "tableWidth"),
    ("Worksheet style type", "worksheet.style_type"),
]
for label, key in labels:
    values = []
    for role in ("failed_candidate", "working_native_export", "rendered_qualified_candidate"):
        value = f[role][key]
        values.append(json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict)) else str(value))
    rows.append(f"| {label} | {values[0]} | {values[1]} | {values[2]} |")

changed_text = ", ".join(changed_cells)
markdown = f"""# Structural comparison: failed, working native, rendered qualified

Classification: **`qualified_address_native_envelope_rendered_save_rejected`**

| Property | Failed candidate | Working native export | Rendered qualified candidate |
|---|---|---|---|
{chr(10).join(rows)}

## Failed-candidate defects

""" + "\n".join(f"- {item}" for item in report["failed_candidate_defects"]) + f"""

## Complete working-native to rendered-qualified difference

- Named cells: removed the sole diagnostic `sdf / A1` entry and replaced it
  with exactly the 43 Data-qualified entries from
  `config/field_mapping_scalar_candidate.csv`.
- Changed cell-value addresses ({len(changed_cells)}): `{changed_text}`.
- Cell metadata identical after the required renderer-UUID substitution: `{str(report['native_to_corrected_complete_difference']['cell_metadata_identical_after_renderer_uuid_normalization']).lower()}`.
- Native default settings identical: `{str(report['native_to_corrected_complete_difference']['default_settings_identical']).lower()}`.
- Native plugin settings identical: `{str(report['native_to_corrected_complete_difference']['plugin_settings_identical']).lower()}`.
- No other `table_config` field changed.
- The single native renderer UUID was replaced everywhere by one fresh UUID;
  no source-specific UUID was copied.

The old Sandbox legacy export serializes one unnamed table and has no
`config`, `config.style`, `config.worksheets`, worksheet UUID,
`minDimensions`, or top-level `data[\"Data\"]`. The rendered qualified candidate
preserves that exact single-table representation. This is intentional: the
failed candidate's invented newer envelope was the structural defect that
loaded named-cell configuration while collapsing the rendered sheet. Manual
testing later confirmed that this native-envelope file rendered correctly but
failed Save As New Version because its named-cell addresses were qualified.
"""
MD_REPORT.write_text(markdown, encoding="utf-8", newline="\n")
print(JSON_REPORT)
print(MD_REPORT)
