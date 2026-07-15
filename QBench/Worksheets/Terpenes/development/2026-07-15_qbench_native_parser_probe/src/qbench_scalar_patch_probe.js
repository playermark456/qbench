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
