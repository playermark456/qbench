"use strict";

(function attachQBenchTerpenesParserCore(root) {
  const VERSION = "terpenes-qbench-browser-core-v1";
  const REQUIRED_SECTIONS = [
    "Header",
    "Sample Information",
    "Original Files",
    "Configuration",
    "Peak Table(Ch1)",
    "Compound Results(Ch1)",
  ];
  const NUMERIC_FIELDS = new Set([
    "R.Time", "I.Time", "F.Time", "Area", "Height", "A/H", "Conc.",
    "k'", "Plate #", "Plate Ht.", "Tailing", "Resolution", "Sep.Factor",
    "Area Ratio", "Height Ratio", "Conc. %", "Norm Conc.", "3rd", "2nd",
    "1st", "Constant", "ID#", "Peak#", "Injection Volume",
    "Injection Count", "Sample Amount", "Dilution Factor", "Vial#",
  ]);
  const DEFAULT_LIMITS = Object.freeze({
    maximum_raw_file_size_bytes: 2000000,
    maximum_section_count: 32,
    maximum_table_row_count: 2000,
    maximum_line_length: 20000,
    maximum_field_count: 128,
    maximum_error_message_length: 500,
  });

  class ProbeParseError extends Error {
    constructor(code, message, details) {
      super(String(message).slice(0, DEFAULT_LIMITS.maximum_error_message_length));
      this.name = "ProbeParseError";
      this.code = code;
      this.section = details && details.section ? details.section : "";
      this.row = details && details.row ? details.row : "";
    }
  }

  function fail(code, message, details) {
    throw new ProbeParseError(code, message, details || {});
  }

  function normalizeLimits(input) {
    return Object.assign({}, DEFAULT_LIMITS, input || {});
  }

  function utf8ByteLength(text) {
    let bytes = 0;
    for (let index = 0; index < text.length; index += 1) {
      const code = text.charCodeAt(index);
      if (code < 0x80) bytes += 1;
      else if (code < 0x800) bytes += 2;
      else if (code >= 0xd800 && code <= 0xdbff && index + 1 < text.length) {
        const next = text.charCodeAt(index + 1);
        if (next >= 0xdc00 && next <= 0xdfff) {
          bytes += 4;
          index += 1;
        } else bytes += 3;
      } else bytes += 3;
    }
    return bytes;
  }

  function normalizeText(input, limits) {
    if (typeof input !== "string") fail("UNSUPPORTED_INPUT_TYPE", "Input must be UTF-8 text.");
    if (utf8ByteLength(input) > limits.maximum_raw_file_size_bytes) {
      fail("RAW_FILE_TOO_LARGE", "Input exceeds the configured file-size limit.");
    }
    return input.charCodeAt(0) === 0xfeff ? input.slice(1) : input;
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
    return NUMERIC_FIELDS.has(header) ? parseNumberStrict(text) : text;
  }

  function normalizeAnalyteName(value) {
    let text = String(value || "");
    if (typeof text.normalize === "function") text = text.normalize("NFKC");
    return text
      .toLowerCase()
      .replace(/\u03b1/g, "alpha")
      .replace(/\u03b2/g, "beta")
      .replace(/\u03b3/g, "gamma")
      .replace(/\u03b4/g, "delta")
      .replace(/[^a-z0-9]+/g, "");
  }

  function configuredChannels(config) {
    const reportable = (config.internal_reportable_channels || []).slice().sort((a, b) => a.order - b.order);
    const audit = (config.audit_only_channels || []).slice();
    if (config.reporting_mode !== "quantitative_only") fail("CONFIG_MODE", "Reporting mode must be quantitative_only.");
    if (!config.quantitation || config.quantitation.source_table !== "Compound Results(Ch1)" || config.quantitation.source_field !== "Conc.") {
      fail("CONFIG_SOURCE", "Quantitation source must be Compound Results(Ch1) Conc.");
    }
    if (reportable.length !== 23 || audit.length !== 1 || audit[0].internal_key !== "dimethylacetamide") {
      fail("CONFIG_COUNTS", "Controlled configuration must contain 23 reportable channels and one Dimethylacetamide audit channel.");
    }
    const channels = reportable.concat(audit);
    const keys = new Set();
    const ids = new Set();
    channels.forEach((channel) => {
      if (!channel.internal_key || keys.has(channel.internal_key)) fail("CONFIG_KEY", "Configured channel keys must be unique and nonblank.");
      if (!Number.isInteger(channel.labsolutions_compound_id) || ids.has(channel.labsolutions_compound_id)) fail("CONFIG_ID", "Configured compound IDs must be unique integers.");
      keys.add(channel.internal_key);
      ids.add(channel.labsolutions_compound_id);
    });
    for (let id = 1; id <= 24; id += 1) {
      if (!ids.has(id)) fail("CONFIG_ID_SET", "Configured compound IDs must equal 1 through 24.");
    }
    return { reportable, audit, channels };
  }

  function buildAliasMap(config) {
    const groups = configuredChannels(config);
    const aliases = new Map();
    groups.channels.forEach((channel) => {
      [channel.worksheet_label, channel.labsolutions_compound_name].concat(channel.aliases || []).forEach((alias) => {
        const normalized = normalizeAnalyteName(alias);
        if (!normalized) return;
        const prior = aliases.get(normalized);
        if (prior && prior.internal_key !== channel.internal_key) fail("CONFIG_ALIAS", "Controlled analyte aliases conflict.");
        aliases.set(normalized, channel);
      });
    });
    return { aliases, groups };
  }

  function splitSections(text, limits) {
    const sections = new Map();
    let current = null;
    text.replace(/\r\n/g, "\n").replace(/\r/g, "\n").split("\n").forEach((line, index) => {
      if (line.length > limits.maximum_line_length) fail("LINE_TOO_LONG", "Input contains a line over the configured limit.", { row: index + 1 });
      const match = line.match(/^\[(.+)]\s*$/);
      if (match) {
        current = match[1];
        if (sections.has(current) && REQUIRED_SECTIONS.includes(current)) fail("DUPLICATE_SECTION", "Repeated required section.", { section: current, row: index + 1 });
        sections.set(current, []);
        if (sections.size > limits.maximum_section_count) fail("TOO_MANY_SECTIONS", "Input contains too many sections.");
      } else if (current) sections.get(current).push(line);
    });
    REQUIRED_SECTIONS.forEach((section) => {
      if (!sections.has(section)) fail("MISSING_SECTION", "Missing required section.", { section });
    });
    return sections;
  }

  function parseTable(sections, sectionName, headerPrefix, aliasMap, limits) {
    let headers = null;
    const rows = [];
    (sections.get(sectionName) || []).forEach((line) => {
      if (!line.trim() || line.indexOf("# of") === 0) return;
      if (line.indexOf(headerPrefix) === 0) {
        if (headers) fail("AMBIGUOUS_HEADER", "Table contains more than one header.", { section: sectionName });
        headers = line.split("\t");
        if (headers.length > limits.maximum_field_count) fail("TOO_MANY_FIELDS", "Table header exceeds field limit.", { section: sectionName });
        return;
      }
      if (!headers) return;
      const cells = line.split("\t");
      if (cells.length !== headers.length) fail("MALFORMED_ROW_WIDTH", "Table row width does not match header.", { section: sectionName, row: rows.length + 1 });
      if (rows.length >= limits.maximum_table_row_count) fail("TOO_MANY_ROWS", "Table exceeds row limit.", { section: sectionName });
      const row = {};
      headers.forEach((header, index) => { row[header] = parseScalar(header, cells[index]); });
      const channel = aliasMap.get(normalizeAnalyteName(row.Name));
      row.internal_key = channel ? channel.internal_key : "";
      row.reportable = channel ? channel.reportable === true : false;
      row.retain_for_audit = channel ? channel.reportable !== true || channel.retain_for_audit === true : true;
      row.unconfigured_analyte = !channel;
      row.configured_labsolutions_compound_id = channel ? channel.labsolutions_compound_id : null;
      rows.push(row);
    });
    if (!headers) fail("MISSING_HEADER", "Required table header is missing.", { section: sectionName });
    return rows;
  }

  function validateRows(compoundRows, peakRows, groups) {
    const expected = new Map(groups.channels.map((channel) => [channel.internal_key, channel]));
    const counts = new Map();
    const errors = [];
    if (compoundRows.length !== 24) errors.push("Compound Results row count must be 24");
    if (peakRows.length !== 34) errors.push("Peak Table row count must be 34");
    compoundRows.forEach((row) => {
      if (row.unconfigured_analyte) {
        errors.push("unknown Compound Results name");
        return;
      }
      counts.set(row.internal_key, (counts.get(row.internal_key) || 0) + 1);
      const channel = expected.get(row.internal_key);
      if (row["ID#"] !== channel.labsolutions_compound_id) errors.push("Compound Results ID/name mismatch");
      if (typeof row["Conc."] !== "number") errors.push("Compound Results concentration must be numeric");
    });
    expected.forEach((_channel, key) => {
      if ((counts.get(key) || 0) !== 1) errors.push("Every configured Compound Results channel must appear exactly once");
    });
    if (compoundRows.filter((row) => row.reportable).length !== 23) errors.push("Reportable Compound Results row count must be 23");
    if ((counts.get("dimethylacetamide") || 0) !== 1) errors.push("Dimethylacetamide audit row count must be one");
    if (errors.length) fail("INVALID_CONTROLLED_RESULTS", Array.from(new Set(errors)).join(" | "), { section: "Compound Results(Ch1)" });
  }

  function parseLabSolutionsAscii(input, config, options) {
    const limits = normalizeLimits(options && options.securityLimits);
    const text = normalizeText(input, limits);
    const sections = splitSections(text, limits);
    const mapping = buildAliasMap(config);
    const compoundRows = parseTable(sections, "Compound Results(Ch1)", "ID#", mapping.aliases, limits);
    const peakRows = parseTable(sections, "Peak Table(Ch1)", "Peak#", mapping.aliases, limits);
    validateRows(compoundRows, peakRows, mapping.groups);
    const byKey = new Map(compoundRows.map((row) => [row.internal_key, row]));
    const reportableAnalytes = mapping.groups.reportable.map((channel) => {
      const row = byKey.get(channel.internal_key);
      return {
        order: channel.order,
        internal_key: channel.internal_key,
        source_id: row["ID#"],
        source_name: row.Name,
        conc: row["Conc."],
        r_time: row["R.Time"],
        area: row.Area,
        height: row.Height,
      };
    });
    const audit = byKey.get("dimethylacetamide");
    return {
      parser_core_version: VERSION,
      quantitation_source: { table: "Compound Results(Ch1)", field: "Conc." },
      compound_results: compoundRows,
      peak_table: peakRows,
      reportable_analytes: reportableAnalytes,
      dimethylacetamide_audit: {
        internal_key: "dimethylacetamide",
        source_id: audit["ID#"],
        source_name: audit.Name,
        conc: audit["Conc."],
        reportable: false,
      },
      counts: {
        compound_result_row_count: compoundRows.length,
        peak_table_row_count: peakRows.length,
        reportable_compound_row_count: reportableAnalytes.length,
        dimethylacetamide_row_count: 1,
      },
      raw_file_retained_in_output: false,
    };
  }

  function toControlledError(error) {
    return {
      code: error && error.code ? error.code : "UNEXPECTED_PARSE_ERROR",
      message: String(error && error.message ? error.message : error).slice(0, DEFAULT_LIMITS.maximum_error_message_length),
      section: error && error.section ? error.section : "",
      row: error && error.row ? error.row : "",
    };
  }

  root.QBenchTerpenesParserCore = Object.freeze({
    VERSION,
    DEFAULT_LIMITS,
    ProbeParseError,
    normalizeAnalyteName,
    parseNumberStrict,
    parseLabSolutionsAscii,
    toControlledError,
  });
})(typeof globalThis !== "undefined" ? globalThis : self);
