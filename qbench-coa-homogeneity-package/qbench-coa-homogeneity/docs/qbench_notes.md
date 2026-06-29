# QBench Notes

## COA rendering

The COA uses Jinja and QBench rendering helpers.

Important pattern:

```jinja
{{QBTestService().render_worksheet(HOMOGENEITY_TEST, named_cell="report_results", ignore_empty_rows=true)}}
```

This means the Homogeneity worksheet must contain a named cell named `report_results` that points to the COA-ready table range.

## Pass/fail logic

The COA macro `get_test_pf_class(test)` reads:

```jinja
test.get_worksheet_value('pass_fail')
```

Therefore the Homogeneity worksheet must contain a `pass_fail` named cell that resolves to `Pass`, `Fail`, or blank/Not Tested.

## Homogeneity assay

Current COA mapping uses:

```jinja
'HOMOGENEITY': 11
```

Do not change this unless the QBench assay ID changes.

## Report asset

The updated COA source expects the 8-tile asset:

```text
hexagon-grid-8tile-1336x618.png
```

stored in QBench report config attachments.
