# Phase 4A.4B Test v3 manual native-file import

Date: 2026-07-21

Neutral Sandbox identifier: `SANDBOX_TEST_WORKSHEET_V3`

## Local gate

- Candidate: `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v3.json`
- SHA-256: `b68f0e1589ba4e2f5c3c85196c648ed5238a1700b02d8feca3e20850ede19014`
- Renderer contract: passed
- Calculation contract: passed
- Runtime-configuration contract: passed
- Formula count: 309
- Writable destinations: 43
- Named definitions: 44
- Unresolved configuration markers: 0
- Candidate regenerated or edited: no

## Clean-shell gate

The visual Sandbox session started from the Worksheets list and reopened the exact existing V3 shell. Before import, the shell was inactive, had no Assay association, displayed default `Sheet1`, and its Versions tab visibly showed no saved versions. No unsaved-change warning or unsaved-change indicator remained.

## Manual native-file import

Codex exposed QBench's native **Import Spreadsheet** dialog and paused. The user was instructed to select the exact V3 file through **Choose file**, use the visible confirmation once, avoid **Save As New Version**, and reply `done`.

- Selected filename shown during the native dialog: `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v3.json`
- Native action used: `Submit`, exactly once
- Visible warning before submission: `Warning! Importing a template will overwrite any current unsaved edits!`
- Visible success message after submission: none
- Visible warning after submission: none
- Visible error after submission: none

After control returned, default `Sheet1` was gone and the renderer displayed `Report`, `Data`, and `Specifications` in that exact order. This satisfied the pre-save native-application gate. No JSON was pasted and no retry import was performed.
