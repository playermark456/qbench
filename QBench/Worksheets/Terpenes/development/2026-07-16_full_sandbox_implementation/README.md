# Prompt 4.6B full Sandbox implementation

This package holds the old-Sandbox compatibility baseline and candidate for
the controlled Prompt 4.6 disposable worksheet probe.

## Current status

- Worksheet 61 is quarantined after the wrong Terpenes-derived compatibility
  artifact was imported into its working draft. It has no versions and must
  not be used.
- Worksheet 62 is the disposable old-Sandbox probe. Version 1 was approved and
  activated only because the old Sandbox required an active worksheet for the
  controlled synthetic Batch assignment.
- The controlled import passed pre-save and post-reload verification: one
  `Probe` tab, 17 rows, 57 columns through `BE`, 15 named cells, nine required
  formula results/sentinels, the exact 64 writable cells, and no legacy
  Terpenes content.
- The actual worksheet 62 **Export Spreadsheet** file is preserved under
  `source/`.
- The replacement candidate under `dist/` was imported into worksheet 62 and
  saved as version 1 only after the controlled `Probe` layout passed the
  pre-save gate.
- A manual **Export Spreadsheet** download of the reopened saved version is
  preserved under `round_trip/`. The semantic comparison passed: formulas,
  named cells, data, and cell permissions are exact after excluding documented
  old-Sandbox runtime normalization.
- Scalar attempt 1 used nested update-style values; scalar attempt 2 used the
  corrected direct string/Number values. Both `QBBatchService.patchWorksheet`
  Previews completed their success callbacks but persisted no cell change.
  Each exact 969-cell grid comparison reported zero changed cells. The second
  result is recorded as a final old-Sandbox silent no-op; no third payload,
  range/matrix test, or Prompt 5 work was attempted.
- A manual Batch worksheet persistence control passed and restored the exact
  blank baseline. The Batch assignment audit also passed: active version 1,
  selected `Probe` tab, 15 named cells, exact scalar mappings, writable B2/B3,
  and working formulas.
- The exact-filename attachment-trigger diagnostic was classified `blocked`:
  the available browser control could not populate QBench's HTML file input,
  so no file was uploaded and no parser job or callback occurred. The parser
  was immediately deactivated, the temporary Batch context was removed, and
  the reusable Draft source was restored exactly. The complete post-cleanup
  969-cell comparison reported zero changes.
- The synthetic Batch and inactive Draft parser remain isolated under the
  `SBX_ONLY_TERPENES_2026_07_16_` prefix. No internal Batch or parser ID is
  recorded in this package.

## Build and validation

From this directory:

```text
python scripts/build_sandbox_probe_from_minimal_export.py
python scripts/validate_sandbox_probe_candidate.py
python scripts/compare_sandbox_probe_round_trip.py
python scripts/validate_scalar_patch_evidence.py
node --test tests/js/qbench_scalar_patch_probe.test.js
```

See `docs/sandbox_import_compatibility_issue.md` for the evidence and the
required QBench Sandbox verification gate. See
`docs/sandbox_scalar_patch_result.md` for the scalar callback and persisted-cell
evidence.
