# Phase 4B.1 AF/AG runtime results

Date: 2026-07-21

AF and AG were not edited. They recalculated from the sanitized parser-writable inputs and persisted after save/reopen.

| Row alias | Category | AF status | AG message | Transfer category |
| --- | --- | --- | --- | --- |
| SBX_NULL_A | Null | Rejected | Sample type required | excluded |
| SBX_BLANK_A | Blank | Valid | Import row valid | excluded control |
| SBX_STD_A | Standard | Valid | Import row valid | excluded control |
| SBX_CCV_A | CCV | Valid | Import row valid | excluded control |
| SBX_LOQ_A | LOQ | Valid | Import row valid | excluded control |
| SBX_QC_A | QC | Valid | Import row valid | excluded control |
| SBX_SAMPLE_A | Sample A | Valid | Import row valid | included sample candidate |
| SBX_SAMPLE_B | Sample B | Valid | Import row valid | included sample candidate |

- Integration review was complete for all populated import rows.
- Dimethylacetamide remained audit-only.
- No control row became a customer analytical result.
- No Pass/Fail was generated.

`batch_v2_af_ag_manual_probe = passed`
