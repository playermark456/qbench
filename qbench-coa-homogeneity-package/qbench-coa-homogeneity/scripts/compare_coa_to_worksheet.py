#!/usr/bin/env python3
"""Light consistency checks between COA source and Homogeneity worksheet JSON."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RENDER_NAMED_CELL_RE = re.compile(r'render_worksheet\(\s*HOMOGENEITY_TEST\s*,\s*named_cell\s*=\s*["\']([^"\']+)["\']')
WORKSHEET_VALUE_RE = re.compile(r'HOMOGENEITY_TEST\.get_worksheet_value\(\s*["\']([^"\']+)["\']\s*\)')


def get_named_cells(path: Path) -> set[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return set(((data.get("qb_config") or {}).get("named_cells") or {}).keys())


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: compare_coa_to_worksheet.py <coa-source.html> <worksheet-template.json>")
        return 2
    coa_path = Path(argv[0])
    json_path = Path(argv[1])
    coa = coa_path.read_text(encoding="utf-8")
    named = get_named_cells(json_path)

    errors = 0
    if "HOMOGENEITY_TEST" not in coa:
        print("ERROR: COA source does not reference HOMOGENEITY_TEST")
        errors += 1
    else:
        print("OK: COA references HOMOGENEITY_TEST")

    render_refs = set(RENDER_NAMED_CELL_RE.findall(coa))
    value_refs = set(WORKSHEET_VALUE_RE.findall(coa))
    refs = render_refs | value_refs
    print(f"Homogeneity render named_cell refs: {sorted(render_refs)}")
    print(f"Homogeneity get_worksheet_value refs: {sorted(value_refs)}")

    missing = sorted(refs - named)
    if missing:
        print(f"ERROR: COA references missing Homogeneity named cell(s): {missing}")
        errors += 1
    else:
        print("OK: Homogeneity named cell references exist in worksheet JSON")

    if "report_results" not in render_refs:
        print("WARNING: COA does not render HOMOGENEITY_TEST named_cell='report_results'")
    if "pass_fail" not in named:
        print("ERROR: worksheet JSON missing pass_fail")
        errors += 1

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
