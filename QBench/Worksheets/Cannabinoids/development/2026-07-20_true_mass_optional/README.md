# Cannabinoid Potency Batch - Optional True Mass per Unit

Date: 2026-07-20
Status: candidate for inactive QBench Sandbox testing; not production-approved.

## Purpose

Add an optional `True Mass per Unit` column to the Cannabinoid Potency Batch Spreadsheet Worksheet so technicians can enter `true_mass_per_unit` on each individual Cannabinoid Potency Test and the batch output can be copied directly into the Homogeneity worksheet.

## QBench field contract

- Field label: `True Mass per Unit`
- Field identifier: `true_mass_per_unit`
- Entity: Test additional field
- Worksheet reference pattern: `${tests[n].additional_fields['true_mass_per_unit'].value}`

## Candidate behavior

- Column `AH` is added with header `True Mass per Unit`.
- Test data rows use the corresponding `tests[n]` additional-field reference.
- Blank, `none`, unresolved, or nonnumeric values return a blank cell.
- The field is optional. No required-field validation, pass/fail gate, named-cell requirement, or workflow blocker is added.
- Existing columns `A:AG` are preserved so the new column can be pasted into the Homogeneity mass-input position.

Representative formula:

```excel
=IF(OR("${tests[0].additional_fields['true_mass_per_unit'].value}"="",LOWER("${tests[0].additional_fields['true_mass_per_unit'].value}")="none"),"",IFERROR(VALUE("${tests[0].additional_fields['true_mass_per_unit'].value}"),""))
```

## Repository artifacts

- `patch_cannabinoid_batch_true_mass_optional.py` deterministically creates the candidate from a QBench Export Spreadsheet JSON.
- `cannabinoid_potency_batch_true_mass_optional_validation_report.md` records the exact source and candidate SHA-256 hashes, formula contract, and Sandbox checks.
- The generated candidate filename is `cannabinoid_potency_batch_true_mass_optional__2026-07-20.json`.

The generated JSON is a large QBench export artifact. When it is copied into the local repository, place it in this directory and verify its SHA-256 against the validation report before import or commit. The patcher plus source hash remains the reproducible definition if the binary-sized artifact is not present in a remote branch.

## Generate the candidate

```powershell
python patch_cannabinoid_batch_true_mass_optional.py `
  "<source Export Spreadsheet JSON>" `
  "cannabinoid_potency_batch_true_mass_optional__2026-07-20.json"
```

Expected candidate SHA-256:

```text
cd3decad45bd6e6475ad19a352d4a16faf118e0f49a3ad3a96595014ebc4ffbc
```

## Sandbox verification

1. Import the generated candidate into an inactive Cannabinoid Potency Batch worksheet.
2. Confirm a Test with a numeric `true_mass_per_unit` displays that value in column AH.
3. Confirm a Test with no value leaves AH blank.
4. Confirm blank AH cells do not cause formula, validation, or batch failures.
5. Copy the Homogeneity input rows and confirm the AH values align with the correct Test IDs.

Do not activate or replace the current QBench worksheet until these checks pass.
