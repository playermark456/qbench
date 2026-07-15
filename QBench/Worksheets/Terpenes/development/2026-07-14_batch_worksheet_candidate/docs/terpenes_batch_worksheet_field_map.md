# Terpenes Batch Worksheet field map

Date: 2026-07-14

## Run Setup named cells

| Named cell | Cell | Default |
|---|---:|---|
| `batch_qbench_id` | `Run Setup!B2` | blank |
| `analytical_batch_id` | `Run Setup!B3` | blank |
| `batch_assay_name` | `Run Setup!B4` | `Terpenes` |
| `run_instrument_name` | `Run Setup!B5` | blank |
| `run_detector_id` | `Run Setup!B6` | blank |
| `run_detector_name` | `Run Setup!B7` | blank |
| `run_method_file` | `Run Setup!B8` | blank |
| `run_sequence_file` | `Run Setup!B9` | blank |
| `run_column` | `Run Setup!B10` | blank |
| `run_carrier_gas` | `Run Setup!B11` | blank |
| `run_analyst` | `Run Setup!B12` | blank |
| `run_start` | `Run Setup!B13` | blank |
| `run_end` | `Run Setup!B14` | blank |
| `calibration_id` | `Run Setup!B15` | blank |
| `standard_lot` | `Run Setup!B16` | blank |
| `extraction_solvent_lot` | `Run Setup!B17` | blank |
| `parser_version` | `Run Setup!B18` | blank |
| `source_package_version` | `Run Setup!B19` | `2026-07-14_config_parser_foundation` |
| `raw_ascii_attachment_reference` | `Run Setup!B20` | blank |
| `raw_batch_manifest_hash` | `Run Setup!B21` | blank |
| `run_setup_reviewed_by` | `Run Setup!B22` | blank |
| `run_setup_reviewed_at` | `Run Setup!B23` | blank |
| `run_setup_complete` | `Run Setup!B24` | formula |
| `run_setup_message` | `Run Setup!B25` | formula |

Required Run Setup fields are `batch_qbench_id`, `analytical_batch_id`, `batch_assay_name`, `run_instrument_name`, `run_detector_id`, `run_detector_name`, `run_method_file`, `run_sequence_file`, `run_analyst`, `run_start`, `run_end`, `parser_version`, `raw_ascii_attachment_reference`, `raw_batch_manifest_hash`, `run_setup_reviewed_by`, and `run_setup_reviewed_at`.

Optional Run Setup fields are `run_column`, `run_carrier_gas`, `calibration_id`, `standard_lot`, `extraction_solvent_lot`, and `source_package_version`.

## Instrument Import ranges

| Named range | Range | Purpose |
|---|---|---|
| `terpenes_batch_import_table` | `Instrument Import!A1:BE201` | Full normalized import table |
| `terpenes_batch_import_test_ids` | `Instrument Import!E2:E201` | Imported QBench Test IDs |
| `terpenes_batch_import_analytes` | `Instrument Import!AH2:BD201` | 23 Compound Results `Conc.` channels |
| `terpenes_batch_import_dimethylacetamide` | `Instrument Import!AA2:AA201` | Audit-only Dimethylacetamide |
| `terpenes_batch_import_validation_status` | `Instrument Import!AF2:AF201` | Valid, Review Required, or Rejected |
| `terpenes_batch_integration_review_status` | `Instrument Import!AE2:AE201` | Not Reviewed, Reviewed, or Review Required |

## QC Review named cells

| Named cell | Cell/range | Default |
|---|---:|---|
| `qc_config_version` | `QC Review!B2` | `2026-07-14-prompt4` |
| `bracketing_ccv_criterion_status` | `QC Review!B3` | `decision_required` |
| `bracketing_ccv_accuracy_percent_window` | `QC Review!B4` | blank |
| `lcs_requirement_status` | `QC Review!B5` | `decision_required` |
| `lcs_requirement_controlled_source` | `QC Review!B6` | blank |
| `lcs_requirement_reviewed_by` | `QC Review!B7` | blank |
| `qc_configuration_complete` | `QC Review!B8` | formula false by default |
| `integration_review_complete` | `QC Review!B9` | formula false by default |
| `qc_data_complete` | `QC Review!B10` | formula false by default |
| `qc_review_complete` | `QC Review!B11` | formula false by default |
| `all_publish_rows_valid` | `QC Review!B12` | formula false by default |
| `duplicate_test_id_count` | `QC Review!B13` | formula |
| `populated_publish_row_count` | `QC Review!B14` | formula |
| `batch_qc_disposition` | `QC Review!B15` | `Hold` |
| `batch_qc_reviewer` | `QC Review!B16` | blank |
| `batch_qc_reviewed_at` | `QC Review!B17` | blank |
| `batch_publish_ready` | `QC Review!B18` | formula false by default |
| `batch_publish_message` | `QC Review!B19` | formula |
| `terpenes_batch_qc_table` | `QC Review!A22:X45` | 23-analyte QC table |

## Publish named ranges

| Named range | Range |
|---|---|
| `terpenes_batch_publish_table` | `Publish!A1:BD87` |
| `terpenes_batch_publish_sample_ids` | `Publish!B2:B87` |
| `terpenes_batch_publish_test_ids` | `Publish!A2:A87` |
| `terpenes_batch_publish_product_matrices` | `Publish!C2:C87` |
| `terpenes_batch_publish_instrument_conc` | `Publish!D2:Z87` |
| `terpenes_batch_publish_sample_mass_g` | `Publish!AA2:AA87` |
| `terpenes_batch_publish_final_volume_ml` | `Publish!AB2:AB87` |
| `terpenes_batch_publish_df` | `Publish!AC2:AC87` |
| `terpenes_batch_publish_df_application_mode` | `Publish!AD2:AD87` |
| `terpenes_batch_publish_conc_unit` | `Publish!AE2:AE87` |
| `terpenes_batch_publish_unit_confirmed` | `Publish!AF2:AF87` |
| `terpenes_batch_publish_preparation_confirmed` | `Publish!AG2:AG87` |
| `terpenes_batch_publish_source_batch_ids` | `Publish!AH2:AH87` |
| `terpenes_batch_publish_source_files` | `Publish!AI2:AI87` |
| `terpenes_batch_publish_source_hashes` | `Publish!AJ2:AJ87` |
| `terpenes_batch_publish_batch_disposition` | `Publish!AY2:AY87` |
| `terpenes_batch_publish_ready` | `Publish!BC2:BC87` |
| `terpenes_batch_publish_messages` | `Publish!BD2:BD87` |

## Publish column map

| Range | Purpose | Writable |
|---|---|---|
| `Publish!A2:A87` | QBench Test ID placeholders from active source | No |
| `Publish!B2:B87` | QBench Sample ID placeholders | No |
| `Publish!C2:C87` | Product Matrix placeholders from active source | No |
| `Publish!D2:Z87` | 23 raw instrument concentration channels | Yes |
| `Publish!AA2:AX87` | Sample prep, source traceability, audit, and import status fields | Yes |
| `Publish!AY2:BD87` | Batch disposition, row gates, Publish Ready, and first message formulas | No |

## Controlled Publish column-contract decision

Publish column A is intentionally `QBench Test ID`, and Publish column B is intentionally `QBench Sample ID`. This is a controlled deviation from the original draft Prompt 4 column list because QBench Test ID is the Prompt 5 join key and the active source Test ID placeholder is preserved in column A.

The named-range and source-contract mapping is the authoritative Prompt 5 interface. The package does not claim exact column-order compliance with the earlier draft list.
