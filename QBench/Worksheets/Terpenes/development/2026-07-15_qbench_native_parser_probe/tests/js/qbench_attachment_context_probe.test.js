"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const PACKAGE = path.resolve(__dirname, "../..");
const SOURCE = path.join(PACKAGE, "src/qbench_attachment_context_probe.js");

function loadProbe() {
  const context = vm.createContext({});
  vm.runInContext(fs.readFileSync(SOURCE, "utf8"), context, { filename: SOURCE });
  return context.QBenchAttachmentContextProbe;
}

function mockQB(values = {}) {
  const state = { logs: [], success: 0, errors: [], serviceCalls: [] };
  return {
    state,
    QB: {
      console: (message) => state.logs.push(message),
      success: () => { state.success += 1; },
      error: (code) => state.errors.push(code),
      patchWorksheet: () => state.serviceCalls.push("patchWorksheet"),
      ...values,
    },
  };
}

test("fixed allowlist observes nested Batch-context types without values", () => {
  const probe = loadProbe();
  const summary = probe.safeSummary({ location: { batch: { id: 123 } } });
  const results = Object.fromEntries(summary.candidate_paths.map((item) => [item.path, item]));
  assert.deepEqual(JSON.parse(JSON.stringify(results["QB.location"])), {
    path: "QB.location", present: true, value_type: "object",
  });
  assert.deepEqual(JSON.parse(JSON.stringify(results["QB.location.batch"])), {
    path: "QB.location.batch", present: true, value_type: "object",
  });
  assert.deepEqual(JSON.parse(JSON.stringify(results["QB.location.batch.id"])), {
    path: "QB.location.batch.id", present: true, value_type: "number",
  });
});

test("missing candidate paths are absent and undefined", () => {
  const probe = loadProbe();
  const summary = probe.safeSummary({});
  assert.equal(summary.candidate_paths.every((item) => !item.present && item.value_type === "undefined"), true);
});

test("execution logs only fixed paths and types, then succeeds without a service call", async () => {
  const probe = loadProbe();
  const mock = mockQB({
    location: { batch: { id: 123 } },
    csrfToken: "controlled-secret-not-for-output",
    file: { content: "controlled-file-content-not-for-output" },
  });
  await probe.execute(mock.QB);
  const logs = mock.state.logs.join("\n");
  assert.equal(mock.state.success, 1);
  assert.deepEqual(mock.state.errors, []);
  assert.deepEqual(mock.state.serviceCalls, []);
  assert.equal(logs.includes("QB.location.batch.id present=true type=number"), true);
  assert.equal(logs.includes("123"), false);
  assert.equal(logs.includes("controlled-secret-not-for-output"), false);
  assert.equal(logs.includes("controlled-file-content-not-for-output"), false);
  assert.equal(logs.includes("csrfToken"), false);
});

test("Stage 2B source has no service, network, dynamic-code, or browser-storage capability", () => {
  const source = fs.readFileSync(SOURCE, "utf8");
  const prohibited = [
    "patchWorksheet", "updateWorksheet", "QBBatchService", "fetch(", "XMLHttpRequest",
    "eval(", "Function(", "localStorage", ".cookie", "csrfToken", "Object.keys(QB)",
  ];
  for (const token of prohibited) assert.equal(source.includes(token), false, token);
});
