// Chụp từng slide (JPEG) + vị trí khung video → <outDir>/sNN.jpg, links.json
// node capture_slides.mjs <deck.html> <outDir> [scale=1.5] [--pages=7,9]
import { writeFileSync, mkdirSync } from 'node:fs';
import { openDeck, showSlide } from './cdp.mjs';
const [file, outDir, scaleArg] = process.argv.slice(2).filter(a => !a.startsWith('--'));
const only = (process.argv.find(a => a.startsWith('--pages=')) || '').slice(8).split(',').filter(Boolean).map(Number);
mkdirSync(outDir, { recursive: true });
const d = await openDeck(file, { scale: +(scaleArg || 1.5) });
const n = await d.ev('document.querySelectorAll(".slide").length');
const links = [];
for (let k = 1; k <= n; k++) {
  if (only.length && !only.includes(k)) continue;
  // trang có bộ đếm chạy theo thời gian: chờ ~1 phút để số đủ dài như lúc chiếu thật
  const live = await d.ev(`!!document.querySelectorAll('.slide')[${k - 1}].querySelector('[data-live]')`);
  await showSlide(d, k, live ? 66000 : (k === 1 ? 4500 : 4200));
  const info = await d.ev(`(()=>{const s=document.querySelectorAll('.slide')[${k-1}];const f=s.querySelector('.vframe.has');if(!f)return null;const r=f.getBoundingClientRect();return{x:r.left,y:r.top,w:r.width,h:r.height}})()`);
  if (info) links.push({ page: k, ...info });
  const shot = await d.send('Page.captureScreenshot', { format: 'jpeg', quality: 90 });
  writeFileSync(`${outDir}/s${String(k).padStart(2, '0')}.jpg`, Buffer.from(shot.result.data, 'base64'));
  process.stdout.write(k + ' ');
}
if (!only.length) writeFileSync(`${outDir}/links.json`, JSON.stringify(links, null, 1));
console.log(`\nxong ${n} trang; trang có video: ${links.map(l => l.page).join(', ') || '—'}`);
d.close();
