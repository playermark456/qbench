"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const core = require("../../src/labsolutions_ascii_core.js");
const wide = require("../../src/wide_import_adapter.js");
const publish = require("../../src/reviewed_publish_adapter.js");

const baseDir = path.resolve(__dirname, "..", "..");
const repoRoot = path.resolve(baseDir, "..", "..", "..", "..", "..");
const fixturePath = path.join(baseDir, "tests", "fixtures", "Output_redacted_fixture.txt");
const configPath = path.join(repoRoot, "QBench", "Worksheets", "Terpenes", "development", "2026-07-14_config_parser_foundation", "config", "terpenes_analytes.json");
const contextPath = path.join(baseDir, "config", "sandbox_context_fixture.json");
const config = JSON.parse(fs.readFileSync(configPath, "utf8"));
const context = JSON.parse(fs.readFileSync(contextPath, "utf8"));
const raw = fs.readFileSync(fixturePath);

function reviewedRow(overrides = {}) {
  const parsed = core.parseLabSolutionsAscii(raw, config, {});
  return wide.buildWideImportRow(parsed, config, { ...context, ...overrides }, {
    rawBytes: raw,
    filename: "Output_redacted_fixture.txt",
    source_instrument_file: "Output_redacted_fixture.txt",
  });
}

function patch(row = reviewedRow(), options = {}) {
  return publish.buildReviewedPublishPatch(row, {
    explicitly_selected: true,
    import_validation_status: "Valid",
    source_batch_id: context.source_batch_id,
    target_row: 2,
    ...options,
  });
}

test("reviewed valid row produces D:AX patch", () => {
  const result = patch();
  assert.equal(result.status, "ok");
  assert.equal(result.range, "Publish!D2:AX2");
  assert.equal(result.writes[0].columns[0], "D");
  assert.equal(result.writes[0].columns.at(-1), "AX");
});

test("AY and later formula/control columns are never written", () => {
  assert.equal(patch().writes[0].columns.includes("AY"), false);
  assert.deepEqual(patch().excluded_formula_columns, ["AY", "AZ", "BA", "BB", "BC", "BD"]);
});

test("Dimethylacetamide maps only to AU", () => {
  const result = patch();
  const au = result.columns.find((col) => col.column === "AU");
  assert.equal(au.key, "dimethylacetamide_conc");
  assert.equal(result.columns.slice(0, 23).some((col) => col.key === "dimethylacetamide_conc"), false);
});

test("Import Validation Status must be Valid", () => {
  assert.equal(patch(reviewedRow(), { import_validation_status: "Review Required" }).status, "blocked");
});

test("Integration Review Status must be Reviewed", () => {
  assert.match(patch(reviewedRow({ integration_review_status: "Not Reviewed" })).errors.join(" "), /Reviewed/);
});

test("explicit source injection selection is required", () => {
  assert.match(patch(reviewedRow(), { explicitly_selected: false }).errors.join(" "), /selection/);
});

test("missing source hash blocks patch", () => {
  const row = reviewedRow();
  row.values.source_row_hash = "";
  assert.match(patch(row).errors.join(" "), /Source Row Hash/);
});

test("missing QBench Test ID blocks patch and Sample ID is not a join key", () => {
  const result = patch(reviewedRow({ qbench_test_id: "", qbench_sample_id: "SAMPLE-ONLY" }));
  assert.match(result.errors.join(" "), /QBench Test ID/);
});

test("multiple selected rows for one Test ID are rejected", () => {
  const rowA = reviewedRow({ run_order: 1 });
  const rowB = reviewedRow({ run_order: 2, imported_at: "2026-07-15T00:02:00Z" });
  const result = publish.buildPublishPatches([rowA, rowB], [rowA.values.source_row_hash, rowB.values.source_row_hash], {
    import_validation_status: "Valid",
    source_batch_id: context.source_batch_id,
  });
  assert.equal(result.status, "blocked");
  assert.match(result.errors[0], /Multiple selected/);
});

test("apply_in_qbench requires valid DF", () => {
  const result = patch(reviewedRow({ df_application_mode: "apply_in_qbench", qbench_df: "" }));
  assert.match(result.errors.join(" "), /DF must be/);
});

test("all 23 analytes must be numbers", () => {
  const row = reviewedRow();
  row.values.apinene = "24.608";
  assert.match(patch(row).errors.join(" "), /apinene/);
});
