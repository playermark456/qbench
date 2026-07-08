# Open Questions - 2026-07-04

## Failed Worksheet Downloads

- Worksheet ID 41 `Cannabis/Hemp {Protocol WS} Overall Chemist Review of Batch`: No worksheet version found.
- Worksheet ID 68 `test`: Export Spreadsheet control not visible on page.
- Worksheet ID 76 `Pest Myco (Qualitative) [Protocol WS] LC-MS/MS Setup and Measurement`: No worksheet version found.

## Active vs Draft Status Unclear

- Worksheet ID 2 `Example Batch Worksheet` did not expose an active approved version in the parsed selector.
- Worksheet ID 4 `Training Worksheet` did not expose an active approved version in the parsed selector.
- Worksheet ID 41 `Cannabis/Hemp {Protocol WS} Overall Chemist Review of Batch` did not expose an active approved version in the parsed selector.
- Worksheet ID 45 `Microbial Analysis [Batch] Worksheet` did not expose an active approved version in the parsed selector.
- Worksheet ID 59 `Preparation of Samples` did not expose an active approved version in the parsed selector.
- Worksheet ID 67 `METRC Worksheet` did not expose an active approved version in the parsed selector.
- Worksheet ID 68 `test` did not expose an active approved version in the parsed selector.
- Worksheet ID 76 `Pest Myco (Qualitative) [Protocol WS] LC-MS/MS Setup and Measurement` did not expose an active approved version in the parsed selector.
- Worksheet ID 111 `[Logs] Gene Up Self-Test` did not expose an active approved version in the parsed selector.
- Worksheet ID 114 `[Logs] Tempo Data Export` did not expose an active approved version in the parsed selector.

## Screenshots or Named-Cell Captures Only

None recorded.

## Parser Internals Not Visible

Parser pages still need browser/UI inspection or a parser export endpoint. No parser export was performed by this worksheet rescan helper.

## Automations Not Fully Visible

Automation pages still need browser/UI inspection or an automation export endpoint. No automation export was performed by this worksheet rescan helper.

## Assets Not Downloadable

COA/report assets were not downloaded by this worksheet rescan helper.

## Pages Requiring Modification To Proceed

None encountered by the read-only worksheet GET/export process.

## Tooling Limitation

The in-app browser connector failed to start and the bundled Playwright package was incomplete. The rescan therefore used authenticated read-only QBench HTTP GET requests and the same client-side dynamic worksheet conversion used by Export Spreadsheet.
