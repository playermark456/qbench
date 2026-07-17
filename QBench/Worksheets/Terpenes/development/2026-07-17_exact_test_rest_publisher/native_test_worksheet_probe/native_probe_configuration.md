# Native probe configuration

## Definition

- Worksheet: `SBX_ONLY_TERPENES_2026_07_17_NATIVE_TEST_WS_PROBE`
- QBench UI type label: `Spreadsheet`
- Engine type: legacy Spreadsheet Worksheet
- Construction: manual old-Sandbox UI only
- Import, clone, reuse, or external generation: none
- Corrected saved version: `2 - Native Test Worksheet Probe v2`
- Final version state: `APPROVED (ACTIVE)`
- Saved size: 6 rows by 5 columns
- Hidden rows: none
- Pass/Fail named cells or values: none

The legacy editor/export has one `table_config` and no sheet-tab naming field.
Accordingly, the requested logical sheet name `Probe` is not represented by a
visible tab or serialized sheet-name property.

## Exact cell contract

| Cell | Saved value | Named cell | Writable | Formula-owned |
|---|---|---|---|---|
| A1 | `Native Test Worksheet Probe` | none | yes | no |
| B2 | blank | `native_probe_text` | yes | no |
| B3 | blank | `native_probe_number` | yes | no |
| B4 | `=ISNUMBER(B3)` | `native_probe_isnumber` | no | yes |
| B5 | `=COUNT(B3)` | `native_probe_count` | no | yes |
| B6 | `UNCHANGED` | `native_probe_sentinel` | no | no |

All five named cells are unique and exportable. The saved/reopened editor and
raw definition export both retain B4, B5, and B6 as read-only. Version 2 also
removes the hidden duplicate B7 formula found by the first instantiated CSV;
the final definition and Test export contain exactly rows 1 through 6.

## Raw saved/reopened definition

- Filename:
  `native_test_worksheet_probe_v2_approved_active_saved_reopened_export_spreadsheet.json`
- SHA-256:
  `a43cb9779e03d401e5b43d69df6169a1236b51e45dd805bd9aee7353109f8b24`
- Bytes: 15,203
- Raw file handling: preserved locally, byte-for-byte, and ignored by Git
