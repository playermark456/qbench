"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const sourcePath = path.resolve(__dirname, "../../src/qbench_scalar_patch_probe.js");
const source = fs.readFileSync(sourcePath, "utf8");

function loadProbe() {
  const sandbox = {
    importScripts() {},
    run() {},
  };
  sandbox.globalThis = sandbox;
  sandbox.self = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(source, sandbox, { filename: sourcePath });
  return sandbox.QBenchScalarPatchProbe;
}

test("scalar builder emits exactly two direct scalar values", () => {
  const probe = loadProbe();
  const request = probe.buildRequest(
    "SANITIZED_BATCH_CONTEXT",
    () => {},
    () => {},
  );

  assert.deepEqual(Object.keys(request).sort(), ["batchId", "data", "error", "success"]);
  assert.deepEqual(Object.keys(request.data).sort(), ["probe_number", "probe_text"]);
  assert.equal(request.data.probe_text, "sandbox_probe");
  assert.equal(typeof request.data.probe_text, "string");
  assert.equal(request.data.probe_number, 1.25);
  assert.equal(typeof request.data.probe_number, "number");
  assert.equal(Number.isFinite(request.data.probe_number), true);
});

test("scalar builder does not emit nested value wrappers", () => {
  const probe = loadProbe();
  const request = probe.buildRequest(
    "SANITIZED_BATCH_CONTEXT",
    () => {},
    () => {},
  );

  assert.equal(request.data.probe_text && request.data.probe_text.value, undefined);
  assert.equal(request.data.probe_number && request.data.probe_number.value, undefined);
  assert.equal(Object.values(request.data).some((value) => value && typeof value === "object"), false);
});
