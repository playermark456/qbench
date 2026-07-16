"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const PACKAGE = path.resolve(__dirname, "../..");

function load(names) {
  const context = vm.createContext({});
  for (const name of names) {
    const file = path.join(PACKAGE, "src", name);
    vm.runInContext(fs.readFileSync(file, "utf8"), context, { filename: file });
  }
  return context;
}

function expected(name) {
  return JSON.parse(fs.readFileSync(path.join(PACKAGE, "tests/fixtures", name), "utf8"));
}

class MockQBBatchService {
  constructor(mode = "success") {
    this.calls = [];
    this.mode = mode;
  }

  patchWorksheet(request) {
    this.calls.push(request);
    if (this.mode === "success") request.success({ status: "ok" });
    else request.error(new Error("controlled mock failure"));
  }
}

test("scalar payload matches the controlled fixture and omits unrelated fields", () => {
  const context = load(["qbench_scalar_patch_probe.js"]);
  const request = context.QBenchScalarPatchProbe.buildRequest("SANITIZED_BATCH_CONTEXT");
  assert.deepEqual(JSON.parse(JSON.stringify(request)), expected("expected_scalar_patch.json"));
  assert.equal(typeof request.data.probe_number.value, "number");
  assert.deepEqual(Object.keys(request.data).sort(), ["probe_number", "probe_text"]);
});

test("scalar runtime mock calls the patch service exactly once", async () => {
  const context = load(["qbench_scalar_patch_probe.js"]);
  const service = new MockQBBatchService();
  await context.QBenchScalarPatchProbe.execute(service, 123);
  assert.equal(service.calls.length, 1);
  assert.equal(service.calls[0].data.probe_number.value, 1.25);
});

test("range payload starts with one-dimensional JavaScript Number values", () => {
  const context = load(["qbench_range_patch_probe.js"]);
  const request = context.QBenchRangePatchProbe.buildRequest("SANITIZED_BATCH_CONTEXT", "one_dimensional");
  assert.deepEqual(JSON.parse(JSON.stringify(request)), expected("expected_range_patch.json"));
  assert.equal(request.data.probe_small_range.value.every((value) => typeof value === "number"), true);
});

test("one-row two-dimensional range shape is prepared only when selected", () => {
  const context = load(["qbench_range_patch_probe.js"]);
  const value = context.QBenchRangePatchProbe.buildRequest(123, "one_row_two_dimensional").data.probe_small_range.value;
  assert.deepEqual(JSON.parse(JSON.stringify(value)), [[1.25, 2.5, 3.75]]);
});

test("small matrix payload contains four JavaScript Number values", () => {
  const context = load(["qbench_range_patch_probe.js"]);
  const value = context.QBenchRangePatchProbe.buildMatrixRequest(123).data.probe_small_matrix.value;
  assert.deepEqual(JSON.parse(JSON.stringify(value)), [[1, 2], [3, 4]]);
  assert.equal(value.flat().every((item) => typeof item === "number"), true);
});

test("unknown range shapes are rejected before a service call", () => {
  const context = load(["qbench_range_patch_probe.js"]);
  assert.throws(() => context.QBenchRangePatchProbe.buildRequest(123, "guessed_shape"), /CONTROLLED_RANGE_SHAPE_REQUIRED/);
});

test("two-block payload contains exactly 31 and 24 Number values", () => {
  const context = load(["qbench_two_block_patch_probe.js"]);
  const request = context.QBenchTwoBlockPatchProbe.buildRequest("SANITIZED_BATCH_CONTEXT");
  assert.deepEqual(JSON.parse(JSON.stringify(request)), expected("expected_two_block_patch.json"));
  assert.equal(request.data.probe_block_a_ae.value.length, 31);
  assert.equal(request.data.probe_block_ah_be.value.length, 24);
  assert.equal(Object.keys(request.data).some((name) => name.includes("gap")), false);
});

test("sequential fallback keeps the two controlled blocks separate", () => {
  const context = load(["qbench_two_block_patch_probe.js"]);
  const requests = context.QBenchTwoBlockPatchProbe.buildSequentialRequests(123);
  assert.deepEqual(JSON.parse(JSON.stringify(requests.map((request) => Object.keys(request.data)))), [["probe_block_a_ae"], ["probe_block_ah_be"]]);
});

test("Batch context is required before any payload can be built", () => {
  const context = load(["qbench_scalar_patch_probe.js", "qbench_range_patch_probe.js", "qbench_two_block_patch_probe.js"]);
  assert.throws(() => context.QBenchScalarPatchProbe.buildRequest(""), /CONTROLLED_BATCH_CONTEXT_REQUIRED/);
  assert.throws(() => context.QBenchRangePatchProbe.buildRequest(null, "one_dimensional"), /CONTROLLED_BATCH_CONTEXT_REQUIRED/);
  assert.throws(() => context.QBenchTwoBlockPatchProbe.buildRequest(undefined), /CONTROLLED_BATCH_CONTEXT_REQUIRED/);
});

test("controlled service errors are returned without automatic retry", async () => {
  const context = load(["qbench_scalar_patch_probe.js"]);
  const service = new MockQBBatchService("error");
  await assert.rejects(() => context.QBenchScalarPatchProbe.execute(service, 123), /controlled mock failure/);
  assert.equal(service.calls.length, 1);
});
