#!/usr/bin/env python3
"""Build the nonproduction Terpenes Test Worksheet candidate."""
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
SOURCE_ACTIVE_EXPORT = (
    REPO_ROOT
    / "QBench"
    / "Rescans"
    / "2026-07-04"
    / "Worksheets"
    / "Terpenes"
    / "terpenes__id_42__worksheet_export_spreadsheet__active__2026-07-04.json"
)
PROMPT2_DIR = (
    REPO_ROOT
    / "QBench"
    / "Worksheets"
    / "Terpenes"
    / "development"
    / "2026-07-14_config_parser_foundation"
)
PROMPT2_CONFIG_FILES = [
    PROMPT2_DIR / "config" / "terpenes_analytes.json",
    PROMPT2_DIR / "config" / "terpenes_qc.json",
    PROMPT2_DIR / "config" / "metrc_profiles.json",
]

CANDIDATE_PATH = BASE_DIR / "dist" / "terpenes__test_ws_id_42__candidate_v1__2026-07-14.json"
MANIFEST_PATH = BASE_DIR / "dist" / "candidate_manifest.json"

REPORT_HEADERS = ["Analyte", "Result (%)", "Result (mg/g)", "LOQ (mg/g)", "MU (%)"]

REPORT_ROWS = [
    ("α-Pinene", 5),
    ("Camphene", 6),
    ("β-Myrcene", 7),
    ("β-Pinene", 8),
    ("Delta-3-Carene", 9),
    ("α-Terpinene", 10),
    ("Ocimene", 28),
    ("D-Limonene", 12),
    ("p-Cymene", 13),
    ("Eucalyptol", 15),
    ("γ-Terpinene", 16),
    ("Terpinolene", 17),
    ("Linalool", 18),
    ("Isopulegol", 19),
    ("Geraniol", 20),
    ("β-Caryophyllene", 21),
    ("α-Humulene", 22),
    ("Nerolidol", 29),
    ("Guaiol", 25),
    ("Caryophyllene Oxide", 26),
    ("α-Bisabolol", 27),
    ("Total Terpenes", 30),
]

CONTROLLED_BELOW_LOQ_REPORTING_MODES = [
    "decision_required",
    "display_less_than_loq",
    "display_numeric_result",
]

