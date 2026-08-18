# Automation Index

## Production rescan 2026-08-16

Current production configuration was verified read-only at `ait.qbench.net` on 2026-08-16/17 UTC. There are 16 automations: 13 active and 3 inactive. All use `Data Modified`. Complete normalized conditions and ordered actions are in `QBench/Rescans/2026-08-16/Automations/`.

| ID | Automation name | Data type | Active | Observed condition | Ordered action summary |
|---:|---|---|---|---|---|
| 17 | Terpenes Batch to Test ws | Batch | Active | Worksheet 43 — Terpenes [Batch] Worksheet | 26 all-Test writes: `terpenes_instrument_conc_01..23` from lookup columns 9–31, then `sample_mass_g`/`df`/`df_application_mode` from columns 6–8 of `B2:AY87` |
| 16 | Homogeneity - Pull potency mg/serving | Test | Active | Homogeneity assay; status changes into `Ready for Homogeneity Pull` | Writes `mg_serving_1` from `Potency Results Lookup` |
| 14 | AC EB YM Batch to Test WS | Batch | Active | Worksheet 89 | Writes `ac_results`, `eb_results`, `ym_results` |
| 13 | Listeria Batch to Test WS | Batch | Active | Worksheet 86 | Writes `lis_results` |
| 12 | Salmonella Species & STEC Batch to Test WS | Batch | Active | Worksheet 82 | Writes `salmonella_results` and `stec_results` |
| 11 | Cannabinoid Potency Batch to Test WS | Batch | Active | Cannabinoid Potency assay and worksheet 7 | Writes `result_1..29` and `df` from `Results`; tracked active exports confirm `result_21`/`result_22` reverse Unknown Peaks 2/3 |
| 10 | Pesticide (Quantitative) Analysis | Batch | Active | Worksheet 13 | Writes `pest_quantitative_results` from `B34:BT200`; likely tracked-export mismatch because worksheet 16 exposes `pesticides_results`, pending a current export |
| 9 | Aspergillus Batch WS to Test WS | Batch | Active | Worksheet 80 | Writes four species-result fields |
| 8 | Pest Myco (Qualitative) Batch WS to Test WS | Batch | Active | Worksheet 15 | Writes `pesticides_results`, `mycotoxin_results`, `df` |
| 6 | Residual Solvents Batch WS to Test WS | Batch | Active | Worksheet 11 | Tracked active exports confirm `residual_solvents_results` receives 17 source cells for a 19-cell destination, omitting Total Xylenes and Trichloroethene; `df` is aligned |
| 4 | Water Activity Batch WS to Test WS | Batch | Active | Worksheet 29 | Writes `wateractivityaw` |
| 3 | Mycotoxin (Quantitative) Batch WS to Test WS | Batch | Active | Worksheet 9 | Writes five toxin fields; action 5 has a distinct all-Samples-Test fan-out label |
| 1 | Heavy Metals Batch WS to Test WS | Batch | Active | Worksheet 5 | Tracked active exports confirm the `lead` and `mercury` source columns are reversed; arsenic, cadmium, and `df` align |
| 15 | Water Activity Protocol WS to Batch WS | Batch Object Protocol Step | Inactive | Protocol Step = Water Activity Sample Measurements | Destination `wateractivity_0`; source blank |
| 5 | test wa | Batch | Inactive | Protocol = [Batch] Water Activity Protocol | Destination `wateractivity_0`; source blank |
| 2 | Heavy Metals Batch WS to Test WS 2 | Batch | Inactive | Worksheet 5 | Older four-metal mappings using `{{get_display_id}}` |

Observed configuration contains 18 condition blocks and 90 actions. IDs 1, 6, and 11 have repository-confirmed mapping defects against the tracked active worksheet exports. ID 10 remains a likely tracked-export mismatch that requires a current native worksheet 16 export before correction. Scheduling, date-driven behavior, notifications, retry/error/idempotency behavior, last-modified metadata, and history counts were not exposed. No automation was run. See `QBench/Rescans/2026-08-16/automation_cascade_analysis.md`.

## Superseded pre-rescan summary

The following table is retained as historical repository context. It predates automation 17 and lacks the condition detail now captured above.

