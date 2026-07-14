#!/usr/bin/env python3
"""Parse Shimadzu LabSolutions ASCII exports for the Terpenes foundation.

This parser is repository-only support code. It reads the controlled
Terpenes analyte configuration, parses the sanitized LabSolutions ASCII
fixture format, retains audit-only compounds, and emits reportable terpene
rows using Compound Results(Ch1) > Conc. as the only potency source.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any


SECTION_RE = re.compile(r"^\[(.+)]\s*$")
BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = BASE_DIR / "config" / "terpenes_analytes.json"
DEFAULT_INPUT_PATH = BASE_DIR / "fixtures" / "labsolutions_ascii" / "Output_redacted_fixture.txt"
DEFAULT_OUTPUT_DIR = BASE_DIR / "generated"

NUMERIC_KEYS = {
    "R.Time",
    "I.Time",
    "F.Time",
    "Area",
    "Height",
    "A/H",
    "Conc.",
    "k'",
    "Plate #",
    "Plate Ht.",
    "Tailing",
    "Resolution",
    "Sep.Factor",
    "Area Ratio",
    "Height Ratio",
    "Conc. %",
    "Norm Conc.",
    "3rd",
    "2nd",
    "1st",
    "Constant",
    "ID#",
    "Peak#",
}

COMPOUND_RESULTS_UNKNOWN_NAME_BEHAVIOR = "capture_for_strict_validation"
PEAK_TABLE_UNKNOWN_NAME_BEHAVIOR = "audit_non_reportable"
UNKNOWN_NAME_BEHAVIORS = {
    COMPOUND_RESULTS_UNKNOWN_NAME_BEHAVIOR,
    PEAK_TABLE_UNKNOWN_NAME_BEHAVIOR,
}

GREEK_TO_WORD = {
    "\u03b1": "alpha",
    "\u0391": "alpha",
    "\u03b2": "beta",
    "\u0392": "beta",
    "\u03b3": "gamma",
    "\u0393": "gamma",
    "\u03b4": "delta",
    "\u0394": "delta",
}


class LabSolutionsParseError(ValueError):
    """Raised when a LabSolutions export does not match the controlled config."""


class TerpenesConfigError(ValueError):
    """Raised when the controlled Terpenes config is internally inconsistent."""


def parse_scalar(value: str) -> Any:
    text = value.strip()
    if text == "":
        return ""
    try:
        if re.fullmatch(r"[-+]?\d+", text):
            return int(text)
        return float(text)
    except ValueError:
        return text


def normalize_analyte_name(value: str) -> str:
    text = unicodedata.normalize("NFKC", value).casefold()
    for symbol, word in GREEK_TO_WORD.items():
        text = text.replace(symbol.casefold(), word)
    return re.sub(r"[^a-z0-9]+", "", text)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def reportable_channels(config: dict[str, Any]) -> list[dict[str, Any]]:
    return list(config.get("internal_reportable_channels", []))


def audit_channels(config: dict[str, Any]) -> list[dict[str, Any]]:
    return list(config.get("audit_only_channels", []))


def configured_compound_channels(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    channels: dict[str, dict[str, Any]] = {}
    for channel in reportable_channels(config) + audit_channels(config):
        key = str(channel.get("internal_key", ""))
        if key in channels:
            raise TerpenesConfigError(f"Duplicate configured internal key: {key}")
        if key:
            channels[key] = channel
    return channels


def _require_false_controls(config: dict[str, Any]) -> None:
    controls = config.get("result_status_controls", {})
    required = [
        "sample_pass_fail_enabled",
        "analyte_pass_fail_enabled",
        "coa_pass_fail_enabled",
        "metrc_pass_fail_enabled",
        "kvstore_pass_fail_enabled",
        "label_claim_pass_fail_enabled",
    ]
    for key in required:
        if controls.get(key) is not False:
            raise TerpenesConfigError(f"{key} must be false for Terpenes.")


def validate_analyte_config(config: dict[str, Any]) -> None:
    if config.get("reporting_mode") != "quantitative_only":
        raise TerpenesConfigError("reporting_mode must be quantitative_only.")
    _require_false_controls(config)

    quantitation = config.get("quantitation", {})
    source_table = quantitation.get("source_table")
    source_field = quantitation.get("source_field")
    blocked = set(quantitation.get("blocked_potency_fields", []))
    if source_table != "Compound Results(Ch1)":
        raise TerpenesConfigError("Quantitation source table must be Compound Results(Ch1).")
    if source_field != "Conc.":
        raise TerpenesConfigError("Quantitation source field must be Conc.")
    if source_field in blocked:
        raise TerpenesConfigError(f"Blocked potency source selected: {source_field}")

    channels = reportable_channels(config)
    audits = audit_channels(config)
    if len(channels) != 23:
        raise TerpenesConfigError(f"Expected 23 reportable channels, found {len(channels)}.")
    if len(audits) != 1:
        raise TerpenesConfigError(f"Expected exactly one audit-only channel, found {len(audits)}.")

    audit = audits[0]
    if audit.get("internal_key") != "dimethylacetamide":
        raise TerpenesConfigError("The only audit-only channel must be dimethylacetamide.")
    if audit.get("reportable") is not False:
        raise TerpenesConfigError("Dimethylacetamide must have reportable = false.")
    if audit.get("retain_for_audit") is not True:
        raise TerpenesConfigError("Dimethylacetamide must have retain_for_audit = true.")

    configured_channels = channels + audits
    if len(configured_channels) != 24:
        raise TerpenesConfigError(
            f"Expected 24 configured Compound Results channels, found {len(configured_channels)}."
        )

    keys = [row.get("internal_key") for row in configured_channels]
    blank_keys = [index for index, key in enumerate(keys, start=1) if not str(key or "").strip()]
    if blank_keys:
        raise TerpenesConfigError(f"Configured internal keys must be nonblank; blank at row(s): {blank_keys}.")
    if len(keys) != len(set(keys)):
        duplicates = sorted({key for key in keys if keys.count(key) > 1})
        raise TerpenesConfigError(f"Duplicate configured internal keys are not allowed: {duplicates}.")

    compound_ids = [row.get("labsolutions_compound_id") for row in configured_channels]
    blank_ids = [index for index, value in enumerate(compound_ids, start=1) if value in ("", None)]
    if blank_ids:
        raise TerpenesConfigError(f"LabSolutions compound IDs must be nonblank; blank at row(s): {blank_ids}.")
    non_integer_ids = [value for value in compound_ids if not isinstance(value, int)]
    if non_integer_ids:
        raise TerpenesConfigError(f"LabSolutions compound IDs must be integers: {non_integer_ids}.")
    if len(compound_ids) != len(set(compound_ids)):
        duplicates = sorted({value for value in compound_ids if compound_ids.count(value) > 1})
        raise TerpenesConfigError(f"Duplicate LabSolutions compound IDs are not allowed: {duplicates}.")

    controlled_id_set = set(range(1, 25))
    configured_id_set = set(compound_ids)
    if configured_id_set != controlled_id_set and not config.get("future_approved_compound_id_alternative"):
        raise TerpenesConfigError(
            "Configured LabSolutions compound IDs must resolve to the controlled set 1 through 24 "
            "unless future_approved_compound_id_alternative documents an approved alternative."
        )

    build_alias_map(config)

    coa = config.get("default_coa_reporting", {})
    direct = set(coa.get("direct_internal_keys", []))
    rollups = coa.get("rollups", [])
    rollup_components = {key for rollup in rollups for key in rollup.get("components", [])}
    expected_keys = {str(row.get("internal_key", "")) for row in channels}
    accounted_keys = direct | rollup_components
    if accounted_keys != expected_keys:
        missing = sorted(expected_keys - accounted_keys)
        extra = sorted(accounted_keys - expected_keys)
        raise TerpenesConfigError(f"Default COA channel accounting mismatch: missing={missing}, extra={extra}.")
    measurand_count = len(direct) + len(rollups)
    if coa.get("measurand_count") != 21 or measurand_count != 21:
        raise TerpenesConfigError("Default COA reporting must resolve to 21 measurands.")


def build_alias_map(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    alias_map: dict[str, dict[str, Any]] = {}
    for channel in reportable_channels(config) + audit_channels(config):
        aliases = {
            str(channel.get("worksheet_label", "")),
            str(channel.get("labsolutions_compound_name", "")),
            *[str(value) for value in channel.get("aliases", [])],
        }
        for alias in aliases:
            normalized = normalize_analyte_name(alias)
            if not normalized:
                continue
            existing = alias_map.get(normalized)
            if existing and existing.get("internal_key") != channel.get("internal_key"):
                raise TerpenesConfigError(
                    "Conflicting alias mapping for "
                    f"{alias!r}: {existing.get('internal_key')} vs {channel.get('internal_key')}"
                )
            alias_map[normalized] = channel
    return alias_map


def parse_sections(path: Path) -> dict[str, list[str]]:
    if not path.is_file():
        raise FileNotFoundError(f"LabSolutions export not found: {path}")

    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.rstrip("\r\n")
        match = SECTION_RE.match(line)
        if match:
            current = match.group(1)
            sections[current] = []
            continue
        if current is not None:
            sections[current].append(line)
    return sections


def parse_key_value_section(sections: dict[str, list[str]], section_name: str) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for line in sections.get(section_name, []):
        if not line.strip():
            continue
        parts = line.split("\t", 1)
        if len(parts) == 2:
            values[parts[0].strip()] = parse_scalar(parts[1])
    return values


def parse_table(
    sections: dict[str, list[str]],
    section_name: str,
    header_prefix: str,
    alias_map: dict[str, dict[str, Any]],
    *,
    unknown_name_behavior: str,
) -> list[dict[str, Any]]:
    if unknown_name_behavior not in UNKNOWN_NAME_BEHAVIORS:
        raise ValueError(f"Unsupported unknown_name_behavior: {unknown_name_behavior}")

    rows: list[dict[str, Any]] = []
    headers: list[str] | None = None
    for line in sections.get(section_name, []):
        if not line.strip() or line.startswith("# of"):
            continue
        if line.startswith(header_prefix):
            headers = line.split("\t")
            continue
        if headers is None:
            continue
        cells = line.split("\t")
        if len(cells) != len(headers):
            raise LabSolutionsParseError(
                f"{section_name} row has {len(cells)} columns; expected {len(headers)}: {line}"
            )
        row: dict[str, Any] = {}
        for header, cell in zip(headers, cells):
            row[header] = parse_scalar(cell) if header in NUMERIC_KEYS else cell.strip()

        source_name = str(row.get("Name", "")).strip()
        channel = alias_map.get(normalize_analyte_name(source_name))
        if channel is None:
            row["internal_key"] = ""
            row["worksheet_label"] = source_name
            row["reportable"] = False
            row["retain_for_audit"] = True
            row["_unconfigured_analyte"] = True
            row["_unknown_name_behavior"] = unknown_name_behavior
        else:
            row["internal_key"] = channel.get("internal_key", "")
            row["worksheet_label"] = channel.get("worksheet_label", source_name)
            row["reportable"] = bool(channel.get("reportable"))
            row["retain_for_audit"] = bool(channel.get("retain_for_audit")) or not bool(channel.get("reportable"))
            row["configured_labsolutions_compound_id"] = channel.get("labsolutions_compound_id", "")
            row["_unconfigured_analyte"] = False
        rows.append(row)
    return rows


def _display_name(value: Any) -> str:
    text = str(value).strip()
    return text if text else "<blank>"


def validate_compound_results(rows: list[dict[str, Any]], config: dict[str, Any]) -> None:
    """Validate Compound Results against configured Terpenes channels and IDs."""
    reportable_by_key = {row["internal_key"]: row for row in reportable_channels(config)}
    configured_by_key = configured_compound_channels(config)
    expected_keys = set(configured_by_key)
    expected_reportable_keys = set(reportable_by_key)
    expected_total_rows = len(configured_by_key)

    configured_rows = [row for row in rows if row.get("internal_key") in expected_keys]
    reportable_rows = [row for row in configured_rows if row.get("reportable")]
    unexpected_rows = [row for row in rows if row.get("_unconfigured_analyte")]
    key_counts = Counter(str(row.get("internal_key", "")) for row in configured_rows if row.get("internal_key"))

    errors: list[str] = []
    if len(rows) != expected_total_rows:
        errors.append(f"Compound Results row count: expected {expected_total_rows}, found {len(rows)}")
    if len(configured_rows) != expected_total_rows:
        errors.append(
            f"configured Compound Results row count: expected {expected_total_rows}, found {len(configured_rows)}"
        )
    if len(reportable_rows) != len(expected_reportable_keys):
        errors.append(
            f"reportable channel count: expected {len(expected_reportable_keys)}, found {len(reportable_rows)}"
        )

    dimethylacetamide_count = key_counts.get("dimethylacetamide", 0)
    if dimethylacetamide_count != 1:
        errors.append(f"Dimethylacetamide audit-only count: expected 1, found {dimethylacetamide_count}")

    duplicate_keys = sorted(key for key, count in key_counts.items() if count > 1)
    if duplicate_keys:
        details = ", ".join(f"{key} ({key_counts[key]})" for key in duplicate_keys)
        errors.append(f"duplicate keys: {details}")

    missing_keys = sorted(expected_keys - set(key_counts))
    if missing_keys:
        errors.append(f"missing keys: {', '.join(missing_keys)}")

    if unexpected_rows:
        unexpected_names = ", ".join(_display_name(row.get("Name", "")) for row in unexpected_rows)
        errors.append(f"unexpected names: {unexpected_names}")

    id_mismatches: list[str] = []
    for row in configured_rows:
        key = str(row.get("internal_key", ""))
        expected_id = configured_by_key[key].get("labsolutions_compound_id")
        actual_id = row.get("ID#")
        if actual_id != expected_id:
            id_mismatches.append(
                f"{_display_name(row.get('Name', ''))} -> {key} ID# {actual_id!r} expected {expected_id!r}"
            )
    if id_mismatches:
        errors.append(f"ID/name mismatches: {'; '.join(id_mismatches)}")

    if errors:
        raise LabSolutionsParseError("Invalid Compound Results(Ch1): " + " | ".join(errors))


def parse_file(
    path: Path,
    config: dict[str, Any],
    *,
    compound_results_unknown_name_behavior: str = COMPOUND_RESULTS_UNKNOWN_NAME_BEHAVIOR,
    peak_table_unknown_name_behavior: str = PEAK_TABLE_UNKNOWN_NAME_BEHAVIOR,
) -> dict[str, Any]:
    validate_analyte_config(config)
    alias_map = build_alias_map(config)
    sections = parse_sections(path)
    required_sections = [
        "Header",
        "Sample Information",
        "Original Files",
        "Configuration",
        "Peak Table(Ch1)",
        "Compound Results(Ch1)",
    ]
    missing = [section for section in required_sections if section not in sections]
    if missing:
        raise LabSolutionsParseError(f"Missing required section(s): {', '.join(missing)}")

    parsed: dict[str, Any] = {
        "source_file": str(path),
        "sections_present": list(sections),
        "quantitation_source_table": config["quantitation"]["source_table"],
        "quantitation_source_field": config["quantitation"]["source_field"],
        "blocked_potency_fields": config["quantitation"]["blocked_potency_fields"],
    }

    for section in ["Header", "File Information", "Sample Information", "Original Files", "Configuration"]:
        parsed[section] = parse_key_value_section(sections, section)

    parsed["Peak Table(Ch1)"] = parse_table(
        sections,
        "Peak Table(Ch1)",
        "Peak#",
        alias_map,
        unknown_name_behavior=peak_table_unknown_name_behavior,
    )
    parsed["Compound Results(Ch1)"] = parse_table(
        sections,
        "Compound Results(Ch1)",
        "ID#",
        alias_map,
        unknown_name_behavior=compound_results_unknown_name_behavior,
    )
    validate_compound_results(parsed["Compound Results(Ch1)"], config)

    sample_info = parsed.get("Sample Information", {})
    original_files = parsed.get("Original Files", {})
    configuration = parsed.get("Configuration", {})
    source_field = config["quantitation"]["source_field"]

    normalized_results: list[dict[str, Any]] = []
    audit_compounds: list[dict[str, Any]] = []
    for row in parsed["Compound Results(Ch1)"]:
        audit_row = {
            "source_id": row.get("ID#", ""),
            "source_name": row.get("Name", ""),
            "internal_key": row.get("internal_key", ""),
            "worksheet_label": row.get("worksheet_label", ""),
            "reportable": row.get("reportable", False),
            "labsolutions_conc": row.get("Conc.", ""),
            "normalized_conc_percent_not_potency": row.get("Conc. %", ""),
            "norm_conc_not_potency": row.get("Norm Conc.", ""),
        }
        audit_compounds.append(audit_row)
        if not row.get("reportable"):
            continue
        normalized_results.append(
            {
                "sample_name": sample_info.get("Sample Name", ""),
                "sample_id": sample_info.get("Sample ID", ""),
                "acquired_at": sample_info.get("Acquired", ""),
                "vial_number": sample_info.get("Vial#", ""),
                "injection_volume_uL": sample_info.get("Injection Volume", ""),
                "source_id": row.get("ID#", ""),
                "source_name": row.get("Name", ""),
                "internal_key": row.get("internal_key", ""),
                "worksheet_label": row.get("worksheet_label", ""),
                "r_time_min": row.get("R.Time", ""),
                "area": row.get("Area", ""),
                "height": row.get("Height", ""),
                "potency_source_field": source_field,
                "labsolutions_conc": row.get(source_field, ""),
                "result_mg_g": None,
                "result_percent": None,
                "result_calculation_status": "requires_confirmed_sample_mass_final_volume_and_unit",
                "curve": row.get("Curve", ""),
                "area_ratio": row.get("Area Ratio", ""),
                "height_ratio": row.get("Height Ratio", ""),
                "normalized_conc_percent_not_potency": row.get("Conc. %", ""),
                "norm_conc_not_potency": row.get("Norm Conc.", ""),
                "sample_amount_export": sample_info.get("Sample Amount", ""),
                "dilution_factor_export": sample_info.get("Dilution Factor", ""),
                "data_file": original_files.get("Data File", ""),
                "method_file": original_files.get("Method File", ""),
                "batch_file": original_files.get("Batch File", ""),
                "instrument_name": configuration.get("Instrument Name", ""),
                "detector_id": configuration.get("Detector ID", ""),
                "detector_name": configuration.get("Detector Name", ""),
            }
        )

    parsed["audit_compound_results"] = audit_compounds
    parsed["audit_non_reportable_compounds"] = [
        row for row in audit_compounds if not row.get("reportable")
    ]
    parsed["normalized_reportable_compound_results"] = normalized_results
    return parsed


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    config = load_json(args.config)
    parsed = parse_file(args.input, config)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    out_json = args.output_dir / "labsolutions_ascii_parsed_output.json"
    out_compound_csv = args.output_dir / "labsolutions_compound_results_fixture.csv"
    out_peak_csv = args.output_dir / "labsolutions_peak_table_fixture.csv"
    out_norm_csv = args.output_dir / "labsolutions_normalized_reportable_results_fixture.csv"
    out_audit_csv = args.output_dir / "labsolutions_audit_compound_results_fixture.csv"

    out_json.write_text(json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(out_compound_csv, parsed["Compound Results(Ch1)"])
    write_csv(out_peak_csv, parsed["Peak Table(Ch1)"])
    write_csv(out_norm_csv, parsed["normalized_reportable_compound_results"])
    write_csv(out_audit_csv, parsed["audit_compound_results"])

    summary = {
        "sections_present": parsed["sections_present"],
        "compound_rows": len(parsed["Compound Results(Ch1)"]),
        "peak_rows": len(parsed["Peak Table(Ch1)"]),
        "reportable_compound_rows": len(parsed["normalized_reportable_compound_results"]),
        "non_reportable_compounds": [
            row.get("source_name", "") for row in parsed["audit_non_reportable_compounds"]
        ],
        "outputs": [
            str(out_json),
            str(out_compound_csv),
            str(out_peak_csv),
            str(out_norm_csv),
            str(out_audit_csv),
        ],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
