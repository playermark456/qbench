#!/usr/bin/env python3
"""Adapt the controlled Prompt 4 workbook to a new old-Sandbox blank export."""
from __future__ import annotations

import argparse
import copy
import json
import uuid
from pathlib import Path
from typing import Any


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parents[4]
CONTROLLED_PATH = REPO_ROOT / (
    "QBench/Worksheets/Terpenes/development/"
    "2026-07-14_batch_worksheet_candidate/dist/"
    "terpenes__batch_ws_id_43__candidate_v1__2026-07-14.json"
)

SEMANTIC_FIELDS = (
    "worksheetName",
    "data",
    "columns",
    "rows",
    "minDimensions",
    "cells",
    "tableWidth",
    "tableHeight",
    "cache",
    "comments",
    "mergeCells",
    "freezeRows",
    "freezeColumns",
    "filters",
    "style",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_candidate(blank_export: Path) -> dict[str, Any]:
    source = load_json(blank_export)
    controlled = load_json(CONTROLLED_PATH)

    source_worksheets = source["config"]["worksheets"]
    controlled_worksheets = controlled["config"]["worksheets"]
    expected_names = ["Run Setup", "Instrument Import", "QC Review", "Publish"]
    if len(source_worksheets) != 1 or source_worksheets[0]["worksheetName"] != "Sheet1":
        raise ValueError("Unexpected blank old-Sandbox worksheet export")
    if [worksheet["worksheetName"] for worksheet in controlled_worksheets] != expected_names:
        raise ValueError("Unexpected controlled Prompt 4 worksheet tabs")

    source_worksheet = source_worksheets[0]
    source_identity = uuid.UUID(source_worksheet["worksheetId"])
    adapted_worksheets: list[dict[str, Any]] = []
    for index, controlled_worksheet in enumerate(controlled_worksheets):
        worksheet = copy.deepcopy(source_worksheet)
        for field in SEMANTIC_FIELDS:
            if field in controlled_worksheet:
                worksheet[field] = copy.deepcopy(controlled_worksheet[field])
            elif field in worksheet and field == "style":
                worksheet.pop(field)
        worksheet["worksheetId"] = (
            source_worksheet["worksheetId"]
            if index == 0
            else str(uuid.uuid5(source_identity, controlled_worksheet["worksheetName"]))
        )
        adapted_worksheets.append(worksheet)

    candidate = copy.deepcopy(source)
    candidate["config"]["worksheets"] = adapted_worksheets
    candidate["config"]["allowDeleteWorksheet"] = False
    candidate["config"]["allowMoveWorksheet"] = False
    candidate["config"]["allowRenameWorksheet"] = False
    candidate["config"]["plugins"] = copy.deepcopy(
        controlled["config"].get("plugins", {"conditionalFormatting": {"rules": []}})
    )
    candidate["qb_config"] = copy.deepcopy(controlled["qb_config"])
    candidate["data"] = copy.deepcopy(controlled["data"])
    return candidate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blank-export", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    candidate = build_candidate(args.blank_export)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(candidate, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
        newline="\n",
    )
    worksheet_names = [
        worksheet["worksheetName"] for worksheet in candidate["config"]["worksheets"]
    ]
    named_cells = candidate["qb_config"].get("named_cells", [])
    named_cell_text = json.dumps(named_cells, ensure_ascii=False).lower()
    if "pass_fail" in named_cell_text or "pass/fail" in named_cell_text:
        raise AssertionError("A prohibited Terpenes Pass/Fail named-cell artifact is present.")
    print(
        json.dumps(
            {
                "status": "ok",
                "tabs": worksheet_names,
                "named_cell_count": len(named_cells),
                "output_bytes": args.output.stat().st_size,
                "runtime_namespace_committed": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
