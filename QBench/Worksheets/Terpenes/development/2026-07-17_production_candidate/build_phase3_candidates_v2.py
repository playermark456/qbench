#!/usr/bin/env python3
"""Build Phase 3 v2 candidates with the proven historical workbook identity."""

from __future__ import annotations

from typing import Any

import build_phase3_candidates as phase3


TEST_TARGET = "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS_V2"
TEST_VERSION = "Terpenes Production Test Worksheet v2"
BATCH_TARGET = "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS_V2"
BATCH_VERSION = "Terpenes Production Batch Worksheet v2"

TEST_OUTPUT = phase3.OUTPUT_DIR / "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v2.json"
BATCH_OUTPUT = phase3.OUTPUT_DIR / "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS__v2.json"


def renderer_identity(candidate: dict[str, Any]) -> dict[str, Any]:
    """Return the renderer-sensitive identity retained from the historical base."""
    return {
        "namespace": candidate["config"]["namespace"],
        "worksheet_ids": {
            worksheet["worksheetName"]: worksheet["worksheetId"]
            for worksheet in candidate["config"]["worksheets"]
        },
    }


def build_candidates() -> tuple[dict[str, Any], dict[str, Any]]:
    test_builder = phase3.load_module("phase3_v2_test_builder_base", phase3.TEST_BUILDER_PATH)
    batch_builder = phase3.load_module("phase3_v2_batch_builder_base", phase3.BATCH_BUILDER_PATH)

    historical_test = test_builder.build_candidate()
    historical_batch = batch_builder.build_candidate()

    test_candidate = phase3.build_test_candidate(
        test_builder,
        target_name=TEST_TARGET,
        version_name=TEST_VERSION,
        preserve_historical_identity=True,
    )
    batch_candidate = phase3.build_batch_candidate(
        batch_builder,
        target_name=BATCH_TARGET,
        version_name=BATCH_VERSION,
        preserve_historical_identity=True,
    )

    if renderer_identity(test_candidate) != renderer_identity(historical_test):
        raise AssertionError("Test v2 did not preserve the historical namespace and worksheet IDs")

    expected_batch_identity = renderer_identity(historical_batch)
    expected_batch_identity["worksheet_ids"] = {
        ("Batch Review" if name == "QC Review" else "Test Transfer" if name == "Publish" else name): value
        for name, value in expected_batch_identity["worksheet_ids"].items()
    }
    if renderer_identity(batch_candidate) != expected_batch_identity:
        raise AssertionError("Batch v2 did not preserve the historical namespace and worksheet IDs")

    return test_candidate, batch_candidate


def main() -> None:
    test_candidate, batch_candidate = build_candidates()
    phase3.dump_json(TEST_OUTPUT, test_candidate)
    phase3.dump_json(BATCH_OUTPUT, batch_candidate)
    print(f"built_test_v2={TEST_OUTPUT.relative_to(phase3.REPO_ROOT).as_posix()}")
    print(f"built_batch_v2={BATCH_OUTPUT.relative_to(phase3.REPO_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
