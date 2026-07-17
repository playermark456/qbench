# Saved 43-field destination-contract proof

Date: 2026-07-17

Current controlled-stop classification:
**`json_import_upload_blocked_browser_file_upload_unsupported`**.

Prior imported-definition runtime classification:
**`normal_assay_test_instantiation_failed_blank_default`**.

Native control classification:
**`native_test_worksheet_instantiation_passed`**.

The saved and reopened isolated Sandbox Worksheet definition passed its exact
43-field structural proof. That result is preserved independently from two
runtime-instantiation failures. The earlier direct Test retained a blank 5x5
default worksheet, and a second, brand-new Test created normally from a
preconfigured isolated Assay also retained the blank 5x5 default after
navigating away and reopening it.

| Evidence layer | Classification |
|---|---|
| Saved/reopened Worksheet definition | `passed_43_of_43` |
| Direct existing-Test instantiation | `failed_blank_default_5x5` |
| Normal Assay-created Test instantiation | `normal_assay_test_instantiation_failed_blank_default` |
| Native UI-built Assay-created Test | `native_test_worksheet_instantiation_passed` |
| Exact native 43-field rebuild Phase 1 | `native_minimal_destination_probe_failed` (4/7) |
| Native underscore-scalar rebuild Phase 1A | `native_scalar_minimal_destination_probe_failed` (0/7 saved/reopened) |
| Unique one-cell persistence diagnostic | `unique_named_cell_control_failed` |
| Native version-creation control | `version_created_named_cell_missing` (visible Draft row; reopened with 0 named cells) |
| Manual `sdf` / A1 persistence control | `manual_named_cell_persistence_control_passed` |
| QBench native named-cell persistence | `operational` |
| Codex B2 save-procedure control | `codex_named_cell_save_control_failed` |
| Generated JSON candidate local validation | `passed_43_of_43` |
| Generated JSON Sandbox import | `blocked_browser_file_upload_unsupported` |
| JSON round-trip export | `not_run_import_gate` |
| Publisher destination gate | `destination_contract_proven=false` |

## Isolated Sandbox objects

- Worksheet: `SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF`
- Saved version: `2 - SBX_ONLY_TERPENES_API_DESTINATION_PROOF_V2 - APPROVED (ACTIVE)`
- Retained direct-path Assay: `SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF_TEST`
- Retained direct-path Sample: `SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF_SAMPLE`
- Normal-path Assay: `SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_ASSAY`
- Normal-path Sample: `SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_ASSAY_SAMPLE`

Internal Sandbox identifiers are omitted from tracked evidence. The new
normal-path Test identifier is recorded only in an ignored local evidence
file. The complete sanitized inventory is in
`sandbox_destination_proof/sanitized_object_inventory.json`.

No analytical results were entered and no Pass/Fail artifact was created.

## Saved Worksheet definition proof

| Evidence | Result |
|---|---|
| Saved/reopened raw Export Spreadsheet | `2026-07-17_SBX_ONLY_TERPENES_API_DESTINATION_PROOF_v2_approved_active_saved_reopened_export_spreadsheet.json` |
| Raw export SHA-256 | `2dfa8e9b94a6806be81b5b4ab58395e3fbefe3ebd0a56a4e7e53e6803d968bef` |
| Logical destinations | 43/43 present and exact |
| Writable targets | 43/43 |
| Missing / renamed / duplicated / formula-owned | None |
| Named-cell systems | 91, with zero duplicate references |
| Surrounding formulas | 265 intact; manifest SHA-256 `f149f36e2892eda5c72dddc9cf281e749df5c5313fceb58b140dae639581e910` |
| Pass/Fail destinations | Zero |
| Dimethylacetamide reportable destination | No |
| Peak Table reportable destination | No |

The raw definition export is preserved byte-for-byte in the ignored local
proof folder. The tracked copy is sanitized and contains no internal Sandbox
object identifiers.

## Normal Assay association proof

Before the new Sample was created, the isolated normal-path Assay was saved
with these settings:

- Active: yes.
- Show in Customer Portal: no.
- Test Worksheet: `SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF`.
- Batch Worksheet: none.
- Associated Worksheet active version: Version 2,
  `SBX_ONLY_TERPENES_API_DESTINATION_PROOF_V2`, APPROVED and ACTIVE.

The Assay page was left and reopened from the Assays list. The Test Worksheet
association persisted, and the Worksheet Versions view independently
confirmed Version 2 was the approved active version before Sample creation.

## Runtime Test evidence

### Direct existing-Test path

