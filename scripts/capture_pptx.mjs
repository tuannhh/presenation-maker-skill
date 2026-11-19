// Thu dữ liệu để dựng PPTX sửa được: mỗi trang gồm
//   - bg.jpg  : nền + mọi thứ đứng yên (chữ đã ẩn)
//   - gNN.png : từng khối có hiệu ứng vào (nền trong suốt, chữ đã ẩn) + vị trí, kiểu hiệu ứng, độ trễ
//   - texts   : từng khối chữ sửa được (data-e): vị trí, đoạn, run (font, cỡ, đậm, màu, giãn chữ…)
// node capture_pptx.mjs <deck.html> <outDir>   → <outDir>/pptx.json + ảnh
import { writeFileSync, mkdirSync } from 'node:fs';
import { openDeck, sleep } from './cdp.mjs';

const [file, outDir] = process.argv.slice(2);
if (!file || !outDir) { console.log('node capture_pptx.mjs <deck.html> <outDir>'); process.exit(1); }
mkdirSync(outDir, { recursive: true });
const d = await openDeck(file);
const n = await d.ev('deck.count');

// CSS phụ: .xt = ẩn chữ (giữ icon SVG, nền, viền); .xclip = bỏ nền gradient của chữ tô gradient;
// .xsolo = chụp riêng 1 khối trên nền trong suốt
await d.ev(`(()=>{const s=document.createElement('style');s.id='xpptx';s.textContent=\`
.xt,.xt *{-webkit-text-fill-color:transparent!important;text-shadow:none!important;-webkit-text-stroke:0!important;text-decoration-color:transparent!important;caret-color:transparent!important}
.xt.xclip,.xt .xclip{background-image:none!important}
.xt ::marker{color:transparent!important}
body.xsolo,body.xsolo #stage,html.xsolo{background:transparent!important}
body.xsolo #bg,body.xsolo #logo,body.xsolo #foot,body.xsolo #prog,body.xsolo .chrome{visibility:hidden!important}
body.xsolo .slide.on{visibility:hidden!important;background:transparent!important}
body.xsolo .slide.on .xsolo-on{visibility:visible!important}
.xgh{visibility:hidden!important}
.caret{display:none!important}\`;document.head.appendChild(s);})()`);

