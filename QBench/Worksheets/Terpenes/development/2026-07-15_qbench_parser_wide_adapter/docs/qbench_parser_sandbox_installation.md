# QBench parser Sandbox installation

## Current status

`qbench_runtime_contract_status = insufficient_for_prompt_4_6`

`qbench_sandbox_probe_status = sufficient_to_begin_controlled_prompt_4_6_probe`

`qbench_native_status = blocked_missing_targeted_qbench_runtime_contract`

This evidence-only update does not authorize creating, pasting, saving,
activating, running, or assigning a Terpenes QBench Code File Parser. A future
explicitly approved Prompt 4.6 effort may begin with a no-write runtime probe
and disposable scalar/range patch experiments only. It may not begin with the
final writer or any production action.

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

The base wrapper and current AIT imports are proven. `updateWorksheet` is not a
candidate because its documented behavior completely replaces Batch worksheet
data. `patchWorksheet` preserves omitted data and is the preferred candidate
for these remaining questions:

1. Does `QBBatchService.patchWorksheet` support Spreadsheet Worksheet named
   cells and named ranges?
2. Can `patchWorksheet` `data` values contain a one-dimensional or
   two-dimensional array for a spreadsheet named range?
3. Can one patch operation or two sequential patch operations safely update
   `Instrument Import!A:AE` and `Instrument Import!AH:BE` while preserving
   AF/AG and all omitted worksheet content?
4. Are JavaScript Number values patched as numeric Spreadsheet Worksheet
   cells recognized by `ISNUMBER` and `COUNT`?
5. Are `patchWorksheet` calls transactional, atomic per request, or capable of
   partial field updates?
6. What failure or rollback behavior applies when the second of two patch
   operations fails?
7. Is there a supported dry-run, preview, or disposable Sandbox debugging
   workflow?

The raw LabSolutions file will not contain a QBench Batch ID. The supported
runtime property or attachment context that exposes the current Batch's
internal numeric ID remains a Sandbox discovery question.

## Next evidence step

After Prompt 4.6 is explicitly authorized, use a no-write context probe before
any disposable scalar/range patch experiment. Keep
`qbench_prompt_4_6_support_request.md` as a fallback for questions that remain
unresolved after those Sandbox experiments. Do not update the final wrapper or
create a final candidate until the native-writer contract is sufficient.
