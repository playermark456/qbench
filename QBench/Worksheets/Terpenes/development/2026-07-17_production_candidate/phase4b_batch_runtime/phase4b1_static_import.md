# Phase 4B.1 native import and static render

Date: 2026-07-21

- The exact Batch v2 JSON was selected through QBench's native Import Spreadsheet workflow.
- The user confirmed the manual file-selection gate with `batch-file-selected`.
- Submit was executed once.
- JSON Editor View was not used.
- The workbook rendered without a one-cell fallback.
- Tabs and order: Run Setup, Instrument Import, Batch Review, Test Transfer.
- Dimensions: Run Setup 25x3; Instrument Import 201x57; Batch Review 45x24; Test Transfer 87x56.
- Default Sheet1 was absent.
- Instrument Import visibly extended through column BE and row 201.
- The 23 terpene channels, audit columns, Dimethylacetamide audit field, and Peak Table audit/QC fields were present.
- AF and AG rendered as readonly formula-owned cells while adjacent parser-write cells remained writable.
- Batch Review and Test Transfer remained distinct.
- No Pass/Fail or automatic Publish/QC Review action appeared.

`batch_v2_static_render = passed`
