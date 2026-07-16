"use strict";

importScripts("https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js");

"use strict";

(function attachScalarPatchProbe(root) {
  function validateBatchId(batchId) {
    if (!(typeof batchId === "number" || (typeof batchId === "string" && batchId.trim()))) throw new Error("CONTROLLED_BATCH_CONTEXT_REQUIRED");
  }

  function buildRequest(batchId) {
    validateBatchId(batchId);
    return {
      batchId,
      data: {
        probe_text: { value: "sandbox_probe" },
        probe_number: { value: 1.25 },
      },
    };
  }

  function execute(service, batchId) {
    const request = buildRequest(batchId);
    return new Promise((resolve, reject) => {
      service.patchWorksheet(Object.assign({}, request, { success: resolve, error: reject }));
    });
  }

  root.QBenchScalarPatchProbe = Object.freeze({ buildRequest, execute, validateBatchId });
})(typeof globalThis !== "undefined" ? globalThis : self);


run(async () => {
  try {
    const context = globalThis.QBenchProbeRuntimeContext;
    if (!context || context.authorized_stage !== "3") throw new Error("CONTROLLED_STAGE_AUTHORIZATION_REQUIRED");
    if (typeof QBBatchService !== "function") throw new Error("EXACT_QBJS_IMPORT_REQUIRED");
    const service = new QBBatchService();
    await QBenchScalarPatchProbe.execute(service, context.batchId);
    QB.success();
  } catch (_error) {
    QB.error("CONTROLLED_STAGE_ERROR");
  }
});
