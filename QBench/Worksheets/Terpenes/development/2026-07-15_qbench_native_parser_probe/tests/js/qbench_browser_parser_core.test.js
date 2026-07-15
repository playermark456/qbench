"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const PACKAGE = path.resolve(__dirname, "../..");
const REPO = path.resolve(PACKAGE, "../../../../..");
const CORE_PATH = path.join(PACKAGE, "src/qbench_browser_parser_core.js");
const CONFIG_PATH = path.join(REPO, "QBench/Worksheets/Terpenes/development/2026-07-14_config_parser_foundation/config/terpenes_analytes.json");
const FIXTURE_PATH = path.join(PACKAGE, "tests/fixtures/Output_redacted_fixture.txt");

function loadCore() {
  const context = vm.createContext({});
  vm.runInContext(fs.readFileSync(CORE_PATH, "utf8"), context, { filename: CORE_PATH });
  return context.QBenchTerpenesParserCore;
}

const core = loadCore();
const config = JSON.parse(fs.readFileSync(CONFIG_PATH, "utf8"));
const fixture = fs.readFileSync(FIXTURE_PATH, "utf8");

function compoundMutation(pattern, replacement) {
  const marker = "[Compound Results(Ch1)]";
  const index = fixture.indexOf(marker);
  return fixture.slice(0, index) + fixture.slice(index).replace(pattern, replacement);
}

test("controlled fixture parses with exact 24/34/23/1 counts", () => {
  const parsed = core.parseLabSolutionsAscii(fixture, config);
  assert.deepEqual(JSON.parse(JSON.stringify(parsed.counts)), {
    compound_result_row_count: 24,
    peak_table_row_count: 34,
    reportable_compound_row_count: 23,
    dimethylacetamide_row_count: 1,
  });
});

test("UTF-8 BOM, LF, and CRLF are accepted", () => {
  for (const text of [`\ufeff${fixture}`, fixture.replace(/\r\n/g, "\n"), fixture.replace(/\r?\n/g, "\r\n")]) {
    assert.equal(core.parseLabSolutionsAscii(text, config).counts.peak_table_row_count, 34);
  }
});

test("numerical zero is preserved as a Number", () => {
  const text = compoundMutation("2\talpha-Pinene\t5.809\t134208\t52649\t24.608\t", "2\talpha-Pinene\t5.809\t134208\t52649\t0\t");
  const parsed = core.parseLabSolutionsAscii(text, config);
  assert.equal(parsed.reportable_analytes[0].conc, 0);
  assert.equal(typeof parsed.reportable_analytes[0].conc, "number");
});

test("negative instrument concentration is preserved as a Number", () => {
  const text = compoundMutation("2\talpha-Pinene\t5.809\t134208\t52649\t24.608\t", "2\talpha-Pinene\t5.809\t134208\t52649\t-1.25\t");
  const parsed = core.parseLabSolutionsAscii(text, config);
  assert.equal(parsed.reportable_analytes[0].conc, -1.25);
});

test("malformed numeric concentration is rejected", () => {
  const text = compoundMutation("2\talpha-Pinene\t5.809\t134208\t52649\t24.608\t", "2\talpha-Pinene\t5.809\t134208\t52649\t1.2.3\t");
  assert.throws(() => core.parseLabSolutionsAscii(text, config), /concentration must be numeric/);
});

test("unknown Compound Results name is rejected", () => {
  const text = compoundMutation("2\talpha-Pinene\t", "2\tUnknown Controlled Result\t");
  assert.throws(() => core.parseLabSolutionsAscii(text, config), /unknown Compound Results name/);
});

test("ID/name mismatch is rejected", () => {
  const text = compoundMutation("2\talpha-Pinene\t", "24\talpha-Pinene\t");
  assert.throws(() => core.parseLabSolutionsAscii(text, config), /ID\/name mismatch/);
});

test("controlled Greek alias maps identically", () => {
  const text = compoundMutation("2\talpha-Pinene\t", "2\tα-Pinene\t");
  assert.equal(core.parseLabSolutionsAscii(text, config).reportable_analytes[0].internal_key, "apinene");
});

test("unknown Peak Table name is retained for audit", () => {
  const peakMarker = "[Peak Table(Ch1)]";
  const compoundMarker = "[Compound Results(Ch1)]";
  const start = fixture.indexOf(peakMarker);
  const end = fixture.indexOf(compoundMarker);
  const peak = fixture.slice(start, end).replace("2\t5.809\t5.742\t5.929\t134208\t52649\t2.549\t24.608\tV\t2\talpha-Pinene\t", "2\t5.809\t5.742\t5.929\t134208\t52649\t2.549\t24.608\tV\t2\tUnknown Audit Peak\t");
  const parsed = core.parseLabSolutionsAscii(fixture.slice(0, start) + peak + fixture.slice(end), config);
  assert.equal(parsed.peak_table[1].unconfigured_analyte, true);
  assert.equal(parsed.peak_table[1].retain_for_audit, true);
});

test("Peak Table values never replace Compound Results quantitation", () => {
  const parsed = core.parseLabSolutionsAscii(fixture.replace("2\t5.809\t5.742\t5.929\t134208\t52649\t2.549\t24.608\t", "2\t5.809\t5.742\t5.929\t134208\t52649\t2.549\t999999\t"), config);
  assert.equal(parsed.reportable_analytes[0].conc, 24.608);
});

test("raw text is not retained in parsed output", () => {
  const output = JSON.stringify(core.parseLabSolutionsAscii(fixture, config));
  assert.equal(output.includes("C:\\LabSolutions\\Data"), false);
  assert.equal(output.includes("[Compound Results(Ch1)]"), false);
});
