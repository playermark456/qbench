#!/usr/bin/env python3
"""Validate the exact V4-to-binding-fix delta and deployment binding gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import build_phase3_candidates_v4 as v4_builder
import build_phase4a6c_binding_fix as binding_builder
import validate_phase4a6_v4 as v4_validator


PACKAGE_DIR = Path(__file__).resolve().parent
ASSOCIATION_EVIDENCE_PATH = (
    PACKAGE_DIR
    / "phase4a_sandbox_runtime/phase4a6c_store_binding_comparison.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def differences(left: Any, right: Any, path: str = "") -> list[str]:
    if type(left) is not type(right):
        return [path]
    if isinstance(left, dict):
        if set(left) != set(right):
            return [path]
        result: list[str] = []
        for key in left:
            result.extend(differences(left[key], right[key], f"{path}.{key}" if path else key))
        return result
    if isinstance(left, list):
        if len(left) != len(right):
            return [path]
        result = []
        for index, (left_item, right_item) in enumerate(zip(left, right)):
            result.extend(differences(left_item, right_item, f"{path}[{index}]"))
        return result
    return [] if left == right else [path]


def formula_map(value: Any, path: str = "") -> dict[str, str]:
    result: dict[str, str] = {}
    if isinstance(value, dict):
        for key, item in value.items():
            result.update(formula_map(item, f"{path}.{key}" if path else key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            result.update(formula_map(item, f"{path}[{index}]"))
    elif isinstance(value, str) and value.startswith("="):
        result[path] = value
    return result


def validate_association_evidence(evidence: dict[str, Any]) -> None:
    expected = {
        "current_binding_matched_TEST": True,
        "corrected_binding_matched_V4": True,
        "visible_associated_store_matched_corrected_binding": True,
        "dynamic_spreadsheet": True,
    }
    for key, value in expected.items():
        if evidence.get(key) is not value:
            raise AssertionError(f"Sanitized association evidence failed: {key}")
    if evidence.get("root_cause") != "wrong_store_binding_test_store_used":
        raise AssertionError("Wrong binding root-cause classification")


def validate_exact_delta(
    original: dict[str, Any],
    corrected: dict[str, Any],
    profile: dict[str, str],
) -> dict[str, Any]:
    specifications_index = next(
        index
        for index, sheet in enumerate(original["config"]["worksheets"])
        if sheet["worksheetName"] == "Specifications"
    )
    allowed = {
        f"config.worksheets[{specifications_index}].data[1][20]",
        "data.Specifications[1][20]",
    }
    actual = set(differences(original, corrected))
    if actual != allowed:
        raise AssertionError(f"Binding fix changed paths outside the exact U2 mirror: {sorted(actual)}")
    if formula_map(original) != formula_map(corrected):
        raise AssertionError("A formula changed in the binding-fix candidate")

    original_binding = original["data"]["Specifications"][1][20]
    corrected_binding = corrected["data"]["Specifications"][1][20]
    if profile["kv_store_binding"] == original_binding:
        raise AssertionError("Intended environment binding still equals the original TEST binding")
    if original_binding == corrected_binding:
        raise AssertionError("Corrected binding still equals the original TEST binding")
    if corrected_binding != profile["kv_store_binding"]:
        raise AssertionError("Corrected U2 does not equal the intended environment binding")
    if corrected["config"]["worksheets"][specifications_index]["data"][1][20] != corrected_binding:
        raise AssertionError("Embedded and mirrored corrected U2 differ")

    candidate_result = v4_validator.validate_candidate(corrected, profile)
    if candidate_result["formula_count"] != 309:
        raise AssertionError("Formula count changed")
    if candidate_result["runtime"]["kv_lookup_calls"] != 44:
        raise AssertionError("Five-argument lookup count changed")
    if candidate_result["destination_count"] != 43:
        raise AssertionError("Writable destination count changed")
    if candidate_result["named_definition_count"] != 44:
        raise AssertionError("Named definition count changed")

    return {
        "binding_fix_delta": "passed_exact_store_binding_only",
        "changed_paths": sorted(actual),
        "formula_count": candidate_result["formula_count"],
        "kv_lookup_calls": candidate_result["runtime"]["kv_lookup_calls"],
        "destination_count": candidate_result["destination_count"],
        "named_definition_count": candidate_result["named_definition_count"],
    }


def main() -> None:
    if sha256(binding_builder.ORIGINAL_PATH) != binding_builder.EXPECTED_ORIGINAL_SHA256:
        raise AssertionError("Original V4 candidate SHA-256 changed")
    original = load_json(binding_builder.ORIGINAL_PATH)
    corrected = load_json(binding_builder.OUTPUT_PATH)
    profile = v4_builder.load_profile()
    validate_association_evidence(load_json(ASSOCIATION_EVIDENCE_PATH))
    result = validate_exact_delta(original, corrected, profile)
    result["binding_fix_sha256"] = sha256(binding_builder.OUTPUT_PATH)
    result["original_v4_sha256"] = sha256(binding_builder.ORIGINAL_PATH)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
