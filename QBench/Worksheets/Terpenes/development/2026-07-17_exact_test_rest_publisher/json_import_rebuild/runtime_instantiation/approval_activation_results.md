# Approval and activation results

Date: 2026-07-17

## Exact identity and pre-change verification

- Worksheet: `SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE`
- Version: `JSON Scalar 43 Field Base v1`
- Initial status: `DRAFT`
- Exact title and breadcrumb: passed
- Data worksheets: 1
- Grid: 40x26
- Required anchors: 28/28
- Named cells: 43/43, unique and unqualified
- Required spot checks: D2, O2, Z2, B12, B22, B23, and B30 passed
- `sdf`: absent
- Pass/Fail and prohibited destinations: absent

## Status progression

1. `DRAFT` was reopened and verified.
2. The supported pending-review workflow was completed.
3. After leaving the worksheet and reopening it from the Worksheets list, the
   exact Version 1 row visibly showed `PENDING`.
4. The supported Approve action was attempted on that exact row.
5. QBench rejected the action with: `This worksheet cannot be modified
   because it is currently locked.`
6. The exact worksheet Locks tab showed one active review lock assigned to a
   different user than the current Sandbox session. No unlock control was
   available to the current session.

Final status: `PENDING`.

- Approved: no
- Active: no
- Version 2 created: no
- Classification:
  `approval_activation_blocked_active_lock_assignee_mismatch`

The stop gate was honored before Assay creation.

## Resume attempt after reported manual resolution

The user reported that the review-assignee lock had been manually resolved.
The resumed verification used a fresh browser state and reopened the exact
worksheet from the Worksheets list. Sanitized result:

- exact title and breadcrumb: passed;
- exact Version 1: present;
- Version 2: absent;
- current status: `PENDING`;
- visible active lock: still assigned to a different account than the current
  signed-in session;
- supported Approve control: available;
- approval confirmation: submitted once;
- result: `This worksheet cannot be modified because it is currently locked.`

A final Worksheets-list reopen again showed the same single Version 1 in
`PENDING` state. The reported resolution was therefore not visible or
effective in the current session. The classification remains
`approval_activation_blocked_active_lock_assignee_mismatch`, and the stop gate
again prevented Assay creation.
