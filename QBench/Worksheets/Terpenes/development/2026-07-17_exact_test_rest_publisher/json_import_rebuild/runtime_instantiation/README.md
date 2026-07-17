# JSON scalar runtime-instantiation gate

Date: 2026-07-17

Classification: **`approval_activation_blocked_active_lock_assignee_mismatch`**.

The saved-definition and raw round-trip gates remain passed at 43/43. The
exact worksheet `SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE` and
exact version `JSON Scalar 43 Field Base v1` were reopened and verified before
the approval workflow began. Version 1 moved from `DRAFT` to `PENDING`, and
that state persisted after leaving the worksheet and reopening it from the
Worksheets list.

The supported Approve action then failed with the exact non-secret QBench
message: `This worksheet cannot be modified because it is currently locked.`
The Locks tab showed one active review lock assigned to a different user than
the currently signed-in Sandbox session, and the session exposed no unlock
control. The approval was not completed and the worksheet was not activated.

Per the Phase 1 stop gate, no Assay, Sample, Test, runtime export, or temporary
worksheet value was created. Runtime-instantiation classifications therefore
remain `not_run_phase_1_approval_gate`; they are not runtime failures.

Current controlled state:

- `approved_active_definition=blocked_active_lock_assignee_mismatch`
- `destination_contract_proven=saved_definition_only_pending_runtime_instantiation`
- `atomicity_classification=api_patch_unresolved`
- `analyte_patch_key_contract=unresolved`

No credential file was read. No token, REST API request, PATCH, live-QBench
access, Publish, QC Review, or Pass/Fail artifact occurred.
