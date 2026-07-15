\# Terpenes Batch Worksheet Sandbox Validation



Date tested: 2026-07-15

Environment: AIT QBench Sandbox

Tester: Mark Adams



\## Candidate



File:

terpenes\_\_batch\_ws\_id\_43\_\_candidate\_v1\_\_2026-07-14.json



Imported file SHA-256:

\[PASTE THE HASH OF THE EXACT FILE IMPORTED]



QBench Sandbox worksheet/version ID:

\[ENTER THE DRAFT VERSION ID IF SHOWN]



\## Instrument Import smoke test



Test row:

Instrument Import row 2



Input blocks:

\- A2:AE2

\- AH2:BE2



Observed results:

\- AF2 Import Validation Status: Valid

\- AG2 Import Message: Import row valid

\- Compound Results row count: 24

\- Peak Table row count: 34

\- Reportable compound row count: 23

\- Numeric analyte count: 23

\- Dimethylacetamide retained as numeric audit value: Yes

\- Dimethylacetamide included as reportable terpene: No

\- Unknown peak count accepted as numeric: Yes

\- Spreadsheet calculation errors observed: None

\- Terpenes Pass/Fail output observed: No



Numeric recognition:

\- Pasted concentrations were recognized as actual QBench numeric values.

\- COUNT/ISNUMBER behavior passed.



Result:

PASS — Instrument Import manual-paste smoke test



\## Limitations



\- This test used manual clipboard input.

\- A QBench-native LabSolutions parser has not yet been tested.

\- Batch-to-Test automation has not yet been tested.

\- Bracketing CCV criteria remain unresolved.

\- LCS requirement remains unresolved.

\- This does not authorize production promotion.



\## Evidence



\- \[Screenshot filename or description]

\- \[Screenshot filename or description]

