# QBench support request: Prompt 4.6 runtime contract

Date prepared: 2026-07-15

`qbench_runtime_contract_status = insufficient_for_prompt_4_6`

## Purpose

Request authoritative clarification for a future Sandbox-only Code File Parser
that would write parsed Terpenes data to a Batch Spreadsheet Worksheet. This
request does not authorize a production change, parser creation, parser run, or
the start of Prompt 4.6 or Prompt 5.

## Documentation already reviewed

- [Introduction to File Parsers](https://junctionconcepts.zendesk.com/hc/en-us/articles/4409122738701-Introduction-to-File-Parsers)
- [QBJS v2.7.0 QBBatchService](https://qbjs.docs.qbench.net/v2.7.0/QBBatchService.html#updateWorksheet)
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

## Questions for QBench Support

3. Does `QBBatchService.updateWorksheet` support Spreadsheet Worksheet named
   cells and named ranges?

4. Can `worksheetData` values contain a one-dimensional or two-dimensional
   array for a named spreadsheet range?

5. Can one update request safely write the two noncontiguous blocks:
   `Instrument Import!A:AE` and `Instrument Import!AH:BE` while leaving AF/AG
   untouched?

6. When triggered by a Batch attachment, how is the triggering Batch ID exposed
   to the Code parser?

7. Are JavaScript Number values written as actual numeric Spreadsheet Worksheet
   cells recognized by `ISNUMBER` and `COUNT`?

8. Is `updateWorksheet` transactional, staged, or capable of partial field
   updates after an error?

9. Is there a dry-run, preview, or disposable Sandbox testing method?

## Requested answer format

For each open question, please provide the applicable `file_parser.js`/`qbjs.js`
version, an official documentation link or minimal sanitized example, and any
Sandbox-only validation constraint. Please do not provide production record
identifiers, credentials, bearer tokens, or permanent links to temporary
attachment URLs.
