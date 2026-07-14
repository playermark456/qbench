# Terpenes Test Worksheet candidate

Date: 2026-07-14

This package builds a deterministic, nonproduction Terpenes Test Worksheet candidate from the latest active Worksheet ID 42 export:

`QBench/Rescans/2026-07-04/Worksheets/Terpenes/terpenes__id_42__worksheet_export_spreadsheet__active__2026-07-04.json`

Source SHA-256:

`1ff46aadc31c32b8b176f3eb0091c8ae26d905271fcbc4f1a118a3776f7820e9`

The package does not modify active/raw worksheet exports, COA source, QBench automation, QBench parser configuration, protocol worksheets, report configuration, or any QBench production object.

## Contents

- `scripts/build_terpenes_test_worksheet.py` builds the candidate JSON and manifest.
- `scripts/validate_terpenes_test_worksheet.py` statically validates the generated candidate.
- `scripts/reference_terpenes_calculations.py` provides test-only reference calculations.
- `tests/test_terpenes_test_worksheet.py` covers generation, validation, gates, formulas, named cells, and reference math.
- `tests/fixtures/calculation_reference_cases.json` stores the required calculation reference cases.
- `dist/terpenes__test_ws_id_42__candidate_v1__2026-07-14.json` is the generated nonproduction candidate.
- `dist/candidate_manifest.json` records source/config hashes and candidate summary metadata.

## Candidate scope

The candidate preserves the three active tabs: `Report`, `Data`, and `Specifications`.

It adds a controlled sample-level input surface, calculation formulas for 23 internal quantitative channels, 21 default COA measurands plus Total Terpenes, report gating, stable named cells for later automation, and static validation.

It intentionally leaves final report release blocked by default. LabSolutions unit confirmation, sample-prep source confirmation, dilution application, LOQ handling, MU source, active COA parity, and METRC profile export behavior remain unresolved.

## Validation commands

Run from this directory:

```powershell
python scripts/build_terpenes_test_worksheet.py
python scripts/validate_terpenes_test_worksheet.py
python -m unittest discover -s tests
python -m py_compile scripts/build_terpenes_test_worksheet.py scripts/validate_terpenes_test_worksheet.py scripts/reference_terpenes_calculations.py
```

Use the bundled Codex Python runtime when `python` is not on PATH.
