# Terpenes config/parser foundation

Date: 2026-07-14

This repository-only package establishes the controlled Terpenes configuration,
LabSolutions ASCII parser, fixture set, and validation tests for future QBench
worksheet work. It does not modify active/raw worksheet exports, COA source,
QBench automation, QBench protocol worksheets, or any QBench object.

## Contents

- `config/terpenes_analytes.json` defines quantitative-only reporting mode,
  the 23 internal reportable chromatographic channels, Dimethylacetamide as an
  audit-only channel, alias handling, the `Compound Results(Ch1) > Conc.`
  potency source, blocked LabSolutions normalized fields, and the default
  21-measurand COA rollup shape.
- `config/terpenes_qc.json` defines internal batch QC dispositions
  `Accepted`, `Hold`, and `Rejected`, plus publish readiness rules.
- `config/metrc_profiles.json` defines profile-driven METRC mapping behavior,
  Ocimene rollup, p-Cymene specificity, profile warnings, and structural
  outcome-column neutrality if an external fixed schema ever requires that
  column.
- `fixtures/labsolutions_ascii/` contains copied sanitized fixtures from the
  source package.
- `scripts/parse_labsolutions_ascii.py` parses the fixture format and emits
  audit compound rows plus normalized reportable result rows.
- `scripts/validate_terpenes_config.py` validates the configs as a bundle.
- `tests/test_terpenes_parser_config.py` covers parser counts, audit retention,
  alias uniqueness, blocked potency sources, METRC mapping coverage, internal
  QC disposition rules, and prohibited Terpenes result-outcome artifacts.

## Controlled rules encoded here

- Terpenes reporting mode is `quantitative_only`.
- Sample, analyte, COA, METRC, key/value-store, and label-claim status-output
  controls are encoded as disabled.
- The only potency source is `Compound Results(Ch1)` field `Conc.`.
- `Conc. %` and `Norm Conc.` are retained only as not-potency audit context.
- Dimethylacetamide is retained in audit output and excluded from reportable
  terpene output.
- Internal batch QC uses `batch_qc_disposition`, separate from sample results.
- `publish_ready` can be true only when the disposition is `Accepted` and
  required analytical and audit fields are complete.
- METRC mappings are profile-driven. Analytes must not silently fall back to
  Other Terpenes.
- Both percent and mg/g result slots are preserved. Final numeric conversion
  remains blocked on unit, mass, final-volume, and dilution decisions.

## Validation commands

Run from this directory with the bundled or system Python runtime:

```powershell
python scripts/validate_terpenes_config.py
python scripts/parse_labsolutions_ascii.py --output-dir $env:TEMP\terpenes_parser_validation
python -m unittest discover -s tests
```

Expected parser summary:

```text
compound_rows: 24
peak_rows: 34
reportable_compound_rows: 23
non_reportable_compounds: [Dimethylacetamide]
```

## Decisions still unresolved

- Confirm the LabSolutions `Conc.` unit.
- Confirm sample mass and final volume sources for percent and mg/g conversion.
- Confirm whether exported dilution factor is already reflected in `Conc.`.
- Confirm below-LOQ report and METRC handling.
- Confirm default COA display units and row labels for the 21-measurand list.
- Confirm whether default COA Nerolidol should remain total cis plus trans or
  follow a split display.
- Confirm R&D Alpha-Humulene ppm handling.
- Confirm Full Panel Finished Products mixed-unit behavior.
- Confirm p-Cymene handling for profiles where the explicit row is absent.
- Confirm Guaiol handling for profiles where the row is absent.
