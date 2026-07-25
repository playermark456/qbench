# Terpenes Simple Results V2 Controls Specification

## Scope and baseline

This is an isolated, Sandbox-only candidate derived from the proven Simple Results V1 persistence model. V1 parser 42, worksheet 79, BATCH-62, attachment 57, asset 77, and successful job 68 are frozen evidence and are not modified by V2.

V2 retains the V1 boundary:

- one parser-owned worksheet tab named `Results`;
- one `QBBatchService` construction;
- one `QBBatchService.update`;
- exactly one `qb_dynamic_spreadsheet_data` key, `Results`;
- no `QBTestService` and no direct Test write;
- one post-update worksheet retrieval and complete verification before `QB.success()`;
- no Batch Review, release, COA, approval, publication, status, or completion logic.

## Results worksheet

The worksheet has exactly 51 columns (`A:AY`), 190 rows, and `minDimensions: [51, 190]`.

### Dynamic Sample Results

| Range | Ownership | Contract |
|---|---|---|
| `A1:AY1` | fixed worksheet contract | Exact V1 Results header |
| `A2:C87` | QBench dynamic Test/Sample context | Unchanged V1 `tests[0]` through `tests[85]` definitions |
| `D2:AY87` | parser-owned for matched rows only | Exact V1 field meanings; V2 parser-version identity |

Only records classified as `Sample` with a nonblank LabSolutions `Sample ID` are candidates. That ID is the QBench Test display ID. Candidate IDs must be unique, resolve to exactly one Batch each, resolve collectively to one Batch, and appear exactly once in Results column B. The parser preserves `A:C`, writes all `D:AY` fields on matched rows, explicitly writes blanks that clear stale matched-row values, and leaves unmatched rows unchanged.

### Fixed Run Records audit

| Range | Ownership | Contract |
|---|---|---|
| `A88:AY88` | fixed worksheet contract | Blank separator |
| `A89:AY89` | fixed worksheet contract | `A89=Run Records`; `B89=Complete LabSolutions sequence audit`; remaining cells blank |
| `A90:AY90` | fixed worksheet contract | Exact audit header |
| `A91:AY190` | parser-owned | 100-record fixed audit capacity |

Record order maps deterministically: record 1 to row 91, record 100 to row 190. A source with more than 100 complete records fails with `RUN_RECORD_CAPACITY_EXCEEDED` before any service construction or update. Records are never truncated.

The exact audit header is:

| Column | Header | Column | Header | Column | Header |
|---|---|---|---|---|---|
| A | Record Order | R | p-Cymene | AI | Manual Integration |
| B | Record Category | S | trans-Ocimene | AJ | Integration Review Status |
| C | LabSolutions Sample ID | T | Eucalyptol | AK | Source Instrument File |
| D | LabSolutions Sample Name | U | γ-Terpinene | AL | Source File Hash |
| E | Sample Type | V | Terpinolene | AM | Source Data File |
| F | Vial | W | Linalool | AN | Source Method File |
| G | Sample Amount | X | (-)-Isopulegol | AO | Source Sequence File |
| H | Dilution Factor | Y | Geraniol | AP | Acquired At |
| I | DF Application Mode | Z | β-Caryophyllene | AQ | Instrument Name |
| J | α-Pinene | AA | α-Humulene | AR | Detector ID |
| K | Camphene | AB | cis-Nerolidol | AS | Detector Name |
| L | β-Myrcene | AC | trans-Nerolidol | AT | Parser Version |
| M | (-)-β-pinene | AD | (-)-Guaiol | AU | Compound Result Row Count |
| N | Delta-3-carene | AE | Caryophyllene Oxide | AV | Peak Table Row Count |
| O | α-Terpinene | AF | (-)-α-Bisabolol | AW | Reportable Compound Row Count |
| P | cis-Ocimene | AG | Dimethylacetamide | AX | Source Row Hash |
| Q | d-Limonene | AH | Unknown Peak Count | AY | Import Status |

Audit rows contain every complete record once and in source order. Sample records intentionally occur both in this audit region and in their linked dynamic Test rows; this is audit traceability plus Test-linked presentation, not duplicate Test persistence.

## Parsing and classification

The parser requires exactly one `.txt` input and retains V1 strict validation for complete records, required sections, table widths, numeric values, 24 controlled compounds, 23 reportable analytes, Unicode labels, peak inspection, manual integration, and one audit-only Dimethylacetamide result.

Controlled categories are `Blank`, `Null`, `System Suitability`, `Standard`, `CCV`, `LOQ`, `Matrix Blank`, `Validation`, and `Sample`. Validation recognition is anchored to the validated `Low`, `Medium`, and `High` labels with optional numeric suffixes; broad substring matching is not used. Controls and validation records are audit-only and never resolve to Test rows.

`Source File Hash` is the SHA-256 of the uploaded source. Dynamic-row `Source Row Hash` retains the proven V1 record-content contract. Audit-row `Source Row Hash` is `SHA-256(source_file_hash + ":" + record_order)`, making its source-and-position identity explicit. `Parser Version` is `terpenes-simple-results-parser-v2-controls`; `Import Status` is the literal `Imported`.

## Targeted stale clearing

The parser stages every `A:AY` value for current audit rows. For unused rows after the current record count, it inspects both raw and processed grids and stages a blank only for a cell that is currently nonblank. Already blank audit cells are omitted. This clearing logic cannot target rows outside `91:190`, dynamic rows, row 89, or row 90.

## Single update

The only update shape is:

```text
QBBatchService.update({
  data: {
    id: batch_id,
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

The Results payload combines matched dynamic rows, all current audit rows, and targeted stale audit cells. Formula, image, and dollar-reference maps are preserved unchanged.

## Read-after-write

After the update callback succeeds, the parser retrieves Results once more and verifies:

- exact 190-by-51 grid structure, row-1 header, row-88 separator, row-89 section label, and row-90 audit header;
- exact candidate identity/count, unchanged `A:C`, exact matched `D:AY`, and byte-equivalent unmatched dynamic rows;
- exact audit record count/order, every `A:AY` value, no missing/duplicate record, and blank unused audit capacity;
- exact formula, image, and dollar-reference maps.

Numeric comparison accepts equivalent finite numeric-string representations without accepting changed values. Any failure emits `RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED`; there is no retry or repair update, and `QB.success()` remains deferred until verification passes.

## Future boundary

V2 does not implement Batch Review. The next phase is separately authorized, isolated Sandbox staging using new worksheet, parser, Batch, Sample, Tests, attachment, and job objects. Production promotion remains outside scope.
