# Phase 4A.4 runtime binding contract

## Key/Value Store binding

The Sandbox visual association table for `SBX_ONLY_TERPENES_RUNTIME_KV_V2` exposes a UUID in its `ID` column. The historical working Terpenes Test worksheet stores the associated Key/Value Store UUID in the cell passed as the first argument to `GET_KVSTORE_VALUE`.

- Required binding classification: `another non-secret visible identifier`
- Required Sandbox binding literal: `4e57fd8a-0241-4eb1-a9c5-370fb243895d`
- Visible store title is not used as the formula binding literal.
- The identifier is environment configuration, not a credential or token.

## Matrix runtime source

- `matrix_runtime_source = Data!C2`
- QBench placeholder: `${test.sample.product_matrix}`
- V3 `Specifications!U4`: `${test.sample.product_matrix}`
- Binding mode: `dynamic_test_matrix_reference`

`Data!C2` is already formula/configuration owned and was proven in the historical working Test generator. It is not one of the 43 parser/publisher destinations. V3 does not add a manual matrix field or hardcode a single matrix for all Tests.

## Matrix normalization

The Sandbox runtime proof is designed to use the exact controlled matrix name already represented in the isolated fixture: `SBX_ONLY_RUNTIME_MATRIX_V2`. For that exact synthetic Test value, normalization is not required.

| Runtime Test matrix | Key/Value controlled matrix | Transformation |
|---|---|---|
| `SBX_ONLY_RUNTIME_MATRIX_V2` | `SBX_ONLY_RUNTIME_MATRIX_V2` | identity |

No broader production matrix-category inference is made. Any future production matrix aliases require an explicit approved mapping before use.
