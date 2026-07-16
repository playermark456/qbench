# Prompt 4.6B old-Sandbox scalar patch results

Date: 2026-07-16

Sandbox hostname: `ait-sandbox.qbench.net`

Result: `failed_safely_two_preview_noops_attachment_trigger_patch_error`

## Controlled objects and configuration

- Synthetic Batch label:
  `SBX_ONLY_TERPENES_2026_07_16_SCALAR_PATCH_PROBE_01`.
- Worksheet label:
  `SBX_ONLY_TERPENES_2026_07_16_Probe_Minimal_Runtime_Baseline`.
- Worksheet version: version 1, `APPROVED (ACTIVE)`.
- Parser label: `SBX_ONLY_TERPENES_2026_07_16_Scalar_Patch_Probe`.
- Parser version: version 1, `Scalar Patch Probe v1 - Runtime Context Guard`.
- Parser final state: inactive; version status `DRAFT`; exact Batch-attachment
  trigger configured; assay unset; filename rule `Equal` to
  `SBX_ONLY_TERPENES_SCALAR_PATCH_TRIGGER_01.txt`.
- Quarantined worksheet 61 was not opened, changed, attached, or deleted.

No internal Batch ID, parser ID, worksheet-version ID, attachment ID, or other
numeric object ID is recorded here. The runtime-mode diagnostic briefly saved
the disposable Batch context only in the isolated parser Draft, then removed
it immediately during cleanup. The final saved source matches the reusable
repository source exactly and contains no numeric Batch literal.

## Read-only target audit

Before attempt 2, and again after its second silent no-op, the following were
verified in the old Sandbox UI:

- the synthetic Batch contained exactly one link to the controlled worksheet;
- the linked worksheet configuration selected version 1 as
  `APPROVED (ACTIVE)`;
- the worksheet configuration contained exactly 15 named cells/ranges;
- `probe_text` existed at `Probe!B2`;
- `probe_number` existed at `Probe!B3`;
- the scalar baseline was blank, blank, `FALSE`, `0`, and `UNCHANGED`;
- no Pass/Fail field or result existed.

This rules out a missing Batch worksheet assignment, inactive worksheet
version, missing scalar named-cell key, or incorrect scalar named-cell address
as the explanation for attempt 2.

## Attempt 1: nested update-style values

Classification:
`scalar_patch_attempt_1 = accepted_callback_but_noop_nested_value_shape`

The first request used nested values:

```json
{
  "batchId": "<runtime-only synthetic Batch context>",
  "data": {
    "probe_text": { "value": "sandbox_probe" },
    "probe_number": { "value": 1.25 }
  },
  "success": "<success callback>",
  "error": "<error callback>"
}
```

The callback record was `patch_callback = success`; the error callback did not
fire. After navigating away and reloading the Batch worksheet, neither target
persisted. The complete 969-cell comparison reported zero changed cells. This
attempt is retained in
`tests/fixtures/attempt_1_nested_scalar_patch_payload.json` and in the Git
history; it is not treated as proof that `patchWorksheet` or named cells are
unsupported.

## Attempt 2: corrected direct scalar values

Classification:
`scalar_patch_attempt_2 = accepted_callback_but_noop_direct_scalar_shape`

The second and final authorized request used direct values:

```json
{
  "batchId": "<runtime-only synthetic Batch context>",
  "data": {
    "probe_text": "sandbox_probe",
    "probe_number": 1.25
  },
  "success": "<success callback>",
  "error": "<error callback>"
}
```

The full request was validated before the call:

- request keys were exactly `batchId`, `data`, `error`, and `success`;
- data keys were exactly `probe_number` and `probe_text`;
- `probe_text` was the JavaScript string `sandbox_probe`;
- `probe_number` was the finite JavaScript Number `1.25`;
- neither data value was an object or contained a `value` wrapper;
- no `worksheetData`, `updateWorksheet`, service `update`, direct HTTP call,
  or unrelated named cell was present.

The callback record was `patch_callback = success`; the error callback did not
fire, and QBench displayed its Preview success state. After navigating away,
reopening the Batch worksheet, waiting, and reloading, neither direct value
persisted.