The earlier direct-path Test remains unchanged. After reopening, its Worksheet
tab contained only a blank 5-column by 5-row grid. QBench's supported
**Export Spreadsheet to CSV** action produced
`2026-07-17_SBX_ONLY_TERPENES_test_294_instantiated_export_spreadsheet.csv`
with SHA-256
`6470821a32c974f33b2421746c305a52dad7cc3fa2c043e0aa234b9f4ec6d12e`.
The export had five blank rows and none of the 43 destination cells.

### Normal Assay-created Test path

A fresh synthetic Sample was created after the Assay association was saved.
Assigning only the new isolated Assay created a brand-new Test through the
normal workflow. The Test:

- identified the expected isolated Assay;
- remained `NOT STARTED`;
- received no analytical results or Pass/Fail values;
- showed only the blank 5-column by 5-row default worksheet initially;
- was left for the Tests list, reopened from that list, and again showed only
  the blank 5x5 default worksheet.

Because the reopened UI state already proved the normal instance did not
retain the Worksheet definition, no runtime CSV export was needed and no
attempt was made to treat CSV as named-cell-contract evidence.

## Native old-Sandbox control

A separate Spreadsheet Worksheet was constructed entirely in the old Sandbox
UI without import, clone, or reuse:
`SBX_ONLY_TERPENES_2026_07_17_NATIVE_TEST_WS_PROBE`. Its corrected Version 2
is APPROVED and ACTIVE and has the exact six-row control contract documented
in `native_test_worksheet_probe/native_probe_configuration.md`.

The isolated Assay
`SBX_ONLY_TERPENES_2026_07_17_NATIVE_TEST_WS_ASSAY` retained that Test
Worksheet after the Assay was left and reopened. Assigning only that Assay to
a fresh synthetic Sample created a fresh Test whose Worksheet tab retained the
six-row native definition after reopen. The exact manual control values also
persisted:

- `native_probe_text = sandbox_native_test_probe`
- `native_probe_number = 2.5` as a numeric value
- `native_probe_isnumber = TRUE`
- `native_probe_count = 1`
- `native_probe_sentinel = UNCHANGED`

The values were then cleared and the blank baseline was saved and reopened.
The final Test has blank B2/B3, `FALSE`, `0`, and `UNCHANGED`; no analytical
result or Pass/Fail artifact remains.

The final raw definition export is
`native_test_worksheet_probe_v2_approved_active_saved_reopened_export_spreadsheet.json`
with SHA-256
`a43cb9779e03d401e5b43d69df6169a1236b51e45dd805bd9aee7353109f8b24`.
The exact-input instantiated CSV is
`native_test_worksheet_probe_v2_exact_input_instantiated_export_spreadsheet.csv`
with SHA-256
`a72835d464d17a858c5d9a3fc88b31eae69c512f517cb1083c85f0cd32d73e9e`.

This control proves:

- `old_sandbox_test_worksheet_engine = operational_for_native_definitions`
- `imported_prompt3_test_worksheet = compatibility_failure`

It does not prove the imported 43-field runtime contract and does not unlock
the publisher gate.

## Exact native 43-field rebuild controlled stop

The next isolated Worksheet,
`SBX_ONLY_TERPENES_2026_07_17_NATIVE_43_FIELD_BASE`, was built as a minimal
40x26 native grid. Its Version 1, `Native 43 Field Base v1`, remains Draft.
After save, navigation away, and reopen:

- `sample_mass_g` at `Data!B12` persisted;
- `batch_qc_disposition` at `Data!B22` persisted;
- `publish_ready` at `Data!B23` persisted;
- `source_file_hash` at `Data!B30` persisted;
- `terpenes_instrument_conc[1]`, `[12]`, and `[23]` did not save;
- otherwise-identical underscore diagnostic names did save and reopen, then
  were removed before the final saved state.

The exact Phase 1 result is therefore 4/7. The failure is in the native
worksheet definition/save path for bracketed named-cell keys. It does not
resolve the REST analyte PATCH representation, which remains `unresolved`.

Per the stop gate, Version 1 was not approved or activated, Version 2 was not
created, and no Assay, Sample, Test, or runtime values were created for this
rebuild. The reopened Export Spreadsheet action was invoked but produced no
downloadable file, so no Phase 1 or Version 2 raw-export SHA is claimed.
Sanitized evidence is in `native_43_field_rebuild/`.

## Native underscore-scalar rebuild controlled stop

The revised 43-row candidate mapping uses exact analyte destination names
`terpenes_instrument_conc_01` through `_23` at `Data!D2:Z2`. Local validation
passes all candidate invariants, but the candidate remains unpromoted.

