importScripts("https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js");
importScripts("https://d731z7k534aiw.cloudfront.net/v2.7.0/qbjs.js");
"use strict";

(function attachScalarPatchProbe(root) {
  function log(message) {
    if (typeof QB.console === "function") QB.console(message);
    else QB.console.log(message);
  }

  function sanitize(value) {
    var text = value && typeof value.message === "string" ? value.message : String(value || "UNKNOWN_ERROR");
    return text.replace(/\b\d+\b/g, "[number]").slice(0, 240);
  }

  function validateBatchId(batchId) {
    var validNumber = typeof batchId === "number" && Number.isFinite(batchId);
    var validString = typeof batchId === "string" && batchId.trim().length > 0;
    if (!validNumber && !validString) throw new Error("CONTROLLED_BATCH_CONTEXT_REQUIRED");
  }

  function validateRequest(request) {
    var requestKeys = Object.keys(request).sort().join(",");
    var dataKeys = Object.keys(request.data || {}).sort().join(",");
    if (requestKeys !== "batchId,data,error,success") throw new Error("INVALID_REQUEST_KEYS");
    validateBatchId(request.batchId);
    if (dataKeys !== "probe_number,probe_text") throw new Error("INVALID_DATA_KEYS");
    if (!request.data.probe_text || request.data.probe_text.value !== "sandbox_probe") throw new Error("INVALID_TEXT_VALUE");
    if (!request.data.probe_number || typeof request.data.probe_number.value !== "number" || request.data.probe_number.value !== 1.25 || !Number.isFinite(request.data.probe_number.value)) throw new Error("INVALID_NUMBER_VALUE");
    if (typeof request.success !== "function" || typeof request.error !== "function") throw new Error("INVALID_CALLBACKS");
    return request;
  }

  function buildRequest(batchId, resolve, reject) {
    return validateRequest({
      batchId: batchId,
      data: {
        probe_text: { value: "sandbox_probe" },
        probe_number: { value: 1.25 }
      },
      success: function (result) {
        log("patch_callback = success");
        resolve(result);
      },
      error: function (error) {
        var sanitized = sanitize(error);
        log("patch_callback = error; sanitized_error = " + sanitized);
        reject(new Error("PATCH_WORKSHEET_ERROR_CALLBACK: " + sanitized));
      }
    });
  }

  function execute(service, context) {
    if (!context || context.authorized_stage !== "3") throw new Error("CONTROLLED_STAGE_AUTHORIZATION_REQUIRED");
    return new Promise(function (resolve, reject) {
      service.patchWorksheet(buildRequest(context.batchId, resolve, reject));
    });
  }

  root.QBenchScalarPatchProbe = Object.freeze({ buildRequest: buildRequest, execute: execute, validateRequest: validateRequest });

  run(async function () {
    try {
      if (typeof QBBatchService !== "function") throw new Error("EXACT_QBJS_IMPORT_REQUIRED");
      var service = new QBBatchService();
      await execute(service, root.QBenchProbeRuntimeContext);
      QB.success();
    } catch (error) {
      log("controlled_error = " + sanitize(error));
      QB.error("CONTROLLED_STAGE_ERROR");
    }
  });
})(typeof globalThis !== "undefined" ? globalThis : self);
