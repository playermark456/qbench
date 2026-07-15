# Terpenes Batch Worksheet Sandbox checklist

Date: 2026-07-14

Do not configure Prompt 5 automation until this checklist is successfully completed and reviewed in QBench Sandbox.

1. Import `dist/terpenes__batch_ws_id_43__candidate_v1__2026-07-14.json` into QBench Sandbox only.
2. Confirm the tab order is `Run Setup`, `Instrument Import`, `QC Review`, `Publish`.
3. Confirm the `Publish` tab preserved the intended 86 QBench test rows.
4. Confirm QBench test/sample placeholders populate correctly on representative batches.
5. Confirm all named cells and ranges are visible.
6. Confirm Run Setup required fields match the B2:B25 field map and that blank required fields report the correct first missing message.
7. Confirm `batch_publish_ready` stays false and `batch_publish_message` reports `Run setup incomplete` until Run Setup is complete.
8. Paste normalized parser output into `Instrument Import`.
9. Confirm numeric fields are recognized by `ISNUMBER` and `COUNT`.
10. Confirm numerical-looking text such as `24`, `23`, `34`, and `10` stored as text is not silently accepted.
11. Confirm Compound Results row count 24, Peak Table row count numeric/nonnegative, reportable analyte count 23, Dimethylacetamide numeric, and unknown peak count numeric/nonnegative are required.
12. Confirm Dimethylacetamide is retained as an audit value and is not reportable.
13. Confirm Peak Table audit behavior does not populate final quantitative values.
14. Confirm unknown Peak Table rows require chromatographic review but do not become quantitative values.
15. Confirm manual integration requires a reason.
16. Confirm QC boundary formulas for calibration, CCV, blank, LOQ recovery, matrix spike, duplicate, retention-time drift, and resolution.
17. Confirm negative RSD, blank fraction, duplicate difference, and RT drift do not evaluate within criteria.
18. Confirm unresolved bracketing CCV blocks release and only `decision_required` or `confirmed` are controlled bracketing statuses.
19. Confirm `lcs_requirement_status = decision_required` blocks QC configuration.
20. Confirm one `outside_criteria`, `decision_required`, `not_evaluated`, or `review_required` overall analyte QC evaluation blocks `qc_review_complete`.
21. Confirm `Hold` and `Rejected` batch dispositions block batch publication.
22. Confirm `Accepted` alone is insufficient without all other gates.
23. Confirm duplicate Test IDs are blocked.
24. Confirm missing source hashes are blocked.
25. Confirm one missing analyte is blocked.
26. Confirm numeric zero remains valid for analyte values.
27. Confirm a valid complete Publish row becomes transfer-ready only when `batch_publish_ready` is true.
28. Confirm Publish column A is QBench Test ID and column B is QBench Sample ID per the controlled column-contract decision.
29. Confirm the Publish surface contains no calculated final sample mg/g, percent, qualifier, total, COA, or METRC value.
30. Confirm no Terpenes Pass/Fail field or conclusion exists.
31. Compare Publish values against the normalized parser output.
32. Confirm no production promotion occurs during Sandbox testing.