The separate isolated Worksheet
`SBX_ONLY_TERPENES_2026_07_17_NATIVE_SCALAR_43_FIELD_BASE` was constructed
through the old Sandbox editor as an exact 40x26 grid. Before save its native
UI displayed all seven representative names and addresses, and all seven
target cells were blank, writable, unique, scalar, and non-formula. Draft
Version 1 `Native Scalar 43 Field Base v1` was created. After navigation to
the Worksheets list and reopen from that list, the grid and blank targets
persisted but the named-cell list contained zero entries.

The saved/reopened result is 0/7: seven missing, zero renamed, zero duplicated,
and zero formula-owned. Version 1 remains Draft and was not moved to Pending,
Approved, or Active. Because Export Spreadsheet was permitted only after
approval and activation, it was not run and no raw export or SHA-256 exists.
No Assay, Sample, Test, runtime value, Version 2, or Phase 3 object was created.
See the `scalar_*` evidence files in `native_43_field_rebuild/`.

## Unique one-cell persistence diagnostic

The follow-up diagnostic used a completely unique system name in a new
isolated 6x5 native Spreadsheet Worksheet:

- Worksheet: `SBX_ONLY_TERPENES_2026_07_17_NAMED_CELL_UNIQUE_CONTROL`
- Draft: `Named Cell Unique Control v1`
- System Name: `terpenes_named_cell_unique_control_20260717`
- Cell: `B2`
- Display Name: `Unique persistence control`
- Exportable: enabled

QBench's **Add Named Cell** control was used exactly once. All fields were
entered with real keystrokes, each was blurred with Tab, focus moved outside
the row, and the complete row was visibly present before Create. After save
completion, full navigation to the Worksheets list, and reopen, the 6x5 grid
and A1 label persisted but the named-cell list contained zero rows. No visible
validation or error message appeared.

Historical classification: **`unique_named_cell_control_failed`**. The earlier
environment-blocker/support conclusion is superseded. The user manually proved
native persistence with `sdf` at `A1`; Codex independently reopened the exact
native scalar Draft and saw that row with blank Display Name and Exportable
enabled. The separate Codex B2 row was visibly complete before **Save Draft**
but absent after refresh/reopen while `sdf` remained. Current classification:
**`codex_named_cell_save_control_failed`** and
`browser_control_authoritative=false`. Manual entry is recommended; no QBench
support request is required.
The required stop gate prevented analyte-name Probe B, no-leading-zero Probe B,
duplicate-name Probe C, and any further seven- or 43-field construction. This
result does not establish that `_01`, underscores, or reused names are
unsupported. Sanitized support evidence is in
`native_43_field_rebuild/named_cell_persistence_diagnostic/`.

## Publisher gate

- `destination_contract_proven=false`
- `atomicity_classification=api_patch_unresolved`
- `analyte_patch_key_contract=unresolved`
- No OAuth token request occurred.
- No QBench REST API request occurred.
- No PATCH occurred.
- Live QBench was not accessed.

The earlier imported 43-field Worksheet definition remains structurally
proven, but the native scalar saved/reopened contract failed before runtime.
The publisher remains blocked until a staged native-schema rebuild retains all
43 exact destinations on a fresh Assay-created Test and a later explicitly
authorized read-only API confirmation resolves the Test worksheet
representation. The candidate mapping was not promoted and publisher
configuration remains unchanged.

## Generated JSON import rebuild

The new implementation path is generated JSON import, not manual entry of 43
named cells. The locally generated candidate is:
`json_import_rebuild/SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE.json`.
It contains one 40x26 `Data` worksheet and exactly 43 sheet-qualified named
cells derived from the unpromoted scalar mapping. Local validation passed
43/43 with no missing, renamed, duplicated, formula-owned, Pass/Fail,
Dimethylacetamide, or Peak Table destinations. SHA-256:
`7cfeeee00403e8c3fa7bf7ec4c2726e25f63cc1f4b867bc1f06550f612ef8f70`.

The exact inactive Sandbox worksheet shell
`SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE` was created and its
title and breadcrumb matched. The in-app browser explicitly does not support
local file uploads, so the candidate was not attached or submitted. The
Versions tab contains no rows. No imported named-cell count, raw round-trip
export, or semantic round-trip result is claimed. The candidate is ready for
manual Sandbox upload.

## Version-creation control reconciliation

The isolated native control
`SBX_ONLY_TERPENES_2026_07_17_VERSION_CREATION_CONTROL` was created solely to
separate version creation from named-cell persistence. Its Version 1 row,
`Version Creation Control v1`, was visibly present in the QBench **Versions**
tab with status `DRAFT`. The reopened saved draft retained a 6x5 grid, A1
`Version creation control`, and blank B2, but contained zero named-cell rows.
The saved Draft row is evidence that a version exists; it is not evidence that
the named-cell contract saved. The destination, OAuth, REST, and PATCH gates
remain closed.
