# Resource Group Index

Last verified in the Adams Independent Testing production tenant on 2026-08-16. Ten resource groups were visible. Counts below are direct membership counts from the resource-group detail tabs; active/inactive state was not exposed and is not inferred.

Row-level evidence is in `QBench/Rescans/2026-08-16/Resource_Groups/`.

| ID | Resource group | Inventory items | Equipment | Auto-use equipment | Direct assay assignment exposed |
|---:|---|---:|---:|---|---|
| 3 | Water Activity Analysis | 4 | 1 | `true` | Water Activity (9), Batch |
| 4 | Foreign Material Analysis | 0 | 3 | `false` | Foreign Material (12), Test |
| 5 | Heavy Metals Analysis | 22 | 16 | `false` | Heavy Metals (3), Batch |
| 6 | Mycotoxin Analysis | 12 | 20 | `false` | None |
| 7 | Residual Solvents Analysis | 6 | 15 | `false` | Residual Solvents (7), Batch |
| 8 | Cannabinoid Potency Analysis | 16 | 29 | `false` | Cannabinoid Potency (2), Batch; Homogeneity (11), Batch |
| 9 | Pest Myco (Qualitative) Analysis | 19 | 14 | `false` | Pesticides (4), Batch; Mycotoxins (5), Batch |
| 10 | Gene Up Microbial Analysis | 18 | 20 | `false` | None |
| 11 | Tempo Microbial Analysis | 8 | 19 | `false` | None |
| 12 | Pest (Quantitative) Analysis | 0 | 0 | Not exposed | Pesticides Quantitative Flower (21), Batch |

The direct-assignment column is reconciled to the assay detail fields captured in Phase 3. It does not infer a relationship from similar names, protocols, equipment, inventory, parsers, automations, or reports. Resource groups 6, 10, and 11 had no direct assay assignment exposed. Terpenes assay 8 had no Batch or Test resource-group assignment, and no Terpenes-named resource group was visible.

## Verification boundary

The canonical index records membership counts and direct assay references only. It does not establish sufficiency, availability, calibration state, lot state, exact location, or operational usage. Protocol-to-resource, control-to-resource, parser, automation, report, and frequency semantics were not exposed. Phase 5 later stopped at the defined sensitive-data condition described in `SYSTEM_MAP.md`; categories after that boundary remain partial. No resource-group, inventory, or equipment configuration was changed.
