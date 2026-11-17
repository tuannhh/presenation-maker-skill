// Bỏ trang khỏi file deck (kể cả file người dùng đã sửa + Ctrl+S): giữ nguyên mọi chỉnh sửa còn lại.
// node remove_slides.mjs <vào.html> <ra.html> 32,36      (số trang 1-based như hiển thị)
// Chỉnh sửa (texts/styles) đánh số theo thứ tự khối chữ trong cả bài → phải đánh số lại sau khi bỏ trang.
import { readFileSync, writeFileSync } from 'node:fs';
import { openDeck } from './cdp.mjs';
const [src, dst, list] = process.argv.slice(2);
const REMOVE = new Set(list.split(',').map(n => +n - 1));
const d = await openDeck(src);
const smap = await d.ev(`(()=>{const S=[...document.querySelectorAll('.slide')];const m=[];document.querySelectorAll('[data-e]').forEach(el=>m[+el.dataset.e]=S.indexOf(el.closest('.slide')));return m})()`);
d.close();
let h = readFileSync(src, 'utf8');
const starts = [...h.matchAll(/<section class="slide/g)].map(m => m.index);
const total = starts.length;
for (const i of [...REMOVE].sort((a, b) => b - a)) {
  if (i < 0 || i >= total) throw new Error('Không có trang ' + (i + 1));
  let a = starts[i]; const b = h.indexOf('</section>', a) + 10;
  const c = h.lastIndexOf('<!--', a); if (c !== -1 && h.slice(c, a).trim().endsWith('-->') && !h.slice(c, a).includes('</section>')) a = c;
  console.log('bỏ trang', i + 1 + ':', (h.slice(starts[i], starts[i] + 400).match(/data-title="([^"]*)"/) || [])[1]);
  h = h.slice(0, a) + h.slice(b);
}
const before = s => [...REMOVE].filter(r => r < s).length;
// chỉnh sửa
const TAG = '<script id="deck-edits" type="application/json">';
const i0 = h.indexOf(TAG) + TAG.length, j0 = h.indexOf('</script>', i0);
const ed = JSON.parse(h.slice(i0, j0).replace(/<\\\//g, '</') || '{}');
const removedIds = smap.map((s, k) => REMOVE.has(s) ? k : -1).filter(k => k >= 0);
const newId = k => REMOVE.has(smap[k]) ? null : k - removedIds.filter(r => r < k).length;
for (const key of ['texts', 'styles']) {
  const o = {}; for (const [k, v] of Object.entries(ed[key] || {})) { const n = newId(+k); if (n === null) console.log('  bỏ chỉnh sửa trên trang đã xoá:', key, k); else o[n] = v; } ed[key] = o;
}
ed.videos = Object.fromEntries(Object.entries(ed.videos || {}).filter(([k]) => !REMOVE.has(+k)).map(([k, v]) => [String(+k - before(+k)), v]));
ed.images = Object.fromEntries(Object.entries(ed.images || {}).filter(([, v]) => !REMOVE.has(v.s)).map(([k, v]) => [k, { ...v, s: v.s - before(v.s) }]));
h = h.slice(0, i0) + JSON.stringify(ed).replace(/<\//g, '<\\/') + h.slice(j0);
// ghi chú thuyết trình
const NK = 'const NOTES = '; const k0 = h.indexOf(NK) + NK.length;
let depth = 0, k1 = k0, inStr = false;
for (; k1 < h.length; k1++) { const ch = h[k1]; if (inStr) { if (ch === '\\') k1++; else if (ch === '"') inStr = false; continue; } if (ch === '"') inStr = true; else if (ch === '[') depth++; else if (ch === ']') { depth--; if (!depth) { k1++; break; } } }
const notes = JSON.parse(h.slice(k0, k1)).filter((_, i) => !REMOVE.has(i));
h = h.slice(0, k0) + JSON.stringify(notes) + h.slice(k1);
// tổng số trang + các phần (from/to) + id video nhúng dv-N (N = số trang)
h = h.replace(/const TOTAL_NUMBERED = (\d+);/, (_, n) => `const TOTAL_NUMBERED = ${+n - [...REMOVE].filter(r => r < +n).length};`);
h = h.replace(/const PARTS = (\[.*?\]);/, (_, j) => 'const PARTS = ' + JSON.stringify(JSON.parse(j).map(p => p && ({ ...p, from: p.from - before(p.from - 1), to: p.to - before(p.to) }))) + ';');
h = h.replace(/id="dv-(\d+)"/g, (_, n) => `id="dv-${+n - before(+n - 1)}"`);
writeFileSync(dst, h);
console.log(`xong: ${total} → ${total - REMOVE.size} trang → ${dst}`);
