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
9. Confirm no dilution double application by comparing an already-applied case with an apply-in-QBench case.
10. Confirm `batch_qc_disposition = Hold` blocks report release.
11. Confirm `batch_qc_disposition = Rejected` blocks report release.
12. Confirm `publish_ready = FALSE` blocks report release.
13. Confirm Ocimene equals cis-Ocimene plus trans-Ocimene.
14. Confirm Nerolidol equals cis-Nerolidol plus trans-Nerolidol.
15. Confirm Total Terpenes equals the 23 internal channels exactly once.
16. Generate a COA preview.
17. Confirm the COA preview renders the 21-measurand table plus Total Terpenes from `report_results`.
18. Confirm there is no Terpenes status field, outcome tile, or compliance conclusion.
19. Confirm the report table fits the current COA layout.
20. Compare key values against independent manual calculations.
21. Confirm no production promotion occurs during testing.
