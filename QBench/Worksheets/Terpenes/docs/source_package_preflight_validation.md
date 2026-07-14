# Terpenes source package preflight validation

Date: 2026-07-14

Repository branch: `codex/terpenes-source-package-2026-07-14`

HEAD: `224bfa06f5c457fc1efec233d17f403f1ac5f555`

Scope: preflight validation only. No active QBench worksheet export, COA source, automation, file parser, protocol worksheet, report, or production configuration was modified.

## File inventory

Command:

```powershell
$source = 'QBench\Worksheets\Terpenes\source'; $expected = @('terpenes_codex_build_brief_v3.md','terpenes_worksheet_spec_v3.json','terpenes_analyte_master_v3.csv','labsolutions_ascii_integration_spec.md','parse_labsolutions_ascii.py','Output_redacted_fixture.txt','metrc_terpene_export_profiles.json','metrc_terpene_reportable_mapping.csv','labsolutions_compound_results_fixture.csv','labsolutions_peak_table_fixture.csv','labsolutions_normalized_reportable_results_fixture.csv','README.md','MANIFEST.sha256'); $actual = Get-ChildItem -Path $source -File | Select-Object -ExpandProperty Name; $missing = $expected | Where-Object { $_ -notin $actual }; $extra = $actual | Where-Object { $_ -notin $expected }; [pscustomobject]@{ExpectedCount=$expected.Count; ActualCount=$actual.Count; Missing=($missing -join ', '); Extra=($extra -join ', ')} | Format-List
```

Result:

```text
ExpectedCount : 13
ActualCount   : 13
Missing       :
Extra         :
```

All requested source-package files are present and no extra files were present in `QBench/Worksheets/Terpenes/source`.

## JSON validation

Command:

```powershell
$files = @('QBench\Worksheets\Terpenes\source\terpenes_worksheet_spec_v3.json','QBench\Worksheets\Terpenes\source\metrc_terpene_export_profiles.json'); foreach ($file in $files) { Get-Content -Path $file -Raw | ConvertFrom-Json | Out-Null; Write-Output "$([System.IO.Path]::GetFileName($file)): valid JSON" }
```

Result:

```text
terpenes_worksheet_spec_v3.json: valid JSON
metrc_terpene_export_profiles.json: valid JSON
```

## SHA-256 manifest verification

Command:

```powershell
$source = 'QBench\Worksheets\Terpenes\source'; Get-Content -Path (Join-Path $source 'MANIFEST.sha256') | ForEach-Object { if ($_ -match '^(?<hash>[0-9a-f]{64})\s+(?<name>.+)$') { $path = Join-Path $source $Matches.name; $actual = (Get-FileHash -Algorithm SHA256 -Path $path).Hash.ToLowerInvariant(); [pscustomobject]@{File=$Matches.name; Expected=$Matches.hash; Actual=$actual; Status=($(if ($actual -eq $Matches.hash) {'OK'} else {'MISMATCH'}))} } } | Format-List
```

Result:

