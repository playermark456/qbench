# Phase 4A.5 matrix and fixture result

Date: 2026-07-21

`environment_profile = sandbox_runtime_only`

The synthetic label `SBX_ONLY_RUNTIME_MATRIX_V2` was not selectable in the Sandbox Sample product-matrix control. The existing generic Sandbox matrix `Cannabis Concentrates` was selected as the safe runtime matrix.

A second `Cannabis Concentrates` branch was added only to `SBX_ONLY_TERPENES_RUNTIME_KV_V2`. It copied the isolated fixture's synthetic 21 LOQ values, 21 direct MU values, and four component MU values. The original `SBX_ONLY_RUNTIME_MATRIX_V2` branch remained present and unchanged. No global matrix, shared store, or operational store was created or modified.

This is a Sandbox-only runtime choice. It is not a production Key/Value binding, matrix alias, or matrix-normalization policy.
