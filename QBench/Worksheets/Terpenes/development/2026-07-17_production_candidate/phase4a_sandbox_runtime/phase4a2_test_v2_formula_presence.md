# Phase 4A.2 Test v2 formula presence

Date: 2026-07-21

## Inspection method

The exact pre-hashed candidate supplied the authoritative formula strings. The authenticated visual editor supplied the rendered formula-driven states before save and after reopen. The legacy editor did not expose formula text reliably in its visible formula bar, so this evidence does not claim that the browser displayed the strings themselves.

The saved re-export preserved every formula in each worksheet's embedded `data` representation: 86 on Report, 0 on Data, and 223 on Specifications.

## Representative formulas

| Requirement | Cell | Formula presence and reference result |
| --- | --- | --- |
| Direct analyte mg/g conversion | `Specifications!D2` | `=IF(ISNUMBER(C2),C2/1000,"")` |
| Direct analyte percent conversion | `Specifications!E2` | `=IF(ISNUMBER(C2),C2/10000,"")` |
| Direct analyte LOQ lookup | `Specifications!F2` | Present; guarded `GET_KVSTORE_VALUE` lookup |
| Direct analyte MU lookup | `Specifications!G2` | Present; guarded `GET_KVSTORE_VALUE` lookup |
| Nerolidol combination | `Specifications!C19` | `=M19+N19` |
| Ocimene combination | `Specifications!C20` | `=M20+N20` |
| Combined Nerolidol MU | `Specifications!G19` | Present; weighted uncertainty formula using M19, N19, O19, and P19 |
| Combined Ocimene MU | `Specifications!G20` | Present; weighted uncertainty formula using M20, N20, O20, and P20 |
| Total Terpenes | `Specifications!C23` | Present; LOQ-aware sum across rows 2 through 22 |
| Report-to-Specifications reference | `Report!B2` | `=SPECIFICATIONS!I2` |

The formulas use the visible `DATA`/`SPECIFICATIONS` tab references accepted by the old Sandbox renderer. No formula cell was edited, and no Key/Value Store fixture was created or changed.
