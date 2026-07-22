# Phase 4B.1 Batch v2 preflight

Date: 2026-07-21

## Source preservation

- Candidate: `production_candidates/SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS__v2.json`
- Expected SHA-256: `a4b92be3590e57f3456e12c65219cb6a5cb340248c6f3e50c6d3f36f56777837`
- Actual SHA-256: `a4b92be3590e57f3456e12c65219cb6a5cb340248c6f3e50c6d3f36f56777837`
- Hash gate: passed.
- The candidate was not regenerated or modified.
- The working tree was clean before Sandbox work.

## Validator results

- Phase 3 Batch candidate validators: passed.
- Scientific-logic, worksheet-schema, and historical-renderer validation: passed.
- No-code import-contract validator: passed.
- Parser configuration tests: 27/27 passed.
- Complete production-candidate suite: 51/51 passed.
- Test V4 binding-fix validator: passed with 43 destinations.
- Test V4 binding-fix SHA-256 remained `92c4e87a9e06157fe37b007e805ce9905f3e18ea4516a48211956a909062dc59`.

## Batch structural contract

- Tabs and order: Run Setup, Instrument Import, Batch Review, Test Transfer.
- Dimensions: 25x3, 201x57, 45x24, and 87x56 respectively.
- Instrument Import contains 200 data rows and 23 numeric terpene channels.
- Dimethylacetamide and Peak Table fields are retained for audit/QC use.
- AF/AG contain formulas for rows 2:201 and are excluded from parser-write targets.
- Parser-write targets are A:AE and AH:BE.
- Batch Review and Test Transfer are separate tabs.
- No Pass/Fail, automatic Test publication/completion, automatic QC Review, or METRC action was found.

`batch_v2_local_preflight = passed`
