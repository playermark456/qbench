# Phase 4A Sandbox import inventory

Date: 2026-07-21

## Origin and collision preflight

- Every controlled browser page used the exact origin `https://ait-sandbox.qbench.net`.
- `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS` was absent before creation.
- `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS` was absent.
- `SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE` remained present and untouched.
- `SBX_ONLY_TERPENES_2026_07_16_No_Code_Batch_Import` remained present and untouched.

No similarly named object was modified.

## Local source verification

| Source | SHA-256 result |
| --- | --- |
| `production_candidates/SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v1.json` | matched `275c8058cd597cfc688121bbdf50d1189897a088f455ff9e00e79a3fdf781a44` |
| `production_candidates/SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS__v1.json` | matched `7c96c9e8bb300f5886a4f66971c6c22c3ae72ee9225134f737d6601a0bbc55b2` |

## Sandbox objects

| Neutral reference | Intended object | State at stop |
| --- | --- | --- |
| `SANDBOX_TEST_WORKSHEET_FIXTURE` | `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS` | Inactive worksheet shell created. Exact Test candidate loaded into the unsaved editor. No version saved, approved, or activated. |
| `SANDBOX_BATCH_WORKSHEET_FIXTURE` | `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS` | Not created or imported. |

No internal QBench numeric identifier is retained in this evidence.
