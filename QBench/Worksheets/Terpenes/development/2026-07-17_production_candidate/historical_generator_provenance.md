# Historical Terpenes worksheet-generator provenance

This record establishes the earlier Codex generator implementations as the local renderer-compatibility baseline. It does not claim a new QBench renderer contract and does not record any new QBench access.

## Reproduction result

| Candidate | Historical implementation | Isolated reproduction | Committed output |
|---|---|---|---|
| Test | merge commit `443fa40809347114d543f442493dae6c55fc8f22` (candidate lineage begins at `ea8668a74b6aae6a3a660963d85748ce3dc0ae92`) | `historical_test_reproduction = passed`; generator completed, validator passed, and 50/50 historical tests passed | Byte-for-byte match, SHA-256 `90686b980882b221008f281be33984dc5232e2f3d2632300db3f4a27b529640a` |
| Batch | merge commit `28cd4f17db96f2c78dd60cba84c490d9e87a6dde` (candidate lineage begins at `aaec1294c3ca521ddcc928e0e7fdbb05d6a64f0e`) | `historical_batch_reproduction = passed`; generator completed, validator passed, and 39/39 historical tests passed | Byte-for-byte match, SHA-256 `e5c80b1213396cab4932e267fd786c6986c933d4b404f11daa5c5aba0629758e` |

The reproductions ran from full Git archives of the two merge commits outside the current worktree. No current-branch source was substituted into either reproduction. All manifest source/dependency hashes passed.

## Test Worksheet generator

- Generator: `QBench/Worksheets/Terpenes/development/2026-07-14_test_worksheet_candidate/scripts/build_terpenes_test_worksheet.py`.
- Historical helper-module SHA-256 at the merge commit: `0164d0c8a6014a3cc9a95c33d52b5a1250e6f308caa037b6a1bfed580d667883`.
- Source JSON: `QBench/Rescans/2026-07-04/Worksheets/Terpenes/terpenes__id_42__worksheet_export_spreadsheet__active__2026-07-04.json`.
- Source SHA-256: `1ff46aadc31c32b8b176f3eb0091c8ae26d905271fcbc4f1a118a3776f7820e9`.
- Construction method: deep-copy the entire source workbook, preserve its config envelope, then replace the data/style/cells/row/column payloads on its existing `Report`, `Data`, and `Specifications` worksheet objects by calling `update_worksheet`.
- Namespace: retained from the source (`62ed4a22-0051-4d05-97f1-fe86cc75adab`).
- Worksheet IDs: all three source IDs were retained: `Report` `cdb783ce-dea5-4779-9246-a0ab1b5b9eb6`, `Data` `562c5dc7-b622-4bf0-a9de-01e3d9076392`, and `Specifications` `415aa1f9-b0fd-4256-9bb2-ebbc917179d0`.
- New worksheet IDs: none.
- Cell metadata: `set_cell_metadata` emits exactly `readonly`, `type`, `width`, and `x`; readonly is a JSON boolean. Each tab builder selected its used/formula/input regions, and the Report tab emitted the full 23x5 cell extent.
- Rows/columns: `row_meta` emits one `{height: 27}` object per row; `column_meta` emits one `{type: "text", width: integer}` object per column.
- Dimensions: `update_worksheet` recalculates `[column_count, row_count]` in `minDimensions` and assigns explicit `tableWidth` and `tableHeight`.
- Mirrored data: after the three worksheet objects were updated, each corresponding top-level `data[tab_name]` value was replaced with the worksheet data.
- Formulas: plain JSON strings beginning with `=`; sheet references used the historical uppercase `DATA` and `SPECIFICATIONS` conventions.
- Named cells: the source named-cell dictionary was deep-copied, then new entries were added as objects with exactly `cell`, `display_name`, and boolean `export`.
- Styles: cell-reference keys mapped to integer style indexes using the historical `style_range` helper.

## Batch Worksheet generator

- Generator: `QBench/Worksheets/Terpenes/development/2026-07-14_batch_worksheet_candidate/scripts/build_terpenes_batch_worksheet.py`.
- Historical helper-module SHA-256 at the merge commit: `1b4bcf3a20cb3faa3e56cd36d82006f528261e7a96f3d5efe2cec01a54345772` (canonical Git-archive bytes).
- Source JSON: `QBench/Rescans/2026-07-04/Worksheets/Terpenes/terpenes__id_43__worksheet_export_spreadsheet__active__2026-07-04.json`.
- Source SHA-256: `db6bfe7a7d306902b78c27af76b4a08a2a17b7d974f63c5593a3455e109bad07`.
- Construction method: deep-copy the entire source workbook. `worksheet_from_template` deep-copied the source `Sheet1` worksheet four times, preserved the worksheet object envelope/default fields, cleared transient collections, and then `update_worksheet` replaced the payload fields.
- Namespace: retained from the source (`1c196e88-c38b-4cc8-ab59-98d46f8943c8`).
- Retained worksheet ID: the output `Publish` tab retained source `Sheet1` ID `c97d47f0-0159-4998-93c3-3fd6abb80b86`.
- New worksheet IDs: stable builder constants created `Run Setup` `cf71364f-84b3-4558-a14c-241b452bd7bb`, `Instrument Import` `f11a5887-6f11-4a45-ae16-9a0f9f64dd16`, and `QC Review` `adc806c8-3a02-4c6f-b8c6-6738df2fe02d`.
- Cell metadata, rows, columns, dimensions, formula strings, named-cell objects, and integer style indexes use the same helper shapes described above. The Batch builders intentionally emit complete cell maps for its table surfaces.
- Mirrored data: top-level `data` was rebuilt in worksheet order from the final worksheet data.

## Config and default-field preservation

Both builders preserved the root order `config`, `qb_config`, `data`, the complete config envelope, and the complete worksheet-object key set. They retained native default, null, empty-string, list, and object types unless a field was intentionally replaced. Both cleared conditional-formatting rules and Key/Value config for their controlled candidate scope.

## Post-import export evidence

The repository contains the original generated candidates, manifests, validators, tests, and later notes about their QBench behavior. It does not contain a tracked **Export Spreadsheet** round-trip file whose bytes are proven to be a post-import export of either exact historical generated file. The user has confirmed that these Codex-generated files rendered correctly; a subsequent exact QBench export is therefore classified `not_present_in_tracked_evidence`, not assumed.
