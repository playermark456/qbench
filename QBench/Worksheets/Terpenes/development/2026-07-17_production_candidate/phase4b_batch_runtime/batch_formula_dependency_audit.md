# Batch formula dependency audit

## Scope and artifacts

- Authoritative source candidate: `production_candidates/SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS__v2.json`
  - SHA-256: `a4b92be3590e57f3456e12c65219cb6a5cb340248c6f3e50c6d3f36f56777837`
- Saved QBench export: local ignored source artifact; not tracked in this repository.
- No worksheet candidate was modified during this audit.

## Build chain

1. Historical source export: immutable local source artifact; not repeated in this sanitized audit.
2. Historical Batch builder: `QBench/Worksheets/Terpenes/development/2026-07-14_batch_worksheet_candidate/scripts/build_terpenes_batch_worksheet.py`. It uses the historical export and the directly read Terpenes analyte/QC configuration files to build the original `QC Review` and `Publish` workbook.
3. Production transformer: `QBench/Worksheets/Terpenes/development/2026-07-17_production_candidate/build_phase3_candidates.py`. `build_batch_candidate()` renames the tabs and globally transforms `Publish!` to `Test Transfer!`; this omitted the required single quotes.
4. Final generator: `QBench/Worksheets/Terpenes/development/2026-07-17_production_candidate/build_phase3_candidates_v2.py`. It retains the historical workbook identity and writes the Batch v2 candidate.
5. Generation command: `python QBench/Worksheets/Terpenes/development/2026-07-17_production_candidate/build_phase3_candidates_v2.py`.

The wrapper dynamically loads the historical Batch builder; there are no repository helper Python modules directly imported by the Batch path. The same wrapper also loads the Test builder to generate its paired Test artifact, but that builder does not contribute to the Batch formulas.

Rebuilding in memory with the current generator was semantically equal to the committed candidate but not byte-for-byte equal: rebuilt SHA-256 `657095aeee3910a167facf41649d5c323def986b8fca65e1c18f32fb4770abba`. No output file was written during that check.

## Exact formulas

Source candidate Batch Review formulas:

```text
B12 =IF(AND($B$14>0,COUNTIF(Test Transfer!BB2:BB87,FALSE)=0),TRUE,FALSE)
B13 =COUNTIF(Test Transfer!BD2:BD87,"Duplicate Test ID")
B14 =COUNTIF(Test Transfer!A2:A87,"<>")
B18 =IF(AND('Run Setup'!$B$24=TRUE,$B$9=TRUE,$B$11=TRUE,$B$12=TRUE,$B$13=0,$B$14>0,$B$15="Accepted"),TRUE,FALSE)
B19 =IF('Run Setup'!$B$24<>TRUE,"Run setup incomplete",IF($B$9<>TRUE,"Integration review incomplete",IF($B$11<>TRUE,"QC review incomplete",IF($B$13>0,"Duplicate Test ID",IF($B$14<=0,"No Publish rows",IF($B$12<>TRUE,"Publish rows incomplete",IF($B$15<>"Accepted","Batch QC on hold","Ready for transfer")))))))
```

Source candidate Test Transfer templates, applied at rows 2:87:

```text
BB[r] =IF(A[r]="","",IF(AND(COUNTIF($A$2:$A$87,A[r])=1,AZ[r]=TRUE,ISNUMBER(AA[r]),AA[r]>0,ISNUMBER(AB[r]),AB[r]>0,AD[r]="already_applied_by_labsolutions",AE[r]="ug/g",AF[r]="TRUE",AG[r]="TRUE",BA[r]=TRUE,AY[r]="Accepted"),TRUE,FALSE))
BC[r] =IF(A[r]="","",IF(AND(BB[r]=TRUE,'Batch Review'!$B$18=TRUE),"TRUE","FALSE"))
BD[r] =IF(A[r]="","",IF(COUNTIF($A$2:$A$87,A[r])>1,"Duplicate Test ID",IF(AZ[r]<>TRUE,"Analytical values incomplete",IF(OR(ISNUMBER(AA[r])<>TRUE,AA[r]<=0),"Sample mass required",IF(OR(ISNUMBER(AB[r])<>TRUE,AB[r]<=0),"Final volume required",IF(AD[r]<>"already_applied_by_labsolutions","Dilution mode required",IF(FALSE,"Dilution factor required",IF(OR(AE[r]<>"ug/g",AF[r]<>"TRUE"),"Unit confirmation required",IF(AG[r]<>"TRUE","Preparation confirmation required",IF(ISNUMBER(AU[r])<>TRUE,"Dimethylacetamide audit value required",IF(AV[r]<>"TRUE","Compound Results validation required",IF(AW[r]<>"Reviewed","Integration review required",IF(AX[r]<>"Valid","Import validation required",IF(BA[r]<>TRUE,"Source traceability incomplete",IF(AY[r]<>"Accepted","Batch QC on hold",IF('Batch Review'!$B$18<>TRUE,"Batch release review required","Ready for transfer"))))))))))))))))
```

