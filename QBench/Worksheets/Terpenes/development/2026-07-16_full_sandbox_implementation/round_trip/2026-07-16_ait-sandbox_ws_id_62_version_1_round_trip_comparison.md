# Worksheet 62 version 1 round-trip comparison

Date: 2026-07-16

Environment: `https://ait-sandbox.qbench.net/`

Worksheet: 62 `SBX_ONLY_TERPENES_2026_07_16_Probe_Minimal_Runtime_Baseline`

Saved version at export time: version 1, status `DRAFT`

## Files

- Imported candidate:
  `../dist/qbench_runtime_probe_batch_ws_candidate__ait_sandbox_runtime.json`
- Saved-version **Export Spreadsheet** file:
  `2026-07-16_ait-sandbox_ws_id_62_version_1_draft_export_spreadsheet.json`
- Candidate SHA-256:
  `af31d5b5ad44d3c35ccb2b3a5d18ec01b504aea31463570b72e38725cf64fe9c`
- Saved export SHA-256:
  `2f3b2b17beae2c3361b2cfcccfde121aeb4ed32757127806864d2c2b2da63d19`

The two manual downloads, `spreadsheet-export-template (10).json` and
`spreadsheet-export-template (11).json`, were byte-identical. The later copy
was preserved without modification under the saved-version export filename.

## Result

Semantic round-trip status: **PASS**

The saved export preserves exactly:

- one worksheet named `Probe`;
- 17 rows and 57 columns through `BE`;
- the nine required formulas in `config.worksheets[0].data`;
- all 15 named cells and ranges in `qb_config`;
- the complete cell configuration, including the exact writable/read-only
  settings;
- all non-formula worksheet data; and
- the absence of legacy Terpenes content.

The saved export differs only in old-Sandbox runtime-managed fields:

- the runtime regenerated `config.namespace`;
- worksheet management flags were normalized from `false` to `true`;
- viewport values were normalized from `2200x720` to `1588x350`;
- `minDimensions` was serialized as `[1, 1]` even though the worksheet data,
  columns, rows, and visible grid remain 17x57;
- empty `style` objects were added; and
- the top-level `data.Probe` cache contains the evaluated results of the nine
  formulas, while the authoritative worksheet data retains the formulas.

No unclassified difference was found. The comparison was run with
`scripts/compare_sandbox_probe_round_trip.py`.

Worksheet 62 remains an inactive, unattached draft. Worksheet 61 remains
quarantined. No scalar patch was run as part of this round-trip check.
