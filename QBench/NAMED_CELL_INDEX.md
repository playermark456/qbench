# Named Cell Index

Generated from exported worksheet JSON files under `QBench/Worksheets`. The address rows remain a historical native-export baseline; current production worksheet versions could not be exported in the 2026-08-16 read-only scan.

## 2026-08-16 production report-source dependency overlay

- Report 26 v24 reads `pass_fail` for status tiles; three total-THC fields for Cannabinoid display; `report_results` for eight assay sections; and `report_header`/`report_content` for the microbial summary.
- Report 44 v2 reads `homogeneity_metrc` first with `pass_fail` fallback. For its Potency summary it reads direct `Report!B2:B4`/`Report!E2:E4` cells first, then falls back to `report_left_total_label`, `report_left_total_mg_container`, `report_left_total_mg_serving`, `report_right_total_label`, `report_right_total_mg_container`, and `report_right_total_mg_serving`. Its Homogeneity status order conflicts with the canonical requirement that `pass_fail` drive first-page status and `report_results` supply the standalone table/page.
- Report 20 v1 renders a complete Test worksheet without a named-cell restriction.
- Current report-critical worksheet versions have advanced, so the ranges below cannot certify current compatibility. The July Terpenes export lacks the `report_results` now required by report 26 v24.
- The 2026-07-04 rescan block was appended four times historically. The first preserved copy is the authoritative last-verified native-export baseline. The three later copies are explicitly deprecated duplicates: they remain for history, are not independent evidence, and must never be counted or used to override the first copy. Before this overlay was added, the historical index contained 2,717 data rows but only 1,158 exact unique rows.

Current report source and the full dependency analysis are in `QBench/Rescans/2026-08-16/Reports/` and `QBench/Rescans/2026-08-16/report_dependency_map.md`.

### Current authority and known gaps

Use this precedence for report work: (1) the production-source overlay above defines current names actually requested by report code; (2) the first preserved 2026-07-04 rescan block defines the last verified native-export addresses; (3) the original pre-rescan rows and three deprecated duplicate rescan blocks are historical only. A source reference does not prove a named cell exists, and no current address is inferred.

| Dependency | Last verified native-export evidence | Current interpretation |
|---|---|---|
| Homogeneity `pass_fail` | `Data!B31` | Required canonical status value; last verified in the first 2026-07-04 block. |
| Homogeneity `homogeneity_metrc` | `COA!F1` | Compatibility/METRC value; not the canonical first-page status source. |
| Homogeneity `report_results` | `COA!A1:G20` | Required canonical standalone Homogeneity table/page. The older original `Report!A1:B1` row is superseded historical evidence. |
| Cannabinoids `total_thc_report_result` | `Data!C11` | Last verified historically and read by report 26. |
| Cannabinoids `total_thc_mg_per_serving_report_result`, `total_thc_mg_per_container_report_result` | Not present | Read by report 26 but export-unverified. |
| Report 44 six `report_left_total_*` / `report_right_total_*` fields | Not present | Optional fallback names after direct cell reads; absence alone is not a runtime defect, but the names remain export-unverified. |
| Terpenes `report_results` | Not present | Required by report 26 v24; current range unknown. |
| Terpenes `pass_fail` | Not present | Read by report 26 tile/overall-status logic; current compatibility remains unverified. |
| Water Activity `pass_fail` | Not present; `pass_fail_report = Specifications!B7` exists | Report 26 reads `pass_fail`; compatibility remains unverified. |
| Listeria `pass_fail` | Not present | Report 26 reads `pass_fail`; current compatibility remains unverified. |
| Cannabinoid Potency generic `pass_fail` | Not present | Source call exists in shared tile logic; current compatibility remains unverified. |

