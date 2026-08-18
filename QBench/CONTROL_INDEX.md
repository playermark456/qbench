# Control Index

Last verified in the Adams Independent Testing production tenant on 2026-08-16. The four visible controls were active. QBench was treated as strictly read-only.

Row-level evidence is in `QBench/Rescans/2026-08-16/Controls/` and `QBench/Rescans/2026-08-16/Control_Groups/`.

## Controls

| ID | Control | Active | Data field, verbatim | Direct control group | Inventory item assignment |
|---:|---|---|---|---|---|
| 1 | Example Control | Yes | `Concentraiton` | 1 — Example Control Group | None exposed |
| 2 | System Suitability 1 | Yes | `Concentration` | 2 — Heavy Metals - Demo - AMM | None exposed |
| 3 | System Suitability 2 | Yes | `Concentration` | 2 — Heavy Metals - Demo - AMM | None exposed |
| 4 | Blank | Yes | `Concentration` | 2 — Heavy Metals - Demo - AMM | None exposed |

`Concentraiton` is the exact production display text for control 1 and is not corrected in this index.

## Control groups

| ID | Control group | Direct members |
|---:|---|---|
| 1 | Example Control Group | 1 — Example Control |
| 2 | Heavy Metals - Demo - AMM | 2 — System Suitability 1; 3 — System Suitability 2; 4 — Blank |

Members are listed by control ID; the observed UI sequence is not treated as a configured execution order.

All 20 assay detail pages captured in Phase 3 had a null/blank **Batch Control Group** field. This establishes that no direct assay-side batch control-group assignment was exposed; it does not establish that the controls are unused elsewhere.

## Verification boundary

Results, comments, attachments, history, operational usage records, acceptance limits, specifications, reporting behavior, automation dependencies, and control frequency were not inspected or exposed as safe configuration evidence. No control or control-group assignment was changed, and no inventory item was assigned. Phase 5 later stopped at the defined sensitive-data condition described in `SYSTEM_MAP.md`; the stop does not invalidate the control records captured before it.
