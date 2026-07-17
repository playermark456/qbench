#!/usr/bin/env python3
"""Validate the corrected legacy JSON scalar candidate."""
from __future__ import annotations

import copy
import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = (
    HERE
    / "source"
    / "2026-07-17_SBX_ONLY_TERPENES_NATIVE_SCALAR_43_FIELD_BASE_working_native_export_spreadsheet.json"
)
CANDIDATE = HERE / "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE.json"
PRIOR_QUALIFIED = (
    HERE
    / "prior_qualified_candidate"
    / "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE_qualified_addresses.json"
)
MAPPING = ROOT / "config" / "field_mapping_scalar_candidate.csv"
SOURCE_SHA256 = "d86e05122bc9a7fc4b6937e5582d9ff469f15c234e606fc0c5bbdd7d7c3659e5"
PRIOR_QUALIFIED_SHA256 = "54a65e029b9f1a038a21428cf40727896130db86041fafcc2d0bdf868e7fe35b"
CANDIDATE_RENDERER_UUID = "051174c5-a7da-4b6d-afc5-0c2addc1a900"
ROWS = 40
COLS = 26
UUID_PATTERN = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
    re.IGNORECASE,
)


def fail(message: str) -> None:
    failures.append(message)


def address_parts(address: str) -> tuple[int, int, str]:
    match = re.fullmatch(r"([A-Z]+)([1-9][0-9]*)", address)
    if not match:
        raise ValueError(address)
    column = 0
    for character in match.group(1):
        column = column * 26 + ord(character) - 64
    return int(match.group(2)) - 1, column - 1, address


def is_formula_owned(cell: dict[str, Any]) -> bool:
    value = cell.get("value")
    if isinstance(value, str) and value.startswith("="):
        return True

    def walk(item: Any) -> bool:
        if isinstance(item, dict):
            for key, nested in item.items():
                if str(key).lower() in {"formula", "formulas"}:
                    return True
                if walk(nested):
                    return True
        elif isinstance(item, list):
            return any(walk(nested) for nested in item)
        return False

    return walk(cell.get("meta_data", {}))


def is_read_only(cell: dict[str, Any]) -> bool:
    def walk(item: Any) -> bool:
        if isinstance(item, dict):
            for key, nested in item.items():
                if str(key).lower() == "readonly" and nested not in (False, None, "false", 0):
                    return True
                if walk(nested):
                    return True
        elif isinstance(item, list):
            return any(walk(nested) for nested in item)
        return False

    return walk(cell.get("meta_data", {}))


def replace_uuid(item: Any, old: str, new: str) -> Any:
    if isinstance(item, dict):
        return {key: replace_uuid(value, old, new) for key, value in item.items()}
    if isinstance(item, list):
        return [replace_uuid(value, old, new) for value in item]
    if isinstance(item, str):
        return item.replace(old, new)
    return item


failures: list[str] = []

if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA256:
    fail("working native export bytes or SHA-256 changed")
if hashlib.sha256(PRIOR_QUALIFIED.read_bytes()).hexdigest() != PRIOR_QUALIFIED_SHA256:
    fail("prior successfully rendered qualified-address candidate changed")