```text
File     : Output_redacted_fixture.txt
Expected : ed796c690b972ca08f1976b1d8f7355d3e5140e73ffa912c441d6185a093283b
Actual   : 9023337df6744ca17590e2085a207b05517961656f5434f93c9c720ccf3ea3f2
Status   : MISMATCH

File     : README.md
Expected : d24ec5f03678113e2696ecebc177ed0218e3c723ad348ae35a54ff7a93ae9637
Actual   : 2b7794c56ee01f2309b1d9c9fa3f71c235bf43a0e9cb1fc43f10f9ba801cd886
Status   : MISMATCH

File     : labsolutions_ascii_integration_spec.md
Expected : a4d3495158167469dd09a38bcd5cb002b070ffc89c600c248d38e84bf10b091f
Actual   : c0de2390a309e2d80f6a37c2846b77d697114d8c8267f6af7822738c62295546
Status   : MISMATCH

File     : labsolutions_compound_results_fixture.csv
Expected : d74ea572cf66ea4318c02c3e7d549b4874c6d8e9acf2226d6f81778ba8e158f5
Actual   : d74ea572cf66ea4318c02c3e7d549b4874c6d8e9acf2226d6f81778ba8e158f5
Status   : OK

File     : labsolutions_normalized_reportable_results_fixture.csv
Expected : a2161d8cc54caaf480190cdea4f13ffd3c5985e62235f57ef5b9ea30ccf71743
Actual   : c2cdfadf5b2eb2d3d992bb44e83bb244f5f7850af51ab18d94f15785d9e94aaa
Status   : MISMATCH

File     : labsolutions_peak_table_fixture.csv
Expected : 9edcb0b1f2a7b50a8e03beed4e30004805ce74a16aeff16658f7b9baa0b94a50
Actual   : 9edcb0b1f2a7b50a8e03beed4e30004805ce74a16aeff16658f7b9baa0b94a50
Status   : OK

File     : metrc_terpene_export_profiles.json
Expected : 39472de3e0c7d0a77fa58d5fa8f9682f1092919469b75040c90e30f54fe83f0b
Actual   : 9ea45096ebcf87273fb3e4783d34f75bd6f738d3ccf03d691f4de558a045e9ae
Status   : MISMATCH

File     : metrc_terpene_reportable_mapping.csv
Expected : 42ae81bf167b8a5329b12c24c8c8cd228415c96d8c2fc4e4b0ef5ec9d6bfccfe
Actual   : 42ae81bf167b8a5329b12c24c8c8cd228415c96d8c2fc4e4b0ef5ec9d6bfccfe
Status   : OK

File     : parse_labsolutions_ascii.py
Expected : b6cd6b893d37a0a69d39a9b80d3152019d2c09bef51b6bbe0bd98b1743edf41c
Actual   : fc17402ba90ed0530ce3a2fd7d48196e4821fb431c028e137b442505641f66b0
Status   : MISMATCH

File     : terpenes_analyte_master_v3.csv
Expected : 0157d051cc79345a8eb4bdb0a7d7294a83cce5fe7a81827d66691096939530b6
Actual   : 0157d051cc79345a8eb4bdb0a7d7294a83cce5fe7a81827d66691096939530b6
Status   : OK

File     : terpenes_codex_build_brief_v3.md
Expected : ed9b26eb63ed0a0168e850b3d3aac35e953551dc4d93d845378ea8f3eb84f4ff
Actual   : 015dde9c87f2d0264e09bd3311746028e4b9796069adf04e0bfd6c8fe3e920cc
Status   : MISMATCH

File     : terpenes_worksheet_spec_v3.json
Expected : e2ea010f433f3f09987ea12d0e09d9e4d7d3cbb3f5d2bb914b7da18dca2807db
Actual   : 33d2190863c6a5d8b30d59f4f36cb6b5553702f91478ccd99e88c769abe0919c
Status   : MISMATCH
```

Working-tree SHA-256 verification did not fully pass. Four files matched the manifest and eight files did not.

### SHA-256 discrepancy diagnostics

Command:

```powershell
& 'C:\Users\Mark Adams\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe' config --show-origin --get-regexp 'core.autocrlf|core.eol|text'
```

Result:

```text
file:C:/Users/Mark Adams/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/etc/gitconfig core.autocrlf true
file:C:/Users/Mark Adams/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/etc/gitconfig diff.astextplain.textconv astextplain
```

Command:

```powershell
& 'C:\Users\Mark Adams\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe' ls-files --eol QBench/Worksheets/Terpenes/source
```

Result:

```text
i/lf    w/crlf  attr/                  QBench/Worksheets/Terpenes/source/MANIFEST.sha256
i/lf    w/crlf  attr/                  QBench/Worksheets/Terpenes/source/Output_redacted_fixture.txt
i/lf    w/crlf  attr/                  QBench/Worksheets/Terpenes/source/README.md
i/lf    w/crlf  attr/                  QBench/Worksheets/Terpenes/source/labsolutions_ascii_integration_spec.md
i/lf    w/crlf  attr/                  QBench/Worksheets/Terpenes/source/labsolutions_compound_results_fixture.csv
i/lf    w/crlf  attr/                  QBench/Worksheets/Terpenes/source/labsolutions_normalized_reportable_results_fixture.csv
i/lf    w/crlf  attr/                  QBench/Worksheets/Terpenes/source/labsolutions_peak_table_fixture.csv
i/lf    w/crlf  attr/                  QBench/Worksheets/Terpenes/source/metrc_terpene_export_profiles.json
i/lf    w/crlf  attr/                  QBench/Worksheets/Terpenes/source/metrc_terpene_reportable_mapping.csv
i/lf    w/crlf  attr/                  QBench/Worksheets/Terpenes/source/parse_labsolutions_ascii.py
i/lf    w/crlf  attr/                  QBench/Worksheets/Terpenes/source/terpenes_analyte_master_v3.csv
i/lf    w/crlf  attr/                  QBench/Worksheets/Terpenes/source/terpenes_codex_build_brief_v3.md
i/lf    w/crlf  attr/                  QBench/Worksheets/Terpenes/source/terpenes_worksheet_spec_v3.json
```

