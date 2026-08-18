# Key/Value Store Dependency Analysis — 2026-08-16

## Scope and evidence boundary

The production read-only capture contains 11 Key/Value Stores and 13,766 ordered leaf values. The inventory JSON, inventory CSV, 11 per-store JSON files, and flattened values CSV reconcile exactly.

Current dependency assignments cannot be confirmed from current worksheet definitions: Phase 2 completed 0 of 161 required native **Export Spreadsheet** downloads. The dependency links below are therefore historical candidates derived from tracked native worksheet exports, chiefly the 2026-07-04 snapshot. They are not assertions about the content of the active 2026-08-16 worksheet versions.

Terpenes is counted in the inventory but excluded from this historical dependency analysis so that unrelated, uncommitted Terpenes development files remain outside the scan evidence review.

## Current production inventory

| Store | Store ID | Leaf rows | Unique paths | Rows on repeated paths | Maximum path occurrence |
|---|---|---:|---:|---:|---:|
| Cannabinoid Potency | `55a33596-fde6-44ed-8b21-c568e0c9b259` | 1,037 | 1,037 | 0 | 1 |
| Cannabis Heavy Metals | `1ddd77a8-1f6f-4b62-afb9-ac0c877af0bc` | 432 | 432 | 0 | 1 |
| Cannabis Mycotoxin | `7085bf4a-27de-4bf1-84f7-208cf8a42127` | 609 | 609 | 0 | 1 |
| Cannabis Pesticides | `3cf5a8a3-dfee-44c4-9473-b6baa9da8c04` | 5,236 | 1,768 | 5,202 | 3 |
| Cannabis Residual Solvents | `fb123928-53d4-4c6d-82b6-51a6d447f5da` | 1,872 | 646 | 1,839 | 3 |
| Cannabis Water Activity | `6ff8d12b-3d6e-4d58-a952-3ed3dc0f2b2f` | 72 | 24 | 72 | 3 |
| Microbial Analysis | `d35d8737-5747-408a-a4e3-4a883c79349a` | 504 | 168 | 504 | 3 |
| QBENCH_TO_METRC_SAMPLE_TYPE_MAPPING | `ff2cde0c-abba-4522-991c-2473042479bc` | 2,003 | 60 | 1,999 | 146 |
| Terpenes | `f68f4eb5-b962-4604-85e0-fdaa72106e39` | 2,001 | 667 | 2,001 | 3 |
| TEST | `e06679d8-cda7-461b-95d8-8637f5e59852` | 0 | 0 | 0 | 0 |
| TEST Potency | `9f287566-0fa1-4eb1-b770-283069826e09` | 0 | 0 | 0 | 0 |

Repeated paths are preserved with occurrence and ordinal fields. They represent ordered multi-field or array positions in the captured view; this evidence does not establish corruption or duplication. Across all stores there are 5,411 unique paths and a maximum occurrence of 146.

## Historical worksheet dependencies

Tracked native worksheet evidence contains literal `GET_KVSTORE_VALUE` formulas for seven analytical stores and `qb_config.kvstore_config` entries for those seven stores plus the METRC mapping store. No unknown or deleted literal store ID was found. The two empty TEST stores have no tracked worksheet dependency.

| Store | Historical direct dependency candidates | Evidence character |
|---|---|---|
| Cannabinoid Potency | Test worksheet 8 | Formula and embedded configuration |
| Cannabis Heavy Metals | Test worksheet 6; batch worksheet 5 | Test formula/config; batch config only |
| Cannabis Mycotoxin | Test worksheet 10 | Formula and embedded configuration |
| Cannabis Pesticides | Qualitative test worksheet 14; quantitative test worksheet 16 | Formula and embedded configuration |
| Cannabis Residual Solvents | Test worksheet 12 | Formula and embedded configuration |
| Cannabis Water Activity | Test worksheet 28 | Formula and embedded configuration |
| Microbial Analysis | Test worksheets 44, 81, 83, 84, 87, 93, and 94; Enterobacteriaceae worksheet 95; Aspergillus batch worksheet 80 | Direct formulas where present; otherwise embedded configuration |
| QBENCH_TO_METRC_SAMPLE_TYPE_MAPPING | Worksheets 28 and 81; config-only candidates 8, 14, 67, and 73 | Dynamic formula/config for 28 and 81; configuration-only for the others |

