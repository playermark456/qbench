# Probe A - completely unique control

Classification: **`unique_named_cell_control_failed`**

- Worksheet: `SBX_ONLY_TERPENES_2026_07_17_NAMED_CELL_UNIQUE_CONTROL`
- Version: `Named Cell Unique Control v1`
- Version status: Draft
- Worksheet type: native old-Sandbox Spreadsheet Worksheet
- Grid: 6 rows by 5 columns
- Visible A1 label: `Probe A unique control`
- System Name: `terpenes_named_cell_unique_control_20260717`
- Cell: `B2`
- Display Name: `Unique persistence control`
- Exportable: enabled
- Destination before and after save: blank and writable
- Named-cell control used: **Add Named Cell**, exactly once
- Row visibly committed before save: yes
- Input commit procedure: real keystrokes; Tab outside each field; focus moved
  to the grid after enabling Exportable
- Save completion observed: yes
- Complete navigation to Worksheets list: yes
- Reopened from exact Worksheet-list entry: yes
- Grid persisted after reopen: yes, 6x5
- A1 label persisted after reopen: yes
- Named cell persisted after reopen: no; named-cell row count was zero
- Visible validation/error message: none

The row was also absent when the editor first returned after Create, and it
remained absent after the required full leave/reopen cycle.

Most narrowly supported observation: a completely unique, syntactically
ordinary single named-cell definition did not persist despite the explicit UI
row-add and input-blur procedure. This result does not isolate the defect to
the system name or to underscore syntax.
