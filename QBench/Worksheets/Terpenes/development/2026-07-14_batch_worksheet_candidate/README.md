# Terpenes Batch Worksheet candidate

Date: 2026-07-14

This repository-only package builds a deterministic, nonproduction Terpenes Batch Worksheet candidate from the latest active Worksheet ID 43 export:

`QBench/Rescans/2026-07-04/Worksheets/Terpenes/terpenes__id_43__worksheet_export_spreadsheet__active__2026-07-04.json`

Source SHA-256:

`db6bfe7a7d306902b78c27af76b4a08a2a17b7d974f63c5593a3455e109bad07`

The package does not modify active/raw worksheet exports, the Prompt 3 Test Worksheet candidate, COA source, QBench automation, active parser configuration, protocol worksheets, key/value-store configuration, METRC export configuration, report configuration, or any QBench production object.

## Contents

- `scripts/build_terpenes_batch_worksheet.py` builds the candidate JSON and manifest.
- `scripts/validate_terpenes_batch_worksheet.py` statically validates the generated candidate.
- `scripts/reference_terpenes_batch_logic.py` provides test-only reference logic for row validation, QC boundaries, release gates, and transfer readiness.
- `tests/test_terpenes_batch_worksheet.py` covers generation, layout, formulas, named cells, release gates, invalid cases, and reference behavior.
- `tests/fixtures/` stores valid import rows, QC boundary cases, and invalid batch cases.
- `config/` stores the layout and normalized import contract used by the package.
- `docs/` stores the design, field map, instrument-import contract, batch-to-test contract, QC crosswalk, and Sandbox checklist.
- `dist/terpenes__batch_ws_id_43__candidate_v1__2026-07-14.json` is the generated candidate.
- `dist/candidate_manifest.json` records source hashes, dependency hashes, tab IDs, counts, ranges, release gates, and scope controls.

## Candidate scope

The generated candidate contains exactly four tabs:

1. `Run Setup`
2. `Instrument Import`
3. `QC Review`
4. `Publish`

`Publish` preserves the active source `Sheet1` worksheet ID and the source test-row capacity. The three new tab IDs are stable constants recorded in the manifest.

The Batch Worksheet stores run metadata, normalized parser/import rows, internal analytical batch QC review, and a controlled one-row-per-QBench-Test Publish surface. It does not calculate final sample mg/g, percent, qualifiers, totals, COA values, LOQ conclusions, MU values, METRC values, or key/value-store values.

Default release gates are intentionally closed:

- `bracketing_ccv_criterion_status = decision_required`
- `qc_configuration_complete = FALSE` by formula/default behavior
- `batch_qc_disposition = Hold`
- `batch_publish_ready = FALSE` by formula/default behavior

The bracketing CCV decision remains unresolved; this package does not choose 10 percent or 15 percent.

`lcs_requirement_status` also defaults to `decision_required`. The repository crosswalk does not contain controlled SOP, Analysis Form, or validation evidence sufficient to close the LCS requirement, so LCS remains a release-control decision rather than an invented worksheet limit.

## Controlled Publish column-contract decision

Publish column A is intentionally `QBench Test ID`, and Publish column B is intentionally `QBench Sample ID`. This is a controlled deviation from the original draft Prompt 4 column list because QBench Test ID is the Prompt 5 join key and the active source Test ID placeholder is preserved in column A.

The named-range and source-contract mapping is the authoritative Prompt 5 interface. The package does not claim exact column-order compliance with the earlier draft list.

## Current generated counts

- Formula count: 1180
- Named-cell count: 67
- Preserved Publish row capacity: 86
- Instrument Import row capacity: 200
- Publish table range: `Publish!A1:BD87`
- Publish 23-analyte range: `Publish!D2:Z87`
- `batch_qc_disposition`: `QC Review!B15`
- `batch_publish_ready`: `QC Review!B18`
- `bracketing_ccv_criterion_status`: `QC Review!B3`
- `lcs_requirement_status`: `QC Review!B5`

## Validation commands

Run from this directory with the bundled or system Python runtime:

```powershell
python scripts/build_terpenes_batch_worksheet.py
python scripts/validate_terpenes_batch_worksheet.py
python -m unittest discover -s tests
python -m py_compile scripts/build_terpenes_batch_worksheet.py scripts/validate_terpenes_batch_worksheet.py scripts/reference_terpenes_batch_logic.py
```

Repository validation is static. QBench Sandbox import and worksheet formula execution remain required before any future automation or production promotion.
