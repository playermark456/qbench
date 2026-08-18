# Open Questions — 2026-08-16 Rescan

The authentication and controlling-SOP availability questions recorded at the original stop checkpoint are resolved:

- `authentication_completed_manually_by_user = true`
- `Terpene Analysis SOP v 1.4.docx` is available and controls the Phase 6 crosswalk.

New configuration questions will be appended as the production inventory proceeds.

## Phase 2 worksheet questions

- Can the user provide the 161 required native **Export Spreadsheet** JSON files through a user-assisted download queue? The visible native control did not produce a downloadable file through the available authenticated browser tooling. No substitute format or reconstructed JSON is acceptable.
- Why is inactive worksheet ID 149, whose displayed name labels it `SANDBOX_ONLY`, visible in the production tenant, and should it remain there? No version exists and no mutation is proposed.
- Is rejected-only worksheet ID 111 intentionally retained without an active or draft version?
- Is Mycotoxin (Qualitative) worksheet ID 10 approved non-active v27 intentionally awaiting activation while v28 remains draft?
- Are the 15 newer `[AIT-88]` / METRC-related drafts and Homogeneity draft v17 intended for coordinated activation? Their automation/report cascade must be examined in later phases before any recommendation.
- Current native definitions are required before canonical named-cell, formula, worksheet-structure, and rendering indexes can be asserted as current. Until then, the 2026-07-04 exports remain historical evidence only.

## Phase 3 configuration questions

- Is Terpenes protocol ID 9 intentionally empty and intentionally unassigned from Terpenes assay ID 8?
- Should Cannabinoid Potency calculation/reporting step 21 (worksheet 39) be assigned to protocol 4? No QBench change is proposed.
- Why does the final overall chemist review step 23, used by 12 protocols, point to active worksheet object 41 when worksheet 41 has no version?
- Is protocol 12 intentionally assigning step 83 to worksheet 151 when worksheet 151 has only draft version 1 and no active version?
- Are the duplicate-name/same-worksheet Quality Control definition step 20 and unassigned patch-preparation steps 74–76 intentionally retained outside protocol 4? Steps 19 and 20 have different descriptions/SOP-section references despite sharing the displayed name and worksheet 38.
- Are protocol IDs 8, 15, and 16 intentionally not assigned on their semantically matching assay pages?
- Which field-definition attributes can be exported through a native read-only mechanism? Data type, validation, formula, option source, KV linkage, and usage were available only behind prohibited Edit controls.
- Do repeated ordered keys in the Pesticides, Residual Solvents, Water Activity, Microbial, METRC mapping, and Terpenes stores intentionally encode multi-value position semantics? The scan preserved every occurrence and did not collapse them.
- Current native worksheet exports are still required to determine whether active worksheets embed stale KV-store values or require new versions to adopt the 2026-07-27 Terpenes store.
- Do the active Pesticides quantitative and microbial worksheets contain the current `Abamectin` key and current 25 g HDCP pathogen limits, or do they retain the differing July embedded values?
- Before any reactivation, should General Microbial Analysis worksheet 44 be aligned with the current Microbial store? Its historical formulas use legacy `mu` and `Limit of Quantification` keys while the current store exposes `MU` and `LOQ`, and its historical embedded KV configuration is empty.

## Phase 4 automation, parser, report, and template questions

Evidence correction: the preliminary viewport/DOM email-source capture was rejected because CodeMirror text was duplicated/truncated. Full-editor Select All recapture and independent validation found all 14 approved-active email v1 sources Jinja-balanced with exact inventory hashes. The earlier “12 malformed sources” finding must not be used.

