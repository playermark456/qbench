# Scalar Phase 1 result

Classification: **`native_scalar_minimal_destination_probe_failed`**

Evidence correction: the historical 0/7 observation remains, but it no longer
supports an environment-blocker conclusion. The user manually created `sdf`
at `A1` in this exact Draft and proved it persisted after **Save Draft** and
refresh. Codex reopened the exact Draft and confirmed `sdf`, blank Display
Name, and Exportable enabled. The subsequent Codex B2 save-control row was
visibly complete before **Save Draft** but absent after refresh/reopen while
`sdf` remained. QBench native named-cell persistence is `operational`;
Codex browser-controlled worksheet editing is not authoritative and is stopped.

Version-state reconciliation: a subsequent direct observation of this
worksheet's QBench **Versions** tab showed the visible row
`1 - Native Scalar 43 Field Base v1` with status `DRAFT`. The 0/7 result is
therefore retained as a named-cell persistence failure, not as evidence that a
Draft version was never created.

Worksheet:
`SBX_ONLY_TERPENES_2026_07_17_NATIVE_SCALAR_43_FIELD_BASE`

Version: `1 - Native Scalar 43 Field Base v1 - DRAFT`

The isolated worksheet was constructed through the old Sandbox worksheet
editor without JSON import, clone, copied `qb_config`, or an externally
generated definition. The saved/reopened grid retained exactly 40 rows and 26
columns. The logical sheet is identified by the visible `Data` label in A1.
No row or column was hidden.

Before save, the UI showed seven unique, exportable native named cells at the
required addresses. Each destination cell was blank, writable, non-formula,
scalar, and not Pass/Fail. After Create, navigation to the Worksheets list,
and reopen from that list, the 40x26 grid and blank target cells remained but
the native named-cell list contained zero entries.

| Required destination | Address | Saved and reopened |
|---|---|---|
| `terpenes_instrument_conc_01` | `Data!D2` | No |
| `terpenes_instrument_conc_12` | `Data!O2` | No |
| `terpenes_instrument_conc_23` | `Data!Z2` | No |
| `sample_mass_g` | `Data!B12` | No |
| `batch_qc_disposition` | `Data!B22` | No |
| `publish_ready` | `Data!B23` | No |
| `source_file_hash` | `Data!B30` | No |

Result: **0/7 saved/reopened destinations**, seven missing, zero renamed,
zero duplicated, and zero formula-owned targets observed. No Pass/Fail named
cell was present.

The saved-definition gate failed before workflow promotion. Version 1 remains
Draft; Pending, Approved, and Active were not entered. Export Spreadsheet was
not run because the user required it only after approval and activation.
Phase 1B runtime instantiation was not run.
