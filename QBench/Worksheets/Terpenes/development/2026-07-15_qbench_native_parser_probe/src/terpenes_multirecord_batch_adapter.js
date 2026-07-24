"use strict";

(function attachTerpenesMultiRecordBatchAdapter(root) {
  const VERSION = "terpenes-multirecord-batch-adapter-v1";
  const MAPPING_HEADERS = ["labsolutions_sample_name", "labsolutions_sample_id", "qbench_test_display_id"];
  const BATCH_HEADERS = [
    "import_row_id", "run_order", "vial", "sample_type", "qbench_test_id", "qbench_sample_id",
    "product_matrix", "sample_mass_g", "final_volume_ml", "qbench_df", "df_application_mode",
    "labsolutions_sample_amount", "labsolutions_dilution_factor", "source_instrument_file", "source_file_hash",
    "source_data_file", "source_method_file", "source_sequence_file", "acquired_at", "instrument_name",
    "detector_id", "detector_name", "parser_version", "compound_result_row_count", "peak_table_row_count",
    "reportable_compound_row_count", "dimethylacetamide_conc", "unknown_peak_count", "manual_integration",
    "integration_reason", "integration_review_status", "import_validation_status", "import_message",
    "α-Pinene", "Camphene", "β-Myrcene", "(-)-β-pinene", "Delta-3-carene", "α-Terpinene", "cis-Ocimene",
    "d-Limonene", "p-Cymene", "trans-Ocimene", "Eucalyptol", "γ-Terpinene", "Terpinolene", "Linalool",
    "(-)-Isopulegol", "Geraniol", "β-Caryophyllene", "α-Humulene", "cis-Nerolidol", "trans-Nerolidol",
    "(-)-Guaiol", "Caryophyllene Oxide", "(-)-α-Bisabolol", "source_row_hash",
  ];
  const FORMULA_OWNED_HEADERS = new Set(["import_validation_status", "import_message"]);

  class BatchAdapterError extends Error {
    constructor(code, message) {
      super(message);
      this.name = "BatchAdapterError";
      this.code = code;
    }
  }

  function fail(code, message) {
    throw new BatchAdapterError(code, message);
  }

  function csvRows(input) {
    const rows = [];
    let row = [];
    let cell = "";
    let quoted = false;
    const text = String(input || "").replace(/^\ufeff/, "");
    for (let index = 0; index < text.length; index += 1) {
      const char = text[index];
      if (quoted) {
        if (char === '"' && text[index + 1] === '"') { cell += '"'; index += 1; }
        else if (char === '"') quoted = false;
        else cell += char;
      } else if (char === '"') {
        if (cell) fail("MAPPING_CSV", "Quoted CSV values must begin at the start of a field.");
        quoted = true;
      } else if (char === ",") {
        row.push(cell); cell = "";
      } else if (char === "\n") {
        row.push(cell); rows.push(row); row = []; cell = "";
      } else if (char !== "\r") cell += char;
    }
    if (quoted) fail("MAPPING_CSV", "Mapping CSV contains an unterminated quoted value.");
    if (cell || row.length) { row.push(cell); rows.push(row); }
    return rows.filter((values) => values.some((value) => String(value).trim()));
  }

  function parseRuntimeMappingCsv(input) {
    const rows = csvRows(input);
    if (!rows.length) return [];
    if (rows[0].join(",") !== MAPPING_HEADERS.join(",")) {
      fail("MAPPING_HEADERS", "Runtime mapping CSV headers must match the controlled mapping contract.");
    }
    const seen = new Set();
    return rows.slice(1).map((values, index) => {
      if (values.length !== MAPPING_HEADERS.length) fail("MAPPING_WIDTH", "Runtime mapping CSV row width is invalid.");
      const entry = Object.fromEntries(MAPPING_HEADERS.map((header, column) => [header, String(values[column]).trim()]));
      if (!entry.qbench_test_display_id || (!entry.labsolutions_sample_name && !entry.labsolutions_sample_id)) {
        fail("MAPPING_VALUE", "Runtime mapping rows require a QBench Test display ID and a LabSolutions name or ID.");
      }
      const key = `${entry.labsolutions_sample_name}\u001f${entry.labsolutions_sample_id}`;
      if (seen.has(key)) fail("MAPPING_DUPLICATE", "Runtime mapping contains a duplicate LabSolutions record selector.");
      seen.add(key);
      entry.mapping_row = index + 2;
      return entry;
    });
  }

  function classifyRecord(sampleInformation) {
    const sampleType = String(sampleInformation["Sample Type"] || "");
    const sampleName = String(sampleInformation["Sample Name"] || "");
    const sampleId = String(sampleInformation["Sample ID"] || "");
    const text = `${sampleType} ${sampleName} ${sampleId}`.toLowerCase();
    if (/system\s*suit/.test(text)) return "System Suitability";
    if (/\bccv\b/.test(text)) return "CCV";
    if (/matrix\s*blank|blank\s*matrix/.test(text)) return "Matrix Blank";
    if (/\bnull\b/.test(text)) return "Null";
    if (/\bblank\b/.test(text)) return "Blank";
    if (/\bloq\b/.test(text)) return "LOQ";
    if (/\bstandard\b/.test(text)) return "Standard";
    return "Sample";
  }

  function batchSampleType(category) {
    return {
      Blank: "Blank",
      Standard: "Calibration Standard",
      CCV: "Continuing CCV",
      LOQ: "LOQ Check",
      "System Suitability": "Other QC",
      "Matrix Blank": "Blank",
      Sample: "Unknown",
      Null: "",
    }[category];
  }

  function isValidationLabel(value) {
    return /(^|\s)(low|medium|high)(\s|$)/i.test(String(value || ""));
  }

  function findMapping(mappings, sampleName, sampleId) {
    const matches = mappings.filter((mapping) => (
      (!mapping.labsolutions_sample_name || mapping.labsolutions_sample_name === sampleName)
      && (!mapping.labsolutions_sample_id || mapping.labsolutions_sample_id === sampleId)
    ));
    if (matches.length > 1) fail("MAPPING_AMBIGUOUS", "More than one runtime mapping matches a LabSolutions record.");
    return matches[0] || null;
  }

  function directTestId(sampleName, sampleId) {
    if (!sampleId || isValidationLabel(sampleName) || isValidationLabel(sampleId)) return "";
    return sampleId;
  }

  function manualIntegration(peakRows) {
    return peakRows.some((row) => /manual/i.test(String(row.Mark || "")));
  }

  function normalizeRecords(parsed, config, options) {
    if (!parsed || !Array.isArray(parsed.records)) fail("PARSED_RECORDS", "A parsed multi-record source is required.");
    const settings = options || {};
    const sourceFileHash = String(settings.source_file_sha256 || "").toLowerCase();
    if (!/^[a-f0-9]{64}$/.test(sourceFileHash)) fail("SOURCE_HASH", "A SHA-256 source hash is required for normalized Batch rows.");
    const configured = (config.internal_reportable_channels || []).slice().sort((left, right) => left.order - right.order);
    if (configured.length !== 23) fail("CONFIG_CHANNELS", "The controlled configuration must provide 23 reportable channels.");
    const expectedLabels = BATCH_HEADERS.slice(33, 56);
    if (configured.map((channel) => channel.worksheet_label).join("\u001f") !== expectedLabels.join("\u001f")) {
      fail("CHANNEL_ORDER", "Controlled reportable channel order does not match the Batch destination contract.");
    }
    const mappings = Array.isArray(settings.runtime_mapping) ? settings.runtime_mapping : [];
    const rows = parsed.records.map((record) => {
      const sample = record.sample_information;
      const files = record.original_files;
      const configuration = record.configuration;
      const category = classifyRecord(sample);
      const sampleName = String(sample["Sample Name"] || "");
      const sampleId = String(sample["Sample ID"] || "");
      const mapping = category === "Sample" ? findMapping(mappings, sampleName, sampleId) : null;
      const qbenchTestId = category === "Sample" ? (mapping ? mapping.qbench_test_display_id : directTestId(sampleName, sampleId)) : "";
      const rowKey = `labsolutions:${sourceFileHash}:${record.record_order}`;
      const data = Array(BATCH_HEADERS.length).fill("");
      const put = (header, value) => { data[BATCH_HEADERS.indexOf(header)] = value === undefined || value === null ? "" : value; };
      const unknownPeakCount = record.peak_table.filter((peak) => peak.unconfigured_analyte).length;
      const isManual = manualIntegration(record.peak_table);
      put("import_row_id", rowKey);
      put("run_order", record.record_order);
      put("vial", sample["Vial#"]);
      put("sample_type", batchSampleType(category));
      put("qbench_test_id", qbenchTestId);
      put("sample_mass_g", sample["Sample Amount"]);
      put("df_application_mode", category === "Sample" ? "already_applied_by_labsolutions" : "");
      put("labsolutions_sample_amount", sample["Sample Amount"]);
      put("labsolutions_dilution_factor", sample["Dilution Factor"]);
      put("source_instrument_file", files["Data File"]);
      put("source_file_hash", sourceFileHash);
      put("source_data_file", files["Data File"]);
      put("source_method_file", files["Method File"]);
      put("source_sequence_file", files["Batch File"]);
      put("acquired_at", sample.Acquired);
      put("instrument_name", configuration["Instrument Name"]);
      put("detector_id", configuration["Detector ID"]);
      put("detector_name", configuration["Detector Name"]);
      put("parser_version", `${parsed.parser_core_version}+${VERSION}`);
      put("compound_result_row_count", record.counts.compound_result_row_count);
      put("peak_table_row_count", record.counts.peak_table_row_count);
      put("reportable_compound_row_count", record.counts.reportable_compound_row_count);
      put("dimethylacetamide_conc", record.dimethylacetamide_audit.conc);
      put("unknown_peak_count", unknownPeakCount);
      put("manual_integration", isManual ? "Yes" : "No");
      put("integration_reason", isManual ? "manual_peak_mark" : "");
      put("integration_review_status", unknownPeakCount || isManual ? "Review Required" : "Not Reviewed");
      record.reportable_analytes.forEach((analyte, index) => put(expectedLabels[index], analyte.conc));
      put("source_row_hash", rowKey);
      const writes = BATCH_HEADERS.map((header, index) => ({ header, value: data[index] })).filter((cell) => !FORMULA_OWNED_HEADERS.has(cell.header));
      return {
        record_order: record.record_order,
        category,
        sample_name: sampleName,
        sample_id: sampleId,
        level: sample.Level || "",
        qbench_test_display_id: qbenchTestId,
        linkage_status: category !== "Sample" ? "control_excluded" : (qbenchTestId ? (mapping ? "mapped_overlay" : "matched_sample_id") : "held_unmapped"),
        transfer_eligible: category === "Sample" && Boolean(qbenchTestId),
        source_row_key: rowKey,
        batch_row: data,
        write_cells: writes,
      };
    });
    return { adapter_version: VERSION, batch_headers: BATCH_HEADERS.slice(), rows };
  }

  const api = Object.freeze({
    VERSION,
    BATCH_HEADERS,
    FORMULA_OWNED_HEADERS,
    BatchAdapterError,
    parseRuntimeMappingCsv,
    classifyRecord,
    normalizeRecords,
  });
  root.QBenchTerpenesMultiRecordBatchAdapter = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof globalThis !== "undefined" ? globalThis : self);
