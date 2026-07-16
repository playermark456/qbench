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
- `qbench_live_probe_status = closed_after_stage_2b`
- `qbench_live_environment = read_only_reference_only`
- `future_writable_environment = https://ait-sandbox.qbench.net/`

Prompt 4.6 live probing is closed after Stage 2B with
`batch_context_status = unresolved_console_output_not_persisted`. The Stage 3
scalar patch and all later write probes were not run. No later live QBench
action is authorized by these status labels.

All future writable work moves to `https://ait-sandbox.qbench.net/`. That
Sandbox is older and may not match live configuration, so its existing objects
are not authoritative. GitHub-controlled worksheet candidates, parser code,
mappings, and specifications remain the source of truth. The next task is
Prompt 4.6B: Full QBench Sandbox implementation and validation. Prompt 5 has
not started.

## Prompt 4.6B old-Sandbox worksheet import compatibility

The first Prompt 4.6B import used a separate Terpenes-derived compatibility
artifact rather than the controlled `Probe` candidate. The visible `Sheet1`,
old Terpenes rows, and `Sheet1!B96` / `Sheet1!C96` mappings exactly match that
uploaded file. This run therefore does not establish that the old Sandbox
importer merged, ignored, translated, or partially imported the controlled
candidate.

Worksheet 61 retained the imported working configuration after reload even
though its Versions tab reported no versions. It is quarantined and is not a
valid probe destination.

Worksheet 62 is a new inactive, unattached, blank Dynamic Spreadsheet created
specifically as an old-Sandbox compatibility baseline. Its actual **Export
Spreadsheet** file is preserved at:

`QBench/Worksheets/Terpenes/development/2026-07-16_full_sandbox_implementation/source/2026-07-16_ait-sandbox_ws_id_62_blank_export_spreadsheet.json`

Resolved: the old Sandbox importer accepted the controlled worksheet 62-native
candidate. The unsaved working configuration and reopened saved draft both
contained one `Probe` tab, 17 rows, 57 columns through `BE`, the exact 15 named
cells, the nine required formula results/sentinels, the exact 64 writable
cells, and no legacy Terpenes content. Worksheet 62 version 1 passed the saved
round-trip gate before later being approved and activated solely for the
controlled synthetic Batch assignment.

Resolved: a manual **Export Spreadsheet** download of the reopened saved
version was preserved and compared with
`dist/qbench_runtime_probe_batch_ws_candidate__ait_sandbox_runtime.json`.
The semantic round trip passed for the exact worksheet data and formulas,
15 named cells, and writable/read-only settings. Differences were limited to
documented old-Sandbox runtime normalization of namespace, worksheet-management
flags, viewport metadata, empty style objects, and the evaluated top-level
formula cache. No scalar patch was run during this verification.

## Prompt 4.6B old-Sandbox scalar patch compatibility

One separately authorized scalar Preview used the exact documented
`QBBatchService.patchWorksheet` argument names and only these data fields:
`probe_text = "sandbox_probe"` and JavaScript Number `probe_number = 1.25`.
The reusable parser validated the complete request before the call and
contained no saved Batch ID.

The old Sandbox emitted `patch_callback = success`; the error callback did not
fire. However, a fresh navigation and reload of the saved Batch worksheet
showed `probe_text` and `probe_number` still blank, `probe_isnumber = FALSE`,
`probe_count = 0`, and `probe_sentinel = UNCHANGED`. The complete 969-cell grid
matched before and after the Preview, so every omitted field and all unrelated
worksheet data were preserved because nothing was written.

Current status:

- `qbench_sandbox_scalar_patch_status = failed_safely_success_callback_without_persisted_cell_changes`
- `qbench_sandbox_scalar_patch_compatibility = silent_no_op_in_old_sandbox_runtime`
- `qbench_sandbox_numeric_cell_behavior = not_written_not_proven`
- `qbench_sandbox_range_matrix_status = not_started`
- `prompt_5_status = not_started`

No alternate payload shape was attempted, and neither `updateWorksheet` nor a
replacement API was used. The remaining support question is whether the older
Sandbox `patchWorksheet` implementation ignores Spreadsheet Worksheet named
cells, targets a different worksheet data model, or returns success before
discarding an unsupported named-cell patch. Sanitized evidence is in
`QBench/Worksheets/Terpenes/development/2026-07-16_full_sandbox_implementation/docs/sandbox_scalar_patch_result.md`.
