"""Static validation for the Prompt 4.6 controlled Sandbox probe package."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import build_probe_worksheet_candidate as worksheet_builder
import build_qbench_probe_distribution as distribution_builder


REPO_ROOT = Path(__file__).resolve().parents[6]
PACKAGE_DIR = Path(__file__).resolve().parents[1]
DIST_DIR = PACKAGE_DIR / "dist"
MANIFEST_PATH = DIST_DIR / "qbench_probe_manifest.json"
WORKSHEET_PATH = DIST_DIR / "qbench_runtime_probe_batch_ws_candidate.json"
CONTRACT_PATH = PACKAGE_DIR / "config/qbench_probe_contract.json"
SOURCE_FIXTURE = REPO_ROOT / "QBench/Worksheets/Terpenes/source/Output_redacted_fixture.txt"
TEST_CANDIDATE = REPO_ROOT / "QBench/Worksheets/Terpenes/development/2026-07-14_test_worksheet_candidate/dist/terpenes__test_ws_id_42__candidate_v1__2026-07-14.json"
BATCH_CANDIDATE = REPO_ROOT / "QBench/Worksheets/Terpenes/development/2026-07-14_batch_worksheet_candidate/dist/terpenes__batch_ws_id_43__candidate_v1__2026-07-14.json"


EXPECTED_HASHES = {
    TEST_CANDIDATE: "90686b980882b221008f281be33984dc5232e2f3d2632300db3f4a27b529640a",
    SOURCE_FIXTURE: "ed796c690b972ca08f1976b1d8f7355d3e5140e73ffa912c441d6185a093283b",
}
EXPECTED_BATCH_CANONICAL = "e5c80b1213396cab4932e267fd786c6986c933d4b404f11daa5c5aba0629758e"


class ProbeValidationError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ProbeValidationError(message)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_lf_hash(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return sha256_bytes(text.encode("utf-8"))


def validate_dependencies() -> None:
    contract = read_json(CONTRACT_PATH)
    if contract["qbench_runtime_contract_status"] != "insufficient_for_prompt_4_6":
        fail("Merged runtime-contract readiness status is missing.")
    if contract["qbench_sandbox_probe_status"] != "sufficient_to_begin_controlled_prompt_4_6_probe":
        fail("Merged Sandbox-probe readiness status is missing.")
    if contract["allowed_batch_write_api"] != "QBBatchService.patchWorksheet":
        fail("Only the documented patch method may be investigated.")
    if contract["batch_context_status"] != "not_available_in_preview_runtime":
        fail("Stage 2A Batch-context status is missing from the runtime contract.")
    if contract["batch_context_path"] is not None:
        fail("Stage 2A must not invent a Batch-context path.")
    if contract["current_tenant_imports"]["qbjs_js"]["url"] is not None:
        fail("An unproven QBJS import URL must not be recorded.")
    for path, expected in EXPECTED_HASHES.items():
        if sha256_file(path) != expected:
            fail(f"Controlled dependency hash mismatch: {path}")
    if canonical_lf_hash(BATCH_CANDIDATE) != EXPECTED_BATCH_CANONICAL:
        fail("Prompt 4 Batch candidate canonical-LF hash mismatch.")


def parse_target(target: str) -> tuple[str, str, str | None]:
    match = re.fullmatch(r"([^!]+)!([A-Z]+\d+)(?::([A-Z]+\d+))?", target)
    if not match:
        fail(f"Invalid named-cell target: {target}")
    return match.group(1), match.group(2), match.group(3)


def address_to_position(address: str) -> tuple[int, int]:
    match = re.fullmatch(r"([A-Z]+)(\d+)", address)
    if not match:
        fail(f"Invalid cell address: {address}")
    column = 0
    for character in match.group(1):
        column = column * 26 + ord(character) - 64
    return int(match.group(2)), column


def validate_worksheet() -> dict[str, Any]:
    workbook_text = WORKSHEET_PATH.read_text(encoding="utf-8")
    if workbook_text != worksheet_builder.render_candidate():
        fail("Probe worksheet is not byte-identical to generator output.")
    workbook = json.loads(workbook_text)
    worksheets = workbook["config"]["worksheets"]
    if len(worksheets) != 1 or worksheets[0]["worksheetName"] != "Probe":
        fail("Probe worksheet must contain exactly one Probe tab.")
    worksheet = worksheets[0]
    if worksheet["worksheetId"] != worksheet_builder.PROBE_WORKSHEET_ID:
        fail("Probe worksheet stable UUID changed.")
    if workbook["qb_config"]["kvstore_config"] != {}:
        fail("Probe worksheet must not contain key/value-store configuration.")
    if workbook["qb_config"]["report_export_range"] or workbook["qb_config"]["portal_export_range"]:
        fail("Probe worksheet must not contain a report or portal range.")
    named = workbook["qb_config"]["named_cells"]
    if named != worksheet_builder.build_named_cells():
        fail("Probe named cells differ from the controlled contract.")
    if len(named) != len(set(named)):
        fail("Probe named-cell system names must be unique.")
    for value in named.values():
        sheet, start, end = parse_target(value["cell"])
        if sheet != "Probe":
            fail("Every probe named target must use the Probe tab.")
        for address in [start] + ([end] if end else []):
            row, column = address_to_position(address)
            if row > worksheet_builder.ROW_COUNT or column > worksheet_builder.COLUMN_COUNT:
                fail("Probe named-cell target is outside worksheet bounds.")
    data = workbook["data"]["Probe"]
    for address, formula in worksheet_builder.FORMULAS.items():
        row, column = address_to_position(address)
        if data[row - 1][column - 1] != formula:
            fail(f"Probe formula changed: {address}")
        if worksheet["cells"][address]["readonly"] is not True:
            fail(f"Formula cell must be read-only: {address}")
    for address in worksheet_builder.writable_cells():
        if worksheet["cells"][address]["readonly"] is not False:
            fail(f"Controlled input cell must be writable: {address}")
    if any("automation" in key.lower() for key in workbook.keys()):
        fail("Probe worksheet must not include automation configuration.")
    return {"named_cell_count": len(named), "formula_count": len(worksheet_builder.FORMULAS)}


def validate_scripts() -> dict[str, int]:
    source_scripts = sorted((PACKAGE_DIR / "src").glob("*.js"))
    generated_scripts = sorted(DIST_DIR.glob("*.js"))
    forbidden = [
        "updateWorksheet",
        "QBBatchService.update(",
        "fetch(",
        "XMLHttpRequest",
        "eval(",
        "Function(",
        "localStorage",
        "cookie",
        "credentials",
        "pass_fail",
        "Pass/Fail",
    ]
    for path in source_scripts + generated_scripts:
        text = path.read_text(encoding="utf-8")
        for token in forbidden:
            if token in text:
                fail(f"Forbidden token {token!r} in {path}")
    core = (PACKAGE_DIR / "src/qbench_browser_parser_core.js").read_text(encoding="utf-8")
    for token in ["require(", "module.exports", "Buffer", "crypto"]:
        if token in core:
            fail(f"Browser core contains Node-only token: {token}")
    no_write_source = (PACKAGE_DIR / "src/qbench_runtime_no_write_probe.js").read_text(encoding="utf-8")
    no_write_dist = (DIST_DIR / "qbench_runtime_no_write_probe_v1.js").read_text(encoding="utf-8")
    for text in [no_write_source, no_write_dist]:
        for token in [
            "QBBatchService",
            "patchWorksheet",
            "updateWorksheet",
            "fetch(",
            "XMLHttpRequest",
            "eval(",
            "Function(",
            "localStorage",
            ".cookie",
        ]:
            if token in text:
                fail(f"Stage 1 no-write script contains prohibited token: {token}")
    if "Array.from" in no_write_source:
        fail("Stage 1 file collection normalization must not use Array.from.")
    for token in [
        "fileCollectionKind",
        "normalizeFileCollection",
        "files.item(0)",
        "probe step = file collection accepted",
        "failed step =",
        "CONTROLLED_FILE_COLLECTION_ERROR",
        "CONTROLLED_FILE_COUNT_ERROR",
        "CONTROLLED_FILE_OBJECT_ERROR",
        "CONTROLLED_FILE_NAME_ERROR",
        "CONTROLLED_FILE_READ_ERROR",
    ]:
        if token not in no_write_source or token not in no_write_dist:
            fail(f"Stage 1 corrected runtime contract token is missing: {token}")
    if "run(async () =>" not in no_write_dist or "FileReader" not in no_write_dist or "qb.files" not in no_write_dist:
        fail("Generated Stage 1 script is missing the proven runtime contract.")
    exact_import = f'importScripts("{distribution_builder.FILE_PARSER_IMPORT_URL}");'
    if exact_import not in no_write_dist:
        fail("Stage 1 script does not use the exact recorded File Parser import URL.")
    template = (PACKAGE_DIR / "src/terpenes_qbench_sandbox_probe.template.js").read_text(encoding="utf-8")
    if template.index("const data = buildWritePlan") > template.index("service.patchWorksheet"):
        fail("Fixture write plan must be fully validated before the patch call.")
    if (DIST_DIR / "terpenes_qbench_file_parser_sandbox_probe_v1.js").exists():
        fail("Stage 7 distribution must not exist during Stage 0.")
    return {"source_script_count": len(source_scripts), "generated_script_count": len(generated_scripts)}


def validate_manifest() -> int:
    manifest = read_json(MANIFEST_PATH)
    if manifest["stage_statuses"]["stage_0_repository_preparation"] != "passed":
        fail("Stage 0 manifest status must be passed.")
    if manifest["stage_statuses"]["stage_1_no_write_runtime"] != "passed":
        fail("Stage 1 corrected no-write Preview must be recorded as passed.")
    if manifest["qbench_sandbox_probe_status"] != "stage_2a_completed_batch_context_not_available_stage_2b_not_authorized":
        fail("Stage 2A completion / Stage 2B authorization boundary is missing.")
    if manifest["stage_statuses"]["stage_2_batch_context"] != "not_available_in_preview_runtime":
        fail("Stage 2A Batch-context result is missing.")
    for stage, status in manifest["stage_statuses"].items():
        if stage not in {
            "stage_0_repository_preparation",
            "stage_1_no_write_runtime",
            "stage_2_batch_context",
        } and status != "not_run":
            fail("Stages after Stage 2A must remain not_run.")
    attempt = manifest["stage_1_initial_attempt"]
    if attempt["result"] != "failed_safely_runtime_file_collection_compatibility":
        fail("Stage 1 initial failed-safe result is missing.")
    if attempt["cause_status"] != "array_like_collection_confirmed_specific_constructor_not_logged":
        fail("The confirmed array-like contract must not claim a specific unlogged constructor.")
    if attempt["runtime_data_modified"] is not False or attempt["worksheet_service_invoked"] is not False:
        fail("Stage 1 must record no runtime data modification or worksheet service invocation.")
    retry = manifest["stage_1_retry_result"]
    if retry["result"] != "passed" or retry["file_collection_kind"] != "array_like":
        fail("Corrected Stage 1 Preview result or array-like observation is missing.")
    if [
        retry["compound_result_row_count"],
        retry["peak_table_row_count"],
        retry["reportable_channel_count"],
        retry["dimethylacetamide_audit_row_count"],
    ] != [24, 34, 23, 1]:
        fail("Corrected Stage 1 controlled counts do not match the runtime evidence.")
    if retry["qb_success_reached"] is not True or retry["web_crypto_available"] is not True:
        fail("Stage 1 QB.success or Web Crypto evidence is missing.")
    if retry["parser_active"] is not False or retry["parser_version_status"] != "DRAFT":
        fail("Stage 1 parser must remain inactive/DRAFT.")
    if retry["trigger_set"] is not False or retry["assay_set"] is not False:
        fail("Stage 1 parser must remain without a trigger or assay.")
    if retry["runtime_data_modified"] is not False or retry["worksheet_service_invoked"] is not False:
        fail("Stage 1 retry must record no runtime data modification or worksheet service invocation.")
    stage_2a = manifest["stage_2a_result"]
    if stage_2a["result"] != "completed" or stage_2a["batch_context_status"] != "not_available_in_preview_runtime":
        fail("Stage 2A completion or Batch-context status is missing.")
    expected_paths = {
        "QB.attachment",
        "QB.batch",
        "QB.context",
        "QB.currentBatch",
        "QB.fileParserContext",
    }
    if set(stage_2a["candidate_paths"]) != expected_paths:
        fail("Stage 2A candidate-path evidence is incomplete.")
    if any(
        item != {"present": False, "value_type": "undefined"}
        for item in stage_2a["candidate_paths"].values()
    ):
        fail("Stage 2A must record every candidate path as absent/undefined.")
    if stage_2a["safe_property_path"] is not None or stage_2a["value_type"] is not None:
        fail("Stage 2A must not invent a Batch-context path or type.")
    if stage_2a["preview_output_group_count_observed"] != 2 or stage_2a["preview_rerun_by_codex"] is not False:
        fail("Stage 2A existing-output inspection evidence is missing.")
    if stage_2a["controlled_fixture_file_count_indicator"] != 1:
        fail("Stage 2A controlled fixture selection evidence is missing.")
    if stage_2a["full_qb_object_serialized"] is not False or stage_2a["security_or_session_value_dereferenced"] is not False:
        fail("Stage 2A must record the safe inspection boundary.")
    if stage_2a["parser_active"] is not False or stage_2a["parser_version_status"] != "DRAFT":
        fail("Stage 2A parser must remain inactive/DRAFT.")
    if stage_2a["trigger_set"] is not False or stage_2a["assay_set"] is not False:
        fail("Stage 2A parser must remain without a trigger or assay.")
    if stage_2a["runtime_data_modified"] is not False or stage_2a["worksheet_service_invoked"] is not False:
        fail("Stage 2A must record no runtime data modification or worksheet service invocation.")
    scope = manifest["scope_controls"]
    if scope["qbench_configuration_draft_modified"] is not True or scope["qbench_modified"] is not True:
        fail("The authorized inactive parser draft change must be recorded accurately.")
    if scope["qbench_runtime_data_modified"] is not False or scope["production_modified"] is not False:
        fail("Stage 1 must record no runtime-data or production modification.")
    expected = distribution_builder.build_manifest()
    if manifest != expected:
        fail("Manifest is not byte-content-equivalent to current package artifacts.")
    for artifact in manifest["artifact_hashes"]:
        path = REPO_ROOT / artifact["path"]
        if sha256_file(path) != artifact["sha256"]:
            fail(f"Manifest artifact hash mismatch: {artifact['path']}")
    return len(manifest["artifact_hashes"])


def validate_package() -> dict[str, Any]:
    validate_dependencies()
    worksheet_summary = validate_worksheet()
    script_summary = validate_scripts()
    artifact_count = validate_manifest()
    copied_fixture = PACKAGE_DIR / "tests/fixtures/Output_redacted_fixture.txt"
    if sha256_file(copied_fixture) != EXPECTED_HASHES[SOURCE_FIXTURE]:
        fail("Controlled fixture copy hash mismatch.")
    return {
        "status": "ok",
        "artifact_count": artifact_count,
        **worksheet_summary,
        **script_summary,
        "qbench_configuration_draft_modified": True,
        "qbench_modified": True,
        "qbench_runtime_data_modified": False,
        "stage_1_authorized": True,
        "stage_1_status": "passed",
        "stage_2a_authorized": True,
        "stage_2a_status": "not_available_in_preview_runtime",
    }


def main() -> None:
    try:
        print(json.dumps(validate_package(), indent=2, sort_keys=True))
    except ProbeValidationError as error:
        print(json.dumps({"status": "error", "error": str(error)}, indent=2, sort_keys=True))
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
