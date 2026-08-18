# Automation Cascade Analysis — 2026-08-16 Production Snapshot

## Evidence boundary

This analysis separates four evidence levels:

1. **Observed** — fields displayed on the read-only production configuration pages and preserved in `Automations/automation_*.csv`.
2. **Source-observed** — behavior visible in captured parser/report source.
3. **Repository evidence** — historical native worksheet exports and canonical documentation.
4. **Inference / hypothesis** — plausible runtime behavior that was not executed during this scan.

No automation or parser was run, and no history page or operational record was opened.

## Broad trigger surface

All 16 automations use `Data Modified`. Thirteen are active:

- 12 active Batch automations: IDs 1, 3, 4, 6, 8–14, and 17.
- 1 active Test automation: ID 16.
- 0 active Sample automations.
- 0 active Batch Object Protocol Step automations; ID 15 is configured for that type but inactive.

Each active Batch automation writes one or more worksheet fields across Tests in the Batch. The displayed action label is `Set value on all Test Worksheets within the Batch` except automation 3 action 5, which displays `Set value on all Samples Test Worksheets within the Batch`. The UI does not expose whether an unchanged write is suppressed, whether every broad trigger creates a history row, or whether condition evaluation itself is logged.

## Observed write map

| Automation | Trigger restriction | Observed destinations | Fan-out surface |
|---|---|---|---|
| 17 Terpenes | Worksheet 43 | `terpenes_instrument_conc_01..23`, `sample_mass_g`, `df`, `df_application_mode` | All Test worksheets in the Batch |
| 16 Homogeneity pull | Homogeneity assay and status transition into `Ready for Homogeneity Pull` | `mg_serving_1` | One Test worksheet |
| 14 AC/EB/YM | Worksheet 89 | `ac_results`, `eb_results`, `ym_results` | All Test worksheets in the Batch |
| 13 Listeria | Worksheet 86 | `lis_results` | All Test worksheets in the Batch |
| 12 Salmonella/STEC | Worksheet 82 | `salmonella_results`, `stec_results` | All Test worksheets in the Batch |
| 11 Potency | Cannabinoid Potency assay and worksheet 7 | `result_1..29`, `df` | All Test worksheets in the Batch |
| 10 Pesticides quantitative | Worksheet 13 | `pest_quantitative_results` | All Test worksheets in the Batch |
| 9 Aspergillus | Worksheet 80 | four species-result fields | All Test worksheets in the Batch |
| 8 Pest/Myco qualitative | Worksheet 15 | `pesticides_results`, `mycotoxin_results`, `df` | All Test worksheets in the Batch |
| 6 Residual Solvents | Worksheet 11 | `residual_solvents_results`, `df` | All Test worksheets in the Batch |
| 4 Water Activity | Worksheet 29 | `wateractivityaw` | All Test worksheets in the Batch |
| 3 Mycotoxin quantitative | Worksheet 9 | five toxin fields | Four all-Test actions plus one all-Samples-Test action |
| 1 Heavy Metals | Worksheet 5 | four metals and `df` | All Test worksheets in the Batch |

Inactive IDs 2, 5, and 15 overlap active Heavy Metals or Water Activity paths. IDs 5 and 15 have a destination field but no visible source expression.

## Observed and inferred cascade chains

### Terpenes

1. **Source-observed:** active parser 50 resolves candidate Test display IDs to exactly one Batch, updates the dynamic Batch `Results` worksheet through `QBBatchService.update`, requests worksheet recalculation, and reads the result back.
2. **Observed:** automation 17 watches worksheet 43 and selects one row per Test display ID from `B2:AY87`.
3. **Observed:** automation 17 writes 26 Terpenes Test-worksheet fields.
4. **Observed:** report 26 renders the Terpenes Test worksheet through `report_results`.
5. **Inference:** a successful parser 50 write can therefore cause Batch automation evaluation, Test writes, further Test-level automation evaluation, and changed report output. Runtime ordering and exact event emission were not tested.

Parser 50's source begins with an `SBX_ONLY` marker despite being active in production. That marker is not a runtime safeguard.

### Cannabinoid Potency and Homogeneity

1. **Source-observed:** active parser 46 writes the dynamic Potency Batch `Results` worksheet.
2. **Observed:** automation 11 copies 29 result fields and `df` to Potency Test worksheets.
3. **Observed:** automation 16 runs only when a Homogeneity Test status changes into `Ready for Homogeneity Pull` and pulls `mg_serving_1` from `Potency Results Lookup`.
4. **Observed:** report 26 reads generic `pass_fail`/THC values and renders `report_results`; report 44 reads Homogeneity/Potency worksheet values directly.
5. **Inference:** parser 46 and automation 11 prepare the data later consumed by the status-gated Homogeneity pull. The status transition is a separate observed guard, so the chain is not asserted as fully automatic.

