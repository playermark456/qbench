"use strict";

(function attachNoWriteProbe(root) {
  const FIXTURE_NAME = "Output_redacted_fixture.txt";
  const CONTROLLED_ERROR_CODES = Object.freeze({
    FILE_COLLECTION: "CONTROLLED_FILE_COLLECTION_ERROR",
    FILE_COUNT: "CONTROLLED_FILE_COUNT_ERROR",
    FILE_OBJECT: "CONTROLLED_FILE_OBJECT_ERROR",
    FILE_NAME: "CONTROLLED_FILE_NAME_ERROR",
    FILE_READ: "CONTROLLED_FILE_READ_ERROR",
  });

  class ControlledRuntimeError extends Error {
    constructor(code) {
      super(code);
      this.name = "ControlledRuntimeError";
      this.code = code;
    }
  }

  function controlledError(code) {
    return new ControlledRuntimeError(code);
  }

  function logSafe(qb, message) {
    if (typeof qb.console === "function") qb.console(message);
    else if (qb.console && typeof qb.console.log === "function") qb.console.log(message);
  }

  function readFileAsText(file, Reader) {
    return new Promise((resolve, reject) => {
      let reader;
      try {
        reader = new Reader();
      } catch (_error) {
        reject(controlledError(CONTROLLED_ERROR_CODES.FILE_READ));
        return;
      }
      reader.onload = () => resolve(String(reader.result || ""));
      reader.onerror = () => reject(controlledError(CONTROLLED_ERROR_CODES.FILE_READ));
      try {
        reader.readAsText(file);
      } catch (_error) {
        reject(controlledError(CONTROLLED_ERROR_CODES.FILE_READ));
      }
    });
  }

  function fileCollectionKind(files) {
    if (Array.isArray(files)) return "Array";
    if (!files || typeof files !== "object") return "unknown";
    try {
      return "length" in files ? "array_like" : "unknown";
    } catch (_error) {
      return "unknown";
    }
  }

  function normalizeFileCollection(files) {
    const kind = fileCollectionKind(files);
    if (kind === "unknown") throw controlledError(CONTROLLED_ERROR_CODES.FILE_COLLECTION);

    let length;
    try {
      length = files.length;
    } catch (_error) {
      throw controlledError(CONTROLLED_ERROR_CODES.FILE_COLLECTION);
    }
    if (!Number.isFinite(length) || !Number.isInteger(length) || length < 0) {
      throw controlledError(CONTROLLED_ERROR_CODES.FILE_COLLECTION);
    }
    if (length !== 1) throw controlledError(CONTROLLED_ERROR_CODES.FILE_COUNT);

    let file;
    try {
      file = files[0];
      if (!file && typeof files.item === "function") file = files.item(0);
    } catch (_error) {
      throw controlledError(CONTROLLED_ERROR_CODES.FILE_OBJECT);
    }
    if (!file || typeof file !== "object") {
      throw controlledError(CONTROLLED_ERROR_CODES.FILE_OBJECT);
    }
    return Object.freeze({ file, kind, count: length });
  }

  function hasTxtExtension(name) {
    return /\.txt$/i.test(String(name || ""));
  }

  function validateFileMetadata(file) {
    const name = typeof file.name === "string" ? file.name : "";
    if (name !== FIXTURE_NAME || !hasTxtExtension(name)) {
      throw controlledError(CONTROLLED_ERROR_CODES.FILE_NAME);
    }
    return file;
  }

  function validateFiles(files) {
    const normalized = normalizeFileCollection(files);
    return validateFileMetadata(normalized.file);
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
    let failedStep = "runtime entered";
    try {
      logSafe(qb, "probe step = runtime entered");
      failedStep = "file collection validation";
      const kind = fileCollectionKind(qb.files);
      logSafe(qb, `file collection kind = ${kind}`);
      const normalized = normalizeFileCollection(qb.files);
      logSafe(qb, "probe step = file collection accepted");
      logSafe(qb, `file count = ${normalized.count}`);

      failedStep = "file metadata validation";
      const file = validateFileMetadata(normalized.file);
      logSafe(qb, "probe step = file metadata accepted");
      logSafe(qb, "extension accepted = .txt");

      failedStep = "file read";
      const text = await readFileAsText(file, Reader);
      logSafe(qb, "probe step = file read complete");

      failedStep = "controlled parse";
      const parsed = core.parseLabSolutionsAscii(text, config, { securityLimits: root.QBenchProbeLimits });
      logSafe(qb, "probe step = controlled parse complete");
      const summary = summaryFromParsed(parsed, Boolean(root.crypto && root.crypto.subtle));
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
      logSafe(qb, `failed step = ${failedStep}`);
      qb.error(safe.code);
      throw error;
    }
  }

  root.QBenchRuntimeNoWriteProbe = Object.freeze({
    CONTROLLED_ERROR_CODES,
    ControlledRuntimeError,
    FIXTURE_NAME,
    controlledError,
    execute,
    fileCollectionKind,
    hasTxtExtension,
    normalizeFileCollection,
    readFileAsText,
    summaryFromParsed,
    validateFileMetadata,
    validateFiles,
  });

  if (typeof run === "function") {
    run(async () => {
      await execute(QB, FileReader, QBenchProbeConfig, QBenchTerpenesParserCore);
    });
  }
})(typeof globalThis !== "undefined" ? globalThis : self);
