"use strict";

const fs = require("fs");
const path = require("path");

const BASE = path.resolve(__dirname, "..");
const V1_BASE = path.resolve(BASE, "..", "2026-07-25_terpenes_simple_results_v1");
const SOURCE = path.join(BASE, "src", "terpenes_simple_results_parser_v2_controls.js");
const DIST_DIR = path.join(BASE, "dist");
const DIST = path.join(DIST_DIR, "terpenes_simple_results_parser_v2_controls.js");
const V1_WORKSHEET = path.join(V1_BASE, "SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V1__dimension_fix.json");
const WORKSHEET = path.join(BASE, "SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V2_CONTROLS.json");
const ARTIFACT_ONLY = process.argv.includes("--artifact-only");
const api = require(SOURCE);

function columnLetter(index) {
  let result = "";
  let value = index + 1;
  while (value > 0) {
    const digit = (value - 1) % 26;
    result = String.fromCharCode(65 + digit) + result;
    value = Math.floor((value - 1) / 26);
  }
  return result;
}

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function requireV1Baseline(candidate) {
  const worksheets = candidate && candidate.config && candidate.config.worksheets;
  if (!Array.isArray(worksheets) || worksheets.length !== 1 || worksheets[0].worksheetName !== "Results") {
    throw new Error("V1 worksheet must contain exactly one Results tab.");
  }
  const worksheet = worksheets[0];
  if (JSON.stringify(worksheet.minDimensions) !== JSON.stringify([51, 87])) {
    throw new Error("V1 corrected worksheet dimensions are not [51,87].");
  }
  if (!Array.isArray(worksheet.columns) || worksheet.columns.length !== api.RESULTS_HEADERS.length) {
    throw new Error("V1 worksheet column contract changed.");
  }
  if (!Array.isArray(worksheet.rows) || worksheet.rows.length !== api.LAST_DATA_ROW) {
    throw new Error("V1 worksheet row contract changed.");
  }
  if (!Array.isArray(worksheet.data) || worksheet.data.length !== api.LAST_DATA_ROW) {
    throw new Error("V1 worksheet data contract changed.");
  }
  if (JSON.stringify(worksheet.data[0]) !== JSON.stringify(api.RESULTS_HEADERS)) {
    throw new Error("V1 Results header changed.");
  }
  for (let index = 0; index < api.LAST_DATA_ROW - 1; index += 1) {
    const row = worksheet.data[index + 1] || [];
    const expected = [
      `\${tests[${index}].sample.get_display_id()}`,
      `\${tests[${index}].get_display_id()}`,
      `\${tests[${index}].sample.product_matrix}`,
    ];
    if (JSON.stringify(row.slice(0, 3)) !== JSON.stringify(expected)
      || row.slice(3).some((value) => value !== "")) {
      throw new Error(`V1 dynamic context row ${index + 2} changed.`);
    }
  }
  return worksheet;
}

function addFixedRunRecordsRegion(candidate) {
  const worksheet = requireV1Baseline(candidate);
  const v1Rows = clone(worksheet.rows);
  const v1Data = clone(worksheet.data);
  const v1Cells = clone(worksheet.cells);
  const v1Style = clone(worksheet.style);

  worksheet.csvFileName = "SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V2_CONTROLS";
  worksheet.worksheetId = "51a5e8c0-4e39-4d9d-9a0a-202607250102";
  worksheet.minDimensions = [api.RESULTS_HEADERS.length, api.WORKSHEET_LAST_ROW];
  worksheet.rows = v1Rows;
  while (worksheet.rows.length < api.WORKSHEET_LAST_ROW) {
    const rowNumber = worksheet.rows.length + 1;
    worksheet.rows.push({ height: rowNumber === api.AUDIT_SECTION_ROW ? 30 : 27 });
  }

  worksheet.data = v1Data;
  worksheet.data.push(Array(api.RESULTS_HEADERS.length).fill(""));
  worksheet.data.push(api.AUDIT_SECTION_VALUES.slice());
  worksheet.data.push(api.AUDIT_HEADERS.slice());
  while (worksheet.data.length < api.WORKSHEET_LAST_ROW) {
    worksheet.data.push(Array(api.RESULTS_HEADERS.length).fill(""));
  }

  worksheet.cells = v1Cells;
  worksheet.style = v1Style;
  const sectionStyle = candidate.config.style.length;
  const auditHeaderStyle = sectionStyle + 1;
  candidate.config.style.push(
    "font-weight:bold;background-color:#d9ead3;border-top:1px solid #6aa84f;border-bottom:1px solid #6aa84f",
    "font-weight:bold;background-color:#e2f0d9;border-top:1px solid #6aa84f;border-bottom:1px solid #6aa84f",
  );
  for (let row = api.AUDIT_SEPARATOR_ROW; row <= api.AUDIT_LAST_DATA_ROW; row += 1) {
    for (let column = 0; column < api.RESULTS_HEADERS.length; column += 1) {
      const address = `${columnLetter(column)}${row}`;
      worksheet.cells[address] = {
        readonly: row <= api.AUDIT_HEADER_ROW,
        type: "text",
        width: worksheet.columns[column].width,
        x: column,
      };
      if (row === api.AUDIT_SECTION_ROW) worksheet.style[address] = sectionStyle;
      if (row === api.AUDIT_HEADER_ROW) worksheet.style[address] = auditHeaderStyle;
    }
  }

  candidate.config.namespace = "51a5e8c0-4e39-4d9d-9a0a-202607250101";
  candidate.data = { Results: worksheet.data };
  return candidate;
}

fs.mkdirSync(DIST_DIR, { recursive: true });
const sourceText = fs.readFileSync(SOURCE, "utf8");
const banner = "/* SBX_ONLY Terpenes Simple Results V2 Controls browser-upload artifact. Generated from src/terpenes_simple_results_parser_v2_controls.js. */\n";
fs.writeFileSync(DIST, banner + sourceText, "utf8");

const v1Candidate = JSON.parse(fs.readFileSync(V1_WORKSHEET, "utf8"));
const v2Candidate = addFixedRunRecordsRegion(v1Candidate);
const worksheetText = `${JSON.stringify(v2Candidate, null, 2)}\n`;
if (ARTIFACT_ONLY) {
  if (fs.readFileSync(WORKSHEET, "utf8") !== worksheetText) {
    throw new Error("Protected V2 worksheet differs from the deterministic build output.");
  }
} else {
  fs.writeFileSync(WORKSHEET, worksheetText, "utf8");
}

console.log(`Built ${DIST}`);
console.log(ARTIFACT_ONLY ? `Verified unchanged ${WORKSHEET}` : `Built ${WORKSHEET}`);
