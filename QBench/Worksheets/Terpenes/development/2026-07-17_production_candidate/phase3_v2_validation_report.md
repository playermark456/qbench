# Phase 3 v2 local validation

- `scientific_logic_validation = passed`
- `worksheet_schema_validation = passed`
- `historical_renderer_compatibility = passed`

## Proven historical sources

- Test generator commit: `443fa40809347114d543f442493dae6c55fc8f22`.
- Batch generator commit: `28cd4f17db96f2c78dd60cba84c490d9e87a6dde`.
- Test source worksheet: `QBench/Rescans/2026-07-04/Worksheets/Terpenes/terpenes__id_42__worksheet_export_spreadsheet__active__2026-07-04.json`; SHA-256 `1ff46aadc31c32b8b176f3eb0091c8ae26d905271fcbc4f1a118a3776f7820e9`.
- Batch source worksheet: `QBench/Rescans/2026-07-04/Worksheets/Terpenes/terpenes__id_43__worksheet_export_spreadsheet__active__2026-07-04.json`; SHA-256 `db6bfe7a7d306902b78c27af76b4a08a2a17b7d974f63c5593a3455e109bad07`.
- Historical Test helper: `QBench/Worksheets/Terpenes/development/2026-07-14_test_worksheet_candidate/scripts/build_terpenes_test_worksheet.py`; canonical merge-commit SHA-256 `0164d0c8a6014a3cc9a95c33d52b5a1250e6f308caa037b6a1bfed580d667883`.
- Historical Batch helper: `QBench/Worksheets/Terpenes/development/2026-07-14_batch_worksheet_candidate/scripts/build_terpenes_batch_worksheet.py`; canonical merge-commit SHA-256 `1b4bcf3a20cb3faa3e56cd36d82006f528261e7a96f3d5efe2cec01a54345772`.
- Corrected v2 builder: `QBench/Worksheets/Terpenes/development/2026-07-17_production_candidate/build_phase3_candidates_v2.py`; SHA-256 `667889e1c862e6b520931a6dc98c99cc3e218f1c40a6cd23837f9a37e1e39181`.

## Candidate results

- Test v2: `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v2.json`; SHA-256 `7aa7469ec7767a7c7b4b0aa40194e927244adc3278999e23151f4eeb134dd5a4`.
- Test tabs/dimensions: `{'Report': (23, 5), 'Data': (40, 26), 'Specifications': (23, 21)}`; named cells `44`; formulas `309`.
- Batch v2: `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS__v2.json`; SHA-256 `a4b92be3590e57f3456e12c65219cb6a5cb340248c6f3e50c6d3f36f56777837`.
- Batch tabs/dimensions: `{'Run Setup': (25, 3), 'Instrument Import': (201, 57), 'Batch Review': (45, 24), 'Test Transfer': (87, 56)}`; named cells `67`; formulas `1180`.
- Scientific calculation vectors: `41` rows; synthetic Total Terpenes `1040 ug/g`.

## Renderer-sensitive regression contract

- Test: `{'namespace_preserved': True, 'worksheet_ids_preserved': True, 'worksheet_key_shapes_preserved': True, 'cell_entry_shapes_preserved': True, 'data_mirroring_preserved': True, 'formula_count': 309, 'style_indexes': [1, 2, 4, 5, 7, 9, 17, 23]}`.
- Batch: `{'namespace_preserved': True, 'worksheet_ids_preserved': True, 'worksheet_key_shapes_preserved': True, 'cell_entry_shapes_preserved': True, 'data_mirroring_preserved': True, 'formula_count': 1180, 'style_indexes': [0, 1, 2]}`.
- The proven source namespace and worksheet IDs are retained; the v1 UUIDv5 rewrite is absent.
- Root/config/worksheet key shapes, worksheet defaults, cells entry shape, boolean readonly values, row/column representations, minDimensions, formula strings, style indexes, named-cell entry shape, and duplicate data mirrors passed.

## Regression matrix

- v2 renderer-compatibility tests: 13/13 passed.
- Existing Phase 3 v1 validator: passed; both failed v1 SHA-256 values unchanged.
- Prompt 2 configuration/parser tests: 27/27 passed.
- Historical Test reproduction: byte-for-byte; validator passed; 50/50 tests passed.
- Historical Batch reproduction: byte-for-byte; validator passed; 39/39 tests passed.
- Wide-adapter tests: 13/13 Python and 143/143 JavaScript passed; package validator passed.
- Native-probe tests: 17/17 Python and 48/48 JavaScript passed; 45-artifact package validator passed in the exact manifest-byte workspace.
- No-code parser package validator: passed.
- Prompt 5 automation package validator: passed in the exact mixed-line-ending manifest workspace.
- Prompt 5B publisher tests: 46/46 passed; no request-capable command was run.

## Safety

- Failed v1 candidate bytes remain unchanged.
- No credential, token, authorization header, URL, signed URL, Pass/Fail artifact, or customer data was found.
- No QBench environment was accessed and no Sandbox object was modified.
