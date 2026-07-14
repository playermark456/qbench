# Terpenes source package preflight validation

Date: 2026-07-14

Branch: `codex/terpenes-source-package-2026-07-14`

Scope: Prompt 0 source-package integrity correction and preflight only. No active QBench worksheet export, COA source, automation, parser configuration, protocol worksheet, report configuration, or production setting was modified.

## Original Manifest Discrepancy

Command:

```powershell
$source='QBench\Worksheets\Terpenes\source'; Get-Content (Join-Path $source 'MANIFEST.sha256') | ForEach-Object { if ($_ -match '^(?<hash>[0-9a-f]{64})\s+(?<name>.+)$') { $path=Join-Path $source $Matches.name; $actual=(Get-FileHash -Algorithm SHA256 -Path $path).Hash.ToLowerInvariant(); [pscustomobject]@{File=$Matches.name; Status=($(if ($actual -eq $Matches.hash) {'OK'} else {'MISMATCH'})); Expected=$Matches.hash; Actual=$actual} } } | Format-List
```

Result before correction:

```text
Output_redacted_fixture.txt                            MISMATCH
README.md                                              MISMATCH
labsolutions_ascii_integration_spec.md                 MISMATCH
labsolutions_compound_results_fixture.csv              OK
labsolutions_normalized_reportable_results_fixture.csv MISMATCH
labsolutions_peak_table_fixture.csv                    OK
metrc_terpene_export_profiles.json                     MISMATCH
metrc_terpene_reportable_mapping.csv                   OK
parse_labsolutions_ascii.py                            MISMATCH
terpenes_analyte_master_v3.csv                         OK
terpenes_codex_build_brief_v3.md                       MISMATCH
terpenes_worksheet_spec_v3.json                        MISMATCH
```

The original manifest did not verify consistently from the Windows working tree.

## Root Cause

Command:

```powershell
& 'C:\Users\Mark Adams\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe' ls-files --eol QBench/Worksheets/Terpenes/source
```

