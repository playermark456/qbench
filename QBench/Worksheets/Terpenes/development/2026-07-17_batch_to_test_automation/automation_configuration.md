# Sanitized Sandbox automation configuration

## Saved configuration

| Property | Value |
|---|---|
| Name | `SBX_ONLY_TERPENES_2026_07_16_Batch_To_Test_Publish` |
| Description | Prompt 5 isolated Sandbox-only reviewed Terpenes Batch Publish to matching Test Worksheet by exact QBench Test ID. Inactive until full validation. |
| Trigger | `Data Modified` |
| Trigger data type | `Batch` |
| Active | No |
| Saved conditions | None |
| Saved actions | None |
| Assay/worksheet assignment | None |

No internal Sandbox object ID is included in this package.

## Task-scoped capability inspection

The new automation's condition editor offered these field types:

- `Data Type`
- `Worksheet`

Choosing `Worksheet` exposed one `Worksheet Field Name` input. This could limit
the trigger to a uniquely named reviewer-controlled Batch Worksheet field, but
it does not identify which Test should receive a row.

The action editor offered `Set value on all Test Worksheets within the Batch`.
For a worksheet destination it exposed:

1. destination `Worksheet Field Name`;
2. `To = Copy Value`;
3. `Copy = From Worksheet`;
4. source `Worksheet Field Name`.

The action did not expose any of the following:

- exact QBench Test ID target selector;
- zero/one/multiple match evaluation;
- per-Test filter expression;
- per-row source selection from an 86-row Publish range;
- full destination contract preflight;
- atomic multi-field transaction;
- per-row publish-status or last-published-hash update.

## Activation decision

Activation was blocked. The only supported Test Worksheet action broadcasts to
all Test Worksheets within the Batch, so it cannot satisfy the deterministic
one-row-to-one-Test contract. No condition or action was saved after this was
observed.
