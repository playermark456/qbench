# Runtime export results

Status: **`runtime_test_worksheet_contract=passed_43_of_43`**.

QBench's Test Worksheet `Export Data to CSV` action produced the raw runtime
export. The unchanged raw file is preserved locally as:

`SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_RUNTIME_TEST_WORKSHEET_export_data.csv`

SHA-256:
`f7c702dd3ecac694c32b3aa686cca6cd4928198b7bda45f4d8e030e65d681bfe`.

The raw file necessarily contains Sandbox runtime identifiers and is ignored;
`runtime_export_sanitized.csv` is the tracked copy with those identifiers and
non-contract metadata removed.

Semantic comparison combined the reopened 40x26 grid with the export's exact
43 destination display columns and the already-proven Approved/Active
definition. Result:

- Data grid: 40x26
- anchors: 28/28
- destination columns: 43/43, exact and unique
- destination values: 43/43 blank
- address contract: unchanged from the Approved/Active definition
- writable, non-formula, exportable contract: 43/43
- prohibited fields: none

Only expected runtime metadata and identifiers were excluded from the tracked
sanitized copy.
