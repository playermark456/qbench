#!/usr/bin/env python3
"""Replace runtime worksheet UUIDs in a QBench Export Spreadsheet artifact."""
from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path
from typing import Any


NAMESPACE = uuid.UUID("4e1f1322-8fa2-5cdb-886a-88f8fb577a25")
EXPECTED_SHEETS = ["Run Setup", "Instrument Import", "QC Review", "Publish"]


def worksheet_id(name: str) -> str:
    return str(uuid.uuid5(NAMESPACE, f"prompt-4.6c/{name}"))


def collect_runtime_ids(value: Any, replacements: dict[str, str]) -> None:
    if isinstance(value, dict):
        if isinstance(value.get("worksheetName"), str) and isinstance(
            value.get("worksheetId"), str
        ):
            replacements[value["worksheetId"]] = worksheet_id(value["worksheetName"])
        for nested in value.values():
            collect_runtime_ids(nested, replacements)
    elif isinstance(value, list):
        for nested in value:
            collect_runtime_ids(nested, replacements)


def replace_runtime_ids(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, dict):
        return {key: replace_runtime_ids(nested, replacements) for key, nested in value.items()}
    if isinstance(value, list):
        return [replace_runtime_ids(nested, replacements) for nested in value]
    if isinstance(value, str):
        result = value
        for runtime_id, sanitized_id in replacements.items():
            result = result.replace(runtime_id, sanitized_id)
        return result
    return value


def worksheet_groups(value: Any) -> list[list[dict[str, Any]]]:
    groups: list[list[dict[str, Any]]] = []
    if isinstance(value, dict):
        worksheets = value.get("worksheets")
        if isinstance(worksheets, list) and all(isinstance(item, dict) for item in worksheets):
            groups.append(worksheets)
        for nested in value.values():
            groups.extend(worksheet_groups(nested))
    elif isinstance(value, list):
        for nested in value:
            groups.extend(worksheet_groups(nested))
    return groups


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_export", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    raw = json.loads(args.raw_export.read_text(encoding="utf-8"))
    replacements: dict[str, str] = {}
    collect_runtime_ids(raw, replacements)
    assert replacements, "No runtime worksheet UUIDs found"
    sanitized = replace_runtime_ids(raw, replacements)

    groups = worksheet_groups(sanitized)
    assert groups, "No worksheet groups found"
    for group in groups:
        names = [worksheet.get("worksheetName") for worksheet in group]
        if names == EXPECTED_SHEETS:
            assert [worksheet.get("worksheetId") for worksheet in group] == [
                worksheet_id(name) for name in EXPECTED_SHEETS
            ]

    serialized = json.dumps(sanitized, ensure_ascii=False, separators=(",", ":"))
    for runtime_id in replacements:
        assert runtime_id not in serialized
    assert "ait.qbench.net" not in serialized
    assert "ait-sandbox.qbench.net" not in serialized
    assert '"worksheetName":"Instrument Import"' in serialized

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(serialized + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": "ok",
                "worksheet_groups": len(groups),
                "runtime_worksheet_ids_replaced": len(replacements),
                "output_bytes": args.output.stat().st_size,
                "sandbox_internal_object_ids_included": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
