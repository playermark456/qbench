# Phase 4A.6 Test save/reopen

The verified Dynamic Spreadsheet Version 1 was directly approved and activated without a review lock. The worksheet object was enabled as Active, and the isolated V4 Key/Value Store association persisted after reopen.

Fresh collision-free runtime objects were created:

- Assay: `SBX_ONLY_TERPENES_RUNTIME_ASSAY_V4_DYNAMIC`
- Sample: `SBX_ONLY_TERPENES_RUNTIME_SAMPLE_V4_DYNAMIC`
- Sample type: Cannabis/Hemp
- Product matrix: Cannabis Concentrates
- Test count: exactly one
- Test state: NOT STARTED

The Assay was saved, reopened from the Assays list, and retained only the verified V4 Dynamic Spreadsheet as its Test Worksheet. Batch Worksheet, Test Protocol, Batch Protocol, and Customer Portal visibility remained unset or disabled.

The fresh Test instantiated Report, Data, and Specifications. One normal Tests-list reopen was performed for the permitted Key/Value retry. Matrix and scope values persisted, but required Alpha-Pinene lookup values remained blank.

No analytical input was entered and the Test worksheet was not saved after analytical entry. The 43-field persistence phase was therefore not run.

`test_list_reopen = passed_single_permitted_retry`

`test_save_reopen = not_run_required_kv_lookup_blank`
