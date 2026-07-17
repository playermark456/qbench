# Prompt 4.6C No-Code File Parser fallback

This package implements the controlled normalized-input fallback for the
Terpenes Batch Worksheet in `https://ait-sandbox.qbench.net/`.

Status: the isolated worksheet, parser, finders, canonical fixture, malformed
fixtures, sanitized exports, local validations, and controlled Sandbox runtime
checks are complete. A normal browser was used only to choose the four local
attachments; all parser jobs and persisted worksheet states were then inspected
in the Sandbox.

```text
Output_redacted_fixture.txt
    -> Prompt 4.5 local LabSolutions parser and typed wide-row adapter
    -> SBX_ONLY_TERPENES_WIDE_IMPORT_01.txt
    -> QBench No-Code File Parser
    -> Batch Instrument Import row
```

QBench does not parse the raw sectioned LabSolutions ASCII file in this
workflow. Local normalization remains an operational requirement.

## Controlled fixture

`normalized_fixture_generator.py` invokes the GitHub-controlled Prompt 4.5
parser and adapter and writes one deterministic two-line TSV with 57 logical
columns A:BE. AF and AG are blank source placeholders; AH:BD contain 23 plain
numeric analyte values; BE contains the Prompt 4.5 source-row hash.

- Fixture: `SBX_ONLY_TERPENES_WIDE_IMPORT_01.txt`
- SHA-256: `7abbcc188ff35ba09908cdfefd917da28d5d194e6f4031f77aad7c0d06b108d2`
- Source-row hash: `cef4d2a0c117ae168d6431c3e918668870546c6d165e36fc5f971515249f4546`
- Compound Results rows: 24
- Peak Table rows: 34
- Reportable analytes: 23
- Dimethylacetamide: numeric, audit-only

The generator also writes the controlled A:AE and AH:BE source blocks plus two
exact-filename malformed fixtures used only on disposable failure-test Batches.

## Sandbox design

The isolated worksheet is
`SBX_ONLY_TERPENES_2026_07_16_No_Code_Batch_Import`. It has Run Setup,
Instrument Import, QC Review, and Publish tabs. Its active version preserves the
Instrument Import AF/AG formulas and has no assay assignment.

The isolated No-Code parser is
`SBX_ONLY_TERPENES_2026_07_16_No_Code_Wide_Import`. One parser safely accepted
two non-overlapping finders: A2:AE2 to `Instrument Import!A2` and AH2:BE2 to
`Instrument Import!AH2`. AF and AG are excluded.

See `sandbox_validation_results.md`, `duplicate_upload_results.md`, and
`failure_results.md` for runtime results. The package does not introduce a
Terpenes Pass/Fail artifact, does not write Publish or Test Worksheet data, does
not implement Prompt 5 automation, and is not production-ready.
