"use strict";

(function attachFixturePatchTemplate(root) {
  const FIXTURE_NAME = "Output_redacted_fixture.txt";
  const FIXTURE_SHA256 = "ed796c690b972ca08f1976b1d8f7355d3e5140e73ffa912c441d6185a093283b";

  function validateParsed(parsed) {
    const counts = parsed.counts;
    if (counts.compound_result_row_count !== 24 || counts.peak_table_row_count !== 34 || counts.reportable_compound_row_count !== 23 || counts.dimethylacetamide_row_count !== 1) {
      throw new Error("CONTROLLED_FIXTURE_COUNTS_INVALID");
    }
    if (parsed.reportable_analytes.some((row) => typeof row.conc !== "number")) throw new Error("CONTROLLED_FIXTURE_NUMERIC_VALUES_REQUIRED");
    if (typeof parsed.dimethylacetamide_audit.conc !== "number") throw new Error("CONTROLLED_AUDIT_NUMBER_REQUIRED");
  }

  function buildWritePlan(parsed, fixtureHash) {
    validateParsed(parsed);
    const leading = Array(31).fill("");
    leading[13] = FIXTURE_NAME;
    leading[14] = fixtureHash || "hash_unavailable_structural_validation_passed";
    leading[22] = parsed.parser_core_version;
    leading[23] = 24;
    leading[24] = 34;
    leading[25] = 23;
    leading[26] = parsed.dimethylacetamide_audit.conc;
    leading[30] = "Not Reviewed";
    const analytes = parsed.reportable_analytes.map((row) => row.conc);
    const sourceIdentity = fixtureHash || "fixture_hash_unavailable";
    const trailing = analytes.concat([sourceIdentity]);
    if (leading.length !== 31 || trailing.length !== 24) throw new Error("CONTROLLED_WRITE_PLAN_WIDTH_INVALID");
    return Object.freeze({
      terpenes_probe_import_row_2_leading: { value: leading },
      terpenes_probe_import_row_2_analytes: { value: trailing },
    });
  }

  async function execute(service, batchId, parsed, fixtureHash) {
    if (!batchId) throw new Error("CONTROLLED_BATCH_CONTEXT_REQUIRED");
    if (fixtureHash && fixtureHash !== FIXTURE_SHA256) throw new Error("CONTROLLED_FIXTURE_HASH_MISMATCH");
    const data = buildWritePlan(parsed, fixtureHash);
    return new Promise((resolve, reject) => {
      service.patchWorksheet({ batchId, data, success: resolve, error: reject });
    });
  }

  root.QBenchTerpenesFixturePatchTemplate = Object.freeze({ FIXTURE_NAME, FIXTURE_SHA256, buildWritePlan, execute, validateParsed });
})(typeof globalThis !== "undefined" ? globalThis : self);
