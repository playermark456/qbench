# Atomicity results

Sandbox classification: **`api_patch_unresolved`**.

No Sandbox token was available, and no actual saved disposable Test Worksheet
proved the probe fields. The task's stop conditions therefore prevented both
the scalar PATCH and the valid-plus-invalid multi-field PATCH.

No claim of transactionality is made.

## Required disposable Sandbox sequence

Use only a fresh task-created Test and its saved Export Spreadsheet.

1. Capture original controlled text and numeric values and prepare a rollback
   payload.
2. PATCH both fields once with `sandbox_api_probe` and native numeric `1.25`.
3. GET, reopen, and Export Spreadsheet; verify values, numeric type, formulas,
   omitted fields, and absence of Pass/Fail.
4. Roll back once and verify exact baseline.
5. PATCH several valid named cells together and verify all, then restore.
6. PATCH the same valid fields plus one deliberately invalid field.
7. GET/reopen/export after the request and compare every field to baseline.
8. Restore baseline and verify.

Classify exactly one:

- `api_patch_atomic`: invalid request changes nothing and valid request changes
  all expected fields;
- `api_patch_partial`: any valid field persists from the invalid request;
- `api_patch_silent_noop`: success is reported with no expected persistence;
- `api_patch_error`: an error is returned and nothing persists;
- `api_patch_unresolved`: response/persistence/rollback evidence is ambiguous.

The local synthetic suite exercises successful, partial, silent-noop, error,
and timeout-after-apply behaviors. Those tests validate publisher defenses;
they do not classify QBench.

If the result is not `api_patch_atomic`, direct publishing remains blocked. A
new Test Worksheet must implement pending staging fields, pending source hash,
reviewer/timestamp, pending-complete, and committed source hash. Phase A must
stage and verify; Phase B must commit only an identical reviewed hash. If the
worksheet cannot prevent incomplete staging from feeding calculations, stop.
