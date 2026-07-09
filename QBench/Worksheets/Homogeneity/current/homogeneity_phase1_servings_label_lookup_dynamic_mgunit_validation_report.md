# Homogeneity Phase 1 Servings + Product Label Lookup + Dynamic mg/unit Validation Report

## File Confirmation
- Confirmed new JSON file path: `C:\Users\Mark Adams\Documents\GitHub\qbench\QBench\Worksheets\Homogeneity\current\homogeneity_phase1_servings_label_lookup_dynamic_mgunit__2026-07-08.json`
- Confirmed file exists: `True`
- File size: `659761` bytes
- Modified timestamp: `2026-07-08T19:10:30`
- Overall validation result: `PASS`

## Formula Count by Tab
| Tab | Formula count |
|---|---:|
| `Paste` | 33 |
| `Data` | 248 |
| `COA` | 94 |

## Named Cell List
| System name | Cell/range | Display name | Export |
|---|---|---|---|
| `average_actual_unit_mass_g` | `Data!B8` | `Average Actual Unit Mass g` | `True` |
| `duplicate_cp_test_id_check` | `Data!B36` | `Duplicate CP Test ID Check` | `True` |
| `extra_pasted_rows_check` | `Data!B37` | `Extra Pasted Rows Check` | `True` |
| `highest_cannabinoid_1_label_variance` | `Data!B28` | `Cannabinoid 1 Label Variance for Highest Cannabinoid` | `True` |
| `highest_cannabinoid_2_label_variance` | `Data!B30` | `Cannabinoid 2 Label Variance for Highest Cannabinoid` | `True` |
| `highest_mass_label_variance` | `Data!B26` | `Mass Label Variance for Highest Unit Mass` | `True` |
| `highest_reported_cannabinoid_1_mg_container` | `Data!B27` | `Highest Reported Cannabinoid 1 mg/unit` | `True` |
| `highest_reported_cannabinoid_2_mg_container` | `Data!B29` | `Highest Reported Cannabinoid 2 mg/unit` | `True` |
| `highest_reported_unit_mass_g` | `Data!B25` | `Highest Reported Unit Mass g` | `True` |
| `homogeneity_metrc` | `COA!F1` | `Homogeneity METRC` | `True` |
| `label_cannabinoid_1_mg_container` | `Data!B4` | `Label Cannabinoid 1 mg/unit` | `True` |
| `label_cannabinoid_1_source_status` | `Paste!Q4` | `Label Cannabinoid 1 Source Status` | `True` |
| `label_cannabinoid_2_mg_container` | `Data!B6` | `Label Cannabinoid 2 mg/unit` | `True` |
| `label_cannabinoid_2_source_status` | `Paste!U4` | `Label Cannabinoid 2 Source Status` | `True` |
| `label_unit_mass_g` | `Data!B7` | `Label Unit Mass g` | `True` |
| `manual_label_cannabinoid_1_mg_container` | `Paste!O4` | `Manual Label Cannabinoid 1 mg/unit Override` | `True` |
| `manual_label_cannabinoid_2_mg_container` | `Paste!S4` | `Manual Label Cannabinoid 2 mg/unit Override` | `True` |
| `optional_target_2_label_claim_check` | `Data!B41` | `Optional Target 2 Label Claim Check` | `True` |
| `parent_sample_match_check` | `Data!B38` | `Parent Sample Match Check` | `True` |
| `pass_fail` | `Data!B31` | `Pass/Fail` | `True` |
| `qbench_sample_label_amount_lookup` | `Paste!N24:P36` | `QBench Product Label Amount Lookup` | `True` |
| `replicate_count` | `Data!B34` | `Replicate Rows Present` | `True` |
| `replicate_results` | `COA!A10:G20` | `Homogeneity Replicate Results` | `True` |
| `report_results` | `COA!A1:G20` | `Homogeneity COA Output` | `True` |
| `required_target_fields_check` | `Data!B40` | `Required Target 1 and Label Claim Check` | `True` |
| `required_unit_mass_check` | `Data!B39` | `Required Unit Mass Check` | `True` |
| `reviewer_parent_sample_confirmation` | `Paste!D6` | `Reviewer Parent Sample Confirmation` | `True` |
| `reviewer_single_serving_confirmation` | `Data!B47` | `Reviewer Single-Serving Confirmation` | `True` |
| `serving_size_g` | `Data!B44` | `Serving Size (g)` | `True` |
| `serving_size_g_comparison` | `Data!B49` | `Serving Size (g) Comparison` | `True` |
| `serving_size_g_source_status` | `Data!B46` | `Serving Size (g) Source Status` | `True` |
| `servings_per_container` | `Data!B43` | `Servings Per Container` | `True` |
| `servings_per_container_check` | `Data!B48` | `Servings Per Container Check` | `True` |
| `servings_per_container_source_status` | `Data!B45` | `Servings Per Container Source Status` | `True` |
| `target_cannabinoid_1` | `Data!B3` | `Target Cannabinoid 1` | `True` |
| `target_cannabinoid_2` | `Data!B5` | `Target Cannabinoid 2` | `True` |
| `unique_cp_test_id_count` | `Data!B35` | `Unique CP Test IDs Counted` | `True` |
| `validation_status` | `Data!B42` | `Overall Input Validation Status` | `True` |

