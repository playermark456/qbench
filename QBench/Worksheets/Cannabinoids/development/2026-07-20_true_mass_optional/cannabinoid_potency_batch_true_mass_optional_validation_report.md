# Cannabinoid Potency Batch Optional True Mass Validation

Date: 2026-07-20
Overall result: **PASS for static JSON validation; QBench Sandbox runtime test still required**.

## Source and candidate

- Uploaded source: `spreadsheet-export-template (31).json`
- Source SHA-256: `3ca5b821051e231bdb3caf69a35d1d2c387dcc6d1aa4688b75f30df6be42d40f`
- Corrected candidate: `cannabinoid_potency_batch_true_mass_optional__2026-07-20.json`
- Candidate SHA-256: `cd3decad45bd6e6475ad19a352d4a16faf118e0f49a3ad3a96595014ebc4ffbc`

## Implemented contract

- Adds column `AH` with header `True Mass per Unit`.
- Pulls Test additional field identifier `true_mass_per_unit`.
- Uses `tests[n]` so each batch row resolves against its corresponding Test.
- Blank, `none`, unresolved, and nonnumeric values resolve to an empty string.
- No required-field check was added.
- No pass/fail logic, named-cell requirement, automation dependency, or report dependency was added.
- Existing columns `A:AG` remain unchanged.
- Root `data["Results"]` and `config.worksheets[0].data` match.

## Formula pattern

```excel
=IF(OR("${tests[n].additional_fields['true_mass_per_unit'].value}"="",LOWER("${tests[n].additional_fields['true_mass_per_unit'].value}")="none"),"",IFERROR(VALUE("${tests[n].additional_fields['true_mass_per_unit'].value}"),""))
```

## Intended Homogeneity workflow

1. Technician records True Mass per Unit on each individual Cannabinoid Potency Test.
2. Cannabinoid Potency Batch worksheet displays the value in column AH.
3. Staff copy the batch results row, including AH.
4. Homogeneity Paste tab receives AH as the measured unit/serving mass.
5. A missing True Mass remains blank and must not break the potency batch worksheet.

## Important limitations

- Static validation cannot prove that the exact QBench merge-field syntax resolves in this QBench environment.
- The candidate must be imported into an inactive Sandbox worksheet and tested with one populated and one blank Test field.
- Do not activate or overwrite the current batch worksheet until runtime behavior is confirmed.

## Sandbox checks

- Numeric Test field value appears in the matching AH row.
- Empty Test field leaves AH blank.
- Nonnumeric input leaves AH blank rather than producing an error.
- Existing potency calculations and columns A:AG are unchanged.
- Copy/paste into Homogeneity preserves Test ID and True Mass row alignment.
