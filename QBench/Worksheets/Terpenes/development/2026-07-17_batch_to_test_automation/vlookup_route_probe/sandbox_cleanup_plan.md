# Prompt 5A Sandbox cleanup plan

The task-created automation is inactive. Retain the isolated objects until the
Draft PR evidence has been reviewed, then remove them only in a separately
authorized Sandbox cleanup action.

Recommended cleanup order:

1. Reconfirm the hostname is exactly `ait-sandbox.qbench.net`.
2. Confirm `SBX_ONLY_TERPENES_2026_07_17_VLOOKUP_AUTOMATION` is inactive, then
   delete it.
3. Delete `SBX_ONLY_TERPENES_2026_07_17_VLOOKUP_ROUTE_BATCH`.
4. Delete the three synthetic Tests and Samples recorded in
   `sandbox_object_inventory.csv`.
5. Delete the isolated assay.
6. Delete the isolated Batch and Test Worksheet objects.
7. Record object-by-object deletion results in a follow-up repository change.

Do not reuse these names for another routing run. A future probe needs new
isolated objects and must verify the required named cells in a fresh **Export
Spreadsheet** before automation activation.
