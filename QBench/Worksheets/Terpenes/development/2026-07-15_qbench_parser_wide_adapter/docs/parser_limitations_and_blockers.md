# Parser limitations and blockers

## Blockers

- Exact QBench Code File Parser runtime contract is not proven.
- QBench write transactionality or dry-run behavior is not proven.
- QBench JavaScript Number preservation during worksheet writes is not proven.
- Safe range-targeted writes to Instrument Import A:AE and AH:BE are not proven.

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
- No paste-ready native QBench parser candidate is created while runtime
  contract evidence is missing.
- Sandbox validation records are not claimed unless tracked in the repository;
  the current manifest records Test Worksheet, Batch Worksheet, and end-to-end
  parser validation as `not_recorded_in_repository`.
- Prompt 5 was not started.
