# Batch-row-to-Test matching contract

## Deterministic key

The only approved key is exact QBench Test ID:

- Batch source: `Publish!A{row}` from
  `terpenes_batch_publish_test_ids`.
- Test Worksheet confirmation: `qbench_test_id` at `Data!B9`.
- QBench entity: the exact Test display/controlled identifier associated with
  that Test Worksheet.

All three values must be nonblank and equal as complete strings. No trimming,
case folding, partial matching, or fuzzy matching is allowed unless QBench's
documented Test-ID format later requires a controlled canonicalization step.

## Cardinality

The automation must build the complete candidate match set before any write:

- exactly one match: continue to source and destination preflight;
- zero matches: write nothing and persist `Missing matching Test` on the Batch
  Publish row;
- more than one match: write nothing and persist `Multiple matching Tests` on
  the Batch Publish row.

The match operation must never select the first result.

## Prohibited keys

- row position;
- QBench Sample ID by itself;
- sample name;
- product matrix;
- partial Test ID;
- source filename;
- source-row hash by itself;
- first matching Test;
- any fuzzy comparison.

## Sandbox result

The original UI-only inspection found no visible Test-ID selector or
match-cardinality result, so the 43-field automation remained inactive. QBench
documentation later established that a source formula can reference
`{{test.id}}`; however, the Prompt 5A old-Sandbox probe was invalidated by a
missing saved destination named cell. Per-Test formula routing therefore
remains unresolved, and no exactly-one-match implementation has been proven.