Command:

```powershell
& 'C:\Users\Mark Adams\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -c "import hashlib, pathlib; source=pathlib.Path('QBench/Worksheets/Terpenes/source');
for line in (source/'MANIFEST.sha256').read_text().splitlines():
    expected,name=line.split(maxsplit=1); data=(source/name).read_bytes(); lf=data.replace(b'\r\n', b'\n'); crlf=lf.replace(b'\n', b'\r\n'); statuses=[]
    if hashlib.sha256(data).hexdigest()==expected: statuses.append('working-tree-bytes')
    if hashlib.sha256(lf).hexdigest()==expected: statuses.append('LF-normalized')
    if hashlib.sha256(crlf).hexdigest()==expected: statuses.append('CRLF-normalized')
    print(name + ': ' + (', '.join(statuses) if statuses else 'no simple newline match'))"
```

Result:

```text
Output_redacted_fixture.txt: LF-normalized
README.md: LF-normalized
labsolutions_ascii_integration_spec.md: LF-normalized
labsolutions_compound_results_fixture.csv: working-tree-bytes, CRLF-normalized
labsolutions_normalized_reportable_results_fixture.csv: LF-normalized
labsolutions_peak_table_fixture.csv: working-tree-bytes, CRLF-normalized
metrc_terpene_export_profiles.json: no simple newline match
metrc_terpene_reportable_mapping.csv: working-tree-bytes, CRLF-normalized
parse_labsolutions_ascii.py: LF-normalized
terpenes_analyte_master_v3.csv: working-tree-bytes, CRLF-normalized
terpenes_codex_build_brief_v3.md: LF-normalized
terpenes_worksheet_spec_v3.json: no simple newline match
```

Discrepancy: the manifest entries are not consistently based on the same byte representation. Some entries match LF-normalized content, some match CRLF-normalized content, and both JSON files failed the simple newline-normalization check. The repository has `core.autocrlf=true` and no `.gitattributes` rule pinning source-package line endings.

## Row counts

Command:

```powershell
$source = 'QBench\Worksheets\Terpenes\source'; [pscustomobject]@{AnalyteMasterRows=@(Import-Csv (Join-Path $source 'terpenes_analyte_master_v3.csv')).Count; MetrcMappingRows=@(Import-Csv (Join-Path $source 'metrc_terpene_reportable_mapping.csv')).Count; CompoundResultsRows=@(Import-Csv (Join-Path $source 'labsolutions_compound_results_fixture.csv')).Count; PeakTableRows=@(Import-Csv (Join-Path $source 'labsolutions_peak_table_fixture.csv')).Count; NormalizedReportableRows=@(Import-Csv (Join-Path $source 'labsolutions_normalized_reportable_results_fixture.csv')).Count} | Format-List
```

Result:

```text
AnalyteMasterRows        : 23
MetrcMappingRows         : 23
CompoundResultsRows      : 24
PeakTableRows            : 34
NormalizedReportableRows : 23
```

The requested row counts were verified.

## Dimethylacetamide fixture handling

Command:

```powershell
$source = 'QBench\Worksheets\Terpenes\source'; $compound = Import-Csv (Join-Path $source 'labsolutions_compound_results_fixture.csv'); $normalized = Import-Csv (Join-Path $source 'labsolutions_normalized_reportable_results_fixture.csv'); $compound | Where-Object { $_.Name -eq 'Dimethylacetamide' } | Select-Object Name,worksheet_label,reportable | Format-List; [pscustomobject]@{DimethylacetamideInNormalizedRows=@($normalized | Where-Object { $_.source_name -eq 'Dimethylacetamide' -or $_.worksheet_label -eq 'Dimethylacetamide' }).Count} | Format-List
```

