# Unqualified-address candidate round-trip result

Classification: **not run - corrected save retry pending**

The qualified-address native-envelope candidate rendered correctly, but QBench
rejected **Save As New Version** before a version could be established. The
new unqualified-address candidate was regenerated and validated locally only.

Consequently:

- no corrected Draft row is claimed;
- Export Spreadsheet was not invoked for the corrected candidate;
- no corrected saved/reopened raw export or SHA-256 exists;
- semantic saved-export comparison was not run;
- `json_import_saved_definition_contract=unproven`;
- `json_import_round_trip=not_run`;
- `destination_contract_proven=false`.

Atomicity remains `api_patch_unresolved` and the analyte PATCH-key contract
remains `unresolved`.
