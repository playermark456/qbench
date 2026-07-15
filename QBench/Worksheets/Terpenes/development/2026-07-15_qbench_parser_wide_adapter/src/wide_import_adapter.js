"use strict";

const crypto = require("crypto");
const path = require("path");
const {
  orderedReportableChannels,
  parseLabSolutionsAscii,
  sha256Hex,
  normalizeSecurityLimits,
} = require("./labsolutions_ascii_core");

const WIDE_ADAPTER_VERSION = "terpenes-wide-import-adapter-v1";

const INSTRUMENT_IMPORT_COLUMNS = [
  ["A", "import_row_id", "import_row_id"],
  ["B", "run_order", "run_order"],
  ["C", "vial", "vial"],
  ["D", "sample_type", "sample_type"],
  ["E", "qbench_test_id", "qbench_test_id"],
  ["F", "qbench_sample_id", "qbench_sample_id"],
  ["G", "product_matrix", "product_matrix"],
  ["H", "sample_mass_g", "sample_mass_g"],
  ["I", "final_volume_ml", "final_volume_ml"],
  ["J", "qbench_df", "qbench_df"],
  ["K", "df_application_mode", "df_application_mode"],
  ["L", "labsolutions_sample_amount", "labsolutions_sample_amount"],
  ["M", "labsolutions_dilution_factor", "labsolutions_dilution_factor"],
  ["N", "source_instrument_file", "source_instrument_file"],
  ["O", "source_file_hash", "source_file_hash"],
  ["P", "source_data_file", "source_data_file"],
  ["Q", "source_method_file", "source_method_file"],
  ["R", "source_sequence_file", "source_sequence_file"],
  ["S", "acquired_at", "acquired_at"],
  ["T", "instrument_name", "instrument_name"],
  ["U", "detector_id", "detector_id"],
  ["V", "detector_name", "detector_name"],
  ["W", "parser_version", "parser_version"],
  ["X", "compound_result_row_count", "compound_result_row_count"],
  ["Y", "peak_table_row_count", "peak_table_row_count"],
  ["Z", "reportable_compound_row_count", "reportable_compound_row_count"],
  ["AA", "dimethylacetamide_conc", "dimethylacetamide_conc"],
  ["AB", "unknown_peak_count", "unknown_peak_count"],
  ["AC", "manual_integration", "manual_integration"],
  ["AD", "integration_reason", "integration_reason"],
  ["AE", "integration_review_status", "integration_review_status"],
  ["AF", "worksheet-owned Import Validation Status formula", "import_validation_status_formula"],
  ["AG", "worksheet-owned Import Message formula", "import_message_formula"],
  ["AH", "apinene", "apinene"],
  ["AI", "camphene", "camphene"],
  ["AJ", "bmyrcene", "bmyrcene"],
  ["AK", "bpinene", "bpinene"],
  ["AL", "delta3carene", "delta3carene"],
  ["AM", "aterpinene", "aterpinene"],
  ["AN", "cisocimene", "cisocimene"],
  ["AO", "dlimonene", "dlimonene"],
  ["AP", "pcymene", "pcymene"],
  ["AQ", "transocimene", "transocimene"],
  ["AR", "eucalyptol", "eucalyptol"],
  ["AS", "gterpinene", "gterpinene"],
  ["AT", "terpinolene", "terpinolene"],
  ["AU", "linalool", "linalool"],
  ["AV", "isopulegol", "isopulegol"],
  ["AW", "geraniol", "geraniol"],
  ["AX", "bcaryophyllene", "bcaryophyllene"],
  ["AY", "ahumulene", "ahumulene"],
  ["AZ", "cisnerolidol", "cisnerolidol"],
  ["BA", "transnerolidol", "transnerolidol"],
  ["BB", "guaiol", "guaiol"],
  ["BC", "caryophylleneoxide", "caryophylleneoxide"],
  ["BD", "bisabolol", "bisabolol"],
  ["BE", "source_row_hash", "source_row_hash"],
];

const DEFAULT_CONTEXT = Object.freeze({
  qbench_test_id: "",
  qbench_sample_id: "",
  product_matrix: "",
  sample_type: "",
  sample_mass_g: "",
  final_volume_ml: "",
  qbench_df: "",
  df_application_mode: "",
  labsolutions_conc_unit: "ug/mL",
  unit_confirmed: false,
  preparation_values_confirmed: false,
  source_batch_id: "",
  manual_integration: "",
  integration_reason: "",
  integration_review_status: "Not Reviewed",
  imported_at: "",
  run_order: "",
});

function typeOfCell(value) {
  if (value === "") return "blank";
  if (Array.isArray(value)) return "array";
  return typeof value;
}

