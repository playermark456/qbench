# Prompt 5A Sandbox change log

All mutations were limited to `ait-sandbox.qbench.net` and were preceded by a
hostname check.

## 2026-07-16 America/Chicago / 2026-07-17 UTC

1. Created the isolated Batch Worksheet and approved/activated version 1.
2. Created the isolated Test Worksheet with only `route_probe`,
   `qbench_test_id_display`, and `route_probe_sentinel`; configured the ID and
   sentinel cells read-only and the sentinel as `="UNCHANGED"`.
3. Entered three intended named-cell mappings in the worksheet editor before
   creating version 1.
4. Created one isolated assay, three synthetic Samples, and three synthetic
   Tests. The QBench Test IDs were 290, 291, and 292.
5. Verified each Test baseline: blank route probe, matching ID display, and
   `UNCHANGED` sentinel.
6. Created the isolated Batch, added only those three Tests, and assigned only
   the isolated Batch Worksheet.
7. The requested automation name was rejected for length. Created the same
   isolated automation under the accepted shortened name and retained the full
   requested name in its description.
8. Saved one worksheet condition and one worksheet action using
   `=VLOOKUP({{test.id}}, A2:B4, 2)`.
9. While the automation was inactive, staged the three exact lookup rows:
   290/101, 291/202, and 292/303.
10. Activated only the isolated automation at
    `2026-07-17T02:36:54.746Z`.
11. Saved the Batch worksheet exactly once at
    `2026-07-17T02:37:05.765Z`.
12. Started deactivation at `2026-07-17T02:37:17.695Z` and confirmed the final
    automation state was inactive.
13. Reopened all three Tests. Every route probe remained blank; the exact Test
    ID displays and `UNCHANGED` sentinels persisted.
14. Confirmed exactly one task-created Automation History entry with status
    `Success`.
15. Downloaded exact **Export Spreadsheet** files for both probe worksheet
    versions. The Test export showed the named cells had not persisted.
16. Classified the run `per_test_vlookup_error`. No retry and no secondary
    guard probe was performed.

No pre-existing Sandbox Terpenes object was modified. No customer data was
used. No production page was accessed.
