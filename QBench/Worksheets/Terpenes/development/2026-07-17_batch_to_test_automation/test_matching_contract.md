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

The native Batch automation action targets `all Test Worksheets within the
Batch`. It offers no Test-ID selector and no match-cardinality result. It cannot
implement this contract, so the automation remained inactive and no matching
test was executed.
