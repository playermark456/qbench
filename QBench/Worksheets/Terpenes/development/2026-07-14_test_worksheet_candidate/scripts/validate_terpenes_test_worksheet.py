#!/usr/bin/env python3
"""Validate the generated Terpenes Test Worksheet candidate."""
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
BUILD_SCRIPT = SCRIPT_DIR / "build_terpenes_test_worksheet.py"

CANDIDATE_PATH = BASE_DIR / "dist" / "terpenes__test_ws_id_42__candidate_v1__2026-07-14.json"
MANIFEST_PATH = BASE_DIR / "dist" / "candidate_manifest.json"
SOURCE_ACTIVE_EXPORT = (
    REPO_ROOT
    / "QBench"
    / "Rescans"
    / "2026-07-04"
    / "Worksheets"
    / "Terpenes"
    / "terpenes__id_42__worksheet_export_spreadsheet__active__2026-07-04.json"
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

EXPECTED_TABS = ["Report", "Data", "Specifications"]
REPORT_HEADERS = ["Analyte", "Result (%)", "Result (mg/g)", "LOQ (mg/g)", "MU (%)"]
REPORT_LABELS = [
    "α-Pinene",
    "Camphene",
    "β-Myrcene",
    "β-Pinene",
    "Delta-3-Carene",
    "α-Terpinene",
    "Ocimene",
    "D-Limonene",
    "p-Cymene",
    "Eucalyptol",
    "γ-Terpinene",
    "Terpinolene",
    "Linalool",
    "Isopulegol",
    "Geraniol",
    "β-Caryophyllene",
    "α-Humulene",
    "Nerolidol",
    "Guaiol",
    "Caryophyllene Oxide",
    "α-Bisabolol",
    "Total Terpenes",
]
FORBIDDEN_TOKENS = ["pass_fail", "Pass", "Fail", "Not Tested", "Claim Met", "Claim Not Met"]
FORBIDDEN_FORMULA_TEXT = ["#REF!", "#NAME?", "#VALUE!", "Conc. %", "Norm Conc."]
CONTROLLED_BELOW_LOQ_REPORTING_MODES = [
    "decision_required",
    "display_less_than_loq",
    "display_numeric_result",
]
NEW_REQUIRED_NAMED_CELLS = [
    "total_ocimene_percent",
    "total_ocimene_mgg",
    "total_nerolidol_percent",
    "total_nerolidol_mgg",
    "total_terpenes_percent",
    "total_terpenes_mgg",
    "report_header",
    "report_content",
    "report_results",
    "terpenes_instrument_conc",
    "terpenes_effective_conc",
    "terpenes_results_mgg",
    "terpenes_results_percent",
    "terpenes_qualifiers",
    "analytical_results_complete",
]
CONTROL_NAMED_CELLS = [
    "qbench_test_id",
    "qbench_sample_id",
    "product_matrix",
    "sample_mass_g",
    "final_volume_ml",
    "df",
    "df_application_mode",
    "labsolutions_conc_unit",
    "labsolutions_conc_unit_confirmed",
    "preparation_values_confirmed",
    "below_loq_reporting_mode",
    "loq_source_status",
    "mu_source_status",
    "batch_qc_disposition",
    "publish_ready",
    "analytical_results_complete",
    "calculation_ready",
    "reporting_ready",
    "calculation_message",
    "source_batch_id",
    "source_instrument_file",
    "source_file_hash",
    "source_data_file",
    "source_method_file",
    "source_sequence_file",
    "parser_version",
    "imported_at",
    "instrument_name",
    "detector_id",
    "detector_name",
]


class CandidateValidationError(ValueError):
    """Raised when the candidate fails static validation."""


def load_build_module():
    spec = importlib.util.spec_from_file_location("build_terpenes_test_worksheet", BUILD_SCRIPT)
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


def count_formulas(workbook: dict[str, Any]) -> int:
    return sum(
        1 for _tab, _row, _col, value in iter_grid_cells(workbook) if isinstance(value, str) and value.startswith("=")
    )


def formulas(workbook: dict[str, Any]) -> list[str]:
    return [
        value
        for _tab, _row, _col, value in iter_grid_cells(workbook)
        if isinstance(value, str) and value.startswith("=")
    ]


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
        fail(f"Named-cell target {worksheet['worksheetName']}!{cell} is outside worksheet bounds.")


def assert_named_target_resolves(
    target: str,
    worksheets: dict[str, dict[str, Any]],
    *,
    bare_target_default_tab: str = "Specifications",
) -> None:
    tab, ref = split_target(target)
    worksheet_name = tab or bare_target_default_tab
    if worksheet_name not in worksheets:
        fail(f"Named-cell target references unknown tab: {target}")
    worksheet = worksheets[worksheet_name]
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


def contains_forbidden_token(text: str, token: str) -> bool:
    if token == "pass_fail":
        return "pass_fail" in text
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
            for token in FORBIDDEN_TOKENS:
                if contains_forbidden_token(value, token):
                    fail(f"Forbidden Terpenes result/reporting token {token!r} at {path}")

    walk(workbook, "candidate")


def validate_tabs(workbook: dict[str, Any]) -> None:
    tabs = workbook_tabs(workbook)
    if tabs != EXPECTED_TABS:
        fail(f"Expected tabs {EXPECTED_TABS}, found {tabs}.")
    if len(tabs) != len(set(tabs)):
        fail("Worksheet names must be unique.")
    worksheet_ids = [worksheet["worksheetId"] for worksheet in workbook["config"]["worksheets"]]
    if len(worksheet_ids) != len(set(worksheet_ids)):
        fail("Worksheet IDs must be unique.")
    if "METRC" in tabs:
        fail("Prompt 3 must not add a METRC tab.")


def validate_synchronized_data(workbook: dict[str, Any]) -> None:
    worksheets = worksheet_by_name(workbook)
    if set(workbook.get("data", {})) != set(worksheets):
        fail("Top-level data tabs do not match config worksheets.")
    for name, worksheet in worksheets.items():
        if workbook["data"][name] != worksheet["data"]:
            fail(f"Top-level data for {name} is not synchronized with config worksheet data.")


def validate_channel_layout(workbook: dict[str, Any], analyte_config: dict[str, Any]) -> None:
    channels = sorted(analyte_config["internal_reportable_channels"], key=lambda row: row["order"])
    labels = [row["worksheet_label"] for row in channels]
    worksheets = worksheet_by_name(workbook)
    data_tab = worksheets["Data"]["data"]
    spec_tab = worksheets["Specifications"]["data"]
    if data_tab[0][3:26] != labels:
        fail("Data!D1:Z1 does not match the Prompt 2 channel order.")
    if len(data_tab[0][3:26]) != 23:
        fail("Data!D:Z must contain exactly 23 channel headers.")
    if [row[0] for row in spec_tab[4:27]] != labels:
        fail("Specifications rows 5:27 do not match the 23 internal channels.")


def validate_report_tab(workbook: dict[str, Any]) -> None:
    report = worksheet_by_name(workbook)["Report"]["data"]
    if len(report) != 23 or any(len(row) != 5 for row in report):
        fail("Report tab must be exactly A1:E23.")
    if report[0] != REPORT_HEADERS:
        fail("Report header row does not match the required columns.")
    labels = [row[0] for row in report[1:]]
    if labels != REPORT_LABELS:
        fail("Report labels do not match the required 21-measurand order plus Total Terpenes.")
    for row_number, row in enumerate(report[1:], start=2):
        spec_row = build_mod.REPORT_ROWS[row_number - 2][1]
        percent_formula = row[1]
        mgg_formula = row[2]
        expected_percent = (
            f'=IF(DATA!$B$26<>TRUE,"",IF(SPECIFICATIONS!F{spec_row}="<LOQ",'
            f'IF(DATA!$B$19="display_less_than_loq","<LOQ",SPECIFICATIONS!D{spec_row}),'
            f'IF(SPECIFICATIONS!F{spec_row}="Reported",SPECIFICATIONS!D{spec_row},"")))'
        )
        expected_mgg = (
            f'=IF(DATA!$B$26<>TRUE,"",IF(SPECIFICATIONS!F{spec_row}="<LOQ",'
            f'IF(DATA!$B$19="display_less_than_loq","<LOQ",SPECIFICATIONS!E{spec_row}),'
            f'IF(SPECIFICATIONS!F{spec_row}="Reported",SPECIFICATIONS!E{spec_row},"")))'
        )
        if percent_formula != expected_percent:
            fail(f"Report percent formula at row {row_number} does not match controlled display logic.")
        if mgg_formula != expected_mgg:
            fail(f"Report mg/g formula at row {row_number} does not match controlled display logic.")
        for value in row[1:]:
            if not (isinstance(value, str) and value.startswith("=IF(DATA!$B$26")):
                fail("Report cells must be formula-driven and gated by reporting_ready.")
            for forbidden in ["Hold", "Review Required", "Pass", "Fail", "Not Tested"]:
                if forbidden in value:
                    fail(f"Report formula contains forbidden display text: {forbidden}")
            if "<LOQ" in value and 'DATA!$B$19="display_less_than_loq"' not in value:
                fail("<LOQ may appear only through controlled below-LOQ display logic.")


def validate_named_cells(workbook: dict[str, Any]) -> dict[str, Any]:
    source = load_json(SOURCE_ACTIVE_EXPORT)
    source_named = source["qb_config"]["named_cells"]
    candidate_named = workbook["qb_config"]["named_cells"]
    if len(source_named) != 47:
        fail(f"Expected 47 source compatibility named cells, found {len(source_named)}.")
    for name, value in source_named.items():
        if candidate_named.get(name) != value:
            fail(f"Compatibility named cell {name} was not preserved exactly.")
    for name in NEW_REQUIRED_NAMED_CELLS + CONTROL_NAMED_CELLS:
        if name not in candidate_named:
            fail(f"Missing required named cell: {name}")
    if len(candidate_named) != len(set(candidate_named)):
        fail("Named-cell system names must be unique.")
    worksheets = worksheet_by_name(workbook)
    seen_display_targets: set[tuple[str, str]] = set()
    for name, item in candidate_named.items():
        target = item.get("cell", "")
        assert_named_target_resolves(target, worksheets)
        pair = (str(item.get("display_name", "")), target)
        if pair in seen_display_targets and item.get("display_name"):
            fail(f"Duplicate named-cell target/display pair found at {name}: {pair}")
        seen_display_targets.add(pair)
    if candidate_named["report_results"]["cell"] != "Report!A1:E23":
        fail("report_results must point to Report!A1:E23.")
    if candidate_named["report_header"]["cell"] != "Report!A1:E1":
        fail("report_header must point to Report!A1:E1.")
    if candidate_named["report_content"]["cell"] != "Report!A2:E23":
        fail("report_content must point to Report!A2:E23.")
    return {"source_named_count": len(source_named), "candidate_named_count": len(candidate_named)}


def validate_formulas(workbook: dict[str, Any]) -> None:
    valid_formula_tabs = {"DATA", "SPECIFICATIONS", "REPORT"}
    for formula in formulas(workbook):
        for forbidden in FORBIDDEN_FORMULA_TEXT:
            if forbidden in formula:
                fail(f"Formula contains forbidden text {forbidden}: {formula}")
        for tab in re.findall(r"([A-Z][A-Z0-9 _]*)!", formula):
            if tab not in valid_formula_tabs:
                fail(f"Formula references unknown worksheet tab {tab}: {formula}")

    formula_text = "\n".join(formulas(workbook))
    for required in [
        '$B$17="TRUE"',
        '$B$16="ug/mL"',
        '$B$18="TRUE"',
        "AND(ISNUMBER($B$12),$B$12>0)",
        "AND(ISNUMBER($B$13),$B$13>0)",
        "AND($B$15=\"apply_in_qbench\",ISNUMBER($B$14),$B$14>0)",
        '"already_applied_by_labsolutions"',
        '"apply_in_qbench"',
        "COUNT($D$2:$Z$2)=23",
        "COUNT($D$4:$Z$4)=23",
        '$B$24=TRUE',
        '$B$22="Accepted"',
        '$B$23="TRUE"',
        '$B$19="display_less_than_loq"',
        '$B$19="display_numeric_result"',
        "Below-LOQ reporting mode required",
        "Analytical results incomplete",
    ]:
        if required not in formula_text:
            fail(f"Required gate fragment missing from formulas: {required}")
    if '$B$19<>"decision_required"' in formula_text:
        fail("reporting_ready must use the controlled below-LOQ value set, not a non-default shortcut.")
    if "IFERROR" in formula_text:
        fail("Prompt 3 formulas must not use IFERROR to hide invalid configuration.")


def validate_result_formulas(workbook: dict[str, Any]) -> None:
    data = worksheet_by_name(workbook)["Data"]["data"]
    for col in range(4, 27):
        label = build_mod.col_letter(col)
        if not data[2][col - 1].startswith(f'=IF({label}2="","",IF($B$25<>TRUE,"",{label}2*'):
            fail(f"Missing effective concentration formula at Data!{label}3.")
        if not data[3][col - 1].startswith(f'=IF({label}3="","",IF($B$25<>TRUE,"",{label}3*$B$13/$B$12/1000))'):
            fail(f"Missing mg/g formula at Data!{label}4.")
        if data[4][col - 1] != f'=IF({label}4="","",{label}4/10)':
            fail(f"Missing percent formula at Data!{label}5.")
        if not data[5][col - 1].startswith(f'=IF({label}2="","",IF($B$25<>TRUE,"Review Required"'):
            fail(f"Missing qualifier formula at Data!{label}6.")


def validate_totals(workbook: dict[str, Any]) -> None:
    spec = worksheet_by_name(workbook)["Specifications"]["data"]
    if spec[27][3] != '=IF(COUNT(D11,D14)=2,SUM(D11,D14),"")':
        fail("Total Ocimene percent formula must require both numeric components.")
    if spec[27][4] != '=IF(COUNT(E11,E14)=2,SUM(E11,E14),"")':
        fail("Total Ocimene mg/g formula must require both numeric components.")
    if spec[28][3] != '=IF(COUNT(D23,D24)=2,SUM(D23,D24),"")':
        fail("Total Nerolidol percent formula must require both numeric components.")
    if spec[28][4] != '=IF(COUNT(E23,E24)=2,SUM(E23,E24),"")':
        fail("Total Nerolidol mg/g formula must require both numeric components.")
    if spec[29][3] != '=IF(COUNT(D5:D27)=23,SUM(D5:D27),"")':
        fail("Total Terpenes percent formula must require 23 numeric internal channel results.")
    if spec[29][4] != '=IF(COUNT(E5:E27)=23,SUM(E5:E27),"")':
        fail("Total Terpenes mg/g formula must require 23 numeric internal channel results.")
    for expected in ["SUM(D5:D27)", "SUM(E5:E27)"]:
        if expected not in "\n".join([spec[29][3], spec[29][4]]):
            fail(f"Total Terpenes formula must include {expected}.")
    total_formula = spec[29][3] + spec[29][4]
    if "D28" in total_formula or "D29" in total_formula or "E28" in total_formula or "E29" in total_formula:
        fail("Total Terpenes must not double-count Ocimene or Nerolidol rollup rows.")


def validate_default_gates(workbook: dict[str, Any]) -> None:
    data = worksheet_by_name(workbook)["Data"]["data"]
    expected = {
        15: "capture_only_until_method_validated",
        16: "ug/mL",
        17: "FALSE",
        18: "FALSE",
        19: "decision_required",
        20: "decision_required",
        21: "decision_required",
        22: "Hold",
        23: "FALSE",
    }
    for row, value in expected.items():
        if data[row - 1][1] != value:
            fail(f"Default gate Data!B{row} must be {value!r}.")
    if data[23][1] != "=IF(AND(COUNT($D$2:$Z$2)=23,COUNT($D$4:$Z$4)=23),TRUE,FALSE)":
        fail("analytical_results_complete must require 23 numeric inputs and 23 numeric mg/g results.")
    calculation_formula = data[24][1]
    for fragment in [
        "AND(ISNUMBER($B$12),$B$12>0)",
        "AND(ISNUMBER($B$13),$B$13>0)",
        'AND($B$15="apply_in_qbench",ISNUMBER($B$14),$B$14>0)',
    ]:
        if fragment not in calculation_formula:
            fail(f"calculation_ready missing numeric preparation gate: {fragment}")
    reporting_formula = data[25][1]
    for fragment in [
        "$B$25=TRUE",
        "$B$24=TRUE",
        '$B$19="display_less_than_loq"',
        '$B$19="display_numeric_result"',
    ]:
        if fragment not in reporting_formula:
            fail(f"reporting_ready missing required gate: {fragment}")


def validate_readonly_metadata(workbook: dict[str, Any]) -> None:
    worksheets = worksheet_by_name(workbook)
    data_cells = worksheets["Data"]["cells"]
    for col in range(4, 27):
        input_ref = f"{build_mod.col_letter(col)}2"
        if data_cells.get(input_ref, {}).get("readonly") is not False:
            fail(f"Instrument input cell Data!{input_ref} must be writable.")
        for row in [3, 4, 5, 6]:
            ref = f"{build_mod.col_letter(col)}{row}"
            if data_cells.get(ref, {}).get("readonly") is not True:
                fail(f"Formula cell Data!{ref} must be readonly.")
    for tab in ["Specifications", "Report"]:
        for _ref, metadata in worksheets[tab]["cells"].items():
            if metadata.get("readonly") is not True:
                fail(f"{tab} formula/support cell metadata must be readonly.")


def validate_internal_metadata(workbook: dict[str, Any]) -> None:
    worksheets = worksheet_by_name(workbook)
    for worksheet in worksheets.values():
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
    conditional_rules = workbook["config"]["plugins"]["conditionalFormatting"]["rules"]
    if conditional_rules:
        fail("No conditional-formatting rules should remain in the Prompt 3 candidate.")


def validate_hashes_and_determinism(workbook_text: str, manifest_text: str, manifest: dict[str, Any]) -> None:
    source_entry = manifest["source_active_export"]
    if source_entry["sha256"] != build_mod.sha256_file(SOURCE_ACTIVE_EXPORT):
        fail("Active source export hash does not match the manifest.")
    for config_entry in manifest["prompt2_config_files"]:
        path = REPO_ROOT / config_entry["path"]
        if config_entry["sha256"] != build_mod.sha256_file(path):
            fail(f"Prompt 2 config hash changed: {config_entry['path']}")
    _candidate, _manifest, expected_candidate_text, expected_manifest_text = build_mod.build_outputs()
    if workbook_text != expected_candidate_text:
        fail("Candidate JSON is not byte-identical to generator output.")
    if manifest_text != expected_manifest_text:
        fail("Manifest JSON is not byte-identical to generator output.")


def validate_manifest_controls(manifest: dict[str, Any]) -> None:
    gates = manifest["default_decision_gates"]
    if gates.get("controlled_below_loq_reporting_modes") != CONTROLLED_BELOW_LOQ_REPORTING_MODES:
        fail("Manifest must record the exact controlled below-LOQ reporting mode set.")
    if gates.get("analytical_results_complete") != "formula_false_by_default":
        fail("Manifest must record analytical_results_complete as a default reporting gate.")


def validate_candidate(candidate_path: Path = CANDIDATE_PATH, manifest_path: Path = MANIFEST_PATH) -> dict[str, Any]:
    workbook_text = candidate_path.read_text(encoding="utf-8")
    manifest_text = manifest_path.read_text(encoding="utf-8")
    workbook = json.loads(workbook_text)
    manifest = json.loads(manifest_text)
    analyte_config = load_json(ANALYTE_CONFIG)

    validate_tabs(workbook)
    validate_synchronized_data(workbook)
    validate_channel_layout(workbook, analyte_config)
    validate_report_tab(workbook)
    named_summary = validate_named_cells(workbook)
    validate_formulas(workbook)
    validate_result_formulas(workbook)
    validate_totals(workbook)
    validate_default_gates(workbook)
    validate_no_forbidden_artifacts(workbook)
    validate_readonly_metadata(workbook)
    validate_internal_metadata(workbook)
    validate_hashes_and_determinism(workbook_text, manifest_text, manifest)
    validate_manifest_controls(manifest)

    if workbook["qb_config"]["kvstore_config"] != {}:
        fail("qb_config.kvstore_config must remain empty for Prompt 3.")
    if manifest["scope_controls"]["prompt4_started"] is not False:
        fail("Prompt 4 must not be started.")
    if manifest["scope_controls"]["active_or_raw_qbench_export_modified"] is not False:
        fail("Manifest must not mark active/raw QBench exports as modified.")

    return {
        "status": "ok",
        "candidate_path": repo_relative(candidate_path),
        "source_active_export_hash": manifest["source_active_export"]["sha256"],
        "formula_count": count_formulas(workbook),
        "named_cell_count": named_summary["candidate_named_count"],
        "preserved_compatibility_named_cell_count": named_summary["source_named_count"],
        "report_results_range": workbook["qb_config"]["named_cells"]["report_results"]["cell"],
        "analytical_results_complete": workbook["qb_config"]["named_cells"]["analytical_results_complete"]["cell"],
        "controlled_below_loq_reporting_modes": CONTROLLED_BELOW_LOQ_REPORTING_MODES,
        "tabs": workbook_tabs(workbook),
        "kvstore_config_empty": workbook["qb_config"]["kvstore_config"] == {},
        "deterministic_generation": True,
        "prompt4_started": False,
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