General Microbial Analysis worksheet 44 is a special reactivation risk in the historical evidence: formulas call the Microbial Analysis store while its embedded `kvstore_config` is empty. It also uses the legacy attribute spellings `mu` and `Limit of Quantification`, whereas the current store exposes `MU` and `LOQ`.

## Current assignment-surface reconciliation

The following table prevents historical worksheet evidence from being mistaken for a current QBench assignment. It is based only on the sanitized production capture.

| Dependency surface | Current 2026-08-16 result | Evidence boundary |
|---|---|---|
| KV-store detail pages | Store identity and ordered values captured; referencing Fields, Worksheets, Assays, Panels, and Protocols were not exposed | Directly observed metadata |
| Field definitions | 277 definitions captured; option sources and KV-store links were not exposed without Edit | Directly observed metadata |
| Assay definitions | Current assay metadata captured; no KV-store-assignment control or reference was exposed | Directly observed metadata |
| Panel definitions | Nine panels and 88 assay-membership rows captured; default-field, worksheet, and KV-store behavior was not exposed | Directly observed metadata |
| Protocol definitions | Fifteen protocols and 118 ordered step assignments captured; no protocol-to-KV-store assignment was exposed | Directly observed metadata |
| Program behavior | No safe current program-to-KV-store assignment surface was captured | Unable to verify read-only |
| Current worksheet definitions | All 161 required native exports were blocked; current formula/config links cannot be certified | Blocked export evidence |
| July worksheet exports | Formula and embedded-config links listed above | Historical repository evidence only |

Accordingly, the scan establishes current store contents and historical dependency candidates, but **zero current Field, Assay, Panel, Protocol, or worksheet assignment edges**. Similar names do not create a confirmed relationship.

The current Terpenes store remains fully counted in the inventory (2,001 leaf rows), but no direct current dependency assignment was exposed. It is not compared to development-candidate worksheet files in this production dependency analysis; the current worksheet definitions were not exported, and the separate Terpenes SOP/form crosswalk owns requirements interpretation.

## Current values versus July embedded snapshots

The following counts compare unique paths in the current stores with the latest usable July embedded `kvstore_config` evidence. “Absent” means a current path was not present in that July snapshot; “changed” means the path was shared but the ordered value differed.

| Historical worksheet/config | Exact shared paths | Current paths absent from July | Shared paths changed |
|---|---:|---:|---:|
| Potency worksheet 8 | 702 | 335 | 0 |
| Heavy Metals worksheets 5/6 | 192 | 240 | 0 |
| Mycotoxin worksheet 10 | 198 | 411 | 0 |
| Pesticides qualitative worksheet 14 | 742 | 1,026 | 0 |
| Pesticides quantitative worksheet 16 | 720 | 1,037 | 11 |
| Residual Solvents worksheet 12 | 476 | 170 | 0 |
| Water Activity worksheet 28 | 24 | 0 | 0 |
| Aspergillus worksheet 81 microbial config | 104 | 56 | 8 |
| Other microbial test/batch configs | 97 | 63 | 8 |
| METRC mapping | 60 | 0 | 0 |

The 11 Pesticides quantitative differences change the analyte key `AbamectinB1a` to `Abamectin` across 11 program/matrix branches. The eight microbial differences change four pathogen limits in each of two HDCP matrices—Non-Liquid Edibles and Topical—from `Not detected in 10 g` to `Not detected in 25 g`.

The July-to-current matrix structure also expanded or renamed materially. Examples include splitting resin and rosin categories into edible and inhalation branches, replacing broader National Hemp categories with current cannabis/hemp matrix labels, and adding National Hemp branches absent from the July Mycotoxin and Pesticides configurations. Historical formulas use the sample product-matrix value as a lookup path segment, so a worksheet retaining obsolete embedded labels could return blank/error lookups or obsolete limits.

## Version-currentness limitation

Phase 2 metadata shows newer “KV Update” versions for multiple affected worksheets. However, Mycotoxin KV Update v27 is approved but non-active while v26 remains active, and Residual Solvents KV Update v37 is non-active while v41 remains active. Without the current native exports, the scan cannot establish whether any KV change was carried forward into the actual active definitions.

Current active worksheet exports must therefore be obtained and checked for current matrix labels, attribute keys, and limits before any stale-value remediation is considered verified. No QBench remediation was attempted.
