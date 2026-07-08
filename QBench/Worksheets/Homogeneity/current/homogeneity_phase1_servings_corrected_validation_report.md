# Homogeneity Servings-Corrected Worksheet Validation Report

Validated worksheet JSON: `C:\Users\Mark Adams\Documents\GitHub\qbench\QBench\Worksheets\Homogeneity\current\homogeneity_phase1_servings_corrected_original_layout_mgunit__2026-07-07.json`

## File Confirmation

- Confirmed new JSON file path: `C:\Users\Mark Adams\Documents\GitHub\qbench\QBench\Worksheets\Homogeneity\current\homogeneity_phase1_servings_corrected_original_layout_mgunit__2026-07-07.json`
- Confirmed file exists: `True`
- File size: `657123 bytes`
- Modified timestamp: `2026-07-08 15:29:46`

## Formula Count By Tab

| Tab | Formula Count |
|---|---:|
| Paste | 31 |
| Data | 242 |
| COA | 86 |

## Named Cells

| System Name | Cell/Range | Display Name |
|---|---|---|
| `average_actual_unit_mass_g` | `Data!B8` | Average Actual Unit Mass g |
| `duplicate_cp_test_id_check` | `Data!B36` | Duplicate CP Test ID Check |
| `extra_pasted_rows_check` | `Data!B37` | Extra Pasted Rows Check |
| `highest_cannabinoid_1_label_variance` | `Data!B28` | Cannabinoid 1 Label Variance for Highest Cannabinoid |
| `highest_cannabinoid_2_label_variance` | `Data!B30` | Cannabinoid 2 Label Variance for Highest Cannabinoid |
| `highest_mass_label_variance` | `Data!B26` | Mass Label Variance for Highest Unit Mass |
| `highest_reported_cannabinoid_1_mg_container` | `Data!B27` | Highest Reported Cannabinoid 1 mg/unit |
| `highest_reported_cannabinoid_2_mg_container` | `Data!B29` | Highest Reported Cannabinoid 2 mg/unit |
| `highest_reported_unit_mass_g` | `Data!B25` | Highest Reported Unit Mass g |
| `homogeneity_metrc` | `COA!F1` | Homogeneity METRC |
| `label_cannabinoid_1_mg_container` | `Data!B4` | Label Cannabinoid 1 mg/unit |
| `label_cannabinoid_1_source_status` | `Paste!Q4` | Label Cannabinoid 1 Source Status |
| `label_cannabinoid_2_mg_container` | `Data!B6` | Label Cannabinoid 2 mg/unit |
| `label_cannabinoid_2_source_status` | `Paste!U4` | Label Cannabinoid 2 Source Status |
| `label_unit_mass_g` | `Data!B7` | Label Unit Mass g |
| `manual_label_cannabinoid_1_mg_container` | `Paste!O4` | Manual Label Cannabinoid 1 mg/unit Override |
| `manual_label_cannabinoid_2_mg_container` | `Paste!S4` | Manual Label Cannabinoid 2 mg/unit Override |
| `optional_target_2_label_claim_check` | `Data!B41` | Optional Target 2 Label Claim Check |
| `parent_sample_match_check` | `Data!B38` | Parent Sample Match Check |
| `pass_fail` | `Data!B31` | Pass/Fail |
| `qbench_sample_label_amount_lookup` | `Paste!N24:P36` | QBench Per-Serving Label Amount Lookup |
| `replicate_count` | `Data!B34` | Replicate Rows Present |
| `replicate_results` | `COA!A10:G20` | Homogeneity Replicate Results |
| `report_results` | `COA!A1:G20` | Homogeneity COA Output |
| `required_target_fields_check` | `Data!B40` | Required Target 1 and Label Claim Check |
| `required_unit_mass_check` | `Data!B39` | Required Unit Mass Check |
| `reviewer_parent_sample_confirmation` | `Paste!D6` | Reviewer Parent Sample Confirmation |
| `reviewer_single_serving_confirmation` | `Data!B47` | Reviewer Single-Serving Confirmation |
| `serving_size_g` | `Data!B44` | Serving Size (g) |
| `serving_size_g_comparison` | `Data!B49` | Serving Size (g) Comparison |
| `serving_size_g_source_status` | `Data!B46` | Serving Size (g) Source Status |
| `servings_per_container` | `Data!B43` | Servings Per Container |
| `servings_per_container_check` | `Data!B48` | Servings Per Container Check |
| `servings_per_container_source_status` | `Data!B45` | Servings Per Container Source Status |
| `target_cannabinoid_1` | `Data!B3` | Target Cannabinoid 1 |
| `target_cannabinoid_2` | `Data!B5` | Target Cannabinoid 2 |
| `unique_cp_test_id_count` | `Data!B35` | Unique CP Test IDs Counted |
| `validation_status` | `Data!B42` | Overall Input Validation Status |

