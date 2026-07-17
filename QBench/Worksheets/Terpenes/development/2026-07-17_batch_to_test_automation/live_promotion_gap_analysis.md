# Live-promotion gap analysis

Prompt 5 is not eligible for promotion. Live QBench was not accessed.

## Blocking gaps

1. **Exact target selection:** the Sandbox Batch action broadcasts to all Test
   Worksheets and cannot select the Test whose exact ID matches the Batch row.
2. **Match cardinality:** the action cannot distinguish zero, one, or multiple
   matching Tests and cannot persist missing/ambiguous status.
3. **Per-row source selection:** the source contract contains up to 86 Publish
   rows, but the action accepts a worksheet field name rather than a selected
   row determined by Test ID.
4. **Atomicity:** the UI exposes field-by-field action cases with no documented
   complete-destination preflight, transaction, or rollback.
5. **Reviewer gate:** the Prompt 4/4.6C Batch Worksheet lacks a dedicated
   per-row reviewer-controlled publish authorization and publish status.
6. **Idempotency state:** the Prompt 3 Test Worksheet has `source_file_hash` but
   no `source_row_hash` destination, and the native action cannot persist or
   compare a row-specific last-published hash.
7. **Changed-hash handling:** no supported branch can block an overwrite and
   require reauthorization after the source-row hash changes.
8. **Destination contract errors:** a missing/renamed named cell cannot be
   proven to block the entire write before any other field changes.
9. **Numeric/formula runtime evidence:** no Prompt 5 publish occurred, so native
   numeric inputs, calculations, formula preservation, and reopen persistence
   remain unvalidated.
10. **Report boundary:** no isolated Prompt 5 report definition was created;
    report/COA preview belongs after a valid one-Test publishing mechanism
    exists.
11. **Inherited Prompt 4 package consistency:** the tracked Batch Worksheet
    layout hash does not match the hash recorded in the tracked Prompt 4
    candidate manifest. Prompt 4 validation must be restored in a controlled
    prerequisite change before promotion.

## Required platform capability

Promotion requires either a QBench-supported automation/managed-interface
operation or a documented API workflow that can, as one controlled unit:

1. read the complete reviewed Batch Publish row;
2. resolve exact QBench Test ID and require exactly one match;
3. validate every source and destination field before writing;
4. update only the enumerated writable Test Worksheet inputs atomically;
5. preserve formulas and read-only fields;
6. persist per-row success/error status and last-published source-row hash;
7. no-op on an unchanged hash;
8. block a changed hash until explicit reviewer reauthorization.

Broadcasting the same row to every Test, replacing a whole Test Worksheet, or
publishing from parser-job `SUCCESS` are not acceptable workarounds.

## Scientific boundary

Terpenes remains quantitative-only. Dimethylacetamide and Peak Table values are
audit-only. No sample compliance conclusion, METRC outcome, label-claim
conclusion, or COA outcome tile may be introduced.
