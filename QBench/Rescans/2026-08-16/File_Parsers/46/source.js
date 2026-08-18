importScripts('https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js');
importScripts('https://d731z7k534aiw.cloudfront.net/v2.7.0/qbjs.js');
importScripts('https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js');
importScripts('https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js');

const TAB = 'Results';
const MATCH_COL = 1;
const HEADER_ROW = 1;
const SECTION_SAMPLE = 'Sample Information';
const SECTION_COMPOUND = 'Compound Results(Detector A)';
const SECTION_PEAK = 'Peak Table(Detector A)';
const TEST_ID_FIELD = 'Sample Name';
const TEST_ID_LABEL = 'Test ID';
const DF_KEY = 'Dilution Factor';
const MAX_UNKNOWN = 10;

function colLetter(i) {
    let s = ''; i++;
    while (i > 0) { const m = (i - 1) % 26; s = String.fromCharCode(65 + m) + s; i = Math.floor((i - 1) / 26); }
    return s;
}

function gridToA1(grid) {
    const m = {};
    for (let r = 0; r < grid.length; r++) {
        const row = grid[r] || [];
        for (let c = 0; c < row.length; c++) {
            const v = row[c];
            if (v !== '' && v !== null && v !== undefined) m[colLetter(c) + (r + 1)] = v;
        }
    }
    return m;
}

function norm(s) {
    return String(s == null ? '' : s).toUpperCase().replace(/Δ/g, 'D').replace(/DELTA[\s-]?/g, 'D').replace(/[^A-Z0-9]/g, '');
}

function cell(row, idx) {
    if (!row || row[idx] === undefined || row[idx] === null) return '';
    return String(row[idx]).trim();
}

function isBlankRow(row) {
    if (!row) return true;
    for (let i = 0; i < row.length; i++) if (cell(row, i) !== '') return false;
    return true;
}

function toNumber(raw) {
    if (raw === undefined || raw === null) return null;
    const s = String(raw).trim();
    if (s === '') return null;
    const n = Number(s);
    return Number.isFinite(n) ? n : null;
}

function getFileExtension(name) {
    return String(name).split('.').pop().toLowerCase();
}

function parseExcel(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const wb = XLSX.read(new Uint8Array(e.target.result), { type: 'array' });
                resolve(XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]], { header: 1, raw: false, defval: '' }));
            } catch (err) { reject(err); }
        };
        reader.onerror = () => reject(new Error('Failed to read Excel file'));
        reader.readAsArrayBuffer(file);
    });
}

function parseDelimited(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const parsed = Papa.parse(e.target.result, {
                header: false, skipEmptyLines: false,
                transform: (v) => (typeof v === 'string' ? v.trim() : v)
            });
            resolve(parsed.data);
        };
        reader.onerror = () => reject(new Error('Failed to read file'));
        reader.readAsText(file);
    });
}

async function parseFileTo2D(file) {
    const ext = getFileExtension(file.name);
    if (ext === 'xlsx' || ext === 'xlsm') return parseExcel(file);
    if (ext === 'csv' || ext === 'txt') return parseDelimited(file);
    throw new Error('Unsupported file type: ' + ext);
}

function segmentBlocks(rows) {
    const starts = [];
    for (let i = 0; i < rows.length; i++) if (cell(rows[i], 0) === '[Header]') starts.push(i);
    if (starts.length === 0) return [];
    const blocks = [];
    for (let s = 0; s < starts.length; s++) {
        const from = starts[s];
        const to = (s + 1 < starts.length) ? starts[s + 1] : rows.length;
        blocks.push(rows.slice(from, to));
    }
    return blocks;
}

function findSection(block, name) {
    const marker = '[' + name + ']';
    let start = -1;
    for (let i = 0; i < block.length; i++) if (cell(block[i], 0) === marker) { start = i; break; }
    if (start === -1) return null;
    let end = block.length;
    for (let i = start + 1; i < block.length; i++) {
        const c = cell(block[i], 0);
        if (c.startsWith('[') && c.endsWith(']')) { end = i; break; }
    }
    return { start, end };
}