- Why is parser 50 active in production while its captured source begins with an `SBX_ONLY` marker? Are inactive probe parsers 48 and 49 intentionally retained in production?
- Has the active parser 50 → worksheet 43 → automation 17 → Terpenes Test contract been validated against the current active worksheet versions? No parser or automation was run here.
- When can the three mapping defects confirmed against tracked active worksheet exports be corrected and validated in QBench Sandbox? Automation 1 reverses Lead/Mercury, automation 6 omits Total Xylenes and Trichloroethene from its 19-cell destination, and automation 11 reverses Unknown Peaks 2/3 between `result_21` and `result_22`.
- Does the current active Pesticides Quantitative Test worksheet still expose `pesticides_results` rather than automation 10's `pest_quantitative_results` destination? Obtain a current native worksheet 16 export before treating this likely tracked-export mismatch as a confirmed current defect.
- Is automation 14 intentionally based on shared worksheet 89 while current TYMC assay metadata names worksheet 94 as its Batch worksheet?
- Is the quantitative Mycotoxin automation 3 path still operationally associated with a current assay binding?
- Should report 26 v24 include Pesticides Quantitative assay ID 21? Its embedded assay map routes Pesticides ID 4 only.
- Which current Terpenes ranges supply `report_results` and generic `pass_fail`? The 2026-07-04 export defines neither, while report 26 renders the former and uses the latter in tile/overall-status logic.
- Do current Cannabinoid Potency exports define `total_thc_mg_per_serving_report_result` and `total_thc_mg_per_container_report_result`, and do they define report 44's six `report_left_total_*` / `report_right_total_*` fallback names? Report 44 reads direct cells first, so absence of its semantic fallbacks alone is not a runtime defect.
- Should Water Activity expose a `pass_fail` compatibility name for report 26 instead of only `pass_fail_report`, and should Listeria add the `pass_fail` value its report tile reads?
- When will report 44 be aligned to the canonical Homogeneity contract—`pass_fail` for first-page status and `report_results` for the standalone Homogeneity table/page—instead of preferring `homogeneity_metrc` and reconstructing Potency cells directly?
- Should report 44 preserve blanks/pending state rather than rendering literal `0.0` when both direct and semantic Potency lookups are empty?
- Can safe Sandbox/PDF previews verify report 26's four source page breaks and CSS page counter, report 44's automatic-plus-CSS duplicate-page-number risk and unused page-break class, reports 26/44's fixed 8.48–8.5-inch elements, and report 20's 100.311%-wide table against one-inch Letter-page margins?
- How should report 44 resolve `AIT Watermark.png` when its configuration exposes no attachment, which safe filenames correspond to report 26's remaining redacted blob/image references, and are report 26's sample-level `sample_img` plus report 20's all-attachment/signature rendering intentionally scoped?
- What production timezone does QBench apply through `local_time`? The read-only General Settings surface exposed no timezone field.
- Are the newer drafts on all six active label configurations intended for promotion, and is there a native read-only source export for existing active label versions?
- Should the externally loaded Google Fonts URL and `qbench.net` anchor that remain on plain `http://` in all 14 recaptured active email sources be migrated to HTTPS and previewed for compatibility in Sandbox?
- Is active Stability Due email ID 51 intended to function with no saved version and empty source? Where are scheduling, timepoints, recipients, and reminder timing defined?
- Should invoice ID 40 capture provenance be normalized where JSON records `initial_selected` but `template_versions.csv` records `selected_at_capture=false`?
- Are active platemap ID 39 and active macro ID 27 intentionally unversioned and empty?
- What query/design source backs internal reports 31 and 52? The configuration surface exposed none, and neither report was executed.

## Phase 5 controls, resources, inventory, equipment, and settings questions

- Are control IDs 2–4 intentionally associated only by name with Heavy Metals, or is a direct assay/control-group assignment missing? All assay-side batch-control-group fields are null.
- Where are control expected values, acceptance ranges, units, frequency, worksheet/protocol behavior, report usage, automation usage, and failure behavior configured? They were not exposed on the safe read-only tabs.
- Why does control 1 use the field spelling `Concentraiton`, and is any downstream integration dependent on that exact production spelling?
- Is resource group 12 intentionally assigned to Pesticides Quantitative assay 21 while containing zero inventory and zero equipment members?
- Should Terpenes assay 8 have a resource group? None is explicitly assigned.
- When will the Terpenes Analysis Form be corrected under document control so its 5 mL internal-standard preparation record agrees with the controlling SOP v1.4 instruction to bring 5.0 µL dimethylacetamide to 25 mL with ethyl acetate?
- Which approved QBench design should represent the SOP’s calibration levels, QC sequence/frequency, acceptance rules, preparation branches, equipment/inventory checks, integration review, and final approval? Protocol 9 is empty and unassigned, and the parser-to-report path alone does not implement those method controls.
- Are resource groups 6, 10, and 11 intentionally unassigned on assay detail pages, or are their name-based relationships configured elsewhere?
- Which inventory configurations actually enable lot, expiration, storage-location, reorder, and minimum-stock behavior? Field presence alone does not prove behavior.
- Are inventory items 292 and 273 intentionally uncategorized, and should resource-group default quantities be configured? All 105 membership rows had blank `default_quantity`; item 174 also lacked a displayed size and item 292 lacked a displayed category ID.
- Where are equipment required-assignment and availability rules defined? The list, Details, and Schedule Configuration surfaces did not expose them.
- Which schedule assignment is intended for equipment 107? Its UI text was the undelimited `No Maintenance Required Cold Storage Temperature | -70C`, so the safe capture cannot distinguish a single label from a concatenated sentinel plus schedule.
- Why does the Phase 1 navigation/list inventory record 47 Documents while the expanded Document Control Show-All tree exposes 68 unique path/name leaves? Which scope is the canonical object count?
- What approval workflow, review interval, training behavior, template association, and field-definition configuration governs Document Control without opening document contents or identity-bearing workflow records?
- The Specification Module is enabled, but no Specifications/spec-group route appears in visible navigation. What safe read-only route or export is authoritative?
- Can one Sample hold multiple stability pull dates, how are 3/6/12-month intervals represented, how are notifications scheduled, when do reminders fire, which recipient roles are used, and is stability modeled as a separate record, field, or protocol step? Current evidence cannot answer these.

## Managed Interfaces

Sensitive integration configuration was encountered on an authenticated settings page. Details were intentionally omitted. Managed Interfaces remains incomplete pending separate administrative or vendor remediation.

- Scan classification: `status = blocked_metadata_only`; `objects_counted = 4`; `details_retained = 0`; `secret_values_committed = 0`; `reason = sensitive_integration_configuration_encountered`; `rescan_required = only_after_separate_remediation_and_explicit_authorization`.
