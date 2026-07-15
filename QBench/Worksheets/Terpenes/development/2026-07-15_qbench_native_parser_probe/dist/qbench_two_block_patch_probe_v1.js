"use strict";

importScripts("https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js");

"use strict";

(function attachTwoBlockPatchProbe(root) {
  function validateBatchId(batchId) {
    if (!(typeof batchId === "number" || (typeof batchId === "string" && batchId.trim()))) throw new Error("CONTROLLED_BATCH_CONTEXT_REQUIRED");
  }

  function sequence(count, offset) {
    return Array.from({ length: count }, (_value, index) => offset + index + 0.25);
  }

  function buildRequest(batchId) {
    validateBatchId(batchId);
    return {
      batchId,
      data: {
        probe_block_a_ae: { value: sequence(31, 0) },
        probe_block_ah_be: { value: sequence(24, 100) },
      },
    };
  }

  function buildSequentialRequests(batchId) {
    const request = buildRequest(batchId);
    return [
      { batchId, data: { probe_block_a_ae: request.data.probe_block_a_ae } },
      { batchId, data: { probe_block_ah_be: request.data.probe_block_ah_be } },
    ];
  }

  function execute(service, request) {
    return new Promise((resolve, reject) => {
      service.patchWorksheet(Object.assign({}, request, { success: resolve, error: reject }));
    });
  }

  root.QBenchTwoBlockPatchProbe = Object.freeze({ buildRequest, buildSequentialRequests, execute });
})(typeof globalThis !== "undefined" ? globalThis : self);


run(async () => {
  try {
    const context = globalThis.QBenchProbeRuntimeContext;
    if (!context || context.authorized_stage !== "5") throw new Error("CONTROLLED_STAGE_AUTHORIZATION_REQUIRED");
    if (typeof QBBatchService !== "function") throw new Error("EXACT_QBJS_IMPORT_REQUIRED");
    const service = new QBBatchService();
    await QBenchTwoBlockPatchProbe.execute(service, QBenchTwoBlockPatchProbe.buildRequest(context.batchId));
    QB.success();
  } catch (_error) {
    QB.error("CONTROLLED_STAGE_ERROR");
  }
});
