# Prompt 4.6B old-Sandbox scalar patch result

Date: 2026-07-16

Sandbox hostname: `ait-sandbox.qbench.net`

Result: `failed_safely_success_callback_without_persisted_cell_changes`

## Controlled objects

- Synthetic Batch label:
  `SBX_ONLY_TERPENES_2026_07_16_SCALAR_PATCH_PROBE_01`.
- Worksheet label:
  `SBX_ONLY_TERPENES_2026_07_16_Probe_Minimal_Runtime_Baseline`.
- Worksheet version: version 1, approved and active for the disposable Batch
  assignment.
- Parser label: `SBX_ONLY_TERPENES_2026_07_16_Scalar_Patch_Probe`.
- Parser version: version 1, `Scalar Patch Probe v1 - Runtime Context Guard`.
- Parser state after the test: inactive; version status `DRAFT`; trigger,
  assay, and filename rule unset.
- Quarantined worksheet 61 was not opened, changed, attached, or deleted.

No internal Batch ID, parser ID, worksheet-version ID, attachment ID, or other
numeric object ID is recorded here. The Batch context was used only in the
one-time unsaved Preview buffer and was discarded without saving.

## Worksheet activation and assignment

The controlled worksheet did not appear on the new-Batch form while it was an
inactive draft. The minimum required activation path was:

1. Move worksheet version 1 from `DRAFT` to `PENDING` and decline the optional
   lock/reviewer step.
2. Approve version 1 and answer yes when asked to make it active.
3. Enable the worksheet object's `Active` setting and save the worksheet
   details.
4. Create the synthetic Batch with only the controlled worksheet selected;
   Assay, Tags, and Protocol were left blank.

The Batch worksheet was verified before the patch. Its five scalar cells were
blank, blank, `FALSE`, `0`, and `UNCHANGED`, respectively.

## Parser execution

The reusable parser source is preserved at
`src/qbench_scalar_patch_probe.js`. It imports `file_parser.js` 1.1.0 and
`qbjs.js` 2.7.0, validates the full request, calls only
`QBBatchService.patchWorksheet`, and requires a guarded runtime context. The
saved source contains no Batch ID. The reloaded Sandbox editor source and the
repository file matched byte-for-byte at SHA-256
`dee7fea032635bb4b19286b722c42c78414513373e852761a2d28bbaa044bbb7`.

For the one authorized Preview, the internal Batch context was supplied only
through a one-time unsaved runtime prelude. The reusable source was reloaded
after the Preview and matched the repository source; the prelude and Batch ID
did not persist. No file or fixture was selected for the Preview.

The exact sanitized request shape was:

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

The validator required request keys to be exactly `batchId`, `data`, `error`,
and `success`; data keys to be exactly `probe_number` and `probe_text`; and
`probe_number.value` to be the finite JavaScript Number `1.25`.

## Callback and persisted result

- `patch_callback = success` was emitted once.
- The error callback did not fire.
- QBench displayed its Preview success state.
- After a new navigation to the Batch worksheet, a wait, and a full reload,
  neither target cell had changed.

Persisted scalar values were:

| Named cell | Expected patch result | Persisted result |
|---|---:|---:|
| `probe_text` | `sandbox_probe` | blank |
| `probe_number` | numeric `1.25` | blank / no numeric-cell class |
| `probe_isnumber` | `TRUE` | `FALSE` |
| `probe_count` | `1` | `0` |
| `probe_sentinel` | `UNCHANGED` | `UNCHANGED` |

The complete 17 by 57 grid was captured before and after the Preview. All 969
cells matched in both displayed value and numeric/read-only class. Therefore:

- both requested target cells remained unchanged;
- every omitted named cell/range remained unchanged;
- all formulas and sentinels remained unchanged;
- no unrelated worksheet data changed;
- no numeric cell was stored, `ISNUMBER` remained false, and `COUNT` remained
  zero;
- no Pass/Fail field or result existed before or after the test.

## Compatibility finding and stop condition

In this older Sandbox runtime, the documented scalar request reached the
`patchWorksheet` success callback but produced no persisted named-cell change
in the controlled Batch Spreadsheet Worksheet. The observed behavior is a
silent no-op compatibility failure. The evidence does not establish whether
the service ignored named-cell keys, targeted another worksheet data model, or
returned success before discarding an unsupported patch.

Per the failure rule, no alternate payload shape was attempted, no
`updateWorksheet` or replacement API was used, and range/matrix testing did
not start. Prompt 5 did not start.

## Sandbox objects created or changed

1. The controlled worksheet version changed from inactive `DRAFT` to approved
   and active.
2. The controlled worksheet object's `Active` setting was enabled.
3. The synthetic Batch was created and assigned only the controlled worksheet.
4. The disposable scalar parser object was created inactive.
5. Parser version 1 was created as `DRAFT` and remained inactive.
6. One Preview ran and returned the success callback without changing any
   worksheet cell.

No assay, sample, test, attachment, protocol, parser trigger, filename rule,
Pass/Fail field, or range/matrix probe was created or changed. Production
`ait.qbench.net` was not accessed or changed.
