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
