#!/usr/bin/env python3
"""Validate renderer, calculation, and runtime configuration contracts for Test v3."""

from __future__ import annotations

import hashlib
import copy
import json
import re
from pathlib import Path
from typing import Any

import build_phase3_candidates as phase3_builder
import build_phase3_candidates_v3 as v3_builder
import validate_phase3_candidates as phase3_validator
import validate_phase3_candidates_v2 as v2_validator


PACKAGE_DIR = Path(__file__).resolve().parent
TEST_PATH = v3_builder.TEST_OUTPUT
V2_PATH = phase3_builder.OUTPUT_DIR / "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v2.json"
UNRESOLVED = v3_builder.UNRESOLVED


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def worksheet(candidate: dict[str, Any], name: str) -> dict[str, Any]:
    return next(item for item in candidate["config"]["worksheets"] if item["worksheetName"] == name)


def formula_count(candidate: dict[str, Any]) -> int:
    return sum(
        isinstance(value, str) and value.startswith("=")
        for sheet in candidate["config"]["worksheets"]
        for row in sheet["data"]
        for value in row
    )


def exact_destination_contract(candidate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    named = candidate["qb_config"]["named_cells"]
    if set(named) - {"report_results"} != set(phase3_builder.exact_test_named_cells()) - {"report_results"}:
        raise AssertionError("The exact 43 destination names changed")
    destinations = {name: value for name, value in named.items() if name != "report_results"}
    if len(destinations) != 43:
        raise AssertionError("Expected exactly 43 writable destinations")
    if len({item["cell"] for item in destinations.values()}) != 43:
        raise AssertionError("Destination addresses are not unique")
    data_cells = worksheet(candidate, "Data")["cells"]
    for name, definition in destinations.items():
        address = definition["cell"].split("!", 1)[1]
        if data_cells[address].get("readonly") is not False:
            raise AssertionError(f"Destination {name} is not writable")
        row = int(re.search(r"\d+$", address).group()) - 1
        letters = re.match(r"[A-Z]+", address).group()
        col = 0
        for char in letters:
            col = col * 26 + ord(char) - 64
        value = worksheet(candidate, "Data")["data"][row][col - 1]
        if value not in ("", None) or (isinstance(value, str) and value.startswith("=")):
            raise AssertionError(f"Destination {name} is not blank and non-formula")
        if definition["export"] is not True:
            raise AssertionError(f"Destination {name} is not exportable")
    return destinations


def validate_calculation_contract(candidate: dict[str, Any]) -> dict[str, Any]:
    """Run the Phase 3 scientific validator after normalizing only V3 bindings."""
    normalized = copy.deepcopy(candidate)
    specifications = worksheet(normalized, "Specifications")
    specifications["data"][1][20] = UNRESOLVED
    specifications["data"][3][20] = UNRESOLVED
    for row in specifications["data"]:
        for index, value in enumerate(row):
            if isinstance(value, str) and v3_builder.RESOLVED_FORMULA_GATE in value:
                row[index] = value.replace(
                    v3_builder.RESOLVED_FORMULA_GATE,
                    v3_builder.UNRESOLVED_FORMULA_GATE,
                )
    normalized["data"]["Specifications"] = copy.deepcopy(specifications["data"])
    return phase3_validator.validate_test_candidate(normalized)


def validate_runtime_configuration(candidate: dict[str, Any], profile: dict[str, str]) -> dict[str, Any]:
    v3_builder.validate_profile(profile)
    serialized = json.dumps(candidate, ensure_ascii=False)
    if UNRESOLVED in serialized:
        raise AssertionError("Runtime candidate contains an unresolved configuration marker")

    specifications = worksheet(candidate, "Specifications")
    data = specifications["data"]
    u2, u3, u4, u5 = data[1][20], data[2][20], data[3][20], data[4][20]
    if not isinstance(u2, str) or not u2.strip() or u2 == UNRESOLVED:
        raise AssertionError("Specifications!U2 store binding is unresolved")
    if u2 != profile["kv_store_binding"]:
        raise AssertionError("Specifications!U2 does not match the environment profile")
    if u3 != profile["assay_key"]:
        raise AssertionError("Specifications!U3 assay key differs from the environment profile")
    if not isinstance(u4, str) or not u4.strip() or u4 == UNRESOLVED:
        raise AssertionError("Specifications!U4 matrix binding is unresolved")
    if u4 != v3_builder.DYNAMIC_MATRIX_SOURCE or profile["matrix_binding_mode"] != "dynamic_test_matrix_reference":
        raise AssertionError("Specifications!U4 is a fixed matrix instead of the current Test matrix reference")
    if u5 != profile["result_unit"]:
        raise AssertionError("Specifications!U5 result unit differs from the environment profile")
    if worksheet(candidate, "Data")["data"][1][2] != v3_builder.DYNAMIC_MATRIX_SOURCE:
        raise AssertionError("Data!C2 no longer holds the proven Test matrix placeholder")

    lookup_formulas = [
        value
        for row in data
        for value in row
        if isinstance(value, str) and "GET_KVSTORE_VALUE" in value
    ]
    lookup_calls = sum(formula.count("GET_KVSTORE_VALUE") for formula in lookup_formulas)
    if len(lookup_formulas) != 44 or lookup_calls != 44:
        raise AssertionError(
            f"Expected 44 Key/Value formula cells containing 44 calls, found "
            f"{len(lookup_formulas)} cells and {lookup_calls} calls"
        )
    if any("$U$2" not in formula or "$U$4" not in formula for formula in lookup_formulas):
        raise AssertionError("A Key/Value lookup bypasses the configured U2/U4 bindings")
    if re.search(r"(?i)pass[_ /-]?fail", serialized):
        raise AssertionError("Pass/Fail is prohibited")
    if re.search(r"(?i)auto(?:matic)?[_ -]?(?:publish|qc review)", serialized):
        raise AssertionError("Automatic Publish or QC Review is prohibited")

    return {
        "kv_lookup_formula_cells": len(lookup_formulas),
        "kv_lookup_calls": lookup_calls,
        "matrix_source": profile["matrix_source_cell"],
        "unresolved_markers": 0,
    }


def validate_candidate(candidate: dict[str, Any], profile: dict[str, str]) -> dict[str, Any]:
    historical = load_json(phase3_validator.HISTORICAL_TEST_PATH)
    v2 = load_json(V2_PATH)
    v2_validator.validate_security(candidate, "Test v3")
    renderer = v2_validator.validate_renderer_contract(
        candidate,
        historical,
        {"Report": "Report", "Data": "Data", "Specifications": "Specifications"},
        "Test v3",
    )
    calculation = validate_calculation_contract(candidate)
    vectors = phase3_validator.validate_vectors()
    destinations = exact_destination_contract(candidate)
    runtime = validate_runtime_configuration(candidate, profile)

    if formula_count(candidate) != formula_count(v2):
        raise AssertionError("V3 formula count differs from renderer-proven V2")
    if candidate["qb_config"]["named_cells"]["report_results"] != {
        "cell": "Report!A1:E23",
        "display_name": "",
        "export": True,
    }:
        raise AssertionError("report_results changed")
    if len(candidate["qb_config"]["named_cells"]) != 44:
        raise AssertionError("Expected 44 named definitions")

    return {
        "renderer_contract": "passed",
        "calculation_contract": "passed",
        "runtime_configuration_contract": "passed",
        "formula_count": formula_count(candidate),
        "destination_count": len(destinations),
        "named_definition_count": len(candidate["qb_config"]["named_cells"]),
        "renderer": renderer,
        "calculation": calculation,
        "vectors": vectors,
        "runtime": runtime,
    }


def main() -> None:
    candidate = load_json(TEST_PATH)
    profile = v3_builder.load_profile()
    result = validate_candidate(candidate, profile)
    print(json.dumps({
        "renderer_contract": result["renderer_contract"],
        "calculation_contract": result["calculation_contract"],
        "runtime_configuration_contract": result["runtime_configuration_contract"],
        "formula_count": result["formula_count"],
        "destination_count": result["destination_count"],
        "named_definition_count": result["named_definition_count"],
        "kv_lookup_formula_cells": result["runtime"]["kv_lookup_formula_cells"],
        "kv_lookup_calls": result["runtime"]["kv_lookup_calls"],
        "unresolved_markers": result["runtime"]["unresolved_markers"],
        "test_v3_sha256": sha256(TEST_PATH),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