## Required Confirmations

| Check | Result | Detail |
|---|---|---|
| report_results range | PASS | `COA!A1:G20` |
| replicate_results range | PASS | `COA!A10:G20` |
| Servings Per Container is present | PASS | `` |
| Serving Size (g) is present as optional comparison field | PASS | `` |
| Data!M12:M21 calculate Target 1 mg/unit as mg/g x total mass / servings | PASS | `` |
| Data!P12:P21 calculate Target 2 mg/unit as mg/g x total mass / servings | PASS | `` |
| Worksheet does not calculate multi-serving mg/unit as mg/g x full container mass only | PASS | `` |
| Report-facing labels say mg/unit | PASS | `` |
| No report-facing Homogeneity labels say mg/container | PASS | `` |
| No bad formula such as =P25IF(...) exists | PASS | `` |
| No formulas were flattened into static values | PASS | `` |
| No duplicate named cells exist | PASS | `` |
| All 10 replicate rows pull from Data | PASS | `` |

## Formula Preservation Checks

All required formula ranges still contain formulas.

## Servings Formula Evidence

- `Data!M12`: `=IF(OR($C12="",H12="",E12="",$B$43=""),"",IFERROR(E12*H12/VALUE($B$43),""))`
- `Data!P12`: `=IF($B$5="","",IF(OR($C12="",H12="",G12="",$B$43=""),"",IFERROR(G12*H12/VALUE($B$43),"")))`
- `Data!B42`: `=IF(AND(B34=10,B36="PASS",B37="PASS",OR(B38="PASS",B38="REVIEWER_CONFIRMED"),B39="PASS",B40="PASS",B41="PASS",B48="PASS"),"READY","INCOMPLETE")`
- `Data!B48`: `=IF(B43="","INCOMPLETE",IFERROR(IF(VALUE(B43)>0,"PASS","INCOMPLETE"),"INCOMPLETE"))`
- `Data!B49`: `=IF(OR(B44="",B43="",B8="",B44=0),"NOT CHECKED",IFERROR(IF(ABS((B8/VALUE(B43))-B44)/B44>0.05,"WARNING","PASS"),"NOT CHECKED"))`

## Source Field Evidence

- `Paste!AA4`: `${test.sample.servings_per_container}`
- `Paste!AK4`: `${test.sample.units_per_serving}`
- `Paste!AC4`: `=IF(Y4<>"","Manual override Paste!Y4",IF(OR(AA4="",LOWER(AA4)="none",LEFT(AA4,2)="${"),IF(AE4="YES","Reviewer confirmed single-serving; using 1","Missing/unresolved QBench sample servings_per_container"),"Pulled from QBench sample servings_per_container"))`
- `Paste!AM4`: `=IF(AI4<>"","Manual override Paste!AI4",IF(OR(AK4="",LOWER(AK4)="none",LEFT(AK4,2)="${"),"Optional: missing/unresolved QBench sample units_per_serving","Pulled from QBench sample units_per_serving"))`

## Created Files

CREATED JSON:
C:\Users\Mark Adams\Documents\GitHub\qbench\QBench\Worksheets\Homogeneity\current\homogeneity_phase1_servings_corrected_original_layout_mgunit__2026-07-07.json

CREATED VALIDATION REPORT:
C:\Users\Mark Adams\Documents\GitHub\qbench\QBench\Worksheets\Homogeneity\current\homogeneity_phase1_servings_corrected_validation_report.md
