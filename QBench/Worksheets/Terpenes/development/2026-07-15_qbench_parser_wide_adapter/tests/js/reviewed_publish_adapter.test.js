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

function variantRaw(label) {
  return Buffer.from(raw.toString("utf8")
    .replaceAll("TERPENE_FIXTURE_001.gcd", `TERPENE_FIXTURE_${label}.gcd`)
    .replace("6/24/2026 11:09:50 AM", `6/24/2026 11:${String(label).padStart(2, "0")}:50 AM`), "utf8");
}

function reviewedRow(overrides = {}, rawBytes = raw) {
  const parsed = core.parseLabSolutionsAscii(rawBytes, config, {});
  return wide.buildWideImportRow(parsed, config, { ...context, ...overrides }, {
    rawBytes,
    filename: "Output_redacted_fixture.txt",
    source_instrument_file: "Output_redacted_fixture.txt",
  });
}

function evidenceFor(row, overrides = {}) {
  return {
    source_row_hash: row.values.source_row_hash,
    explicitly_selected: true,
    import_validation_status: "Valid",
    import_message: "Import row valid",
    ...overrides,
  };
}

function patch(row = reviewedRow(), options = {}) {
  return publish.buildReviewedPublishPatch(row, {
    review_evidence: evidenceFor(row),
    source_batch_id: context.source_batch_id,
    target_row: 2,
    ...options,
  });
}

function patches(rows, mapping, options = {}) {
  return publish.buildPublishPatches(rows, rows.map((row) => row.values.source_row_hash), {
    review_evidence: rows.map((row) => evidenceFor(row)),
    source_batch_id: context.source_batch_id,
    publish_row_mapping: mapping,
    ...options,
  });
}

