# Sandbox failure and controlled-stop results

No token or Sandbox API request was made. The current pre-token gate stops
because the exact native 43-field contract failed its representative Phase 1
save/reopen probe and the official OAuth endpoint contract is absent. The
credential presence check passed without exposing any value. Atomicity proof
is also absent.

The historical isolated version-creation control created a visibly present
`DRAFT` row in QBench's Versions tab, then reopened with zero named-cell rows.
Its classification was **`version_created_named_cell_missing`**. This corrects
any prior inference that the current stop condition was the absence of a saved
worksheet version. Its earlier environment-blocker conclusion is superseded by
the user's persisted `sdf` / A1 control.

Current control result: QBench native named-cell persistence is operational.
The Codex B2 row was complete before **Save Draft** but disappeared after
refresh and list-based reopen while `sdf` remained. Classification:
**`codex_named_cell_save_control_failed`** with
`browser_control_authoritative=false`. Further Codex-controlled QBench
worksheet editing stopped; manual field entry is recommended.

## Destination proof controlled stop

The earlier imported saved definition has a passing 43/43 structural export,
but its direct and normal Assay-created Tests instantiate as QBench's blank 5x5
default. A UI-built native six-row control proved the old-Sandbox engine works
for native definitions.

The exact native rebuild then stopped at 4/7 representative destinations:

- four scalar names saved and reopened exactly;
- all three representative indexed names with brackets were rejected;
- underscore diagnostic controls persisted and were removed;
- Version 1 remains Draft;
- Version 2, Assay, Sample, Test, and runtime probes were not created;
- Export Spreadsheet was invoked on the reopened Draft but produced no local
  download, so no raw-export hash is claimed.

Classification: **`native_minimal_destination_probe_failed`**.

## Native underscore-scalar controlled stop

The revised candidate uses exact analyte names
`terpenes_instrument_conc_01` through `_23` and passes its local 43-row
validator. A separate native 40x26 Worksheet and Draft Version 1 were created
through the old Sandbox editor. The pre-save UI showed all seven representative
definitions, but after navigation away and reopen from the Worksheet list the
named-cell list contained zero entries.

Saved/reopened result: 0/7, with seven missing, zero renamed, zero duplicated,
and zero formula-owned. Version 1 remained Draft; approval, activation, Export
Spreadsheet, Phase 1B runtime instantiation, Version 2, Phase 2, and Phase 3
were not run. The candidate mapping was not promoted.

Current classification:
**`native_scalar_minimal_destination_probe_failed`**.

## Unique one-cell persistence diagnostic

Probe A created only
`SBX_ONLY_TERPENES_2026_07_17_NAMED_CELL_UNIQUE_CONTROL` and Draft
`Named Cell Unique Control v1`. It used a 6x5 native grid, a visible A1 label,
blank writable B2, the unique system name
`terpenes_named_cell_unique_control_20260717`, and QBench's **Add Named Cell**
control exactly once.

The row was entered with real keystrokes, blurred with Tab, and visibly present
before Create. After save completion, navigation to the Worksheets list, and
reopen, the grid and label persisted but the named-cell list contained zero
rows. No visible validation or error message appeared.

- Probe A: `unique_named_cell_control_failed`
- Probe B `_01`: not run
- Probe B `_1`: not run
- Probe C: not run
- Historical classification: `unique_named_cell_control_failed`
- Current correction: `qbench_native_named_cell_persistence=operational`
- Current Codex control: `codex_named_cell_save_control_failed`

The stop gate prohibits further Codex browser-controlled worksheet
construction. No support request is required. No claim about underscore,
zero-padded, prefix, length, or duplicate system-name compatibility is made.

## Required failure cases exercised locally

| Case | Local result |
|---|---|
| Batch not found | safe error; no PATCH |
| Test not found | `BLOCKED` |
| Test not in selected Batch | `BLOCKED` |
| duplicate Test ID in Publish | complete plan blocked |
| missing Test ID | row retained and blocked |
| missing source hash | blocked |
| authorization off | blocked |
| Import AF rejected | blocked |
| Import AG invalid | blocked |
| non-numeric analyte | blocked |
| incorrect counts | blocked |
| missing destination named cell | blocked |
| formula-owned destination | blocked |
| GET timeout | limited retries, sanitized error |
| timeout after PATCH submission | no retry, verify, rollback, stop |
| HTTP error | status-only sanitized error |
| success response with failed persistence | rollback, stop |
| changed source hash | `REAUTHORIZATION REQUIRED` |
| unchanged duplicate publish | `NO CHANGE`, no PATCH |
| later Test fails after prior success | prior success recorded; Batch stops |

Additional local checks reject Pass/Fail/result fields, formula-like input,
alternate hosts, missing runtime approvals, and unrelated-cell mutation.

Sandbox classification for every PATCH-dependent case remains **not run**.
