#!/usr/bin/env python3
"""Build Sandbox Test v4 with the proven five-argument Key/Value contract."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any

import build_phase3_candidates as phase3
import build_phase3_candidates_v2 as v2
import build_phase3_candidates_v3 as v3


PACKAGE_DIR = Path(__file__).resolve().parent
PROFILE_PATH = PACKAGE_DIR / "sandbox_runtime_profile_v4.local.json"
TEST_TARGET = "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS_V4"
TEST_VERSION = "Terpenes Production Candidate Test Worksheet v4"
TEST_OUTPUT = phase3.OUTPUT_DIR / "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v4.json"

FIVE_ARGUMENT_CALL = re.compile(
    r'GET_KVSTORE_VALUE\(\$U\$2,\$U\$3,\$U\$4,([^,]+),"(LOQ|MU)"\)'
)
SIX_ARGUMENT_CALL = re.compile(
    r'GET_KVSTORE_VALUE\(\$U\$2,\$U\$3,([^,]+),\$U\$4,\$U\$5,"(LOQ|MU%)"\)'
)


def load_profile(path: Path = PROFILE_PATH) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_profile(profile: dict[str, str]) -> None:
    required = {
        "kv_store_binding",
        "kv_store_binding_classification",
        "scope_key",
        "matrix_binding_mode",
        "matrix_source",
        "matrix_source_cell",
        "result_unit",
    }
    if set(profile) != required:
        raise AssertionError(f"Runtime profile keys must be exactly {sorted(required)}")

    binding = profile["kv_store_binding"].strip()
    if not binding or binding == v3.UNRESOLVED:
        raise AssertionError("kv_store_binding must be a nonblank resolved Sandbox binding")
    if profile["kv_store_binding_classification"] != "another_non_secret_visible_identifier":
        raise AssertionError("kv_store_binding classification is not the visible association identifier")
    if profile["scope_key"] != "Terpenes":
        raise AssertionError("scope_key must be Terpenes")
    if profile["matrix_binding_mode"] != "dynamic_test_matrix_reference":
        raise AssertionError("V4 must use the current Test matrix dynamically")
    if profile["matrix_source"] != v3.DYNAMIC_MATRIX_SOURCE:
        raise AssertionError("matrix_source must dynamically reference the current Test sample matrix")
    if profile["matrix_source_cell"] != v3.DYNAMIC_MATRIX_SOURCE_CELL:
        raise AssertionError("matrix_source_cell must remain Data!C2")
    if profile["result_unit"] != "ug/g":
        raise AssertionError("result_unit must remain informational ug/g")


def convert_formula_to_five_arguments(value: Any) -> tuple[Any, int]:
    if not isinstance(value, str) or "GET_KVSTORE_VALUE" not in value:
        return value, 0

    def replacement(match: re.Match[str]) -> str:
        analyte = match.group(1)
        terminal = "MU" if match.group(2) == "MU%" else "LOQ"
        return f'GET_KVSTORE_VALUE($U$2,$U$3,$U$4,{analyte},"{terminal}")'

    converted, count = SIX_ARGUMENT_CALL.subn(replacement, value)
    if count != value.count("GET_KVSTORE_VALUE"):
        raise AssertionError(f"A V3 lookup formula did not match the proven conversion pattern: {value}")
    return converted, count


def build_candidate(profile: dict[str, str] | None = None) -> dict[str, Any]:
    runtime_profile = copy.deepcopy(profile if profile is not None else load_profile())
    validate_profile(runtime_profile)

    test_builder = phase3.load_module("phase3_v4_test_builder_base", phase3.TEST_BUILDER_PATH)
    historical_test = test_builder.build_candidate()
    candidate = phase3.build_test_candidate(
        test_builder,
        target_name=TEST_TARGET,
        version_name=TEST_VERSION,
        preserve_historical_identity=True,
    )

    data_sheet = phase3.worksheet_by_name(candidate, "Data")
    if data_sheet["data"][1][2] != v3.DYNAMIC_MATRIX_SOURCE:
        raise AssertionError("The proven Data!C2 Test matrix placeholder changed")

    specifications = phase3.worksheet_by_name(candidate, "Specifications")
    specifications["data"][1][20] = runtime_profile["kv_store_binding"]
    specifications["data"][2][20] = runtime_profile["scope_key"]
    specifications["data"][3][20] = runtime_profile["matrix_source"]
    specifications["data"][4][20] = runtime_profile["result_unit"]
    specifications["data"][5][20] = "LOQ / MU"

    converted_calls = 0
    for row in specifications["data"]:
        for index, value in enumerate(row):
            if isinstance(value, str) and v3.UNRESOLVED_FORMULA_GATE in value:
                value = value.replace(v3.UNRESOLVED_FORMULA_GATE, v3.RESOLVED_FORMULA_GATE)
            value, count = convert_formula_to_five_arguments(value)
            row[index] = value
            converted_calls += count

    if converted_calls != 44:
        raise AssertionError(f"Expected to convert 44 V3 lookup calls, converted {converted_calls}")
    candidate["data"]["Specifications"] = copy.deepcopy(specifications["data"])

    if v2.renderer_identity(candidate) != v2.renderer_identity(historical_test):
        raise AssertionError("Test v4 did not preserve the renderer-proven historical identity")
    serialized = json.dumps(candidate, ensure_ascii=False)
    if v3.UNRESOLVED in serialized:
        raise AssertionError("Test v4 retained an unresolved runtime configuration marker")
    return candidate


def main() -> None:
    candidate = build_candidate()
    phase3.dump_json(TEST_OUTPUT, candidate)
    print(f"built_test_v4={TEST_OUTPUT.relative_to(phase3.REPO_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
