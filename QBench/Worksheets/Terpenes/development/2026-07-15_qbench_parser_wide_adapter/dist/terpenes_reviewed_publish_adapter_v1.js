"use strict";

const { INSTRUMENT_IMPORT_COLUMNS } = require("./wide_import_adapter");

const REVIEWED_PUBLISH_ADAPTER_VERSION = "terpenes-reviewed-publish-adapter-v1";
const REQUIRED_LABSOLUTIONS_CONC_UNIT = "ug/mL";
const DEFAULT_PUBLISH_ROW_MIN = 2;
const DEFAULT_PUBLISH_ROW_MAX = 87;

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

function blocked(errors, extra = {}) {
  return {
    schema_version: 1,
    adapter_version: REVIEWED_PUBLISH_ADAPTER_VERSION,
    status: "blocked",
    errors,
    patches: [],
    writes: [],
    ...extra,
  };
}

function normalizeSelectedHashes(selections) {
  const selected = selections instanceof Set ? Array.from(selections) : [...(selections || [])];
  const seen = new Set();
  const duplicates = [];
  for (const hash of selected) {
    if (seen.has(hash)) duplicates.push(hash);
    seen.add(hash);
  }
  return { selected, selected_set: seen, duplicate_selected_hashes: duplicates };
}

function evidenceHash(evidence) {
  return evidence && (evidence.source_row_hash || evidence.hash);
}

function normalizeReviewEvidence(reviewEvidence = []) {
  const evidence = reviewEvidence || [];
  const entries = [];
  if (Array.isArray(evidence)) {
    for (const item of evidence) entries.push(item || {});
  } else if (evidence instanceof Map) {
    for (const [sourceRowHash, value] of evidence.entries()) entries.push({ source_row_hash: sourceRowHash, ...(value || {}) });
  } else if (typeof evidence === "object") {
    if (evidence.source_row_hash || evidence.import_validation_status || evidence.import_message || evidence.explicitly_selected !== undefined) {
      entries.push(evidence);
    } else {
      for (const [sourceRowHash, value] of Object.entries(evidence)) {
        entries.push({ source_row_hash: sourceRowHash, ...(value || {}) });
      }
    }
  }

  const byHash = new Map();
  const duplicateHashes = [];
  for (const entry of entries) {
    const hash = evidenceHash(entry);
    if (!hash) {
      duplicateHashes.push("<blank>");
      continue;
    }
    if (byHash.has(hash)) duplicateHashes.push(hash);
    byHash.set(hash, { ...entry, source_row_hash: hash });
  }
  return { by_hash: byHash, duplicate_hashes: duplicateHashes, entries };
}

function reviewEvidenceErrors(row, evidence) {
  const errors = [];
  if (!evidence) {
    errors.push(`Missing review evidence for source_row_hash ${row.source_row_hash}.`);
    return errors;
  }
  if (evidence.explicitly_selected !== true) {
    errors.push(`Review evidence for ${row.source_row_hash} must have explicitly_selected = true.`);
  }
  if (evidence.import_validation_status !== "Valid") {
    errors.push(`Review evidence for ${row.source_row_hash} must have import_validation_status = Valid.`);
  }
  if (evidence.import_message !== "Import row valid") {
    errors.push(`Review evidence for ${row.source_row_hash} must have import_message = Import row valid.`);
  }
  return errors;
}

function validateReviewedRow(rowInput, options = {}) {
  const row = asValues(rowInput);
  const errors = [];
  const evidence = options.review_evidence;
  if (!row.qbench_test_id) errors.push("QBench Test ID is required.");
  if (!row.source_row_hash) errors.push("Source Row Hash is required.");
  if (evidence) errors.push(...reviewEvidenceErrors(row, evidence));
  if (!evidence) errors.push(`Review evidence keyed by source_row_hash is required for ${row.source_row_hash || "<blank>"}.`);
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
  if (row.labsolutions_conc_unit !== REQUIRED_LABSOLUTIONS_CONC_UNIT) {
    errors.push(`LabSolutions concentration unit must be exactly ${REQUIRED_LABSOLUTIONS_CONC_UNIT}.`);
  }
  if (!isTrue(row.unit_confirmed)) errors.push("Unit confirmation must be TRUE.");
  if (!isTrue(row.preparation_values_confirmed)) errors.push("Preparation values confirmation must be TRUE.");
  if (!isNumber(row.dimethylacetamide_conc)) errors.push("Dimethylacetamide must be numeric.");
  if (row.compound_result_row_count !== 24 || row.reportable_compound_row_count !== 23) {
    errors.push("Compound Results validation is incomplete.");
  }
  if (row.integration_review_status !== "Reviewed") errors.push("Integration Review Status must be Reviewed.");
  if (!options.source_batch_id && !row.source_batch_id) errors.push("Source Batch ID is required.");
  return { ok: errors.length === 0, errors, row };
}

