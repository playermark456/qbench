# Terpenes Batch Worksheet Sandbox checklist

Date: 2026-07-14

Do not configure Prompt 5 automation until this checklist is successfully completed and reviewed in QBench Sandbox.

1. Import `dist/terpenes__batch_ws_id_43__candidate_v1__2026-07-14.json` into QBench Sandbox only.
2. Confirm the tab order is `Run Setup`, `Instrument Import`, `QC Review`, `Publish`.
3. Confirm the `Publish` tab preserved the intended 86 QBench test rows.
4. Confirm QBench test/sample placeholders populate correctly on representative batches.
5. Confirm all named cells and ranges are visible.
6. Paste normalized parser output into `Instrument Import`.
7. Confirm numeric fields are recognized by `ISNUMBER` and `COUNT`.
8. Confirm numerical-looking text such as `10` stored as text is not silently accepted.
9. Confirm Compound Results row count 24 and reportable analyte count 23 are required.
10. Confirm Dimethylacetamide is retained as an audit value and is not reportable.
11. Confirm Peak Table audit behavior does not populate final quantitative values.
12. Confirm unknown Peak Table rows require chromatographic review but do not become quantitative values.
13. Confirm manual integration requires a reason.
14. Confirm QC boundary formulas for calibration, CCV, blank, LOQ recovery, matrix spike, duplicate, retention-time drift, and resolution.
15. Confirm unresolved bracketing CCV blocks release.
16. Confirm `Hold` and `Rejected` batch dispositions block batch publication.
17. Confirm `Accepted` alone is insufficient without all other gates.
18. Confirm duplicate Test IDs are blocked.
19. Confirm missing source hashes are blocked.
20. Confirm one missing analyte is blocked.
21. Confirm numeric zero remains valid for analyte values.
22. Confirm a valid complete Publish row becomes transfer-ready only when `batch_publish_ready` is true.
23. Confirm the Publish surface contains no calculated final sample mg/g, percent, qualifier, total, COA, or METRC value.
24. Confirm no Terpenes Pass/Fail field or conclusion exists.
25. Compare Publish values against the normalized parser output.
26. Confirm no production promotion occurs during Sandbox testing.
