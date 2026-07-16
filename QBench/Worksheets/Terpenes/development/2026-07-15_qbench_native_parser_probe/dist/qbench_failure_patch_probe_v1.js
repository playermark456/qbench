"use strict";

importScripts("https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js");

"use strict";

(function attachFailurePatchProbe(root) {
  function validateBatchId(batchId) {
    if (!(typeof batchId === "number" || (typeof batchId === "string" && batchId.trim()))) throw new Error("CONTROLLED_BATCH_CONTEXT_REQUIRED");
  }

  function buildMixedValidityRequest(batchId) {
    validateBatchId(batchId);
    return {
      batchId,
      data: {
        probe_text: { value: "failure_probe_valid_field" },
        probe_intentionally_invalid_field: { value: "controlled_invalid_field" },
      },
    };
  }

  function buildSequentialRequests(batchId) {
    validateBatchId(batchId);
    return [
      { batchId, data: { probe_text: { value: "sequential_first_patch" } } },
      { batchId, data: { probe_intentionally_invalid_field: { value: "controlled_invalid_field" } } },
    ];
  }

  function execute(service, request) {
    return new Promise((resolve, reject) => {
      service.patchWorksheet(Object.assign({}, request, { success: resolve, error: reject }));
    });
  }

  root.QBenchFailurePatchProbe = Object.freeze({ buildMixedValidityRequest, buildSequentialRequests, execute });
})(typeof globalThis !== "undefined" ? globalThis : self);


run(async () => {
  try {
    const context = globalThis.QBenchProbeRuntimeContext;
    if (!context || context.authorized_stage !== "6") throw new Error("CONTROLLED_STAGE_AUTHORIZATION_REQUIRED");
    if (typeof QBBatchService !== "function") throw new Error("EXACT_QBJS_IMPORT_REQUIRED");
    const service = new QBBatchService();
    await QBenchFailurePatchProbe.execute(service, QBenchFailurePatchProbe.buildMixedValidityRequest(context.batchId));
    QB.success();
  } catch (_error) {
    QB.error("CONTROLLED_STAGE_ERROR");
  }
});
