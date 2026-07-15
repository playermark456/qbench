# QBench File Parser Results History Evidence

## Scope and safety boundary

Read-only inspection was performed on 2026-07-15 in the AIT QBench Sandbox
File Parser History and parser metadata pages. No QBench object was changed.
No Retry, Rerun, Reprocess, Run Again, Delete, Approve, Release, raw-file
download, Save, or other mutation control was invoked.

The inspection did not open any customer, order, sample, test, batch-result,
certificate, or underlying Batch Worksheet record. Raw attachments were not
downloaded. Job IDs, attachment IDs, creator names, and any other record
identifiers were omitted and replaced with controlled labels.

Results history is treated only as supporting runtime evidence. It does not
prove or supply a JavaScript entry-point name, function signature, input object
shape, output API, worksheet-write API, transaction guarantee, or numeric-write
semantics.

## Aggregate history inventory

Both available history pages were inspected. The visible inventory contained
39 jobs:

| Visible characteristic | Count |
|---|---:|
| `SUCCESS` | 38 |
| `IN_PROGRESS` | 1 |
| Failed status | 0 |
| Cannabinoid Potency Parser (ID 46) | 3 |
| Pest Myco Qualitative (ID 47) | 9 |
| Heavy Metals DataManager (ID 41) | 27 |
| Data Target `None` | 3 |
| Data Target `Batch Worksheet` | 36 |
| Trigger `Attachment Added To Batch` | 39 |

No history job was present for inactive Code parser Gene-up (ID 45). Its
read-only Details page showed Editor Type `Code`, inactive status, and its
Versions tab showed `No Versions Found`.

## Sanitized record evidence

### SUCCESS-RECORD-1

- Parser: ID 46, Cannabinoid Potency Parser.
- Parser type: Code.
- Parser version: not displayed in the history job. The parser Versions tab
  showed one approved version, version 1, active since 2026-07-10.
- Result status: `SUCCESS`.
- Execution date/time: 2026-07-15 08:33 AM; created and completed in the same
  displayed minute.
- Input: one visible attachment; sanitized filename `Output.csv`; extension
  `.csv`.
- Invocation model: appears to be per attachment or per file for this
  single-file case. Upload-group behavior is not proven.
- Destination object type: `None` in the history list and no destination field
  in this detail modal.
- Output-row or field count: not visible.
- User-facing error: not applicable to this success; no error code or error
  format was visible.
- Logs: no log link or log panel was visible. A separate log facility was not
  established.
- Parsed-output preview: not visible.
- Worksheet-write summary: not visible.
- Partial output after failure: not applicable; this was a success record.
- Retry/reprocess controls: not visible.
- Numeric destination values: not confirmed. No destination record was opened.
- Evidence source: QBench Sandbox File Parser History page 1, sanitized job
  detail modal, and parser 46 Details/Versions tabs.
- Confidence: medium-high for visible history fields; medium for version
  correlation because the history job did not display a version.
- Data sensitivity: Sandbox history metadata only; underlying data sensitivity
  was not verified; raw file not opened or downloaded.

### REPEATED-FILE-RECORD-1

- Parser: ID 46, Cannabinoid Potency Parser; Code.
- Parser version: not displayed in the history job; version 1 was the only
  approved version visible and was active on the job date.
- Result status: `SUCCESS`.
- Execution date/time: 2026-07-15 08:27 AM; created and completed in the same
  displayed minute.
- Input: one visible attachment; sanitized filename `Output.csv`; extension
  `.csv`.
- Repeated-file evidence: SUCCESS-RECORD-1 and this record used the same
  sanitized filename pattern in separate jobs six minutes apart.
- Invocation model: the repeated uploads were represented as separate jobs,
  corroborating per-attachment or per-file invocation for these single-file
  cases. Multi-file upload-group behavior remains unproven.
- Destination object type: `None`.
- Destination mapping, output summary, logs, preview, worksheet-write summary,
  retry controls, and numeric values: not visible.
- Evidence source: QBench Sandbox File Parser History page 1 and sanitized job
  detail modal.
- Confidence: medium-high for repetition and visible fields; not sufficient to
  generalize all invocation behavior.
- Data sensitivity: Sandbox history metadata only; raw files not opened or
  downloaded.

### VERSION-ADJACENT-RECORD-1

- Parser: ID 46, Cannabinoid Potency Parser; Code.
- Result status: `IN_PROGRESS`.
- Execution date/time: 2026-07-10 08:45 AM as displayed for both created and
  completed columns.
