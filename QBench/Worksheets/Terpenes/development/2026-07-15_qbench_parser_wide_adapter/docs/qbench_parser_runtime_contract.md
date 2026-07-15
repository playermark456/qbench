# QBench parser runtime contract

## Current contract state

The native QBench wrapper is blocked. Repository evidence proves only a visible
parser-library import URL from an existing Code parser. It does not prove the
runtime API needed to safely read a file, produce output, or write a worksheet.

## Implemented local contract

The local parser core accepts:

- UTF-8 text or bytes, with or without BOM.
- LF or CRLF line endings.
- Prompt 2 analyte configuration.
- Controlled security limits.

The local wide adapter emits:

- One logical Instrument Import row per injection.
- 57 A:BE columns.
- QBench-neutral write blocks for A:AE and AH:BE.
- Explicit exclusion of AF and AG.
- JavaScript Number values for numeric fields.

The local reviewed Publish adapter emits:

- A D:AX preview patch only after row-specific review evidence keyed by
  `source_row_hash`.
- Exact `labsolutions_conc_unit === "ug/mL"` validation; blank, case-changed,
  or alternate units are blocked.
- Explicit QBench Test ID to Publish-row mapping.
- Atomic multi-row preview behavior with no partial write plan.
- No AY or later formula/control writes.
- No direct Test Worksheet, Publish worksheet, QC Review, COA, METRC, or
  automation execution.

## Runtime blockers

The following QBench facts must be inspected read-only before a native wrapper
can become a Sandbox installation candidate:

1. Exact Code File Parser entry function name and signature.
2. Exact input file object shape.
3. Exact text or byte access method.
4. Exact output/return API.
5. Exact worksheet write API, including tab/range targeting.
6. Exact error reporting API.
7. Whether `.txt` registration is declarative or code-controlled.
8. Whether parser writes are transactional or dry-run capable.
9. Whether QBench preserves JavaScript Number values in worksheet writes.
10. Whether a parser can write only A:AE and AH:BE without touching AF/AG.

Until those are proven, `dist/terpenes_qbench_file_parser_candidate_v1.js` must
not be created.