Result:

```text
Name            : Dimethylacetamide
worksheet_label : Dimethylacetamide
reportable      : False

DimethylacetamideInNormalizedRows : 0
```

Dimethylacetamide is retained in Compound Results for audit, marked non-reportable, and absent from normalized reportable terpene results.

## Parser run

Command:

```powershell
$out = Join-Path $env:TEMP 'qbench_terpenes_preflight_20260714'; & 'C:\Users\Mark Adams\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' QBench\Worksheets\Terpenes\source\parse_labsolutions_ascii.py QBench\Worksheets\Terpenes\source\Output_redacted_fixture.txt --output-dir $out
```

Result:

```json
{
  "sections_present": [
    "Header",
    "File Information",
    "Sample Information",
    "Original Files",
    "File Description",
    "Configuration",
    "Peak Table(Ch1)",
    "Compound Results(Ch1)"
  ],
  "compound_rows": 24,
  "peak_rows": 34,
  "reportable_compound_rows": 23,
  "non_reportable_compounds": [
    "Dimethylacetamide"
  ],
  "outputs": [
    "C:\\Users\\MARKAD~1\\AppData\\Local\\Temp\\qbench_terpenes_preflight_20260714\\labsolutions_ascii_parsed_output.json",
    "C:\\Users\\MARKAD~1\\AppData\\Local\\Temp\\qbench_terpenes_preflight_20260714\\labsolutions_compound_results_fixture.csv",
    "C:\\Users\\MARKAD~1\\AppData\\Local\\Temp\\qbench_terpenes_preflight_20260714\\labsolutions_peak_table_fixture.csv",
    "C:\\Users\\MARKAD~1\\AppData\\Local\\Temp\\qbench_terpenes_preflight_20260714\\labsolutions_normalized_reportable_results_fixture.csv"
  ]
}
```

Command:

```powershell
$out = Join-Path $env:TEMP 'qbench_terpenes_preflight_20260714'; $compound = Import-Csv (Join-Path $out 'labsolutions_compound_results_fixture.csv'); $peak = Import-Csv (Join-Path $out 'labsolutions_peak_table_fixture.csv'); $normalized = Import-Csv (Join-Path $out 'labsolutions_normalized_reportable_results_fixture.csv'); [pscustomobject]@{GeneratedCompoundRows=@($compound).Count; GeneratedPeakRows=@($peak).Count; GeneratedNormalizedReportableRows=@($normalized).Count; GeneratedDimethylacetamideCompoundRows=@($compound | Where-Object { $_.Name -eq 'Dimethylacetamide' -and $_.reportable -eq 'False' }).Count; GeneratedDimethylacetamideNormalizedRows=@($normalized | Where-Object { $_.source_name -eq 'Dimethylacetamide' -or $_.worksheet_label -eq 'Dimethylacetamide' }).Count} | Format-List
```

Result:

```text
GeneratedCompoundRows                    : 24
GeneratedPeakRows                        : 34
GeneratedNormalizedReportableRows        : 23
GeneratedDimethylacetamideCompoundRows   : 1
GeneratedDimethylacetamideNormalizedRows : 0
```

The parser ran against `Output_redacted_fixture.txt`, produced the expected row counts, retained Dimethylacetamide in compound output, and excluded it from generated normalized reportable results.

## Summary

Passed:

- All 13 expected package files are present.
- Both JSON files parse successfully.
- Analyte master has 23 rows.
- METRC mapping has 23 rows.
- Compound Results fixture has 24 rows.
- Peak Table fixture has 34 rows.
- Normalized reportable-result fixture has 23 rows.
- Parser run completed successfully with 24 compound rows, 34 peak rows, 23 reportable rows, and Dimethylacetamide as the non-reportable compound.
- Dimethylacetamide is retained for audit and excluded from reportable terpene results.

Discrepancy:

- `MANIFEST.sha256` does not fully verify against the current working-tree bytes. Four files matched and eight files mismatched.
- The hash basis appears inconsistent across package files. Some manifest entries match LF-normalized content, some match CRLF-normalized content, and the two JSON files do not match either simple newline-normalized form in this checkout.

This note is a preflight record only and does not designate the package as production-ready.
