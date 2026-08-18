"use strict";

importScripts("https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js");

"use strict";

(function attachBatchContextProbe(root) {
  const CANDIDATE_PATHS = ["batch", "currentBatch", "context", "fileParserContext", "attachment"];

  function valueType(value) {
    if (value === null) return "null";
    if (Array.isArray(value)) return "array";
    return typeof value;
  }

  function safeSummary(qb) {
    const files = Array.isArray(qb.files) ? qb.files : [];
    return Object.freeze({
      qb_keys: Object.keys(qb).sort(),
      candidate_paths: CANDIDATE_PATHS.map((key) => ({
        path: `QB.${key}`,
        present: Object.prototype.hasOwnProperty.call(qb, key),
        value_type: valueType(qb[key]),
      })),
      files: files.map((file) => ({
        name: String(file && file.name ? file.name : ""),
        type: String(file && file.type ? file.type : ""),
        size: Number(file && Number.isFinite(file.size) ? file.size : 0),
      })),
    });
  }

  function logSummary(qb, summary) {
    const log = typeof qb.console === "function"
      ? (message) => qb.console(message)
      : (message) => qb.console.log(message);
    log(`QB keys = ${summary.qb_keys.join(",")}`);
    summary.candidate_paths.forEach((item) => log(`${item.path} present=${item.present} type=${item.value_type}`));
    summary.files.forEach((file) => log(`file name=${file.name} type=${file.type} size=${file.size}`));
  }

  async function execute(qb) {
    const summary = safeSummary(qb);
    logSummary(qb, summary);
    qb.success();
    return summary;
  }

  root.QBenchBatchContextProbe = Object.freeze({ CANDIDATE_PATHS, execute, safeSummary });

  if (typeof run === "function") run(async () => { await execute(QB); });
})(typeof globalThis !== "undefined" ? globalThis : self);
