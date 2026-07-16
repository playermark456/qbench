"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const PACKAGE = path.resolve(__dirname, "../..");
const REPO = path.resolve(PACKAGE, "../../../../..");
const config = JSON.parse(fs.readFileSync(path.join(REPO, "QBench/Worksheets/Terpenes/development/2026-07-14_config_parser_foundation/config/terpenes_analytes.json"), "utf8"));
const fixture = fs.readFileSync(path.join(PACKAGE, "tests/fixtures/Output_redacted_fixture.txt"), "utf8");
const expected = JSON.parse(fs.readFileSync(path.join(PACKAGE, "tests/fixtures/expected_no_write_summary.json"), "utf8"));

function loadProbe() {
  const context = vm.createContext({});
  for (const name of ["qbench_browser_parser_core.js", "qbench_runtime_no_write_probe.js"]) {
    const file = path.join(PACKAGE, "src", name);
    vm.runInContext(fs.readFileSync(file, "utf8"), context, { filename: file });
  }
  return context;
}

class MockFileReader {
  readAsText(file) {
    this.result = file.text;
    Promise.resolve().then(() => this.onload());
  }
}

class FailedFileReader {
  readAsText() {
    Promise.resolve().then(() => this.onerror(new Error("sanitized mock read failure")));
  }
}

function controlledFile(name = "Output_redacted_fixture.txt") {
  return { name, type: "text/plain", size: fixture.length, text: fixture };
}

function mockQB(files) {
  const state = { logs: [], progress: [], success: 0, errors: [], serviceCalls: [] };
  return {
    state,
    QB: {
      files,
      console: (message) => state.logs.push(message),
      progressBar: (value) => state.progress.push(value),
      success: () => { state.success += 1; },
      error: (value) => state.errors.push(value),
      patchWorksheet: () => state.serviceCalls.push("patchWorksheet"),
      updateWorksheet: () => state.serviceCalls.push("updateWorksheet"),
    },
  };
}

async function executeWith(files, Reader = MockFileReader) {
  const context = loadProbe();
  const mock = mockQB(files);
  const summary = await context.QBenchRuntimeNoWriteProbe.execute(mock.QB, Reader, config, context.QBenchTerpenesParserCore);
  return { context, mock, summary };
}

async function expectControlledFailure(files, expectedCode, expectedStep, Reader = MockFileReader) {
  const context = loadProbe();
  const mock = mockQB(files);
  await assert.rejects(
    () => context.QBenchRuntimeNoWriteProbe.execute(mock.QB, Reader, config, context.QBenchTerpenesParserCore),
    (error) => {
      assert.equal(error.code, expectedCode);
      return true;
    },
  );
  assert.equal(mock.state.success, 0);
  assert.deepEqual(mock.state.errors, [expectedCode]);
  assert.equal(mock.state.logs.includes(`controlled error = ${expectedCode}`), true);
  assert.equal(mock.state.logs.includes(`failed step = ${expectedStep}`), true);
  assert.deepEqual(mock.state.serviceCalls, []);
  const logs = mock.state.logs.join("\n");
  assert.equal(logs.includes(fixture), false);
  assert.equal(logs.includes("[Header]"), false);
  return { context, mock };
}

test("QB.files as a normal Array succeeds with the controlled sanitized summary", async () => {
  const { mock, summary } = await executeWith([controlledFile()]);
  assert.deepEqual(JSON.parse(JSON.stringify(summary)), expected);
  assert.equal(mock.state.success, 1);
  assert.deepEqual(mock.state.errors, []);
  assert.deepEqual(mock.state.serviceCalls, []);
  assert.equal(mock.state.logs.length, 13);
  assert.equal(mock.state.logs.includes("file collection kind = Array"), true);
  assert.equal(summary.web_crypto_available, false);
});

test("QB.files as a FileList-like object with item(index) succeeds", async () => {
  const file = controlledFile();
  const files = { 0: file, length: 1, item(index) { return index === 0 ? file : null; } };
  const { mock, summary } = await executeWith(files);
  assert.deepEqual(JSON.parse(JSON.stringify(summary)), expected);
  assert.equal(mock.state.logs.includes("file collection kind = array_like"), true);
  assert.equal(mock.state.success, 1);
  assert.deepEqual(mock.state.serviceCalls, []);
});

test("array-like QB.files with an indexed entry and no item method succeeds", async () => {
  const { mock, summary } = await executeWith({ 0: controlledFile(), length: 1 });
  assert.deepEqual(JSON.parse(JSON.stringify(summary)), expected);
  assert.equal(mock.state.logs.includes("probe step = file collection accepted"), true);
  assert.equal(mock.state.success, 1);
  assert.deepEqual(mock.state.serviceCalls, []);
});

test("item(index) is used when an array-like collection has no indexed entry", async () => {
  const file = controlledFile();
  const { mock } = await executeWith({ length: 1, item(index) { return index === 0 ? file : null; } });
  assert.equal(mock.state.success, 1);
  assert.deepEqual(mock.state.serviceCalls, []);
});

