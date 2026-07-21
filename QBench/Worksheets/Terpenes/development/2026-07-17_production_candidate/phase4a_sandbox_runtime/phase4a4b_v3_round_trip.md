# Phase 4A.4B Test v3 saved-definition round trip

Date: 2026-07-21

## Inputs

- Local V3 candidate SHA-256: `b68f0e1589ba4e2f5c3c85196c648ed5238a1700b02d8feca3e20850ede19014`
- Raw saved/reopened Export Spreadsheet filename: `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS_V3__saved_reopened_export_spreadsheet.json`
- Raw export SHA-256: `729a35c78deb03e6fa8e5032ed30e02f412d4c6854a828e57d52d4a006d87b2f`
- Raw export tracking state: ignored and uncommitted

The visual export action produced two byte-identical downloads while the browser's download event timed out. Both had the same 188,281-byte length and SHA-256. One unchanged copy was preserved as the ignored raw evidence file; no second export was treated as a distinct proof artifact.

## Authoritative comparison

| Contract element | Result |
| --- | --- |
| Worksheet count and order | exact: Report, Data, Specifications |
| Actual data-array dimensions | exact: 23x5, 40x26, 23x21 |
| Embedded worksheet data | exact |
| Embedded formulas | exact: 309 of 309 |
| Non-formula top-level values | exact: 1,329 compared |
| Named definitions | exact: 44 |
| Writable destination contract | exact: 43 |
| `report_results` | exact: `Report!A1:E23` |
| Rows, columns, cells, styles, protection, and number formats | exact |
| Key/Value formulas in embedded worksheet data | exact |

## Accepted QBench normalization

- Generated namespace differed and was ignored as non-semantic.
- All three `minDimensions` values normalized to the editor minimum.
- Six viewport fields normalized.
- The top-level duplicate formula cache contained 309 evaluated display values while all corresponding formulas remained exact in `config.worksheets[*].data`.

`test_v3_round_trip = passed_with_expected_qbench_normalization`
