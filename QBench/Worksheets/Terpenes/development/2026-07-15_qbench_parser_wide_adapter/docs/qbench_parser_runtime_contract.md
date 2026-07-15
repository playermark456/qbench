# QBench parser runtime contract

## Current contract state

`qbench_runtime_contract_status = insufficient_for_prompt_4_6`

Official QBench documentation and read-only AIT tenant inspection now prove the
base Code File Parser wrapper, selected-file access, logging/progress, completion
calls, current imports, and Batch service availability. The remaining targeted
Spreadsheet Worksheet destination, range, numeric, Batch-context, and
partial-write questions still block a native Terpenes wrapper. Prompt 4.6 and
Prompt 5 have not started.

## Version separation

| Evidence context | `file_parser.js` | `qbjs.js` |
|---|---:|---:|
| Official Introduction tutorial example | 1.0.0 | 1.0.0 |
| Current AIT parser 46 and visible parser 45 template | 1.1.0 | 2.7.0 |

The tutorial versions are documentation-example versions and are not treated
as current-tenant versions.

## Implemented local contract

The local parser core accepts:

- UTF-8 text or bytes, with or without BOM.
- LF or CRLF line endings.
- Prompt 2 analyte configuration.
- Controlled security limits.

The local wide adapter emits:

- One logical Instrument Import row per injection.
- Explicit source filename or name is required; invented filenames are rejected.
- 57 A:BE columns.
- QBench-neutral write blocks for A:AE and AH:BE.
- Explicit exclusion of AF and AG.
- JavaScript Number values for numeric fields.

The local reviewed Publish adapter emits:

- A D:AX preview patch only after row-specific review evidence keyed by
  `source_row_hash`.
- Review evidence must contain nonblank `source_row_hash` and exactly match the
  reviewed row.
- Exact `labsolutions_conc_unit === "ug/mL"` validation; blank, case-changed,
  or alternate units are blocked.
- Exact text `"TRUE"` output for Publish AF, AG, and AV.
- Explicit QBench Test ID to Publish-row mapping.
- Atomic multi-row preview behavior with no partial write plan.
- No AY or later formula/control writes.
- No direct Test Worksheet, Publish worksheet, QC Review, COA, METRC, or
  automation execution.

## Runtime blockers

The first two targeted live questions are resolved: the current AIT templates
use `file_parser.js` 1.1.0 with the documented `run`/`QB`/`QBBatchService` base
contract, and parser 46 imports `qbjs.js` 2.7.0. Only these targeted blockers
remain:

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

Until those are proven, `dist/terpenes_qbench_file_parser_candidate_v1.js` must
not be created.

## Runtime-contract evidence matrix

Rows 1-20 now record official documentation and current-tenant evidence. Rows
21-28 retain the sanitized result-history addendum from
`QBench/Rescans/2026-07-15/File_Parsers/file_parser_results_history_evidence.md`.
Detailed citations and limits are in `qbench_parser_api_evidence.md`.

