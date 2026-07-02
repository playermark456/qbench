# AGENTS.md

## Project purpose

This repository maintains Adams Independent Testing's QBench Sandbox exports, QBench worksheet JSON templates, COA/Jinja/HTML report source code, file parser documentation, automation documentation, image assets, validation scripts, and QBench workflow notes.

Use this repository as the source of truth for designing and validating QBench template/report changes before anything is uploaded or changed in QBench.

## Safety rules

- Do not modify QBench directly unless the user explicitly instructs you to do so for a specific action.
- Treat QBench Sandbox as read-only unless explicitly instructed otherwise.
- Never modify production QBench.
- Do not click Save, Delete, Submit, Approve, Set Active, Import, Update, Create, Duplicate, Publish, or any other QBench action that changes data or configuration unless explicitly instructed.
- Prefer making changes in repository files, then provide a QBench Sandbox test checklist for the user.
- Preserve all user-provided/raw exports. Do not overwrite source exports; create edited/production-candidate copies in a current or release folder.
- Do not remove archived attempts unless explicitly instructed.
- Do not hardcode new QBench production blob URLs if a report config attachment can be referenced by filename.

## QBench-specific conventions

- QBench worksheet templates are usually exported/imported as spreadsheet JSON files.
- The required worksheet export action is QBench's **Export Spreadsheet** option, not **Export to Excel**, unless the user specifically requests Excel.
- A worksheet is not considered fully exported unless the actual file from **Export Spreadsheet** exists in this repo and is listed in the export status documentation.
- Named-cell captures/screenshots are useful, but they are not a substitute for a full Export Spreadsheet file.
- Maintain clear distinction between active/approved worksheet versions and draft/default worksheet versions.
- Preserve QBench formula syntax as written in worksheet JSON unless intentionally fixing a formula.
- Avoid duplicate named-cell system names.
- Avoid duplicate named cells pointing to the same exact cell/range with the same display name unless documented.
- Keep report output ranges compact enough to render cleanly in the QBench PDF/COA renderer.

## COA/report rendering rules

- Preserve QBench Jinja/HTML syntax in COA source files.
- Preserve service calls such as:
  - `QBTestService().render_worksheet(...)`
  - `QBOrderService().render_test_worksheets_summary(...)`
- When a report renders a worksheet by named cell, confirm that the named cell exists in the related worksheet JSON.
- When editing COA source, verify assay IDs and named-cell references against the repository indexes.
- The Homogeneity COA integration should use:
  - `pass_fail` for the first-page hex tile / pass-fail logic.
  - `report_results` for the standalone Homogeneity table/page.

## Required Homogeneity behavior

The Homogeneity worksheet/workflow must support:

- 10 replicate units.
- Pasted Cannabinoid Potency batch result rows.
- Actual unit mass for each replicate.
- Optional label unit mass.
- Target Cannabinoid 1.
- Optional Target Cannabinoid 2.
- Label cannabinoid content, mg/container, for each target cannabinoid used.
- mg/container calculation for each target cannabinoid.
- Cannabinoid label variance for each target cannabinoid.
- Mass variance from label mass when label mass is provided.
- Mass variance from average actual unit mass when no label mass is provided.
- Highest reported unit mass and its variance.
- Highest reported cannabinoid mg/container and its variance.
- Overall Pass/Fail.
- Use the word **Highest**, not **Worst**, in report labels.

Required Homogeneity named cells:

- `pass_fail`
- `report_results`

Compatibility named cells, if used by current COA/report code:

- `homogeneity_metrc`
- `target_cannabinoid_1`
- `target_cannabinoid_2`

## Repository organization

Recommended top-level structure:

```text
QBench/
  COA/
  Worksheets/
  File_Parsers/
  Automations/
  Docs/
  Examples/
  Archive/
```

For each assay/module, keep a README explaining:

- Assay name.
- QBench assay ID, if known.
- Worksheet/template file(s).
- Active vs draft status.
- Required named cells.
- COA/report dependencies.
- Parser files/status.
- Automation rules/status.
- Raw instrument/source file type.
- Calculation notes.
- Open questions.

## Important index files

Maintain these if present:

- `QBench/SYSTEM_MAP.md`
- `QBench/ASSAY_ID_MAP.md`
- `QBench/NAMED_CELL_INDEX.md`
- `QBench/REPORT_RENDERING_MAP.md`
- `QBench/FILE_PARSER_INDEX.md`
- `QBench/AUTOMATION_INDEX.md`
- `QBench/Docs/qbench_open_questions.md`
- `QBench/Docs/qbench_export_status.md`

## Validation checklist after worksheet JSON edits

After editing a worksheet JSON file:

1. Confirm the JSON parses.
2. Confirm worksheet names are unique.
3. Confirm named-cell system names are unique.
4. Confirm required named cells exist.
5. Confirm report named-cell ranges exist and are not empty.
6. Confirm no duplicate named-cell targets with the same display name unless documented.
7. Confirm formulas are compatible with QBench's spreadsheet editor.
8. Confirm the edited file is a production-candidate copy and raw exports are preserved.

If validation scripts exist, run them and include the output in the response.

## Validation checklist after COA source edits

After editing a COA/Jinja/HTML source file:

1. Confirm Jinja blocks remain balanced.
2. Confirm assay IDs match `QBench/ASSAY_ID_MAP.md` where applicable.
3. Confirm every rendered named cell exists in the corresponding worksheet JSON.
4. Confirm Homogeneity, if present, uses `pass_fail` and renders `report_results`.
5. Confirm image assets referenced by filename exist in the repo or are documented as QBench report config attachments.
6. Provide a QBench Sandbox preview checklist.

## Working style

For complex work, use this sequence:

1. Inspect and report findings without editing.
2. Propose a design/plan.
3. Wait for user approval if the change is broad.
4. Implement a narrow, focused change.
5. Run validation.
6. Summarize changed files, validation results, QBench import risks, and manual test steps.

Avoid broad prompts like "fix everything." Make one controlled change at a time.

## QBench Sandbox testing checklist template

For any worksheet/report release, provide steps for the user to test in QBench Sandbox:

1. Import worksheet JSON.
2. Attach worksheet to the intended assay/test.
3. Confirm required named cells are visible.
4. Create or open a representative test/sample.
5. Enter or paste test data.
6. Confirm calculations and Pass/Fail.
7. Generate COA preview.
8. Confirm the first-page tile displays correctly.
9. Confirm rendered worksheet/report table fits the COA page.
10. Compare key results against manual calculation.
11. Only promote to production after Sandbox testing passes.