Result before correction:

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
& 'C:\Users\Mark Adams\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe' config --show-origin --get-regexp 'core.autocrlf|core.eol|text'
```

Result:

```text
file:C:/Users/Mark Adams/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/etc/gitconfig core.autocrlf true
file:C:/Users/Mark Adams/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/etc/gitconfig diff.astextplain.textconv astextplain
```

There was no Terpenes-specific `.gitattributes` file, and the runtime Git configuration used `core.autocrlf=true`. The source files were stored as LF in the repository but checked out as CRLF in the working tree. The original manifest entries were also mixed: some matched LF-normalized bytes, some matched CRLF-normalized bytes, and the two JSON entries matched LF-normalized bytes only after removing the final newline.

## JSON Discrepancy Diagnosis

Command:

```powershell
& 'C:\Users\Mark Adams\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -c "import hashlib,json,pathlib; files=['terpenes_worksheet_spec_v3.json','metrc_terpene_export_profiles.json']; source=pathlib.Path('QBench/Worksheets/Terpenes/source'); expected={}; [expected.setdefault(n,h) for h,n in (line.split(maxsplit=1) for line in (source/'MANIFEST.sha256').read_text().splitlines())];
for name in files:
    data=(source/name).read_bytes(); obj=json.loads(data.decode('utf-8-sig')); lf=data.replace(b'\r\n',b'\n'); variants={'raw':data,'lf_normalized':lf,'lf_no_final_newline':lf.rstrip(b'\n'),'canonical_sorted_compact':json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8'),'canonical_sorted_indent2':(json.dumps(obj,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode('utf-8')}; print(name, [k for k,v in variants.items() if hashlib.sha256(v).hexdigest()==expected[name]], 'bom', data.startswith(b'\xef\xbb\xbf'), 'trailing_crlf', data.endswith(b'\r\n'))"
```

Result:

```text
terpenes_worksheet_spec_v3.json ['lf_no_final_newline'] bom False trailing_crlf True
metrc_terpene_export_profiles.json ['lf_no_final_newline'] bom False trailing_crlf True
```

Diagnosis:

- The two JSON mismatches were caused by the old manifest hashing LF-normalized JSON bytes with the final newline omitted, while the committed files contain a final newline.
- No UTF-8 BOM was present.
- The mismatch was not caused by JSON key-order changes or semantic JSON content changes.
- No separate original task attachment or source-package copy was available in this workspace. The committed JSON structures were therefore validated against the build brief, analyte master, METRC mapping, fixture row-count expectations, and parser requirements before accepting the committed versions as canonical.

Command:

```powershell
& 'C:\Users\Mark Adams\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -c "import csv,json,pathlib,sys; source=pathlib.Path('QBench/Worksheets/Terpenes/source'); spec=json.loads((source/'terpenes_worksheet_spec_v3.json').read_text(encoding='utf-8-sig')); profiles=json.loads((source/'metrc_terpene_export_profiles.json').read_text(encoding='utf-8-sig')); analytes=list(csv.DictReader((source/'terpenes_analyte_master_v3.csv').open(encoding='utf-8-sig'))); mapping=list(csv.DictReader((source/'metrc_terpene_reportable_mapping.csv').open(encoding='utf-8-sig'))); compounds=list(csv.DictReader((source/'labsolutions_compound_results_fixture.csv').open(encoding='utf-8-sig'))); normalized=list(csv.DictReader((source/'labsolutions_normalized_reportable_results_fixture.csv').open(encoding='utf-8-sig'))); field_map=spec.get('labsolutions_ascii_import',{}).get('compound_result_field_mapping',{}); checks=[('analyte_master_count_23',len(analytes)==23),('metrc_mapping_count_23',len(mapping)==23),('compound_results_count_24',len(compounds)==24),('normalized_reportable_count_23',len(normalized)==23),('units_include_percent_and_mg_g',spec.get('units',{}).get('result_primary_units')==['%','mg/g']),('quantitation_source_is_compound_results_conc',spec.get('labsolutions_ascii_import',{}).get('quantitation_source_table')=='Compound Results(Ch1)' and field_map.get('extract_concentration_input')=='Conc.'),('do_not_use_conc_percent_norm_conc',set(spec.get('labsolutions_ascii_import',{}).get('do_not_use_for_potency',[]))=={'Conc. %','Norm Conc.'}),('ignore_dimethylacetamide','Dimethylacetamide' in spec.get('labsolutions_ascii_import',{}).get('ignore_for_report',[])),('dimethylacetamide_not_reportable_fixture',any(r.get('Name')=='Dimethylacetamide' and r.get('reportable')=='False' for r in compounds)),('dimethylacetamide_absent_normalized',not any(r.get('source_name')=='Dimethylacetamide' or r.get('worksheet_label')=='Dimethylacetamide' for r in normalized)),('all_analytes_use_conc_for_quant',all(r.get('labsolutions_conc_field')=='Conc.' and r.get('labsolutions_use_for_quant')=='yes' for r in analytes)),('profile_count_9',len(profiles.get('export_profiles',{}))==9),('metrc_issues_count_8',len(profiles.get('issues_requiring_confirmation',[]))==8),('ocimene_rollup_in_mapping',sum(1 for r in mapping if r.get('metrc_target_analyte_label')=='Ocimene' and r.get('metrc_mapping_rule')=='rollup_component')==2),('nerolidol_mapping_present',any(r.get('worksheet_label')=='cis-Nerolidol' and r.get('metrc_target_analyte_label')=='Cis-Nerolidol' for r in mapping) and any(r.get('worksheet_label')=='trans-Nerolidol' and r.get('metrc_target_analyte_label')=='Nerolidol' for r in mapping)),('other_terpenes_not_silent','Other Terpenes' not in {r.get('metrc_target_analyte_label') for r in mapping})]; [print(('PASS' if ok else 'FAIL')+' '+name) for name,ok in checks]; sys.exit(0 if all(ok for _,ok in checks) else 1)"
```

Result:

```text
PASS analyte_master_count_23
PASS metrc_mapping_count_23
PASS compound_results_count_24
PASS normalized_reportable_count_23
PASS units_include_percent_and_mg_g
PASS quantitation_source_is_compound_results_conc
PASS do_not_use_conc_percent_norm_conc
PASS ignore_dimethylacetamide
PASS dimethylacetamide_not_reportable_fixture
PASS dimethylacetamide_absent_normalized
PASS all_analytes_use_conc_for_quant
PASS profile_count_9
PASS metrc_issues_count_8
PASS ocimene_rollup_in_mapping
PASS nerolidol_mapping_present
PASS other_terpenes_not_silent
```

## Correction Made

Added `QBench/Worksheets/Terpenes/.gitattributes` with directory-specific LF rules:

```text
source/*.md text eol=lf
source/*.json text eol=lf
source/*.csv text eol=lf
source/*.py text eol=lf
source/*.txt text eol=lf
source/*.sha256 text eol=lf
```

Renormalized only `QBench/Worksheets/Terpenes/source` files covered by those rules. No semantic changes were made to the source package to resolve line endings.

Regenerated `QBench/Worksheets/Terpenes/source/MANIFEST.sha256` from the normalized raw bytes of the 12 source-package files, excluding `MANIFEST.sha256` itself, using lowercase SHA-256 hashes and filename-sorted entries.

## Final Validation

### Source Inventory

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

### JSON Parse

Command:

```powershell
$files = @('QBench\Worksheets\Terpenes\source\terpenes_worksheet_spec_v3.json','QBench\Worksheets\Terpenes\source\metrc_terpene_export_profiles.json'); foreach ($file in $files) { Get-Content -Path $file -Raw | ConvertFrom-Json | Out-Null; Write-Output "$([System.IO.Path]::GetFileName($file)): valid JSON" }
```

Result:

```text
terpenes_worksheet_spec_v3.json: valid JSON
metrc_terpene_export_profiles.json: valid JSON
```

### Manifest Verification

Command:

```powershell
$source='QBench\Worksheets\Terpenes\source'; $result = Get-Content (Join-Path $source 'MANIFEST.sha256') | ForEach-Object { if ($_ -match '^(?<hash>[0-9a-f]{64})\s+(?<name>.+)$') { $path=Join-Path $source $Matches.name; $actual=(Get-FileHash -Algorithm SHA256 -Path $path).Hash.ToLowerInvariant(); [pscustomobject]@{File=$Matches.name; Status=($(if ($actual -eq $Matches.hash) {'PASS'} else {'FAIL'}))} } }; $result | Format-Table File,Status -AutoSize; $pass = @($result | Where-Object {$_.Status -eq 'PASS'}).Count; $total = @($result).Count; Write-Output "Manifest summary: $pass/$total PASS"
```

Result:

```text
File                                                   Status
----                                                   ------
labsolutions_ascii_integration_spec.md                 PASS
labsolutions_compound_results_fixture.csv              PASS
labsolutions_normalized_reportable_results_fixture.csv PASS
labsolutions_peak_table_fixture.csv                    PASS
metrc_terpene_export_profiles.json                     PASS
metrc_terpene_reportable_mapping.csv                   PASS
Output_redacted_fixture.txt                            PASS
parse_labsolutions_ascii.py                            PASS
README.md                                              PASS
terpenes_analyte_master_v3.csv                         PASS
terpenes_codex_build_brief_v3.md                       PASS
terpenes_worksheet_spec_v3.json                        PASS

Manifest summary: 12/12 PASS
```

### LF Checkout Verification

Command:

```powershell
& 'C:\Users\Mark Adams\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe' ls-files --eol QBench/Worksheets/Terpenes/source
```

Result:

```text
i/lf    w/lf    attr/text eol=lf       QBench/Worksheets/Terpenes/source/MANIFEST.sha256
i/lf    w/lf    attr/text eol=lf       QBench/Worksheets/Terpenes/source/Output_redacted_fixture.txt
i/lf    w/lf    attr/text eol=lf       QBench/Worksheets/Terpenes/source/README.md
i/lf    w/lf    attr/text eol=lf       QBench/Worksheets/Terpenes/source/labsolutions_ascii_integration_spec.md
i/lf    w/lf    attr/text eol=lf       QBench/Worksheets/Terpenes/source/labsolutions_compound_results_fixture.csv
i/lf    w/lf    attr/text eol=lf       QBench/Worksheets/Terpenes/source/labsolutions_normalized_reportable_results_fixture.csv
i/lf    w/lf    attr/text eol=lf       QBench/Worksheets/Terpenes/source/labsolutions_peak_table_fixture.csv
i/lf    w/lf    attr/text eol=lf       QBench/Worksheets/Terpenes/source/metrc_terpene_export_profiles.json
i/lf    w/lf    attr/text eol=lf       QBench/Worksheets/Terpenes/source/metrc_terpene_reportable_mapping.csv
i/lf    w/lf    attr/text eol=lf       QBench/Worksheets/Terpenes/source/parse_labsolutions_ascii.py
i/lf    w/lf    attr/text eol=lf       QBench/Worksheets/Terpenes/source/terpenes_analyte_master_v3.csv
i/lf    w/lf    attr/text eol=lf       QBench/Worksheets/Terpenes/source/terpenes_codex_build_brief_v3.md
i/lf    w/lf    attr/text eol=lf       QBench/Worksheets/Terpenes/source/terpenes_worksheet_spec_v3.json
```

### Row Counts

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

### Parser Run

Command:

```powershell
$out = Join-Path $env:TEMP 'qbench_terpenes_preflight_20260714_final'; & 'C:\Users\Mark Adams\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' QBench\Worksheets\Terpenes\source\parse_labsolutions_ascii.py QBench\Worksheets\Terpenes\source\Output_redacted_fixture.txt --output-dir $out
```

Result:

```json
{
  "compound_rows": 24,
  "peak_rows": 34,
  "reportable_compound_rows": 23,
  "non_reportable_compounds": [
    "Dimethylacetamide"
  ]
}
```

Command:

```powershell
$out = Join-Path $env:TEMP 'qbench_terpenes_preflight_20260714_final'; $compound = Import-Csv (Join-Path $out 'labsolutions_compound_results_fixture.csv'); $peak = Import-Csv (Join-Path $out 'labsolutions_peak_table_fixture.csv'); $normalized = Import-Csv (Join-Path $out 'labsolutions_normalized_reportable_results_fixture.csv'); [pscustomobject]@{GeneratedCompoundRows=@($compound).Count; GeneratedPeakRows=@($peak).Count; GeneratedNormalizedReportableRows=@($normalized).Count; GeneratedDimethylacetamideCompoundRows=@($compound | Where-Object { $_.Name -eq 'Dimethylacetamide' -and $_.reportable -eq 'False' }).Count; GeneratedDimethylacetamideNormalizedRows=@($normalized | Where-Object { $_.source_name -eq 'Dimethylacetamide' -or $_.worksheet_label -eq 'Dimethylacetamide' }).Count} | Format-List
```

Result:

```text
GeneratedCompoundRows                    : 24
GeneratedPeakRows                        : 34
GeneratedNormalizedReportableRows        : 23
GeneratedDimethylacetamideCompoundRows   : 1
GeneratedDimethylacetamideNormalizedRows : 0
```

### Diff Checks

Command:

```powershell
& 'C:\Users\Mark Adams\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe' diff --check
```

Result:

```text
PASS
```

Command:

```powershell
& 'C:\Users\Mark Adams\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe' diff --cached --name-only
```

Result:

```text
QBench/Worksheets/Terpenes/.gitattributes
QBench/Worksheets/Terpenes/docs/source_package_preflight_validation.md
QBench/Worksheets/Terpenes/source/MANIFEST.sha256
```

`QBench/Worksheets/Terpenes/AGENTS.md` is already tracked on this branch and was verified to contain the required Prompt 0 instructions. No active QBench worksheet export, COA source, automation, parser configuration, protocol worksheet, report configuration, or production setting changed.

## Final Results

- Exactly 13 expected files remain in `QBench/Worksheets/Terpenes/source`.
- Both JSON files parse.
- `MANIFEST.sha256` verifies `12/12 PASS`.
- `git ls-files --eol` shows `i/lf w/lf attr/text eol=lf` for the normalized source files.
- Analyte master has 23 data rows.
- METRC mapping has 23 data rows.
- Compound Results fixture has 24 data rows.
- Peak Table fixture has 34 data rows.
- Normalized reportable fixture has 23 data rows.
- Parser produces 24 compound rows.
- Parser produces 34 peak rows.
- Parser produces 23 reportable rows.
- Dimethylacetamide is retained in compound/audit output.
- Dimethylacetamide is absent from normalized reportable output.
- `git diff --check` passes.
- No active QBench object or production artifact was modified.

This remains a Prompt 0 preflight record only and does not designate the package as production-ready.
