# Phase 4A.4 local V3 validation

## Candidate

- Path: `production_candidates/SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v3.json`
- SHA-256: `b68f0e1589ba4e2f5c3c85196c648ed5238a1700b02d8feca3e20850ede19014`
- Renderer-proven V2 SHA-256: `7aa7469ec7767a7c7b4b0aa40194e927244adc3278999e23151f4eeb134dd5a4`
- V2 modified: no

## Build profile

`sandbox_runtime_profile_v3.json` contains only the visually proven non-secret Sandbox store binding, assay key, dynamic Test matrix placeholder and source cell, matrix binding mode, and result unit. The builder rejects blank or unresolved bindings and rejects a fixed one-matrix source.

V3 uses:

- `Specifications!U2`: visually proven Sandbox association UUID
- `Specifications!U3`: `Terpenes`
- `Specifications!U4`: `${test.sample.product_matrix}`
- `Specifications!U5`: `ug/g`

The 44 Key/Value lookup formula cells retain all 44 `GET_KVSTORE_VALUE` calls. Their obsolete sentinel comparison was replaced with a fail-closed blank-binding guard. Total embedded formula count remains 309, matching V2.

## Contract results

- `renderer_contract = passed`
- `calculation_contract = passed`
- `runtime_configuration_contract = passed`
- JSON syntax: passed
- Tabs and order: Report, Data, Specifications
- Embedded formulas: 309, equal to V2
- Key/Value lookup formula cells/calls: 44/44
- Exact writable destinations: 43/43, unchanged from V2
- Named definitions: 44/44
- `report_results`: `Report!A1:E23`
- Unresolved configuration markers: 0
- Hardcoded LOQ or MU values: none
- Pass/Fail: absent
- Automatic Publish/QC Review: absent
- Phase 4A.4 configuration tests: 10/10 passed
- Full production-candidate tests: 26/26 passed
- Phase 3 V2 scientific/schema/renderer package validation: passed

The candidate passed all local gates before the Sandbox load attempt.
