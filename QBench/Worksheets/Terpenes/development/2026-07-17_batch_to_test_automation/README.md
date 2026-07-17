# Terpenes Prompt 5 Batch-to-Test automation

Date: 2026-07-17

Status: **blocked at a mandatory stop condition before activation**.

Prompt 4.6C PR #11 was confirmed merged into `main` at
`969dea9703df16a99cbe74e575ee5bf001fe6064`. Prompt 5 work is on
`codex/terpenes-prompt-5-batch-to-test-automation`.

## Outcome

The Prompt 3 Test Worksheet, Prompt 4 Batch Worksheet, Prompt 4.5 adapter, and
Prompt 4.6C No-Code import evidence define an unambiguous source and destination
contract. The intended matching key is exact QBench Test ID.

Sandbox capability discovery then found that the available Batch automation
action is `Set value on all Test Worksheets within the Batch`. It accepts a
destination worksheet field and can copy a Batch Worksheet field, but it does
not expose a target-Test selector, an exact-Test-ID comparison, or an
exactly-one-match cardinality guard. The interface also does not provide a
complete-destination preflight or a transaction covering multiple worksheet
fields.

Using that action would broadcast a value to every Test Worksheet in the Batch
and could partially apply a multi-field transfer. This violates the Prompt 5
matching, isolation, and no-partial-write requirements. The automation was
therefore not activated or configured with saved conditions/actions.

## Sandbox facts

- Verified hostname: `ait-sandbox.qbench.net`.
- Created one isolated automation:
  `SBX_ONLY_TERPENES_2026_07_16_Batch_To_Test_Publish`.
- Trigger: `Data Modified`; data type: `Batch`.
- Final state: inactive, with no saved conditions and no saved actions.
- No assay, Batch, Sample, Test, Batch Worksheet, or Test Worksheet was created
  for Prompt 5 after the stop condition was identified.
- No Test Worksheet value was written.
- No pre-existing Sandbox Terpenes object was modified.
- Live QBench was not accessed.
- No customer data was used.
- No Terpenes Pass/Fail or compliance artifact was introduced.

The Prompt 4.6C canonical and malformed results were reviewed as repository
evidence only. They are not claimed as Prompt 5 publishing results.

## Exact contracts

- `batch_publish_gate.md` defines the complete proposed row gate and the missing
  reviewer-controlled fields.
- `test_matching_contract.md` defines exact-Test-ID matching and zero/multiple
  match behavior.
- `automation_mapping.csv` enumerates every intended writable Test Worksheet
  field. None of these mappings was saved in the Sandbox automation.
- `idempotency_contract.md` defines unchanged-hash and changed-hash behavior and
  records why it could not be implemented.

## Validation boundary

Prompt 5 success, malformed, duplicate, changed-hash, numeric-cell, formula
preservation, reopen, and COA preview tests were not run because each requires
an automation capable of selecting exactly one Test and preflighting the full
write set. The safe observed result is zero publishing writes.

Local validation results:

- Prompt 5 package validator: passed; 16 required files, 43 intended mappings,
  source hashes, inactive configuration, and zero-write state verified.
- Prompt 3 validator: passed; 50 unit tests passed.
- Prompt 4.5 validator: passed; 13 Python and 143 JavaScript tests passed.
- Prompt 4.6C package validator: passed.
- Prompt 4 validator and 39-test suite: inherited failure. The tracked
  `terpenes_batch_layout.json` SHA-256 is
  `7f1270063f689f9cac94ee22e4f69b0ea7953a6f5dc86e1f6b4c00bb4bed7ef0`,
  while its tracked candidate manifest records
  `fe137404165a044907a7fe31a7cc386f53f402bb643dd94bf2fbffe958571410`.
  Prompt 5 did not modify either file. This pre-existing mismatch is retained
  as a promotion gap rather than silently regenerating prior-prompt artifacts.

## Package contents

- `automation_configuration.md`
- `automation_mapping.csv`
- `batch_publish_gate.md`
- `test_matching_contract.md`
- `idempotency_contract.md`
- `sandbox_object_inventory.csv`
- `sandbox_success_results.md`
- `sandbox_failure_results.md`
- `sandbox_duplicate_results.md`
- `sandbox_change_log.md`
- `sandbox_cleanup_plan.md`
- `live_promotion_gap_analysis.md`
- `sanitized_automation_configuration.json`
- `validate_prompt_5_package.py`
- `prompt_5_manifest.json`