function buildReviewedPublishPatch(rowInput, options = {}) {
  const validation = validateReviewedRow(rowInput, options);
  if (!validation.ok) return blocked(validation.errors);

  const row = {
    ...validation.row,
    source_batch_id: options.source_batch_id || validation.row.source_batch_id,
    compound_results_complete: true,
    import_validation_status: "Valid",
  };
  const targetRow = options.target_row;
  const range = targetRow ? `Publish!D${targetRow}:AX${targetRow}` : null;
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
    expected_qbench_test_id: row.qbench_test_id,
    qbench_test_id: row.qbench_test_id,
    target_worksheet: "Publish",
    target_publish_row: targetRow || null,
    range,
    source_row_hash: row.source_row_hash,
    excluded_formula_columns: ["AY", "AZ", "BA", "BB", "BC", "BD"],
    writes: range ? [
      {
        range,
        expected_qbench_test_id: row.qbench_test_id,
        target_publish_row: targetRow,
        source_row_hash: row.source_row_hash,
        columns: columns.map((col) => col.column),
        values: columns.map((col) => col.value),
      },
    ] : [],
    columns,
  };
}

function buildTestIdPreview(rows) {
  return rows.map((rowInput) => {
    const row = asValues(rowInput);
    return {
      qbench_test_id: row.qbench_test_id,
      source_row_hash: row.source_row_hash,
      target_publish_row: null,
      range: null,
    };
  });
}

