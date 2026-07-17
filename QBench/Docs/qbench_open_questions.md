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

Scalar attempt 1 used nested update-style values. Its success callback fired,
but the complete 969-cell Batch worksheet grid was unchanged. It is retained
as `accepted_callback_but_noop_nested_value_shape`, not as proof that
`patchWorksheet` or Spreadsheet named cells are unsupported.

Scalar attempt 2 used the official direct-value model: JavaScript string
`probe_text = "sandbox_probe"` and JavaScript Number `probe_number = 1.25`.
The reusable parser validated exactly the two direct data keys, emitted no
`{ value: ... }` wrappers, and contained no saved Batch ID. Before and after
the attempt, read-only inspection confirmed the synthetic Batch linked the
controlled worksheet, version 1 was `APPROVED (ACTIVE)`, all 15 named cells
were present, and the scalar addresses were `Probe!B2` and `Probe!B3`.

Attempt 2 also emitted `patch_callback = success`; the error callback did not
fire. After reopening and reloading the Batch worksheet, `probe_text` and
`probe_number` remained blank, `probe_isnumber = FALSE`, `probe_count = 0`,
and `probe_sentinel = UNCHANGED`. Its complete 969-cell comparison also
reported zero changed cells.

A manual Batch worksheet control then proved the instantiated worksheet can
persist edits: `manual_persistence_control` and numeric `2.5` survived
save/reopen, produced `TRUE` and `1`, and were cleared with a second
save/reopen that restored the exact blank baseline. Read-only inspection also
verified the selected `Probe` tab, active version 1, all 15 named cells, exact
B2/B3 mappings, writable inputs, and functioning formulas.

The exact-filename attachment-trigger diagnostic was prepared with a
byte-identical controlled fixture, exact Batch-attachment trigger, no assay,
and the same direct payload. The available in-app browser control could not
populate QBench's HTML file input. No file was uploaded, no attachment or
parser job was created, no File Parser Result existed, and no callback was
reached. The parser was immediately deactivated, its temporary Batch context
was removed, and the saved Draft source was restored exactly. The pre/post
cleanup 969-cell comparison reported zero changes.

Current status:

- `qbench_sandbox_scalar_patch_attempt_1 = accepted_callback_but_noop_nested_value_shape`
- `qbench_sandbox_scalar_patch_attempt_2 = accepted_callback_but_noop_direct_scalar_shape`
- `qbench_sandbox_scalar_patch_status = runtime_mode_diagnostic_blocked_after_two_preview_noops`
- `qbench_sandbox_scalar_patch_compatibility = possible_legacy_dynamic_qwml_target_only_unproven`
- `qbench_sandbox_numeric_cell_behavior = not_written_not_proven`
- `qbench_sandbox_manual_persistence = passed`
- `qbench_sandbox_batch_assignment = verified`
- `qbench_sandbox_runtime_mode_diagnostic = blocked_before_upload`
- `qbench_sandbox_parser_final_state = inactive_sanitized_draft_exact_trigger_inert`
- `qbench_sandbox_range_matrix_status = not_started`
- `prompt_5_status = not_started`

No third payload shape was attempted, and neither `updateWorksheet` nor a
replacement API was used. The two no-ops are consistent with the older
Sandbox service targeting only legacy Dynamic/QWML named-field data rather
than the Spreadsheet Worksheet named-cell layer, but that remains an unproven
compatibility hypothesis. The blocked attachment upload did not distinguish
Preview-only behavior from service incompatibility. Sanitized evidence is in
`QBench/Worksheets/Terpenes/development/2026-07-16_full_sandbox_implementation/docs/sandbox_scalar_patch_result.md`.

## Prompt 4.6C No-Code attachment-run result

An isolated Standard/No-Code parser accepted two non-overlapping cell-range
finders in one configuration: A2:AE2 to `Instrument Import!A2` and AH2:BE2 to
`Instrument Import!AH2`. AF and AG are excluded, `Patch Worksheet Data` is
disabled, no assay is assigned, and the exact Batch attachment filename is
`SBX_ONLY_TERPENES_WIDE_IMPORT_01.txt`.

The canonical attachment populated both finder ranges, preserved the AF2/AG2
formulas, and evaluated to `Valid` / `Import row valid` after navigate-away and
reload. The 23 analytes, counts `24` / `34` / `23`, and Dimethylacetamide audit
value `100` used native numeric cells. The source-row hash persisted and no
spreadsheet error appeared.

The duplicate advanced the single attachment record to version 2, triggered a
second successful parser job, retained the canonical row 2, and did not append
row 3. The nonnumeric-analyte and missing-peak-count fixtures each triggered a
successful parser job and persisted the expected worksheet-owned rejection
message after reopen. All four jobs reported `SUCCESS`; Publish and Tests
remained untouched and no Pass/Fail artifact was created.

Detailed sanitized evidence is in
`QBench/Worksheets/Terpenes/development/2026-07-16_no_code_parser_fallback/`.
The operational limitation remains: Prompt 4.5 local normalization must run
before QBench upload. This is not production-ready, and Prompt 5 has not
started.
