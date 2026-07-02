#!/usr/bin/env python3
"""Validate the Phase 1 Homogeneity worksheet release candidate.

The script is intentionally read-only. It parses the QBench worksheet JSON,
lists named cells, checks required Homogeneity named cells and validation
fields, reports duplicate named-cell targets, and writes a markdown report.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


REQUIRED_NAMED_CELLS = {
    "pass_fail",
    "report_results",
}

REQUIRED_VALIDATION_NAMED_CELLS = {
    "reviewer_parent_sample_confirmation",
    "parent_sample_match_check",
    "replicate_count",
    "unique_cp_test_id_count",
    "duplicate_cp_test_id_check",
    "extra_pasted_rows_check",
    "required_unit_mass_check",
    "required_target_fields_check",
    "optional_target_2_label_claim_check",
    "validation_status",
}

REQUIRED_LABEL_SOURCE_NAMED_CELLS = {
    "label_cannabinoid_1_source_status",
    "label_cannabinoid_2_source_status",
    "manual_label_cannabinoid_1_mg_container",
    "manual_label_cannabinoid_2_mg_container",
    "qbench_sample_label_amount_lookup",
}

REQUIRED_SAMPLE_LABEL_FIELDS = {
    "${test.sample.product_label_totalthc}",
    "${test.sample.product_label_totalcbd}",
    "${test.sample.product_label_cbd}",
    "${test.sample.product_label_cbda}",
    "${test.sample.product_label_cbn}",
    "${test.sample.product_label_cbg}",
    "${test.sample.product_label_cbga}",
    "${test.sample.product_label_d8thc}",
    "${test.sample.product_label_thc}",
    "${test.sample.product_label_thcv}",
    "${test.sample.product_label_cbc}",
    "${test.sample.product_label_thca}",
}


def col_to_index(col: str) -> int:
    index = 0
    for ch in col.upper():
        if not ("A" <= ch <= "Z"):
            raise ValueError(f"Invalid column letter: {col}")
        index = index * 26 + (ord(ch) - ord("A") + 1)
    return index - 1


def split_cell_ref(ref: str) -> tuple[str, int, int]:
    if "!" not in ref:
        raise ValueError(f"Missing worksheet in cell reference: {ref}")
    sheet, cell = ref.split("!", 1)
    if ":" in cell:
        cell = cell.split(":", 1)[0]
    letters = "".join(ch for ch in cell if ch.isalpha())
    digits = "".join(ch for ch in cell if ch.isdigit())
    if not letters or not digits:
        raise ValueError(f"Invalid cell reference: {ref}")
    return sheet, int(digits) - 1, col_to_index(letters)


def get_cell_value(data: dict[str, Any], ref: str) -> Any:
    sheet, row_idx, col_idx = split_cell_ref(ref)
    rows = data.get("data", {}).get(sheet)
    if not isinstance(rows, list):
        return None
    if row_idx < 0 or row_idx >= len(rows):
        return None
    row = rows[row_idx]
    if not isinstance(row, list) or col_idx < 0 or col_idx >= len(row):
        return None
    return row[col_idx]


def cell_ref_exists(data: dict[str, Any], ref: str) -> bool:
    try:
        value = get_cell_value(data, ref)
    except ValueError:
        return False
    return value is not None


def range_has_content(data: dict[str, Any], ref: str) -> bool:
    if ":" not in ref:
        value = get_cell_value(data, ref)
        return value not in (None, "")
    sheet, range_part = ref.split("!", 1)
    start, end = range_part.split(":", 1)
    start_sheet, start_row, start_col = split_cell_ref(f"{sheet}!{start}")
    end_sheet, end_row, end_col = split_cell_ref(f"{sheet}!{end}")
    if start_sheet != end_sheet:
        return False
    rows = data.get("data", {}).get(sheet)
    if not isinstance(rows, list):
        return False
    for row_idx in range(start_row, end_row + 1):
        if row_idx < 0 or row_idx >= len(rows):
            continue
        row = rows[row_idx]
        if not isinstance(row, list):
            continue
        for col_idx in range(start_col, end_col + 1):
            if 0 <= col_idx < len(row) and row[col_idx] not in ("", None):
                return True
    return False


def get_worksheet_config(data: dict[str, Any], worksheet_name: str) -> dict[str, Any] | None:
    for worksheet in (data.get("config") or {}).get("worksheets", []):
        if isinstance(worksheet, dict) and worksheet.get("worksheetName") == worksheet_name:
            return worksheet
    return None


def get_cell_style_text(data: dict[str, Any], worksheet_name: str, cell_ref: str) -> str:
    worksheet = get_worksheet_config(data, worksheet_name)
    if not worksheet:
        return ""
    cell_meta = (worksheet.get("cells") or {}).get(cell_ref)
    if not isinstance(cell_meta, dict):
        return ""
    style_id = cell_meta.get("style")
    styles = ((data.get("config") or {}).get("style") or [])
    if not isinstance(style_id, int) or style_id < 0 or style_id >= len(styles):
        return ""
    style_text = styles[style_id]
    return style_text if isinstance(style_text, str) else ""


def display_percent(value: float) -> str:
    return f"{value:.1%}"


def flatten_values(obj: Any) -> list[str]:
    values: list[str] = []
    if isinstance(obj, str):
        values.append(obj)
    elif isinstance(obj, list):
        for item in obj:
            values.extend(flatten_values(item))
    elif isinstance(obj, dict):
        for item in obj.values():
            values.extend(flatten_values(item))
    return values


def validate(json_path: Path, report_path: Path) -> int:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as exc:
        report_path.write_text(f"# Phase 1 Homogeneity Validation Report\n\nERROR: invalid JSON: {exc}\n", encoding="utf-8")
        return 1

    named = ((data.get("qb_config") or {}).get("named_cells") or {})
    if not isinstance(named, dict):
        errors.append("qb_config.named_cells is missing or is not an object.")
        named = {}

    worksheet_names = []
    for ws in (data.get("config") or {}).get("worksheets", []):
        if isinstance(ws, dict):
            worksheet_names.append(ws.get("worksheetName"))
    duplicate_worksheets = sorted(name for name, count in Counter(worksheet_names).items() if name and count > 1)
    if duplicate_worksheets:
        errors.append(f"Duplicate worksheet names: {', '.join(duplicate_worksheets)}")

    missing_required = sorted(REQUIRED_NAMED_CELLS - set(named))
    if missing_required:
        errors.append(f"Missing required named cells: {', '.join(missing_required)}")

    missing_validation = sorted(REQUIRED_VALIDATION_NAMED_CELLS - set(named))
    if missing_validation:
        errors.append(f"Missing required validation named cells: {', '.join(missing_validation)}")

    missing_label_source = sorted(REQUIRED_LABEL_SOURCE_NAMED_CELLS - set(named))
    if missing_label_source:
        errors.append(f"Missing required label-source named cells: {', '.join(missing_label_source)}")

    bad_refs: list[str] = []
    for system_name, info in sorted(named.items()):
        cell = info.get("cell") if isinstance(info, dict) else None
        if not cell or not cell_ref_exists(data, cell):
            bad_refs.append(system_name)
    if bad_refs:
        errors.append(f"Named cells with missing/invalid targets: {', '.join(bad_refs)}")

    target_to_names: dict[str, list[str]] = {}
    for system_name, info in sorted(named.items()):
        cell = info.get("cell") if isinstance(info, dict) else None
        if cell:
            target_to_names.setdefault(cell, []).append(system_name)
    duplicate_targets = {cell: names for cell, names in target_to_names.items() if len(names) > 1}
    if duplicate_targets:
        warnings.append("Duplicate named-cell targets exist and must be documented before import.")

    pass_fail_ref = named.get("pass_fail", {}).get("cell") if isinstance(named.get("pass_fail"), dict) else None
    pass_fail_formula = get_cell_value(data, pass_fail_ref) if pass_fail_ref else None
    if not isinstance(pass_fail_formula, str) or "B42" not in pass_fail_formula or "INCOMPLETE" not in pass_fail_formula:
        errors.append("pass_fail does not appear to be gated by the Phase 1 validation status.")

    report_ref = named.get("report_results", {}).get("cell") if isinstance(named.get("report_results"), dict) else None
    if not report_ref or not range_has_content(data, report_ref):
        errors.append("report_results target is missing or empty.")

    validation_status = get_cell_value(data, named.get("validation_status", {}).get("cell", "Data!B42"))
    if not isinstance(validation_status, str) or "B34=10" not in validation_status or "REVIEWER_CONFIRMED" not in validation_status:
        errors.append("validation_status does not enforce the expected Phase 1 validation gates.")

    parent_check = get_cell_value(data, named.get("parent_sample_match_check", {}).get("cell", "Data!B38"))
    if not isinstance(parent_check, str) or "Paste!D6" not in parent_check:
        errors.append("parent_sample_match_check does not reference the reviewer confirmation fallback.")

    paste_ai10 = get_cell_value(data, "Paste!AI10")
    paste_aj10 = get_cell_value(data, "Paste!AJ10")
    data_e12 = get_cell_value(data, "Data!E12")
    data_g12 = get_cell_value(data, "Data!G12")
    data_m12 = get_cell_value(data, "Data!M12")
    data_p12 = get_cell_value(data, "Data!P12")
    data_b9 = get_cell_value(data, "Data!B9")
    data_r12 = get_cell_value(data, "Data!R12")
    data_s12 = get_cell_value(data, "Data!S12")
    data_t12 = get_cell_value(data, "Data!T12")
    paste_d4 = get_cell_value(data, "Paste!D4")
    paste_h4 = get_cell_value(data, "Paste!H4")
    paste_q4 = get_cell_value(data, "Paste!Q4")
    paste_u4 = get_cell_value(data, "Paste!U4")
    default_target_1 = get_cell_value(data, "Paste!B4")
    p25_p36 = [get_cell_value(data, f"Paste!P{row}") for row in range(25, 37)]

    if default_target_1 != "Total THC":
        errors.append("Paste!B4 default Target Cannabinoid 1 is not Total THC.")

    if not isinstance(paste_ai10, str) or "/1000" not in paste_ai10 or "M10" not in paste_ai10 or "Q10" not in paste_ai10:
        errors.append("Paste!AI10 does not convert Total THC from pasted ug/g values to mg/g.")

    if not isinstance(paste_aj10, str) or "/1000" not in paste_aj10 or "I10" not in paste_aj10 or "F10" not in paste_aj10:
        errors.append("Paste!AJ10 does not convert Total CBD from pasted ug/g values to mg/g.")

    if not isinstance(data_e12, str) or "Paste!AI10" not in data_e12 or "Paste!AJ10" not in data_e12 or "/1000" not in data_e12:
        errors.append("Data!E12 does not return Target 1 result in mg/g for both total and individual cannabinoids.")

    if not isinstance(data_g12, str) or "Paste!AI10" not in data_g12 or "Paste!AJ10" not in data_g12 or "/1000" not in data_g12:
        errors.append("Data!G12 does not return Target 2 result in mg/g for both total and individual cannabinoids.")

    if not isinstance(data_m12, str) or "E12*H12" not in data_m12:
        errors.append("Data!M12 does not calculate Target 1 mg/container from converted mg/g times unit mass.")

    if not isinstance(data_p12, str) or "G12*H12" not in data_p12:
        errors.append("Data!P12 does not calculate Target 2 mg/container from converted mg/g times unit mass.")

    required_percent_cells = ["B9", "B26", "B28", "B30"]
    for col in ("K", "N", "Q"):
        required_percent_cells.extend(f"{col}{row}" for row in range(12, 22))
    missing_percent_styles = [
        f"Data!{cell}"
        for cell in required_percent_cells
        if "0.0%" not in get_cell_style_text(data, "Data", cell)
    ]
    if missing_percent_styles:
        errors.append(f"Data tab variance cells missing 0.0% percent display style: {', '.join(missing_percent_styles)}")

    if data_b9 != "=Paste!L4":
        errors.append("Data!B9 allowed variance must remain linked to Paste!L4.")

    for ref, formula in (("Data!R12", data_r12), ("Data!S12", data_s12), ("Data!T12", data_t12)):
        if not isinstance(formula, str) or "<=$B$9" not in formula or "*100" in formula:
            errors.append(f"{ref} pass/fail logic must compare decimal variance values against Data!B9 without multiplying by 100.")

    if not isinstance(paste_d4, str) or paste_d4.startswith("=P25IF") or "P25IF" in paste_d4:
        errors.append("Paste!D4 contains the invalid P25IF formula corruption.")

    if not isinstance(paste_d4, str) or not paste_d4.startswith('=IF(O4<>"",O4,IF(B4=""'):
        errors.append("Paste!D4 does not start with the expected manual-override label lookup structure.")

    if not isinstance(paste_h4, str) or not paste_h4.startswith('=IF(S4<>"",S4,IF(F4=""'):
        errors.append("Paste!H4 does not start with the expected manual-override label lookup structure.")

    for ref, formula in (("Paste!D4", paste_d4), ("Paste!H4", paste_h4)):
        if not isinstance(formula, str) or "INDEX($P$25:$P$36" not in formula:
            errors.append(f"{ref} does not auto-pull from the visible QBench sample label source table.")
        if not isinstance(formula, str) or 'LOWER(' not in formula or '="none"' not in formula or 'LEFT(' not in formula or '="${"' not in formula:
            errors.append(f"{ref} does not treat blank, None, and unresolved ${{...}} source values as blank.")

    formula_source_cells = [f"Paste!P{idx + 25}" for idx, value in enumerate(p25_p36) if isinstance(value, str) and value.startswith("=")]
    if formula_source_cells:
        errors.append(f"P25:P36 must remain raw QBench sample label source values, but formulas were found in: {', '.join(formula_source_cells)}")

    if not isinstance(paste_q4, str) or "Pulled from" not in paste_q4:
        errors.append("Paste!Q4 does not expose Label Claim 1 source/status.")

    if not isinstance(paste_u4, str) or "Pulled from" not in paste_u4:
        errors.append("Paste!U4 does not expose Label Claim 2 source/status.")

    all_strings = flatten_values(data.get("data", {}))
    if any("Worst" in value or "worst" in value for value in all_strings):
        errors.append('Worksheet output contains "Worst"; Phase 1 requires "Highest".')

    if any("P25IF" in value for value in all_strings):
        errors.append("Worksheet contains invalid P25IF formula corruption.")

    missing_sample_label_fields = sorted(REQUIRED_SAMPLE_LABEL_FIELDS - set(all_strings))
    if missing_sample_label_fields:
        errors.append(f"Missing QBench sample label field placeholders: {', '.join(missing_sample_label_fields)}")

    example_d9_ug_g = 4058.954
    example_thca_ug_g = 0.0
    example_mass_g = 5.0
    example_total_thc_mg_g = (example_d9_ug_g + example_thca_ug_g * 0.877) / 1000
    example_total_thc_mg_container = example_total_thc_mg_g * example_mass_g
    example_cbg_ug_g = 4105.178
    example_cbg_mg_g = example_cbg_ug_g / 1000
    example_cbg_mg_container = example_cbg_mg_g * example_mass_g
    example_positive_variance_display = display_percent(0.0147385)
    example_negative_variance_display = display_percent(-0.0108085)
    example_allowed_variance_display = display_percent(0.15)

    lines: list[str] = []
    lines.append("# Phase 1 Homogeneity Validation Report")
    lines.append("")
    lines.append(f"Worksheet JSON: `{json_path.name}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- JSON parsed: yes")
    lines.append(f"- Worksheet names checked: {len(worksheet_names)}")
    lines.append(f"- Named cells found: {len(named)}")
    lines.append(f"- Errors: {len(errors)}")
    lines.append(f"- Warnings: {len(warnings)}")
    lines.append("")
    lines.append("## Required Checks")
    lines.append("")
    required_rows = [
        ("pass_fail exists", "pass_fail" in named),
        ("report_results exists", "report_results" in named),
        ("required validation named cells exist", not missing_validation),
        ("label source named cells exist", not missing_label_source),
        ("pass_fail gated by validation_status", not any("pass_fail does not" in error for error in errors)),
        ("parent sample fallback references Paste!D6", not any("parent_sample_match_check" in error for error in errors)),
        ("Total THC helper converts ug/g to mg/g", not any("Paste!AI10" in error for error in errors)),
        ("Total CBD helper converts ug/g to mg/g", not any("Paste!AJ10" in error for error in errors)),
        ("individual cannabinoid targets convert ug/g to mg/g", not any("Data!E12" in error or "Data!G12" in error for error in errors)),
        ("mg/container uses converted mg/g times unit mass", not any("Data!M12" in error or "Data!P12" in error for error in errors)),
        ("Data tab variance cells use 0.0% display format", not missing_percent_styles),
        ("allowed variance remains decimal threshold from Paste!L4", data_b9 == "=Paste!L4"),
        ("pass/fail logic compares decimal variances against 0.15 threshold", not any("pass/fail logic" in error for error in errors)),
        ("Paste!D4 has no P25IF corruption", not any("Paste!D4 contains" in error or "P25IF" in error for error in errors)),
        ("Paste!D4/Paste!H4 blank None and unresolved placeholders", not any("source values as blank" in error for error in errors)),
        ("P25:P36 remains raw QBench source table", not formula_source_cells),
        ("Actual unit mass validation requires all 10 AH values", not any("Required Unit Mass" in error for error in errors) and isinstance(get_cell_value(data, "Data!B39"), str) and "COUNT(H12:H21)=10" in get_cell_value(data, "Data!B39")),
        ("QBench sample label fields are documented/pulled", not missing_sample_label_fields and not any("label claim" in error.lower() for error in errors)),
        ('worksheet uses "Highest" terminology only', not any("Worst" in error for error in errors)),
        ("report_results range has content", not any("report_results target" in error for error in errors)),
    ]
    lines.append("| Check | Result |")
    lines.append("|---|---|")
    for label, ok in required_rows:
        lines.append(f"| {label} | {'PASS' if ok else 'FAIL'} |")
    lines.append("")
    lines.append("## Named Cells")
    lines.append("")
    lines.append("| System Name | Cell/Range | Display Name |")
    lines.append("|---|---|---|")
    for system_name, info in sorted(named.items()):
        cell = info.get("cell", "") if isinstance(info, dict) else ""
        display = info.get("display_name", "") if isinstance(info, dict) else ""
        lines.append(f"| `{system_name}` | `{cell}` | {display} |")
    lines.append("")
    lines.append("## Duplicate Named-Cell Targets")
    lines.append("")
    if duplicate_targets:
        lines.append("| Cell/Range | Named Cells |")
        lines.append("|---|---|")
        for cell, names in sorted(duplicate_targets.items()):
            lines.append(f"| `{cell}` | {', '.join(f'`{name}`' for name in names)} |")
    else:
        lines.append("No duplicate named-cell targets found.")
    lines.append("")
    lines.append("## Formula Checks")
    lines.append("")
    lines.append(f"- pass_fail `{pass_fail_ref}`: `{pass_fail_formula}`")
    lines.append(f"- validation_status `Data!B42`: `{validation_status}`")
    lines.append(f"- parent_sample_match_check `Data!B38`: `{parent_check}`")
    lines.append(f"- Total THC helper `Paste!AI10`: `{paste_ai10}`")
    lines.append(f"- Total CBD helper `Paste!AJ10`: `{paste_aj10}`")
    lines.append(f"- Target 1 result `Data!E12`: `{data_e12}`")
    lines.append(f"- Target 2 result `Data!G12`: `{data_g12}`")
    lines.append(f"- Target 1 mg/container `Data!M12`: `{data_m12}`")
    lines.append(f"- Target 2 mg/container `Data!P12`: `{data_p12}`")
    lines.append(f"- Allowed variance `Data!B9`: `{data_b9}`")
    lines.append(f"- Mass pass/fail sample `Data!R12`: `{data_r12}`")
    lines.append(f"- Cannabinoid 1 pass/fail sample `Data!S12`: `{data_s12}`")
    lines.append(f"- Cannabinoid 2 pass/fail sample `Data!T12`: `{data_t12}`")
    lines.append(f"- Target 1 label lookup `Paste!D4`: `{paste_d4}`")
    lines.append(f"- Target 2 label lookup `Paste!H4`: `{paste_h4}`")
    lines.append(f"- Required unit mass check `Data!B39`: `{get_cell_value(data, 'Data!B39')}`")
    lines.append("")
    lines.append("## Numeric Example Checks")
    lines.append("")
    lines.append(f"- D9-THC `{example_d9_ug_g}` ug/g with THCa `{example_thca_ug_g}` ug/g -> Total THC `{example_total_thc_mg_g:.6f}` mg/g.")
    lines.append(f"- Total THC `{example_total_thc_mg_g:.6f}` mg/g with `{example_mass_g:g}` g unit mass -> `{example_total_thc_mg_container:.5f}` mg/container.")
    lines.append(f"- CBG `{example_cbg_ug_g}` ug/g -> `{example_cbg_mg_g:.6f}` mg/g.")
    lines.append(f"- CBG `{example_cbg_mg_g:.6f}` mg/g with `{example_mass_g:g}` g unit mass -> `{example_cbg_mg_container:.5f}` mg/container.")
    lines.append(f"- Data variance display `0.0147385` -> `{example_positive_variance_display}` with 0.0% formatting.")
    lines.append(f"- Data variance display `-0.0108085` -> `{example_negative_variance_display}` with 0.0% formatting.")
    lines.append(f"- Allowed variance display `0.15` -> `{example_allowed_variance_display}` with 0.0% formatting.")
    lines.append("")
    lines.append("## Data Tab Percent Display Formatting")
    lines.append("")
    lines.append("| Cell/Range | Purpose | Style Contains 0.0% |")
    lines.append("|---|---|---|")
    percent_rows = [
        ("Data!B9", "Allowed Variance"),
        ("Data!K12:K21", "Mass % Variance"),
        ("Data!N12:N21", "Cannabinoid 1 % Variance"),
        ("Data!Q12:Q21", "Cannabinoid 2 % Variance"),
        ("Data!B26", "Highest Mass Label Variance"),
        ("Data!B28", "Highest Cannabinoid 1 Label Variance"),
        ("Data!B30", "Highest Cannabinoid 2 Label Variance"),
    ]
    for cell_range, purpose in percent_rows:
        if ":" in cell_range:
            sheet, range_part = cell_range.split("!", 1)
            start, end = range_part.split(":", 1)
            start_col = "".join(ch for ch in start if ch.isalpha())
            start_row = int("".join(ch for ch in start if ch.isdigit()))
            end_row = int("".join(ch for ch in end if ch.isdigit()))
            cells = [f"{start_col}{row}" for row in range(start_row, end_row + 1)]
            ok = all("0.0%" in get_cell_style_text(data, sheet, cell) for cell in cells)
        else:
            sheet, cell = cell_range.split("!", 1)
            ok = "0.0%" in get_cell_style_text(data, sheet, cell)
        lines.append(f"| `{cell_range}` | {purpose} | {'yes' if ok else 'no'} |")
    lines.append("")
    lines.append("## Label Claim Source Logic")
    lines.append("")
    lines.append("- Direct QBench sample label placeholders were found in exported worksheet templates and are used in this release.")
    lines.append("- Target 1 label claim `Paste!D4` pulls from `Paste!N25:P36` unless manual override `Paste!O4` is populated.")
    lines.append("- Target 2 label claim `Paste!H4` pulls from `Paste!N25:P36` unless manual override `Paste!S4` is populated.")
    lines.append(f"- Label Claim 1 source/status `Paste!Q4`: `{paste_q4}`")
    lines.append(f"- Label Claim 2 source/status `Paste!U4`: `{paste_u4}`")
    lines.append("")
    lines.append("## Errors")
    lines.append("")
    if errors:
        for error in errors:
            lines.append(f"- {error}")
    else:
        lines.append("None.")
    lines.append("")
    lines.append("## Warnings")
    lines.append("")
    if warnings:
        for warning in warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("None.")
    lines.append("")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(report_path)
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Phase 1 Homogeneity QBench worksheet JSON.")
    parser.add_argument("json_path", type=Path)
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()
    report_path = args.report or args.json_path.with_name("phase1_validation_report.md")
    return validate(args.json_path, report_path)


if __name__ == "__main__":
    raise SystemExit(main())