// Hàm chạy trong trang: đo khối hiệu ứng + khối chữ của trang k (0-based)
function collect(k) {
  const stage = document.getElementById('stage'), sr = stage.getBoundingClientRect(), K = sr.width / 1920;
  const S = r => ({ x: (r.left - sr.left) / K, y: (r.top - sr.top) / K, w: r.width / K, h: r.height / K });
  const s = document.querySelectorAll('.slide')[k];
  const vis = el => { const cs = getComputedStyle(el); const r = el.getBoundingClientRect(); return cs.display !== 'none' && cs.visibility !== 'hidden' && +cs.opacity > 0.02 && r.width > 1 && r.height > 1 && !el.closest('.xdel'); };
  // khối có hiệu ứng vào: [data-a] không nằm trong [data-a] khác
  const anims = [...s.querySelectorAll('[data-a]')].filter(el => !el.parentElement.closest('[data-a]') && vis(el) && !el.closest('svg') || (el.matches('svg[data-a]') && !el.parentElement.closest('[data-a]') && vis(el)));
  const groups = anims.map((el, i) => {
    el.dataset.xg = i;
    let delay = 0, dur = 800;
    try { const t = el._a && el._a.effect.getTiming(); if (t) { delay = +t.delay || 0; dur = +t.duration || 800; } } catch (e) {}
    return { i, kind: el.dataset.a, delay, dur, box: S(el.getBoundingClientRect()) };
  });
  // khối chữ sửa được
  const texts = [];
  const colorOf = (cs) => {
    const fill = cs.webkitTextFillColor;
    if (cs.backgroundClip === 'text' || cs.webkitBackgroundClip === 'text' || /rgba\(0, 0, 0, 0\)|transparent/.test(fill) && cs.backgroundImage !== 'none') {
      const m = cs.backgroundImage.match(/rgba?\([^)]+\)|#[0-9a-f]{3,8}/i); if (m) return m[0];
    }
    return fill && !/rgba\(0, 0, 0, 0\)/.test(fill) ? fill : cs.color;
  };
  s.querySelectorAll('[data-e]').forEach(el => {
    if (!vis(el) || el.closest('svg')) return;
    // các run chữ, tách đoạn theo phần tử khối và <br>
    const paras = [[]], firsts = [];
    const gradOf = p => { for (let e = p; e && e !== el.parentElement; e = e.parentElement) { const c = getComputedStyle(e); if (/gradient/.test(c.backgroundImage) && (c.backgroundClip === 'text' || c.webkitBackgroundClip === 'text' || /rgba\(0, 0, 0, 0\)/.test(c.webkitTextFillColor))) return c.backgroundImage; } return null; };
    const walk = node => {
      for (const c of node.childNodes) {
        if (c.nodeType === 3) {
          const t = c.data.replace(/[\s ]+/g, m => m.includes(' ') ? ' ' : ' '); if (!t) continue;
          const p = c.parentElement, cs = getComputedStyle(p); if (cs.display === 'none' || cs.visibility === 'hidden') continue;
          if (!paras[paras.length - 1].some(r => r.t && r.t.trim()) && c.data.trim()) firsts[paras.length - 1] = c;
          paras[paras.length - 1].push({ t, gr: gradOf(p), f: cs.fontFamily.split(',')[0].replace(/["']/g, '').trim(), fs: parseFloat(cs.fontSize) / K * K, fw: +cs.fontWeight || 400,
            it: cs.fontStyle === 'italic', u: /underline/.test(cs.textDecorationLine), c: colorOf(cs), ls: parseFloat(cs.letterSpacing) || 0,
            tt: cs.textTransform, sup: cs.verticalAlign === 'super' });
        } else if (c.nodeType === 1) {
          if (c.tagName === 'BR') { paras[paras.length - 1].push({ br: 1 }); continue; }
          if (c.matches('svg,img,.i,.caret,script,style')) continue;
          const cs = getComputedStyle(c); if (cs.display === 'none') continue;
          const blk = /^(block|flex|grid|list-item|table)/.test(cs.display);
          if (blk && paras[paras.length - 1].length) paras.push([]);
          walk(c);
          if (blk) paras.push([]);
        }
      }
    };
    walk(el);
    const ps0 = paras.map((p, i) => {
      while (p.length && !p[0].br && !p[0].t.trim()) p.shift();
      if (p.length && p[0].t) p[0].t = p[0].t.replace(/^ +/, '');
      const L = p.length - 1; if (L >= 0 && p[L].t) p[L].t = p[L].t.replace(/ +$/, '');
      return { r: p.filter(r => r.br || r.t), n: firsts[i] };
    }).filter(p => p.r.length);
    if (!ps0.length) return;
    // khung chữ thật = hợp các dòng chữ (bỏ icon, padding)
    const rg = document.createRange(), rects = [];
    const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let t;
    while ((t = tw.nextNode())) { if (!t.data.trim()) continue; rg.selectNodeContents(t); for (const r of rg.getClientRects()) if (r.width > 0) rects.push(r); }
    if (!rects.length) return;
    const L = Math.min(...rects.map(r => r.left)), R = Math.max(...rects.map(r => r.right)), T = Math.min(...rects.map(r => r.top)), B = Math.max(...rects.map(r => r.bottom));
    const tops = [...new Set(rects.map(r => Math.round(r.top / 4)))].length;
    const cs = getComputedStyle(el);
    const fs = parseFloat(cs.fontSize), lh = cs.lineHeight === 'normal' ? fs * 1.2 : parseFloat(cs.lineHeight);
    const first = rects[0];
    // thụt đầu dòng từng đoạn (vd chữ đứng sau icon): lề trái dòng đầu của đoạn so với khung chữ
    const ps = ps0.map(p => { let ind = 0; if (p.n) { rg.selectNodeContents(p.n); const r0 = [...rg.getClientRects()].find(r => r.width > 0); if (r0) ind = Math.max(0, (r0.left - L) / K); } return { runs: p.r, ind }; });
    const g = el.closest('[data-xg]');
    texts.push({ box: S({ left: L, top: T, width: R - L, height: B - T }), lineTop: (first.top + first.height / 2 - (lh * K) / 2 - sr.top) / K,
      lines: tops, lh: lh, align: cs.textAlign, nowrap: cs.whiteSpace === 'nowrap' || tops === 1, paras: ps, g: g ? +g.dataset.xg : -1 });
    [el, ...el.querySelectorAll('*')].forEach(c => { const cc = getComputedStyle(c);
      if (cc.backgroundImage !== 'none' && (cc.backgroundClip === 'text' || cc.webkitBackgroundClip === 'text' || /rgba\(0, 0, 0, 0\)/.test(cc.webkitTextFillColor))) c.classList.add('xclip'); });
    el.classList.add('xt');
  });
  // khung video
  const vf = s.querySelector('.vframe.has'); const video = vf ? S(vf.getBoundingClientRect()) : null;
  return { groups, texts, video, tr: window.deck.tr(k + 1), title: s.dataset.title || '' };
}

const out = { slides: [], motion: await d.ev('deck.motion') };
for (let k = 1; k <= n; k++) {
  await d.ev(`deck.go(${k})`); await sleep(k === 1 ? 4500 : 4200);
  await d.ev(`document.getAnimations().forEach(a=>{try{if(a.effect&&a.effect.getComputedTiming().iterations!==Infinity)a.finish()}catch(e){}})`);
  await sleep(300);
  const info = await d.ev(`(${collect})(${k - 1})`);
  const pre = `s${String(k).padStart(2, '0')}`;
  // nền: ẩn các khối hiệu ứng
  await d.ev(`document.querySelectorAll('.slide.on [data-xg]').forEach(e=>e.classList.add('xgh'))`); await sleep(150);
  let shot = await d.send('Page.captureScreenshot', { format: 'jpeg', quality: 92 });
  writeFileSync(`${outDir}/${pre}-bg.jpg`, Buffer.from(shot.result.data, 'base64'));
  await d.ev(`document.querySelectorAll('.slide.on [data-xg]').forEach(e=>e.classList.remove('xgh'))`);
  // từng khối hiệu ứng trên nền trong suốt
  await d.send('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } });
  await d.ev(`document.documentElement.classList.add('xsolo');document.body.classList.add('xsolo')`);
  for (const g of info.groups) {
    const M = 48, x = Math.max(0, g.box.x - M), y = Math.max(0, g.box.y - M);
    const w = Math.min(1920, g.box.x + g.box.w + M) - x, h = Math.min(1080, g.box.y + g.box.h + M) - y;
    if (w < 2 || h < 2) { g.skip = true; continue; }
    g.clip = { x, y, w, h };
    await d.ev(`document.querySelector('.slide.on [data-xg="${g.i}"]').classList.add('xsolo-on')`); await sleep(60);
    const sr = await d.ev(`(()=>{const r=document.getElementById('stage').getBoundingClientRect();return {x:r.left,y:r.top,k:r.width/1920}})()`);
    shot = await d.send('Page.captureScreenshot', { format: 'png', clip: { x: sr.x + x * sr.k, y: sr.y + y * sr.k, width: w * sr.k, height: h * sr.k, scale: 1 / sr.k } });
    writeFileSync(`${outDir}/${pre}-g${String(g.i).padStart(2, '0')}.png`, Buffer.from(shot.result.data, 'base64'));
    await d.ev(`document.querySelector('.slide.on [data-xg="${g.i}"]').classList.remove('xsolo-on')`);
  }
  await d.ev(`document.documentElement.classList.remove('xsolo');document.body.classList.remove('xsolo')`);
  await d.send('Emulation.setDefaultBackgroundColorOverride', {});
  await d.ev(`document.querySelectorAll('.xt').forEach(e=>e.classList.remove('xt'));document.querySelectorAll('[data-xg]').forEach(e=>delete e.dataset.xg)`);
  out.slides.push({ k, pre, ...info });
  process.stdout.write(k + ' ');
}
writeFileSync(`${outDir}/pptx.json`, JSON.stringify(out));
console.log(`\nxong ${n} trang → ${outDir}/pptx.json`);
d.close();
