"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const core = require("../../src/labsolutions_ascii_core.js");
const wide = require("../../src/wide_import_adapter.js");

const baseDir = path.resolve(__dirname, "..", "..");
const repoRoot = path.resolve(baseDir, "..", "..", "..", "..", "..");
const fixturePath = path.join(baseDir, "tests", "fixtures", "Output_redacted_fixture.txt");
const configPath = path.join(repoRoot, "QBench", "Worksheets", "Terpenes", "development", "2026-07-14_config_parser_foundation", "config", "terpenes_analytes.json");
const contextPath = path.join(baseDir, "config", "sandbox_context_fixture.json");
const config = JSON.parse(fs.readFileSync(configPath, "utf8"));
const context = JSON.parse(fs.readFileSync(contextPath, "utf8"));
const raw = fs.readFileSync(fixturePath);

function parsedWith(textBuffer = raw) {
  return core.parseLabSolutionsAscii(textBuffer, config, {});
}

function build(ctx = context, parsed = parsedWith()) {
  return wide.buildWideImportRow(parsed, config, ctx, {
    rawBytes: raw,
    filename: "Output_redacted_fixture.txt",
    source_instrument_file: "Output_redacted_fixture.txt",
  });
}

test("wide row has exactly 57 A:BE logical columns", () => {
  assert.equal(build().columns.length, 57);
  assert.equal(build().columns[0].column, "A");
  assert.equal(build().columns.at(-1).column, "BE");
});

test("AF and AG are excluded from write plan", () => {
  const plan = build().write_plan;
  assert.deepEqual(plan.excludes_formula_owned_columns, ["AF", "AG"]);
  assert.equal(plan.blocks.length, 2);
  assert.equal(plan.blocks[0].range, "Instrument Import!A2:AE2");
  assert.equal(plan.blocks[1].range, "Instrument Import!AH2:BE2");
});

test("AH:BD contains exactly 23 analyte values", () => {
  const columns = build().columns.slice(33, 56);
  assert.equal(columns[0].column, "AH");
  assert.equal(columns.at(-1).column, "BD");
  assert.equal(columns.length, 23);
});

test("Prompt 2 analyte order is preserved", () => {
  const expected = config.internal_reportable_channels.sort((a, b) => a.order - b.order).map((row) => row.internal_key);
  const actual = build().columns.slice(33, 56).map((col) => col.key);
  assert.deepEqual(actual, expected);
});

test("every analyte value is a JavaScript Number", () => {
  for (const column of build().columns.slice(33, 56)) {
    assert.equal(column.js_type, "number", column.key);
  }
});

test("zero remains a JavaScript Number", () => {
  const text = raw.toString("utf8").replace("2\talpha-Pinene\t5.809\t134208\t52649\t24.608", "2\talpha-Pinene\t5.809\t134208\t52649\t0");
  const row = build(context, parsedWith(Buffer.from(text, "utf8")));
  assert.equal(row.values.apinene, 0);
  assert.equal(row.columns.find((col) => col.key === "apinene").js_type, "number");
});

test("negative numeric concentration remains a JavaScript Number", () => {
  const text = raw.toString("utf8").replace("2\talpha-Pinene\t5.809\t134208\t52649\t24.608", "2\talpha-Pinene\t5.809\t134208\t52649\t-2.5");
  assert.equal(build(context, parsedWith(Buffer.from(text, "utf8"))).values.apinene, -2.5);
});

test("Dimethylacetamide is audit-only and not in AH:BD", () => {
  const row = build();
  assert.equal(row.values.dimethylacetamide_conc, 100);
  assert.equal(row.columns.slice(33, 56).some((col) => col.key === "dimethylacetamide"), false);
});

test("source metadata and hashes are preserved", () => {
  const row = build();
  assert.equal(row.values.source_instrument_file, "Output_redacted_fixture.txt");
  assert.equal(row.values.source_file_hash.length, 64);
  assert.equal(row.values.source_data_file.includes("TERPENE_FIXTURE_001.gcd"), true);
  assert.equal(row.values.detector_id, "DET#2");
});

test("source row hash is deterministic", () => {
  assert.equal(build().values.source_row_hash, build().values.source_row_hash);
});

test("generated output does not include local machine paths", () => {
  assert.equal(JSON.stringify(build()).includes("C:\\Users"), false);
});

test("missing context uses safe blank/default values", () => {
  const row = build({});
  assert.equal(row.values.qbench_test_id, "");
  assert.equal(row.values.sample_mass_g, "");
  assert.equal(row.values.final_volume_ml, "");
  assert.equal(row.values.integration_review_status, "Not Reviewed");
});

test("LabSolutions sample amount is not silently used as QBench mass", () => {
  const row = build({});
  assert.equal(row.values.labsolutions_sample_amount, 1);
  assert.equal(row.values.sample_mass_g, "");
});

test("LabSolutions dilution factor is retained but not silently applied", () => {
  const row = build({});
  assert.equal(row.values.labsolutions_dilution_factor, 1);
  assert.equal(row.values.qbench_df, "");
});

test("duplicate source row hash is rejected", () => {
  const row = build();
  assert.throws(() => wide.validateWideRowSet([row, row]), /Duplicate source_row_hash/);
});

test("duplicate file hash is recorded while distinct injections are retained", () => {
  const rowA = build({ ...context, qbench_test_id: "TR-0001" });
  const rowB = build({ ...context, qbench_test_id: "TR-0002" });
  const summary = wide.validateWideRowSet([rowA, rowB]);
  assert.deepEqual(summary.duplicate_file_hashes, [rowA.values.source_file_hash]);
});

test("multiple reviewed rows for one Test ID require decision", () => {
  const rowA = build({ ...context, run_order: 1 });
  const rowB = build({ ...context, run_order: 2, imported_at: "2026-07-15T00:01:00Z" });
  assert.equal(wide.publishSelectionStatus([rowA, rowB]), "decision_required");
});

test("rows sort deterministically without selecting a winner", () => {
  const rowA = build({ ...context, run_order: 2, qbench_test_id: "TR-0002" });
  const rowB = build({ ...context, run_order: 1, qbench_test_id: "TR-0001" });
  const sorted = wide.sortWideRows([rowA, rowB]);
  assert.equal(sorted[0].values.run_order, 1);
  assert.equal(sorted.length, 2);
});

test("TSV is a human artifact and leaves AF/AG blanks in full row", () => {
  const tsv = wide.rowToTsv(build().columns);
  const values = tsv.trimEnd().split("\n")[1].split("\t");
  assert.equal(values[31], "");
  assert.equal(values[32], "");
});
