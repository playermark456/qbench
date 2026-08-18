# Assay ID Map

Last verified against the Adams Independent Testing production tenant on 2026-08-16. All 20 visible assays were active. Codes below omit the visual trailing `|` separator shown by the list UI.

| QBench ID | Assay | Code | Method reference | Test worksheet | Batch worksheet | Explicit protocol assignment |
|---:|---|---|---|---|---|---|
| 2 | Cannabinoid Potency | CP | MTH-CP-01 | 8 | 7 | Batch protocol 4 |
| 3 | Heavy Metals | HM | MTH-HM-01 | 6 | 5 | Batch protocol 2 |
| 4 | Pesticides | PE | MTH-PM-01; MTH-PE-01 | 14 | 15 | Batch protocol 7 |
| 5 | Mycotoxins | MY | MTH-PM-01; MTH-MY-01 | 10 | 15 | Batch protocol 7 |
| 6 | Microbial Analysis | MICRO | MTH-MICRO-GU-01; MTH-MICRO-TE-01 | 44 | 45 | No protocol configured in captured assay fields |
| 7 | Residual Solvents | RS | MTH-RS-01 | 12 | 11 | Batch protocol 6 |
| 8 | Terpenes | TR | Not displayed | 42 | 43 | No protocol configured in captured assay fields; protocol 9 exists but has zero assigned steps |
| 9 | Water Activity | WA | MTH-WA-01 | 28 | 29 | Batch protocol 3 |
| 10 | Moisture Analysis | MO | Not displayed | None | None | No protocol configured in captured assay fields |
| 11 | Homogeneity | HOM | Not displayed | 73 | 7 | Batch protocol 11 |
| 12 | Foreign Material | FM | MTH-FM-01 | 31 | None | Test protocol 10 |
| 13 | Stability | STAB | Not displayed | None | None | No protocol configured in captured assay fields |
| 14 | Aspergillus spp. | MI-ASP | MTH-MICRO-ASP-01 | 81 | 80 | Batch protocol 14 |
| 15 | Salmonella Species | MI-SLM | MTH-MICRO-SLM-01 | 83 | 82 | Batch protocol 13 |
| 16 | Shiga toxin-producing E. coli | MI-STEC | MTH-MICRO-STCSLM-01 | 84 | 82 | Batch protocol 13 |
| 17 | Listeria Monocytogenes | MI-LIS | MTH-MICRO-LIS-01 | 87 | 86 | No protocol configured in captured assay fields |
| 18 | Total Aerobic Microbial | MI-AE | MTH-MICRO-AE-01 | 93 | 89 | No protocol configured in captured assay fields |
| 19 | Total Yeast and Mold | MI-YM | MTH-MICRO-YM-01 | 94 | 94 | No protocol configured in captured assay fields |
| 20 | Enterobacteriaceae | MI-EB | MTH-MICRO-EN-01 | 95 | 89 | No protocol configured in captured assay fields |
| 21 | Pesticides Quantitative Flower | PEqf | MTH-PM-02 | 16 | 13 | Batch protocol 12 |

## Direct control and resource assignments

Phase 5 reconciled these direct resource-group references from the Phase 3 assay detail capture:

| Assay ID | Assay | Resource group | Assignment level |
|---:|---|---|---|
| 2 | Cannabinoid Potency | 8 — Cannabinoid Potency Analysis | Batch |
| 3 | Heavy Metals | 5 — Heavy Metals Analysis | Batch |
| 4 | Pesticides | 9 — Pest Myco (Qualitative) Analysis | Batch |
| 5 | Mycotoxins | 9 — Pest Myco (Qualitative) Analysis | Batch |
| 7 | Residual Solvents | 7 — Residual Solvents Analysis | Batch |
| 9 | Water Activity | 3 — Water Activity Analysis | Batch |
| 11 | Homogeneity | 8 — Cannabinoid Potency Analysis | Batch |
| 12 | Foreign Material | 4 — Foreign Material Analysis | Test |
| 21 | Pesticides Quantitative Flower | 12 — Pest (Quantitative) Analysis | Batch |

No direct Batch or Test resource group was exposed for assay IDs 6, 8, 10, or 13–20. In particular, Terpenes assay 8 had no resource-group assignment. Every captured assay-side **Batch Control Group** field was null/blank. These are direct UI relationships only; absence does not prove that no indirect protocol, automation, parser, report, control, inventory, or equipment dependency exists. See `RESOURCE_INDEX.md` and `CONTROL_INDEX.md`.

The dated source evidence is in `QBench/Rescans/2026-08-16/Assays/assay_inventory.json`. Assay-side panel arrays were empty during capture; the authoritative current panel memberships come from the nine panel detail pages and their 88 rows in `Panels/panel_assay_relationships.csv`.

## Cross-family dependency reconciliation

This table joins direct assay metadata to the separately captured parser, automation, report, control, and resource evidence. `T` and `B` denote assay-level Test and Batch worksheets. A parser/automation/report entry is a downstream configuration relationship, not proof that the path was executed during this read-only scan. Protocol-step worksheet sets are normalized in `QBench/Rescans/2026-08-16/protocol_relationship_map.md`.

