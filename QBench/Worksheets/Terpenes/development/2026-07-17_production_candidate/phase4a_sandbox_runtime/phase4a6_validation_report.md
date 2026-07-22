# Phase 4A.6 validation report

Date: 2026-07-21

## Local V4 contract

- Candidate: `production_candidates/SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v4.json`
- SHA-256: `53554a8dc167202da373e856df7c1905aab19d117353ec2899cc2de708447924`
- Candidate modified during Phase 4A.6B: no
- Unexpected V3 differences after reversing intended V4 changes: 0
- Embedded formulas: 309
- Five-argument Key/Value calls: 44
- LOQ / MU calls: 21 / 23
- Writable destinations: 43
- Named definitions: 44
- `report_results`: `Report!A1:E23`
- Pass/Fail: absent

## Corrected static-render classification

The unchanged JSON produced different results based only on QBench worksheet object type:

- Regular Spreadsheet negative control: named definitions loaded, workbook collapsed to the one-cell fallback.
- Dynamic Spreadsheet: complete Report, Data, and Specifications workbook rendered.

The regular Spreadsheet event remains preserved as negative-control evidence. The V4 JSON, five-argument lookup formulas, Key/Value Store, named definitions, styles, formulas, and dimensions are not classified as the cause of that collapse.

`v4_regular_spreadsheet_control = failed_expected_object_type_mismatch`

`v4_dynamic_spreadsheet_static_render = passed`

`v4_static_failure_root_cause = qbench_object_type_mismatch`

## Saved definition and round trip

- Dynamic object: `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS_V4_DYNAMIC`
- Existing object reused: no; the refreshed Worksheets list contained no suitable V4 Dynamic Spreadsheet
- New Dynamic Spreadsheet shell created: yes, exactly one
- Native file selection and import submission: performed manually by the user
- Codex static verification: passed
- Version count: 1
- Version: `Terpenes Production Candidate Test Worksheet v4 Dynamic`
- Version status: directly approved and active
- Review lock: not created
- Worksheet object: Active
- Worksheet type after reopen: Dynamic Spreadsheet
- Raw ignored export SHA-256: `3db41897b9d9fa8f134458c0dce66fdac097f0c9aca67474520feffae2cbfff1`
- Round-trip comparator: passed with only expected QBench normalization

The comparator preserved exact embedded formulas, worksheet data, non-formula content, tab order, dimensions, rows, columns, styles, metadata, number formats, protection, named definitions, `report_results`, and Key/Value formulas. Permitted normalization was three minimum-dimension resets, six positive viewport values, and 309 evaluated top-level formula-cache cells.

## Isolated runtime setup

- Isolated V4 store association: saved and persisted after reopen
- Regular Spreadsheet negative control association: none
- Fresh Assay: `SBX_ONLY_TERPENES_RUNTIME_ASSAY_V4_DYNAMIC`
- Assay Test Worksheet: only the verified V4 Dynamic Spreadsheet
- Assay Batch Worksheet / protocols / portal visibility: unset or disabled
- Assay save/reopen: passed
- Fresh Sample: `SBX_ONLY_TERPENES_RUNTIME_SAMPLE_V4_DYNAMIC`
- Sample type: Cannabis/Hemp
- Product matrix: Cannabis Concentrates
- Fresh Test count: 1
- Test state: NOT STARTED
- Test worksheet tabs: Report, Data, Specifications

## Runtime lookup gate

- `Data!C2`: Cannabis Concentrates
- `Specifications!U3`: Terpenes
- `Specifications!U4`: Cannabis Concentrates
- Alpha-Pinene LOQ: blank
- Alpha-Pinene MU: blank
- Permitted list-based Test reopen count: 1
- Alpha-Pinene LOQ and MU after reopen: blank
- Ocimene and Nerolidol lookup checks: not evaluated after the first required lookup failed

The 43-field vector was not entered. No destination or formula cell was changed; no value was hardcoded. Total Terpenes, display values, input types, formula results, final Test save/reopen, and COA preview were not run.

## Deployment guard

`terpenes_deployment_contract.json` separates the locally passed JSON contract from the required Dynamic Spreadsheet shell and the currently blocked Sandbox runtime contract. Both Test and Batch worksheet deployment entries require `dynamic_spreadsheet`, and the guard explicitly rejects `spreadsheet`. Future import work must first verify the Worksheets list visibly reports **Dynamic Spreadsheet**.

## Safety result

The regular Spreadsheet negative control, V1, V2, V3, shared stores, operational stores, and all existing runtime fixtures remained unchanged. No Pass/Fail, automatic Publish, QC Review, METRC action, Batch v2 work, cleanup, completion, publication, release, OAuth, QBench API call, live-QBench access, tracked raw export, screenshot, username, internal identifier, token, credential, cookie, or signed URL was introduced.

## Local validation

- V4 candidate validator: passed
- Accepted semantic round-trip comparator: `passed_with_expected_qbench_normalization`
- Production-candidate tests: 39/39 passed
- Candidate SHA-256 preservation: passed
- JSON and CSV parse validation: passed
- Sanitized tracked-evidence security scans: passed
- Git whitespace checks: passed

Final classification: `test_v4_dynamic_runtime_blocked_required_kv_lookup_blank`