try:
    source = json.loads(SOURCE.read_text(encoding="utf-8-sig"))
    candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))
    prior_qualified = json.loads(PRIOR_QUALIFIED.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as error:
    print(f"JSON candidate validation FAILED: {error}")
    raise SystemExit(1)

if set(source) != {"table_config", "qb_config"}:
    fail("working native export is not the legacy table_config/qb_config envelope")
if set(candidate) != {"table_config", "qb_config"}:
    fail("corrected candidate does not preserve the legacy native envelope")
if "config" in source or "config" in candidate:
    fail("a newer config object was introduced into the legacy native envelope")
if "data" in source or "data" in candidate:
    fail("a duplicate top-level Data representation was introduced")

source_table = source.get("table_config", {})
table = candidate.get("table_config", {})
source_grid = source_table.get("cell_settings", [])
grid = table.get("cell_settings", [])
if len(grid) != ROWS or any(len(row) != COLS for row in grid):
    fail("legacy logical Data worksheet is not exactly 40x26")
defaults = table.get("default_settings", {})
if len(defaults.get("rowHeights", [])) != ROWS:
    fail("native row settings are not exactly 40 rows")
if len(defaults.get("colWidths", [])) != COLS:
    fail("native column settings are not exactly 26 columns")
if table.get("default_settings") != source_table.get("default_settings"):
    fail("native default row/column settings changed")
if table.get("plugin_settings") != source_table.get("plugin_settings"):
    fail("native plugin settings changed")

with MAPPING.open(newline="", encoding="utf-8") as handle:
    mapping = list(csv.DictReader(handle))
if len(mapping) != 43:
    fail(f"expected 43 mapping rows, found {len(mapping)}")
if any(not row["destination_cell"].startswith("Data!") for row in mapping):
    fail("logical mapping does not refer exclusively to the Data worksheet")

expected = {
    row["destination_named_cell"]: {
        "cell": row["destination_cell"].split("!", 1)[1],
        "display_name": row["source_header"],
        "export": True,
    }
    for row in mapping
}
named = candidate.get("qb_config", {}).get("named_cells", {})
if named != expected:
    fail("named-cell contract is not exactly the validated 43-field mapping")
if len(named) != 43:
    fail(f"expected 43 named cells, found {len(named)}")
if "sdf" in named:
    fail("diagnostic named cell sdf remains")
if any("[" in name or "]" in name for name in named):
    fail("bracketed destination name present")
addresses = [entry.get("cell") for entry in named.values()]
if len(addresses) != len(set(addresses)):
    fail("duplicate destination address present")
if any(not isinstance(address, str) or "!" in address for address in addresses):
    fail("one or more JSON named-cell addresses are sheet-qualified")

expected_analyte_names = [f"terpenes_instrument_conc_{index:02d}" for index in range(1, 24)]
expected_analyte_addresses = [f"{chr(68 + index)}2" for index in range(23)]
analyte_names = [name for name in named if name.startswith("terpenes_instrument_conc_")]
if analyte_names != expected_analyte_names:
    fail("analyte names are not exactly _01 through _23")
if [named[name]["cell"] for name in expected_analyte_names] != expected_analyte_addresses:
    fail("analyte JSON destinations are not exactly unqualified D2:Z2")
if named.get("terpenes_instrument_conc_01", {}).get("cell") != "D2":
    fail("first analyte is not exactly D2")
if any(address == "A2" for address in addresses):
    fail("prohibited A2 mapping is present")

remaining_names = [row["destination_named_cell"] for row in mapping[23:]]
expected_remaining_address_set = set(
    [f"B{row}" for row in range(12, 19)]
    + ["B22", "B23"]
    + [f"B{row}" for row in range(28, 39)]
)
if {named[name]["cell"] for name in remaining_names} != expected_remaining_address_set:
    fail("remaining 20 JSON destinations do not match the expected B-column rows")
for name, expected_address in {
    "terpenes_instrument_conc_01": "D2",
    "terpenes_instrument_conc_12": "O2",
    "terpenes_instrument_conc_23": "Z2",
    "sample_mass_g": "B12",
    "batch_qc_disposition": "B22",
    "publish_ready": "B23",
    "source_file_hash": "B30",
}.items():
    if named.get(name, {}).get("cell") != expected_address:
        fail(f"required compatibility mapping differs: {name} != {expected_address}")

destination_locals: set[str] = set()
for name, entry in named.items():
    try:
        row_index, column_index, local = address_parts(str(entry.get("cell", "")))
    except ValueError:
        fail(f"invalid unqualified address for {name}")
        continue
    if row_index >= ROWS or column_index >= COLS:
        fail(f"out-of-range address for {name}")
        continue
    destination_locals.add(local)
    cell = grid[row_index][column_index]
    if cell.get("value") not in ("", None):
        fail(f"destination is not blank: {name}")
    if is_formula_owned(cell):
        fail(f"destination is formula-owned: {name}")
    if is_read_only(cell):
        fail(f"destination is read-only: {name}")
    if entry.get("export") is not True:
        fail(f"destination is not exportable: {name}")

anchors: dict[str, str] = {
    "A1": "Terpenes JSON scalar 43-field base",
    "A12": "Preparation and calculation inputs",
    "A22": "Controlled disposition",
    "A28": "Source and audit metadata",
    "A40": "End of worksheet",
}
for index, row in enumerate(mapping[:23]):
    anchors[f"{chr(68 + index)}1"] = row["source_header"]
for address, expected_value in anchors.items():
    row_index, column_index, _ = address_parts(address)
    if grid[row_index][column_index].get("value") != expected_value:
        fail(f"required visible anchor missing or changed at {address}")
if len(anchors) != 28:
    fail("required anchor count is not 28")

# Normalize only the explicitly allowed value and named-cell changes. Any
# remaining difference means native structure, metadata, sizing, or content drifted.
source_uuid_values = set(UUID_PATTERN.findall(json.dumps(source)))
candidate_uuid_values = set(UUID_PATTERN.findall(json.dumps(candidate)))
if len(source_uuid_values) != 1:
    fail(f"expected one native renderer UUID, found {len(source_uuid_values)}")
if candidate_uuid_values != {CANDIDATE_RENDERER_UUID}:
    fail("corrected candidate does not contain exactly the fresh renderer UUID")
if source_uuid_values & candidate_uuid_values:
    fail("corrected candidate reused the source renderer UUID")
source_uuid = next(iter(source_uuid_values), "")
normalized_source = replace_uuid(copy.deepcopy(source), source_uuid, CANDIDATE_RENDERER_UUID)
normalized_source["qb_config"]["named_cells"] = copy.deepcopy(named)
for address in set(anchors) | destination_locals:
    row_index, column_index, _ = address_parts(address)
    normalized_source["table_config"]["cell_settings"][row_index][column_index]["value"] = (
        grid[row_index][column_index].get("value")
    )
if normalized_source != candidate:
    fail("candidate contains changes beyond named cells and required anchor/destination values")

# The prior qualified-address candidate rendered correctly. Prove that this
# regeneration changes only the 43 runtime address strings under named_cells.
normalized_prior = copy.deepcopy(prior_qualified)
prior_named = normalized_prior.get("qb_config", {}).get("named_cells", {})
address_change_count = 0
for name, entry in named.items():
    old_entry = prior_named.get(name)
    if not isinstance(old_entry, dict):
        fail(f"prior qualified candidate is missing named cell: {name}")
        continue
    if old_entry.get("cell") != f"Data!{entry['cell']}":
        fail(f"prior logical/runtime address pair is incorrect for {name}")
    if {key: value for key, value in old_entry.items() if key != "cell"} != {
        key: value for key, value in entry.items() if key != "cell"
    }:
        fail(f"non-address named-cell metadata changed for {name}")
    normalized_prior["qb_config"]["named_cells"][name]["cell"] = entry["cell"]
    address_change_count += 1
if address_change_count != 43:
    fail(f"expected 43 address-format changes, found {address_change_count}")
if normalized_prior != candidate:
    fail("rendered worksheet structure changed beyond the 43 address strings")

contract_text = json.dumps(named, ensure_ascii=False, sort_keys=True).lower()
for prohibited in (
    "pass_fail",
    "pass/fail",
    "pass fail",
    "result_status",
    "dimethylacetamide",
    "peak table",
    "peak_table",
):
    if prohibited in contract_text:
        fail(f"prohibited reportable field present: {prohibited}")

serialized = json.dumps(candidate, ensure_ascii=False, sort_keys=True).lower()
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
        fail(f"credential, token, signed URL, or customer-data marker present: {prohibited}")
if source_uuid and source_uuid.lower() in serialized:
    fail("source-specific renderer UUID remains in corrected legacy candidate")

if failures:
    print("JSON candidate validation FAILED")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

nonempty_count = sum(
    cell.get("value") not in ("", None) for row in grid for cell in row
)
digest = hashlib.sha256(CANDIDATE.read_bytes()).hexdigest()
print("JSON candidate validation PASSED")
print("- exactly one legacy logical Data worksheet; native envelope preserved")
print(f"- grid={ROWS}x{COLS}; anchors={len(anchors)}; nonempty_cells={nonempty_count}")
print(f"- named_cells={len(named)}; analytes={len(analyte_names)}")
print("- all 43 JSON named-cell addresses are unqualified; analytes=D2:Z2; no A2")
print("- all destinations resolve, are blank, writable, unique, non-formula, and exportable")
print("- rendered worksheet structure unchanged; exactly 43 cell strings changed")
print("- config.style/config.worksheets/top-level data remain absent exactly as in native reference")
print("- source renderer UUID replaced; no sdf, Pass/Fail, prohibited destination, credential, or customer-data marker")
print(f"- sha256={digest}")