test("sanitized success logs contain only steps, collection kind, counts, extension, and Web Crypto availability", async () => {
  const { mock } = await executeWith([controlledFile()]);
  const logs = mock.state.logs.join("\n");
  for (const expectedLog of [
    "probe step = runtime entered",
    "probe step = file collection accepted",
    "probe step = file metadata accepted",
    "probe step = file read complete",
    "probe step = controlled parse complete",
    "file count = 1",
    "extension accepted = .txt",
    "Compound Results rows = 24",
    "Peak Table rows = 34",
    "reportable channels = 23",
    "Dimethylacetamide audit rows = 1",
    "Web Crypto available = false",
  ]) assert.equal(logs.includes(expectedLog), true, expectedLog);
  for (const prohibited of ["24.608", "alpha-Pinene", "[Header]", "Output_redacted_fixture.txt"]) {
    assert.equal(logs.includes(prohibited), false, prohibited);
  }
});

test("missing collection uses CONTROLLED_FILE_COLLECTION_ERROR", async () => {
  await expectControlledFailure(undefined, "CONTROLLED_FILE_COLLECTION_ERROR", "file collection validation");
});

test("invalid collection lengths use CONTROLLED_FILE_COLLECTION_ERROR", async () => {
  for (const length of [-1, 1.5, Number.POSITIVE_INFINITY, "1", Number.NaN]) {
    await expectControlledFailure({ 0: controlledFile(), length }, "CONTROLLED_FILE_COLLECTION_ERROR", "file collection validation");
  }
});

test("empty collection uses CONTROLLED_FILE_COUNT_ERROR", async () => {
  await expectControlledFailure([], "CONTROLLED_FILE_COUNT_ERROR", "file collection validation");
});

test("two-file collection uses CONTROLLED_FILE_COUNT_ERROR", async () => {
  await expectControlledFailure([controlledFile(), controlledFile()], "CONTROLLED_FILE_COUNT_ERROR", "file collection validation");
});

test("missing file object uses CONTROLLED_FILE_OBJECT_ERROR", async () => {
  await expectControlledFailure({ length: 1, item() { return null; } }, "CONTROLLED_FILE_OBJECT_ERROR", "file collection validation");
  await expectControlledFailure({ 0: "not a file object", length: 1 }, "CONTROLLED_FILE_OBJECT_ERROR", "file collection validation");
});

test("incorrect exact filename uses CONTROLLED_FILE_NAME_ERROR", async () => {
  await expectControlledFailure([controlledFile("wrong.txt")], "CONTROLLED_FILE_NAME_ERROR", "file metadata validation");
});

test("uppercase TXT extension is recognized but does not weaken the exact controlled filename gate", async () => {
  const context = loadProbe();
  assert.equal(context.QBenchRuntimeNoWriteProbe.hasTxtExtension("fixture.TXT"), true);
  await expectControlledFailure([controlledFile("Output_redacted_fixture.TXT")], "CONTROLLED_FILE_NAME_ERROR", "file metadata validation");
});

test("file-reader failure uses CONTROLLED_FILE_READ_ERROR", async () => {
  await expectControlledFailure([controlledFile()], "CONTROLLED_FILE_READ_ERROR", "file read", FailedFileReader);
});

test("controlled runtime error codes survive toControlledError", () => {
  const context = loadProbe();
  for (const code of Object.values(JSON.parse(JSON.stringify(context.QBenchRuntimeNoWriteProbe.CONTROLLED_ERROR_CODES)))) {
    const error = context.QBenchRuntimeNoWriteProbe.controlledError(code);
    assert.equal(context.QBenchTerpenesParserCore.toControlledError(error).code, code);
  }
  assert.equal(context.QBenchTerpenesParserCore.toControlledError(new Error("unexpected")).code, "UNEXPECTED_PARSE_ERROR");
});

test("Stage 1 source and distribution contain no write, network, dynamic-code, or browser-storage capability", () => {
  const prohibited = [
    "patchWorksheet", "updateWorksheet", "QBBatchService", "fetch(", "XMLHttpRequest",
    "eval(", "Function(", "localStorage", ".cookie",
  ];
  for (const file of [path.join(PACKAGE, "src/qbench_runtime_no_write_probe.js"), path.join(PACKAGE, "dist/qbench_runtime_no_write_probe_v1.js")]) {
    const text = fs.readFileSync(file, "utf8");
    for (const token of prohibited) assert.equal(text.includes(token), false, `${token} in ${file}`);
  }
  const source = fs.readFileSync(path.join(PACKAGE, "src/qbench_runtime_no_write_probe.js"), "utf8");
  assert.equal(source.includes("Array.from"), false, "file collection normalization must not use Array.from");
});

test("Stage 1 distribution uses the exact proven import and run wrapper", () => {
  const text = fs.readFileSync(path.join(PACKAGE, "dist/qbench_runtime_no_write_probe_v1.js"), "utf8");
  assert.match(text, /https:\/\/d30nr38ylt5b32\.cloudfront\.net\/v1\.1\.0\/file_parser\.js/);
  assert.match(text, /run\(async \(\) =>/);
  assert.match(text, /FileReader/);
});
