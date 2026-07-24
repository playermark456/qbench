"use strict";

/* Builds the uploadable browser source from the locally validated core and adapter. */
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");

const PACKAGE = path.resolve(__dirname, "..");
const REPO = path.resolve(PACKAGE, "../../../../..");
const CORE = path.join(PACKAGE, "src", "qbench_browser_parser_core.js");
const ADAPTER = path.join(PACKAGE, "src", "terpenes_multirecord_batch_adapter.js");
const CONFIG = path.join(REPO, "QBench", "Worksheets", "Terpenes", "development", "2026-07-14_config_parser_foundation", "config", "terpenes_analytes.json");
const OUTPUT = path.join(PACKAGE, "dist", "terpenes_multirecord_qbench_parser.js");

function browserSource(source) {
  return source.replace(/\n\s*if \(typeof module !== "undefined" && module\.exports\) module\.exports = api;\n/, "\n");
}

const RUNTIME = String.raw`
const TERPENES_CONFIG = __CONFIG__;
const TERPENES_TAB = "Instrument Import";
const TERPENES_HEADER = QBenchTerpenesMultiRecordBatchAdapter.BATCH_HEADERS.slice();
const TERPENES_FORMULA_COLUMNS = new Set([31, 32]);
const TERPENES_PARSER_VERSION = "terpenes-qbench-coded-parser-v1";

function terpeneColumn(index) { let value = ""; let n = index + 1; while (n) { const m = (n - 1) % 26; value = String.fromCharCode(65 + m) + value; n = Math.floor((n - 1) / 26); } return value; }
function terpeneA1(column, row) { return terpeneColumn(column) + row; }
function terpeneCell(value) { return value === undefined || value === null ? "" : String(value).trim(); }
function terpeneGridToMap(grid) { const map = {}; (grid || []).forEach((row, r) => (row || []).forEach((value, c) => { if (value !== "" && value !== null && value !== undefined) map[terpeneA1(c, r + 1)] = value; })); return map; }
function terpeneIsSample(row) { return row.category === "Sample"; }
function terpeneCandidateId(row) { return terpeneIsSample(row) && row.sample_id && !/^\s*$/.test(row.sample_id) ? String(row.sample_id).trim() : ""; }
function terpeneSha256(text) {
  const bytes = unescape(encodeURIComponent(String(text))); const words = []; const bitLength = bytes.length * 8;
  for (let i = 0; i < bytes.length; i += 1) words[i >> 2] = (words[i >> 2] || 0) | (bytes.charCodeAt(i) << (24 - (i % 4) * 8));
  words[bitLength >> 5] = (words[bitLength >> 5] || 0) | (0x80 << (24 - (bitLength % 32)));
  words[((bitLength + 64 >> 9) << 4) + 15] = bitLength;
  const k = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
  let h0=0x6a09e667,h1=0xbb67ae85,h2=0x3c6ef372,h3=0xa54ff53a,h4=0x510e527f,h5=0x9b05688c,h6=0x1f83d9ab,h7=0x5be0cd19;
  for (let offset=0; offset<words.length; offset+=16) { const w=[]; for(let i=0;i<64;i+=1){ if(i<16) w[i]=words[offset+i]||0; else { const a=w[i-15], b=w[i-2]; const s0=((a>>>7)|(a<<25))^((a>>>18)|(a<<14))^(a>>>3); const s1=((b>>>17)|(b<<15))^((b>>>19)|(b<<13))^(b>>>10); w[i]=(((w[i-16]+s0)|0)+((w[i-7]+s1)|0))|0; }} let a=h0,b=h1,c=h2,d=h3,e=h4,f=h5,g=h6,h=h7; for(let i=0;i<64;i+=1){ const s1=((e>>>6)|(e<<26))^((e>>>11)|(e<<21))^((e>>>25)|(e<<7)); const ch=(e&f)^((~e)&g); const t1=(((h+s1)|0)+((ch+k[i])|0)+w[i])|0; const s0=((a>>>2)|(a<<30))^((a>>>13)|(a<<19))^((a>>>22)|(a<<10)); const maj=(a&b)^(a&c)^(b&c); const t2=(s0+maj)|0; h=g;g=f;f=e;e=(d+t1)|0;d=c;c=b;b=a;a=(t1+t2)|0; } h0=(h0+a)|0;h1=(h1+b)|0;h2=(h2+c)|0;h3=(h3+d)|0;h4=(h4+e)|0;h5=(h5+f)|0;h6=(h6+g)|0;h7=(h7+h)|0; }
  return [h0,h1,h2,h3,h4,h5,h6,h7].map((v) => (v >>> 0).toString(16).padStart(8,"0")).join("");
}
function terpeneReadText(file) { return new Promise((resolve,reject) => { const reader=new FileReader(); reader.onload=(event)=>resolve(String(event.target.result)); reader.onerror=()=>reject(new Error("FILE_READ_FAILED")); reader.readAsText(file); }); }
function terpenePapaValidate(text, extension) { const parsed=Papa.parse(text,{delimiter:extension === "txt" ? "\t" : "",skipEmptyLines:false}); if (parsed.errors && parsed.errors.length) throw new Error("DELIMITED_INPUT_INVALID"); }
function terpeneCall(fn) { return new Promise((resolve,reject) => { try { const value=fn(resolve,reject); if(value && typeof value.then === "function") value.then(resolve,reject); } catch(error) { reject(error); } }); }
function terpeneDocumentList(payload) { if(Array.isArray(payload)) return payload; if(payload && Array.isArray(payload.data)) return payload.data; if(payload && typeof payload === "object") return Object.values(payload).filter((value)=>value && typeof value === "object"); return []; }
function terpeneGetDocument(documents, type) { return documents.find((item)=>item && item.worksheet_name === TERPENES_TAB && item.type === type); }
function terpeneDocumentGrid(documents, type) { const item=terpeneGetDocument(documents,type); return item && Array.isArray(item.data) ? item.data : null; }
function terpeneDocumentMap(documents, type) { const item=terpeneGetDocument(documents,type); return item && item.data && typeof item.data === "object" && !Array.isArray(item.data) ? item.data : {}; }
function terpeneRequireHeader(grid) { const header=(grid && grid[0]) || []; if(header.length !== TERPENES_HEADER.length || header.some((value,index)=>value !== TERPENES_HEADER[index])) throw new Error("INSTRUMENT_IMPORT_HEADER_MISMATCH"); }
function terpeneSetCell(dataMap, procMap, column, row, value) { const a1=terpeneA1(column,row); const native=value === undefined || value === null ? "" : value; dataMap[a1]=native; procMap[a1]=native === "" ? "" : String(native); }
function terpeneApplyRange(dataMap, procMap, rows) { for(let row=2;row<=201;row+=1){ for(let column=0;column<57;column+=1){ if(TERPENES_FORMULA_COLUMNS.has(column)) continue; terpeneSetCell(dataMap,procMap,column,row,""); }} rows.forEach((record,index)=>{ const destination=index+2; record.batch_row.forEach((value,column)=>{ if(!TERPENES_FORMULA_COLUMNS.has(column)) terpeneSetCell(dataMap,procMap,column,destination,value); }); }); }
function terpeneCategoryCounts(rows) { const result={}; rows.forEach((row)=>{result[row.category]=(result[row.category]||0)+1;}); return result; }

run(async () => {
  const qbConsole=QB.console; const qbProgress=QB.progressBar; let failed=false;
  const fail=(error) => { if(failed) return; failed=true; qbConsole.log("ERROR: " + String(error && error.message ? error.message : error).replace(/[\r\n]/g," ").slice(0,180)); QB.error(); };
  try {
    qbProgress.setPercentage(0); qbConsole.clear();
    const selected=Array.isArray(QB.files) ? QB.files : Object.values(QB.files || {});
    if(selected.length !== 1) throw new Error("EXACTLY_ONE_SOURCE_FILE_REQUIRED");
    const file=selected[0]; const extension=String(file && file.name || "").split(".").pop().toLowerCase();
    if(extension !== "txt" && extension !== "csv") throw new Error("UNSUPPORTED_FILE_TYPE");
    const source=await terpeneReadText(file); terpenePapaValidate(source,extension);
    const sourceHash=terpeneSha256(source); const parsed=QBenchTerpenesParserCore.parseLabSolutionsAsciiMultiRecord(source,TERPENES_CONFIG);
    const normalized=QBenchTerpenesMultiRecordBatchAdapter.normalizeRecords(parsed,TERPENES_CONFIG,{source_file_sha256:sourceHash,runtime_mapping:[]});
    if(normalized.rows.length > 200) throw new Error("INSTRUMENT_IMPORT_ROW_CAPACITY_EXCEEDED");
    const candidates=[]; normalized.rows.forEach((row)=>{const id=terpeneCandidateId(row); if(id) candidates.push(id);});
    const svc=new QBBatchService(); const resolution={}; const batches=new Set();
    for(const candidate of Array.from(new Set(candidates))) { const response=await terpeneCall((resolve,reject)=>svc.getJson({url:"/batches/get",urlParams:{test_id:candidate},success:resolve,error:reject})); const matches=Array.isArray(response)?response:(response && Array.isArray(response.data)?response.data:[]); const ids=Array.from(new Set(matches.map((item)=>item && item.id).filter((id)=>id !== undefined && id !== null).map(String))); if(ids.length > 1) throw new Error("AMBIGUOUS_TEST_BATCH_RESOLUTION"); if(ids.length === 1){resolution[candidate]=ids[0]; batches.add(ids[0]);} }
    const resolvedRows=normalized.rows.filter((row)=>resolution[terpeneCandidateId(row)]); if(!resolvedRows.length) throw new Error("NO_TEST_IDS_RESOLVED");
    const duplicate=new Set(); const seen=new Set(); resolvedRows.forEach((row)=>{const id=terpeneCandidateId(row); if(seen.has(id)) duplicate.add(id); seen.add(id);}); if(duplicate.size) throw new Error("DUPLICATE_RESOLVED_TEST_ID");
    if(batches.size !== 1) throw new Error("RESOLVED_TESTS_MUST_HAVE_ONE_BATCH"); const batchId=Array.from(batches)[0];
    normalized.rows.forEach((row)=>{const candidate=terpeneCandidateId(row); const linked=Boolean(candidate && resolution[candidate]); row.qbench_test_display_id=linked ? candidate : ""; row.linkage_status=!terpeneIsSample(row)?"control_excluded":(linked?"matched_sample_id":"held_unmapped"); row.transfer_eligible=linked; row.batch_row[4]=linked ? candidate : ""; row.batch_row[22]=TERPENES_PARSER_VERSION;});
    qbProgress.setPercentage(35);
    const documents=terpeneDocumentList(await terpeneCall((resolve,reject)=>svc.getJson({url:"/batches/worksheets/dynamic",urlParams:{entity_ids:batchId,process_references:true,construct_worksheet_data_array:true,convert_datetime_values_to_localtime:true},success:resolve,error:reject})));
    const rawGrid=terpeneDocumentGrid(documents,"WORKSHEET_DATA"); const processedGrid=terpeneDocumentGrid(documents,"WORKSHEET_DATA_PROCESSED"); if(!rawGrid || !processedGrid) throw new Error("INSTRUMENT_IMPORT_TAB_MISSING"); terpeneRequireHeader(processedGrid); if(rawGrid.length < 201 || processedGrid.length < 201) throw new Error("INSTRUMENT_IMPORT_ROW_CAPACITY_EXCEEDED");
    const formulas=terpeneDocumentMap(documents,"WORKSHEET_FORMULAS"); const images=terpeneDocumentMap(documents,"WORKSHEET_IMAGE_DATA"); const references=terpeneDocumentMap(documents,"WORKSHEET_DOLLAR_REFERENCES");
    const dataMap=terpeneGridToMap(rawGrid); const procMap=terpeneGridToMap(processedGrid); terpeneApplyRange(dataMap,procMap,normalized.rows);
    qbProgress.setPercentage(80);
    await terpeneCall((resolve,reject)=>svc.update({data:{id:String(batchId),qb_dynamic_spreadsheet_data:{"Instrument Import":{WORKSHEET_DATA:dataMap,WORKSHEET_FORMULAS:formulas,WORKSHEET_IMAGE_DATA:images,WORKSHEET_DOLLAR_REFERENCES:references,WORKSHEET_DATA_PROCESSED:procMap}}},urlParams:{run_worksheet_calculations:true},success:resolve,error:reject}));
    const categories=terpeneCategoryCounts(normalized.rows); qbConsole.log("Imported records="+normalized.rows.length+" resolved="+resolvedRows.length+" held="+(categories.Sample-resolvedRows.length)+" controls="+(normalized.rows.length-categories.Sample)); qbProgress.setPercentage(100); QB.success();
  } catch(error) { fail(error); }
});
`;

function build() {
  const config = JSON.parse(fs.readFileSync(CONFIG, "utf8"));
  const artifact = [
    "/* Generated by scripts/build_qbench_parser_artifact.js; browser upload artifact. */",
    "importScripts('https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js');",
    "importScripts('https://d731z7k534aiw.cloudfront.net/v2.7.0/qbjs.js');",
    "importScripts('https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js');",
    "importScripts('https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js');",
    browserSource(fs.readFileSync(CORE, "utf8")),
    browserSource(fs.readFileSync(ADAPTER, "utf8")),
    RUNTIME.replace("__CONFIG__", JSON.stringify(config)),
    "",
  ].join("\n");
  fs.mkdirSync(path.dirname(OUTPUT), { recursive: true });
  fs.writeFileSync(OUTPUT, artifact, "utf8");
  return { path: OUTPUT, sha256: crypto.createHash("sha256").update(artifact).digest("hex"), bytes: Buffer.byteLength(artifact) };
}

if (require.main === module) process.stdout.write(`${JSON.stringify(build())}\n`);
module.exports = { build };
