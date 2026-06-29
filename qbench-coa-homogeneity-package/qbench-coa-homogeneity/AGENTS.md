# AGENTS.md

## Project purpose

Maintain QBench COA source code and QBench spreadsheet JSON templates for MN OCM Homogeneity reporting.

## Important constraints

- Preserve QBench Jinja/HTML syntax in COA files.
- Preserve QBench worksheet JSON structure.
- Do not remove these Homogeneity named cells:
  - `pass_fail`
  - `report_results`
  - `homogeneity_metrc`
- Do not hardcode new production blob URLs if a report config attachment can be referenced by filename.
- Avoid duplicate named-cell system names.
- Prefer formulas that QBench spreadsheet editor can evaluate.
- Keep report output compact enough for PDF rendering.

## Validation checklist after worksheet JSON edits

Run:

```bash
python scripts/validate_qbench_json.py worksheets/current/homogeneity_copy_paste_v6_two_target_COA_import_safe.json
```

Confirm:

- JSON parses.
- Worksheet names are unique.
- Named cell system names are unique.
- `pass_fail` exists.
- `report_results` exists.
- No obvious duplicate named cells.

## Validation checklist after COA source edits

Run:

```bash
python scripts/compare_coa_to_worksheet.py coa/coa_source_8tile_homogeneity_full.html worksheets/current/homogeneity_copy_paste_v6_two_target_COA_import_safe.json
```

Confirm:

- COA references `HOMOGENEITY_TEST`.
- COA renders Homogeneity `report_results`.
- Homogeneity named cells used by the COA exist in the worksheet JSON.

## Project conventions

- Put production-candidate files in `worksheets/current/` and `coa/`.
- Put older attempts in `worksheets/archive/`.
- Keep source/user-provided exports unchanged in `uploaded_sources/`.
- Update `README.md` and `docs/CHANGELOG.md` when changing behavior.
