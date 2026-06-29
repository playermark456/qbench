# Start Here

## What to upload into QBench

### 1. Report asset
Upload this file to QBench report configuration attachments:

```text
assets/hexagon-grid-8tile-1336x618.png
```

Use this exact attachment filename unless you also update the COA source:

```text
hexagon-grid-8tile-1336x618.png
```

### 2. COA source code
Copy all contents from:

```text
coa/coa_source_8tile_homogeneity_full.html
```

Paste it into the QBench COA source editor.

### 3. Homogeneity worksheet template
Import this JSON into the QBench Homogeneity worksheet template:

```text
worksheets/current/homogeneity_copy_paste_v6_two_target_COA_import_safe.json
```

## What to test in QBench

1. Create a test order with Cannabinoid Potency and Homogeneity.
2. Paste 10 cannabinoid result rows into the Homogeneity worksheet.
3. Enter actual unit masses.
4. Enter one target cannabinoid, then test again with two target cannabinoids.
5. Confirm the Homogeneity worksheet resolves `pass_fail`.
6. Generate a COA preview.
7. Confirm the first page shows Homogeneity in the 8th tile.
8. Confirm the standalone Homogeneity page renders the `report_results` table.

## Safe first test settings

Use one target first:

```text
Target Cannabinoid 1: Total THC
Target Cannabinoid 2: blank
```

Then test two targets:

```text
Target Cannabinoid 1: Total THC
Target Cannabinoid 2: Total CBD
```
