# Terpenes calculation contract — blocked missing authoritative requirement

## Controlling classification

`calculation_contract = blocked_missing_authoritative_requirement`

The authoritative-method intake found candidate Terpenes SOP, Analysis Form, and Analysis Protocol files, but it did not establish the current approved revision. Multiple distinct SOP byte streams share the same visible revision, a filename claiming revision 1.2 contains a visible revision-1.1 control block, and no standalone controlled LabSolutions concentration-unit evidence was found.

The live QBench review is an implementation-pattern review only. The user clarified that live QBench has no operational Terpenes implementation. A live definition artifact, another assay's worksheet, or another assay's formula cannot establish Terpenes scientific requirements.

## Unresolved authoritative requirements

- `Compound Results(Ch1) > Conc.` unit (`TERPENES_CONC_UNIT_UNRESOLVED`).
- Meaning of `Conc.` in the authoritative instrument output.
- Extraction or final-volume convention.
- Dilution-factor definition and whether it is already incorporated.
- mg/g equation (`TERPENES_MG_G_FORMULA_UNRESOLVED`).
- percent equation (`TERPENES_PERCENT_FORMULA_UNRESOLVED`).
- LOQ, negative, blank, and qualifier policy (`TERPENES_LOQ_POLICY_UNRESOLVED`).
- Significant figures and rounding (`TERPENES_ROUNDING_POLICY_UNRESOLVED`).
- Measurement uncertainty (`TERPENES_MU_POLICY_UNRESOLVED`).
- Approved COA measurands and units (`TERPENES_REPORT_MEASURANDS_UNRESOLVED`).
- Ocimene treatment (`TERPENES_OCIMENE_POLICY_UNRESOLVED`).
- Nerolidol treatment (`TERPENES_NEROLIDOL_POLICY_UNRESOLVED`).
- METRC reporting policy.
- Peak Table, Dimethylacetamide, and other audit-only conventions.

The uppercase tokens above are documentation markers only. They must not be inserted into QBench.

## Non-authoritative implementation evidence

Prior repository specifications contain proposed dimensional forms and live non-Terpenes worksheets demonstrate supported spreadsheet functions and blank/error safeguards. Those sources are useful for software design and validation mechanics only. They are not approved Terpenes scientific authority and cannot be used to create a Terpenes formula, worked example, test vector, or production-candidate worksheet JSON.

## Resume gate

Formula work may resume only after the current approved Terpenes method set and controlled instrument evidence explicitly resolve every calculation-critical item above, including reporting and rollup policy. Until then:

- no Terpenes formulas;
- no production-candidate worksheet JSON;
- no scientific constants copied from another assay; and
- no calculation-contract pass classification.
