# Key/Value Stores — 2026-08-16

The complete two-page production list contained 11 stores, correcting the Phase 1 first-page visible count of 10. Each detail page was opened by safe GET navigation. Only the Details and Store tabs were read; API Clients and History were intentionally not opened. The Store tab's **Expand all** presentation control was used, and Save/Delete were never used.

## Evidence

- `kvstore_inventory.json` and `kvstore_inventory.csv` — safe store metadata.
- One `<store UUID>.json` file per store — ordered path/value evidence.
- `kvstore_values.csv` — 13,766 ordered scalar rows across all stores.

| Store | ID | Scalar rows | Unique paths | Maximum repeated-path occurrence |
|---|---|---:|---:|---:|
| Cannabinoid Potency | 55a33596-fde6-44ed-8b21-c568e0c9b259 | 1,037 | 1,037 | 1 |
| Cannabis Heavy Metals | 1ddd77a8-1f6f-4b62-afb9-ac0c877af0bc | 432 | 432 | 1 |
| Cannabis Mycotoxin | 7085bf4a-27de-4bf1-84f7-208cf8a42127 | 609 | 609 | 1 |
| Cannabis Pesticides | 3cf5a8a3-dfee-44c4-9473-b6baa9da8c04 | 5,236 | 1,768 | 3 |
| Cannabis Residual Solvents | fb123928-53d4-4c6d-82b6-51a6d447f5da | 1,872 | 646 | 3 |
| Cannabis Water Activity | 6ff8d12b-3d6e-4d58-a952-3ed3dc0f2b2f | 72 | 24 | 3 |
| Microbial Analysis | d35d8737-5747-408a-a4e3-4a883c79349a | 504 | 168 | 3 |
| QBENCH_TO_METRC_SAMPLE_TYPE_MAPPING | ff2cde0c-abba-4522-991c-2473042479bc | 2,003 | 60 | 146 |
| Terpenes | f68f4eb5-b962-4604-85e0-fdaa72106e39 | 2,001 | 667 | 3 |
| TEST | e06679d8-cda7-461b-95d8-8637f5e59852 | 0 | 0 | 0 |
| TEST Potency | 9f287566-0fa1-4eb1-b770-283069826e09 | 0 | 0 | 0 |

Repeated paths are retained with both global `ordinal` and `path_occurrence`; they are not collapsed. Automated checks found no email, JWT, authorization, cookie, session-query, or secret-like value requiring redaction. Created-by identities were omitted.
