"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");

const PACKAGE = path.resolve(__dirname, "../..");
const REPO = path.resolve(PACKAGE, "../../../../..");
const core = require(path.join(PACKAGE, "src/qbench_browser_parser_core.js"));
const adapter = require(path.join(PACKAGE, "src/terpenes_multirecord_batch_adapter.js"));
const config = JSON.parse(fs.readFileSync(path.join(REPO, "QBench/Worksheets/Terpenes/development/2026-07-14_config_parser_foundation/config/terpenes_analytes.json"), "utf8"));
const fixture = fs.readFileSync(path.join(PACKAGE, "tests/fixtures/Output_redacted_fixture.txt"), "utf8");
const sourceHash = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef";

function changeField(text, field, value) {
  return text.replace(new RegExp(`^${field.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\t.*$`, "m"), `${field}\t${value}`);
}

function completeRecord(sampleName, sampleId, sampleType) {
  return changeField(changeField(changeField(fixture, "Sample Name", sampleName), "Sample ID", sampleId), "Sample Type", sampleType);
}

function parsedPair() {
  return core.parseLabSolutionsAsciiMultiRecord(`${completeRecord("Synthetic Sample One", "Synthetic-Test-1", "Unknown")}\n${completeRecord("Synthetic Sample Two", "Synthetic-Test-2", "Unknown")}`, config);
}

test("complete records split at [Header] and preserve all required source sections", () => {
  const parsed = parsedPair();
  assert.equal(parsed.records.length, 2);
  parsed.records.forEach((record, index) => {
    assert.equal(record.record_order, index + 1);
    assert.equal(record.counts.compound_result_row_count, 24);
    assert.equal(record.counts.reportable_compound_row_count, 23);
    assert.equal(record.counts.peak_table_row_count, 34);
    assert.ok(record.sample_information["Sample Name"]);
    assert.ok(record.original_files["Data File"]);
    assert.equal(record.peak_table.length, 34);
  });
});

test("Batch normalization emits 57 columns but never writes formula-owned AF/AG", () => {
  const normalized = adapter.normalizeRecords(parsedPair(), config, { source_file_sha256: sourceHash });
  assert.equal(normalized.batch_headers.length, 57);
  assert.equal(normalized.rows.length, 2);
  normalized.rows.forEach((row) => {
    assert.equal(row.batch_row.length, 57);
    assert.equal(row.write_cells.length, 55);
    assert.equal(row.write_cells.some((cell) => adapter.FORMULA_OWNED_HEADERS.has(cell.header)), false);
    assert.equal(row.category, "Sample");
    assert.equal(row.linkage_status, "matched_sample_id");
    assert.equal(row.transfer_eligible, true);
  });
  assert.deepEqual(normalized.batch_headers.slice(33, 56), config.internal_reportable_channels
    .slice().sort((left, right) => left.order - right.order).map((channel) => channel.worksheet_label));
});

test("optional mapping overlay replaces only normalized Sample-to-Test linkage", () => {
  const mapping = adapter.parseRuntimeMappingCsv([
    "labsolutions_sample_name,labsolutions_sample_id,qbench_test_display_id",
    "Synthetic Sample One,Synthetic-Test-1,QB-TEST-1001",
    "Synthetic Sample Two,Synthetic-Test-2,QB-TEST-1002",
  ].join("\n"));
  const normalized = adapter.normalizeRecords(parsedPair(), config, { source_file_sha256: sourceHash, runtime_mapping: mapping });
  assert.deepEqual(normalized.rows.map((row) => row.qbench_test_display_id), ["QB-TEST-1001", "QB-TEST-1002"]);
  assert.deepEqual(normalized.rows.map((row) => row.linkage_status), ["mapped_overlay", "mapped_overlay"]);
});

test("controls remain excluded and validation labels are held from Test Transfer", () => {
  const source = [
    completeRecord("System Suitability", "Control 1", "Control"),
    completeRecord("Low 1", "Low 1", "Unknown"),
  ].join("\n");
  const normalized = adapter.normalizeRecords(core.parseLabSolutionsAsciiMultiRecord(source, config), config, { source_file_sha256: sourceHash });
  assert.equal(normalized.rows[0].category, "System Suitability");
  assert.equal(normalized.rows[0].linkage_status, "control_excluded");
  assert.equal(normalized.rows[0].transfer_eligible, false);
  assert.equal(normalized.rows[1].linkage_status, "held_unmapped");
  assert.equal(normalized.rows[1].transfer_eligible, false);
});

test("zero, negative, and blank Compound Results concentrations retain their controlled types", () => {
  const zero = completeRecord("Synthetic Sample One", "Synthetic-Test-1", "Unknown").replace("2\talpha-Pinene\t5.809\t134208\t52649\t24.608\t", "2\talpha-Pinene\t5.809\t134208\t52649\t0\t");
  const negative = completeRecord("Synthetic Sample One", "Synthetic-Test-1", "Unknown").replace("2\talpha-Pinene\t5.809\t134208\t52649\t24.608\t", "2\talpha-Pinene\t5.809\t134208\t52649\t-1.25\t");
  const blank = completeRecord("Synthetic Sample One", "Synthetic-Test-1", "Unknown").replace("2\talpha-Pinene\t5.809\t134208\t52649\t24.608\t", "2\talpha-Pinene\t5.809\t134208\t52649\t\t");
  assert.equal(core.parseLabSolutionsAsciiMultiRecord(zero, config).records[0].reportable_analytes[0].conc, 0);
  assert.equal(core.parseLabSolutionsAsciiMultiRecord(negative, config).records[0].reportable_analytes[0].conc, -1.25);
  assert.equal(core.parseLabSolutionsAsciiMultiRecord(blank, config).records[0].reportable_analytes[0].conc, "");
});

test("normalized rows and stable keys are deterministic", () => {
  const source = `${completeRecord("Synthetic Sample One", "Synthetic-Test-1", "Unknown")}\n${completeRecord("Synthetic Sample Two", "Synthetic-Test-2", "Unknown")}`;
  const first = adapter.normalizeRecords(core.parseLabSolutionsAsciiMultiRecord(source, config), config, { source_file_sha256: sourceHash });
  const second = adapter.normalizeRecords(core.parseLabSolutionsAsciiMultiRecord(source, config), config, { source_file_sha256: sourceHash });
  assert.deepEqual(JSON.parse(JSON.stringify(first)), JSON.parse(JSON.stringify(second)));
  assert.deepEqual(first.rows.map((row) => row.source_row_key), [`labsolutions:${sourceHash}:1`, `labsolutions:${sourceHash}:2`]);
});
