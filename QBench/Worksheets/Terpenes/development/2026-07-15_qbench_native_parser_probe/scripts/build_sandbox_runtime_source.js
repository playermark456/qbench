"use strict";

/* Creates a synthetic-only runtime source in the ignored runtime directory. */
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");

const REQUIRED_SHA256 = "bfd88621e2e8ab791e63ba38f07c9a1174f9600e1cf3f28d5b12ffbd08f2eb91";
const PACKAGE = path.resolve(__dirname, "..");
const DEFAULT_OUTPUT = path.join(PACKAGE, "runtime", "terpenes_synthetic_runtime_source.txt");

function hash(buffer) { return crypto.createHash("sha256").update(buffer).digest("hex"); }
function sampleType(block) { const match = block.match(/^Sample Type\t([^\r\n]*)/m); const name = block.match(/^Sample Name\t([^\r\n]*)/m); const id = block.match(/^Sample ID\t([^\r\n]*)/m); return `${match ? match[1] : ""} ${name ? name[1] : ""} ${id ? id[1] : ""}`; }
function reportableSample(block) { const text = sampleType(block).toLowerCase(); return !/system\s*suit|\bccv\b|matrix\s*blank|\bnull\b|\bblank\b|\bloq\b|\bstandard\b/.test(text); }
function build(input, output, identifiers) {
  if (!identifiers[0] || !identifiers[1]) throw new Error("TEST_A_VISIBLE_IDENTIFIER and TEST_B_VISIBLE_IDENTIFIER are required.");
  const original = fs.readFileSync(input); if (hash(original) !== REQUIRED_SHA256) throw new Error("operational_raw_source_missing_or_changed");
  const text = original.toString("utf8"); const blocks = text.split(/(?=^\[Header\]\r?\n)/m); const selected = [];
  blocks.forEach((block, index) => { if (reportableSample(block) && /^Sample ID\t[^\r\n]+/m.test(block)) selected.push(index); });
  if (selected.length < 2) throw new Error("insufficient_reportable_samples");
  const replacement = new Map([[selected[0], identifiers[0]], [selected[1], identifiers[1]]]);
  const outputText = blocks.map((block, index) => replacement.has(index) ? block.replace(/(^Sample ID\t)[^\r\n]*/m, `$1${replacement.get(index)}`) : block).join("");
  fs.mkdirSync(path.dirname(output), { recursive: true }); fs.writeFileSync(output, outputText, "utf8");
  return { output, original_sha256: REQUIRED_SHA256, runtime_sha256: hash(Buffer.from(outputText, "utf8")), replaced_record_count: 2 };
}
if (require.main === module) {
  const input = process.argv[2]; if (!input) throw new Error("Usage: node build_sandbox_runtime_source.js <authoritative-source-path> [output-path]");
  process.stdout.write(`${JSON.stringify(build(input, process.argv[3] || DEFAULT_OUTPUT, [process.env.TEST_A_VISIBLE_IDENTIFIER, process.env.TEST_B_VISIBLE_IDENTIFIER]))}\n`);
}
module.exports = { build, REQUIRED_SHA256 };
