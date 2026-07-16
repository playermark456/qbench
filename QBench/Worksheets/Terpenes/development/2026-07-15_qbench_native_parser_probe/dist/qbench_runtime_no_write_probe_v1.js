"use strict";

importScripts("https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js");

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

const QBenchProbeConfig = Object.freeze({"audit_only_channels": [{"aliases": ["Dimethylacetamide", "dimethylacetamide"], "internal_key": "dimethylacetamide", "labsolutions_compound_id": 1, "labsolutions_compound_name": "Dimethylacetamide", "reportable": false, "retain_for_audit": true, "worksheet_label": "Dimethylacetamide"}], "internal_reportable_channels": [{"aliases": ["alpha-Pinene", "Alpha-Pinene", "alpha pinene", "α-Pinene"], "internal_key": "apinene", "labsolutions_compound_id": 2, "labsolutions_compound_name": "alpha-Pinene", "order": 1, "reportable": true, "worksheet_label": "α-Pinene"}, {"aliases": ["Camphene", "camphene"], "internal_key": "camphene", "labsolutions_compound_id": 3, "labsolutions_compound_name": "Camphene", "order": 2, "reportable": true, "worksheet_label": "Camphene"}, {"aliases": ["beta-Myrcene", "Beta-Myrcene", "beta myrcene", "β-Myrcene"], "internal_key": "bmyrcene", "labsolutions_compound_id": 4, "labsolutions_compound_name": "beta-Myrcene", "order": 3, "reportable": true, "worksheet_label": "β-Myrcene"}, {"aliases": ["(-)-beta-Pinene", "beta-Pinene", "Beta-Pinene", "(-)-β-pinene"], "internal_key": "bpinene", "labsolutions_compound_id": 5, "labsolutions_compound_name": "(-)-beta-Pinene", "order": 4, "reportable": true, "worksheet_label": "(-)-β-pinene"}, {"aliases": ["delta-3-Carene", "Delta-3-carene", "delta 3 carene", "δ-3-Carene"], "internal_key": "delta3carene", "labsolutions_compound_id": 6, "labsolutions_compound_name": "delta-3-Carene", "order": 5, "reportable": true, "worksheet_label": "Delta-3-carene"}, {"aliases": ["alpha-Terpinene", "Alpha-Terpinene", "alpha terpinene", "α-Terpinene"], "internal_key": "aterpinene", "labsolutions_compound_id": 7, "labsolutions_compound_name": "alpha-Terpinene", "order": 6, "reportable": true, "worksheet_label": "α-Terpinene"}, {"aliases": ["Ocimene 1", "ocimene-1", "cis-Ocimene", "cis ocimene"], "internal_key": "cisocimene", "labsolutions_compound_id": 8, "labsolutions_compound_name": "Ocimene 1", "order": 7, "reportable": true, "worksheet_label": "cis-Ocimene"}, {"aliases": ["D-Limonene", "d-Limonene", "d limonene", "Limonene"], "internal_key": "dlimonene", "labsolutions_compound_id": 9, "labsolutions_compound_name": "D-Limonene", "order": 8, "reportable": true, "worksheet_label": "d-Limonene"}, {"aliases": ["p-Cymene", "P-Cymene", "p cymene", "P-Isopropyltoluene (P-Cymene)"], "internal_key": "pcymene", "labsolutions_compound_id": 10, "labsolutions_compound_name": "p-Cymene", "order": 9, "reportable": true, "worksheet_label": "p-Cymene"}, {"aliases": ["Ocimene 2", "ocimene-2", "trans-Ocimene", "trans ocimene"], "internal_key": "transocimene", "labsolutions_compound_id": 11, "labsolutions_compound_name": "Ocimene 2", "order": 10, "reportable": true, "worksheet_label": "trans-Ocimene"}, {"aliases": ["Eucalyptol", "eucalyptol", "1,8-Cineole", "1 8 Cineole"], "internal_key": "eucalyptol", "labsolutions_compound_id": 12, "labsolutions_compound_name": "Eucalyptol", "order": 11, "reportable": true, "worksheet_label": "Eucalyptol"}, {"aliases": ["Gamma terpinene", "gamma-Terpinene", "gamma terpinene", "γ-Terpinene"], "internal_key": "gterpinene", "labsolutions_compound_id": 13, "labsolutions_compound_name": "Gamma terpinene", "order": 12, "reportable": true, "worksheet_label": "γ-Terpinene"}, {"aliases": ["Terpinolene", "terpinolene"], "internal_key": "terpinolene", "labsolutions_compound_id": 14, "labsolutions_compound_name": "Terpinolene", "order": 13, "reportable": true, "worksheet_label": "Terpinolene"}, {"aliases": ["Linalool", "linalool"], "internal_key": "linalool", "labsolutions_compound_id": 15, "labsolutions_compound_name": "Linalool", "order": 14, "reportable": true, "worksheet_label": "Linalool"}, {"aliases": ["(-)-Isopulegol", "Isopulegol", "isopulegol"], "internal_key": "isopulegol", "labsolutions_compound_id": 16, "labsolutions_compound_name": "(-)-Isopulegol", "order": 15, "reportable": true, "worksheet_label": "(-)-Isopulegol"}, {"aliases": ["Geraniol", "geraniol"], "internal_key": "geraniol", "labsolutions_compound_id": 17, "labsolutions_compound_name": "Geraniol", "order": 16, "reportable": true, "worksheet_label": "Geraniol"}, {"aliases": ["beta-Caryophyllene", "Beta-Caryophyllene", "beta caryophyllene", "β-Caryophyllene"], "internal_key": "bcaryophyllene", "labsolutions_compound_id": 18, "labsolutions_compound_name": "beta-Caryophyllene", "order": 17, "reportable": true, "worksheet_label": "β-Caryophyllene"}, {"aliases": ["alpha-Humulene", "Alpha-Humulene", "alpha humulene", "α-Humulene"], "internal_key": "ahumulene", "labsolutions_compound_id": 19, "labsolutions_compound_name": "alpha-Humulene", "order": 18, "reportable": true, "worksheet_label": "α-Humulene"}, {"aliases": ["Nerolidol 1", "nerolidol-1", "cis-Nerolidol", "cis nerolidol"], "internal_key": "cisnerolidol", "labsolutions_compound_id": 20, "labsolutions_compound_name": "Nerolidol 1", "order": 19, "reportable": true, "worksheet_label": "cis-Nerolidol"}, {"aliases": ["Nerolidol 2", "nerolidol-2", "trans-Nerolidol", "trans nerolidol"], "internal_key": "transnerolidol", "labsolutions_compound_id": 21, "labsolutions_compound_name": "Nerolidol 2", "order": 20, "reportable": true, "worksheet_label": "trans-Nerolidol"}, {"aliases": ["(-)-Guaiol", "Guaiol", "guaiol"], "internal_key": "guaiol", "labsolutions_compound_id": 22, "labsolutions_compound_name": "(-)-Guaiol", "order": 21, "reportable": true, "worksheet_label": "(-)-Guaiol"}, {"aliases": ["Caryophyllene oxide", "Caryophyllene Oxide", "caryophyllene oxide"], "internal_key": "caryophylleneoxide", "labsolutions_compound_id": 23, "labsolutions_compound_name": "Caryophyllene oxide", "order": 22, "reportable": true, "worksheet_label": "Caryophyllene Oxide"}, {"aliases": ["(-)-alpha-Bisabolol", "alpha-Bisabolol", "Alpha-Bisabolol", "(-)-α-Bisabolol"], "internal_key": "bisabolol", "labsolutions_compound_id": 24, "labsolutions_compound_name": "(-)-alpha-Bisabolol", "order": 23, "reportable": true, "worksheet_label": "(-)-α-Bisabolol"}], "quantitation": {"source_field": "Conc.", "source_table": "Compound Results(Ch1)"}, "reporting_mode": "quantitative_only"});
const QBenchProbeLimits = Object.freeze({"allowed_file_extensions": [".txt"], "controlled_fixture_filename": "Output_redacted_fixture.txt", "maximum_error_message_length": 500, "maximum_field_count": 128, "maximum_files_per_run": 1, "maximum_line_length": 20000, "maximum_raw_file_size_bytes": 2000000, "maximum_section_count": 32, "maximum_table_row_count": 2000, "schema_version": 1});

