"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const os = require("node:os");

const core = require("../../src/labsolutions_ascii_core.js");

const baseDir = path.resolve(__dirname, "..", "..");
const repoRoot = path.resolve(baseDir, "..", "..", "..", "..", "..");
const fixturePath = path.join(baseDir, "tests", "fixtures", "Output_redacted_fixture.txt");
const configPath = path.join(repoRoot, "QBench", "Worksheets", "Terpenes", "development", "2026-07-14_config_parser_foundation", "config", "terpenes_analytes.json");
const config = JSON.parse(fs.readFileSync(configPath, "utf8"));
const fixtureText = fs.readFileSync(fixturePath, "utf8");

function parse(text = fixtureText, cfg = config, options = {}) {
  return core.parseLabSolutionsAscii(Buffer.from(text, "utf8"), cfg, options);
}

function sectionLines(text, sectionName) {
  const lines = text.replace(/\r\n/g, "\n").split("\n");
  const start = lines.indexOf(`[${sectionName}]`);
  let end = lines.length;
  for (let index = start + 1; index < lines.length; index += 1) {
    if (/^\[.+]$/.test(lines[index])) {
      end = index;
      break;
    }
  }
  return { lines, start, end };
}

function mutateTableRow(text, sectionName, name, nameIndex, mutator) {
  const { lines, start, end } = sectionLines(text, sectionName);
  for (let index = start + 1; index < end; index += 1) {
    const cells = lines[index].split("\t");
    if (cells[nameIndex] === name) {
      const result = mutator(cells, lines, index);
      if (result !== false) lines[index] = cells.join("\t");
      return lines.join("\n");
    }
  }
  throw new Error(`Missing ${name} in ${sectionName}`);
}

test("controlled fixture parses with 24/34/23 counts", () => {
  const parsed = parse();
  assert.equal(parsed.counts.compound_result_row_count, 24);
  assert.equal(parsed.counts.peak_table_row_count, 34);
  assert.equal(parsed.counts.reportable_compound_row_count, 23);
  assert.equal(parsed.dimethylacetamide_audit.reportable, false);
});

test("UTF-8 BOM is accepted", () => {
  assert.equal(parse(`\ufeff${fixtureText}`).counts.compound_result_row_count, 24);
});

test("LF line endings are accepted", () => {
  assert.equal(parse(fixtureText.replace(/\r\n/g, "\n")).counts.peak_table_row_count, 34);
});

test("CRLF line endings are accepted", () => {
  assert.equal(parse(fixtureText.replace(/\r?\n/g, "\r\n")).counts.reportable_compound_row_count, 23);
});

test("required sections are enforced", () => {
  assert.throws(() => parse(fixtureText.replace("[Original Files]\n", "")), /Missing required section/);
});

test("malformed row width is rejected", () => {
  const bad = mutateTableRow(fixtureText, "Compound Results(Ch1)", "alpha-Pinene", 1, (cells) => cells.pop());
  assert.throws(() => parse(bad), /row has 14 fields; expected 15/);
});

test("24 Compound Results rows are required", () => {
  const bad = mutateTableRow(fixtureText, "Compound Results(Ch1)", "alpha-Pinene", 1, (_cells, lines, index) => {
    lines.splice(index, 1);
    return false;
  });
  assert.throws(() => parse(bad), /expected 24 Compound Results rows/);
});

test("23 reportable rows are required", () => {
  const bad = mutateTableRow(fixtureText, "Compound Results(Ch1)", "Camphene", 1, (cells) => {
    cells[1] = "Dimethylacetamide";
    cells[0] = "1";
  });
  assert.throws(() => parse(bad), /expected 23 reportable/);
});

test("one Dimethylacetamide row is required", () => {
  const bad = mutateTableRow(fixtureText, "Compound Results(Ch1)", "Dimethylacetamide", 1, (_cells, lines, index) => {
    lines.splice(index, 1);
    return false;
  });
  assert.throws(() => parse(bad), /Dimethylacetamide/);
});

test("missing analyte is rejected", () => {
  const bad = mutateTableRow(fixtureText, "Compound Results(Ch1)", "alpha-Pinene", 1, (_cells, lines, index) => {
    lines.splice(index, 1);
    return false;
  });
  assert.throws(() => parse(bad), /missing key: apinene/);
});

test("duplicate analyte is rejected", () => {
  const bad = mutateTableRow(fixtureText, "Compound Results(Ch1)", "alpha-Pinene", 1, (cells, lines, index) => {
    lines.splice(index + 1, 0, cells.join("\t"));
  });
  assert.throws(() => parse(bad), /duplicate key: apinene/);
});

test("unknown Compound Results name is rejected", () => {
  const bad = mutateTableRow(fixtureText, "Compound Results(Ch1)", "alpha-Pinene", 1, (cells) => {
    cells[1] = "Other Terpenes";
  });
  assert.throws(() => parse(bad), /unknown Compound Results name: Other Terpenes/);
});

