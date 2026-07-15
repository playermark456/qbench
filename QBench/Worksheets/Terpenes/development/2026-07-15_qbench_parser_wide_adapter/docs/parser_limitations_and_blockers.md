# Parser limitations and blockers

## Blockers

`qbench_runtime_contract_status = insufficient_for_prompt_4_6`

The current AIT `run`/`QB`/`QBBatchService` model and current imports are now
proven read-only. Only these targeted blockers remain:

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
- Sandbox validation records are not claimed unless tracked in the repository;
  the current manifest records Test Worksheet, Batch Worksheet, and end-to-end
  parser validation as `not_recorded_in_repository`.
- Prompt 5 was not started.
