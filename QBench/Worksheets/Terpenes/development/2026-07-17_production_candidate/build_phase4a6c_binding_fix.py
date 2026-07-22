#!/usr/bin/env python3
"""Build the V4 binding fix by changing only the mirrored store binding."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import build_phase3_candidates as phase3
import build_phase3_candidates_v4 as v4_builder


PACKAGE_DIR = Path(__file__).resolve().parent
ORIGINAL_PATH = v4_builder.TEST_OUTPUT
OUTPUT_PATH = (
    phase3.OUTPUT_DIR
    / "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v4_binding_fix.json"
)
EXPECTED_ORIGINAL_SHA256 = (
    "53554a8dc167202da373e856df7c1905aab19d117353ec2899cc2de708447924"
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def specifications(candidate: dict[str, Any]) -> dict[str, Any]:
    return next(
        sheet
        for sheet in candidate["config"]["worksheets"]
        if sheet["worksheetName"] == "Specifications"
    )


def build_candidate(
    original_bytes: bytes | None = None,
    profile: dict[str, str] | None = None,
) -> dict[str, Any]:
    source_bytes = ORIGINAL_PATH.read_bytes() if original_bytes is None else original_bytes
    if sha256_bytes(source_bytes) != EXPECTED_ORIGINAL_SHA256:
        raise AssertionError("Original V4 candidate bytes changed")

    original = json.loads(source_bytes.decode("utf-8"))
    corrected = copy.deepcopy(original)
    runtime_profile = copy.deepcopy(profile if profile is not None else v4_builder.load_profile())
    v4_builder.validate_profile(runtime_profile)

    original_embedded = specifications(original)["data"][1][20]
    original_mirrored = original["data"]["Specifications"][1][20]
    corrected_binding = runtime_profile["kv_store_binding"]
    if original_embedded != original_mirrored:
        raise AssertionError("Original embedded and mirrored Specifications!U2 differ")
    if original_embedded == corrected_binding:
        raise AssertionError("Binding-fix profile still contains the original V4 binding")

    specifications(corrected)["data"][1][20] = corrected_binding
    corrected["data"]["Specifications"][1][20] = corrected_binding
    return corrected


def main() -> None:
    candidate = build_candidate()
    phase3.dump_json(OUTPUT_PATH, candidate)
    print(f"built_binding_fix={OUTPUT_PATH.relative_to(phase3.REPO_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
