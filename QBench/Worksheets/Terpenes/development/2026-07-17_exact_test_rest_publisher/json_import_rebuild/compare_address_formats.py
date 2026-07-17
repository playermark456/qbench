#!/usr/bin/env python3
"""Compare the rendered qualified candidate to the unqualified save candidate."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PRIOR = (
    HERE
    / "prior_qualified_candidate"
    / "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE_qualified_addresses.json"
)
CURRENT = HERE / "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE.json"
MAPPING = ROOT / "config" / "field_mapping_scalar_candidate.csv"
JSON_REPORT = HERE / "address_format_comparison.json"
MD_REPORT = HERE / "address_format_comparison.md"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def differences(left: Any, right: Any, path: str = "$") -> list[dict[str, Any]]:
    if type(left) is not type(right):
        return [{"path": path, "before": left, "after": right}]
    if isinstance(left, dict):
        output: list[dict[str, Any]] = []
        for key in sorted(set(left) | set(right)):
            child = f"{path}.{key}"
            if key not in left:
                output.append({"path": child, "before": "<absent>", "after": right[key]})
            elif key not in right:
                output.append({"path": child, "before": left[key], "after": "<absent>"})
            else:
                output.extend(differences(left[key], right[key], child))
        return output
    if isinstance(left, list):
        output = []
        if len(left) != len(right):
            output.append({"path": f"{path}.length", "before": len(left), "after": len(right)})
        for index, (left_item, right_item) in enumerate(zip(left, right)):
            output.extend(differences(left_item, right_item, f"{path}[{index}]"))
        return output
    return [] if left == right else [{"path": path, "before": left, "after": right}]


prior = json.loads(PRIOR.read_text(encoding="utf-8"))
current = json.loads(CURRENT.read_text(encoding="utf-8"))
with MAPPING.open(newline="", encoding="utf-8") as handle:
    mapping = list(csv.DictReader(handle))

diffs = differences(prior, current)
expected_paths = {
    f"$.qb_config.named_cells.{row['destination_named_cell']}.cell" for row in mapping
}
actual_paths = {item["path"] for item in diffs}
all_changes_intended = len(diffs) == 43 and actual_paths == expected_paths

changes = []
for row in mapping:
    name = row["destination_named_cell"]
    logical = row["destination_cell"]
    runtime = logical.split("!", 1)[1]
    old = prior["qb_config"]["named_cells"][name]["cell"]
    new = current["qb_config"]["named_cells"][name]["cell"]
    changes.append(
        {
            "name": name,
            "logical_address": logical,
            "previous_json_cell": old,
            "old_sandbox_json_cell": new,
            "expected_runtime_cell": runtime,
            "exact_conversion": old == logical and new == runtime,
        }
    )

report = {
    "classification": "qualified_to_unqualified_one_tab_compatibility_correction",
    "previous_candidate": {"filename": PRIOR.name, "sha256": digest(PRIOR)},
    "new_candidate": {"filename": CURRENT.name, "sha256": digest(CURRENT)},
    "difference_count": len(diffs),
    "expected_difference_count": 43,
    "all_differences_under_qb_config_named_cells_cell": all_changes_intended,
    "rendered_worksheet_structure_unchanged": all_changes_intended,
    "grid_dimensions": "40x26",
    "required_anchor_count": 28,
    "named_cell_count": len(current["qb_config"]["named_cells"]),
    "all_json_cells_unqualified": all("!" not in item["old_sandbox_json_cell"] for item in changes),
    "a2_mapping_present": any(item["old_sandbox_json_cell"] == "A2" for item in changes),
    "specific_mappings": {
        name: current["qb_config"]["named_cells"][name]["cell"]
        for name in (
            "terpenes_instrument_conc_01",
            "terpenes_instrument_conc_12",
            "terpenes_instrument_conc_23",
            "sample_mass_g",
            "batch_qc_disposition",
            "publish_ready",
            "source_file_hash",
        )
    },
    "changes": changes,
}
JSON_REPORT.write_text(
    json.dumps(report, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
    newline="\n",
)

rows = "\n".join(
    f"| `{item['name']}` | `{item['logical_address']}` | "
    f"`{item['old_sandbox_json_cell']}` |"
    for item in changes
)
markdown = f"""# Qualified-to-unqualified address comparison

Classification: **`qualified_to_unqualified_one_tab_compatibility_correction`**

- Previous candidate SHA-256: `{report['previous_candidate']['sha256']}`
- New candidate SHA-256: `{report['new_candidate']['sha256']}`
- JSON differences: `{len(diffs)}`
- Expected named-cell address differences: `43`
- All differences limited to `qb_config.named_cells.<name>.cell`:
  `{str(all_changes_intended).lower()}`
- Rendered 40x26 worksheet structure and 28 anchors unchanged:
  `{str(all_changes_intended).lower()}`
- All new JSON cell values unqualified:
  `{str(report['all_json_cells_unqualified']).lower()}`
- A2 mapping present: `{str(report['a2_mapping_present']).lower()}`

The CSV remains the logical, sheet-qualified mapping. The old-Sandbox runtime
JSON uses the corresponding unqualified scalar cell for this exact one-tab
legacy worksheet.

| Named cell | Logical address | Old-Sandbox JSON cell |
|---|---|---|
{rows}
"""
MD_REPORT.write_text(markdown, encoding="utf-8", newline="\n")
print(JSON_REPORT)
print(MD_REPORT)
