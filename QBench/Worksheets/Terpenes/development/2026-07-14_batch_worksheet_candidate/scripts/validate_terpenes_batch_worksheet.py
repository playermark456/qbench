#!/usr/bin/env python3
"""Validate the generated Terpenes Batch Worksheet candidate."""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path
from typing import Any, Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
REPO_ROOT = SCRIPT_DIR.parents[5]
BUILD_SCRIPT = SCRIPT_DIR / "build_terpenes_batch_worksheet.py"

CANDIDATE_PATH = BASE_DIR / "dist" / "terpenes__batch_ws_id_43__candidate_v1__2026-07-14.json"
MANIFEST_PATH = BASE_DIR / "dist" / "candidate_manifest.json"
SOURCE_ACTIVE_EXPORT = (
    REPO_ROOT
    / "QBench"
    / "Rescans"
    / "2026-07-04"
    / "Worksheets"
    / "Terpenes"
    / "terpenes__id_43__worksheet_export_spreadsheet__active__2026-07-04.json"
)
PROMPT2_CONFIG_DIR = (
    REPO_ROOT
    / "QBench"
    / "Worksheets"
    / "Terpenes"
    / "development"
    / "2026-07-14_config_parser_foundation"
    / "config"
)
ANALYTE_CONFIG = PROMPT2_CONFIG_DIR / "terpenes_analytes.json"

EXPECTED_TABS = ["Run Setup", "Instrument Import", "QC Review", "Publish"]
FORBIDDEN_FORMULA_TEXT = ["#REF!", "#NAME?", "#VALUE!", "Conc. %", "Norm Conc.", "IFERROR", "VALUE("]
FORBIDDEN_CANDIDATE_TOKENS = [
    "pass_fail",
    "Pass/Fail",
    "Pass",
    "Fail",
    "Not Tested",
    "Claim Met",
    "Claim Not Met",
    "METRC",
    "key/value-store",
]
ALLOWED_QC_EVALUATIONS = {
    "within_criteria",
    "outside_criteria",
    "decision_required",
    "not_evaluated",
    "not_applicable",
    "review_required",
}
REQUIRED_NAMED_CELLS = [
    "batch_qbench_id",
    "analytical_batch_id",
    "batch_assay_name",
    "run_instrument_name",
    "run_detector_id",
    "run_detector_name",
    "run_method_file",
    "run_sequence_file",
    "run_column",
    "run_carrier_gas",
    "run_analyst",
    "run_start",
    "run_end",
    "calibration_id",
    "standard_lot",
    "extraction_solvent_lot",
    "parser_version",
    "source_package_version",
    "raw_ascii_attachment_reference",
    "raw_batch_manifest_hash",
    "run_setup_complete",
    "run_setup_message",
    "terpenes_batch_import_table",
    "terpenes_batch_import_test_ids",
    "terpenes_batch_import_analytes",
    "terpenes_batch_import_dimethylacetamide",
    "terpenes_batch_import_validation_status",
    "terpenes_batch_integration_review_status",
    "qc_config_version",
    "bracketing_ccv_criterion_status",
    "bracketing_ccv_accuracy_percent_window",
    "lcs_requirement_status",
    "lcs_requirement_controlled_source",
    "lcs_requirement_reviewed_by",
    "qc_configuration_complete",
    "integration_review_complete",
    "qc_data_complete",
    "qc_review_complete",
    "all_publish_rows_valid",
    "duplicate_test_id_count",
    "populated_publish_row_count",
    "batch_qc_disposition",
    "batch_qc_reviewer",
    "batch_qc_reviewed_at",
    "batch_publish_ready",
    "batch_publish_message",
    "terpenes_batch_qc_table",
    "terpenes_batch_publish_table",
    "terpenes_batch_publish_sample_ids",
    "terpenes_batch_publish_test_ids",
    "terpenes_batch_publish_product_matrices",
    "terpenes_batch_publish_instrument_conc",
    "terpenes_batch_publish_sample_mass_g",
    "terpenes_batch_publish_final_volume_ml",
    "terpenes_batch_publish_df",
    "terpenes_batch_publish_df_application_mode",
    "terpenes_batch_publish_conc_unit",
    "terpenes_batch_publish_unit_confirmed",
    "terpenes_batch_publish_preparation_confirmed",
    "terpenes_batch_publish_source_batch_ids",
    "terpenes_batch_publish_source_files",
    "terpenes_batch_publish_source_hashes",
    "terpenes_batch_publish_batch_disposition",
    "terpenes_batch_publish_ready",
    "terpenes_batch_publish_messages",
]


