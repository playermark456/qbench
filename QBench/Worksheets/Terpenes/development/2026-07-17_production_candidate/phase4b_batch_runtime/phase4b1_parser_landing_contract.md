# Phase 4B.1 parser landing contract

Date: 2026-07-21

For Instrument Import rows 2:201:

- Writable metadata region: A:AE.
- Formula-owned validation region: AF:AG.
- Writable analyte/audit region: AH:BE.

Validation results:

- AF and AG contained formulas for all intended rows and rendered readonly.
- Adjacent intended parser cells rendered writable.
- No parser target included AF or AG.
- No parser-writable cell contained a formula.
- No formula-owned cell was included in the parser target map.
- No validation/protection setting made an intended parser destination nonwritable.
- The Phase 4B.1 manual probe used two bounded pastes, A:AE and AH:BE; AF/AG were not edited.
- No parser was created or uploaded.

`batch_v2_parser_landing_contract = passed`
