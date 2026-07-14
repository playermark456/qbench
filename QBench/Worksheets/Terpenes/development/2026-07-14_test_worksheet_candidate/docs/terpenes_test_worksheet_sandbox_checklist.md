# Terpenes Test Worksheet Sandbox checklist

Date: 2026-07-14

Use this checklist only in QBench Sandbox. Do not promote anything to production during Prompt 3 testing.

1. Import `dist/terpenes__test_ws_id_42__candidate_v1__2026-07-14.json` into QBench Sandbox as a worksheet candidate.
2. Attach the candidate to the intended Sandbox Terpenes assay/test.
3. Confirm the required named cells are visible, including `report_results`, `report_header`, `report_content`, `terpenes_instrument_conc`, `terpenes_results_mgg`, `terpenes_results_percent`, and the control/audit named cells.
4. Confirm the 23-channel input order in `Data!D2:Z2` matches the Prompt 2 config order.
5. Enter a controlled test-only data set in `Data!D2:Z2`.
6. Enter test-only sample mass and final volume values.
7. Confirm the default configuration gates block report output before any decisions are confirmed.
8. Confirm `calculation_ready` remains false until unit, preparation, mass, volume, and dilution prerequisites are satisfied.
9. Confirm nonnumeric sample mass, final volume, and applicable DF values block calculation.
10. Confirm zero or negative sample mass, final volume, and applicable DF values block calculation.
11. Confirm no dilution double application by comparing an already-applied case with an apply-in-QBench case.
12. Confirm `analytical_results_complete` is false with fewer than 23 numeric inputs or fewer than 23 numeric mg/g results.
13. Confirm parser/automation values arrive in `Data!D2:Z2` as actual numerical values recognized by QBench `ISNUMBER` and `COUNT`.
14. Confirm a numerical-looking text value such as `"10"` is not silently accepted if QBench stores it as text.
15. Confirm nonnumeric pasted input such as `abc`, `10 ug/mL`, or `N/A` produces `Review Required` without a spreadsheet calculation error.
16. Confirm all 23 parser-imported values satisfy `analytical_results_complete` only when QBench recognizes them as numbers.
17. If QBench automation writes numeric strings rather than numbers, record it as a blocking integration issue for Prompt 4/5 instead of adding worksheet coercion.
18. Confirm 23 numeric inputs, including legitimate zeros, can satisfy `analytical_results_complete` once calculated results are numeric.
19. Confirm invalid `below_loq_reporting_mode` values such as `approved`, `complete`, `x`, and blank block report release.
20. Confirm `display_less_than_loq` displays `<LOQ` only in Report result columns when the Specifications qualifier is `<LOQ`.
21. Confirm `display_numeric_result` displays numerical report results when the Specifications qualifier is `<LOQ`.
22. Confirm `batch_qc_disposition = Hold` blocks report release.
23. Confirm `batch_qc_disposition = Rejected` blocks report release.
24. Confirm `publish_ready = FALSE` blocks report release.
25. Confirm one missing Ocimene component leaves Total Ocimene blank.
26. Confirm one missing Nerolidol component leaves Total Nerolidol blank.
27. Confirm one missing internal channel leaves Total Terpenes blank.
28. Confirm Total Terpenes equals the 23 internal channels exactly once and does not add rollup rows again.
29. Generate a COA preview.
30. Confirm the COA preview renders the 21-measurand table plus Total Terpenes from `report_results`.
31. Confirm there is no Terpenes status field, outcome tile, or compliance conclusion.
32. Confirm the report table fits the current COA layout.
33. Compare key values against independent manual calculations.
34. Confirm no production promotion occurs during testing.
