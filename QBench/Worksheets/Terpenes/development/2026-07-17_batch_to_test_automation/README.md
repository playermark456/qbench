# Terpenes Prompt 5 Batch-to-Test automation

Date: 2026-07-17

Status: **43-field publishing remains blocked; Prompt 5A routing probe
classified `per_test_vlookup_error`**.

Prompt 4.6C PR #11 was confirmed merged into `main` at
`969dea9703df16a99cbe74e575ee5bf001fe6064`. Prompt 5 work is on
`codex/terpenes-prompt-5-batch-to-test-automation`.

## Original Prompt 5 outcome

The Prompt 3 Test Worksheet, Prompt 4 Batch Worksheet, Prompt 4.5 adapter, and
Prompt 4.6C No-Code import evidence define an unambiguous source and destination
contract. The intended matching key is exact QBench Test ID.

The initial UI-only Sandbox capability inspection found that the available
Batch automation action is `Set value on all Test Worksheets within the Batch`.
It accepts a destination worksheet field and can copy a Batch Worksheet field,
but it does not expose a visible target-Test selector, an exactly-one-match
cardinality guard, a complete-destination preflight, or a transaction covering
multiple worksheet fields.

On that initial UI evidence, the design treated the action as a same-value
broadcast that could partially apply a multi-field transfer. The automation
was therefore not activated or configured with saved conditions/actions. That
was a valid controlled stop for the proposed 43-field design, but the broad
same-value-broadcast inference is not retained as a current platform finding.

## Prompt 5A official VLOOKUP routing follow-up

QBench's official Batch Spreadsheet Worksheets & Automations guide documents
that the action supplies `test` and can evaluate a Batch source expression such
as `VLOOKUP({{test.id}}, ...)`. Prompt 5A therefore ran one isolated one-field
probe in the old Sandbox.

The automation job ran once and reported `Success`, but all three destination
cells remained blank. The exact post-run Test Worksheet **Export Spreadsheet**
then proved that the intended named cells had not persisted in `qb_config`.
Because the configured `route_probe` destination did not exist in the saved
worksheet version, the run is classified **`per_test_vlookup_error`** and is
not evidence that routing is unsupported or that the same value is broadcast.
The automation was immediately deactivated; no retry or secondary guard probe
was performed.

Exact evidence is in `vlookup_route_probe/`.

## Original Prompt 5 Sandbox facts

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

- Prompt 5 package validator: passed; 16 core files plus the Prompt 5A probe
  extension, 43 intended mappings, source hashes, inactive final states, and
  zero-write state verified.
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
- `vlookup_route_probe/`
