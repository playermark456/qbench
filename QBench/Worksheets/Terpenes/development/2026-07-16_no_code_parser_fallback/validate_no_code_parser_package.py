#!/usr/bin/env python3
"""Validate the deterministic Prompt 4.6C repository package."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FIXTURE_NAME = "SBX_ONLY_TERPENES_WIDE_IMPORT_01.txt"
FIXTURE = ROOT / FIXTURE_NAME
MANIFEST = ROOT / "no_code_parser_manifest.json"
CONFIG = ROOT / "sanitized_no_code_parser_configuration.json"
MAPPING = ROOT / "no_code_parser_mapping.csv"
SANITIZED_EXPORT = (
    ROOT
    / "SBX_ONLY_TERPENES_2026_07_16_No_Code_Batch_Import__sanitized_export_spreadsheet.json"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def letters(start: str, end: str) -> list[str]:
    def number(value: str) -> int:
        result = 0
        for character in value:
            result = result * 26 + ord(character) - 64
        return result

    def label(value: int) -> str:
        result = ""
        while value:
            value, remainder = divmod(value - 1, 26)
            result = chr(65 + remainder) + result
        return result

    return [label(value) for value in range(number(start), number(end) + 1)]


def load_tsv(path: Path) -> tuple[list[str], list[str]]:
    rows = list(csv.reader(path.read_text(encoding="utf-8").splitlines(), delimiter="\t"))
    assert len(rows) == 2, f"{path}: expected exactly two rows"
    assert len(rows[0]) == len(rows[1]), f"{path}: uneven rows"
    return rows[0], rows[1]


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "sandbox_validation_complete"
    assert manifest["sandbox_validation"]["canonical_parser_job"] == "SUCCESS"
    assert manifest["sandbox_validation"]["duplicate_parser_job"] == "SUCCESS"
    assert manifest["sandbox_validation"]["non_numeric_parser_job"] == "SUCCESS"
    assert manifest["sandbox_validation"]["missing_peak_count_parser_job"] == "SUCCESS"
    assert manifest["sandbox_validation"]["publish_writes"] == 0
    assert manifest["sandbox_validation"]["test_worksheet_writes"] == 0
    assert manifest["sandbox_validation"]["pass_fail_artifact_created"] is False
    assert manifest["sandbox_validation"]["navigate_away_reload_verified"] is True
    headers, values = load_tsv(FIXTURE)
    columns = letters("A", "BE")
    by_column = dict(zip(columns, values, strict=True))

    assert len(headers) == len(values) == len(columns) == 57
    assert by_column["AF"] == by_column["AG"] == ""
    assert by_column["BE"] == manifest["typed_row"]["source_row_hash"]
    assert sha256(FIXTURE) == manifest["fixtures"][FIXTURE_NAME]["sha256"]
    assert not any("pass" in header.lower() or "fail" in header.lower() for header in headers)

    numeric_columns = ["X", "Y", "Z", "AA"] + letters("AH", "BD")
    for column in numeric_columns:
        float(by_column[column])
    assert int(float(by_column["X"])) == 24
    assert int(float(by_column["Y"])) == 34
    assert int(float(by_column["Z"])) == 23
    assert len(letters("AH", "BD")) == 23
    assert "dimethylacetamide" not in [
        header.lower() for header in headers[columns.index("AH") : columns.index("BD") + 1]
    ]

    leading_headers, leading_values = load_tsv(
        ROOT / "SBX_ONLY_TERPENES_WIDE_IMPORT_01_A_AE.txt"
    )
    analyte_headers, analyte_values = load_tsv(
        ROOT / "SBX_ONLY_TERPENES_WIDE_IMPORT_01_AH_BE.txt"
    )
    assert len(leading_headers) == len(leading_values) == 31
    assert len(analyte_headers) == len(analyte_values) == 24

    non_numeric_headers, non_numeric_values = load_tsv(
        ROOT / "failure_fixtures" / "non_numeric_analyte" / FIXTURE_NAME
    )
    missing_headers, missing_values = load_tsv(
        ROOT / "failure_fixtures" / "missing_peak_count" / FIXTURE_NAME
    )
    assert non_numeric_headers == missing_headers == headers
    assert non_numeric_values[columns.index("AH")] == "NOT_NUMERIC"
    assert missing_values[columns.index("Y")] == ""

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    assert config["assay_assignment"] is None
    assert config["filename_match"] == {
        "operator": "Should Equal",
        "value": FIXTURE_NAME,
    }
    assert config["excluded_formula_columns"] == ["AF", "AG"]
    assert config["uses_updateWorksheet"] is False
    assert config["uses_patchWorksheet"] is False
    assert [finder["source_range"] for finder in config["finders"]] == [
        "A2:AE2",
        "AH2:BE2",
    ]
    assert [finder["target_start_cell"] for finder in config["finders"]] == [
        "A2",
        "AH2",
    ]

    mapping = list(csv.DictReader(MAPPING.open(encoding="utf-8", newline="")))
    assert len(mapping) == 2
    assert [row["source_range"] for row in mapping] == ["A2:AE2", "AH2:BE2"]
    assert all(row["formula_columns_touched"] == "none" for row in mapping)

    worksheet_export = json.loads(SANITIZED_EXPORT.read_text(encoding="utf-8"))
    worksheets = worksheet_export["config"]["worksheets"]
    assert [worksheet["worksheetName"] for worksheet in worksheets] == [
        "Run Setup",
        "Instrument Import",
        "QC Review",
        "Publish",
    ]
    instrument = next(
        worksheet for worksheet in worksheets if worksheet["worksheetName"] == "Instrument Import"
    )
    assert len(instrument["columns"]) == 57
    assert len(instrument["data"][0]) == len(instrument["data"][1]) == 57
    af_formula = instrument["data"][1][columns.index("AF")]
    ag_formula = instrument["data"][1][columns.index("AG")]
    assert af_formula.startswith('=IF(A2="","",IF(OR(AG2=')
    assert '"Valid"' in af_formula and '"Rejected"' in af_formula
    assert ag_formula.startswith('=IF(A2="","",IF(OR(D2=')
    assert 'COUNT(AH2:BD2)<>23' in ag_formula
    assert '"Import row valid"' in ag_formula
    serialized_export = json.dumps(worksheet_export, ensure_ascii=False)
    assert '"pass_fail"' not in serialized_export.lower()
    assert 'pass/fail' not in serialized_export.lower()
    assert "ait.qbench.net" not in serialized_export
    assert "ait-sandbox.qbench.net" not in serialized_export

    print(
        json.dumps(
            {
                "status": "ok",
                "fixture_sha256": sha256(FIXTURE),
                "logical_columns": len(columns),
                "numeric_analytes": 23,
                "finder_ranges": ["A2:AE2", "AH2:BE2"],
                "formula_columns_excluded": ["AF", "AG"],
                "failure_fixtures": 2,
                "sandbox_worksheet_export": "sanitized and validated",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
