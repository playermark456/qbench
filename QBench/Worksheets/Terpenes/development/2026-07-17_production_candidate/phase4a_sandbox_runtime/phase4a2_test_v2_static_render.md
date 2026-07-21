# Phase 4A.2 Test v2 static render

Date: 2026-07-21

Neutral Sandbox identifier: `SANDBOX_TEST_WORKSHEET_V2`

## Preconditions

- Exact origin on every controlled page: `https://ait-sandbox.qbench.net`
- Exact-name collision search: no preexisting v2 object
- Failed v1 shell: located, inactive, and untouched
- Local candidate SHA-256: `7aa7469ec7767a7c7b4b0aa40194e927244adc3278999e23151f4eeb134dd5a4`
- Local candidate changed during the run: no

## Unsaved static render

`test_v2_static_render = passed`

QBench reported a successful import and rendered three selectable tabs in this exact order:

| Order | Tab | Visible dimensions | Result |
| ---: | --- | --- | --- |
| 1 | Report | 23 rows x 5 columns | passed |
| 2 | Data | 40 rows x 26 columns | passed |
| 3 | Specifications | 23 rows x 21 columns | passed |

### Report

- Headers were visible: Analyte, Result (mg/g), Result (%), LOQ, and MU (%).
- Rows 2 through 22 contained the 21 reportable analytes.
- Row 23 contained Total Terpenes.
- No rows for Ocimene 1, Ocimene 2, Nerolidol 1, Nerolidol 2, or Dimethylacetamide appeared.
- No Pass/Fail column or result appeared.

### Data

- Columns A through Z and rows 1 through 40 were visible.
- The 23 internal chromatographic channels occupied D through Z.
- Destination cells were blank and visibly writable.
- Preparation, controlled-disposition, and audit sections were visible.
- Row 40 retained the end-of-worksheet anchor.
- The workbook did not collapse to a one-cell/default grid.

### Specifications

- Columns A through U and rows 1 through 23 were visible.
- Reportable-analyte mapping, LOQ/MU bindings, combined Nerolidol/Ocimene logic, and Total Terpenes logic were present.
- Formula-driven unresolved/zero display states rendered without collapsing the worksheet; no Key/Value fixture was created.

## Save and reopen

The definition was saved once as inactive Draft version `1 - Terpenes Production Candidate Test Worksheet v2`. A visible `DRAFT` row existed in the Versions tab. It was then reopened from the Worksheets list.

`test_v2_save_reopen = passed`

After reopen, tab order, visible dimensions, content, styles, formulas, named definitions, and the non-collapsed layout remained present.
