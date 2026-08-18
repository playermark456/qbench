# Automations — Production Read-Only Snapshot

Captured from `https://ait.qbench.net/automations` on 2026-08-16/17 UTC without running, testing, saving, or changing an automation.

## Inventory

- 16 automations: 13 active and 3 inactive.
- All 16 use the `Data Modified` trigger.
- Data types: 14 Batch, 1 Test (ID 16), and 1 Batch Object Protocol Step (ID 15).
- 18 visible condition blocks and 90 visible action blocks were recorded in order.
- ID 17, `Terpenes Batch to Test ws`, is the only object added to the prior 15-ID production baseline.

The normalized inventory is in `automation_inventory.csv`. Every visible condition and action is preserved in `automation_conditions.csv` and `automation_actions.csv`; `automation_inventory.json` retains the sanitized read-only page evidence.

## Significant current configuration

- ID 17 is active when worksheet 43, `Terpenes [Batch] Worksheet`, changes. It writes 26 Test-worksheet fields: `terpenes_instrument_conc_01` through `terpenes_instrument_conc_23`, `sample_mass_g`, `df`, and `df_application_mode`. Each value is selected from `B2:AY87` by `VLOOKUP({{test.get_display_id()}}, ...)`.
- ID 11 is active for Cannabinoid Potency and worksheet 7. It writes `result_1` through `result_29` and `df` from the Batch `Results` sheet.
- ID 16 is active for a Homogeneity Test only when status changes to `Ready for Homogeneity Pull`. It writes `mg_serving_1` from the Test worksheet's `Potency Results Lookup` sheet.
- IDs 2, 5, and 15 are inactive. Their overlapping Heavy Metals or Water Activity mappings remain visible but were not exercised.

## Cross-export reconciliation

Current automation actions were compared with the tracked 2026-07-04 active worksheet exports. Three defects are confirmed in that evidence: ID 1 reverses Lead and Mercury; ID 6 returns only 17 of the 19 cells required by `residual_solvents_results`, omitting Total Xylenes and Trichloroethene; and ID 11 reverses Unknown Peaks 2 and 3 between `result_21` and `result_22`. ID 10 is a likely destination mismatch rather than a confirmed current defect: `pest_quantitative_results` is absent from the tracked exports, while worksheet 16 has the width-compatible `pesticides_results`; a current native worksheet 16 export is required before correction.

See `../automation_cascade_analysis.md` for direct observations, repository-backed dependencies, reasoned inferences, and unresolved loop/fan-out questions.

## Capture boundary

- No automation history, job, run, retry, preview, or test was opened.
- No Save, Delete, activation, or form-submission control was used.
- Scheduling, notification recipients, retry behavior, idempotency behavior, error behavior, last-modified metadata, and aggregate history counts were not exposed on the inspected read-only surfaces.
- Screenshots were omitted because the available full-page scope included account UI. Structured configuration evidence was retained instead.
