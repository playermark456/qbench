# Prompt 4.6C No-Code parser configuration

The isolated Sandbox parser is `SBX_ONLY_TERPENES_2026_07_16_No_Code_Wide_Import`.
It is a Standard/No-Code parser configured for tab-separated files, a Batch
Worksheet destination, and the Batch attachment trigger. It has no assay
assignment. The exact filename rule is **Should Equal**
`SBX_ONLY_TERPENES_WIDE_IMPORT_01.txt`.

`Patch Worksheet Data` is disabled. The workflow does not call or depend on
`updateWorksheet` or `patchWorksheet`.

## Accepted finder structure

| Finder | Source range | Target sheet | Import mode | Target start | Transpose | Repeat |
| --- | --- | --- | --- | --- | --- | --- |
| `SBX_ONLY_TERPENES_2026_07_16_A_AE` | `A2:AE2` | `Instrument Import` | Target Start Cell | `A2` | No | No |
| `SBX_ONLY_TERPENES_2026_07_16_AH_BE` | `AH2:BE2` | `Instrument Import` | Target Start Cell | `AH2` | No | No |

The two ranges are non-overlapping and intentionally omit worksheet-owned
formula columns AF and AG. A single No-Code parser accepted both finders, so a
two-parser fallback was not needed.

The machine-readable sanitized configuration is in
`sanitized_no_code_parser_configuration.json`. Neither file contains internal
Sandbox object IDs.
