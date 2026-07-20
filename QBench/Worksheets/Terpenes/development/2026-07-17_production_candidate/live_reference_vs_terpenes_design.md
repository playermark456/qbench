# Live reference patterns versus the Terpenes proposal

## Adopted implementation patterns

| Live implementation pattern | Terpenes documentation proposal | Boundary |
| --- | --- | --- |
| Dedicated input, calculation/review, report, and technical/audit layers | Test tabs: Report, Data, Specifications, Audit, METRC | No formulas until the remaining component preprocessing rule is approved. |
| Compact named COA range with headers | `report_results = Report!A1:E23` | One header, 21 reportable measurands, and Total Terpenes. |
| Blank/error guards around formula-owned cells | Future source-absent → blank and denominator guards | Shape only; no equation or constant copied. |
| Qualified addresses in multi-tab definitions | Qualified logical addresses for multi-tab documentation | Old-Sandbox one-tab JSON import remains unqualified where proven. |
| Read-only/hidden technical columns | Formula-owned and audit-only fields are visually distinct and protected | Hidden content must remain reviewable and exportable. |
| Parser and automation definitions are separate objects | Raw Import, Normalized Import, Review, Transfer, Audit responsibilities | Transfer remains manual/reviewable until authorized. |
| Fresh UUID-backed worksheets with preserved renderer metadata | Generate fresh UUIDs from a target-generation export base | No candidate JSON created in this phase. |

## Explicitly rejected patterns

- Another assay's equations, concentration units, dilution factors, LOQ thresholds, rounding, MU, analyte rollups, result qualifiers, METRC mappings, or Pass/Fail logic.
- The live-labeled Terpenes definition artifact as proof of an operational or authoritative Terpenes workflow.
- Legacy one-sheet Batch definitions as the target polished architecture.
- Automation names as proof of automation bodies, atomicity, or error behavior.
- A blank or hidden report row as proof of report-template empty-row suppression.
- Any formula placeholder inside QBench.

## Remaining authoritative marker

- `TERPENES_COMPONENT_PREPROCESSING_RULE_UNRESOLVED`

The unit, dilution, conversions, 21-measurand mapping, reportable-analyte `<LOQ` qualifier, Key/Value Store dimensions, MU method, Total Terpenes rule, rounding, and Metrc routing are resolved. Only the missing/negative/below-threshold component-channel numeric treatment remains. This marker is documentation-only and must not be put into QBench.

`calculation_contract = blocked_missing_authoritative_requirement`
