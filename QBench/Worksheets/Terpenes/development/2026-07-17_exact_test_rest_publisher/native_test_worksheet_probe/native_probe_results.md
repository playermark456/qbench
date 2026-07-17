# Native probe results

Date: 2026-07-17

Final classification: **`native_test_worksheet_instantiation_passed`**

## Saved definition and version result

- The manually built worksheet was saved, left, and reopened from the
  Worksheets list.
- The title, six-row grid, all five named cells, both formulas, read-only
  metadata, and `UNCHANGED` sentinel persisted.
- Version 1 completed Draft -> Pending -> Approved -> Active.
- A raw instantiated export exposed a hidden nonnamed duplicate B7
  `COUNT(B3)` formula. Version 2 removed that row, was saved and reopened, and
  completed Draft -> Pending -> Approved -> Active.
- The final approved-active raw definition has six rows, five columns, zero
  hidden rows, and the exact five-cell named contract.
- Final raw definition:
  `native_test_worksheet_probe_v2_approved_active_saved_reopened_export_spreadsheet.json`
- Final raw definition SHA-256:
  `a43cb9779e03d401e5b43d69df6169a1236b51e45dd805bd9aee7353109f8b24`

## Assay and fresh Test result

- Assay: `SBX_ONLY_TERPENES_2026_07_17_NATIVE_TEST_WS_ASSAY`
- Test Worksheet association:
  `SBX_ONLY_TERPENES_2026_07_17_NATIVE_TEST_WS_PROBE` only
- Batch Worksheet association: none
- The Assay was left and reopened; its Test Worksheet association persisted.
- A fresh synthetic Sample was created.
- Assigning only the isolated Assay to that Sample created one fresh Test.
- No worksheet was manually assigned or pinned after Test creation.
- After navigating away and reopening, the Test Worksheet displayed the
  native six-row definition rather than QBench's blank 5x5 default.
- The Test was updated through QBench's normal **Update Version** action after
  corrected Version 2 became active.

## Exact manual persistence result

| Check | Reopened result |
|---|---|
| `native_probe_text` | `sandbox_native_test_probe` |
| `native_probe_number` | numeric `2.5` |
| `native_probe_isnumber` | `TRUE` |
| `native_probe_count` | `1` |
| `native_probe_sentinel` | `UNCHANGED` |

The instantiated Version 2 spreadsheet export contains exactly rows 1-6 and
the values above. Its filename is
`native_test_worksheet_probe_v2_exact_input_instantiated_export_spreadsheet.csv`
and its SHA-256 is
`a72835d464d17a858c5d9a3fc88b31eae69c512f517cb1083c85f0cd32d73e9e`.

After proof, only B2 and B3 were cleared. The Test Worksheet was saved, left,
and reopened. Final state: B2 blank, B3 blank, B4 `FALSE`, B5 `0`, B6
`UNCHANGED`, with B4-B6 still read-only and no hidden seventh row.

## Compatibility conclusion

- `old_sandbox_test_worksheet_engine = operational_for_native_definitions`
- `imported_prompt3_test_worksheet = compatibility_failure`

The saved 43-field destination definition remains structurally proven, but
its imported Prompt 3 runtime instance remains the earlier blank-default
failure. Therefore `destination_contract_proven` remains `false`,
`atomicity_classification` remains `api_patch_unresolved`, and no OAuth or API
gate is unlocked.

Recommended route:

1. Rebuild on the exact native old-Sandbox schema with the 43 writable named
   destinations and minimal layout/formulas.
2. Instantiate through an Assay and prove 43/43 destinations on a fresh Test.
3. Add the remaining formulas and Prompt 3 layout incrementally, rechecking
   instantiation at each stage.

## Safety result

- Credentials displayed: no
- OAuth token requested: no
- QBench REST API request: no
- PATCH request: no
- Live QBench accessed: no
- Analytical results entered: no; only disposable synthetic control values
- Pass/Fail artifact introduced: no
