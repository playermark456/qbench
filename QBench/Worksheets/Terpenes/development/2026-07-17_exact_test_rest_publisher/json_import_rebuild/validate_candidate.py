from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import uuid
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CANDIDATE = HERE / "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE.json"
MAPPING = ROOT / "config" / "field_mapping_scalar_candidate.csv"
REFERENCE_PATHS = [
    ROOT.parents[0]
    / "2026-07-16_full_sandbox_implementation"
    / "round_trip"
    / "2026-07-16_ait-sandbox_ws_id_62_version_1_draft_export_spreadsheet.json",
    ROOT.parents[3]
    / "Rescans"
    / "2026-07-04"
    / "Worksheets"
    / "Terpenes"
    / "terpenes__id_42__worksheet_export_spreadsheet__active__2026-07-04.json",
]


def column_index(name: str) -> int:
    value = 0
    for character in name:
        value = value * 26 + ord(character) - 64
    return value - 1


def fail(message: str) -> None:
    failures.append(message)


failures: list[str] = []

try:
    candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as error:
    print(f"candidate validation FAILED: {error}")
    raise SystemExit(1)

with MAPPING.open(newline="", encoding="utf-8") as handle:
    mapping = list(csv.DictReader(handle))

for key in ("config", "qb_config", "data"):
    if key not in candidate:
        fail(f"missing top-level {key}")

config = candidate.get("config", {})
qb_config = candidate.get("qb_config", {})
top_data = candidate.get("data", {})
worksheets = config.get("worksheets", [])
if len(worksheets) != 1:
    fail(f"expected one worksheet, found {len(worksheets)}")
worksheet = worksheets[0] if worksheets else {}
if worksheet.get("worksheetName") != "Data":
    fail("worksheet name is not Data")
if set(top_data) != {"Data"}:
    fail("top-level data does not contain exactly Data")

rows = worksheet.get("rows", [])
columns = worksheet.get("columns", [])
grid = worksheet.get("data", [])
evaluated_grid = top_data.get("Data", [])
if len(rows) < 40 or len(grid) < 40 or len(evaluated_grid) < 40:
    fail("Data grid has fewer than 40 rows")
if len(columns) < 26:
    fail("Data grid has fewer than 26 columns")
if any(len(row) < 26 for row in grid[:40]):
    fail("worksheet Data rows have fewer than 26 columns")
if any(len(row) < 26 for row in evaluated_grid[:40]):
    fail("top-level Data rows have fewer than 26 columns")

named_cells = qb_config.get("named_cells", {})
if len(named_cells) != 43:
    fail(f"expected 43 named cells, found {len(named_cells)}")
if len(mapping) != 43:
    fail(f"expected 43 mapping rows, found {len(mapping)}")

expected = {
    row["destination_named_cell"]: {
        "cell": row["destination_cell"],
        "display_name": row["source_header"],
        "export": True,
    }
    for row in mapping
}
if named_cells != expected:
    missing = sorted(set(expected) - set(named_cells))
    extra = sorted(set(named_cells) - set(expected))
    fail(f"named-cell contract differs from mapping; missing={missing}; extra={extra}")

names = list(named_cells)
addresses = [entry.get("cell") for entry in named_cells.values()]
if len(names) != len(set(names)):
    fail("duplicate system names")
if len(addresses) != len(set(addresses)):
    fail("duplicate named-cell addresses")
if any("[" in name or "]" in name for name in names):
    fail("bracketed destination name present")
if "sdf" in names:
    fail("manual diagnostic name sdf is present")

analyte_names = [name for name in names if name.startswith("terpenes_instrument_conc_")]
expected_analytes = [f"terpenes_instrument_conc_{index:02d}" for index in range(1, 24)]
if analyte_names != expected_analytes:
    fail("analyte names are not the exact contiguous _01 through _23 sequence")
