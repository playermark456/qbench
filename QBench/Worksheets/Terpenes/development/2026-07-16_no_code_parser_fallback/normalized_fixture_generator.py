#!/usr/bin/env python3
"""Generate the controlled Prompt 4.6C normalized Terpenes TSV fixtures."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


OUTPUT_DIR = Path(__file__).resolve().parent
REPO_ROOT = OUTPUT_DIR.parents[4]
PROMPT_45_DIR = (
    REPO_ROOT
    / "QBench"
    / "Worksheets"
    / "Terpenes"
    / "development"
    / "2026-07-15_qbench_parser_wide_adapter"
)
PROMPT_2_CONFIG = (
    REPO_ROOT
    / "QBench"
    / "Worksheets"
    / "Terpenes"
    / "development"
    / "2026-07-14_config_parser_foundation"
    / "config"
    / "terpenes_analytes.json"
)
SOURCE_FIXTURE = PROMPT_45_DIR / "tests" / "fixtures" / "Output_redacted_fixture.txt"
CONTEXT_FIXTURE = PROMPT_45_DIR / "config" / "sandbox_context_fixture.json"

FULL_FIXTURE = OUTPUT_DIR / "SBX_ONLY_TERPENES_WIDE_IMPORT_01.txt"
LEADING_BLOCK_FIXTURE = OUTPUT_DIR / "SBX_ONLY_TERPENES_WIDE_IMPORT_01_A_AE.txt"
ANALYTE_BLOCK_FIXTURE = OUTPUT_DIR / "SBX_ONLY_TERPENES_WIDE_IMPORT_01_AH_BE.txt"
NON_NUMERIC_FIXTURE = (
    OUTPUT_DIR
    / "failure_fixtures"
    / "non_numeric_analyte"
    / "SBX_ONLY_TERPENES_WIDE_IMPORT_01.txt"
)
MISSING_PEAK_COUNT_FIXTURE = (
    OUTPUT_DIR
    / "failure_fixtures"
    / "missing_peak_count"
    / "SBX_ONLY_TERPENES_WIDE_IMPORT_01.txt"
)
MAPPING_CSV = OUTPUT_DIR / "no_code_parser_mapping.csv"
MANIFEST = OUTPUT_DIR / "no_code_parser_manifest.json"
SANITIZED_WORKSHEET_EXPORT = (
    OUTPUT_DIR
    / "SBX_ONLY_TERPENES_2026_07_16_No_Code_Batch_Import__sanitized_export_spreadsheet.json"
)
SANITIZED_PARSER_CONFIG = OUTPUT_DIR / "sanitized_no_code_parser_configuration.json"

NODE_SCRIPT = r"""
const fs = require("fs");
const path = require("path");

const prompt45Dir = process.argv[1];
const configPath = process.argv[2];
const sourcePath = process.argv[3];
const contextPath = process.argv[4];
const core = require(path.join(prompt45Dir, "src", "labsolutions_ascii_core.js"));
const wide = require(path.join(prompt45Dir, "src", "wide_import_adapter.js"));

const config = JSON.parse(fs.readFileSync(configPath, "utf8"));
const context = JSON.parse(fs.readFileSync(contextPath, "utf8"));
const raw = fs.readFileSync(sourcePath);
const parsed = core.parseLabSolutionsAscii(raw, config, {});
const row = wide.buildWideImportRow(parsed, config, context, {
  rawBytes: raw,
  filename: "Output_redacted_fixture.txt",
  source_instrument_file: "Output_redacted_fixture.txt"
});

