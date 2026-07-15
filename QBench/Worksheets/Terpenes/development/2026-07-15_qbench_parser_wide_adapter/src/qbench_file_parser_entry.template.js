"use strict";

/*
INTEGRATION_BLOCKER: QBench Code File Parser runtime contract is not proven.

Known repository evidence:
- Parser 46 visibly imports:
  importScripts('https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js');

Missing evidence:
- Parser entry-point function name/signature.
- Input file object shape and text/byte access API.
- Output or worksheet-write API.
- Error reporting API.
- File-extension registration behavior.
- Assay attachment and worksheet target behavior.
- Transactionality or dry-run behavior.
- Whether numeric writes preserve JavaScript Number values.
- Whether a parser can target Instrument Import A:AE and AH:BE without
  overwriting AF/AG formulas.

Do not paste this template into QBench as a working parser. It is a controlled
integration scaffold only. Replace every INTEGRATION_BLOCKER marker only after
read-only QBench evidence proves the exact runtime API.
*/

/* INTEGRATION_BLOCKER: documented QBench parser library URL only. */
importScripts("https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js");

/* INTEGRATION_BLOCKER: entry point name and input contract unknown.
function qbenchParserEntry(qbenchFileParserContext) {
  // Expected behavior after runtime proof:
  // 1. Accept .txt LabSolutions ASCII input only.
  // 2. Enforce parser_security_limits.json.
  // 3. Parse with labsolutions_ascii_core.js.
  // 4. Adapt to Instrument Import A:AE and AH:BE only.
  // 5. Exclude AF/AG formula-owned columns.
  // 6. Never write Test Worksheet, Publish, QC Review, Run Setup, COA, METRC,
  //    key/value-store, automation, or production objects.
  // 7. Stop without partial writes on structural validation failure.
  // 8. Return controlled non-sensitive errors.
}
*/
