# Wide Instrument Import row mapping

The wide adapter creates one logical row for one LabSolutions injection.

| Range | Behavior |
|---|---|
| `A:AE` | Writable source/context/audit block |
| `AF` | Worksheet-owned Import Validation Status formula |
| `AG` | Worksheet-owned Import Message formula |
| `AH:BD` | 23 Prompt 2 analyte `Conc.` values in config order |
| `BE` | Deterministic source row hash |

The generated write plan excludes `AF` and `AG`.

## Column map

| Column | Field |
|---|---|
| A | import_row_id |
| B | run_order |
| C | vial |
| D | sample_type |
| E | qbench_test_id |
| F | qbench_sample_id |
| G | product_matrix |
| H | sample_mass_g |
| I | final_volume_ml |
| J | qbench_df |
| K | df_application_mode |
| L | labsolutions_sample_amount |
| M | labsolutions_dilution_factor |
| N | source_instrument_file |
| O | source_file_hash |
| P | source_data_file |
| Q | source_method_file |
| R | source_sequence_file |
| S | acquired_at |
| T | instrument_name |
| U | detector_id |
| V | detector_name |
| W | parser_version |
| X | compound_result_row_count |
| Y | peak_table_row_count |
| Z | reportable_compound_row_count |
| AA | dimethylacetamide_conc |
| AB | unknown_peak_count |
| AC | manual_integration |
| AD | integration_reason |
| AE | integration_review_status |
| AF | worksheet-owned formula |
| AG | worksheet-owned formula |
| AH:BD | 23 reportable analyte `Conc.` values |
| BE | source_row_hash |

The JSON fixture preserves JavaScript number types. TSV files are only
human-testing artifacts.
