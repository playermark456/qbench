"use strict";

const { INSTRUMENT_IMPORT_COLUMNS } = require("./wide_import_adapter");

const REVIEWED_PUBLISH_ADAPTER_VERSION = "terpenes-reviewed-publish-adapter-v1";

const ANALYTE_KEYS = INSTRUMENT_IMPORT_COLUMNS
  .filter((col) => col[0] >= "AH" && col[0] <= "BD")
  .map((col) => col[2]);

const PUBLISH_COLUMNS = [
  ["D", "apinene"],
  ["E", "camphene"],
  ["F", "bmyrcene"],
  ["G", "bpinene"],
  ["H", "delta3carene"],
  ["I", "aterpinene"],
  ["J", "cisocimene"],
  ["K", "dlimonene"],
  ["L", "pcymene"],
  ["M", "transocimene"],
  ["N", "eucalyptol"],
  ["O", "gterpinene"],
  ["P", "terpinolene"],
  ["Q", "linalool"],
  ["R", "isopulegol"],
  ["S", "geraniol"],
  ["T", "bcaryophyllene"],
  ["U", "ahumulene"],
  ["V", "cisnerolidol"],
  ["W", "transnerolidol"],
  ["X", "guaiol"],
  ["Y", "caryophylleneoxide"],
  ["Z", "bisabolol"],
  ["AA", "sample_mass_g"],
  ["AB", "final_volume_ml"],
  ["AC", "qbench_df"],
  ["AD", "df_application_mode"],
  ["AE", "labsolutions_conc_unit"],
  ["AF", "unit_confirmed"],
  ["AG", "preparation_values_confirmed"],
  ["AH", "source_batch_id"],
  ["AI", "source_instrument_file"],
  ["AJ", "source_file_hash"],
  ["AK", "source_data_file"],
  ["AL", "source_method_file"],
  ["AM", "source_sequence_file"],
  ["AN", "parser_version"],
  ["AO", "imported_at"],
  ["AP", "instrument_name"],
  ["AQ", "detector_id"],
  ["AR", "detector_name"],
  ["AS", "import_row_id"],
  ["AT", "source_row_hash"],
  ["AU", "dimethylacetamide_conc"],
  ["AV", "compound_results_complete"],
  ["AW", "integration_review_status"],
  ["AX", "import_validation_status"],
];

function asValues(row) {
  if (row && row.values) return { ...row.context, ...row.values };
  return { ...(row || {}) };
}

function isTrue(value) {
  return value === true || value === "TRUE";
}

function isPositiveNumber(value) {
  return typeof value === "number" && Number.isFinite(value) && value > 0;
}

function isNumber(value) {
  return typeof value === "number" && Number.isFinite(value);
}

function validateReviewedRow(rowInput, options = {}) {
  const row = asValues(rowInput);
  const errors = [];
  if (!row.qbench_test_id) errors.push("QBench Test ID is required.");
  if (!options.explicitly_selected) errors.push("Explicit reviewer selection is required.");
  for (const key of ANALYTE_KEYS) {
    if (!isNumber(row[key])) errors.push(`Analyte ${key} must be a JavaScript Number.`);
  }
  if (!isPositiveNumber(row.sample_mass_g)) errors.push("Sample mass must be a positive number.");
  if (!isPositiveNumber(row.final_volume_ml)) errors.push("Final volume must be a positive number.");
  if (!["already_applied_by_labsolutions", "apply_in_qbench"].includes(row.df_application_mode)) {
    errors.push("DF application mode is invalid.");
  }
  if (row.df_application_mode === "apply_in_qbench" && !isPositiveNumber(row.qbench_df)) {
    errors.push("DF must be a positive number when apply_in_qbench is selected.");
  }
  if (!isTrue(row.unit_confirmed)) errors.push("Unit confirmation must be TRUE.");
  if (!isTrue(row.preparation_values_confirmed)) errors.push("Preparation values confirmation must be TRUE.");
  if (!isNumber(row.dimethylacetamide_conc)) errors.push("Dimethylacetamide must be numeric.");
  if (row.compound_result_row_count !== 24 || row.reportable_compound_row_count !== 23) {
    errors.push("Compound Results validation is incomplete.");
  }
  if (row.integration_review_status !== "Reviewed") errors.push("Integration Review Status must be Reviewed.");
  if (options.import_validation_status !== "Valid") errors.push("Import Validation Status must be Valid.");
  if (!row.source_row_hash) errors.push("Source Row Hash is required.");
  if (!options.source_batch_id && !row.source_batch_id) errors.push("Source Batch ID is required.");
  return { ok: errors.length === 0, errors, row };
}

function buildReviewedPublishPatch(rowInput, options = {}) {
  const validation = validateReviewedRow(rowInput, options);
  if (!validation.ok) {
    return {
      schema_version: 1,
      adapter_version: REVIEWED_PUBLISH_ADAPTER_VERSION,
      status: "blocked",
      errors: validation.errors,
      writes: [],
    };
  }
  const row = {
    ...validation.row,
    source_batch_id: options.source_batch_id || validation.row.source_batch_id,
    labsolutions_conc_unit: validation.row.labsolutions_conc_unit || "ug/mL",
    compound_results_complete: true,
    import_validation_status: options.import_validation_status,
  };
  const targetRow = options.target_row || 2;
  const columns = PUBLISH_COLUMNS.map(([column, key]) => ({
    column,
    key,
    value: row[key] ?? "",
    js_type: row[key] === "" || row[key] === undefined ? "blank" : typeof row[key],
  }));
  return {
    schema_version: 1,
    adapter_version: REVIEWED_PUBLISH_ADAPTER_VERSION,
    status: "ok",
    qbench_test_id: row.qbench_test_id,
    target_worksheet: "Publish",
    range: `Publish!D${targetRow}:AX${targetRow}`,
    excluded_formula_columns: ["AY", "AZ", "BA", "BB", "BC", "BD"],
    writes: [
      {
        range: `Publish!D${targetRow}:AX${targetRow}`,
        columns: columns.map((col) => col.column),
        values: columns.map((col) => col.value),
      },
    ],
    columns,
  };
}

function buildPublishPatches(rows, selections, options = {}) {
  const selected = rows.filter((row) => selections.includes(asValues(row).source_row_hash));
  const byTest = new Map();
  for (const row of selected) {
    const testId = asValues(row).qbench_test_id;
    byTest.set(testId, (byTest.get(testId) || 0) + 1);
  }
  const duplicated = Array.from(byTest.entries()).filter(([, count]) => count > 1).map(([testId]) => testId);
  if (duplicated.length) {
    return {
      schema_version: 1,
      adapter_version: REVIEWED_PUBLISH_ADAPTER_VERSION,
      status: "blocked",
      errors: [`Multiple selected rows for one Test ID rejected: ${duplicated.join(", ")}`],
      patches: [],
    };
  }
  return {
    schema_version: 1,
    adapter_version: REVIEWED_PUBLISH_ADAPTER_VERSION,
    status: "ok",
    patches: selected.map((row, index) => buildReviewedPublishPatch(row, {
      ...options,
      explicitly_selected: true,
      target_row: (options.start_row || 2) + index,
    })),
  };
}

module.exports = {
  REVIEWED_PUBLISH_ADAPTER_VERSION,
  ANALYTE_KEYS,
  PUBLISH_COLUMNS,
  validateReviewedRow,
  buildReviewedPublishPatch,
  buildPublishPatches,
};
