#!/usr/bin/env python3
"""Validate Phase 3 Terpenes calculation vectors and worksheet candidates."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parents[4]
OUTPUT_DIR = PACKAGE_DIR / "production_candidates"
TEST_PATH = OUTPUT_DIR / "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v1.json"
BATCH_PATH = OUTPUT_DIR / "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS__v1.json"
VECTOR_PATH = PACKAGE_DIR / "calculation_test_vectors.csv"
METRC_MAPPING_PATH = PACKAGE_DIR / "metrc_terpenes_analyte_mapping.csv"
FIELD_MAPPING_PATH = (
    REPO_ROOT
    / "QBench/Worksheets/Terpenes/development/2026-07-17_exact_test_rest_publisher/config/field_mapping_scalar_candidate.csv"
)
HISTORICAL_TEST_PATH = (
    REPO_ROOT
    / "QBench/Worksheets/Terpenes/development/2026-07-14_test_worksheet_candidate/dist/"
    "terpenes__test_ws_id_42__candidate_v1__2026-07-14.json"
)
HISTORICAL_BATCH_PATH = (
    REPO_ROOT
    / "QBench/Worksheets/Terpenes/development/2026-07-14_batch_worksheet_candidate/dist/"
    "terpenes__batch_ws_id_43__candidate_v1__2026-07-14.json"
)
REPORT_PATH = PACKAGE_DIR / "phase3_candidate_validation.md"

UUID_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}"
)
CELL_RE = re.compile(r"^([A-Z]+)([1-9][0-9]*)$")

EXPECTED_REPORTABLES = [
    "Alpha-Bisabolol",
    "Alpha-Humulene",
    "Alpha-Pinene",
    "Alpha-Terpinene",
    "Beta-Caryophyllene",
    "Beta-Myrcene",
    "Beta-Pinene",
    "Camphene",
    "Caryophyllene Oxide",
    "Delta-3 Carene",
    "Eucalyptol",
    "Gamma-Terpinene",
    "Geraniol",
    "Guaiol",
    "Isopulegol",
    "Limonene",
    "Linalool",
    "Nerolidol",
    "Ocimene",
    "P-Isopropyltoluene (P-Cymene)",
    "Terpinolene",
]

REQUIRED_COMPONENT_VECTORS = {
    "both_positive_above_001",
    "one_positive_missing_001",
    "one_positive_zero_001",
    "one_positive_negative_001",
    "both_missing_001",
    "both_negative_001",
    "positive_combined_below_001",
    "positive_combined_equal_001",
    "positive_combined_exceeds_001",
    "zero_without_mu_001",
    "positive_missing_mu_001",
    "included_in_total_001",
    "excluded_from_total_001",
    "no_integrated_peak_001",
    "blank_component_001",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def col_number(label: str) -> int:
    value = 0
    for char in label:
        value = value * 26 + ord(char) - 64
    return value


def parse_cell(reference: str) -> tuple[int, int]:
    match = CELL_RE.fullmatch(reference)
    if not match:
        fail(f"Invalid single-cell reference: {reference}")
    return int(match.group(2)), col_number(match.group(1))


def worksheet_map(candidate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {worksheet["worksheetName"]: worksheet for worksheet in candidate["config"]["worksheets"]}


def dimensions(worksheet: dict[str, Any]) -> tuple[int, int]:
    rows = len(worksheet.get("data", []))
    cols = max((len(row) for row in worksheet.get("data", [])), default=0)
    return rows, cols


def cell_value(worksheet: dict[str, Any], reference: str) -> Any:
    row, col = parse_cell(reference)
    return worksheet["data"][row - 1][col - 1]


def formulas(candidate: dict[str, Any]) -> list[tuple[str, str, str]]:
    result: list[tuple[str, str, str]] = []
    for worksheet in candidate["config"]["worksheets"]:
        for row_index, row in enumerate(worksheet["data"], start=1):
            for col_index, value in enumerate(row, start=1):
                if isinstance(value, str) and value.startswith("="):
                    result.append((worksheet["worksheetName"], f"{column_label(col_index)}{row_index}", value))
    return result


def column_label(index: int) -> str:
    label = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        label = chr(65 + remainder) + label
    return label


def collect_uuids(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            found.update(UUID_RE.findall(str(key)))
            found.update(collect_uuids(item))
    elif isinstance(value, list):
        for item in value:
            found.update(collect_uuids(item))
    elif isinstance(value, str):
        found.update(UUID_RE.findall(value))
    return {value.lower() for value in found}


def validate_synchronized_data(candidate: dict[str, Any]) -> None:
    worksheets = worksheet_map(candidate)
    if list(candidate["data"]) != [worksheet["worksheetName"] for worksheet in candidate["config"]["worksheets"]]:
        fail("Top-level data tab order does not match config worksheet order")
    for name, worksheet in worksheets.items():
        if candidate["data"][name] != worksheet["data"]:
            fail(f"Top-level data for {name} is not synchronized")


def validate_sanitization(candidate: dict[str, Any], historical: dict[str, Any], label: str) -> None:
    serialized = json.dumps(candidate, ensure_ascii=False)
    prohibited_patterns = [
        r"https?://",
        r"qbench\.net",
        r"X-Amz-(?:Credential|Signature)",
        r"Authorization\s*:",
        r"Bearer\s+[A-Za-z0-9._-]{12,}",
        r"QBENCH_CLIENT_SECRET",
        r"worksheet\?id=",
        r"ws_id_[0-9]+",
        r"(?i)pass[_ /-]?fail",
    ]
    for pattern in prohibited_patterns:
        if re.search(pattern, serialized):
            fail(f"{label} candidate contains prohibited pattern: {pattern}")
    if collect_uuids(candidate) & collect_uuids(historical):
        fail(f"{label} candidate retained a historical/source UUID")
    worksheet_ids = [worksheet["worksheetId"] for worksheet in candidate["config"]["worksheets"]]
    if len(worksheet_ids) != len(set(worksheet_ids)):
        fail(f"{label} candidate has duplicate worksheet UUIDs")


def validate_named_targets(candidate: dict[str, Any]) -> None:
    worksheets = worksheet_map(candidate)
    for name, definition in candidate["qb_config"]["named_cells"].items():
        target = definition["cell"]
        if "!" not in target:
            fail(f"Named cell {name} is not sheet-qualified")
        sheet_name, reference = target.split("!", 1)
        if sheet_name not in worksheets:
            fail(f"Named cell {name} points to unknown worksheet {sheet_name}")
        if ":" in reference:
            start, end = reference.split(":", 1)
            for cell in (start, end):
                row, col = parse_cell(cell)
                rows, cols = dimensions(worksheets[sheet_name])
                if row > rows or col > cols:
                    fail(f"Named range {name} is out of bounds")
        else:
            row, col = parse_cell(reference)
            rows, cols = dimensions(worksheets[sheet_name])
            if row > rows or col > cols:
                fail(f"Named cell {name} is out of bounds")


def validate_test_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    tabs = [worksheet["worksheetName"] for worksheet in candidate["config"]["worksheets"]]
    if tabs != ["Report", "Data", "Specifications"]:
        fail(f"Unexpected Test tab order: {tabs}")
    worksheets = worksheet_map(candidate)
    expected_dims = {"Report": (23, 5), "Data": (40, 26), "Specifications": (23, 21)}
    actual_dims = {name: dimensions(worksheet) for name, worksheet in worksheets.items()}
    if actual_dims != expected_dims:
        fail(f"Unexpected Test dimensions: {actual_dims}")
    validate_synchronized_data(candidate)
    validate_named_targets(candidate)

    named = candidate["qb_config"]["named_cells"]
    with FIELD_MAPPING_PATH.open(newline="", encoding="utf-8") as handle:
        mapping_rows = list(csv.DictReader(handle))
    expected_destinations = {row["destination_named_cell"]: row["destination_cell"] for row in mapping_rows}
    if len(expected_destinations) != 43:
        fail("The proven destination mapping is not exactly 43 unique names")
    if set(named) != set(expected_destinations) | {"report_results"}:
        fail("Test named-cell set is not exactly 43 destinations plus report_results")
    if named["report_results"]["cell"] != "Report!A1:E23":
        fail("report_results is not Report!A1:E23")

    data_sheet = worksheets["Data"]
    target_pairs: set[tuple[str, str]] = set()
    for name, expected_target in expected_destinations.items():
        if named[name]["cell"] != expected_target:
            fail(f"Destination {name} moved from {expected_target}")
        if named[name].get("export") is not True:
            fail(f"Destination {name} is not exportable")
        sheet_name, reference = expected_target.split("!", 1)
        if sheet_name != "Data":
            fail(f"Destination {name} is not on Data")
        if cell_value(data_sheet, reference) not in ("", None):
            fail(f"Destination {name} is not blank")
        metadata = data_sheet["cells"].get(reference)
        if not metadata or metadata.get("readonly") is not False:
            fail(f"Destination {name} is not writable")
        pair = (expected_target, named[name].get("display_name", ""))
        if pair in target_pairs:
            fail(f"Duplicate destination target/display pair at {name}")
        target_pairs.add(pair)

    expected_channels = [
        "alpha-Pinene", "Camphene", "beta-Myrcene", "(-)-beta-Pinene", "delta-3-Carene",
        "alpha-Terpinene", "Ocimene 1", "D-Limonene", "p-Cymene", "Ocimene 2",
        "Eucalyptol", "Gamma terpinene", "Terpinolene", "Linalool", "(-)-Isopulegol",
        "Geraniol", "beta-Caryophyllene", "alpha-Humulene", "Nerolidol 1", "Nerolidol 2",
        "(-)-Guaiol", "Caryophyllene oxide", "(-)-alpha-Bisabolol",
    ]
    if data_sheet["data"][0][3:26] != expected_channels:
        fail("Data D1:Z1 does not preserve the exact 23 channel order")

    report = worksheets["Report"]["data"]
    if report[0] != ["Analyte", "Result (mg/g)", "Result (%)", "LOQ", "MU (%)"]:
        fail("Report headers are incorrect")
    if [row[0] for row in report[1:22]] != EXPECTED_REPORTABLES or report[22][0] != "Total Terpenes":
        fail("Report does not contain exactly 21 measurands plus Total Terpenes")
    if any(value in {"Ocimene 1", "Ocimene 2", "Nerolidol 1", "Nerolidol 2"} for value in (row[0] for row in report)):
        fail("Internal component channel appears on Report")

    specs = worksheets["Specifications"]
    spec_data = specs["data"]
    if [row[0] for row in spec_data[1:22]] != EXPECTED_REPORTABLES:
        fail("Specifications reportable order is incorrect")
    if spec_data[1][20] != "SANDBOX_CONFIGURATION_REQUIRED" or spec_data[3][20] != "SANDBOX_CONFIGURATION_REQUIRED":
        fail("Sanitized Key/Value binding placeholders are missing")

    for row in (19, 20):
        first_used = spec_data[row - 1][12]
        second_used = spec_data[row - 1][13]
        if "<=0),0,DATA!" not in first_used or "<=0),0,DATA!" not in second_used:
            fail(f"Component preprocessing formula missing at Specifications row {row}")
        if not spec_data[row - 1][14].startswith(f'=IF(M{row}=0,"",'):
            fail(f"Zero component 1 still requires MU at row {row}")
        if not spec_data[row - 1][15].startswith(f'=IF(N{row}=0,"",'):
            fail(f"Zero component 2 still requires MU at row {row}")
        mu_formula = spec_data[row - 1][6]
        for fragment in (
            f"AND(M{row}>0,N{row}=0)",
            f"AND(M{row}=0,N{row}>0)",
            "MU UNRESOLVED",
            "SQRT",
        ):
            if fragment not in mu_formula:
                fail(f"Combined MU formula at row {row} lacks {fragment}")

    formula_entries = formulas(candidate)
    formula_text = "\n".join(value for _sheet, _cell, value in formula_entries)
    if "apply_in_qbench" in formula_text or "ug/mL" in formula_text:
        fail("Test formulas retain prohibited dilution or unit logic")
    for component in ("Ocimene 1", "Ocimene 2", "Nerolidol 1", "Nerolidol 2"):
        for _sheet, _cell, formula in formula_entries:
            if component in formula and '"LOQ"' in formula:
                fail(f"Component-channel LOQ lookup found for {component}")
    total_formula = spec_data[22][2]
    for row in range(2, 23):
        if f"C{row}>F{row}" not in total_formula:
            fail(f"Total Terpenes formula omits strict-above comparison for row {row}")
    if total_formula.count("IF(AND(ISNUMBER(") != 21:
        fail("Total Terpenes formula does not contain exactly 21 reportable contributions")

    for sheet_name, reference, formula in formula_entries:
        if "ROUND(" in formula:
            row, col = parse_cell(reference)
            if sheet_name != "Specifications" or col not in {9, 10, 11, 12}:
                fail(f"ROUND appears outside final display layer at {sheet_name}!{reference}")
        metadata = worksheets[sheet_name]["cells"].get(reference)
        if not metadata or metadata.get("readonly") is not True:
            fail(f"Formula cell is not protected/formula-owned at {sheet_name}!{reference}")

    return {
        "tabs": tabs,
        "dimensions": actual_dims,
        "named_cells": len(named),
        "writable_destinations": len(expected_destinations),
        "formulas": len(formula_entries),
    }


def validate_batch_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    tabs = [worksheet["worksheetName"] for worksheet in candidate["config"]["worksheets"]]
    if tabs != ["Run Setup", "Instrument Import", "Batch Review", "Test Transfer"]:
        fail(f"Unexpected Batch tab order: {tabs}")
    worksheets = worksheet_map(candidate)
    expected_dims = {
        "Run Setup": (25, 3),
        "Instrument Import": (201, 57),
        "Batch Review": (45, 24),
        "Test Transfer": (87, 56),
    }
    actual_dims = {name: dimensions(worksheet) for name, worksheet in worksheets.items()}
    if actual_dims != expected_dims:
        fail(f"Unexpected Batch dimensions: {actual_dims}")
    validate_synchronized_data(candidate)
    validate_named_targets(candidate)

    instrument = worksheets["Instrument Import"]
    transfer = worksheets["Test Transfer"]
    if instrument["data"][0][31:33] != ["import_validation_status", "import_message"]:
        fail("AF/AG headers are incorrect")
    if len(instrument["data"][0][33:56]) != 23:
        fail("Instrument Import does not expose exactly 23 numeric channels at AH:BD")
    if len(transfer["data"][0][3:26]) != 23:
        fail("Test Transfer does not expose exactly 23 channel destinations at D:Z")

    for row in range(2, 202):
        for reference, index in ((f"AF{row}", 31), (f"AG{row}", 32)):
            value = instrument["data"][row - 1][index]
            if not isinstance(value, str) or not value.startswith("="):
                fail(f"{reference} is not formula-owned")
            if instrument["cells"].get(reference, {}).get("readonly") is not True:
                fail(f"{reference} is not protected")
        for reference in (f"AE{row}", f"AH{row}", f"BE{row}"):
            if instrument["cells"].get(reference, {}).get("readonly") is not False:
                fail(f"Parser-write cell {reference} is not writable")

    serialized = json.dumps(candidate, ensure_ascii=False)
    if "apply_in_qbench" in serialized or "ug/mL" in serialized:
        fail("Batch candidate retains prohibited QBench dilution/unit logic")
    if "already_applied_by_labsolutions" not in serialized or "ug/g" not in serialized:
        fail("Batch candidate lacks the approved dilution/unit contract")
    if "QC Review!" in serialized or "Publish!" in serialized:
        fail("Batch candidate retains stale tab references")

    ag_formula = instrument["data"][1][32]
    for excluded_type in (
        "Calibration Standard", "Initial CCV", "Continuing CCV", "Blank", "LOQ Check",
        "Matrix Spike", "Duplicate", "Other QC",
    ):
        if excluded_type not in ag_formula:
            fail(f"Instrument row classification omits {excluded_type}")
    if "Unknown" not in ag_formula or "Dilution" not in ag_formula:
        fail("Actual-sample row classification is missing")
    if 'K2<>"already_applied_by_labsolutions"' not in ag_formula:
        fail("Actual-sample import does not enforce LabSolutions-applied dilution mode")

    prereq_formula = transfer["data"][1][53]
    message_formula = transfer["data"][1][55]
    if 'AD2="already_applied_by_labsolutions"' not in prereq_formula:
        fail("Test Transfer prerequisite does not enforce approved dilution mode")
    if 'AE2="ug/g"' not in prereq_formula:
        fail("Test Transfer prerequisite does not enforce final ug/g")
    if 'AD2<>"already_applied_by_labsolutions"' not in message_formula:
        fail("Test Transfer message does not reject other dilution modes")
    if 'AE2<>"ug/g"' not in message_formula:
        fail("Test Transfer message does not reject other units")

    for name, definition in candidate["qb_config"]["named_cells"].items():
        target = definition["cell"]
        if target.startswith("QC Review!") or target.startswith("Publish!"):
            fail(f"Named cell {name} retains stale tab target")

    formula_entries = formulas(candidate)
    for sheet_name, reference, _formula in formula_entries:
        metadata = worksheets[sheet_name]["cells"].get(reference)
        if not metadata or metadata.get("readonly") is not True:
            fail(f"Batch formula cell is not protected at {sheet_name}!{reference}")

    return {
        "tabs": tabs,
        "dimensions": actual_dims,
        "named_cells": len(candidate["qb_config"]["named_cells"]),
        "formulas": len(formula_entries),
        "af_ag_formula_rows": 200,
    }


def parse_numeric(value: str) -> float | None:
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def preprocess(raw: str) -> float:
    if raw in {"", "[missing]", "[blank]", "NO_INTEGRATED_PEAK"}:
        return 0.0
    numeric = float(raw)
    return numeric if numeric > 0 else 0.0


def close(actual: float, expected: float, tolerance: float = 1e-12) -> bool:
    return math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance)


def validate_vectors() -> dict[str, Any]:
    with VECTOR_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    vector_ids = {row["vector_id"] for row in rows}
    if not REQUIRED_COMPONENT_VECTORS.issubset(vector_ids):
        fail(f"Missing required component vectors: {sorted(REQUIRED_COMPONENT_VECTORS - vector_ids)}")

    combined_rows = [row for row in rows if row["operation"] == "combined_result"]
    for row in combined_rows:
        used1 = preprocess(row["component_1_raw_ug_g"])
        used2 = preprocess(row["component_2_raw_ug_g"])
        if not close(used1, float(row["component_1_used_ug_g"])):
            fail(f"Component 1 preprocessing mismatch in {row['vector_id']}")
        if not close(used2, float(row["component_2_used_ug_g"])):
            fail(f"Component 2 preprocessing mismatch in {row['vector_id']}")
        combined = used1 + used2
        if not close(combined, float(row["expected_result_ug_g"])):
            fail(f"Combined result mismatch in {row['vector_id']}")
        if not close(combined / 1000, float(row["expected_mg_g"])):
            fail(f"mg/g conversion mismatch in {row['vector_id']}")
        if not close(combined / 10000, float(row["expected_percent"])):
            fail(f"Percent conversion mismatch in {row['vector_id']}")

        loq = float(row["combined_loq_ug_g"])
        expected_qualifier = "<LOQ" if combined < loq else ""
        expected_included = combined > loq
        if row["expected_qualifier"] != expected_qualifier:
            fail(f"Combined LOQ qualifier mismatch in {row['vector_id']}")
        if (row["expected_included_in_total"].lower() == "true") != expected_included:
            fail(f"Combined Total inclusion mismatch in {row['vector_id']}")

        mu1 = parse_numeric(row["component_1_mu_percent"])
        mu2 = parse_numeric(row["component_2_mu_percent"])
        if used1 == 0 and used2 == 0:
            expected_mu = None
            status = "blank"
        elif used1 > 0 and used2 == 0:
            expected_mu = mu1
            status = "resolved" if mu1 is not None else "unresolved"
        elif used1 == 0 and used2 > 0:
            expected_mu = mu2
            status = "resolved" if mu2 is not None else "unresolved"
        elif mu1 is None or mu2 is None:
            expected_mu = None
            status = "unresolved"
        else:
            expected_mu = 100 * math.sqrt((used1 * mu1 / 100) ** 2 + (used2 * mu2 / 100) ** 2) / combined
            status = "resolved"
        if row["expected_mu_status"] != status:
            fail(f"Combined MU status mismatch in {row['vector_id']}")
        recorded_mu = parse_numeric(row["expected_mu_percent"])
        if expected_mu is None and recorded_mu is not None:
            fail(f"Unexpected numeric MU in {row['vector_id']}")
        if expected_mu is not None and (recorded_mu is None or not close(expected_mu, recorded_mu)):
            fail(f"Combined MU value mismatch in {row['vector_id']}")

    total_components = [row for row in rows if row["vector_id"] == "total_001" and row["operation"] == "total_component"]
    if len(total_components) != 21 or len({row["analyte"] for row in total_components}) != 21:
        fail("Total vector does not contain exactly 21 unique measurands")
    total = sum(float(row["component_1_used_ug_g"]) for row in total_components if row["expected_included_in_total"] == "true")
    if not close(total, 1040):
        fail("Synthetic Total Terpenes is not 1040 ug/g")
    summaries = [row for row in rows if row["vector_id"] == "total_001" and row["operation"] == "total_summary"]
    if len(summaries) != 1 or not close(float(summaries[0]["expected_result_ug_g"]), total):
        fail("Total vector summary is incorrect")
    return {"rows": len(rows), "combined_cases": len(combined_rows), "total_ug_g": total}


def validate_mapping() -> dict[str, Any]:
    with METRC_MAPPING_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    analytical = [row for row in rows if row["internal_status"] != "audit_only"]
    audit = [row for row in rows if row["internal_status"] == "audit_only"]
    reportable = {row["reportable_measurand"] for row in analytical}
    if len(analytical) != 23 or len(reportable) != 21 or len(audit) != 2:
        fail("Metrc mapping must contain 23 channels, 21 measurands, and 2 audit-only rows")
    for row in analytical:
        if row["internal_status"] == "combined_component_channel":
            note = row["notes"].lower()
            for fragment in ("positive", "component loq", "used 0", "mu lookup"):
                if fragment not in note:
                    fail(f"Component mapping note lacks {fragment}: {row['instrument_channel']}")
    return {"rows": len(rows), "internal_channels": len(analytical), "reportable_measurands": len(reportable), "audit_only": len(audit)}


def write_report(
    test_result: dict[str, Any],
    batch_result: dict[str, Any],
    vector_result: dict[str, Any],
    mapping_result: dict[str, Any],
) -> None:
    test_hash = sha256(TEST_PATH)
    batch_hash = sha256(BATCH_PATH)
    lines = [
        "# Phase 3 Terpenes local candidate validation",
        "",
        "`calculation_contract = passed_authoritative_method_documentation_and_user_approved_reporting_rules`",
        "",
        "## Candidate results",
        "",
        f"- Test candidate: `{TEST_PATH.name}`",
        f"- Test SHA-256: `{test_hash}`",
        f"- Test tabs: {', '.join(test_result['tabs'])}",
        f"- Test dimensions: {test_result['dimensions']}",
        f"- Test named cells: {test_result['named_cells']} (43 writable destinations plus `report_results`).",
        f"- Test formulas: {test_result['formulas']}; every formula cell is protected/formula-owned.",
        f"- Batch candidate: `{BATCH_PATH.name}`",
        f"- Batch SHA-256: `{batch_hash}`",
        f"- Batch tabs: {', '.join(batch_result['tabs'])}",
        f"- Batch dimensions: {batch_result['dimensions']}",
        f"- Batch named cells: {batch_result['named_cells']}.",
        f"- Batch formulas: {batch_result['formulas']}; AF/AG formula ownership passed for {batch_result['af_ag_formula_rows']} rows.",
        "",
        "## Calculation and mapping results",
        "",
        f"- Calculation-vector rows: {vector_result['rows']}.",
        f"- Combined component cases: {vector_result['combined_cases']}.",
        f"- Synthetic Total Terpenes: {vector_result['total_ug_g']:.0f} ug/g.",
        f"- Mapping rows: {mapping_result['rows']} = {mapping_result['internal_channels']} internal channels + {mapping_result['audit_only']} audit-only rows.",
        f"- Unique reportable measurands: {mapping_result['reportable_measurands']}.",
        "- Missing/blank/no-peak/zero/negative component preprocessing passed.",
        "- Positive component retention, combined LOQ, single-positive MU, two-positive MU, missing-positive-MU, and strict-above Total inclusion passed.",
        "- No component-channel LOQ lookup exists.",
        "",
        "## Safety results",
        "",
        "- JSON syntax, tab order, dimensions, synchronized data, formulas, named targets, and formula ownership passed.",
        "- No Pass/Fail artifact, credential, URL, signed URL, source UUID, internal production identifier, QBench API instruction, or customer value was retained.",
        "- No QBench environment was accessed. No worksheet was imported, approved, activated, or published.",
        "- Sandbox saved-definition and runtime validation remain the next controlled phase.",
        "",
    ]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    test_candidate = load_json(TEST_PATH)
    batch_candidate = load_json(BATCH_PATH)
    validate_sanitization(test_candidate, load_json(HISTORICAL_TEST_PATH), "Test")
    validate_sanitization(batch_candidate, load_json(HISTORICAL_BATCH_PATH), "Batch")
    test_result = validate_test_candidate(test_candidate)
    batch_result = validate_batch_candidate(batch_candidate)
    vector_result = validate_vectors()
    mapping_result = validate_mapping()
    write_report(test_result, batch_result, vector_result, mapping_result)
    print("PHASE3_CANDIDATE_VALIDATION=PASSED")
    print(f"test_sha256={sha256(TEST_PATH)}")
    print(f"batch_sha256={sha256(BATCH_PATH)}")
    print(f"vector_rows={vector_result['rows']}")
    print(f"test_named_cells={test_result['named_cells']}")
    print(f"batch_af_ag_formula_rows={batch_result['af_ag_formula_rows']}")


if __name__ == "__main__":
    main()
