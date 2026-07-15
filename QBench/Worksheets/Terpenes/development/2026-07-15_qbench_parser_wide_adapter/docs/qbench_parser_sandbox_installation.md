# QBench parser Sandbox installation

## Current status

`qbench_runtime_contract_status = insufficient_for_prompt_4_6`

`qbench_native_status = blocked_missing_targeted_qbench_runtime_contract`

Do not create, paste, save, activate, run, or assign a Terpenes QBench Code File
Parser from this package yet.

## Complete locally

- Pure JavaScript LabSolutions parser core.
- Wide Instrument Import row adapter.
- Reviewed Publish preview adapter.
- Deterministic JSON and TSV fixtures.
- Security limits and local tests.
- QBench wrapper template with explicit integration blockers.

The distribution intentionally omits
`dist/terpenes_qbench_file_parser_candidate_v1.js` until the runtime contract is
proved.

## Missing evidence

The base wrapper and current AIT imports are proven. Only these targeted
questions remain:

1. Does `QBBatchService.updateWorksheet` support Spreadsheet Worksheet named
   cells and named ranges?
2. Can `worksheetData` values contain a one-dimensional or two-dimensional
   array for a named spreadsheet range?
3. Can one update request safely write the two noncontiguous blocks
   `Instrument Import!A:AE` and `Instrument Import!AH:BE` while leaving AF/AG
   untouched?
4. When triggered by a Batch attachment, how is the triggering Batch ID exposed
   to the Code parser?
5. Are JavaScript Number values written as actual numeric Spreadsheet Worksheet
   cells recognized by `ISNUMBER` and `COUNT`?
6. Is `updateWorksheet` transactional, staged, or capable of partial field
   updates after an error?
7. Is there a dry-run, preview, or disposable Sandbox testing method?

## Next evidence step

Obtain authoritative answers to the targeted support questions in
`qbench_prompt_4_6_support_request.md`. Do not update the wrapper, create a
candidate, or begin Prompt 4.6 until the remaining contract is sufficient.
