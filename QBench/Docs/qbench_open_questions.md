# QBench Open Questions

- COA report template ID 26 exposes a Visual Editor but no visible source export/copy/download control. Active version 17 was selected read-only; source HTML was not extractable from the DOM inspection.
- COA assets were visible as QBench attachment download links, including `AIT Watermark.png`, `CoA Signatures.png`, `Header Image.png`, `hexagon-grid-8tile-1336x618.png`, `hexagon-grid.png`, and `Quality Control Verified.png`. Browser download attempts did not create local files, so assets were not saved into the repo.
- Confirm whether active report template ID 44 `Homogeneity` is used for production/sandbox Homogeneity COAs or only retained separately; inspected assays listed Certificate of Analysis Report as default.
- Parser internals for no-code parsers were not fully visible from read-only detail pages, and no parser export/download option was visible.
- File parser code pages did not expose a parser-specific export/download control. A later read-only editor inspection captured parser 46's complete active source and parser 45's visible template without invoking Save, Set Active, Preview, or file selection. Both import `file_parser.js` 1.1.0 and `qbjs.js` 2.7.0 and use the documented `run`/`QB` base model.
- Automation condition rows were not fully exposed in the compact read-only extraction; worksheet-field actions were visible and indexed.
- Moisture Analysis, Stability, and general Microbial Analysis did not show configured assay-level worksheet templates during inspection.

## Prompt 4.6 targeted QBench support request

Current-tenant read-only inspection resolved the base runtime and library
version questions. Official QBJS v2.7.0 documentation also establishes that
`updateWorksheet` completely replaces Batch worksheet data, so it is unsuitable
for the proposed Terpenes writer. `patchWorksheet`, which updates only included
fields and preserves omitted data, is the preferred candidate for a controlled
Sandbox investigation. Named ranges, array payloads, noncontiguous writes,
numeric cells, atomicity, rollback, and debugging behavior remain unproven.

The raw LabSolutions file will not contain a QBench Batch ID. The future parser
must obtain the current named Batch's internal numeric ID from supported runtime
or attachment context and must not infer or hardcode it.

Stage 2A found no supported Batch-context path in draft Preview runtime. Stage
2B then completed one exact-filename Batch-attachment trigger against the
authorized disposable Sandbox Batch. File Parser History recorded `SUCCESS`,
but did not persist the probe's safe property presence/type console lines.
Batch context therefore remains unresolved; the successful trigger does not
establish any property path or type.

Remaining questions are maintained in the sanitized fallback support request:

`QBench/Worksheets/Terpenes/development/2026-07-15_qbench_parser_wide_adapter/docs/qbench_prompt_4_6_support_request.md`

Current status:

- `qbench_runtime_contract_status = insufficient_for_prompt_4_6`
- `qbench_sandbox_probe_status = stage_2b_completed_attachment_job_success_console_not_persisted_batch_context_unresolved`

Prompt 4.6 is complete through Stage 2B only. Stages 3 and later and Prompt 5
have not started. No later QBench action is authorized by these status labels.
