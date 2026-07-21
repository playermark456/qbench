# Phase 4A.6 validation report

Date: 2026-07-21

## Local V4 result

- Candidate: `production_candidates/SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v4.json`
- SHA-256: `53554a8dc167202da373e856df7c1905aab19d117353ec2899cc2de708447924`
- Renderer-sensitive namespace and worksheet identifiers: unchanged from V3
- Unexpected V3 differences after reversing the intended V4 changes: 0
- Embedded formulas: 309
- Five-argument Key/Value calls: 44
- LOQ / MU calls: 21 / 23
- Writable destinations: 43
- Named definitions: 44
- `report_results`: unchanged
- Scientific vectors: passed
- Production-candidate tests: 37 / 37 passed

## Cross-package validation

- Parser configuration tests: 27 / 27 passed
- Wide-adapter tests: 13 / 13 passed
- No-code parser fallback package: passed
- Native parser probe: 16 / 17 tests passed; its validator and one test remain blocked by a pre-existing controlled hash mismatch for the legacy July 14 Test worksheet dependency
- Prompt 5B publisher package: passed, including 115 generated-file hashes
- Publisher tests: 46 / 46 passed
- Prompt 5A route probe: passed
- Prompt 5 and the legacy Batch package: blocked by the same pre-existing July 14 dependency-hash mismatch; the historical dependency was not modified in this phase

## Sandbox result

The isolated V4 store was saved and reopened with the exact five-level semantic path terminating at field/value, no unit hierarchy, no `MU%` terminal, and no Pass/Fail key.

The isolated worksheet shell accepted exactly one native import submission. Its named-cell configuration populated, but the spreadsheet renderer remained collapsed to the default one-cell grid and did not show Report, Data, or Specifications. The prompt required an immediate stop on static-render failure.

No Draft version, round-trip export, approval, activation, store association, Assay, Sample, Test, representative lookup, runtime vector, analytical result, save/reopen, Report evaluation, COA preview, publication, completion, QC Review, METRC activity, Batch v2 activity, or Pass/Fail artifact followed.

V1, V2, and V3 objects and candidates remained unchanged.

Final classification: `test_v4_runtime_blocked_static_import_collapsed_renderer`
