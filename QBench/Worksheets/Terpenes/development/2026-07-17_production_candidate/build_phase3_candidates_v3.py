#!/usr/bin/env python3
"""Build the Sandbox Test v3 candidate with explicit runtime bindings."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import build_phase3_candidates as phase3
import build_phase3_candidates_v2 as v2


PACKAGE_DIR = Path(__file__).resolve().parent
PROFILE_PATH = PACKAGE_DIR / "sandbox_runtime_profile_v3.json"
TEST_TARGET = "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS_V3"
TEST_VERSION = "Terpenes Production Test Worksheet v3"
TEST_OUTPUT = phase3.OUTPUT_DIR / "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v3.json"

UNRESOLVED = "SANDBOX_CONFIGURATION_REQUIRED"
DYNAMIC_MATRIX_SOURCE = "${test.sample.product_matrix}"
DYNAMIC_MATRIX_SOURCE_CELL = "Data!C2"
UNRESOLVED_FORMULA_GATE = 'OR($U$2="SANDBOX_CONFIGURATION_REQUIRED",$U$4="SANDBOX_CONFIGURATION_REQUIRED")'
RESOLVED_FORMULA_GATE = 'OR($U$2="",$U$4="")'


def load_profile(path: Path = PROFILE_PATH) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_profile(profile: dict[str, str]) -> None:
    required = {
        "kv_store_binding",
        "kv_store_binding_classification",
        "assay_key",
        "matrix_binding_mode",
        "matrix_source",
        "matrix_source_cell",
        "result_unit",
    }
    if set(profile) != required:
        raise AssertionError(f"Runtime profile keys must be exactly {sorted(required)}")

    binding = profile["kv_store_binding"].strip()
    if not binding or binding == UNRESOLVED:
        raise AssertionError("kv_store_binding must be a nonblank resolved Sandbox binding")
    if profile["kv_store_binding_classification"] != "another_non_secret_visible_identifier":
        raise AssertionError("kv_store_binding classification is not the visually proven association identifier")
    if profile["assay_key"] != "Terpenes":
        raise AssertionError("assay_key must be Terpenes")
    if profile["matrix_binding_mode"] != "dynamic_test_matrix_reference":
        raise AssertionError("The general Test worksheet must not use a fixed one-matrix binding")
    if not profile["matrix_source"].strip() or profile["matrix_source"] == UNRESOLVED:
        raise AssertionError("matrix_source must be resolved")
    if profile["matrix_source"] != DYNAMIC_MATRIX_SOURCE:
        raise AssertionError("matrix_source must dynamically reference the current Test sample matrix")
    if profile["matrix_source_cell"] != DYNAMIC_MATRIX_SOURCE_CELL:
        raise AssertionError("matrix_source_cell must remain the proven Data!C2 field")
    if profile["result_unit"] != "ug/g":
        raise AssertionError("result_unit must be ug/g")


def build_candidate(profile: dict[str, str] | None = None) -> dict[str, Any]:
    runtime_profile = copy.deepcopy(profile if profile is not None else load_profile())
    validate_profile(runtime_profile)

    test_builder = phase3.load_module("phase3_v3_test_builder_base", phase3.TEST_BUILDER_PATH)
    historical_test = test_builder.build_candidate()
    candidate = phase3.build_test_candidate(
        test_builder,
        target_name=TEST_TARGET,
        version_name=TEST_VERSION,
        preserve_historical_identity=True,
    )

    data_sheet = phase3.worksheet_by_name(candidate, "Data")
    if data_sheet["data"][1][2] != DYNAMIC_MATRIX_SOURCE:
        raise AssertionError("The proven Data!C2 Test matrix placeholder changed")

    specifications = phase3.worksheet_by_name(candidate, "Specifications")
    specifications["data"][1][20] = runtime_profile["kv_store_binding"]
    specifications["data"][2][20] = runtime_profile["assay_key"]
    specifications["data"][3][20] = runtime_profile["matrix_source"]
    specifications["data"][4][20] = runtime_profile["result_unit"]
    for row in specifications["data"]:
        for index, value in enumerate(row):
            if isinstance(value, str) and UNRESOLVED_FORMULA_GATE in value:
                row[index] = value.replace(UNRESOLVED_FORMULA_GATE, RESOLVED_FORMULA_GATE)
    candidate["data"]["Specifications"] = copy.deepcopy(specifications["data"])

    if v2.renderer_identity(candidate) != v2.renderer_identity(historical_test):
        raise AssertionError("Test v3 did not preserve the renderer-proven historical identity")
    if UNRESOLVED in json.dumps(candidate, ensure_ascii=False):
        raise AssertionError("Test v3 retained an unresolved runtime configuration marker")
    return candidate


def main() -> None:
    candidate = build_candidate()
    phase3.dump_json(TEST_OUTPUT, candidate)
    print(f"built_test_v3={TEST_OUTPUT.relative_to(phase3.REPO_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
