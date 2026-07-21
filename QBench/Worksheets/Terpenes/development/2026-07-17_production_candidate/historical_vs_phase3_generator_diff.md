# Historical versus Phase 3 generator comparison

## Conclusion

Phase 3 did not select a different source export and did not replace the native root/config/worksheet envelope. It loaded each historical builder, called that builder's `build_candidate`, and continued to use the historical `update_worksheet`, `set_cell_metadata`, `style_range`, row, and column helpers.

The primary renderer-contract regression path was the final call to `freshen_uuids`: it recursively replaced the proven source namespace and every proven worksheet ID with deterministic UUIDv5 values after the workbook had been constructed. That behavior did not exist in either historical working generator. Phase 3 also populated formerly blank `csvFileName` fields, and its Test Report cell-map builder omitted two blank cells from the historical full 23x5 Report extent. Those changes were unnecessary renderer-sensitive divergences.

The failed Test v1 is the only Phase 3 production candidate that was imported in the interrupted Phase 4A attempt. Consequently, the association between the UUID/cell-extent/csv divergences and the observed collapse is strong but cannot be apportioned among those three fields without the authorized static v2 render test. The v2 path removes all three divergences together while retaining the approved scientific changes.

## Generator behavior comparison

| Area | Historical working pattern | Phase 3 v1 behavior | Classification | v2 treatment |
|---|---|---|---|---|
| Base source | Test starts from active id-42 export; Batch starts from active id-43 export | Same historical builders and same source exports | `proven_compatible_historical_pattern` | Preserved |
| Root/config envelope | Deep-copy native workbook; retain all root/config keys and value types | Same key set/order and types | `proven_compatible_historical_pattern` | Preserved and regression-tested |
| Namespace | Retain source namespace | Recursively replace with UUIDv5 | `likely_renderer_regression` | Historical namespace retained |
| Test worksheet IDs | Retain all three source IDs | Recursively replace all three with UUIDv5 | `likely_renderer_regression` | All historical IDs retained |
| Batch worksheet IDs | Three stable builder IDs plus the retained source Publish ID | Recursively replace all four with UUIDv5 | `likely_renderer_regression` | Historical IDs retained; renamed tabs keep their corresponding historical IDs |
| Worksheet object construction | Mutate deep-copied source/template worksheet objects through historical helper | Same historical object construction before the final identity rewrite | `proven_compatible_historical_pattern` | Preserved |
| Worksheet object keys | Native 34-key worksheet object | Exact same key set/order | `proven_compatible_historical_pattern` | Exact equality tested |
| `cells` entry shape | `readonly`, `type`, `width`, `x` | Same four fields and JSON types | `proven_compatible_historical_pattern` | Exact equality tested |
| Test Report cell extent | Full 23x5 map (115 entries), including two blank total-row cells | Sparse non-empty map (113 entries) | `likely_renderer_regression` | Historical full Report extent restored |
| Test Data/Specifications cell selection | Used, formula, input, and controlled regions | New approved layouts construct non-empty/formula cells and reserve all 43 blank destinations | `intentional_business_logic_change` | Retained; every destination and formula remains explicitly represented |
| Batch cell maps | Complete historical table maps | Historical maps retained | `proven_compatible_historical_pattern` | Preserved |
| `colElement` / `element` | Absent | Absent | `proven_compatible_historical_pattern` | Absence preserved |
| `readonly` | JSON booleans | JSON booleans | `proven_compatible_historical_pattern` | Type and formula ownership tested |
| Columns | List of `{type: "text", width: integer}` | Same representation; Test widths changed for the new layout | `intentional_business_logic_change` | Representation preserved |
| Rows | List of `{height: 27}` | Same representation; counts follow new grids | `intentional_business_logic_change` | Representation preserved |
| `minDimensions` | `[max_columns, row_count]` | Same calculation; Test values changed with approved grids | `intentional_business_logic_change` | Exact dimension relationship tested |
| `tableHeight` / `tableWidth` | Explicit integers | Batch unchanged; Test values track the new layout | `intentional_business_logic_change` | Explicit integer fields retained |
| Formula serialization | Plain strings beginning with `=` | Same serialization | `proven_compatible_historical_pattern` | Type/prefix and formula ownership tested |
| Formula sheet-name casing | Uppercase Test sheet references; quoted Batch names where required | Test stays uppercase; renamed Batch references are rewritten consistently | `intentional_business_logic_change` | Validated with no stale `QC Review`/`Publish` references |
| Top-level `data` | Exact duplicate of each final worksheet `data`, in worksheet order | Explicitly rebuilt and synchronized | `proven_compatible_historical_pattern` | Exact equality tested |
| Named cells | Objects with `cell`, `display_name`, boolean `export` | Same serialization; Test replaced with 43 destinations plus `report_results`; Batch retained 67 with renamed tab targets | `intentional_business_logic_change` | Scientific/schema validators enforce exact contracts |
| `report_results` | `Report!A1:E23` | Same | `proven_compatible_historical_pattern` | Preserved |
| Styles | Cell references to integer style indexes | Same representation; new layouts use historical indexes | `proven_compatible_historical_pattern` | Key/value types tested |
| Conditional formatting | Empty rules in generated historical candidates | Empty | `proven_compatible_historical_pattern` | Preserved |
| Key/Value config | Empty in generated historical candidates | Empty; worksheet formulas contain sanitized runtime binding placeholders | `intentional_business_logic_change` | Preserved |
| `csvFileName` | Empty string | Phase 3 populated target-specific filenames | `likely_renderer_regression` | Historical empty-string behavior restored |
| Default/null/empty values | Native types retained | Retained apart from intentional payload updates and `csvFileName` | `harmless_metadata_change` for payload text; `likely_renderer_regression` for `csvFileName` | Historical renderer-sensitive defaults retained |