## Range Confirmation
- report_results range: `COA!A1:G20`
- replicate_results range: `COA!A10:G20`
- report_results remains `COA!A1:G20`: `PASS`
- replicate_results remains `COA!A10:G20`: `PASS`
- Replicate header remains on COA row 10: `PASS`
- Replicate rows remain on COA rows 11 through 20: `PASS`

## Validation Checks
| Requirement | Result | Evidence |
|---|---|---|
| Confirmed new JSON file path | `PASS` | `C:\Users\Mark Adams\Documents\GitHub\qbench\QBench\Worksheets\Homogeneity\current\homogeneity_phase1_servings_label_lookup_dynamic_mgunit__2026-07-08.json` |
| Confirmed file exists | `PASS` | `True` |
| report_results remains COA!A1:G20 | `PASS` | `COA!A1:G20` |
| replicate_results remains COA!A10:G20 | `PASS` | `COA!A10:G20` |
| Replicate header remains on COA row 10 | `PASS` | `COA!A10:G10 populated` |
| Replicate rows remain on COA rows 11 through 20 | `PASS` | `COA!A11:A20 formulas present` |
| Servings Per Container is present | `PASS` | `named=Data!B43; Data!B43==Paste!W4` |
| Serving Size (g) is present or documented as optional | `PASS` | `named=Data!B44; Data!C44=Optional comparison field; does not block validation when absent.` |
| Data!M12:M21 calculate Target 1 mg/unit as mg/g x actual total unit/container mass g / servings per container | `PASS` | `=IF(OR($C12="",H12="",E12="",$B$43=""),"",IFERROR(E12*H12/VALUE($B$43),""))` |
| Data!P12:P21 calculate Target 2 mg/unit as mg/g x actual total unit/container mass g / servings per container | `PASS` | `=IF($B$5="","",IF(OR($C12="",H12="",G12="",$B$43=""),"",IFERROR(G12*H12/VALUE($B$43),"")))` |
| Worksheet does not calculate multi-serving mg/unit as mg/g x full container mass only | `PASS` | `M/P formulas include servings division` |
| Report-facing labels say mg/unit | `PASS` | `D10==IF(Data!B3="","","mg/unit ("&Data!B3&")"); F10==IF(Data!B5="","","mg/unit ("&Data!B5&")")` |
| No visible Homogeneity labels say mg/container | `PASS` | `[]` |
| Product Label Amount fields use product_label_* QBench sample fields | `PASS` | `${test.sample.product_label_totalthc}, ${test.sample.product_label_totalcbd}, ${test.sample.product_label_cbd}, ${test.sample.product_label_cbda}, ${test.sample.product_label_cbn}, ${test.sample.product_label_cbg}, ${test.sample.product_label_cbga}, ${test.sample.product_label_d8thc}, ${test.sample.product_label_thc}, ${test.sample.product_label_thcv}, ${test.sample.product_label_cbc}, ${test.sample.product_label_thca}` |
| CBG and CBGa have QBench sample field mappings | `PASS` | `P30=${test.sample.product_label_cbg}; P31=${test.sample.product_label_cbga}` |
| Target 2 can be Total CBG and still pulls the CBG label amount | `PASS` | `Paste!AQ4==IF(F4="","",IF(LOWER(TRIM(F4))="total cbg","CBG",IF(LOWER(TRIM(F4))="total cbga","CBGa",F4))); Paste!H4==IF(S4<>"",S4,IF(F4="","",IFERROR(IF(OR(INDEX($P$25:$P$36,MATCH($AQ$4,$N$25:$N$36,0))="",LOWER(INDEX($P$25:$P$36,MATCH($AQ$4,$N$25:$N$36,0)))="none",LEFT(INDEX($P$25:$P$36,MATCH($AQ$4,$N$25:$N$36,0)),2)="${"),"",INDEX($P$25:$P$36,MATCH($AQ$4,$N$25:$N$36,0))),"")))` |
| Target 2 can be Total CBG and still calculates actual mg/unit from the CBG result column | `PASS` | `Data!D5==Paste!AQ4; Data!G12==IF($C12="","",IF($F12="","",IF($D$5="Total THC",Paste!AI10,IF($D$5="Total CBD",Paste!AJ10,IFERROR(INDEX(Paste!$A10:$AK10,MATCH($D$5,Paste!$A$9:$AK$9,0))/1000,"")))))` |
| COA Target 2 headers display the selected target name | `PASS` | `=IF(Data!B5="","","mg/unit ("&Data!B5&")")` |
| COA Target 2 variance header displays the selected target name | `PASS` | `=IF(Data!B5="","","Cannabinoid Label Variance ("&Data!B5&")")` |
| No bad formula such as =P25IF(...) exists | `PASS` | `searched generated JSON` |
| No formulas were flattened into static values | `PASS` | `formula counts={'Paste': 33, 'Data': 248, 'COA': 94}` |
| No duplicate named cells exist | `PASS` | `named cell count=38` |
| Root data layer and config worksheet data layer match for Paste, Data, and COA | `PASS` | `{'Paste': True, 'Data': True, 'COA': True}` |
| Paste, Data, and COA formula changes were applied to both JSON data layers | `PASS` | `{'Paste': True, 'Data': True, 'COA': True}` |
| No *_persrv fields are used for Product Label Amount lookup | `PASS` | `[]` |
| Source/status fields still show Servings Per Container and Serving Size (g) pull/manual state | `PASS` | `Paste!AC4==IF(Y4<>"","Manual override Paste!Y4",IF(OR(AA4="",LOWER(AA4)="none",LEFT(AA4,2)="${"),IF(AE4="YES","Reviewer confirmed single-serving; using 1","Missing/unresolved QBench sample servings_per_container"),"Pulled from QBench sample servings_per_container")); Paste!AM4==IF(AI4<>"","Manual override Paste!AI4",IF(OR(AK4="",LOWER(AK4)="none",LEFT(AK4,2)="${"),"Optional: missing/unresolved QBench sample units_per_serving","Pulled from QBench sample units_per_serving"))` |
| Worksheet documentation states mg/unit is mg/serving formula | `PASS` | `Paste!B22=Pasted cannabinoid result values are expected in ug/g. AI:AJ and Data target formulas convert to mg/g before mg/unit calculations. For Homogeneity, mg/unit is mg/serving: mg/g x actual total unit/container mass g / servings per container.; Data!B2=Pasted cannabinoid result values are expected in ug/g. Target result formulas convert to mg/g before mg/unit calculations. Homogeneity mg/unit is mg/serving: mg/g x actual total unit/container mass g / servings per container.` |

