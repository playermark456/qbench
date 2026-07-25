"use strict";

const assert = require("assert");
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

const BASE = path.resolve(__dirname, "..");
const V1_BASE = path.resolve(BASE, "..", "2026-07-25_terpenes_simple_results_v1");
const SOURCE_PATH = path.join(BASE, "src", "terpenes_simple_results_parser_v2_controls.js");
const ARTIFACT_PATH = path.join(BASE, "dist", "terpenes_simple_results_parser_v2_controls.js");
const WORKSHEET_PATH = path.join(BASE, "SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V2_CONTROLS.json");
const RUNTIME_PATH = path.join(BASE, "runtime", "terpenes_simple_results_310_311_runtime_source.txt");
const BATCH63_RUNTIME_PATH = path.join(BASE, "runtime", "terpenes_simple_results_v2_controls_312_313_runtime_source.txt");
const V1_SOURCE_PATH = path.join(V1_BASE, "src", "terpenes_simple_results_parser.js");
const V1_WORKSHEET_PATH = path.join(V1_BASE, "SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V1__dimension_fix.json");
const V1_RUNTIME_PATH = path.join(V1_BASE, "runtime", "terpenes_simple_results_310_311_runtime_source.txt");

const api = require(SOURCE_PATH);
const v1Api = require(V1_SOURCE_PATH);
const sourceBuffer = fs.readFileSync(RUNTIME_PATH);
const sourceText = fs.readFileSync(RUNTIME_PATH, "utf8");
const sourceHash = sha256Text(sourceText);
const parsed = api.parseSource(sourceText, "terpenes_simple_results_310_311_runtime_source.txt");
const batch63Buffer = fs.readFileSync(BATCH63_RUNTIME_PATH);
const batch63Text = fs.readFileSync(BATCH63_RUNTIME_PATH, "utf8");
const batch63Hash = sha256Text(batch63Text);
const batch63Parsed = api.parseSource(batch63Text, "terpenes_simple_results_v2_controls_312_313_runtime_source.txt");
const worksheet = JSON.parse(fs.readFileSync(WORKSHEET_PATH, "utf8"));
const v1Worksheet = JSON.parse(fs.readFileSync(V1_WORKSHEET_PATH, "utf8"));
const artifactText = fs.readFileSync(ARTIFACT_PATH, "utf8");

const EXPECTED_HASHES = {
  runtime: "1e5087715a9bcf216c2991cca53f41fb4ae84b4f9e80eea0e95d7618ec77a36e",
  batch63_runtime: "6b6a208faa83a16e54aa7168467d2221fa23db8f8c6c8a82d183f2bb235ce2a7",
  artifact: "1c3b0badb33acee3152da95aa40fb8c4332aa465fd1733789456293e0a6c7189",
  worksheet: "80fde1ebb3d4207a2fdcbe297c3b457906cca7355d12ff50baf3e1fca14bfeb3",
  v1_artifact: "bcec7bf0aa1f0b3edfab6ff2f6bcf370abf863226a81472714202aca5efbc871",
  v1_worksheet: "f8d58b33024cce2bf90171df79c7f73e984674fa64b83f99e8030935f9030448",
  protected_v2: "c3f3ecccf346ce1a1338911ee3bcb45ab4c43342d93bcee7b74b2c70fc847e99",
  protected_v3: "5a849a6cf3f78784f728cd89d6665310ddc04e299f769bd3ef5e646e31203e85",
  protected_ws78: "50fb7883a6932bc54b09f6997b91f01674e392696e82f77872935bb00576acda",
  protected_c6: "5de17d8f9eb21a8dfc068daf2297efb707a8b783f63393df432781e5e692e6aa"
};

const PROTECTED = {
  v1_artifact: path.join(V1_BASE, "dist", "terpenes_simple_results_parser_v1.js"),
  v1_worksheet: V1_WORKSHEET_PATH,
  protected_v2: path.resolve(BASE, "..", "2026-07-15_qbench_native_parser_probe", "dist", "terpenes_multirecord_qbench_parser.js"),
  protected_v3: path.resolve(BASE, "..", "2026-07-15_qbench_native_parser_probe", "dist", "terpenes_multirecord_qbench_parser_c6_headerfix_v3.js"),
  protected_ws78: path.resolve(BASE, "..", "2026-07-17_production_candidate", "production_candidates", "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS__v2_formula_fix.json"),
  protected_c6: path.resolve(BASE, "..", "2026-07-15_qbench_native_parser_probe", "runtime", "terpenes_c6_308_309_runtime_source.txt")
};

const tests = [];
function test(name, fn) {
  tests.push({ name, fn });
}

function sha256Text(text) {
  return crypto.createHash("sha256").update(text, "utf8").digest("hex");
}

function sha256File(filePath) {
  return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}

function expectCode(fn, code) {
  assert.throws(fn, function (error) {
    return error && error.code === code;
  }, "Expected error code " + code);
}

async function expectRuntimeCode(runtime, code) {
  const result = await api.executeRuntime(runtime.env);
  assert.strictEqual(result.ok, false);
  assert.strictEqual(result.error.code, code);
  return result;
}

function deepCopy(value) {
  return JSON.parse(JSON.stringify(value));
}