## Output-level summary

### Test

- Historical: 3 tabs; dimensions Report 23x5, Data 38x26, Specifications 30x8; 91 named cells.
- Failed Phase 3 v1: 3 tabs; dimensions Report 23x5, Data 40x26, Specifications 23x21; 44 named cells (43 destinations plus `report_results`).
- Root/config/worksheet key shapes and cell-entry shapes match.
- Namespace and all worksheet IDs differ solely because of `freshen_uuids`.
- The Phase 3 grid, formulas, named-cell replacement, LOQ/MU logic, combined analytes, and report surface are approved business changes, not treated as the renderer cause merely because their content differs.

### Batch

- Historical: Run Setup 25x3, Instrument Import 201x57, QC Review 45x24, Publish 87x56; 67 named cells.
- Phase 3 v1: identical dimensions and counts; `QC Review` became `Batch Review`, `Publish` became `Test Transfer`, and formulas/named targets were consistently renamed.
- Namespace and all worksheet IDs differ solely because of `freshen_uuids`; `csvFileName` changed from empty to target-specific.
- The unit/dilution, tab-name, control-record exclusion, and transfer-gate changes are intentional business logic.

## Corrected code path

`build_phase3_candidates.py` now exposes an explicit `preserve_historical_identity` mode without changing its default v1 behavior. `build_phase3_candidates_v2.py` calls the same historical builders and approved Phase 3 scientific builders with that mode enabled. It verifies the historical namespace and worksheet-ID mapping before writing either v2 file. The Test v2 path also restores the historical full Report cell extent; both v2 paths leave `csvFileName` at the historical empty string.

No historical helper function was rewritten. The corrected path reuses:

- Test and Batch `build_candidate`;
- `update_worksheet`;
- `worksheet_from_template` for Batch;
- `set_cell_metadata`;
- `style_range`;
- `row_meta` and `column_meta`;
- the historical JSON serialization types and worksheet envelopes.

The only changes to the Phase 3 wrapper are controlled parameters selecting the proven identity/default behavior. Failed v1 output hashes remain unchanged.
