# Phase 4A.4B Test v3 validation report

Date: 2026-07-21

## Outcome

The existing V3 candidate passed native Sandbox file import, pre-save static rendering, the one-Draft save gate, list-based reopen, named-definition persistence, raw Export Spreadsheet capture, and semantic round-trip comparison.

Final classification: `test_v3_static_round_trip_passed_ready_for_runtime_validation`

## Results

| Gate | Result |
| --- | --- |
| V3 SHA-256 | exact: `b68f0e1589ba4e2f5c3c85196c648ed5238a1700b02d8feca3e20850ede19014` |
| Clean existing shell | inactive, zero versions, default Sheet1, Assays (0) |
| Native manual import | passed; `Submit` used once |
| Default Sheet1 removed before save | yes |
| Static render | passed |
| Dimensions | Report 23x5; Data 40x26; Specifications 23x21 |
| Embedded formulas | 309/309 |
| Writable destinations | 43/43 |
| Named definitions | 44/44 |
| `report_results` | exact: `Report!A1:E23` |
| Draft save | one version only |
| Visible Versions row | `1 - Terpenes Production Candidate Test Worksheet v3`, `DRAFT` |
| List-based reopen | passed |
| Raw export SHA-256 | `729a35c78deb03e6fa8e5032ed30e02f412d4c6854a828e57d52d4a006d87b2f` |
| Semantic round trip | passed with expected QBench normalization |
| V3 validator | renderer, calculation, and runtime-configuration contracts passed |
| Unit tests | 26/26 passed |

## Stop gate

Runtime validation was not started. The worksheet remained inactive and unapproved. No Key/Value Store association changed, and no Assay, Sample, Test, or Batch was created. No runtime vector, report preview, instrument import, publication, QC Review, Pass/Fail, or METRC activity occurred. Live QBench and all QBench APIs were not accessed. V1, V2, and V3 candidate JSON files were not modified.
