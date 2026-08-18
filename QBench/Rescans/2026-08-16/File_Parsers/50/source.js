/* SBX_ONLY Terpenes Simple Results V2 Controls browser-upload artifact. Generated from src/terpenes_simple_results_parser_v2_controls.js. */
"use strict";

if (typeof importScripts === "function") {
  importScripts("https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js");
  importScripts("https://d731z7k534aiw.cloudfront.net/v2.7.0/qbjs.js");
}

(function attachTerpenesSimpleResultsV2Controls(root) {
const VERSION =
  "terpenes-simple-results-parser-v2-controls-r3-sample-name-test-id";
const CORE_VERSION =
  "terpenes-simple-results-core-v2-controls-r3-sample-name-test-id";
  const RESULTS_TAB = "Results";
  const FIRST_DATA_ROW = 2;
  const LAST_DATA_ROW = 87;
  const CONTEXT_LAST_COLUMN = 2;
  const PARSER_FIRST_COLUMN = 3;
  const PARSER_LAST_COLUMN = 50;
  const WORKSHEET_LAST_ROW = 190;
  const AUDIT_SEPARATOR_ROW = 88;
  const AUDIT_SECTION_ROW = 89;
  const AUDIT_HEADER_ROW = 90;
  const AUDIT_FIRST_DATA_ROW = 91;
  const AUDIT_LAST_DATA_ROW = 190;
  const AUDIT_CAPACITY = 100;
  const REQUIRED_SECTIONS = Object.freeze([
    "Header",
    "File Information",
    "Sample Information",
    "Original Files",
    "File Description",
    "Configuration",
    "Peak Table(Ch1)",
    "Compound Results(Ch1)",
  ]);
  const NUMERIC_FIELDS = new Set([
    "R.Time", "I.Time", "F.Time", "Area", "Height", "A/H", "Conc.",
    "k'", "Plate #", "Plate Ht.", "Tailing", "Resolution", "Sep.Factor",
    "Area Ratio", "Height Ratio", "Conc. %", "Norm Conc.", "3rd", "2nd",
    "1st", "Constant", "ID#", "Peak#", "Injection Volume",
    "Injection Count", "Sample Amount", "Dilution Factor", "Vial#",
  ]);
  const LIMITS = Object.freeze({
    maximum_raw_file_size_bytes: 2_000_000,
    maximum_record_count: 200,
    maximum_section_count: 32,
    maximum_table_row_count: 2_000,
    maximum_line_length: 20_000,
    maximum_field_count: 128,
    maximum_error_message_length: 500,
  });

  const REPORTABLE_ANALYTES = Object.freeze([
    { id: 2, key: "apinene", label: "α-Pinene", source: "alpha-Pinene", aliases: ["Alpha-Pinene", "alpha pinene", "α-Pinene"] },
    { id: 3, key: "camphene", label: "Camphene", source: "Camphene", aliases: ["camphene"] },
    { id: 4, key: "bmyrcene", label: "β-Myrcene", source: "beta-Myrcene", aliases: ["Beta-Myrcene", "beta myrcene", "β-Myrcene"] },
    { id: 5, key: "bpinene", label: "(-)-β-pinene", source: "(-)-beta-Pinene", aliases: ["beta-Pinene", "Beta-Pinene", "(-)-β-pinene"] },
    { id: 6, key: "delta3carene", label: "Delta-3-carene", source: "delta-3-Carene", aliases: ["Delta-3-carene", "delta 3 carene", "δ-3-Carene"] },
    { id: 7, key: "aterpinene", label: "α-Terpinene", source: "alpha-Terpinene", aliases: ["Alpha-Terpinene", "alpha terpinene", "α-Terpinene"] },
    { id: 8, key: "cisocimene", label: "cis-Ocimene", source: "Ocimene 1", aliases: ["ocimene-1", "cis-Ocimene", "cis ocimene"] },
    { id: 9, key: "dlimonene", label: "d-Limonene", source: "D-Limonene", aliases: ["d-Limonene", "d limonene", "Limonene"] },
    { id: 10, key: "pcymene", label: "p-Cymene", source: "p-Cymene", aliases: ["P-Cymene", "p cymene", "P-Isopropyltoluene (P-Cymene)"] },
    { id: 11, key: "transocimene", label: "trans-Ocimene", source: "Ocimene 2", aliases: ["ocimene-2", "trans-Ocimene", "trans ocimene"] },
    { id: 12, key: "eucalyptol", label: "Eucalyptol", source: "Eucalyptol", aliases: ["eucalyptol", "1,8-Cineole", "1 8 Cineole"] },
    { id: 13, key: "gterpinene", label: "γ-Terpinene", source: "Gamma terpinene", aliases: ["gamma-Terpinene", "gamma terpinene", "γ-Terpinene"] },
    { id: 14, key: "terpinolene", label: "Terpinolene", source: "Terpinolene", aliases: ["terpinolene"] },
    { id: 15, key: "linalool", label: "Linalool", source: "Linalool", aliases: ["linalool"] },
    { id: 16, key: "isopulegol", label: "(-)-Isopulegol", source: "(-)-Isopulegol", aliases: ["Isopulegol", "isopulegol"] },
    { id: 17, key: "geraniol", label: "Geraniol", source: "Geraniol", aliases: ["geraniol"] },
    { id: 18, key: "bcaryophyllene", label: "β-Caryophyllene", source: "beta-Caryophyllene", aliases: ["Beta-Caryophyllene", "beta caryophyllene", "β-Caryophyllene"] },
    { id: 19, key: "ahumulene", label: "α-Humulene", source: "alpha-Humulene", aliases: ["Alpha-Humulene", "alpha humulene", "α-Humulene"] },
    { id: 20, key: "cisnerolidol", label: "cis-Nerolidol", source: "Nerolidol 1", aliases: ["nerolidol-1", "cis-Nerolidol", "cis nerolidol"] },
    { id: 21, key: "transnerolidol", label: "trans-Nerolidol", source: "Nerolidol 2", aliases: ["nerolidol-2", "trans-Nerolidol", "trans nerolidol"] },
    { id: 22, key: "guaiol", label: "(-)-Guaiol", source: "(-)-Guaiol", aliases: ["Guaiol", "guaiol"] },
    { id: 23, key: "caryophylleneoxide", label: "Caryophyllene Oxide", source: "Caryophyllene oxide", aliases: ["Caryophyllene Oxide", "caryophyllene oxide"] },
    { id: 24, key: "bisabolol", label: "(-)-α-Bisabolol", source: "(-)-alpha-Bisabolol", aliases: ["alpha-Bisabolol", "Alpha-Bisabolol", "(-)-α-Bisabolol"] },
  ]);
  const AUDIT_ANALYTE = Object.freeze({
    id: 1,
    key: "dimethylacetamide",
    label: "Dimethylacetamide",
    source: "Dimethylacetamide",
    aliases: ["dimethylacetamide"],
  });
  const ALL_ANALYTES = Object.freeze([AUDIT_ANALYTE].concat(REPORTABLE_ANALYTES));
  const RESULTS_HEADERS = Object.freeze([
    "Sample ID",
    "Test ID",
    "Product Matrix",
    "LabSolutions Sample Name",
    "Sample Type",
    "Vial",
    "Sample Amount",
    "Dilution Factor",
    "DF Application Mode",
    ...REPORTABLE_ANALYTES.map((analyte) => analyte.label),
    "Dimethylacetamide",
    "Unknown Peak Count",
    "Manual Integration",
    "Integration Review Status",
    "Source Instrument File",
    "Source File Hash",
    "Source Data File",
    "Source Method File",
    "Source Sequence File",
    "Acquired At",
    "Instrument Name",
    "Detector ID",
    "Detector Name",
    "Parser Version",
    "Compound Result Row Count",
    "Peak Table Row Count",
    "Reportable Compound Row Count",
    "Source Row Hash",
    "Import Status",
  ]);
  const AUDIT_HEADERS = Object.freeze([
    "Record Order",
    "Record Category",
    "LabSolutions Sample ID",
    ...RESULTS_HEADERS.slice(PARSER_FIRST_COLUMN),
  ]);
  const AUDIT_SECTION_VALUES = Object.freeze([
    "Run Records",
    "Complete LabSolutions sequence audit",
    ...Array(RESULTS_HEADERS.length - 2).fill(""),
  ]);

  class SimpleResultsError extends Error {
    constructor(code, message, details) {
      super(String(message || code).slice(0, LIMITS.maximum_error_message_length));
      this.name = "SimpleResultsError";
      this.code = code;
      this.details = details || {};
    }
  }

  function fail(code, message, details) {
    throw new SimpleResultsError(code, message, details);
  }

  function cellText(value) {
    return value === undefined || value === null ? "" : String(value).trim();
  }

  function columnLetter(index) {
    let result = "";
    let value = index + 1;
    while (value > 0) {
      const digit = (value - 1) % 26;
      result = String.fromCharCode(65 + digit) + result;
      value = Math.floor((value - 1) / 26);
    }
    return result;
  }

  function a1(column, row) {
    return `${columnLetter(column)}${row}`;
  }

  function utf8Bytes(text) {
    const encoded = unescape(encodeURIComponent(String(text)));
    const bytes = [];
    for (let index = 0; index < encoded.length; index += 1) bytes.push(encoded.charCodeAt(index));
    return bytes;
  }

  function byteView(input) {
    if (input instanceof Uint8Array) return input;
    if (typeof ArrayBuffer !== "undefined" && input instanceof ArrayBuffer) return new Uint8Array(input);
    if (typeof ArrayBuffer !== "undefined" && ArrayBuffer.isView && ArrayBuffer.isView(input)) {
      return new Uint8Array(input.buffer, input.byteOffset, input.byteLength);
    }
    fail("UNSUPPORTED_INPUT_TYPE", "Source input must be an exact byte sequence.");
  }

  function sha256BytesHex(input) {
    const bytes = byteView(input);
    const words = [];
    const bitLength = bytes.length * 8;
    for (let index = 0; index < bytes.length; index += 1) {
      words[index >> 2] = (words[index >> 2] || 0) | (bytes[index] << (24 - (index % 4) * 8));
    }
    words[bitLength >> 5] = (words[bitLength >> 5] || 0) | (0x80 << (24 - (bitLength % 32)));
    words[((bitLength + 64 >> 9) << 4) + 15] = bitLength;
    const constants = [
      0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
      0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
      0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
      0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
      0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
      0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
      0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
      0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
    ];
    let h0 = 0x6a09e667;
    let h1 = 0xbb67ae85;
    let h2 = 0x3c6ef372;
    let h3 = 0xa54ff53a;
    let h4 = 0x510e527f;
    let h5 = 0x9b05688c;
    let h6 = 0x1f83d9ab;
    let h7 = 0x5be0cd19;
    for (let offset = 0; offset < words.length; offset += 16) {
      const schedule = [];
      for (let index = 0; index < 64; index += 1) {
        if (index < 16) schedule[index] = words[offset + index] || 0;
        else {
          const left = schedule[index - 15];
          const right = schedule[index - 2];
          const s0 = ((left >>> 7) | (left << 25)) ^ ((left >>> 18) | (left << 14)) ^ (left >>> 3);
          const s1 = ((right >>> 17) | (right << 15)) ^ ((right >>> 19) | (right << 13)) ^ (right >>> 10);
          schedule[index] = (((schedule[index - 16] + s0) | 0) + ((schedule[index - 7] + s1) | 0)) | 0;
        }
      }
      let a = h0;
      let b = h1;
      let c = h2;
      let d = h3;
      let e = h4;
      let f = h5;
      let g = h6;
      let h = h7;
      for (let index = 0; index < 64; index += 1) {
        const rotateE = ((e >>> 6) | (e << 26)) ^ ((e >>> 11) | (e << 21)) ^ ((e >>> 25) | (e << 7));
        const choose = (e & f) ^ ((~e) & g);
        const temp1 = (((h + rotateE) | 0) + ((choose + constants[index]) | 0) + schedule[index]) | 0;
        const rotateA = ((a >>> 2) | (a << 30)) ^ ((a >>> 13) | (a << 19)) ^ ((a >>> 22) | (a << 10));
        const majority = (a & b) ^ (a & c) ^ (b & c);
        const temp2 = (rotateA + majority) | 0;
        h = g;
        g = f;
        f = e;
        e = (d + temp1) | 0;
        d = c;
        c = b;
        b = a;
        a = (temp1 + temp2) | 0;
      }
      h0 = (h0 + a) | 0;
      h1 = (h1 + b) | 0;
      h2 = (h2 + c) | 0;
      h3 = (h3 + d) | 0;
      h4 = (h4 + e) | 0;
      h5 = (h5 + f) | 0;
      h6 = (h6 + g) | 0;
      h7 = (h7 + h) | 0;
    }
    return [h0, h1, h2, h3, h4, h5, h6, h7]
      .map((value) => (value >>> 0).toString(16).padStart(8, "0"))
      .join("");
  }

  function sha256Hex(input) {
    return sha256BytesHex(Uint8Array.from(utf8Bytes(input)));
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

  function buildAliasMap() {
    const aliases = new Map();
    ALL_ANALYTES.forEach((analyte) => {
      [analyte.label, analyte.source].concat(analyte.aliases || []).forEach((alias) => {
        const normalized = normalizeAnalyteName(alias);
        const prior = aliases.get(normalized);
        if (prior && prior.key !== analyte.key) fail("ANALYTE_CONFIGURATION_INVALID", "Controlled analyte aliases conflict.");
        aliases.set(normalized, analyte);
      });
    });
    return aliases;
  }

  function normalizeSourceText(input) {
    if (typeof input !== "string") fail("UNSUPPORTED_INPUT_TYPE", "LabSolutions source must be UTF-8 text.");
    if (utf8Bytes(input).length > LIMITS.maximum_raw_file_size_bytes) {
      fail("RAW_FILE_TOO_LARGE", "LabSolutions source exceeds the controlled file-size limit.");
    }
    const withoutBom = input.charCodeAt(0) === 0xfeff ? input.slice(1) : input;
    return withoutBom.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  }

  function decodeSourceBytes(input, TextDecoderCtor) {
    const bytes = byteView(input);
    if (bytes.length > LIMITS.maximum_raw_file_size_bytes) {
      fail("RAW_FILE_TOO_LARGE", "LabSolutions source exceeds the controlled file-size limit.");
    }
    const sourceFileHash = sha256BytesHex(bytes);
    if (bytes.length >= 3 && bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf) {
      fail("SOURCE_UTF8_BOM_NOT_ALLOWED", "UTF-8 BOM is not allowed in the LabSolutions source.");
    }
    if (typeof TextDecoderCtor !== "function") {
      fail("SOURCE_UTF8_INVALID", "Fatal UTF-8 decoding is unavailable.");
    }
    let text;
    try {
      text = new TextDecoderCtor("utf-8", { fatal: true }).decode(bytes);
    } catch (_error) {
      fail("SOURCE_UTF8_INVALID", "LabSolutions source is not valid UTF-8.");
    }
    return { bytes, text, source_file_hash: sourceFileHash };
  }

  function splitCompleteRecords(input) {
    const normalized = normalizeSourceText(input);
    const lines = normalized.split("\n");
    const starts = [];
    lines.forEach((line, index) => {
      if (line.length > LIMITS.maximum_line_length) fail("LINE_TOO_LONG", "LabSolutions source contains an overlong line.");
      if (/^\[Header\]\s*$/.test(line)) starts.push(index);
    });
    if (!starts.length) fail("MISSING_RECORD_HEADER", "LabSolutions source contains no complete record boundary.");
    if (starts.length > LIMITS.maximum_record_count) fail("TOO_MANY_RECORDS", "LabSolutions source exceeds the controlled record limit.");
    if (lines.slice(0, starts[0]).some((line) => line.trim())) {
      fail("UNEXPECTED_PREAMBLE", "Nonblank data appears before the first LabSolutions record.");
    }
    return starts.map((start, index) => lines.slice(start, starts[index + 1]).join("\n"));
  }

  function splitSections(recordText) {
    const sections = new Map();
    let current = null;
    recordText.split("\n").forEach((line, lineIndex) => {
      const marker = line.match(/^\[(.+)]\s*$/);
      if (marker) {
        current = marker[1];
        if (sections.has(current)) fail("DUPLICATE_SECTION", `Repeated section ${current}.`, { line: lineIndex + 1 });
        sections.set(current, []);
        if (sections.size > LIMITS.maximum_section_count) fail("TOO_MANY_SECTIONS", "Record exceeds the controlled section limit.");
      } else if (current) sections.get(current).push(line);
    });
    REQUIRED_SECTIONS.forEach((section) => {
      if (!sections.has(section)) fail("MISSING_REQUIRED_SECTION", `Missing required section: ${section}.`, { section });
    });
    return sections;
  }

  function parseNumberStrict(value, field, section, row) {
    const text = String(value).trim();
    if (text === "") return "";
    if (!/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$/.test(text)) {
      fail("INVALID_NUMERIC_VALUE", `Invalid numeric value in ${field}.`, { field, section, row });
    }
    const parsed = Number(text);
    if (!Number.isFinite(parsed)) fail("INVALID_NUMERIC_VALUE", `Non-finite numeric value in ${field}.`, { field, section, row });
    return parsed;
  }

  function parseScalar(field, value, section, row) {
    return NUMERIC_FIELDS.has(field)
      ? parseNumberStrict(value, field, section, row)
      : String(value).trim();
  }

  function parseKeyValueSection(sections, sectionName) {
    const output = {};
    (sections.get(sectionName) || []).forEach((line, index) => {
      if (!line.trim()) return;
      const cells = line.split("\t");
      if (cells.length < 2 || cells.length > LIMITS.maximum_field_count) {
        fail("MALFORMED_KEY_VALUE_ROW", `Malformed row in ${sectionName}.`, { section: sectionName, row: index + 1 });
      }
      const key = String(cells.shift()).trim();
      if (!key || Object.prototype.hasOwnProperty.call(output, key)) {
        fail("MALFORMED_KEY_VALUE_ROW", `Duplicate or blank key in ${sectionName}.`, { section: sectionName, row: index + 1 });
      }
      output[key] = parseScalar(key, cells.join("\t"), sectionName, index + 1);
    });
    return output;
  }

  function parseTable(sections, sectionName, headerPrefix, aliasMap) {
    let headers = null;
    const rows = [];
    (sections.get(sectionName) || []).forEach((line) => {
      if (!line.trim() || line.indexOf("# of") === 0) return;
      if (line.indexOf(headerPrefix) === 0) {
        if (headers) fail("AMBIGUOUS_TABLE_HEADER", `More than one table header in ${sectionName}.`);
        headers = line.split("\t");
        if (headers.length > LIMITS.maximum_field_count) fail("TOO_MANY_FIELDS", `Too many fields in ${sectionName}.`);
        return;
      }
      if (!headers) return;
      const cells = line.split("\t");
      if (cells.length !== headers.length) {
        fail("MALFORMED_TABLE_ROW", `Row width mismatch in ${sectionName}.`, { section: sectionName, row: rows.length + 1 });
      }
      if (rows.length >= LIMITS.maximum_table_row_count) fail("TOO_MANY_TABLE_ROWS", `Too many rows in ${sectionName}.`);
      const row = {};
      headers.forEach((header, column) => {
        row[header] = parseScalar(header, cells[column], sectionName, rows.length + 1);
      });
      const analyte = aliasMap.get(normalizeAnalyteName(row.Name));
      row.internal_key = analyte ? analyte.key : "";
      row.configured_id = analyte ? analyte.id : null;
      row.reportable = analyte ? analyte.id !== AUDIT_ANALYTE.id : false;
      row.unconfigured_analyte = !analyte;
      rows.push(row);
    });
    if (!headers) fail("MISSING_TABLE_HEADER", `Missing table header in ${sectionName}.`, { section: sectionName });
    return rows;
  }

  function validateCompoundResults(rows) {
    const errors = [];
    const counts = new Map();
    if (rows.length !== 24) errors.push(`expected 24 rows, found ${rows.length}`);
    rows.forEach((row) => {
      if (row.unconfigured_analyte) {
        errors.push(`unknown analyte ${cellText(row.Name) || "<blank>"}`);
        return;
      }
      counts.set(row.internal_key, (counts.get(row.internal_key) || 0) + 1);
      if (row["ID#"] !== row.configured_id) errors.push(`ID/name mismatch for ${cellText(row.Name)}`);
      if (typeof row["Conc."] !== "number") errors.push(`non-numeric concentration for ${cellText(row.Name)}`);
    });
    ALL_ANALYTES.forEach((analyte) => {
      if ((counts.get(analyte.key) || 0) !== 1) errors.push(`controlled analyte count for ${analyte.key} is not one`);
    });
    if (rows.filter((row) => row.reportable).length !== 23) errors.push("reportable analyte count is not 23");
    if (errors.length) {
      fail("INVALID_CONTROLLED_COMPOUND_RESULTS", `Invalid Compound Results(Ch1): ${Array.from(new Set(errors)).join(" | ")}`);
    }
  }

  function isValidationLabel(value) {
    return /^(?:low|medium|high)(?:\s+\d+)?$/i.test(cellText(value));
  }

function classifyRecord(sampleInformation) {
  const sampleType = cellText(sampleInformation["Sample Type"]);
  const sampleName = cellText(sampleInformation["Sample Name"]);
  const sampleId = cellText(sampleInformation["Sample ID"]);
  const combined = `${sampleType} ${sampleName} ${sampleId}`.toLowerCase();

  // Preserve the existing specific control categories first.
  if (/system\s*suit/.test(combined)) return "System Suitability";
  if (/\bccv\b/.test(combined)) return "CCV";
  if (/matrix\s*blank|blank\s*matrix/.test(combined)) {
    return "Matrix Blank";
  }
  if (/\bmatrix\s*spike\b/.test(combined)) return "Matrix Spike";
  if (/\bnull\b/.test(combined)) return "Null";
  if (/\bblank\b/.test(combined)) return "Blank";
  if (/\bloq\b/.test(combined)) return "LOQ";

  // Accept both "Standard 1" and "Std 1" formatting.
  if (/\bstandard\b|\bstd(?:\s*\d+)?\b/.test(combined)) {
    return "Standard";
  }

  // Preserve the existing Low/Medium/High validation classification.
  if (isValidationLabel(sampleName) || isValidationLabel(sampleId)) {
    return "Validation";
  }

  // Operational QC labels that are not one of the specific categories above.
  if (/\bqc(?:\s*\d+)?\b|\blcs\b/.test(combined)) {
    return "Other QC";
  }

  // Final defensive control rule:
  // a LabSolutions Control record must never be treated as a QBench Test.
  if (/control/i.test(sampleType)) {
    return "Other QC";
  }

  return "Sample";
}

  function detectManualIntegration(peakRows) {
    return peakRows.some((row) => {
      const mark = cellText(row.Mark);
      return /manual/i.test(mark) || mark.split(/[\s,;/]+/).some((token) => token.toUpperCase() === "M");
    });
  }

  function countUnknownPeaks(peakRows) {
    return peakRows.filter((row) => {
      const name = cellText(row.Name);
      return row.unconfigured_analyte || !name || /unknown|unidentified/i.test(name);
    }).length;
  }

  function parseRecord(recordText, recordOrder, aliasMap) {
    const sections = splitSections(recordText);
    const compoundResults = parseTable(sections, "Compound Results(Ch1)", "ID#", aliasMap);
    const peakTable = parseTable(sections, "Peak Table(Ch1)", "Peak#", aliasMap);
    validateCompoundResults(compoundResults);
    const sampleInformation = parseKeyValueSection(sections, "Sample Information");
    const originalFiles = parseKeyValueSection(sections, "Original Files");
    const configuration = parseKeyValueSection(sections, "Configuration");
    const header = parseKeyValueSection(sections, "Header");
    const byKey = new Map(compoundResults.map((row) => [row.internal_key, row]));
    const reportableAnalytes = REPORTABLE_ANALYTES.map((analyte) => ({
      order: analyte.id - 1,
      internal_key: analyte.key,
      worksheet_label: analyte.label,
      source_id: analyte.id,
      source_name: byKey.get(analyte.key).Name,
      conc: byKey.get(analyte.key)["Conc."],
    }));
    const unknownPeakCount = countUnknownPeaks(peakTable);
    const manualIntegration = detectManualIntegration(peakTable);
    const category = classifyRecord(sampleInformation);
    return {
      record_order: recordOrder,
      category,
      header,
      sample_information: sampleInformation,
      original_files: originalFiles,
      configuration,
      compound_results: compoundResults,
      peak_table: peakTable,
      reportable_analytes: reportableAnalytes,
      dimethylacetamide_audit: {
        internal_key: AUDIT_ANALYTE.key,
        source_id: AUDIT_ANALYTE.id,
        source_name: byKey.get(AUDIT_ANALYTE.key).Name,
        conc: byKey.get(AUDIT_ANALYTE.key)["Conc."],
        reportable: false,
      },
      counts: {
        compound_result_row_count: compoundResults.length,
        peak_table_row_count: peakTable.length,
        reportable_compound_row_count: reportableAnalytes.length,
      },
      unknown_peak_count: unknownPeakCount,
      manual_integration: manualIntegration,
      integration_review_status: unknownPeakCount || manualIntegration ? "Review Required" : "Not Reviewed",
      source_row_hash: sha256Hex(recordText),
    };
  }

  function parseSource(input, sourceFileHash) {
    if (REPORTABLE_ANALYTES.length !== 23 || ALL_ANALYTES.length !== 24) {
      fail("ANALYTE_CONFIGURATION_INVALID", "Controlled analyte counts are invalid.");
    }
    if (!/^[a-f0-9]{64}$/.test(cellText(sourceFileHash))) {
      fail("SOURCE_FILE_HASH_REQUIRED", "An exact uploaded-byte SHA-256 is required.");
    }
    const aliasMap = buildAliasMap();
    const recordTexts = splitCompleteRecords(input);
    if (recordTexts.length > AUDIT_CAPACITY) {
      fail("RUN_RECORD_CAPACITY_EXCEEDED", `Run Records capacity is ${AUDIT_CAPACITY} complete records.`);
    }
    const records = recordTexts.map((recordText, index) => parseRecord(recordText, index + 1, aliasMap));
    return {
      parser_core_version: CORE_VERSION,
      source_file_hash: sourceFileHash,
      records,
      record_count: records.length,
    };
  }

  function parseSourceBytes(input, TextDecoderCtor) {
    const decoded = decodeSourceBytes(input, TextDecoderCtor);
    return parseSource(decoded.text, decoded.source_file_hash);
  }

function candidateTestId(record) {
  if (!record || record.category !== "Sample") {
    return "";
  }

  const sample = record.sample_information || {};
  const sampleType = cellText(sample["Sample Type"]);
  const sampleName = cellText(sample["Sample Name"]);

  // Defense in depth: even if classification changes later,
  // a LabSolutions Control record can never resolve as a QBench Test.
  if (/control/i.test(sampleType)) {
    return "";
  }

  // Current QBench Test display IDs are numeric.
  // This excludes CCV 1, QC 1, LOQ, Blank, Std 1, etc.
  if (!/^\d+$/.test(sampleName)) {
    return "";
  }

  return sampleName;
}

  function requireUniqueCandidates(records) {
    const candidates = records.filter((record) => candidateTestId(record));
    const seen = new Set();
    candidates.forEach((record) => {
      const id = candidateTestId(record);
      if (seen.has(id)) fail("DUPLICATE_CANDIDATE_TEST_ID", "Candidate Test IDs must be unique.");
      seen.add(id);
    });
    if (!candidates.length) fail("NO_SAMPLE_TEST_IDS", "No eligible Sample record contains a numeric QBench Test display ID in LabSolutions Sample Name.");
    return candidates;
  }

  function buildParserOwnedValues(record, sourceFileHash) {
    const sample = record.sample_information;
    const files = record.original_files;
    const configuration = record.configuration;
    const values = [
      cellText(sample["Sample Name"]),
      cellText(sample["Sample Type"]),
      sample["Vial#"] === undefined ? "" : sample["Vial#"],
      sample["Sample Amount"] === undefined ? "" : sample["Sample Amount"],
      sample["Dilution Factor"] === undefined ? "" : sample["Dilution Factor"],
      "already_applied_by_labsolutions",
      ...record.reportable_analytes.map((analyte) => analyte.conc),
      record.dimethylacetamide_audit.conc,
      record.unknown_peak_count,
      record.manual_integration ? "Yes" : "No",
      record.integration_review_status,
      cellText(record.header["Data File Name"] || files["Data File"]),
      sourceFileHash,
      cellText(files["Data File"]),
      cellText(files["Method File"]),
      cellText(files["Batch File"]),
      cellText(sample.Acquired),
      cellText(configuration["Instrument Name"]),
      cellText(configuration["Detector ID"]),
      cellText(configuration["Detector Name"]),
      VERSION,
      record.counts.compound_result_row_count,
      record.counts.peak_table_row_count,
      record.counts.reportable_compound_row_count,
      record.source_row_hash,
      "Imported",
    ];
    if (values.length !== PARSER_LAST_COLUMN - PARSER_FIRST_COLUMN + 1) {
      fail("RESULTS_VALUE_CONTRACT_INVALID", "Parser-owned Results value count is invalid.");
    }
    return values;
  }

  function buildAuditValues(record, sourceFileHash) {
    const values = [
      record.record_order,
      record.category,
      cellText(record.sample_information["Sample ID"]),
      ...buildParserOwnedValues(record, sourceFileHash),
    ];
    values[RESULTS_HEADERS.indexOf("Source Row Hash")] = sha256Hex(`${sourceFileHash}:${record.record_order}`);
    if (values.length !== AUDIT_HEADERS.length) {
      fail("AUDIT_VALUE_CONTRACT_INVALID", "Run Records audit value count is invalid.");
    }
    return values;
  }

  function documentList(payload) {
    if (Array.isArray(payload)) return payload;
    if (payload && Array.isArray(payload.data)) return payload.data;
    if (payload && typeof payload === "object") return Object.values(payload).filter((value) => value && typeof value === "object");
    return [];
  }

  function worksheetDocument(documents, type) {
    const matches = documents.filter((item) => item && item.worksheet_name === RESULTS_TAB && item.type === type);
    if (matches.length !== 1) fail("RESULTS_WORKSHEET_DOCUMENT_INVALID", `Expected one Results ${type} document.`);
    return matches[0];
  }

  function worksheetGrid(documents, type) {
    const value = worksheetDocument(documents, type).data;
    if (!Array.isArray(value)) fail("RESULTS_WORKSHEET_DOCUMENT_INVALID", `${type} must be a worksheet grid.`);
    return value;
  }

  function worksheetMap(documents, type) {
    const value = worksheetDocument(documents, type).data;
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      fail("RESULTS_WORKSHEET_DOCUMENT_INVALID", `${type} must be a worksheet map.`);
    }
    return value;
  }

  function requireResultsBundle(payload) {
    const documents = documentList(payload);
    const worksheetNames = Array.from(new Set(documents.map((item) => item && item.worksheet_name).filter(Boolean)));
    if (worksheetNames.length !== 1 || worksheetNames[0] !== RESULTS_TAB) {
      fail("RESULTS_WORKSHEET_CONTRACT_INVALID", "Dynamic Batch worksheet must contain exactly one worksheet named Results.");
    }
    const rawGrid = worksheetGrid(documents, "WORKSHEET_DATA");
    const processedGrid = worksheetGrid(documents, "WORKSHEET_DATA_PROCESSED");
    if (rawGrid.length !== WORKSHEET_LAST_ROW || processedGrid.length !== WORKSHEET_LAST_ROW) {
      fail("RESULTS_WORKSHEET_DIMENSIONS_INVALID", "Results worksheet must contain exactly 51 columns and 190 rows.");
    }
    if (rawGrid.some((row) => !Array.isArray(row) || row.length !== RESULTS_HEADERS.length)
      || processedGrid.some((row) => !Array.isArray(row) || row.length !== RESULTS_HEADERS.length)) {
      fail("RESULTS_WORKSHEET_DIMENSIONS_INVALID", "Results worksheet must contain exactly 51 columns through AY.");
    }
    const header = processedGrid[0] || rawGrid[0] || [];
    if (header.length !== RESULTS_HEADERS.length || header.some((value, index) => value !== RESULTS_HEADERS[index])) {
      fail("RESULTS_HEADER_MISMATCH", "Results worksheet header contract does not match A:AY.");
    }
    for (let column = 0; column < RESULTS_HEADERS.length; column += 1) {
      if (cellText(visibleCell(rawGrid, processedGrid, AUDIT_SEPARATOR_ROW, column))) {
        fail("RUN_RECORD_SEPARATOR_MISMATCH", "Results row 88 must remain blank.");
      }
      if (!exactCellEqual(
        visibleCell(rawGrid, processedGrid, AUDIT_SECTION_ROW, column),
        AUDIT_SECTION_VALUES[column],
      )) {
        fail("RUN_RECORD_SECTION_MISMATCH", "Results row 89 Run Records label contract changed.");
      }
      if (!exactCellEqual(
        visibleCell(rawGrid, processedGrid, AUDIT_HEADER_ROW, column),
        AUDIT_HEADERS[column],
      )) {
        fail("RUN_RECORD_HEADER_MISMATCH", "Results row 90 audit header contract changed.");
      }
    }
    return {
      documents,
      rawGrid,
      processedGrid,
      formulas: worksheetMap(documents, "WORKSHEET_FORMULAS"),
      images: worksheetMap(documents, "WORKSHEET_IMAGE_DATA"),
      references: worksheetMap(documents, "WORKSHEET_DOLLAR_REFERENCES"),
    };
  }

  function visibleCell(rawGrid, processedGrid, row, column) {
    const processedRow = processedGrid[row - 1] || [];
    const rawRow = rawGrid[row - 1] || [];
    const processed = processedRow[column];
    return processed === undefined || processed === null || processed === "" ? rawRow[column] : processed;
  }

  function buildTestRowIndex(rawGrid, processedGrid, references) {
    const index = {};
    const referenceIds = new Map();
    Object.entries(references || {}).forEach(([address, value]) => {
      const match = address.match(/^B(\d+)$/i);
      if (!match) return;
      const row = Number(match[1]);
      if (row < FIRST_DATA_ROW || row > LAST_DATA_ROW) return;
      const id = cellText(value);
      if (!id) return;
      const prior = referenceIds.get(row);
      if (prior && prior !== id) {
        fail("RESULTS_TEST_CONTEXT_MISMATCH", `Results row ${row} has conflicting Test references.`, { row });
      }
      referenceIds.set(row, id);
    });
    for (let row = FIRST_DATA_ROW; row <= LAST_DATA_ROW; row += 1) {
      const visibleId = cellText(visibleCell(rawGrid, processedGrid, row, 1));
      const referenceId = referenceIds.get(row) || "";
      if (visibleId && referenceId && visibleId !== referenceId) {
        fail("RESULTS_TEST_CONTEXT_MISMATCH", `Results row ${row} Test context does not agree.`, { row });
      }
      const effectiveId = visibleId || referenceId;
      if (!effectiveId) continue;
      if (index[effectiveId] && !index[effectiveId].has(row)) {
        fail("RESULTS_TEST_ID_DUPLICATE", `Test ID ${effectiveId} appears on more than one Results row.`);
      }
      if (!index[effectiveId]) index[effectiveId] = new Set();
      index[effectiveId].add(row);
    }
    return index;
  }

  function cloneGrid(grid) {
    return (grid || []).map((row) => (row || []).slice());
  }

  function cloneMap(value) {
    return JSON.parse(JSON.stringify(value || {}));
  }

  function gridToMap(grid) {
    const output = {};
    (grid || []).forEach((row, rowIndex) => {
      (row || []).forEach((value, columnIndex) => {
        if (value !== undefined && value !== null && value !== "") output[a1(columnIndex, rowIndex + 1)] = value;
      });
    });
    return output;
  }

  function setMapCell(dataMap, processedMap, column, row, value) {
    const address = a1(column, row);
    const nativeValue = value === undefined || value === null ? "" : value;
    dataMap[address] = nativeValue;
    processedMap[address] = nativeValue === "" ? "" : String(nativeValue);
  }

  function planCandidateRows(bundle, candidates, sourceFileHash) {
    const index = buildTestRowIndex(bundle.rawGrid, bundle.processedGrid, bundle.references);
    const plans = candidates.map((record) => {
      const id = candidateTestId(record);
      const rows = index[id] ? Array.from(index[id]) : [];
      if (!rows.length) fail("RESULTS_TEST_ID_MISSING", `Candidate Test ID ${id} is missing from Results.`);
      if (rows.length !== 1) fail("RESULTS_TEST_ID_DUPLICATE", `Candidate Test ID ${id} appears more than once in Results.`);
      return {
        id,
        row: rows[0],
        record,
        values: buildParserOwnedValues(record, sourceFileHash),
      };
    });
    requireDistinctCandidateRows(plans);
    return plans;
  }

  function requireDistinctCandidateRows(plans) {
    const rows = new Set();
    (plans || []).forEach((plan) => {
      if (rows.has(plan.row)) {
        fail("RESULTS_TEST_ROW_ALIAS", `More than one candidate resolves to Results row ${plan.row}.`, { row: plan.row });
      }
      rows.add(plan.row);
    });
    return plans;
  }

  function planAuditRows(bundle, records, sourceFileHash) {
    if (!records.length) fail("NO_COMPLETE_RECORDS", "At least one complete LabSolutions record is required.");
    if (records.length > AUDIT_CAPACITY) {
      fail("RUN_RECORD_CAPACITY_EXCEEDED", `Run Records capacity is ${AUDIT_CAPACITY} complete records.`);
    }
    const rows = records.map((record, index) => ({
      record_order: record.record_order,
      row: AUDIT_FIRST_DATA_ROW + index,
      record,
      values: buildAuditValues(record, sourceFileHash),
    }));
    const staleCells = [];
    const staleRows = new Set();
    for (let row = AUDIT_FIRST_DATA_ROW + records.length; row <= AUDIT_LAST_DATA_ROW; row += 1) {
      for (let column = 0; column < AUDIT_HEADERS.length; column += 1) {
        const rawValue = (bundle.rawGrid[row - 1] || [])[column];
        const processedValue = (bundle.processedGrid[row - 1] || [])[column];
        if (cellText(rawValue) || cellText(processedValue)) {
          staleCells.push({ row, column });
          staleRows.add(row);
        }
      }
    }
    return {
      rows,
      stale_cells: staleCells,
      stale_rows: Array.from(staleRows).sort((left, right) => left - right),
    };
  }

  function applyResultsPlans(bundle, candidatePlans, auditPlan) {
    const dataMap = gridToMap(bundle.rawGrid);
    const processedMap = gridToMap(bundle.processedGrid);
    candidatePlans.forEach((plan) => {
      plan.values.forEach((value, offset) => {
        setMapCell(dataMap, processedMap, PARSER_FIRST_COLUMN + offset, plan.row, value);
      });
    });
    auditPlan.rows.forEach((plan) => {
      plan.values.forEach((value, column) => {
        setMapCell(dataMap, processedMap, column, plan.row, value);
      });
    });
    auditPlan.stale_cells.forEach(({ row, column }) => {
      setMapCell(dataMap, processedMap, column, row, "");
    });
    return {
      WORKSHEET_DATA: dataMap,
      WORKSHEET_FORMULAS: cloneMap(bundle.formulas),
      WORKSHEET_IMAGE_DATA: cloneMap(bundle.images),
      WORKSHEET_DOLLAR_REFERENCES: cloneMap(bundle.references),
      WORKSHEET_DATA_PROCESSED: processedMap,
    };
  }

  function stableValue(value) {
    if (Array.isArray(value)) return value.map(stableValue);
    if (value && typeof value === "object") {
      const output = {};
      Object.keys(value).sort().forEach((key) => { output[key] = stableValue(value[key]); });
      return output;
    }
    return value;
  }

  function mapsEqual(left, right) {
    return JSON.stringify(stableValue(left || {})) === JSON.stringify(stableValue(right || {}));
  }

  function exactCellEqual(left, right) {
    const normalizedLeft = left === undefined || left === null ? "" : left;
    const normalizedRight = right === undefined || right === null ? "" : right;
    return Object.is(normalizedLeft, normalizedRight);
  }

  function persistedCellEqual(expected, actual) {
    if (expected === "" || expected === undefined || expected === null) return cellText(actual) === "";
    if (typeof expected === "number") {
      if (typeof actual === "number") return Number.isFinite(actual) && actual === expected;
      const text = cellText(actual);
      return /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$/.test(text)
        && Number.isFinite(Number(text))
        && Number(text) === expected;
    }
    return String(actual === undefined || actual === null ? "" : actual) === String(expected);
  }

  function verifyReadback(before, readbackPayload, candidatePlans, auditPlan) {
    try {
      const after = requireResultsBundle(readbackPayload);
      const index = buildTestRowIndex(after.rawGrid, after.processedGrid, after.references);
      const matchedRows = new Set();
      candidatePlans.forEach((plan) => {
        const rows = index[plan.id] ? Array.from(index[plan.id]) : [];
        if (rows.length !== 1 || rows[0] !== plan.row) throw new Error("candidate row identity changed");
        matchedRows.add(plan.row);
      });
      if (matchedRows.size !== candidatePlans.length) throw new Error("candidate row count changed");

      for (let row = FIRST_DATA_ROW; row <= LAST_DATA_ROW; row += 1) {
        for (let column = 0; column <= CONTEXT_LAST_COLUMN; column += 1) {
          const beforeRaw = (before.rawGrid[row - 1] || [])[column];
          const afterRaw = (after.rawGrid[row - 1] || [])[column];
          const beforeProcessed = (before.processedGrid[row - 1] || [])[column];
          const afterProcessed = (after.processedGrid[row - 1] || [])[column];
          if (!exactCellEqual(beforeRaw, afterRaw) || !exactCellEqual(beforeProcessed, afterProcessed)) {
            throw new Error("context-owned cell changed");
          }
        }
        if (!matchedRows.has(row)) {
          for (let column = 0; column < RESULTS_HEADERS.length; column += 1) {
            const beforeRaw = (before.rawGrid[row - 1] || [])[column];
            const afterRaw = (after.rawGrid[row - 1] || [])[column];
            const beforeProcessed = (before.processedGrid[row - 1] || [])[column];
            const afterProcessed = (after.processedGrid[row - 1] || [])[column];
            if (!exactCellEqual(beforeRaw, afterRaw) || !exactCellEqual(beforeProcessed, afterProcessed)) {
              throw new Error("unmatched Results row changed");
            }
          }
        }
      }

      candidatePlans.forEach((plan) => {
        plan.values.forEach((expected, offset) => {
          const column = PARSER_FIRST_COLUMN + offset;
          const rawValue = (after.rawGrid[plan.row - 1] || [])[column];
          const processedValue = (after.processedGrid[plan.row - 1] || [])[column];
          if (!persistedCellEqual(expected, rawValue) || !persistedCellEqual(expected, processedValue)) {
            throw new Error(`persisted value mismatch at ${a1(column, plan.row)}`);
          }
        });
      });

      [1, AUDIT_SEPARATOR_ROW, AUDIT_SECTION_ROW, AUDIT_HEADER_ROW].forEach((row) => {
        for (let column = 0; column < RESULTS_HEADERS.length; column += 1) {
          const beforeRaw = (before.rawGrid[row - 1] || [])[column];
          const afterRaw = (after.rawGrid[row - 1] || [])[column];
          const beforeProcessed = (before.processedGrid[row - 1] || [])[column];
          const afterProcessed = (after.processedGrid[row - 1] || [])[column];
          if (!exactCellEqual(beforeRaw, afterRaw) || !exactCellEqual(beforeProcessed, afterProcessed)) {
            throw new Error(`fixed worksheet contract changed at ${a1(column, row)}`);
          }
        }
      });

      const auditRowsByOrder = new Map();
      for (let row = AUDIT_FIRST_DATA_ROW; row <= AUDIT_LAST_DATA_ROW; row += 1) {
        const orderValue = visibleCell(after.rawGrid, after.processedGrid, row, 0);
        if (!cellText(orderValue)) continue;
        const order = Number(orderValue);
        if (!Number.isInteger(order) || order < 1 || order > AUDIT_CAPACITY) {
          throw new Error(`invalid audit record order at A${row}`);
        }
        if (auditRowsByOrder.has(order)) throw new Error(`duplicate audit record order ${order}`);
        auditRowsByOrder.set(order, row);
      }
      if (auditRowsByOrder.size !== auditPlan.rows.length) throw new Error("audit record count changed");

      auditPlan.rows.forEach((plan) => {
        if (auditRowsByOrder.get(plan.record_order) !== plan.row) {
          throw new Error(`audit record ${plan.record_order} row identity changed`);
        }
        plan.values.forEach((expected, column) => {
          const rawValue = (after.rawGrid[plan.row - 1] || [])[column];
          const processedValue = (after.processedGrid[plan.row - 1] || [])[column];
          if (!persistedCellEqual(expected, rawValue) || !persistedCellEqual(expected, processedValue)) {
            throw new Error(`persisted audit value mismatch at ${a1(column, plan.row)}`);
          }
        });
      });

      for (let row = AUDIT_FIRST_DATA_ROW + auditPlan.rows.length; row <= AUDIT_LAST_DATA_ROW; row += 1) {
        for (let column = 0; column < AUDIT_HEADERS.length; column += 1) {
          const rawValue = (after.rawGrid[row - 1] || [])[column];
          const processedValue = (after.processedGrid[row - 1] || [])[column];
          if (cellText(rawValue) || cellText(processedValue)) {
            throw new Error(`unused audit row is not blank at ${a1(column, row)}`);
          }
        }
      }

      if (!mapsEqual(before.formulas, after.formulas)
        || !mapsEqual(before.images, after.images)
        || !mapsEqual(before.references, after.references)) {
        throw new Error("worksheet maps changed");
      }
      return {
        dynamic_rows_verified: candidatePlans.length,
        audit_rows_verified: auditPlan.rows.length,
      };
    } catch (error) {
      fail("RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED", "Results worksheet read-after-write verification failed.", {
        reason: error && error.message ? error.message : String(error),
      });
    }
  }

  function serviceCall(invoke) {
    return new Promise((resolve, reject) => {
      let settled = false;
      const success = (value) => {
        if (!settled) {
          settled = true;
          resolve(value);
        }
      };
      const error = (reason) => {
        if (!settled) {
          settled = true;
          reject(reason);
        }
      };
      try {
        const result = invoke(success, error);
        if (result && typeof result.then === "function") result.then(success, error);
      } catch (reason) {
        error(reason);
      }
    });
  }

  function selectedFiles(filesValue) {
    return Array.isArray(filesValue) ? filesValue : Object.values(filesValue || {});
  }

  function readFileBytes(file, FileReaderCtor) {
    if (file && typeof file.arrayBuffer === "function") {
      return Promise.resolve(file.arrayBuffer()).then((value) => byteView(value));
    }
    return new Promise((resolve, reject) => {
      if (typeof FileReaderCtor !== "function") {
        reject(new SimpleResultsError("FILE_READER_UNAVAILABLE", "FileReader is unavailable."));
        return;
      }
      const reader = new FileReaderCtor();
      reader.onload = (event) => {
        try {
          resolve(byteView(event.target.result));
        } catch (error) {
          reject(error);
        }
      };
      reader.onerror = () => reject(new SimpleResultsError("FILE_READ_FAILED", "The selected source file could not be read."));
      reader.readAsArrayBuffer(file);
    });
  }

  function extractBatchIds(response) {
    const rows = Array.isArray(response) ? response : (response && Array.isArray(response.data) ? response.data : []);
    return Array.from(new Set(rows
      .map((row) => row && row.id)
      .filter((id) => id !== undefined && id !== null && cellText(id))
      .map(String)));
  }

  async function executeRuntime(env) {
    const qb = env.QB;
    const qbConsole = qb.console;
    const progress = qb.progressBar;
    let terminalSignalSent = false;
    const signalError = (error) => {
      const code = error && error.code ? error.code : "UNEXPECTED_SIMPLE_RESULTS_ERROR";
      qbConsole.log(`ERROR: ${code}`);
      if (!terminalSignalSent) {
        terminalSignalSent = true;
        qb.error();
      }
      return {
        ok: false,
        error: {
          code,
          message: String(error && error.message ? error.message : error).slice(0, LIMITS.maximum_error_message_length),
        },
      };
    };

    try {
      progress.setPercentage(0);
      qbConsole.clear();
      const files = selectedFiles(qb.files);
      qbConsole.log(`files selected=${files.length}`);
      if (files.length !== 1) fail("EXACTLY_ONE_TXT_SOURCE_REQUIRED", "Exactly one .txt source file is required.");
      const file = files[0];
      if (!/\.txt$/i.test(cellText(file && file.name))) fail("EXACTLY_ONE_TXT_SOURCE_REQUIRED", "Exactly one .txt source file is required.");
      const sourceBytes = await readFileBytes(file, env.FileReader);
      const parsed = parseSourceBytes(
        sourceBytes,
        env.TextDecoder || (typeof TextDecoder === "function" ? TextDecoder : undefined),
      );
      const candidates = requireUniqueCandidates(parsed.records);
      const sampleRecords = parsed.records.filter((record) => record.category === "Sample");
      const controlRecords = parsed.records.length - sampleRecords.length;
      const skippedRecords = parsed.records.length - candidates.length;
      const warningCount = parsed.records.filter((record) => record.integration_review_status === "Review Required").length;
      qbConsole.log(`records parsed=${parsed.records.length}`);
      qbConsole.log(`control records validated=${controlRecords}`);
      qbConsole.log(`Sample candidates discovered=${candidates.length}`);
      progress.setPercentage(25);

      const batchService = new env.QBBatchService();
      const resolvedBatchIds = [];
      for (const record of candidates) {
        const testId = candidateTestId(record);
        const response = await serviceCall((success, error) => batchService.getJson({
          url: "/batches/get",
          urlParams: { test_id: testId },
          success,
          error,
        }));
        const batchIds = extractBatchIds(response);
        if (!batchIds.length) fail("TEST_ID_NOT_FOUND", "Every candidate Test ID must resolve to exactly one Batch.");
        if (batchIds.length !== 1) fail("TEST_ID_BATCH_AMBIGUOUS", "A candidate Test ID resolves to more than one Batch.");
        resolvedBatchIds.push(batchIds[0]);
      }
      const uniqueBatchIds = Array.from(new Set(resolvedBatchIds));
      if (uniqueBatchIds.length !== 1) fail("CANDIDATES_RESOLVE_TO_MULTIPLE_BATCHES", "All candidate Test IDs must resolve to the same Batch.");
      const batchId = uniqueBatchIds[0];
      qbConsole.log(`Test IDs resolved=${resolvedBatchIds.length}`);
      progress.setPercentage(40);

      const getDynamicWorksheet = () => serviceCall((success, error) => batchService.getJson({
        url: "/batches/worksheets/dynamic",
        urlParams: {
          entity_ids: batchId,
          process_references: true,
          construct_worksheet_data_array: true,
          convert_datetime_values_to_localtime: true,
        },
        success,
        error,
      }));
      const before = requireResultsBundle(await getDynamicWorksheet());
      const candidatePlans = planCandidateRows(before, candidates, parsed.source_file_hash);
      const auditPlan = planAuditRows(before, parsed.records, parsed.source_file_hash);
      qbConsole.log(`dynamic rows staged=${candidatePlans.length}`);
      qbConsole.log(`audit rows staged=${auditPlan.rows.length}`);
      qbConsole.log(`stale audit rows cleared=${auditPlan.stale_rows.length}`);
      const resultsUpdate = applyResultsPlans(before, candidatePlans, auditPlan);
      progress.setPercentage(70);

      await serviceCall((success, error) => batchService.update({
        data: {
          id: String(batchId),
          qb_dynamic_spreadsheet_data: {
            [RESULTS_TAB]: resultsUpdate,
          },
        },
        urlParams: { run_worksheet_calculations: true },
        success,
        error,
      }));
      progress.setPercentage(85);

      const readback = await getDynamicWorksheet();
      const verification = verifyReadback(before, readback, candidatePlans, auditPlan);
      qbConsole.log(`audit rows read back=${verification.audit_rows_verified}`);
      qbConsole.log(`dynamic rows read back=${verification.dynamic_rows_verified}`);
      qbConsole.log(`skipped records=${skippedRecords}`);
      qbConsole.log(`warnings=${warningCount}`);
      progress.setPercentage(100);
      if (!terminalSignalSent) {
        terminalSignalSent = true;
        qb.success();
      }
      return {
        ok: true,
        summary: {
          files_selected: files.length,
          records_parsed: parsed.records.length,
          control_records_validated: controlRecords,
          sample_records_discovered: sampleRecords.length,
          sample_candidates_discovered: candidates.length,
          test_ids_resolved: resolvedBatchIds.length,
          dynamic_rows_staged: candidatePlans.length,
          audit_rows_staged: auditPlan.rows.length,
          stale_audit_rows_cleared: auditPlan.stale_rows.length,
          stale_audit_cells_cleared: auditPlan.stale_cells.length,
          dynamic_rows_written: candidatePlans.length,
          audit_rows_written: auditPlan.rows.length,
          dynamic_rows_read_back: verification.dynamic_rows_verified,
          audit_rows_read_back: verification.audit_rows_verified,
          skipped_records: skippedRecords,
          warnings: warningCount,
          matched_test_ids: candidatePlans.map((plan) => plan.id),
          source_file_hash: parsed.source_file_hash,
        },
      };
    } catch (error) {
      return signalError(error);
    }
  }

  const api = Object.freeze({
    VERSION,
    CORE_VERSION,
    RESULTS_TAB,
    RESULTS_HEADERS,
    AUDIT_HEADERS,
    AUDIT_SECTION_VALUES,
    REPORTABLE_ANALYTES,
    AUDIT_ANALYTE,
    FIRST_DATA_ROW,
    LAST_DATA_ROW,
    WORKSHEET_LAST_ROW,
    AUDIT_SEPARATOR_ROW,
    AUDIT_SECTION_ROW,
    AUDIT_HEADER_ROW,
    AUDIT_FIRST_DATA_ROW,
    AUDIT_LAST_DATA_ROW,
    AUDIT_CAPACITY,
    PARSER_FIRST_COLUMN,
    PARSER_LAST_COLUMN,
    SimpleResultsError,
    sha256Hex,
    sha256BytesHex,
    decodeSourceBytes,
    normalizeAnalyteName,
    classifyRecord,
    parseSource,
    parseSourceBytes,
    candidateTestId,
    requireUniqueCandidates,
    buildParserOwnedValues,
    buildAuditValues,
    requireResultsBundle,
    buildTestRowIndex,
    requireDistinctCandidateRows,
    planCandidateRows,
    planAuditRows,
    applyResultsPlans,
    verifyReadback,
    executeRuntime,
  });

  root.TerpenesSimpleResultsV2Controls = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;

  if (typeof run === "function"
    && typeof QB !== "undefined"
    && typeof QBBatchService === "function") {
    run(() => executeRuntime({
      QB,
      QBBatchService,
      FileReader: typeof FileReader === "function" ? FileReader : undefined,
      TextDecoder: typeof TextDecoder === "function" ? TextDecoder : undefined,
    }));
  }
})(typeof globalThis !== "undefined" ? globalThis : self);
