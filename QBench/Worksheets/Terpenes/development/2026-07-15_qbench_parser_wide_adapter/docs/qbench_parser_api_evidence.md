# QBench parser API evidence

## Evidence status

`qbench_runtime_contract_status = insufficient_for_prompt_4_6`

`qbench_sandbox_probe_status = sufficient_to_begin_controlled_prompt_4_6_probe`

`runtime-contract evidence status = official_base_contract_plus_tenant_runtime_partial`

`qbench_native_status = blocked_missing_targeted_qbench_runtime_contract`

Prompt 4.6 and Prompt 5 have not started. No QBench parser was created,
edited, saved, activated, previewed, or run during this evidence update.
The generated Prompt 4.5 manifest retains its original coarse blocked status;
it was not regenerated or re-versioned for this evidence-only Prompt 4.6A
update.

## Official documentation sources

| Official source | Contract evidence used | Important limit |
|---|---|---|
| [Introduction to File Parsers](https://junctionconcepts.zendesk.com/hc/en-us/articles/4409122738701-Introduction-to-File-Parsers) | File Parsers are custom JavaScript templates; `run(() => { ... })`; `QB.files`; asynchronous `QB.files[n].text()`; `QB.console`; `QB.progressBar`; `QB.success()`; `QB.error()`; `QBBatchService`; `updateWorksheet`; attachment triggers; API-triggered attachment parsing. | The tutorial imports `file_parser.js` 1.0.0 and `qbjs.js` 1.0.0. Those tutorial versions are not current-tenant version evidence, and the tutorial's `updateWorksheet` example is not approved for the proposed Terpenes writer. |
| [QBJS documentation version selector](https://qbjs.docs.qbench.net/) and [QBBatchService v2.7.0](https://qbjs.docs.qbench.net/v2.7.0/QBBatchService.html) | v2.7.0 documents `updateWorksheet({ batchId, worksheetData, urlParams?, success?, error? })` and states that `worksheetData` completely replaces Batch worksheet data. It also documents `patchWorksheet({ batchId, data, urlParams?, success?, error? })` and states that only payload fields are updated and omitted data is not removed. | `updateWorksheet` is unsuitable for the proposed Terpenes writer. `patchWorksheet` is the preferred candidate for controlled Sandbox investigation, but the page does not document Spreadsheet named ranges, array values, noncontiguous ranges, numeric cell typing, atomicity/rollback, or dry-run behavior. |
| [No-Code File Parsers](https://junctionconcepts.zendesk.com/hc/en-us/articles/9147024166797-No-Code-File-Parsers) | Standard/No-Code parser targets, triggers, filename operators, delimited formats, finder types, and Cell Range same-position/Target Start Cell behavior. | It does not prove that the sectioned raw LabSolutions ASCII export is directly parseable. |
| [Batch Spreadsheet Worksheets & Automations](https://junctionconcepts.zendesk.com/hc/en-us/articles/9705726121229-Batch-Spreadsheet-Worksheets-Automations) | Batch Data Modified automation, all Test Worksheets in the Batch, named Test Worksheet destination, Batch Worksheet source, and `VLOOKUP({{test.id}}, ...)`. | Supports future Prompt 5 architecture only. Prompt 5 has not started. |
| [API - Attachments](https://junctionconcepts.zendesk.com/hc/en-us/articles/360044230052-API-Attachments) | BATCH/TEST attachment association, list retrieval by attachment type and object ID, API creation, and temporary retrieval URLs. | Temporary URLs are not permanent links. No example authorization value from the article is recorded here. |

## Officially documented Code parser contract

The official tutorial proves the following base contract:

- File Parsers are custom JavaScript templates.
- The execution wrapper is `run(() => { ... })`.
- `QB.files` is the selected-file array.
- `QB.files[n].text()` provides asynchronous text access.
- `QB.console` provides parser-visible logging.
- `QB.progressBar` provides progress reporting.
- `QB.success()` and `QB.error()` report successful and failed completion.
- `QBBatchService` is the documented Batch service.
- `QBBatchService.updateWorksheet` accepts `batchId` and `worksheetData`, plus
  optional `urlParams`, success, and error callbacks. QBJS v2.7.0 states that
  `worksheetData` completely replaces Batch worksheet data.
- `QBBatchService.patchWorksheet` accepts `batchId` and `data`, plus optional
  `urlParams`, success, and error callbacks. QBJS v2.7.0 states that it updates
  only fields included in the payload and does not remove omitted data.
- The tutorial's simple `updateWorksheet` payload maps a worksheet field name
  to `{ value: supplied_value }`. That example does not establish a safe
  Spreadsheet Worksheet range-patching contract.
- A configured attachment trigger can execute a File Parser, including after
  an attachment is uploaded through the API.

Official tutorial versions are recorded separately:

| Tutorial import | Version |
|---|---|
| `file_parser.js` | 1.0.0 |
| `qbjs.js` | 1.0.0 |

These tutorial versions are not silently equated with current AIT tenant
versions.

## Current AIT tenant evidence

Read-only inspection on 2026-07-15 captured the complete 380-line active source
for parser ID 46 and the visible inactive Code template for parser ID 45.

| Tenant question | Read-only observation | Status and limit |
|---|---|---|
| Current imports | Parser 46 and the visible parser 45 template import `file_parser.js` 1.1.0 and `qbjs.js` 2.7.0. | Proven for the inspected current AIT tenant templates. Tutorial 1.0.0 versions remain separate. |
| Wrapper and globals | Parser 46 uses `run(async () => { ... })`, `QB.files`, `QB.console`, `QB.progressBar`, `QBBatchService`, `QB.success()`, and `QB.error()`. Parser 45's visible template uses the same base wrapper/globals. | The current AIT tenant uses the documented base runtime model with its current imports. |
| File access | Parser 46 uses `FileReader.readAsArrayBuffer` for Excel and `FileReader.readAsText` for delimited files. It does not call `file.text()`. | Current tenant File/Blob compatibility is corroborated; direct `.text()` behavior under `file_parser.js` 1.1.0 was not separately exercised. |
| Batch service write | Parser 46 creates `QBBatchService` but writes with inherited `update(...)` and a `qb_dynamic_spreadsheet_data` payload for tab `Results`; it calls neither documented `updateWorksheet(...)` nor `patchWorksheet(...)`. | This is current parser source evidence, not a contract for the proposed Terpenes writer. It does not prove named ranges, array payloads, safe A:AE/AH:BE targeting, or patch behavior. |
| Batch ID source | Parser 46 extracts candidate Test IDs from file content, calls `/batches/get` through `QBBatchService.getJson`, and uses the first returned Batch ID. | It does not show how the triggering Batch ID is exposed by a Batch-attachment invocation. |
| Error and partial behavior | Hard failures call `QB.error()`. Per-block exceptions are logged and skipped; remaining blocks may still be submitted and the parser may call `QB.success()` with warnings. | Controlled completion calls are proven. All-or-nothing behavior and QBench update transactionality are not proven. |
| Trigger configuration | Parser 46 is configured for Batch attachments, Cannabinoid Potency, and filenames ending in `.csv`. | Attachment-trigger configuration is proven without running it. |

No Save, Set Active, Preview, Choose file, or other mutation/execution control
was invoked.

## No-Code parser evidence and fallback

Official No-Code documentation proves:

- Data Target may be Populate Batch Worksheet or Populate Test Worksheet.
- Triggers may be Batch attachments or Test attachments.
- Filename matching supports Equal, Start With, End With, and Contain.
- Delimited formats include Excel, comma-separated, tab-separated, and a
  single-character custom delimiter.
- Finder types include By Cell Range, By Sample in Batch, By Test in Batch, By
  Sample in List, and By Test in List.
- A Cell Range finder supports same-position or Target Start Cell behavior.

It does not prove direct parsing of the sectioned raw LabSolutions ASCII file.
The following is only an untested Sandbox fallback option, not the approved
native design:

```text
Local Prompt 4.5 parser/adapter
    -> generated wide TSV
    -> No-Code File Parser
    -> Batch Instrument Import worksheet
```

## Batch automation evidence

Official documentation proves that a Batch `Data Modified` automation can set
a named field on all Test Worksheets in the Batch by copying from the Batch
Worksheet, and that a `VLOOKUP` expression may use `{{test.id}}` as its Test ID
lookup key. This supports the future Prompt 5 architecture but does not begin
Prompt 5.

## Attachment API evidence

Official documentation proves that attachments can be associated with BATCH or
TEST objects; lists can be retrieved by attachment type and object ID; an
attachment can be created through the API; and retrieving an attachment returns
a temporary download URL. Temporary download/upload URLs must not be stored as
permanent links. No example bearer token or signed URL is copied into the
repository.

## Resolved targeted questions

1. The current AIT tenant does use the `run`/`QB`/`QBBatchService` base contract
   with `file_parser.js` 1.1.0 in both inspected Code templates.
2. The current working Code parser imports `qbjs.js` 2.7.0.

## API disposition for the proposed Terpenes writer

- `updateWorksheet` remains documented evidence only. Its `worksheetData`
  parameter completely replaces Batch worksheet data, so it could replace
  unrelated worksheet data, formulas, tabs, or metadata. It is not approved
  for the Terpenes Batch Spreadsheet Worksheet.
- `patchWorksheet` is the preferred candidate API for a controlled Prompt 4.6
  Sandbox investigation because its `data` payload updates only included fields
  and does not remove omitted data.
- No claim is made that `patchWorksheet` supports Spreadsheet Worksheet named
  ranges, one- or two-dimensional arrays, or noncontiguous ranges.

## Resolved Batch-context project decision

- The raw LabSolutions file will not include a QBench Batch ID.
- The user uploads the file while working inside the intended named QBench
  Batch.
- The parser must obtain the current Batch's internal numeric ID from supported
  runtime or attachment context.
- The parser must not infer the Batch from customer or sample data.
- The parser must not hardcode a Batch ID.
- The parser must not require the instrument export to contain a QBench Batch
  ID.

The remaining Sandbox discovery question is: when a parser is triggered by a
Batch attachment, what supported runtime property or attachment context exposes
the current Batch's internal numeric ID?

## Remaining targeted patch questions

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

## Preflight record

Direct PATH checks failed for `git --version`, `node --version`, and
`py --version`. Bundled Codex runtime tools were available:

| Tool | Version |
|---|---|
| Git | `git version 2.53.0.windows.3` |
| Node.js | `v24.14.0` |
| Python | `Python 3.12.13` |

Controlled dependency hashes:

| Dependency | Raw checkout SHA-256 | Canonical LF SHA-256 | Controlled outcome |
|---|---|---|---|
| Prompt 3 Test candidate | `90686b980882b221008f281be33984dc5232e2f3d2632300db3f4a27b529640a` | `90686b980882b221008f281be33984dc5232e2f3d2632300db3f4a27b529640a` | Accepted |
| Prompt 4 Batch candidate | `f779d0175a7aec09eb5f57a778fde91cccf07bb7078a9573132547ee158da151` | `e5c80b1213396cab4932e267fd786c6986c933d4b404f11daa5c5aba0629758e` | Accepted by canonical LF hash |
| Prompt 4 layout config | `7f1270063f689f9cac94ee22e4f69b0ea7953a6f5dc86e1f6b4c00bb4bed7ef0` | `fe137404165a044907a7fe31a7cc386f53f402bb643dd94bf2fbffe958571410` | Canonical matches Prompt 4 manifest |
| Prompt 4 import contract config | `7382a15789f8771b2888c908e69811898e5213454ec380d8efc68c0b7488b72a` | `b389c3d96447d6c3dfb5c879d3a624ce5f05bb39b16951305f609febe77f9a23` | Canonical matches Prompt 4 manifest |

The Prompt 4 Batch candidate is controlled by the canonical LF hash. The raw
Windows checkout hash mismatch is recorded and is not a dependency failure
because canonical LF SHA-256 matches the controlled value.

Baseline result summary:

| Package | Result |
|---|---|
| Prompt 2 validation/parser/tests | Passed; 27 tests; fixture 24/34/23 |
| Prompt 3 generator/validator/tests | Passed; generator hash matched; validator passed; 50 tests |
| Prompt 4 generator/validator/tests | Passed during controlled baseline build; 39 tests; canonical LF hash matched the controlled Prompt 4 hash |
| Prompt 4.5 JavaScript tests | Passed; 143 tests |
| Prompt 4.5 Python tests | Passed; 13 tests |

Final Prompt 4.5 hardening controls:

| Control | Status |
|---|---|
| Publish AF/AG/AV outputs | Exact text `"TRUE"` |
| Boolean true output for AF/AG/AV | Not emitted |
| Review evidence identity | `source_row_hash` required and must match reviewed row |
| Generic `hash` review evidence | Rejected |
| Missing source filename/name | Rejected with `SOURCE_FILENAME_REQUIRED` |
| Invented source filename | Not allowed |

Sandbox validation evidence status in the generated manifest:

| Validation record | Status | Path | SHA-256 |
|---|---|---|---|
| Test Worksheet Sandbox validation | `not_recorded_in_repository` | `null` | `null` |
| Batch Worksheet Sandbox validation | `not_recorded_in_repository` | `null` | `null` |
| End-to-end QBench parser validation | `not_recorded_in_repository` | `null` | `null` |

Local untracked Sandbox notes are not used as generated evidence.
