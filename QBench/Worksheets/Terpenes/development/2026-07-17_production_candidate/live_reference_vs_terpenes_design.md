# Live reference patterns versus the Terpenes implementation

## Adopted implementation patterns

| Sanitized implementation pattern | Terpenes Phase 3 implementation | Boundary |
| --- | --- | --- |
| Separate input, calculation/review, and report layers | Test tabs: Report, Data, Specifications | Scientific rules come only from the approved Terpenes contract. |
| Compact named COA range with headers | `report_results = Report!A1:E23` | One header, 21 reportable measurands, and Total Terpenes. |
| Blank/error guards around formula-owned cells | Source-absent guards, positive-component preprocessing, denominator and missing-MU guards | No equation or constant was copied from another assay. |
| Qualified addresses in multi-tab definitions | Exact logical addresses such as `Data!D2` and `Report!A1:E23` | The historical one-tab old-Sandbox unqualified-address exception remains separate. |
| Read-only technical formula cells | Protected, visually distinct Specifications calculations and Batch AF/AG columns | Technical content remains reviewable and exportable. |
| Separate import, review, and transfer responsibilities | Batch tabs: Run Setup, Instrument Import, Batch Review, Test Transfer | Transfer is manual/reviewable; no automatic publication or QC Review. |
| Fresh UUID-backed worksheet definitions | Deterministic fresh UUIDs, disjoint from the sanitized structural sources | No source-specific UUID is retained. |

## Explicitly rejected patterns

- Another assay's equations, units, dilution factors, LOQ thresholds, rounding, MU, analyte rollups, result qualifiers, Metrc mappings, or Pass/Fail logic.
- A live-labeled Terpenes definition as proof of an operational or authoritative workflow.
- Legacy one-sheet Batch definitions as the polished target architecture.
- Automation names as proof of automation bodies, atomicity, or error behavior.
- Component-channel LOQ filtering or adding component LOQs.
- Any unresolved placeholder inside a scientific calculation.

## Current calculation boundary

The user-approved rule resolves the final component preprocessing behavior. Missing, blank, no-peak, zero, and negative Ocimene/Nerolidol components contribute zero; positive numeric components contribute at full precision. Only the combined reportable result receives an LOQ comparison. Combined MU requires values only for positive contributors.

`calculation_contract = passed_authoritative_method_documentation_and_user_approved_reporting_rules`

Local candidate generation is complete. No QBench environment was accessed during Phase 3 generation; isolated Sandbox runtime validation is the next controlled gate.
