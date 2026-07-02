# Phase 2 COA Compatibility Report

Release folder:
`QBench/Releases/Homogeneity/2026-07-01/`

Worksheet JSON:
`homogeneity_phase1_production_candidate__2026-07-01.json`

COA sources checked:

- `COA format/COA Body Source Code.txt`
- `qbench-coa-homogeneity-package/qbench-coa-homogeneity/coa/coa_source_8tile_homogeneity_full.html`

No QBench changes were made.
No production QBench access was used.
No COA source files were modified.

## Compatibility Findings

| Check | Result | Evidence |
|---|---:|---|
| Homogeneity assay ID 11 is mapped | PASS | COA source contains `HOMOGENEITY`: `11` in `ASSAY_ID_MAP`. |
| COA references `HOMOGENEITY_TEST` | PASS | Existing comparison script reports `OK: COA references HOMOGENEITY_TEST`. |
| COA detail page renders `report_results` | PASS | COA source renders `QBTestService().render_worksheet(HOMOGENEITY_TEST, named_cell="report_results", ignore_empty_rows=true)`. |
| `report_results` exists in worksheet | PASS | Named cell `report_results` points to `COA!A1:G20`. |
| `report_results` range has content | PASS | Phase 1 validation report confirms the range is present and non-empty. |
| COA first-page tile uses worksheet `pass_fail` | PASS | COA macro `get_test_pf_class(test)` reads `test.get_worksheet_value('pass_fail')`. |
| COA calculates Homogeneity itself | PASS | No Homogeneity calculation formulas were found in the COA source; the COA displays worksheet output. |

## Current COA Pass/Fail Behavior

The current COA macro reads:

```jinja
{% set pass_fail = test.get_worksheet_value('pass_fail') or 'Not Tested' %}
{% set pf_class = 'not-tested' %}
{% set pf_class = 'pass' if pass_fail|trim|lower == 'pass' else pf_class %}
{% set pf_class = 'fail' if pass_fail|trim|lower == 'fail' else pf_class %}
```

The COA label map only includes:

```jinja
'fail': 'Fail'
'pass': 'Pass'
'not-tested': 'Not Tested'
```

Therefore, if the worksheet `pass_fail` value is `INCOMPLETE`, the current COA will treat it as `not-tested` and display `Not Tested` on the tile.

## Recommendation For Incomplete Worksheet State

Recommendation: use `Not Tested` as the COA-facing `pass_fail` value when `validation_status` is not `READY`.

Reason:

- The current COA expects only `Pass`, `Fail`, or `Not Tested`.
- Any value other than `Pass` or `Fail` is already normalized to the `not-tested` tile style.
- Returning `Not Tested` directly would make the worksheet output match the COA behavior.
- The worksheet can still expose the more specific `validation_status` value as `INCOMPLETE` for reviewer troubleshooting.

Suggested future worksheet expression:

```text
=IF(B42<>"READY","Not Tested",IF(COUNTIF(U12:U21,"FAIL")>0,"FAIL","PASS"))
```

Current Phase 1 worksheet expression:

```text
=IF(B42<>"READY","INCOMPLETE",IF(COUNTIF(U12:U21,"FAIL")>0,"FAIL","PASS"))
```

No `pass_fail` incomplete-state wording change has been made. Make this adjustment only if approved before Sandbox import.
