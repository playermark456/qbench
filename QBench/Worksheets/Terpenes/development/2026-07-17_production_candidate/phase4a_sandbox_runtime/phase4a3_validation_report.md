# Phase 4A.3 validation report

## Round-trip correction

`test_v2_round_trip = passed_with_expected_qbench_normalization`

The comparator treats `config.worksheets[*].data` as authoritative for formulas. It compares embedded data and formulas, substantive worksheet structure, named definitions, report range, and non-formula values exactly. It permits only the observed QBench-generated namespace, `[1,1]` editor minimums, positive editor viewport sizes, and top-level evaluated formula-cache values whose corresponding embedded formulas remain exact.

The observed round trip passes. A deliberately changed embedded formula fails. A changed non-formula top-level value also fails.

## Exact worksheet state

- Worksheet: `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS_V2`
- Version: `1 - Terpenes Production Candidate Test Worksheet v2`
- Status before Phase 4A.3 actions: Draft
- Status after required workflow: Approved and Active
- Tabs: 3
- Embedded formulas: 309
- Named definitions: 44
- `report_results`: `Report!A1:E23`
- Pass/Fail: absent
- Existing assay associations before status change: 0

The failed V1 shell and all other worksheets were left unchanged. The local V2 candidate was not modified.

## Isolated fixture and controlled blocker

The Sandbox-only fixture `SBX_ONLY_TERPENES_RUNTIME_KV_V2` was created with synthetic LOQ and MU values, saved, reloaded, and associated only with the exact V2 worksheet. No shared store was changed.

Association did not resolve the saved definition's read-only `Specifications!U2` store binding or read-only `Specifications!U4` matrix/product-type binding. Both remained `SANDBOX_CONFIGURATION_REQUIRED`, which makes the retained LOQ/MU formulas return blank. No supported visual workflow was available to supply those bindings without changing the worksheet definition, so the runtime gate failed before an Assay, Sample, or Test was created.

## Local validation

- Phase 4A.3 comparator against the saved round trip: passed
- Comparator tests: 3/3 passed
- Production-candidate test suite: 16/16 passed
- Phase 3 candidate validator: passed
- Phase 3 V2 package validator: passed
- Candidate JSON SHA-256: `7aa7469ec7767a7c7b4b0aa40194e927244adc3278999e23151f4eeb134dd5a4`
- Candidate JSON changed in Phase 4A.3: no

## Safety result

Only the authenticated visual Sandbox session was used. No live QBench page, QBench API, OAuth flow, customer record, shared Key/Value store, publication, QC Review, METRC action, or Pass/Fail artifact was used or created. Sanitized evidence contains no internal IDs, usernames, credentials, tokens, cookies, signed URLs, or screenshots.

Final classification: `test_v2_runtime_blocked_readonly_kv_and_matrix_bindings`
