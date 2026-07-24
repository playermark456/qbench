# Phase 4B.2 QBench coded-parser artifact validation

Result: `qbench_parser_artifact_ready_for_sandbox_upload`

- Operational parser reference SHA-256 matched: `61f91070e0b68b5c5c06de580efe0569d13075a032441968e9d43bec763c1d9e`.
- Authoritative raw source SHA-256 matched: `bfd88621e2e8ab791e63ba38f07c9a1174f9600e1cf3f28d5b12ffbd08f2eb91`.
- The complete source parsed as 34 records: 3 Null, 2 Blank, 3 System Suitability, 6 Standard, 3 CCV, 1 LOQ, 1 Matrix Blank, and 15 Sample.
- Every record satisfied the required sections, 24 compound IDs, controlled 23-channel order, and audit-only Dimethylacetamide handling. Peak Table audit total: 138 unknown peaks.
- The browser artifact uses the authoritative wrapper, has no Node-only dependencies, and passes JavaScript syntax validation.
- Mock QBench execution resolved two synthetic Sample IDs to one Batch, held 13 unresolved Samples, excluded 19 controls, populated rows 2:35, and cleared parser-owned destinations through row 201.
- The write contract restricted data changes to `A:AE` and `AH:BE`; `AF:AG`, formulas, images, and dollar references were preserved. One atomic update with recalculation enabled was observed.
- Zero-resolution, multiple-Batch, duplicate-Test-ID, malformed-source, missing-tab, header-mismatch, capacity, unsupported-input, and service-rejection paths made no unauthorized update and called `QB.error`.
- Local adapter/CLI-to-artifact equivalence and deterministic range-replacement idempotency passed. `local_qbench_write_idempotency = passed_deterministic_range_replacement`.
- Focused browser-contract tests: 30 passed. Production-candidate compatibility suite: 5 passed.
- No raw source was changed or tracked; no worksheet candidate was changed; no QBench access, parser creation, Git staging, commit, push, or PR update occurred.