expected_analyte_cells = [
    f"Data!{chr(ord('D') + index)}2" for index in range(23)
]
if [named_cells[name]["cell"] for name in expected_analytes] != expected_analyte_cells:
    fail("analyte cells are not exactly Data!D2:Z2")

cells = worksheet.get("cells", {})
address_pattern = re.compile(r"^Data!([A-Z]+)([1-9][0-9]*)$")
for name, entry in named_cells.items():
    match = address_pattern.fullmatch(str(entry.get("cell", "")))
    if not match:
        fail(f"invalid sheet-qualified address for {name}")
        continue
    column = column_index(match.group(1))
    row = int(match.group(2)) - 1
    if row >= len(grid) or column >= len(columns):
        fail(f"out-of-grid address for {name}")
        continue
    address = entry["cell"].split("!", 1)[1]
    value = grid[row][column]
    evaluated = evaluated_grid[row][column]
    cell_config = cells.get(address, {})
    if value not in ("", None) or evaluated not in ("", None):
        fail(f"destination is not blank: {name}")
    if isinstance(value, str) and value.startswith("="):
        fail(f"destination is formula-owned: {name}")
    if "formula" in cell_config:
        fail(f"destination cell config contains formula: {name}")
    if cell_config.get("readonly") is not False:
        fail(f"destination is not writable: {name}")
    if entry.get("export") is not True:
        fail(f"destination export flag is not true: {name}")

normalized_contract = json.dumps(named_cells, sort_keys=True).lower()
for prohibited in (
    "pass_fail",
    "pass/fail",
    "pass fail",
    "result_status",
    "dimethylacetamide",
    "peak table",
    "peak_table",
):
    if prohibited in normalized_contract:
        fail(f"prohibited reportable field present: {prohibited}")

if worksheet.get("mergeCells") not in ({}, None):
    fail("merged cells are present")
if config.get("plugins", {}).get("conditionalFormatting", {}).get("rules") != []:
    fail("conditional formatting is present")
if worksheet.get("freezeRows") or worksheet.get("freezeColumns"):
    fail("hidden/frozen rows or columns are present")

candidate_namespace = config.get("namespace")
candidate_worksheet_id = worksheet.get("worksheetId")
try:
    uuid.UUID(str(candidate_namespace))
    uuid.UUID(str(candidate_worksheet_id))
except ValueError:
    fail("candidate namespace or worksheetId is not a UUID")
if candidate_namespace == candidate_worksheet_id:
    fail("namespace and worksheetId are reused")

reference_namespaces: set[str] = set()
reference_worksheet_ids: set[str] = set()
for path in REFERENCE_PATHS:
    reference = json.loads(path.read_text(encoding="utf-8"))
    reference_namespaces.add(str(reference.get("config", {}).get("namespace")))
    reference_worksheet_ids.update(
        str(item.get("worksheetId"))
        for item in reference.get("config", {}).get("worksheets", [])
    )
if candidate_namespace in reference_namespaces:
    fail("candidate reused a source namespace")
if candidate_worksheet_id in reference_worksheet_ids:
    fail("candidate reused a source worksheet UUID")

serialized = json.dumps(candidate, sort_keys=True).lower()
for prohibited in (
    "qbench_client_id",
    "qbench_client_secret",
    "authorization:",
    "bearer ",
    "signed_url",
    "customer_name",
    "customer_data",
):
    if prohibited in serialized:
        fail(f"credential, token, signed URL, or customer data marker present: {prohibited}")

if failures:
    print("JSON candidate validation FAILED")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

digest = hashlib.sha256(CANDIDATE.read_bytes()).hexdigest()
print("JSON candidate validation PASSED")
print("- one Data worksheet")
print(f"- rows={len(rows)} columns={len(columns)}")
print(f"- named_cells={len(named_cells)} analytes={len(analyte_names)}")
print("- all destinations blank, writable, unique, non-formula, exportable")
print("- no prohibited fields, reused source identifiers, or sensitive data")
print(f"- sha256={digest}")
