#!/usr/bin/env python3
"""Validate the saved/reopened old-Sandbox Draft round-trip export."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REBUILD = HERE.parent
ROOT = REBUILD.parent
CANDIDATE = REBUILD / "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE.json"
ROUND_TRIP = (
    HERE
    / "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE_v1_DRAFT_saved_reopened_export_spreadsheet.json"
)
MAPPING = ROOT / "config" / "field_mapping_scalar_candidate.csv"
CANDIDATE_SHA256 = "e5ef20a5cec574dc292ed679867e01313233c92ceda9ef863bf98dd8d4485b80"
ROUND_TRIP_SHA256 = "3589f2ace8afb96db96d4da638e9effc86bda404e03f97b85fca0e43aa349912"
ROWS = 40
COLS = 26
UUID_PATTERN = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
    re.IGNORECASE,
)


def address_parts(address: str) -> tuple[int, int]:
    match = re.fullmatch(r"([A-Z]+)([1-9][0-9]*)", address)
    if not match:
        raise ValueError(address)
    column = 0
    for character in match.group(1):
        column = column * 26 + ord(character) - 64
    return int(match.group(2)) - 1, column - 1


def contains_key(item: Any, key_name: str, truthy_only: bool = False) -> bool:
    if isinstance(item, dict):
        for key, value in item.items():
            if str(key).lower() == key_name.lower():
                if not truthy_only or value not in (False, None, "false", 0):
                    return True
            if contains_key(value, key_name, truthy_only):
                return True
    elif isinstance(item, list):
        return any(contains_key(value, key_name, truthy_only) for value in item)
    return False


def normalized_renderer_uuid(item: Any) -> Any:
    if isinstance(item, dict):
        return {key: normalized_renderer_uuid(value) for key, value in item.items()}
    if isinstance(item, list):
        return [normalized_renderer_uuid(value) for value in item]
    if isinstance(item, str):
        return UUID_PATTERN.sub("<QBENCH_RENDERER_UUID>", item)
    return item


failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


if hashlib.sha256(CANDIDATE.read_bytes()).hexdigest() != CANDIDATE_SHA256:
    fail("candidate bytes or SHA-256 changed")
if hashlib.sha256(ROUND_TRIP.read_bytes()).hexdigest() != ROUND_TRIP_SHA256:
    fail("raw round-trip export bytes or SHA-256 changed")

try:
    candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))
    exported = json.loads(ROUND_TRIP.read_text(encoding="utf-8-sig"))
except (OSError, json.JSONDecodeError) as error:
    print(f"Round-trip validation FAILED: {error}")
    raise SystemExit(1)

if set(exported) != {"table_config", "qb_config"}:
    fail("round trip is not the exact legacy table_config/qb_config envelope")
if "config" in exported or "data" in exported or "worksheets" in exported:
    fail("round trip introduced a second worksheet or newer-envelope field")

grid = exported.get("table_config", {}).get("cell_settings", [])
if len(grid) != ROWS or any(len(row) != COLS for row in grid):
    fail("saved/reopened logical Data worksheet is not exactly 40x26")

with MAPPING.open(newline="", encoding="utf-8") as handle:
    mapping = list(csv.DictReader(handle))
expected_named = {
    row["destination_named_cell"]: {
        "cell": row["destination_cell"].split("!", 1)[1],
        "display_name": row["source_header"],
        "export": True,
    }
    for row in mapping
}
named = exported.get("qb_config", {}).get("named_cells", {})
if len(mapping) != 43 or len(named) != 43:
    fail("saved/reopened named-cell count is not exactly 43")
if named != expected_named:
    fail("saved/reopened names, addresses, display names, or export flags changed")

addresses = [entry.get("cell") for entry in named.values()]
if len(addresses) != len(set(addresses)):
    fail("saved/reopened named-cell addresses are duplicated")
if any(not isinstance(address, str) or "!" in address for address in addresses):
    fail("saved/reopened named-cell address is not unqualified")
if any(address == "A2" for address in addresses):
    fail("an A2 destination exists")
if named.get("terpenes_instrument_conc_01", {}).get("cell") != "D2":
    fail("first analyte is not D2")

expected_analytes = [f"{chr(68 + index)}2" for index in range(23)]
actual_analytes = [
    named[f"terpenes_instrument_conc_{index:02d}"]["cell"]
    for index in range(1, 24)
]
if actual_analytes != expected_analytes:
    fail("saved/reopened analytes are not D2:Z2 in order")

for name, entry in named.items():
    try:
        row_index, column_index = address_parts(str(entry.get("cell", "")))
    except ValueError:
        fail(f"invalid saved/reopened address for {name}")
        continue
    if row_index >= ROWS or column_index >= COLS:
        fail(f"out-of-range saved/reopened address for {name}")
        continue
    cell = grid[row_index][column_index]
    if cell.get("value") not in ("", None):
        fail(f"saved/reopened destination is not blank: {name}")
    if isinstance(cell.get("value"), str) and cell["value"].startswith("="):
        fail(f"saved/reopened destination is formula-owned: {name}")
    if contains_key(cell.get("meta_data", {}), "formula"):
        fail(f"saved/reopened destination has formula metadata: {name}")
    if contains_key(cell.get("meta_data", {}), "readonly", truthy_only=True):
        fail(f"saved/reopened destination is read-only: {name}")
    if entry.get("export") is not True:
        fail(f"saved/reopened destination is not exportable: {name}")

anchors = {
    "A1": "Terpenes JSON scalar 43-field base",
    "A12": "Preparation and calculation inputs",
    "A22": "Controlled disposition",
    "A28": "Source and audit metadata",
    "A40": "End of worksheet",
}
for index, row in enumerate(mapping[:23]):
    anchors[f"{chr(68 + index)}1"] = row["source_header"]
for address, expected_value in anchors.items():
    row_index, column_index = address_parts(address)
    if grid[row_index][column_index].get("value") != expected_value:
        fail(f"saved/reopened anchor missing or changed at {address}")

contract_text = json.dumps(named, ensure_ascii=False, sort_keys=True).lower()
for prohibited in (
    "sdf",
    "pass_fail",
    "pass/fail",
    "pass fail",
    "result_status",
    "dimethylacetamide",
    "peak table",
    "peak_table",
):
    if prohibited in contract_text:
        fail(f"prohibited reportable destination present: {prohibited}")

candidate_uuids = set(UUID_PATTERN.findall(json.dumps(candidate)))
exported_uuids = set(UUID_PATTERN.findall(json.dumps(exported)))
if len(candidate_uuids) != 1 or len(exported_uuids) != 1:
    fail("expected exactly one renderer UUID in each artifact")
if candidate_uuids == exported_uuids:
    fail("QBench did not regenerate the renderer UUID on the saved round trip")
if normalized_renderer_uuid(candidate) != normalized_renderer_uuid(exported):
    fail("round trip differs from the candidate beyond the renderer UUID")

serialized = json.dumps(exported, ensure_ascii=False, sort_keys=True).lower()
for prohibited in (
    "qbench_client_id",
    "qbench_client_secret",
    "authorization:",
    "bearer ",
    "customer_name",
    "customer_data",
):
    if prohibited in serialized:
        fail(f"credential, token, or customer-data marker present: {prohibited}")

if failures:
    print("Round-trip validation FAILED")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("Round-trip validation PASSED")
print("- saved Draft logical Data worksheet=1; grid=40x26; anchors=28")
print("- named_cells=43; unqualified=43; unique=43; exportable=43")
print("- destinations blank=43; writable=43; non_formula=43")
print("- first analyte=D2; no A2; no sdf; no prohibited destination")
print("- semantic comparison passed after normalizing only the regenerated renderer UUID")
print(f"- raw_export_sha256={ROUND_TRIP_SHA256}")
