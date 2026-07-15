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

function mockQB(files) {
  const state = { logs: [], progress: [], success: 0, errors: [] };
  return {
    state,
    QB: {
      files,
      console: (message) => state.logs.push(message),
      progressBar: (value) => state.progress.push(value),
      success: () => { state.success += 1; },
      error: (value) => state.errors.push(value),
    },
  };
}

test("no-write runtime mock returns only the controlled sanitized summary", async () => {
  const context = loadProbe();
  const mock = mockQB([{ name: "Output_redacted_fixture.txt", type: "text/plain", size: fixture.length, text: fixture }]);
  const summary = await context.QBenchRuntimeNoWriteProbe.execute(mock.QB, MockFileReader, config, context.QBenchTerpenesParserCore);
  assert.deepEqual(JSON.parse(JSON.stringify(summary)), expected);
  assert.equal(mock.state.success, 1);
  assert.deepEqual(mock.state.errors, []);
  assert.equal(mock.state.logs.length, 7);
  assert.equal(summary.web_crypto_available, false);
});

test("sanitized logs contain counts but no raw text or analyte values", async () => {
  const context = loadProbe();
  const mock = mockQB([{ name: "Output_redacted_fixture.txt", type: "text/plain", size: fixture.length, text: fixture }]);
  await context.QBenchRuntimeNoWriteProbe.execute(mock.QB, MockFileReader, config, context.QBenchTerpenesParserCore);
  const logs = mock.state.logs.join("\n");
  assert.match(logs, /Compound Results rows = 24/);
  assert.equal(logs.includes("24.608"), false);
  assert.equal(logs.includes("alpha-Pinene"), false);
  assert.equal(logs.includes("[Header]"), false);
});

test("exactly one controlled txt file is required", async () => {
  const context = loadProbe();
  for (const files of [[], [{ name: "wrong.txt", text: fixture }], [{ name: "Output_redacted_fixture.csv", text: fixture }], [{ name: "Output_redacted_fixture.txt", text: fixture }, { name: "second.txt", text: fixture }]]) {
    const mock = mockQB(files);
    await assert.rejects(() => context.QBenchRuntimeNoWriteProbe.execute(mock.QB, MockFileReader, config, context.QBenchTerpenesParserCore));
    assert.equal(mock.state.success, 0);
    assert.equal(mock.state.errors.length, 1);
  }
});

test("Stage 1 source and distribution contain no worksheet service", () => {
  for (const file of [path.join(PACKAGE, "src/qbench_runtime_no_write_probe.js"), path.join(PACKAGE, "dist/qbench_runtime_no_write_probe_v1.js")]) {
    const text = fs.readFileSync(file, "utf8");
    assert.equal(text.includes("QBBatchService"), false);
    assert.equal(text.includes("patchWorksheet"), false);
  }
});

test("Stage 1 distribution uses the exact proven import and run wrapper", () => {
  const text = fs.readFileSync(path.join(PACKAGE, "dist/qbench_runtime_no_write_probe_v1.js"), "utf8");
  assert.match(text, /https:\/\/d30nr38ylt5b32\.cloudfront\.net\/v1\.1\.0\/file_parser\.js/);
  assert.match(text, /run\(async \(\) =>/);
  assert.match(text, /FileReader/);
});