"use strict";

(function attachNoWriteProbe(root) {
  const FIXTURE_NAME = "Output_redacted_fixture.txt";
  const CONTROLLED_ERROR_CODES = Object.freeze({
    FILE_COLLECTION: "CONTROLLED_FILE_COLLECTION_ERROR",
    FILE_COUNT: "CONTROLLED_FILE_COUNT_ERROR",
    FILE_OBJECT: "CONTROLLED_FILE_OBJECT_ERROR",
    FILE_NAME: "CONTROLLED_FILE_NAME_ERROR",
    FILE_READ: "CONTROLLED_FILE_READ_ERROR",
  });

  class ControlledRuntimeError extends Error {
    constructor(code) {
      super(code);
      this.name = "ControlledRuntimeError";
      this.code = code;
    }
  }

  function controlledError(code) {
    return new ControlledRuntimeError(code);
  }

  function logSafe(qb, message) {
    if (typeof qb.console === "function") qb.console(message);
    else if (qb.console && typeof qb.console.log === "function") qb.console.log(message);
  }

  function readFileAsText(file, Reader) {
    return new Promise((resolve, reject) => {
      let reader;
      try {
        reader = new Reader();
      } catch (_error) {
        reject(controlledError(CONTROLLED_ERROR_CODES.FILE_READ));
        return;
      }
      reader.onload = () => resolve(String(reader.result || ""));
      reader.onerror = () => reject(controlledError(CONTROLLED_ERROR_CODES.FILE_READ));
      try {
        reader.readAsText(file);
      } catch (_error) {
        reject(controlledError(CONTROLLED_ERROR_CODES.FILE_READ));
      }
    });
  }

  function fileCollectionKind(files) {
    if (Array.isArray(files)) return "Array";
    if (!files || typeof files !== "object") return "unknown";
    try {
      return "length" in files ? "array_like" : "unknown";
    } catch (_error) {
      return "unknown";
    }
  }

  function normalizeFileCollection(files) {
    const kind = fileCollectionKind(files);
    if (kind === "unknown") throw controlledError(CONTROLLED_ERROR_CODES.FILE_COLLECTION);

    let length;
    try {
      length = files.length;
    } catch (_error) {
      throw controlledError(CONTROLLED_ERROR_CODES.FILE_COLLECTION);
    }
    if (!Number.isFinite(length) || !Number.isInteger(length) || length < 0) {
      throw controlledError(CONTROLLED_ERROR_CODES.FILE_COLLECTION);
    }
    if (length !== 1) throw controlledError(CONTROLLED_ERROR_CODES.FILE_COUNT);

    let file;
    try {
      file = files[0];
      if (!file && typeof files.item === "function") file = files.item(0);
    } catch (_error) {
      throw controlledError(CONTROLLED_ERROR_CODES.FILE_OBJECT);
    }
    if (!file || typeof file !== "object") {
      throw controlledError(CONTROLLED_ERROR_CODES.FILE_OBJECT);
    }
    return Object.freeze({ file, kind, count: length });
  }

  function hasTxtExtension(name) {
    return /\.txt$/i.test(String(name || ""));
  }

  function validateFileMetadata(file) {
    const name = typeof file.name === "string" ? file.name : "";
    if (name !== FIXTURE_NAME || !hasTxtExtension(name)) {
      throw controlledError(CONTROLLED_ERROR_CODES.FILE_NAME);
    }
    return file;
  }

  function validateFiles(files) {
    const normalized = normalizeFileCollection(files);
    return validateFileMetadata(normalized.file);
  }

  function summaryFromParsed(parsed, webCryptoAvailable) {
    return Object.freeze({
      file_count: 1,
      extension_accepted: ".txt",
      compound_result_rows: parsed.counts.compound_result_row_count,
      peak_table_rows: parsed.counts.peak_table_row_count,
      reportable_channels: parsed.counts.reportable_compound_row_count,
      dimethylacetamide_audit_rows: parsed.counts.dimethylacetamide_row_count,
      web_crypto_available: webCryptoAvailable,
    });
  }

  async function execute(qb, Reader, config, core) {
    let failedStep = "runtime entered";
    try {
      logSafe(qb, "probe step = runtime entered");
      failedStep = "file collection validation";
      const kind = fileCollectionKind(qb.files);
      logSafe(qb, `file collection kind = ${kind}`);
      const normalized = normalizeFileCollection(qb.files);
      logSafe(qb, "probe step = file collection accepted");
      logSafe(qb, `file count = ${normalized.count}`);

      failedStep = "file metadata validation";
      const file = validateFileMetadata(normalized.file);
      logSafe(qb, "probe step = file metadata accepted");
      logSafe(qb, "extension accepted = .txt");

      failedStep = "file read";
      const text = await readFileAsText(file, Reader);
      logSafe(qb, "probe step = file read complete");

      failedStep = "controlled parse";
      const parsed = core.parseLabSolutionsAscii(text, config, { securityLimits: root.QBenchProbeLimits });
      logSafe(qb, "probe step = controlled parse complete");
      const summary = summaryFromParsed(parsed, Boolean(root.crypto && root.crypto.subtle));
      logSafe(qb, `Compound Results rows = ${summary.compound_result_rows}`);
      logSafe(qb, `Peak Table rows = ${summary.peak_table_rows}`);
      logSafe(qb, `reportable channels = ${summary.reportable_channels}`);
      logSafe(qb, `Dimethylacetamide audit rows = ${summary.dimethylacetamide_audit_rows}`);
      logSafe(qb, `Web Crypto available = ${summary.web_crypto_available}`);
      qb.success();
      return summary;
    } catch (error) {
      const safe = core.toControlledError(error);
      logSafe(qb, `controlled error = ${safe.code}`);
      logSafe(qb, `failed step = ${failedStep}`);
      qb.error(safe.code);
      throw error;
    }
  }

  root.QBenchRuntimeNoWriteProbe = Object.freeze({
    CONTROLLED_ERROR_CODES,
    ControlledRuntimeError,
    FIXTURE_NAME,
    controlledError,
    execute,
    fileCollectionKind,
    hasTxtExtension,
    normalizeFileCollection,
    readFileAsText,
    summaryFromParsed,
    validateFileMetadata,
    validateFiles,
  });

  if (typeof run === "function") {
    run(async () => {
      await execute(QB, FileReader, QBenchProbeConfig, QBenchTerpenesParserCore);
    });
  }
})(typeof globalThis !== "undefined" ? globalThis : self);
