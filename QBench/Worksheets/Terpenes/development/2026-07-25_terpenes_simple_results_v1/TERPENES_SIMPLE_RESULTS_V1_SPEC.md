# Terpenes Simple Results V1 specification

## Status boundary

This directory is an isolated, local-only development package. It does not authorize or perform a QBench, Sandbox, Production, browser, network, Git, GitHub, or pull-request action.

Parser 41, worksheet 78, BATCH-61, Tests 308/309, attachment 53, job 65, the deployed V2/V3 parser artifacts, the existing production-candidate worksheet, and the immutable C6 input remain preserved diagnostic evidence.

## Architectural pivot

Simple Results V1 mirrors the proven Cannabinoid Potency persistence boundary:

- one parser-owned Batch worksheet tab named exactly `Results`;
- one `QBBatchService` construction;
- one `QBBatchService.update` call;
- one `qb_dynamic_spreadsheet_data` key, `Results`;
- no cross-tab read or write;
- no Test service or direct Test mutation;
- no second Batch update;
- one read-after-write retrieval before success.

## Results contract

The worksheet contains exactly 87 rows and 51 columns (`A:AY`).

QBench worksheet exports encode `minDimensions` as `[columns, rows]`. The
Sandbox-ready candidate therefore uses:

```text
minDimensions = [51, 87]
```

The original diagnostic candidate is preserved at
`SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V1.json`, SHA-256
`ce50d670be71fccf02912b30cacb918fd48916e8f154a164b095f8f0670a96be`. It
contains the incorrect `minDimensions = [87, 51]`.

The corrected import candidate is
`SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V1__dimension_fix.json`, SHA-256
`f8d58b33024cce2bf90171df79c7f73e984674fa64b83f99e8030935f9030448`. Its
only semantic differences from the original are the two ordered scalar values
at `config.worksheets[0].minDimensions`: index 0 changes from `87` to `51` and
index 1 changes from `51` to `87`. The files have equal length and differ at
exactly four byte offsets: `614306`, `614307`, `614320`, and `614321`.

Persistent validation requires exactly one `Results` worksheet, 51 configured
columns ending at `AY`, 87 configured rows ending at row `87`, exactly 51
headers, and no cell, data, style, formula, image, reference, or named-cell
address beyond `AY87`.

Rows 2:87 use normal QBench Batch dynamic context:

- A `Sample ID`: `${tests[i].sample.get_display_id()}`
- B `Test ID`: `${tests[i].get_display_id()}`
- C `Product Matrix`: `${tests[i].sample.product_matrix}`

Columns A:C are context-owned and never written by the parser. Columns D:AY are parser-owned only for a uniquely matched candidate row. Unmatched rows are not cleared or rewritten.

The exact header vector is:

`Sample ID`, `Test ID`, `Product Matrix`, `LabSolutions Sample Name`, `Sample Type`, `Vial`, `Sample Amount`, `Dilution Factor`, `DF Application Mode`, `α-Pinene`, `Camphene`, `β-Myrcene`, `(-)-β-pinene`, `Delta-3-carene`, `α-Terpinene`, `cis-Ocimene`, `d-Limonene`, `p-Cymene`, `trans-Ocimene`, `Eucalyptol`, `γ-Terpinene`, `Terpinolene`, `Linalool`, `(-)-Isopulegol`, `Geraniol`, `β-Caryophyllene`, `α-Humulene`, `cis-Nerolidol`, `trans-Nerolidol`, `(-)-Guaiol`, `Caryophyllene Oxide`, `(-)-α-Bisabolol`, `Dimethylacetamide`, `Unknown Peak Count`, `Manual Integration`, `Integration Review Status`, `Source Instrument File`, `Source File Hash`, `Source Data File`, `Source Method File`, `Source Sequence File`, `Acquired At`, `Instrument Name`, `Detector ID`, `Detector Name`, `Parser Version`, `Compound Result Row Count`, `Peak Table Row Count`, `Reportable Compound Row Count`, `Source Row Hash`, `Import Status`.

The first candidate has no worksheet formulas, report behavior, portal behavior, pass/fail logic, QC logic, release logic, publication logic, or status formulas.

## Analytical contract

