# Phase 1 Homogeneity Validation Report

Worksheet JSON: `homogeneity_phase1_production_candidate__2026-07-01.json`

## Summary

- JSON parsed: yes
- Worksheet names checked: 3
- Named cells found: 31
- Errors: 0
- Warnings: 0

## Required Checks

| Check | Result |
|---|---|
| pass_fail exists | PASS |
| report_results exists | PASS |
| required validation named cells exist | PASS |
| label source named cells exist | PASS |
| pass_fail gated by validation_status | PASS |
| parent sample fallback references Paste!D6 | PASS |
| Total THC helper converts ug/g to mg/g | PASS |
| Total CBD helper converts ug/g to mg/g | PASS |
| individual cannabinoid targets convert ug/g to mg/g | PASS |
| mg/unit uses converted mg/g times unit mass | PASS |
| Data tab variance cells use 0.0% display format | PASS |
| allowed variance remains decimal threshold from Paste!L4 | PASS |
| pass/fail logic compares decimal variances against 0.15 threshold | PASS |
| Paste!D4 has no P25IF corruption | PASS |
| Paste!D4/Paste!H4 use required label lookup formulas | PASS |
| P25:P36 remains raw QBench source table | PASS |
| Actual unit mass validation requires all 10 AH values | PASS |
| QBench per-serving sample label fields are documented/pulled | PASS |
| worksheet uses "Highest" terminology only | PASS |
| report_results range has content | PASS |

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
| `target_cannabinoid_1` | `Data!B3` | Target Cannabinoid 1 |
| `target_cannabinoid_2` | `Data!B5` | Target Cannabinoid 2 |
| `unique_cp_test_id_count` | `Data!B35` | Unique CP Test IDs Counted |
| `validation_status` | `Data!B42` | Overall Input Validation Status |

## Duplicate Named-Cell Targets

No duplicate named-cell targets found.

## Formula Checks

- pass_fail `Data!B31`: `=IF(B42<>"READY","INCOMPLETE",IF(COUNTIF(U12:U21,"FAIL")>0,"FAIL","PASS"))`
- validation_status `Data!B42`: `=IF(AND(B34=10,B36="PASS",B37="PASS",OR(B38="PASS",B38="REVIEWER_CONFIRMED"),B39="PASS",B40="PASS",B41="PASS"),"READY","INCOMPLETE")`
- parent_sample_match_check `Data!B38`: `=IF(B34<10,"INCOMPLETE",IF(COUNTA(B12:B21)=10,IF(COUNTIF(B12:B21,B12)=10,"PASS","FAIL"),IF(Paste!D6="YES","REVIEWER_CONFIRMED","INCOMPLETE")))`
- Total THC helper `Paste!AI10`: `=IF(AND(M10="",Q10=""),"",(IF(M10="",0,M10)+IF(Q10="",0,Q10)*0.877)/1000)`
- Total CBD helper `Paste!AJ10`: `=IF(AND(I10="",F10=""),"",(IF(I10="",0,I10)+IF(F10="",0,F10)*0.877)/1000)`
- Target 1 result `Data!E12`: `=IF($C12="","",IF($D12="","",IF($D12="Total THC",Paste!AI10,IF($D12="Total CBD",Paste!AJ10,IFERROR(INDEX(Paste!$A10:$AK10,MATCH($D12,Paste!$A$9:$AK$9,0))/1000,"")))))`
- Target 2 result `Data!G12`: `=IF($C12="","",IF($F12="","",IF($F12="Total THC",Paste!AI10,IF($F12="Total CBD",Paste!AJ10,IFERROR(INDEX(Paste!$A10:$AK10,MATCH($F12,Paste!$A$9:$AK$9,0))/1000,"")))))`
- Target 1 mg/unit `Data!M12`: `=IF(OR($C12="",H12="",E12=""),"",E12*H12)`
- Target 2 mg/unit `Data!P12`: `=IF($B$5="","",IF(OR($C12="",H12="",G12=""),"",G12*H12))`
- Allowed variance `Data!B9`: `=Paste!L4`
- Mass pass/fail sample `Data!R12`: `=IF(K12="","",IF(ABS(K12)<=$B$9,"PASS","FAIL"))`
- Cannabinoid 1 pass/fail sample `Data!S12`: `=IF(N12="","",IF(ABS(N12)<=$B$9,"PASS","FAIL"))`
- Cannabinoid 2 pass/fail sample `Data!T12`: `=IF($B$5="","",IF(Q12="","",IF(ABS(Q12)<=$B$9,"PASS","FAIL")))`
- Target 1 label lookup `Paste!D4`: `=IF(O4<>"",O4,IF(B4="","",IFERROR(IF(OR(INDEX($P$25:$P$36,MATCH(B4,$N$25:$N$36,0))="",LOWER(INDEX($P$25:$P$36,MATCH(B4,$N$25:$N$36,0)))="none",LEFT(INDEX($P$25:$P$36,MATCH(B4,$N$25:$N$36,0)),2)="${"),"",INDEX($P$25:$P$36,MATCH(B4,$N$25:$N$36,0))),"")))`
- Target 2 label lookup `Paste!H4`: `=IF(S4<>"",S4,IF(F4="","",IFERROR(IF(OR(INDEX($P$25:$P$36,MATCH(F4,$N$25:$N$36,0))="",LOWER(INDEX($P$25:$P$36,MATCH(F4,$N$25:$N$36,0)))="none",LEFT(INDEX($P$25:$P$36,MATCH(F4,$N$25:$N$36,0)),2)="${"),"",INDEX($P$25:$P$36,MATCH(F4,$N$25:$N$36,0))),"")))`
- Required unit mass check `Data!B39`: `=IF(B34<10,"INCOMPLETE",IF(COUNT(H12:H21)=10,"PASS","INCOMPLETE"))`

