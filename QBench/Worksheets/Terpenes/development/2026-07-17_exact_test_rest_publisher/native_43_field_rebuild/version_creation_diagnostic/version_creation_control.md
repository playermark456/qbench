# Version-creation control result

Worksheet: `SBX_ONLY_TERPENES_2026_07_17_VERSION_CREATION_CONTROL`

Native construction before Create:

- Spreadsheet grid: 6 rows by 5 columns.
- A1: `Version creation control`.
- B2: blank, writable, and non-formula.
- Exactly one visible Named Cell row was added with system name
  `terpenes_version_creation_control_20260717`, cell B2, display name
  `Version creation control`, and Exportable enabled.

The native **Save As New Version** workflow was used. Its **Create** action
produced the visible QBench Versions-tab row `1 - Version Creation Control v1`
with status `DRAFT`.

On reopen of that saved draft, the 6x5 grid, A1, and blank B2 remained, while
the Named Cells section had zero rows. The control classification is
`version_created_named_cell_missing`; no further destination construction is
permitted by that historical run.

The environment-blocker conclusion from this control is superseded by the
user's persisted `sdf` / A1 control in the exact native scalar Draft. The
current control is `codex_named_cell_save_control_failed`: the Codex B2 row was
complete before **Save Draft** and absent after refresh/reopen while `sdf`
remained. QBench persistence is operational, but browser-controlled worksheet
entry is not authoritative.
