#!/usr/bin/env python3
"""Validate QBench spreadsheet-template JSON files.

Checks:
- valid JSON
- unique worksheet names
- unique named-cell system names
- required named cells: pass_fail and report_results
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from collections import Counter

REQUIRED_NAMED_CELLS = {"pass_fail", "report_results"}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_named_cells(data: dict) -> dict:
    qb_config = data.get("qb_config") or data.get("config", {}).get("qb_config") or {}
    named = qb_config.get("named_cells") or {}
    return named if isinstance(named, dict) else {}


def validate(path: Path) -> int:
    print(f"\n== {path} ==")
    try:
        data = load_json(path)
    except Exception as exc:
        print(f"ERROR: invalid JSON: {exc}")
        return 1

    errors = 0
    config = data.get("config", {})
    worksheets = config.get("worksheets", [])
    worksheet_names = [w.get("worksheetName") for w in worksheets if isinstance(w, dict)]
    dup_ws = [name for name, count in Counter(worksheet_names).items() if name and count > 1]
    if dup_ws:
        print(f"ERROR: duplicate worksheet names: {dup_ws}")
        errors += 1
    else:
        print(f"OK: {len(worksheet_names)} worksheet name(s), no duplicates")

    named = get_named_cells(data)
    print(f"Found {len(named)} named cell(s)")
    missing = sorted(REQUIRED_NAMED_CELLS - set(named.keys()))
    if missing:
        print(f"ERROR: missing required named cells: {missing}")
        errors += 1
    else:
        print("OK: required named cells present")

    bad_defs = []
    for system_name, info in named.items():
        if not isinstance(info, dict):
            bad_defs.append(system_name)
            continue
        if not info.get("cell"):
            bad_defs.append(system_name)
    if bad_defs:
        print(f"ERROR: named cells with missing/invalid cell definitions: {bad_defs}")
        errors += 1

    # Report duplicate cell targets for visibility. Sometimes intentional, so warn only.
    cell_to_names: dict[str, list[str]] = {}
    for system_name, info in named.items():
        if isinstance(info, dict):
            cell = info.get("cell")
            if cell:
                cell_to_names.setdefault(cell, []).append(system_name)
    dup_targets = {cell: names for cell, names in cell_to_names.items() if len(names) > 1}
    if dup_targets:
        print("WARNING: multiple named cells point to same cell/range:")
        for cell, names in dup_targets.items():
            print(f"  {cell}: {', '.join(names)}")
    else:
        print("OK: no duplicate named-cell targets")

    if errors:
        print(f"FAILED with {errors} error(s)")
    else:
        print("PASSED")
    return 1 if errors else 0


def iter_paths(args: list[str]) -> list[Path]:
    paths: list[Path] = []
    for arg in args:
        p = Path(arg)
        if p.is_dir():
            paths.extend(sorted(p.rglob("*.json")))
        else:
            paths.append(p)
    return paths


def main(argv: list[str]) -> int:
    if not argv:
        print("Usage: validate_qbench_json.py <file-or-directory> [...]")
        return 2
    exit_code = 0
    for path in iter_paths(argv):
        exit_code |= validate(path)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
