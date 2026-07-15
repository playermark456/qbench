"use strict";

importScripts("https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js");

"use strict";

(function attachRangePatchProbe(root) {
  function validateBatchId(batchId) {
    if (!(typeof batchId === "number" || (typeof batchId === "string" && batchId.trim()))) throw new Error("CONTROLLED_BATCH_CONTEXT_REQUIRED");
  }

  function buildRequest(batchId, shape) {
    validateBatchId(batchId);
    const values = [1.25, 2.5, 3.75];
    if (shape !== "one_dimensional" && shape !== "one_row_two_dimensional") throw new Error("CONTROLLED_RANGE_SHAPE_REQUIRED");
    return {
      batchId,
      data: {
        probe_small_range: { value: shape === "one_dimensional" ? values : [values] },
      },
    };
  }

  function buildMatrixRequest(batchId) {
    validateBatchId(batchId);
    return { batchId, data: { probe_small_matrix: { value: [[1, 2], [3, 4]] } } };
  }

  function execute(service, request) {
    return new Promise((resolve, reject) => {
      service.patchWorksheet(Object.assign({}, request, { success: resolve, error: reject }));
    });
  }

  root.QBenchRangePatchProbe = Object.freeze({ buildMatrixRequest, buildRequest, execute, validateBatchId });
})(typeof globalThis !== "undefined" ? globalThis : self);


run(async () => {
  try {
    const context = globalThis.QBenchProbeRuntimeContext;
    if (!context || context.authorized_stage !== "4") throw new Error("CONTROLLED_STAGE_AUTHORIZATION_REQUIRED");
    if (typeof QBBatchService !== "function") throw new Error("EXACT_QBJS_IMPORT_REQUIRED");
    const service = new QBBatchService();
    await QBenchRangePatchProbe.execute(service, QBenchRangePatchProbe.buildRequest(context.batchId, "one_dimensional"));
    QB.success();
  } catch (_error) {
    QB.error("CONTROLLED_STAGE_ERROR");
  }
});