function stableStringify(value) {
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

function hashCanonical(value) {
  return crypto.createHash("sha256").update(stableStringify(value), "utf8").digest("hex");
}

function normalizeContext(context = {}) {
  return { ...DEFAULT_CONTEXT, ...(context || {}) };
}

function basenameOnly(filename) {
  if (!filename) return "";
  return path.basename(String(filename).replace(/\\/g, "/"));
}

function adapterError(code, message, details = {}) {
  const error = new Error(message);
  error.code = code;
  error.details = details;
  return error;
}

function explicitSourceFilename(fileInput) {
  if (!fileInput || typeof fileInput !== "object") {
    throw adapterError("SOURCE_FILENAME_REQUIRED", "Source filename or name is required.");
  }
  const filename = fileInput.filename ?? fileInput.name;
  if (filename === undefined || filename === null || String(filename).trim() === "") {
    throw adapterError("SOURCE_FILENAME_REQUIRED", "Source filename or name is required.");
  }
  return String(filename);
}

function analyteValueMap(parsed) {
  const values = {};
  for (const row of parsed.reportable_analytes || []) {
    if (typeof row.conc !== "number") {
      throw new Error(`Reportable analyte ${row.internal_key} Conc. is not a JavaScript number.`);
    }
    values[row.internal_key] = row.conc;
  }
  return values;
}

function sourceRowHashPayload(parsed, sourceFileHash) {
  const sample = parsed.source_metadata.sample_information || {};
  const original = parsed.source_metadata.original_files || {};
  const configuration = parsed.source_metadata.configuration || {};
  return {
    source_file_hash: sourceFileHash,
    labsolutions_sample_name: sample["Sample Name"] || "",
    labsolutions_sample_id: sample["Sample ID"] || "",
    acquired_at: sample.Acquired || "",
    vial: sample["Vial#"] ?? "",
    source_data_file: original["Data File"] || "",
    source_method_file: original["Method File"] || "",
    source_sequence_file: original["Batch File"] || "",
    instrument_name: configuration["Instrument Name"] || "",
    detector_id: configuration["Detector ID"] || "",
    ordered_analyte_values: (parsed.reportable_analytes || []).map((row) => [row.internal_key, row.conc]),
    dimethylacetamide_conc: parsed.dimethylacetamide_audit.conc,
    compound_result_row_count: parsed.counts.compound_result_row_count,
    peak_table_row_count: parsed.counts.peak_table_row_count,
  };
}

function assignmentHashPayload(sourceRowHash, context) {
  if (!context.qbench_test_id) return null;
  return {
    source_row_hash: sourceRowHash,
    qbench_test_id: context.qbench_test_id,
  };
}

function buildWideImportRow(parsed, config, contextInput = {}, source = {}) {
  const context = normalizeContext(contextInput);
  const sample = parsed.source_metadata.sample_information || {};
  const original = parsed.source_metadata.original_files || {};
  const configuration = parsed.source_metadata.configuration || {};
  const sourceBytes = source.rawBytes || source.rawText || "";
  const sourceFileHash = source.source_file_hash || parsed.source_provenance.source_file_hash || sha256Hex(sourceBytes);
  const valuesByAnalyte = analyteValueMap(parsed);
  const rowHash = hashCanonical(sourceRowHashPayload(parsed, sourceFileHash));
  const assignmentPayload = assignmentHashPayload(rowHash, context);
  const importRowId = `inj-${rowHash.slice(0, 16)}`;
  const values = {
    import_row_id: importRowId,
    run_order: context.run_order,
    vial: sample["Vial#"] ?? "",
    sample_type: context.sample_type,
    qbench_test_id: context.qbench_test_id,
    qbench_sample_id: context.qbench_sample_id,
    product_matrix: context.product_matrix,
    sample_mass_g: context.sample_mass_g,
    final_volume_ml: context.final_volume_ml,
    qbench_df: context.qbench_df,
    df_application_mode: context.df_application_mode,
    labsolutions_sample_amount: sample["Sample Amount"] ?? "",
    labsolutions_dilution_factor: sample["Dilution Factor"] ?? "",
    source_instrument_file: basenameOnly(source.source_instrument_file || source.filename || ""),
    source_file_hash: sourceFileHash,
    source_data_file: original["Data File"] || "",
    source_method_file: original["Method File"] || "",
    source_sequence_file: original["Batch File"] || "",
    acquired_at: sample.Acquired || "",
    instrument_name: configuration["Instrument Name"] || "",
    detector_id: configuration["Detector ID"] || "",
    detector_name: configuration["Detector Name"] || "",
    parser_version: WIDE_ADAPTER_VERSION,
    compound_result_row_count: parsed.counts.compound_result_row_count,
    peak_table_row_count: parsed.counts.peak_table_row_count,
    reportable_compound_row_count: parsed.counts.reportable_compound_row_count,
    dimethylacetamide_conc: parsed.dimethylacetamide_audit.conc,
    unknown_peak_count: parsed.counts.unknown_peak_count,
    manual_integration: context.manual_integration,
    integration_reason: context.integration_reason,
    integration_review_status: context.integration_review_status,
    import_validation_status_formula: "",
    import_message_formula: "",
    source_row_hash: rowHash,
    assignment_hash: assignmentPayload ? hashCanonical(assignmentPayload) : "",
  };
  for (const channel of orderedReportableChannels(config)) {
    values[channel.internal_key] = valuesByAnalyte[channel.internal_key];
  }

  const columns = INSTRUMENT_IMPORT_COLUMNS.map(([letter, header, key]) => ({
    column: letter,
    header,
    key,
    value: values[key] ?? "",
    js_type: typeOfCell(values[key] ?? ""),
  }));
  return {
    schema_version: 1,
    adapter_version: WIDE_ADAPTER_VERSION,
    worksheet: "Instrument Import",
    logical_range: "A:BE",
    formula_owned_excluded_columns: ["AF", "AG"],
    context,
    columns,
    values,
    write_plan: buildInstrumentImportWritePlan(columns),
  };
}

function valuesForRange(columns, start, end) {
  const startIndex = columns.findIndex((col) => col.column === start);
  const endIndex = columns.findIndex((col) => col.column === end);
  return columns.slice(startIndex, endIndex + 1).map((col) => col.value);
}

function buildInstrumentImportWritePlan(columns, rowNumber = 2) {
  const leadingColumns = columns.slice(0, columns.findIndex((col) => col.column === "AF"));
  const analyteBlockColumns = columns.slice(columns.findIndex((col) => col.column === "AH"));
  return {
    target_worksheet: "Instrument Import",
    qbench_neutral: true,
    excludes_formula_owned_columns: ["AF", "AG"],
    blocks: [
      {
        label: "Instrument Import A:AE",
        range: `Instrument Import!A${rowNumber}:AE${rowNumber}`,
        columns: leadingColumns.map((col) => col.column),
        values: leadingColumns.map((col) => col.value),
      },
      {
        label: "Instrument Import AH:BE",
        range: `Instrument Import!AH${rowNumber}:BE${rowNumber}`,
        columns: analyteBlockColumns.map((col) => col.column),
        values: analyteBlockColumns.map((col) => col.value),
      },
    ],
  };
}

function tsvEscape(value) {
  if (value === null || value === undefined) return "";
  return String(value).replace(/\t/g, " ").replace(/\r?\n/g, " ");
}

function rowToTsv(columns) {
  const header = columns.map((col) => col.header).join("\t");
  const row = columns.map((col) => tsvEscape(col.value)).join("\t");
  return `${header}\n${row}\n`;
}

function blockToTsv(columns, start, end) {
  const startIndex = columns.findIndex((col) => col.column === start);
  const endIndex = columns.findIndex((col) => col.column === end);
  return rowToTsv(columns.slice(startIndex, endIndex + 1));
}

function sortWideRows(rows) {
  return [...rows].sort((a, b) => {
    const av = a.values;
    const bv = b.values;
    return String(av.run_order).localeCompare(String(bv.run_order), undefined, { numeric: true })
      || String(av.source_instrument_file).localeCompare(String(bv.source_instrument_file))
      || String(av.source_row_hash).localeCompare(String(bv.source_row_hash));
  });
}

function summarizeWideRowSet(rows) {
  const seenRows = new Set();
  const fileHashes = new Map();
  const duplicateFileHashes = [];
  const errors = [];
  for (const row of rows) {
    const rowHash = row.values.source_row_hash;
    if (seenRows.has(rowHash)) errors.push(`Duplicate source_row_hash rejected: ${rowHash}`);
    seenRows.add(rowHash);
    const fileHash = row.values.source_file_hash;
    if (fileHashes.has(fileHash) && !duplicateFileHashes.includes(fileHash)) duplicateFileHashes.push(fileHash);
    fileHashes.set(fileHash, true);
  }
  return { ok: errors.length === 0, errors, duplicate_file_hashes: duplicateFileHashes };
}

function validateWideRowSet(rows) {
  const summary = summarizeWideRowSet(rows);
  if (!summary.ok) {
    const error = new Error(summary.errors.join(" | "));
    error.code = "DUPLICATE_SOURCE_ROW_HASH";
    error.duplicate_file_hashes = summary.duplicate_file_hashes;
    throw error;
  }
  return { duplicate_file_hashes: summary.duplicate_file_hashes };
}

function publishSelectionStatus(rows) {
  const reviewedByTest = new Map();
  for (const row of rows) {
    if (!row.values.qbench_test_id) continue;
    if (row.values.integration_review_status !== "Reviewed") continue;
    const key = row.values.qbench_test_id;
    reviewedByTest.set(key, (reviewedByTest.get(key) || 0) + 1);
  }
  return Array.from(reviewedByTest.values()).some((count) => count > 1) ? "decision_required" : "single_or_none";
}

function rawBytesFromInput(fileInput) {
  if (Buffer.isBuffer(fileInput.rawBytes)) return Buffer.from(fileInput.rawBytes);
  if (fileInput.rawBytes instanceof Uint8Array) return Buffer.from(fileInput.rawBytes);
  if (typeof fileInput.rawText === "string") return Buffer.from(fileInput.rawText, "utf8");
  if (typeof fileInput.text === "string") return Buffer.from(fileInput.text, "utf8");
  if (typeof fileInput.content === "string") return Buffer.from(fileInput.content, "utf8");
  if (Buffer.isBuffer(fileInput.content)) return Buffer.from(fileInput.content);
  if (fileInput.content instanceof Uint8Array) return Buffer.from(fileInput.content);
  throw new Error("File input must include rawBytes, rawText, text, or content.");
}

function contextForFile(contexts, fileInput, index) {
  if (Array.isArray(contexts)) return contexts[index] || {};
  if (contexts && typeof contexts === "object") {
    const name = fileInput.filename || fileInput.name || String(index);
    return contexts[name] || contexts[index] || {};
  }
  return {};
}

function buildWideImportRows(fileInputs, config, contexts = {}, securityLimits = {}) {
  const limits = normalizeSecurityLimits(securityLimits);
  if (!Array.isArray(fileInputs)) {
    throw new Error("fileInputs must be an array.");
  }
  if (fileInputs.length > limits.max_files_per_run) {
    throw new Error(`File count ${fileInputs.length} exceeds maximum_files_per_run ${limits.max_files_per_run}.`);
  }
  const rows = [];
  for (let index = 0; index < fileInputs.length; index += 1) {
    const fileInput = fileInputs[index] || {};
    const filename = explicitSourceFilename(fileInput);
    if (path.extname(String(filename)).toLowerCase() !== ".txt") {
      throw adapterError("UNSUPPORTED_SOURCE_EXTENSION", `Unsupported file extension for ${filename}; only .txt is allowed.`, {
        filename,
      });
    }
    const rawBytes = rawBytesFromInput(fileInput);
    if (rawBytes.length > limits.max_raw_file_size_bytes) {
      throw new Error(`File ${filename} exceeds maximum raw file size.`);
    }
    const parsed = parseLabSolutionsAscii(rawBytes, config, { securityLimits: limits });
    rows.push(buildWideImportRow(parsed, config, contextForFile(contexts, fileInput, index), {
      rawBytes,
      filename,
      source_instrument_file: filename,
    }));
  }
  const duplicateFileSummary = summarizeWideRowSet(rows);
  const sortedRows = sortWideRows(rows);
  if (!duplicateFileSummary.ok) {
    return {
      schema_version: 1,
      adapter_version: WIDE_ADAPTER_VERSION,
      status: "blocked",
      errors: duplicateFileSummary.errors,
      rows: [],
      duplicate_file_hashes: duplicateFileSummary.duplicate_file_hashes,
      publish_selection_status: "blocked_duplicate_source_row",
    };
  }
  return {
    schema_version: 1,
    adapter_version: WIDE_ADAPTER_VERSION,
    status: "ok",
    rows: sortedRows,
    duplicate_file_hashes: duplicateFileSummary.duplicate_file_hashes,
    publish_selection_status: publishSelectionStatus(sortedRows),
  };
}

module.exports = {
  WIDE_ADAPTER_VERSION,
  INSTRUMENT_IMPORT_COLUMNS,
  DEFAULT_CONTEXT,
  stableStringify,
  hashCanonical,
  normalizeContext,
  buildWideImportRow,
  sourceRowHashPayload,
  assignmentHashPayload,
  explicitSourceFilename,
  buildInstrumentImportWritePlan,
  rowToTsv,
  blockToTsv,
  sortWideRows,
  summarizeWideRowSet,
  validateWideRowSet,
  publishSelectionStatus,
  buildWideImportRows,
};
