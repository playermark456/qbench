# Phase 4A.3 formula results

## Saved-definition result

The semantic round-trip comparison passed with expected QBench normalization:

- authoritative formula representation: `config.worksheets[*].data`
- embedded formulas retained exactly: 309/309
- named definitions retained exactly: 44/44
- `report_results`: `Report!A1:E23`
- top-level formula duplicates: accepted as QBench evaluated display-cache values only when the corresponding embedded formula remains exact

## Runtime formula gate

The exact approved and active V2 worksheet retained the intended LOQ and MU guards. In substance, each lookup returns blank when either `Specifications!U2` or `Specifications!U4` is still `SANDBOX_CONFIGURATION_REQUIRED`; otherwise it evaluates the saved `GET_KVSTORE_VALUE(...)` formula.

After associating the isolated synthetic store:

- `Specifications!U2` remained the read-only store-binding sentinel.
- `Specifications!U4` remained the read-only matrix/product-type sentinel.
- Both cells are read-only in the local candidate and the saved round-trip export.
- Consequently, runtime LOQ/MU lookup results would be blank by design.

## Controlled result

The synthetic 43-field vector was not entered, so no actual direct conversion, component preprocessing, combined MU, LOQ-boundary, Total Terpenes, or display-rounding result was produced. Expected values are preserved separately for a future run after a supported binding mechanism is established.

Classification: `test_v2_runtime_blocked_readonly_kv_and_matrix_bindings`
