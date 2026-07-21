# Phase 4A.6 operational lookup-pattern comparison

Date: 2026-07-21

The proven operational signature is:

`GET_KVSTORE_VALUE(store, scope_or_program, matrix, analyte, field)`

The V3 candidate used the unproven six-argument order `store, assay, analyte, matrix, result_unit, selector`. V4 changes the contract to five arguments, takes scope from `Specifications!U3`, takes the runtime matrix from `Specifications!U4`, and permits only terminal field `LOQ` or `MU`.

`Specifications!U5 = ug/g` remains informational. It is not passed to the lookup and is not represented in the V4 store hierarchy. Stored LOQ values are numeric `ug/g`; stored MU values are numeric relative percent. Display-unit conversion remains worksheet-owned.

No Pass/Fail behavior was copied from an operational worksheet.
