"use strict";

const fs = require("fs");
const path = require("path");

const BASE = path.resolve(__dirname, "..");
const SOURCE = path.join(BASE, "src", "terpenes_simple_results_parser.js");
const DIST_DIR = path.join(BASE, "dist");
const DIST = path.join(DIST_DIR, "terpenes_simple_results_parser_v1.js");
const WORKSHEET = path.join(BASE, "SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V1.json");
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

function widthFor(header, index) {
  if (index === 0 || index === 1) return 145;
  if (index === 2) return 170;
  if (index >= 9 && index <= 31) return 125;
  if (/Hash|File|Status|Version|Name/.test(header)) return 190;
  if (/Count|Amount|Factor|Vial/.test(header)) return 125;
  return 155;
}

function buildWorksheetCandidate() {
  const headers = api.RESULTS_HEADERS.slice();
  const rows = Array.from({ length: api.LAST_DATA_ROW }, () => ({ height: 27 }));
  const columns = headers.map((header, index) => ({ type: "text", width: widthFor(header, index) }));
  const data = [headers];
  for (let testIndex = 0; testIndex < api.LAST_DATA_ROW - 1; testIndex += 1) {
    const row = Array(headers.length).fill("");
    row[0] = `\${tests[${testIndex}].sample.get_display_id()}`;
    row[1] = `\${tests[${testIndex}].get_display_id()}`;
    row[2] = `\${tests[${testIndex}].sample.product_matrix}`;
    data.push(row);
  }

  const cells = {};
  const style = {};
  for (let row = 1; row <= api.LAST_DATA_ROW; row += 1) {
    headers.forEach((header, column) => {
      const address = `${columnLetter(column)}${row}`;
      cells[address] = {
        readonly: row === 1 || column <= 2,
        type: "text",
        width: widthFor(header, column),
        x: column,
      };
      if (row === 1) style[address] = column === headers.length - 1 ? 3 : 2;
    });
  }

  const worksheet = {
    allowComments: false,
    allowDeleteColumn: true,
    allowDeleteRow: true,
    allowInsertColumn: true,
    allowInsertRow: true,
    allowRenameColumn: false,
    cache: {},
    cells,
    columnDrag: true,
    columnResize: true,
    columnSorting: false,
    columns,
    comments: {},
    csvFileName: "SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V1",
    filters: false,
    freezeColumnControl: true,
    freezeColumns: [],
    freezeRowControl: true,
    freezeRows: [],
    mergeCells: {},
    meta: {},
    minDimensions: [api.LAST_DATA_ROW, headers.length],
    resize: "vertical",
    rowDrag: true,
    rowResize: true,
    rows,
    tableHeight: 850,
    tableOverflow: true,
    tableWidth: 2200,
    worksheetId: "51a5e8c0-4e39-4d9d-9a0a-202607250001",
    worksheetName: api.RESULTS_TAB,
    data,
    style,
  };

  return {
    config: {
      allowDeleteWorksheet: true,
      allowMoveWorksheet: true,
      allowRenameWorksheet: true,
      application: "QBench",
      autoCasting: false,
      bar: true,
      entityId: "SPREADSHEET_EDITOR",
      namespace: "51a5e8c0-4e39-4d9d-9a0a-202607250000",
      plugins: { conditionalFormatting: { rules: [] } },
      qbConfigs: {
        generalSpreadsheetSettings: {
          enableSpreadsheetCustomization: false,
          allowTabEditing: true,
          showToolbar: true,
        },
        reportSpreadsheetSettings: { enableReportBorders: false },
      },
      tabs: {
        allowCreate: true,
        allowChangePosition: true,
        animation: true,
        position: "top",
        maxWidth: "-50px",
      },
      style: [
        "font-weight:bold",
        "font-weight:bold;background-color:#e0e0e0",
        "font-weight:bold;background-color:#e0e0e0;border-top:1px solid black;border-bottom:1px solid black;border-left:1px solid black",
        "font-weight:bold;background-color:#e0e0e0;border-top:1px solid black;border-right:1px solid black;border-bottom:1px solid black;border-left:1px solid black",
      ],
      worksheets: [worksheet],
    },
    qb_config: { kvstore_config: {} },
    data: { Results: data },
  };
}

fs.mkdirSync(DIST_DIR, { recursive: true });
const sourceText = fs.readFileSync(SOURCE, "utf8");
const banner = "/* SBX_ONLY Terpenes Simple Results V1 browser-upload artifact. Generated from src/terpenes_simple_results_parser.js. */\n";
fs.writeFileSync(DIST, banner + sourceText, "utf8");
fs.writeFileSync(WORKSHEET, `${JSON.stringify(buildWorksheetCandidate(), null, 2)}\n`, "utf8");

console.log(`Built ${DIST}`);
console.log(`Built ${WORKSHEET}`);
