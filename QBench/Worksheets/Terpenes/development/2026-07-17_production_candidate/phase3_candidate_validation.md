# Phase 3 Terpenes local candidate validation

`calculation_contract = passed_authoritative_method_documentation_and_user_approved_reporting_rules`

## Candidate results

- Test candidate: `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v1.json`
- Test SHA-256: `275c8058cd597cfc688121bbdf50d1189897a088f455ff9e00e79a3fdf781a44`
- Test tabs: Report, Data, Specifications
- Test dimensions: {'Report': (23, 5), 'Data': (40, 26), 'Specifications': (23, 21)}
- Test named cells: 44 (43 writable destinations plus `report_results`).
- Test formulas: 309; every formula cell is protected/formula-owned.
- Batch candidate: `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS__v1.json`
- Batch SHA-256: `7c96c9e8bb300f5886a4f66971c6c22c3ae72ee9225134f737d6601a0bbc55b2`
- Batch tabs: Run Setup, Instrument Import, Batch Review, Test Transfer
- Batch dimensions: {'Run Setup': (25, 3), 'Instrument Import': (201, 57), 'Batch Review': (45, 24), 'Test Transfer': (87, 56)}
- Batch named cells: 67.
- Batch formulas: 1180; AF/AG formula ownership passed for 200 rows.

## Calculation and mapping results

- Calculation-vector rows: 41.
- Combined component cases: 15.
- Synthetic Total Terpenes: 1040 ug/g.
- Mapping rows: 25 = 23 internal channels + 2 audit-only rows.
- Unique reportable measurands: 21.
- Missing/blank/no-peak/zero/negative component preprocessing passed.
- Positive component retention, combined LOQ, single-positive MU, two-positive MU, missing-positive-MU, and strict-above Total inclusion passed.
- No component-channel LOQ lookup exists.

## Safety results

- JSON syntax, tab order, dimensions, synchronized data, formulas, named targets, and formula ownership passed.
- No Pass/Fail artifact, credential, URL, signed URL, source UUID, internal production identifier, QBench API instruction, or customer value was retained.
- No QBench environment was accessed. No worksheet was imported, approved, activated, or published.
- Sandbox saved-definition and runtime validation remain the next controlled phase.
