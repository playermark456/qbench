#!/usr/bin/env python3
"""Validate the Terpenes V4 five-argument Key/Value lookup contract."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import build_phase3_candidates as phase3_builder
import build_phase3_candidates_v2 as v2_builder
import build_phase3_candidates_v3 as v3_builder
import build_phase3_candidates_v4 as v4_builder
import validate_phase3_candidates as phase3_validator
import validate_phase3_candidates_v2 as v2_validator
import validate_phase4a4_v3 as v3_validator


PACKAGE_DIR = Path(__file__).resolve().parent
TEST_PATH = (
    PACKAGE_DIR
    / "production_candidates"
    / "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v4_binding_fix.json"
)
DEPLOYMENT_CONTRACT_PATH = PACKAGE_DIR / "terpenes_deployment_contract.json"


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


def extract_lookup_calls(formula: str) -> list[str]:
    calls: list[str] = []
    marker = "GET_KVSTORE_VALUE("
    cursor = 0
    while True:
        start = formula.find(marker, cursor)
        if start < 0:
            break
        depth = 0
        quoted = False
        escaped = False
        for index in range(start, len(formula)):
            char = formula[index]
            if escaped:
                escaped = False
                continue
            if char == "\\" and quoted:
                escaped = True
                continue
            if char == '"':
                quoted = not quoted
            elif not quoted and char == "(":
                depth += 1
            elif not quoted and char == ")":
                depth -= 1
                if depth == 0:
                    calls.append(formula[start : index + 1])
                    cursor = index + 1
                    break
        else:
            raise AssertionError("Unclosed GET_KVSTORE_VALUE call")
    return calls


def split_call_arguments(call: str) -> list[str]:
    if not call.startswith("GET_KVSTORE_VALUE(") or not call.endswith(")"):
        raise AssertionError("Not a GET_KVSTORE_VALUE call")
    body = call[len("GET_KVSTORE_VALUE(") : -1]
    arguments: list[str] = []
    start = 0
    depth = 0
    quoted = False
    escaped = False
    for index, char in enumerate(body):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quoted:
            escaped = True
            continue
        if char == '"':
            quoted = not quoted
        elif not quoted and char == "(":
            depth += 1
        elif not quoted and char == ")":
            depth -= 1
        elif not quoted and depth == 0 and char == ",":
            arguments.append(body[start:index].strip())
            start = index + 1
    arguments.append(body[start:].strip())
    return arguments


def validate_lookup_call(call: str) -> tuple[str, str]:
    arguments = split_call_arguments(call)
    if len(arguments) != 5:
        raise AssertionError(f"Key/Value lookup must have exactly five arguments, found {len(arguments)}")
    if arguments[:3] != ["$U$2", "$U$3", "$U$4"]:
        raise AssertionError("Key/Value argument order must be store, scope, matrix, analyte, field")
    analyte = arguments[3]
    if not analyte or analyte in {"$U$2", "$U$3", "$U$4", "$U$5"}:
        raise AssertionError("Key/Value analyte argument is missing or misordered")
    if arguments[4] not in {'"LOQ"', '"MU"'}:
        raise AssertionError("Key/Value terminal field must be LOQ or MU")
    if "$U$5" in call:
        raise AssertionError("Result unit must not be a Key/Value lookup dimension")
    if "MU%" in call:
        raise AssertionError("MU% is not an allowed terminal field")
    if re.search(r"(?i)pass[_ /-]?fail", call):
        raise AssertionError("Pass/Fail is not an allowed terminal field")
    return analyte, arguments[4].strip('"')


def normalize_for_scientific_validator(candidate: dict[str, Any]) -> dict[str, Any]:
    normalized = copy.deepcopy(candidate)
    specifications = worksheet(normalized, "Specifications")

    def replacement(match: re.Match[str]) -> str:
        analyte = match.group(1)
        selector = "MU%" if match.group(2) == "MU" else "LOQ"
        return f'GET_KVSTORE_VALUE($U$2,$U$3,{analyte},$U$4,$U$5,"{selector}")'

    reverted = 0
    for row in specifications["data"]:
        for index, value in enumerate(row):
            if isinstance(value, str) and "GET_KVSTORE_VALUE" in value:
                value, count = v4_builder.FIVE_ARGUMENT_CALL.subn(replacement, value)
                reverted += count
                row[index] = value
    if reverted != 44:
        raise AssertionError(f"Expected to normalize 44 V4 lookup calls, normalized {reverted}")
    specifications["data"][5][20] = "LOQ / MU%"
    normalized["data"]["Specifications"] = copy.deepcopy(specifications["data"])
    return normalized


def validate_only_intended_v3_differences(
    candidate: dict[str, Any], v3_candidate: dict[str, Any]
) -> dict[str, int]:
    normalized = phase3_builder.replace_strings(
        copy.deepcopy(candidate),
        [
            (v4_builder.TEST_TARGET, v3_builder.TEST_TARGET),
            (v4_builder.TEST_VERSION, v3_builder.TEST_VERSION),
        ],
    )
    specifications = worksheet(normalized, "Specifications")
    v3_specifications = worksheet(v3_candidate, "Specifications")

    def replacement(match: re.Match[str]) -> str:
        analyte = match.group(1)
        selector = "MU%" if match.group(2) == "MU" else "LOQ"
        return f'GET_KVSTORE_VALUE($U$2,$U$3,{analyte},$U$4,$U$5,"{selector}")'

    reverted = 0
    for row in specifications["data"]:
        for index, value in enumerate(row):
            if isinstance(value, str) and "GET_KVSTORE_VALUE" in value:
                value, count = v4_builder.FIVE_ARGUMENT_CALL.subn(replacement, value)
                row[index] = value
                reverted += count
    specifications["data"][1][20] = v3_specifications["data"][1][20]
    specifications["data"][5][20] = v3_specifications["data"][5][20]
    normalized["data"]["Specifications"] = copy.deepcopy(specifications["data"])

    if normalized != v3_candidate:
        raise AssertionError("V4 contains changes beyond identity text, store binding, and lookup contract")
    return {"reverted_lookup_calls": reverted, "unexpected_differences": 0}


def validate_runtime_configuration(candidate: dict[str, Any], profile: dict[str, str]) -> dict[str, Any]:
    v4_builder.validate_profile(profile)
    serialized = json.dumps(candidate, ensure_ascii=False)
    if v3_builder.UNRESOLVED in serialized:
        raise AssertionError("Runtime candidate contains an unresolved configuration marker")

    specifications = worksheet(candidate, "Specifications")
    data = specifications["data"]
    u2, u3, u4, u5 = data[1][20], data[2][20], data[3][20], data[4][20]
    if u2 != profile["kv_store_binding"]:
        raise AssertionError("Specifications!U2 does not match the V4 environment profile")
    if u3 != "Terpenes" or u3 != profile["scope_key"]:
        raise AssertionError("Specifications!U3 must provide the Terpenes scope key")
    if u4 != v3_builder.DYNAMIC_MATRIX_SOURCE or u4 != profile["matrix_source"]:
        raise AssertionError("Specifications!U4 must provide the dynamic Test matrix")
    if u5 != "ug/g" or u5 != profile["result_unit"]:
        raise AssertionError("Specifications!U5 must remain informational ug/g")
    if data[5][20] != "LOQ / MU":
        raise AssertionError("Specifications selector description must be LOQ / MU")
    if worksheet(candidate, "Data")["data"][1][2] != v3_builder.DYNAMIC_MATRIX_SOURCE:
        raise AssertionError("Data!C2 no longer holds the dynamic Test matrix placeholder")

    lookup_formulas = [
        value
        for row in data
        for value in row
        if isinstance(value, str) and "GET_KVSTORE_VALUE" in value
    ]
    calls = [call for formula in lookup_formulas for call in extract_lookup_calls(formula)]
    if len(lookup_formulas) != 44 or len(calls) != 44:
        raise AssertionError(
            f"Expected 44 Key/Value formula cells and calls, found {len(lookup_formulas)} cells and {len(calls)} calls"
        )
    validated = [validate_lookup_call(call) for call in calls]
    terminal_counts = {
        "LOQ": sum(field == "LOQ" for _, field in validated),
        "MU": sum(field == "MU" for _, field in validated),
    }
    if terminal_counts != {"LOQ": 21, "MU": 23}:
        raise AssertionError(f"Unexpected terminal-field counts: {terminal_counts}")
    if "MU%" in "".join(calls):
        raise AssertionError("A V4 formula still requests MU%")
    if any("$U$5" in call for call in calls):
        raise AssertionError("A V4 formula still passes the result unit")
    if re.search(r"(?i)pass[_ /-]?fail", serialized):
        raise AssertionError("Pass/Fail is prohibited")
    if re.search(r"(?i)auto(?:matic)?[_ -]?(?:publish|qc review)", serialized):
        raise AssertionError("Automatic Publish or QC Review is prohibited")

    return {
        "kv_lookup_formula_cells": len(lookup_formulas),
        "kv_lookup_calls": len(calls),
        "loq_calls": terminal_counts["LOQ"],
        "mu_calls": terminal_counts["MU"],
        "argument_count": 5,
        "matrix_source": profile["matrix_source_cell"],
        "unresolved_markers": 0,
    }


def validate_deployment_contract(contract: dict[str, Any]) -> dict[str, str]:
    if contract.get("worksheet_json_contract") != "passed":
        raise AssertionError("Terpenes worksheet JSON contract must pass before deployment")
    if contract.get("qbench_shell_type") != "dynamic_spreadsheet":
        raise AssertionError("Terpenes deployment requires dynamic_spreadsheet QBench shell type")
    if contract.get("allowed_qbench_shell_types") != ["dynamic_spreadsheet"]:
        raise AssertionError("Only dynamic_spreadsheet may be an allowed Terpenes QBench shell type")
    if "spreadsheet" not in contract.get("rejected_qbench_shell_types", []):
        raise AssertionError("Regular spreadsheet must be explicitly rejected for Terpenes deployment")
    pre_import = contract.get("pre_import_gate", {})
    if pre_import.get("verify_in_qbench_worksheets_list") is not True:
        raise AssertionError("Future imports must verify the QBench Worksheets list")
    if pre_import.get("required_visible_type") != "Dynamic Spreadsheet":
        raise AssertionError("Future imports must visibly confirm Dynamic Spreadsheet type")
    for surface in ("test_worksheet", "batch_worksheet"):
        if contract.get(surface, {}).get("qbench_shell_type") != "dynamic_spreadsheet":
            raise AssertionError(f"{surface} requires dynamic_spreadsheet QBench shell type")
    runtime = contract.get("sandbox_runtime_contract")
    if runtime not in {
        "passed",
        "passed_version_2_runtime_vector",
        "blocked_required_kv_lookup_blank",
        "not_started",
    }:
        raise AssertionError("Unsupported Sandbox runtime-contract classification")
    return {
        "worksheet_json_contract": "passed",
        "qbench_shell_type": "dynamic_spreadsheet",
        "sandbox_runtime_contract": runtime,
    }


def validate_candidate(candidate: dict[str, Any], profile: dict[str, str]) -> dict[str, Any]:
    historical = load_json(phase3_validator.HISTORICAL_TEST_PATH)
    v3_candidate = load_json(v3_builder.TEST_OUTPUT)
    v2_validator.validate_security(candidate, "Test v4")
    renderer = v2_validator.validate_renderer_contract(
        candidate,
        historical,
        {"Report": "Report", "Data": "Data", "Specifications": "Specifications"},
        "Test v4",
    )
    calculation = v3_validator.validate_calculation_contract(normalize_for_scientific_validator(candidate))
    vectors = phase3_validator.validate_vectors()
    destinations = v3_validator.exact_destination_contract(candidate)
    runtime = validate_runtime_configuration(candidate, profile)
    difference_contract = validate_only_intended_v3_differences(candidate, v3_candidate)
    deployment = validate_deployment_contract(load_json(DEPLOYMENT_CONTRACT_PATH))

    if formula_count(candidate) != formula_count(v3_candidate) or formula_count(candidate) != 309:
        raise AssertionError("V4 formula count differs from renderer-proven V3")
    if candidate["qb_config"]["named_cells"] != v3_candidate["qb_config"]["named_cells"]:
        raise AssertionError("V4 named definitions differ from V3")
    if candidate["qb_config"]["named_cells"]["report_results"] != {
        "cell": "Report!A1:E23",
        "display_name": "",
        "export": True,
    }:
        raise AssertionError("report_results changed")
    if len(candidate["qb_config"]["named_cells"]) != 44:
        raise AssertionError("Expected 44 named definitions")
    if v2_builder.renderer_identity(candidate) != v2_builder.renderer_identity(v3_candidate):
        raise AssertionError("Renderer namespace or worksheet identifiers changed")

    return {
        "renderer_contract": "passed",
        "calculation_contract": "passed",
        "lookup_contract": "passed_proven_five_argument_hierarchy",
        "formula_count": formula_count(candidate),
        "destination_count": len(destinations),
        "named_definition_count": len(candidate["qb_config"]["named_cells"]),
        "renderer": renderer,
        "calculation": calculation,
        "vectors": vectors,
        "runtime": runtime,
        "difference_contract": difference_contract,
        "deployment": deployment,
    }


def main() -> None:
    candidate = load_json(TEST_PATH)
    profile = v4_builder.load_profile()
    result = validate_candidate(candidate, profile)
    print(json.dumps({
        "calculation_contract": result["calculation_contract"],
        "destination_count": result["destination_count"],
        "formula_count": result["formula_count"],
        "kv_lookup_argument_count": result["runtime"]["argument_count"],
        "kv_lookup_calls": result["runtime"]["kv_lookup_calls"],
        "loq_calls": result["runtime"]["loq_calls"],
        "lookup_contract": result["lookup_contract"],
        "mu_calls": result["runtime"]["mu_calls"],
        "named_definition_count": result["named_definition_count"],
        "unexpected_v3_differences": result["difference_contract"]["unexpected_differences"],
        "renderer_contract": result["renderer_contract"],
        "qbench_shell_type": result["deployment"]["qbench_shell_type"],
        "sandbox_runtime_contract": result["deployment"]["sandbox_runtime_contract"],
        "test_v4_sha256": sha256(TEST_PATH),
        "unresolved_markers": result["runtime"]["unresolved_markers"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
