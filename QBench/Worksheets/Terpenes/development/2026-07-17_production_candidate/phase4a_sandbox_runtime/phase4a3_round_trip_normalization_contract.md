# Phase 4A.3 QBench round-trip normalization contract

Date: 2026-07-21

## Revised classification

`test_v2_round_trip = passed_with_expected_qbench_normalization`

The Phase 4A.2 raw saved/reopened export passed the revised comparator. The comparator found three worksheets, 44 named definitions, 309 exact embedded formulas, 309 allowed evaluated top-level formula-cache values, and 1,329 exact non-formula top-level values.

## Representation contract

- `authoritative_formula_representation = config.worksheets[*].data`
- `top_level_data_representation = qbench_evaluated_display_cache`
- `minDimensions = qbench_normalized_editor_minimum_not_actual_content_extent`
- `tableWidth_and_tableHeight = qbench_normalized_editor_viewport`

The local v2 candidate remains the source candidate and is not rewritten to imitate a saved QBench export.

## Exact comparisons

The comparator requires exact worksheet names/order, embedded worksheet data and formulas, actual embedded and top-level array dimensions, rows, columns, cell metadata, styles, number formats, protection, hidden rows/columns, named cells, `report_results`, Key/Value formulas, and all non-formula top-level values.

## Narrow normalization allowances

The comparator permits only:

1. a QBench-generated namespace;
2. `minDimensions` changing from the candidate extent to `[1, 1]`;
3. positive numeric `tableWidth`/`tableHeight` values representing the current editor viewport; and
4. a top-level formula string becoming a scalar evaluated display value when the corresponding embedded cell retains the exact original formula.

It does not permit an embedded formula change, missing formula, changed non-formula value, moved named cell, changed metadata/style/protection, or changed actual array extent.

## Tests

- The observed QBench normalization passes.
- A changed embedded formula fails.
- A changed non-formula top-level value fails.
- The real ignored Phase 4A.2 export passes with 309/309 embedded formulas exact.
