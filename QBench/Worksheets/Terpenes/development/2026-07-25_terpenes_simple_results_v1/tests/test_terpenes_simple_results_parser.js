"use strict";

const assert = require("assert");
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

const BASE = path.resolve(__dirname, "..");
const SOURCE_PATH = path.join(BASE, "src", "terpenes_simple_results_parser.js");
const DIST_PATH = path.join(BASE, "dist", "terpenes_simple_results_parser_v1.js");
const WORKSHEET_PATH = path.join(BASE, "SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V1.json");
const CORRECTED_WORKSHEET_PATH = path.join(
  BASE,
  "SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V1__dimension_fix.json",
);
const EXPECTED_ORIGINAL_WORKSHEET_HASH = "ce50d670be71fccf02912b30cacb918fd48916e8f154a164b095f8f0670a96be";
const EXPECTED_CORRECTED_WORKSHEET_HASH = "f8d58b33024cce2bf90171df79c7f73e984674fa64b83f99e8030935f9030448";
const EXPECTED_PARSER_ARTIFACT_HASH = "bcec7bf0aa1f0b3edfab6ff2f6bcf370abf863226a81472714202aca5efbc871";
const EXPECTED_SOURCE_HASH = "5de17d8f9eb21a8dfc068daf2297efb707a8b783f63393df432781e5e692e6aa";
const RUNTIME_FIXTURE_PATH = path.join(
  BASE,
  "runtime",
  "terpenes_simple_results_310_311_runtime_source.txt",
);
const EXPECTED_RUNTIME_FIXTURE_HASH = "1e5087715a9bcf216c2991cca53f41fb4ae84b4f9e80eea0e95d7618ec77a36e";
const STAGED_BATCH_ID = "62";
const STAGED_SAMPLE_ID = "AIT-SAMP-170";
const STAGED_TEST_IDS = Object.freeze(["310", "311"]);
const EXPECTED_P1 = [
  268.375, 267.231, 277.946, 269.847, 268.609, 249.622, 270.535, 268.561,
  268.076, 269.906, 270.582, 266.685, 271.521, 279.619, 267.341, 253.982,
  338.966, 303.428, 279.876, 281.767, 299.279, 288.586, 314.54,
];
const EXPECTED_P2 = [
  276.352, 275.209, 286.067, 278.342, 276.646, 256.992, 278.802, 276.596,
  276.823, 278.128, 278.097, 274.94, 278.671, 286.798, 274.303, 262.321,
  352.455, 309.286, 289.961, 284.832, 299.126, 284.973, 338.797,
];

const api = require(SOURCE_PATH);
const runtimeFixtureBytes = fs.readFileSync(RUNTIME_FIXTURE_PATH);
const runtimeFixture = fs.readFileSync(RUNTIME_FIXTURE_PATH, "utf8");
const fixture = runtimeFixture
  .replace("Sample Name\tP1\r\nSample ID\t310", "Sample Name\tP1\r\nSample ID\t308")
  .replace("Sample Name\tP2\r\nSample ID\t311", "Sample Name\tP2\r\nSample ID\t309");
const fixtureBytes = Buffer.from(fixture, "utf8");
const tests = [];

function test(name, fn) {
  tests.push({ name, fn });
}

function expectCode(fn, code) {
  assert.throws(fn, (error) => error && error.code === code);
}

function deepClone(value) {
  return JSON.parse(JSON.stringify(value));
}

function fileSha256(filePath) {
  return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}

function addressCoordinates(address) {
  const match = /^([A-Z]+)([1-9]\d*)$/.exec(address);
  if (!match) return null;
  let column = 0;
  for (const character of match[1]) {
    column = column * 26 + character.charCodeAt(0) - 64;
  }
  return { column, row: Number(match[2]) };
}

function collectAddressTokens(value, pathName = "$", tokens = []) {
  if (Array.isArray(value)) {
    value.forEach((entry, index) => collectAddressTokens(entry, `${pathName}[${index}]`, tokens));
    return tokens;
  }
  if (value && typeof value === "object") {
    Object.entries(value).forEach(([key, entry]) => {
      if (addressCoordinates(key)) tokens.push({ address: key, path: `${pathName}.${key}` });
      collectAddressTokens(entry, `${pathName}.${key}`, tokens);
    });
    return tokens;
  }
  if (typeof value === "string" && addressCoordinates(value)) {
    tokens.push({ address: value, path: pathName });
  }
  return tokens;
}

function collectScalarDifferences(left, right, pathName = "$", differences = []) {
  if (Object.is(left, right)) return differences;
  const leftIsObject = left !== null && typeof left === "object";
  const rightIsObject = right !== null && typeof right === "object";
  if (!leftIsObject || !rightIsObject || Array.isArray(left) !== Array.isArray(right)) {
    differences.push({ path: pathName, left, right });
    return differences;
  }
  const leftKeys = Object.keys(left);
  const rightKeys = Object.keys(right);
  assert.deepStrictEqual(leftKeys, rightKeys);
  leftKeys.forEach((key) => {
    const nextPath = Array.isArray(left) ? `${pathName}[${key}]` : `${pathName}.${key}`;
    collectScalarDifferences(left[key], right[key], nextPath, differences);
  });
  return differences;
}

function byteDifferenceOffsets(left, right) {
  assert.equal(left.length, right.length);
  const offsets = [];
  for (let index = 0; index < left.length; index += 1) {
    if (left[index] !== right[index]) offsets.push(index);
  }
  return offsets;
}

function contractedSampleBindings(source) {
  return source
    .split(/(?=^\[Header\]\r?$)/m)
    .filter((record) => record.startsWith("[Header]"))
    .map((record, index) => {
      const lines = record.split(/\r\n|\n|\r/);
      const sectionStart = lines.indexOf("[Sample Information]");
      assert.notEqual(sectionStart, -1, `record ${index + 1} lacks Sample Information`);
      let sectionEnd = lines.findIndex(
        (line, lineIndex) => lineIndex > sectionStart && /^\[.+]$/.test(line),
      );
      if (sectionEnd < 0) sectionEnd = lines.length;
      const entries = {};
      lines.slice(sectionStart + 1, sectionEnd).forEach((line) => {
        const separator = line.indexOf("\t");
        if (separator > 0) entries[line.slice(0, separator)] = line.slice(separator + 1);
      });
      return {
        record_order: index + 1,
        sample_name: entries["Sample Name"] || "",
        sample_id: entries["Sample ID"] || "",
      };
    });
}

