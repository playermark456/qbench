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

## Source identity and multi-file behavior

`source_row_hash` identifies the instrument source injection. It is built from
controlled source-derived fields only: raw source file hash, LabSolutions sample
name and sample ID, acquired time, vial, source data/method/sequence files,
instrument name, detector ID, the ordered 23 analyte values, Dimethylacetamide,
Compound Results count, and Peak Table count.

QBench assignment fields are excluded from `source_row_hash`, including QBench
Test ID, QBench Sample ID, product matrix, source batch ID, reviewer selection,
and confirmation flags. The optional `assignment_hash` combines
`source_row_hash` with QBench Test ID for traceability only; duplicate source
row detection uses `source_row_hash`.

`buildWideImportRows(fileInputs, config, contexts, securityLimits)` accepts
multiple `.txt` files, enforces `maximum_files_per_run` and per-file size
limits, parses one row per file, rejects duplicate `source_row_hash`, reports
duplicate `source_file_hash`, sorts deterministically, and returns
`publish_selection_status = decision_required` when multiple reviewed
injections remain plausible for one Test ID. It never averages or selects a
winner.

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
