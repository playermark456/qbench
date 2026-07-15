# Terpenes QC requirements crosswalk

Date: 2026-07-14

Repository search did not find a separate controlled Terpenes SOP, Analysis Form, or validation document file beyond the Terpenes source package and Prompt 2 configuration. This crosswalk therefore uses the controlled repository sources available in this snapshot and records unresolved source gaps explicitly.

## Sources checked

- `QBench/Worksheets/Terpenes/development/2026-07-14_config_parser_foundation/config/terpenes_qc.json`
- `QBench/Worksheets/Terpenes/source/terpenes_worksheet_spec_v3.json`
- `QBench/Worksheets/Terpenes/source/labsolutions_ascii_integration_spec.md`
- `QBench/Worksheets/Terpenes/source/terpenes_codex_build_brief_v3.md`
- `QBench/Worksheets/Terpenes/docs/terpenes_current_state_gap_analysis.md`

## Crosswalk

| QC item | Source document | Source section or field | Configured criterion | Confirmed? | Worksheet implementation | Blocks batch publication? | Unresolved discrepancy |
|---|---|---|---|---|---|---|---|
| Calibration correlation | `terpenes_qc.json`; `terpenes_worksheet_spec_v3.json` | `calibration_r_min` | r >= 0.99 | Yes, from Prompt 2 config | QC table Calibration r evaluation | Yes, through QC data/review gates | None in repository evidence |
| Initial CCV accuracy | `terpenes_qc.json`; `terpenes_worksheet_spec_v3.json` | `initial_ccv_accuracy_percent_window` | 85 to 115 percent | Yes, from Prompt 2 config | QC table Initial CCV Recovery Evaluation | Yes | None in repository evidence |
| Initial CCV triplicate RSD | `terpenes_qc.json`; `terpenes_worksheet_spec_v3.json` | `initial_ccv_rsd_max_percent` | <= 10 percent | Yes, from Prompt 2 config | QC table Initial CCV RSD Evaluation | Yes | None in repository evidence |
| Blank response/fraction of LOQ | `terpenes_qc.json`; `terpenes_worksheet_spec_v3.json` | `blank_max_fraction_of_loq` | <= 0.2 of LOQ | Yes, from Prompt 2 config | QC table Blank Evaluation | Yes | None in repository evidence |
| LOQ recovery | `terpenes_qc.json`; `terpenes_worksheet_spec_v3.json` | `loq_recovery_min_percent`, `loq_recovery_max_percent` | 70 to 130 percent | Yes, from Prompt 2 config | QC table LOQ Evaluation | Yes | Final sample below-LOQ reporting remains Prompt 3/Test Worksheet scope |
| Matrix-spike recovery | `terpenes_qc.json`; `terpenes_worksheet_spec_v3.json` | `matrix_spike_recovery_min_percent`, `matrix_spike_recovery_max_percent` | 85 to 115 percent | Yes, from Prompt 2 config | QC table Matrix Spike Evaluation | Yes | None in repository evidence |
| Duplicate difference | `terpenes_qc.json`; `terpenes_worksheet_spec_v3.json` | `duplicate_difference_max_percent` | <= 20 percent | Yes, from Prompt 2 config | QC table Duplicate Evaluation | Yes | None in repository evidence |
| Bracketing CCV accuracy | `terpenes_qc.json`; `terpenes_worksheet_spec_v3.json` | `bracketing_ccv_accuracy_percent_window` | decision required | No | `bracketing_ccv_criterion_status` permits only `decision_required` or `confirmed`; bracketing evaluation returns `decision_required` until confirmed with a numeric window greater than zero | Yes | SOP text reportedly says 10 percent; Analysis Form reportedly says 15 percent. Prompt 4 does not choose. |
| Retention-time drift | `terpenes_qc.json`; `terpenes_worksheet_spec_v3.json` | `rt_drift_window_min` | <= 0.5 min | Yes, from Prompt 2 config | QC table Retention Time Evaluation | Yes | None in repository evidence |
| Resolution | `terpenes_qc.json`; `terpenes_worksheet_spec_v3.json` | `resolution_min` | >= 1.0 | Yes, from Prompt 2 config | QC table Resolution Evaluation | Yes | None in repository evidence |
| LCS requirement | Repository search | No controlled Terpenes LCS criterion found | Unresolved | No | `lcs_requirement_status = decision_required`; no LCS acceptance formula or invented LCS limit added | Yes, through `qc_configuration_complete` | Missing repository evidence does not resolve the LCS requirement. If a controlled source later says LCS is required, `lcs_requirement_status = required` must continue to block release until acceptance criteria and worksheet implementation exist. If a controlled source later says LCS is not required, the crosswalk must identify the approved source and reviewer decision before `not_required` may be used. |

## Release-gate summary

The default batch cannot release because the bracketing CCV criterion and LCS requirement status are unresolved. `qc_configuration_complete` remains false, `batch_qc_disposition` defaults to `Hold`, and `batch_publish_ready` remains false.

The worksheet also treats calibration r as physically bounded by `calibration_r_min <= value <= 1.0`, and treats initial CCV RSD, blank fraction of LOQ, duplicate difference, and RT drift as physically nonnegative metrics. Negative values in those fields are outside criteria, not within criteria.
