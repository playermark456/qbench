# Prompt 4.6B Sandbox import compatibility record

Date: 2026-07-16

## Stop condition

No scalar patch may begin until a disposable worksheet visibly contains the
exact controlled `Probe` tab, 17 rows, formulas, data, and named-cell
locations from:

`../2026-07-15_qbench_native_parser_probe/dist/qbench_runtime_probe_batch_ws_candidate.json`

Do not save a version, activate a version, attach an assay, or run a patch on a
worksheet that fails this check.

## Mismatched import on worksheet 61

The imported file was
`sandbox_probe_worksheet_compatibility_candidate.json`, not the controlled
`dist/qbench_runtime_probe_batch_ws_candidate.json`.

The uploaded file itself contains:

- one worksheet named `Sheet1`;
- 96 rows of the pre-existing Terpenes Batch Worksheet export;
- old visible values including `STD 1`, `Blank`, and `System Suitability`;
- `probe_text = Sheet1!B96`;
- `probe_number = Sheet1!C96`.

QBench displayed those same values after reporting `Import Successful!`.
Therefore this run does not prove that the older Sandbox importer merged,
ignored, translated, or partially imported the controlled `Probe` candidate.
It proves that the wrong compatibility artifact was selected and that the
Terpenes-derived compatibility design is invalid for this probe.

Reloading worksheet 61 did not clear the imported configuration. The Versions
tab reported `No Versions Found`, so no version was created, but the imported
configuration remained as a persisted working draft. Worksheet 61 is
quarantined and must not be saved, activated, attached, or used for a patch.

## Replacement compatibility baseline

A new inactive, disposable Dynamic Spreadsheet worksheet was created in the
older Sandbox runtime:

- QBench Sandbox worksheet ID: `62`;
- name: `SBX_ONLY_TERPENES_2026_07_16_Probe_Minimal_Runtime_Baseline`;
- active: no;
- assays: 0;
- initial worksheet: blank `Sheet1`, 8 rows by 8 columns;
- initial named cells: 0;
- versions: none.

Its actual **Export Spreadsheet** file is preserved at:

`source/2026-07-16_ait-sandbox_ws_id_62_blank_export_spreadsheet.json`

SHA-256:

`02e986a41bcd9f6b1bc9586c3df041cbaf930ad4309fb28d5e20d26c6057e5c2`

The replacement candidate is generated from that file while preserving its
old-Sandbox namespace and worksheet identity and replacing only the blank
spreadsheet payload with the exact controlled `Probe` semantics.

## Required import verification

Before any save or patch:

1. Import `dist/qbench_runtime_probe_batch_ws_candidate__ait_sandbox_runtime.json`
   into worksheet 62.
2. Confirm the only tab is `Probe`.
3. Confirm the visible worksheet has 17 rows and no Terpenes batch content.
4. Confirm the initial named cells include:
   - `probe_text = Probe!B2`
   - `probe_number = Probe!B3`
   - `probe_isnumber = Probe!B4`
   - `probe_count = Probe!B5`
   - `probe_sentinel = Probe!B6`
5. Confirm all 15 controlled named cells and nine controlled formulas.
6. Stop without saving if any value differs.

The controlled candidate has not yet been imported into worksheet 62. No
scalar patch is authorized or ready.