The complete 17 by 57 grid was captured immediately before and after attempt
2. Both captures contained 969 cells and the comparison reported zero changed
cells in displayed value and numeric/read-only class.

Persisted scalar values after attempt 2 were:

| Named cell | Expected result | Persisted result |
|---|---:|---:|
| `probe_text` | `sandbox_probe` | blank |
| `probe_number` | numeric `1.25` | blank / no numeric-cell class |
| `probe_isnumber` | `TRUE` | `FALSE` |
| `probe_count` | `1` | `0` |
| `probe_sentinel` | `UNCHANGED` | `UNCHANGED` |

Therefore no numeric cell was stored, `ISNUMBER` did not recognize a number,
`COUNT` remained zero, the sentinel formula was unchanged, every omitted
named cell/range remained unchanged, and no unrelated worksheet cell changed.

## Manual worksheet persistence control

Classification: `manual_persistence_result = manual_persistence_passed`.

The disposable Batch worksheet began at the restored blank scalar baseline.
Only `Probe!B2` and `Probe!B3` were edited manually:

- `probe_text = manual_persistence_control`;
- `probe_number = 2.5`.

After the normal Batch worksheet Save action, navigation away, and reopen,
the values persisted exactly. `probe_number` had the `jss_number` numeric-cell
class, `probe_isnumber = TRUE`, `probe_count = 1`, and
`probe_sentinel = UNCHANGED`.

Only B2 and B3 were then cleared. After a second Save, navigation away, and
reopen, the original baseline persisted again: blank, blank, `FALSE`, `0`,
and `UNCHANGED`. This rules out a general Batch worksheet persistence failure.

## Instantiated Batch worksheet audit

Classification: `batch_assignment_result = batch_assignment_verified`.

Read-only inspection confirmed:

- the Batch had exactly one link to the controlled worksheet label;
- version 1 was `APPROVED (ACTIVE)`;
- the selected worksheet tab was `Probe`;
- all 15 named cells/ranges were present;
- `probe_text = Probe!B2` and `probe_number = Probe!B3`;
- B2 and B3 were writable while B4, B5, and B6 were read-only;
- the manual control caused B4 and B5 to recalculate to `TRUE` and `1`;
- clearing B2 and B3 restored B4 and B5 to `FALSE` and `0`;
- the sentinel remained `UNCHANGED` throughout.

This rules out an unexpected worksheet instance, inactive version, missing
named-cell key, incorrect scalar address, or broken assigned formula layer.

## Runtime-mode diagnostic

Earlier browser-control classification:
`runtime_mode_diagnostic_initial_attempt = blocked`.

Final manual-handoff classification:
`runtime_mode_diagnostic = attachment_trigger_patch_error`.

A byte-identical copy of the controlled redacted fixture was created as
`SBX_ONLY_TERPENES_SCALAR_PATCH_TRIGGER_01.txt`. Both files are 8,692 bytes
and have SHA-256
`ed796c690b972ca08f1976b1d8f7355d3e5140e73ffa912c441d6185a093283b`.

The isolated parser was configured with only:

- `When file is added to Batch attachments`;
- no assay;
- filename condition `Equal`;
- filename text `SBX_ONLY_TERPENES_SCALAR_PATCH_TRIGGER_01.txt`.

The complete 969-cell blank baseline was captured before activation. The
temporary runtime source contained the same validated direct-value payload as
attempt 2 and no alternate payload, wrapper, `updateWorksheet`, service
`update`, direct HTTP call, range, or matrix value. The isolated parser was
briefly activated.

The first attempt stopped at the approved manual-handoff boundary because the
available in-app browser control could not populate QBench's HTML file input.
No file was selected or uploaded, and no attachment or parser job was created.
File Parser Results status: not created. Callback result: not reached. The
parser was immediately deactivated, the temporary Batch context was removed,
and the sanitized reusable Draft was restored.

For the approved manual handoff, the same baseline and exact trigger were
prepared again. The method owner selected the byte-identical local fixture and
clicked Upload exactly once. Inspection after navigation and reload confirmed:

- exactly one attachment with the controlled filename was created;
- exactly one File Parser Results job was created for
  `SBX_ONLY_TERPENES_2026_07_16_Scalar_Patch_Probe`;
