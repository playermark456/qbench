# QBench parser Sandbox validation checklist

Use this only after the QBench runtime contract is proven and a Sandbox-only
inactive/draft parser candidate is created.

1. Confirm the parser remains inactive/draft.
2. Upload only the redacted `.txt` fixture.
3. Confirm one Instrument Import row is created.
4. Confirm AH:BD contains 23 numeric values.
5. Confirm counts are numeric: 24 Compound Results, 34 Peak Table, 23 reportable.
6. Confirm Dimethylacetamide is numeric and audit-only.
7. Confirm unknown Peak Table count is correct.
8. Confirm source hashes are populated.
9. Confirm source metadata is populated.
10. Confirm AF and AG formulas are not overwritten.
11. Confirm AF evaluates to `Valid`.
12. Confirm AG evaluates to `Import row valid`.
13. Confirm no spreadsheet errors.
14. Confirm no Test Worksheet write.
15. Confirm no Publish write before reviewed selection.
16. Confirm no QC Review write.
17. Confirm no Terpenes Pass/Fail output or conclusion.
18. Confirm malformed file rejection leaves no partial write.
19. Confirm the same source injection cannot be reused under another Test ID;
    duplicate `source_row_hash` is blocked.
20. Confirm duplicate source file hashes are reported.
21. Confirm multiple legitimate injections for one Test ID require explicit
    selection and do not auto-average or auto-select.
22. Confirm reviewed-row Publish preview requires exact `ug/mL`,
    row-specific review evidence, matching `source_row_hash`, and QBench Test ID
    to Publish-row mapping.
23. Confirm Publish preview AF, AG, and AV output exact text `"TRUE"`, not
    Boolean true.
24. Confirm missing, blank, or unsupported source filenames are rejected.
25. Confirm any invalid selected row blocks the entire multi-row preview.
26. Confirm no production activation.
