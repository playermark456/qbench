# QBench support request: Prompt 4.6 runtime contract

Date prepared: 2026-07-15

`qbench_runtime_contract_status = insufficient_for_prompt_4_6`

`qbench_sandbox_probe_status = sufficient_to_begin_controlled_prompt_4_6_probe`

## Purpose

Fallback request for authoritative clarification after controlled Prompt 4.6
Sandbox probes and disposable patch experiments leave questions unresolved.
Do not send this request yet. It does not authorize a production change, parser
creation, parser run, or the start of Prompt 4.6 or Prompt 5.

## Documentation already reviewed

- [Introduction to File Parsers](https://junctionconcepts.zendesk.com/hc/en-us/articles/4409122738701-Introduction-to-File-Parsers)
- [QBJS v2.7.0 QBBatchService](https://qbjs.docs.qbench.net/v2.7.0/QBBatchService.html)
- [No-Code File Parsers](https://junctionconcepts.zendesk.com/hc/en-us/articles/9147024166797-No-Code-File-Parsers)
- [Batch Spreadsheet Worksheets & Automations](https://junctionconcepts.zendesk.com/hc/en-us/articles/9705726121229-Batch-Spreadsheet-Worksheets-Automations)
- [API - Attachments](https://junctionconcepts.zendesk.com/hc/en-us/articles/360044230052-API-Attachments)

No authorization value, signed attachment URL, customer identifier, sample
identifier, Test ID, Batch ID, or result value is included in this request.

## Resolved by current-tenant read-only evidence

1. The current AIT tenant uses the documented `run`/`QB`/`QBBatchService` base
   contract with `file_parser.js` 1.1.0.
2. The current working Code parser and visible Code template import `qbjs.js`
   2.7.0.

The official tutorial's `file_parser.js` 1.0.0 and `qbjs.js` 1.0.0 imports are
recorded separately and are not treated as current-tenant versions.

## Worksheet API disposition

- QBJS v2.7.0 documents `QBBatchService.updateWorksheet` with
  `worksheetData` and states that it completely replaces Batch worksheet data.
  It is not the intended Terpenes method because it could replace unrelated
  worksheet data, formulas, tabs, or metadata.
- QBJS v2.7.0 documents `QBBatchService.patchWorksheet` with `batchId` and
  `data` and states that only included fields are updated and omitted data is
  not removed. It is the preferred candidate for controlled Sandbox
  investigation.
- No claim is made that `patchWorksheet` supports Spreadsheet Worksheet named
  ranges, one- or two-dimensional arrays, or noncontiguous ranges.

## Batch-context project decision

- The raw LabSolutions file will not include a QBench Batch ID.
- The user uploads the file while working inside the intended named QBench
  Batch.
- The parser must obtain the current Batch's internal numeric ID from supported
  runtime or attachment context.
- The parser must not infer the Batch from customer or sample data.
- The parser must not hardcode a Batch ID.
- The parser must not require the instrument export to contain a QBench Batch
  ID.

The Batch ID question concerns supported runtime or attachment context only; it
is not a requirement to place a Batch ID inside the raw instrument file.

## Questions for QBench Support if Sandbox evidence remains insufficient

1. Does `QBBatchService.patchWorksheet` support Spreadsheet Worksheet named
   cells and named ranges?

2. Can `patchWorksheet` `data` values contain a one-dimensional or
   two-dimensional array for a spreadsheet named range?

3. Can one patch operation or two sequential patch operations safely update:
   - `Instrument Import!A:AE`
   - `Instrument Import!AH:BE`
   while preserving AF/AG and all omitted worksheet content?

4. Are JavaScript Number values patched as numeric Spreadsheet Worksheet cells
   recognized by `ISNUMBER` and `COUNT`?

5. Are `patchWorksheet` calls transactional, atomic per request, or capable of
   partial field updates?

6. What failure or rollback behavior applies when the second of two patch
   operations fails?

7. Is there a supported dry-run, preview, or disposable Sandbox debugging
   workflow?

Batch-context question: when a parser is triggered by a Batch attachment, what
supported runtime property or attachment context exposes the current Batch's
internal numeric ID?

## Requested answer format

For each open question, please provide the applicable `file_parser.js`/`qbjs.js`
version, an official documentation link or minimal sanitized example, and any
Sandbox-only validation constraint. Please do not provide production record
identifiers, credentials, bearer tokens, or permanent links to temporary
attachment URLs.
