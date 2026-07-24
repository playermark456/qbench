"use strict";

const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const core = require("../src/qbench_browser_parser_core.js");
const adapter = require("../src/terpenes_multirecord_batch_adapter.js");

const PACKAGE = path.resolve(__dirname, "..");
const REPO = path.resolve(PACKAGE, "../../../../..");
const CONFIG_PATH = path.join(REPO, "QBench/Worksheets/Terpenes/development/2026-07-14_config_parser_foundation/config/terpenes_analytes.json");
const BATCH_CANDIDATE_PATH = path.join(REPO, "QBench/Worksheets/Terpenes/development/2026-07-17_production_candidate/production_candidates/SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS__v2_formula_fix.json");
const EXPECTED_COUNTS = Object.freeze({ Null: 3, Blank: 2, "System Suitability": 3, Standard: 6, CCV: 3, LOQ: 1, "Matrix Blank": 1, Sample: 15 });

function quoteCsv(value) {
  return `"${String(value).replace(/"/g, '""')}"`;
}

function countBy(items, getKey) {
  return items.reduce((counts, item) => {
    const key = getKey(item);
    counts[key] = (counts[key] || 0) + 1;
    return counts;
  }, {});
}

function assert(condition, code) {
  if (!condition) { const error = new Error(code); error.code = code; throw error; }
}

function run(inputPath) {
  if (!inputPath) throw new Error("Usage: node validate_terpenes_multirecord_parser.js <ASCIIData.txt>");
  const sourceBuffer = fs.readFileSync(inputPath);
  const sourceText = sourceBuffer.toString("utf8");
  const sourceHash = crypto.createHash("sha256").update(sourceBuffer).digest("hex");
  const config = JSON.parse(fs.readFileSync(CONFIG_PATH, "utf8"));
  const candidate = JSON.parse(fs.readFileSync(BATCH_CANDIDATE_PATH, "utf8"));
  const parsed = core.parseLabSolutionsAsciiMultiRecord(sourceText, config);
  const normalized = adapter.normalizeRecords(parsed, config, { source_file_sha256: sourceHash });
  const secondNormalized = adapter.normalizeRecords(core.parseLabSolutionsAsciiMultiRecord(sourceText, config), config, { source_file_sha256: sourceHash });
  const categoryCounts = countBy(normalized.rows, (row) => row.category);
  assert(JSON.stringify(categoryCounts) === JSON.stringify(EXPECTED_COUNTS), "CATEGORY_COUNTS");
  assert(normalized.rows.length === 34, "RECORD_COUNT");
  assert(parsed.records.every((record) => record.sample_information && record.original_files && record.peak_table && record.compound_results.length === 24), "COMPLETE_RECORD_SECTIONS");
  assert(normalized.batch_headers.length === 57, "BATCH_COLUMN_COUNT");
  assert(normalized.rows.every((row) => row.write_cells.length === 55 && !row.write_cells.some((cell) => adapter.FORMULA_OWNED_HEADERS.has(cell.header))), "FORMULA_OWNED_EXCLUSION");
  assert(JSON.stringify(candidate.data["Instrument Import"][0]) === JSON.stringify(normalized.batch_headers), "BATCH_CANDIDATE_HEADER_COMPATIBILITY");
  assert(JSON.stringify(normalized) === JSON.stringify(secondNormalized), "IDEMPOTENCY");
  assert(normalized.batch_headers.every((header) => !/pass\s*\/?\s*fail/i.test(header)), "NO_PASS_FAIL_FIELDS");
  const reportableRows = normalized.rows.filter((row) => row.category === "Sample");
  const controls = normalized.rows.filter((row) => row.category !== "Sample");
  assert(reportableRows.length === 15 && reportableRows.every((row) => row.linkage_status === "held_unmapped" && !row.transfer_eligible), "UNMAPPED_REPORTABLE_HOLD");
  assert(controls.length === 19 && controls.every((row) => row.linkage_status === "control_excluded" && !row.transfer_eligible), "CONTROL_EXCLUSION");
  const overlayRows = reportableRows.slice(0, 2);
  const byRecordOrder = new Map(parsed.records.map((record) => [record.record_order, record]));
  const overlayCsv = ["labsolutions_sample_name,labsolutions_sample_id,qbench_test_display_id"].concat(overlayRows.map((row, index) => {
    const source = byRecordOrder.get(row.record_order).sample_information;
    return [source["Sample Name"], source["Sample ID"], `SYNTHETIC-QB-${index + 1}`].map(quoteCsv).join(",");
  })).join("\n");
  const overlay = adapter.normalizeRecords(parsed, config, { source_file_sha256: sourceHash, runtime_mapping: adapter.parseRuntimeMappingCsv(overlayCsv) });
  assert(overlay.rows.filter((row) => row.linkage_status === "mapped_overlay").length === 2, "TWO_RECORD_OVERLAY");
  const concentrationValues = parsed.records.flatMap((record) => record.compound_results.map((row) => row["Conc."]));
  const peakCounts = countBy(parsed.records, (record) => String(record.counts.peak_table_row_count));
  return {
    source_sha256: sourceHash,
    parser_entrypoint: "src/terpenes_multirecord_batch_cli.js",
    parser_core_version: core.VERSION,
    adapter_version: adapter.VERSION,
    records: normalized.rows.length,
    category_counts: categoryCounts,
    required_section_presence: {
      sample_information: parsed.records.filter((record) => Object.keys(record.sample_information).length > 0).length,
      original_files: parsed.records.filter((record) => Object.keys(record.original_files).length > 0).length,
      peak_table: parsed.records.filter((record) => record.peak_table.length >= 0).length,
      compound_results_24: parsed.records.filter((record) => record.compound_results.length === 24).length,
    },
    peak_table_row_count_distribution: peakCounts,
    batch_output: {
      total_columns: normalized.batch_headers.length,
      written_columns_per_row: normalized.rows[0].write_cells.length,
      write_ranges: ["A:AE", "AH:BE"],
      formula_owned_columns_excluded: ["AF", "AG"],
      reportable_channel_labels: normalized.batch_headers.slice(33, 56),
      dimethylacetamide_destination: "AA",
    },
    source_quantitation: { table: "Compound Results(Ch1)", field: "Conc." },
    peak_table_audit: {
      preserved_record_count: parsed.records.filter((record) => record.peak_table.length >= 0).length,
      unknown_peak_total: normalized.rows.reduce((total, row) => total + row.batch_row[27], 0),
      manual_integration_record_count: normalized.rows.filter((row) => row.batch_row[28] === "Yes").length,
    },
    concentration_type_observations: {
      numeric_zero: concentrationValues.filter((value) => value === 0).length,
      numeric_negative: concentrationValues.filter((value) => typeof value === "number" && value < 0).length,
      blank: concentrationValues.filter((value) => value === "").length,
    },
    linkage: {
      unmapped_reportable_held: reportableRows.length,
      controls_excluded: controls.length,
      synthetic_overlay_resolved: 2,
    },
    deterministic: true,
    no_pass_fail_result_created: true,
  };
}

if (require.main === module) {
  try { process.stdout.write(`${JSON.stringify(run(process.argv[2]), null, 2)}\n`); }
  catch (error) { process.stderr.write(`${error.code || "VALIDATION_ERROR"}: ${error.message}\n`); process.exitCode = 1; }
}

module.exports = { run };
