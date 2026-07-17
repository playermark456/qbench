# Corrected-candidate round-trip result

Classification: **not run - corrected candidate not uploaded**

The prior wrong-worksheet, collapsed-renderer import is invalid and is not a
round-trip result. The corrected native-envelope candidate was validated only
in the repository. Consequently:

- no corrected Draft row exists;
- Export Spreadsheet was not invoked for the corrected candidate;
- no raw corrected round-trip JSON or SHA-256 is claimed;
- semantic corrected-candidate-versus-export comparison was not run;
- `json_import_saved_definition_contract=unproven`;
- `json_import_round_trip=not_run`;
- `destination_contract_proven=false`.

Atomicity remains `api_patch_unresolved` and the analyte PATCH-key contract
remains `unresolved`.
