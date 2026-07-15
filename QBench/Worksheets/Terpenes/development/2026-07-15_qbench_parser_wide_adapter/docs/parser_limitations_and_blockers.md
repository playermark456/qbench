# Parser limitations and blockers

## Blockers

`qbench_runtime_contract_status = insufficient_for_prompt_4_6`

`qbench_sandbox_probe_status = sufficient_to_begin_controlled_prompt_4_6_probe`

The current AIT `run`/`QB`/`QBBatchService` model and current imports are now
proven read-only. Official QBJS v2.7.0 documentation proves that
`updateWorksheet` completely replaces Batch worksheet data, so it is not
approved for the proposed Terpenes writer. `patchWorksheet` updates only fields
included in `data` and does not remove omitted data, making it the preferred
candidate for controlled Sandbox investigation.

The following patch questions remain:

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

## Resolved Batch-context decision

- The raw LabSolutions file will not include a QBench Batch ID.
- The user uploads the file while working inside the intended named QBench
  Batch.
- The parser must obtain the current Batch's internal numeric ID from supported
  runtime or attachment context.
- The parser must not infer the Batch from customer or sample data.
- The parser must not hardcode a Batch ID.
- The parser must not require the instrument export to contain a QBench Batch
  ID.

Sandbox discovery question: when a parser is triggered by a Batch attachment,
what supported runtime property or attachment context exposes the current
Batch's internal numeric ID?

## Scientific and release limitations

- Final LabSolutions `Conc.` unit confirmation remains required.
- Approved sample mass and final volume sources remain required.
- Dilution behavior is controlled only by explicit context.
- Below-LOQ, measurement uncertainty, COA rendering, METRC export, totals, final
  sample mg/g, final percent, and qualifiers remain outside Prompt 4.5.

## Scope controls

- No QBench object was changed.
- No Prompt 2, Prompt 3, or Prompt 4 file was modified.
- No COA/report source was modified.
- No automation was created or modified.
- No Test Worksheet, Publish, QC Review, METRC, or key/value-store write is
  performed automatically.
- Publish preview outputs AF, AG, and AV as exact text `"TRUE"`; this remains a
  local preview contract until native QBench write semantics are proven.
- Multi-file preview requires explicit source filenames and rejects invented
  placeholders.
- No paste-ready native QBench parser candidate is created while runtime
  contract evidence is missing.
- The Sandbox-probe readiness status permits only a future explicitly approved
  no-write runtime probe and disposable patch experiments; it does not
  authorize a final writer or production action.
- Sandbox validation records are not claimed unless tracked in the repository;
  the current manifest records Test Worksheet, Batch Worksheet, and end-to-end
  parser validation as `not_recorded_in_repository`.
- Prompt 4.6 was not started.
- Prompt 5 was not started.
