# Qualified-to-unqualified address comparison

Classification: **`qualified_to_unqualified_one_tab_compatibility_correction`**

- Previous candidate SHA-256: `54a65e029b9f1a038a21428cf40727896130db86041fafcc2d0bdf868e7fe35b`
- New candidate SHA-256: `e5ef20a5cec574dc292ed679867e01313233c92ceda9ef863bf98dd8d4485b80`
- JSON differences: `43`
- Expected named-cell address differences: `43`
- All differences limited to `qb_config.named_cells.<name>.cell`:
  `true`
- Rendered 40x26 worksheet structure and 28 anchors unchanged:
  `true`
- All new JSON cell values unqualified:
  `true`
- A2 mapping present: `false`

The CSV remains the logical, sheet-qualified mapping. The old-Sandbox runtime
JSON uses the corresponding unqualified scalar cell for this exact one-tab
legacy worksheet.

| Named cell | Logical address | Old-Sandbox JSON cell |
|---|---|---|
| `terpenes_instrument_conc_01` | `Data!D2` | `D2` |
| `terpenes_instrument_conc_02` | `Data!E2` | `E2` |
| `terpenes_instrument_conc_03` | `Data!F2` | `F2` |
| `terpenes_instrument_conc_04` | `Data!G2` | `G2` |
| `terpenes_instrument_conc_05` | `Data!H2` | `H2` |
| `terpenes_instrument_conc_06` | `Data!I2` | `I2` |
| `terpenes_instrument_conc_07` | `Data!J2` | `J2` |
| `terpenes_instrument_conc_08` | `Data!K2` | `K2` |
| `terpenes_instrument_conc_09` | `Data!L2` | `L2` |
| `terpenes_instrument_conc_10` | `Data!M2` | `M2` |
| `terpenes_instrument_conc_11` | `Data!N2` | `N2` |
| `terpenes_instrument_conc_12` | `Data!O2` | `O2` |
| `terpenes_instrument_conc_13` | `Data!P2` | `P2` |
| `terpenes_instrument_conc_14` | `Data!Q2` | `Q2` |
| `terpenes_instrument_conc_15` | `Data!R2` | `R2` |
| `terpenes_instrument_conc_16` | `Data!S2` | `S2` |
| `terpenes_instrument_conc_17` | `Data!T2` | `T2` |
| `terpenes_instrument_conc_18` | `Data!U2` | `U2` |
| `terpenes_instrument_conc_19` | `Data!V2` | `V2` |
| `terpenes_instrument_conc_20` | `Data!W2` | `W2` |
| `terpenes_instrument_conc_21` | `Data!X2` | `X2` |
| `terpenes_instrument_conc_22` | `Data!Y2` | `Y2` |
| `terpenes_instrument_conc_23` | `Data!Z2` | `Z2` |
| `sample_mass_g` | `Data!B12` | `B12` |
| `final_volume_ml` | `Data!B13` | `B13` |
| `df` | `Data!B14` | `B14` |
| `df_application_mode` | `Data!B15` | `B15` |
| `labsolutions_conc_unit` | `Data!B16` | `B16` |
| `labsolutions_conc_unit_confirmed` | `Data!B17` | `B17` |
| `preparation_values_confirmed` | `Data!B18` | `B18` |
| `source_batch_id` | `Data!B28` | `B28` |
| `source_instrument_file` | `Data!B29` | `B29` |
| `source_file_hash` | `Data!B30` | `B30` |
| `source_data_file` | `Data!B31` | `B31` |
| `source_method_file` | `Data!B32` | `B32` |
| `source_sequence_file` | `Data!B33` | `B33` |
| `parser_version` | `Data!B34` | `B34` |
| `imported_at` | `Data!B35` | `B35` |
| `instrument_name` | `Data!B36` | `B36` |
| `detector_id` | `Data!B37` | `B37` |
| `detector_name` | `Data!B38` | `B38` |
| `batch_qc_disposition` | `Data!B22` | `B22` |
| `publish_ready` | `Data!B23` | `B23` |
