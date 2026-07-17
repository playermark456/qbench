# Native version-creation diagnostic

Date: 2026-07-17

Classification: **`version_created_named_cell_missing`**.

This isolated Sandbox-only control separates the existence of a saved
worksheet version from named-cell persistence. The QBench Versions tab visibly
showed the first row as `1 - Version Creation Control v1` with status `DRAFT`.
That visible Draft row is the required proof that a worksheet version was
saved.

The saved draft was reopened through the normal worksheet UI. It retained the
6x5 grid, A1 text, and blank B2, but the named-cell configuration had zero
rows. The control therefore does not unlock destination proof or further
worksheet construction.

No approval, activation, Assay, Sample, Test, analytical result, Pass/Fail,
token request, REST request, PATCH, or live-QBench access occurred.