CONTROL_ROWS = [
    ("qbench_test_id", "=A2", "QBench test display ID placeholder"),
    ("qbench_sample_id", "=B2", "QBench sample display ID placeholder"),
    ("product_matrix", "=C2", "QBench sample product matrix placeholder"),
    ("sample_mass_g", "", "Required before calculation"),
    ("final_volume_ml", "", "Required before calculation"),
    ("df", "", "Used only when df_application_mode is apply_in_qbench"),
    ("df_application_mode", "capture_only_until_method_validated", "Decision gate"),
    ("labsolutions_conc_unit", "ug/mL", "Default assumption requires confirmation"),
    ("labsolutions_conc_unit_confirmed", "FALSE", "Must be TRUE before calculation"),
    ("preparation_values_confirmed", "FALSE", "Must be TRUE before calculation"),
    ("below_loq_reporting_mode", "decision_required", "Blocks report release by default"),
    ("loq_source_status", "decision_required", "Blocks report release by default"),
    ("mu_source_status", "decision_required", "Blocks report release by default"),
    ("batch_qc_disposition", "Hold", "Internal batch QC disposition"),
    ("publish_ready", "FALSE", "Must be TRUE with Accepted batch disposition"),
    (
        "analytical_results_complete",
        "=IF(AND(COUNT($D$2:$Z$2)=23,COUNT($D$4:$Z$4)=23),TRUE,FALSE)",
        "TRUE only when all 23 inputs and all 23 mg/g results are numeric",
    ),
    (
        "calculation_ready",
        '=IF(AND($B$17="TRUE",$B$16="ug/mL",$B$18="TRUE",'
        "AND(ISNUMBER($B$12),$B$12>0),AND(ISNUMBER($B$13),$B$13>0),"
        'OR($B$15="already_applied_by_labsolutions",'
        'AND($B$15="apply_in_qbench",ISNUMBER($B$14),$B$14>0))),TRUE,FALSE)',
        "TRUE only when unit, prep, mass, volume, and dilution prerequisites are met",
    ),
    (
        "reporting_ready",
        '=IF(AND($B$25=TRUE,$B$24=TRUE,$B$22="Accepted",$B$23="TRUE",'
        'OR($B$19="display_less_than_loq",$B$19="display_numeric_result"),'
        '$B$20="confirmed",$B$21="confirmed"),TRUE,FALSE)',
        "TRUE only when calculation and reporting gates are complete",
    ),
    (
        "calculation_message",
        '=IF($B$17<>"TRUE","Unit confirmation required",IF($B$16<>"ug/mL","Unit confirmation required",'
        'IF($B$18<>"TRUE","Preparation values required",IF(ISNUMBER($B$12)<>TRUE,'
        '"Preparation values required",IF($B$12<=0,"Preparation values required",'
        'IF(ISNUMBER($B$13)<>TRUE,"Preparation values required",IF($B$13<=0,'
        '"Preparation values required",IF(AND($B$15<>"already_applied_by_labsolutions",'
        '$B$15<>"apply_in_qbench"),"Dilution mode required",IF(AND($B$15="apply_in_qbench",'
        'ISNUMBER($B$14)<>TRUE),"Dilution mode required",IF(AND($B$15="apply_in_qbench",'
        '$B$14<=0),"Dilution mode required",IF($B$24<>TRUE,"Analytical results incomplete",'
        'IF(AND($B$19<>"display_less_than_loq",$B$19<>"display_numeric_result"),'
        '"Below-LOQ reporting mode required",IF($B$20<>"confirmed","LOQ configuration required",'
        'IF($B$21<>"confirmed","MU configuration required",IF($B$22<>"Accepted","Batch on hold",'
        'IF($B$23<>"TRUE","Review required","Ready"))))))))))))))))',
        "First neutral prerequisite message",
    ),
    ("source_batch_id", "", "Deferred batch-to-test automation field"),
    ("source_instrument_file", "", "LabSolutions source export filename"),
    ("source_file_hash", "", "Source export hash when imported"),
    ("source_data_file", "", "LabSolutions data file"),
    ("source_method_file", "", "LabSolutions method file"),
    ("source_sequence_file", "", "LabSolutions sequence or batch file"),
    ("parser_version", "", "Repository parser/config version used for import"),
    ("imported_at", "", "Import timestamp supplied by future automation"),
    ("instrument_name", "", "LabSolutions instrument name"),
    ("detector_id", "", "LabSolutions detector ID"),
    ("detector_name", "", "LabSolutions detector name"),
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


def style_range(style: dict[str, int], row: int, start_col: int, end_col: int, style_id: int) -> None:
    for col in range(start_col, end_col + 1):
        style[cell_ref(row, col)] = style_id


def set_cell_metadata(
    cells: dict[str, dict[str, Any]],
    row: int,
    col: int,
    *,
    readonly: bool,
    widths: list[int],
) -> None:
    cells[cell_ref(row, col)] = cell_meta(readonly, widths[col - 1], col - 1)


def formula_count(workbook: dict[str, Any]) -> int:
    count = 0
    for worksheet in workbook["config"]["worksheets"]:
        for row in worksheet.get("data", []):
            for value in row:
                if isinstance(value, str) and value.startswith("="):
                    count += 1
    return count


def formulas_in(workbook: dict[str, Any]) -> list[str]:
    formulas: list[str] = []
    for worksheet in workbook["config"]["worksheets"]:
        for row in worksheet.get("data", []):
            for value in row:
                if isinstance(value, str) and value.startswith("="):
                    formulas.append(value)
    return formulas


def update_worksheet(
    workbook: dict[str, Any],
    worksheet_name: str,
    data: list[list[Any]],
    widths: list[int],
    style: dict[str, int],
    cells: dict[str, dict[str, Any]],
    *,
    table_width: int,
    table_height: int,
) -> None:
    worksheet = next(
        item for item in workbook["config"]["worksheets"] if item["worksheetName"] == worksheet_name
    )
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


def build_data_tab(channels: list[dict[str, Any]]) -> tuple[list[list[Any]], list[int], dict[str, int], dict[str, dict[str, Any]]]:
    widths = [150, 150, 170] + [115] * 23
    data = blank_grid(38, 26)

    data[0][0:3] = ["QBench Test ID", "QBench Sample ID", "Product Matrix"]
    for index, channel in enumerate(channels, start=4):
        data[0][index - 1] = channel["worksheet_label"]
    data[1][0:3] = ["${test.get_display_id()}", "${test.sample.get_display_id()}", "${test.sample.product_matrix}"]
    data[2][2] = "Effective concentration (ug/mL)"
    data[3][2] = "Result (mg/g)"
    data[4][2] = "Result (%)"
    data[5][2] = "Qualifier"

    for offset, channel in enumerate(channels):
        col = 4 + offset
        label = col_letter(col)
        spec_row = 5 + offset
        data[2][col - 1] = (
            f'=IF({label}2="","",IF($B$25<>TRUE,"",{label}2*IF($B$15="already_applied_by_labsolutions",'
            f'1,IF($B$15="apply_in_qbench",$B$14,""))))'
        )
        data[3][col - 1] = f'=IF({label}3="","",IF($B$25<>TRUE,"",{label}3*$B$13/$B$12/1000))'
        data[4][col - 1] = f'=IF({label}4="","",{label}4/10)'
        data[5][col - 1] = (
            f'=IF({label}2="","",IF($B$25<>TRUE,"Review Required",IF($B$22<>"Accepted","Hold",'
            f'IF($B$23<>"TRUE","Hold",IF(OR(AND($B$19<>"display_less_than_loq",'
            f'$B$19<>"display_numeric_result"),$B$20<>"confirmed",$B$21<>"confirmed"),'
            f'"Review Required",IF(AND(SPECIFICATIONS!$C${spec_row}<>"",{label}4<SPECIFICATIONS!$C${spec_row}),'
            f'"<LOQ","Reported"))))))'
        )

    data[7][0:3] = ["Control/Audit Field", "Value", "Notes"]
    for row_number, (field, value, note) in enumerate(CONTROL_ROWS, start=9):
        data[row_number - 1][0:3] = [field, value, note]

    style: dict[str, int] = {}
    for row in [1, 8]:
        style_range(style, row, 1, 26 if row == 1 else 3, 7)
    style_range(style, 2, 1, 3, 4)
    style_range(style, 2, 4, 26, 9)
    for row in range(3, 7):
        style_range(style, row, 1, 3, 4)
        style_range(style, row, 4, 26, 1)
    for row in range(9, 39):
        style[cell_ref(row, 1)] = 2
        style[cell_ref(row, 2)] = 9 if row not in {9, 10, 11, 24, 25, 26, 27} else 1
        style[cell_ref(row, 3)] = 1

    cells: dict[str, dict[str, Any]] = {}
    for row in range(1, 39):
        for col in range(1, 27):
            has_value = data[row - 1][col - 1] not in ("", None)
            in_formula_layer = row in {3, 4, 5, 6} and col >= 4
            instrument_input = row == 2 and col >= 4
            control_value = col == 2 and 9 <= row <= 38
            metadata_value = row == 2 and col <= 3
            if not (has_value or in_formula_layer or instrument_input or control_value):
                continue
            readonly = True
            if instrument_input:
                readonly = False
            elif control_value and row not in {9, 10, 11, 24, 25, 26, 27}:
                readonly = False
            elif metadata_value:
                readonly = True
            set_cell_metadata(cells, row, col, readonly=readonly, widths=widths)

    return data, widths, style, cells


def spec_blank_check(col: str) -> str:
    checks = ",".join(f"{col}{row}=\"\"" for row in range(5, 28))
    return f"AND({checks})"


def build_specifications_tab(
    channels: list[dict[str, Any]]
) -> tuple[list[list[Any]], list[int], dict[str, int], dict[str, dict[str, Any]]]:
    widths = [170, 150, 120, 110, 110, 125, 135, 150]
    data = blank_grid(30, 8)
    data[0][0:3] = ["Customer", "Program", "Matrix"]
    data[1][0:3] = [
        "${test.sample.order.customer_account.customer_name}",
        "${test.sample.order.customer_account.customer_program}",
        "${test.sample.product_matrix}",
    ]
    data[3][0:8] = [
        "Analyte",
        "Measurement Uncertainty (%)",
        "LOQ (mg/g)",
        "Result (%)",
        "Result (mg/g)",
        "Qualifier",
        "Internal Key",
        "COA Mapping Key",
    ]

    for offset, channel in enumerate(channels):
        row = 5 + offset
        data[row - 1][0] = channel["worksheet_label"]
        data[row - 1][3] = f"=DATA!{col_letter(4 + offset)}5"
        data[row - 1][4] = f"=DATA!{col_letter(4 + offset)}4"
        data[row - 1][5] = f"=DATA!{col_letter(4 + offset)}6"
        data[row - 1][6] = channel["internal_key"]
        data[row - 1][7] = channel.get("default_coa_rollup", channel["internal_key"])

    data[27][0] = "Total Ocimene"
    data[27][3] = '=IF(COUNT(D11,D14)=2,SUM(D11,D14),"")'
    data[27][4] = '=IF(COUNT(E11,E14)=2,SUM(E11,E14),"")'
    data[27][5] = '=IF(E28="","",IF(DATA!$B$26<>TRUE,"Review Required","Reported"))'
    data[27][6] = "total_ocimene"
    data[27][7] = "total_ocimene"

    data[28][0] = "Total Nerolidol"
    data[28][3] = '=IF(COUNT(D23,D24)=2,SUM(D23,D24),"")'
    data[28][4] = '=IF(COUNT(E23,E24)=2,SUM(E23,E24),"")'
    data[28][5] = '=IF(E29="","",IF(DATA!$B$26<>TRUE,"Review Required","Reported"))'
    data[28][6] = "total_nerolidol"
    data[28][7] = "total_nerolidol"

    data[29][0] = "Total Terpenes"
    data[29][3] = '=IF(COUNT(D5:D27)=23,SUM(D5:D27),"")'
    data[29][4] = '=IF(COUNT(E5:E27)=23,SUM(E5:E27),"")'
    data[29][5] = '=IF(E30="","",IF(DATA!$B$26<>TRUE,"Review Required","Reported"))'
    data[29][6] = "total_terpenes"
    data[29][7] = "total_terpenes"

    style: dict[str, int] = {}
    style_range(style, 1, 1, 3, 7)
    style_range(style, 2, 1, 3, 4)
    style_range(style, 4, 1, 8, 7)
    for row in range(5, 31):
        style[cell_ref(row, 1)] = 2 if row < 28 else 17
        for col in range(2, 9):
            style[cell_ref(row, col)] = 1 if row < 28 else 4

    cells: dict[str, dict[str, Any]] = {}
    for row in range(1, 31):
        for col in range(1, 9):
            has_value = data[row - 1][col - 1] not in ("", None)
            formula_col = col in {4, 5, 6} and row >= 5
            if not (has_value or formula_col):
                continue
            readonly = True
            set_cell_metadata(cells, row, col, readonly=readonly, widths=widths)

    return data, widths, style, cells


def build_report_tab() -> tuple[list[list[Any]], list[int], dict[str, int], dict[str, dict[str, Any]]]:
    widths = [175, 100, 110, 105, 90]
    data = blank_grid(23, 5)
    data[0] = REPORT_HEADERS[:]
    for row_index, (label, spec_row) in enumerate(REPORT_ROWS, start=2):
        data[row_index - 1][0] = label
        data[row_index - 1][1] = (
            f'=IF(DATA!$B$26<>TRUE,"",IF(SPECIFICATIONS!F{spec_row}="<LOQ",'
            f'IF(DATA!$B$19="display_less_than_loq","<LOQ",SPECIFICATIONS!D{spec_row}),'
            f'IF(SPECIFICATIONS!F{spec_row}="Reported",SPECIFICATIONS!D{spec_row},"")))'
        )
        data[row_index - 1][2] = (
            f'=IF(DATA!$B$26<>TRUE,"",IF(SPECIFICATIONS!F{spec_row}="<LOQ",'
            f'IF(DATA!$B$19="display_less_than_loq","<LOQ",SPECIFICATIONS!E{spec_row}),'
            f'IF(SPECIFICATIONS!F{spec_row}="Reported",SPECIFICATIONS!E{spec_row},"")))'
        )
        data[row_index - 1][3] = f'=IF(DATA!$B$26=TRUE,SPECIFICATIONS!C{spec_row},"")'
        data[row_index - 1][4] = f'=IF(DATA!$B$26=TRUE,SPECIFICATIONS!B{spec_row},"")'

    style: dict[str, int] = {}
    style_range(style, 1, 1, 5, 23)
    for row in range(2, 24):
        for col in range(1, 6):
            style[cell_ref(row, col)] = 5

    cells: dict[str, dict[str, Any]] = {}
    for row in range(1, 24):
        for col in range(1, 6):
            set_cell_metadata(cells, row, col, readonly=True, widths=widths)
    return data, widths, style, cells


def add_named_cell(named_cells: dict[str, Any], name: str, cell: str, display_name: str = "") -> None:
    named_cells[name] = {"cell": cell, "display_name": display_name, "export": True}


def build_named_cells(source_named_cells: dict[str, Any]) -> dict[str, Any]:
    named_cells = copy.deepcopy(source_named_cells)

    for name, cell, display in [
        ("total_ocimene_percent", "Specifications!D28", "Total Ocimene Percent"),
        ("total_ocimene_mgg", "Specifications!E28", "Total Ocimene mg/g"),
        ("total_nerolidol_percent", "Specifications!D29", "Total Nerolidol Percent"),
        ("total_nerolidol_mgg", "Specifications!E29", "Total Nerolidol mg/g"),
        ("total_terpenes_percent", "Specifications!D30", "Total Terpenes Percent"),
        ("total_terpenes_mgg", "Specifications!E30", "Total Terpenes mg/g"),
        ("report_header", "Report!A1:E1", ""),
        ("report_content", "Report!A2:E23", ""),
        ("report_results", "Report!A1:E23", ""),
        ("terpenes_instrument_conc", "Data!D2:Z2", "Terpenes Instrument Conc."),
        ("terpenes_effective_conc", "Data!D3:Z3", "Terpenes Effective Conc."),
        ("terpenes_results_mgg", "Data!D4:Z4", "Terpenes Results mg/g"),
        ("terpenes_results_percent", "Data!D5:Z5", "Terpenes Results Percent"),
        ("terpenes_qualifiers", "Data!D6:Z6", "Terpenes Qualifiers"),
    ]:
        add_named_cell(named_cells, name, cell, display)

    control_start_row = 9
    for offset, (field, _value, _note) in enumerate(CONTROL_ROWS):
        add_named_cell(named_cells, field, f"Data!B{control_start_row + offset}", field.replace("_", " ").title())

    return named_cells


def build_candidate() -> dict[str, Any]:
    source = read_json(SOURCE_ACTIVE_EXPORT)
    analyte_config = read_json(PROMPT2_CONFIG_FILES[0])
    channels = list(analyte_config["internal_reportable_channels"])
    channels.sort(key=lambda row: row["order"])

    candidate = copy.deepcopy(source)
    candidate["config"]["plugins"]["conditionalFormatting"]["rules"] = []
    candidate["qb_config"]["kvstore_config"] = {}
    candidate["qb_config"]["portal_export_range"] = ""
    candidate["qb_config"]["report_export_range"] = ""
    candidate["qb_config"]["named_cells"] = build_named_cells(source["qb_config"]["named_cells"])

    report_data, report_widths, report_style, report_cells = build_report_tab()
    data_data, data_widths, data_style, data_cells = build_data_tab(channels)
    spec_data, spec_widths, spec_style, spec_cells = build_specifications_tab(channels)

    update_worksheet(
        candidate,
        "Report",
        report_data,
        report_widths,
        report_style,
        report_cells,
        table_width=640,
        table_height=650,
    )
    update_worksheet(
        candidate,
        "Data",
        data_data,
        data_widths,
        data_style,
        data_cells,
        table_width=996,
        table_height=850,
    )
    update_worksheet(
        candidate,
        "Specifications",
        spec_data,
        spec_widths,
        spec_style,
        spec_cells,
        table_width=1070,
        table_height=760,
    )

    worksheet_data_by_name = {
        worksheet["worksheetName"]: worksheet["data"] for worksheet in candidate["config"]["worksheets"]
    }
    for tab_name in list(candidate["data"].keys()):
        candidate["data"][tab_name] = worksheet_data_by_name[tab_name]

    return candidate


def build_manifest(candidate: dict[str, Any], candidate_text: str) -> dict[str, Any]:
    source_hash = sha256_file(SOURCE_ACTIVE_EXPORT)
    config_hashes = [
        {"path": repo_relative(path), "sha256": sha256_file(path)} for path in PROMPT2_CONFIG_FILES
    ]
    source_named_cells = read_json(SOURCE_ACTIVE_EXPORT)["qb_config"]["named_cells"]
    candidate_named_cells = candidate["qb_config"]["named_cells"]
    worksheets = candidate["config"]["worksheets"]
    return {
        "schema_version": 1,
        "package": "2026-07-14_test_worksheet_candidate",
        "prompt": "Prompt 3",
        "nonproduction_candidate": True,
        "stable_generation_date": PROMPT_DATE,
        "source_active_export": {
            "path": repo_relative(SOURCE_ACTIVE_EXPORT),
            "sha256": source_hash,
            "unchanged_source_required": True,
        },
        "prompt2_config_files": config_hashes,
        "generated_candidate": {
            "path": repo_relative(CANDIDATE_PATH),
            "sha256": sha256_bytes(candidate_text.encode("utf-8")),
            "tabs": [worksheet["worksheetName"] for worksheet in worksheets],
            "worksheet_ids": {
                worksheet["worksheetName"]: worksheet["worksheetId"] for worksheet in worksheets
            },
            "formula_count": formula_count(candidate),
            "named_cell_count": len(candidate_named_cells),
            "preserved_compatibility_named_cell_count": len(source_named_cells),
            "report_results_range": candidate_named_cells["report_results"]["cell"],
            "kvstore_config_empty": candidate["qb_config"]["kvstore_config"] == {},
            "conditional_formatting_rule_count": len(
                candidate["config"]["plugins"]["conditionalFormatting"]["rules"]
            ),
        },
        "deterministic_generation": {
            "uses_stable_constants_only": True,
            "generation_timestamps_omitted": True,
            "random_uuid_values_omitted": True,
        },
        "default_decision_gates": {
            "labsolutions_conc_unit": "ug/mL",
            "labsolutions_conc_unit_confirmed": "FALSE",
            "preparation_values_confirmed": "FALSE",
            "df_application_mode": "capture_only_until_method_validated",
            "below_loq_reporting_mode": "decision_required",
            "controlled_below_loq_reporting_modes": CONTROLLED_BELOW_LOQ_REPORTING_MODES,
            "loq_source_status": "decision_required",
            "mu_source_status": "decision_required",
            "batch_qc_disposition": "Hold",
            "publish_ready": "FALSE",
            "analytical_results_complete": "formula_false_by_default",
            "final_report_release_blocked_by_default": True,
        },
        "unresolved_scientific_reporting_decisions": [
            "Confirm LabSolutions Conc. unit and whether it is extract concentration in ug/mL.",
            "Confirm sample mass and final volume sources.",
            "Confirm dilution factor application mode and avoid double application.",
            "Confirm below-LOQ reporting and METRC handling.",
            "Confirm Measurement Uncertainty and LOQ source.",
            "Confirm active COA source parity before release.",
            "Confirm METRC profile selection and export behavior in Prompt 7.",
        ],
        "scope_controls": {
            "active_or_raw_qbench_export_modified": False,
            "coa_source_modified": False,
            "qbench_automation_modified": False,
            "qbench_parser_configuration_modified": False,
            "protocol_worksheet_modified": False,
            "report_configuration_modified": False,
            "qbench_production_object_modified": False,
            "prompt4_started": False,
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
        "preserved_compatibility_named_cell_count": manifest["generated_candidate"][
            "preserved_compatibility_named_cell_count"
        ],
        "report_results_range": manifest["generated_candidate"]["report_results_range"],
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
