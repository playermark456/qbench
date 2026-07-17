# Prompt 4.6C Sandbox cleanup plan

The Prompt 4.6C objects use the unique
`SBX_ONLY_TERPENES_2026_07_16_` prefix and have no assay, customer, production,
sample, test, or protocol association.

After the validation evidence is reviewed:

1. Deactivate `SBX_ONLY_TERPENES_2026_07_16_No_Code_Wide_Import` so the exact
   filename trigger is inert.
2. Retain the approved worksheet version and synthetic validation Batches only
   while the draft PR is under review.
3. Export any final evidence that is still needed, then delete the disposable
   Batches and attachments if the reviewer authorizes removal.
4. Deactivate or delete the isolated worksheet only after confirming it has no
   Batch links and no assay links.
5. Confirm no object outside the unique prefix was changed.

Cleanup is intentionally a plan, not an automatic action in this task, so the
Sandbox evidence remains independently reviewable. Never perform these steps in
live QBench.
