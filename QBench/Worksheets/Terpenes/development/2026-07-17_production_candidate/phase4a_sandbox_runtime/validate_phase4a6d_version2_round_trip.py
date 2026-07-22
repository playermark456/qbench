#!/usr/bin/env python3
"""Compare user-created Version 2 with the deterministic binding-fix build."""

from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path
from typing import Any

from validate_phase4a3_round_trip import compare_round_trip, load_json


def validate_kvstore_config(candidate: dict[str, Any], exported: dict[str, Any]) -> dict[str, Any]:
    candidate_config = candidate["qb_config"].get("kvstore_config")
    exported_config = exported["qb_config"].get("kvstore_config")
    if candidate_config not in ({}, None):
        raise AssertionError("Deterministic candidate unexpectedly embeds QBench store data")
    if not isinstance(exported_config, dict) or len(exported_config) != 1:
        raise AssertionError("Version 2 must embed exactly one associated scientific store")

    binding = exported["data"]["Specifications"][1][20]
    if list(exported_config) != [binding]:
        raise AssertionError("Embedded store key does not match Specifications!U2")
    hierarchy = exported_config[binding]
    if list(hierarchy) != ["Terpenes"]:
        raise AssertionError("Embedded store must have only the Terpenes scope")
    matrices = hierarchy["Terpenes"]
    if list(matrices) != ["Cannabis Concentrates"]:
        raise AssertionError("Embedded store must have only the validated runtime matrix")
    analytes = matrices["Cannabis Concentrates"]

    expected = {
        ("Alpha-Pinene", "LOQ"): 10,
        ("Alpha-Pinene", "MU"): 5,
        ("Ocimene", "LOQ"): 10,
        ("Ocimene 1", "MU"): 4,
        ("Ocimene 2", "MU"): 8,
        ("Nerolidol", "LOQ"): 10,
        ("Nerolidol 1", "MU"): 7,
        ("Nerolidol 2", "MU"): 11,
    }
    for (analyte, field), expected_value in expected.items():
        if analytes.get(analyte, {}).get(field) != expected_value:
            raise AssertionError(f"Unexpected embedded value for {analyte} {field}")

    serialized = json.dumps(exported_config, ensure_ascii=False)
    if '"MU%"' in serialized or re.search(r"(?i)pass[_ /-]?fail", serialized):
        raise AssertionError("Prohibited Key/Value terminal field is present")
    if re.search(r'(?i)"(?:unit|ug/g)"\s*:', serialized):
        raise AssertionError("A prohibited unit hierarchy is present")
    return {
        "embedded_store_count": 1,
        "embedded_scope": "Terpenes",
        "embedded_matrix": "Cannabis Concentrates",
        "representative_values": "passed_8_of_8",
    }


def compare_version2(candidate: dict[str, Any], exported: dict[str, Any]) -> dict[str, Any]:
    store_result = validate_kvstore_config(candidate, exported)
    normalized_candidate = copy.deepcopy(candidate)
    normalized_candidate["qb_config"]["kvstore_config"] = copy.deepcopy(
        exported["qb_config"]["kvstore_config"]
    )
    candidate_specifications = next(
        sheet
        for sheet in normalized_candidate["config"]["worksheets"]
        if sheet["worksheetName"] == "Specifications"
    )
    exported_specifications = next(
        sheet
        for sheet in exported["config"]["worksheets"]
        if sheet["worksheetName"] == "Specifications"
    )
    exported_u2_readonly = exported_specifications["cells"]["U2"]["readonly"]
    candidate_specifications["cells"]["U2"]["readonly"] = exported_u2_readonly
    result = compare_round_trip(normalized_candidate, exported)
    result["version_2_round_trip"] = "passed_with_expected_qbench_normalization"
    result["qbench_embedded_store_normalization"] = store_result
    result["store_binding_cell_protection"] = (
        "passed_readonly"
        if exported_u2_readonly is True
        else "runtime_proof_allowed_but_final_hardening_required"
    )
    return result


def main() -> None:
    runtime_dir = Path(__file__).resolve().parent
    candidate_dir = runtime_dir.parent / "production_candidates"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--candidate",
        type=Path,
        default=candidate_dir
        / "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v4_binding_fix.json",
    )
    parser.add_argument("--export", type=Path, required=True)
    args = parser.parse_args()
    result = compare_version2(load_json(args.candidate), load_json(args.export))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
