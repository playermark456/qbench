# Phase 4B.1 Batch save/reopen

Date: 2026-07-21

- Saved the synthetic Batch through the normal nonfinal worksheet workflow.
- Navigated away and reopened the Batch.
- All eight sanitized manual rows persisted with numeric/text types intact.
- AF/AG formulas and all eight classifications persisted.
- Batch Review persisted its expected QC Hold state and the two aggregate `#ERROR` values.
- Test Transfer persisted the two sample candidates, excluded controls, retained its mappings, and persisted the Publish Ready/Message `#ERROR` values.
- Both fresh Tests remained NOT STARTED and analytically unmodified.
- No parser/ASCII upload or Batch-to-Test write occurred.
- Nothing was completed, published, released, or marked QC Review.
- No METRC activity or cleanup occurred.

`batch_v2_batch_save_reopen = passed_with_persistent_formula_blocker`
