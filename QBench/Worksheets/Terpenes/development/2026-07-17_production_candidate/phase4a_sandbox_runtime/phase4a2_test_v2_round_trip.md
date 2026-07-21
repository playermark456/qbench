# Phase 4A.2 Test v2 saved-definition round trip

Date: 2026-07-21

## Inputs

- Local candidate SHA-256: `7aa7469ec7767a7c7b4b0aa40194e927244adc3278999e23151f4eeb134dd5a4`
- Raw saved/reopened Export Spreadsheet SHA-256: `cf479247be1271d4e8559bb6991d9869a9b6c1324c83c32b227d68d42e7ef127`
- Raw export tracking state: ignored and uncommitted
- Comparison mode: parsed JSON with key ordering ignored; generated namespace value treated as non-semantic

## Preserved contract

| Contract element | Result |
| --- | --- |
| Tab order `Report`, `Data`, `Specifications` | exact |
| Actual top-level array dimensions 23x5, 40x26, 23x21 | exact |
| Embedded worksheet `data` arrays | exact |
| Embedded formulas | exact: 309 of 309 retained |
| `qb_config`, named cells, and `report_results` | exact |
| Config and worksheet styles | exact |
| Rows, columns, cells, and cell metadata | exact |
| Number formats, protection, hidden-row/column configuration | exact |
| Key/Value formulas in embedded worksheet data | exact |

## QBench serialization normalizations

The raw comparison found 322 scalar differences:

- 1 generated namespace difference, ignored as non-semantic.
- 6 `minDimensions` scalar differences: Report `[5, 23]`, Data `[26, 40]`, and Specifications `[21, 23]` each became `[1, 1]`.
- 6 viewport-size differences: each worksheet's `tableWidth`/`tableHeight` became `1954`/`350` instead of its candidate value.
- 309 top-level `data` differences: every candidate formula cell in the top-level Report and Specifications arrays was replaced by its evaluated display value. No non-formula top-level cell differed. The duplicate formulas remained intact only in the worksheets' embedded `data` arrays.

Phase 4A.3 supplied the controlling interpretation for these saved-export differences. They are expected old-Sandbox serialization normalizations because the authoritative embedded worksheet model, actual array dimensions, all non-formula content, named definitions, styles, metadata, protection, and number formats remained exact and the workbook visibly saved and reopened.

The authoritative formula representation is `config.worksheets[*].data`. The duplicate top-level `data` representation is a QBench evaluated display cache. `minDimensions` is the QBench-normalized editor minimum, not actual content extent, and `tableWidth`/`tableHeight` are the normalized editor viewport.

`test_v2_round_trip = passed_with_expected_qbench_normalization`

No local candidate rewrite is required to reproduce these saved-export normalizations. No repair, second import, approval, activation, or runtime instantiation occurred during Phase 4A.2.
