# Sandbox duplicate and changed-hash results

Prompt 5 duplicate execution and changed-source-hash tests were not run because
the automation cannot target exactly one Test or persist row-specific
last-published hash state.

Safe observed result:

- execution count: zero;
- Test Worksheets created: zero;
- Test Worksheet writes: zero;
- duplicate values appended: zero;
- formulas changed: zero;
- prior results overwritten: zero.

The Prompt 4.6C duplicate upload remained idempotent at fixed Instrument Import
targets, but that does not prove Prompt 5 publishing idempotency. It is not
counted as a Prompt 5 duplicate result.

Required future behavior is defined in `idempotency_contract.md`: unchanged
hash must be a no-op, while a changed hash must block and require explicit
reviewer reauthorization before any controlled replacement.
