# Native named-cell persistence diagnostic

Date: 2026-07-17

Historical Probe A classification:
**`unique_named_cell_control_failed`**.

Current controlled-stop classification:
**`codex_named_cell_save_control_failed`**.

Probe A used a completely unique system name in a new isolated native
Spreadsheet Worksheet. QBench's **Add Named Cell** control was used exactly
once. The three fields were entered with real keystrokes, each field was
blurred with Tab, Exportable was enabled, and focus was moved outside the row.
The complete row was visibly present before Create.

After the Draft version save completed, a full navigation back to the
Worksheets list, and reopen from that list, the 6x5 grid and A1 probe label
persisted but the named-cell list contained zero rows. No visible validation
or error message appeared.

Probe A therefore failed. The required stop gate prevented Probes B and C,
the no-leading-zero fallback, any further candidate-name test, and any new
seven- or 43-field worksheet construction.

The later version-creation control independently produced a visibly present
Draft row in the Versions tab and then reopened with zero named-cell rows.
That result confirms the current failure is not a missing-version assertion.

These historical results do not prove that underscore names, `_01`, reused
scalar names, or the candidate mapping are unsupported. The user's later
manual control supersedes the earlier environment conclusion: `sdf` at `A1`
persisted in the exact native scalar Draft after **Save Draft** and refresh.
Codex visibly confirmed it after reopening the exact worksheet and version;
its Display Name was blank and Exportable was enabled.

Codex then entered exactly one additional row,
`terpenes_codex_save_control_20260717` at `B2`, Display Name
`Codex save control`, Exportable enabled. The complete row was visible before
**Save Draft**, but it was absent after refresh and list-based reopen while
`sdf` remained. This is a Codex browser-control/input/save failure, not a QBench
environment failure. No support request is required. The current implementation
path is generated JSON import; manually typing 43 named cells is prohibited.

Controls remain:

- `destination_contract_proven=false`
- `atomicity_classification=api_patch_unresolved`
- `analyte_patch_key_contract=unresolved`
- `config/field_mapping_scalar_candidate.csv` remains unpromoted
- `manual_named_cell_persistence_control=passed`
- `qbench_native_named_cell_persistence=operational`
- `codex_browser_named_cell_save_control=failed`
- `browser_control_authoritative=false`
- no token, REST API request, PATCH, live-QBench access, Assay, Sample, Test,
  analytical result, or Pass/Fail artifact occurred
