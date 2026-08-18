# Key/Value Store Index

Last verified in production on 2026-08-16. The full two-page list contains 11 stores and 13,766 ordered scalar rows.

| Store | QBench store ID | Scalar rows | Status / note |
|---|---|---:|---|
| Cannabinoid Potency | 55a33596-fde6-44ed-8b21-c568e0c9b259 | 1,037 | Current values captured |
| Cannabis Heavy Metals | 1ddd77a8-1f6f-4b62-afb9-ac0c877af0bc | 432 | Current values captured |
| Cannabis Mycotoxin | 7085bf4a-27de-4bf1-84f7-208cf8a42127 | 609 | Current values captured |
| Cannabis Pesticides | 3cf5a8a3-dfee-44c4-9473-b6baa9da8c04 | 5,236 | Repeated paths preserved in order |
| Cannabis Residual Solvents | fb123928-53d4-4c6d-82b6-51a6d447f5da | 1,872 | Repeated paths preserved in order |
| Cannabis Water Activity | 6ff8d12b-3d6e-4d58-a952-3ed3dc0f2b2f | 72 | Repeated paths preserved in order |
| Microbial Analysis | d35d8737-5747-408a-a4e3-4a883c79349a | 504 | Repeated paths preserved in order |
| QBENCH_TO_METRC_SAMPLE_TYPE_MAPPING | ff2cde0c-abba-4522-991c-2473042479bc | 2,003 | 60 unique paths; ordered repeats retained |
| Terpenes | f68f4eb5-b962-4604-85e0-fdaa72106e39 | 2,001 | Created 2026-07-27; current values captured |
| TEST | e06679d8-cda7-461b-95d8-8637f5e59852 | 0 | Empty store |
| TEST Potency | 9f287566-0fa1-4eb1-b770-283069826e09 | 0 | Empty store |

Active/inactive state and a distinct system name were not exposed. Created-by identities, API Clients, and History were intentionally omitted. See `QBench/Rescans/2026-08-16/Key_Value_Stores/` and `QBench/Rescans/2026-08-16/kvstore_dependency_analysis.md` for evidence and dependency analysis.