function blankGrid(rows, columns) {
  return Array.from({ length: rows }, function () {
    return Array(columns).fill("");
  });
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

function toAddress(row, column) {
  return columnLetter(column - 1) + row;
}

function makeState(options) {
  const opts = options || {};
  const controlsFixture = Boolean(opts.controlsFixture);
  const grid = blankGrid(api.WORKSHEET_LAST_ROW, api.RESULTS_HEADERS.length);
  grid[0] = api.RESULTS_HEADERS.slice();
  if (controlsFixture) {
    grid[1][0] = "AIT-SAMP-171";
    grid[1][1] = "312";
    grid[1][2] = "Cannabis Concentrates";
    grid[2][0] = "AIT-SAMP-171";
    grid[2][1] = "313";
    grid[2][2] = "Cannabis Concentrates";
  } else {
    grid[1][0] = "SAMPLE-310";
    grid[1][1] = "310";
    grid[1][2] = "Flower";
    grid[2][0] = "SAMPLE-311";
    grid[2][1] = "311";
    grid[2][2] = "Flower";
    grid[3][0] = "UNMATCHED-SAMPLE";
    grid[3][1] = "999";
    grid[3][2] = "Concentrate";
    grid[3][3] = "unmatched-sentinel";
  }
  grid[api.AUDIT_SECTION_ROW - 1] = api.AUDIT_SECTION_VALUES.slice();
  grid[api.AUDIT_HEADER_ROW - 1] = api.AUDIT_HEADERS.slice();
  if (opts.matchedStale) {
    for (let columnIndex = api.PARSER_FIRST_COLUMN; columnIndex <= api.PARSER_LAST_COLUMN; columnIndex += 1) {
      grid[1][columnIndex] = "stale-" + columnIndex;
      grid[2][columnIndex] = "stale-" + columnIndex;
    }
  }
  if (opts.unusedAuditStale) {
    grid[124][0] = "stale-order";
    grid[124][10] = 123;
    grid[129][50] = "stale-status";
  }
  return {
    rawGrid: deepCopy(grid),
    processedGrid: grid.map(function (row) {
      return row.map(function (value) { return value === "" ? "" : String(value); });
    }),
    formulas: { Z87: "=SENTINEL_FORMULA" },
    images: { A1: { id: "sentinel-image" } },
    references: controlsFixture ? { B2: "312", B3: "313" } : { B2: "310", B3: "311", B4: "999" }
  };
}

function gridToMap(grid) {
  const result = {};
  for (let rowIndex = 0; rowIndex < grid.length; rowIndex += 1) {
    for (let columnIndex = 0; columnIndex < grid[rowIndex].length; columnIndex += 1) {
      const value = grid[rowIndex][columnIndex];
      if (value !== "" && value !== null && value !== undefined) {
        result[toAddress(rowIndex + 1, columnIndex + 1)] = value;
      }
    }
  }
  return result;
}

function mapToGrid(map) {
  const grid = blankGrid(api.WORKSHEET_LAST_ROW, api.RESULTS_HEADERS.length);
  Object.keys(map || {}).forEach(function (address) {
    const parsedAddress = coordinates(address);
    if (parsedAddress && parsedAddress.row <= api.WORKSHEET_LAST_ROW && parsedAddress.column <= api.RESULTS_HEADERS.length) {
      grid[parsedAddress.row - 1][parsedAddress.column - 1] = map[address];
    }
  });
  return grid;
}

function documentsFromState(state) {
  return [
    { worksheet_name: "Results", type: "WORKSHEET_DATA", data: deepCopy(state.rawGrid) },
    { worksheet_name: "Results", type: "WORKSHEET_DATA_PROCESSED", data: deepCopy(state.processedGrid) },
    { worksheet_name: "Results", type: "WORKSHEET_FORMULAS", data: deepCopy(state.formulas) },
    { worksheet_name: "Results", type: "WORKSHEET_IMAGE_DATA", data: deepCopy(state.images) },
    { worksheet_name: "Results", type: "WORKSHEET_DOLLAR_REFERENCES", data: deepCopy(state.references) }
  ];
}

function makeRuntime(options) {
  const opts = options || {};
  const state = makeState({
    controlsFixture: Boolean(opts.controlsFixture),
    matchedStale: Boolean(opts.matchedStale),
    unusedAuditStale: Boolean(opts.unusedAuditStale)
  });
  const counters = {
    batch_constructs: 0,
    dynamic_reads: 0,
    batch_updates: 0,
    test_service_constructs: 0,
    success_calls: 0,
    error_calls: 0
  };
  const events = [];
  const logs = [];
  let updatePayload = null;

  function mutateReadback(mode) {
    if (mode === "missing-audit-row") {
      state.rawGrid[90][0] = "";
      state.processedGrid[90][0] = "";
    } else if (mode === "duplicate-audit-order") {
      state.rawGrid[91][0] = 1;
      state.processedGrid[91][0] = "1";
    } else if (mode === "changed-audit-value") {
      state.rawGrid[90][9] = "changed";
      state.processedGrid[90][9] = "changed";
    } else if (mode === "changed-dynamic-value") {
      state.rawGrid[1][9] = "changed";
      state.processedGrid[1][9] = "changed";
    } else if (mode === "changed-context") {
      state.rawGrid[1][0] = "changed-context";
      state.processedGrid[1][0] = "changed-context";
    } else if (mode === "stale-unused-after-readback") {
      state.rawGrid[124][0] = "returned-stale";
      state.processedGrid[124][0] = "returned-stale";
    } else if (mode === "changed-audit-header") {
      state.rawGrid[89][0] = "Changed Record Order";
      state.processedGrid[89][0] = "Changed Record Order";
    } else if (mode === "changed-maps") {
      state.formulas.Z87 = "=CHANGED";
    } else if (mode === "missing-dynamic-row") {
      state.rawGrid[1][1] = "";
      state.processedGrid[1][1] = "";
    } else if (mode === "missing-dynamic-source") {
      state.rawGrid[1][1] = "";
      state.processedGrid[1][1] = "";
    } else if (mode === "missing-dynamic-target") {
      state.rawGrid[2][1] = "";
      state.processedGrid[2][1] = "";
    } else if (mode === "duplicate-dynamic-source") {
      state.rawGrid[3][1] = "312";
      state.processedGrid[3][1] = "312";
    } else if (mode === "duplicate-dynamic-target") {
      state.rawGrid[3][1] = "313";
      state.processedGrid[3][1] = "313";
    }
  }

  class QBBatchService {
    constructor() {
      counters.batch_constructs += 1;
      events.push("construct");
    }

    getJson(request) {
      if (request.url === "/batches/get") {
        const id = String(request.urlParams.test_id);
        events.push("resolve:" + id);
        if (opts.unknownTestId === id) {
          request.success([]);
          return undefined;
        }
        const expectedBatchId = Object.prototype.hasOwnProperty.call(opts, "batchId") ? Number(opts.batchId) : (opts.controlsFixture ? 63 : 62);
        if (opts.ambiguousTestId === id) {
          request.success([{ id: expectedBatchId }, { id: expectedBatchId + 1 }]);
          return undefined;
        }
        const alternateCandidate = opts.controlsFixture ? "313" : "311";
        const batchId = opts.multipleBatches && id === alternateCandidate ? expectedBatchId + 1 : expectedBatchId;
        request.success([{ id: batchId }]);
        return undefined;
      }
      if (request.url === "/batches/worksheets/dynamic") {
        counters.dynamic_reads += 1;
        events.push("dynamic:" + counters.dynamic_reads);
        request.success(documentsFromState(state));
        return undefined;
      }
      request.error(new Error("unexpected getJson route"));
      return undefined;
    }

    update(request) {
      counters.batch_updates += 1;
      events.push("update");
      updatePayload = deepCopy(request);
      if (opts.updateFailure) {
        request.error(new Error("forced update failure"));
        return;
      }
      if (opts.persistenceMode !== "no-op") {
        const payload = request.data.qb_dynamic_spreadsheet_data.Results;
        state.rawGrid = mapToGrid(payload.WORKSHEET_DATA);
        state.processedGrid = mapToGrid(payload.WORKSHEET_DATA_PROCESSED);
        state.formulas = deepCopy(payload.WORKSHEET_FORMULAS);
        state.images = deepCopy(payload.WORKSHEET_IMAGE_DATA);
        state.references = deepCopy(payload.WORKSHEET_DOLLAR_REFERENCES);
      }
      mutateReadback(opts.persistenceMode);
      request.success({ ok: true });
      return undefined;
    }
  }

  const env = {
    QBBatchService: QBBatchService,
    QB: {
      files: [{
        name: opts.controlsFixture ? "terpenes_simple_results_v2_controls_312_313_runtime_source.txt" : "terpenes_simple_results_310_311_runtime_source.txt",
        text: async function () {
          if (Object.prototype.hasOwnProperty.call(opts, "source")) return opts.source;
          return opts.controlsFixture ? batch63Text : sourceText;
        }
      }],
      console: {
        clear: function () {},
        log: function (value) { logs.push(String(value)); }
      },
      progressBar: {
        setPercentage: function (value) { events.push("progress:" + value); }
      },
      success: function () {
        counters.success_calls += 1;
        events.push("success");
      },
      error: function () {
        counters.error_calls += 1;
        events.push("error");
      }
    }
  };

  return {
    env: env,
    counters: counters,
    events: events,
    logs: logs,
    getState: function () { return state; },
    getUpdatePayload: function () { return updatePayload; }
  };
}

function worksheetSheet(document) {
  assert.strictEqual(document.config.worksheets.length, 1);
  return document.config.worksheets[0];
}

function coordinates(address) {
  const match = /^([A-Z]+)(\d+)$/.exec(address);
  if (!match) return null;
  let column = 0;
  for (const character of match[1]) column = column * 26 + character.charCodeAt(0) - 64;
  return { row: Number(match[2]), column: column };
}

function collectAddresses(value, results) {
  const output = results || [];
  if (Array.isArray(value)) {
    value.forEach(function (entry) { collectAddresses(entry, output); });
  } else if (value && typeof value === "object") {
    Object.entries(value).forEach(function (entry) {
      collectAddresses(entry[0], output);
      collectAddresses(entry[1], output);
    });
  } else if (typeof value === "string") {
    const matches = value.match(/[A-Z]{1,3}[1-9]\d*/g) || [];
    matches.forEach(function (address) {
      if (coordinates(address)) output.push(address);
    });
  }
  return output;
}

function addressEntriesThrough(entries, lastRow) {
  if (Array.isArray(entries)) {
    return entries.filter(function (entry) {
      const parsedAddress = coordinates(entry.address);
      return parsedAddress && parsedAddress.row <= lastRow;
    });
  }
  return Object.fromEntries(Object.entries(entries || {}).filter(function (entry) {
    const parsedAddress = coordinates(entry[0]);
    return parsedAddress && parsedAddress.row <= lastRow;
  }));
}

function sourceRecords(source) {
  return source.split(/(?=^\[Header\]\r?$)/m).filter(function (part) {
    return /^\[Header\]\r?$/m.test(part);
  });
}

function classificationVector(records) {
  return records.map(function (record) {
    return [record.record_order, record.category, record.sample_information["Sample ID"]];
  });
}

function isBlank(value) {
  return value === "" || value === null || value === undefined;
}

function byteDifferences(left, right) {
  assert.strictEqual(left.length, right.length);
  const differences = [];
  for (let index = 0; index < left.length; index += 1) {
    if (left[index] !== right[index]) {
      differences.push({ offset: index, old: left[index], new: right[index] });
    }
  }
  return differences;
}

function categoryCounts(records) {
  return records.reduce(function (result, record) {
    result[record.category] = (result[record.category] || 0) + 1;
    return result;
  }, {});
}

function analyticallyComparableRecords(records) {
  return deepCopy(records).map(function (record) {
    delete record.source_row_hash;
    if (record.sample_information["Sample Name"] === "P1" || record.sample_information["Sample Name"] === "P2") {
      delete record.sample_information["Sample ID"];
    }
    return record;
  });
}

// A. Preflight protection and V1 baseline.
test("A01 runtime fixture hash matches the approved V1 proof input", function () {
  assert.strictEqual(sha256File(RUNTIME_PATH), EXPECTED_HASHES.runtime);
});

test("A02 V1 parser artifact remains byte-identical", function () {
  assert.strictEqual(sha256File(PROTECTED.v1_artifact), EXPECTED_HASHES.v1_artifact);
});

test("A03 V1 corrected worksheet remains byte-identical", function () {
  assert.strictEqual(sha256File(PROTECTED.v1_worksheet), EXPECTED_HASHES.v1_worksheet);
});

test("A04 protected multi-tab V2 parser remains byte-identical", function () {
  assert.strictEqual(sha256File(PROTECTED.protected_v2), EXPECTED_HASHES.protected_v2);
});

test("A05 protected multi-tab V3 parser remains byte-identical", function () {
  assert.strictEqual(sha256File(PROTECTED.protected_v3), EXPECTED_HASHES.protected_v3);
});

test("A06 protected worksheet 78 candidate remains byte-identical", function () {
  assert.strictEqual(sha256File(PROTECTED.protected_ws78), EXPECTED_HASHES.protected_ws78);
});

test("A07 protected C6 diagnostic source remains byte-identical", function () {
  assert.strictEqual(sha256File(PROTECTED.protected_c6), EXPECTED_HASHES.protected_c6);
});

// B. Worksheet layout.
test("B01 worksheet contains exactly one tab named Results", function () {
  assert.deepStrictEqual(worksheet.config.worksheets.map(function (sheet) { return sheet.worksheetName; }), ["Results"]);
});

test("B02 worksheet dimensions are exactly AY190", function () {
  const sheet = worksheetSheet(worksheet);
  assert.deepStrictEqual(sheet.minDimensions, [51, 190]);
  assert.strictEqual(sheet.data.length, 190);
  assert.ok(sheet.data.every(function (row) { return row.length === 51; }));
});

test("B03 rows 1 through 87 data remain identical to V1", function () {
  assert.deepStrictEqual(worksheetSheet(worksheet).data.slice(0, 87), worksheetSheet(v1Worksheet).data.slice(0, 87));
});

test("B04 rows 1 through 87 row configuration remains identical to V1", function () {
  assert.deepStrictEqual(worksheetSheet(worksheet).rows.slice(0, 87), worksheetSheet(v1Worksheet).rows.slice(0, 87));
});

test("B05 rows 1 through 87 cell configuration remains identical to V1", function () {
  assert.deepStrictEqual(
    addressEntriesThrough(worksheetSheet(worksheet).cells, 87),
    addressEntriesThrough(worksheetSheet(v1Worksheet).cells, 87)
  );
});

test("B06 row 88 is completely blank", function () {
  assert.ok(worksheetSheet(worksheet).data[87].every(isBlank));
});

test("B07 row 89 is the fixed Run Records section row", function () {
  assert.deepStrictEqual(worksheetSheet(worksheet).data[88], api.AUDIT_SECTION_VALUES);
});

test("B08 row 90 is the exact fixed audit header", function () {
  assert.deepStrictEqual(worksheetSheet(worksheet).data[89], api.AUDIT_HEADERS);
  assert.strictEqual(api.AUDIT_HEADERS.length, 51);
});

test("B09 rows 91 through 190 are blank audit capacity", function () {
  assert.ok(worksheetSheet(worksheet).data.slice(90).every(function (row) {
    return row.every(isBlank);
  }));
});

test("B10 candidate contains no formula values", function () {
  const serialized = JSON.stringify(worksheet);
  assert.ok(!/"=[^"]*"/.test(serialized));
});

test("B11 candidate contains no forbidden worksheet tabs", function () {
  const names = worksheet.config.worksheets.map(function (sheet) { return sheet.worksheetName; });
  ["Instrument Import", "Test Transfer", "Run Setup", "Batch Review"].forEach(function (name) {
    assert.ok(!names.includes(name));
  });
});

test("B12 the dynamic Test context remains generic and fixture-independent", function () {
  const rows = worksheetSheet(worksheet).data.slice(1, 87);
  assert.deepStrictEqual(rows, worksheetSheet(v1Worksheet).data.slice(1, 87));
  assert.ok(rows.every(function (row) { return row.slice(3).every(isBlank); }));
  assert.ok(!JSON.stringify(rows).includes('"310"'));
  assert.ok(!JSON.stringify(rows).includes('"311"'));
});

test("B13 no configured worksheet address exceeds AY190", function () {
  const addresses = collectAddresses(worksheet);
  assert.ok(addresses.length > 0);
  addresses.forEach(function (address) {
    const parsedAddress = coordinates(address);
    assert.ok(parsedAddress.column <= 51, address + " exceeds AY");
    assert.ok(parsedAddress.row <= 190, address + " exceeds row 190");
  });
});

test("B14 audit rows 91 through 190 are parser-owned editable cells", function () {
  const cells = worksheetSheet(worksheet).cells;
  for (let row = 91; row <= 190; row += 1) {
    for (let column = 1; column <= 51; column += 1) {
      assert.strictEqual(cells[toAddress(row, column)].readonly, false);
    }
  }
});

// C. Parsing and classification.
test("C01 complete runtime source parses 34 records", function () {
  assert.strictEqual(parsed.records.length, 34);
});

test("C02 every record has 23 reportable analytes and Dimethylacetamide audit", function () {
  parsed.records.forEach(function (record) {
    assert.strictEqual(record.counts.compound_result_row_count, 24);
    assert.strictEqual(record.reportable_analytes.length, 23);
    assert.strictEqual(record.dimethylacetamide_audit.reportable, false);
  });
});

test("C03 Unicode controlled analyte labels remain exact", function () {
  ["α-Pinene", "β-Myrcene", "(-)-β-pinene", "γ-Terpinene", "β-Caryophyllene", "α-Humulene", "(-)-α-Bisabolol"].forEach(function (label) {
    assert.ok(api.REPORTABLE_ANALYTES.map(function (analyte) { return analyte.label; }).includes(label));
  });
});

test("C04 classification vector matches the complete approved sequence", function () {
  assert.deepStrictEqual(classificationVector(parsed.records), [
    [1, "Null", "Null"], [2, "Blank", ""],
    [3, "System Suitability", ""], [4, "System Suitability", ""], [5, "System Suitability", ""],
    [6, "Null", "Null"],
    [7, "Standard", "10 �g/mL"], [8, "Standard", "25 �g/mL"], [9, "Standard", "50 �g/mL"], [10, "Standard", "100 �g/mL"], [11, "Standard", "300 �g/mL"], [12, "Standard", "1000 �g/mL"],
    [13, "Blank", ""], [14, "CCV", ""], [15, "LOQ", ""], [16, "Matrix Blank", "Matrix Blank"],
    [17, "Sample", "310"], [18, "Sample", "311"],
    [19, "Validation", "Low 3"], [20, "Validation", "Low 4"], [21, "Validation", "Low 5"],
    [22, "Validation", "Medium 1"], [23, "Validation", "Medium 2"], [24, "Validation", "Medium 3"],
    [25, "CCV", ""],
    [26, "Validation", "Medium 4"], [27, "Validation", "Medium 5"],
    [28, "Validation", "High 1"], [29, "Validation", "High 2"], [30, "Validation", "High 3"], [31, "Validation", "High 4"], [32, "Validation", "High 5"],
    [33, "Null", "Null"], [34, "CCV", ""]
  ]);
});

test("C05 classification counts are exact", function () {
  const counts = parsed.records.reduce(function (result, record) {
    result[record.category] = (result[record.category] || 0) + 1;
    return result;
  }, {});
  assert.deepStrictEqual(counts, {
    Null: 3,
    Blank: 2,
    "System Suitability": 3,
    Standard: 6,
    CCV: 3,
    LOQ: 1,
    "Matrix Blank": 1,
    Sample: 2,
    Validation: 13
  });
});

test("C06 validation Low and Medium and High identities remain visible", function () {
  const labels = parsed.records.filter(function (record) {
    return record.category === "Validation";
  }).map(function (record) {
    return record.sample_information["Sample ID"];
  });
  assert.deepStrictEqual(labels, [
    "Low 3", "Low 4", "Low 5",
    "Medium 1", "Medium 2", "Medium 3",
    "Medium 4", "Medium 5",
    "High 1", "High 2", "High 3", "High 4", "High 5"
  ]);
});

test("C07 malformed Compound Results section fails closed", function () {
  const malformed = sourceText.replace("[Compound Results(Ch1)]", "[Compound Results Broken]");
  expectCode(function () { api.parseSource(malformed, "malformed.txt"); }, "MISSING_REQUIRED_SECTION");
});

test("C08 wrong controlled compound count fails closed", function () {
  const lines = sourceText.split(/\r?\n/);
  const section = lines.indexOf("[Compound Results(Ch1)]");
  const header = lines.findIndex(function (line, index) {
    return index > section && line.startsWith("ID#\t");
  });
  lines.splice(header + 1, 1);
  const malformed = lines.join("\n");
  expectCode(function () { api.parseSource(malformed, "wrong-count.txt"); }, "INVALID_CONTROLLED_COMPOUND_RESULTS");
});

// D. Audit staging.
test("D01 audit capacity is exactly 100 records", function () {
  assert.strictEqual(api.AUDIT_CAPACITY, 100);
  assert.strictEqual(api.AUDIT_FIRST_DATA_ROW, 91);
  assert.strictEqual(api.AUDIT_LAST_DATA_ROW, 190);
});

test("D02 record N maps deterministically to worksheet row 90 plus N", function () {
  const bundle = api.requireResultsBundle(documentsFromState(makeState()));
  const plan = api.planAuditRows(bundle, parsed.records, sourceHash);
  assert.deepStrictEqual(plan.rows.map(function (row) { return row.row; }), Array.from({ length: 34 }, function (_, index) { return 91 + index; }));
});

test("D03 all 34 records are staged in source order", function () {
  const bundle = api.requireResultsBundle(documentsFromState(makeState()));
  const plan = api.planAuditRows(bundle, parsed.records, sourceHash);
  assert.strictEqual(plan.rows.length, 34);
  plan.rows.forEach(function (rowPlan, index) {
    assert.strictEqual(rowPlan.values[0], index + 1);
    assert.strictEqual(rowPlan.record.record_order, index + 1);
  });
});

test("D04 audit rows carry category and original Sample ID", function () {
  const bundle = api.requireResultsBundle(documentsFromState(makeState()));
  const plan = api.planAuditRows(bundle, parsed.records, sourceHash);
  assert.deepStrictEqual(plan.rows[0].values.slice(0, 3), [1, "Null", "Null"]);
  assert.deepStrictEqual(plan.rows[16].values.slice(0, 3), [17, "Sample", "310"]);
  assert.deepStrictEqual(plan.rows[17].values.slice(0, 3), [18, "Sample", "311"]);
});

test("D05 Sample records appear in both dynamic and audit regions", function () {
  const bundle = api.requireResultsBundle(documentsFromState(makeState()));
  const candidates = api.planCandidateRows(bundle, api.requireUniqueCandidates(parsed.records), sourceHash);
  const audit = api.planAuditRows(bundle, parsed.records, sourceHash);
  assert.deepStrictEqual(candidates.map(function (plan) { return plan.id; }), ["310", "311"]);
  assert.deepStrictEqual(audit.rows.filter(function (plan) {
    return plan.record.category === "Sample";
  }).map(function (plan) {
    return plan.values[2];
  }), ["310", "311"]);
});

test("D06 exactly 100 complete records are accepted", function () {
  const record = sourceRecords(sourceText)[0];
  assert.strictEqual(api.parseSource(Array(100).fill(record).join(""), "100-records.txt").records.length, 100);
});

test("D07 101 complete records fail with RUN_RECORD_CAPACITY_EXCEEDED", function () {
  const record = sourceRecords(sourceText)[0];
  expectCode(function () {
    api.parseSource(Array(101).fill(record).join(""), "101-records.txt");
  }, "RUN_RECORD_CAPACITY_EXCEEDED");
});

test("D08 record 100 maps to row 190 without truncation", function () {
  const recordText = sourceRecords(sourceText)[0];
  const parsed100 = api.parseSource(Array(100).fill(recordText).join(""), "100-records.txt");
  const bundle = api.requireResultsBundle(documentsFromState(makeState()));
  const plan = api.planAuditRows(bundle, parsed100.records, parsed100.source_file_hash);
  assert.strictEqual(plan.rows.length, 100);
  assert.strictEqual(plan.rows[99].record_order, 100);
  assert.strictEqual(plan.rows[99].row, 190);
});

// E. Dynamic compatibility.
test("E01 transfer candidates remain exactly 310 and 311", function () {
  assert.deepStrictEqual(api.requireUniqueCandidates(parsed.records).map(api.candidateTestId), ["310", "311"]);
});

test("E02 controls and validations do not become dynamic candidates", function () {
  parsed.records.filter(function (record) {
    return record.category !== "Sample";
  }).forEach(function (record) {
    assert.strictEqual(api.candidateTestId(record), "");
  });
});

test("E03 dynamic Test-ID row map requires exact unique matches", function () {
  const bundle = api.requireResultsBundle(documentsFromState(makeState()));
  assert.deepStrictEqual(api.planCandidateRows(bundle, api.requireUniqueCandidates(parsed.records), sourceHash).map(function (plan) {
    return [plan.id, plan.row];
  }), [["310", 2], ["311", 3]]);
});

test("E04 dynamic parser-owned values match V1 except Parser Version", function () {
  const v2Values = api.buildParserOwnedValues(parsed.records[16], sourceHash);
  const v1Parsed = v1Api.parseSource(sourceText, "terpenes_simple_results_310_311_runtime_source.txt");
  const v1Values = v1Api.buildParserOwnedValues(v1Parsed.records[16], sourceHash);
  const differing = [];
  for (let index = 0; index < v2Values.length; index += 1) {
    if (v2Values[index] !== v1Values[index]) differing.push(index);
  }
  assert.deepStrictEqual(differing, [42]);
  assert.strictEqual(v2Values[42], api.VERSION);
});

test("E05 duplicate candidate Test IDs fail", function () {
  const duplicate = deepCopy(parsed.records);
  duplicate[17].sample_information["Sample ID"] = "310";
  expectCode(function () { api.requireUniqueCandidates(duplicate); }, "DUPLICATE_CANDIDATE_TEST_ID");
});

test("E06 missing Results Test row fails", function () {
  const state = makeState();
  state.rawGrid[2][1] = "";
  state.processedGrid[2][1] = "";
  delete state.references.B3;
  const bundle = api.requireResultsBundle(documentsFromState(state));
  expectCode(function () {
    api.planCandidateRows(bundle, api.requireUniqueCandidates(parsed.records), sourceHash);
  }, "RESULTS_TEST_ID_MISSING");
});

test("E07 duplicate Results Test row fails", function () {
  const state = makeState();
  state.rawGrid[4][1] = "310";
  state.processedGrid[4][1] = "310";
  state.references.B5 = "310";
  const bundle = api.requireResultsBundle(documentsFromState(state));
  expectCode(function () {
    api.planCandidateRows(bundle, api.requireUniqueCandidates(parsed.records), sourceHash);
  }, "RESULTS_TEST_ID_DUPLICATE");
});

// F. One-service and one-update boundary.
test("F01 artifact constructs exactly one QBBatchService", function () {
  assert.strictEqual((artifactText.match(/new env\.QBBatchService\(/g) || []).length, 1);
});

test("F02 artifact calls Batch update exactly once", function () {
  assert.strictEqual((artifactText.match(/batchService\.update\(/g) || []).length, 1);
});

test("F03 artifact contains no Test service or direct Test write", function () {
  assert.strictEqual((artifactText.match(/QBTestService/g) || []).length, 0);
  assert.strictEqual((artifactText.match(/testService\.(?:update|create|delete)/g) || []).length, 0);
});

test("F04 runtime uses one QBBatchService and one update", async function () {
  const runtime = makeRuntime();
  await api.executeRuntime(runtime.env);
  assert.strictEqual(runtime.counters.batch_constructs, 1);
  assert.strictEqual(runtime.counters.batch_updates, 1);
  assert.strictEqual(runtime.counters.test_service_constructs, 0);
});

test("F05 update contains exactly one worksheet key Results", async function () {
  const runtime = makeRuntime();
  await api.executeRuntime(runtime.env);
  assert.deepStrictEqual(Object.keys(runtime.getUpdatePayload().data.qb_dynamic_spreadsheet_data), ["Results"]);
});

test("F06 update preserves formulas images and dollar references", async function () {
  const runtime = makeRuntime();
  await api.executeRuntime(runtime.env);
  const results = runtime.getUpdatePayload().data.qb_dynamic_spreadsheet_data.Results;
  assert.deepStrictEqual(results.WORKSHEET_FORMULAS, { Z87: "=SENTINEL_FORMULA" });
  assert.deepStrictEqual(results.WORKSHEET_IMAGE_DATA, { A1: { id: "sentinel-image" } });
  assert.deepStrictEqual(results.WORKSHEET_DOLLAR_REFERENCES, { B2: "310", B3: "311", B4: "999" });
});

test("F07 update requests worksheet calculations", async function () {
  const runtime = makeRuntime();
  await api.executeRuntime(runtime.env);
  assert.strictEqual(runtime.getUpdatePayload().urlParams.run_worksheet_calculations, true);
});

test("F08 101-record capacity failure occurs before service construction or update", async function () {
  const record = sourceRecords(sourceText)[0];
  const runtime = makeRuntime({ source: Array(101).fill(record).join("") });
  await expectRuntimeCode(runtime, "RUN_RECORD_CAPACITY_EXCEEDED");
  assert.strictEqual(runtime.counters.batch_constructs, 0);
  assert.strictEqual(runtime.counters.batch_updates, 0);
});

test("F09 candidates resolving to multiple Batches fail before update", async function () {
  const runtime = makeRuntime({ multipleBatches: true });
  await expectRuntimeCode(runtime, "CANDIDATES_RESOLVE_TO_MULTIPLE_BATCHES");
  assert.strictEqual(runtime.counters.batch_updates, 0);
});

test("F10 unknown Test ID fails before update", async function () {
  const runtime = makeRuntime({ unknownTestId: "311" });
  await expectRuntimeCode(runtime, "TEST_ID_NOT_FOUND");
  assert.strictEqual(runtime.counters.batch_updates, 0);
});

test("F11 dynamic and audit changes share the same Results payload", async function () {
  const runtime = makeRuntime();
  await api.executeRuntime(runtime.env);
  const data = runtime.getUpdatePayload().data.qb_dynamic_spreadsheet_data.Results.WORKSHEET_DATA;
  assert.strictEqual(data.D2, "P1");
  assert.strictEqual(data.D3, "P2");
  assert.strictEqual(data.A91, 1);
  assert.strictEqual(data.A124, 34);
});

// G. Stale clearing.
test("G01 stale clearing targets only nonblank unused audit cells", function () {
  const bundle = api.requireResultsBundle(documentsFromState(makeState({ unusedAuditStale: true })));
  const plan = api.planAuditRows(bundle, parsed.records, sourceHash);
  assert.deepStrictEqual(plan.stale_cells.map(function (cell) { return toAddress(cell.row, cell.column + 1); }), ["A125", "K125", "AY130"]);
  assert.deepStrictEqual(plan.stale_rows, [125, 130]);
});

test("G02 already blank unused audit cells are not staged", function () {
  const bundle = api.requireResultsBundle(documentsFromState(makeState({ unusedAuditStale: true })));
  const plan = api.planAuditRows(bundle, parsed.records, sourceHash);
  assert.ok(!plan.stale_cells.some(function (cell) { return cell.row === 125 && cell.column === 1; }));
});

test("G03 stale clearing never targets dynamic rows or audit labels", function () {
  const bundle = api.requireResultsBundle(documentsFromState(makeState({ unusedAuditStale: true })));
  const plan = api.planAuditRows(bundle, parsed.records, sourceHash);
  assert.ok(plan.stale_cells.every(function (cell) {
    return cell.row >= 125 && cell.row <= 190;
  }));
});

test("G04 stale unused audit cells are blank after a successful update", async function () {
  const runtime = makeRuntime({ unusedAuditStale: true });
  await api.executeRuntime(runtime.env);
  assert.strictEqual(runtime.getState().rawGrid[124][0], "");
  assert.strictEqual(runtime.getState().rawGrid[124][10], "");
  assert.strictEqual(runtime.getState().rawGrid[129][50], "");
});

test("G05 unmatched dynamic rows remain byte-for-byte unchanged", async function () {
  const runtime = makeRuntime({ unusedAuditStale: true });
  const before = deepCopy(runtime.getState().rawGrid.slice(3, 87));
  await api.executeRuntime(runtime.env);
  assert.deepStrictEqual(runtime.getState().rawGrid.slice(3, 87), before);
});

// H. Readback.
test("H01 successful persistence passes verified readback", async function () {
  const runtime = makeRuntime();
  const result = await api.executeRuntime(runtime.env);
  assert.strictEqual(result.summary.dynamic_rows_read_back, 2);
  assert.strictEqual(result.summary.audit_rows_read_back, 34);
  assert.strictEqual(runtime.counters.success_calls, 1);
});

test("H02 QB.success occurs after the second worksheet read", async function () {
  const runtime = makeRuntime();
  await api.executeRuntime(runtime.env);
  assert.ok(runtime.events.indexOf("success") > runtime.events.lastIndexOf("dynamic:2"));
});

test("H03 no-op update fails readback and does not retry", async function () {
  const runtime = makeRuntime({ persistenceMode: "no-op" });
  await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
  assert.strictEqual(runtime.counters.batch_updates, 1);
  assert.strictEqual(runtime.counters.success_calls, 0);
});

test("H04 missing audit row fails readback", async function () {
  const runtime = makeRuntime({ persistenceMode: "missing-audit-row" });
  await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("H05 duplicate audit record order fails readback", async function () {
  const runtime = makeRuntime({ persistenceMode: "duplicate-audit-order" });
  await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("H06 changed audit value fails readback", async function () {
  const runtime = makeRuntime({ persistenceMode: "changed-audit-value" });
  await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("H07 changed dynamic value fails readback", async function () {
  const runtime = makeRuntime({ persistenceMode: "changed-dynamic-value" });
  await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("H08 changed A:C context fails readback", async function () {
  const runtime = makeRuntime({ persistenceMode: "changed-context" });
  await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("H09 stale value returned in unused audit capacity fails readback", async function () {
  const runtime = makeRuntime({ persistenceMode: "stale-unused-after-readback" });
  await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("H10 changed audit header fails readback", async function () {
  const runtime = makeRuntime({ persistenceMode: "changed-audit-header" });
  await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("H11 altered worksheet maps fail readback", async function () {
  const runtime = makeRuntime({ persistenceMode: "changed-maps" });
  await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("H12 missing dynamic Test row fails readback", async function () {
  const runtime = makeRuntime({ persistenceMode: "missing-dynamic-row" });
  await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

// I. Parser-owned values and ownership.
test("I01 matched dynamic rows set every parser-owned D:AY cell", async function () {
  const runtime = makeRuntime({ matchedStale: true });
  await api.executeRuntime(runtime.env);
  const row310 = runtime.getState().rawGrid[1];
  const expected = api.buildParserOwnedValues(parsed.records[16], sourceHash);
  assert.deepStrictEqual(row310.slice(3), expected);
});

test("I02 matched dynamic A:C context is preserved", async function () {
  const runtime = makeRuntime();
  await api.executeRuntime(runtime.env);
  assert.deepStrictEqual(runtime.getState().rawGrid[1].slice(0, 3), ["SAMPLE-310", "310", "Flower"]);
  assert.deepStrictEqual(runtime.getState().rawGrid[2].slice(0, 3), ["SAMPLE-311", "311", "Flower"]);
});

test("I03 explicit blanks clear stale parser-owned values in matched rows", function () {
  const bundle = api.requireResultsBundle(documentsFromState(makeState({ matchedStale: true })));
  const record = deepCopy(parsed.records[16]);
  record.sample_information["Sample Type"] = "";
  const candidatePlans = api.planCandidateRows(bundle, [record], sourceHash);
  const auditPlan = api.planAuditRows(bundle, parsed.records, sourceHash);
  const update = api.applyResultsPlans(bundle, candidatePlans, auditPlan);
  assert.strictEqual(update.WORKSHEET_DATA.E2, "");
  assert.strictEqual(update.WORKSHEET_DATA_PROCESSED.E2, "");
});

test("I04 parser writes Imported as a controlled literal", async function () {
  const runtime = makeRuntime();
  await api.executeRuntime(runtime.env);
  assert.strictEqual(runtime.getState().rawGrid[1][50], "Imported");
  assert.strictEqual(runtime.getState().rawGrid[2][50], "Imported");
});

test("I05 Results header and fixed label rows are unchanged after update", async function () {
  const runtime = makeRuntime();
  const before = deepCopy(runtime.getState().rawGrid);
  await api.executeRuntime(runtime.env);
  [0, 87, 88, 89].forEach(function (rowIndex) {
    assert.deepStrictEqual(runtime.getState().rawGrid[rowIndex], before[rowIndex]);
  });
});

// J. Category isolation.
test("J01 only Sample category records with nonblank IDs can transfer", function () {
  parsed.records.forEach(function (record) {
    const id = api.candidateTestId(record);
    assert.strictEqual(Boolean(id), record.category === "Sample" && Boolean(record.sample_information["Sample ID"]));
  });
});

test("J02 control-like words inside an ordinary Sample name do not force Validation classification", function () {
  const record = deepCopy(parsed.records[16]);
  record.sample_information["Sample Name"] = "High Quality Customer Sample";
  record.sample_information["Sample ID"] = "777";
  assert.strictEqual(api.classifyRecord(record.sample_information), "Sample");
});

test("J03 Null category records remain audit-only", function () {
  assert.ok(parsed.records.filter(function (record) {
    return record.category === "Null";
  }).every(function (record) {
    return api.candidateTestId(record) === "";
  }));
});

test("J04 System Suitability records remain audit-only", function () {
  assert.ok(parsed.records.filter(function (record) {
    return record.category === "System Suitability";
  }).every(function (record) {
    return api.candidateTestId(record) === "";
  }));
});

test("J05 Standard records remain audit-only", function () {
  assert.ok(parsed.records.filter(function (record) {
    return record.category === "Standard";
  }).every(function (record) {
    return api.candidateTestId(record) === "";
  }));
});

test("J06 CCV LOQ Matrix Blank and Blank records remain audit-only", function () {
  const categories = new Set(["CCV", "LOQ", "Matrix Blank", "Blank"]);
  assert.ok(parsed.records.filter(function (record) {
    return categories.has(record.category);
  }).every(function (record) {
    return api.candidateTestId(record) === "";
  }));
});

test("J07 Validation Low Medium and High records remain audit-only", function () {
  assert.ok(parsed.records.filter(function (record) {
    return record.category === "Validation";
  }).every(function (record) {
    return api.candidateTestId(record) === "";
  }));
});

// K. Exact fixture proof.
test("K01 runtime summary proves 34 audit rows and two dynamic rows", async function () {
  const runtime = makeRuntime();
  const result = await api.executeRuntime(runtime.env);
  assert.strictEqual(result.summary.records_parsed, 34);
  assert.strictEqual(result.summary.audit_rows_staged, 34);
  assert.strictEqual(result.summary.dynamic_rows_written, 2);
  assert.deepStrictEqual(result.summary.matched_test_ids, ["310", "311"]);
});

test("K02 P1 and P2 analytes in dynamic rows match source parsing", async function () {
  const runtime = makeRuntime();
  await api.executeRuntime(runtime.env);
  [16, 17].forEach(function (recordIndex, offset) {
    const expected = api.REPORTABLE_ANALYTES.map(function (analyte) {
      return parsed.records[recordIndex].reportable_analytes.find(function (value) {
        return value.internal_key === analyte.key;
      }).conc;
    });
    assert.deepStrictEqual(runtime.getState().rawGrid[offset + 1].slice(9, 32), expected);
  });
});

test("K03 every audit row matches its deterministic source record values", async function () {
  const runtime = makeRuntime();
  await api.executeRuntime(runtime.env);
  parsed.records.forEach(function (record, index) {
    assert.deepStrictEqual(runtime.getState().rawGrid[90 + index], api.buildAuditValues(record, sourceHash));
  });
});

test("K04 Source File Hash matches the immutable runtime source in both regions", async function () {
  const runtime = makeRuntime();
  await api.executeRuntime(runtime.env);
  const sourceHashColumn = api.RESULTS_HEADERS.indexOf("Source File Hash");
  assert.strictEqual(runtime.getState().rawGrid[1][sourceHashColumn], sourceHash);
  assert.strictEqual(runtime.getState().rawGrid[2][sourceHashColumn], sourceHash);
  parsed.records.forEach(function (_, index) {
    assert.strictEqual(runtime.getState().rawGrid[90 + index][sourceHashColumn], sourceHash);
  });
});

test("K05 Source Row Hash follows the controlled dynamic and audit contracts", async function () {
  const runtime = makeRuntime();
  await api.executeRuntime(runtime.env);
  const sourceRowHashColumn = api.RESULTS_HEADERS.indexOf("Source Row Hash");
  assert.strictEqual(runtime.getState().rawGrid[1][sourceRowHashColumn], parsed.records[16].source_row_hash);
  assert.strictEqual(runtime.getState().rawGrid[2][sourceRowHashColumn], parsed.records[17].source_row_hash);
  assert.strictEqual(runtime.getState().rawGrid[106][sourceRowHashColumn], sha256Text(sourceHash + ":17"));
  assert.strictEqual(runtime.getState().rawGrid[107][sourceRowHashColumn], sha256Text(sourceHash + ":18"));
});

test("K06 exactly rows 91 through 124 contain audit data after proof", async function () {
  const runtime = makeRuntime();
  await api.executeRuntime(runtime.env);
  assert.ok(runtime.getState().rawGrid.slice(90, 124).every(function (row) { return !isBlank(row[0]); }));
  assert.ok(runtime.getState().rawGrid.slice(124).every(function (row) { return row.every(isBlank); }));
});

test("K07 controlled summary logging does not include the raw source", async function () {
  const runtime = makeRuntime();
  await api.executeRuntime(runtime.env);
  const serialized = JSON.stringify(runtime.logs);
  assert.ok(serialized.length < 5000);
  assert.ok(!serialized.includes("[Compound Results(Ch1)]"));
});

test("K08 update failure produces no second update and no success", async function () {
  const runtime = makeRuntime({ updateFailure: true });
  const result = await api.executeRuntime(runtime.env);
  assert.strictEqual(result.ok, false);
  assert.strictEqual(runtime.counters.batch_updates, 1);
  assert.strictEqual(runtime.counters.success_calls, 0);
});

test("K09 fixture candidates resolve to and update internal Batch ID 62", async function () {
  const runtime = makeRuntime();
  await api.executeRuntime(runtime.env);
  assert.strictEqual(runtime.getUpdatePayload().data.id, "62");
});

// L. Immutable staged Batch-63 runtime binding.
test("L01 Batch-63 runtime fixture exists with stable protected hashes and byte lengths", function () {
  assert.ok(fs.existsSync(BATCH63_RUNTIME_PATH));
  assert.strictEqual(sha256File(BATCH63_RUNTIME_PATH), EXPECTED_HASHES.batch63_runtime);
  assert.strictEqual(sha256File(ARTIFACT_PATH), EXPECTED_HASHES.artifact);
  assert.strictEqual(sha256File(WORKSHEET_PATH), EXPECTED_HASHES.worksheet);
  assert.strictEqual(sha256File(RUNTIME_PATH), EXPECTED_HASHES.runtime);
  assert.deepStrictEqual(fs.readFileSync(RUNTIME_PATH), fs.readFileSync(V1_RUNTIME_PATH));
  assert.strictEqual(sourceBuffer.length, 286204);
  assert.strictEqual(batch63Buffer.length, 286204);
});

test("L02 immutable transformation changes exactly the two approved bytes", function () {
  assert.deepStrictEqual(byteDifferences(sourceBuffer, batch63Buffer), [
    { offset: 124302, old: 48, new: 50 },
    { offset: 133049, old: 49, new: 51 }
  ]);
  assert.ok(!batch63Buffer.subarray(0, 3).equals(Buffer.from([0xef, 0xbb, 0xbf])));
  for (let index = 0; index < batch63Buffer.length; index += 1) {
    if (batch63Buffer[index] === 0x0a) assert.strictEqual(batch63Buffer[index - 1], 0x0d);
    if (batch63Buffer[index] === 0x0d) assert.strictEqual(batch63Buffer[index + 1], 0x0a);
  }
  assert.deepStrictEqual(Array.from(batch63Buffer.subarray(-2)), [0x0d, 0x0a]);
});

test("L03 only P1 and P2 contracted Sample IDs change semantically", function () {
  assert.deepStrictEqual(analyticallyComparableRecords(batch63Parsed.records), analyticallyComparableRecords(parsed.records));
  const p1 = batch63Parsed.records.find(function (record) { return record.sample_information["Sample Name"] === "P1"; });
  const p2 = batch63Parsed.records.find(function (record) { return record.sample_information["Sample Name"] === "P2"; });
  assert.deepStrictEqual([p1.sample_information["Sample ID"], p2.sample_information["Sample ID"]], ["312", "313"]);
  assert.strictEqual((batch63Text.match(/^Sample ID\t312\r$/gm) || []).length, 1);
  assert.strictEqual((batch63Text.match(/^Sample ID\t313\r$/gm) || []).length, 1);
  assert.strictEqual((batch63Text.match(/^Sample ID\t310\r$/gm) || []).length, 0);
  assert.strictEqual((batch63Text.match(/^Sample ID\t311\r$/gm) || []).length, 0);
});

test("L04 Batch-63 fixture retains 34 valid records categories compounds and candidates", function () {
  assert.strictEqual(batch63Parsed.records.length, 34);
  assert.ok(batch63Parsed.records.every(function (record) {
    return record.compound_results.length === 24 &&
      record.reportable_analytes.length === 23 &&
      Boolean(record.dimethylacetamide_audit);
  }));
  assert.deepStrictEqual(categoryCounts(batch63Parsed.records), {
    Null: 3,
    Blank: 2,
    "System Suitability": 3,
    Standard: 6,
    CCV: 3,
    LOQ: 1,
    "Matrix Blank": 1,
    Sample: 2,
    Validation: 13
  });
  const candidates = api.requireUniqueCandidates(batch63Parsed.records).map(api.candidateTestId);
  assert.deepStrictEqual(candidates, ["312", "313"]);
  assert.ok(candidates.every(function (id) { return typeof id === "string"; }));
});

test("L05 Test 312 and 313 map exactly once to staged dynamic rows 2 and 3", function () {
  const state = makeState({ controlsFixture: true });
  const bundle = api.requireResultsBundle(documentsFromState(state));
  const plans = api.planCandidateRows(bundle, api.requireUniqueCandidates(batch63Parsed.records), batch63Hash);
  assert.deepStrictEqual(plans.map(function (plan) { return [plan.id, plan.row]; }), [["312", 2], ["313", 3]]);
  assert.deepStrictEqual(state.rawGrid[1].slice(0, 3), ["AIT-SAMP-171", "312", "Cannabis Concentrates"]);
  assert.deepStrictEqual(state.rawGrid[2].slice(0, 3), ["AIT-SAMP-171", "313", "Cannabis Concentrates"]);
  assert.ok(state.rawGrid.slice(3, 87).every(function (row) { return row.every(isBlank); }));
});

test("L06 both staged candidates resolve only to internal Batch ID 63", async function () {
  const runtime = makeRuntime({ controlsFixture: true });
  const result = await api.executeRuntime(runtime.env);
  assert.strictEqual(result.ok, true);
  assert.deepStrictEqual(result.summary.matched_test_ids, ["312", "313"]);
  assert.deepStrictEqual(runtime.events.filter(function (event) { return event.startsWith("resolve:"); }), ["resolve:312", "resolve:313"]);
  assert.strictEqual(runtime.getUpdatePayload().data.id, "63");
});

test("L07 partial Batch-63 candidate resolution fails closed", async function () {
  const runtime = makeRuntime({ controlsFixture: true, unknownTestId: "313" });
  await expectRuntimeCode(runtime, "TEST_ID_NOT_FOUND");
  assert.strictEqual(runtime.counters.batch_updates, 0);
  assert.deepStrictEqual(runtime.events.filter(function (event) { return event.startsWith("resolve:"); }), ["resolve:312", "resolve:313"]);
});

test("L08 unknown first Batch-63 candidate resolution fails closed", async function () {
  const runtime = makeRuntime({ controlsFixture: true, unknownTestId: "312" });
  await expectRuntimeCode(runtime, "TEST_ID_NOT_FOUND");
  assert.strictEqual(runtime.counters.batch_updates, 0);
});

test("L09 ambiguous resolution for Test 312 fails closed", async function () {
  const runtime = makeRuntime({ controlsFixture: true, ambiguousTestId: "312" });
  await expectRuntimeCode(runtime, "TEST_ID_BATCH_AMBIGUOUS");
  assert.strictEqual(runtime.counters.batch_updates, 0);
});

test("L10 candidates resolving across Batch 63 and an alternate Batch fail closed", async function () {
  const runtime = makeRuntime({ controlsFixture: true, multipleBatches: true });
  await expectRuntimeCode(runtime, "CANDIDATES_RESOLVE_TO_MULTIPLE_BATCHES");
  assert.strictEqual(runtime.counters.batch_updates, 0);
});

test("L11 duplicate Batch-63 transfer candidates fail closed", function () {
  const duplicate = deepCopy(batch63Parsed.records);
  duplicate[17].sample_information["Sample ID"] = "312";
  expectCode(function () { api.requireUniqueCandidates(duplicate); }, "DUPLICATE_CANDIDATE_TEST_ID");
});

test("L12 Batch-63 runtime stages exactly two dynamic D to AY rows and preserves rows 4 through 87", async function () {
  const runtime = makeRuntime({ controlsFixture: true });
  const beforeUnused = deepCopy(runtime.getState().rawGrid.slice(3, 87));
  const result = await api.executeRuntime(runtime.env);
  assert.strictEqual(result.summary.dynamic_rows_written, 2);
  assert.deepStrictEqual(runtime.getState().rawGrid[1].slice(0, 3), ["AIT-SAMP-171", "312", "Cannabis Concentrates"]);
  assert.deepStrictEqual(runtime.getState().rawGrid[2].slice(0, 3), ["AIT-SAMP-171", "313", "Cannabis Concentrates"]);
  assert.deepStrictEqual(runtime.getState().rawGrid[1].slice(3), api.buildParserOwnedValues(batch63Parsed.records[16], batch63Hash));
  assert.deepStrictEqual(runtime.getState().rawGrid[2].slice(3), api.buildParserOwnedValues(batch63Parsed.records[17], batch63Hash));
  assert.deepStrictEqual(runtime.getState().rawGrid.slice(3, 87), beforeUnused);
});

test("L13 Batch-63 controls and validations never map to dynamic rows", function () {
  assert.ok(batch63Parsed.records.filter(function (record) {
    return record.category !== "Sample";
  }).every(function (record) {
    return api.candidateTestId(record) === "";
  }));
});

test("L14 all 34 Batch-63 records map once to audit rows 91 through 124", function () {
  const bundle = api.requireResultsBundle(documentsFromState(makeState({ controlsFixture: true })));
  const plan = api.planAuditRows(bundle, batch63Parsed.records, batch63Hash);
  assert.strictEqual(plan.rows.length, 34);
  assert.deepStrictEqual(plan.rows.map(function (row) { return row.row; }), Array.from({ length: 34 }, function (_, index) { return index + 91; }));
  assert.strictEqual(plan.rows[0].record_order, 1);
  assert.strictEqual(plan.rows[33].record_order, 34);
});

test("L15 Batch-63 controls and validation records appear only in the audit region", function () {
  const bundle = api.requireResultsBundle(documentsFromState(makeState({ controlsFixture: true })));
  const audit = api.planAuditRows(bundle, batch63Parsed.records, batch63Hash);
  const auditOnly = audit.rows.filter(function (plan) { return plan.record.category !== "Sample"; });
  assert.strictEqual(auditOnly.length, 32);
  assert.ok(auditOnly.every(function (plan) { return api.candidateTestId(plan.record) === ""; }));
});

test("L16 P1 and P2 retain record orders 17 and 18 and audit rows 107 and 108", function () {
  const bundle = api.requireResultsBundle(documentsFromState(makeState({ controlsFixture: true })));
  const audit = api.planAuditRows(bundle, batch63Parsed.records, batch63Hash);
  const p1 = audit.rows.find(function (plan) { return plan.record.sample_information["Sample Name"] === "P1"; });
  const p2 = audit.rows.find(function (plan) { return plan.record.sample_information["Sample Name"] === "P2"; });
  assert.deepStrictEqual([p1.record_order, p1.row, p1.values[2]], [17, 107, "312"]);
  assert.deepStrictEqual([p2.record_order, p2.row, p2.values[2]], [18, 108, "313"]);
});

test("L17 common P1 and P2 dynamic and audit values match under the controlled hash contracts", function () {
  const sourceRowHashColumn = api.RESULTS_HEADERS.indexOf("Source Row Hash");
  [16, 17].forEach(function (recordIndex) {
    const dynamic = api.buildParserOwnedValues(batch63Parsed.records[recordIndex], batch63Hash);
    const audit = api.buildAuditValues(batch63Parsed.records[recordIndex], batch63Hash);
    for (let columnIndex = 3; columnIndex < api.RESULTS_HEADERS.length; columnIndex += 1) {
      if (columnIndex !== sourceRowHashColumn) assert.deepStrictEqual(audit[columnIndex], dynamic[columnIndex - 3]);
    }
    assert.strictEqual(dynamic[sourceRowHashColumn - 3], batch63Parsed.records[recordIndex].source_row_hash);
    assert.strictEqual(audit[sourceRowHashColumn], sha256Text(batch63Hash + ":" + (recordIndex + 1)));
  });
});

test("L18 every Batch-63 audit row has the new file hash deterministic row hash version and Imported status", function () {
  const sourceHashColumn = api.RESULTS_HEADERS.indexOf("Source File Hash");
  const sourceRowHashColumn = api.RESULTS_HEADERS.indexOf("Source Row Hash");
  const versionColumn = api.RESULTS_HEADERS.indexOf("Parser Version");
  const statusColumn = api.RESULTS_HEADERS.indexOf("Import Status");
  batch63Parsed.records.forEach(function (record, index) {
    const values = api.buildAuditValues(record, batch63Hash);
    assert.strictEqual(values[sourceHashColumn], batch63Hash);
    assert.strictEqual(values[sourceRowHashColumn], sha256Text(batch63Hash + ":" + (index + 1)));
    assert.strictEqual(values[versionColumn], "terpenes-simple-results-parser-v2-controls");
    assert.strictEqual(values[statusColumn], "Imported");
  });
});

test("L19 Batch-63 service boundary is one Results-only Batch update to internal ID 63", async function () {
  const runtime = makeRuntime({ controlsFixture: true });
  await api.executeRuntime(runtime.env);
  const payload = runtime.getUpdatePayload();
  assert.strictEqual(runtime.counters.batch_constructs, 1);
  assert.strictEqual(runtime.counters.batch_updates, 1);
  assert.strictEqual(runtime.counters.test_service_constructs, 0);
  assert.strictEqual(payload.data.id, "63");
  assert.deepStrictEqual(Object.keys(payload.data.qb_dynamic_spreadsheet_data), ["Results"]);
  assert.strictEqual(payload.urlParams.run_worksheet_calculations, true);
  const results = payload.data.qb_dynamic_spreadsheet_data.Results;
  assert.strictEqual(results.WORKSHEET_DATA.D2, "P1");
  assert.strictEqual(results.WORKSHEET_DATA.D3, "P2");
  assert.strictEqual(results.WORKSHEET_DATA.A91, 1);
  assert.strictEqual(results.WORKSHEET_DATA.A124, 34);
});

test("L20 Batch-63 readback verifies both dynamic rows all audit rows blanks context and maps before success", async function () {
  const runtime = makeRuntime({ controlsFixture: true });
  const before = deepCopy(runtime.getState());
  const result = await api.executeRuntime(runtime.env);
  assert.strictEqual(result.summary.dynamic_rows_read_back, 2);
  assert.strictEqual(result.summary.audit_rows_read_back, 34);
  assert.ok(runtime.events.indexOf("success") > runtime.events.lastIndexOf("dynamic:2"));
  assert.deepStrictEqual(runtime.getState().rawGrid[1].slice(0, 3), before.rawGrid[1].slice(0, 3));
  assert.deepStrictEqual(runtime.getState().rawGrid[2].slice(0, 3), before.rawGrid[2].slice(0, 3));
  assert.deepStrictEqual(runtime.getState().rawGrid.slice(3, 87), before.rawGrid.slice(3, 87));
  assert.deepStrictEqual(runtime.getState().rawGrid[88], before.rawGrid[88]);
  assert.deepStrictEqual(runtime.getState().rawGrid[89], before.rawGrid[89]);
  assert.ok(runtime.getState().rawGrid.slice(90, 124).every(function (row) { return !isBlank(row[0]); }));
  assert.ok(runtime.getState().rawGrid.slice(124).every(function (row) { return row.every(isBlank); }));
  assert.deepStrictEqual(runtime.getState().formulas, before.formulas);
  assert.deepStrictEqual(runtime.getState().images, before.images);
  assert.deepStrictEqual(runtime.getState().references, before.references);
});

test("L21 missing persisted Test 312 row fails Batch-63 readback", async function () {
  const runtime = makeRuntime({ controlsFixture: true, persistenceMode: "missing-dynamic-source" });
  await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("L22 missing persisted Test 313 row fails Batch-63 readback", async function () {
  const runtime = makeRuntime({ controlsFixture: true, persistenceMode: "missing-dynamic-target" });
  await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("L23 duplicate persisted Test 312 row fails Batch-63 readback", async function () {
  const runtime = makeRuntime({ controlsFixture: true, persistenceMode: "duplicate-dynamic-source" });
  await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("L24 duplicate persisted Test 313 row fails Batch-63 readback", async function () {
  const runtime = makeRuntime({ controlsFixture: true, persistenceMode: "duplicate-dynamic-target" });
  await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
});

test("L25 missing and duplicate Batch-63 audit records fail readback", async function () {
  for (const mode of ["missing-audit-row", "duplicate-audit-order"]) {
    const runtime = makeRuntime({ controlsFixture: true, persistenceMode: mode });
    await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
  }
});

test("L26 changed Batch-63 audit dynamic and context values fail readback", async function () {
  for (const mode of ["changed-audit-value", "changed-dynamic-value", "changed-context"]) {
    const runtime = makeRuntime({ controlsFixture: true, persistenceMode: mode });
    await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
  }
});

test("L27 returned stale audit data and changed protected maps fail Batch-63 readback", async function () {
  for (const mode of ["stale-unused-after-readback", "changed-maps", "changed-audit-header"]) {
    const runtime = makeRuntime({ controlsFixture: true, persistenceMode: mode });
    await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
  }
});

test("L28 Batch-63 no-op update fails once without retry or premature success", async function () {
  const runtime = makeRuntime({ controlsFixture: true, persistenceMode: "no-op" });
  await expectRuntimeCode(runtime, "RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED");
  assert.strictEqual(runtime.counters.batch_updates, 1);
  assert.strictEqual(runtime.counters.success_calls, 0);
});

test("L29 Batch-63 stale clearing is targeted only to nonblank unused audit cells", async function () {
  const state = makeState({ controlsFixture: true, unusedAuditStale: true });
  const bundle = api.requireResultsBundle(documentsFromState(state));
  const plan = api.planAuditRows(bundle, batch63Parsed.records, batch63Hash);
  assert.deepStrictEqual(plan.stale_cells.map(function (cell) { return toAddress(cell.row, cell.column + 1); }), ["A125", "K125", "AY130"]);
  assert.ok(plan.stale_cells.every(function (cell) { return cell.row >= 125 && cell.row <= 190; }));
  assert.ok(!plan.stale_cells.some(function (cell) { return cell.row === 125 && cell.column === 1; }));
  const runtime = makeRuntime({ controlsFixture: true, unusedAuditStale: true });
  const beforeRows2Through90 = deepCopy(runtime.getState().rawGrid.slice(1, 90));
  await api.executeRuntime(runtime.env);
  assert.deepStrictEqual(runtime.getState().rawGrid.slice(1, 3).map(function (row) { return row.slice(0, 3); }), beforeRows2Through90.slice(0, 2).map(function (row) { return row.slice(0, 3); }));
  assert.deepStrictEqual(runtime.getState().rawGrid.slice(3, 87), beforeRows2Through90.slice(2, 86));
  assert.deepStrictEqual(runtime.getState().rawGrid[88], beforeRows2Through90[87]);
  assert.deepStrictEqual(runtime.getState().rawGrid[89], beforeRows2Through90[88]);
  assert.strictEqual(runtime.getState().rawGrid[124][0], "");
  assert.strictEqual(runtime.getState().rawGrid[124][10], "");
  assert.strictEqual(runtime.getState().rawGrid[129][50], "");
});

test("L30 Batch-63 runtime filename and human-reviewed roles remain fixture data", function () {
  const runtime = makeRuntime({ controlsFixture: true });
  assert.strictEqual(runtime.env.QB.files.length, 1);
  assert.strictEqual(runtime.env.QB.files[0].name, "terpenes_simple_results_v2_controls_312_313_runtime_source.txt");
  const p1 = batch63Parsed.records.find(function (record) { return record.sample_information["Sample Name"] === "P1"; });
  const p2 = batch63Parsed.records.find(function (record) { return record.sample_information["Sample Name"] === "P2"; });
  assert.deepStrictEqual(
    [[p1.sample_information["Sample Name"], p1.sample_information["Sample ID"], "Source"], [p2.sample_information["Sample Name"], p2.sample_information["Sample ID"], "Target"]],
    [["P1", "312", "Source"], ["P2", "313", "Target"]]
  );
  assert.ok(!artifactText.includes("\"312\""));
  assert.ok(!artifactText.includes("\"313\""));
});

(async function run() {
  let passed = 0;
  let failed = 0;
  for (const item of tests) {
    try {
      await item.fn();
      passed += 1;
      process.stdout.write("PASS " + item.name + "\n");
    } catch (error) {
      failed += 1;
      process.stdout.write("FAIL " + item.name + "\n");
      process.stdout.write(String(error && error.stack ? error.stack : error) + "\n");
    }
  }
  process.stdout.write("TOTAL=" + tests.length + " PASSED=" + passed + " FAILED=" + failed + " SKIPPED=0\n");
  if (failed) process.exitCode = 1;
}());
