# Sandbox controlled-success results

Prompt 5A qualification: QBench documentation later supplied the per-Test
`VLOOKUP({{test.id}}, ...)` source pattern. Its isolated follow-up did not yield
a valid routing result because the destination named cell was absent from the
saved worksheet version. This file remains the historical record of the
original Prompt 5 no-activation decision.

Result: **not run; safely blocked before activation**.

The required success run needs one reviewed Batch row to resolve to exactly one
Test and needs the complete destination contract validated before any write.
At the time of this original stop, the UI-only inspection had not revealed a
per-Test source expression or a cardinality guard, so the success run was not
considered controlled.

## Observed safe result

- Automation created with the required unique name.
- Trigger saved as `Data Modified` on `Batch`.
- Automation remained inactive.
- No conditions or actions were saved.
- No Prompt 5 Batch, Sample, Test, Batch Worksheet, or Test Worksheet was
  created.
- No Test Worksheet received a value.
- No formula or read-only field was touched.
- No spreadsheet error was introduced.
- No Terpenes Pass/Fail or final sample outcome was created.

## Not claimed

The following Prompt 5 results are not claimed:

- parser upload and pre-authorization no-write observation on a fresh Prompt 5
  Batch;
- 23 native numeric Test Worksheet inputs;
- Test Worksheet calculation update;
- formula preservation after a publish;
- navigate-away/reopen persistence;
- three-Test row correspondence;
- COA/report preview.

Prompt 4.6C established the canonical normalized-input behavior in a different
disposable Batch. That repository evidence was reviewed but was not reused as a
Prompt 5 publishing target or relabeled as a Prompt 5 success result.