## Formula Evidence
- `Data!M12`: `=IF(OR($C12="",H12="",E12="",$B$43=""),"",IFERROR(E12*H12/VALUE($B$43),""))`
- `Data!P12`: `=IF($B$5="","",IF(OR($C12="",H12="",G12="",$B$43=""),"",IFERROR(G12*H12/VALUE($B$43),"")))`
- `Data!B42 validation_status`: `=IF(AND(B34=10,B36="PASS",B37="PASS",OR(B38="PASS",B38="REVIEWER_CONFIRMED"),B39="PASS",B40="PASS",B41="PASS",B48="PASS"),"READY","INCOMPLETE")`
- `Data!B48 servings_per_container check`: `=IF(B43="","INCOMPLETE",IFERROR(IF(VALUE(B43)>0,"PASS","INCOMPLETE"),"INCOMPLETE"))`
- `Paste!D4 Target 1 label lookup formula`: `=IF(O4<>"",O4,IF(B4="","",IFERROR(IF(OR(INDEX($P$25:$P$36,MATCH($AO$4,$N$25:$N$36,0))="",LOWER(INDEX($P$25:$P$36,MATCH($AO$4,$N$25:$N$36,0)))="none",LEFT(INDEX($P$25:$P$36,MATCH($AO$4,$N$25:$N$36,0)),2)="${"),"",INDEX($P$25:$P$36,MATCH($AO$4,$N$25:$N$36,0))),"")))`
- `Paste!H4 Target 2 label lookup formula`: `=IF(S4<>"",S4,IF(F4="","",IFERROR(IF(OR(INDEX($P$25:$P$36,MATCH($AQ$4,$N$25:$N$36,0))="",LOWER(INDEX($P$25:$P$36,MATCH($AQ$4,$N$25:$N$36,0)))="none",LEFT(INDEX($P$25:$P$36,MATCH($AQ$4,$N$25:$N$36,0)),2)="${"),"",INDEX($P$25:$P$36,MATCH($AQ$4,$N$25:$N$36,0))),"")))`
- `Paste!AO4 Target 1 normalized lookup key formula`: `=IF(B4="","",IF(LOWER(TRIM(B4))="total cbg","CBG",IF(LOWER(TRIM(B4))="total cbga","CBGa",B4)))`
- `Paste!AQ4 Target 2 normalized lookup key formula`: `=IF(F4="","",IF(LOWER(TRIM(F4))="total cbg","CBG",IF(LOWER(TRIM(F4))="total cbga","CBGa",F4)))`
- `COA!D10`: `=IF(Data!B3="","","mg/unit ("&Data!B3&")")`
- `COA!E10`: `=IF(Data!B3="","","Cannabinoid Label Variance ("&Data!B3&")")`
- `COA!F10`: `=IF(Data!B5="","","mg/unit ("&Data!B5&")")`
- `COA!G10`: `=IF(Data!B5="","","Cannabinoid Label Variance ("&Data!B5&")")`

