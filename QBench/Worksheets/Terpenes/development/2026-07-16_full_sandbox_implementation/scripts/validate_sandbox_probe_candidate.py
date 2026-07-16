"""Validate the old-Sandbox-based Prompt 4.6B probe candidate."""

from __future__ import annotations

import hashlib
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
CANDIDATE_PATH = (
    PACKAGE_DIR
    / "dist/qbench_runtime_probe_batch_ws_candidate__ait_sandbox_runtime.json"
)
INVALID_PATH = PACKAGE_DIR / "sandbox_probe_worksheet_compatibility_candidate.json"
EXPECTED_SOURCE_SHA256 = "02e986a41bcd9f6b1bc9586c3df041cbaf930ad4309fb28d5e20d26c6057e5c2"
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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def cell_value(data: list[list[Any]], address: str) -> Any:
    letters = "".join(character for character in address if character.isalpha())
    row = int("".join(character for character in address if character.isdigit()))
    column = 0
    for character in letters:
        column = column * 26 + ord(character.upper()) - 64
    return data[row - 1][column - 1]


def main() -> None:
    errors: list[str] = []
    source_bytes = SOURCE_PATH.read_bytes()
    source = json.loads(source_bytes)
    controlled = load_json(CONTROLLED_PATH)
    candidate = load_json(CANDIDATE_PATH)

    source_sha = hashlib.sha256(source_bytes).hexdigest()
    if source_sha != EXPECTED_SOURCE_SHA256:
        errors.append(f"old-Sandbox source SHA changed: {source_sha}")

    source_ws = source["config"]["worksheets"][0]
    candidate_worksheets = candidate["config"].get("worksheets", [])
    controlled_ws = controlled["config"]["worksheets"][0]
    if len(candidate_worksheets) != 1:
        errors.append("candidate must contain exactly one worksheet")
        candidate_ws: dict[str, Any] = {}
    else:
        candidate_ws = candidate_worksheets[0]

    if candidate_ws.get("worksheetName") != "Probe":
        errors.append("candidate worksheet must be named Probe")
    if candidate_ws.get("worksheetId") != source_ws.get("worksheetId"):
        errors.append("candidate did not preserve the old-Sandbox worksheet identity")
    if candidate["config"].get("namespace") != source["config"].get("namespace"):
        errors.append("candidate did not preserve the old-Sandbox namespace")
    if candidate_ws.get("data") != controlled_ws.get("data"):
        errors.append("candidate worksheet data differs from the controlled Probe")
    if candidate.get("data") != controlled.get("data"):
        errors.append("candidate top-level data differs from the controlled Probe")
    if candidate.get("qb_config") != controlled.get("qb_config"):
        errors.append("candidate named-cell configuration differs from the controlled Probe")
    if candidate_ws.get("cells") != controlled_ws.get("cells"):
        errors.append("candidate cell configuration differs from the controlled Probe")

    data = candidate_ws.get("data", [])
    if len(data) != 17 or any(len(row) != 57 for row in data):
        errors.append("candidate must contain a 17-row by 57-column Probe matrix")
    for address, formula in EXPECTED_FORMULAS.items():
        if not data or cell_value(data, address) != formula:
            errors.append(f"formula mismatch at {address}")

    named_cells = candidate.get("qb_config", {}).get("named_cells", {})
    expected_named_cells = controlled.get("qb_config", {}).get("named_cells", {})
    if len(named_cells) != 15:
        errors.append("candidate must contain 15 named cells")
    targets = [definition.get("cell") for definition in named_cells.values()]
    if len(targets) != len(set(targets)):
        errors.append("candidate contains duplicate named-cell targets")
    if named_cells != expected_named_cells:
        errors.append("candidate named-cell mappings are not exact")

    serialized = json.dumps(candidate)
    for forbidden in ("STD 1", "System Suitability", "Sheet1!B96", "pass_fail"):
        if forbidden in serialized:
            errors.append(f"forbidden legacy value found: {forbidden}")

    if INVALID_PATH.exists() and candidate == load_json(INVALID_PATH):
        errors.append("candidate unexpectedly matches the quarantined Terpenes-derived attempt")

    result = {
        "status": "ok" if not errors else "failed",
        "source_sha256": source_sha,
        "worksheet": candidate_ws.get("worksheetName"),
        "rows": len(data),
        "columns": len(data[0]) if data else 0,
        "named_cells": len(named_cells),
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
