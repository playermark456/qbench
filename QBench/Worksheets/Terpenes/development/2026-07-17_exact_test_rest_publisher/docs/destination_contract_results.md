# Saved 43-field destination-contract proof

Date: 2026-07-17

Final result: **not proven; paused before the first token request**.

## Local proof inputs and results

The controlled mapping contains exactly 43 ordered, unique destinations: 23
reportable analytes and 20 approved calculation/source/control inputs. It maps
no Pass/Fail field, Dimethylacetamide result, or Peak Table value.

| Worksheet input | SHA-256 | Structural result | Saved proof result |
|---|---|---|---|
| Prompt 3 Test Worksheet candidate | `90686b980882b221008f281be33984dc5232e2f3d2632300db3f4a27b529640a` | 43 present, 43 unique, 43 writable, zero formula-owned targets | Failed: saved/reopened Sandbox provenance missing |
| Active Test Worksheet Export Spreadsheet dated 2026-06-30 | `2ebae7a36e95038777f116a7d8ce821009841e39f6a9f338e552eba90c096138` | Zero current destinations found | Failed |

Mapping SHA-256:
`180665ba85142638de0df6a2db64be856aa3b24be274f37b7082468e4d68d331`.

No passing proof JSON was written, and publisher configuration remains locked
with `destination_contract_proven: false`.

## Required saved-export provenance

After saving and reopening the exact task-created synthetic Test Worksheet in
QBench Sandbox, use QBench's **Export Spreadsheet** action. Create a local,
ignored provenance JSON beside that export with these fields:

```json
{
  "sandbox_hostname": "ait-sandbox.qbench.net",
  "export_action": "Export Spreadsheet",
  "saved": true,
  "reopened": true,
  "synthetic_only": true,
  "export_sha256": "<sha256-of-exact-export-file>",
  "worksheet_display_name": "SBX_ONLY_<task-worksheet-name>"
}
```

Then run the local-only proof command. It writes the proof artifact only when
the export, mapping, writability metadata, and provenance all pass:

```text
python terpenes_publisher.py prove-destination --worksheet-export <saved-export.json> --provenance <provenance.json> --output <proof.json>
```

The resulting proof file and its SHA-256 must then be locked in
`publisher_config.json`. This step still makes no token or QBench API request.
