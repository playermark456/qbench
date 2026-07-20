# Live non-Terpenes Batch patterns

## Worksheet-definition findings

| Reference | Shape | Formulas | Named cells | Interpretation |
| --- | --- | ---: | ---: | --- |
| Residual Solvents Batch | One `Sheet1`, 155×30 | 0 | 0 | Legacy sequence/import surface; not a polished multi-stage model. |
| Quantitative Pesticides Batch | One `Sheet1`, 190×72 | 0 | 0 | Wide parser/operation surface with extensive read-only metadata; transfer logic is external to formulas. |

The safe exports did not expose a reusable multi-tab Raw Import → Normalized Import → Review → Transfer design. That absence is evidence against claiming that the proposed Terpenes Batch layout was copied from live.

## Automation and parser patterns

- The live automation list contains active `Data Modified` Batch-to-Test automations for multiple established assays.
- Homogeneity also demonstrates a Test-level `Data Modified` pull pattern.
- The active parser list includes both code-based and no-code parsers.
- Parser definition shells do not expose a configuration export or enough mapping detail to infer write ranges safely.
- Automation bodies and parser mappings were not copied; no customer or runtime object was opened.

## Reusable implementation boundary

Reusable:

- Keep parser landing, staff review, and Test transfer as distinct responsibilities.
- Mark formula/system-owned fields read-only.
- Treat Batch-to-Test movement as an explicit automation or manual transfer contract, not an incidental worksheet formula.
- Maintain source hashes, duplicate checks, and transfer state as audit data.
- Validate sample/Test matching and duplicate behavior with synthetic Sandbox objects.

Not reusable for Terpenes:

- Any other assay's source columns, equations, qualifier logic, QC decisions, analyte mapping, or automatic publish behavior.
- Any assumption that a `Data Modified` trigger proves the body, atomicity, error handling, or scientific mapping.

The proposed Terpenes tabs remain documentation-only: Run Setup, Raw Import, Normalized Import, Batch Review, Test Transfer, and Audit. The established 43-field contract and no-code parser boundaries remain the local technical inputs; scientific transfer stays blocked.
