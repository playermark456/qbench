# Phase 4A.6 V4 formula contract

Date: 2026-07-21

V4 was generated from the renderer-proven V3 path. A strict local normalizer proves that reverting only the V4 identity text, isolated store binding, terminal label, and five-argument calls produces the exact V3 candidate with zero unexpected differences.

- Embedded formulas: 309
- Key/Value formula cells and calls: 44 / 44
- Arguments per call: exactly 5
- Argument order: store, scope, matrix, analyte, field
- LOQ calls: 21
- MU calls: 23
- Result-unit arguments: 0
- `MU%` calls: 0
- Writable destinations: 43
- Named definitions: 44
- `report_results`: `Report!A1:E23`
- Unresolved markers: 0
- Pass/Fail: absent

The V3 six-argument signature, swapped analyte/matrix order, added unit level, and `MU%` terminal field all fail the project-specific validator. Five-argument LOQ and MU fixtures pass.
