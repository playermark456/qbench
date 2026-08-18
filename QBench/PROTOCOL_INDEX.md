# Protocol Index

Last verified in production on 2026-08-16. Protocol active/inactive state was not exposed on the detail pages and is not inferred.

| ID | Protocol | Assigned steps | Explicit assay assignments from assay pages | Key gap |
|---:|---|---:|---|---|
| 2 | [Batch] Heavy Metals Protocol | 12 | Heavy Metals (3) | Digestion step 27 has no worksheet; shared final-review worksheet 41 has no version |
| 3 | [Batch] Water Activity Protocol | 7 | Water Activity (9) | Shared final-review worksheet 41 has no version |
| 4 | [Batch] Cannabinoid Potency Protocol | 24 | Cannabinoid Potency (2) | Calculation/reporting worksheet 39 is not assigned; final review worksheet 41 has no version |
| 5 | [Batch] Microbials Protocol | 0 | No configured association in captured assay fields | Empty protocol |
| 6 | [Batch] Residual Solvents Protocol | 8 | Residual Solvents (7) | Shared final-review worksheet 41 has no version |
| 7 | [Batch] Qualitative Pesticides & Mycotoxin Protocol | 9 | Pesticides (4); Mycotoxins (5) | Shared final-review worksheet 41 has no version |
| 8 | [Batch] Mycotoxin (Quantitative) Protocol | 10 | No configured association in captured assay fields | Assay detail does not assign it; shared final-review worksheet 41 has no version |
| 9 | [Batch] Terpenes Protocol | 0 | No configured association in captured assay fields | Empty and not assigned to Terpenes assay 8 |
| 10 | [Test] Foreign Material Protocol | 3 | Foreign Material (12) | Shared final-review worksheet 41 has no version |
| 11 | [Batch] Homogeneity Protocol | 4 | Homogeneity (11) | None identified at metadata layer |
| 12 | [Batch] Quantitative Pesticide in Cannabis Flower Protocol | 13 | Pesticides Quantitative Flower (21) | Step 83 worksheet 151 has draft v1 only; shared worksheet 41 has no version |
| 13 | [Batch] Gene Up Salmonella & STEC Microbial Analysis | 7 | Salmonella Species (15); STEC (16) | Shared final-review worksheet 41 has no version |
| 14 | [Batch] Gene Up Aspergillus Microbial Analysis Protocol | 8 | Aspergillus spp. (14) | Shared final-review worksheet 41 has no version |
| 15 | [Batch] Gene Up Listeria Microbial Analysis Protocol | 7 | No configured association in captured assay fields | Assay detail does not assign it; shared final-review worksheet 41 has no version |
| 16 | [Batch] Tempo Microbial Analysis Protocol | 6 | No configured association in captured assay fields | Assay detail does not assign it; shared final-review worksheet 41 has no version |

Complete ordered evidence is in `QBench/Rescans/2026-08-16/Protocols/`. The canonical index records only explicit UI relationships; semantic names are not promoted to confirmed assignments.

## Cannabinoid Potency baseline reconciliation

The prior-scan baseline worksheets 32–40 still exist as active Dynamic Spreadsheet objects. Protocol 4 assigns worksheets 32–38 and shared general worksheet 40, but does **not** assign worksheet 39.

| Worksheet | Step | Protocol 4 sequence | Active version | Complete visible version-status sequence | Assignment result |
|---:|---:|---:|---:|---|---|
| 32 | 13 | 4 | 2 | v1 Draft; v2 Approved Active | Assigned |
| 33 | 14 | 5 | 5 | v1 Draft; v2 Approved; v3 Approved; v4 Pending; v5 Approved Active | Assigned; pending v4 predates active v5 |
| 34 | 15 | 6 | 2 | v1 Draft; v2 Approved Active | Assigned |
| 35 | 16 | 7 | 6 | v1 Draft; v2 Approved; v3 Rejected; v4 Rejected; v5 Approved; v6 Approved Active | Assigned |
| 36 | 17 | 8 | 5 | v1 Draft; v2 Rejected; v3 Approved; v4 Approved; v5 Approved Active | Assigned |
| 37 | 18 | 21 | 2 | v1 Draft; v2 Approved Active | Assigned |
| 38 | 19 | 22 | 6 | v1 Draft; v2–v5 Approved; v6 Approved Active | Assigned; duplicate step 20 also points to WS38 but is unassigned |
| 39 | 21 | — | 7 | v1 Approved; v2 Rejected; v3–v6 Approved; v7 Approved Active | **Defined and active, but unassigned to every protocol** |
| 40 | 22 | 23 | 1 | v1 Approved Active | Assigned shared general step; six protocol memberships |

No visible version is newer than the displayed active version for any baseline worksheet. Required/optional state, equipment/resource/inventory assignments, fields completed, direct automation/report bindings, and version pinning versus follow-active behavior were not exposed. Current native worksheet definitions were not exported, so this is a metadata reconciliation rather than worksheet-content certification.

Protocol 4 is the most complete visible structural reference for a future Terpenes protocol: it has 24 ordered assignments spanning shared equipment/inventory instructions, solution preparation, flower/plant, concentrate, beverage, and edible preparation, dilution, instrumental measurement, quality control, upload, and final review. This is a reasoned structural comparison, not a QBench designation. It is not a complete gold standard because calculation/reporting worksheet 39 is omitted, final-review worksheet 41 has zero versions, patch steps 74–76 are unassigned, and conditional/required behavior is not exposed. Terpenes protocol 9 remains empty and unassigned to assay 8.

## Control and resource relationship boundary

The resource-group relationships in `RESOURCE_INDEX.md` are direct assay-detail assignments, not protocol assignments. No protocol-to-resource or protocol-to-control relationship was exposed in the captured protocol pages, so none is inferred from a shared assay or similar name. All captured assay-side Batch Control Group fields were null/blank. Control acceptance, reporting, automation, and frequency semantics were also unavailable.