- Input is exactly one UTF-8 `.txt` file.
- Records split only at `[Header]`.
- Every record requires all eight controlled LabSolutions sections.
- Every record requires exactly 24 controlled `Compound Results(Ch1)` rows.
- Quantitation uses only `Compound Results(Ch1) > Conc.`.
- IDs 2:24 are the ordered 23 reportable analytes.
- ID 1, Dimethylacetamide, is retained as audit-only.
- Peak Table rows are inspected for unknown peaks and manual integration.
- Numeric fields reject malformed nonblank values.
- Unicode worksheet analyte labels are retained exactly.
- Dilution Factor is captured; values are not recalculated or double-applied.

## Candidate and control behavior

A transfer candidate must:

1. classify as `Sample`;
2. contain a nonblank LabSolutions `Sample Information > Sample ID`;
3. use that exact Sample ID as the QBench Test display ID;
4. resolve through `/batches/get` to exactly one Batch;
5. resolve to the same Batch as every other candidate;
6. appear exactly once in Results column B or its B-column dollar reference.

`Sample Information > Sample ID` is the sole Test-display-ID source.
`Sample Information > Sample Name` is retained as analytical provenance and is
never interpreted as a Test ID. Runtime Test IDs are fixture/input data, not
parser configuration or hardcoded generic-parser values.

Controlled standards, blanks, system-suitability records, CCVs, LOQ, matrix blanks, nulls, and Low/Medium/High validation records are fully parsed and validated but are not persisted in V1.

## Write and readback contract

The update shape is:

```text
QBBatchService.update({
  data: {
    id: <resolved Batch id>,
    qb_dynamic_spreadsheet_data: {
      Results: {
        WORKSHEET_DATA,
        WORKSHEET_FORMULAS,
        WORKSHEET_IMAGE_DATA,
        WORKSHEET_DOLLAR_REFERENCES,
        WORKSHEET_DATA_PROCESSED
      }
    }
  },
  urlParams: { run_worksheet_calculations: true }
})
```

For each matched row, every D:AY address is explicitly set, including blank source values that must clear stale parser-owned data. A:C and every unmatched row are preserved. Worksheet formulas, images, and dollar-reference maps are forwarded unchanged.

After the update callback succeeds, the parser retrieves the same dynamic Results worksheet and verifies:

- every expected D:AY value;
- numeric equivalence without accepting changed numeric values;
- unchanged A:C context;
- unchanged unmatched rows;
- unchanged formula, image, and dollar-reference maps;
- unchanged unique Test-ID-to-row mapping;
- candidate and verified-row counts.

Any mismatch emits `RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED`. There is no repair update or retry, and `QB.success` is called only after verification passes.

## Staged Sandbox validation example

The isolated Sandbox staging example uses active worksheet `79` version `1`,
active parser `42` version `1`, assay `21`, BATCH-62/internal Batch ID `62`,
Sample AIT-SAMP-170/internal Sample ID `170`, Source Test `310` in Results row
2, and Target Test `311` in Results row 3. These IDs are staged validation data,
not generic parser constants.

The controlled local runtime fixture for that example is
`runtime/terpenes_simple_results_310_311_runtime_source.txt`, SHA-256
`1e5087715a9bcf216c2991cca53f41fb4ae84b4f9e80eea0e95d7618ec77a36e`.
Its only changes from the immutable diagnostic C6 input are the Sample IDs
`308 -> 310` for P1 and `309 -> 311` for P2. Configuring the parser trigger and
filename, uploading this file, and executing the parser remain separate,
explicitly authorized Sandbox actions.

## Self-contained focused-test contract

The main-based package runs the V1 focused suite without the historical
`2026-07-15_qbench_native_parser_probe` tree. The committed 310/311 runtime
fixture is the only persistent analytical fixture. The historical 308/309
form is derived in memory by reversing only the P1 `310 -> 308` and P2
`311 -> 309` Sample ID substitutions, and the derived bytes must retain
SHA-256 `5de17d8f9eb21a8dfc068daf2297efb707a8b783f63393df432781e5e692e6aa`.
No derived file is written. All persistent V1 fixture paths are asserted to
remain inside this V1 directory.
