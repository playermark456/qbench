# Codex Setup Notes

## Do you need GitHub?

For Codex web/cloud, the official setup is to connect a GitHub account and let Codex work from repositories. A private GitHub repository is fine. If you do not want to create GitHub, you can still use this folder as a normal file package, but the cloud repo workflow and PR workflow are designed around GitHub.

## Recommended repo name

```text
qbench-coa-homogeneity
```

## First Codex task prompt

```text
Read this repository. Summarize how the QBench Homogeneity worksheet, COA source code, and 8-tile hex asset work together. Then run the validation scripts and report any issues. Do not change files yet.
```

## Second Codex task prompt

```text
Review the Homogeneity worksheet JSON and COA source for consistency. Confirm that the COA's Homogeneity tile uses pass_fail and that the standalone Homogeneity page renders report_results. Fix only if a mismatch is found.
```

## QBench account safety

Prefer exported files over live QBench access. If Codex is ever used to inspect QBench through a browser, use a read-only QBench user in a sandbox/staging environment. Do not use a production admin account.