function analyticalRecordProjection(record) {
  const projected = deepClone(record);
  if (projected.sample_information) delete projected.sample_information["Sample ID"];
  delete projected.source_row_hash;
  return projected;
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

function makeGridState(options = {}) {
  const rawGrid = Array.from(
    { length: api.LAST_DATA_ROW },
    () => Array(api.RESULTS_HEADERS.length).fill(""),
  );
  rawGrid[0] = api.RESULTS_HEADERS.slice();
  rawGrid[1][0] = "AIT-SAMP-169";
  rawGrid[1][1] = "308";
  rawGrid[1][2] = "Cannabis Concentrates";
  rawGrid[2][0] = "AIT-SAMP-169";
  rawGrid[2][1] = "309";
  rawGrid[2][2] = "Cannabis Concentrates";
  rawGrid[3][0] = "UNMATCHED-SAMPLE";
  rawGrid[3][1] = "999";
  rawGrid[3][2] = "Unmatched Matrix";
  rawGrid[3][3] = "unmatched-byte-value";
  rawGrid[3][4] = 17;
  for (let column = api.PARSER_FIRST_COLUMN; column <= api.PARSER_LAST_COLUMN; column += 1) {
    rawGrid[1][column] = `stale-308-${column}`;
    rawGrid[2][column] = `stale-309-${column}`;
  }
  const references = {
    B2: "308",
    B3: "309",
    B4: "999",
  };
  if (options.missing309) {
    rawGrid[2][1] = "";
    delete references.B3;
  }
  if (options.duplicate308) {
    rawGrid[4][0] = "DUPLICATE-SAMPLE";
    rawGrid[4][1] = "308";
    rawGrid[4][2] = "Duplicate Matrix";
    references.B5 = "308";
  }
  return {
    rawGrid,
    processedGrid: rawGrid.map((row) => row.map((value) => (value === "" ? "" : String(value)))),
    formulas: { Z87: "=SENTINEL_FORMULA" },
    images: { "image-1": { source: "sentinel-image" } },
    references,
  };
}

function documentsFromState(state, includeOtherWorksheet = false) {
  const documents = [
    { worksheet_name: "Results", type: "WORKSHEET_DATA", data: deepClone(state.rawGrid) },
    { worksheet_name: "Results", type: "WORKSHEET_DATA_PROCESSED", data: deepClone(state.processedGrid) },
    { worksheet_name: "Results", type: "WORKSHEET_FORMULAS", data: deepClone(state.formulas) },
    { worksheet_name: "Results", type: "WORKSHEET_IMAGE_DATA", data: deepClone(state.images) },
    { worksheet_name: "Results", type: "WORKSHEET_DOLLAR_REFERENCES", data: deepClone(state.references) },
  ];
  if (includeOtherWorksheet) {
    documents.push({ worksheet_name: "Other", type: "WORKSHEET_DATA", data: [[]] });
  }
  return documents;
}

function mapToGrid(map) {
  const grid = Array.from(
    { length: api.LAST_DATA_ROW },
    () => Array(api.RESULTS_HEADERS.length).fill(""),
  );
  Object.entries(map || {}).forEach(([address, value]) => {
    const match = address.match(/^([A-Z]+)(\d+)$/);
    if (!match) return;
    let column = 0;
    for (const character of match[1]) column = column * 26 + character.charCodeAt(0) - 64;
    column -= 1;
    const row = Number(match[2]) - 1;
    if (row >= 0 && row < grid.length && column >= 0 && column < api.RESULTS_HEADERS.length) {
      grid[row][column] = value;
    }
  });
  return grid;
}

function makeRuntime(options = {}) {
  const state = options.state || makeGridState(options.worksheet || {});
  const counters = {
    serviceConstructions: 0,
    updates: 0,
    dynamicReads: 0,
    success: 0,
    error: 0,
    payload: null,
    events: [],
    logs: [],
  };
  const resolution = options.resolution || {
    "308": [{ id: 61 }],
    "309": [{ id: 61 }],
  };

  class MockBatchService {
    constructor() {
      counters.serviceConstructions += 1;
      counters.events.push("construct");
    }

    getJson(request) {
      if (request.url === "/batches/get") {
        const testId = String(request.urlParams.test_id);
        counters.events.push(`resolve:${testId}`);
        request.success(deepClone(resolution[testId] || []));
        return undefined;
      }
      if (request.url === "/batches/worksheets/dynamic") {
        counters.dynamicReads += 1;
        counters.events.push(`dynamic:${counters.dynamicReads}`);
        request.success(documentsFromState(state, options.includeOtherWorksheet));
        return undefined;
      }
      request.error(new Error("unexpected getJson route"));
      return undefined;
    }

    update(request) {
      counters.updates += 1;
      counters.events.push(`update:${counters.updates}`);
      counters.payload = deepClone(request);
      if (options.updateError) {
        request.error(new Error("mock update failure"));
        return undefined;
      }
      if (options.persistenceMode !== "noop") {
        const result = request.data.qb_dynamic_spreadsheet_data.Results;
        state.rawGrid = mapToGrid(result.WORKSHEET_DATA);
        state.processedGrid = mapToGrid(result.WORKSHEET_DATA_PROCESSED);
        state.formulas = deepClone(result.WORKSHEET_FORMULAS);
        state.images = deepClone(result.WORKSHEET_IMAGE_DATA);
        state.references = deepClone(result.WORKSHEET_DOLLAR_REFERENCES);
      }
      if (options.persistenceMode === "missing-value") {
        state.rawGrid[1][9] = "";
        state.processedGrid[1][9] = "";
      }
      if (options.persistenceMode === "changed-value") {
        state.rawGrid[1][9] = 999999;
        state.processedGrid[1][9] = "999999";
      }
      if (options.persistenceMode === "changed-context") {
        state.rawGrid[1][0] = "CHANGED-SAMPLE";
        state.processedGrid[1][0] = "CHANGED-SAMPLE";
      }
      if (options.persistenceMode === "missing-row") {
        state.rawGrid[2][1] = "";
        state.processedGrid[2][1] = "";
        delete state.references.B3;
      }
      if (options.persistenceMode === "changed-unmatched") {
        state.rawGrid[3][3] = "changed-unmatched-value";
        state.processedGrid[3][3] = "changed-unmatched-value";
      }
      request.success({ ok: true });
      return undefined;
    }
  }

  const QB = {
    files: options.files || [{ name: options.fileName || "terpenes_c6_308_309_runtime_source.txt", text: async () => options.source || fixture }],
    console: {
      clear() { counters.events.push("console:clear"); },
      log(value) { counters.logs.push(String(value)); },
    },
    progressBar: {
      setPercentage(value) { counters.events.push(`progress:${value}`); },
    },
    success() {
      counters.success += 1;
      counters.events.push("success");
    },
    error() {
      counters.error += 1;
      counters.events.push("error");
    },
  };

  return {
    state,
    counters,
    env: {
      QB,
      QBBatchService: MockBatchService,
    },
  };
}

async function runRuntime(options = {}) {
  const runtime = makeRuntime(options);
  runtime.result = await api.executeRuntime(runtime.env);
  return runtime;
}

function makeStagedGridState(options = {}) {
  const rawGrid = Array.from(
    { length: api.LAST_DATA_ROW },
    () => Array(api.RESULTS_HEADERS.length).fill(""),
  );
  rawGrid[0] = api.RESULTS_HEADERS.slice();
  rawGrid[1][0] = STAGED_SAMPLE_ID;
  rawGrid[1][1] = "310";
  rawGrid[1][2] = "Cannabis Concentrates";
  rawGrid[2][0] = STAGED_SAMPLE_ID;
  rawGrid[2][1] = "311";
  rawGrid[2][2] = "Cannabis Concentrates";
  const references = {
    B2: "310",
    B3: "311",
  };
  if (options.missing310) {
    rawGrid[1][1] = "";
    delete references.B2;
  }
  if (options.missing311) {
    rawGrid[2][1] = "";
    delete references.B3;
  }
  if (options.duplicate310) {
    rawGrid[3][0] = STAGED_SAMPLE_ID;
    rawGrid[3][1] = "310";
    rawGrid[3][2] = "Cannabis Concentrates";
    references.B4 = "310";
  }
  if (options.duplicate311) {
    rawGrid[3][0] = STAGED_SAMPLE_ID;
    rawGrid[3][1] = "311";
    rawGrid[3][2] = "Cannabis Concentrates";
    references.B4 = "311";
  }
  return {
    rawGrid,
    processedGrid: rawGrid.map((row) => row.map((value) => (value === "" ? "" : String(value)))),
    formulas: {},
    images: {},
    references,
  };
}

function makeStagedRuntime(options = {}) {
  const resolution = Object.prototype.hasOwnProperty.call(options, "resolution")
    ? options.resolution
    : {
        "310": [{ id: Number(STAGED_BATCH_ID) }],
        "311": [{ id: Number(STAGED_BATCH_ID) }],
      };
  return makeRuntime({
    ...options,
    source: Object.prototype.hasOwnProperty.call(options, "source")
      ? options.source
      : runtimeFixture,
    fileName: "terpenes_simple_results_310_311_runtime_source.txt",
    state: options.state || makeStagedGridState(options.worksheet || {}),
    resolution,
  });
}

async function runStagedRuntime(options = {}) {
  const runtime = makeStagedRuntime(options);
  runtime.result = await api.executeRuntime(runtime.env);
  return runtime;
}

function removeFirstCompoundRow(source) {
  const lines = source.split(/\r?\n/);
  const section = lines.indexOf("[Compound Results(Ch1)]");
  const header = lines.findIndex((line, index) => index > section && line.startsWith("ID#\t"));
  lines.splice(header + 1, 1);
  return lines.join("\n");
}

function malformedFirstCompoundRow(source) {
  const lines = source.split(/\r?\n/);
  const section = lines.indexOf("[Compound Results(Ch1)]");
  const header = lines.findIndex((line, index) => index > section && line.startsWith("ID#\t"));
  const fields = lines[header + 1].split("\t");
  fields.pop();
  lines[header + 1] = fields.join("\t");
  return lines.join("\n");
}

function invalidFirstCompoundNumber(source) {
  const lines = source.split(/\r?\n/);
  const section = lines.indexOf("[Compound Results(Ch1)]");
  const header = lines.findIndex((line, index) => index > section && line.startsWith("ID#\t"));
  const headers = lines[header].split("\t");
  const fields = lines[header + 1].split("\t");
  fields[headers.indexOf("Conc.")] = "not-a-number";
  lines[header + 1] = fields.join("\t");
  return lines.join("\n");
}

function duplicateFixtureTestId(source) {
  return source.replace(
    "Sample Name\tP2\r\nSample ID\t309",
    "Sample Name\tP2\r\nSample ID\t308",
  );
}

// A. Worksheet architecture
test("worksheet JSON contains exactly one worksheet named Results", () => {
  const workbook = JSON.parse(fs.readFileSync(WORKSHEET_PATH, "utf8"));
  assert.deepStrictEqual(workbook.config.worksheets.map((worksheet) => worksheet.worksheetName), ["Results"]);
  assert.deepStrictEqual(Object.keys(workbook.data), ["Results"]);
});

test("worksheet header order is the exact A:AY contract", () => {
  const workbook = JSON.parse(fs.readFileSync(WORKSHEET_PATH, "utf8"));
  assert.equal(api.RESULTS_HEADERS.length, 51);
  assert.deepStrictEqual(workbook.config.worksheets[0].data[0], api.RESULTS_HEADERS);
});

test("worksheet has no legacy or review tabs", () => {
  const text = fs.readFileSync(WORKSHEET_PATH, "utf8");
  for (const forbidden of ["Instrument Import", "Test Transfer", "Run Setup", "Batch Review"]) {
    assert.equal(text.includes(forbidden), false);
  }
});

test("worksheet capacity is rows 2:87 with no fixture Test IDs", () => {
  const workbook = JSON.parse(fs.readFileSync(WORKSHEET_PATH, "utf8"));
  const worksheet = workbook.config.worksheets[0];
  assert.equal(worksheet.rows.length, 87);
  assert.equal(worksheet.data.length, 87);
  assert.equal(JSON.stringify(worksheet).includes('"308"'), false);
  assert.equal(JSON.stringify(worksheet).includes('"309"'), false);
});

test("A:C use the proven dynamic Test and Sample context", () => {
  const workbook = JSON.parse(fs.readFileSync(WORKSHEET_PATH, "utf8"));
  const data = workbook.config.worksheets[0].data;
  assert.deepStrictEqual(data[1].slice(0, 3), [
    "${tests[0].sample.get_display_id()}",
    "${tests[0].get_display_id()}",
    "${tests[0].sample.product_matrix}",
  ]);
  assert.deepStrictEqual(data[86].slice(0, 3), [
    "${tests[85].sample.get_display_id()}",
    "${tests[85].get_display_id()}",
    "${tests[85].sample.product_matrix}",
  ]);
});

test("A:C are context-owned and D:AY are parser-owned", () => {
  const workbook = JSON.parse(fs.readFileSync(WORKSHEET_PATH, "utf8"));
  const cells = workbook.config.worksheets[0].cells;
  assert.equal(cells.A2.readonly, true);
  assert.equal(cells.B2.readonly, true);
  assert.equal(cells.C2.readonly, true);
  assert.equal(cells.D2.readonly, false);
  assert.equal(cells.AY2.readonly, false);
});

test("worksheet candidate contains no formulas", () => {
  const workbook = JSON.parse(fs.readFileSync(WORKSHEET_PATH, "utf8"));
  const formulaValues = workbook.config.worksheets[0].data.flat().filter((value) => typeof value === "string" && value.startsWith("="));
  assert.deepStrictEqual(formulaValues, []);
});

// A2. Persistent dimension-fix regression coverage
test("original and corrected worksheet hashes and minDimensions remain exact", () => {
  const original = JSON.parse(fs.readFileSync(WORKSHEET_PATH, "utf8"));
  const corrected = JSON.parse(fs.readFileSync(CORRECTED_WORKSHEET_PATH, "utf8"));
  assert.equal(fileSha256(WORKSHEET_PATH), EXPECTED_ORIGINAL_WORKSHEET_HASH);
  assert.equal(fileSha256(CORRECTED_WORKSHEET_PATH), EXPECTED_CORRECTED_WORKSHEET_HASH);
  assert.deepStrictEqual(original.config.worksheets[0].minDimensions, [87, 51]);
  assert.deepStrictEqual(corrected.config.worksheets[0].minDimensions, [51, 87]);
});

test("corrected minDimensions use the established columns-then-rows ordering", () => {
  const corrected = JSON.parse(fs.readFileSync(CORRECTED_WORKSHEET_PATH, "utf8"));
  const worksheet = corrected.config.worksheets[0];
  assert.deepStrictEqual(worksheet.minDimensions, [
    worksheet.columns.length,
    worksheet.rows.length,
  ]);
});

test("corrected worksheet is exactly one Results tab with 51 headers through AY and 87 rows", () => {
  const corrected = JSON.parse(fs.readFileSync(CORRECTED_WORKSHEET_PATH, "utf8"));
  const worksheet = corrected.config.worksheets[0];
  assert.deepStrictEqual(corrected.config.worksheets.map((entry) => entry.worksheetName), ["Results"]);
  assert.deepStrictEqual(Object.keys(corrected.data), ["Results"]);
  assert.equal(worksheet.columns.length, 51);
  assert.equal(columnLetter(worksheet.columns.length - 1), "AY");
  assert.equal(worksheet.rows.length, 87);
  assert.equal(worksheet.data.length, 87);
  assert.equal(worksheet.data.every((row) => row.length === 51), true);
  assert.equal(worksheet.data[0].length, 51);
  assert.deepStrictEqual(worksheet.data[0], api.RESULTS_HEADERS);
  assert.equal(Object.prototype.hasOwnProperty.call(worksheet.cells, "AY87"), true);
});

test("corrected cell, data, style, formula, image, reference, and named-cell bounds stop at AY87", () => {
  const corrected = JSON.parse(fs.readFileSync(CORRECTED_WORKSHEET_PATH, "utf8"));
  const worksheet = corrected.config.worksheets[0];
  assert.equal(Object.keys(worksheet.cells).length, 51 * 87);
  assert.equal(Object.keys(worksheet.style).length, 51);
  assert.equal(Object.prototype.hasOwnProperty.call(worksheet.style, "AY1"), true);
  assert.equal(worksheet.data.length, 87);
  assert.equal(worksheet.data.every((row) => row.length === 51), true);
  for (const token of collectAddressTokens(corrected)) {
    const coordinates = addressCoordinates(token.address);
    assert.equal(
      coordinates.column <= 51 && coordinates.row <= 87,
      true,
      `${token.path} exceeds AY87`,
    );
  }
  const serialized = JSON.stringify(corrected);
  assert.equal(/"=[^"]*"/.test(serialized), false);
  assert.equal(/https?:\/\//i.test(serialized), false);
  assert.deepStrictEqual(corrected.qb_config.kvstore_config, {});
});

test("corrected rows 2:87 retain generic A:C context, blank D:AY, and no fixture Test IDs", () => {
  const corrected = JSON.parse(fs.readFileSync(CORRECTED_WORKSHEET_PATH, "utf8"));
  const data = corrected.config.worksheets[0].data;
  for (let rowIndex = 1; rowIndex < 87; rowIndex += 1) {
    const testIndex = rowIndex - 1;
    assert.deepStrictEqual(data[rowIndex].slice(0, 3), [
      `\${tests[${testIndex}].sample.get_display_id()}`,
      `\${tests[${testIndex}].get_display_id()}`,
      `\${tests[${testIndex}].sample.product_matrix}`,
    ]);
    assert.deepStrictEqual(data[rowIndex].slice(3), Array(48).fill(""));
  }
  const serialized = JSON.stringify(corrected);
  assert.equal(serialized.includes('"308"'), false);
  assert.equal(serialized.includes('"309"'), false);
});

test("original and corrected candidates differ semantically only at minDimensions", () => {
  const original = JSON.parse(fs.readFileSync(WORKSHEET_PATH, "utf8"));
  const corrected = JSON.parse(fs.readFileSync(CORRECTED_WORKSHEET_PATH, "utf8"));
  assert.deepStrictEqual(collectScalarDifferences(original, corrected), [
    {
      path: "$.config.worksheets[0].minDimensions[0]",
      left: 87,
      right: 51,
    },
    {
      path: "$.config.worksheets[0].minDimensions[1]",
      left: 51,
      right: 87,
    },
  ]);
  corrected.config.worksheets[0].minDimensions = [87, 51];
  assert.deepStrictEqual(corrected, original);
});

test("dimension fix is the exact four-byte binary change", () => {
  const original = fs.readFileSync(WORKSHEET_PATH);
  const corrected = fs.readFileSync(CORRECTED_WORKSHEET_PATH);
  assert.equal(corrected.length, original.length);
  const offsets = [];
  for (let index = 0; index < original.length; index += 1) {
    if (original[index] !== corrected[index]) offsets.push(index);
  }
  assert.deepStrictEqual(offsets, [614306, 614307, 614320, 614321]);
});

test("dimension correction leaves the parser upload artifact hash unchanged", () => {
  assert.equal(fileSha256(DIST_PATH), EXPECTED_PARSER_ARTIFACT_HASH);
});

// B. Input parsing
test("complete C6 source parses all 34 records", () => {
  assert.equal(api.parseSource(fixture).records.length, 34);
});

test("every complete record has 23 ordered reportable analytes", () => {
  const parsed = api.parseSource(fixture);
  assert.equal(parsed.records.every((record) => record.reportable_analytes.length === 23), true);
});

test("Dimethylacetamide remains an audit-only result", () => {
  const parsed = api.parseSource(fixture);
  assert.equal(parsed.records.every((record) => (
    record.dimethylacetamide_audit.internal_key === "dimethylacetamide"
      && record.dimethylacetamide_audit.reportable === false
      && typeof record.dimethylacetamide_audit.conc === "number"
  )), true);
});

test("Unicode analyte labels remain exact", () => {
  const labels = api.REPORTABLE_ANALYTES.map((analyte) => analyte.label);
  assert.equal(labels.includes("α-Pinene"), true);
  assert.equal(labels.includes("β-Myrcene"), true);
  assert.equal(labels.includes("γ-Terpinene"), true);
  assert.equal(labels.includes("(-)-α-Bisabolol"), true);
  assert.deepStrictEqual(api.RESULTS_HEADERS.slice(9, 32), labels);
});

test("missing required sections fail closed", () => {
  expectCode(() => api.parseSource(fixture.replace("[Configuration]", "[Configuration Missing]")), "MISSING_REQUIRED_SECTION");
});

test("wrong Compound Results row counts fail closed", () => {
  expectCode(() => api.parseSource(removeFirstCompoundRow(fixture)), "INVALID_CONTROLLED_COMPOUND_RESULTS");
});

test("malformed table row widths fail closed", () => {
  expectCode(() => api.parseSource(malformedFirstCompoundRow(fixture)), "MALFORMED_TABLE_ROW");
});

test("malformed numeric fields fail closed", () => {
  expectCode(() => api.parseSource(invalidFirstCompoundNumber(fixture)), "INVALID_NUMERIC_VALUE");
});

// C. Test mapping
test("fixture candidates are exactly P1/308 and P2/309", () => {
  const parsed = api.parseSource(fixture);
  const candidates = api.requireUniqueCandidates(parsed.records);
  assert.deepStrictEqual(candidates.map((record) => [record.sample_information["Sample Name"], api.candidateTestId(record)]), [
    ["P1", "308"],
    ["P2", "309"],
  ]);
});

test("controls and validation records are parsed but not candidates", () => {
  const parsed = api.parseSource(fixture);
  const candidates = api.requireUniqueCandidates(parsed.records);
  assert.equal(parsed.records.length - candidates.length, 32);
  assert.equal(parsed.records.filter((record) => record.category === "Validation").length, 13);
});

test("duplicate candidate Test IDs fail", async () => {
  const runtime = await runRuntime({ source: duplicateFixtureTestId(fixture) });
  assert.equal(runtime.result.error.code, "DUPLICATE_CANDIDATE_TEST_ID");
  assert.equal(runtime.counters.updates, 0);
});

test("unknown Test IDs fail", async () => {
  const runtime = await runRuntime({ resolution: { "308": [{ id: 61 }], "309": [] } });
  assert.equal(runtime.result.error.code, "TEST_ID_NOT_FOUND");
  assert.equal(runtime.counters.updates, 0);
});

test("candidate resolution across multiple Batches fails", async () => {
  const runtime = await runRuntime({ resolution: { "308": [{ id: 61 }], "309": [{ id: 62 }] } });
  assert.equal(runtime.result.error.code, "CANDIDATES_RESOLVE_TO_MULTIPLE_BATCHES");
  assert.equal(runtime.counters.updates, 0);
});

test("missing Results Test rows fail", async () => {
  const runtime = await runRuntime({ worksheet: { missing309: true } });
  assert.equal(runtime.result.error.code, "RESULTS_TEST_ID_MISSING");
  assert.equal(runtime.counters.updates, 0);
});

test("duplicate Results Test rows fail", async () => {
  const runtime = await runRuntime({ worksheet: { duplicate308: true } });
  assert.equal(runtime.result.error.code, "RESULTS_TEST_ID_DUPLICATE");
  assert.equal(runtime.counters.updates, 0);
});

// D. One-tab update
test("successful runtime constructs one Batch service and performs one update", async () => {
  const runtime = await runRuntime();
  assert.equal(runtime.result.ok, true);
  assert.equal(runtime.counters.serviceConstructions, 1);
  assert.equal(runtime.counters.updates, 1);
});

test("update contains exactly one dynamic worksheet key Results", async () => {
  const runtime = await runRuntime();
  assert.deepStrictEqual(Object.keys(runtime.counters.payload.data.qb_dynamic_spreadsheet_data), ["Results"]);
  assert.equal(runtime.counters.payload.urlParams.run_worksheet_calculations, true);
});

test("artifact contains one service construction and one update expression", () => {
  const artifact = fs.readFileSync(DIST_PATH, "utf8");
  assert.equal((artifact.match(/new env\.QBBatchService\s*\(/g) || []).length, 1);
  assert.equal((artifact.match(/batchService\.update\s*\(/g) || []).length, 1);
});

test("artifact has no Test service or direct Test write route", () => {
  const artifact = fs.readFileSync(DIST_PATH, "utf8");
  for (const forbidden of ["QBTestService", "updateTest", "test_worksheet"]) {
    assert.equal(artifact.includes(forbidden), false);
  }
});

test("failed readback does not perform a second update", async () => {
  const runtime = await runRuntime({ persistenceMode: "noop" });
  assert.equal(runtime.result.error.code, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
  assert.equal(runtime.counters.updates, 1);
  assert.equal(runtime.counters.serviceConstructions, 1);
});

// E. Cell ownership
test("A:C remain unchanged after a successful write", async () => {
  const runtime = makeRuntime();
  const before = runtime.state.rawGrid.map((row) => row.slice(0, 3));
  const result = await api.executeRuntime(runtime.env);
  assert.equal(result.ok, true);
  assert.deepStrictEqual(runtime.state.rawGrid.map((row) => row.slice(0, 3)), before);
});

test("matched D:AY values are set exactly", async () => {
  const runtime = await runRuntime();
  const parsed = api.parseSource(fixture);
  const candidates = api.requireUniqueCandidates(parsed.records);
  const expected308 = api.buildParserOwnedValues(candidates[0], parsed.source_file_hash);
  const expected309 = api.buildParserOwnedValues(candidates[1], parsed.source_file_hash);
  assert.deepStrictEqual(runtime.state.rawGrid[1].slice(3, 51), expected308);
  assert.deepStrictEqual(runtime.state.rawGrid[2].slice(3, 51), expected309);
});

test("explicit blank source values clear stale parser-owned values", () => {
  const parsed = api.parseSource(fixture);
  const record = api.requireUniqueCandidates(parsed.records)[0];
  record.configuration["Detector Name"] = "";
  const state = makeGridState();
  const bundle = api.requireResultsBundle(documentsFromState(state));
  const plans = api.planCandidateRows(bundle, [record], parsed.source_file_hash);
  const update = api.applyCandidatePlans(bundle, plans);
  const detectorNameColumn = api.RESULTS_HEADERS.indexOf("Detector Name");
  assert.equal(update.WORKSHEET_DATA[`${columnLetter(detectorNameColumn)}2`], "");
  assert.equal(update.WORKSHEET_DATA_PROCESSED[`${columnLetter(detectorNameColumn)}2`], "");
});

test("unmatched rows remain byte-for-byte unchanged", async () => {
  const runtime = makeRuntime();
  const beforeRaw = JSON.stringify(runtime.state.rawGrid[3]);
  const beforeProcessed = JSON.stringify(runtime.state.processedGrid[3]);
  const result = await api.executeRuntime(runtime.env);
  assert.equal(result.ok, true);
  assert.equal(JSON.stringify(runtime.state.rawGrid[3]), beforeRaw);
  assert.equal(JSON.stringify(runtime.state.processedGrid[3]), beforeProcessed);
});

test("formula, image, and dollar-reference maps are preserved", async () => {
  const runtime = makeRuntime();
  const before = {
    formulas: deepClone(runtime.state.formulas),
    images: deepClone(runtime.state.images),
    references: deepClone(runtime.state.references),
  };
  const result = await api.executeRuntime(runtime.env);
  assert.equal(result.ok, true);
  const update = runtime.counters.payload.data.qb_dynamic_spreadsheet_data.Results;
  assert.deepStrictEqual(update.WORKSHEET_FORMULAS, before.formulas);
  assert.deepStrictEqual(update.WORKSHEET_IMAGE_DATA, before.images);
  assert.deepStrictEqual(update.WORKSHEET_DOLLAR_REFERENCES, before.references);
});

// F. Readback
test("successful persistence passes readback", async () => {
  const runtime = await runRuntime();
  assert.equal(runtime.result.ok, true);
  assert.equal(runtime.result.summary.readback_rows_verified, 2);
  assert.equal(runtime.counters.success, 1);
  assert.equal(runtime.counters.error, 0);
});

test("missing persisted values fail readback", async () => {
  const runtime = await runRuntime({ persistenceMode: "missing-value" });
  assert.equal(runtime.result.error.code, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
  assert.equal(runtime.counters.success, 0);
});

test("changed persisted numeric values fail readback", async () => {
  const runtime = await runRuntime({ persistenceMode: "changed-value" });
  assert.equal(runtime.result.error.code, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("changed A:C context fails readback", async () => {
  const runtime = await runRuntime({ persistenceMode: "changed-context" });
  assert.equal(runtime.result.error.code, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("missing candidate rows fail readback", async () => {
  const runtime = await runRuntime({ persistenceMode: "missing-row" });
  assert.equal(runtime.result.error.code, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("no-op updates fail readback", async () => {
  const runtime = await runRuntime({ persistenceMode: "noop" });
  assert.equal(runtime.result.error.code, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("changed unmatched rows fail readback", async () => {
  const runtime = await runRuntime({ persistenceMode: "changed-unmatched" });
  assert.equal(runtime.result.error.code, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("QB.success occurs only after the second dynamic worksheet retrieval", async () => {
  const runtime = await runRuntime();
  const readbackIndex = runtime.counters.events.indexOf("dynamic:2");
  const successIndex = runtime.counters.events.indexOf("success");
  assert.equal(readbackIndex >= 0, true);
  assert.equal(successIndex > readbackIndex, true);
});

// G. Fixture expectations
test("fixture source hash matches the immutable C6 hash", () => {
  assert.equal(api.sha256Hex(fixture), EXPECTED_SOURCE_HASH);
  assert.equal(api.parseSource(fixture).source_file_hash, EXPECTED_SOURCE_HASH);
});

test("P1 has every expected analyte value", () => {
  const parsed = api.parseSource(fixture);
  const record = api.requireUniqueCandidates(parsed.records).find((candidate) => api.candidateTestId(candidate) === "308");
  assert.deepStrictEqual(record.reportable_analytes.map((analyte) => analyte.conc), EXPECTED_P1);
});

test("P2 has every expected analyte value", () => {
  const parsed = api.parseSource(fixture);
  const record = api.requireUniqueCandidates(parsed.records).find((candidate) => api.candidateTestId(candidate) === "309");
  assert.deepStrictEqual(record.reportable_analytes.map((analyte) => analyte.conc), EXPECTED_P2);
});

test("fixture writes exactly two rows for Test IDs 308 and 309", async () => {
  const runtime = await runRuntime();
  assert.deepStrictEqual(runtime.result.summary.matched_test_ids, ["308", "309"]);
  assert.equal(runtime.result.summary.records_parsed, 34);
  assert.equal(runtime.result.summary.rows_written, 2);
  assert.equal(runtime.result.summary.skipped_records, 32);
});

test("fixture retains audit, integration, and source-row hashes for both candidates", () => {
  const parsed = api.parseSource(fixture);
  const candidates = api.requireUniqueCandidates(parsed.records);
  candidates.forEach((record) => {
    assert.equal(record.dimethylacetamide_audit.conc, 100);
    assert.equal(record.unknown_peak_count > 0, true);
    assert.equal(record.manual_integration, true);
    assert.equal(record.integration_review_status, "Review Required");
    assert.match(record.source_row_hash, /^[a-f0-9]{64}$/);
  });
  assert.notEqual(candidates[0].source_row_hash, candidates[1].source_row_hash);
});

// H. Immutable staged Sandbox runtime binding fixture
test("staged runtime input exists at the authorized isolated path", () => {
  assert.equal(fs.existsSync(RUNTIME_FIXTURE_PATH), true);
  const relativePath = path.relative(BASE, RUNTIME_FIXTURE_PATH);
  assert.equal(relativePath, path.join("runtime", "terpenes_simple_results_310_311_runtime_source.txt"));
  assert.equal(relativePath.startsWith(`..${path.sep}`), false);
  assert.equal(path.isAbsolute(relativePath), false);
});

test("staged runtime input hash is stable", () => {
  assert.equal(fileSha256(RUNTIME_FIXTURE_PATH), EXPECTED_RUNTIME_FIXTURE_HASH);
  assert.equal(api.sha256Hex(runtimeFixture), EXPECTED_RUNTIME_FIXTURE_HASH);
});

test("staged runtime input differs from the in-memory historical source by exactly four bytes", () => {
  assert.equal(runtimeFixtureBytes.length, fixtureBytes.length);
  assert.equal(crypto.createHash("sha256").update(fixtureBytes).digest("hex"), EXPECTED_SOURCE_HASH);
  assert.deepStrictEqual(
    byteDifferenceOffsets(fixtureBytes, runtimeFixtureBytes),
    [124301, 124302, 133048, 133049],
  );
});

test("staged runtime input changes only the contracted P1 and P2 Sample IDs", () => {
  const restored = runtimeFixture
    .replace("Sample Name\tP1\r\nSample ID\t310", "Sample Name\tP1\r\nSample ID\t308")
    .replace("Sample Name\tP2\r\nSample ID\t311", "Sample Name\tP2\r\nSample ID\t309");
  assert.equal(restored, fixture);
  const sourceBindings = contractedSampleBindings(fixture);
  const targetBindings = contractedSampleBindings(runtimeFixture);
  const differences = sourceBindings
    .map((sourceBinding, index) => ({ source: sourceBinding, target: targetBindings[index] }))
    .filter(({ source, target }) => source.sample_id !== target.sample_id);
  assert.deepStrictEqual(differences, [
    {
      source: sourceBindings.find((binding) => binding.sample_name === "P1"),
      target: targetBindings.find((binding) => binding.sample_name === "P1"),
    },
    {
      source: sourceBindings.find((binding) => binding.sample_name === "P2"),
      target: targetBindings.find((binding) => binding.sample_name === "P2"),
    },
  ]);
  assert.deepStrictEqual(
    differences.map(({ source, target }) => [
      source.sample_name,
      source.sample_id,
      target.sample_id,
    ]),
    [
      ["P1", "308", "310"],
      ["P2", "309", "311"],
    ],
  );
});

test("staged runtime input retains all 34 valid records and 23 reportable analytes", () => {
  const parsed = api.parseSource(runtimeFixture);
  assert.equal(parsed.records.length, 34);
  assert.equal(parsed.records.every((record) => record.reportable_analytes.length === 23), true);
  assert.equal(parsed.records.every((record) => record.counts.compound_result_row_count === 24), true);
});

test("staged runtime candidate set is exactly Test IDs 310 and 311", () => {
  const parsed = api.parseSource(runtimeFixture);
  const candidates = api.requireUniqueCandidates(parsed.records);
  assert.deepStrictEqual(candidates.map((record) => api.candidateTestId(record)), STAGED_TEST_IDS);
  assert.equal(candidates.every((record) => typeof api.candidateTestId(record) === "string"), true);
  assert.equal(new Set(candidates.map((record) => api.candidateTestId(record))).size, 2);
});

test("staged Source role is P1 bound to Test 310", () => {
  const candidates = api.requireUniqueCandidates(api.parseSource(runtimeFixture).records);
  assert.deepStrictEqual(
    [candidates[0].sample_information["Sample Name"], api.candidateTestId(candidates[0])],
    ["P1", "310"],
  );
});

test("staged Target role is P2 bound to Test 311", () => {
  const candidates = api.requireUniqueCandidates(api.parseSource(runtimeFixture).records);
  assert.deepStrictEqual(
    [candidates[1].sample_information["Sample Name"], api.candidateTestId(candidates[1])],
    ["P2", "311"],
  );
});

test("staged Test 310 resolves exactly once to internal Batch 62", async () => {
  const runtime = await runStagedRuntime();
  assert.equal(runtime.result.ok, true);
  assert.equal(runtime.counters.events.filter((event) => event === "resolve:310").length, 1);
  assert.equal(runtime.counters.payload.data.id, STAGED_BATCH_ID);
});

test("staged Test 311 resolves exactly once to internal Batch 62", async () => {
  const runtime = await runStagedRuntime();
  assert.equal(runtime.result.ok, true);
  assert.equal(runtime.counters.events.filter((event) => event === "resolve:311").length, 1);
  assert.equal(runtime.counters.payload.data.id, STAGED_BATCH_ID);
});

test("both staged candidates resolve to the same Batch 62", async () => {
  const runtime = await runStagedRuntime();
  assert.equal(runtime.result.ok, true);
  assert.deepStrictEqual(runtime.result.summary.matched_test_ids, STAGED_TEST_IDS);
  assert.equal(runtime.counters.payload.data.id, STAGED_BATCH_ID);
});

test("successful staged resolution selects no alternate Batch", async () => {
  const runtime = await runStagedRuntime();
  assert.equal(runtime.result.ok, true);
  assert.equal(runtime.counters.payload.data.id, "62");
  assert.equal(runtime.counters.events.some((event) => event.includes("63")), false);
});

test("staged Test 310 maps exactly once to Results row 2", () => {
  const parsed = api.parseSource(runtimeFixture);
  const bundle = api.requireResultsBundle(documentsFromState(makeStagedGridState()));
  const plans = api.planCandidateRows(
    bundle,
    api.requireUniqueCandidates(parsed.records),
    parsed.source_file_hash,
  );
  const plan = plans.find((entry) => entry.id === "310");
  assert.equal(plan.row, 2);
  assert.equal(plans.filter((entry) => entry.id === "310").length, 1);
});

test("staged Test 311 maps exactly once to Results row 3", () => {
  const parsed = api.parseSource(runtimeFixture);
  const bundle = api.requireResultsBundle(documentsFromState(makeStagedGridState()));
  const plans = api.planCandidateRows(
    bundle,
    api.requireUniqueCandidates(parsed.records),
    parsed.source_file_hash,
  );
  const plan = plans.find((entry) => entry.id === "311");
  assert.equal(plan.row, 3);
  assert.equal(plans.filter((entry) => entry.id === "311").length, 1);
});

test("staged row 2 A:C remain unchanged", async () => {
  const runtime = makeStagedRuntime();
  const before = runtime.state.rawGrid[1].slice(0, 3);
  const result = await api.executeRuntime(runtime.env);
  assert.equal(result.ok, true);
  assert.deepStrictEqual(runtime.state.rawGrid[1].slice(0, 3), before);
});

test("staged row 3 A:C remain unchanged", async () => {
  const runtime = makeStagedRuntime();
  const before = runtime.state.rawGrid[2].slice(0, 3);
  const result = await api.executeRuntime(runtime.env);
  assert.equal(result.ok, true);
  assert.deepStrictEqual(runtime.state.rawGrid[2].slice(0, 3), before);
});

test("staged runtime writes exactly two Results rows", async () => {
  const runtime = await runStagedRuntime();
  assert.equal(runtime.result.ok, true);
  assert.equal(runtime.result.summary.rows_written, 2);
  assert.equal(runtime.result.summary.matched_results_rows, 2);
  assert.deepStrictEqual(runtime.result.summary.matched_test_ids, STAGED_TEST_IDS);
});

test("staged runtime sets parser-owned D:AY only on rows 2 and 3", async () => {
  const runtime = await runStagedRuntime();
  const dataMap = runtime.counters.payload.data.qb_dynamic_spreadsheet_data.Results.WORKSHEET_DATA;
  const parserOwnedAddresses = Object.keys(dataMap).filter((address) => {
    const coordinates = addressCoordinates(address);
    return coordinates
      && coordinates.row >= 2
      && coordinates.column >= api.PARSER_FIRST_COLUMN + 1;
  });
  assert.equal(parserOwnedAddresses.length, 48 * 2);
  assert.deepStrictEqual(
    Array.from(new Set(parserOwnedAddresses.map((address) => addressCoordinates(address).row))),
    [2, 3],
  );
  for (const row of [2, 3]) {
    for (let column = api.PARSER_FIRST_COLUMN; column <= api.PARSER_LAST_COLUMN; column += 1) {
      assert.equal(Object.prototype.hasOwnProperty.call(dataMap, `${columnLetter(column)}${row}`), true);
    }
  }
});

test("staged unmatched Results rows 4:87 remain unchanged", async () => {
  const runtime = makeStagedRuntime();
  const before = JSON.stringify(runtime.state.rawGrid.slice(3));
  const result = await api.executeRuntime(runtime.env);
  assert.equal(result.ok, true);
  assert.equal(JSON.stringify(runtime.state.rawGrid.slice(3)), before);
  assert.deepStrictEqual(
    runtime.state.rawGrid.slice(3),
    Array.from({ length: 84 }, () => Array(api.RESULTS_HEADERS.length).fill("")),
  );
});

test("staged control records are validated but not persisted", async () => {
  const runtime = await runStagedRuntime();
  assert.equal(runtime.result.ok, true);
  assert.equal(runtime.result.summary.records_parsed, 34);
  assert.equal(runtime.result.summary.rows_written, 2);
  assert.equal(runtime.result.summary.skipped_records, 32);
});

test("no staged control record maps to a Results row", () => {
  const parsed = api.parseSource(runtimeFixture);
  const candidates = api.requireUniqueCandidates(parsed.records);
  const bundle = api.requireResultsBundle(documentsFromState(makeStagedGridState()));
  const plans = api.planCandidateRows(bundle, candidates, parsed.source_file_hash);
  assert.deepStrictEqual(
    plans.map((plan) => plan.record.sample_information["Sample Name"]),
    ["P1", "P2"],
  );
  assert.equal(plans.some((plan) => plan.record.category !== "Sample"), false);
});

test("staged runtime constructs exactly one QBBatchService", async () => {
  const runtime = await runStagedRuntime();
  assert.equal(runtime.result.ok, true);
  assert.equal(runtime.counters.serviceConstructions, 1);
});

test("staged runtime performs exactly one Batch update", async () => {
  const runtime = await runStagedRuntime();
  assert.equal(runtime.result.ok, true);
  assert.equal(runtime.counters.updates, 1);
});

test("staged update payload contains exactly one Results worksheet key", async () => {
  const runtime = await runStagedRuntime();
  const payload = runtime.counters.payload;
  assert.deepStrictEqual(Object.keys(payload.data.qb_dynamic_spreadsheet_data), ["Results"]);
  assert.equal(payload.data.id, "62");
  assert.deepStrictEqual(payload.urlParams, { run_worksheet_calculations: true });
});

test("staged runtime constructs no Test service", async () => {
  const runtime = await runStagedRuntime();
  assert.equal(runtime.result.ok, true);
  assert.equal(runtime.counters.serviceConstructions, 1);
  assert.equal(fs.readFileSync(DIST_PATH, "utf8").includes("QBTestService"), false);
});

test("staged runtime performs no direct Test write", async () => {
  const runtime = await runStagedRuntime();
  assert.equal(runtime.result.ok, true);
  const artifact = fs.readFileSync(DIST_PATH, "utf8");
  assert.equal(artifact.includes("QBTestService"), false);
  assert.equal(artifact.includes("updateTest"), false);
  assert.equal(runtime.counters.updates, 1);
});

test("failed staged readback performs no second Batch update", async () => {
  const runtime = await runStagedRuntime({ persistenceMode: "noop" });
  assert.equal(runtime.result.error.code, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
  assert.equal(runtime.counters.updates, 1);
  assert.equal(runtime.counters.serviceConstructions, 1);
});

test("staged read-after-write verifies Results rows 2 and 3", async () => {
  const runtime = await runStagedRuntime();
  assert.equal(runtime.result.ok, true);
  assert.equal(runtime.result.summary.readback_rows_verified, 2);
  assert.deepStrictEqual(runtime.result.summary.matched_test_ids, STAGED_TEST_IDS);
  assert.equal(runtime.counters.dynamicReads, 2);
});

test("staged readback preserves all A:C context", async () => {
  const runtime = makeStagedRuntime();
  const before = runtime.state.rawGrid.map((row) => row.slice(0, 3));
  const result = await api.executeRuntime(runtime.env);
  assert.equal(result.ok, true);
  assert.deepStrictEqual(runtime.state.rawGrid.map((row) => row.slice(0, 3)), before);
});

test("missing staged Test 310 Results row fails closed", async () => {
  const runtime = await runStagedRuntime({ worksheet: { missing310: true } });
  assert.equal(runtime.result.error.code, "RESULTS_TEST_ID_MISSING");
  assert.equal(runtime.counters.updates, 0);
});

test("missing staged Test 311 Results row fails closed", async () => {
  const runtime = await runStagedRuntime({ worksheet: { missing311: true } });
  assert.equal(runtime.result.error.code, "RESULTS_TEST_ID_MISSING");
  assert.equal(runtime.counters.updates, 0);
});

test("duplicate staged Test 310 Results row fails closed", async () => {
  const runtime = await runStagedRuntime({ worksheet: { duplicate310: true } });
  assert.equal(runtime.result.error.code, "RESULTS_TEST_ID_DUPLICATE");
  assert.equal(runtime.counters.updates, 0);
});

test("duplicate staged Test 311 Results row fails closed", async () => {
  const runtime = await runStagedRuntime({ worksheet: { duplicate311: true } });
  assert.equal(runtime.result.error.code, "RESULTS_TEST_ID_DUPLICATE");
  assert.equal(runtime.counters.updates, 0);
});

test("alternate-Batch staged resolution fails closed", async () => {
  const runtime = await runStagedRuntime({
    resolution: {
      "310": [{ id: 62 }],
      "311": [{ id: 63 }],
    },
  });
  assert.equal(runtime.result.error.code, "CANDIDATES_RESOLVE_TO_MULTIPLE_BATCHES");
  assert.equal(runtime.counters.updates, 0);
});

test("partial staged candidate resolution fails closed", async () => {
  const runtime = await runStagedRuntime({
    resolution: {
      "310": [{ id: 62 }],
      "311": [],
    },
  });
  assert.equal(runtime.result.error.code, "TEST_ID_NOT_FOUND");
  assert.equal(runtime.counters.updates, 0);
});

test("unknown staged candidate resolution fails closed", async () => {
  const unknownSource = runtimeFixture.replace(
    "Sample Name\tP2\r\nSample ID\t311",
    "Sample Name\tP2\r\nSample ID\t312",
  );
  const runtime = await runStagedRuntime({ source: unknownSource });
  assert.equal(runtime.result.error.code, "TEST_ID_NOT_FOUND");
  assert.equal(runtime.counters.updates, 0);
});

test("staged no-op update fails with RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED", async () => {
  const runtime = await runStagedRuntime({ persistenceMode: "noop" });
  assert.equal(runtime.result.error.code, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
  assert.equal(runtime.counters.success, 0);
});

test("changed staged persisted value fails readback", async () => {
  const runtime = await runStagedRuntime({ persistenceMode: "changed-value" });
  assert.equal(runtime.result.error.code, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
  assert.equal(runtime.counters.success, 0);
});

test("changed staged A:C context fails readback", async () => {
  const runtime = await runStagedRuntime({ persistenceMode: "changed-context" });
  assert.equal(runtime.result.error.code, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
  assert.equal(runtime.counters.success, 0);
});

test("staged Source File Hash output equals the new runtime-input SHA-256", async () => {
  const runtime = await runStagedRuntime();
  const column = api.RESULTS_HEADERS.indexOf("Source File Hash");
  assert.equal(runtime.result.summary.source_file_hash, EXPECTED_RUNTIME_FIXTURE_HASH);
  assert.equal(runtime.state.rawGrid[1][column], EXPECTED_RUNTIME_FIXTURE_HASH);
  assert.equal(runtime.state.rawGrid[2][column], EXPECTED_RUNTIME_FIXTURE_HASH);
});

test("staged Source Row Hash values are deterministic for the new source record order", async () => {
  const firstParse = api.parseSource(runtimeFixture);
  const secondParse = api.parseSource(runtimeFixture);
  const firstCandidates = api.requireUniqueCandidates(firstParse.records);
  const secondCandidates = api.requireUniqueCandidates(secondParse.records);
  assert.deepStrictEqual(
    firstCandidates.map((record) => [record.record_order, record.source_row_hash]),
    secondCandidates.map((record) => [record.record_order, record.source_row_hash]),
  );
  assert.deepStrictEqual(
    firstCandidates.map((record) => record.sample_information["Sample Name"]),
    ["P1", "P2"],
  );
  assert.notEqual(firstCandidates[0].source_row_hash, firstCandidates[1].source_row_hash);
  const runtime = await runStagedRuntime();
  const column = api.RESULTS_HEADERS.indexOf("Source Row Hash");
  assert.deepStrictEqual(
    [runtime.state.rawGrid[1][column], runtime.state.rawGrid[2][column]],
    firstCandidates.map((record) => record.source_row_hash),
  );
});

test("staged analytical data are unchanged except contracted IDs and derived row hashes", () => {
  const sourceParsed = api.parseSource(fixture);
  const targetParsed = api.parseSource(runtimeFixture);
  assert.equal(targetParsed.records.length, sourceParsed.records.length);
  sourceParsed.records.forEach((sourceRecord, index) => {
    const targetRecord = targetParsed.records[index];
    assert.deepStrictEqual(
      analyticalRecordProjection(targetRecord),
      analyticalRecordProjection(sourceRecord),
    );
    const sampleName = sourceRecord.sample_information["Sample Name"];
    if (sampleName === "P1" || sampleName === "P2") {
      assert.notEqual(targetRecord.source_row_hash, sourceRecord.source_row_hash);
    } else {
      assert.equal(targetRecord.source_row_hash, sourceRecord.source_row_hash);
    }
  });
  assert.notEqual(targetParsed.source_file_hash, sourceParsed.source_file_hash);
});

test("staged Parser Version output remains the validated Simple Results version", async () => {
  const runtime = await runStagedRuntime();
  const column = api.RESULTS_HEADERS.indexOf("Parser Version");
  assert.equal(api.VERSION, "terpenes-simple-results-v1");
  assert.equal(runtime.state.rawGrid[1][column], api.VERSION);
  assert.equal(runtime.state.rawGrid[2][column], api.VERSION);
});

test("staged Import Status output is the controlled Imported literal", async () => {
  const runtime = await runStagedRuntime();
  const column = api.RESULTS_HEADERS.indexOf("Import Status");
  assert.equal(runtime.state.rawGrid[1][column], "Imported");
  assert.equal(runtime.state.rawGrid[2][column], "Imported");
});

(async () => {
  let passed = 0;
  let failed = 0;
  for (const entry of tests) {
    try {
      await entry.fn();
      passed += 1;
      console.log(`PASS ${entry.name}`);
    } catch (error) {
      failed += 1;
      console.error(`FAIL ${entry.name}`);
      console.error(error && error.stack ? error.stack : error);
    }
  }
  console.log(`TOTAL=${tests.length} PASSED=${passed} FAILED=${failed} SKIPPED=0`);
  if (failed) process.exitCode = 1;
})();
