# Prompt 4.6C malformed normalized fixture results

Two deterministic exact-filename malformed fixtures were generated and passed
local structural validation:

| Fixture directory | Mutation | Expected worksheet-owned formula outcome |
| --- | --- | --- |
| `failure_fixtures/non_numeric_analyte/` | AH2 is literal text `NOT_NUMERIC` | AF2 `Rejected`; AG2 `Analytical values incomplete` |
| `failure_fixtures/missing_peak_count/` | Y2 is blank | AF2 `Rejected`; AG2 `Peak Table row count required` |

Each malformed fixture was uploaded to its own fresh disposable Batch using the
same isolated worksheet and exact-filename parser. Both File Parser History
entries reported `SUCCESS`; rejection was correctly owned by the worksheet
formulas rather than by parser-job failure.

Observed results:

- `non_numeric_analyte`: AH2 persisted as text `NOT_NUMERIC`; AF2 evaluated to
  `Rejected`; AG2 evaluated to `Analytical values incomplete`; the other 22
  analyte cells remained native numeric cells.
- `missing_peak_count`: Y2 persisted blank; AF2 evaluated to `Rejected`; AG2
  evaluated to `Peak Table row count required`; all 23 analyte cells remained
  native numeric cells.

For both runs, the expected result persisted after navigating away and
reopening the Batch. Row 3 remained blank, no spreadsheet error was present,
Publish remained blank, and no Test Worksheet, test association, or Pass/Fail
result was created.
