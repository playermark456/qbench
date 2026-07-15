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

function load(names) {
  const context = vm.createContext({});
  for (const name of names) {
    const file = path.join(PACKAGE, "src", name);
    vm.runInContext(fs.readFileSync(file, "utf8"), context, { filename: file });
  }
  return context;
}

class MockQBBatchService {
  constructor() { this.calls = []; }
  patchWorksheet(request) { this.calls.push(request); request.success({ status: "ok" }); }
}

function compoundMutation(pattern, replacement) {
  const marker = "[Compound Results(Ch1)]";
  const index = fixture.indexOf(marker);
  return fixture.slice(0, index) + fixture.slice(index).replace(pattern, replacement);
}

test("malformed parser variants fail before any patch call", () => {
  const context = load(["qbench_browser_parser_core.js", "terpenes_qbench_sandbox_probe.template.js"]);
  const service = new MockQBBatchService();
  const variants = [
    compoundMutation("24\t(-)-alpha-Bisabolol", ""),
    compoundMutation("2\talpha-Pinene", "2\tUnknown Controlled Result"),
    compoundMutation("2\talpha-Pinene", "24\talpha-Pinene"),
    compoundMutation("2\talpha-Pinene\t5.809\t134208\t52649\t24.608\t", "2\talpha-Pinene\t5.809\t134208\t52649\tbad-number\t"),
  ];
  for (const text of variants) {
    assert.throws(() => context.QBenchTerpenesParserCore.parseLabSolutionsAscii(text, config));
  }
  assert.equal(service.calls.length, 0);
});

test("fixture write plan is complete before the patch service is invoked", async () => {
  const context = load(["qbench_browser_parser_core.js", "terpenes_qbench_sandbox_probe.template.js"]);
  const parsed = context.QBenchTerpenesParserCore.parseLabSolutionsAscii(fixture, config);
  const service = new MockQBBatchService();
  await context.QBenchTerpenesFixturePatchTemplate.execute(service, 123, parsed, context.QBenchTerpenesFixturePatchTemplate.FIXTURE_SHA256);
  assert.equal(service.calls.length, 1);
  assert.deepEqual(Object.keys(service.calls[0].data).sort(), ["terpenes_probe_import_row_2_analytes", "terpenes_probe_import_row_2_leading"]);
  assert.equal(service.calls[0].data.terpenes_probe_import_row_2_leading.value.length, 31);
  assert.equal(service.calls[0].data.terpenes_probe_import_row_2_analytes.value.length, 24);
});

test("fixture hash mismatch prevents the patch call", async () => {
  const context = load(["qbench_browser_parser_core.js", "terpenes_qbench_sandbox_probe.template.js"]);
  const parsed = context.QBenchTerpenesParserCore.parseLabSolutionsAscii(fixture, config);
  const service = new MockQBBatchService();
  await assert.rejects(() => context.QBenchTerpenesFixturePatchTemplate.execute(service, 123, parsed, "wrong-hash"), /CONTROLLED_FIXTURE_HASH_MISMATCH/);
  assert.equal(service.calls.length, 0);
});

test("failure probe creates one mixed-validity request and no retry", async () => {
  const context = load(["qbench_failure_patch_probe.js"]);
  const service = new MockQBBatchService();
  const request = context.QBenchFailurePatchProbe.buildMixedValidityRequest(123);
  await context.QBenchFailurePatchProbe.execute(service, request);
  assert.equal(service.calls.length, 1);
  assert.deepEqual(Object.keys(service.calls[0].data).sort(), ["probe_intentionally_invalid_field", "probe_text"]);
});

test("sequential failure probe prepares exactly two narrow requests", () => {
  const context = load(["qbench_failure_patch_probe.js"]);
  const requests = context.QBenchFailurePatchProbe.buildSequentialRequests(123);
  assert.equal(requests.length, 2);
  assert.deepEqual(Object.keys(requests[0].data), ["probe_text"]);
  assert.deepEqual(Object.keys(requests[1].data), ["probe_intentionally_invalid_field"]);
});

test("all source and generated scripts exclude prohibited capabilities", () => {
  const files = [
    ...fs.readdirSync(path.join(PACKAGE, "src")).filter((name) => name.endsWith(".js")).map((name) => path.join(PACKAGE, "src", name)),
    ...fs.readdirSync(path.join(PACKAGE, "dist")).filter((name) => name.endsWith(".js")).map((name) => path.join(PACKAGE, "dist", name)),
  ];
  const forbidden = ["updateWorksheet", "QBBatchService.update(", "fetch(", "XMLHttpRequest", "eval(", "Function(", "localStorage", "cookie", "credentials", "pass_fail", "Pass/Fail"];
  for (const file of files) {
    const text = fs.readFileSync(file, "utf8");
    for (const token of forbidden) assert.equal(text.includes(token), false, `${token} found in ${file}`);
  }
});

test("Stage 7 distribution is absent during Stage 0", () => {
  assert.equal(fs.existsSync(path.join(PACKAGE, "dist/terpenes_qbench_file_parser_sandbox_probe_v1.js")), false);
});