function getSampleInfoValue(block, key) {
    const sec = findSection(block, SECTION_SAMPLE);
    if (!sec) return undefined;
    const target = key.toLowerCase().trim();
    for (let i = sec.start + 1; i < sec.end; i++) {
        if (cell(block[i], 0).toLowerCase().trim() === target) return cell(block[i], 1);
    }
    return undefined;
}

function getTableRows(block, name) {
    const sec = findSection(block, name);
    if (!sec) return null;
    let headerIdx = -1;
    for (let i = sec.start + 1; i < sec.end; i++) {
        const first = cell(block[i], 0);
        if (first === '') continue;
        if (/^#\s*of\b/i.test(first)) continue;
        headerIdx = i; break;
    }
    if (headerIdx === -1) return null;
    const headerRow = block[headerIdx];
    const dataRows = [];
    for (let i = headerIdx + 1; i < sec.end; i++) if (!isBlankRow(block[i])) dataRows.push(block[i]);
    return { headerRow, dataRows };
}

function colIndex(headerRow, name) {
    const target = name.toLowerCase().trim();
    for (let i = 0; i < headerRow.length; i++) {
        if (String(headerRow[i] || '').toLowerCase().trim() === target) return i;
    }
    return -1;
}

function extractBlock(block) {
    const out = { testId: (getSampleInfoValue(block, TEST_ID_FIELD) || '').trim(), named: {}, unknowns: [], warnings: [] };

    const df = toNumber(getSampleInfoValue(block, DF_KEY));
    if (df !== null) out.named['DF'] = df;

    const compound = getTableRows(block, SECTION_COMPOUND);
    if (!compound) {
        out.warnings.push('missing ' + SECTION_COMPOUND);
    } else {
        const h = compound.headerRow;
        const iName = colIndex(h, 'Name');
        const iConc = colIndex(h, 'Conc.');
        const iArea = colIndex(h, 'Area');
        const i2nd = colIndex(h, '2nd');
        const i1st = colIndex(h, '1st');
        const iConst = colIndex(h, 'Constant');
        const areaSet = { CBDV: 1, THCV: 1, CBL: 1 };
        for (const row of compound.dataRows) {
            const name = iName >= 0 ? cell(row, iName) : '';
            if (!name) continue;
            const key = norm(name);
            const conc = toNumber(cell(row, iConc));
            if (conc !== null) out.named[key] = conc;
            const upper = name.toUpperCase().trim();
            if (areaSet[upper] && iArea >= 0) {
                const a = toNumber(cell(row, iArea));
                if (a !== null) out.named[key + 'AREA'] = a;
            }
            if (key === 'CBD') {
                const c2 = toNumber(cell(row, i2nd)); if (c2 !== null) out.named['CBD2ND'] = c2;
                const c1 = toNumber(cell(row, i1st)); if (c1 !== null) out.named['CBD1ST'] = c1;
                const cc = toNumber(cell(row, iConst)); if (cc !== null) out.named['CBDCONSTANT'] = cc;
            }
        }
    }

    const peaks = getTableRows(block, SECTION_PEAK);
    if (peaks) {
        const pName = colIndex(peaks.headerRow, 'Name');
        const pArea = colIndex(peaks.headerRow, 'Area');
        for (const row of peaks.dataRows) {
            if (out.unknowns.length >= MAX_UNKNOWN) break;
            if (pName >= 0 && cell(row, pName)) continue;
            const a = toNumber(cell(row, pArea));
            out.unknowns.push(a === null ? '' : a);
        }
    }

    return out;
}

run(async () => {
    const qbConsole = QB.console;
    const qbProgressBar = QB.progressBar;

    const call = (fn) => new Promise((resolve, reject) => {
        try {
            const p = fn(resolve, reject);
            if (p && typeof p.then === 'function') p.then(resolve, reject);
        } catch (e) { reject(e); }
    });

    const stats = { blocks: 0, written: 0, skipped: 0, warnings: [] };

    try {
        qbProgressBar.setPercentage(0);
        qbConsole.clear();
        const svc = new QBBatchService();

        const filesObj = QB.files || {};
        const files = Array.isArray(filesObj) ? filesObj : Object.values(filesObj);
        if (files.length === 0) { qbConsole.log('ERROR: no files selected'); QB.error(); return; }
        qbConsole.log('Files: ' + files.length);

        const allBlocks = [];
        for (const f of files) {
            try {
                const rows = await parseFileTo2D(f);
                for (const b of segmentBlocks(rows)) allBlocks.push(b);
            } catch (e) {
                stats.warnings.push('File ' + (f && f.name) + ': ' + (e && e.message));
            }
        }
        stats.blocks = allBlocks.length;
        qbConsole.log('Blocks: ' + allBlocks.length);
        if (allBlocks.length === 0) { qbConsole.log('ERROR: no sample blocks found'); QB.error(); return; }
        qbProgressBar.setPercentage(10);

        const candidates = [];
        const seen = {};
        for (const b of allBlocks) {
            const t = (getSampleInfoValue(b, TEST_ID_FIELD) || '').trim();
            if (t && !seen[t]) { seen[t] = 1; candidates.push(t); }
        }
        if (candidates.length === 0) { qbConsole.log('ERROR: no "' + TEST_ID_FIELD + '" value found in any block'); QB.error(); return; }

        let batchId = null, usedTestId = null;
        for (const t of candidates) {
            let blist = [];
            try {
                const batches = await call((resolve, reject) => svc.getJson({
                    url: '/batches/get', urlParams: { test_id: t }, success: resolve, error: reject
                }));
                blist = Array.isArray(batches) ? batches : (batches && Array.isArray(batches.data)) ? batches.data : [];
            } catch (e) { blist = []; }
            if (blist.length) {
                if (blist.length > 1) stats.warnings.push(TEST_ID_LABEL + ' ' + t + ' is on ' + blist.length + ' batches; using the first');
                batchId = blist[0] && blist[0].id;
                usedTestId = t;
                break;
            }
        }
        if (batchId == null) { qbConsole.log('ERROR: no batch found for any ' + TEST_ID_LABEL + ' in the file (tried ' + candidates.length + ' value(s), e.g. controls have no ' + TEST_ID_LABEL + ')'); QB.error(); return; }
        qbConsole.log('Batch ' + batchId + ' (matched via ' + TEST_ID_LABEL + ' ' + usedTestId + ')');
        qbProgressBar.setPercentage(25);

        const docs = await call((resolve) => svc.getJson({
            url: '/batches/worksheets/dynamic',
            urlParams: { entity_ids: batchId, process_references: true, construct_worksheet_data_array: true, convert_datetime_values_to_localtime: true },
            success: resolve
        }));
        const docList = Array.isArray(docs) ? docs
            : (docs && Array.isArray(docs.data)) ? docs.data
            : (docs && typeof docs === 'object') ? Object.values(docs).filter((v) => v && typeof v === 'object') : [];
        const findDoc = (type) => docList.find((x) => x && x.worksheet_name === TAB && x.type === type);
        const docData = (type) => { const it = findDoc(type); return it && Array.isArray(it.data) ? it.data : null; };
        const docMap = (type) => { const it = findDoc(type); return (it && it.data && typeof it.data === 'object' && !Array.isArray(it.data)) ? it.data : {}; };
        const rawGrid = docData('WORKSHEET_DATA');
        const procGrid = docData('WORKSHEET_DATA_PROCESSED');
        if (!rawGrid || !procGrid) throw new Error('could not read "' + TAB + '" worksheet for batch ' + batchId);
        const formulasMap = docMap('WORKSHEET_FORMULAS');
        const imageMap = docMap('WORKSHEET_IMAGE_DATA');
        const refMap = docMap('WORKSHEET_DOLLAR_REFERENCES');

        const headerMap = {};
        const headerRow = procGrid[HEADER_ROW - 1] || [];
        for (let c = 0; c < headerRow.length; c++) {
            const key = norm(headerRow[c]);
            if (key && !(key in headerMap)) headerMap[key] = c;
        }

        const rowByTest = {};
        for (let r = HEADER_ROW; r < procGrid.length; r++) {
            const key = cell(procGrid[r], MATCH_COL);
            if (key !== '' && !(key in rowByTest)) rowByTest[key] = r + 1;
        }
        const matchColLetter = colLetter(MATCH_COL);
        const refRowRe = new RegExp('^' + matchColLetter + '(\\d+)$');
        for (const k of Object.keys(refMap)) {
            const m = k.match(refRowRe);
            if (!m) continue;
            const v = String(refMap[k] == null ? '' : refMap[k]).trim();
            if (v !== '' && !(v in rowByTest)) rowByTest[v] = parseInt(m[1], 10);
        }
        qbConsole.log(TEST_ID_LABEL + 's on worksheet: ' + Object.keys(rowByTest).length + (usedTestId ? ' (e.g. ' + usedTestId + ' -> row ' + rowByTest[usedTestId] + ')' : ''));

        const dataMap = gridToA1(rawGrid);
        const procMap = gridToA1(procGrid);
        qbProgressBar.setPercentage(40);

        for (let bi = 0; bi < allBlocks.length; bi++) {
            const label = 'Block ' + (bi + 1);
            try {
                const ex = extractBlock(allBlocks[bi]);
                ex.warnings.forEach((w) => stats.warnings.push(label + ': ' + w));
                if (!ex.testId) { qbConsole.log(label + ': SKIP no ' + TEST_ID_LABEL); stats.skipped++; continue; }
                const rowNum = rowByTest[ex.testId];
                if (!rowNum) { qbConsole.log(label + ': SKIP ' + TEST_ID_LABEL + ' ' + ex.testId + ' not on worksheet'); stats.warnings.push(label + ': ' + TEST_ID_LABEL + ' ' + ex.testId + ' not on worksheet'); stats.skipped++; continue; }

                const setCell = (colIdx, value) => {
                    const a1 = colLetter(colIdx) + rowNum;
                    dataMap[a1] = value;
                    procMap[a1] = String(value);
                };
                let n = 0;
                for (const key of Object.keys(ex.named)) {
                    if (key in headerMap) { setCell(headerMap[key], ex.named[key]); n++; }
                }
                for (let u = 0; u < ex.unknowns.length; u++) {
                    const key = 'UNKNOWNPEAK' + (u + 1);
                    if (key in headerMap && ex.unknowns[u] !== '') { setCell(headerMap[key], ex.unknowns[u]); n++; }
                }
                qbConsole.log(label + ': ' + TEST_ID_LABEL + ' ' + ex.testId + ' -> row ' + rowNum + ' (' + n + ' cells)');
                stats.written++;
            } catch (e) {
                qbConsole.log(label + ': ERROR ' + (e && e.message));
                stats.warnings.push(label + ': ' + (e && e.message));
                stats.skipped++;
            }
            qbProgressBar.setPercentage(Math.min(40 + ((bi + 1) / allBlocks.length) * 45, 85));
        }

        if (stats.written === 0) {
            qbConsole.log('No rows matched — nothing written.');
        } else {
            await call((resolve, reject) => svc.update({
                data: {
                    id: String(batchId),
                    qb_dynamic_spreadsheet_data: {
                        [TAB]: { WORKSHEET_DATA: dataMap, WORKSHEET_FORMULAS: formulasMap, WORKSHEET_IMAGE_DATA: imageMap, WORKSHEET_DOLLAR_REFERENCES: refMap, WORKSHEET_DATA_PROCESSED: procMap }
                    }
                },
                urlParams: { run_worksheet_calculations: true },
                success: resolve, error: reject
            }));
        }

        qbProgressBar.setPercentage(100);
        qbConsole.log('=== Done ===');
        qbConsole.log('Blocks: ' + stats.blocks + ' | Rows written: ' + stats.written + ' | Skipped: ' + stats.skipped);
        if (stats.warnings.length) {
            qbConsole.log('Warnings (' + stats.warnings.length + '):');
            stats.warnings.forEach((w) => qbConsole.log('  ' + w));
        }
        QB.success();
    } catch (e) {
        qbConsole.log('FATAL: ' + (e && e.message ? e.message : e));
        QB.error();
    }
});