## Numeric Example Checks

- D9-THC `4058.954` ug/g with THCa `0.0` ug/g -> Total THC `4.058954` mg/g.
- Total THC `4.058954` mg/g with `5` g unit mass -> `20.29477` mg/unit.
- CBG `4105.178` ug/g -> `4.105178` mg/g.
- CBG `4.105178` mg/g with `5` g unit mass -> `20.52589` mg/unit.
- Data variance display `0.0147385` -> `1.5%` with 0.0% formatting.
- Data variance display `-0.0108085` -> `-1.1%` with 0.0% formatting.
- Allowed variance display `0.15` -> `15.0%` with 0.0% formatting.

## Data Tab Percent Display Formatting

| Cell/Range | Purpose | Style Contains 0.0% |
|---|---|---|
| `Data!B9` | Allowed Variance | yes |
| `Data!K12:K21` | Mass % Variance | yes |
| `Data!N12:N21` | Cannabinoid 1 % Variance | yes |
| `Data!Q12:Q21` | Cannabinoid 2 % Variance | yes |
| `Data!B26` | Highest Mass Label Variance | yes |
| `Data!B28` | Highest Cannabinoid 1 Label Variance | yes |
| `Data!B30` | Highest Cannabinoid 2 Label Variance | yes |

## Label Claim Source Logic

- For Homogeneity, `mg/unit` is treated as the `mg/serving` value requested by OCM and is calculated as `mg/g x actual unit mass g`.
- Target 1 label claim `Paste!D4` pulls per-serving/unit values from `Paste!N25:P36` unless manual override `Paste!O4` is populated.
- Target 2 label claim `Paste!H4` pulls per-serving/unit values from `Paste!N25:P36` unless manual override `Paste!S4` is populated.
- Targets without an exported per-serving QBench sample field remain blank and require manual override rather than falling back to package/container label values.
- Label Claim 1 source/status `Paste!Q4`: `=IF(O4<>"","Manual per-serving/unit override Paste!O4",IF(B4="","",IFERROR(IF(OR(INDEX($P$25:$P$36,MATCH(B4,$N$25:$N$36,0))="",LOWER(INDEX($P$25:$P$36,MATCH(B4,$N$25:$N$36,0)))="none",LEFT(INDEX($P$25:$P$36,MATCH(B4,$N$25:$N$36,0)),2)="${"),"Mapped per-serving/unit field is blank/unresolved: "&INDEX($O$25:$O$36,MATCH(B4,$N$25:$N$36,0)),"Pulled per-serving/unit value from "&INDEX($O$25:$O$36,MATCH(B4,$N$25:$N$36,0))),"No mapped per-serving/unit QBench sample label field")))`
- Label Claim 2 source/status `Paste!U4`: `=IF(F4="","Target 2 not used",IF(S4<>"","Manual per-serving/unit override Paste!S4",IFERROR(IF(OR(INDEX($P$25:$P$36,MATCH(F4,$N$25:$N$36,0))="",LOWER(INDEX($P$25:$P$36,MATCH(F4,$N$25:$N$36,0)))="none",LEFT(INDEX($P$25:$P$36,MATCH(F4,$N$25:$N$36,0)),2)="${"),"Mapped per-serving/unit field is blank/unresolved: "&INDEX($O$25:$O$36,MATCH(F4,$N$25:$N$36,0)),"Pulled per-serving/unit value from "&INDEX($O$25:$O$36,MATCH(F4,$N$25:$N$36,0))),"No mapped per-serving/unit QBench sample label field")))`

## Errors

None.

## Warnings

None.

