"use strict";

const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { build } = require("../scripts/build_qbench_parser_artifact.js");
const runtimeGenerator = require("../scripts/build_sandbox_runtime_source.js");
const cli = require("../src/terpenes_multirecord_batch_cli.js");
const core = require("../src/qbench_browser_parser_core.js");
const adapter = require("../src/terpenes_multirecord_batch_adapter.js");

const PACKAGE = path.resolve(__dirname, "..");
const REPO = path.resolve(PACKAGE, "../../../../..");
const RAW = "C:\\Users\\Mark Adams\\Downloads\\ASCIIData (1).txt";
const ARTIFACT = path.join(PACKAGE, "dist", "terpenes_multirecord_qbench_parser.js");
const RUNTIME = path.join(PACKAGE, "runtime", "terpenes_synthetic_runtime_source.txt");
const CONFIG = JSON.parse(fs.readFileSync(path.join(REPO, "QBench/Worksheets/Terpenes/development/2026-07-14_config_parser_foundation/config/terpenes_analytes.json"), "utf8"));
const EXPECTED_OPERATIONAL_HASH = "61f91070e0b68b5c5c06de580efe0569d13075a032441968e9d43bec763c1d9e";
const EXPECTED_RAW_HASH = runtimeGenerator.REQUIRED_SHA256;
let count = 0;

function test(name, fn) { return Promise.resolve().then(fn).then(() => { count += 1; process.stdout.write(`ok ${count} - ${name}\n`); }); }
function hash(input) { return crypto.createHash("sha256").update(input).digest("hex"); }
function column(index) { let value = ""; let n = index + 1; while (n) { const part = (n - 1) % 26; value = String.fromCharCode(65 + part) + value; n = Math.floor((n - 1) / 26); } return value; }
function grid() { const values = Array.from({ length: 201 }, () => Array(57).fill("")); values[0] = adapter.BATCH_HEADERS.slice(); return values; }
function deep(value) { return JSON.parse(JSON.stringify(value)); }

function makeHarness(source, options = {}) {
  const calls = { imports: [], gets: [], updates: [], success: 0, error: 0, logs: [], progress: [] };
  const raw = grid(); const processed = grid();
  if (options.badHeader) processed[0][0] = "wrong_header";
  raw[1][31] = "formula-owned-raw"; raw[1][32] = "formula-owned-raw";
  processed[1][31] = "formula-owned-processed"; processed[1][32] = "formula-owned-processed";
  const formulas = { AF2: "=preserved_formula", AG2: "=preserved_message_formula" };
  const images = { logo: "preserved_image" }; const refs = { B2: "preserved_reference" };
  if (options.missingTab) raw.length = 0;
  class Reader { readAsText(file) { this.onload({ target: { result: file.content } }); } }
  class Service {
    getJson(request) {
      calls.gets.push({ url: request.url, urlParams: deep(request.urlParams) });
      if (request.url === "/batches/get") {
        const id = request.urlParams.test_id;
        let answer = [];
        if (options.mode === "zero") answer = [];
        else if (options.mode === "multiple") answer = id === "SYNTHETIC_TEST_A" ? [{ id: "batch-a" }] : [{ id: "batch-b" }];
        else answer = id === "SYNTHETIC_TEST_A" || id === "SYNTHETIC_TEST_B" ? [{ id: "batch-one" }] : [];
        request.success(answer); return;
      }
      if (request.url === "/batches/worksheets/dynamic") {
        if (options.missingTab) { request.success([]); return; }
        request.success([
          { worksheet_name: "Instrument Import", type: "WORKSHEET_DATA", data: raw },
          { worksheet_name: "Instrument Import", type: "WORKSHEET_DATA_PROCESSED", data: processed },
          { worksheet_name: "Instrument Import", type: "WORKSHEET_FORMULAS", data: formulas },
          { worksheet_name: "Instrument Import", type: "WORKSHEET_IMAGE_DATA", data: images },
          { worksheet_name: "Instrument Import", type: "WORKSHEET_DOLLAR_REFERENCES", data: refs },
        ]); return;
      }
      request.error(new Error("unexpected request"));
    }
    update(request) { calls.updates.push(request); if (options.rejectUpdate) request.error(new Error("synthetic update failure")); else request.success({ ok: true }); }
  }
  const context = {
    console: { log() {} },
    importScripts: (...urls) => calls.imports.push(...urls),
    run: (fn) => { context.done = Promise.resolve().then(fn); },
    QB: { files: [{ name: options.name || "runtime.txt", content: source }], console: { clear() {}, log(value) { calls.logs.push(String(value)); } }, progressBar: { setPercentage(value) { calls.progress.push(value); } }, success() { calls.success += 1; }, error() { calls.error += 1; } },
    QBBatchService: Service,
    FileReader: Reader,
    Papa: { parse() { return { data: [], errors: [] }; } },
    XLSX: {},
    Set, Map, Object, Array, String, Number, Boolean, RegExp, Error, Promise, JSON, Math, Date, encodeURIComponent, unescape,
  };
  vm.createContext(context); vm.runInContext(fs.readFileSync(ARTIFACT, "utf8"), context, { filename: "terpenes_multirecord_qbench_parser.js" });
  return context.done.then(() => ({ calls, formulas, images, refs }));
}

