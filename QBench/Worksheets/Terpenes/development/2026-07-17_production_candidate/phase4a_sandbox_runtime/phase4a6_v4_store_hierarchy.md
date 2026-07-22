# Phase 4A.6 isolated V4 Key/Value Store

Date: 2026-07-21

- Name: `SBX_ONLY_TERPENES_RUNTIME_KV_V4`
- Environment: authenticated QBench Sandbox visual browser only
- Collision check: no exact-name store existed
- Save/reopen: passed
- Binding evidence: SHA-256 `9f6c5235ab754f947e56fa883d6786b25dfa697c644df8e918cf917460c84b9e`; the full visible binding is retained only in ignored local runtime configuration and the candidate that requires it

The complete hierarchy is `Terpenes -> Cannabis Concentrates -> analyte or component channel -> field/value`.

- Analyte/component keys: 25
- Reportable-analyte LOQ entries: 21, each numeric `10` ug/g
- Direct-analyte MU entries: 19; Alpha-Pinene `5`, Camphene `6`, Beta-Myrcene `7`, Beta-Pinene `8`, and the remaining direct analytes `9`
- Ocimene: reportable LOQ `10`; component MUs `Ocimene 1 = 4`, `Ocimene 2 = 8`
- Nerolidol: reportable LOQ `10`; component MUs `Nerolidol 1 = 7`, `Nerolidol 2 = 11`
- Total MU entries: 23
- Component-channel LOQ entries: 0
- Unit hierarchy levels: 0
- `MU%` terminal fields: 0
- Pass/Fail keys: 0

The V2 store and every V1-V3 object were left unchanged.

After the V4 Dynamic Spreadsheet passed static and round-trip validation, this store alone was associated with `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS_V4_DYNAMIC`. The association persisted after navigating away and reopening the worksheet. It was not associated with the regular Spreadsheet negative control.
