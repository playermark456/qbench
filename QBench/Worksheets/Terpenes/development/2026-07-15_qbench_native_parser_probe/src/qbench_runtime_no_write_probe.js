"use strict";

(function attachNoWriteProbe(root) {
  const FIXTURE_NAME = "Output_redacted_fixture.txt";

  function logSafe(qb, message) {
    if (typeof qb.console === "function") qb.console(message);
    else if (qb.console && typeof qb.console.log === "function") qb.console.log(message);
  }

  function readFileAsText(file, Reader) {
    return new Promise((resolve, reject) => {
      const reader = new Reader();
      reader.onload = () => resolve(String(reader.result || ""));
      reader.onerror = () => reject(new Error("CONTROLLED_FILE_READ_ERROR"));
      reader.readAsText(file);
    });
  }

  function validateFiles(files) {
    if (!Array.isArray(files) || files.length !== 1) throw new Error("CONTROLLED_FILE_COUNT_ERROR");
    const file = files[0];
    const name = String(file && file.name ? file.name : "");
    if (name !== FIXTURE_NAME || !/\.txt$/i.test(name)) throw new Error("CONTROLLED_FILE_NAME_ERROR");
    return file;
  }

  function summaryFromParsed(parsed, webCryptoAvailable) {
    return Object.freeze({
      file_count: 1,
      extension_accepted: ".txt",
      compound_result_rows: parsed.counts.compound_result_row_count,
      peak_table_rows: parsed.counts.peak_table_row_count,
      reportable_channels: parsed.counts.reportable_compound_row_count,
      dimethylacetamide_audit_rows: parsed.counts.dimethylacetamide_row_count,
      web_crypto_available: webCryptoAvailable,
    });
  }

  async function execute(qb, Reader, config, core) {
    try {
      const file = validateFiles(qb.files);
      const text = await readFileAsText(file, Reader);
      const parsed = core.parseLabSolutionsAscii(text, config, { securityLimits: root.QBenchProbeLimits });
      const summary = summaryFromParsed(parsed, Boolean(root.crypto && root.crypto.subtle));
      logSafe(qb, `file count = ${summary.file_count}`);
      logSafe(qb, `extension accepted = ${summary.extension_accepted}`);
      logSafe(qb, `Compound Results rows = ${summary.compound_result_rows}`);
      logSafe(qb, `Peak Table rows = ${summary.peak_table_rows}`);
      logSafe(qb, `reportable channels = ${summary.reportable_channels}`);
      logSafe(qb, `Dimethylacetamide audit rows = ${summary.dimethylacetamide_audit_rows}`);
      logSafe(qb, `Web Crypto available = ${summary.web_crypto_available}`);
      qb.success();
      return summary;
    } catch (error) {
      const safe = core.toControlledError(error);
      logSafe(qb, `controlled error = ${safe.code}`);
      qb.error(safe.code);
      throw error;
    }
  }

  root.QBenchRuntimeNoWriteProbe = Object.freeze({
    FIXTURE_NAME,
    execute,
    readFileAsText,
    summaryFromParsed,
    validateFiles,
  });

  if (typeof run === "function") {
    run(async () => {
      await execute(QB, FileReader, QBenchProbeConfig, QBenchTerpenesParserCore);
    });
  }
})(typeof globalThis !== "undefined" ? globalThis : self);
