"use strict";

const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const core = require("./qbench_browser_parser_core.js");
const adapter = require("./terpenes_multirecord_batch_adapter.js");

const PACKAGE = path.resolve(__dirname, "..");
const REPO = path.resolve(PACKAGE, "../../../../..");
const CONFIG_PATH = path.join(REPO, "QBench/Worksheets/Terpenes/development/2026-07-14_config_parser_foundation/config/terpenes_analytes.json");

function usage() {
  return "Usage: node terpenes_multirecord_batch_cli.js --input <ASCIIData.txt> [--mapping <ignored-runtime.csv>] [--output <ignored-normalized.json>]";
}

function argumentsToObject(argumentsList) {
  const options = {};
  for (let index = 0; index < argumentsList.length; index += 1) {
    const option = argumentsList[index];
    if (!option.startsWith("--") || !argumentsList[index + 1]) throw new Error(usage());
    options[option.slice(2)] = argumentsList[index + 1];
    index += 1;
  }
  if (!options.input) throw new Error(usage());
  return options;
}

function run(argumentsList) {
  const options = argumentsToObject(argumentsList);
  const sourceBuffer = fs.readFileSync(options.input);
  const source = sourceBuffer.toString("utf8");
  const sourceHash = crypto.createHash("sha256").update(sourceBuffer).digest("hex");
  const config = JSON.parse(fs.readFileSync(CONFIG_PATH, "utf8"));
  const runtimeMapping = options.mapping ? adapter.parseRuntimeMappingCsv(fs.readFileSync(options.mapping, "utf8")) : [];
  const parsed = core.parseLabSolutionsAsciiMultiRecord(source, config);
  const normalized = adapter.normalizeRecords(parsed, config, {
    source_file_sha256: sourceHash,
    runtime_mapping: runtimeMapping,
  });
  if (options.output) fs.writeFileSync(options.output, `${JSON.stringify(normalized, null, 2)}\n`, "utf8");
  const categories = {};
  normalized.rows.forEach((row) => { categories[row.category] = (categories[row.category] || 0) + 1; });
  return {
    source_sha256: sourceHash,
    records: normalized.rows.length,
    batch_columns: normalized.batch_headers.length,
    write_columns: normalized.rows[0] ? normalized.rows[0].write_cells.length : 0,
    categories,
    output_written: Boolean(options.output),
  };
}

if (require.main === module) {
  try { process.stdout.write(`${JSON.stringify(run(process.argv.slice(2)))}\n`); }
  catch (error) { process.stderr.write(`${error.code || "CLI_ERROR"}: ${error.message}\n`); process.exitCode = 1; }
}

module.exports = { run, argumentsToObject };
