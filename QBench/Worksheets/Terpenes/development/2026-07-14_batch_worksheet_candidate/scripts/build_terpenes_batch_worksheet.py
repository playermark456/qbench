#!/usr/bin/env python3
"""Build the nonproduction Terpenes Batch Worksheet candidate."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
REPO_ROOT = SCRIPT_DIR.parents[5]

PROMPT_DATE = "2026-07-14"
PACKAGE_NAME = "2026-07-14_batch_worksheet_candidate"
SOURCE_ACTIVE_EXPORT = (
    REPO_ROOT
    / "QBench"
    / "Rescans"
    / "2026-07-04"
    / "Worksheets"
    / "Terpenes"
    / "terpenes__id_43__worksheet_export_spreadsheet__active__2026-07-04.json"
)
PROMPT2_DIR = (
    REPO_ROOT
    / "QBench"
    / "Worksheets"
    / "Terpenes"
    / "development"
    / "2026-07-14_config_parser_foundation"
)
PROMPT3_DIR = (
    REPO_ROOT
    / "QBench"
    / "Worksheets"
    / "Terpenes"
    / "development"
    / "2026-07-14_test_worksheet_candidate"
)
PROMPT2_CONFIG_FILES = [
    PROMPT2_DIR / "config" / "terpenes_analytes.json",
    PROMPT2_DIR / "config" / "terpenes_qc.json",
    PROMPT2_DIR / "config" / "metrc_profiles.json",
]
PROMPT3_DEPENDENCY_FILES = [
    PROMPT3_DIR / "dist" / "terpenes__test_ws_id_42__candidate_v1__2026-07-14.json",
    PROMPT3_DIR / "dist" / "candidate_manifest.json",
]
LAYOUT_CONFIG = BASE_DIR / "config" / "terpenes_batch_layout.json"
IMPORT_CONTRACT_CONFIG = BASE_DIR / "config" / "terpenes_batch_import_contract.json"
CANDIDATE_PATH = BASE_DIR / "dist" / "terpenes__batch_ws_id_43__candidate_v1__2026-07-14.json"
MANIFEST_PATH = BASE_DIR / "dist" / "candidate_manifest.json"

RUN_SETUP_WORKSHEET_ID = "cf71364f-84b3-4558-a14c-241b452bd7bb"
INSTRUMENT_IMPORT_WORKSHEET_ID = "f11a5887-6f11-4a45-ae16-9a0f9f64dd16"
QC_REVIEW_WORKSHEET_ID = "adc806c8-3a02-4c6f-b8c6-6738df2fe02d"
PUBLISH_SOURCE_SHEET_NAME = "Sheet1"
PUBLISH_TAB_NAME = "Publish"

IMPORT_CAPACITY = 200
PUBLISH_HEADER_ROW_COUNT = 1
QC_TABLE_START_ROW = 19

SAMPLE_TYPES = [
    "Calibration Standard",
    "Initial CCV",
    "Continuing CCV",
    "Blank",
    "LOQ Check",
    "Matrix Spike",
    "Duplicate",
    "Unknown",
    "Dilution",
    "Other QC",
]
PUBLISH_SAMPLE_TYPES = ["Unknown", "Dilution"]
MANUAL_INTEGRATION_VALUES = ["No", "Yes"]
INTEGRATION_REVIEW_VALUES = ["Not Reviewed", "Reviewed", "Review Required"]
IMPORT_STATUS_VALUES = ["Valid", "Review Required", "Rejected"]
DF_APPLICATION_MODES = ["already_applied_by_labsolutions", "apply_in_qbench"]
BATCH_QC_DISPOSITIONS = ["Accepted", "Hold", "Rejected"]
INTERNAL_QC_EVALUATION_VALUES = [
    "within_criteria",
    "outside_criteria",
    "decision_required",
    "not_evaluated",
    "not_applicable",
    "review_required",
]

RUN_SETUP_FIELDS = [
    ("batch_qbench_id", "", "QBench batch ID or display ID"),
    ("analytical_batch_id", "", "Required analytical run identifier"),
    ("batch_assay_name", "Terpenes", "Fixed assay name"),
    ("run_instrument_name", "", "Required instrument name"),
    ("run_detector_id", "", "Required detector ID"),
    ("run_detector_name", "", "Required detector name"),
    ("run_method_file", "", "Required method file"),
    ("run_sequence_file", "", "Required sequence or batch file"),
    ("run_column", "", "Analytical column identifier"),
    ("run_carrier_gas", "", "Carrier gas"),
    ("run_analyst", "", "Required analyst"),
    ("run_start", "", "Required run start"),
    ("run_end", "", "Required run end"),
    ("calibration_id", "", "Calibration identifier"),
    ("standard_lot", "", "Standard lot"),
    ("extraction_solvent_lot", "", "Extraction solvent lot"),
    ("parser_version", "", "Parser/config package version"),
    ("source_package_version", "2026-07-14_config_parser_foundation", "Controlled source package"),
    ("raw_ascii_attachment_reference", "", "QBench attachment or file reference"),
    ("raw_batch_manifest_hash", "", "Required source manifest hash"),
    ("run_setup_reviewed_by", "", "Required reviewer"),
    ("run_setup_reviewed_at", "", "Required review timestamp"),
    (
        "run_setup_complete",
        '=IF(AND($B$3<>"",$B$4<>"",$B$5<>"",$B$6<>"",$B$7<>"",$B$8<>"",$B$11<>"",$B$12<>"",$B$13<>"",$B$20<>"",$B$21<>"",$B$22<>""),TRUE,FALSE)',
        "Formula gate only; not laboratory approval",
    ),
    (
        "run_setup_message",
        '=IF($B$3="","Analytical batch ID required",IF($B$4="","Instrument required",IF($B$7="","Method file required",IF($B$8="","Sequence file required",IF($B$11="","Analyst required",IF(OR($B$12="",$B$13=""),"Run time required",IF($B$20="","Source manifest required",IF(OR($B$21="",$B$22=""),"Run setup review required","Run setup complete"))))))))',
        "First neutral run setup message",
    ),
]

IMPORT_LEADING_HEADERS = [
    "import_row_id",
    "run_order",
    "vial",
    "sample_type",
    "qbench_test_id",
    "qbench_sample_id",
    "product_matrix",
    "sample_mass_g",
    "final_volume_ml",
    "qbench_df",
    "df_application_mode",
    "labsolutions_sample_amount",
    "labsolutions_dilution_factor",
    "source_instrument_file",
    "source_file_hash",
    "source_data_file",
    "source_method_file",
    "source_sequence_file",
    "acquired_at",
    "instrument_name",
    "detector_id",
    "detector_name",
    "parser_version",
    "compound_result_row_count",
    "peak_table_row_count",
    "reportable_compound_row_count",
    "dimethylacetamide_conc",
    "unknown_peak_count",
    "manual_integration",
    "integration_reason",
    "integration_review_status",
    "import_validation_status",
    "import_message",
]
IMPORT_SOURCE_ROW_HASH_HEADER = "source_row_hash"

QC_CONTROL_ROWS = [
    ("qc_config_version", "2026-07-14-prompt4", "Prompt 2 QC config version used"),
    ("bracketing_ccv_criterion_status", "decision_required", "Known unresolved criterion"),
    ("bracketing_ccv_accuracy_percent_window", "", "Blank until method owner decision"),
    (
        "qc_configuration_complete",
        '=IF(AND($B$3<>"decision_required",OR($B$3="not_applicable",ISNUMBER($B$4))),TRUE,FALSE)',
        "False while bracketing CCV is unresolved",
    ),
    (
        "integration_review_complete",
        '=IF(AND(COUNTIF(\'Instrument Import\'!A2:A201,"<>")>0,COUNTIF(\'Instrument Import\'!AE2:AE201,"Reviewed")=COUNTIF(\'Instrument Import\'!A2:A201,"<>")),TRUE,FALSE)',
        "All populated import rows reviewed",
    ),
    (
        "qc_data_complete",
        '=IF(AND(COUNTIF(W20:W42,"not_evaluated")=0,COUNTIF(W20:W42,"review_required")=0),TRUE,FALSE)',
        "All analyte QC rows evaluated",
    ),
    (
        "qc_review_complete",
        '=IF(AND($B$7=TRUE,COUNTIF(W20:W42,"decision_required")=0,$B$13<>"",$B$14<>""),TRUE,FALSE)',
        "QC data reviewed with no release-blocking decision",
    ),
    (
        "all_publish_rows_valid",
        '=IF(AND($B$11>0,COUNTIF(Publish!BB2:BB87,FALSE)=0),TRUE,FALSE)',
        "All populated Publish rows meet row prerequisites",
    ),
    (
        "duplicate_test_id_count",
        '=COUNTIF(Publish!BD2:BD87,"Duplicate Test ID")',
        "Duplicate QBench Test IDs across Publish rows",
    ),
    (
        "populated_publish_row_count",
        '=COUNTIF(Publish!A2:A87,"<>")',
        "Populated Publish rows",
    ),
    ("batch_qc_disposition", "Hold", "Internal analytical batch disposition"),
    ("batch_qc_reviewer", "", "Required reviewer before release"),
    ("batch_qc_reviewed_at", "", "Required review timestamp before release"),
    (
        "batch_publish_ready",
        '=IF(AND($B$5=TRUE,$B$6=TRUE,$B$7=TRUE,$B$8=TRUE,$B$9=TRUE,$B$10=0,$B$12="Accepted",$B$13<>"",$B$14<>""),TRUE,FALSE)',
        "Batch release gate; false by default",
    ),
    (
        "batch_publish_message",
        '=IF($B$5<>TRUE,"QC configuration incomplete",IF($B$6<>TRUE,"Integration review incomplete",IF($B$7<>TRUE,"QC data incomplete",IF($B$8<>TRUE,"QC review incomplete",IF($B$9<>TRUE,"Publish rows incomplete",IF($B$10>0,"Duplicate Test ID",IF($B$12<>"Accepted","Batch QC on hold",IF(OR($B$13="",$B$14=""),"Batch release review required","Ready for transfer"))))))))',
        "First neutral batch release message",
    ),
]

QC_TABLE_HEADERS = [
    "Analyte",
    "Internal Key",
    "Calibration r",
    "Calibration Evaluation",
    "Initial CCV Recovery (%)",
    "Initial CCV Recovery Evaluation",
    "Initial CCV RSD (%)",
    "Initial CCV RSD Evaluation",
    "Blank Fraction LOQ",
    "Blank Evaluation",
    "LOQ Recovery (%)",
    "LOQ Evaluation",
    "Matrix Spike Recovery (%)",
    "Matrix Spike Evaluation",
    "Duplicate Difference (%)",
    "Duplicate Evaluation",
    "Bracketing CCV Recovery (%)",
    "Bracketing CCV Evaluation",
    "Retention Time Drift (min)",
    "Retention Time Evaluation",
    "Resolution",
    "Resolution Evaluation",
    "Overall Evaluation",
    "Reviewer Notes",
]

PUBLISH_PREFIX_HEADERS = ["QBench Test ID", "QBench Sample ID", "Product Matrix"]
PUBLISH_SUFFIX_HEADERS = [
    "Sample Mass",
    "Final Volume",
    "DF",
    "DF Application Mode",
    "LabSolutions Conc. Unit",
    "Unit Confirmed",
    "Preparation Values Confirmed",
    "Source Batch ID",
    "Source Instrument File",
    "Source File Hash",
    "Source Data File",
    "Source Method File",
    "Source Sequence File",
    "Parser Version",
    "Imported At",
    "Instrument Name",
    "Detector ID",
    "Detector Name",
    "Source Injection ID",
    "Source Row Hash",
    "Dimethylacetamide Conc.",
    "Compound Results Complete",
    "Integration Review Status",
    "Import Validation Status",
    "Batch QC Disposition",
    "Analytical Values Complete",
    "Source/Audit Complete",
    "Row Prerequisites Complete",
    "Publish Ready",
    "Publish Message",
]


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json_text(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def col_letter(index: int) -> str:
    letters = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def cell_ref(row: int, col: int) -> str:
    return f"{col_letter(col)}{row}"


def blank_grid(rows: int, cols: int) -> list[list[Any]]:
    return [["" for _ in range(cols)] for _ in range(rows)]


def row_meta(rows: int, height: int = 27) -> list[dict[str, Any]]:
    return [{"height": height} for _ in range(rows)]


def column_meta(widths: list[int]) -> list[dict[str, Any]]:
    return [{"type": "text", "width": width} for width in widths]


def cell_meta(readonly: bool, width: int, x: int) -> dict[str, Any]:
    return {"readonly": readonly, "type": "text", "width": width, "x": x}


def set_cell_metadata(
    cells: dict[str, dict[str, Any]],
    row: int,
    col: int,
    *,
    readonly: bool,
    widths: list[int],
) -> None:
    cells[cell_ref(row, col)] = cell_meta(readonly, widths[col - 1], col - 1)


def style_range(style: dict[str, int], row: int, start_col: int, end_col: int, style_id: int) -> None:
    for col in range(start_col, end_col + 1):
        style[cell_ref(row, col)] = style_id


def formula_count(workbook: dict[str, Any]) -> int:
    count = 0
    for worksheet in workbook["config"]["worksheets"]:
        for row in worksheet.get("data", []):
            for value in row:
                if isinstance(value, str) and value.startswith("="):
                    count += 1
    return count


def add_named_cell(named_cells: dict[str, Any], name: str, cell: str, display_name: str = "") -> None:
    named_cells[name] = {"cell": cell, "display_name": display_name, "export": True}


def channels() -> list[dict[str, Any]]:
    analyte_config = read_json(PROMPT2_CONFIG_FILES[0])
    rows = list(analyte_config["internal_reportable_channels"])
    rows.sort(key=lambda row: row["order"])
    return rows


def source_publish_capacity(source: dict[str, Any]) -> int:
    rows = source["data"][PUBLISH_SOURCE_SHEET_NAME]
    return sum(
        1
        for row in rows
        if row
        and isinstance(row[0], str)
        and row[0].startswith("${tests[")
        and ".get_display_id()" in row[0]
    )


def source_publish_placeholders(source: dict[str, Any]) -> list[dict[str, str]]:
    rows = source["data"][PUBLISH_SOURCE_SHEET_NAME]
    placeholders: list[dict[str, str]] = []
    for row in rows:
        if row and isinstance(row[0], str) and row[0].startswith("${tests["):
            placeholders.append({"test_id": row[0], "product_matrix": row[1] if len(row) > 1 else ""})
    return placeholders


def import_headers(analytes: list[dict[str, Any]]) -> list[str]:
    return (
        IMPORT_LEADING_HEADERS
        + [row["worksheet_label"] for row in analytes]
        + [IMPORT_SOURCE_ROW_HASH_HEADER]
    )


def import_issue_formula(row: int) -> str:
    analyte_range = f"AH{row}:BD{row}"
    sample_type_check = "OR(" + ",".join(f'D{row}="{value}"' for value in SAMPLE_TYPES) + ")"
    return (
        f'=IF(A{row}="","",'
        f'IF({sample_type_check}<>TRUE,"Sample type required",'
        f'IF(AND(OR(D{row}="Unknown",D{row}="Dilution"),E{row}=""),"QBench Test ID required",'
        f'IF(AND(H{row}<>"",OR(ISNUMBER(H{row})<>TRUE,H{row}<=0)),"Sample mass required",'
        f'IF(AND(I{row}<>"",OR(ISNUMBER(I{row})<>TRUE,I{row}<=0)),"Final volume required",'
        f'IF(AND(K{row}<>"",K{row}<>"already_applied_by_labsolutions",K{row}<>"apply_in_qbench"),"Dilution mode required",'
        f'IF(AND(K{row}="apply_in_qbench",OR(ISNUMBER(J{row})<>TRUE,J{row}<=0)),"Dilution factor required",'
        f'IF(X{row}<>24,"Compound Results row count required",'
        f'IF(Z{row}<>23,"Reportable analyte count required",'
        f'IF(AND(OR(D{row}="Unknown",D{row}="Dilution"),COUNT({analyte_range})<>23),"Analytical values incomplete",'
        f'IF(ISNUMBER(AA{row})<>TRUE,"Dimethylacetamide audit value required",'
        f'IF(AND(AC{row}<>"No",AC{row}<>"Yes"),"Manual integration value required",'
        f'IF(AND(AC{row}="Yes",AD{row}=""),"Integration reason required",'
        f'IF(AND(AE{row}<>"Not Reviewed",AE{row}<>"Reviewed",AE{row}<>"Review Required"),"Integration review required",'
        f'IF(AND(OR(AB{row}>0,AC{row}="Yes"),AE{row}<>"Reviewed"),"Integration review required",'
        f'IF(OR(N{row}="",O{row}="",P{row}="",Q{row}="",R{row}="",T{row}="",U{row}="",V{row}="",W{row}="",BE{row}=""),"Source traceability incomplete",'
        f'"Import row valid")))))))))))))))))'
    )


def import_status_formula(row: int) -> str:
    return (
        f'=IF(A{row}="","",'
        f'IF(OR(AG{row}="Sample type required",AG{row}="QBench Test ID required",'
        f'AG{row}="Compound Results row count required",AG{row}="Reportable analyte count required",'
        f'AG{row}="Analytical values incomplete",AG{row}="Dimethylacetamide audit value required"),'
        f'"Rejected",IF(AG{row}="Import row valid","Valid","Review Required")))'
    )


def build_run_setup_tab() -> tuple[list[list[Any]], list[int], dict[str, int], dict[str, dict[str, Any]]]:
    rows = 1 + len(RUN_SETUP_FIELDS)
    widths = [240, 260, 420]
    data = blank_grid(rows, 3)
    data[0] = ["Field", "Value", "Notes"]
    for index, (field, value, note) in enumerate(RUN_SETUP_FIELDS, start=2):
        data[index - 1] = [field, value, note]

    style: dict[str, int] = {}
    style_range(style, 1, 1, 3, 2)
    for row in range(2, rows + 1):
        style[cell_ref(row, 1)] = 0

    cells: dict[str, dict[str, Any]] = {}
    readonly_formula_fields = {"run_setup_complete", "run_setup_message", "batch_assay_name", "source_package_version"}
    for row in range(1, rows + 1):
        for col in range(1, 4):
            readonly = True
            if col == 2 and row > 1 and data[row - 1][0] not in readonly_formula_fields:
                readonly = False
            set_cell_metadata(cells, row, col, readonly=readonly, widths=widths)
    return data, widths, style, cells


def build_import_tab(analytes: list[dict[str, Any]]) -> tuple[list[list[Any]], list[int], dict[str, int], dict[str, dict[str, Any]]]:
    headers = import_headers(analytes)
    rows = 1 + IMPORT_CAPACITY
    cols = len(headers)
    widths = [118, 80, 70, 150, 135, 140, 150, 110, 120, 95, 190, 145, 165]
    widths += [180, 180, 180, 180, 190, 145, 155, 120, 155, 125, 150, 130, 185, 170, 140]
    widths += [130, 170, 160, 160, 220]
    widths += [120] * 23
    widths += [180]
    data = blank_grid(rows, cols)
    data[0] = headers
    for row in range(2, rows + 1):
        data[row - 1][31] = import_status_formula(row)
        data[row - 1][32] = import_issue_formula(row)

    style: dict[str, int] = {}
    style_range(style, 1, 1, cols, 2)
    for row in range(2, rows + 1):
        style[cell_ref(row, 32)] = 1
        style[cell_ref(row, 33)] = 1

    cells: dict[str, dict[str, Any]] = {}
    for row in range(1, rows + 1):
        for col in range(1, cols + 1):
            readonly = row == 1 or col in {32, 33}
            set_cell_metadata(cells, row, col, readonly=readonly, widths=widths)
    return data, widths, style, cells


def eval_between(value_cell: str, low: Any, high: Any) -> str:
    return (
        f'=IF({value_cell}="","not_evaluated",'
        f'IF(AND(ISNUMBER({value_cell}),{value_cell}>={low},{value_cell}<={high}),'
        f'"within_criteria","outside_criteria"))'
    )


def eval_max(value_cell: str, maximum: Any) -> str:
    return (
        f'=IF({value_cell}="","not_evaluated",'
        f'IF(AND(ISNUMBER({value_cell}),{value_cell}<={maximum}),'
        f'"within_criteria","outside_criteria"))'
    )


def eval_min(value_cell: str, minimum: Any) -> str:
    return (
        f'=IF({value_cell}="","not_evaluated",'
        f'IF(AND(ISNUMBER({value_cell}),{value_cell}>={minimum}),'
        f'"within_criteria","outside_criteria"))'
    )


def bracketing_eval_formula(row: int) -> str:
    return (
        f'=IF($B$3="decision_required","decision_required",'
        f'IF(Q{row}="","not_evaluated",'
        f'IF(OR($B$4="",ISNUMBER($B$4)<>TRUE),"decision_required",'
        f'IF(AND(ISNUMBER(Q{row}),Q{row}>=(100-$B$4),Q{row}<=(100+$B$4)),'
        f'"within_criteria","outside_criteria"))))'
    )


def overall_qc_formula(row: int) -> str:
    eval_range = f"D{row}:V{row}"
    return (
        f'=IF(COUNTIF({eval_range},"outside_criteria")>0,"outside_criteria",'
        f'IF(COUNTIF({eval_range},"decision_required")>0,"decision_required",'
        f'IF(COUNTIF({eval_range},"review_required")>0,"review_required",'
        f'IF(COUNTIF({eval_range},"not_evaluated")>0,"not_evaluated","within_criteria"))))'
    )


def build_qc_review_tab(analytes: list[dict[str, Any]]) -> tuple[list[list[Any]], list[int], dict[str, int], dict[str, dict[str, Any]]]:
    qc = read_json(PROMPT2_CONFIG_FILES[1])["qc_criteria"]
    rows = QC_TABLE_START_ROW + len(analytes)
    cols = len(QC_TABLE_HEADERS)
    widths = [175, 150] + [120, 170] * 10 + [170, 260]
    data = blank_grid(rows, cols)
    data[0][0:3] = ["Field", "Value", "Notes"]
    for index, (field, value, note) in enumerate(QC_CONTROL_ROWS, start=2):
        data[index - 1][0:3] = [field, value, note]
    header_row = QC_TABLE_START_ROW
    data[header_row - 1] = QC_TABLE_HEADERS[:]
    for offset, channel in enumerate(analytes):
        row = QC_TABLE_START_ROW + 1 + offset
        data[row - 1][0] = channel["worksheet_label"]
        data[row - 1][1] = channel["internal_key"]
        data[row - 1][3] = eval_min(f"C{row}", qc["calibration_r_min"])
        data[row - 1][5] = eval_between(
            f"E{row}",
            100 - qc["initial_ccv_accuracy_percent_window"],
            100 + qc["initial_ccv_accuracy_percent_window"],
        )
        data[row - 1][7] = eval_max(f"G{row}", qc["initial_ccv_rsd_max_percent"])
        data[row - 1][9] = eval_max(f"I{row}", qc["blank_max_fraction_of_loq"])
        data[row - 1][11] = eval_between(
            f"K{row}",
            qc["loq_recovery_min_percent"],
            qc["loq_recovery_max_percent"],
        )
        data[row - 1][13] = eval_between(
            f"M{row}",
            qc["matrix_spike_recovery_min_percent"],
            qc["matrix_spike_recovery_max_percent"],
        )
        data[row - 1][15] = eval_max(f"O{row}", qc["duplicate_difference_max_percent"])
        data[row - 1][17] = bracketing_eval_formula(row)
        data[row - 1][19] = eval_max(f"S{row}", qc["rt_drift_window_min"])
        data[row - 1][21] = eval_min(f"U{row}", qc["resolution_min"])
        data[row - 1][22] = overall_qc_formula(row)

    style: dict[str, int] = {}
    style_range(style, 1, 1, 3, 2)
    style_range(style, header_row, 1, cols, 2)
    for row in range(2, len(QC_CONTROL_ROWS) + 2):
        style[cell_ref(row, 1)] = 0
    for row in range(header_row + 1, rows + 1):
        style[cell_ref(row, 1)] = 0
        style[cell_ref(row, 2)] = 0
        for col in [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 23]:
            style[cell_ref(row, col)] = 1

    cells: dict[str, dict[str, Any]] = {}
    formula_control_fields = {
        "qc_configuration_complete",
        "integration_review_complete",
        "qc_data_complete",
        "qc_review_complete",
        "all_publish_rows_valid",
        "duplicate_test_id_count",
        "populated_publish_row_count",
        "batch_publish_ready",
        "batch_publish_message",
    }
    for row in range(1, rows + 1):
        for col in range(1, cols + 1):
            value = data[row - 1][col - 1]
            has_formula = isinstance(value, str) and value.startswith("=")
            has_value = value not in ("", None)
            if not has_value and not has_formula and row != header_row:
                continue
            readonly = True
            if row > 1 and row <= len(QC_CONTROL_ROWS) + 1 and col == 2:
                field_name = data[row - 1][0]
                readonly = field_name in formula_control_fields
            elif row > header_row and col in {3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 24}:
                readonly = False
            set_cell_metadata(cells, row, col, readonly=readonly, widths=widths)
    return data, widths, style, cells


def publish_analytical_complete_formula(row: int) -> str:
    return f'=IF(A{row}="","",IF(COUNT(D{row}:Z{row})=23,TRUE,FALSE))'


def publish_source_complete_formula(row: int) -> str:
    return (
        f'=IF(A{row}="","",IF(AND(AH{row}<>"",AI{row}<>"",AJ{row}<>"",AK{row}<>"",'
        f'AL{row}<>"",AM{row}<>"",AN{row}<>"",AO{row}<>"",AP{row}<>"",AQ{row}<>"",'
        f'AR{row}<>"",AS{row}<>"",AT{row}<>"",ISNUMBER(AU{row}),AV{row}="TRUE",'
        f'AW{row}="Reviewed",AX{row}="Valid"),TRUE,FALSE))'
    )


def publish_prereq_formula(row: int) -> str:
    return (
        f'=IF(A{row}="","",IF(AND(COUNTIF($A$2:$A$87,A{row})=1,AZ{row}=TRUE,'
        f'ISNUMBER(AA{row}),AA{row}>0,ISNUMBER(AB{row}),AB{row}>0,'
        f'OR(AD{row}="already_applied_by_labsolutions",AND(AD{row}="apply_in_qbench",ISNUMBER(AC{row}),AC{row}>0)),'
        f'AE{row}="ug/mL",AF{row}="TRUE",AG{row}="TRUE",BA{row}=TRUE,AY{row}="Accepted"),TRUE,FALSE))'
    )


def publish_ready_formula(row: int) -> str:
    return (
        f'=IF(A{row}="","",IF(AND(BB{row}=TRUE,\'QC Review\'!$B$15=TRUE),"TRUE","FALSE"))'
    )


def publish_message_formula(row: int) -> str:
    return (
        f'=IF(A{row}="","",IF(COUNTIF($A$2:$A$87,A{row})>1,"Duplicate Test ID",'
        f'IF(AZ{row}<>TRUE,"Analytical values incomplete",'
        f'IF(OR(ISNUMBER(AA{row})<>TRUE,AA{row}<=0),"Sample mass required",'
        f'IF(OR(ISNUMBER(AB{row})<>TRUE,AB{row}<=0),"Final volume required",'
        f'IF(AND(AD{row}<>"already_applied_by_labsolutions",AD{row}<>"apply_in_qbench"),"Dilution mode required",'
        f'IF(AND(AD{row}="apply_in_qbench",OR(ISNUMBER(AC{row})<>TRUE,AC{row}<=0)),"Dilution factor required",'
        f'IF(OR(AE{row}<>"ug/mL",AF{row}<>"TRUE"),"Unit confirmation required",'
        f'IF(AG{row}<>"TRUE","Preparation confirmation required",'
        f'IF(BA{row}<>TRUE,"Source traceability incomplete",'
        f'IF(ISNUMBER(AU{row})<>TRUE,"Dimethylacetamide audit value required",'
        f'IF(AV{row}<>"TRUE","Compound Results validation required",'
        f'IF(AW{row}<>"Reviewed","Integration review required",'
        f'IF(AX{row}<>"Valid","Import validation required",'
        f'IF(AY{row}<>"Accepted","Batch QC on hold",'
        f'IF(\'QC Review\'!$B$15<>TRUE,"Batch release review required","Ready for transfer"))))))))))))))))'
    )


def build_publish_tab(
    source: dict[str, Any],
    analytes: list[dict[str, Any]],
) -> tuple[list[list[Any]], list[int], dict[str, int], dict[str, dict[str, Any]]]:
    placeholders = source_publish_placeholders(source)
    capacity = len(placeholders)
    headers = PUBLISH_PREFIX_HEADERS + [row["worksheet_label"] for row in analytes] + PUBLISH_SUFFIX_HEADERS
    rows = PUBLISH_HEADER_ROW_COUNT + capacity
    cols = len(headers)
    widths = [145, 145, 155] + [120] * 23 + [
        115,
        120,
        85,
        195,
        145,
        125,
        170,
        145,
        180,
        180,
        180,
        180,
        190,
        125,
        145,
        155,
        120,
        155,
        145,
        180,
        170,
        175,
        175,
        165,
        160,
        185,
        175,
        185,
        120,
        220,
    ]
    data = blank_grid(rows, cols)
    data[0] = headers
    for offset, placeholder in enumerate(placeholders, start=2):
        data[offset - 1][0] = placeholder["test_id"]
        data[offset - 1][1] = f"${{tests[{offset - 2}].sample.get_display_id()}}"
        data[offset - 1][2] = placeholder["product_matrix"]
        data[offset - 1][50] = '=\'QC Review\'!$B$12'
        data[offset - 1][51] = publish_analytical_complete_formula(offset)
        data[offset - 1][52] = publish_source_complete_formula(offset)
        data[offset - 1][53] = publish_prereq_formula(offset)
        data[offset - 1][54] = publish_ready_formula(offset)
        data[offset - 1][55] = publish_message_formula(offset)

    style: dict[str, int] = {}
    style_range(style, 1, 1, cols, 2)
    for row in range(2, rows + 1):
        for col in range(51, 57):
            style[cell_ref(row, col)] = 1

    cells: dict[str, dict[str, Any]] = {}
    formula_cols = {51, 52, 53, 54, 55, 56}
    readonly_cols = {1, 2, 3} | formula_cols
    for row in range(1, rows + 1):
        for col in range(1, cols + 1):
            readonly = row == 1 or col in readonly_cols
            set_cell_metadata(cells, row, col, readonly=readonly, widths=widths)
    return data, widths, style, cells


def worksheet_from_template(template: dict[str, Any], name: str, worksheet_id: str) -> dict[str, Any]:
    worksheet = copy.deepcopy(template)
    worksheet["worksheetName"] = name
    worksheet["worksheetId"] = worksheet_id
    worksheet["cache"] = {}
    worksheet["comments"] = {}
    worksheet["mergeCells"] = {}
    worksheet["meta"] = {}
    worksheet["filters"] = False
    worksheet["freezeColumns"] = []
    worksheet["freezeRows"] = []
    worksheet["csvFileName"] = ""
    return worksheet


def update_worksheet(
    worksheet: dict[str, Any],
    data: list[list[Any]],
    widths: list[int],
    style: dict[str, int],
    cells: dict[str, dict[str, Any]],
    *,
    table_width: int,
    table_height: int,
) -> None:
    rows = len(data)
    cols = max(len(row) for row in data)
    worksheet["data"] = data
    worksheet["columns"] = column_meta(widths)
    worksheet["rows"] = row_meta(rows)
    worksheet["minDimensions"] = [cols, rows]
    worksheet["style"] = style
    worksheet["cells"] = cells
    worksheet["mergeCells"] = {}
    worksheet["comments"] = {}
    worksheet["meta"] = {}
    worksheet["cache"] = {}
    worksheet["tableWidth"] = table_width
    worksheet["tableHeight"] = table_height


def build_named_cells(publish_capacity: int) -> dict[str, Any]:
    named_cells: dict[str, Any] = {}
    for offset, (field, _value, _note) in enumerate(RUN_SETUP_FIELDS, start=2):
        add_named_cell(named_cells, field, f"Run Setup!B{offset}", field.replace("_", " ").title())

    add_named_cell(named_cells, "terpenes_batch_import_table", "Instrument Import!A1:BE201", "Terpenes Batch Import Table")
    add_named_cell(named_cells, "terpenes_batch_import_test_ids", "Instrument Import!E2:E201", "Terpenes Batch Import Test IDs")
    add_named_cell(named_cells, "terpenes_batch_import_analytes", "Instrument Import!AH2:BD201", "Terpenes Batch Import Analytes")
    add_named_cell(named_cells, "terpenes_batch_import_dimethylacetamide", "Instrument Import!AA2:AA201", "Terpenes Batch Import Dimethylacetamide")
    add_named_cell(named_cells, "terpenes_batch_import_validation_status", "Instrument Import!AF2:AF201", "Terpenes Batch Import Validation Status")
    add_named_cell(named_cells, "terpenes_batch_integration_review_status", "Instrument Import!AE2:AE201", "Terpenes Batch Integration Review Status")

    for offset, (field, _value, _note) in enumerate(QC_CONTROL_ROWS, start=2):
        add_named_cell(named_cells, field, f"QC Review!B{offset}", field.replace("_", " ").title())
    add_named_cell(named_cells, "terpenes_batch_qc_table", "QC Review!A19:X42", "Terpenes Batch QC Table")

    end_row = 1 + publish_capacity
    add_named_cell(named_cells, "terpenes_batch_publish_table", f"Publish!A1:BD{end_row}", "Terpenes Batch Publish Table")
    add_named_cell(named_cells, "terpenes_batch_publish_sample_ids", f"Publish!B2:B{end_row}", "Terpenes Batch Publish Sample IDs")
    add_named_cell(named_cells, "terpenes_batch_publish_test_ids", f"Publish!A2:A{end_row}", "Terpenes Batch Publish Test IDs")
    add_named_cell(named_cells, "terpenes_batch_publish_product_matrices", f"Publish!C2:C{end_row}", "Terpenes Batch Publish Product Matrices")
    add_named_cell(named_cells, "terpenes_batch_publish_instrument_conc", f"Publish!D2:Z{end_row}", "Terpenes Batch Publish Instrument Conc.")
    add_named_cell(named_cells, "terpenes_batch_publish_sample_mass_g", f"Publish!AA2:AA{end_row}", "Terpenes Batch Publish Sample Mass G")
    add_named_cell(named_cells, "terpenes_batch_publish_final_volume_ml", f"Publish!AB2:AB{end_row}", "Terpenes Batch Publish Final Volume ML")
    add_named_cell(named_cells, "terpenes_batch_publish_df", f"Publish!AC2:AC{end_row}", "Terpenes Batch Publish DF")
    add_named_cell(named_cells, "terpenes_batch_publish_df_application_mode", f"Publish!AD2:AD{end_row}", "Terpenes Batch Publish DF Application Mode")
    add_named_cell(named_cells, "terpenes_batch_publish_conc_unit", f"Publish!AE2:AE{end_row}", "Terpenes Batch Publish Conc Unit")
    add_named_cell(named_cells, "terpenes_batch_publish_unit_confirmed", f"Publish!AF2:AF{end_row}", "Terpenes Batch Publish Unit Confirmed")
    add_named_cell(named_cells, "terpenes_batch_publish_preparation_confirmed", f"Publish!AG2:AG{end_row}", "Terpenes Batch Publish Preparation Confirmed")
    add_named_cell(named_cells, "terpenes_batch_publish_source_batch_ids", f"Publish!AH2:AH{end_row}", "Terpenes Batch Publish Source Batch IDs")
    add_named_cell(named_cells, "terpenes_batch_publish_source_files", f"Publish!AI2:AI{end_row}", "Terpenes Batch Publish Source Files")
    add_named_cell(named_cells, "terpenes_batch_publish_source_hashes", f"Publish!AJ2:AJ{end_row}", "Terpenes Batch Publish Source Hashes")
    add_named_cell(named_cells, "terpenes_batch_publish_batch_disposition", f"Publish!AY2:AY{end_row}", "Terpenes Batch Publish Batch Disposition")
    add_named_cell(named_cells, "terpenes_batch_publish_ready", f"Publish!BC2:BC{end_row}", "Terpenes Batch Publish Ready")
    add_named_cell(named_cells, "terpenes_batch_publish_messages", f"Publish!BD2:BD{end_row}", "Terpenes Batch Publish Messages")
    return named_cells


def build_candidate() -> dict[str, Any]:
    source = read_json(SOURCE_ACTIVE_EXPORT)
    analytes = channels()
    publish_capacity = source_publish_capacity(source)
    source_worksheet = source["config"]["worksheets"][0]

    candidate = copy.deepcopy(source)
    candidate["qb_config"]["kvstore_config"] = {}
    candidate["qb_config"]["named_cells"] = build_named_cells(publish_capacity)
    candidate["qb_config"]["portal_export_range"] = ""
    candidate["qb_config"]["report_export_range"] = ""
    candidate["config"]["plugins"]["conditionalFormatting"]["rules"] = []

    run_ws = worksheet_from_template(source_worksheet, "Run Setup", RUN_SETUP_WORKSHEET_ID)
    import_ws = worksheet_from_template(source_worksheet, "Instrument Import", INSTRUMENT_IMPORT_WORKSHEET_ID)
    qc_ws = worksheet_from_template(source_worksheet, "QC Review", QC_REVIEW_WORKSHEET_ID)
    publish_ws = worksheet_from_template(source_worksheet, PUBLISH_TAB_NAME, source_worksheet["worksheetId"])

    run_data, run_widths, run_style, run_cells = build_run_setup_tab()
    import_data, import_widths, import_style, import_cells = build_import_tab(analytes)
    qc_data, qc_widths, qc_style, qc_cells = build_qc_review_tab(analytes)
    publish_data, publish_widths, publish_style, publish_cells = build_publish_tab(source, analytes)

    update_worksheet(run_ws, run_data, run_widths, run_style, run_cells, table_width=920, table_height=720)
    update_worksheet(import_ws, import_data, import_widths, import_style, import_cells, table_width=2200, table_height=850)
    update_worksheet(qc_ws, qc_data, qc_widths, qc_style, qc_cells, table_width=2200, table_height=900)
    update_worksheet(publish_ws, publish_data, publish_widths, publish_style, publish_cells, table_width=2200, table_height=850)

    candidate["config"]["worksheets"] = [run_ws, import_ws, qc_ws, publish_ws]
    candidate["data"] = {ws["worksheetName"]: ws["data"] for ws in candidate["config"]["worksheets"]}
    return candidate


def dependency_hashes(paths: list[Path]) -> list[dict[str, str]]:
    return [{"path": repo_relative(path), "sha256": sha256_file(path)} for path in paths]


def build_manifest(candidate: dict[str, Any], candidate_text: str) -> dict[str, Any]:
    source = read_json(SOURCE_ACTIVE_EXPORT)
    publish_capacity = source_publish_capacity(source)
    named_cells = candidate["qb_config"]["named_cells"]
    worksheets = candidate["config"]["worksheets"]
    worksheet_ids = {worksheet["worksheetName"]: worksheet["worksheetId"] for worksheet in worksheets}
    return {
        "schema_version": 1,
        "package": PACKAGE_NAME,
        "prompt": "Prompt 4",
        "nonproduction_candidate": True,
        "stable_generation_date": PROMPT_DATE,
        "source_active_export": {
            "path": repo_relative(SOURCE_ACTIVE_EXPORT),
            "sha256": sha256_file(SOURCE_ACTIVE_EXPORT),
            "worksheet_id_43_sheet1_id": source["config"]["worksheets"][0]["worksheetId"],
            "publish_row_capacity": publish_capacity,
            "unchanged_source_required": True,
        },
        "prompt2_config_files": dependency_hashes(PROMPT2_CONFIG_FILES),
        "prompt3_dependency_files": dependency_hashes(PROMPT3_DEPENDENCY_FILES),
        "local_config_files": dependency_hashes([LAYOUT_CONFIG, IMPORT_CONTRACT_CONFIG])
        if LAYOUT_CONFIG.exists() and IMPORT_CONTRACT_CONFIG.exists()
        else [],
        "generated_candidate": {
            "path": repo_relative(CANDIDATE_PATH),
            "sha256": sha256_bytes(candidate_text.encode("utf-8")),
            "tabs": [worksheet["worksheetName"] for worksheet in worksheets],
            "worksheet_ids": worksheet_ids,
            "new_tab_ids": {
                "Run Setup": RUN_SETUP_WORKSHEET_ID,
                "Instrument Import": INSTRUMENT_IMPORT_WORKSHEET_ID,
                "QC Review": QC_REVIEW_WORKSHEET_ID,
            },
            "publish_tab_preserves_source_sheet1_id": worksheet_ids["Publish"]
            == source["config"]["worksheets"][0]["worksheetId"],
            "formula_count": formula_count(candidate),
            "named_cell_count": len(named_cells),
            "instrument_import_row_capacity": IMPORT_CAPACITY,
            "publish_row_capacity": publish_capacity,
            "publish_table_range": named_cells["terpenes_batch_publish_table"]["cell"],
            "publish_analyte_range": named_cells["terpenes_batch_publish_instrument_conc"]["cell"],
            "batch_qc_disposition_cell": named_cells["batch_qc_disposition"]["cell"],
            "batch_publish_ready_cell": named_cells["batch_publish_ready"]["cell"],
            "bracketing_ccv_criterion_status_cell": named_cells["bracketing_ccv_criterion_status"]["cell"],
            "kvstore_config_empty": candidate["qb_config"]["kvstore_config"] == {},
            "conditional_formatting_rule_count": len(
                candidate["config"]["plugins"]["conditionalFormatting"]["rules"]
            ),
        },
        "controlled_values": {
            "sample_types": SAMPLE_TYPES,
            "manual_integration": MANUAL_INTEGRATION_VALUES,
            "integration_review_status": INTEGRATION_REVIEW_VALUES,
            "import_validation_status": IMPORT_STATUS_VALUES,
            "df_application_modes": DF_APPLICATION_MODES,
            "batch_qc_dispositions": BATCH_QC_DISPOSITIONS,
            "internal_qc_evaluation_values": INTERNAL_QC_EVALUATION_VALUES,
        },
        "default_release_gates": {
            "bracketing_ccv_criterion_status": "decision_required",
            "qc_configuration_complete": "FALSE by formula/default behavior",
            "batch_qc_disposition": "Hold",
            "batch_publish_ready": "FALSE by formula/default behavior",
            "batch_publication_blocked_by_default": True,
        },
        "unresolved_scientific_qc_decisions": [
            "Bracketing CCV criterion remains decision_required; Prompt 4 does not choose 10 percent or 15 percent.",
            "No separate controlled Terpenes LCS requirement was found in repository source files.",
            "LabSolutions Conc. unit, sample mass/final volume sources, and dilution application remain Sandbox-confirmation items from Prompt 3.",
            "Below-LOQ, MU, final sample calculations, COA, METRC, key/value-store, and automation remain out of Prompt 4 scope.",
        ],
        "scope_controls": {
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
        },
        "deterministic_generation": {
            "uses_stable_constants_only": True,
            "generation_timestamps_omitted": True,
            "random_uuid_values_omitted": True,
            "machine_specific_paths_omitted": True,
        },
    }


def build_outputs() -> tuple[dict[str, Any], dict[str, Any], str, str]:
    candidate = build_candidate()
    candidate_text = dump_json_text(candidate)
    manifest = build_manifest(candidate, candidate_text)
    manifest_text = dump_json_text(manifest)
    return candidate, manifest, candidate_text, manifest_text


def write_outputs(candidate_path: Path = CANDIDATE_PATH, manifest_path: Path = MANIFEST_PATH) -> dict[str, Any]:
    candidate, manifest, candidate_text, manifest_text = build_outputs()
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path.write_text(candidate_text, encoding="utf-8", newline="\n")
    manifest_path.write_text(manifest_text, encoding="utf-8", newline="\n")
    return {
        "status": "ok",
        "candidate_path": repo_relative(candidate_path),
        "manifest_path": repo_relative(manifest_path),
        "source_active_export_hash": manifest["source_active_export"]["sha256"],
        "candidate_hash": manifest["generated_candidate"]["sha256"],
        "formula_count": manifest["generated_candidate"]["formula_count"],
        "named_cell_count": manifest["generated_candidate"]["named_cell_count"],
        "publish_row_capacity": manifest["generated_candidate"]["publish_row_capacity"],
        "instrument_import_row_capacity": manifest["generated_candidate"]["instrument_import_row_capacity"],
        "publish_table_range": manifest["generated_candidate"]["publish_table_range"],
        "publish_analyte_range": manifest["generated_candidate"]["publish_analyte_range"],
        "batch_publish_ready_cell": manifest["generated_candidate"]["batch_publish_ready_cell"],
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-path", type=Path, default=CANDIDATE_PATH)
    parser.add_argument("--manifest-path", type=Path, default=MANIFEST_PATH)
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    summary = write_outputs(args.candidate_path, args.manifest_path)
    print(dump_json_text(summary), end="")


if __name__ == "__main__":
    main()
