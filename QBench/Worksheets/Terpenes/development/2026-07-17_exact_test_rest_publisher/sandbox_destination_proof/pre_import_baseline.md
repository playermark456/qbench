# Pre-import destination-contract baseline

Captured before any QBench Sandbox import or save on 2026-07-17.

## Source locks

- Prompt 3 Test Worksheet candidate SHA-256:
  `90686b980882b221008f281be33984dc5232e2f3d2632300db3f4a27b529640a`
- Prompt 5B field mapping SHA-256:
  `180665ba85142638de0df6a2db64be856aa3b24be274f37b7082468e4d68d331`
- Expected logical destinations: 43.
- Expected writable destinations: 43.
- Candidate structural issues: 0.
- Candidate named-cell systems: 91.
- Duplicate named-cell references: 0.
- Surrounding formula count: 265.
- Canonical surrounding-formula manifest SHA-256:
  `f149f36e2892eda5c72dddc9cf281e749df5c5313fceb58b140dae639581e910`

The exact logical destination names, QBench named-cell systems, addresses,
expected runtime value types, and non-formula/writability expectations are in
`expected_destination_contract.csv`.

## Range representation

The first 23 logical destinations are the 23 scalar positions
`Data!D2:Z2` under the single QBench named-cell range
`terpenes_instrument_conc`. The other 20 destinations are scalar named cells.
This baseline proves worksheet persistence only; it does not resolve whether
the REST PATCH contract uses indexed scalar keys or one range value.
`analyte_patch_key_contract` therefore remains `unresolved`.

## Prohibited destinations

- No mapped destination is Pass/Fail or a Test result.
- Dimethylacetamide is an audit value only and is not a reportable destination.
- Peak Table data is not mapped as a reportable result.
- All 43 target cells are expected to be writable and non-formula-owned.
