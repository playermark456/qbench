#!/usr/bin/env python3
"""Parse Shimadzu LabSolutions ASCII report exports for Terpenes workups.

The parser reads bracketed sections, key/value metadata, and tab-delimited
Peak Table / Compound Results sections. It intentionally does not assume a
concentration unit; unit conversion belongs to the controlled worksheet config.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

SECTION_RE = re.compile(r"^\[(.+)]\s*$")

ALIASES = {
    "alpha-pinene": "α-Pinene",
    "camphene": "Camphene",
    "beta-myrcene": "β-Myrcene",
    "(-)-beta-pinene": "(-)-β-pinene",
    "delta-3-carene": "Delta-3-carene",
    "alpha-terpinene": "α-Terpinene",
    "ocimene 1": "cis-Ocimene",
    "d-limonene": "d-Limonene",
    "p-cymene": "p-Cymene",
    "ocimene 2": "trans-Ocimene",
    "eucalyptol": "Eucalyptol",
    "gamma terpinene": "γ-Terpinene",
    "terpinolene": "Terpinolene",
    "linalool": "Linalool",
    "(-)-isopulegol": "(-)-Isopulegol",
    "geraniol": "Geraniol",
    "beta-caryophyllene": "β-Caryophyllene",
    "alpha-humulene": "α-Humulene",
    "nerolidol 1": "cis-Nerolidol",
    "nerolidol 2": "trans-Nerolidol",
    "(-)-guaiol": "(-)-Guaiol",
    "caryophyllene oxide": "Caryophyllene Oxide",
    "(-)-alpha-bisabolol": "(-)-α-Bisabolol",
    "dimethylacetamide": "Dimethylacetamide",
}

REPORTABLE = {value for value in ALIASES.values() if value != "Dimethylacetamide"}

NUMERIC_KEYS = {
    "R.Time", "I.Time", "F.Time", "Area", "Height", "A/H", "Conc.", "k'", "Plate #", "Plate Ht.",
    "Tailing", "Resolution", "Sep.Factor", "Area Ratio", "Height Ratio", "Conc. %", "Norm Conc.",
    "3rd", "2nd", "1st", "Constant", "ID#", "Peak#",
}


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


def parse_file(path: Path) -> dict[str, Any]:
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

    parsed: dict[str, Any] = {"source_file": str(path), "sections_present": list(sections)}

    for section in ["Header", "File Information", "Sample Information", "Original Files", "Configuration"]:
        values: dict[str, Any] = {}
        for line in sections.get(section, []):
            if not line.strip():
                continue
            parts = line.split("\t", 1)
            if len(parts) == 2:
                values[parts[0].strip()] = parse_scalar(parts[1])
        parsed[section] = values

    def parse_table(section_name: str, header_prefix: str) -> list[dict[str, Any]]:
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
                rows.append({
                    "_parse_warning": "wrong_column_count",
                    "_raw_line": line,
                    "_expected_columns": len(headers),
                    "_actual_columns": len(cells),
                })
                continue
            row: dict[str, Any] = {}
            for header, cell in zip(headers, cells):
                row[header] = parse_scalar(cell) if header in NUMERIC_KEYS else cell.strip()
            source_name = str(row.get("Name", "")).strip()
            mapped = ALIASES.get(source_name.lower(), source_name)
            row["worksheet_label"] = mapped
            row["reportable"] = mapped in REPORTABLE
            rows.append(row)
        return rows

    parsed["Peak Table(Ch1)"] = parse_table("Peak Table(Ch1)", "Peak#")
    parsed["Compound Results(Ch1)"] = parse_table("Compound Results(Ch1)", "ID#")

    sample_info = parsed.get("Sample Information", {})
    sample_amount = sample_info.get("Sample Amount", "")
    dilution_factor = sample_info.get("Dilution Factor", "")

    normalized_results: list[dict[str, Any]] = []
    for row in parsed["Compound Results(Ch1)"]:
        if not row.get("reportable"):
            continue
        normalized_results.append({
            "sample_name": sample_info.get("Sample Name", ""),
            "sample_id": sample_info.get("Sample ID", ""),
            "source_id": row.get("ID#", ""),
            "source_name": row.get("Name", ""),
            "worksheet_label": row.get("worksheet_label", ""),
            "r_time_min": row.get("R.Time", ""),
            "area": row.get("Area", ""),
            "height": row.get("Height", ""),
            "labsolutions_conc": row.get("Conc.", ""),
            "curve": row.get("Curve", ""),
            "area_ratio": row.get("Area Ratio", ""),
            "height_ratio": row.get("Height Ratio", ""),
            "normalized_conc_percent_not_potency": row.get("Conc. %", ""),
            "sample_amount_export": sample_amount,
            "dilution_factor_export": dilution_factor,
        })
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
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=script_dir / "Output_redacted_fixture.txt",
        help="LabSolutions ASCII export path (default: bundled redacted fixture)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=script_dir / "generated",
        help="Directory for parsed JSON and CSV outputs",
    )
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    parsed = parse_file(args.input)
    out_json = args.output_dir / "labsolutions_ascii_parsed_output.json"
    out_compound_csv = args.output_dir / "labsolutions_compound_results_fixture.csv"
    out_peak_csv = args.output_dir / "labsolutions_peak_table_fixture.csv"
    out_norm_csv = args.output_dir / "labsolutions_normalized_reportable_results_fixture.csv"

    out_json.write_text(json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(out_compound_csv, parsed["Compound Results(Ch1)"])
    write_csv(out_peak_csv, parsed["Peak Table(Ch1)"])
    write_csv(out_norm_csv, parsed["normalized_reportable_compound_results"])

    summary = {
        "sections_present": parsed["sections_present"],
        "compound_rows": len(parsed["Compound Results(Ch1)"]),
        "peak_rows": len(parsed["Peak Table(Ch1)"]),
        "reportable_compound_rows": len(parsed["normalized_reportable_compound_results"]),
        "non_reportable_compounds": [
            row.get("Name", "")
            for row in parsed["Compound Results(Ch1)"]
            if not row.get("reportable")
        ],
        "outputs": [str(out_json), str(out_compound_csv), str(out_peak_csv), str(out_norm_csv)],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
