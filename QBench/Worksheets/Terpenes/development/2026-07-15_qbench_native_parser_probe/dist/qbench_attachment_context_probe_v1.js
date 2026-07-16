"use strict";

importScripts("https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js");

"use strict";

(function attachAttachmentContextProbe(root) {
  const CANDIDATE_PATHS = Object.freeze([
    "QB.batch",
    "QB.currentBatch",
    "QB.context",
    "QB.context.batch",
    "QB.context.batch.id",
    "QB.context.batchId",
    "QB.context.batch_id",
    "QB.fileParserContext",
    "QB.fileParserContext.batch",
    "QB.fileParserContext.batch.id",
    "QB.fileParserContext.batchId",
    "QB.fileParserContext.batch_id",
    "QB.location",
    "QB.location.id",
    "QB.location.batch",
    "QB.location.batch.id",
    "QB.location.batchId",
    "QB.location.batch_id",
    "QB.file",
    "QB.file.id",
    "QB.file.batch",
    "QB.file.batch.id",
    "QB.file.batchId",
    "QB.file.batch_id",
    "QB.file.location",
    "QB.file.location.id",
    "QB.file.parent",
    "QB.file.parent.id",
    "QB.file.objectId",
    "QB.file.object_id",
    "QB.attachment",
    "QB.attachment.id",
    "QB.attachment.batch",
    "QB.attachment.batch.id",
    "QB.attachment.batchId",
    "QB.attachment.batch_id",
    "QB.attachment.location",
    "QB.attachment.location.id",
    "QB.attachment.parent",
    "QB.attachment.parent.id",
    "QB.attachment.objectId",
    "QB.attachment.object_id",
  ]);

  function valueType(value) {
    if (value === null) return "null";
    if (Array.isArray(value)) return "array";
    return typeof value;
  }

  function isContainer(value) {
    return value !== null && (typeof value === "object" || typeof value === "function");
  }

  function readCandidate(qb, path) {
    const segments = path.split(".").slice(1);
    let current = qb;
    for (const segment of segments) {
      if (!isContainer(current) || !Object.prototype.hasOwnProperty.call(current, segment)) {
        return Object.freeze({ path, present: false, value_type: "undefined" });
      }
      current = current[segment];
    }
    return Object.freeze({ path, present: true, value_type: valueType(current) });
  }

  function safeSummary(qb) {
    return Object.freeze({
      candidate_paths: Object.freeze(CANDIDATE_PATHS.map((path) => readCandidate(qb, path))),
    });
  }

  function logSafe(qb, message) {
    if (typeof qb.console === "function") qb.console(message);
    else qb.console.log(message);
  }

  async function execute(qb) {
    try {
      logSafe(qb, "Stage 2B context probe = entered");
      const summary = safeSummary(qb);
      summary.candidate_paths.forEach((item) => {
        logSafe(qb, `${item.path} present=${item.present} type=${item.value_type}`);
      });
      logSafe(qb, "Stage 2B context probe = complete");
      qb.success();
      return summary;
    } catch (error) {
      logSafe(qb, "controlled error = CONTROLLED_ATTACHMENT_CONTEXT_PROBE_ERROR");
      qb.error("CONTROLLED_ATTACHMENT_CONTEXT_PROBE_ERROR");
      throw error;
    }
  }

  root.QBenchAttachmentContextProbe = Object.freeze({
    CANDIDATE_PATHS,
    execute,
    readCandidate,
    safeSummary,
    valueType,
  });

  if (typeof run === "function") run(async () => { await execute(QB); });
})(typeof globalThis !== "undefined" ? globalThis : self);
