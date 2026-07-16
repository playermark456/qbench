# Prompt 4.6B QBench Sandbox change log

Date: 2026-07-16

Environment: `https://ait-sandbox.qbench.net/`

| Worksheet | Change | Result | Disposition |
|---|---|---|---|
| 61 `SBX_ONLY_TERPENES_2026_07_16_Patch_Probe_Dynamic_Batch_Worksheet` | Imported `sandbox_probe_worksheet_compatibility_candidate.json`; did not save a version or activate a version | QBench reported success and retained the imported working configuration after reload; Versions reported no versions | Quarantined; do not save, activate, attach, or patch |
| 62 `SBX_ONLY_TERPENES_2026_07_16_Probe_Minimal_Runtime_Baseline` | Created as a new inactive Dynamic Spreadsheet with no assay association | Blank `Sheet1`, 8x8 data, 0 named cells, no versions | Approved compatibility baseline only |
| 62 export | Used **Export Spreadsheet** twice; both downloads were byte-identical | SHA-256 `02e986a41bcd9f6b1bc9586c3df041cbaf930ad4309fb28d5e20d26c6057e5c2` | One raw copy preserved under `source/` |
| 62 controlled import | Imported only `dist/qbench_runtime_probe_batch_ws_candidate__ait_sandbox_runtime.json` into the blank worksheet 62 working configuration | Exact `Probe` tab; 17 rows x 57 columns through `BE`; 15 required named cells; 9 required formula results/sentinels; exact 64 writable cells; no legacy Terpenes content | Pre-save gate passed |
| 62 saved version | Saved as version 1, title `Prompt 4.6B Probe v1 - Sandbox Round Trip` | Initially `DRAFT`; `Set Active` disabled; Assays (0) | Kept inactive and unattached through round-trip verification |
| 62 saved-version reopen | Reloaded worksheet 62 and reopened version 1 from the Configuration version selector | `Probe`, 969 cells, 15 named cells, formula results/sentinels, and writable/read-only settings persisted with no differences | Reopen verification passed |
| 62 saved-version export | Manually invoked **Export Spreadsheet** after reopening version 1; two byte-identical files were downloaded | Preserved SHA-256 `2f3b2b17beae2c3361b2cfcccfde121aeb4ed32757127806864d2c2b2da63d19`; semantic comparison found no unclassified difference | Round-trip comparison passed |
| 62 activation | Moved version 1 from `DRAFT` to `PENDING` without the optional lock/reviewer, approved it, made it active, and enabled the worksheet object's `Active` setting | The controlled worksheet became selectable on the synthetic Batch form | Minimum old-Sandbox activation needed for the scalar test |
| Synthetic scalar Batch | Created `SBX_ONLY_TERPENES_2026_07_16_SCALAR_PATCH_PROBE_01` with only worksheet 62 selected; Assay, Tags, and Protocol left blank | Probe baseline was blank, blank, `FALSE`, `0`, `UNCHANGED` | Isolated Sandbox-only Batch retained for evidence; no internal ID recorded |
| Scalar parser | Created inactive Code parser `SBX_ONLY_TERPENES_2026_07_16_Scalar_Patch_Probe` and version 1 `Scalar Patch Probe v1 - Runtime Context Guard` as `DRAFT` | Saved source contains no Batch ID; trigger, assay, and filename rule unset | Parser remains inactive |
| Scalar Preview attempt 1 | Ran one validated `QBBatchService.patchWorksheet` request with nested `probe_text: { value: ... }` and `probe_number: { value: ... }` data | Success callback fired; error callback did not; all 969 Batch worksheet cells were unchanged after reload | `accepted_callback_but_noop_nested_value_shape`; retained in the audit trail |
| Scalar parser correction | Updated existing inactive parser version 1 in place as `DRAFT` to emit direct `probe_text: "sandbox_probe"` and `probe_number: 1.25` values | Reloaded saved source contained no nested wrapper, no Batch ID, and no forbidden write path; trigger, assay, and filename rule remained unset | Parser remained inactive |
| Scalar Preview attempt 2 | Ran one corrected direct-value `QBBatchService.patchWorksheet` request after confirming the Batch link, active worksheet version, and exact named-cell keys/addresses | Success callback fired; error callback did not; all 969 Batch worksheet cells were unchanged after reopen/reload | `accepted_callback_but_noop_direct_scalar_shape`; second silent no-op; stopped before third payload or range testing |
| Manual persistence control | Entered only `manual_persistence_control` and numeric `2.5` in B2/B3, saved, reopened, then cleared only B2/B3, saved, and reopened again | Manual values persisted with `TRUE`, `1`, and `UNCHANGED`; the second save restored blank, blank, `FALSE`, `0`, and `UNCHANGED` | `manual_persistence_passed`; general Batch worksheet persistence works |
| Instantiated worksheet audit | Reverified the single controlled worksheet link, active version 1, selected `Probe` tab, 15 named cells, exact scalar mappings, B2/B3 writability, and formula behavior | Assignment and formula layer matched the controlled worksheet | `batch_assignment_verified` |
| Runtime trigger preparation | Created byte-identical `SBX_ONLY_TERPENES_SCALAR_PATCH_TRIGGER_01.txt`, saved the exact Batch-attachment/Equal filename trigger with assay unset, captured 969 baseline cells, and briefly activated the isolated parser | SHA-256 `ed796c690b972ca08f1976b1d8f7355d3e5140e73ffa912c441d6185a093283b`; direct payload unchanged | No alternate payload or write path introduced |
| Runtime trigger blocker and cleanup | The available browser control could not populate the HTML file input; no upload, attachment, parser job, File Parser Result, or callback occurred | Parser immediately deactivated; temporary Batch context removed; reusable Draft source restored; post-cleanup 969-cell comparison reported zero changes | Initial attempt `blocked`; exact trigger left inert |
| Runtime trigger manual handoff | Reprepared the exact trigger and temporary runtime context, activated only the isolated parser, and paused for the method owner to select the byte-identical fixture and click Upload once | Exactly one controlled attachment and one parser-history job were created for the exact parser; the job remained `IN_PROGRESS`, neither callback was observable, and all 969 worksheet cells matched the blank baseline with zero changes | `attachment_trigger_runtime_stalled`; no confirmed patch error response, alternate payload, or retry |
| Runtime trigger final cleanup | Inspected only the created attachment/job, then deactivated the parser and removed the temporary Batch context from the saved Draft | Reload confirmed the runtime-only source segment was absent; parser inactive; exact trigger inert; controlled attachment retained | Safe cleanup passed |

Worksheet 61 remains quarantined and unchanged. Worksheet 62 version 1 is
approved/active and assigned only to the controlled synthetic Batch; it remains
unassociated with an assay. Both the nested and corrected direct scalar
requests produced no persisted write despite their success callbacks. Manual
Batch worksheet persistence and the controlled worksheet assignment passed.
The initial attachment-trigger attempt was blocked before upload and cleaned
up safely. The approved manual handoff then created one attachment and one
parser-history job, but the job remained `IN_PROGRESS`, exposed no callback,
and changed zero of 969 worksheet cells. It is classified
`attachment_trigger_runtime_stalled`, with
`code_parser_patchworksheet_status = blocked_old_sandbox_runtime_stall`. The
parser is inactive, its runtime-only context was removed, and the attachment
remains isolated on the synthetic Batch. The recommended next route is a
separately reviewed No-Code File Parser workflow using normalized TSV input;
it is not implemented here. No third payload, range/matrix patch, or Prompt 5
work was started, and production `ait.qbench.net` was not accessed.
