# Terpenes Codex source package

This folder contains the sanitized source documents and fixtures needed to begin the Terpenes QBench/Codex implementation.

## Included files

- `terpenes_codex_build_brief_v3.md` — current implementation brief, including METRC conclusions.
- `terpenes_worksheet_spec_v3.json` — calculation, QC, import, and export specification.
- `terpenes_analyte_master_v3.csv` — 23-channel internal analyte master and aliases.
- `labsolutions_ascii_integration_spec.md` — LabSolutions ASCII import contract.
- `parse_labsolutions_ascii.py` — repository-friendly parser with CLI arguments.
- `Output_redacted_fixture.txt` — sanitized LabSolutions ASCII fixture.
- `metrc_terpene_export_profiles.json` — profile-specific METRC units and sheet mappings.
- `metrc_terpene_reportable_mapping.csv` — analyte-to-METRC mapping decisions.
- `labsolutions_compound_results_fixture.csv` — 24 compound-result rows, including Dimethylacetamide.
- `labsolutions_peak_table_fixture.csv` — 34 chromatographic peak rows.
- `labsolutions_normalized_reportable_results_fixture.csv` — 23 reportable terpene rows.
- `MANIFEST.sha256` — file-integrity hashes.

## Redaction

The repository is public. The original raw `Output.txt` is therefore not included. The redacted fixture preserves table structure, analyte names, representative values, and row counts while replacing internal usernames, instrument names, and local file paths.

## Parser check

From this directory:

```bash
python parse_labsolutions_ascii.py --output-dir generated
```

Expected summary:

```text
compound_rows: 24
peak_rows: 34
reportable_compound_rows: 23
non_reportable_compounds: [Dimethylacetamide]
```

## Status

These are implementation inputs, not approved QBench production templates. Any generated worksheet, parser, automation, METRC, or COA change must be tested in QBench Sandbox and approved under laboratory document control before production use.
