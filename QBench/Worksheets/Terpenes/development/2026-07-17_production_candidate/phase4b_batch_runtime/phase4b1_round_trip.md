# Phase 4B.1 worksheet round trip

Date: 2026-07-21

- Saved exactly one draft named `Terpenes Production Candidate Batch Worksheet v2 Dynamic`.
- The Versions tab showed exactly one Draft Version 1 before approval.
- After list-based reopen, all four tabs, exact order, dimensions, formulas, styles, and protection remained intact.
- AF/AG ownership and parser-write separation remained intact.
- Raw Export Spreadsheet bytes were kept outside tracked evidence.
- Raw export SHA-256: `d7969c0708c64d2eef08d0b8ee600cbca5d232c39a05d61d7cea2910f4bdfbe7`.

Semantic comparison preserved:

- four worksheets in exact order;
- 1,180 embedded formulas;
- 1,180 formula-cache values;
- 16,304 nonformula values;
- 67 named definitions;
- all dimensions, cell values, styles, protection, Batch Review logic, and Test Transfer logic.

Observed normalization was limited to generated namespace/worksheet identifiers, minimum and viewport dimensions, top-level evaluated formula cache, JSON ordering, quoted named-cell sheet references, named-configuration ordering, QBench's default CSV filename, and QBench's internal canonicalization of three `Test Transfer` formula references.

`batch_v2_round_trip = passed_with_expected_qbench_normalization`