- the job identified the exact controlled parser, whose sole configured
  execution version was version 1, `Scalar Patch Probe v1 - Runtime Context
  Guard`;
- the job remained `IN_PROGRESS` through repeated history reloads;
- neither the success nor error callback was observable;
- no completed success or sanitized error detail was exposed by QBench;
- the complete persisted worksheet contained the same 969 cells as the
  recorded blank baseline, with zero changed cells.

Persisted scalar values after the attachment-trigger attempt were blank,
blank, `FALSE`, `0`, and `UNCHANGED`. Therefore `probe_text` and
`probe_number` were not patched, no numeric cell was stored, `ISNUMBER`
remained false, `COUNT` remained zero, the sentinel remained unchanged, and
all omitted and unrelated cells were preserved.

Because the job was created but never reported `SUCCESS`, this result is not
classified `attachment_trigger_patch_noop`. The non-completing job and absent
callback are recorded as `attachment_trigger_patch_error`; no alternate
payload shape or fallback write path was attempted.

Immediately after inspecting the created job, the parser was deactivated. The
temporary Batch context was removed from the saved Draft, the runtime-only
source segment was absent after reload, and the reusable guarded direct-value
source remained. The exact trigger is inert because the parser is inactive.

After cleanup, a complete 969-cell capture matched the pre-activation baseline
with zero changed cells. The single controlled attachment was retained as
required and was not deleted.

## Reusable parser source

The corrected reusable parser source is preserved at
`src/qbench_scalar_patch_probe.js`. It imports `file_parser.js` 1.1.0 and
`qbjs.js` 2.7.0, validates the direct-value request, calls only
`QBBatchService.patchWorksheet`, and requires a guarded runtime context. The
saved source contains no Batch ID and no nested value wrapper.

The reloaded Sandbox editor source and repository file matched byte-for-byte
at SHA-256
`c0e8f5567e8c770dbe1944a28299e8e94f4e5b282d32f9db807a063a22344550`.
After the manual-handoff cleanup, the saved Draft was reloaded and confirmed
to contain the reusable guarded source without the runtime-only context
segment.

## Compatibility assessment and stop condition

Attempt 2 is a second silent no-op. Both the nested and official direct scalar
shapes reached the success callback without changing the controlled Batch
Spreadsheet Worksheet. The Batch-to-worksheet link, active version, named-cell
keys, and named-cell addresses were all present and correct.

The two Preview results are consistent with the old Sandbox `patchWorksheet`
implementation targeting only a legacy Dynamic/QWML named-field data model
rather than the Spreadsheet Worksheet named-cell layer used by this probe.
That remains a compatibility hypothesis, not a proven service contract,
because no supported read-only UI exposed the service's internal target model.

The manual control and assignment audit eliminate general worksheet
persistence and wrong-instance explanations. The manual handoff eliminated
the browser file-input blocker: the exact attachment and parser job were
created. The job did not complete, neither callback was observable, and the
worksheet remained unchanged. The required final classification is therefore
`attachment_trigger_patch_error`.

No third payload shape was attempted. `updateWorksheet`, full worksheet
replacement, service `update`, and direct HTTP writes were not used.
Range/matrix testing did not start. Prompt 5 did not start.

## Sandbox objects changed by the runtime-mode diagnostic

1. Only B2 and B3 of the disposable Batch worksheet were manually populated,
   saved, reopened, cleared, saved again, and verified at the original blank
   baseline.
2. The existing parser configuration was narrowed to the exact Batch
   attachment filename while leaving assay unset.
3. The isolated parser was activated for the controlled manual upload, then
   deactivated immediately after the created job was inspected.
4. The parser Draft briefly contained the runtime-only Batch context, then was
   restored to the sanitized reusable source.
5. Exactly one controlled attachment and one associated File Parser Results
   job were created. The attachment was retained; the job remained
   `IN_PROGRESS`.

No new worksheet, Batch, assay, sample, test, protocol, Pass/Fail field, or
range/matrix probe was created. No third payload shape was attempted.
Range/matrix testing did not start. Prompt 5 did not start. Production `ait.qbench.net` was not accessed or changed.
