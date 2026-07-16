"""Build the Prompt 4.6B probe from an old-Sandbox blank export."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[6]
PACKAGE_DIR = Path(__file__).resolve().parents[1]
SOURCE_PATH = (
    PACKAGE_DIR
    / "source/2026-07-16_ait-sandbox_ws_id_62_blank_export_spreadsheet.json"
)
CONTROLLED_PATH = REPO_ROOT / (
    "QBench/Worksheets/Terpenes/development/"
    "2026-07-15_qbench_native_parser_probe/dist/"
    "qbench_runtime_probe_batch_ws_candidate.json"
)
OUTPUT_PATH = (
    PACKAGE_DIR
    / "dist/qbench_runtime_probe_batch_ws_candidate__ait_sandbox_runtime.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_candidate() -> dict[str, Any]:
    source = load_json(SOURCE_PATH)
    controlled = load_json(CONTROLLED_PATH)

    source_worksheets = source["config"]["worksheets"]
    controlled_worksheets = controlled["config"]["worksheets"]
    if len(source_worksheets) != 1 or source_worksheets[0]["worksheetName"] != "Sheet1":
        raise ValueError("Unexpected old-Sandbox source worksheet")
    if len(controlled_worksheets) != 1 or controlled_worksheets[0]["worksheetName"] != "Probe":
        raise ValueError("Unexpected controlled probe worksheet")

    source_worksheet = source_worksheets[0]
    controlled_worksheet = controlled_worksheets[0]
    candidate = copy.deepcopy(source)
    worksheet = copy.deepcopy(source_worksheet)

    # Keep the old-Sandbox namespace and worksheet identity while replacing the
    # blank spreadsheet payload with the controlled Probe semantics.
    for field in (
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
    ):
        worksheet[field] = copy.deepcopy(controlled_worksheet[field])
    worksheet["worksheetId"] = source_worksheet["worksheetId"]

    candidate["config"]["worksheets"] = [worksheet]
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
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(build_candidate(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": "ok",
                "source": str(SOURCE_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
                "controlled_semantics": str(CONTROLLED_PATH.relative_to(REPO_ROOT)).replace(
                    "\\", "/"
                ),
                "output": str(OUTPUT_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
                "worksheet": "Probe",
                "rows": 17,
                "columns": 57,
                "named_cells": 15,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