| Assay | Worksheet | Named Cell | Cell/Range | Purpose | Used by COA? | Notes |
|---|---|---|---|---|---|---|
| Cannabinoids | cannabinoid potency test ws id 8 | df | Data!G2 | Dilution factor | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | purity_results | 'Purity Data'!C2:R2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | report_results | Report!A1:F21 | Full report result range | Yes/likely | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_1 | Data!E5 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_10 | Data!N5 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_11 | Data!O5 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_12 | Data!P5 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_13 | Data!Q5 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_14 | 'Purity Data'!C2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_15 | 'Purity Data'!D2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_16 | 'Purity Data'!E2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_17 | 'Purity Data'!F2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_18 | 'Purity Data'!G2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_19 | 'Purity Data'!H2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_2 | Data!F5 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_20 | 'Purity Data'!I2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_21 | 'Purity Data'!J2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_22 | 'Purity Data'!K2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_23 | 'Purity Data'!L2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_24 | 'Purity Data'!M2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_25 | 'Purity Data'!N2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_26 | 'Purity Data'!O2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_27 | 'Purity Data'!P2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_28 | 'Purity Data'!Q2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_29 | 'Purity Data'!R2 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_3 | Data!G5 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_4 | Data!H5 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_5 | Data!I5 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_6 | Data!J5 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_7 | Data!K5 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_8 | Data!L5 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | result_9 | Data!M5 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | results | Data!E5:Q5 | Assay result field | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | total_thc | Report!B1 | Worksheet named cell | Unknown | Exportable=True |
| Cannabinoids | cannabinoid potency test ws id 8 | total_thc_report_result | Data!C11 | Assay result field | Unknown | Exportable=True |
| Foreign_Material | foreign material test ws id 31 | ffm_metrc | Report!C2 | METRC reporting field | Yes/likely | Exportable=True; Display=Foreign Material METRC |
| Foreign_Material | foreign material test ws id 31 | pass_fail | Data!D2 | Pass/fail status for report and/or METRC | Yes/likely | Exportable=True |
| Foreign_Material | foreign material test ws id 31 | report_results | Report!A1:C5 | Full report result range | Yes/likely | Exportable=True |
| Heavy_Metals | heavy metals test ws id 6 | arsenic | Data!E2 | Worksheet named cell | Unknown | Exportable=True; Display=Arsenic |
| Heavy_Metals | heavy metals test ws id 6 | arsenic_limit | Specifications!C5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Arsenic Limit |
| Heavy_Metals | heavy metals test ws id 6 | arsenic_loq | Specifications!B5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Arsenic LOQ |
| Heavy_Metals | heavy metals test ws id 6 | arsenic_mu | Specifications!E5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Arsenic MU |
| Heavy_Metals | heavy metals test ws id 6 | arsenic_result | Specifications!D5 | Assay result field | Unknown | Exportable=True; Display=Arsenic Result |
| Heavy_Metals | heavy metals test ws id 6 | arsenic_status | Specifications!F5 | Worksheet named cell | Unknown | Exportable=True; Display=Arsenic Status |
| Heavy_Metals | heavy metals test ws id 6 | cadmium | Data!F2 | Worksheet named cell | Unknown | Exportable=True; Display=Cadmium |
| Heavy_Metals | heavy metals test ws id 6 | cadmium_limit | Specifications!C6 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Cadmium Limit |
| Heavy_Metals | heavy metals test ws id 6 | cadmium_loq | Specifications!B6 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Cadmium LOQ |
| Heavy_Metals | heavy metals test ws id 6 | cadmium_mu | Specifications!E6 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Cadmium MU |
| Heavy_Metals | heavy metals test ws id 6 | cadmium_result | Specifications!D6 | Assay result field | Unknown | Exportable=True; Display=Cadmium Result |
| Heavy_Metals | heavy metals test ws id 6 | cadmium_status | Specifications!F6 | Worksheet named cell | Unknown | Exportable=True; Display=Cadmium Status |
| Heavy_Metals | heavy metals test ws id 6 | df | Data!I2 | Dilution factor | Unknown | Exportable=True |
| Heavy_Metals | heavy metals test ws id 6 | lead | Data!G2 | Worksheet named cell | Unknown | Exportable=True; Display=Lead |
| Heavy_Metals | heavy metals test ws id 6 | lead_limit | Specifications!C7 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Lead Limit |
| Heavy_Metals | heavy metals test ws id 6 | lead_loq | Specifications!B7 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Lead LOQ |
| Heavy_Metals | heavy metals test ws id 6 | lead_mu | Specifications!E7 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Lead MU |
| Heavy_Metals | heavy metals test ws id 6 | lead_result | Specifications!D7 | Assay result field | Unknown | Exportable=True; Display=Lead Result |
| Heavy_Metals | heavy metals test ws id 6 | mercury | Data!H2 | Worksheet named cell | Unknown | Exportable=True; Display=Mercury |
| Heavy_Metals | heavy metals test ws id 6 | mercury_limit | Specifications!C8 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Mercury Limit |
| Heavy_Metals | heavy metals test ws id 6 | mercury_loq | Specifications!B8 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Mercury LOQ |
| Heavy_Metals | heavy metals test ws id 6 | mercury_mu | Specifications!E8 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Mercury MU |
| Heavy_Metals | heavy metals test ws id 6 | mercury_result | Specifications!D8 | Assay result field | Unknown | Exportable=True; Display=Mercury Result |
| Heavy_Metals | heavy metals test ws id 6 | mercury_status | Specifications!F8 | Worksheet named cell | Unknown | Exportable=True; Display=Mercury Status |
| Heavy_Metals | heavy metals test ws id 6 | pass_fail | Specifications!D2 | Pass/fail status for report and/or METRC | Yes/likely | Exportable=True |
| Heavy_Metals | heavy metals test ws id 6 | report_results | Report!A1:F6 | Full report result range | Yes/likely | Exportable=True |
| Homogeneity | test ws id 73 | homogeneity_metrc | Report!B1 | METRC reporting field | Yes/likely | Exportable=True; Display=Homogeneity METRC |
| Homogeneity | test ws id 73 | report_results | Report!A1:B1 | Full report result range | Yes/likely | Exportable=True |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | asp_limit | Specifications!C5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Aspergillus Limit |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | asp_loq | Specifications!B5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Aspergillus LOQ |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | asp_mu | Specifications!E5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Aspergillus MU |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | asp_result | Specifications!D9 | Assay result field | Unknown | Exportable=True; Display=Aspergillus Result |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | asp_status | Specifications!F9 | Worksheet named cell | Unknown | Exportable=True; Display=Aspergillus Status |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | aspergillusspp_metrc | Report!C6 | METRC reporting field | Yes/likely | Exportable=True; Display=Aspergillus Results |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | flavus_result | Data!E3 | Assay result field | Unknown | Exportable=True; Display=A. Flavus Result |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | fumigatus_result | Data!E4 | Assay result field | Unknown | Exportable=True; Display=A. fumigatus Result |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | metrc_analyte_name_aspergillusspp | METRC!A5 | METRC reporting field | Yes/likely | Exportable=True |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | metrc_notes_aspergillusspp | METRC!D5 | METRC reporting field | Yes/likely | Exportable=True |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | metrc_pass_fail_aspergillusspp | METRC!C5 | METRC reporting field | Yes/likely | Exportable=True |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | metrc_quantity_aspergillusspp | METRC!B5 | METRC reporting field | Yes/likely | Exportable=True |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | metrc_to_include_aspergillusspp | METRC!E5 | METRC reporting field | Yes/likely | Exportable=True |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | niger_result | Data!E2 | Assay result field | Unknown | Exportable=True; Display=A. niger (HEX) Result |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | pass_fail | Specifications!D2 | Pass/fail status for report and/or METRC | Yes/likely | Exportable=True |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | report_content | Report!A2:D5 | Report result content range | Yes/likely | Exportable=True |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | report_header | Report!A1:D1 | Report table header range | Yes/likely | Exportable=True |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | report_results | Report!A1:D5 | Full report result range | Yes/likely | Exportable=True |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | sub_species | Data!F2 | Worksheet named cell | Unknown | Exportable=True; Display=Asp Sub Species |
| Microbiology - Aspergillus | total aspergillus microbial analysis test ws id 81 | terreus_result | Data!E5 | Assay result field | Unknown | Exportable=True; Display=A. terreus Result |
| Microbiology - Enterobacteriaceae | enterobacteriaceae test ws id 95 | eb_limit | Specifications!C5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Enterobacteriaceae Limit |
| Microbiology - Enterobacteriaceae | enterobacteriaceae test ws id 95 | eb_loq | Specifications!B5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Enterobacteriaceae LOQ |
| Microbiology - Enterobacteriaceae | enterobacteriaceae test ws id 95 | eb_mu | Specifications!E5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Enterobacteriaceae MU |
| Microbiology - Enterobacteriaceae | enterobacteriaceae test ws id 95 | eb_result | Specifications!D5 | Assay result field | Unknown | Exportable=True; Display=Enterobacteriaceae Result |
| Microbiology - Enterobacteriaceae | enterobacteriaceae test ws id 95 | eb_results | Data!E2 | Assay result field | Unknown | Exportable=True; Display=Enterobacteriaceae Results |
| Microbiology - Enterobacteriaceae | enterobacteriaceae test ws id 95 | eb_status | Specifications!F5 | Worksheet named cell | Unknown | Exportable=True; Display=Enterobacteriaceae Status |
| Microbiology - Enterobacteriaceae | enterobacteriaceae test ws id 95 | pass_fail | Specifications!D2 | Pass/fail status for report and/or METRC | Yes/likely | Exportable=True |
| Microbiology - Enterobacteriaceae | enterobacteriaceae test ws id 95 | report_content | Report!A2:E2 | Report result content range | Yes/likely | Exportable=True |
| Microbiology - Enterobacteriaceae | enterobacteriaceae test ws id 95 | report_header | Report!A1:E1 | Report table header range | Yes/likely | Exportable=True |
| Microbiology - Enterobacteriaceae | enterobacteriaceae test ws id 95 | report_results | Report!A1:E2 | Full report result range | Yes/likely | Exportable=True |
| Microbiology - Listeria | listeria monocytogenes test ws id 87 | lis_results | Data!E2 | Assay result field | Unknown | Exportable=True; Display=Listeria Results |
| Microbiology - Listeria | listeria monocytogenes test ws id 87 | report_content | Report!A2:E2 | Report result content range | Yes/likely | Exportable=True |
| Microbiology - Listeria | listeria monocytogenes test ws id 87 | report_header | Report!A1:E1 | Report table header range | Yes/likely | Exportable=True |
| Microbiology - Listeria | listeria monocytogenes test ws id 87 | report_results | Report!A1:E2 | Full report result range | Yes/likely | Exportable=True |
| Microbiology - Salmonella | salmonella species test ws id 83 | pass_fail | Specifications!D2 | Pass/fail status for report and/or METRC | Yes/likely | Exportable=True |
| Microbiology - Salmonella | salmonella species test ws id 83 | report_content | Report!A2:E2 | Report result content range | Yes/likely | Exportable=True |
| Microbiology - Salmonella | salmonella species test ws id 83 | report_header | Report!A1:E1 | Report table header range | Yes/likely | Exportable=True |
| Microbiology - Salmonella | salmonella species test ws id 83 | report_results | Report!A1:E2 | Full report result range | Yes/likely | Exportable=True |
| Microbiology - Salmonella | salmonella species test ws id 83 | salm_limit | Specifications!C5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Salmonella Limit |
| Microbiology - Salmonella | salmonella species test ws id 83 | salm_loq | Specifications!B5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Salmonella LOQ |
| Microbiology - Salmonella | salmonella species test ws id 83 | salm_mu | Specifications!E5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Salmonella MU |
| Microbiology - Salmonella | salmonella species test ws id 83 | salm_result | Specifications!D5 | Assay result field | Unknown | Exportable=True; Display=Salmonella Result |
| Microbiology - Salmonella | salmonella species test ws id 83 | salm_status | Specifications!F5 | Worksheet named cell | Unknown | Exportable=True; Display=Salmonella Status |
| Microbiology - Salmonella | salmonella species test ws id 83 | salmonella_results | Data!E2 | Assay result field | Unknown | Exportable=True; Display=Salmonella Results |
| Microbiology - STEC | stec test ws id 84 | pass_fail | Specifications!D2 | Pass/fail status for report and/or METRC | Yes/likely | Exportable=True |
| Microbiology - STEC | stec test ws id 84 | report_content | Report!A2:E2 | Report result content range | Yes/likely | Exportable=True |
| Microbiology - STEC | stec test ws id 84 | report_header | Report!A1:E1 | Report table header range | Yes/likely | Exportable=True |
| Microbiology - STEC | stec test ws id 84 | report_results | Report!A1:E2 | Full report result range | Yes/likely | Exportable=True |
| Microbiology - STEC | stec test ws id 84 | stec_limit | Specifications!C5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=STEC Limit |
| Microbiology - STEC | stec test ws id 84 | stec_loq | Specifications!B5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=STEC LOQ |
| Microbiology - STEC | stec test ws id 84 | stec_mu | Specifications!E5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=STEC MU |
| Microbiology - STEC | stec test ws id 84 | stec_result | Specifications!D5 | Assay result field | Unknown | Exportable=True; Display=STEC Result |
| Microbiology - STEC | stec test ws id 84 | stec_results | Data!E2 | Assay result field | Unknown | Exportable=True; Display=STEC Results |
| Microbiology - STEC | stec test ws id 84 | stec_status | Specifications!F5 | Worksheet named cell | Unknown | Exportable=True; Display=STEC Status |
| Microbiology - TAMC | total aerobic count test ws id 93 | ac_limit | Specifications!C5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Total Aerobic Count Limit |
| Microbiology - TAMC | total aerobic count test ws id 93 | ac_loq | Specifications!B5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Total Aerobic Count LOQ |
| Microbiology - TAMC | total aerobic count test ws id 93 | ac_mu | Specifications!E5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Total Aerobic Count MU |
| Microbiology - TAMC | total aerobic count test ws id 93 | ac_result | Specifications!D5 | Assay result field | Unknown | Exportable=True; Display=Total Aerobic Count Result |
| Microbiology - TAMC | total aerobic count test ws id 93 | ac_results | Data!E2 | Assay result field | Unknown | Exportable=True; Display=Total Aerobic Count Results |
| Microbiology - TAMC | total aerobic count test ws id 93 | ac_status | Specifications!F5 | Worksheet named cell | Unknown | Exportable=True; Display=Total Aerobic Count Status |
| Microbiology - TAMC | total aerobic count test ws id 93 | pass_fail | Specifications!D2 | Pass/fail status for report and/or METRC | Yes/likely | Exportable=True |
| Microbiology - TAMC | total aerobic count test ws id 93 | report_content | Report!A2:E2 | Report result content range | Yes/likely | Exportable=True |
| Microbiology - TAMC | total aerobic count test ws id 93 | report_header | Report!A1:E1 | Report table header range | Yes/likely | Exportable=True |
| Microbiology - TAMC | total aerobic count test ws id 93 | report_results | Report!A1:E2 | Full report result range | Yes/likely | Exportable=True |
| Microbiology - TYMC | total yeast and mold test ws id 94 | pass_fail | Specifications!D2 | Pass/fail status for report and/or METRC | Yes/likely | Exportable=True |
| Microbiology - TYMC | total yeast and mold test ws id 94 | report_content | Report!A2:E2 | Report result content range | Yes/likely | Exportable=True |
| Microbiology - TYMC | total yeast and mold test ws id 94 | report_header | Report!A1:E1 | Report table header range | Yes/likely | Exportable=True |
| Microbiology - TYMC | total yeast and mold test ws id 94 | report_results | Report!A1:E2 | Full report result range | Yes/likely | Exportable=True |
| Microbiology - TYMC | total yeast and mold test ws id 94 | ym_limit | Specifications!C5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Total Yeast and Mold Limit |
| Microbiology - TYMC | total yeast and mold test ws id 94 | ym_loq | Specifications!B5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Total Yeast and Mold LOQ |
| Microbiology - TYMC | total yeast and mold test ws id 94 | ym_mu | Specifications!E5 | Specification or measurement uncertainty field | Unknown | Exportable=True; Display=Total Yeast and Mold MU |
| Microbiology - TYMC | total yeast and mold test ws id 94 | ym_result | Specifications!D5 | Assay result field | Unknown | Exportable=True; Display=Total Yeast and Mold Result |
| Microbiology - TYMC | total yeast and mold test ws id 94 | ym_results | Data!E2 | Assay result field | Unknown | Exportable=True; Display=YM Automation Results |
| Microbiology - TYMC | total yeast and mold test ws id 94 | ym_status | Specifications!F5 | Worksheet named cell | Unknown | Exportable=True; Display=Total Yeast and Mold Status |
| Mycotoxins | mycotoxin qualitative test ws id 10 | aflatoxinb1 | Data!E2 | Worksheet named cell | Unknown | Exportable=True; Display=Aflatoxin B1 |
| Mycotoxins | mycotoxin qualitative test ws id 10 | aflatoxinb1_metrc | Specifications!D5 | METRC reporting field | Yes/likely | Exportable=True |
| Mycotoxins | mycotoxin qualitative test ws id 10 | aflatoxinb2 | Data!F2 | Worksheet named cell | Unknown | Exportable=True; Display=Aflatoxin B2 |
| Mycotoxins | mycotoxin qualitative test ws id 10 | aflatoxinb2_metrc | Specifications!D6 | METRC reporting field | Yes/likely | Exportable=True |
| Mycotoxins | mycotoxin qualitative test ws id 10 | aflatoxing1 | Data!G2 | Worksheet named cell | Unknown | Exportable=True; Display=Aflatoxin G1 |
| Mycotoxins | mycotoxin qualitative test ws id 10 | aflatoxing1_metrc | Specifications!D7 | METRC reporting field | Yes/likely | Exportable=True |
| Mycotoxins | mycotoxin qualitative test ws id 10 | aflatoxing2 | Data!H2 | Worksheet named cell | Unknown | Exportable=True; Display=Aflatoxin G2 |
| Mycotoxins | mycotoxin qualitative test ws id 10 | aflatoxing2_metrc | Specifications!D8 | METRC reporting field | Yes/likely | Exportable=True |
| Mycotoxins | mycotoxin qualitative test ws id 10 | df | Data!J2 | Dilution factor | Unknown | Exportable=True |
| Mycotoxins | mycotoxin qualitative test ws id 10 | mycotoxin_results | Data!E2:I2 | Assay result field | Unknown | Exportable=True; Display=Mycotoxin Results |
| Mycotoxins | mycotoxin qualitative test ws id 10 | ochratoxina | Data!I2 | Worksheet named cell | Unknown | Exportable=True; Display=Ochratoxin A |
| Mycotoxins | mycotoxin qualitative test ws id 10 | ochratoxina_metrc | Specifications!D9 | METRC reporting field | Yes/likely | Exportable=True |
| Mycotoxins | mycotoxin qualitative test ws id 10 | pass_fail | Specifications!F2 | Pass/fail status for report and/or METRC | Yes/likely | Exportable=True |
| Mycotoxins | mycotoxin qualitative test ws id 10 | report_results | Report!A1:F8 | Full report result range | Yes/likely | Exportable=True |
| Mycotoxins | mycotoxin qualitative test ws id 10 | totalmycod_b1b2g1g2_metrc | Specifications!D11 | METRC reporting field | Yes/likely | Exportable=True |
| Mycotoxins | mycotoxin qualitative test ws id 10 | totalmycod_b1b2g1g2oa_metrc | Specifications!D10 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | abamectin_metrc | Specifications!E5 | METRC reporting field | Yes/likely | Exportable=True; Display=Abamectin METRC |
| Pesticides | pesticides qualitative test ws id 14 | acephate_metrc | Specifications!E6 | METRC reporting field | Yes/likely | Exportable=True; Display=Acephate METRC |
| Pesticides | pesticides qualitative test ws id 14 | acequinocyl_metrc | Specifications!E7 | METRC reporting field | Yes/likely | Exportable=True; Display=Acequinocyl METRC |
| Pesticides | pesticides qualitative test ws id 14 | acetamiprid_metrc | Specifications!E8 | METRC reporting field | Yes/likely | Exportable=True; Display=Acetamiprid METRC |
| Pesticides | pesticides qualitative test ws id 14 | azadirachtin_metrc | Specifications!E9 | METRC reporting field | Yes/likely | Exportable=True; Display=Azadirachtin METRC |
| Pesticides | pesticides qualitative test ws id 14 | azoxystrobin_metrc | Specifications!E10 | METRC reporting field | Yes/likely | Exportable=True; Display=Azoxystrobin METRC |
| Pesticides | pesticides qualitative test ws id 14 | bifenazate_metrc | Specifications!E11 | METRC reporting field | Yes/likely | Exportable=True; Display=Bifenazate METRC |
| Pesticides | pesticides qualitative test ws id 14 | bifenthrin_metrc | Specifications!E12 | METRC reporting field | Yes/likely | Exportable=True; Display=Bifenthrin METRC |
| Pesticides | pesticides qualitative test ws id 14 | boscalid_metrc | Specifications!E13 | METRC reporting field | Yes/likely | Exportable=True; Display=Boscalid METRC |
| Pesticides | pesticides qualitative test ws id 14 | carbaryl_metrc | Specifications!E14 | METRC reporting field | Yes/likely | Exportable=True; Display=Carbaryl METRC |
| Pesticides | pesticides qualitative test ws id 14 | chlorantraniliprole_metrc | Specifications!E15 | METRC reporting field | Yes/likely | Exportable=True; Display=Chlorantraniliprole METRC |
| Pesticides | pesticides qualitative test ws id 14 | chlorfenapyr_metrc | Specifications!E16 | METRC reporting field | Yes/likely | Exportable=True; Display=Chlorfenapyr METRC |
| Pesticides | pesticides qualitative test ws id 14 | chlormequatchloride_metrc | Specifications!E17 | METRC reporting field | Yes/likely | Exportable=True; Display=Chlormequat Chloride METRC |
| Pesticides | pesticides qualitative test ws id 14 | chlorpyrifos_metrc | Specifications!E18 | METRC reporting field | Yes/likely | Exportable=True; Display=Chlorpyrifos METRC |
| Pesticides | pesticides qualitative test ws id 14 | clofentezine_metrc | Specifications!E19 | METRC reporting field | Yes/likely | Exportable=True; Display=Clofentezine METRC |
| Pesticides | pesticides qualitative test ws id 14 | cyfluthrin_metrc | Specifications!E20 | METRC reporting field | Yes/likely | Exportable=True; Display=Cyfluthrin METRC |
| Pesticides | pesticides qualitative test ws id 14 | cypermethrin_metrc | Specifications!E21 | METRC reporting field | Yes/likely | Exportable=True; Display=Cypermethrin METRC |
| Pesticides | pesticides qualitative test ws id 14 | daminozide_metrc | Specifications!E22 | METRC reporting field | Yes/likely | Exportable=True; Display=Daminozide METRC |
| Pesticides | pesticides qualitative test ws id 14 | df | Data!BH2 | Dilution factor | Unknown | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | diazinon_metrc | Specifications!E23 | METRC reporting field | Yes/likely | Exportable=True; Display=Diazinon METRC |
| Pesticides | pesticides qualitative test ws id 14 | dimethoate_metrc | Specifications!E25 | METRC reporting field | Yes/likely | Exportable=True; Display=Dimethoate METRC |
| Pesticides | pesticides qualitative test ws id 14 | etofenprox_metrc | Specifications!E26 | METRC reporting field | Yes/likely | Exportable=True; Display=Etofenprox METRC |
| Pesticides | pesticides qualitative test ws id 14 | etoxazole_metrc | Specifications!E27 | METRC reporting field | Yes/likely | Exportable=True; Display=Etoxazole METRC |
| Pesticides | pesticides qualitative test ws id 14 | fenoxycarb_metrc | Specifications!E28 | METRC reporting field | Yes/likely | Exportable=True; Display=Fenoxycarb METRC |
| Pesticides | pesticides qualitative test ws id 14 | fenpyroximate_metrc | Specifications!E29 | METRC reporting field | Yes/likely | Exportable=True; Display=Fenpyroximate METRC |
| Pesticides | pesticides qualitative test ws id 14 | fipronil_metrc | Specifications!E30 | METRC reporting field | Yes/likely | Exportable=True; Display=Fipronil METRC |
| Pesticides | pesticides qualitative test ws id 14 | flonicamid_metrc | Specifications!E31 | METRC reporting field | Yes/likely | Exportable=True; Display=Flonicamid METRC |
| Pesticides | pesticides qualitative test ws id 14 | fludioxonil_metrc | Specifications!E32 | METRC reporting field | Yes/likely | Exportable=True; Display=Fludioxonil METRC |
| Pesticides | pesticides qualitative test ws id 14 | hexythiazox_metrc | Specifications!E33 | METRC reporting field | Yes/likely | Exportable=True; Display=Hexythiazox METRC |
| Pesticides | pesticides qualitative test ws id 14 | imazalil_metrc | Specifications!E34 | METRC reporting field | Yes/likely | Exportable=True; Display=Imazalil METRC |
| Pesticides | pesticides qualitative test ws id 14 | imidacloprid_metrc | Specifications!E35 | METRC reporting field | Yes/likely | Exportable=True; Display=Imidacloprid METRC |
| Pesticides | pesticides qualitative test ws id 14 | kresoximmethyl_metrc | Specifications!E36 | METRC reporting field | Yes/likely | Exportable=True; Display=Kresoxim Methyl METRC |
| Pesticides | pesticides qualitative test ws id 14 | malathion_metrc | Specifications!E37 | METRC reporting field | Yes/likely | Exportable=True; Display=Malathion METRC |
| Pesticides | pesticides qualitative test ws id 14 | metalaxyl_metrc | Specifications!E38 | METRC reporting field | Yes/likely | Exportable=True; Display=Metalaxyl METRC |
| Pesticides | pesticides qualitative test ws id 14 | methiocarb_metrc | Specifications!E39 | METRC reporting field | Yes/likely | Exportable=True; Display=Methiocarb METRC |
| Pesticides | pesticides qualitative test ws id 14 | methomyl_metrc | Specifications!E40 | METRC reporting field | Yes/likely | Exportable=True; Display=Methomyl METRC |
| Pesticides | pesticides qualitative test ws id 14 | myclobutanil_metrc | Specifications!E41 | METRC reporting field | Yes/likely | Exportable=True; Display=Myclobutanil METRC |
| Pesticides | pesticides qualitative test ws id 14 | naled_metrc | Specifications!E42 | METRC reporting field | Yes/likely | Exportable=True; Display=Naled METRC |
| Pesticides | pesticides qualitative test ws id 14 | oxamyl_metrc | Specifications!E43 | METRC reporting field | Yes/likely | Exportable=True; Display=Oxamyl METRC |
| Pesticides | pesticides qualitative test ws id 14 | paclobutrazol_metrc | Specifications!E44 | METRC reporting field | Yes/likely | Exportable=True; Display=Paclobutrazol METRC |
| Pesticides | pesticides qualitative test ws id 14 | pass_fail | Specifications!F2 | Pass/fail status for report and/or METRC | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | permethrins_metrc | Specifications!E45 | METRC reporting field | Yes/likely | Exportable=True; Display=Permethrins METRC |
| Pesticides | pesticides qualitative test ws id 14 | pesticides_results | Data!E2:BG2 | Assay result field | Unknown | Exportable=True; Display=Pesticide Results |
| Pesticides | pesticides qualitative test ws id 14 | phosmet_metrc | Specifications!E46 | METRC reporting field | Yes/likely | Exportable=True; Display=Phosmet METRC |
| Pesticides | pesticides qualitative test ws id 14 | piperonyl_butoxide_metrc | Specifications!E47 | METRC reporting field | Yes/likely | Exportable=True; Display=Piperonyl Butoxide METRC |
| Pesticides | pesticides qualitative test ws id 14 | prallethrin_metrc | Specifications!E48 | METRC reporting field | Yes/likely | Exportable=True; Display=Prallethrin METRC |
| Pesticides | pesticides qualitative test ws id 14 | propiconazole_metrc | Specifications!E49 | METRC reporting field | Yes/likely | Exportable=True; Display=Propiconazole METRC |
| Pesticides | pesticides qualitative test ws id 14 | propoxur_metrc | Specifications!E50 | METRC reporting field | Yes/likely | Exportable=True; Display=Propoxur METRC |
| Pesticides | pesticides qualitative test ws id 14 | pyrethrins_metrc | Specifications!E51 | METRC reporting field | Yes/likely | Exportable=True; Display=Pyrethrins METRC |
| Pesticides | pesticides qualitative test ws id 14 | pyridaben_metrc | Specifications!E52 | METRC reporting field | Yes/likely | Exportable=True; Display=Pyridaben METRC |
| Pesticides | pesticides qualitative test ws id 14 | report_results | Report!A1:R25 | Full report result range | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | report_results_single | A1:F75 | Assay result field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | spinosad_metrc | Specifications!E55 | METRC reporting field | Yes/likely | Exportable=True; Display=Spinosad METRC |
| Pesticides | pesticides qualitative test ws id 14 | spiromesifen_metrc | Specifications!E56 | METRC reporting field | Yes/likely | Exportable=True; Display=Spiromesifen METRC |
| Pesticides | pesticides qualitative test ws id 14 | spirotetramat_metrc | Specifications!E57 | METRC reporting field | Yes/likely | Exportable=True; Display=Spirotetramat METRC |
| Pesticides | pesticides qualitative test ws id 14 | tebuconazole_metrc | Specifications!E58 | METRC reporting field | Yes/likely | Exportable=True; Display=Tebuconazole METRC |
| Pesticides | pesticides qualitative test ws id 14 | thiamethoxam_metrc | Specifications!E59 | METRC reporting field | Yes/likely | Exportable=True; Display=Thiamethoxam METRC |
| Pesticides | pesticides qualitative test ws id 14 | trifloxystrobin_metrc | Specifications!E60 | METRC reporting field | Yes/likely | Exportable=True; Display=Trifloxystrobin METRC |
| Pesticides | pesticides qualitative test ws id 14 | abamectin_metrc | Specifications!E5 | METRC reporting field | Yes/likely | Exportable=True; Display=Abamectin METRC |
| Pesticides | pesticides qualitative test ws id 14 | acephate_metrc | Specifications!E6 | METRC reporting field | Yes/likely | Exportable=True; Display=Acephate METRC |
| Pesticides | pesticides qualitative test ws id 14 | acequinocyl_metrc | Specifications!E7 | METRC reporting field | Yes/likely | Exportable=True; Display=Acequinocyl METRC |
| Pesticides | pesticides qualitative test ws id 14 | acetamiprid_metrc | Specifications!E8 | METRC reporting field | Yes/likely | Exportable=True; Display=Acetamiprid METRC |
| Pesticides | pesticides qualitative test ws id 14 | azadirachtin_metrc | Specifications!E9 | METRC reporting field | Yes/likely | Exportable=True; Display=Azadirachtin METRC |
| Pesticides | pesticides qualitative test ws id 14 | azoxystrobin_metrc | Specifications!E10 | METRC reporting field | Yes/likely | Exportable=True; Display=Azoxystrobin METRC |
| Pesticides | pesticides qualitative test ws id 14 | bifenazate_metrc | Specifications!E11 | METRC reporting field | Yes/likely | Exportable=True; Display=Bifenazate METRC |
| Pesticides | pesticides qualitative test ws id 14 | bifenthrin_metrc | Specifications!E12 | METRC reporting field | Yes/likely | Exportable=True; Display=Bifenthrin METRC |
| Pesticides | pesticides qualitative test ws id 14 | boscalid_metrc | Specifications!E13 | METRC reporting field | Yes/likely | Exportable=True; Display=Boscalid METRC |
| Pesticides | pesticides qualitative test ws id 14 | carbaryl_metrc | Specifications!E14 | METRC reporting field | Yes/likely | Exportable=True; Display=Carbaryl METRC |
| Pesticides | pesticides qualitative test ws id 14 | chlorantraniliprole_metrc | Specifications!E15 | METRC reporting field | Yes/likely | Exportable=True; Display=Chlorantraniliprole METRC |
| Pesticides | pesticides qualitative test ws id 14 | chlorfenapyr_metrc | Specifications!E16 | METRC reporting field | Yes/likely | Exportable=True; Display=Chlorfenapyr METRC |
| Pesticides | pesticides qualitative test ws id 14 | chlormequatchloride_metrc | Specifications!E17 | METRC reporting field | Yes/likely | Exportable=True; Display=Chlormequat Chloride METRC |
| Pesticides | pesticides qualitative test ws id 14 | chlorpyrifos_metrc | Specifications!E18 | METRC reporting field | Yes/likely | Exportable=True; Display=Chlorpyrifos METRC |
| Pesticides | pesticides qualitative test ws id 14 | clofentezine_metrc | Specifications!E19 | METRC reporting field | Yes/likely | Exportable=True; Display=Clofentezine METRC |
| Pesticides | pesticides qualitative test ws id 14 | cyfluthrin_metrc | Specifications!E20 | METRC reporting field | Yes/likely | Exportable=True; Display=Cyfluthrin METRC |
| Pesticides | pesticides qualitative test ws id 14 | cypermethrin_metrc | Specifications!E21 | METRC reporting field | Yes/likely | Exportable=True; Display=Cypermethrin METRC |
| Pesticides | pesticides qualitative test ws id 14 | daminozide_metrc | Specifications!E22 | METRC reporting field | Yes/likely | Exportable=True; Display=Daminozide METRC |
| Pesticides | pesticides qualitative test ws id 14 | df | Data!BH2 | Dilution factor | Unknown | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | diazinon_metrc | Specifications!E23 | METRC reporting field | Yes/likely | Exportable=True; Display=Diazinon METRC |
| Pesticides | pesticides qualitative test ws id 14 | dimethoate_metrc | Specifications!E25 | METRC reporting field | Yes/likely | Exportable=True; Display=Dimethoate METRC |
| Pesticides | pesticides qualitative test ws id 14 | etofenprox_metrc | Specifications!E26 | METRC reporting field | Yes/likely | Exportable=True; Display=Etofenprox METRC |
| Pesticides | pesticides qualitative test ws id 14 | etoxazole_metrc | Specifications!E27 | METRC reporting field | Yes/likely | Exportable=True; Display=Etoxazole METRC |
| Pesticides | pesticides qualitative test ws id 14 | fenoxycarb_metrc | Specifications!E28 | METRC reporting field | Yes/likely | Exportable=True; Display=Fenoxycarb METRC |
| Pesticides | pesticides qualitative test ws id 14 | fenpyroximate_metrc | Specifications!E29 | METRC reporting field | Yes/likely | Exportable=True; Display=Fenpyroximate METRC |
| Pesticides | pesticides qualitative test ws id 14 | fipronil_metrc | Specifications!E30 | METRC reporting field | Yes/likely | Exportable=True; Display=Fipronil METRC |
| Pesticides | pesticides qualitative test ws id 14 | flonicamid_metrc | Specifications!E31 | METRC reporting field | Yes/likely | Exportable=True; Display=Flonicamid METRC |
| Pesticides | pesticides qualitative test ws id 14 | fludioxonil_metrc | Specifications!E32 | METRC reporting field | Yes/likely | Exportable=True; Display=Fludioxonil METRC |
| Pesticides | pesticides qualitative test ws id 14 | hexythiazox_metrc | Specifications!E33 | METRC reporting field | Yes/likely | Exportable=True; Display=Hexythiazox METRC |
| Pesticides | pesticides qualitative test ws id 14 | imazalil_metrc | Specifications!E34 | METRC reporting field | Yes/likely | Exportable=True; Display=Imazalil METRC |
| Pesticides | pesticides qualitative test ws id 14 | imidacloprid_metrc | Specifications!E35 | METRC reporting field | Yes/likely | Exportable=True; Display=Imidacloprid METRC |
| Pesticides | pesticides qualitative test ws id 14 | kresoximmethyl_metrc | Specifications!E36 | METRC reporting field | Yes/likely | Exportable=True; Display=Kresoxim Methyl METRC |
| Pesticides | pesticides qualitative test ws id 14 | malathion_metrc | Specifications!E37 | METRC reporting field | Yes/likely | Exportable=True; Display=Malathion METRC |
| Pesticides | pesticides qualitative test ws id 14 | metalaxyl_metrc | Specifications!E38 | METRC reporting field | Yes/likely | Exportable=True; Display=Metalaxyl METRC |
| Pesticides | pesticides qualitative test ws id 14 | methiocarb_metrc | Specifications!E39 | METRC reporting field | Yes/likely | Exportable=True; Display=Methiocarb METRC |
| Pesticides | pesticides qualitative test ws id 14 | methomyl_metrc | Specifications!E40 | METRC reporting field | Yes/likely | Exportable=True; Display=Methomyl METRC |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_abamectin | METRC!A5 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_acephate | METRC!A6 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_acequinocyl | METRC!A7 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_acetamiprid | METRC!A8 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_azadirachtin | METRC!A9 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_azoxystrobin | METRC!A10 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_bifenazate | METRC!A11 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_bifenthrin | METRC!A12 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_boscalid | METRC!A13 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_carbaryl | METRC!A14 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_chlorantraniliprole | METRC!A15 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_chlorfenapyr | METRC!A16 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_chlormequat_chloride | METRC!A17 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_chlorpyrifos_dursban | METRC!A18 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_clofentezine | METRC!A19 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_cyfluthrin | METRC!A20 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_cypermethrin | METRC!A21 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_daminozide | METRC!A22 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_ddvp | METRC!A24 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_diazinon | METRC!A23 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_dimethoate | METRC!A25 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_etofenprox | METRC!A26 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_etoxazole | METRC!A27 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_fenoxycarb | METRC!A28 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_fenpyroximate | METRC!A29 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_fipronil | METRC!A30 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_flonicamid | METRC!A31 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_fludioxonil | METRC!A32 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_hexythiazox | METRC!A33 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_imazalil | METRC!A34 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_imidacloprid | METRC!A35 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_kresoxim_methyl | METRC!A36 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_malathion | METRC!A37 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_metalaxyl | METRC!A38 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_methiocarb | METRC!A39 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_methomyl | METRC!A40 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_myclobutanil | METRC!A41 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_naled | METRC!A42 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_oxamyl | METRC!A43 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_paclobutrazol | METRC!A44 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_permethrins | METRC!A45 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_phosmet | METRC!A46 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_piperonyl_butoxide | METRC!A47 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_prallethrin | METRC!A48 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_propiconazole | METRC!A49 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_propoxur | METRC!A50 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_pyrethrins | METRC!A51 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_pyridaben | METRC!A52 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_spinosad | METRC!A55 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_spiromesifen | METRC!A56 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_spirotetramat | METRC!A57 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_tebuconazole | METRC!A58 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_thiamethoxam | METRC!A59 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_analyte_name_trifloxystrobin | METRC!A60 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_abamectin | METRC!D5 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_acephate | METRC!D6 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_acequinocyl | METRC!D7 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_acetamiprid | METRC!D8 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_azadirachtin | METRC!D9 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_azoxystrobin | METRC!D10 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_bifenazate | METRC!D11 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_bifenthrin | METRC!D12 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_boscalid | METRC!D13 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_carbaryl | METRC!D14 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_chlorantraniliprole | METRC!D15 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_chlorfenapyr | METRC!D16 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_chlormequat_chloride | METRC!D17 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_chlorpyrifos_dursban | METRC!D18 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_clofentezine | METRC!D19 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_cyfluthrin | METRC!D20 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_cypermethrin | METRC!D21 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_daminozide | METRC!D22 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_ddvp | METRC!D24 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_diazinon | METRC!D23 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_dimethoate | METRC!D25 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_etofenprox | METRC!D26 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_etoxazole | METRC!D27 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_fenoxycarb | METRC!D28 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_fenpyroximate | METRC!D29 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_fipronil | METRC!D30 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_flonicamid | METRC!D31 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_fludioxonil | METRC!D32 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_hexythiazox | METRC!D33 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_imazalil | METRC!D34 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_imidacloprid | METRC!D35 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_kresoxim_methyl | METRC!D36 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_malathion | METRC!D37 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_metalaxyl | METRC!D38 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_methiocarb | METRC!D39 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_methomyl | METRC!D40 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_myclobutanil | METRC!D41 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_naled | METRC!D42 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_oxamyl | METRC!D43 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_paclobutrazol | METRC!D44 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_permethrins | METRC!D45 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_phosmet | METRC!D46 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_piperonyl_butoxide | METRC!D47 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_prallethrin | METRC!D48 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_propiconazole | METRC!D49 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_propoxur | METRC!D50 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_pyrethrins | METRC!D51 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_pyridaben | METRC!D52 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_spinosad | METRC!D55 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_spiromesifen | METRC!D56 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_spirotetramat | METRC!D57 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_tebuconazole | METRC!D58 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_thiamethoxam | METRC!D59 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_notes_trifloxystrobin | METRC!D60 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_abamectin | METRC!C5 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_acephate | METRC!C6 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_acequinocyl | METRC!C7 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_acetamiprid | METRC!C8 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_azadirachtin | METRC!C9 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_azoxystrobin | METRC!C10 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_bifenazate | METRC!C11 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_bifenthrin | METRC!C12 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_boscalid | METRC!C13 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_carbaryl | METRC!C14 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_chlorantraniliprole | METRC!C15 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_chlorfenapyr | METRC!C16 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_chlormequat_chloride | METRC!C17 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_chlorpyrifos_dursban | METRC!C18 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_clofentezine | METRC!C19 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_cyfluthrin | METRC!C20 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_cypermethrin | METRC!C21 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_daminozide | METRC!C22 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_ddvp | METRC!C24 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_diazinon | METRC!C23 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_dimethoate | METRC!C25 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_etofenprox | METRC!C26 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_etoxazole | METRC!C27 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_fenoxycarb | METRC!C28 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_fenpyroximate | METRC!C29 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_fipronil | METRC!C30 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_flonicamid | METRC!C31 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_fludioxonil | METRC!C32 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_hexythiazox | METRC!C33 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_imazalil | METRC!C34 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_imidacloprid | METRC!C35 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_kresoxim_methyl | METRC!C36 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_malathion | METRC!C37 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_metalaxyl | METRC!C38 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_methiocarb | METRC!C39 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_methomyl | METRC!C40 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_myclobutanil | METRC!C41 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_naled | METRC!C42 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_oxamyl | METRC!C43 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_paclobutrazol | METRC!C44 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_permethrins | METRC!C45 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_phosmet | METRC!C46 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_piperonyl_butoxide | METRC!C47 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_prallethrin | METRC!C48 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_propiconazole | METRC!C49 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_propoxur | METRC!C50 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_pyrethrins | METRC!C51 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_pyridaben | METRC!C52 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_spinosad | METRC!C55 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_spiromesifen | METRC!C56 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_spirotetramat | METRC!C57 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_tebuconazole | METRC!C58 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_thiamethoxam | METRC!C59 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_pass_fail_trifloxystrobin | METRC!C60 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_abamectin | METRC!B5 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_acephate | METRC!B6 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_acequinocyl | METRC!B7 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_acetamiprid | METRC!B8 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_azadirachtin | METRC!B9 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_azoxystrobin | METRC!B10 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_bifenazate | METRC!B11 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_bifenthrin | METRC!B12 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_boscalid | METRC!B13 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_carbaryl | METRC!B14 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_chlorantraniliprole | METRC!B15 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_chlorfenapyr | METRC!B16 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_chlormequat_chloride | METRC!B17 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_chlorpyrifos_dursban | METRC!B18 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_clofentezine | METRC!B19 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_cyfluthrin | METRC!B20 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_cypermethrin | METRC!B21 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_daminozide | METRC!B22 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_ddvp | METRC!B24 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_diazinon | METRC!B23 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_dimethoate | METRC!B25 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_etofenprox | METRC!B26 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_etoxazole | METRC!B27 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_fenoxycarb | METRC!B28 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_fenpyroximate | METRC!B29 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_fipronil | METRC!B30 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_flonicamid | METRC!B31 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_fludioxonil | METRC!B32 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_hexythiazox | METRC!B33 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_imazalil | METRC!B34 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_imidacloprid | METRC!B35 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_kresoxim_methyl | METRC!B36 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_malathion | METRC!B37 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_metalaxyl | METRC!B38 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_methiocarb | METRC!B39 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_methomyl | METRC!B40 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_myclobutanil | METRC!B41 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_naled | METRC!B42 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_oxamyl | METRC!B43 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_paclobutrazol | METRC!B44 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_permethrins | METRC!B45 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_phosmet | METRC!B46 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_piperonyl_butoxide | METRC!B47 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_prallethrin | METRC!B48 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_propiconazole | METRC!B49 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_propoxur | METRC!B50 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_pyrethrins | METRC!B51 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_pyridaben | METRC!B52 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_spinosad | METRC!B55 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_spiromesifen | METRC!B56 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_spirotetramat | METRC!B57 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_tebuconazole | METRC!B58 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_thiamethoxam | METRC!B59 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_quantity_trifloxystrobin | METRC!B60 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_abamectin | METRC!E5 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_acephate | METRC!E6 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_acequinocyl | METRC!E7 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_acetamiprid | METRC!E8 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_azadirachtin | METRC!E9 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_azoxystrobin | METRC!E10 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_bifenazate | METRC!E11 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_bifenthrin | METRC!E12 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_boscalid | METRC!E13 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_carbaryl | METRC!E14 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_chlorantraniliprole | METRC!E15 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_chlorfenapyr | METRC!E16 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_chlormequat_chloride | METRC!E17 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_chlorpyrifos_dursban | METRC!E18 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_clofentezine | METRC!E19 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_cyfluthrin | METRC!E20 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_cypermethrin | METRC!E21 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_daminozide | METRC!E22 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_ddvp | METRC!E24 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_diazinon | METRC!E23 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_dimethoate | METRC!E25 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_etofenprox | METRC!E26 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_etoxazole | METRC!E27 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_fenoxycarb | METRC!E28 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_fenpyroximate | METRC!E29 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_fipronil | METRC!E30 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_flonicamid | METRC!E31 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_fludioxonil | METRC!E32 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_hexythiazox | METRC!E33 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_imazalil | METRC!E34 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_imidacloprid | METRC!E35 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_kresoxim_methyl | METRC!E36 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_malathion | METRC!E37 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_metalaxyl | METRC!E38 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_methiocarb | METRC!E39 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_methomyl | METRC!E40 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_myclobutanil | METRC!E41 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_naled | METRC!E42 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_oxamyl | METRC!E43 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_paclobutrazol | METRC!E44 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_permethrins | METRC!E45 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_phosmet | METRC!E46 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_piperonyl_butoxide | METRC!E47 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_prallethrin | METRC!E48 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_propiconazole | METRC!E49 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_propoxur | METRC!E50 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_pyrethrins | METRC!E51 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_pyridaben | METRC!E52 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_spinosad | METRC!E55 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_spiromesifen | METRC!E56 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_spirotetramat | METRC!E57 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_tebuconazole | METRC!E58 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_thiamethoxam | METRC!E59 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | metrc_to_include_trifloxystrobin | METRC!E60 | METRC reporting field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | myclobutanil_metrc | Specifications!E41 | METRC reporting field | Yes/likely | Exportable=True; Display=Myclobutanil METRC |
| Pesticides | pesticides qualitative test ws id 14 | naled_metrc | Specifications!E42 | METRC reporting field | Yes/likely | Exportable=True; Display=Naled METRC |
| Pesticides | pesticides qualitative test ws id 14 | oxamyl_metrc | Specifications!E43 | METRC reporting field | Yes/likely | Exportable=True; Display=Oxamyl METRC |
| Pesticides | pesticides qualitative test ws id 14 | paclobutrazol_metrc | Specifications!E44 | METRC reporting field | Yes/likely | Exportable=True; Display=Paclobutrazol METRC |
| Pesticides | pesticides qualitative test ws id 14 | pass_fail | Specifications!F2 | Pass/fail status for report and/or METRC | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | permethrins_metrc | Specifications!E45 | METRC reporting field | Yes/likely | Exportable=True; Display=Permethrins METRC |
| Pesticides | pesticides qualitative test ws id 14 | pesticides_results | Data!E2:BG2 | Assay result field | Unknown | Exportable=True; Display=Pesticide Results |
| Pesticides | pesticides qualitative test ws id 14 | phosmet_metrc | Specifications!E46 | METRC reporting field | Yes/likely | Exportable=True; Display=Phosmet METRC |
| Pesticides | pesticides qualitative test ws id 14 | piperonyl_butoxide_metrc | Specifications!E47 | METRC reporting field | Yes/likely | Exportable=True; Display=Piperonyl Butoxide METRC |
| Pesticides | pesticides qualitative test ws id 14 | prallethrin_metrc | Specifications!E48 | METRC reporting field | Yes/likely | Exportable=True; Display=Prallethrin METRC |
| Pesticides | pesticides qualitative test ws id 14 | propiconazole_metrc | Specifications!E49 | METRC reporting field | Yes/likely | Exportable=True; Display=Propiconazole METRC |
| Pesticides | pesticides qualitative test ws id 14 | propoxur_metrc | Specifications!E50 | METRC reporting field | Yes/likely | Exportable=True; Display=Propoxur METRC |
| Pesticides | pesticides qualitative test ws id 14 | pyrethrins_metrc | Specifications!E51 | METRC reporting field | Yes/likely | Exportable=True; Display=Pyrethrins METRC |
| Pesticides | pesticides qualitative test ws id 14 | pyridaben_metrc | Specifications!E52 | METRC reporting field | Yes/likely | Exportable=True; Display=Pyridaben METRC |
| Pesticides | pesticides qualitative test ws id 14 | report_results | Report!A1:R25 | Full report result range | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | report_results_single | A1:F75 | Assay result field | Yes/likely | Exportable=True |
| Pesticides | pesticides qualitative test ws id 14 | spinosad_metrc | Specifications!E55 | METRC reporting field | Yes/likely | Exportable=True; Display=Spinosad METRC |
| Pesticides | pesticides qualitative test ws id 14 | spiromesifen_metrc | Specifications!E56 | METRC reporting field | Yes/likely | Exportable=True; Display=Spiromesifen METRC |
| Pesticides | pesticides qualitative test ws id 14 | spirotetramat_metrc | Specifications!E57 | METRC reporting field | Yes/likely | Exportable=True; Display=Spirotetramat METRC |
| Pesticides | pesticides qualitative test ws id 14 | tebuconazole_metrc | Specifications!E58 | METRC reporting field | Yes/likely | Exportable=True; Display=Tebuconazole METRC |
| Pesticides | pesticides qualitative test ws id 14 | thiamethoxam_metrc | Specifications!E59 | METRC reporting field | Yes/likely | Exportable=True; Display=Thiamethoxam METRC |
| Pesticides | pesticides qualitative test ws id 14 | trifloxystrobin_metrc | Specifications!E60 | METRC reporting field | Yes/likely | Exportable=True; Display=Trifloxystrobin METRC |
| Residual_Solvents | residual solvents test ws id 12 | acetone | Data!F2 | Worksheet named cell | Unknown | Exportable=True; Display=Acetone |
| Residual_Solvents | residual solvents test ws id 12 | acetone_metrc | Specifications!E9 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | acetonitrile | Data!G2 | Worksheet named cell | Unknown | Exportable=True; Display=Acetonitrile |
| Residual_Solvents | residual solvents test ws id 12 | benzene | Data!H2 | Worksheet named cell | Unknown | Exportable=True; Display=Benzene |
| Residual_Solvents | residual solvents test ws id 12 | benzene_metrc | Specifications!E11 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | butane_metrc | Specifications!E12 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | butanes | Data!I2 | Worksheet named cell | Unknown | Exportable=True; Display=Butanes |
| Residual_Solvents | residual solvents test ws id 12 | butanol_metrc | Specifications!E6 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | chloroform | Data!J2 | Worksheet named cell | Unknown | Exportable=True; Display=Chloroform |
| Residual_Solvents | residual solvents test ws id 12 | chloroform_metrc | Specifications!E13 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | cyclohexane | Data!K2 | Worksheet named cell | Unknown | Exportable=True; Display=Cyclohexane |
| Residual_Solvents | residual solvents test ws id 12 | cyclohexane_metrc | Specifications!E15 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | df | Data!X2 | Dilution factor | Unknown | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | dichloromethane | Data!L2 | Worksheet named cell | Unknown | Exportable=True; Display=Dichloromethane |
| Residual_Solvents | residual solvents test ws id 12 | dichloromethane_metrc | Specifications!E16 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | dioxane14_metrc | Specifications!E5 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | ethanol | Data!M2 | Worksheet named cell | Unknown | Exportable=True; Display=Ethanol |
| Residual_Solvents | residual solvents test ws id 12 | ethanol_metrc | Specifications!E17 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | ethoxyethanol_metrc | Specifications!E7 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | ethylacetate | Data!O2 | Worksheet named cell | Unknown | Exportable=True; Display=Ethyl Acetate |
| Residual_Solvents | residual solvents test ws id 12 | ethylacetate_metrc | Specifications!E19 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | ethylether | Data!N2 | Worksheet named cell | Unknown | Exportable=True; Display=Ethyl Ether |
| Residual_Solvents | residual solvents test ws id 12 | heptane | Data!P2 | Worksheet named cell | Unknown | Exportable=True; Display=Heptane |
| Residual_Solvents | residual solvents test ws id 12 | heptane_metrc | Specifications!E22 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | hexane_metrc | Specifications!E23 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | hexanes | Data!Q2 | Worksheet named cell | Unknown | Exportable=True; Display=Hexanes |
| Residual_Solvents | residual solvents test ws id 12 | isopropanol2_metrc | Specifications!E8 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | methanol | Data!R2 | Worksheet named cell | Unknown | Exportable=True; Display=Methanol |
| Residual_Solvents | residual solvents test ws id 12 | methanol_metrc | Specifications!E25 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | pass_fail | Specifications!F2 | Pass/fail status for report and/or METRC | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | pentane_metrc | Specifications!E26 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | pentanes | Data!S2 | Worksheet named cell | Unknown | Exportable=True; Display=Pentanes |
| Residual_Solvents | residual solvents test ws id 12 | propane | Data!T2 | Worksheet named cell | Unknown | Exportable=True; Display=Propane |
| Residual_Solvents | residual solvents test ws id 12 | propane_metrc | Specifications!E27 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | propranolipa2 | Data!E2 | Worksheet named cell | Unknown | Exportable=True; Display=2 Propanol IPA |
| Residual_Solvents | residual solvents test ws id 12 | report_results | Report!A1:F31 | Full report result range | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | residual_solvents_results | Data!E2:W2 | Assay result field | Unknown | Exportable=True; Display=Residual Solvents Results |
| Residual_Solvents | residual solvents test ws id 12 | toluene | Data!U2 | Worksheet named cell | Unknown | Exportable=True; Display=Toluene |
| Residual_Solvents | residual solvents test ws id 12 | toluene_metrc | Specifications!E29 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | totalxylenes | Data!V2 | Worksheet named cell | Unknown | Exportable=True; Display=Total Xylenes |
| Residual_Solvents | residual solvents test ws id 12 | totalxylenes_metrc | Specifications!E30 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | trichloroethene | Data!W2 | Worksheet named cell | Unknown | Exportable=True; Display=Trichloroethene |
| Residual_Solvents | residual solvents test ws id 12 | trichloroethene_metrc | Specifications!E31 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | acetone | Data!F2 | Worksheet named cell | Unknown | Exportable=True; Display=Acetone |
| Residual_Solvents | residual solvents test ws id 12 | acetone_metrc | Specifications!E9 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | acetonitrile | Data!G2 | Worksheet named cell | Unknown | Exportable=True; Display=Acetonitrile |
| Residual_Solvents | residual solvents test ws id 12 | benzene | Data!H2 | Worksheet named cell | Unknown | Exportable=True; Display=Benzene |
| Residual_Solvents | residual solvents test ws id 12 | benzene_metrc | Specifications!E11 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | butane_metrc | Specifications!E12 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | butanes | Data!I2 | Worksheet named cell | Unknown | Exportable=True; Display=Butanes |
| Residual_Solvents | residual solvents test ws id 12 | butanol_metrc | Specifications!E6 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | chloroform | Data!J2 | Worksheet named cell | Unknown | Exportable=True; Display=Chloroform |
| Residual_Solvents | residual solvents test ws id 12 | chloroform_metrc | Specifications!E13 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | cyclohexane | Data!K2 | Worksheet named cell | Unknown | Exportable=True; Display=Cyclohexane |
| Residual_Solvents | residual solvents test ws id 12 | cyclohexane_metrc | Specifications!E15 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | df | Data!X2 | Dilution factor | Unknown | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | dichloromethane | Data!L2 | Worksheet named cell | Unknown | Exportable=True; Display=Dichloromethane |
| Residual_Solvents | residual solvents test ws id 12 | dichloromethane_metrc | Specifications!E16 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | dioxane14_metrc | Specifications!E5 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | ethanol | Data!M2 | Worksheet named cell | Unknown | Exportable=True; Display=Ethanol |
| Residual_Solvents | residual solvents test ws id 12 | ethanol_metrc | Specifications!E17 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | ethoxyethanol_metrc | Specifications!E7 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | ethylacetate | Data!O2 | Worksheet named cell | Unknown | Exportable=True; Display=Ethyl Acetate |
| Residual_Solvents | residual solvents test ws id 12 | ethylacetate_metrc | Specifications!E19 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | ethylether | Data!N2 | Worksheet named cell | Unknown | Exportable=True; Display=Ethyl Ether |
| Residual_Solvents | residual solvents test ws id 12 | heptane | Data!P2 | Worksheet named cell | Unknown | Exportable=True; Display=Heptane |
| Residual_Solvents | residual solvents test ws id 12 | heptane_metrc | Specifications!E22 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | hexane_metrc | Specifications!E23 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | hexanes | Data!Q2 | Worksheet named cell | Unknown | Exportable=True; Display=Hexanes |
| Residual_Solvents | residual solvents test ws id 12 | isopropanol2_metrc | Specifications!E8 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | methanol | Data!R2 | Worksheet named cell | Unknown | Exportable=True; Display=Methanol |
| Residual_Solvents | residual solvents test ws id 12 | methanol_metrc | Specifications!E25 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_acetone | METRC!A6 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_benzene | METRC!A8 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_butane | METRC!A9 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_chloroform | METRC!A10 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_cyclohexane | METRC!A11 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_dichloromethane | METRC!A12 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_ethanol | METRC!A13 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_ethylacetate | METRC!A15 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_heptane | METRC!A16 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_hexane | METRC!A17 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_isopropanol2 | METRC!A5 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_methanol | METRC!A18 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_pentane | METRC!A19 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_propane | METRC!A20 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_toluene | METRC!A21 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_totalxylenes | METRC!A22 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_analyte_name_trichloroethene | METRC!A23 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_acetone | METRC!D6 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_benzene | METRC!D8 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_butane | METRC!D9 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_chloroform | METRC!D10 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_cyclohexane | METRC!D11 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_dichloromethane | METRC!D12 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_ethanol | METRC!D13 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_ethylacetate | METRC!D15 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_heptane | METRC!D16 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_hexane | METRC!D17 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_isopropanol2 | METRC!D5 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_methanol | METRC!D18 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_pentane | METRC!D19 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_propane | METRC!D20 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_toluene | METRC!D21 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_totalxylenes | METRC!D22 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_notes_trichloroethene | METRC!D23 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_acetone | METRC!C6 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_benzene | METRC!C8 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_butane | METRC!C9 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_chloroform | METRC!C10 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_cyclohexane | METRC!C11 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_dichloromethane | METRC!C12 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_ethanol | METRC!C13 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_ethylacetate | METRC!C15 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_heptane | METRC!C16 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_hexane | METRC!C17 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_isopropanol2 | METRC!C5 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_methanol | METRC!C18 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_pentane | METRC!C19 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_propane | METRC!C20 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_toluene | METRC!C21 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_totalxylenes | METRC!C22 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_pass_fail_trichloroethene | METRC!C23 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_acetone | METRC!B6 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_benzene | METRC!B8 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_butane | METRC!B9 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_chloroform | METRC!B10 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_cyclohexane | METRC!B11 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_dichloromethane | METRC!B12 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_ethanol | METRC!B13 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_ethylacetate | METRC!B15 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_heptane | METRC!B16 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_hexane | METRC!B17 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_isopropanol2 | METRC!B5 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_methanol | METRC!B18 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_pentane | METRC!B19 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_propane | METRC!B20 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_toluene | METRC!B21 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_totalxylenes | METRC!B22 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_quantity_trichloroethene | METRC!B23 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_acetone | METRC!E6 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_benzene | METRC!E8 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_butane | METRC!E9 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_chloroform | METRC!E10 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_cyclohexane | METRC!E11 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_dichloromethane | METRC!E12 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_ethanol | METRC!E13 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_ethylacetate | METRC!E15 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_heptane | METRC!E16 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_hexane | METRC!E17 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_isopropanol2 | METRC!E5 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_methanol | METRC!E18 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_pentane | METRC!E19 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_propane | METRC!E20 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_toluene | METRC!E21 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_totalxylenes | METRC!E22 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | metrc_to_include_trichloroethene | METRC!E23 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | pass_fail | Specifications!F2 | Pass/fail status for report and/or METRC | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | pentane_metrc | Specifications!E26 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | pentanes | Data!S2 | Worksheet named cell | Unknown | Exportable=True; Display=Pentanes |
| Residual_Solvents | residual solvents test ws id 12 | propane | Data!T2 | Worksheet named cell | Unknown | Exportable=True; Display=Propane |
| Residual_Solvents | residual solvents test ws id 12 | propane_metrc | Specifications!E27 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | propranolipa2 | Data!E2 | Worksheet named cell | Unknown | Exportable=True; Display=2 Propanol IPA |
| Residual_Solvents | residual solvents test ws id 12 | report_results | Report!A1:F31 | Full report result range | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | residual_solvents_results | Data!E2:W2 | Assay result field | Unknown | Exportable=True; Display=Residual Solvents Results |
| Residual_Solvents | residual solvents test ws id 12 | toluene | Data!U2 | Worksheet named cell | Unknown | Exportable=True; Display=Toluene |
| Residual_Solvents | residual solvents test ws id 12 | toluene_metrc | Specifications!E29 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | totalxylenes | Data!V2 | Worksheet named cell | Unknown | Exportable=True; Display=Total Xylenes |
| Residual_Solvents | residual solvents test ws id 12 | totalxylenes_metrc | Specifications!E30 | METRC reporting field | Yes/likely | Exportable=True |
| Residual_Solvents | residual solvents test ws id 12 | trichloroethene | Data!W2 | Worksheet named cell | Unknown | Exportable=True; Display=Trichloroethene |
| Residual_Solvents | residual solvents test ws id 12 | trichloroethene_metrc | Specifications!E31 | METRC reporting field | Yes/likely | Exportable=True |
| Terpenes | terpenes test ws id 42 | ahumulene_metrc | D22 | METRC reporting field | Yes/likely | Exportable=True; Display=A Humulene METRC |
| Terpenes | terpenes test ws id 42 | ahumulene_metrc_mgg | E22 | METRC reporting field | Yes/likely | Exportable=True; Display=A Humulene METRC mg/g |
| Terpenes | terpenes test ws id 42 | apinene_metrc | D5 | METRC reporting field | Yes/likely | Exportable=True; Display=A Pinene METRC |
| Terpenes | terpenes test ws id 42 | apinene_metrc_mgg | E5 | METRC reporting field | Yes/likely | Exportable=True; Display=A Pinene METRC mg/g |
| Terpenes | terpenes test ws id 42 | aterpinene_metrc | D10 | METRC reporting field | Yes/likely | Exportable=True; Display=A Terpinene METRC |
| Terpenes | terpenes test ws id 42 | aterpinene_metrc_mgg | E10 | METRC reporting field | Yes/likely | Exportable=True; Display=A Terpinene METRC mg/g |
| Terpenes | terpenes test ws id 42 | bcaryophyllene_metrc | D21 | METRC reporting field | Yes/likely | Exportable=True; Display=B Caryophyllene METRC |
| Terpenes | terpenes test ws id 42 | bcaryophyllene_metrc_mgg | E21 | METRC reporting field | Yes/likely | Exportable=True; Display=B Caryophyllene METRC mg/g |
| Terpenes | terpenes test ws id 42 | bisabolol_metrc | D27 | METRC reporting field | Yes/likely | Exportable=True; Display=Bisabolol METRC |
| Terpenes | terpenes test ws id 42 | bisabolol_metrc_mgg | E27 | METRC reporting field | Yes/likely | Exportable=True; Display=Bisabolol METRC mg/g |
| Terpenes | terpenes test ws id 42 | bmyrcene_metrc | D7 | METRC reporting field | Yes/likely | Exportable=True; Display=B Myrcene METRC |
| Terpenes | terpenes test ws id 42 | bmyrcene_metrc_mgg | E7 | METRC reporting field | Yes/likely | Exportable=True; Display=B Myrcene METRC mg/g |
| Terpenes | terpenes test ws id 42 | bpinene_metrc | D8 | METRC reporting field | Yes/likely | Exportable=True; Display=B Pinene METRC |
| Terpenes | terpenes test ws id 42 | bpinene_metrc_mgg | E8 | METRC reporting field | Yes/likely | Exportable=True; Display=B Pinene METRC mg/g |
| Terpenes | terpenes test ws id 42 | camphene_metrc | D6 | METRC reporting field | Yes/likely | Exportable=True; Display=Camphene METRC |
| Terpenes | terpenes test ws id 42 | camphene_metrc_mgg | E6 | METRC reporting field | Yes/likely | Exportable=True; Display=Camphene METRC mg/g |
| Terpenes | terpenes test ws id 42 | caryophylleneoxide_metrc | D26 | METRC reporting field | Yes/likely | Exportable=True; Display=Caryophyllene Oxide METRC |
| Terpenes | terpenes test ws id 42 | caryophylleneoxide_metrc_mgg | E26 | METRC reporting field | Yes/likely | Exportable=True; Display=Caryophyllene Oxide METRC mg/g |
| Terpenes | terpenes test ws id 42 | cisnerolidol_metrc | D23 | METRC reporting field | Yes/likely | Exportable=True; Display=Cis Nerolidol METRC |
| Terpenes | terpenes test ws id 42 | cisnerolidol_metrc_mgg | E23 | METRC reporting field | Yes/likely | Exportable=True; Display=Cis Nerolidol METRC mg/g |
| Terpenes | terpenes test ws id 42 | cisocimene_metrc | D11 | METRC reporting field | Yes/likely | Exportable=True; Display=Cis Ocimene METRC |
| Terpenes | terpenes test ws id 42 | cisocimene_metrc_mgg | E11 | METRC reporting field | Yes/likely | Exportable=True; Display=Cis Ocimene METRC mg/g |
| Terpenes | terpenes test ws id 42 | delta3carene_metrc | D9 | METRC reporting field | Yes/likely | Exportable=True; Display=Delta 3 Carene METRC |
| Terpenes | terpenes test ws id 42 | delta3carene_metrc_mgg | E9 | METRC reporting field | Yes/likely | Exportable=True; Display=Delta 3 Carene METRC mg/g |
| Terpenes | terpenes test ws id 42 | dlimonene_metrc | D12 | METRC reporting field | Yes/likely | Exportable=True; Display=D Limonene METRC |
| Terpenes | terpenes test ws id 42 | dlimonene_metrc_mgg | E12 | METRC reporting field | Yes/likely | Exportable=True; Display=D Limonene METRC mg/g |
| Terpenes | terpenes test ws id 42 | eucalyptol_metrc | D15 | METRC reporting field | Yes/likely | Exportable=True; Display=Eucalyptol METRC |
| Terpenes | terpenes test ws id 42 | eucalyptol_metrc_mgg | E15 | METRC reporting field | Yes/likely | Exportable=True; Display=Eucalyptol METRC mg/g |
| Terpenes | terpenes test ws id 42 | geraniol_metrc | D20 | METRC reporting field | Yes/likely | Exportable=True; Display=Geraniol METRC |
| Terpenes | terpenes test ws id 42 | geraniol_metrc_mgg | E20 | METRC reporting field | Yes/likely | Exportable=True; Display=Geraniol METRC mg/g |
| Terpenes | terpenes test ws id 42 | gterpinene_metrc | D16 | METRC reporting field | Yes/likely | Exportable=True; Display=G Terpinene METRC |
| Terpenes | terpenes test ws id 42 | gterpinene_metrc_mgg | E16 | METRC reporting field | Yes/likely | Exportable=True; Display=G Terpinene METRC mg/g |
| Terpenes | terpenes test ws id 42 | guaiol_metrc | D25 | METRC reporting field | Yes/likely | Exportable=True; Display=Guaiol METRC |
| Terpenes | terpenes test ws id 42 | guaiol_metrc_mgg | E25 | METRC reporting field | Yes/likely | Exportable=True; Display=Guaiol METRC mg/g |
| Terpenes | terpenes test ws id 42 | isopulegol_metrc | D19 | METRC reporting field | Yes/likely | Exportable=True; Display=Isopulegol METRC |
| Terpenes | terpenes test ws id 42 | isopulegol_metrc_mgg | E19 | METRC reporting field | Yes/likely | Exportable=True; Display=Isopulegol METRC mg/g |
| Terpenes | terpenes test ws id 42 | linalool_metrc | D18 | METRC reporting field | Yes/likely | Exportable=True; Display=Linalool METRC |
| Terpenes | terpenes test ws id 42 | linalool_metrc_mgg | E18 | METRC reporting field | Yes/likely | Exportable=True; Display=Linalool METRC mg/g |
| Terpenes | terpenes test ws id 42 | pcymene_metrc | D13 | METRC reporting field | Yes/likely | Exportable=True; Display=P Cymene METRC |
| Terpenes | terpenes test ws id 42 | pcymene_metrc_mgg | E13 | METRC reporting field | Yes/likely | Exportable=True; Display=P Cymene METRC mg/g |
| Terpenes | terpenes test ws id 42 | terpinolene_metrc | D17 | METRC reporting field | Yes/likely | Exportable=True; Display=Terpinolene METRC |
| Terpenes | terpenes test ws id 42 | terpinolene_metrc_mgg | E17 | METRC reporting field | Yes/likely | Exportable=True; Display=Terpinolene METRC mg/g |
| Terpenes | terpenes test ws id 42 | testterpenes | E4 | Worksheet named cell | Unknown | Exportable=True; Display=Test Terpenes |
| Terpenes | terpenes test ws id 42 | transnerolidol_metrc | D24 | METRC reporting field | Yes/likely | Exportable=True; Display=Trans Nerolidol METRC |
| Terpenes | terpenes test ws id 42 | transnerolidol_metrc_mgg | E24 | METRC reporting field | Yes/likely | Exportable=True; Display=Trans Nerolidol METRC mg/g |
| Terpenes | terpenes test ws id 42 | transocimene_metrc | D14 | METRC reporting field | Yes/likely | Exportable=True; Display=Trans Ocimene METRC |
| Terpenes | terpenes test ws id 42 | transocimene_metrc_mgg | E14 | METRC reporting field | Yes/likely | Exportable=True; Display=Trans Ocimene METRC mg/g |
| Water_Activity | water activity batch ws id 29 | test | F2 | Worksheet named cell | Unknown | Exportable=True; Display=stes |
| Water_Activity | water activity batch ws id 29 | test2 | F3 | Worksheet named cell | Unknown | Exportable=True; Display=steste |
| Water_Activity | water activity test ws id 28 | metrc_analyte_name_wateractivity | METRC!A5 | METRC reporting field | Yes/likely | Exportable=True |
| Water_Activity | water activity test ws id 28 | metrc_notes_wateractivity | METRC!D5 | METRC reporting field | Yes/likely | Exportable=True |
| Water_Activity | water activity test ws id 28 | metrc_pass_fail_wateractivity | METRC!C5 | METRC reporting field | Yes/likely | Exportable=True |
| Water_Activity | water activity test ws id 28 | metrc_quantity_wateractivity | METRC!B5 | METRC reporting field | Yes/likely | Exportable=True |
| Water_Activity | water activity test ws id 28 | metrc_to_include_wateractivity | METRC!E5 | METRC reporting field | Yes/likely | Exportable=True |
| Water_Activity | water activity test ws id 28 | pass_fail_report | Specifications!B7 | Worksheet named cell | Yes/likely | Exportable=True |
| Water_Activity | water activity test ws id 28 | report_content | Report!A2:E2 | Report result content range | Yes/likely | Exportable=True |
| Water_Activity | water activity test ws id 28 | report_header | Report!A1:E1 | Report table header range | Yes/likely | Exportable=True |
| Water_Activity | water activity test ws id 28 | report_results | Report!A1:E2 | Full report result range | Yes/likely | Exportable=True |
| Water_Activity | water activity test ws id 28 | wateractivity_metrc | Specifications!D5 | METRC reporting field | Yes/likely | Exportable=True |
| Water_Activity | water activity test ws id 28 | wateractivityaw | Data!D2 | Worksheet named cell | Unknown | Exportable=True; Display=Water Activity aw |