| Row | Contract question | Status | Sanitized evidence | Runtime consequence |
|---:|---|---|---|---|
| 1 | File Parser technology | proven | Official documentation defines a File Parser as a custom JavaScript template saved in QBench. | JavaScript is the documented implementation language. |
| 2 | Execution wrapper | proven | The official tutorial uses `run(() => { ... })`; current parser 46 uses `run(async () => { ... })`; the visible parser 45 template uses `run(() => { ... })`. | The current tenant wrapper model is established. |
| 3 | Selected-file collection | proven | Official documentation defines `QB.files` as the selected-file array; both current templates reference `QB.files`. | The selected-file global is established for the current tenant. |
| 4 | Asynchronous text access | partially_proven | The official 1.0.0 tutorial uses `QB.files[n].text()`. Current parser 46 under 1.1.0 instead uses `FileReader.readAsText`/`readAsArrayBuffer`. | File/Blob access is corroborated, but direct `.text()` under the current runtime was not exercised. |
| 5 | Parser-visible logging | proven | Official documentation and both current templates use `QB.console`. | Controlled user-visible logging is available. |
| 6 | Progress reporting | proven | Official documentation and both current templates use `QB.progressBar`. | Progress reporting is available. |
| 7 | Successful completion | proven | Official documentation and both current templates use `QB.success()`. | The success completion call is established. |
| 8 | Failed completion | proven | Official documentation and both current templates use `QB.error()`. | The failure completion call is established; transactionality is separate. |
| 9 | Batch service | proven | Official documentation, QBJS v2.7.0, and parser 46 identify `QBBatchService`. | The Batch service class is available in the current tenant. |
| 10 | `updateWorksheet` parameter object | proven | The official tutorial and QBJS v2.7.0 document `batchId`, `worksheetData`, success, and error; v2.7.0 also documents optional `urlParams`. | The basic Batch worksheet method signature is documented. |
| 11 | Simple `worksheetData` value form | proven | The official tutorial maps worksheet field names to `{ value: supplied_value }`. | Simple field writes are documented; Spreadsheet named ranges and array payloads are not. |
| 12 | Attachment trigger | proven | Official documentation describes attachment triggers; parser 46 is configured for Batch attachments ending in `.csv`. | Attachment-triggered execution is established. |
| 13 | API-triggered attachment parsing | proven | The Introduction states that attachment-triggered parsing also works through API attachment upload. | API upload can initiate a configured parser trigger. |
| 14 | Official tutorial library versions | proven | The tutorial imports `file_parser.js` 1.0.0 and `qbjs.js` 1.0.0. | These are tutorial versions only and are not tenant-version claims. |
| 15 | Current AIT library versions | proven | Parser 46 and the visible parser 45 template import `file_parser.js` 1.1.0 and `qbjs.js` 2.7.0. | Current inspected tenant versions are established. |
| 16 | No-Code configuration model | proven | Official documentation lists Batch/Test targets and triggers; Equal/Start With/End With/Contain matching; Excel/CSV/TSV/custom delimiter. | Wide TSV to Batch Worksheet is a plausible configuration surface. |
| 17 | No-Code finder model | proven | Official documentation lists five finder types and same-position/Target Start Cell behavior for Cell Range. | Finder capabilities are documented. |
| 18 | Raw LabSolutions ASCII suitability | not_found | Official No-Code documentation covers spreadsheet-like delimited files, not the sectioned LabSolutions ASCII structure. | Direct raw-file use must not be claimed without testing. |
| 19 | Batch-to-Test automation architecture | proven | Official documentation shows Batch Data Modified, all Test Worksheets in Batch, named destination field, Batch Worksheet source, and `VLOOKUP({{test.id}}, ...)`. | Supports future Prompt 5 architecture only; Prompt 5 has not started. |
| 20 | Attachment API contract | proven | Official documentation covers BATCH/TEST association, list retrieval, creation, and temporary retrieval URLs. | Attachment automation is documented; temporary URLs must not be persisted. |
| 21 | Result-history invocation model | partially_proven | All 39 jobs used trigger `Attachment Added To Batch`. Inspected success details showed one attachment each, and two Code-parser jobs used the same sanitized filename pattern as separate jobs. | Per-attachment or per-file invocation is corroborated for the inspected single-file cases. Multi-file upload-group behavior and the native input object remain unproven. |
| 22 | Result-history status model | partially_proven | Complete visible history contained 38 `SUCCESS` and one `IN_PROGRESS` job; no failed job was present. | Only the two observed labels are corroborated. Failure, cancellation, timeout, and terminal-state semantics remain unproven. |
| 23 | Result-history error format | not_found | No failed record existed. Success details exposed a user-facing success message but no error code or error structure. | The native error-reporting API and user-facing failure format remain blocked. |
| 24 | Result-history destination association | partially_proven | History displayed Data Target `None` for parser 46 and `Batch Worksheet` for parsers 47 and 41. Exact worksheet names, ranges, and parser mappings were not displayed. | Destination type association is corroborated; worksheet/range write APIs and mappings remain unproven. |
| 25 | Result-history logging behavior | not_found | Inspected detail modals had a user-facing Message field but no log link, log panel, parsed-output preview, or worksheet-write summary. | Log availability, structure, retention, and diagnostic detail remain unproven. |
| 26 | Failure partial-write evidence | not_found | No failed result was present in the complete 39-job history. | No record-scoped partial-write observation can be made, and no transaction guarantee is implied. |
| 27 | Successful numeric-write evidence | not_inspected_due_to_production_data_boundary | Inspected successes exposed no numeric preview or write summary. No underlying Batch Worksheet was opened because no linked destination record was confirmed as a synthetic or redacted fixture. | JavaScript Number preservation and successful numeric worksheet-write semantics remain unproven. |
| 28 | Retry/reprocess behavior | not_found | No Retry, Rerun, Reprocess, or Run Again control was visible in the history list or inspected detail modals. No such action was invoked. | Retry availability, idempotency, reprocessing semantics, and duplicate-write behavior remain unproven. |
