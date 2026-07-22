# Phase 4A.6F conditional component-MU runtime validation

Date: 2026-07-21

Environment: QBench Sandbox through the authenticated visual browser only.

## Corrected expectation

- `component_mu_preentry_blank = expected_conditional_lookup_behavior`
- Blank, zero, and negative raw components produce a zero used concentration.
- A zero used concentration intentionally produces a blank component MU.
- A positive used concentration requires its Key/Value MU lookup.
- A positive component with a missing MU produces `MU UNRESOLVED`; no numeric MU is fabricated.

The historical controlled stop is preserved and reclassified:

- `previous_component_mu_blank_stop = superseded_invalid_preentry_expectation`
- `former_final_classification = superseded_by_fresh_version_2_runtime_evidence`

## Existing Test provenance and pre-entry gate

- Runtime alias: `SANDBOX_TEST_V4_BINDING_FIX_A`
- Prior lifecycle control: `SANDBOX_TEST_PRE_VERSION_2_CONTROL`, left unchanged.
- Exact Dynamic Spreadsheet object: `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS_V4_DYNAMIC`.
- Version 2 was visibly approved and active for newly instantiated Tests; Version 1 remained preserved and no Version 3 existed.
- Report, Data, and Specifications tabs were present.
- Matrix: Cannabis Concentrates.
- Exact V4 store binding: matched the corrected candidate without recording the internal identifier.
- Alpha-Pinene LOQ/MU: 10 / 5.
- Ocimene LOQ: 10.
- Nerolidol LOQ: 10.
- All four component MU cells were blank before entry because all four used values were zero.
- `preentry_lookup_gate = passed`

## Staged component probe

| Measurand | Raw components (ug/g) | Used components (ug/g) | Component MUs (%) | Combined result (ug/g) | Combined MU (%) | Display MU (%) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Ocimene | 3.25 / 9.75 | 3.25 / 9.75 | 4 / 8 | 13 | 6.082762530298 | 6.083 |
| Nerolidol | 12.5 / -2.5 | 12.5 / 0 | 7 / blank | 12.5 | 7 | 7.000 |

- `conditional_component_mu_lookup = passed`
- `positive_component_mu_runtime_lookup = passed`
- `noncontributing_component_mu_blank = expected`

## Complete vector and persisted types

- Exact destinations entered: 43/43.
- Saved and list-reopened values: 43/43 exact.
- Exported destination types: 25 numbers, 1 blank, 17 text.
- All 23 analytical destinations except the intentional blank remained native numeric values.
- Numeric zero and negative inputs remained numeric.
- The intentional Delta-3 Carene destination remained blank.
- QBench defines the compatibility confirmation destinations as text cells, so `true` and `false` persisted as lowercase text; `publish_ready` remained `false`.
- No formula cell or unrelated cell was populated.

## Expected versus actual calculations

- Alpha-Pinene: 0.0151234 mg/g; 0.00151234%; display 0.015 mg/g and 0.002%; MU 5.000%.
- Camphene: `<LOQ`; Total Terpenes contribution zero.
- Beta-Myrcene: numeric at the LOQ boundary; Total Terpenes contribution zero because the total requires strictly greater than LOQ.
- Beta-Pinene: 0.0205678 mg/g; 0.00205678%; display 0.021 mg/g and 0.002%; included in the total.
- Delta-3 Carene: blank and excluded.
- Alpha-Terpinene: numeric zero internally; display `<LOQ`; excluded.
- P-Isopropyltoluene (P-Cymene): raw -1.5 preserved; display `<LOQ`; no negative potency; excluded.
- Ocimene: 0.013 mg/g; 0.0013%; reported once.
- Nerolidol: 0.0125 mg/g; 0.00125%; reported once.
- Total Terpenes: 204.7801 ug/g; 0.2047801 mg/g; 0.02047801%; display 0.205 mg/g and 0.020%.

## Report and reopen proof

- Report contained 21 reportable analytes plus Total Terpenes in `Report!A1:E23`.
- Ocimene and Nerolidol appeared once each.
- Raw component rows, Dimethylacetamide, Peak Table values, negative potency, and Pass/Fail were absent.
- All values, conditional MUs, calculations, and Report output remained correct after the normal nonfinal save and list-based reopen.

## Raw ignored export and preview

- Ignored raw export filename: `phase4a6f_SANDBOX_TEST_V4_BINDING_FIX_A_runtime_export.xlsx`
- SHA-256: `c85ef6bd0d9f37ada17ce2b7ea827b5c565a95e51661312bf4a557b556490dfc`
- Workbook contract: Report 23x5, Data 40x26, Specifications 23x21, 309 formulas.
- Blank standalone custom-function caches are not a QBench runtime failure gate; the saved and reopened live Test is authoritative.
- The explicit preview-only report workflow was attempted with no signature. QBench returned a generic preview-generation error. No report was saved, published, or released.

## Local validation

- Conditional component-MU regression tests: 8/8 passed.
- Complete production-candidate tests: 51/51 passed.
- V4 candidate validator: passed; 43 destinations, 309 formulas, 44 five-argument Key/Value lookups.
- Binding-fix delta validator: `passed_exact_store_binding_only`.
- Saved Version 2 semantic comparator: `passed_with_expected_qbench_normalization`.
- Scientific-logic, worksheet-schema, and historical-renderer package validator: passed.
- JSON and CSV validation: passed.
- Changed-file credential, token, assertion, binding UUID, username/email, numeric QBench-ID, signed-URL, customer/sample-data, and live-origin scans: zero findings.

## Remaining hardening and final classification

- `store_binding_cell_protection = runtime_validated_but_final_hardening_required`
- Batch v2 validation was not started.
- `test_v4_binding_fix_runtime_passed_ready_for_coa_and_batch_v2_validation`