function buildPublishPatches(rowsInput, selections, options = {}) {
  const rows = [...(rowsInput || [])];
  const rowValues = rows.map(asValues);
  const errors = [];
  const { selected, selected_set: selectedSet, duplicate_selected_hashes: duplicateSelectedHashes } = normalizeSelectedHashes(selections);
  const evidence = normalizeReviewEvidence(options.review_evidence || options.reviewEvidence);
  const rowByHash = new Map();
  const selectedRows = [];
  const selectedHashCounts = new Map();
  const selectedByTestId = new Map();

  if (duplicateSelectedHashes.length) {
    errors.push(`Duplicate selected source_row_hash rejected: ${duplicateSelectedHashes.join(", ")}`);
  }
  if (evidence.duplicate_hashes.length) {
    errors.push(`Duplicate review evidence rejected: ${evidence.duplicate_hashes.join(", ")}`);
  }

  for (const row of rowValues) {
    if (row.source_row_hash) {
      if (rowByHash.has(row.source_row_hash)) errors.push(`Duplicate row source_row_hash rejected: ${row.source_row_hash}`);
      rowByHash.set(row.source_row_hash, row);
    }
  }

  for (const hash of evidence.by_hash.keys()) {
    if (!rowByHash.has(hash)) errors.push(`Review evidence for unknown source_row_hash rejected: ${hash}`);
  }

  for (const hash of selected) {
    const row = rowByHash.get(hash);
    if (!row) {
      errors.push(`Selected source_row_hash has no matching row: ${hash}`);
      continue;
    }
    selectedRows.push(row);
    selectedHashCounts.set(hash, (selectedHashCounts.get(hash) || 0) + 1);
  }

  for (const row of rowValues) {
    if (!selectedSet.has(row.source_row_hash)) {
      errors.push(`Row source_row_hash is missing from selected hashes: ${row.source_row_hash || "<blank>"}`);
    }
  }

  for (const row of selectedRows) {
    const evidenceForRow = evidence.by_hash.get(row.source_row_hash);
    errors.push(...reviewEvidenceErrors(row, evidenceForRow));
    const validation = validateReviewedRow(row, {
      review_evidence: evidenceForRow,
      source_batch_id: options.source_batch_id,
    });
    errors.push(...validation.errors);
    if (!row.qbench_test_id) continue;
    selectedByTestId.set(row.qbench_test_id, (selectedByTestId.get(row.qbench_test_id) || 0) + 1);
  }

  const duplicateTestIds = Array.from(selectedByTestId.entries()).filter(([, count]) => count > 1).map(([testId]) => testId);
  if (duplicateTestIds.length) {
    errors.push(`Multiple selected rows for one Test ID rejected: ${duplicateTestIds.join(", ")}`);
  }

  const mapping = options.publish_row_mapping || options.publishRowMapping || null;
  const allowPreview = options.allow_test_id_preview_without_range === true || options.allow_unmapped_preview === true;
  const minRow = options.publish_row_min || DEFAULT_PUBLISH_ROW_MIN;
  const maxRow = options.publish_row_max || DEFAULT_PUBLISH_ROW_MAX;

  if (!mapping && !allowPreview) {
    errors.push("Explicit QBench Test ID to Publish row mapping is required.");
  }

  if (mapping) {
    const selectedTestIds = new Set(selectedRows.map((row) => row.qbench_test_id).filter(Boolean));
    const mappedRows = new Map();
    for (const [testId, targetRow] of Object.entries(mapping)) {
      if (!selectedTestIds.has(testId)) {
        errors.push(`Publish row mapping for wrong or unselected Test ID rejected: ${testId}`);
        continue;
      }
      if (!Number.isInteger(targetRow)) {
        errors.push(`Publish row mapping for ${testId} must be an integer row number.`);
        continue;
      }
      if (targetRow < minRow || targetRow > maxRow) {
        errors.push(`Publish row mapping for ${testId} is out of range ${minRow}:${maxRow}.`);
      }
      if (mappedRows.has(targetRow)) {
        errors.push(`Duplicate Publish destination row rejected: ${targetRow}`);
      }
      mappedRows.set(targetRow, testId);
    }
    for (const row of selectedRows) {
      if (!Object.prototype.hasOwnProperty.call(mapping, row.qbench_test_id)) {
        errors.push(`Missing Publish row mapping for QBench Test ID ${row.qbench_test_id}.`);
      }
    }
    const rowsBySelectedHash = new Map();
    for (const row of selectedRows) {
      const existing = rowsBySelectedHash.get(row.source_row_hash) || new Set();
      if (row.qbench_test_id && mapping[row.qbench_test_id] !== undefined) existing.add(mapping[row.qbench_test_id]);
      rowsBySelectedHash.set(row.source_row_hash, existing);
    }
    for (const [hash, destinations] of rowsBySelectedHash.entries()) {
      if (destinations.size > 1 || (selectedHashCounts.get(hash) || 0) > 1) {
        errors.push(`One selected source_row_hash assigned more than once: ${hash}`);
      }
    }
  }

  const uniqueErrors = Array.from(new Set(errors));
  if (uniqueErrors.length) return blocked(uniqueErrors);

  if (!mapping && allowPreview) {
    return {
      schema_version: 1,
      adapter_version: REVIEWED_PUBLISH_ADAPTER_VERSION,
      status: "preview_only",
      patches: [],
      test_id_preview: buildTestIdPreview(selectedRows),
      errors: [],
    };
  }

  return {
    schema_version: 1,
    adapter_version: REVIEWED_PUBLISH_ADAPTER_VERSION,
    status: "ok",
    patches: selectedRows.map((row) => buildReviewedPublishPatch(row, {
      review_evidence: evidence.by_hash.get(row.source_row_hash),
      source_batch_id: options.source_batch_id,
      target_row: mapping[row.qbench_test_id],
    })),
  };
}

module.exports = {
  REVIEWED_PUBLISH_ADAPTER_VERSION,
  REQUIRED_LABSOLUTIONS_CONC_UNIT,
  DEFAULT_PUBLISH_ROW_MIN,
  DEFAULT_PUBLISH_ROW_MAX,
  ANALYTE_KEYS,
  PUBLISH_COLUMNS,
  asValues,
  normalizeReviewEvidence,
  validateReviewedRow,
  buildReviewedPublishPatch,
  buildPublishPatches,
};
