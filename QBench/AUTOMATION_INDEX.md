# Automation Index

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