class CandidateValidationError(ValueError):
    """Raised when static validation fails."""


def load_build_module():
    spec = importlib.util.spec_from_file_location("build_terpenes_batch_worksheet", BUILD_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


build_mod = load_build_module()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def fail(message: str) -> None:
    raise CandidateValidationError(message)


def workbook_tabs(workbook: dict[str, Any]) -> list[str]:
    return [worksheet["worksheetName"] for worksheet in workbook["config"]["worksheets"]]


def worksheet_by_name(workbook: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {worksheet["worksheetName"]: worksheet for worksheet in workbook["config"]["worksheets"]}


def iter_grid_cells(workbook: dict[str, Any]) -> Iterable[tuple[str, int, int, Any]]:
    for worksheet in workbook["config"]["worksheets"]:
        tab = worksheet["worksheetName"]
        for row_index, row in enumerate(worksheet.get("data", []), start=1):
            for col_index, value in enumerate(row, start=1):
                yield tab, row_index, col_index, value


def formulas(workbook: dict[str, Any]) -> list[str]:
    return [
        value
        for _tab, _row, _col, value in iter_grid_cells(workbook)
        if isinstance(value, str) and value.startswith("=")
    ]


def count_formulas(workbook: dict[str, Any]) -> int:
    return len(formulas(workbook))


def col_index(label: str) -> int:
    result = 0
    for char in label:
        result = result * 26 + (ord(char) - 64)
    return result


CELL_RE = re.compile(r"^([A-Z]+)([1-9][0-9]*)$")
RANGE_RE = re.compile(r"^([A-Z]+[1-9][0-9]*):([A-Z]+[1-9][0-9]*)$")


def split_target(target: str) -> tuple[str | None, str]:
    if "!" not in target:
        return None, target
    tab, ref = target.split("!", 1)
    return tab.strip("'"), ref


def parse_cell(cell: str) -> tuple[int, int]:
    match = CELL_RE.match(cell)
    if not match:
        fail(f"Invalid cell reference: {cell}")
    return int(match.group(2)), col_index(match.group(1))


def worksheet_bounds(worksheet: dict[str, Any]) -> tuple[int, int]:
    rows = len(worksheet.get("data", []))
    cols = max((len(row) for row in worksheet.get("data", [])), default=0)
    return rows, cols


def assert_cell_in_bounds(worksheet: dict[str, Any], cell: str) -> None:
    row, col = parse_cell(cell)
    row_count, col_count = worksheet_bounds(worksheet)
    if row < 1 or col < 1 or row > row_count or col > col_count:
        fail(f"Target {worksheet['worksheetName']}!{cell} is outside worksheet bounds.")


def assert_named_target_resolves(target: str, worksheets: dict[str, dict[str, Any]]) -> None:
    tab, ref = split_target(target)
    if not tab:
        fail(f"Named-cell target must include a tab for Prompt 4: {target}")
    if tab not in worksheets:
        fail(f"Named-cell target references unknown tab: {target}")
    worksheet = worksheets[tab]
    range_match = RANGE_RE.match(ref)
    if range_match:
        start, end = range_match.groups()
        assert_cell_in_bounds(worksheet, start)
        assert_cell_in_bounds(worksheet, end)
        start_row, start_col = parse_cell(start)
        end_row, end_col = parse_cell(end)
        if start_row > end_row or start_col > end_col:
            fail(f"Named-cell range is reversed: {target}")
        return
    assert_cell_in_bounds(worksheet, ref)


def validate_tabs_and_ids(workbook: dict[str, Any], manifest: dict[str, Any]) -> None:
    tabs = workbook_tabs(workbook)
    if tabs != EXPECTED_TABS:
        fail(f"Expected tabs {EXPECTED_TABS}, found {tabs}.")
    if len(tabs) != len(set(tabs)):
        fail("Worksheet names must be unique.")
    worksheet_ids = [worksheet["worksheetId"] for worksheet in workbook["config"]["worksheets"]]
    if len(worksheet_ids) != len(set(worksheet_ids)):
        fail("Worksheet IDs must be unique.")
    source = load_json(SOURCE_ACTIVE_EXPORT)
    source_sheet_id = source["config"]["worksheets"][0]["worksheetId"]
    ids = {worksheet["worksheetName"]: worksheet["worksheetId"] for worksheet in workbook["config"]["worksheets"]}
    if ids["Publish"] != source_sheet_id:
        fail("Publish tab must preserve the source Sheet1 worksheet ID.")
    for tab, expected_id in {
        "Run Setup": build_mod.RUN_SETUP_WORKSHEET_ID,
        "Instrument Import": build_mod.INSTRUMENT_IMPORT_WORKSHEET_ID,
        "QC Review": build_mod.QC_REVIEW_WORKSHEET_ID,
    }.items():
        if ids[tab] != expected_id:
            fail(f"{tab} worksheet ID is not the stable Prompt 4 constant.")
    if manifest["generated_candidate"]["worksheet_ids"] != ids:
        fail("Manifest worksheet IDs do not match the candidate.")
    for forbidden in ["Report", "METRC", "Key Value Store", "KV Store"]:
        if forbidden in tabs:
            fail(f"Prompt 4 must not add a {forbidden} tab.")


def validate_synchronized_data(workbook: dict[str, Any]) -> None:
    worksheets = worksheet_by_name(workbook)
    if set(workbook.get("data", {})) != set(worksheets):
        fail("Top-level data tabs do not match config worksheets.")
    for name, worksheet in worksheets.items():
        if workbook["data"][name] != worksheet["data"]:
            fail(f"Top-level data for {name} is not synchronized with config worksheet data.")


def validate_source_publish_capacity(workbook: dict[str, Any], manifest: dict[str, Any]) -> None:
    source = load_json(SOURCE_ACTIVE_EXPORT)
    source_capacity = build_mod.source_publish_capacity(source)
    publish = worksheet_by_name(workbook)["Publish"]["data"]
    if len(publish) - 1 != source_capacity:
        fail("Publish row capacity must match the active source test-row capacity.")
    if manifest["source_active_export"]["publish_row_capacity"] != source_capacity:
        fail("Manifest source publish row capacity is stale.")
    source_placeholders = build_mod.source_publish_placeholders(source)
    for offset, placeholder in enumerate(source_placeholders, start=2):
        row = publish[offset - 1]
        if row[0] != placeholder["test_id"]:
            fail(f"Publish row {offset} did not preserve the source test ID placeholder.")
        if row[2] != placeholder["product_matrix"]:
            fail(f"Publish row {offset} did not preserve the source product-matrix placeholder.")


def validate_channel_layout(workbook: dict[str, Any]) -> None:
    analytes = sorted(load_json(ANALYTE_CONFIG)["internal_reportable_channels"], key=lambda item: item["order"])
    labels = [row["worksheet_label"] for row in analytes]
    worksheets = worksheet_by_name(workbook)
    import_headers = worksheets["Instrument Import"]["data"][0]
    publish_headers = worksheets["Publish"]["data"][0]
    if import_headers[33:56] != labels:
        fail("Instrument Import AH:BD must contain exactly the 23 Prompt 2 analytes in order.")
    if publish_headers[3:26] != labels:
        fail("Publish D:Z must contain exactly the 23 Prompt 2 analytes in order.")
    if "Dimethylacetamide" in publish_headers[3:26]:
        fail("Dimethylacetamide must not appear in the reportable Publish analyte columns.")
    if "Dimethylacetamide Conc." not in import_headers and "dimethylacetamide_conc" not in import_headers:
        fail("Dimethylacetamide audit field is missing from Instrument Import.")
    if "Dimethylacetamide Conc." not in publish_headers:
        fail("Dimethylacetamide audit field is missing from Publish source/audit columns.")


def validate_named_cells(workbook: dict[str, Any]) -> None:
    named_cells = workbook["qb_config"].get("named_cells", {})
    if not isinstance(named_cells, dict):
        fail("qb_config.named_cells must be an object.")
    missing = [name for name in REQUIRED_NAMED_CELLS if name not in named_cells]
    if missing:
        fail(f"Missing required named cells: {missing}")
    if "pass_fail" in named_cells:
        fail("Terpenes Batch Worksheet must not define pass_fail.")
    if len(named_cells) != len(set(named_cells)):
        fail("Named-cell system names must be unique.")
    worksheets = worksheet_by_name(workbook)
    seen_display_targets: set[tuple[str, str]] = set()
    for name, item in named_cells.items():
        target = item.get("cell", "")
        assert_named_target_resolves(target, worksheets)
        pair = (str(item.get("display_name", "")), target)
        if pair in seen_display_targets and item.get("display_name"):
            fail(f"Duplicate named-cell target/display pair found at {name}: {pair}")
        seen_display_targets.add(pair)
    expected_ranges = {
        "terpenes_batch_import_table": "Instrument Import!A1:BE201",
        "terpenes_batch_import_analytes": "Instrument Import!AH2:BD201",
        "terpenes_batch_qc_table": "QC Review!A22:X45",
        "terpenes_batch_publish_table": "Publish!A1:BD87",
        "terpenes_batch_publish_instrument_conc": "Publish!D2:Z87",
        "batch_qc_disposition": "QC Review!B15",
        "batch_publish_ready": "QC Review!B18",
        "bracketing_ccv_criterion_status": "QC Review!B3",
        "lcs_requirement_status": "QC Review!B5",
    }
    for name, target in expected_ranges.items():
        if named_cells[name]["cell"] != target:
            fail(f"{name} must target {target}.")


def validate_formulas(workbook: dict[str, Any]) -> None:
    formula_text = "\n".join(formulas(workbook))
    for formula in formulas(workbook):
        for forbidden in FORBIDDEN_FORMULA_TEXT:
            if forbidden in formula:
                fail(f"Formula contains forbidden text {forbidden}: {formula}")
    required_fragments = [
        "COUNT(D2:Z2)=23",
        "ISNUMBER(AA2)",
        "ISNUMBER(AB2)",
        'AD2="already_applied_by_labsolutions"',
        'AD2="apply_in_qbench"',
        'AE2="ug/mL"',
        'AF2="TRUE"',
        'AG2="TRUE"',
        'AW2="Reviewed"',
        'AX2="Valid"',
        "'QC Review'!$B$18=TRUE",
        "'QC Review'!$B$15",
        "'Run Setup'!$B$24=TRUE",
        'bracketing_ccv_accuracy_percent_window',
    ]
    # The named string is not in formulas; the cell target check covers it.
    required_fragments.remove("bracketing_ccv_accuracy_percent_window")
    for fragment in required_fragments:
        if fragment not in formula_text:
            fail(f"Required formula gate missing: {fragment}")
    for row in range(2, 88):
        publish = worksheet_by_name(workbook)["Publish"]["data"]
        analytical = publish[row - 1][51]
        prereq = publish[row - 1][53]
        ready = publish[row - 1][54]
        if f"COUNT(D{row}:Z{row})=23" not in analytical:
            fail(f"Publish row {row} analytical completeness must require 23 numeric analytes.")
        if f"'QC Review'!$B$18=TRUE" in prereq:
            fail("Row Prerequisites Complete must not depend on batch_publish_ready.")
        if f"BB{row}=TRUE" not in ready or "'QC Review'!$B$18=TRUE" not in ready:
            fail("Publish Ready must require row prerequisites and batch_publish_ready.")
    batch_formula = worksheet_by_name(workbook)["QC Review"]["data"][17][1]
    if "Publish!BC" in batch_formula:
        fail("batch_publish_ready must not depend on row Publish Ready.")
    if "'Run Setup'!$B$24=TRUE" not in batch_formula:
        fail("batch_publish_ready must require run_setup_complete.")
    if '$B$15="Accepted"' not in batch_formula:
        fail("batch_publish_ready must require Accepted batch disposition.")
    if 'COUNTIF(W23:W45,"within_criteria")=23' not in formula_text:
        fail("qc_review_complete must require all 23 overall evaluations within criteria.")
    if 'COUNTIF(W23:W45,"outside_criteria")=0' not in formula_text:
        fail("qc_review_complete must block outside_criteria.")
    if 'COUNTIF(W23:W45,"decision_required")=0' not in formula_text:
        fail("qc_review_complete must block decision_required.")
    if '$B$3="confirmed"' not in formula_text or '$B$3<>"confirmed"' not in formula_text:
        fail("Bracketing formulas must only open the confirmed status path.")
    if '$B$5="not_required"' not in formula_text or '$B$6<>""' not in formula_text or '$B$7<>""' not in formula_text:
        fail("LCS not_required status must require controlled-source and reviewer fields.")
    if '"Run setup incomplete"' not in worksheet_by_name(workbook)["QC Review"]["data"][18][1]:
        fail("batch_publish_message must report run setup incomplete first.")
    import_formula = worksheet_by_name(workbook)["Instrument Import"]["data"][1][32]
    for fragment in [
        "ISNUMBER(X2)<>TRUE",
        "ISNUMBER(Y2)<>TRUE",
        "Y2<0",
        "ISNUMBER(Z2)<>TRUE",
        "ISNUMBER(AA2)<>TRUE",
        "ISNUMBER(AB2)<>TRUE",
        "AB2<0",
        "COUNT(AH2:BD2)<>23",
    ]:
        if fragment not in import_formula:
            fail(f"Import validation formula missing hardened check: {fragment}")
    qc_review = worksheet_by_name(workbook)["QC Review"]["data"]
    for row in range(23, 46):
        for col in [3, 5, 7, 9, 11, 13, 15, 17, 19, 21]:
            formula = qc_review[row - 1][col]
            if "ISNUMBER(" not in formula:
                fail(f"QC formula at row {row} col {col + 1} must classify nonnumeric values explicitly.")
        for col in [7, 9, 15, 19]:
            formula = qc_review[row - 1][col]
            if ">=0" not in formula:
                fail(f"Physically nonnegative QC formula at row {row} col {col + 1} must reject negatives.")


def validate_defaults(workbook: dict[str, Any]) -> None:
    worksheets = worksheet_by_name(workbook)
    run_setup = worksheets["Run Setup"]["data"]
    qc_review = worksheets["QC Review"]["data"]
    if run_setup[3][1] != "Terpenes":
        fail("batch_assay_name default must be Terpenes.")
    if run_setup[23][1] != build_mod.RUN_SETUP_FIELDS[22][1]:
        fail("run_setup_complete formula/default behavior changed.")
    if build_mod.run_setup_complete_formula() != run_setup[23][1]:
        fail("run_setup_complete formula must use the exact controlled field map.")
    if build_mod.run_setup_message_formula() != run_setup[24][1]:
        fail("run_setup_message formula must report the first missing controlled field.")
    if qc_review[2][1] != "decision_required":
        fail("bracketing_ccv_criterion_status default must be decision_required.")
    if qc_review[3][1] != "":
        fail("bracketing_ccv_accuracy_percent_window default must be blank.")
    if qc_review[4][1] != "decision_required":
        fail("lcs_requirement_status default must be decision_required.")
    if qc_review[14][1] != "Hold":
        fail("batch_qc_disposition default must be Hold.")
    if '$B$3="confirmed"' not in qc_review[7][1] or '$B$5="not_required"' not in qc_review[7][1]:
        fail("qc_configuration_complete must require confirmed bracketing and controlled LCS not_required status.")
    if qc_review[17][1].startswith("=") is not True:
        fail("batch_publish_ready must be formula-driven.")


def contains_forbidden_token(text: str, token: str) -> bool:
    if token in {"pass_fail", "Pass/Fail", "key/value-store"}:
        return token in text
    if token == "METRC":
        return re.search(r"\bMETRC\b", text) is not None
    return re.search(rf"\b{re.escape(token)}\b", text) is not None


def validate_no_forbidden_artifacts(workbook: dict[str, Any]) -> None:
    def walk(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                walk(key, f"{path}.{key}<key>")
                walk(child, f"{path}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{path}[{index}]")
        elif isinstance(value, str):
            for token in FORBIDDEN_CANDIDATE_TOKENS:
                if contains_forbidden_token(value, token):
                    fail(f"Forbidden Terpenes outcome/config artifact {token!r} at {path}")

    walk(workbook, "candidate")


def validate_qc_outputs(workbook: dict[str, Any]) -> None:
    qc = worksheet_by_name(workbook)["QC Review"]["data"]
    formula_text = "\n".join(str(value) for row in qc for value in row)
    for value in ALLOWED_QC_EVALUATIONS:
        if value not in formula_text:
            # not_applicable is allowed through the bracketing status control and may not appear in formula text.
            if value != "not_applicable":
                fail(f"QC evaluation value is not represented in formulas: {value}")
    for forbidden in ["Accepted", "Hold", "Rejected"]:
        qc_table_text = "\n".join(
            str(value)
            for row in qc[22:45]
            for value in row[3:23]
        )
        if forbidden in qc_table_text:
            fail(f"Individual QC evaluations must not use batch disposition value {forbidden}.")


def validate_readonly_metadata(workbook: dict[str, Any]) -> None:
    worksheets = worksheet_by_name(workbook)
    import_cells = worksheets["Instrument Import"]["cells"]
    for row in range(2, 202):
        for col in [32, 33]:
            ref = f"{build_mod.col_letter(col)}{row}"
            if import_cells.get(ref, {}).get("readonly") is not True:
                fail(f"Instrument Import formula cell {ref} must be readonly.")
        for col in [1, 4, 34, 56, 57]:
            ref = f"{build_mod.col_letter(col)}{row}"
            if import_cells.get(ref, {}).get("readonly") is not False:
                fail(f"Instrument Import input cell {ref} must be writable.")
    publish_cells = worksheets["Publish"]["cells"]
    for row in range(2, 88):
        for col in range(4, 51):
            ref = f"{build_mod.col_letter(col)}{row}"
            if publish_cells.get(ref, {}).get("readonly") is not False:
                fail(f"Publish input/source cell {ref} must be writable.")
        for col in range(51, 57):
            ref = f"{build_mod.col_letter(col)}{row}"
            if publish_cells.get(ref, {}).get("readonly") is not True:
                fail(f"Publish formula cell {ref} must be readonly.")


def validate_internal_metadata(workbook: dict[str, Any]) -> None:
    for worksheet in workbook["config"]["worksheets"]:
        row_count, col_count = worksheet_bounds(worksheet)
        if len(worksheet.get("columns", [])) != col_count:
            fail(f"{worksheet['worksheetName']} column metadata count does not match data width.")
        if len(worksheet.get("rows", [])) != row_count:
            fail(f"{worksheet['worksheetName']} row metadata count does not match data height.")
        if worksheet.get("minDimensions") != [col_count, row_count]:
            fail(f"{worksheet['worksheetName']} minDimensions are stale.")
        for collection_name in ["style", "cells", "mergeCells", "comments", "meta"]:
            collection = worksheet.get(collection_name, {})
            if not isinstance(collection, dict):
                fail(f"{worksheet['worksheetName']} {collection_name} must be an object.")
            for target in collection:
                if ":" in target:
                    start, end = target.split(":", 1)
                    assert_cell_in_bounds(worksheet, start)
                    assert_cell_in_bounds(worksheet, end)
                else:
                    assert_cell_in_bounds(worksheet, target)
    rules = workbook["config"]["plugins"]["conditionalFormatting"]["rules"]
    if rules:
        fail("No conditional-formatting rules should remain in the Prompt 4 candidate.")


def validate_hashes_and_determinism(workbook_text: str, manifest_text: str, manifest: dict[str, Any]) -> None:
    if manifest["source_active_export"]["sha256"] != build_mod.sha256_file(SOURCE_ACTIVE_EXPORT):
        fail("Active source export hash does not match the manifest.")
    for entry in manifest["prompt2_config_files"] + manifest["prompt3_dependency_files"] + manifest.get("local_config_files", []):
        path = REPO_ROOT / entry["path"]
        if entry["sha256"] != build_mod.sha256_file(path):
            fail(f"Dependency hash changed: {entry['path']}")
    _candidate, _manifest, expected_candidate_text, expected_manifest_text = build_mod.build_outputs()
    if workbook_text != expected_candidate_text:
        fail("Candidate JSON is not byte-identical to generator output.")
    if manifest_text != expected_manifest_text:
        fail("Manifest JSON is not byte-identical to generator output.")


def validate_scope_controls(workbook: dict[str, Any], manifest: dict[str, Any]) -> None:
    if workbook["qb_config"]["kvstore_config"] != {}:
        fail("qb_config.kvstore_config must remain empty.")
    for key, expected in {
        "active_or_raw_qbench_export_modified": False,
        "test_worksheet_candidate_modified": False,
        "coa_source_modified": False,
        "qbench_automation_modified": False,
        "qbench_parser_configuration_modified": False,
        "protocol_worksheet_modified": False,
        "kvstore_configuration_modified": False,
        "metrc_export_configuration_modified": False,
        "report_configuration_modified": False,
        "qbench_production_object_modified": False,
        "prompt5_started": False,
    }.items():
        if manifest["scope_controls"].get(key) is not expected:
            fail(f"Manifest scope control {key} must be {expected}.")


def validate_candidate(candidate_path: Path = CANDIDATE_PATH, manifest_path: Path = MANIFEST_PATH) -> dict[str, Any]:
    workbook_text = candidate_path.read_text(encoding="utf-8")
    manifest_text = manifest_path.read_text(encoding="utf-8")
    workbook = json.loads(workbook_text)
    manifest = json.loads(manifest_text)

    validate_tabs_and_ids(workbook, manifest)
    validate_synchronized_data(workbook)
    validate_source_publish_capacity(workbook, manifest)
    validate_channel_layout(workbook)
    validate_named_cells(workbook)
    validate_formulas(workbook)
    validate_defaults(workbook)
    validate_no_forbidden_artifacts(workbook)
    validate_qc_outputs(workbook)
    validate_readonly_metadata(workbook)
    validate_internal_metadata(workbook)
    validate_hashes_and_determinism(workbook_text, manifest_text, manifest)
    validate_scope_controls(workbook, manifest)

    named_cells = workbook["qb_config"]["named_cells"]
    return {
        "status": "ok",
        "candidate_path": repo_relative(candidate_path),
        "source_active_export_hash": manifest["source_active_export"]["sha256"],
        "tabs": workbook_tabs(workbook),
        "worksheet_ids": manifest["generated_candidate"]["worksheet_ids"],
        "formula_count": count_formulas(workbook),
        "named_cell_count": len(named_cells),
        "publish_row_capacity": manifest["generated_candidate"]["publish_row_capacity"],
        "instrument_import_row_capacity": manifest["generated_candidate"]["instrument_import_row_capacity"],
        "publish_table_range": named_cells["terpenes_batch_publish_table"]["cell"],
        "publish_analyte_range": named_cells["terpenes_batch_publish_instrument_conc"]["cell"],
        "batch_qc_disposition": named_cells["batch_qc_disposition"]["cell"],
        "batch_publish_ready": named_cells["batch_publish_ready"]["cell"],
        "bracketing_ccv_criterion_status": named_cells["bracketing_ccv_criterion_status"]["cell"],
        "lcs_requirement_status": named_cells["lcs_requirement_status"]["cell"],
        "default_batch_publication_blocked": True,
        "deterministic_generation": True,
        "prompt5_started": False,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-path", type=Path, default=CANDIDATE_PATH)
    parser.add_argument("--manifest-path", type=Path, default=MANIFEST_PATH)
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    try:
        summary = validate_candidate(args.candidate_path, args.manifest_path)
    except CandidateValidationError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, ensure_ascii=False))
        raise SystemExit(1) from exc
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
