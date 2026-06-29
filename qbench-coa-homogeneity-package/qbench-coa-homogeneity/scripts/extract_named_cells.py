#!/usr/bin/env python3
"""Print named cells from a QBench spreadsheet-template JSON."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("Usage: extract_named_cells.py <qbench-template.json>")
        return 2
    path = Path(argv[0])
    data = json.loads(path.read_text(encoding="utf-8"))
    named = (data.get("qb_config") or {}).get("named_cells") or {}
    for name, info in sorted(named.items()):
        cell = info.get("cell") if isinstance(info, dict) else ""
        display = info.get("display_name") if isinstance(info, dict) else ""
        print(f"{name}\t{cell}\t{display}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
