# Native old-Sandbox Test Worksheet probe

Date: 2026-07-17

Classification: **`native_test_worksheet_instantiation_passed`**

This folder records the UI-only control used to distinguish an old-Sandbox
Spreadsheet Worksheet engine failure from a Prompt 3 import-compatibility
failure. The native definition was built manually in
`https://ait-sandbox.qbench.net/`; it was not imported, cloned, copied from an
existing worksheet, or generated outside QBench.

The corrected saved/reopened definition is Version 2, APPROVED and ACTIVE.
It contains exactly six rows by five columns, five unique exportable named
cells, no hidden rows, and no Pass/Fail cell. A fresh Test created only by
assigning the isolated Assay instantiated the same six-row worksheet.

The requested values `sandbox_native_test_probe` and numeric `2.5` persisted
after save and reopen. `ISNUMBER(B3)` returned `TRUE`, `COUNT(B3)` returned
`1`, and the read-only sentinel remained `UNCHANGED`. The two writable inputs
were then cleared, saved, and reopened; the final Test baseline is blank with
the formulas back at `FALSE` and `0`.

The old editor labels this worksheet type `Spreadsheet`; this is QBench's
legacy Spreadsheet Worksheet type. It is a single-table editor and exposes no
sheet-tab naming control or sheet-name property in Export Spreadsheet, so a
visible tab named `Probe` cannot be evidenced. That schema limitation does not
change the successful native-instantiation classification.

Tracked evidence contains no internal Sandbox IDs. Raw downloaded exports are
preserved byte-for-byte beside these files but are ignored by Git.

## Evidence files

- `native_probe_configuration.md` — exact saved definition contract.
- `native_probe_results.md` — save/reopen, Assay, Test, persistence, and
  classification results.
- `sanitized_object_inventory.json` — task-created objects without internal
  IDs.
- `raw_export_sha256.txt` — raw definition and instantiated-export hashes.
- `sandbox_cleanup_plan.md` — scoped later cleanup steps; no cleanup was run.
