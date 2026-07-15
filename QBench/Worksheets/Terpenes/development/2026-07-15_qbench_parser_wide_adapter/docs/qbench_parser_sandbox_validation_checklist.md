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
19. Confirm duplicate source file detection.
20. Confirm multiple injections for one Test ID require explicit selection.
21. Confirm reviewed-row Publish preview matches Prompt 4 D:AX contract.
22. Confirm no production activation.