## Product Label Amount Lookup Evidence
| Target key | Field display/status | Placeholder |
|---|---|---|
| `Total THC` | `Product Label Amount - Total THC (if applicable)` | `${test.sample.product_label_totalthc}` |
| `Total CBD` | `Product Label Amount - Total CBD (if applicable)` | `${test.sample.product_label_totalcbd}` |
| `CBD` | `Product Label Amount - CBD (if applicable)` | `${test.sample.product_label_cbd}` |
| `CBDa` | `Product Label Amount - CBDa (if applicable)` | `${test.sample.product_label_cbda}` |
| `CBN` | `Product Label Amount - CBN (if applicable)` | `${test.sample.product_label_cbn}` |
| `CBG` | `Product Label Amount - CBG (if applicable)` | `${test.sample.product_label_cbg}` |
| `CBGa` | `Product Label Amount - CBGa (if applicable)` | `${test.sample.product_label_cbga}` |
| `D8-THC` | `Product Label Amount - d8 THC (if applicable)` | `${test.sample.product_label_d8thc}` |
| `D9-THC` | `Product Label Amount - d9 THC (if applicable)` | `${test.sample.product_label_thc}` |
| `THCV` | `Product Label Amount - THCV (if applicable)` | `${test.sample.product_label_thcv}` |
| `CBC` | `Product Label Amount - CBC (if applicable)` | `${test.sample.product_label_cbc}` |
| `THCa` | `Product Label Amount - THCa (if applicable)` | `${test.sample.product_label_thca}` |

## Logical Manual Test Scenarios
### Scenario A - Total THC + Total CBG, 15 servings
- Inputs: Target Cannabinoid 1 = `Total THC`; Target Cannabinoid 2 = `Total CBG`; Servings Per Container = `15`; Product Label Amount - Total THC = `10`; Product Label Amount - CBG = `10`.
- Expected/validated: Target 1 lookup uses `${test.sample.product_label_totalthc}` and pulls `10`; Target 2 display `Total CBG` normalizes through `Paste!AQ4`/`Data!D5` to `CBG`, uses `${test.sample.product_label_cbg}`, and pulls `10`.
- Expected/validated: Target 2 result lookup uses `MATCH($D$5,Paste!$A$9:$AK$9,0)`, so `Total CBG` uses the pasted `CBG` result column while COA display remains `Total CBG`.
- Expected/validated COA headers: `mg/unit (Total THC)`, `Cannabinoid Label Variance (Total THC)`, `mg/unit (Total CBG)`, `Cannabinoid Label Variance (Total CBG)`.

### Scenario B - Multi-serving calculation
- Inputs: mg/g = `4.058954`; actual total unit/container mass g = `50`; servings per container = `10`.
- Expected: `4.058954 x 50 / 10 = 20.29477` mg/unit.
- Formula path: `Data!M12`/`Data!P12` calculate `result mg/g x actual total unit/container mass g / VALUE(Data!B43)`; PASS.

### Scenario C - Single-serving calculation
- Inputs: mg/g = `4.058954`; actual total unit/container mass g = `5`; servings per container = `1`.
- Expected: `4.058954 x 5 / 1 = 20.29477` mg/unit.
- Formula path: the same `Data!M12`/`Data!P12` formulas divide by `1`; PASS.

## QBench Sandbox Test Checklist
1. Import the corrected worksheet JSON in QBench Sandbox.
2. Attach worksheet to the intended Homogeneity assay/test.
3. Confirm required named cells are visible: `pass_fail`, `report_results`, `replicate_results`, `validation_status`, `target_cannabinoid_1`, `target_cannabinoid_2`, `servings_per_container`, and `serving_size_g`.
4. Create or open a representative Homogeneity test/sample.
5. Enter/paste 10 Cannabinoid Potency replicate rows and actual total unit/container masses.
6. Test Target 1 = `Total THC`, Target 2 = `Total CBG`, Servings Per Container = `15`, Product Label Amount - Total THC = `10`, Product Label Amount - CBG = `10`.
7. Confirm calculations and Pass/Fail after validation_status becomes READY.
8. Generate COA preview.
9. Confirm the first-page tile uses `pass_fail` and the standalone Homogeneity table renders `report_results`.
10. Confirm rendered worksheet/report table fits the COA page and dynamic headers show the selected target names.
11. Compare key mg/unit and variance results against manual calculation before promoting beyond Sandbox.

