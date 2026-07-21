# Phase 4A.5 Report tab validation

Date: 2026-07-21

`environment_profile = sandbox_runtime_only`

The fresh Test instantiated the expected Report tab from V3. The saved definition retains headers `Analyte`, `Result (mg/g)`, `Result (%)`, `LOQ`, and `MU (%)`; 21 reportable analytes; Total Terpenes; and `report_results = Report!A1:E23`. Raw component channels, Dimethylacetamide, Peak Table fields, and Pass/Fail are absent from the report contract.

Runtime result and total validation was not performed because the required pre-entry Key/Value lookup gate failed. No COA preview was generated.