### Other instrument/batch paths

- **Strong inference:** parser 47 (active, Pesticides Batch Worksheet target) feeds worksheet 15, which automation 8 watches.
- **Strong inference:** parser 41 (active, Heavy Metals Batch Worksheet target) feeds worksheet 5, which automation 1 watches.
- **Unverified:** inactive Heavy Metals parsers 22/25 could feed the same path if reactivated.

The exact No-Code finder-to-cell mappings were not exposed without Edit and are therefore not stated as direct observations.

## Potential loops, fan-out, and history volume

- A Batch write can make every active Batch `Data Modified` automation eligible for evaluation; worksheet/assay conditions should narrow actions, but evaluation/history behavior is not exposed.
- The 12 active Batch automations target all Tests in a Batch. One source write can therefore fan out to many Test worksheet writes.
- Those Test writes can make Test `Data Modified` automation 16 eligible for evaluation. Its before/after status-transition condition should block unrelated Test updates, but whether blocked evaluations still create history is unknown.
- Automation 16 writes a Test worksheet field under a Test `Data Modified` trigger. Its status-transition condition is a visible loop guard for the captured action, but self-retrigger/no-op behavior remains unverified.
- Formula-based row selection is deterministic only if the lookup key is unique. No automation exposes an explicit duplicate-match or exactly-one-match check.
- Several XLOOKUP actions write the literal fallback `not found`. VLOOKUP-based actions expose no comparable error handling. How lookup errors affect partial action execution is unknown.
- Retry, transactionality, rollback, action atomicity, action ordering guarantees, and duplicate history suppression are not exposed.

## Repository-confirmed mapping defects and remaining reconciliation

- **Confirmed against tracked active worksheet exports — automation 1:** Batch worksheet 5 has Mercury in column G and Lead in H, while Test worksheet 6 exposes `lead` and `mercury` as distinct named cells. The active actions send lookup column 6 (G/Mercury) to `lead` and column 7 (H/Lead) to `mercury`, reversing the two results. The differing `B19:H60` and `B15:H60` row starts both include the worksheet's sample rows and are not the confirmed defect.
- **Confirmed against tracked active worksheet exports — automation 6:** Batch worksheet 11 has 19 analytes in E:W, and Test worksheet 12 defines `residual_solvents_results` as `Data!E2:W2`. The active action returns only `E11:U96` (17 cells), omitting Total Xylenes and Trichloroethene. `df` from D is aligned.
- **Confirmed against tracked active worksheet exports — automation 11:** Batch worksheet 7 places Unknown Peak 2 at lookup column 24 and Unknown Peak 3 at column 25; Test worksheet 8 maps `result_21` and `result_22` to Unknown Peaks 2 and 3. Active actions 21–22 use columns 25 and 24 respectively, reversing those two results. The other `result_1..29`/`df` mappings align with the tracked worksheet headers.
- **Likely mismatch requiring a current export — automation 10:** the active destination `pest_quantitative_results` does not exist in the complete tracked 2026-07-04 worksheet exports. Tracked Test worksheet 16 instead defines `pesticides_results` as `Data!E2:BU2`, whose 69-cell width matches the action's Batch worksheet 13 return range `D34:BT200`. Obtain the current native worksheet 16 export before changing the destination.
- Automation 3 action 5 has a different fan-out label from its first four actions.
- Automation 14 watches shared worksheet 89 while current assay metadata binds TYMC's batch worksheet to 94; the intended shared-vs-assay-specific relationship is unresolved.
- Automation 3's quantitative Mycotoxin path should be reconciled to the current assay binding.
- Current named-cell/range compatibility beyond the four comparisons above cannot be certified because Phase 2 native worksheet exports are blocked.

## Stability and notification findings

No date-driven or scheduled automation, notification role, or stability-pull automation was exposed among the 16 automation objects. The Phase 5 settings cross-check found only these stability anchors: assay 13, the Sample fields `Stability Required`, `Stability Pull Date`, and `Storage Bin`, and active Alert email template 51 (`Stability Due`) with no saved version and empty source. Multiple pulls, 3/6/12-month interval representation, scheduling, reminder timing, recipient roles, and the underlying stability-record model remain unable to verify read-only. No stability records or operational alerts were opened.
