"use strict";

const crypto = require("crypto");

const PARSER_CORE_VERSION = "terpenes-labsolutions-core-v1";

const REQUIRED_SECTIONS = [
  "Header",
  "Sample Information",
  "Original Files",
  "Configuration",
  "Peak Table(Ch1)",
  "Compound Results(Ch1)",
];

const NUMERIC_FIELDS = new Set([
  "R.Time",
  "I.Time",
  "F.Time",
  "Area",
  "Height",
  "A/H",
  "Conc.",
  "k'",
  "Plate #",
  "Plate Ht.",
  "Tailing",
  "Resolution",
  "Sep.Factor",
  "Area Ratio",
  "Height Ratio",
  "Conc. %",
  "Norm Conc.",
  "3rd",
  "2nd",
  "1st",
  "Constant",
  "ID#",
  "Peak#",
  "Injection Volume",
  "Injection Count",
  "Sample Amount",
  "Dilution Factor",
  "Vial#",
]);

const DEFAULT_SECURITY_LIMITS = Object.freeze({
  max_raw_file_size_bytes: 2_000_000,
  max_section_count: 32,
  max_table_row_count: 2000,
  max_line_length: 20000,
  max_field_count: 128,
  max_error_message_length: 500,
});

class TerpenesParserError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.name = "TerpenesParserError";
    this.code = code;
    this.section = details.section || "";
    this.analyte = details.analyte || "";
    this.row = details.row || "";
    this.details = sanitizeDetails(details);
  }

  toJSON() {
    return {
      code: this.code,
      message: this.message,
      section: this.section,
      analyte: this.analyte,
      row: this.row,
      details: this.details,
    };
  }
}

function sanitizeDetails(details) {
  const out = {};
  for (const [key, value] of Object.entries(details || {})) {
    if (key === "raw" || key === "rawFile" || key === "text") continue;
    out[key] = value;
  }
  return out;
}

function controlledError(code, message, details = {}) {
  const maxLength = details.max_error_message_length || DEFAULT_SECURITY_LIMITS.max_error_message_length;
  const safeMessage = String(message).slice(0, maxLength);
  return new TerpenesParserError(code, safeMessage, details);
}