- Parser version: not displayed on the history record. Parser version 1 was
  shown as active since 2026-07-10, the same date as this job.
- Version-change association: temporal adjacency only. The evidence does not
  prove which parser version executed this job or the exact activation time.
- Input file count and extension: not confirmed from an available detail
  surface.
- Trigger: `Attachment Added To Batch`.
- Destination object type: `None`.
- Logs, error format, output preview, worksheet-write summary, retry controls,
  partial output, and numeric writes: not visible.
- Evidence source: QBench Sandbox File Parser History page 1 and parser 46
  Versions tab.
- Confidence: medium-low because the version association is inferred only from
  the shared date.
- Data sensitivity: aggregate Sandbox metadata only; no underlying record or
  attachment opened.

### FAILURE-RECORD-NOT-FOUND

No failed result was present in the complete 39-job history. Therefore no
user-facing failure error format, failure logging behavior, retry behavior, or
failure partial-write behavior could be inspected. No statement about
transactionality can be made.

### CODE-PARSER-NO-HISTORY-1

Gene-up (parser ID 45) was verified as an inactive Code parser with no parser
versions and no job in the complete visible history. Success, failure,
multi-file/repeated-file, destination, and version-change history evidence were
not available for this parser.

### NOCODE-SUCCESS-RECORD-1

- Parser: ID 47, Pest Myco Qualitative.
- Parser type: QBench Editor Type `Standard`, documented here as No-Code.
- Parser version: not applicable; no Code-parser Versions tab was present.
- Result status: `SUCCESS`.
- Execution date/time: created 2026-07-02 08:44 AM; completed 08:45 AM.
- Input: one attachment; sanitized filename pattern `YYYYMMDD.csv`; extension
  `.csv`.
- Invocation model: appears per attachment or per file for this single-file
  case.
- Destination object type: `Batch Worksheet`; the exact worksheet or mapping
  was not visible in history.
- User-facing message: a success message associated the job with the parser and
  attachment. Identifiers were omitted.
- Logs, parsed-output preview, worksheet-write summary, retry controls, and
  numeric destination values: not visible.
- Evidence source: QBench Sandbox File Parser History page 1, sanitized job
  detail modal, and parser 47 Details page.
- Confidence: medium-high for visible status/destination fields.
- Data sensitivity: Sandbox history metadata only; underlying Batch Worksheet
  and raw file not opened.

### NOCODE-SYNTHETIC-RECORD-1

- Parser: ID 41, Heavy Metals DataManager.
- Parser type: QBench Editor Type `Standard`, documented here as No-Code.
- Parser version: not applicable; no Code-parser Versions tab was present.
- Result status: `SUCCESS`.
- Execution date/time: created and completed 2026-05-27 01:38 PM.
- Input: one attachment; sanitized filename `test.txt`; extension `.txt`.
- Invocation model: appears per attachment or per file for this single-file
  case.
- Destination object type: `Batch Worksheet`; the exact worksheet or mapping
  was not visible in history.
- User-facing message: a success message associated the job with the parser and
  attachment. Identifiers were omitted.
- Logs, parsed-output preview, worksheet-write summary, retry controls, and
  numeric destination values: not visible.
- Evidence source: QBench Sandbox File Parser History page 1, sanitized job
  detail modal, and parser 41 Details page.
- Confidence: medium-high for visible status/destination fields; medium for the
  synthetic classification because it is inferred only from `test.txt`.
- Data sensitivity: likely synthetic Sandbox fixture metadata; underlying Batch
  Worksheet and raw file not opened.

## Runtime interpretation limits

- The history corroborates the visible trigger label `Attachment Added To
  Batch` and single-attachment job behavior.
- It corroborates the observed status labels `SUCCESS` and `IN_PROGRESS` only.
- It corroborates that history can associate a job with Data Target `None` or
  `Batch Worksheet`.
- It does not expose a parsed-output preview, worksheet-write summary, logs,
  numeric destination values, or retry/reprocess controls in the inspected
  records.
- It does not prove that a success status means every intended field was
  written, or that numeric values retained JavaScript Number semantics.
- It does not prove that failures are transactional. No failed record was
  available, so even the record-scoped phrase `no partial write observed in the
  inspected record` is not applicable here.
- It must not be used to invent an undocumented parser entry point, function
  signature, file API, return API, or worksheet-write API.
