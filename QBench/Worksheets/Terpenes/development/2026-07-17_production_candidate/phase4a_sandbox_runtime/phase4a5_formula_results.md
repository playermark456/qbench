# Phase 4A.5 formula results

Date: 2026-07-21

`environment_profile = sandbox_runtime_only`

## Passed pre-entry resolution

- `Data!C2`: `Cannabis Concentrates`
- `Specifications!U2`: matched the expected isolated Sandbox fixture binding; value intentionally omitted
- `Specifications!U3`: `Terpenes`
- `Specifications!U4`: `Cannabis Concentrates`
- `Specifications!U5`: `ug/g`
- Literal runtime placeholders: absent in the inspected configuration cells

## Controlled blocker

Alpha-Pinene's required lookup results were blank on first Test open and remained blank after the one permitted normal list-based reopen:

| Lookup | Expected | Actual |
| --- | ---: | --- |
| Alpha-Pinene LOQ | 10 | blank |
| Alpha-Pinene MU | 5 | blank |

The first required lookup failure activated the hard stop. The vector was not entered, and Ocimene, Nerolidol, direct-analyte, rounding, total, and full-precision runtime calculations were not evaluated. No formula or worksheet value was manually changed.
