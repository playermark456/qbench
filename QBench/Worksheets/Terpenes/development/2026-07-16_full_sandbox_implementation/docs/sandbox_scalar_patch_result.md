# Prompt 4.6B old-Sandbox scalar patch results

Date: 2026-07-16

Sandbox hostname: `ait-sandbox.qbench.net`

Result: `failed_safely_two_success_callbacks_two_persisted_noops`

## Controlled objects and configuration

- Synthetic Batch label:
  `SBX_ONLY_TERPENES_2026_07_16_SCALAR_PATCH_PROBE_01`.
- Worksheet label:
  `SBX_ONLY_TERPENES_2026_07_16_Probe_Minimal_Runtime_Baseline`.
- Worksheet version: version 1, `APPROVED (ACTIVE)`.
- Parser label: `SBX_ONLY_TERPENES_2026_07_16_Scalar_Patch_Probe`.
- Parser version: version 1, `Scalar Patch Probe v1 - Runtime Context Guard`.
- Parser state after both attempts: inactive; version status `DRAFT`;
  trigger, assay, and filename rule unset.
- Quarantined worksheet 61 was not opened, changed, attached, or deleted.

No internal Batch ID, parser ID, worksheet-version ID, attachment ID, or other
numeric object ID is recorded here. For each attempt, the Batch context was
used only in a one-time unsaved Preview buffer and was discarded without
saving.

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
persisted. The complete
969-cell comparison reported zero changed cells. This attempt is retained in
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
reopening the
Batch worksheet, waiting, and reloading, neither direct value persisted.

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

## Reusable parser source

The corrected reusable parser source is preserved at
`src/qbench_scalar_patch_probe.js`. It imports `file_parser.js` 1.1.0 and
`qbjs.js` 2.7.0, validates the direct-value request, calls only
`QBBatchService.patchWorksheet`, and requires a guarded runtime context. The
saved source contains no Batch ID and no nested value wrapper.

The reloaded Sandbox editor source and repository file matched byte-for-byte
at SHA-256
`c0e8f5567e8c770dbe1944a28299e8e94f4e5b282d32f9db807a063a22344550`.
After the Preview, the saved Draft was reloaded and confirmed to contain only
the reusable source; the one-time runtime prelude and Batch ID did not persist.

## Compatibility assessment and stop condition

Attempt 2 is a second silent no-op. Both the nested and official direct scalar
shapes reached the success callback without changing the controlled Batch
Spreadsheet Worksheet. The Batch-to-worksheet link, active version, named-cell
keys, and named-cell addresses were all present and correct.

The result is consistent with the old Sandbox `patchWorksheet` implementation
targeting only a legacy Dynamic/QWML named-field data model rather than the
Spreadsheet Worksheet named-cell layer used by this probe. That remains a
compatibility hypothesis, not a proven service contract, because no supported
read-only UI exposed the service's internal target model.

No third payload shape was attempted. `updateWorksheet`, full worksheet
replacement, service `update`, and direct HTTP writes were not used.
Range/matrix testing did not start. Prompt 5 did not start.

## Sandbox objects changed by attempt 2

1. Existing inactive parser version 1 was updated in place as a `DRAFT` to use
   direct scalar values.
2. One controlled Preview ran and returned the success callback without
   changing any worksheet cell.

No worksheet, Batch, assay, sample, test, attachment, protocol, parser trigger,
filename rule, Pass/Fail field, or range/matrix probe was created or changed
during attempt 2. Production `ait.qbench.net` was not accessed or changed.