async function expectFailure(source, options) { const result = await makeHarness(source, options); assert.equal(result.calls.updates.length, 0); assert.equal(result.calls.success, 0); assert.equal(result.calls.error, 1); return result; }

(async () => {
  await test("operational reference hash", () => assert.equal(hash(fs.readFileSync("C:\\Users\\Mark Adams\\Downloads\\Qbench live potency parser.txt")), EXPECTED_OPERATIONAL_HASH));
  await test("authoritative raw source hash", () => assert.equal(hash(fs.readFileSync(RAW)), EXPECTED_RAW_HASH));
  const buildResult = build();
  await test("artifact was deterministically built", () => assert.equal(hash(fs.readFileSync(ARTIFACT)), buildResult.sha256));
  await test("artifact syntax and Node dependency exclusion", () => { const source = fs.readFileSync(ARTIFACT, "utf8"); new vm.Script(source); assert.doesNotMatch(source, /\brequire\s*\(|\bmodule\b|\bexports\b|\bprocess\b|\bBuffer\b|\b__dirname\b|\b__filename\b|\bchild_process\b|node:/); });
  await test("wrapper contract imports the operational services", () => { const source = fs.readFileSync(ARTIFACT, "utf8"); assert.match(source, /file_parser\.js/); assert.match(source, /qbjs\.js/); assert.match(source, /xlsx\.full\.min\.js/); assert.match(source, /papaparse\.min\.js/); assert.match(source, /QBBatchService/); });
  const runtime = runtimeGenerator.build(RAW, RUNTIME, ["SYNTHETIC_TEST_A", "SYNTHETIC_TEST_B"]);
  const source = fs.readFileSync(RUNTIME, "utf8");
  await test("runtime source generator preserves original and replaces two synthetic IDs", () => { assert.equal(runtime.original_sha256, EXPECTED_RAW_HASH); assert.equal(runtime.replaced_record_count, 2); assert.notEqual(runtime.runtime_sha256, EXPECTED_RAW_HASH); assert.equal(hash(fs.readFileSync(RAW)), EXPECTED_RAW_HASH); });
  const parsed = core.parseLabSolutionsAsciiMultiRecord(source, CONFIG);
  const normalized = adapter.normalizeRecords(parsed, CONFIG, { source_file_sha256: runtime.runtime_sha256, runtime_mapping: [] });
  await test("local CLI summary agrees with the adapter baseline", () => { const summary=cli.run(["--input", RUNTIME]); assert.equal(summary.records, 34); assert.equal(summary.batch_columns, 57); assert.equal(summary.write_columns, 55); assert.deepEqual(summary.categories, { Null: 3, Blank: 2, "System Suitability": 3, Standard: 6, CCV: 3, LOQ: 1, "Matrix Blank": 1, Sample: 15 }); });
  await test("TXT split, required sections, channels, and category counts", () => { assert.equal(parsed.records.length, 34); const categories = normalized.rows.reduce((out, row) => ((out[row.category] = (out[row.category] || 0) + 1), out), {}); assert.deepEqual(categories, { Null: 3, Blank: 2, "System Suitability": 3, Standard: 6, CCV: 3, LOQ: 1, "Matrix Blank": 1, Sample: 15 }); parsed.records.forEach((record) => { assert.equal(record.counts.compound_result_row_count, 24); assert.equal(record.counts.reportable_compound_row_count, 23); }); });
  await test("every Compound Results table has the controlled IDs one through 24", () => parsed.records.forEach((record) => assert.deepEqual(record.compound_results.map((row) => row["ID#"]), Array.from({ length: 24 }, (_, index) => index + 1))));
  await test("23-channel order matches the Batch AH:BD contract", () => assert.deepEqual(CONFIG.internal_reportable_channels.map((channel) => channel.worksheet_label), adapter.BATCH_HEADERS.slice(33, 56)));
  await test("audit-only Dimethylacetamide and Peak Table audit are retained", () => { assert.equal(normalized.batch_headers.length, 57); assert.equal(normalized.rows[0].batch_row[26] !== "", true); assert.equal(normalized.rows.reduce((sum,row) => sum + Number(row.batch_row[27] || 0), 0), 138); });
  await test("adapter owns 55 writable fields and excludes formula-owned AF/AG", () => normalized.rows.forEach((row) => assert.equal(row.write_cells.length, 55)));
  const success = await makeHarness(source);
  await test("mock browser runtime performs one atomic update", () => { assert.equal(success.calls.success, 1); assert.equal(success.calls.error, 0); assert.equal(success.calls.updates.length, 1); assert.equal(success.calls.gets.filter((call) => call.url === "/batches/worksheets/dynamic").length, 1); assert.equal(success.calls.updates[0].urlParams.run_worksheet_calculations, true); });
  await test("batch discovery resolves exactly two synthetic IDs on one batch", () => { const requests = success.calls.gets.filter((call) => call.url === "/batches/get"); assert.equal(requests.length, 15); assert.equal(requests.filter((call) => call.urlParams.test_id === "SYNTHETIC_TEST_A" || call.urlParams.test_id === "SYNTHETIC_TEST_B").length, 2); });
  const payload = success.calls.updates[0].data.qb_dynamic_spreadsheet_data["Instrument Import"];
  await test("57-column mapping and parser-owned ranges are exact", () => { for(let row=2;row<=35;row+=1){ assert.ok(Object.prototype.hasOwnProperty.call(payload.WORKSHEET_DATA, `A${row}`)); assert.ok(Object.prototype.hasOwnProperty.call(payload.WORKSHEET_DATA, `BE${row}`)); } for(let row=36;row<=201;row+=1){ assert.equal(payload.WORKSHEET_DATA[`A${row}`], ""); assert.equal(payload.WORKSHEET_DATA[`BE${row}`], ""); } });
  await test("artifact and local adapter use the same source SHA-256", () => { assert.equal(payload.WORKSHEET_DATA.O2, runtime.runtime_sha256); assert.equal(normalized.rows[0].batch_row[14], runtime.runtime_sha256); });
  await test("AF/AG and non-data maps are preserved", () => { assert.equal(payload.WORKSHEET_DATA.AF2, "formula-owned-raw"); assert.equal(payload.WORKSHEET_DATA.AG2, "formula-owned-raw"); for(let row=3;row<=201;row+=1){ assert.equal(payload.WORKSHEET_DATA[`AF${row}`], undefined); assert.equal(payload.WORKSHEET_DATA[`AG${row}`], undefined); } assert.deepEqual(payload.WORKSHEET_FORMULAS, success.formulas); assert.deepEqual(payload.WORKSHEET_IMAGE_DATA, success.images); assert.deepEqual(payload.WORKSHEET_DOLLAR_REFERENCES, success.refs); });
  await test("sample linkage, unresolved holds, and control exclusion", () => { const map=payload.WORKSHEET_DATA; const ids=Array.from({length:34},(_,i)=>map[`E${i+2}`]); assert.equal(ids.filter(Boolean).length,2); assert.equal(ids.includes("SYNTHETIC_TEST_A"),true); assert.equal(ids.includes("SYNTHETIC_TEST_B"),true); assert.equal(ids.filter(Boolean).length + ids.filter((_,i)=>normalized.rows[i].category === "Sample" && !ids[i]).length,15); assert.equal(normalized.rows.filter((row)=>row.category !== "Sample").length,19); });
  await test("CLI-to-artifact field equivalence after runtime linkage normalization", () => { normalized.rows.forEach((row,index)=>{ const current=payload.WORKSHEET_DATA; const expected=row.batch_row.slice(); expected[4] = row.sample_id === "SYNTHETIC_TEST_A" || row.sample_id === "SYNTHETIC_TEST_B" ? row.sample_id : ""; expected[22] = "terpenes-qbench-coded-parser-v1"; expected.forEach((value,columnIndex)=>{ if(columnIndex === 31 || columnIndex === 32) return; assert.deepEqual(current[`${column(columnIndex)}${index + 2}`], value === undefined || value === null ? "" : value); }); }); });
  await test("CSV input follows the same contract", async () => { const result=await makeHarness(source,{name:"runtime.csv"}); assert.equal(result.calls.success,1); assert.equal(result.calls.updates.length,1); });
  await test("unsupported input type fails before update", () => expectFailure(source,{name:"runtime.xlsx"}));
  await test("zero resolved IDs fails before update", () => expectFailure(source,{mode:"zero"}));
  await test("multiple resolved batches fail before update", () => expectFailure(source,{mode:"multiple"}));
  await test("duplicate resolved Test ID fails before update", () => expectFailure(source.replace("SYNTHETIC_TEST_B","SYNTHETIC_TEST_A")));
  await test("malformed record fails before update", () => expectFailure(source.replace("[Configuration]","[Broken Configuration]")));
  await test("missing Instrument Import tab fails before update", () => expectFailure(source,{missingTab:true}));
  await test("57-column header mismatch fails before update", () => expectFailure(source,{badHeader:true}));
  await test("over-capacity source fails before update", () => expectFailure(source.repeat(6)));
  await test("update rejection calls QB.error", async () => { const result=await makeHarness(source,{rejectUpdate:true}); assert.equal(result.calls.updates.length,1); assert.equal(result.calls.success,0); assert.equal(result.calls.error,1); });
  await test("deterministic range replacement is idempotent", async () => { const first=await makeHarness(source); const second=await makeHarness(source); const a=first.calls.updates[0].data.qb_dynamic_spreadsheet_data["Instrument Import"]; const b=second.calls.updates[0].data.qb_dynamic_spreadsheet_data["Instrument Import"]; assert.equal(JSON.stringify(a.WORKSHEET_DATA),JSON.stringify(b.WORKSHEET_DATA)); assert.equal(JSON.stringify(a.WORKSHEET_DATA_PROCESSED),JSON.stringify(b.WORKSHEET_DATA_PROCESSED)); });
  process.stdout.write(JSON.stringify({ focused_tests_passed: count, artifact: ARTIFACT, runtime_source_sha256: runtime.runtime_sha256 }) + "\n");
})().catch((error) => { process.stderr.write(`${error.stack || error}\n`); process.exitCode = 1; });