## Authoritative historical baseline — Rescan 2026-07-04 (first preserved copy)

| Assay | Worksheet | Named Cell | Cell/Range | Purpose | Used by COA? | Notes |
|---|---|---|---|---|---|---|
| Other | Example Batch Worksheet | control | D2 | Control  | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Other | [Batch] Example Worksheet | control | D2 | Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Other | Training Worksheet | example_named_cell | General!A18 | Example | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic | Data!E2 | Arsenic | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_limit | Specifications!C5 | Arsenic Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_loq | Specifications!B5 | Arsenic LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_mu | Specifications!E5 | Arsenic MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_result | Specifications!D5 | Arsenic Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_status | Specifications!F5 | Arsenic Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium | Data!F2 | Cadmium  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_limit | Specifications!C6 | Cadmium Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_loq | Specifications!B6 | Cadmium LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_mu | Specifications!E6 | Cadmium MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_result | Specifications!D6 | Cadmium Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_status | Specifications!F6 | Cadmium Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | df | Data!I2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead | Data!G2 | Lead | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead_limit | Specifications!C7 | Lead Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead_loq | Specifications!B7 | Lead LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead_mu | Specifications!E7 | Lead MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead_result | Specifications!D7 | Lead Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury | Data!H2 | Mercury | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_limit | Specifications!C8 | Mercury Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_loq | Specifications!B8 | Mercury LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_mu | Specifications!E8 | Mercury MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_result | Specifications!D8 | Mercury Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_status | Specifications!F8 | Mercury Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | report_results | Report!A1:F6 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | df | Data!G2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | purity_results | 'Purity Data'!C2:R2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | report_results | Report!A1:F21 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_1 | Data!E5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_10 | Data!N5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_11 | Data!O5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_12 | Data!P5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_13 | Data!Q5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_14 | 'Purity Data'!C2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_15 | 'Purity Data'!D2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_16 | 'Purity Data'!E2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_17 | 'Purity Data'!F2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_18 | 'Purity Data'!G2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_19 | 'Purity Data'!H2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_2 | Data!F5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_20 | 'Purity Data'!I2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_21 | 'Purity Data'!J2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_22 | 'Purity Data'!K2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_23 | 'Purity Data'!L2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_24 | 'Purity Data'!M2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_25 | 'Purity Data'!N2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_26 | 'Purity Data'!O2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_27 | 'Purity Data'!P2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_28 | 'Purity Data'!Q2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_29 | 'Purity Data'!R2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_3 | Data!G5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_4 | Data!H5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_5 | Data!I5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_6 | Data!J5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_7 | Data!K5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_8 | Data!L5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_9 | Data!M5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | results | Data!E5:Q5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | total_thc | Report!B1 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | total_thc_report_result | Data!C11 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxinb1 | Data!E2 | Aflatoxin B1 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxinb1_metrc | Specifications!D5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxinb2 | Data!F2 | Aflatoxin B2 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxinb2_metrc | Specifications!D6 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxing1 | Data!G2 | Aflatoxin G1 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxing1_metrc | Specifications!D7 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxing2 | Data!H2 | Aflatoxin G2 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxing2_metrc | Specifications!D8 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | df | Data!J2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | mycotoxin_results | Data!E2:I2 | Mycotoxin Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | ochratoxina | Data!I2 | Ochratoxin A | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | ochratoxina_metrc | Specifications!D9 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | pass_fail | Specifications!F2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | report_results | Report!A1:F8 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | totalmycod_b1b2g1g2_metrc | Specifications!D11 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | totalmycod_b1b2g1g2oa_metrc | Specifications!D10 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | acetone | Data!F2 | Acetone | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | acetone_metrc | Specifications!E9 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | acetonitrile | Data!G2 | Acetonitrile | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | benzene | Data!H2 | Benzene | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | benzene_metrc | Specifications!E11 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | butane_metrc | Specifications!E12 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | butanes | Data!I2 | Butanes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | butanol_metrc | Specifications!E6 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | chloroform | Data!J2 | Chloroform | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | chloroform_metrc | Specifications!E13 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | cyclohexane | Data!K2 | Cyclohexane | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | cyclohexane_metrc | Specifications!E15 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | df | Data!X2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | dichloromethane | Data!L2 | Dichloromethane | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | dichloromethane_metrc | Specifications!E16 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | dioxane14_metrc | Specifications!E5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethanol | Data!M2 | Ethanol | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethanol_metrc | Specifications!E17 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethoxyethanol_metrc | Specifications!E7 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethylacetate | Data!O2 | Ethyl Acetate | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethylacetate_metrc | Specifications!E19 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethylether | Data!N2 | Ethyl Ether | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | heptane | Data!P2 | Heptane | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | heptane_metrc | Specifications!E22 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | hexane_metrc | Specifications!E23 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | hexanes | Data!Q2 | Hexanes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | isopropanol2_metrc | Specifications!E8 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | methanol | Data!R2 | Methanol | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | methanol_metrc | Specifications!E25 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | pass_fail | Specifications!F2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | pentane_metrc | Specifications!E26 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | pentanes | Data!S2 | Pentanes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | propane | Data!T2 | Propane | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | propane_metrc | Specifications!E27 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | propranolipa2 | Data!E2 | 2 Propanol IPA | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | report_results | Report!A1:F31 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | residual_solvents_results | Data!E2:W2 | Residual Solvents Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | toluene | Data!U2 | Toluene | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | toluene_metrc | Specifications!E29 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | totalxylenes | Data!V2 | Total Xylenes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | totalxylenes_metrc | Specifications!E30 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | trichloroethene | Data!W2 | Trichloroethene | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | trichloroethene_metrc | Specifications!E31 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | abamectin_metrc | Specifications!E5 | Abamectin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | acephate_metrc | Specifications!E6 | Acephate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | acequinocyl_metrc | Specifications!E7 | Acequinocyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | acetamiprid_metrc | Specifications!E8 | Acetamiprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | azadirachtin_metrc | Specifications!E9 | Azadirachtin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | azoxystrobin_metrc | Specifications!E10 | Azoxystrobin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | bifenazate_metrc | Specifications!E11 | Bifenazate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | bifenthrin_metrc | Specifications!E12 | Bifenthrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | boscalid_metrc | Specifications!E13 | Boscalid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | carbaryl_metrc | Specifications!E14 | Carbaryl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | chlorantraniliprole_metrc | Specifications!E15 | Chlorantraniliprole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | chlorfenapyr_metrc | Specifications!E16 | Chlorfenapyr METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | chlormequatchloride_metrc | Specifications!E17 | Chlormequat Chloride METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | chlorpyrifos_metrc | Specifications!E18 | Chlorpyrifos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | clofentezine_metrc | Specifications!E19 | Clofentezine METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | cyfluthrin_metrc | Specifications!E20 | Cyfluthrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | cypermethrin_metrc | Specifications!E21 | Cypermethrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | daminozide_metrc | Specifications!E22 | Daminozide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | df | Data!BH2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | diazinon_metrc | Specifications!E23 | Diazinon METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | dimethoate_metrc | Specifications!E25 | Dimethoate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | etofenprox_metrc | Specifications!E26 | Etofenprox METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | etoxazole_metrc | Specifications!E27 | Etoxazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | fenoxycarb_metrc | Specifications!E28 | Fenoxycarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | fenpyroximate_metrc | Specifications!E29 | Fenpyroximate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | fipronil_metrc | Specifications!E30 | Fipronil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | flonicamid_metrc | Specifications!E31 | Flonicamid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | fludioxonil_metrc | Specifications!E32 | Fludioxonil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | hexythiazox_metrc | Specifications!E33 | Hexythiazox METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | imazalil_metrc | Specifications!E34 | Imazalil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | imidacloprid_metrc | Specifications!E35 | Imidacloprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | kresoximmethyl_metrc | Specifications!E36 | Kresoxim Methyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | malathion_metrc | Specifications!E37 | Malathion METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | metalaxyl_metrc | Specifications!E38 | Metalaxyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | methiocarb_metrc | Specifications!E39 | Methiocarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | methomyl_metrc | Specifications!E40 | Methomyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | myclobutanil_metrc | Specifications!E41 | Myclobutanil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | naled_metrc | Specifications!E42 | Naled METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | oxamyl_metrc | Specifications!E43 | Oxamyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | paclobutrazol_metrc | Specifications!E44 | Paclobutrazol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | pass_fail | Specifications!F2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | permethrins_metrc | Specifications!E45 | Permethrins METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | pesticides_results | Data!E2:BG2 | Pesticide Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | phosmet_metrc | Specifications!E46 | Phosmet METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | piperonyl_butoxide_metrc | Specifications!E47 | Piperonyl Butoxide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | prallethrin_metrc | Specifications!E48 | Prallethrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | propiconazole_metrc | Specifications!E49 | Propiconazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | propoxur_metrc | Specifications!E50 | Propoxur METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | pyrethrins_metrc | Specifications!E51 | Pyrethrins METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | pyridaben_metrc | Specifications!E52 | Pyridaben METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | report_results | Report!A1:R25 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | report_results_single | A1:F75 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | spinosad_metrc | Specifications!E55 | Spinosad METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | spiromesifen_metrc | Specifications!E56 | Spiromesifen METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | spirotetramat_metrc | Specifications!E57 | Spirotetramat METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | tebuconazole_metrc | Specifications!E58 | Tebuconazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | thiamethoxam_metrc | Specifications!E59 | Thiamethoxam METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | trifloxystrobin_metrc | Specifications!E60 | Trifloxystrobin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | abamectin_metrc | Specifications!E5 | Abamectin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | acephate_metrc | Specifications!E6 | Acephate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | acequinocyl_metrc | Specifications!E7 | Acequinocyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | acetamiprid_metrc | Specifications!E8 | Acetamiprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | aldicarb_metrc | Specifications!E9 | Aldicarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | azadirachtin_metrc | Specifications!E10 | Azadirachtin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | azoxystrobin_metrc | Specifications!E11 | Azoxystrobin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | bifenazate_metrc | Specifications!E12 | Bifenazate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | bifenthrin_metrc | Specifications!E13 | Bifenthrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | boscalid_metrc | Specifications!E14 | Boscalid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | carbaryl_metrc | Specifications!E15 | Carbaryl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | carbofuran_metrc | Specifications!E16 | Carbofuran METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlorantraniliprole_metrc | Specifications!E17 | Chlorantraniliprole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlorfenapyr_metrc | Specifications!E18 | Chlorfenapyr METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlormequat_metrc | Specifications!E19 | Chlormequat METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlormequatchloride_metrc | Specifications!E20 | Chlormequat Chloride METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlorpyrifos_metrc | Specifications!E21 | Chlorpyrifos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | clofentezine_metrc | Specifications!E22 | Clofentezine METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | coumaphos_metrc | Specifications!E23 | Coumaphos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | cyfluthrin_metrc | Specifications!E24 | Cyfluthrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | cypermethrin_metrc | Specifications!E25 | Cypermethrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | daminozide_metrc | Specifications!E27 | Daminozide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | ddvp_metrc | Specifications!E26 | DDVP METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | diazinon_metrc | Specifications!E28 | Diazinon METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | dimethoate_metrc | Specifications!E29 | Dimethoate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | dimethomorph_metrc | Specifications!E30 | Dimethomorph METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | ethoprophos_metrc | Specifications!E31 | Ethoprophos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | etofenprox_metrc | Specifications!E32 | Etofenprox METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | etoxazole_metrc | Specifications!E33 | Etoxazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fenhexamid_metrc | Specifications!E34 | Fenhexamid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fenoxycarb_metrc | Specifications!E35 | Fenoxycarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fenpyroximate_metrc | Specifications!E36 | Fenpyroximate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fipronil_metrc | Specifications!E37 | Fipronil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | flonicamid_metrc | Specifications!E38 | Flonicamid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fludioxonil_metrc | Specifications!E39 | Fludioxonil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | hexythiazox_metrc | Specifications!E40 | Hexythiazox METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | imazalil_metrc | Specifications!E41 | Imazalil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | imidacloprid_metrc | Specifications!E42 | Imidacloprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | kresoximmethyl_metrc | Specifications!E43 | Kresoxim Methyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | malathion_metrc | Specifications!E45 | Malathion METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | metalaxyl_metrc | Specifications!E46 | Metalaxyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | metalaxylmefenoxam_metrc | Specifications!E47 | Metalaxyl/Mefenoxam METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | methiocarb_metrc | Specifications!E48 | Methiocarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | methomyl_metrc | Specifications!E49 | Methomyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | methyl_parathion_metrc | Specifications!E50 | Methyl Parathion METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | mevinphos_metrc | Specifications!E51 | Mevinphos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | mgk264_metrc | Specifications!E44 | MGK-264 METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | myclobutanil_metrc | Specifications!E52 | Myclobutanil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | naled_metrc | Specifications!E53 | Naled METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | oxamyl_metrc | Specifications!E54 | Oxamyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | paclobutrazol_metrc | Specifications!E55 | Paclobutrazol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pass_fail | Specifications!F2 |  | Yes | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pentachlorobenzene_metrc | Specifications!E56 | Pentachlorobenzene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | permethrins_metrc | Specifications!E57 | Permethrins METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pesticides_results | Data!E2:BU2 | Pesticide Results | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | phosmet_metrc | Specifications!E58 | Phosmet METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | piperonyl_butoxide_metrc | Specifications!E59 | Piperonyl Butoxide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | prallethrin_metrc | Specifications!E60 | Prallethrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | propiconazole_metrc | Specifications!E61 | Propiconazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | propoxur_metrc | Specifications!E62 | Propoxur METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pyrethrins_metrc | Specifications!E63 | Pyrethrins METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pyridaben_metrc | Specifications!E64 | Pyridaben METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | report_results | Report!A1:L40 |  | Yes | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spinetoram_metrc | Specifications!E65 | Spinetoram METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spinosad_metrc | Specifications!E66 | Spinosad METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spiromesifen_metrc | Specifications!E67 | Spiromesifen METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spirotetramat_metrc | Specifications!E68 | Spirotetramat METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spiroxamine_metrc | Specifications!E69 | Spiroxamine METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | tebuconazole_metrc | Specifications!E70 | Tebuconazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | thiacloprid_metrc | Specifications!E71 | Thiacloprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | thiamethoxam_metrc | Specifications!E72 | Thiamethoxam METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | trifloxystrobin_metrc | Specifications!E73 | Trifloxystrobin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_0 | F3 | Water Activity 0 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_1 | F4 | Water Activity 1 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_10 | F15 | Water Activity 10 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_11 | F16 | Water Activity 11 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_12 | F17 | Water Activity 12 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_13 | F18 | Water Activity 13 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_14 | F19 | Water Activity 14 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_15 | F20 | Water Activity 15 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_16 | F21 | Water Activity 16 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_17 | F22 | Water Activity 17 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_18 | F23 | Water Activity 18 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_19 | F24 | Water Activity 19 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_2 | F5 | Water Activity 2 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_20 | F27 | Water Activity 20 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_21 | F28 | Water Activity 21 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_22 | F29 | Water Activity 22 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_23 | F30 | Water Activity 23 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_24 | F31 | Water Activity 24 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_25 | F32 | Water Activity 25 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_26 | F33 | Water Activity 26 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_27 | F34 | Water Activity 27 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_28 | F35 | Water Activity 28 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_29 | F36 | Water Activity 29 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_3 | F6 | Water Activity 3 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_30 | F39 | Water Activity 30 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_31 | F40 | Water Activity 31 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_32 | F41 | Water Activity 32 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_33 | F42 | Water Activity 33 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_34 | F43 | Water Activity 34 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_35 | F44 | Water Activity 35 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_36 | F45 | Water Activity 36 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_37 | F46 | Water Activity 37 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_38 | F47 | Water Activity 38 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_39 | F48 | Water Activity 39 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_4 | F7 | Water Activity 4 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_5 | F8 | Water Activity 5 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_6 | F9 | Water Activity 6 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_7 | F10 | Water Activity 7 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_8 | F11 | Water Activity 8 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_9 | F12 | Water Activity 9 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_1 | F13 | Water Activity SS 1 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_1_control | F14 | Water Activity SS 1 Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_2 | F25 | Water Activity SS 2 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_2_control | F26 | Water Activity SS 2 Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_3 | F37 | Water Activity SS 3 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_3_control | F38 | Water Activity SS 3 Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_4 | F49 | Water Activity SS 4 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_4_control | F50 | Water Activity SS 4 Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Test WS] | metrc_analyte_name_wateractivity | METRC!A5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | metrc_notes_wateractivity | METRC!D5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | metrc_pass_fail_wateractivity | METRC!C5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | metrc_quantity_wateractivity | METRC!B5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | metrc_to_include_wateractivity | METRC!E5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | pass_fail_report | Specifications!B7 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | wateractivity_metrc | Specifications!D5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | wateractivityaw | Data!D2 | Water Activity aw | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Batch WS] | test | F2 | stes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Batch WS] | test2 | F3 | steste | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Foreign_Material | Foreign Material [Test WS] | ffm_metrc | Report!C2 | Foreign Material METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Foreign_Material | Foreign Material [Test WS] | pass_fail | Data!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Foreign_Material | Foreign Material [Test WS] | report_results | Report!A1:C5 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | ahumulene_metrc | D22 | A Humulene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | ahumulene_metrc_mgg | E22 | A Humulene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | apinene_metrc | D5 | A Pinene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | apinene_metrc_mgg | E5 | A Pinene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | aterpinene_metrc | D10 | A Terpinene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | aterpinene_metrc_mgg | E10 | A Terpinene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bcaryophyllene_metrc | D21 | B Caryophyllene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bcaryophyllene_metrc_mgg | E21 | B Caryophyllene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bisabolol_metrc | D27 | Bisabolol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bisabolol_metrc_mgg | E27 | Bisabolol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bmyrcene_metrc | D7 | B Myrcene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bmyrcene_metrc_mgg | E7 | B Myrcene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bpinene_metrc | D8 | B Pinene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bpinene_metrc_mgg | E8 | B Pinene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | camphene_metrc | D6 | Camphene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | camphene_metrc_mgg | E6 | Camphene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | caryophylleneoxide_metrc | D26 | Caryophyllene Oxide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | caryophylleneoxide_metrc_mgg | E26 | Caryophyllene Oxide METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | cisnerolidol_metrc | D23 | Cis Nerolidol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | cisnerolidol_metrc_mgg | E23 | Cis Nerolidol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | cisocimene_metrc | D11 | Cis Ocimene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | cisocimene_metrc_mgg | E11 | Cis Ocimene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | delta3carene_metrc | D9 | Delta 3 Carene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | delta3carene_metrc_mgg | E9 | Delta 3 Carene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | dlimonene_metrc | D12 | D Limonene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | dlimonene_metrc_mgg | E12 | D Limonene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | eucalyptol_metrc | D15 | Eucalyptol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | eucalyptol_metrc_mgg | E15 | Eucalyptol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | geraniol_metrc | D20 | Geraniol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | geraniol_metrc_mgg | E20 | Geraniol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | gterpinene_metrc | D16 | G Terpinene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | gterpinene_metrc_mgg | E16 | G Terpinene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | guaiol_metrc | D25 | Guaiol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | guaiol_metrc_mgg | E25 | Guaiol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | isopulegol_metrc | D19 | Isopulegol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | isopulegol_metrc_mgg | E19 | Isopulegol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | linalool_metrc | D18 | Linalool METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | linalool_metrc_mgg | E18 | Linalool METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | pcymene_metrc | D13 | P Cymene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | pcymene_metrc_mgg | E13 | P Cymene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | terpinolene_metrc | D17 | Terpinolene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | terpinolene_metrc_mgg | E17 | Terpinolene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | testterpenes | E4 | Test Terpenes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | transnerolidol_metrc | D24 | Trans Nerolidol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | transnerolidol_metrc_mgg | E24 | Trans Nerolidol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | transocimene_metrc | D14 | Trans Ocimene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | transocimene_metrc_mgg | E14 | Trans Ocimene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | aspergillusspp | I2 | Aspergillus spp. | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | aspergillusspp_metrc | Specifications!E10 | Aspergillus Spp METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | enterobacteriaceae | F2 | Enterobacteriaceae | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | enterobacteriaceae_metrc | Specifications!E7 | Enterobacteriaceae METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | lmonocytogenes | J2 | L. monocytogenes | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | lmonocytogenes_metrc | Specifications!E11 | L Monocytogenes METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | microbials_results | Data!D2:J2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | report_result | Report!A1:F9 |  | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | salmonellaspecies | G2 | Salmonella species | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | salmonellaspecies_metrc | Specifications!E8 | Salmonella Species METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | shigatoxin_producingecoli_metrc | Specifications!E9 | Shiga Toxin-Producing E Coli METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | shigatoxinproducingecoli | H2 | Shiga toxin-producing E. coli | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | totalaerobic | D2 | Total aerobic microbial | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | totalaerobicmicrobial_metrc | Specifications!E5 | Total Aerobic Microbial METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | totalyeastandmold_metrc | Specifications!E6 | Total Yeast And Mold METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | yeastmold | E2 | Total yeast and mold | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Homogeneity | Homogeneity [Test WS] | average_actual_unit_mass_g | Data!B8 | Average Actual Unit Mass g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | duplicate_cp_test_id_check | Data!B36 | Duplicate CP Test ID Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | extra_pasted_rows_check | Data!B37 | Extra Pasted Rows Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_cannabinoid_1_label_variance | Data!B28 | Cannabinoid 1 Label Variance for Highest Cannabinoid | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_cannabinoid_2_label_variance | Data!B30 | Cannabinoid 2 Label Variance for Highest Cannabinoid | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_mass_label_variance | Data!B26 | Mass Label Variance for Highest Unit Mass | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_reported_cannabinoid_1_mg_container | Data!B27 | Highest Reported Cannabinoid 1 mg/container | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_reported_cannabinoid_2_mg_container | Data!B29 | Highest Reported Cannabinoid 2 mg/container | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_reported_unit_mass_g | Data!B25 | Highest Reported Unit Mass g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | homogeneity_metrc | COA!F1 | Homogeneity METRC | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_cannabinoid_1_mg_container | Data!B4 | Label Cannabinoid 1 mg/container | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_cannabinoid_1_source_status | Paste!Q4 | Label Cannabinoid 1 Source Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_cannabinoid_2_mg_container | Data!B6 | Label Cannabinoid 2 mg/container | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_cannabinoid_2_source_status | Paste!U4 | Label Cannabinoid 2 Source Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_unit_mass_g | Data!B7 | Label Unit Mass g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | manual_label_cannabinoid_1_mg_container | Paste!O4 | Manual Label Cannabinoid 1 mg/container Override | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | manual_label_cannabinoid_2_mg_container | Paste!S4 | Manual Label Cannabinoid 2 mg/container Override | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | optional_target_2_label_claim_check | Data!B41 | Optional Target 2 Label Claim Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | parent_sample_match_check | Data!B38 | Parent Sample Match Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | pass_fail | Data!B31 | Pass/Fail | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | qbench_sample_label_amount_lookup | Paste!N24:P36 | QBench Sample Label Amount Lookup | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | replicate_count | Data!B34 | Replicate Rows Present | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | replicate_results | COA!A10:G20 | Homogeneity Replicate Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | report_results | COA!A1:G20 | Homogeneity COA Output | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | required_target_fields_check | Data!B40 | Required Target 1 and Label Claim Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | required_unit_mass_check | Data!B39 | Required Unit Mass Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | reviewer_parent_sample_confirmation | Paste!D6 | Reviewer Parent Sample Confirmation | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | target_cannabinoid_1 | Data!B3 | Target Cannabinoid 1 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | target_cannabinoid_2 | Data!B5 | Target Cannabinoid 2 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | unique_cp_test_id_count | Data!B35 | Unique CP Test IDs Counted | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | validation_status | Data!B42 | Overall Input Validation Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_limit | Specifications!C5 | Aspergillus Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_loq | Specifications!B5 | Aspergillus LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_mu | Specifications!E5 | Aspergillus MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_result | Specifications!D9 | Aspergillus Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_status | Specifications!F9 | Aspergillus Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | aspergillusspp_metrc | Report!C6 | Aspergillus Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | flavus_result | Data!E3 | A. Flavus Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | fumigatus_result | Data!E4 | A. fumigatus Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_analyte_name_aspergillusspp | METRC!A5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_notes_aspergillusspp | METRC!D5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_pass_fail_aspergillusspp | METRC!C5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_quantity_aspergillusspp | METRC!B5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_to_include_aspergillusspp | METRC!E5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | niger_result | Data!E2 | A. niger (HEX) Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | report_content | Report!A2:D5 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | report_header | Report!A1:D1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | report_results | Report!A1:D5 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | sub_species | Data!F2 | Asp Sub Species | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | terreus_result | Data!E5 | A. terreus Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_limit | Specifications!C5 | Salmonella Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_loq | Specifications!B5 | Salmonella LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_mu | Specifications!E5 | Salmonella MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_result | Specifications!D5 | Salmonella Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_status | Specifications!F5 | Salmonella Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salmonella_results | Data!E2 | Salmonella Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_limit | Specifications!C5 | STEC Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_loq | Specifications!B5 | STEC LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_mu | Specifications!E5 | STEC MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_result | Specifications!D5 | STEC Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_results | Data!E2 | STEC Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_status | Specifications!F5 | STEC Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Listeria | Listeria Monocytogenes [Test] Worksheet | lis_results | Data!E2 | Listeria Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Listeria | Listeria Monocytogenes [Test] Worksheet | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Listeria | Listeria Monocytogenes [Test] Worksheet | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Listeria | Listeria Monocytogenes [Test] Worksheet | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_limit | Specifications!C5 | Total Aerobic Count Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_loq | Specifications!B5 | Total Aerobic Count LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_mu | Specifications!E5 | Total Aerobic Count MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_result | Specifications!D5 | Total Aerobic Count Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_results | Data!E2 | Total Aerobic Count Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_status | Specifications!F5 | Total Aerobic Count Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_limit | Specifications!C5 | Total Yeast and Mold Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_loq | Specifications!B5 | Total Yeast and Mold LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_mu | Specifications!E5 | Total Yeast and Mold MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_result | Specifications!D5 | Total Yeast and Mold Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_results | Data!E2 | YM Automation Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_status | Specifications!F5 | Total Yeast and Mold Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_limit | Specifications!C5 | Enterobacteriaceae Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_loq | Specifications!B5 | Enterobacteriaceae LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_mu | Specifications!E5 | Enterobacteriaceae MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_result | Specifications!D5 | Enterobacteriaceae Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_results | Data!E2 | Enterobacteriaceae Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_status | Specifications!F5 | Enterobacteriaceae Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |

## Deprecated duplicate 1 of 3 — Rescan 2026-07-04 (preserved, do not use)

| Assay | Worksheet | Named Cell | Cell/Range | Purpose | Used by COA? | Notes |
|---|---|---|---|---|---|---|
| Other | Example Batch Worksheet | control | D2 | Control  | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Other | [Batch] Example Worksheet | control | D2 | Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Other | Training Worksheet | example_named_cell | General!A18 | Example | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic | Data!E2 | Arsenic | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_limit | Specifications!C5 | Arsenic Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_loq | Specifications!B5 | Arsenic LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_mu | Specifications!E5 | Arsenic MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_result | Specifications!D5 | Arsenic Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_status | Specifications!F5 | Arsenic Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium | Data!F2 | Cadmium  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_limit | Specifications!C6 | Cadmium Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_loq | Specifications!B6 | Cadmium LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_mu | Specifications!E6 | Cadmium MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_result | Specifications!D6 | Cadmium Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_status | Specifications!F6 | Cadmium Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | df | Data!I2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead | Data!G2 | Lead | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead_limit | Specifications!C7 | Lead Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead_loq | Specifications!B7 | Lead LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead_mu | Specifications!E7 | Lead MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead_result | Specifications!D7 | Lead Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury | Data!H2 | Mercury | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_limit | Specifications!C8 | Mercury Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_loq | Specifications!B8 | Mercury LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_mu | Specifications!E8 | Mercury MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_result | Specifications!D8 | Mercury Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_status | Specifications!F8 | Mercury Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | report_results | Report!A1:F6 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | df | Data!G2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | purity_results | 'Purity Data'!C2:R2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | report_results | Report!A1:F21 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_1 | Data!E5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_10 | Data!N5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_11 | Data!O5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_12 | Data!P5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_13 | Data!Q5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_14 | 'Purity Data'!C2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_15 | 'Purity Data'!D2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_16 | 'Purity Data'!E2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_17 | 'Purity Data'!F2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_18 | 'Purity Data'!G2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_19 | 'Purity Data'!H2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_2 | Data!F5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_20 | 'Purity Data'!I2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_21 | 'Purity Data'!J2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_22 | 'Purity Data'!K2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_23 | 'Purity Data'!L2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_24 | 'Purity Data'!M2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_25 | 'Purity Data'!N2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_26 | 'Purity Data'!O2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_27 | 'Purity Data'!P2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_28 | 'Purity Data'!Q2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_29 | 'Purity Data'!R2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_3 | Data!G5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_4 | Data!H5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_5 | Data!I5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_6 | Data!J5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_7 | Data!K5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_8 | Data!L5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_9 | Data!M5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | results | Data!E5:Q5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | total_thc | Report!B1 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | total_thc_report_result | Data!C11 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxinb1 | Data!E2 | Aflatoxin B1 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxinb1_metrc | Specifications!D5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxinb2 | Data!F2 | Aflatoxin B2 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxinb2_metrc | Specifications!D6 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxing1 | Data!G2 | Aflatoxin G1 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxing1_metrc | Specifications!D7 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxing2 | Data!H2 | Aflatoxin G2 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxing2_metrc | Specifications!D8 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | df | Data!J2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | mycotoxin_results | Data!E2:I2 | Mycotoxin Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | ochratoxina | Data!I2 | Ochratoxin A | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | ochratoxina_metrc | Specifications!D9 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | pass_fail | Specifications!F2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | report_results | Report!A1:F8 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | totalmycod_b1b2g1g2_metrc | Specifications!D11 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | totalmycod_b1b2g1g2oa_metrc | Specifications!D10 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | acetone | Data!F2 | Acetone | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | acetone_metrc | Specifications!E9 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | acetonitrile | Data!G2 | Acetonitrile | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | benzene | Data!H2 | Benzene | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | benzene_metrc | Specifications!E11 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | butane_metrc | Specifications!E12 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | butanes | Data!I2 | Butanes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | butanol_metrc | Specifications!E6 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | chloroform | Data!J2 | Chloroform | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | chloroform_metrc | Specifications!E13 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | cyclohexane | Data!K2 | Cyclohexane | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | cyclohexane_metrc | Specifications!E15 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | df | Data!X2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | dichloromethane | Data!L2 | Dichloromethane | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | dichloromethane_metrc | Specifications!E16 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | dioxane14_metrc | Specifications!E5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethanol | Data!M2 | Ethanol | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethanol_metrc | Specifications!E17 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethoxyethanol_metrc | Specifications!E7 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethylacetate | Data!O2 | Ethyl Acetate | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethylacetate_metrc | Specifications!E19 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethylether | Data!N2 | Ethyl Ether | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | heptane | Data!P2 | Heptane | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | heptane_metrc | Specifications!E22 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | hexane_metrc | Specifications!E23 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | hexanes | Data!Q2 | Hexanes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | isopropanol2_metrc | Specifications!E8 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | methanol | Data!R2 | Methanol | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | methanol_metrc | Specifications!E25 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | pass_fail | Specifications!F2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | pentane_metrc | Specifications!E26 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | pentanes | Data!S2 | Pentanes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | propane | Data!T2 | Propane | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | propane_metrc | Specifications!E27 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | propranolipa2 | Data!E2 | 2 Propanol IPA | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | report_results | Report!A1:F31 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | residual_solvents_results | Data!E2:W2 | Residual Solvents Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | toluene | Data!U2 | Toluene | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | toluene_metrc | Specifications!E29 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | totalxylenes | Data!V2 | Total Xylenes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | totalxylenes_metrc | Specifications!E30 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | trichloroethene | Data!W2 | Trichloroethene | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | trichloroethene_metrc | Specifications!E31 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | abamectin_metrc | Specifications!E5 | Abamectin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | acephate_metrc | Specifications!E6 | Acephate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | acequinocyl_metrc | Specifications!E7 | Acequinocyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | acetamiprid_metrc | Specifications!E8 | Acetamiprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | azadirachtin_metrc | Specifications!E9 | Azadirachtin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | azoxystrobin_metrc | Specifications!E10 | Azoxystrobin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | bifenazate_metrc | Specifications!E11 | Bifenazate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | bifenthrin_metrc | Specifications!E12 | Bifenthrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | boscalid_metrc | Specifications!E13 | Boscalid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | carbaryl_metrc | Specifications!E14 | Carbaryl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | chlorantraniliprole_metrc | Specifications!E15 | Chlorantraniliprole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | chlorfenapyr_metrc | Specifications!E16 | Chlorfenapyr METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | chlormequatchloride_metrc | Specifications!E17 | Chlormequat Chloride METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | chlorpyrifos_metrc | Specifications!E18 | Chlorpyrifos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | clofentezine_metrc | Specifications!E19 | Clofentezine METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | cyfluthrin_metrc | Specifications!E20 | Cyfluthrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | cypermethrin_metrc | Specifications!E21 | Cypermethrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | daminozide_metrc | Specifications!E22 | Daminozide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | df | Data!BH2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | diazinon_metrc | Specifications!E23 | Diazinon METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | dimethoate_metrc | Specifications!E25 | Dimethoate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | etofenprox_metrc | Specifications!E26 | Etofenprox METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | etoxazole_metrc | Specifications!E27 | Etoxazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | fenoxycarb_metrc | Specifications!E28 | Fenoxycarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | fenpyroximate_metrc | Specifications!E29 | Fenpyroximate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | fipronil_metrc | Specifications!E30 | Fipronil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | flonicamid_metrc | Specifications!E31 | Flonicamid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | fludioxonil_metrc | Specifications!E32 | Fludioxonil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | hexythiazox_metrc | Specifications!E33 | Hexythiazox METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | imazalil_metrc | Specifications!E34 | Imazalil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | imidacloprid_metrc | Specifications!E35 | Imidacloprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | kresoximmethyl_metrc | Specifications!E36 | Kresoxim Methyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | malathion_metrc | Specifications!E37 | Malathion METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | metalaxyl_metrc | Specifications!E38 | Metalaxyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | methiocarb_metrc | Specifications!E39 | Methiocarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | methomyl_metrc | Specifications!E40 | Methomyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | myclobutanil_metrc | Specifications!E41 | Myclobutanil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | naled_metrc | Specifications!E42 | Naled METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | oxamyl_metrc | Specifications!E43 | Oxamyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | paclobutrazol_metrc | Specifications!E44 | Paclobutrazol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | pass_fail | Specifications!F2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | permethrins_metrc | Specifications!E45 | Permethrins METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | pesticides_results | Data!E2:BG2 | Pesticide Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | phosmet_metrc | Specifications!E46 | Phosmet METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | piperonyl_butoxide_metrc | Specifications!E47 | Piperonyl Butoxide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | prallethrin_metrc | Specifications!E48 | Prallethrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | propiconazole_metrc | Specifications!E49 | Propiconazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | propoxur_metrc | Specifications!E50 | Propoxur METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | pyrethrins_metrc | Specifications!E51 | Pyrethrins METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | pyridaben_metrc | Specifications!E52 | Pyridaben METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | report_results | Report!A1:R25 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | report_results_single | A1:F75 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | spinosad_metrc | Specifications!E55 | Spinosad METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | spiromesifen_metrc | Specifications!E56 | Spiromesifen METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | spirotetramat_metrc | Specifications!E57 | Spirotetramat METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | tebuconazole_metrc | Specifications!E58 | Tebuconazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | thiamethoxam_metrc | Specifications!E59 | Thiamethoxam METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | trifloxystrobin_metrc | Specifications!E60 | Trifloxystrobin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | abamectin_metrc | Specifications!E5 | Abamectin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | acephate_metrc | Specifications!E6 | Acephate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | acequinocyl_metrc | Specifications!E7 | Acequinocyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | acetamiprid_metrc | Specifications!E8 | Acetamiprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | aldicarb_metrc | Specifications!E9 | Aldicarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | azadirachtin_metrc | Specifications!E10 | Azadirachtin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | azoxystrobin_metrc | Specifications!E11 | Azoxystrobin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | bifenazate_metrc | Specifications!E12 | Bifenazate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | bifenthrin_metrc | Specifications!E13 | Bifenthrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | boscalid_metrc | Specifications!E14 | Boscalid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | carbaryl_metrc | Specifications!E15 | Carbaryl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | carbofuran_metrc | Specifications!E16 | Carbofuran METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlorantraniliprole_metrc | Specifications!E17 | Chlorantraniliprole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlorfenapyr_metrc | Specifications!E18 | Chlorfenapyr METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlormequat_metrc | Specifications!E19 | Chlormequat METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlormequatchloride_metrc | Specifications!E20 | Chlormequat Chloride METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlorpyrifos_metrc | Specifications!E21 | Chlorpyrifos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | clofentezine_metrc | Specifications!E22 | Clofentezine METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | coumaphos_metrc | Specifications!E23 | Coumaphos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | cyfluthrin_metrc | Specifications!E24 | Cyfluthrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | cypermethrin_metrc | Specifications!E25 | Cypermethrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | daminozide_metrc | Specifications!E27 | Daminozide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | ddvp_metrc | Specifications!E26 | DDVP METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | diazinon_metrc | Specifications!E28 | Diazinon METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | dimethoate_metrc | Specifications!E29 | Dimethoate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | dimethomorph_metrc | Specifications!E30 | Dimethomorph METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | ethoprophos_metrc | Specifications!E31 | Ethoprophos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | etofenprox_metrc | Specifications!E32 | Etofenprox METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | etoxazole_metrc | Specifications!E33 | Etoxazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fenhexamid_metrc | Specifications!E34 | Fenhexamid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fenoxycarb_metrc | Specifications!E35 | Fenoxycarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fenpyroximate_metrc | Specifications!E36 | Fenpyroximate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fipronil_metrc | Specifications!E37 | Fipronil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | flonicamid_metrc | Specifications!E38 | Flonicamid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fludioxonil_metrc | Specifications!E39 | Fludioxonil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | hexythiazox_metrc | Specifications!E40 | Hexythiazox METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | imazalil_metrc | Specifications!E41 | Imazalil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | imidacloprid_metrc | Specifications!E42 | Imidacloprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | kresoximmethyl_metrc | Specifications!E43 | Kresoxim Methyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | malathion_metrc | Specifications!E45 | Malathion METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | metalaxyl_metrc | Specifications!E46 | Metalaxyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | metalaxylmefenoxam_metrc | Specifications!E47 | Metalaxyl/Mefenoxam METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | methiocarb_metrc | Specifications!E48 | Methiocarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | methomyl_metrc | Specifications!E49 | Methomyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | methyl_parathion_metrc | Specifications!E50 | Methyl Parathion METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | mevinphos_metrc | Specifications!E51 | Mevinphos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | mgk264_metrc | Specifications!E44 | MGK-264 METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | myclobutanil_metrc | Specifications!E52 | Myclobutanil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | naled_metrc | Specifications!E53 | Naled METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | oxamyl_metrc | Specifications!E54 | Oxamyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | paclobutrazol_metrc | Specifications!E55 | Paclobutrazol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pass_fail | Specifications!F2 |  | Yes | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pentachlorobenzene_metrc | Specifications!E56 | Pentachlorobenzene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | permethrins_metrc | Specifications!E57 | Permethrins METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pesticides_results | Data!E2:BU2 | Pesticide Results | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | phosmet_metrc | Specifications!E58 | Phosmet METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | piperonyl_butoxide_metrc | Specifications!E59 | Piperonyl Butoxide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | prallethrin_metrc | Specifications!E60 | Prallethrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | propiconazole_metrc | Specifications!E61 | Propiconazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | propoxur_metrc | Specifications!E62 | Propoxur METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pyrethrins_metrc | Specifications!E63 | Pyrethrins METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pyridaben_metrc | Specifications!E64 | Pyridaben METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | report_results | Report!A1:L40 |  | Yes | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spinetoram_metrc | Specifications!E65 | Spinetoram METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spinosad_metrc | Specifications!E66 | Spinosad METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spiromesifen_metrc | Specifications!E67 | Spiromesifen METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spirotetramat_metrc | Specifications!E68 | Spirotetramat METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spiroxamine_metrc | Specifications!E69 | Spiroxamine METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | tebuconazole_metrc | Specifications!E70 | Tebuconazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | thiacloprid_metrc | Specifications!E71 | Thiacloprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | thiamethoxam_metrc | Specifications!E72 | Thiamethoxam METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | trifloxystrobin_metrc | Specifications!E73 | Trifloxystrobin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_0 | F3 | Water Activity 0 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_1 | F4 | Water Activity 1 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_10 | F15 | Water Activity 10 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_11 | F16 | Water Activity 11 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_12 | F17 | Water Activity 12 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_13 | F18 | Water Activity 13 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_14 | F19 | Water Activity 14 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_15 | F20 | Water Activity 15 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_16 | F21 | Water Activity 16 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_17 | F22 | Water Activity 17 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_18 | F23 | Water Activity 18 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_19 | F24 | Water Activity 19 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_2 | F5 | Water Activity 2 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_20 | F27 | Water Activity 20 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_21 | F28 | Water Activity 21 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_22 | F29 | Water Activity 22 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_23 | F30 | Water Activity 23 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_24 | F31 | Water Activity 24 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_25 | F32 | Water Activity 25 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_26 | F33 | Water Activity 26 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_27 | F34 | Water Activity 27 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_28 | F35 | Water Activity 28 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_29 | F36 | Water Activity 29 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_3 | F6 | Water Activity 3 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_30 | F39 | Water Activity 30 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_31 | F40 | Water Activity 31 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_32 | F41 | Water Activity 32 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_33 | F42 | Water Activity 33 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_34 | F43 | Water Activity 34 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_35 | F44 | Water Activity 35 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_36 | F45 | Water Activity 36 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_37 | F46 | Water Activity 37 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_38 | F47 | Water Activity 38 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_39 | F48 | Water Activity 39 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_4 | F7 | Water Activity 4 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_5 | F8 | Water Activity 5 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_6 | F9 | Water Activity 6 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_7 | F10 | Water Activity 7 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_8 | F11 | Water Activity 8 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_9 | F12 | Water Activity 9 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_1 | F13 | Water Activity SS 1 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_1_control | F14 | Water Activity SS 1 Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_2 | F25 | Water Activity SS 2 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_2_control | F26 | Water Activity SS 2 Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_3 | F37 | Water Activity SS 3 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_3_control | F38 | Water Activity SS 3 Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_4 | F49 | Water Activity SS 4 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_4_control | F50 | Water Activity SS 4 Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Test WS] | metrc_analyte_name_wateractivity | METRC!A5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | metrc_notes_wateractivity | METRC!D5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | metrc_pass_fail_wateractivity | METRC!C5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | metrc_quantity_wateractivity | METRC!B5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | metrc_to_include_wateractivity | METRC!E5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | pass_fail_report | Specifications!B7 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | wateractivity_metrc | Specifications!D5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | wateractivityaw | Data!D2 | Water Activity aw | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Batch WS] | test | F2 | stes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Batch WS] | test2 | F3 | steste | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Foreign_Material | Foreign Material [Test WS] | ffm_metrc | Report!C2 | Foreign Material METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Foreign_Material | Foreign Material [Test WS] | pass_fail | Data!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Foreign_Material | Foreign Material [Test WS] | report_results | Report!A1:C5 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | ahumulene_metrc | D22 | A Humulene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | ahumulene_metrc_mgg | E22 | A Humulene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | apinene_metrc | D5 | A Pinene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | apinene_metrc_mgg | E5 | A Pinene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | aterpinene_metrc | D10 | A Terpinene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | aterpinene_metrc_mgg | E10 | A Terpinene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bcaryophyllene_metrc | D21 | B Caryophyllene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bcaryophyllene_metrc_mgg | E21 | B Caryophyllene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bisabolol_metrc | D27 | Bisabolol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bisabolol_metrc_mgg | E27 | Bisabolol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bmyrcene_metrc | D7 | B Myrcene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bmyrcene_metrc_mgg | E7 | B Myrcene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bpinene_metrc | D8 | B Pinene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bpinene_metrc_mgg | E8 | B Pinene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | camphene_metrc | D6 | Camphene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | camphene_metrc_mgg | E6 | Camphene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | caryophylleneoxide_metrc | D26 | Caryophyllene Oxide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | caryophylleneoxide_metrc_mgg | E26 | Caryophyllene Oxide METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | cisnerolidol_metrc | D23 | Cis Nerolidol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | cisnerolidol_metrc_mgg | E23 | Cis Nerolidol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | cisocimene_metrc | D11 | Cis Ocimene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | cisocimene_metrc_mgg | E11 | Cis Ocimene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | delta3carene_metrc | D9 | Delta 3 Carene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | delta3carene_metrc_mgg | E9 | Delta 3 Carene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | dlimonene_metrc | D12 | D Limonene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | dlimonene_metrc_mgg | E12 | D Limonene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | eucalyptol_metrc | D15 | Eucalyptol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | eucalyptol_metrc_mgg | E15 | Eucalyptol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | geraniol_metrc | D20 | Geraniol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | geraniol_metrc_mgg | E20 | Geraniol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | gterpinene_metrc | D16 | G Terpinene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | gterpinene_metrc_mgg | E16 | G Terpinene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | guaiol_metrc | D25 | Guaiol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | guaiol_metrc_mgg | E25 | Guaiol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | isopulegol_metrc | D19 | Isopulegol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | isopulegol_metrc_mgg | E19 | Isopulegol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | linalool_metrc | D18 | Linalool METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | linalool_metrc_mgg | E18 | Linalool METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | pcymene_metrc | D13 | P Cymene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | pcymene_metrc_mgg | E13 | P Cymene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | terpinolene_metrc | D17 | Terpinolene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | terpinolene_metrc_mgg | E17 | Terpinolene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | testterpenes | E4 | Test Terpenes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | transnerolidol_metrc | D24 | Trans Nerolidol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | transnerolidol_metrc_mgg | E24 | Trans Nerolidol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | transocimene_metrc | D14 | Trans Ocimene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | transocimene_metrc_mgg | E14 | Trans Ocimene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | aspergillusspp | I2 | Aspergillus spp. | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | aspergillusspp_metrc | Specifications!E10 | Aspergillus Spp METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | enterobacteriaceae | F2 | Enterobacteriaceae | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | enterobacteriaceae_metrc | Specifications!E7 | Enterobacteriaceae METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | lmonocytogenes | J2 | L. monocytogenes | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | lmonocytogenes_metrc | Specifications!E11 | L Monocytogenes METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | microbials_results | Data!D2:J2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | report_result | Report!A1:F9 |  | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | salmonellaspecies | G2 | Salmonella species | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | salmonellaspecies_metrc | Specifications!E8 | Salmonella Species METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | shigatoxin_producingecoli_metrc | Specifications!E9 | Shiga Toxin-Producing E Coli METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | shigatoxinproducingecoli | H2 | Shiga toxin-producing E. coli | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | totalaerobic | D2 | Total aerobic microbial | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | totalaerobicmicrobial_metrc | Specifications!E5 | Total Aerobic Microbial METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | totalyeastandmold_metrc | Specifications!E6 | Total Yeast And Mold METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | yeastmold | E2 | Total yeast and mold | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Homogeneity | Homogeneity [Test WS] | average_actual_unit_mass_g | Data!B8 | Average Actual Unit Mass g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | duplicate_cp_test_id_check | Data!B36 | Duplicate CP Test ID Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | extra_pasted_rows_check | Data!B37 | Extra Pasted Rows Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_cannabinoid_1_label_variance | Data!B28 | Cannabinoid 1 Label Variance for Highest Cannabinoid | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_cannabinoid_2_label_variance | Data!B30 | Cannabinoid 2 Label Variance for Highest Cannabinoid | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_mass_label_variance | Data!B26 | Mass Label Variance for Highest Unit Mass | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_reported_cannabinoid_1_mg_container | Data!B27 | Highest Reported Cannabinoid 1 mg/container | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_reported_cannabinoid_2_mg_container | Data!B29 | Highest Reported Cannabinoid 2 mg/container | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_reported_unit_mass_g | Data!B25 | Highest Reported Unit Mass g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | homogeneity_metrc | COA!F1 | Homogeneity METRC | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_cannabinoid_1_mg_container | Data!B4 | Label Cannabinoid 1 mg/container | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_cannabinoid_1_source_status | Paste!Q4 | Label Cannabinoid 1 Source Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_cannabinoid_2_mg_container | Data!B6 | Label Cannabinoid 2 mg/container | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_cannabinoid_2_source_status | Paste!U4 | Label Cannabinoid 2 Source Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_unit_mass_g | Data!B7 | Label Unit Mass g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | manual_label_cannabinoid_1_mg_container | Paste!O4 | Manual Label Cannabinoid 1 mg/container Override | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | manual_label_cannabinoid_2_mg_container | Paste!S4 | Manual Label Cannabinoid 2 mg/container Override | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | optional_target_2_label_claim_check | Data!B41 | Optional Target 2 Label Claim Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | parent_sample_match_check | Data!B38 | Parent Sample Match Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | pass_fail | Data!B31 | Pass/Fail | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | qbench_sample_label_amount_lookup | Paste!N24:P36 | QBench Sample Label Amount Lookup | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | replicate_count | Data!B34 | Replicate Rows Present | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | replicate_results | COA!A10:G20 | Homogeneity Replicate Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | report_results | COA!A1:G20 | Homogeneity COA Output | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | required_target_fields_check | Data!B40 | Required Target 1 and Label Claim Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | required_unit_mass_check | Data!B39 | Required Unit Mass Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | reviewer_parent_sample_confirmation | Paste!D6 | Reviewer Parent Sample Confirmation | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | target_cannabinoid_1 | Data!B3 | Target Cannabinoid 1 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | target_cannabinoid_2 | Data!B5 | Target Cannabinoid 2 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | unique_cp_test_id_count | Data!B35 | Unique CP Test IDs Counted | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | validation_status | Data!B42 | Overall Input Validation Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_limit | Specifications!C5 | Aspergillus Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_loq | Specifications!B5 | Aspergillus LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_mu | Specifications!E5 | Aspergillus MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_result | Specifications!D9 | Aspergillus Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_status | Specifications!F9 | Aspergillus Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | aspergillusspp_metrc | Report!C6 | Aspergillus Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | flavus_result | Data!E3 | A. Flavus Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | fumigatus_result | Data!E4 | A. fumigatus Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_analyte_name_aspergillusspp | METRC!A5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_notes_aspergillusspp | METRC!D5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_pass_fail_aspergillusspp | METRC!C5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_quantity_aspergillusspp | METRC!B5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_to_include_aspergillusspp | METRC!E5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | niger_result | Data!E2 | A. niger (HEX) Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | report_content | Report!A2:D5 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | report_header | Report!A1:D1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | report_results | Report!A1:D5 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | sub_species | Data!F2 | Asp Sub Species | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | terreus_result | Data!E5 | A. terreus Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_limit | Specifications!C5 | Salmonella Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_loq | Specifications!B5 | Salmonella LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_mu | Specifications!E5 | Salmonella MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_result | Specifications!D5 | Salmonella Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_status | Specifications!F5 | Salmonella Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salmonella_results | Data!E2 | Salmonella Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_limit | Specifications!C5 | STEC Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_loq | Specifications!B5 | STEC LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_mu | Specifications!E5 | STEC MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_result | Specifications!D5 | STEC Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_results | Data!E2 | STEC Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_status | Specifications!F5 | STEC Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Listeria | Listeria Monocytogenes [Test] Worksheet | lis_results | Data!E2 | Listeria Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Listeria | Listeria Monocytogenes [Test] Worksheet | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Listeria | Listeria Monocytogenes [Test] Worksheet | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Listeria | Listeria Monocytogenes [Test] Worksheet | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_limit | Specifications!C5 | Total Aerobic Count Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_loq | Specifications!B5 | Total Aerobic Count LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_mu | Specifications!E5 | Total Aerobic Count MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_result | Specifications!D5 | Total Aerobic Count Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_results | Data!E2 | Total Aerobic Count Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_status | Specifications!F5 | Total Aerobic Count Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_limit | Specifications!C5 | Total Yeast and Mold Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_loq | Specifications!B5 | Total Yeast and Mold LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_mu | Specifications!E5 | Total Yeast and Mold MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_result | Specifications!D5 | Total Yeast and Mold Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_results | Data!E2 | YM Automation Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_status | Specifications!F5 | Total Yeast and Mold Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_limit | Specifications!C5 | Enterobacteriaceae Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_loq | Specifications!B5 | Enterobacteriaceae LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_mu | Specifications!E5 | Enterobacteriaceae MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_result | Specifications!D5 | Enterobacteriaceae Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_results | Data!E2 | Enterobacteriaceae Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_status | Specifications!F5 | Enterobacteriaceae Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |

## Deprecated duplicate 2 of 3 — Rescan 2026-07-04 (preserved, do not use)

| Assay | Worksheet | Named Cell | Cell/Range | Purpose | Used by COA? | Notes |
|---|---|---|---|---|---|---|
| Other | Example Batch Worksheet | control | D2 | Control  | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Other | [Batch] Example Worksheet | control | D2 | Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Other | Training Worksheet | example_named_cell | General!A18 | Example | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic | Data!E2 | Arsenic | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_limit | Specifications!C5 | Arsenic Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_loq | Specifications!B5 | Arsenic LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_mu | Specifications!E5 | Arsenic MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_result | Specifications!D5 | Arsenic Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_status | Specifications!F5 | Arsenic Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium | Data!F2 | Cadmium  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_limit | Specifications!C6 | Cadmium Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_loq | Specifications!B6 | Cadmium LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_mu | Specifications!E6 | Cadmium MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_result | Specifications!D6 | Cadmium Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_status | Specifications!F6 | Cadmium Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | df | Data!I2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead | Data!G2 | Lead | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead_limit | Specifications!C7 | Lead Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead_loq | Specifications!B7 | Lead LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead_mu | Specifications!E7 | Lead MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead_result | Specifications!D7 | Lead Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury | Data!H2 | Mercury | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_limit | Specifications!C8 | Mercury Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_loq | Specifications!B8 | Mercury LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_mu | Specifications!E8 | Mercury MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_result | Specifications!D8 | Mercury Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_status | Specifications!F8 | Mercury Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | report_results | Report!A1:F6 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | df | Data!G2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | purity_results | 'Purity Data'!C2:R2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | report_results | Report!A1:F21 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_1 | Data!E5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_10 | Data!N5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_11 | Data!O5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_12 | Data!P5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_13 | Data!Q5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_14 | 'Purity Data'!C2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_15 | 'Purity Data'!D2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_16 | 'Purity Data'!E2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_17 | 'Purity Data'!F2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_18 | 'Purity Data'!G2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_19 | 'Purity Data'!H2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_2 | Data!F5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_20 | 'Purity Data'!I2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_21 | 'Purity Data'!J2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_22 | 'Purity Data'!K2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_23 | 'Purity Data'!L2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_24 | 'Purity Data'!M2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_25 | 'Purity Data'!N2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_26 | 'Purity Data'!O2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_27 | 'Purity Data'!P2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_28 | 'Purity Data'!Q2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_29 | 'Purity Data'!R2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_3 | Data!G5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_4 | Data!H5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_5 | Data!I5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_6 | Data!J5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_7 | Data!K5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_8 | Data!L5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_9 | Data!M5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | results | Data!E5:Q5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | total_thc | Report!B1 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | total_thc_report_result | Data!C11 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxinb1 | Data!E2 | Aflatoxin B1 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxinb1_metrc | Specifications!D5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxinb2 | Data!F2 | Aflatoxin B2 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxinb2_metrc | Specifications!D6 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxing1 | Data!G2 | Aflatoxin G1 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxing1_metrc | Specifications!D7 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxing2 | Data!H2 | Aflatoxin G2 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxing2_metrc | Specifications!D8 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | df | Data!J2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | mycotoxin_results | Data!E2:I2 | Mycotoxin Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | ochratoxina | Data!I2 | Ochratoxin A | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | ochratoxina_metrc | Specifications!D9 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | pass_fail | Specifications!F2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | report_results | Report!A1:F8 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | totalmycod_b1b2g1g2_metrc | Specifications!D11 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | totalmycod_b1b2g1g2oa_metrc | Specifications!D10 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | acetone | Data!F2 | Acetone | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | acetone_metrc | Specifications!E9 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | acetonitrile | Data!G2 | Acetonitrile | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | benzene | Data!H2 | Benzene | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | benzene_metrc | Specifications!E11 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | butane_metrc | Specifications!E12 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | butanes | Data!I2 | Butanes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | butanol_metrc | Specifications!E6 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | chloroform | Data!J2 | Chloroform | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | chloroform_metrc | Specifications!E13 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | cyclohexane | Data!K2 | Cyclohexane | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | cyclohexane_metrc | Specifications!E15 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | df | Data!X2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | dichloromethane | Data!L2 | Dichloromethane | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | dichloromethane_metrc | Specifications!E16 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | dioxane14_metrc | Specifications!E5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethanol | Data!M2 | Ethanol | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethanol_metrc | Specifications!E17 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethoxyethanol_metrc | Specifications!E7 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethylacetate | Data!O2 | Ethyl Acetate | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethylacetate_metrc | Specifications!E19 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethylether | Data!N2 | Ethyl Ether | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | heptane | Data!P2 | Heptane | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | heptane_metrc | Specifications!E22 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | hexane_metrc | Specifications!E23 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | hexanes | Data!Q2 | Hexanes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | isopropanol2_metrc | Specifications!E8 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | methanol | Data!R2 | Methanol | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | methanol_metrc | Specifications!E25 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | pass_fail | Specifications!F2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | pentane_metrc | Specifications!E26 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | pentanes | Data!S2 | Pentanes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | propane | Data!T2 | Propane | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | propane_metrc | Specifications!E27 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | propranolipa2 | Data!E2 | 2 Propanol IPA | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | report_results | Report!A1:F31 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | residual_solvents_results | Data!E2:W2 | Residual Solvents Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | toluene | Data!U2 | Toluene | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | toluene_metrc | Specifications!E29 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | totalxylenes | Data!V2 | Total Xylenes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | totalxylenes_metrc | Specifications!E30 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | trichloroethene | Data!W2 | Trichloroethene | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | trichloroethene_metrc | Specifications!E31 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | abamectin_metrc | Specifications!E5 | Abamectin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | acephate_metrc | Specifications!E6 | Acephate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | acequinocyl_metrc | Specifications!E7 | Acequinocyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | acetamiprid_metrc | Specifications!E8 | Acetamiprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | azadirachtin_metrc | Specifications!E9 | Azadirachtin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | azoxystrobin_metrc | Specifications!E10 | Azoxystrobin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | bifenazate_metrc | Specifications!E11 | Bifenazate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | bifenthrin_metrc | Specifications!E12 | Bifenthrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | boscalid_metrc | Specifications!E13 | Boscalid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | carbaryl_metrc | Specifications!E14 | Carbaryl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | chlorantraniliprole_metrc | Specifications!E15 | Chlorantraniliprole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | chlorfenapyr_metrc | Specifications!E16 | Chlorfenapyr METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | chlormequatchloride_metrc | Specifications!E17 | Chlormequat Chloride METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | chlorpyrifos_metrc | Specifications!E18 | Chlorpyrifos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | clofentezine_metrc | Specifications!E19 | Clofentezine METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | cyfluthrin_metrc | Specifications!E20 | Cyfluthrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | cypermethrin_metrc | Specifications!E21 | Cypermethrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | daminozide_metrc | Specifications!E22 | Daminozide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | df | Data!BH2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | diazinon_metrc | Specifications!E23 | Diazinon METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | dimethoate_metrc | Specifications!E25 | Dimethoate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | etofenprox_metrc | Specifications!E26 | Etofenprox METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | etoxazole_metrc | Specifications!E27 | Etoxazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | fenoxycarb_metrc | Specifications!E28 | Fenoxycarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | fenpyroximate_metrc | Specifications!E29 | Fenpyroximate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | fipronil_metrc | Specifications!E30 | Fipronil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | flonicamid_metrc | Specifications!E31 | Flonicamid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | fludioxonil_metrc | Specifications!E32 | Fludioxonil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | hexythiazox_metrc | Specifications!E33 | Hexythiazox METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | imazalil_metrc | Specifications!E34 | Imazalil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | imidacloprid_metrc | Specifications!E35 | Imidacloprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | kresoximmethyl_metrc | Specifications!E36 | Kresoxim Methyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | malathion_metrc | Specifications!E37 | Malathion METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | metalaxyl_metrc | Specifications!E38 | Metalaxyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | methiocarb_metrc | Specifications!E39 | Methiocarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | methomyl_metrc | Specifications!E40 | Methomyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | myclobutanil_metrc | Specifications!E41 | Myclobutanil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | naled_metrc | Specifications!E42 | Naled METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | oxamyl_metrc | Specifications!E43 | Oxamyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | paclobutrazol_metrc | Specifications!E44 | Paclobutrazol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | pass_fail | Specifications!F2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | permethrins_metrc | Specifications!E45 | Permethrins METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | pesticides_results | Data!E2:BG2 | Pesticide Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | phosmet_metrc | Specifications!E46 | Phosmet METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | piperonyl_butoxide_metrc | Specifications!E47 | Piperonyl Butoxide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | prallethrin_metrc | Specifications!E48 | Prallethrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | propiconazole_metrc | Specifications!E49 | Propiconazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | propoxur_metrc | Specifications!E50 | Propoxur METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | pyrethrins_metrc | Specifications!E51 | Pyrethrins METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | pyridaben_metrc | Specifications!E52 | Pyridaben METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | report_results | Report!A1:R25 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | report_results_single | A1:F75 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | spinosad_metrc | Specifications!E55 | Spinosad METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | spiromesifen_metrc | Specifications!E56 | Spiromesifen METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | spirotetramat_metrc | Specifications!E57 | Spirotetramat METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | tebuconazole_metrc | Specifications!E58 | Tebuconazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | thiamethoxam_metrc | Specifications!E59 | Thiamethoxam METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | trifloxystrobin_metrc | Specifications!E60 | Trifloxystrobin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | abamectin_metrc | Specifications!E5 | Abamectin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | acephate_metrc | Specifications!E6 | Acephate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | acequinocyl_metrc | Specifications!E7 | Acequinocyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | acetamiprid_metrc | Specifications!E8 | Acetamiprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | aldicarb_metrc | Specifications!E9 | Aldicarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | azadirachtin_metrc | Specifications!E10 | Azadirachtin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | azoxystrobin_metrc | Specifications!E11 | Azoxystrobin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | bifenazate_metrc | Specifications!E12 | Bifenazate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | bifenthrin_metrc | Specifications!E13 | Bifenthrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | boscalid_metrc | Specifications!E14 | Boscalid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | carbaryl_metrc | Specifications!E15 | Carbaryl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | carbofuran_metrc | Specifications!E16 | Carbofuran METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlorantraniliprole_metrc | Specifications!E17 | Chlorantraniliprole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlorfenapyr_metrc | Specifications!E18 | Chlorfenapyr METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlormequat_metrc | Specifications!E19 | Chlormequat METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlormequatchloride_metrc | Specifications!E20 | Chlormequat Chloride METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlorpyrifos_metrc | Specifications!E21 | Chlorpyrifos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | clofentezine_metrc | Specifications!E22 | Clofentezine METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | coumaphos_metrc | Specifications!E23 | Coumaphos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | cyfluthrin_metrc | Specifications!E24 | Cyfluthrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | cypermethrin_metrc | Specifications!E25 | Cypermethrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | daminozide_metrc | Specifications!E27 | Daminozide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | ddvp_metrc | Specifications!E26 | DDVP METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | diazinon_metrc | Specifications!E28 | Diazinon METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | dimethoate_metrc | Specifications!E29 | Dimethoate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | dimethomorph_metrc | Specifications!E30 | Dimethomorph METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | ethoprophos_metrc | Specifications!E31 | Ethoprophos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | etofenprox_metrc | Specifications!E32 | Etofenprox METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | etoxazole_metrc | Specifications!E33 | Etoxazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fenhexamid_metrc | Specifications!E34 | Fenhexamid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fenoxycarb_metrc | Specifications!E35 | Fenoxycarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fenpyroximate_metrc | Specifications!E36 | Fenpyroximate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fipronil_metrc | Specifications!E37 | Fipronil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | flonicamid_metrc | Specifications!E38 | Flonicamid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fludioxonil_metrc | Specifications!E39 | Fludioxonil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | hexythiazox_metrc | Specifications!E40 | Hexythiazox METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | imazalil_metrc | Specifications!E41 | Imazalil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | imidacloprid_metrc | Specifications!E42 | Imidacloprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | kresoximmethyl_metrc | Specifications!E43 | Kresoxim Methyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | malathion_metrc | Specifications!E45 | Malathion METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | metalaxyl_metrc | Specifications!E46 | Metalaxyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | metalaxylmefenoxam_metrc | Specifications!E47 | Metalaxyl/Mefenoxam METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | methiocarb_metrc | Specifications!E48 | Methiocarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | methomyl_metrc | Specifications!E49 | Methomyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | methyl_parathion_metrc | Specifications!E50 | Methyl Parathion METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | mevinphos_metrc | Specifications!E51 | Mevinphos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | mgk264_metrc | Specifications!E44 | MGK-264 METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | myclobutanil_metrc | Specifications!E52 | Myclobutanil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | naled_metrc | Specifications!E53 | Naled METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | oxamyl_metrc | Specifications!E54 | Oxamyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | paclobutrazol_metrc | Specifications!E55 | Paclobutrazol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pass_fail | Specifications!F2 |  | Yes | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pentachlorobenzene_metrc | Specifications!E56 | Pentachlorobenzene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | permethrins_metrc | Specifications!E57 | Permethrins METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pesticides_results | Data!E2:BU2 | Pesticide Results | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | phosmet_metrc | Specifications!E58 | Phosmet METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | piperonyl_butoxide_metrc | Specifications!E59 | Piperonyl Butoxide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | prallethrin_metrc | Specifications!E60 | Prallethrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | propiconazole_metrc | Specifications!E61 | Propiconazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | propoxur_metrc | Specifications!E62 | Propoxur METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pyrethrins_metrc | Specifications!E63 | Pyrethrins METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pyridaben_metrc | Specifications!E64 | Pyridaben METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | report_results | Report!A1:L40 |  | Yes | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spinetoram_metrc | Specifications!E65 | Spinetoram METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spinosad_metrc | Specifications!E66 | Spinosad METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spiromesifen_metrc | Specifications!E67 | Spiromesifen METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spirotetramat_metrc | Specifications!E68 | Spirotetramat METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spiroxamine_metrc | Specifications!E69 | Spiroxamine METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | tebuconazole_metrc | Specifications!E70 | Tebuconazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | thiacloprid_metrc | Specifications!E71 | Thiacloprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | thiamethoxam_metrc | Specifications!E72 | Thiamethoxam METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | trifloxystrobin_metrc | Specifications!E73 | Trifloxystrobin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_0 | F3 | Water Activity 0 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_1 | F4 | Water Activity 1 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_10 | F15 | Water Activity 10 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_11 | F16 | Water Activity 11 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_12 | F17 | Water Activity 12 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_13 | F18 | Water Activity 13 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_14 | F19 | Water Activity 14 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_15 | F20 | Water Activity 15 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_16 | F21 | Water Activity 16 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_17 | F22 | Water Activity 17 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_18 | F23 | Water Activity 18 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_19 | F24 | Water Activity 19 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_2 | F5 | Water Activity 2 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_20 | F27 | Water Activity 20 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_21 | F28 | Water Activity 21 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_22 | F29 | Water Activity 22 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_23 | F30 | Water Activity 23 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_24 | F31 | Water Activity 24 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_25 | F32 | Water Activity 25 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_26 | F33 | Water Activity 26 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_27 | F34 | Water Activity 27 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_28 | F35 | Water Activity 28 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_29 | F36 | Water Activity 29 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_3 | F6 | Water Activity 3 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_30 | F39 | Water Activity 30 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_31 | F40 | Water Activity 31 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_32 | F41 | Water Activity 32 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_33 | F42 | Water Activity 33 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_34 | F43 | Water Activity 34 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_35 | F44 | Water Activity 35 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_36 | F45 | Water Activity 36 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_37 | F46 | Water Activity 37 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_38 | F47 | Water Activity 38 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_39 | F48 | Water Activity 39 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_4 | F7 | Water Activity 4 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_5 | F8 | Water Activity 5 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_6 | F9 | Water Activity 6 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_7 | F10 | Water Activity 7 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_8 | F11 | Water Activity 8 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_9 | F12 | Water Activity 9 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_1 | F13 | Water Activity SS 1 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_1_control | F14 | Water Activity SS 1 Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_2 | F25 | Water Activity SS 2 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_2_control | F26 | Water Activity SS 2 Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_3 | F37 | Water Activity SS 3 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_3_control | F38 | Water Activity SS 3 Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_4 | F49 | Water Activity SS 4 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_4_control | F50 | Water Activity SS 4 Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Test WS] | metrc_analyte_name_wateractivity | METRC!A5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | metrc_notes_wateractivity | METRC!D5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | metrc_pass_fail_wateractivity | METRC!C5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | metrc_quantity_wateractivity | METRC!B5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | metrc_to_include_wateractivity | METRC!E5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | pass_fail_report | Specifications!B7 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | wateractivity_metrc | Specifications!D5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | wateractivityaw | Data!D2 | Water Activity aw | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Batch WS] | test | F2 | stes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Batch WS] | test2 | F3 | steste | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Foreign_Material | Foreign Material [Test WS] | ffm_metrc | Report!C2 | Foreign Material METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Foreign_Material | Foreign Material [Test WS] | pass_fail | Data!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Foreign_Material | Foreign Material [Test WS] | report_results | Report!A1:C5 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | ahumulene_metrc | D22 | A Humulene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | ahumulene_metrc_mgg | E22 | A Humulene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | apinene_metrc | D5 | A Pinene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | apinene_metrc_mgg | E5 | A Pinene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | aterpinene_metrc | D10 | A Terpinene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | aterpinene_metrc_mgg | E10 | A Terpinene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bcaryophyllene_metrc | D21 | B Caryophyllene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bcaryophyllene_metrc_mgg | E21 | B Caryophyllene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bisabolol_metrc | D27 | Bisabolol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bisabolol_metrc_mgg | E27 | Bisabolol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bmyrcene_metrc | D7 | B Myrcene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bmyrcene_metrc_mgg | E7 | B Myrcene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bpinene_metrc | D8 | B Pinene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bpinene_metrc_mgg | E8 | B Pinene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | camphene_metrc | D6 | Camphene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | camphene_metrc_mgg | E6 | Camphene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | caryophylleneoxide_metrc | D26 | Caryophyllene Oxide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | caryophylleneoxide_metrc_mgg | E26 | Caryophyllene Oxide METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | cisnerolidol_metrc | D23 | Cis Nerolidol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | cisnerolidol_metrc_mgg | E23 | Cis Nerolidol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | cisocimene_metrc | D11 | Cis Ocimene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | cisocimene_metrc_mgg | E11 | Cis Ocimene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | delta3carene_metrc | D9 | Delta 3 Carene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | delta3carene_metrc_mgg | E9 | Delta 3 Carene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | dlimonene_metrc | D12 | D Limonene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | dlimonene_metrc_mgg | E12 | D Limonene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | eucalyptol_metrc | D15 | Eucalyptol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | eucalyptol_metrc_mgg | E15 | Eucalyptol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | geraniol_metrc | D20 | Geraniol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | geraniol_metrc_mgg | E20 | Geraniol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | gterpinene_metrc | D16 | G Terpinene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | gterpinene_metrc_mgg | E16 | G Terpinene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | guaiol_metrc | D25 | Guaiol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | guaiol_metrc_mgg | E25 | Guaiol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | isopulegol_metrc | D19 | Isopulegol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | isopulegol_metrc_mgg | E19 | Isopulegol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | linalool_metrc | D18 | Linalool METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | linalool_metrc_mgg | E18 | Linalool METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | pcymene_metrc | D13 | P Cymene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | pcymene_metrc_mgg | E13 | P Cymene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | terpinolene_metrc | D17 | Terpinolene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | terpinolene_metrc_mgg | E17 | Terpinolene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | testterpenes | E4 | Test Terpenes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | transnerolidol_metrc | D24 | Trans Nerolidol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | transnerolidol_metrc_mgg | E24 | Trans Nerolidol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | transocimene_metrc | D14 | Trans Ocimene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | transocimene_metrc_mgg | E14 | Trans Ocimene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | aspergillusspp | I2 | Aspergillus spp. | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | aspergillusspp_metrc | Specifications!E10 | Aspergillus Spp METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | enterobacteriaceae | F2 | Enterobacteriaceae | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | enterobacteriaceae_metrc | Specifications!E7 | Enterobacteriaceae METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | lmonocytogenes | J2 | L. monocytogenes | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | lmonocytogenes_metrc | Specifications!E11 | L Monocytogenes METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | microbials_results | Data!D2:J2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | report_result | Report!A1:F9 |  | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | salmonellaspecies | G2 | Salmonella species | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | salmonellaspecies_metrc | Specifications!E8 | Salmonella Species METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | shigatoxin_producingecoli_metrc | Specifications!E9 | Shiga Toxin-Producing E Coli METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | shigatoxinproducingecoli | H2 | Shiga toxin-producing E. coli | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | totalaerobic | D2 | Total aerobic microbial | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | totalaerobicmicrobial_metrc | Specifications!E5 | Total Aerobic Microbial METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | totalyeastandmold_metrc | Specifications!E6 | Total Yeast And Mold METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | yeastmold | E2 | Total yeast and mold | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Homogeneity | Homogeneity [Test WS] | average_actual_unit_mass_g | Data!B8 | Average Actual Unit Mass g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | duplicate_cp_test_id_check | Data!B36 | Duplicate CP Test ID Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | extra_pasted_rows_check | Data!B37 | Extra Pasted Rows Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_cannabinoid_1_label_variance | Data!B28 | Cannabinoid 1 Label Variance for Highest Cannabinoid | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_cannabinoid_2_label_variance | Data!B30 | Cannabinoid 2 Label Variance for Highest Cannabinoid | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_mass_label_variance | Data!B26 | Mass Label Variance for Highest Unit Mass | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_reported_cannabinoid_1_mg_container | Data!B27 | Highest Reported Cannabinoid 1 mg/container | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_reported_cannabinoid_2_mg_container | Data!B29 | Highest Reported Cannabinoid 2 mg/container | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_reported_unit_mass_g | Data!B25 | Highest Reported Unit Mass g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | homogeneity_metrc | COA!F1 | Homogeneity METRC | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_cannabinoid_1_mg_container | Data!B4 | Label Cannabinoid 1 mg/container | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_cannabinoid_1_source_status | Paste!Q4 | Label Cannabinoid 1 Source Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_cannabinoid_2_mg_container | Data!B6 | Label Cannabinoid 2 mg/container | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_cannabinoid_2_source_status | Paste!U4 | Label Cannabinoid 2 Source Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_unit_mass_g | Data!B7 | Label Unit Mass g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | manual_label_cannabinoid_1_mg_container | Paste!O4 | Manual Label Cannabinoid 1 mg/container Override | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | manual_label_cannabinoid_2_mg_container | Paste!S4 | Manual Label Cannabinoid 2 mg/container Override | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | optional_target_2_label_claim_check | Data!B41 | Optional Target 2 Label Claim Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | parent_sample_match_check | Data!B38 | Parent Sample Match Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | pass_fail | Data!B31 | Pass/Fail | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | qbench_sample_label_amount_lookup | Paste!N24:P36 | QBench Sample Label Amount Lookup | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | replicate_count | Data!B34 | Replicate Rows Present | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | replicate_results | COA!A10:G20 | Homogeneity Replicate Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | report_results | COA!A1:G20 | Homogeneity COA Output | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | required_target_fields_check | Data!B40 | Required Target 1 and Label Claim Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | required_unit_mass_check | Data!B39 | Required Unit Mass Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | reviewer_parent_sample_confirmation | Paste!D6 | Reviewer Parent Sample Confirmation | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | target_cannabinoid_1 | Data!B3 | Target Cannabinoid 1 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | target_cannabinoid_2 | Data!B5 | Target Cannabinoid 2 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | unique_cp_test_id_count | Data!B35 | Unique CP Test IDs Counted | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | validation_status | Data!B42 | Overall Input Validation Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_limit | Specifications!C5 | Aspergillus Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_loq | Specifications!B5 | Aspergillus LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_mu | Specifications!E5 | Aspergillus MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_result | Specifications!D9 | Aspergillus Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_status | Specifications!F9 | Aspergillus Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | aspergillusspp_metrc | Report!C6 | Aspergillus Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | flavus_result | Data!E3 | A. Flavus Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | fumigatus_result | Data!E4 | A. fumigatus Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_analyte_name_aspergillusspp | METRC!A5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_notes_aspergillusspp | METRC!D5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_pass_fail_aspergillusspp | METRC!C5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_quantity_aspergillusspp | METRC!B5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_to_include_aspergillusspp | METRC!E5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | niger_result | Data!E2 | A. niger (HEX) Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | report_content | Report!A2:D5 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | report_header | Report!A1:D1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | report_results | Report!A1:D5 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | sub_species | Data!F2 | Asp Sub Species | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | terreus_result | Data!E5 | A. terreus Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_limit | Specifications!C5 | Salmonella Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_loq | Specifications!B5 | Salmonella LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_mu | Specifications!E5 | Salmonella MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_result | Specifications!D5 | Salmonella Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_status | Specifications!F5 | Salmonella Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salmonella_results | Data!E2 | Salmonella Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_limit | Specifications!C5 | STEC Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_loq | Specifications!B5 | STEC LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_mu | Specifications!E5 | STEC MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_result | Specifications!D5 | STEC Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_results | Data!E2 | STEC Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_status | Specifications!F5 | STEC Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Listeria | Listeria Monocytogenes [Test] Worksheet | lis_results | Data!E2 | Listeria Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Listeria | Listeria Monocytogenes [Test] Worksheet | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Listeria | Listeria Monocytogenes [Test] Worksheet | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Listeria | Listeria Monocytogenes [Test] Worksheet | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_limit | Specifications!C5 | Total Aerobic Count Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_loq | Specifications!B5 | Total Aerobic Count LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_mu | Specifications!E5 | Total Aerobic Count MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_result | Specifications!D5 | Total Aerobic Count Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_results | Data!E2 | Total Aerobic Count Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_status | Specifications!F5 | Total Aerobic Count Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_limit | Specifications!C5 | Total Yeast and Mold Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_loq | Specifications!B5 | Total Yeast and Mold LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_mu | Specifications!E5 | Total Yeast and Mold MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_result | Specifications!D5 | Total Yeast and Mold Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_results | Data!E2 | YM Automation Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_status | Specifications!F5 | Total Yeast and Mold Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_limit | Specifications!C5 | Enterobacteriaceae Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_loq | Specifications!B5 | Enterobacteriaceae LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_mu | Specifications!E5 | Enterobacteriaceae MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_result | Specifications!D5 | Enterobacteriaceae Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_results | Data!E2 | Enterobacteriaceae Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_status | Specifications!F5 | Enterobacteriaceae Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |

## Deprecated duplicate 3 of 3 — Rescan 2026-07-04 (preserved, do not use)

| Assay | Worksheet | Named Cell | Cell/Range | Purpose | Used by COA? | Notes |
|---|---|---|---|---|---|---|
| Other | Example Batch Worksheet | control | D2 | Control  | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Other | [Batch] Example Worksheet | control | D2 | Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Other | Training Worksheet | example_named_cell | General!A18 | Example | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic | Data!E2 | Arsenic | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_limit | Specifications!C5 | Arsenic Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_loq | Specifications!B5 | Arsenic LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_mu | Specifications!E5 | Arsenic MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_result | Specifications!D5 | Arsenic Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | arsenic_status | Specifications!F5 | Arsenic Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium | Data!F2 | Cadmium  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_limit | Specifications!C6 | Cadmium Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_loq | Specifications!B6 | Cadmium LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_mu | Specifications!E6 | Cadmium MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_result | Specifications!D6 | Cadmium Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | cadmium_status | Specifications!F6 | Cadmium Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | df | Data!I2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead | Data!G2 | Lead | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead_limit | Specifications!C7 | Lead Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead_loq | Specifications!B7 | Lead LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead_mu | Specifications!E7 | Lead MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | lead_result | Specifications!D7 | Lead Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury | Data!H2 | Mercury | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_limit | Specifications!C8 | Mercury Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_loq | Specifications!B8 | Mercury LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_mu | Specifications!E8 | Mercury MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_result | Specifications!D8 | Mercury Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | mercury_status | Specifications!F8 | Mercury Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Heavy_Metals | Heavy Metals [Test] Worksheet | report_results | Report!A1:F6 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | df | Data!G2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | purity_results | 'Purity Data'!C2:R2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | report_results | Report!A1:F21 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_1 | Data!E5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_10 | Data!N5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_11 | Data!O5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_12 | Data!P5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_13 | Data!Q5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_14 | 'Purity Data'!C2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_15 | 'Purity Data'!D2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_16 | 'Purity Data'!E2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_17 | 'Purity Data'!F2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_18 | 'Purity Data'!G2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_19 | 'Purity Data'!H2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_2 | Data!F5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_20 | 'Purity Data'!I2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_21 | 'Purity Data'!J2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_22 | 'Purity Data'!K2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_23 | 'Purity Data'!L2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_24 | 'Purity Data'!M2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_25 | 'Purity Data'!N2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_26 | 'Purity Data'!O2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_27 | 'Purity Data'!P2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_28 | 'Purity Data'!Q2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_29 | 'Purity Data'!R2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_3 | Data!G5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_4 | Data!H5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_5 | Data!I5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_6 | Data!J5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_7 | Data!K5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_8 | Data!L5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | result_9 | Data!M5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | results | Data!E5:Q5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | total_thc | Report!B1 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Cannabinoids | Cannabinoid Potency [Test] Worksheet | total_thc_report_result | Data!C11 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxinb1 | Data!E2 | Aflatoxin B1 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxinb1_metrc | Specifications!D5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxinb2 | Data!F2 | Aflatoxin B2 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxinb2_metrc | Specifications!D6 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxing1 | Data!G2 | Aflatoxin G1 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxing1_metrc | Specifications!D7 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxing2 | Data!H2 | Aflatoxin G2 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | aflatoxing2_metrc | Specifications!D8 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | df | Data!J2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | mycotoxin_results | Data!E2:I2 | Mycotoxin Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | ochratoxina | Data!I2 | Ochratoxin A | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | ochratoxina_metrc | Specifications!D9 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | pass_fail | Specifications!F2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | report_results | Report!A1:F8 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | totalmycod_b1b2g1g2_metrc | Specifications!D11 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Mycotoxins | Mycotoxin (Qualitative) [Test] Worksheet | totalmycod_b1b2g1g2oa_metrc | Specifications!D10 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | acetone | Data!F2 | Acetone | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | acetone_metrc | Specifications!E9 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | acetonitrile | Data!G2 | Acetonitrile | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | benzene | Data!H2 | Benzene | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | benzene_metrc | Specifications!E11 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | butane_metrc | Specifications!E12 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | butanes | Data!I2 | Butanes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | butanol_metrc | Specifications!E6 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | chloroform | Data!J2 | Chloroform | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | chloroform_metrc | Specifications!E13 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | cyclohexane | Data!K2 | Cyclohexane | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | cyclohexane_metrc | Specifications!E15 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | df | Data!X2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | dichloromethane | Data!L2 | Dichloromethane | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | dichloromethane_metrc | Specifications!E16 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | dioxane14_metrc | Specifications!E5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethanol | Data!M2 | Ethanol | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethanol_metrc | Specifications!E17 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethoxyethanol_metrc | Specifications!E7 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethylacetate | Data!O2 | Ethyl Acetate | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethylacetate_metrc | Specifications!E19 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | ethylether | Data!N2 | Ethyl Ether | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | heptane | Data!P2 | Heptane | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | heptane_metrc | Specifications!E22 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | hexane_metrc | Specifications!E23 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | hexanes | Data!Q2 | Hexanes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | isopropanol2_metrc | Specifications!E8 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | methanol | Data!R2 | Methanol | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | methanol_metrc | Specifications!E25 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | pass_fail | Specifications!F2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | pentane_metrc | Specifications!E26 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | pentanes | Data!S2 | Pentanes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | propane | Data!T2 | Propane | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | propane_metrc | Specifications!E27 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | propranolipa2 | Data!E2 | 2 Propanol IPA | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | report_results | Report!A1:F31 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | residual_solvents_results | Data!E2:W2 | Residual Solvents Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | toluene | Data!U2 | Toluene | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | toluene_metrc | Specifications!E29 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | totalxylenes | Data!V2 | Total Xylenes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | totalxylenes_metrc | Specifications!E30 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | trichloroethene | Data!W2 | Trichloroethene | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Residual_Solvents | Residual Solvents [Test] Worksheet | trichloroethene_metrc | Specifications!E31 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | abamectin_metrc | Specifications!E5 | Abamectin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | acephate_metrc | Specifications!E6 | Acephate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | acequinocyl_metrc | Specifications!E7 | Acequinocyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | acetamiprid_metrc | Specifications!E8 | Acetamiprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | azadirachtin_metrc | Specifications!E9 | Azadirachtin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | azoxystrobin_metrc | Specifications!E10 | Azoxystrobin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | bifenazate_metrc | Specifications!E11 | Bifenazate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | bifenthrin_metrc | Specifications!E12 | Bifenthrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | boscalid_metrc | Specifications!E13 | Boscalid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | carbaryl_metrc | Specifications!E14 | Carbaryl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | chlorantraniliprole_metrc | Specifications!E15 | Chlorantraniliprole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | chlorfenapyr_metrc | Specifications!E16 | Chlorfenapyr METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | chlormequatchloride_metrc | Specifications!E17 | Chlormequat Chloride METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | chlorpyrifos_metrc | Specifications!E18 | Chlorpyrifos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | clofentezine_metrc | Specifications!E19 | Clofentezine METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | cyfluthrin_metrc | Specifications!E20 | Cyfluthrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | cypermethrin_metrc | Specifications!E21 | Cypermethrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | daminozide_metrc | Specifications!E22 | Daminozide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | df | Data!BH2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | diazinon_metrc | Specifications!E23 | Diazinon METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | dimethoate_metrc | Specifications!E25 | Dimethoate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | etofenprox_metrc | Specifications!E26 | Etofenprox METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | etoxazole_metrc | Specifications!E27 | Etoxazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | fenoxycarb_metrc | Specifications!E28 | Fenoxycarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | fenpyroximate_metrc | Specifications!E29 | Fenpyroximate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | fipronil_metrc | Specifications!E30 | Fipronil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | flonicamid_metrc | Specifications!E31 | Flonicamid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | fludioxonil_metrc | Specifications!E32 | Fludioxonil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | hexythiazox_metrc | Specifications!E33 | Hexythiazox METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | imazalil_metrc | Specifications!E34 | Imazalil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | imidacloprid_metrc | Specifications!E35 | Imidacloprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | kresoximmethyl_metrc | Specifications!E36 | Kresoxim Methyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | malathion_metrc | Specifications!E37 | Malathion METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | metalaxyl_metrc | Specifications!E38 | Metalaxyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | methiocarb_metrc | Specifications!E39 | Methiocarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | methomyl_metrc | Specifications!E40 | Methomyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | myclobutanil_metrc | Specifications!E41 | Myclobutanil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | naled_metrc | Specifications!E42 | Naled METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | oxamyl_metrc | Specifications!E43 | Oxamyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | paclobutrazol_metrc | Specifications!E44 | Paclobutrazol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | pass_fail | Specifications!F2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | permethrins_metrc | Specifications!E45 | Permethrins METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | pesticides_results | Data!E2:BG2 | Pesticide Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | phosmet_metrc | Specifications!E46 | Phosmet METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | piperonyl_butoxide_metrc | Specifications!E47 | Piperonyl Butoxide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | prallethrin_metrc | Specifications!E48 | Prallethrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | propiconazole_metrc | Specifications!E49 | Propiconazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | propoxur_metrc | Specifications!E50 | Propoxur METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | pyrethrins_metrc | Specifications!E51 | Pyrethrins METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | pyridaben_metrc | Specifications!E52 | Pyridaben METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | report_results | Report!A1:R25 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | report_results_single | A1:F75 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | spinosad_metrc | Specifications!E55 | Spinosad METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | spiromesifen_metrc | Specifications!E56 | Spiromesifen METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | spirotetramat_metrc | Specifications!E57 | Spirotetramat METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | tebuconazole_metrc | Specifications!E58 | Tebuconazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | thiamethoxam_metrc | Specifications!E59 | Thiamethoxam METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Qualitative) [Test] Worksheet | trifloxystrobin_metrc | Specifications!E60 | Trifloxystrobin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | abamectin_metrc | Specifications!E5 | Abamectin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | acephate_metrc | Specifications!E6 | Acephate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | acequinocyl_metrc | Specifications!E7 | Acequinocyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | acetamiprid_metrc | Specifications!E8 | Acetamiprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | aldicarb_metrc | Specifications!E9 | Aldicarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | azadirachtin_metrc | Specifications!E10 | Azadirachtin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | azoxystrobin_metrc | Specifications!E11 | Azoxystrobin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | bifenazate_metrc | Specifications!E12 | Bifenazate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | bifenthrin_metrc | Specifications!E13 | Bifenthrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | boscalid_metrc | Specifications!E14 | Boscalid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | carbaryl_metrc | Specifications!E15 | Carbaryl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | carbofuran_metrc | Specifications!E16 | Carbofuran METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlorantraniliprole_metrc | Specifications!E17 | Chlorantraniliprole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlorfenapyr_metrc | Specifications!E18 | Chlorfenapyr METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlormequat_metrc | Specifications!E19 | Chlormequat METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlormequatchloride_metrc | Specifications!E20 | Chlormequat Chloride METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | chlorpyrifos_metrc | Specifications!E21 | Chlorpyrifos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | clofentezine_metrc | Specifications!E22 | Clofentezine METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | coumaphos_metrc | Specifications!E23 | Coumaphos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | cyfluthrin_metrc | Specifications!E24 | Cyfluthrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | cypermethrin_metrc | Specifications!E25 | Cypermethrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | daminozide_metrc | Specifications!E27 | Daminozide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | ddvp_metrc | Specifications!E26 | DDVP METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | diazinon_metrc | Specifications!E28 | Diazinon METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | dimethoate_metrc | Specifications!E29 | Dimethoate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | dimethomorph_metrc | Specifications!E30 | Dimethomorph METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | ethoprophos_metrc | Specifications!E31 | Ethoprophos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | etofenprox_metrc | Specifications!E32 | Etofenprox METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | etoxazole_metrc | Specifications!E33 | Etoxazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fenhexamid_metrc | Specifications!E34 | Fenhexamid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fenoxycarb_metrc | Specifications!E35 | Fenoxycarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fenpyroximate_metrc | Specifications!E36 | Fenpyroximate METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fipronil_metrc | Specifications!E37 | Fipronil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | flonicamid_metrc | Specifications!E38 | Flonicamid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | fludioxonil_metrc | Specifications!E39 | Fludioxonil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | hexythiazox_metrc | Specifications!E40 | Hexythiazox METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | imazalil_metrc | Specifications!E41 | Imazalil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | imidacloprid_metrc | Specifications!E42 | Imidacloprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | kresoximmethyl_metrc | Specifications!E43 | Kresoxim Methyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | malathion_metrc | Specifications!E45 | Malathion METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | metalaxyl_metrc | Specifications!E46 | Metalaxyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | metalaxylmefenoxam_metrc | Specifications!E47 | Metalaxyl/Mefenoxam METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | methiocarb_metrc | Specifications!E48 | Methiocarb METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | methomyl_metrc | Specifications!E49 | Methomyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | methyl_parathion_metrc | Specifications!E50 | Methyl Parathion METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | mevinphos_metrc | Specifications!E51 | Mevinphos METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | mgk264_metrc | Specifications!E44 | MGK-264 METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | myclobutanil_metrc | Specifications!E52 | Myclobutanil METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | naled_metrc | Specifications!E53 | Naled METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | oxamyl_metrc | Specifications!E54 | Oxamyl METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | paclobutrazol_metrc | Specifications!E55 | Paclobutrazol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pass_fail | Specifications!F2 |  | Yes | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pentachlorobenzene_metrc | Specifications!E56 | Pentachlorobenzene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | permethrins_metrc | Specifications!E57 | Permethrins METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pesticides_results | Data!E2:BU2 | Pesticide Results | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | phosmet_metrc | Specifications!E58 | Phosmet METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | piperonyl_butoxide_metrc | Specifications!E59 | Piperonyl Butoxide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | prallethrin_metrc | Specifications!E60 | Prallethrin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | propiconazole_metrc | Specifications!E61 | Propiconazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | propoxur_metrc | Specifications!E62 | Propoxur METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pyrethrins_metrc | Specifications!E63 | Pyrethrins METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | pyridaben_metrc | Specifications!E64 | Pyridaben METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | report_results | Report!A1:L40 |  | Yes | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spinetoram_metrc | Specifications!E65 | Spinetoram METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spinosad_metrc | Specifications!E66 | Spinosad METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spiromesifen_metrc | Specifications!E67 | Spiromesifen METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spirotetramat_metrc | Specifications!E68 | Spirotetramat METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | spiroxamine_metrc | Specifications!E69 | Spiroxamine METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | tebuconazole_metrc | Specifications!E70 | Tebuconazole METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | thiacloprid_metrc | Specifications!E71 | Thiacloprid METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | thiamethoxam_metrc | Specifications!E72 | Thiamethoxam METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Pesticides | Pesticides (Quantitative) [Test] Worksheet | trifloxystrobin_metrc | Specifications!E73 | Trifloxystrobin METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_0 | F3 | Water Activity 0 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_1 | F4 | Water Activity 1 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_10 | F15 | Water Activity 10 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_11 | F16 | Water Activity 11 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_12 | F17 | Water Activity 12 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_13 | F18 | Water Activity 13 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_14 | F19 | Water Activity 14 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_15 | F20 | Water Activity 15 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_16 | F21 | Water Activity 16 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_17 | F22 | Water Activity 17 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_18 | F23 | Water Activity 18 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_19 | F24 | Water Activity 19 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_2 | F5 | Water Activity 2 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_20 | F27 | Water Activity 20 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_21 | F28 | Water Activity 21 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_22 | F29 | Water Activity 22 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_23 | F30 | Water Activity 23 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_24 | F31 | Water Activity 24 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_25 | F32 | Water Activity 25 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_26 | F33 | Water Activity 26 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_27 | F34 | Water Activity 27 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_28 | F35 | Water Activity 28 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_29 | F36 | Water Activity 29 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_3 | F6 | Water Activity 3 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_30 | F39 | Water Activity 30 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_31 | F40 | Water Activity 31 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_32 | F41 | Water Activity 32 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_33 | F42 | Water Activity 33 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_34 | F43 | Water Activity 34 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_35 | F44 | Water Activity 35 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_36 | F45 | Water Activity 36 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_37 | F46 | Water Activity 37 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_38 | F47 | Water Activity 38 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_39 | F48 | Water Activity 39 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_4 | F7 | Water Activity 4 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_5 | F8 | Water Activity 5 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_6 | F9 | Water Activity 6 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_7 | F10 | Water Activity 7 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_8 | F11 | Water Activity 8 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_9 | F12 | Water Activity 9 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_1 | F13 | Water Activity SS 1 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_1_control | F14 | Water Activity SS 1 Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_2 | F25 | Water Activity SS 2 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_2_control | F26 | Water Activity SS 2 Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_3 | F37 | Water Activity SS 3 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_3_control | F38 | Water Activity SS 3 Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_4 | F49 | Water Activity SS 4 | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Protocol WS] Sample Analysis | wateractivity_ss_4_control | F50 | Water Activity SS 4 Control | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Water_Activity | Water Activity [Test WS] | metrc_analyte_name_wateractivity | METRC!A5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | metrc_notes_wateractivity | METRC!D5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | metrc_pass_fail_wateractivity | METRC!C5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | metrc_quantity_wateractivity | METRC!B5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | metrc_to_include_wateractivity | METRC!E5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | pass_fail_report | Specifications!B7 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | wateractivity_metrc | Specifications!D5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Test WS] | wateractivityaw | Data!D2 | Water Activity aw | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Batch WS] | test | F2 | stes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Water_Activity | Water Activity [Batch WS] | test2 | F3 | steste | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Foreign_Material | Foreign Material [Test WS] | ffm_metrc | Report!C2 | Foreign Material METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Foreign_Material | Foreign Material [Test WS] | pass_fail | Data!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Foreign_Material | Foreign Material [Test WS] | report_results | Report!A1:C5 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | ahumulene_metrc | D22 | A Humulene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | ahumulene_metrc_mgg | E22 | A Humulene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | apinene_metrc | D5 | A Pinene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | apinene_metrc_mgg | E5 | A Pinene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | aterpinene_metrc | D10 | A Terpinene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | aterpinene_metrc_mgg | E10 | A Terpinene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bcaryophyllene_metrc | D21 | B Caryophyllene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bcaryophyllene_metrc_mgg | E21 | B Caryophyllene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bisabolol_metrc | D27 | Bisabolol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bisabolol_metrc_mgg | E27 | Bisabolol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bmyrcene_metrc | D7 | B Myrcene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bmyrcene_metrc_mgg | E7 | B Myrcene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bpinene_metrc | D8 | B Pinene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | bpinene_metrc_mgg | E8 | B Pinene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | camphene_metrc | D6 | Camphene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | camphene_metrc_mgg | E6 | Camphene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | caryophylleneoxide_metrc | D26 | Caryophyllene Oxide METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | caryophylleneoxide_metrc_mgg | E26 | Caryophyllene Oxide METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | cisnerolidol_metrc | D23 | Cis Nerolidol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | cisnerolidol_metrc_mgg | E23 | Cis Nerolidol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | cisocimene_metrc | D11 | Cis Ocimene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | cisocimene_metrc_mgg | E11 | Cis Ocimene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | delta3carene_metrc | D9 | Delta 3 Carene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | delta3carene_metrc_mgg | E9 | Delta 3 Carene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | dlimonene_metrc | D12 | D Limonene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | dlimonene_metrc_mgg | E12 | D Limonene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | eucalyptol_metrc | D15 | Eucalyptol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | eucalyptol_metrc_mgg | E15 | Eucalyptol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | geraniol_metrc | D20 | Geraniol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | geraniol_metrc_mgg | E20 | Geraniol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | gterpinene_metrc | D16 | G Terpinene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | gterpinene_metrc_mgg | E16 | G Terpinene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | guaiol_metrc | D25 | Guaiol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | guaiol_metrc_mgg | E25 | Guaiol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | isopulegol_metrc | D19 | Isopulegol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | isopulegol_metrc_mgg | E19 | Isopulegol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | linalool_metrc | D18 | Linalool METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | linalool_metrc_mgg | E18 | Linalool METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | pcymene_metrc | D13 | P Cymene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | pcymene_metrc_mgg | E13 | P Cymene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | terpinolene_metrc | D17 | Terpinolene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | terpinolene_metrc_mgg | E17 | Terpinolene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | testterpenes | E4 | Test Terpenes | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | transnerolidol_metrc | D24 | Trans Nerolidol METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | transnerolidol_metrc_mgg | E24 | Trans Nerolidol METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | transocimene_metrc | D14 | Trans Ocimene METRC | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Terpenes | Terpenes [Test] Worksheet | transocimene_metrc_mgg | E14 | Trans Ocimene METRC mg/g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | aspergillusspp | I2 | Aspergillus spp. | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | aspergillusspp_metrc | Specifications!E10 | Aspergillus Spp METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | enterobacteriaceae | F2 | Enterobacteriaceae | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | enterobacteriaceae_metrc | Specifications!E7 | Enterobacteriaceae METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | lmonocytogenes | J2 | L. monocytogenes | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | lmonocytogenes_metrc | Specifications!E11 | L Monocytogenes METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | microbials_results | Data!D2:J2 |  | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | report_result | Report!A1:F9 |  | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | salmonellaspecies | G2 | Salmonella species | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | salmonellaspecies_metrc | Specifications!E8 | Salmonella Species METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | shigatoxin_producingecoli_metrc | Specifications!E9 | Shiga Toxin-Producing E Coli METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | shigatoxinproducingecoli | H2 | Shiga toxin-producing E. coli | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | totalaerobic | D2 | Total aerobic microbial | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | totalaerobicmicrobial_metrc | Specifications!E5 | Total Aerobic Microbial METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | totalyeastandmold_metrc | Specifications!E6 | Total Yeast And Mold METRC | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Microbiology/General_Microbial_Analysis | Microbial Analysis [Test] Worksheet | yeastmold | E2 | Total yeast and mold | Unknown | Discovered/verified in 2026-07-04 rescan (new). |
| Homogeneity | Homogeneity [Test WS] | average_actual_unit_mass_g | Data!B8 | Average Actual Unit Mass g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | duplicate_cp_test_id_check | Data!B36 | Duplicate CP Test ID Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | extra_pasted_rows_check | Data!B37 | Extra Pasted Rows Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_cannabinoid_1_label_variance | Data!B28 | Cannabinoid 1 Label Variance for Highest Cannabinoid | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_cannabinoid_2_label_variance | Data!B30 | Cannabinoid 2 Label Variance for Highest Cannabinoid | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_mass_label_variance | Data!B26 | Mass Label Variance for Highest Unit Mass | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_reported_cannabinoid_1_mg_container | Data!B27 | Highest Reported Cannabinoid 1 mg/container | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_reported_cannabinoid_2_mg_container | Data!B29 | Highest Reported Cannabinoid 2 mg/container | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | highest_reported_unit_mass_g | Data!B25 | Highest Reported Unit Mass g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | homogeneity_metrc | COA!F1 | Homogeneity METRC | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_cannabinoid_1_mg_container | Data!B4 | Label Cannabinoid 1 mg/container | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_cannabinoid_1_source_status | Paste!Q4 | Label Cannabinoid 1 Source Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_cannabinoid_2_mg_container | Data!B6 | Label Cannabinoid 2 mg/container | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_cannabinoid_2_source_status | Paste!U4 | Label Cannabinoid 2 Source Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | label_unit_mass_g | Data!B7 | Label Unit Mass g | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | manual_label_cannabinoid_1_mg_container | Paste!O4 | Manual Label Cannabinoid 1 mg/container Override | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | manual_label_cannabinoid_2_mg_container | Paste!S4 | Manual Label Cannabinoid 2 mg/container Override | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | optional_target_2_label_claim_check | Data!B41 | Optional Target 2 Label Claim Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | parent_sample_match_check | Data!B38 | Parent Sample Match Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | pass_fail | Data!B31 | Pass/Fail | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | qbench_sample_label_amount_lookup | Paste!N24:P36 | QBench Sample Label Amount Lookup | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | replicate_count | Data!B34 | Replicate Rows Present | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | replicate_results | COA!A10:G20 | Homogeneity Replicate Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | report_results | COA!A1:G20 | Homogeneity COA Output | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | required_target_fields_check | Data!B40 | Required Target 1 and Label Claim Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | required_unit_mass_check | Data!B39 | Required Unit Mass Check | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | reviewer_parent_sample_confirmation | Paste!D6 | Reviewer Parent Sample Confirmation | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | target_cannabinoid_1 | Data!B3 | Target Cannabinoid 1 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | target_cannabinoid_2 | Data!B5 | Target Cannabinoid 2 | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | unique_cp_test_id_count | Data!B35 | Unique CP Test IDs Counted | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Homogeneity | Homogeneity [Test WS] | validation_status | Data!B42 | Overall Input Validation Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_limit | Specifications!C5 | Aspergillus Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_loq | Specifications!B5 | Aspergillus LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_mu | Specifications!E5 | Aspergillus MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_result | Specifications!D9 | Aspergillus Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | asp_status | Specifications!F9 | Aspergillus Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | aspergillusspp_metrc | Report!C6 | Aspergillus Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | flavus_result | Data!E3 | A. Flavus Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | fumigatus_result | Data!E4 | A. fumigatus Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_analyte_name_aspergillusspp | METRC!A5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_notes_aspergillusspp | METRC!D5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_pass_fail_aspergillusspp | METRC!C5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_quantity_aspergillusspp | METRC!B5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | metrc_to_include_aspergillusspp | METRC!E5 |  | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | niger_result | Data!E2 | A. niger (HEX) Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | report_content | Report!A2:D5 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | report_header | Report!A1:D1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | report_results | Report!A1:D5 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | sub_species | Data!F2 | Asp Sub Species | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Aspergillus | Total Aspergillus Microbial Analysis [Test WS] | terreus_result | Data!E5 | A. terreus Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_limit | Specifications!C5 | Salmonella Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_loq | Specifications!B5 | Salmonella LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_mu | Specifications!E5 | Salmonella MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_result | Specifications!D5 | Salmonella Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salm_status | Specifications!F5 | Salmonella Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Salmonella | Salmonella Species [Test] Worksheet | salmonella_results | Data!E2 | Salmonella Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_limit | Specifications!C5 | STEC Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_loq | Specifications!B5 | STEC LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_mu | Specifications!E5 | STEC MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_result | Specifications!D5 | STEC Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_results | Data!E2 | STEC Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/STEC | STEC [Test] Worksheet | stec_status | Specifications!F5 | STEC Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Listeria | Listeria Monocytogenes [Test] Worksheet | lis_results | Data!E2 | Listeria Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Listeria | Listeria Monocytogenes [Test] Worksheet | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Listeria | Listeria Monocytogenes [Test] Worksheet | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Listeria | Listeria Monocytogenes [Test] Worksheet | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_limit | Specifications!C5 | Total Aerobic Count Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_loq | Specifications!B5 | Total Aerobic Count LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_mu | Specifications!E5 | Total Aerobic Count MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_result | Specifications!D5 | Total Aerobic Count Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_results | Data!E2 | Total Aerobic Count Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | ac_status | Specifications!F5 | Total Aerobic Count Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TAMC | Total Aerobic Count [Test] WS | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_limit | Specifications!C5 | Total Yeast and Mold Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_loq | Specifications!B5 | Total Yeast and Mold LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_mu | Specifications!E5 | Total Yeast and Mold MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_result | Specifications!D5 | Total Yeast and Mold Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_results | Data!E2 | YM Automation Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/TYMC | Total Yeast and Mold {Test WS} | ym_status | Specifications!F5 | Total Yeast and Mold Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_limit | Specifications!C5 | Enterobacteriaceae Limit | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_loq | Specifications!B5 | Enterobacteriaceae LOQ | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_mu | Specifications!E5 | Enterobacteriaceae MU | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_result | Specifications!D5 | Enterobacteriaceae Result | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_results | Data!E2 | Enterobacteriaceae Results | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | eb_status | Specifications!F5 | Enterobacteriaceae Status | Unknown | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | pass_fail | Specifications!D2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | report_content | Report!A2:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | report_header | Report!A1:E1 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
| Microbiology/Enterobacteriaceae | Enterobacteriaceae [Test] WS | report_results | Report!A1:E2 |  | Yes | Discovered/verified in 2026-07-04 rescan (changed). |