Saved export B12:B14 use `TESTTRANSFER!` in place of the source candidate's invalid `Test Transfer!`; the B18/B19 and BB:BD formulas are otherwise the same. Both forms evaluate as `#ERROR` at the top-level Batch Review formulas because neither refers validly to the space-containing sheet name.

```text
B12 =IF(AND($B$14>0,COUNTIF(TESTTRANSFER!BB2:BB87,FALSE)=0),TRUE,FALSE)
B13 =COUNTIF(TESTTRANSFER!BD2:BD87,"Duplicate Test ID")
B14 =COUNTIF(TESTTRANSFER!A2:A87,"<>")
```

The historical source-code expressions are `Publish!` for B12:B14, `'QC Review'!$B$18` for the BC/BD templates, and the B18/B19 expressions shown above. `build_phase3_candidates.py` produces the candidate expressions through its global replacements `Publish! -> Test Transfer!`, `'QC Review'! -> 'Batch Review'!`, followed by worksheet renaming. The first replacement is the syntax defect.

## Dependency graph and cycle

- Test Transfer A2:A87 are test identifiers (placeholder-backed on the template rows).
- BB2:BB87 depend on their A row and A2:A87 duplicate check, plus AZ, AA, AB, AD, AE, AF, AG, BA, and AY on the same row.
- B12 depends on B14 and BB2:BB87.
- B14 depends on A2:A87.
- BD2:BD87 depend on their A row/A2:A87 duplicate check, row data AZ/AA/AB/AD/AE/AF/AG/AU/AV/AW/AX/BA/AY, and Batch Review B18.
- B13 depends on BD2:BD87.
- B18 depends on Run Setup B24 and Batch Review B9, B11, B12, B13, B14, and B15; B19 uses the same Batch Review gating inputs for its message.
- BC2:BC87 depend on BB2:BB87 and B18.

`dependency_graph = circular_dependency_confirmed`

Exact cycle: `Batch Review B13 -> Test Transfer BD2:BD87 -> Batch Review B18 -> Batch Review B13`.

## Recommended durable patch target

Update the authoritative sources, then regenerate a new candidate; do not patch only a saved export.

1. In `QC_CONTROL_ROWS` in the historical Batch builder, quote its original `Publish` references. The existing production transformer already maps quoted `'Publish'!` to quoted `'Test Transfer'!`, so the regenerated candidate receives the exact space-containing name safely:

```text
B12 historical =IF(AND($B$14>0,COUNTIF('Publish'!BB2:BB87,FALSE)=0),TRUE,FALSE)
B13 historical =COUNTIF('Publish'!BD2:BD87,"Duplicate Test ID")
B14 historical =COUNTIF('Publish'!A2:A87,"<>")

B12 generated =IF(AND($B$14>0,COUNTIF('Test Transfer'!BB2:BB87,FALSE)=0),TRUE,FALSE)
B13 generated =COUNTIF('Test Transfer'!BD2:BD87,"Duplicate Test ID")
B14 generated =COUNTIF('Test Transfer'!A2:A87,"<>")
```

2. In `publish_message_formula(row)`, replace only the final `'QC Review'!$B$18` test with the following historical-builder expression. The production transformer changes the quoted `QC Review` references to quoted `Batch Review` references; the result is applied to Test Transfer BD2:BD87:

```text
IF(AND('Run Setup'!$B$24=TRUE,'QC Review'!$B$9=TRUE,'QC Review'!$B$11=TRUE,'QC Review'!$B$12=TRUE,'QC Review'!$B$14>0,'QC Review'!$B$15="Accepted"),"Ready for transfer","Batch release review required")
```

This replaces `IF('QC Review'!$B$18<>TRUE,"Batch release review required","Ready for transfer")` in the historical builder, which currently transforms to the Batch Review expression. The duplicate-ID branch remains first, so for every row reaching this final branch B13 is necessarily zero. The inline condition is therefore equivalent to B18 for those rows while removing `BD -> B18`; B13 may continue to count the existing duplicate-ID message. It uses only `IF` and `AND`, which are already used throughout the workbook. The Batch gate B18, BC Publish Ready, AF/AG ownership, parser landing ranges, control/sample filtering, no-Pass/Fail behavior, and no automatic Publish or QC Review remain unchanged.

After regeneration, the B12:B14 formula strings will be mirrored in both worksheet data stores, and the revised BD template will be mirrored for rows 2:87. This audit does not authorize or perform that change.
