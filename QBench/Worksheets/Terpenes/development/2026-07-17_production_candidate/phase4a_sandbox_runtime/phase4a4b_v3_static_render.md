# Phase 4A.4B Test v3 static render

Date: 2026-07-21

## Result

`test_v3_static_render = passed`

The native file import removed default `Sheet1` before save and rendered three selectable tabs in this exact order:

| Order | Tab | Dimensions | Result |
| ---: | --- | --- | --- |
| 1 | Report | 23 rows x 5 columns | passed |
| 2 | Data | 40 rows x 26 columns | passed |
| 3 | Specifications | 23 rows x 21 columns | passed |

### Report

- Exact headers: `Analyte`, `Result (mg/g)`, `Result (%)`, `LOQ`, and `MU (%)`.
- Exactly 21 reportable analytes plus Total Terpenes.
- No report row for Ocimene 1, Ocimene 2, Nerolidol 1, Nerolidol 2, or Dimethylacetamide.
- No Pass/Fail field or result.

### Data

- Rows 1 through 40 and columns A through Z retained the V3 structure.
- The 23 internal chromatographic channels remained in D through Z.
- All 43 destination cells were blank, writable, unique, non-formula, and exportable.
- Preparation, controlled-disposition, and source/audit sections remained visible.
- The runtime matrix placeholder remained definition-owned; no runtime value was required or entered.

### Specifications and formulas

- Rows 1 through 23 and columns A through U retained the analyte mapping and LOQ/MU binding structure.
- Direct mg/g conversion remained at `Specifications!D2`.
- Direct percent conversion remained at `Specifications!E2`.
- Direct LOQ and MU lookup formulas remained at `Specifications!F2:G2`.
- Nerolidol and Ocimene combinations remained at `Specifications!C19` and `Specifications!C20`.
- Combined Nerolidol and Ocimene MU formulas remained at `Specifications!G19` and `Specifications!G20`.
- Total Terpenes remained at `Specifications!C23`.
- The Report-to-Specifications reference remained at `Report!B2`.
- All 309 authoritative embedded formulas were retained by the saved/reopened export.
- No `SANDBOX_CONFIGURATION_REQUIRED` marker remained.

The single saved version was reopened from the Worksheets list. The same three tabs, exact order, dimensions, structure, styles, protection, formulas, named definitions, and non-collapsed layout remained present.
