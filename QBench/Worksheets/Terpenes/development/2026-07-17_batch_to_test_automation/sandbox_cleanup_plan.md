# Sandbox cleanup plan

## Object in scope

`SBX_ONLY_TERPENES_2026_07_16_Batch_To_Test_Publish`

The automation is inactive and has no saved conditions or actions. It cannot
run in its current state.

## Cleanup steps

1. In `https://ait-sandbox.qbench.net/`, open Automations.
2. Locate the exact prefixed name above.
3. Confirm Active is off and that Conditions and Action contain no saved cases.
4. Delete the automation only after this draft PR and evidence package have
   been reviewed, if the lab does not want to retain the inert blocker record.
5. Record the deletion in a follow-up change log; do not reuse the name for a
   different design without updating the repository contract.

No Batch, Sample, Test, assay, worksheet, parser, report, or attachment was
created during the original Prompt 5 stop. Prompt 5A later created a separate
isolated routing-probe object set; its cleanup scope and order are recorded in
`vlookup_route_probe/sandbox_cleanup_plan.md`.