| ID / assay | Method | Protocol | Worksheets | Parser | Automations | Report | Controls | Resources | External mappings |
|---|---|---|---|---|---|---|---|---|---|
| 2 Cannabinoid Potency | MTH-CP-01 | Batch 4 | T8; B7; assigned protocol-step WS 26, 27, 32–38, 40, 41, 132–139, 143, 145–148; WS39/140–142 are defined but unassigned | 46 active | 11 active; 16 is a downstream Homogeneity pull | 26; 44 also reads Potency values | None directly exposed | RG8, Batch | Not exposed |
| 3 Heavy Metals | MTH-HM-01 | Batch 2 | T6; B5; 12 ordered protocol steps, including one step with no worksheet | 41 active; 22/25 inactive | 1 active; 2 inactive | 26 | None directly exposed | RG5, Batch | Not exposed |
| 4 Pesticides | MTH-PM-01; MTH-PE-01 | Batch 7 | T14; shared B15; 9 ordered protocol-step worksheets | 47 active | 8 active | 26 | None directly exposed | RG9, Batch | Not exposed |
| 5 Mycotoxins | MTH-PM-01; MTH-MY-01 | Batch 7 | T10; shared B15; 9 ordered protocol-step worksheets | 47 is only an indirect shared-B15 candidate; no direct parser setting | 8 active on B15; 3 active watches the separate, assay-unassigned quantitative B9 path | 26 | None directly exposed | RG9, Batch | Not exposed |
| 6 Microbial Analysis | MTH-MICRO-GU-01; MTH-MICRO-TE-01 | None configured | T44; B45 | None directly configured | None directly configured | 26 contains only a `-1` general-microbial placeholder, not assay 6 routing | None directly exposed | None directly exposed | Not exposed |
| 7 Residual Solvents | MTH-RS-01 | Batch 6 | T12; B11; 8 ordered protocol-step worksheets | None directly configured | 6 active | 26 | None directly exposed | RG7, Batch | Not exposed |
| 8 Terpenes | Not displayed | None configured; protocol 9 is empty/unassigned | T42; B43 | 50 active | 17 active | 26 | None directly exposed | None directly exposed | Not exposed |
| 9 Water Activity | MTH-WA-01 | Batch 3 | T28; B29; 7 ordered protocol-step worksheets | None directly configured | 4 active; 5/15 inactive | 26 summary route | None directly exposed | RG3, Batch | Not exposed |
| 10 Moisture Analysis | Not displayed | None configured | None | None directly configured | None directly configured | None routed | None directly exposed | None directly exposed | Not exposed |
| 11 Homogeneity | Not displayed | Batch 11 | T73; shared Potency B7; protocol-step WS69–72 | None directly configured | 16 active; Potency automation 11 is only a reasoned upstream candidate | 26 and 44 | None directly exposed | RG8, Batch | Not exposed |
| 12 Foreign Material | MTH-FM-01 | Test 10 | T31; no B worksheet; 3 ordered protocol-step worksheets | None directly configured | None directly configured | 26 | None directly exposed | RG4, Test | Not exposed |
| 13 Stability | Not displayed | None configured | None | None directly configured | No scheduled/date-driven automation exposed | None routed | None directly exposed | None directly exposed | Not exposed |
| 14 Aspergillus spp. | MTH-MICRO-ASP-01 | Batch 14 | T81; B80; 8 ordered protocol-step worksheets | None directly configured | 9 active | 26 | None directly exposed | None directly exposed | Not exposed |
| 15 Salmonella Species | MTH-MICRO-SLM-01 | Batch 13 | T83; shared B82; 7 ordered protocol-step worksheets | None directly configured | 12 active | 26 | None directly exposed | None directly exposed | Not exposed |
| 16 Shiga toxin-producing E. coli | MTH-MICRO-STCSLM-01 | Batch 13 | T84; shared B82; 7 ordered protocol-step worksheets | None directly configured | 12 active | 26 | None directly exposed | None directly exposed | Not exposed |
| 17 Listeria Monocytogenes | MTH-MICRO-LIS-01 | None configured; protocol 15 is semantic-only/unassigned | T87; B86 | None directly configured | 13 active | 26 | None directly exposed | None directly exposed | Not exposed |
| 18 Total Aerobic Microbial | MTH-MICRO-AE-01 | None configured; protocol 16 is semantic-only/unassigned | T93; shared B89 | None directly configured | 14 active | 26 | None directly exposed | None directly exposed | Not exposed |
| 19 Total Yeast and Mold | MTH-MICRO-YM-01 | None configured | T94; assay metadata also sets B94 | None directly configured | 14 watches B89, not the assay-configured B94; relationship unresolved | 26 | None directly exposed | None directly exposed | Not exposed |
| 20 Enterobacteriaceae | MTH-MICRO-EN-01 | None configured | T95; shared B89 | None directly configured | 14 active | 26 | None directly exposed | None directly exposed | Not exposed |
| 21 Pesticides Quantitative Flower | MTH-PM-02 | Batch 12 | T16; B13; 13 ordered protocol-step worksheets | None directly configured | 10 active; destination-name compatibility remains unverified | Absent from report 26 routing | None directly exposed | RG12, Batch | Not exposed |

All report edges above are source-observed routes. All 20 captured assay-side Batch Control Group fields were null/blank. No assay-level external mapping control was exposed; historical METRC KV or report references are not promoted to current assay assignments. Current worksheet-internal compatibility remains blocked because Phase 2 obtained zero native Export Spreadsheet files.
