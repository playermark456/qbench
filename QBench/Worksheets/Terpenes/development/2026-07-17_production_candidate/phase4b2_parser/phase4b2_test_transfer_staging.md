# Phase 4B.2 Test Transfer staging

Status: `staff_staging_ready_expected_staff_review_preparation_and_batch_qc_prerequisites`

The prior filename blocker is superseded.

- `artifact_validation_source = phase4b2_validation_report.md`
- `missing_artifact_validation_alias = nonblocking_prompt_filename_mismatch`

Exactly two mapped Sample rows appeared in Test Transfer staging. The other
thirteen Sample rows remained held without a QBench Test mapping, and all
nineteen control rows were excluded.

The two staged rows contained the intended Test/Sample linkage and Product
Matrix. Their downstream analytical and audit fields remained gated because
both corresponding Instrument Import rows had:

- `import_validation_status = Review Required`;
- `import_message = Integration review required`;
- `manual_integration = No`;
- `integration_review_status = Review Required`.

This is a staff-review hold, not a parser-write failure. The imported rows
retained their parser version, source-row hashes, source audit, compound/peak
counts, Dimethylacetamide values, and analyte landing. No staff-controlled
field was manually completed.

Batch Review remained neutral and non-releasing:

- two populated publish rows;
- zero duplicate Test IDs;
- QC data complete;
- integration review incomplete;
- QC configuration and QC review incomplete;
- Batch disposition `Hold`;
- Batch publish ready `false`;
- first release message `Run setup incomplete`.

Task C2E left the Batch without Save and reopened it from the normal Batches
list. Both Test Transfer candidates persisted. Rows below the two candidates
remained blank in visible top, middle, and bottom checks.

For both persisted candidates:

- AZ `Analytical Values Complete` = `false`;
- BA `Source/Audit Complete` = `false`;
- BB `Row Prerequisites Complete` = `false`;
- BC `Publish Ready` = `false`;
- BD `Publish Message` = `Analytical values incomplete`.

All five fields remained readonly computed cells. AZ/BA/BB/BC were valid
Boolean states, BD was neutral text, and no `#ERROR` appeared. Staff-controlled
incomplete fields remained incomplete.

## Task C3 idempotency result

After explicit user authorization, the same ignored runtime source was
submitted exactly once more. The parser again reported 34 imported records,
two resolved Samples, thirteen held Samples, and nineteen controls.

The second import performed deterministic range replacement:

- pre-import logical rows: 34;
- post-import logical rows: 34;
- duplicate logical rows: 0;
- rows 36:201 with an `import_row_id`: 0;
- ordered stable row keys, source hashes, parser versions, and source-row
  hashes: exact baseline match;
- all 782 analytical cells: exact baseline match and native numeric type;
- AF formula cells preserved: 34;
- AG formula cells preserved: 34;
- mapped Samples: 2;
- held/unmapped Samples: 13;
- excluded controls: 19;
- Test Transfer candidates: 2.

`sandbox_parser_idempotency =
passed_deterministic_range_replacement`.

## Candidate aliases

The two candidates are recorded only as Candidate A and Candidate B. No Test
identifier or validation Sample name is tracked.

For both candidates, the mapped Instrument Import source row had:

- 23 numeric analytical channels and zero blank channels;
- complete parser-populated source files, instrument/detector audit,
  parser version, source injection key, and source-row hash;
- 24 compound-result rows and 23 reportable compound rows;
- numeric Dimethylacetamide;
- `manual_integration = No`;
- `integration_review_status = Review Required`;
- `import_validation_status = Review Required`;
- `import_message = Integration review required`.

## AZ — Analytical Values Complete

The AZ formula contract requires all 23 Test Transfer analytical result cells
D:Z to be populated.

Candidate A and Candidate B each had:

- numeric cells: 0;
- blank cells: 23;
- text/error cells: 0;
- AZ evaluated result: `false`;
- classification:
  `analytical_staging = incomplete_with_exact_missing_columns`.

The exact missing columns for each candidate were:

`α-Pinene`, `Camphene`, `β-Myrcene`, `(-)-β-pinene`,
`Delta-3-carene`, `α-Terpinene`, `cis-Ocimene`, `d-Limonene`,
`p-Cymene`, `trans-Ocimene`, `Eucalyptol`, `γ-Terpinene`,
`Terpinolene`, `Linalool`, `(-)-Isopulegol`, `Geraniol`,
`β-Caryophyllene`, `α-Humulene`, `cis-Nerolidol`, `trans-Nerolidol`,
`(-)-Guaiol`, `Caryophyllene Oxide`, and `(-)-α-Bisabolol`.