process.stdout.write(JSON.stringify({row, parsed_counts: parsed.counts}));
"""

NUMERIC_COLUMNS = {
    "B", "C", "H", "I", "L", "M", "X", "Y", "Z", "AA", "AB",
    "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ",
    "AR", "AS", "AT", "AU", "AV", "AW", "AX", "AY", "AZ", "BA",
    "BB", "BC", "BD",
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def find_node() -> str:
    env_node = os.environ.get("TERPENES_NODE_EXE") or os.environ.get("NODE_EXE")
    if env_node and Path(env_node).is_file():
        return env_node
    installed = shutil.which("node")
    if installed:
        return installed
    exe = Path(sys.executable)
    candidates: list[Path] = []
    for parent in exe.parents:
        candidates.append(parent / "node" / "bin" / "node.exe")
        candidates.append(parent / "node" / "bin" / "node")
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    raise SystemExit(
        "Node.js executable not found. Set TERPENES_NODE_EXE or use the bundled Codex runtime."
    )


def excel_columns(start: str, end: str) -> list[str]:
    def number(column: str) -> int:
        value = 0
        for character in column:
            value = value * 26 + ord(character) - ord("A") + 1
        return value

    def letters(value: int) -> str:
        result = ""
        while value:
            value, remainder = divmod(value - 1, 26)
            result = chr(ord("A") + remainder) + result
        return result

    return [letters(value) for value in range(number(start), number(end) + 1)]


def tsv_cell(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        raise AssertionError("Boolean values are not permitted in the normalized fixture.")
    if isinstance(value, float):
        return format(value, ".15g")
    return str(value).replace("\t", " ").replace("\r", " ").replace("\n", " ")


def tsv_bytes(columns: list[dict[str, object]]) -> bytes:
    header = "\t".join(str(column["header"]) for column in columns)
    values = "\t".join(tsv_cell(column["value"]) for column in columns)
    return f"{header}\n{values}\n".encode("utf-8")


def write_bytes_if_changed(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_bytes() != value:
        path.write_bytes(value)


def mutate_value(
    columns: list[dict[str, object]], column_letter: str, value: object
) -> list[dict[str, object]]:
    mutated = deepcopy(columns)
    matches = [column for column in mutated if column["column"] == column_letter]
    assert len(matches) == 1
    matches[0]["value"] = value
    return mutated


def validate_row(row: dict[str, object], parsed_counts: dict[str, object]) -> None:
    columns = row["columns"]
    assert isinstance(columns, list)
    expected_letters = excel_columns("A", "BE")
    actual_letters = [column["column"] for column in columns]
    assert actual_letters == expected_letters
    assert len(columns) == 57

    by_letter = {column["column"]: column for column in columns}
    assert by_letter["AF"]["value"] == ""
    assert by_letter["AG"]["value"] == ""
    assert by_letter["BE"]["value"] == row["values"]["source_row_hash"]
    assert len(str(by_letter["BE"]["value"])) == 64

    analytes = [by_letter[letter] for letter in excel_columns("AH", "BD")]
    assert len(analytes) == 23
    assert all(isinstance(column["value"], (int, float)) for column in analytes)
    assert all(
        isinstance(by_letter[letter]["value"], (int, float))
        for letter in NUMERIC_COLUMNS
    )
    assert parsed_counts["compound_result_row_count"] == 24
    assert parsed_counts["peak_table_row_count"] == 34
    assert parsed_counts["reportable_compound_row_count"] == 23
    assert isinstance(by_letter["AA"]["value"], (int, float))

    headers = [str(column["header"]).lower() for column in columns]
    assert not any("pass" in header or "fail" in header for header in headers)
    assert "dimethylacetamide" not in [
        str(column["header"]).lower() for column in analytes
    ]


def build_mapping_csv() -> bytes:
    rows = [
        [
            "finder_name",
            "source_file",
            "source_range",
            "target_sheet",
            "target_start_cell",
            "target_range",
            "transpose",
            "repeat",
            "formula_columns_touched",
        ],
        [
            "SBX_ONLY_TERPENES_2026_07_16_A_AE",
            FULL_FIXTURE.name,
            "A2:AE2",
            "Instrument Import",
            "A2",
            "A2:AE2",
            "false",
            "false",
            "none",
        ],
        [
            "SBX_ONLY_TERPENES_2026_07_16_AH_BE",
            FULL_FIXTURE.name,
            "AH2:BE2",
            "Instrument Import",
            "AH2",
            "AH2:BE2",
            "false",
            "false",
            "none",
        ],
    ]
    return ("\n".join(",".join(row) for row in rows) + "\n").encode("utf-8")


def main() -> None:
    completed = subprocess.run(
        [
            find_node(),
            "-e",
            NODE_SCRIPT,
            str(PROMPT_45_DIR),
            str(PROMPT_2_CONFIG),
            str(SOURCE_FIXTURE),
            str(CONTEXT_FIXTURE),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    generated = json.loads(completed.stdout)
    row = generated["row"]
    parsed_counts = generated["parsed_counts"]
    validate_row(row, parsed_counts)

    columns = row["columns"]
    by_letter = {column["column"]: index for index, column in enumerate(columns)}
    full = tsv_bytes(columns)
    leading = tsv_bytes(columns[by_letter["A"] : by_letter["AE"] + 1])
    analytes = tsv_bytes(columns[by_letter["AH"] : by_letter["BE"] + 1])
    non_numeric = tsv_bytes(mutate_value(columns, "AH", "NOT_NUMERIC"))
    missing_peak_count = tsv_bytes(mutate_value(columns, "Y", ""))

    write_bytes_if_changed(FULL_FIXTURE, full)
    write_bytes_if_changed(LEADING_BLOCK_FIXTURE, leading)
    write_bytes_if_changed(ANALYTE_BLOCK_FIXTURE, analytes)
    write_bytes_if_changed(NON_NUMERIC_FIXTURE, non_numeric)
    write_bytes_if_changed(MISSING_PEAK_COUNT_FIXTURE, missing_peak_count)
    write_bytes_if_changed(MAPPING_CSV, build_mapping_csv())

    sandbox_exports = {}
    if SANITIZED_WORKSHEET_EXPORT.exists():
        sandbox_exports[SANITIZED_WORKSHEET_EXPORT.name] = {
            "sha256": sha256_file(SANITIZED_WORKSHEET_EXPORT),
            "internal_sandbox_ids_removed": True,
        }
    if SANITIZED_PARSER_CONFIG.exists():
        sandbox_exports[SANITIZED_PARSER_CONFIG.name] = {
            "sha256": sha256_file(SANITIZED_PARSER_CONFIG),
            "internal_sandbox_ids_removed": True,
        }

    manifest = {
        "schema_version": 1,
        "package": "2026-07-16_no_code_parser_fallback",
        "prompt": "Prompt 4.6C",
        "status": "sandbox_validation_complete",
        "source_pipeline": [
            "Output_redacted_fixture.txt",
            "Prompt 4.5 local LabSolutions parser",
            "Prompt 4.5 typed wide-row adapter",
            FULL_FIXTURE.name,
            "QBench No-Code File Parser",
            "Batch Worksheet Instrument Import row",
        ],
        "source_fixture": {
            "path": SOURCE_FIXTURE.relative_to(REPO_ROOT).as_posix(),
            "sha256": sha256_file(SOURCE_FIXTURE),
        },
        "prompt_45_dependencies": {
            "parser_core": (
                PROMPT_45_DIR / "src" / "labsolutions_ascii_core.js"
            ).relative_to(REPO_ROOT).as_posix(),
            "wide_adapter": (
                PROMPT_45_DIR / "src" / "wide_import_adapter.js"
            ).relative_to(REPO_ROOT).as_posix(),
            "context": CONTEXT_FIXTURE.relative_to(REPO_ROOT).as_posix(),
        },
        "fixtures": {
            FULL_FIXTURE.name: {
                "sha256": sha256_bytes(full),
                "rows": 2,
                "logical_columns": 57,
                "logical_range": "A:BE",
            },
            LEADING_BLOCK_FIXTURE.name: {
                "sha256": sha256_bytes(leading),
                "rows": 2,
                "logical_columns": 31,
                "logical_range": "A:AE",
            },
            ANALYTE_BLOCK_FIXTURE.name: {
                "sha256": sha256_bytes(analytes),
                "rows": 2,
                "logical_columns": 24,
                "logical_range": "AH:BE",
            },
        },
        "typed_row": {
            "source_row_hash": row["values"]["source_row_hash"],
            "compound_result_row_count": parsed_counts["compound_result_row_count"],
            "peak_table_row_count": parsed_counts["peak_table_row_count"],
            "reportable_compound_row_count": parsed_counts[
                "reportable_compound_row_count"
            ],
            "analyte_numeric_count": 23,
            "dimethylacetamide_numeric_audit_only": True,
            "pass_fail_field_present": False,
        },
        "finder_mapping": [
            {
                "source_range": "A2:AE2",
                "target_range": "Instrument Import!A2:AE2",
            },
            {
                "source_range": "AH2:BE2",
                "target_range": "Instrument Import!AH2:BE2",
            },
        ],
        "formula_owned_columns": {
            "AF": "blank source placeholder; excluded from finder mappings",
            "AG": "blank source placeholder; excluded from finder mappings",
        },
        "failure_fixtures": {
            NON_NUMERIC_FIXTURE.relative_to(OUTPUT_DIR).as_posix(): {
                "sha256": sha256_bytes(non_numeric),
                "mutation": "AH2 is the literal text NOT_NUMERIC",
                "expected_formula_result": "AF2 Rejected; AG2 Analytical values incomplete",
            },
            MISSING_PEAK_COUNT_FIXTURE.relative_to(OUTPUT_DIR).as_posix(): {
                "sha256": sha256_bytes(missing_peak_count),
                "mutation": "Y2 is blank",
                "expected_formula_result": "AF2 Rejected; AG2 Peak Table row count required",
            },
        },
        "sandbox_validation": {
            "canonical_parser_job": "SUCCESS",
            "canonical_formula_result": "AF2 Valid; AG2 Import row valid",
            "duplicate_parser_job": "SUCCESS",
            "duplicate_attachment_behavior": (
                "single attachment record advanced to version 2; row 2 remained "
                "canonical and row 3 remained blank"
            ),
            "non_numeric_parser_job": "SUCCESS",
            "non_numeric_formula_result": (
                "AF2 Rejected; AG2 Analytical values incomplete"
            ),
            "missing_peak_count_parser_job": "SUCCESS",
            "missing_peak_count_formula_result": (
                "AF2 Rejected; AG2 Peak Table row count required"
            ),
            "publish_writes": 0,
            "test_worksheet_writes": 0,
            "pass_fail_artifact_created": False,
            "navigate_away_reload_verified": True,
        },
        "sandbox_exports": sandbox_exports,
        "sandbox_internal_object_ids_committed": False,
        "local_normalization_required": True,
        "raw_labsolutions_parsed_directly_in_qbench": False,
        "production_ready": False,
        "prompt5_started": False,
    }
    manifest_bytes = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
    write_bytes_if_changed(MANIFEST, manifest_bytes)

    print(
        json.dumps(
            {
                "status": "ok",
                "fixture": FULL_FIXTURE.name,
                "fixture_sha256": sha256_bytes(full),
                "logical_columns": len(columns),
                "source_row_hash": row["values"]["source_row_hash"],
                "numeric_analytes": 23,
                "compound_result_rows": parsed_counts["compound_result_row_count"],
                "peak_table_rows": parsed_counts["peak_table_row_count"],
                "reportable_rows": parsed_counts["reportable_compound_row_count"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
