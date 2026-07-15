#!/usr/bin/env python3
"""Generate controlled Prompt 4.5 parser and wide-row fixtures."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = BASE_DIR.parents[4]
NODE_MODULE_SCRIPT = r"""
const fs = require("fs");
const path = require("path");
const core = require(path.join(process.argv[1], "src", "labsolutions_ascii_core.js"));
const wide = require(path.join(process.argv[1], "src", "wide_import_adapter.js"));
const publish = require(path.join(process.argv[1], "src", "reviewed_publish_adapter.js"));

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}
function writeJson(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), {recursive: true});
  fs.writeFileSync(filePath, JSON.stringify(value, null, 2) + "\n", "utf8");
}
function writeText(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), {recursive: true});
  fs.writeFileSync(filePath, value, "utf8");
}

const baseDir = process.argv[1];
const repoRoot = process.argv[2];
const configPath = path.join(repoRoot, "QBench", "Worksheets", "Terpenes", "development", "2026-07-14_config_parser_foundation", "config", "terpenes_analytes.json");
const fixturePath = path.join(baseDir, "tests", "fixtures", "Output_redacted_fixture.txt");
const contextPath = path.join(baseDir, "config", "sandbox_context_fixture.json");
const config = readJson(configPath);
const context = readJson(contextPath);
const raw = fs.readFileSync(fixturePath);
const parsed = core.parseLabSolutionsAscii(raw, config, {});
const row = wide.buildWideImportRow(parsed, config, context, {
  rawBytes: raw,
  filename: "Output_redacted_fixture.txt",
  source_instrument_file: "Output_redacted_fixture.txt"
});
const patch = publish.buildReviewedPublishPatch(row, {
  explicitly_selected: true,
  import_validation_status: "Valid",
  source_batch_id: context.source_batch_id,
  target_row: 2
});

writeJson(path.join(baseDir, "tests", "fixtures", "expected_parsed_core.json"), parsed);
writeJson(path.join(baseDir, "tests", "fixtures", "expected_wide_import_row.json"), row);
writeJson(path.join(baseDir, "tests", "fixtures", "expected_publish_patch.json"), patch);
writeJson(path.join(baseDir, "dist", "Output_redacted_wide_import_row.json"), row);
writeText(path.join(baseDir, "dist", "Output_redacted_wide_import_row.tsv"), wide.rowToTsv(row.columns));
writeText(path.join(baseDir, "dist", "Output_redacted_block_A_AE.tsv"), wide.blockToTsv(row.columns, "A", "AE"));
writeText(path.join(baseDir, "dist", "Output_redacted_block_AH_BE.tsv"), wide.blockToTsv(row.columns, "AH", "BE"));
console.log(JSON.stringify({
  status: "ok",
  compound_result_row_count: parsed.counts.compound_result_row_count,
  peak_table_row_count: parsed.counts.peak_table_row_count,
  reportable_compound_row_count: parsed.counts.reportable_compound_row_count,
  dimethylacetamide_conc_type: typeof parsed.dimethylacetamide_audit.conc,
  source_file_hash: row.values.source_file_hash,
  source_row_hash: row.values.source_row_hash,
  write_plan_block_count: row.write_plan.blocks.length
}, null, 2));
"""


def find_node() -> str:
    candidates: list[Path] = []
    env_node = os.environ.get("TERPENES_NODE_EXE") or os.environ.get("NODE_EXE")
    if env_node:
        candidates.append(Path(env_node))
    if shutil.which("node"):
        return str(shutil.which("node"))
    exe = Path(sys.executable)
    for parent in exe.parents:
        candidates.append(parent / "node" / "bin" / "node.exe")
        candidates.append(parent / "node" / "bin" / "node")
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    raise SystemExit("Node.js executable not found. Set TERPENES_NODE_EXE or use the bundled Codex runtime.")


def main() -> None:
    node = find_node()
    result = subprocess.run(
        [node, "-e", NODE_MODULE_SCRIPT, str(BASE_DIR), str(REPO_ROOT)],
        check=True,
        text=True,
        capture_output=True,
    )
    print(result.stdout, end="")


if __name__ == "__main__":
    main()
