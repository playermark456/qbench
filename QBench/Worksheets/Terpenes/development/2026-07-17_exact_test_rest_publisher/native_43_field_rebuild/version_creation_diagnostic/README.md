# Native version-creation diagnostic

Date: 2026-07-17

Historical classification: **`version_created_named_cell_missing`**.

Current classification: **`codex_named_cell_save_control_failed`**.

This isolated Sandbox-only control separates the existence of a saved
worksheet version from named-cell persistence. The QBench Versions tab visibly
showed the first row as `1 - Version Creation Control v1` with status `DRAFT`.
That visible Draft row is the required proof that a worksheet version was
saved.

The saved draft was reopened through the normal worksheet UI. It retained the
6x5 grid, A1 text, and blank B2, but the named-cell configuration had zero
rows. That historical observation remains valid, but its inference that QBench
native named-cell persistence was environmentally blocked is superseded.

The user manually added `sdf` at `A1` to
`SBX_ONLY_TERPENES_2026_07_17_NATIVE_SCALAR_43_FIELD_BASE`, exact version
`1 - Native Scalar 43 Field Base v1 - DRAFT`, used **Save Draft**, refreshed,
and confirmed persistence. Codex then reopened that exact Draft and visibly
confirmed `sdf`, blank Display Name, and Exportable enabled. A separate Codex
control at `B2` was visibly complete before **Save Draft** but did not survive
refresh and list-based reopen while `sdf` remained. Therefore QBench native
named-cell persistence is operational, the Codex browser save procedure is not
authoritative, and further Codex-controlled worksheet editing is stopped.

No approval, activation, Assay, Sample, Test, analytical result, Pass/Fail,
token request, REST request, PATCH, or live-QBench access occurred.
