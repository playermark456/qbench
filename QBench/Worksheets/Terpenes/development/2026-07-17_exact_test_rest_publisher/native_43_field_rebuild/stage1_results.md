# Phase 1 representative native destination probe

Classification: **`native_minimal_destination_probe_failed`**

Worksheet: `SBX_ONLY_TERPENES_2026_07_17_NATIVE_43_FIELD_BASE`

Version: `1 - Native 43 Field Base v1 - DRAFT`

Saved/reopened grid: 40 rows by 26 columns, no hidden rows or columns

| Required named destination | Address | Saved and reopened |
|---|---|---|
| `terpenes_instrument_conc[1]` | `Data!D2` | No - bracketed key rejected |
| `terpenes_instrument_conc[12]` | `Data!O2` | No - bracketed key rejected |
| `terpenes_instrument_conc[23]` | `Data!Z2` | No - bracketed key rejected |
| `sample_mass_g` | `Data!B12` | Yes |
| `batch_qc_disposition` | `Data!B22` | Yes |
| `publish_ready` | `Data!B23` | Yes |
| `source_file_hash` | `Data!B30` | Yes |

The final saved/reopened Version 1 contains the four exact scalar named cells
and none of the three required indexed named cells. The four retained targets
are blank, writable, and non-formula. There are no formulas, duplicate named
cells, merged cells, hidden rows/columns, Pass/Fail fields, Dimethylacetamide
destinations, or Peak Table result destinations.

Diagnostic control: replacing the bracketed suffixes with `_1`, `_12`, and
`_23` allowed all seven otherwise-identical definitions to save and reopen.
Those non-contract diagnostic names were removed before the final save. This
control is evidence about the native editor/save path only; it does not resolve
the REST PATCH-key representation.

The saved/reopened Export Spreadsheet action was invoked, but the in-app
browser received no download and no new local export file appeared. Because
the exact contract had already failed, no alternate or fabricated raw export
was created.

The stop gate prevented approval, activation, Assay creation, Sample creation,
Test creation, manual value entry, and runtime persistence testing.