This is not an analytical parser-write failure. The source landing contains
23/23 numeric values; Test Transfer projections are intentionally gated while
the mapped rows remain at staff integration review. All 23 missing D:Z cells
are `formula_owned` transfer projections with `parser_populated` analytical
source values.

## BA — Source/Audit Complete

The immediate Test Transfer values AH:AX were blank for both candidates
because the transfer projection remained gated. Their required ownership and
underlying source state were:

| Cell | Header | Ownership | Underlying state |
|---|---|---|---|
| AH | Source Batch ID | `qbench_context` | Batch context exists; projection gated |
| AI | Source Instrument File | `parser_populated` | present in Instrument Import |
| AJ | Source File Hash | `parser_populated` | present in Instrument Import |
| AK | Source Data File | `parser_populated` | present in Instrument Import |
| AL | Source Method File | `parser_populated` | present in Instrument Import |
| AM | Source Sequence File | `parser_populated` | present in Instrument Import |
| AN | Parser Version | `parser_populated` | present in Instrument Import |
| AO | Imported At | `formula_owned` | source acquisition time present; projection gated |
| AP | Instrument Name | `parser_populated` | present in Instrument Import |
| AQ | Detector ID | `parser_populated` | present in Instrument Import |
| AR | Detector Name | `parser_populated` | present in Instrument Import |
| AS | Source Injection ID | `parser_populated` | present in Instrument Import |
| AT | Source Row Hash | `parser_populated` | present in Instrument Import |
| AU | Dimethylacetamide Conc. | `parser_populated` | numeric in Instrument Import |
| AV | Compound Results Complete | `formula_owned` | 24 compound / 23 reportable rows |
| AW | Integration Review Status | `staff_required` | `Review Required`, not `Reviewed` |
| AX | Import Validation Status | `formula_owned` | `Review Required`, not `Valid` |

BA evaluated `false` for both candidates. The root incomplete prerequisite is
AW staff integration review; AX remains non-Valid as the dependent AF result.
The blank source/audit projections are dependent gated outputs, not missing
parser values.

## BB — Row Prerequisites Complete

The current prerequisite diagnosis was identical for both candidates:

| Prerequisite | Current Test Transfer value / underlying source state | Pass | Ownership |
|---|---|---:|---|
| unique Test ID | present and unique | yes | `qbench_context` |
| AZ = true | `false` | no | `formula_owned` |
| AA numeric and > 0 | blank; source value `1` | no | `parser_populated` |
| AB numeric and > 0 | final volume blank | no | `staff_required` |
| AD = already_applied_by_labsolutions | blank; source value matched | no | `parser_populated` |
| AE = ug/g | blank formula projection | no | `formula_owned` |
| AF = TRUE | blank | no | `staff_required` |
| AG = TRUE | blank | no | `staff_required` |
| BA = true | `false` | no | `formula_owned` |
| AY = Accepted | `Hold` | no | `staff_required` |

No parser-owned value required by the current raw-source contract was missing.
Final volume, unit confirmation, preparation confirmation, integration review,
and Batch QC disposition remain expected staff-controlled prerequisites.

## BC and BD

For both candidates:

- BC `Publish Ready` = valid Boolean `false`;
- BD `Publish Message` = neutral text `Analytical values incomplete`;
- no `#ERROR`;
- all AZ:BD computed cells remained readonly;
- no transfer occurred.

BD matches the first failing formula prerequisite because AZ is false.

## Classification and controlled stop

- Parser defects: none.
- Worksheet/formula defects: none.
- Expected QBench context: present unique Test/Sample/Batch associations.
- Expected staff-controlled prerequisites: integration review, final volume,
  unit confirmation, preparation confirmation, and accepted Batch QC
  disposition.
- `recommended_next_action = staff_staging_ready`.
- `transfer_staging_classification =
  staff_staging_ready_expected_staff_review_preparation_and_batch_qc_prerequisites`.

Both associated Tests remained NOT STARTED. The Test worksheets were not
opened. No Batch-to-Test write, analytical Test modification, Pass/Fail,
completion, publication, release, QC Review, third import, cleanup, stage,
commit, push, or PR update occurred.