function sha256Hex(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function decodeInput(input, options = {}) {
  let bytes;
  if (typeof input === "string") {
    bytes = Buffer.from(input, "utf8");
  } else if (Buffer.isBuffer(input)) {
    bytes = Buffer.from(input);
  } else if (input instanceof Uint8Array) {
    bytes = Buffer.from(input);
  } else {
    throw controlledError("UNSUPPORTED_INPUT_TYPE", "Input must be a string, Buffer, or Uint8Array.");
  }

  const limits = { ...DEFAULT_SECURITY_LIMITS, ...(options.securityLimits || {}) };
  if (bytes.length > limits.max_raw_file_size_bytes) {
    throw controlledError("RAW_FILE_TOO_LARGE", "LabSolutions export exceeds configured maximum file size.", {
      maxBytes: limits.max_raw_file_size_bytes,
      actualBytes: bytes.length,
    });
  }

  let text = bytes.toString("utf8");
  if (text.charCodeAt(0) === 0xfeff) text = text.slice(1);
  return { bytes, text, limits };
}

function parseNumberStrict(value) {
  const text = String(value).trim();
  if (text === "") return "";
  if (!/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$/.test(text)) return text;
  const parsed = Number(text);
  return Number.isFinite(parsed) ? parsed : text;
}

function parseScalar(header, value) {
  const text = String(value).trim();
  if (NUMERIC_FIELDS.has(header)) return parseNumberStrict(text);
  return text;
}

function normalizeAnalyteName(value) {
  return String(value || "")
    .normalize("NFKC")
    .toLowerCase()
    .replace(/\u03b1|\u0391/g, "alpha")
    .replace(/\u03b2|\u0392/g, "beta")
    .replace(/\u03b3|\u0393/g, "gamma")
    .replace(/\u03b4|\u0394/g, "delta")
    .replace(/[^a-z0-9]+/g, "");
}

function orderedReportableChannels(config) {
  return [...(config.internal_reportable_channels || [])].sort((a, b) => a.order - b.order);
}

function auditChannels(config) {
  return [...(config.audit_only_channels || [])];
}

function allConfiguredChannels(config) {
  return [...orderedReportableChannels(config), ...auditChannels(config)];
}

function validateConfig(config) {
  if (!config || typeof config !== "object") {
    throw controlledError("CONFIG_MISSING", "Analyte configuration is required.");
  }
  if (config.reporting_mode !== "quantitative_only") {
    throw controlledError("CONFIG_REPORTING_MODE", "Terpenes reporting mode must be quantitative_only.");
  }
  const quantitation = config.quantitation || {};
  if (quantitation.source_table !== "Compound Results(Ch1)" || quantitation.source_field !== "Conc.") {
    throw controlledError("CONFIG_QUANTITATION_SOURCE", "Quantitation must use Compound Results(Ch1) > Conc.");
  }
  for (const blocked of quantitation.blocked_potency_fields || []) {
    if (blocked === quantitation.source_field) {
      throw controlledError("CONFIG_BLOCKED_SOURCE", `Blocked potency field selected: ${blocked}`);
    }
  }
  const controls = config.result_status_controls || {};
  for (const key of [
    "sample_pass_fail_enabled",
    "analyte_pass_fail_enabled",
    "coa_pass_fail_enabled",
    "metrc_pass_fail_enabled",
    "kvstore_pass_fail_enabled",
    "label_claim_pass_fail_enabled",
  ]) {
    if (controls[key] !== false) {
      throw controlledError("CONFIG_PASS_FAIL_ENABLED", `Terpenes must not enable ${key}.`);
    }
  }
  const reportable = orderedReportableChannels(config);
  const audits = auditChannels(config);
  if (reportable.length !== 23) {
    throw controlledError("CONFIG_REPORTABLE_COUNT", `Expected 23 reportable channels, found ${reportable.length}.`);
  }
  if (audits.length !== 1 || audits[0].internal_key !== "dimethylacetamide") {
    throw controlledError("CONFIG_AUDIT_COUNT", "Expected exactly one Dimethylacetamide audit-only channel.");
  }
  const keys = new Set();
  const ids = new Set();
  for (const channel of allConfiguredChannels(config)) {
    if (!channel.internal_key) throw controlledError("CONFIG_BLANK_KEY", "Configured internal keys must be nonblank.");
    if (keys.has(channel.internal_key)) {
      throw controlledError("CONFIG_DUPLICATE_KEY", `Duplicate configured key: ${channel.internal_key}`);
    }
    keys.add(channel.internal_key);
    if (!Number.isInteger(channel.labsolutions_compound_id)) {
      throw controlledError("CONFIG_BAD_ID", `LabSolutions compound ID must be an integer for ${channel.internal_key}.`);
    }
    if (ids.has(channel.labsolutions_compound_id)) {
      throw controlledError("CONFIG_DUPLICATE_ID", `Duplicate LabSolutions ID: ${channel.labsolutions_compound_id}`);
    }
    ids.add(channel.labsolutions_compound_id);
  }
}

function buildAliasMap(config) {
  const aliasMap = new Map();
  for (const channel of allConfiguredChannels(config)) {
    const aliases = new Set([
      channel.worksheet_label,
      channel.labsolutions_compound_name,
      ...(channel.aliases || []),
    ]);
    for (const alias of aliases) {
      const normalized = normalizeAnalyteName(alias);
      if (!normalized) continue;
      const existing = aliasMap.get(normalized);
      if (existing && existing.internal_key !== channel.internal_key) {
        throw controlledError("CONFIG_ALIAS_CONFLICT", `Conflicting analyte alias: ${alias}`);
      }
      aliasMap.set(normalized, channel);
    }
  }
  return aliasMap;
}

function splitSections(text, limits) {
  const lines = text.replace(/\r\n/g, "\n").replace(/\r/g, "\n").split("\n");
  const sections = new Map();
  let current = null;
  lines.forEach((line, lineIndex) => {
    if (line.length > limits.max_line_length) {
      throw controlledError("LINE_TOO_LONG", "LabSolutions export contains a line over the configured limit.", {
        row: lineIndex + 1,
      });
    }
    const match = line.match(/^\[(.+)]\s*$/);
    if (match) {
      current = match[1];
      sections.set(current, []);
      if (sections.size > limits.max_section_count) {
        throw controlledError("TOO_MANY_SECTIONS", "LabSolutions export contains too many sections.");
      }
      return;
    }
    if (current) sections.get(current).push(line);
  });
  for (const section of REQUIRED_SECTIONS) {
    if (!sections.has(section)) {
      throw controlledError("MISSING_REQUIRED_SECTION", `Missing required section: ${section}`, { section });
    }
  }
  return sections;
}

function parseKeyValueSection(sections, sectionName) {
  const values = {};
  for (const line of sections.get(sectionName) || []) {
    if (!line.trim()) continue;
    const parts = line.split("\t");
    if (parts.length >= 2) values[parts[0].trim()] = parseScalar(parts[0].trim(), parts.slice(1).join("\t"));
  }
  return values;
}

function parseTable(sections, sectionName, headerPrefix, aliasMap, limits) {
  const rows = [];
  let headers = null;
  for (const line of sections.get(sectionName) || []) {
    if (!line.trim() || line.startsWith("# of")) continue;
    if (line.startsWith(headerPrefix)) {
      headers = line.split("\t");
      if (headers.length > limits.max_field_count) {
        throw controlledError("TOO_MANY_FIELDS", `${sectionName} header has too many fields.`, { section: sectionName });
      }
      continue;
    }
    if (!headers) continue;
    const cells = line.split("\t");
    if (cells.length !== headers.length) {
      throw controlledError("MALFORMED_ROW_WIDTH", `${sectionName} row has ${cells.length} fields; expected ${headers.length}.`, {
        section: sectionName,
        row: rows.length + 1,
      });
    }
    if (rows.length >= limits.max_table_row_count) {
      throw controlledError("TOO_MANY_TABLE_ROWS", `${sectionName} exceeds configured row limit.`, { section: sectionName });
    }
    const row = {};
    headers.forEach((header, index) => {
      row[header] = parseScalar(header, cells[index]);
    });
    const name = String(row.Name || "").trim();
    const channel = aliasMap.get(normalizeAnalyteName(name));
    if (channel) {
      row.internal_key = channel.internal_key;
      row.worksheet_label = channel.worksheet_label || name;
      row.reportable = Boolean(channel.reportable);
      row.retain_for_audit = Boolean(channel.retain_for_audit) || !Boolean(channel.reportable);
      row.configured_labsolutions_compound_id = channel.labsolutions_compound_id;
      row.unconfigured_analyte = false;
    } else {
      row.internal_key = "";
      row.worksheet_label = name;
      row.reportable = false;
      row.retain_for_audit = true;
      row.unconfigured_analyte = true;
    }
    rows.push(row);
  }
  return rows;
}

function validateCompoundResults(rows, config) {
  const configured = new Map(allConfiguredChannels(config).map((channel) => [channel.internal_key, channel]));
  const expectedKeys = new Set(configured.keys());
  const configuredRows = rows.filter((row) => expectedKeys.has(row.internal_key));
  const reportableRows = configuredRows.filter((row) => row.reportable);
  const keyCounts = new Map();
  const errors = [];

  if (rows.length !== 24) errors.push(`expected 24 Compound Results rows, found ${rows.length}`);
  if (reportableRows.length !== 23) errors.push(`expected 23 reportable Compound Results rows, found ${reportableRows.length}`);

  for (const row of rows) {
    if (row.unconfigured_analyte) {
      errors.push(`unknown Compound Results name: ${String(row.Name || "<blank>")}`);
      continue;
    }
    keyCounts.set(row.internal_key, (keyCounts.get(row.internal_key) || 0) + 1);
    const expected = configured.get(row.internal_key);
    if (row["ID#"] !== expected.labsolutions_compound_id) {
      errors.push(`${row.Name} ID# ${row["ID#"]} expected ${expected.labsolutions_compound_id}`);
    }
    if (typeof row["Conc."] !== "number") {
      errors.push(`${row.Name} Conc. is not a numeric value`);
    }
  }
  for (const key of expectedKeys) {
    const count = keyCounts.get(key) || 0;
    if (count === 0) errors.push(`missing key: ${key}`);
    if (count > 1) errors.push(`duplicate key: ${key}`);
  }
  if ((keyCounts.get("dimethylacetamide") || 0) !== 1) {
    errors.push("Dimethylacetamide audit-only row must appear exactly once");
  }
  if (errors.length) {
    throw controlledError("INVALID_COMPOUND_RESULTS", `Invalid Compound Results(Ch1): ${errors.join(" | ")}`, {
      section: "Compound Results(Ch1)",
    });
  }
}

function unknownPeakCount(rows) {
  return rows.filter((row) => {
    const name = String(row.Name || "").trim();
    if (!name) return true;
    if (row.unconfigured_analyte) return true;
    return /unknown|unidentified/i.test(name);
  }).length;
}

function parseLabSolutionsAscii(input, config, options = {}) {
  validateConfig(config);
  const { bytes, text, limits } = decodeInput(input, options);
  const sections = splitSections(text, limits);
  const aliasMap = buildAliasMap(config);
  const compoundRows = parseTable(sections, "Compound Results(Ch1)", "ID#", aliasMap, limits);
  const peakRows = parseTable(sections, "Peak Table(Ch1)", "Peak#", aliasMap, limits);
  validateCompoundResults(compoundRows, config);

  const sampleInformation = parseKeyValueSection(sections, "Sample Information");
  const originalFiles = parseKeyValueSection(sections, "Original Files");
  const configuration = parseKeyValueSection(sections, "Configuration");
  const header = parseKeyValueSection(sections, "Header");
  const fileInformation = parseKeyValueSection(sections, "File Information");
  const fileDescription = parseKeyValueSection(sections, "File Description");

  const byKey = new Map(compoundRows.map((row) => [row.internal_key, row]));
  const reportableAnalytes = orderedReportableChannels(config).map((channel) => {
    const row = byKey.get(channel.internal_key);
    return {
      order: channel.order,
      internal_key: channel.internal_key,
      worksheet_label: channel.worksheet_label,
      source_id: row["ID#"],
      source_name: row.Name,
      conc: row["Conc."],
      conc_percent_not_potency: row["Conc. %"],
      norm_conc_not_potency: row["Norm Conc."],
      r_time: row["R.Time"],
      area: row.Area,
      height: row.Height,
    };
  });
  const dimethylacetamideRow = byKey.get("dimethylacetamide");
  const counts = {
    compound_result_row_count: compoundRows.length,
    peak_table_row_count: peakRows.length,
    reportable_compound_row_count: reportableAnalytes.length,
    dimethylacetamide_row_count: dimethylacetamideRow ? 1 : 0,
    unknown_peak_count: unknownPeakCount(peakRows),
  };

  return {
    parser_core_version: PARSER_CORE_VERSION,
    quantitation_source: {
      table: "Compound Results(Ch1)",
      field: "Conc.",
      blocked_fields: ["Conc. %", "Norm Conc."],
    },
    source_metadata: {
      header,
      file_information: fileInformation,
      file_description: fileDescription,
      sample_information: sampleInformation,
      original_files: originalFiles,
      configuration,
    },
    compound_results: compoundRows,
    peak_table: peakRows,
    reportable_analytes: reportableAnalytes,
    dimethylacetamide_audit: {
      internal_key: "dimethylacetamide",
      source_id: dimethylacetamideRow["ID#"],
      source_name: dimethylacetamideRow.Name,
      conc: dimethylacetamideRow["Conc."],
      reportable: false,
    },
    counts,
    audit_warnings: counts.unknown_peak_count
      ? [{ code: "UNKNOWN_PEAK_TABLE_ROWS", message: "Peak Table contains unknown, unidentified, or blank-name audit rows." }]
      : [],
    source_provenance: {
      source_file_hash: sha256Hex(bytes),
      sections_present: Array.from(sections.keys()),
      raw_file_retained_in_output: false,
    },
  };
}

function toControlledError(error) {
  if (error instanceof TerpenesParserError) return error.toJSON();
  return {
    code: "UNEXPECTED_PARSE_ERROR",
    message: String(error && error.message ? error.message : error).slice(0, DEFAULT_SECURITY_LIMITS.max_error_message_length),
    section: "",
    analyte: "",
    row: "",
  };
}

module.exports = {
  PARSER_CORE_VERSION,
  DEFAULT_SECURITY_LIMITS,
  REQUIRED_SECTIONS,
  NUMERIC_FIELDS,
  TerpenesParserError,
  controlledError,
  parseNumberStrict,
  normalizeAnalyteName,
  orderedReportableChannels,
  validateConfig,
  buildAliasMap,
  parseLabSolutionsAscii,
  toControlledError,
  sha256Hex,
};
