# Live-promotion gap analysis

This package is not production-ready and live promotion has not begun.

Blocking gaps:

1. The official same-host OAuth token endpoint has not been proven or locked.
2. No token request or authenticated Sandbox request has been authorized yet.
3. Read-only Batch/Test response shapes have not been observed in the Sandbox.
4. Exact synthetic assay and workflow identifiers are not configured.
5. The native old-Sandbox Spreadsheet Worksheet engine is operational, but the
   imported Prompt 3 Test Worksheet is a compatibility failure and the exact
   native rebuild failed Phase 1 at 4/7 representative destinations.
6. The native Worksheet save path rejected bracketed indexed named-cell keys;
   indexed-versus-range REST analyte PATCH representation is still unresolved.
7. Scalar text/numeric persistence and rollback have not been run.
8. Multi-field failure behavior is `api_patch_unresolved`.
9. Direct publishing is blocked unless atomicity is empirically
   `api_patch_atomic`.
10. If partial writes are possible, no saved staging-and-commit worksheet exists.
11. No Sandbox full 43-field single-Test publish has been verified.
12. No Sandbox three-Test sequential publish has been verified.
13. The 43-field Test contract lacks a durable committed source-row hash.
14. The local ledger is not a QBench-native live-promotion system of record.
15. The inherited Prompt 4 candidate-manifest layout hash mismatch remains.
16. No live-specific credential, identifier, report, COA, METRC, rollback, or
    operational procedure has been designed or tested.

The recommended compatibility route is staged rather than another full import:

1. Resolve an exact, supportable native representation for the required
   bracketed analyte destination names; do not substitute underscore controls.
2. Repeat the seven-field Phase 1 save/reopen probe and require 7/7.
3. Only then build the complete 43-field Version 2, instantiate it through an
   Assay, and prove all destinations on a fresh reopened Test.
4. Add formulas and the remaining Prompt 3 layout incrementally, repeating the
   runtime proof at each stage.

Live QBench was not accessed. No customer data was used. No Pass/Fail artifact
was created. No COA was generated and nothing was transmitted to METRC.
