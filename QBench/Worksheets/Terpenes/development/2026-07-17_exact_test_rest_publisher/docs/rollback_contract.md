# Rollback contract

Before each Test PATCH, the publisher re-GETs the exact Test and requires all
43 current values and the formula manifest to match the reviewed dry-run
baseline. The rollback payload is exactly those captured 43 values.

After PATCH, verification checks:

- all 43 mapped values;
- native numeric type for all 23 analytes;
- complete formula manifest equality;
- digest equality for every unrelated worksheet cell;
- destination named-cell contract;
- absence of prohibited Pass/Fail named cells.

If verification fails, rollback is attempted only when every mapped current
value is either the captured baseline or the proposed value. Any third value
indicates possible concurrent modification and blocks automatic rollback.

Rollback uses one PATCH, no retry, with reason
`Prompt 5B controlled rollback; source hash <short hash>`, followed by GET
verification of values, formulas, and unrelated-cell digest. Failure or
ambiguity stops the Batch immediately.

A PATCH timeout after submission is never retried. The publisher GETs the Test,
treats the attempt as failed even if proposed values persisted, and performs a
controlled rollback when safe.

Sandbox rollback result: not run. Local synthetic partial-write and
timeout-after-apply rollback tests passed.