| ID | Automation name | Trigger | Data type | Active | Related assay/module | Conditions | Actions / worksheet fields updated |
|---:|---|---|---|---|---|---|---|
| 16 | Homogeneity - Pull potency mg/serving | Data Modified | Test | Active | Homogeneity | Condition table present, specific row values not exposed in read-only summary | Updates mg_serving_1 using VLOOKUP against Potency Results Lookup. |
| 14 | AC EB YM Batch to Test WS | Data Modified | Batch | Active | TAMC, Enterobacteriaceae, TYMC | Condition table present, specific row values not exposed in read-only summary | Updates ac_results, eb_results, ym_results from Calculations ranges. |
| 13 | Listeria Batch to Test WS | Data Modified | Batch | Active | Listeria | Condition table present, specific row values not exposed in read-only summary | Updates lis_results from Calculations range. |
| 12 | Salmonella Species & STEC Batch to Test WS | Data Modified | Batch | Active | Salmonella, STEC | Condition table present, specific row values not exposed in read-only summary | Updates salmonella_results and stec_results from Calculations ranges. |
| 11 | Cannabinoid Potency Batch to Test WS | Data Modified | Batch | Active | Cannabinoid Potency, Homogeneity | Condition table present, specific row values not exposed in read-only summary | Updates result_1 through result_29 and df from Results ranges. |
| 10 | Pesticide (Quantitative) Analysis | Data Modified | Batch | Active | Pesticides | Condition table present, specific row values not exposed in read-only summary | Updates pest_quantitative_results from B34:BT200. |
| 9 | Aspergillus Batch WS to Test WS | Data Modified | Batch | Active | Aspergillus | Condition table present, specific row values not exposed in read-only summary | Updates terreus_result, niger_result, flavus_result, fumigatus_result. |
| 8 | Pest Myco (Qualitative) Batch WS to Test WS | Data Modified | Batch | Active | Pesticides, Mycotoxins | Condition table present, specific row values not exposed in read-only summary | Updates pesticides_results, mycotoxin_results, df. |
| 6 | Residual Solvents Batch WS to Test WS | Data Modified | Batch | Active | Residual Solvents | Condition table present, specific row values not exposed in read-only summary | Updates residual_solvents_results and df. |
| 4 | Water Activity Batch WS to Test WS | Data Modified | Batch | Active | Water Activity | Condition table present, specific row values not exposed in read-only summary | Updates wateractivityaw. |
| 3 | Mycotoxin (Quantitative) Batch WS to Test WS | Data Modified | Batch | Active | Mycotoxins | Condition table present, specific row values not exposed in read-only summary | Updates aflatoxinb1, aflatoxinb2, aflatoxing1, aflatoxing2, ochratoxina. |
| 1 | Heavy Metals Batch WS to Test WS | Data Modified | Batch | Active | Heavy Metals | Condition table present, specific row values not exposed in read-only summary | Updates arsenic, cadmium, lead, mercury, df. |
| 15 | Water Activity Protocol WS to Batch WS | Data Modified | Batch Object Protocol Step | Inactive | Water Activity | Condition table present, specific row values not exposed in read-only summary | No worksheet-field updates visible. |
| 5 | test wa | Data Modified | Batch | Inactive | Water Activity | Condition table present, specific row values not exposed in read-only summary | wateractivity_0 mapping visible but blank value. |
| 2 | Heavy Metals Batch WS to Test WS 2 | Data Modified | Batch | Inactive | Heavy Metals | Condition table present, specific row values not exposed in read-only summary | Older mappings for arsenic, cadmium, lead, mercury using get_display_id. |

## Rescan 2026-07-04

| ID | Automation name | Trigger | Data type | Description / notes |
|---:|---|---|---|---|
| 16 | Homogeneity - Pull potency mg/serving | Data Modified | Test | When a Homogeneity worksheet has manually entered Cannabinoid Potency Test IDs, pull the target cannabinoid mg/serving result into the Homogeneity worksheet. |
| 14 | AC EB YM Batch to Test WS | Data Modified | Batch | No description visible in parsed detail fields. |
| 13 | Listeria Batch to Test WS | Data Modified | Batch | No description visible in parsed detail fields. |
| 12 | Salmonella Species & STEC Batch to Test WS | Data Modified | Batch | No description visible in parsed detail fields. |
| 11 | Cannabinoid Potency Batch to Test WS | Data Modified | Batch | No description visible in parsed detail fields. |
| 10 | Pesticide (Quantitative) Analysis | Data Modified | Batch | No description visible in parsed detail fields. |
| 9 | Aspergillus Batch WS to Test WS | Data Modified | Batch | No description visible in parsed detail fields. |
| 8 | Pest Myco (Qualitative) Batch WS to Test WS | Data Modified | Batch | No description visible in parsed detail fields. |
| 6 | Residual Solvents Batch WS to Test WS | Data Modified | Batch | No description visible in parsed detail fields. |
| 4 | Water Activity Batch WS to Test WS | Data Modified | Batch | No description visible in parsed detail fields. |
| 3 | Mycotoxin (Quantitative) Batch WS to Test WS | Data Modified | Batch | No description visible in parsed detail fields. |
| 1 | Heavy Metals Batch WS to Test WS | Data Modified | Batch | No description visible in parsed detail fields. |
| 15 | Water Activity Protocol WS to Batch WS | Data Modified | Batch Object Protocol Step | No description visible in parsed detail fields. |
| 5 | test wa | Data Modified | Batch | No description visible in parsed detail fields. |
| 2 | Heavy Metals Batch WS to Test WS 2 | Data Modified | Batch | No description visible in parsed detail fields. |

## Prompt 5 Sandbox attempt 2026-07-17

`SBX_ONLY_TERPENES_2026_07_16_Batch_To_Test_Publish` was created in
`ait-sandbox.qbench.net` with trigger `Data Modified`, data type `Batch`, and
Active off. No conditions or actions were saved. The available action targets
all Test Worksheets within a Batch and exposes no exact-Test-ID selector or
exactly-one-match guard, so activation was blocked under the Prompt 5 stop
conditions. Sanitized evidence is in
`QBench/Worksheets/Terpenes/development/2026-07-17_batch_to_test_automation/`.

## Prompt 5A VLOOKUP routing probe 2026-07-17

QBench's official Batch Spreadsheet Worksheets & Automations guide documents
that the all-Test action supplies `test` and can use a Batch source formula of
the form `VLOOKUP({{test.id}}, ...)`. An isolated old-Sandbox probe used
`=VLOOKUP({{test.id}}, A2:B4, 2)` for three synthetic Tests with distinct
values. The Batch was saved exactly once and one task-created automation job
reported `Success`, but all destination values stayed blank.

The exact post-run Test Worksheet export contained the expected cell contents
but no saved `named_cells` configuration, so `route_probe` was not a valid
destination. Classification: `per_test_vlookup_error`. The automation was
deactivated immediately. Zero-match, duplicate-match, and COUNTIF/IF probes
were not run. This corrects the original broad broadcast conclusion without
claiming that old-Sandbox per-Test routing passed. Evidence is in the
`vlookup_route_probe/` subdirectory of the Prompt 5 package.
