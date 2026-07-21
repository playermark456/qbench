# Phase 4A.5 validation report

Date: 2026-07-21

`environment_profile = sandbox_runtime_only`

## Outcome

Final classification: `test_v3_runtime_blocked_required_kv_lookup_blank`

V3 passed local/static preflight, direct approval and activation, additive isolated fixture association, Assay persistence, Sample creation, one-Test instantiation, workbook identity, and runtime placeholder resolution. The workflow stopped before analytical entry because Alpha-Pinene LOQ and MU were blank both before and after the permitted Tests-list reopen.

## Results

| Gate | Result |
| --- | --- |
| V3 SHA-256 | `b68f0e1589ba4e2f5c3c85196c648ed5238a1700b02d8feca3e20850ede19014` |
| V3 validator | renderer, calculation, and runtime-configuration contracts passed; 309 formulas; 44 KV calls; 43 destinations; 44 named definitions |
| Saved-definition semantic comparator | `passed_with_expected_qbench_normalization` |
| Production-candidate tests | 29/29 passed |
| Sanitized secret/internal-ID scans | clear |
| Version state | Version 1 APPROVED and active; worksheet object active |
| Review lock | not used |
| Runtime matrix | `Cannabis Concentrates` |
| Additional isolated fixture branch | required and saved; original branch preserved |
| V3 KV association | additive and persisted |
| V2 KV association | preserved |
| Isolated Assay | created; V3 persisted; no Batch Worksheet or specification |
| Isolated Sample | created with `Cannabis Concentrates` |
| Fresh Test | exactly one; V3 three-tab workbook; `NOT STARTED` |
| Placeholder/config resolution | passed |
| Alpha-Pinene LOQ / MU | blank / blank; expected 10 / 5 |
| Vector entry | 0/43 by hard stop |
| Runtime save/reopen proof | list reopen performed; no analytical save |
| Runtime export | not created |
| Pass/Fail | absent |
| Publish, release, completion, QC Review, METRC | none |
| Live QBench or QBench API | not accessed |

Passing local structure and placeholder resolution does not establish a production Key/Value binding or production matrix-alias mapping. Runtime calculation, type, persistence, total, and report-result proof remain pending resolution of the lookup blocker.