test("reviewed valid row produces D:AX patch with Test ID, row, range, and source hash", () => {
  const row = reviewedRow();
  const result = patch(row);
  assert.equal(result.status, "ok");
  assert.equal(result.expected_qbench_test_id, context.qbench_test_id);
  assert.equal(result.target_publish_row, 2);
  assert.equal(result.range, "Publish!D2:AX2");
  assert.equal(result.source_row_hash, row.values.source_row_hash);
  assert.equal(result.writes[0].columns[0], "D");
  assert.equal(result.writes[0].columns.at(-1), "AX");
  assert.equal(result.writes[0].expected_qbench_test_id, context.qbench_test_id);
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

for (const badUnit of ["", "mg/mL", "ppm", "UG/ML", "arbitrary text"]) {
  test(`LabSolutions unit ${badUnit || "<blank>"} blocks patch`, () => {
    const row = reviewedRow();
    row.values.labsolutions_conc_unit = badUnit;
    row.values.unit_confirmed = true;
    const result = patch(row, { review_evidence: evidenceFor(row) });
    assert.equal(result.status, "blocked");
    assert.match(result.errors.join(" "), /exactly ug\/mL/);
  });
}

test("unit_confirmed TRUE with blank unit is still blocked", () => {
  const row = reviewedRow();
  row.values.labsolutions_conc_unit = "";
  row.values.unit_confirmed = "TRUE";
  const result = patch(row, { review_evidence: evidenceFor(row) });
  assert.equal(result.status, "blocked");
  assert.match(result.errors.join(" "), /exactly ug\/mL/);
});

test("only exact ug/mL plus unit confirmation proceeds", () => {
  const row = reviewedRow();
  row.values.labsolutions_conc_unit = "ug/mL";
  row.values.unit_confirmed = true;
  assert.equal(patch(row, { review_evidence: evidenceFor(row) }).status, "ok");
  row.values.unit_confirmed = false;
  assert.match(patch(row, { review_evidence: evidenceFor(row) }).errors.join(" "), /Unit confirmation/);
});

test("global import_validation_status cannot authorize a reviewed row", () => {
  const result = publish.buildReviewedPublishPatch(reviewedRow(), {
    explicitly_selected: true,
    import_validation_status: "Valid",
    source_batch_id: context.source_batch_id,
    target_row: 2,
  });
  assert.equal(result.status, "blocked");
  assert.match(result.errors.join(" "), /Review evidence keyed/);
});

test("row-specific review evidence requires selected, Valid status, and exact valid message", () => {
  const row = reviewedRow();
  for (const evidence of [
    undefined,
    evidenceFor(row, { explicitly_selected: false }),
    evidenceFor(row, { import_validation_status: "Review Required" }),
    evidenceFor(row, { import_message: "Looks fine" }),
  ]) {
    assert.equal(patch(row, { review_evidence: evidence }).status, "blocked");
  }
});

test("missing source hash blocks patch", () => {
  const row = reviewedRow();
  row.values.source_row_hash = "";
  assert.match(patch(row, { review_evidence: evidenceFor(row) }).errors.join(" "), /Source Row Hash/);
});

test("missing QBench Test ID blocks patch and Sample ID is not a join key", () => {
  const result = patch(reviewedRow({ qbench_test_id: "", qbench_sample_id: "SAMPLE-ONLY" }));
  assert.match(result.errors.join(" "), /QBench Test ID/);
});

test("buildPublishPatches requires explicit Test ID to Publish row mapping", () => {
  const row = reviewedRow();
  const result = publish.buildPublishPatches([row], [row.values.source_row_hash], {
    review_evidence: [evidenceFor(row)],
    source_batch_id: context.source_batch_id,
  });
  assert.equal(result.status, "blocked");
  assert.equal(result.patches.length, 0);
  assert.match(result.errors.join(" "), /mapping is required/);
});

test("physical mapping unavailable returns Test-ID-keyed preview without a concrete range", () => {
  const row = reviewedRow();
  const result = publish.buildPublishPatches([row], [row.values.source_row_hash], {
    review_evidence: [evidenceFor(row)],
    source_batch_id: context.source_batch_id,
    allow_test_id_preview_without_range: true,
  });
  assert.equal(result.status, "preview_only");
  assert.deepEqual(result.test_id_preview, [{
    qbench_test_id: context.qbench_test_id,
    source_row_hash: row.values.source_row_hash,
    target_publish_row: null,
    range: null,
  }]);
});

test("mapped publish patches use Test ID, not Sample ID", () => {
  const row = reviewedRow({ qbench_sample_id: "SAMPLE-WOULD-BE-WRONG" });
  const result = patches([row], { [context.qbench_test_id]: 12 });
  assert.equal(result.status, "ok");
  assert.equal(result.patches[0].target_publish_row, 12);
  assert.equal(result.patches[0].range, "Publish!D12:AX12");
});

test("duplicate destination rows are rejected atomically", () => {
  const rowA = reviewedRow({ qbench_test_id: "TR-0001" }, variantRaw("002"));
  const rowB = reviewedRow({ qbench_test_id: "TR-0002" }, variantRaw("003"));
  const result = patches([rowA, rowB], { "TR-0001": 12, "TR-0002": 12 });
  assert.equal(result.status, "blocked");
  assert.deepEqual(result.patches, []);
  assert.match(result.errors.join(" "), /Duplicate Publish destination row/);
});

test("out-of-range Publish rows are rejected", () => {
  const row = reviewedRow();
  const result = patches([row], { [context.qbench_test_id]: 99 });
  assert.equal(result.status, "blocked");
  assert.match(result.errors.join(" "), /out of range/);
});

test("mapping for wrong Test ID is rejected", () => {
  const row = reviewedRow();
  const result = patches([row], { "TR-WRONG": 12 });
  assert.equal(result.status, "blocked");
  assert.match(result.errors.join(" "), /wrong or unselected Test ID/);
});

test("two selected rows for one Test ID are rejected", () => {
  const rowA = reviewedRow({ run_order: 1, qbench_test_id: "TR-DUP" }, variantRaw("004"));
  const rowB = reviewedRow({ run_order: 2, qbench_test_id: "TR-DUP" }, variantRaw("005"));
  const result = patches([rowA, rowB], { "TR-DUP": 12 });
  assert.equal(result.status, "blocked");
  assert.match(result.errors.join(" "), /Multiple selected rows/);
});

test("one selected row assigned multiple times is rejected by duplicate selection", () => {
  const row = reviewedRow();
  const result = publish.buildPublishPatches([row], [row.values.source_row_hash, row.values.source_row_hash], {
    review_evidence: [evidenceFor(row)],
    source_batch_id: context.source_batch_id,
    publish_row_mapping: { [context.qbench_test_id]: 12 },
  });
  assert.equal(result.status, "blocked");
  assert.match(result.errors.join(" "), /Duplicate selected source_row_hash/);
});

test("unknown review evidence hash is rejected", () => {
  const row = reviewedRow();
  const result = publish.buildPublishPatches([row], [row.values.source_row_hash], {
    review_evidence: [evidenceFor(row), evidenceFor(row, { source_row_hash: "unknown" })],
    source_batch_id: context.source_batch_id,
    publish_row_mapping: { [context.qbench_test_id]: 12 },
  });
  assert.equal(result.status, "blocked");
  assert.match(result.errors.join(" "), /unknown source_row_hash/);
});

test("duplicate review evidence is rejected", () => {
  const row = reviewedRow();
  const result = publish.buildPublishPatches([row], [row.values.source_row_hash], {
    review_evidence: [evidenceFor(row), evidenceFor(row)],
    source_batch_id: context.source_batch_id,
    publish_row_mapping: { [context.qbench_test_id]: 12 },
  });
  assert.equal(result.status, "blocked");
  assert.match(result.errors.join(" "), /Duplicate review evidence/);
});

test("selected hash without a matching row is rejected", () => {
  const row = reviewedRow();
  const result = publish.buildPublishPatches([row], [row.values.source_row_hash, "missing"], {
    review_evidence: [evidenceFor(row)],
    source_batch_id: context.source_batch_id,
    publish_row_mapping: { [context.qbench_test_id]: 12 },
  });
  assert.equal(result.status, "blocked");
  assert.match(result.errors.join(" "), /no matching row/);
});

test("row without matching selected hash is rejected", () => {
  const row = reviewedRow();
  const result = publish.buildPublishPatches([row], [], {
    review_evidence: [evidenceFor(row)],
    source_batch_id: context.source_batch_id,
    publish_row_mapping: { [context.qbench_test_id]: 12 },
  });
  assert.equal(result.status, "blocked");
  assert.match(result.errors.join(" "), /missing from selected hashes/);
});

test("one valid and one invalid selected row blocks the entire preview", () => {
  const rowA = reviewedRow({ qbench_test_id: "TR-0001" }, variantRaw("006"));
  const rowB = reviewedRow({ qbench_test_id: "TR-0002" }, variantRaw("007"));
  rowB.values.apinene = "24.608";
  const result = patches([rowA, rowB], { "TR-0001": 12, "TR-0002": 27 });
  assert.equal(result.status, "blocked");
  assert.deepEqual(result.patches, []);
  assert.match(result.errors.join(" "), /apinene/);
});

test("wrong unit on one selected row blocks all patches", () => {
  const rowA = reviewedRow({ qbench_test_id: "TR-0001" }, variantRaw("008"));
  const rowB = reviewedRow({ qbench_test_id: "TR-0002" }, variantRaw("009"));
  rowB.values.labsolutions_conc_unit = "ppm";
  const result = patches([rowA, rowB], { "TR-0001": 12, "TR-0002": 27 });
  assert.equal(result.status, "blocked");
  assert.deepEqual(result.patches, []);
});

test("invalid worksheet review status on one selected row blocks all patches", () => {
  const rowA = reviewedRow({ qbench_test_id: "TR-0001" }, variantRaw("010"));
  const rowB = reviewedRow({ qbench_test_id: "TR-0002", integration_review_status: "Not Reviewed" }, variantRaw("011"));
  const result = patches([rowA, rowB], { "TR-0001": 12, "TR-0002": 27 });
  assert.equal(result.status, "blocked");
  assert.deepEqual(result.patches, []);
  assert.match(result.errors.join(" "), /Integration Review Status/);
});

test("missing Publish row mapping for one selected row blocks all patches", () => {
  const rowA = reviewedRow({ qbench_test_id: "TR-0001" }, variantRaw("012"));
  const rowB = reviewedRow({ qbench_test_id: "TR-0002" }, variantRaw("013"));
  const result = patches([rowA, rowB], { "TR-0001": 12 });
  assert.equal(result.status, "blocked");
  assert.deepEqual(result.patches, []);
  assert.match(result.errors.join(" "), /Missing Publish row mapping/);
});

test("apply_in_qbench requires valid DF", () => {
  const result = patch(reviewedRow({ df_application_mode: "apply_in_qbench", qbench_df: "" }));
  assert.match(result.errors.join(" "), /DF must be/);
});
