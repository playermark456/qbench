# QBench File Parser Prompt 4.6A scan package

Controlled scan date: 2026-07-15

- `qbench_runtime_contract_status = insufficient_for_prompt_4_6`
- `qbench_sandbox_probe_status = sufficient_to_begin_controlled_prompt_4_6_probe`

## Scope

This directory contains sanitized, read-only QBench Sandbox evidence for seven
File Parsers and the complete visible 39-job File Parser Results history. It is
supporting runtime evidence only and must not be used to invent undocumented
JavaScript function names, signatures, named-range payloads, or write behavior.

Inventory totals:

- Parsers: 7
- Code parsers: 2
- Result-history jobs: 39
- `SUCCESS`: 38
- `IN_PROGRESS`: 1
- Failed jobs: 0

## Worksheet API disposition

- `QBBatchService.updateWorksheet` uses `worksheetData` and officially
  completely replaces Batch worksheet data. It is unsuitable for the proposed
  Terpenes writer because it could replace unrelated worksheet data, formulas,
  tabs, or metadata.
- `QBBatchService.patchWorksheet` uses `batchId` and `data` and officially
  updates only included fields without removing omitted data. It is the
  preferred candidate for controlled Prompt 4.6 Sandbox investigation.
- Named ranges, one- or two-dimensional arrays, noncontiguous ranges, numeric
  cell typing, request atomicity, second-patch rollback, and supported
  dry-run/debugging behavior remain Sandbox questions.

## Batch-context decision

The raw LabSolutions file will not contain a QBench Batch ID. The user uploads
the file from the intended named Batch, and a future parser must obtain that
Batch's internal numeric ID from supported runtime or attachment context. It
must not infer the Batch from customer/sample data, hardcode an ID, or require
the instrument file to contain one.

## Artifacts

| Artifact | Purpose |
|---|---|
| `file_parser_inventory.json` | Deterministic structured inventory of seven parsers. |
| `file_parser_inventory.csv` | CSV representation of the same parser inventory. |
| `file_parser_results_history_inventory.csv` | Sanitized representative result-history records. |
| `file_parser_results_history_evidence.md` | Aggregate and record-level history evidence and limits. |
| `qbench_file_parser_runtime_contract_matrix.csv` | CSV representation of the 28-row runtime matrix. |
| `qbench_file_parser_scan_limitations.md` | Evidence boundaries and unproven behavior. |
| `qbench_file_parser_scan_manifest.json` | Counts, scope controls, source metadata, and SHA-256 hashes for all other scan artifacts. |

The manifest cannot contain its own stable SHA-256 without self-reference. Its
SHA-256 is validated and reported externally after the manifest is finalized.

## Safety

No QBench object was changed. No parser was created, edited, saved, activated,
previewed, or run. No underlying result file or destination worksheet was
opened or downloaded. Prompt 4.6 and Prompt 5 have not started, and no
production action is authorized.