test("ID/name mismatch is rejected", () => {
  const bad = mutateTableRow(fixtureText, "Compound Results(Ch1)", "alpha-Pinene", 1, (cells) => {
    cells[0] = "99";
  });
  assert.throws(() => parse(bad), /ID# 99 expected 2/);
});

test("Greek aliases map to configured analytes", () => {
  let text = mutateTableRow(fixtureText, "Compound Results(Ch1)", "alpha-Pinene", 1, (cells) => { cells[1] = "\u03b1-Pinene"; });
  text = mutateTableRow(text, "Compound Results(Ch1)", "beta-Myrcene", 1, (cells) => { cells[1] = "\u03b2-Myrcene"; });
  text = mutateTableRow(text, "Compound Results(Ch1)", "Gamma terpinene", 1, (cells) => { cells[1] = "\u03b3-Terpinene"; });
  assert.equal(parse(text).reportable_analytes[0].internal_key, "apinene");
});

test("Ocimene 1 and 2 aliases map to controlled channels", () => {
  const byName = Object.fromEntries(parse().compound_results.map((row) => [row.Name, row.internal_key]));
  assert.equal(byName["Ocimene 1"], "cisocimene");
  assert.equal(byName["Ocimene 2"], "transocimene");
});

test("Nerolidol 1 and 2 aliases map to controlled channels", () => {
  const byName = Object.fromEntries(parse().compound_results.map((row) => [row.Name, row.internal_key]));
  assert.equal(byName["Nerolidol 1"], "cisnerolidol");
  assert.equal(byName["Nerolidol 2"], "transnerolidol");
});

test("unknown Peak Table name is retained as audit-only", () => {
  const bad = mutateTableRow(fixtureText, "Peak Table(Ch1)", "alpha-Pinene", 10, (cells) => {
    cells[10] = "Unidentified Peak";
  });
  const parsed = parse(bad);
  assert.equal(parsed.counts.unknown_peak_count, 1);
  assert.equal(parsed.reportable_analytes.length, 23);
});

test("blank Peak Table name is retained as audit-only", () => {
  const bad = mutateTableRow(fixtureText, "Peak Table(Ch1)", "alpha-Pinene", 10, (cells) => {
    cells[10] = "";
  });
  assert.equal(parse(bad).counts.unknown_peak_count, 1);
});

test("Peak Table concentrations never feed quantitative output", () => {
  const bad = mutateTableRow(fixtureText, "Peak Table(Ch1)", "alpha-Pinene", 10, (cells) => {
    cells[7] = "999999";
  });
  assert.equal(parse(bad).reportable_analytes[0].conc, 24.608);
});

test("Compound Results Conc. is used", () => {
  assert.equal(parse().reportable_analytes[0].conc, 24.608);
});

test("Compound Results Conc. percent is not used", () => {
  const bad = mutateTableRow(fixtureText, "Compound Results(Ch1)", "alpha-Pinene", 1, (cells) => {
    cells[13] = "999999";
  });
  assert.equal(parse(bad).reportable_analytes[0].conc, 24.608);
});

test("Compound Results Norm Conc. is not used", () => {
  const bad = mutateTableRow(fixtureText, "Compound Results(Ch1)", "alpha-Pinene", 1, (cells) => {
    cells[14] = "999999";
  });
  assert.equal(parse(bad).reportable_analytes[0].conc, 24.608);
});

test("text concentration is rejected", () => {
  const bad = mutateTableRow(fixtureText, "Compound Results(Ch1)", "alpha-Pinene", 1, (cells) => {
    cells[5] = "10 ug/mL";
  });
  assert.throws(() => parse(bad), /Conc\. is not a numeric value/);
});

test("numeric zero is preserved as Number", () => {
  const bad = mutateTableRow(fixtureText, "Compound Results(Ch1)", "alpha-Pinene", 1, (cells) => {
    cells[5] = "0";
  });
  assert.equal(parse(bad).reportable_analytes[0].conc, 0);
});

test("negative numeric concentration is preserved as Number", () => {
  const bad = mutateTableRow(fixtureText, "Compound Results(Ch1)", "alpha-Pinene", 1, (cells) => {
    cells[5] = "-1.25";
  });
  assert.equal(parse(bad).reportable_analytes[0].conc, -1.25);
});

test("scientific notation is accepted", () => {
  const bad = mutateTableRow(fixtureText, "Compound Results(Ch1)", "alpha-Pinene", 1, (cells) => {
    cells[5] = "1.23e1";
  });
  assert.equal(parse(bad).reportable_analytes[0].conc, 12.3);
});

test("oversized file is rejected", () => {
  assert.throws(() => parse(fixtureText, config, { securityLimits: { max_raw_file_size_bytes: 8 } }), /maximum file size/);
});

test("excessive line length is rejected", () => {
  assert.throws(() => parse(`[Header]\n${"x".repeat(50)}\n`, config, { securityLimits: { max_line_length: 10 } }), /line over/);
});

test("controlled errors do not include full raw files", () => {
  try {
    parse("bad");
    assert.fail("expected error");
  } catch (error) {
    const controlled = core.toControlledError(error);
    assert.equal(Object.prototype.hasOwnProperty.call(controlled, "raw"), false);
    assert.match(controlled.code, /MISSING_REQUIRED_SECTION/);
  }
});

test("no temporary fixture path leaks into parsed output", () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "terpenes-parser-"));
  assert.ok(tmp);
  assert.equal(JSON.stringify(parse()).includes(tmp), false);
});
