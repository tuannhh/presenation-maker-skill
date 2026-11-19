(() => {
'use strict';
/* ---------- Bản gốc để lưu lại file khi chỉnh sửa ---------- */
/* Video nhúng (vài chục MB) giữ riêng 1 bản trong bộ nhớ, không nhân đôi vào PRISTINE */
const DV = {}; document.querySelectorAll('script[id^="dv-"]').forEach(s => { DV[s.id] = s.textContent.trim(); s.textContent = ''; });
const PRISTINE = '<!doctype html>\n' + document.documentElement.outerHTML;
const EDIT_TAG = '<script id="deck-' + 'edits" type="application/json">';
let EDITS = { texts:{}, videos:{}, styles:{}, images:{}, blocks:{} };
try { const j = JSON.parse(document.getElementById('deck-edits').textContent || '{}'); EDITS = { texts: j.texts || {}, videos: j.videos || {}, styles: j.styles || {}, images: j.images || {}, blocks: j.blocks || {} }; } catch(e) {}
const NOTES = {{NOTES_JSON}};
const stage = document.getElementById('stage');
const slides = [...document.querySelectorAll('.slide')];
const TOTAL_NUMBERED = {{TOTAL_NUMBERED}};
const PARTS = {{PARTS_JSON}};
/* Nhịp chuyển động theo theme (build chèn từ themes.json + deck.json "motion") */
const MOTION = Object.assign({speed:1, blur:true, enter:'slide', big:'circle'}, {{MOTION_JSON}});
const SP = +MOTION.speed || 1;
/* data-stagger: cho các con xuất hiện lần lượt.  <div data-stagger="120" data-sa="up" data-d0="400">…</div> */
slides.forEach(s => s.querySelectorAll('[data-stagger]').forEach(box => {
  const step = +box.dataset.stagger || 110, d0 = +(box.dataset.d0 || 300), kind = box.dataset.sa || 'up';
  [...box.children].forEach((c, i) => { if (!c.dataset.a) c.dataset.a = kind; if (c.dataset.d === undefined) c.dataset.d = d0 + i * step; });
}));

/* ---------- Đánh số các khối chữ sửa được + áp dụng nội dung đã sửa ---------- */
const EDITABLE = [];
slides.forEach(s => {
  const walk = el => { for (const c of el.children) {
    if (c.matches('svg,script,style,input,video,.vframe,.reel,[data-live],.im')) continue;
    if (c.matches('[data-count],[data-slot]')) { EDITABLE.push(c); continue; }
    const hasText = [...c.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (hasText && !c.querySelector('[data-count],[data-slot],[data-live]')) EDITABLE.push(c); else walk(c);
  } };
  walk(s);
});
EDITABLE.forEach((el, i) => el.dataset.e = i);
/* Đánh số mọi khối (chữ, hình, thẻ…) theo "trang:thứ tự" để di chuyển / xoá ở chế độ Bố cục (phím M).
   Đánh số trên DOM gốc, trước mọi thay đổi → giống nhau ở mọi lần mở file. Không đi vào trong khối chữ và SVG. */
slides.forEach((s, si) => { let k = 0;
  const walk = el => { for (const c of el.children) {
    if (c.matches('script,style,input,video,source,br,.uimg')) continue;
    c.dataset.b = si + ':' + (k++);
    if (!c.matches('svg,[data-e]')) walk(c);
  } };
  walk(s);
});
function applyText(el, html){
  if (el.hasAttribute('data-count')) { const v = parseInt(html.replace(/<[^>]*>/g,'').replace(/\D/g,'')); if (!isNaN(v)) el.dataset.count = v; return; }
  if (el.hasAttribute('data-slot')) { const v = parseInt(html.replace(/<[^>]*>/g,'').replace(/\D/g,'').slice(-1)); if (!isNaN(v)) el.dataset.slot = v; return; }
  el.innerHTML = html;
  if (el.hasAttribute('data-type')) el.dataset.full = el.textContent;
  if (el.matches('h2.t')) { const s = el.closest('.slide'); if (s) s.dataset.title = el.textContent.trim(); }
}
const ORIG_STYLE = EDITABLE.map(el => el.getAttribute('style'));
Object.entries(EDITS.texts).forEach(([id, html]) => { const el = EDITABLE[+id]; if (el) applyText(el, html); });
Object.entries(EDITS.styles).forEach(([id, st]) => { const el = EDITABLE[+id]; if (el) { if (st) el.setAttribute('style', st); else el.removeAttribute('style'); } });

/* ---------- Easing kiểu spring (Remotion-like) ---------- */
const canLinear = CSS.supports && CSS.supports('animation-timing-function', 'linear(0, 1)');
const SPRING = canLinear ? 'linear(0, 0.006, 0.025 2.8%, 0.101 6.1%, 0.539 18.9%, 0.721 25.3%, 0.849 31.5%, 0.937 38.1%, 0.968 41.8%, 0.991 45.7%, 1.006 50.1%, 1.015 55%, 1.017 63.9%, 1.001)' : 'cubic-bezier(.2,.9,.25,1.05)';
const BOUNCE = canLinear ? 'linear(0, 0.009, 0.035 2.1%, 0.141, 0.281 6.7%, 0.723 12.9%, 0.938 16.7%, 1.017, 1.077, 1.121, 1.149 24.3%, 1.159, 1.163, 1.161, 1.154 29.9%, 1.129 32.8%, 1.051 39.6%, 1.017 43.1%, 0.991, 0.977 51%, 0.974 53.8%, 0.975 57.1%, 0.997 69.8%, 1.003 76.9%, 1.004 83.8%, 1)' : 'cubic-bezier(.34,1.56,.64,1)';
const SMOOTH = 'cubic-bezier(.65,0,.35,1)';
const KF = {
  up:   [{opacity:0, transform:'translateY(46px)', filter:'blur(10px)'}, {opacity:1, transform:'none', filter:'blur(0px)'}],
  down: [{opacity:0, transform:'translateY(-40px)'}, {opacity:1, transform:'none'}],
  left: [{opacity:0, transform:'translateX(-70px)', filter:'blur(8px)'}, {opacity:1, transform:'none', filter:'blur(0px)'}],
  right:[{opacity:0, transform:'translateX(70px)', filter:'blur(8px)'}, {opacity:1, transform:'none', filter:'blur(0px)'}],
  fade: [{opacity:0}, {opacity:1}],
  pop:  [{opacity:0, transform:'scale(.4)'}, {opacity:1, transform:'scale(1)'}],
  zoom: [{opacity:0, transform:'scale(1.18)', filter:'blur(22px)'}, {opacity:1, transform:'scale(1)', filter:'blur(0px)'}],
  flip: [{opacity:0, transform:'perspective(600px) rotateX(-95deg)'}, {opacity:1, transform:'perspective(600px) rotateX(0deg)'}],
  bar:  [{opacity:0, transform:'scaleY(0)'}, {opacity:1, transform:'scaleY(1)'}],
  grow: [{opacity:1, transform:'scaleX(0)'}, {opacity:1, transform:'scaleX(1)'}],
  mask: [{opacity:1, clipPath:'inset(0 100% 0 0 round 26px)'}, {opacity:1, clipPath:'inset(0 0% 0 0 round 26px)'}],
  rise: [{opacity:0, transform:'translateY(90px) scale(.92)'}, {opacity:1, transform:'none'}],
  slam: [{opacity:0, transform:'scale(1.7) rotate(-4deg)'}, {opacity:1, transform:'scale(1) rotate(0)'}],
  tilt: [{opacity:0, transform:'translateY(40px) rotate(-6deg)'}, {opacity:1, transform:'none'}],
  blur: [{opacity:0, filter:'blur(24px)'}, {opacity:1, filter:'blur(0px)'}],
  wipe: [{opacity:1, clipPath:'inset(0 0 100% 0)'}, {opacity:1, clipPath:'inset(0 0 0% 0)'}],
  spin: [{opacity:0, transform:'rotate(-180deg) scale(.3)'}, {opacity:1, transform:'none'}],
};
/* Theme phẳng (blur:false): bỏ hiệu ứng mờ cho mọi kiểu trừ 'blur' */
if (!MOTION.blur) Object.entries(KF).forEach(([k, fr]) => { if (k !== 'blur') fr.forEach(f => { if (f.filter) delete f.filter; }); });
const EZ = {pop:BOUNCE, bar:SPRING, grow:SMOOTH, mask:SMOOTH, fade:'ease-out', flip:BOUNCE, slam:BOUNCE, spin:BOUNCE, wipe:SMOOTH, blur:'ease-out', ring:SMOOTH};
const DUR = {up:1100, down:900, left:1100, right:1100, fade:900, pop:1000, zoom:1500, flip:1000, bar:1300, grow:1100, mask:1000, rise:1100, slam:800, tilt:1000, blur:1200, wipe:1000, spin:1100, ring:1800};

/* ---------- Fit 1920x1080 ---------- */
function fit(){ const s = Math.min(innerWidth/1920, innerHeight/1080); stage.style.transform = `translate(-50%,-50%) scale(${s})`; }
addEventListener('resize', fit); fit();

/* ---------- Footer ---------- */
const foot = document.getElementById('foot');
foot.querySelector('.parts').innerHTML = PARTS.slice(1).map(p=>`<div class="pt" style="--pc:${p.c}"><b><i></i></b><span>${p.n}</span></div>`).join('');
const pg = foot.querySelector('.pg');

/* ---------- Animation per slide ---------- */
function runIn(slide){
  layoutStairs(slide);
  const els = [...slide.querySelectorAll('[data-a]')];
  let auto = 0;
  els.forEach(el => {
    const kind = el.dataset.a;
    const d = (el.dataset.d !== undefined ? +el.dataset.d : 120 + (auto++) * 90) * SP;
    const t = +(el.dataset.t || DUR[kind] || 1000) * SP;
    if (kind === 'ring') {   /* vòng tiến độ: <circle class="val" pathLength="100" data-a="ring"> trong .ring style="--v:72" */
      const v = parseFloat(getComputedStyle(el.closest('.ring') || el).getPropertyValue('--v')) || 0;
      el._a = el.animate([{opacity:1, strokeDasharray:`0 100`}, {opacity:1, strokeDasharray:`${v} 100`}], {duration:t, delay:d, easing:SMOOTH, fill:'both'});
      return;
    }
    if (kind === 'draw') {
      if (el.getAttribute('stroke-dasharray')) { el._a = el.animate([{opacity:0, clipPath:'inset(0 100% 0 0)'},{opacity:1, clipPath:'inset(0 0 0 0)'}], {duration:t, delay:d, easing:SMOOTH, fill:'both'}); return; }
      const len = el.getTotalLength ? el.getTotalLength() : 1000;
      el.style.strokeDasharray = len;
      el._a = el.animate([{opacity:1, strokeDashoffset: len}, {opacity:1, strokeDashoffset: 0}], {duration:t, delay:d, easing:SMOOTH, fill:'both'});
      return;
    }
    el._a = el.animate(KF[kind] || KF.up, {duration:t, delay:d, easing:EZ[kind] || SPRING, fill:'both'});
  });
  // counters
  slide.querySelectorAll('[data-count]').forEach(el => {
    const host = el.closest('[data-a]'); const d = host ? (+host.dataset.d || 300) : 300;
    countUp(el, +el.dataset.count, (d + 150) * SP, 1800 * SP, +(el.dataset.dec || 0));
  });
  // typewriter
  slide.querySelectorAll('[data-type]').forEach((el, i) => {
    if (!el.dataset.full) el.dataset.full = el.textContent;
    const full = [...el.dataset.full]; el.textContent = '';
    const caret = document.createElement('span'); caret.className = 'caret'; el.after(caret);
    let k = 0; const start = 900 + i*120;
    el._tt = setTimeout(function tick(){ el.textContent = full.slice(0, ++k).join(''); if (k < full.length) el._tt = setTimeout(tick, 70 + Math.random()*60); else setTimeout(()=>caret.remove(), 1600); }, start);
  });
  // slot reels
  slide.querySelectorAll('[data-slot]').forEach(el => {
    const target = +el.dataset.slot; const seq = [];
    for (let r=0; r<2; r++) for (let n=0; n<10; n++) seq.push(n);
    seq.push(...Array.from({length: target+1}, (_, n)=>n));
    el.innerHTML = `<div class="reel">${seq.map(n=>`<span>${n}</span>`).join('')}</div>`;
    const reel = el.firstChild; const H = el.clientHeight || 300;
    el._a = reel.animate([{transform:'translateY(0)'}, {transform:`translateY(${-(seq.length-1)*H}px)`}], {duration:1700, delay:+el.dataset.d||400, easing: canLinear ? SPRING : 'cubic-bezier(.15,.85,.25,1)', fill:'both'});
  });
  // traffic lights
  slide.querySelectorAll('[data-light]').forEach(el => { el._t = setTimeout(()=>el.classList.add('on'), +el.dataset.light); });
  // bộ đếm chạy theo thời gian thực: data-live="<số lượng mỗi ngày>" (mặc định 14e9 = 14 tỷ/ngày)
  slide.querySelectorAll('[data-live]').forEach(el => {
    const perMs = (parseFloat(el.dataset.live) || 14e9) / 86400000; const t0 = performance.now();
    // Giữ cố định độ rộng con số (đủ cho 99.999.999 ≈ 10 phút trên trang) để chữ xám bên cạnh đứng yên
    el.style.display = 'inline-block'; el.style.fontVariantNumeric = 'tabular-nums'; el.style.minWidth = '';
    el.textContent = '88.888.888'; el.style.minWidth = el.offsetWidth + 'px';
    const f = () => { el.textContent = Math.round((performance.now()-t0)*perMs).toLocaleString('vi-VN'); el._raf = requestAnimationFrame(f); };
    f();
  });
}
function layoutStairs(slide){
  const box = slide.querySelector('.stairs'); if (!box) return;
  const svg = box.querySelector('.stairsvg'), path = box.querySelector('.stairline'), head = box.querySelector('.stairhead');
  const W = box.clientWidth, H = box.clientHeight; svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  const pts = [...box.querySelectorAll(".st")].map(c => [c.offsetLeft + c.offsetWidth * 0.5, c.offsetTop - 38]);
  if (!pts.length) return;
  const first = [pts[0][0] - pts[0][0] * 0.7, pts[0][1] + 10];
  const all = [first, ...pts]; const last = pts[pts.length - 1]; const end = [W - 20, Math.max(18, last[1] - 70)];
  all.push(end);
  let d = `M${all[0][0]} ${all[0][1]}`;
  for (let i = 1; i < all.length; i++) { const [x0, y0] = all[i-1], [x1, y1] = all[i]; const mx = (x0 + x1) / 2; d += ` C${mx} ${y0}, ${mx} ${y1}, ${x1} ${y1}`; }
  path.setAttribute('d', d);
  head.setAttribute('transform', `translate(${end[0]} ${end[1]})`);
}
function countUp(el, to, delay, dur, dec = 0){
  const fmt = n => n.toLocaleString('vi-VN', {minimumFractionDigits: dec, maximumFractionDigits: dec});
  el.textContent = fmt(0);
  el._t = setTimeout(() => {
    const t0 = performance.now();
    const step = now => { const p = Math.min(1, (now - t0)/dur); const e = 1 - Math.pow(2, -10*p); el.textContent = fmt(to * (p>=1?1:e)); if (p < 1) el._raf = requestAnimationFrame(step); };
    el._raf = requestAnimationFrame(step);
  }, delay);
}
function reset(slide){
  slide.querySelectorAll('[data-a],[data-slot] .reel,[data-slot]').forEach(el => { if (el._a) { el._a.cancel(); el._a = null; } });
  slide.querySelectorAll('[data-count],[data-live]').forEach(el => { clearTimeout(el._t); cancelAnimationFrame(el._raf); });
  slide.querySelectorAll('[data-type]').forEach(el => { clearTimeout(el._tt); el.textContent = el.dataset.full || el.textContent; });
  slide.querySelectorAll('.caret').forEach(c => c.remove());
  slide.querySelectorAll('[data-light]').forEach(el => { clearTimeout(el._t); el.classList.remove('on'); });
  slide.querySelectorAll('video').forEach(v => v.pause());
  slide.querySelectorAll('.vframe').forEach(fr => fr.dataset.played = '');
}

/* ---------- Navigation ---------- */
let cur = -1;
function chrome(i){
  const s = slides[i];
  stage.dataset.p = s.dataset.p || '1';
  stage.classList.toggle('nologo', s.hasAttribute('data-nologo'));
  const n = i + 1;
  pg.innerHTML = n <= TOTAL_NUMBERED ? `<b>${String(n).padStart(2,'0')}</b> / ${TOTAL_NUMBERED}` : '';
  foot.querySelectorAll('.pt').forEach((el, k) => {
    const p = PARTS[k+1]; let w = 0;
    if (n > p.to) w = 100; else if (n >= p.from) w = (n - p.from + 1) / (p.to - p.from + 1) * 100;
    el.querySelector('i').style.width = w + '%';
    el.classList.toggle('on', n >= p.from && n <= p.to);
  });
  try { history.replaceState(null, '', '#' + n); } catch(e) {}
  updateNotes();
}
function go(n, dir){
  n = Math.max(0, Math.min(slides.length-1, n));
  if (n === cur) return;
  if (typeof vfs !== 'undefined' && vfsOpen()) closeVfs();
  imgDeselect();
  dir = dir || (n > cur ? 1 : -1);
  const a = slides[cur], b = slides[n];
  if (a) {
    a.style.zIndex = 1;
    const outKF = MOTION.enter === 'cut' ? [{opacity:1}, {opacity:0}] : MOTION.blur ? [{opacity:1, transform:'none', filter:'blur(0px)'}, {opacity:0, transform:`translateX(${-dir*70}px) scale(.97)`, filter:'blur(8px)'}] : [{opacity:1, transform:'none'}, {opacity:0, transform: MOTION.enter === 'slide' ? `translateX(${-dir*70}px)` : 'scale(.98)'}];
    const out = a.animate(outKF, {duration:(MOTION.enter === 'cut' ? 1 : 480) * SP, easing:'cubic-bezier(.4,0,.2,1)', fill:'forwards'});
    out.onfinish = () => { if (slides[cur] !== a) { a.classList.remove('on'); reset(a); } out.cancel(); a.style.zIndex = ''; };
  }
  b.classList.add('on'); b.style.zIndex = 2;
  const big = b.classList.contains('sect') || b.classList.contains('cover') || b.classList.contains('statement') || b.classList.contains('thanks');
  if (a) {
    const BIG = {
      circle: [[{clipPath:'circle(0% at 50% 55%)'}, {clipPath:'circle(75% at 50% 55%)'}], 1200, 'cubic-bezier(.75,0,.2,1)'],
      wipe:   [[{clipPath: dir > 0 ? 'inset(0 0 0 100%)' : 'inset(0 100% 0 0)'}, {clipPath:'inset(0 0 0 0)'}], 900, 'cubic-bezier(.75,0,.2,1)'],
      fade:   [[{opacity:0}, {opacity:1}], 1100, 'ease-in-out'],
      zoom:   [[{opacity:0, transform:'scale(1.12)'}, {opacity:1, transform:'none'}], 1100, SPRING],
    };
    const ENTER = {
      slide: [[{opacity:0, transform:`translateX(${dir*90}px)`}, {opacity:1, transform:'none'}], 900, SPRING],
      fade:  [[{opacity:0}, {opacity:1}], 700, 'ease-out'],
      zoom:  [[{opacity:0, transform:'scale(.94)'}, {opacity:1, transform:'none'}], 800, SPRING],
      rise:  [[{opacity:0, transform:'translateY(60px)'}, {opacity:1, transform:'none'}], 850, SPRING],
      cut:   [[{opacity:1}, {opacity:1}], 1, 'linear'],
    };
    const [kf, du, ez] = big ? (BIG[MOTION.big] || BIG.circle) : (ENTER[MOTION.enter] || ENTER.slide);
    b.animate(kf, {duration: du * SP, easing: ez});
  }
  reset(b); runIn(b);
  cur = n; chrome(n);
  if (editing) setTimeout(() => settle(b), 50);
  if (editing && blkMode) { blkSelect(null); }
}
const goNext = () => go(cur + 1, 1);
/* Bút trình chiếu: tới trang video → video CHƯA chạy; bấm next lần nữa → phát toàn màn hình có tiếng; next tiếp → sang trang */
function next(){
  if (vfsOpen()) { closeVfs(); goNext(); return; }
  const fr = slides[cur] && slides[cur].querySelector('.vframe.has');
  if (fr && !editing && fr.dataset.played !== '1') { playFull(fr); return; }
  goNext();
}
function prev(){ if (vfsOpen()) { closeVfs(); return; } go(cur - 1, -1); }

/* ---------- Keyboard / mouse / touch ---------- */
let jumpBuf = '', jumpT; const jumpEl = document.getElementById('jump');
function onKey(e){
  if (e.target && (e.target.tagName === 'INPUT' || e.target.isContentEditable)) {
    if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S')) { e.preventDefault(); saveFile(); }
    else if (e.key === 'Enter' && e.target.isContentEditable) { e.preventDefault(); document.execCommand('insertLineBreak'); }
    else if (e.key === 'Escape') e.target.blur();
    return;
  }
  const k = e.key;
  if ((e.ctrlKey || e.metaKey) && (k === 's' || k === 'S')) { e.preventDefault(); saveFile(); return; }
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  if (editing && selImg && imgKey(e)) return;
  if (editing && (k === 'm' || k === 'M')) { blkToggle(); return; }
  if (editing && blkMode && blkKey(e)) return;
  if (k === 'e' || k === 'E') { toggleEdit(); return; }
  if (k === 'Escape' && editing && !ov.classList.contains('on')) { toggleEdit(false); return; }
  if (vfsOpen() && (k === 'p' || k === 'P' || k === 'k' || k === 'K')) { const v = vfs.querySelector('video'); v.paused ? v.play() : v.pause(); return; }
  if (vfsOpen() && k === 'Escape') { closeVfs(); return; }
  if (/^[0-9]$/.test(k)) { jumpBuf += k; jumpEl.style.display = 'block'; jumpEl.textContent = jumpBuf; clearTimeout(jumpT); jumpT = setTimeout(()=>{jumpBuf=''; jumpEl.style.display='none';}, 2500); return; }
  if (k === 'Enter' && jumpBuf) { go(+jumpBuf - 1); jumpBuf = ''; jumpEl.style.display='none'; return; }
  if (['ArrowRight','ArrowDown','PageDown',' ','Enter','MediaTrackNext'].includes(k)) { e.preventDefault(); next(); }
  else if (['ArrowLeft','ArrowUp','PageUp','Backspace','MediaTrackPrevious'].includes(k)) { e.preventDefault(); prev(); }
  else if (k === 'Home') go(0); else if (k === 'End') go(slides.length-1);
  else if (k === 'f' || k === 'F') toggleFs();
  else if (k === 'n' || k === 'N') openNotes();
  else if (k === 'g' || k === 'G' || k === 'o' || k === 'O') toggleOv();
  else if (k === 'Escape') { ov.classList.remove('on'); }
  else if (k === 'h' || k === 'H' || k === '?') help.classList.toggle('off');
}
document.addEventListener('keydown', onKey);
function toggleFs(){ if (!document.fullscreenElement) document.documentElement.requestFullscreen?.(); else document.exitFullscreen?.(); }
stage.addEventListener('click', e => { if (editing || e.target.closest('.vframe,a,button,input,video')) return; next(); });
stage.addEventListener('contextmenu', e => { e.preventDefault(); prev(); });
let tx = null; stage.addEventListener('touchstart', e => tx = e.touches[0].clientX, {passive:true});
stage.addEventListener('touchend', e => { if (tx === null) return; const dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 50) (dx < 0 ? next : prev)(); tx = null; });
let mt; addEventListener('mousemove', e => {
  document.body.classList.remove('hidecursor'); clearTimeout(mt); mt = setTimeout(()=>document.body.classList.add('hidecursor'), 2500);
  stage.style.setProperty('--mx', (e.clientX/innerWidth - .5) * 2); stage.style.setProperty('--my', (e.clientY/innerHeight - .5) * 2);
});

/* ---------- Video (kéo-thả hoặc chọn tệp, phát ngay trong slide) ---------- */
const vfs = document.getElementById('vfs');
const vfsOpen = () => vfs.classList.contains('on');
let vfsHome = null;
function setVideo(fr, src){
  let v = fr.querySelector('video');
  if (!v) { v = document.createElement('video'); v.playsInline = true; v.preload = 'auto'; fr.insertBefore(v, fr.firstChild);
    v.addEventListener('ended', () => { if (vfsOpen()) closeVfs(); });
    v.addEventListener('error', () => toast('Không phát được video này trên trình duyệt hiện tại — thử mở bằng Chrome hoặc Edge.', 6000)); }
  v.src = src; fr.classList.add('has'); fr.dataset.played = '';
  v.addEventListener('loadeddata', () => { try { if (v.currentTime === 0) v.currentTime = 0.05; } catch(e){} }, {once:true});
}
function playFull(fr){
  const v = fr.querySelector('video'); if (!v) return;
  fr.dataset.played = '1'; vfsHome = fr;
  if (!document.fullscreenElement) document.documentElement.requestFullscreen?.().catch(()=>{});
  vfs.appendChild(v); vfs.classList.add('on');
  v.controls = true; v.muted = false; v.volume = 1;
  try { v.currentTime = 0; } catch(e){}
  v.play().catch(() => { toast('Trình duyệt chặn phát tự động — bấm vào video để phát.'); });
}
function closeVfs(){
  const v = vfs.querySelector('video'); vfs.classList.remove('on');
  if (v) { v.pause(); v.controls = false; if (vfsHome) vfsHome.insertBefore(v, vfsHome.firstChild); }
  vfsHome = null;
}
vfs.addEventListener('click', e => { const v = vfs.querySelector('video'); if (v && e.target === vfs) v.paused ? v.play() : v.pause(); });
/* Giải mã base64 thành Blob theo từng khúc (Safari không nạp được chuỗi data: vài chục MB) */
function b64Blob(b64, type){
  if (Uint8Array.fromBase64) { try { return new Blob([Uint8Array.fromBase64(b64)], {type}); } catch(e){} }
  const CH = 1 << 22, parts = [];
  for (let i = 0; i < b64.length; i += CH) {
    const s = atob(b64.slice(i, i + CH)), u = new Uint8Array(s.length);
    for (let j = 0; j < s.length; j++) u[j] = s.charCodeAt(j);
    parts.push(u);
  }
  return new Blob(parts, {type});
}
const vidQueue = [];
document.querySelectorAll('.vframe').forEach(fr => {
  const si = slides.indexOf(fr.closest('.slide'));
  const inp = fr.querySelector('input');
  inp.accept = 'video/*';
  const load = file => {
    if (!file || !/^video\//.test(file.type)) { if (file) toast('Tệp này không phải video.'); return; }
    setVideo(fr, URL.createObjectURL(file));
    const mb = file.size / 1048576;
    if (mb > 300) { toast(`Video ${mb.toFixed(0)} MB quá lớn để nhúng vào file — chỉ phát trong phiên này. Hãy nén video dưới 300 MB.`, 7000); return; }
    const rd = new FileReader();
    rd.onload = () => { EDITS.videos[si] = rd.result; markDirty(); toast(`Đã gắn video (${mb.toFixed(1)} MB). Bấm <b>Ctrl+S</b> để lưu vĩnh viễn vào file trình chiếu.`, 6000); };
    rd.readAsDataURL(file);
  };
  fr.addEventListener('click', e => { if (e.target.closest('.vrm')) return; if (!fr.classList.contains('has') || editing) inp.click(); else playFull(fr); });
  inp.addEventListener('change', () => { load(inp.files[0]); inp.value = ''; });
  fr.addEventListener('dragover', e => { e.preventDefault(); fr.classList.add('drag'); });
  fr.addEventListener('dragleave', () => fr.classList.remove('drag'));
  fr.addEventListener('drop', e => { e.preventDefault(); fr.classList.remove('drag'); load(e.dataTransfer.files[0]); });
  const rm = document.createElement('button'); rm.className = 'vrm'; rm.textContent = '✕ Gỡ video'; fr.appendChild(rm);
  rm.addEventListener('click', e => { e.stopPropagation(); const v = fr.querySelector('video'); if (v) { v.pause(); v.remove(); } fr.classList.remove('has'); delete EDITS.videos[si]; EDITS.videos[si] = null; markDirty(); });
  // ưu tiên video người dùng gắn (Ctrl+S), sau đó video nhúng sẵn lúc build
  const emb = DV['dv-' + (si + 1)];
  if (EDITS.videos[si] === null) return;
  if (EDITS.videos[si]) { const d = EDITS.videos[si]; vidQueue.push(() => fetch(d).then(r => r.blob()).then(b => setVideo(fr, URL.createObjectURL(b))).catch(() => setVideo(fr, d))); }
  else if (emb) vidQueue.push(() => setVideo(fr, URL.createObjectURL(b64Blob(emb, 'video/mp4'))));
});
// nạp lần lượt từng video để không khựng lúc mở file
(function runQ(){ const f = vidQueue.shift(); if (!f) return; try { f(); } catch(e){ console.error(e); } setTimeout(runQ, 30); })();
// chặn trình duyệt mở tệp khi thả ra ngoài khung
addEventListener('dragover', e => e.preventDefault()); addEventListener('drop', e => e.preventDefault());

/* ---------- Overview (G) ---------- */
const ov = document.getElementById('ov');
const PC = PARTS.map(p => p ? p.c : '#4D8BFF'); PC[0] = PC[1] || '#4D8BFF';
ov.innerHTML = '<h2>Mục lục trình chiếu</h2><div class="gridv">' + slides.map((s,i) => `<div class="it" data-i="${i}" style="--c:${PC[+s.dataset.p||1]}"><span class="no">${i+1 <= TOTAL_NUMBERED ? i+1 : 'Kết'}</span><div class="k">${s.dataset.k||''}</div><div class="tt">${s.dataset.title||''}</div></div>`).join('') + '</div>';
ov.addEventListener('click', e => { const it = e.target.closest('.it'); if (it) { ov.classList.remove('on'); go(+it.dataset.i); } else ov.classList.remove('on'); });
function toggleOv(){ ov.classList.toggle('on'); ov.querySelectorAll('.it').forEach((el,i)=>el.classList.toggle('cur', i===cur)); }

/* ---------- Help hint ---------- */
const help = document.getElementById('help');
setTimeout(() => help.classList.add('off'), 6000);

/* ---------- Presenter notes window (N) ---------- */
let nw = null, t0 = null;
function esc(s){ return s.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])); }
function openNotes(){
  if (nw && !nw.closed) { nw.focus(); return; }
  nw = window.open('', 'misa-notes', 'width=980,height=760');
  if (!nw) { alert('Trình duyệt đã chặn cửa sổ ghi chú. Hãy cho phép pop-up rồi bấm N lại.'); return; }
  nw.document.write(`<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Ghi chú người trình bày</title><style>
  body{margin:0;font:400 20px/1.6 Inter,system-ui,sans-serif;background:#0C1836;color:#E8EDF8}
  header{display:flex;align-items:center;gap:20px;padding:18px 28px;background:#132453;position:sticky;top:0}
  #no{font:700 34px/1 'Google Sans',Inter,sans-serif;color:#fff}#tt{font:700 20px/1.3 'Google Sans',Inter,sans-serif;text-transform:uppercase;flex:1}
  #clk{font:700 30px/1 'Google Sans',Inter,sans-serif;color:#7FB0FF;font-variant-numeric:tabular-nums;cursor:pointer}
  main{padding:24px 32px 40px;white-space:pre-wrap}#nx{padding:14px 28px;background:#132453;color:#9BB0DA;font-size:16px;position:sticky;bottom:0}
  button{background:#1957F5;color:#fff;border:0;border-radius:10px;padding:10px 16px;font:600 15px Inter;cursor:pointer}
  </style></head><body><header><span id="no"></span><span id="tt"></span><span id="clk" title="Bấm để đặt lại">00:00</span><button id="pv">◀</button><button id="nxb">▶</button></header><main id="nt"></main><div id="nx"></div></body></html>`);
  nw.document.close();
  nw.document.addEventListener('keydown', onKey);
  nw.document.getElementById('pv').onclick = prev; nw.document.getElementById('nxb').onclick = next;
  t0 = Date.now(); nw.document.getElementById('clk').onclick = () => t0 = Date.now();
  const tick = () => { if (!nw || nw.closed) return; const s = Math.floor((Date.now()-t0)/1000); nw.document.getElementById('clk').textContent = String(Math.floor(s/60)).padStart(2,'0') + ':' + String(s%60).padStart(2,'0'); setTimeout(tick, 500); };
  tick(); updateNotes();
}
function updateNotes(){
  if (!nw || nw.closed) return;
  const d = nw.document, s = slides[cur], nx = slides[cur+1];
  d.getElementById('no').textContent = (cur+1 <= TOTAL_NUMBERED ? cur+1 : 'Kết');
  d.getElementById('tt').textContent = s.dataset.title || '';
  d.getElementById('nt').innerHTML = esc(NOTES[cur] || '(Không có ghi chú cho slide này)');
  d.getElementById('nx').textContent = nx ? 'Tiếp theo → ' + (nx.dataset.title || '') : 'Hết bài trình bày';
  nw.scrollTo(0, 0);
}

/* ---------- Chế độ chỉnh sửa (E) + lưu file (Ctrl+S) ---------- */
let editing = false, dirty = false;
const ebar = document.getElementById('ebar'), toastEl = document.getElementById('toast');
let toastT; function toast(html, ms){ toastEl.innerHTML = html; toastEl.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(()=>toastEl.classList.remove('on'), ms || 3500); }
function markDirty(){ dirty = true; ebar.classList.add('dirty'); }
function settle(slide){
  slide.getAnimations({subtree:true}).forEach(an => { try { if (an.effect.getComputedTiming().iterations !== Infinity) an.finish(); } catch(e){} });
  slide.querySelectorAll('[data-a]').forEach(el => { if (el._a) el._a.finish(); });
  slide.querySelectorAll('[data-type]').forEach(el => { clearTimeout(el._tt); el.textContent = el.dataset.full || el.textContent; });
  slide.querySelectorAll('.caret').forEach(c => c.remove());
  slide.querySelectorAll('[data-count]').forEach(el => { clearTimeout(el._t); cancelAnimationFrame(el._raf); el.textContent = (+el.dataset.count).toLocaleString('vi-VN'); });
  slide.querySelectorAll('[data-light]').forEach(el => { clearTimeout(el._t); el.classList.add('on'); });
}
function toggleEdit(on){
  editing = on === undefined ? !editing : on;
  document.body.classList.toggle('editing', editing);
  if (!editing) { lastEl = null; updFmt(); imgDeselect(); if (blkMode) blkToggle(false); }
  EDITABLE.forEach(el => { if (editing && !blkMode) { el.contentEditable = 'true'; el.spellcheck = false; } else el.removeAttribute('contenteditable'); });
  if (editing) { settle(slides[cur]); help.classList.add('off'); }
  else if (document.activeElement && document.activeElement.isContentEditable) document.activeElement.blur();
}
EDITABLE.forEach(el => {
  el.addEventListener('input', () => {
    if (el.hasAttribute('data-type')) el.dataset.full = el.textContent;
    if (el.hasAttribute('data-count')) { const v = parseInt(el.textContent.replace(/\D/g,'')); if (!isNaN(v)) el.dataset.count = v; }
    if (el.hasAttribute('data-slot')) { const v = parseInt(el.textContent.replace(/\D/g,'').slice(-1)); if (!isNaN(v)) el.dataset.slot = v; }
    if (el.matches('h2.t')) { const s = el.closest('.slide'); s.dataset.title = el.textContent.trim(); }
    saveEl(el);
  });
  el.addEventListener('paste', e => { e.preventDefault(); const t = (e.clipboardData || window.clipboardData).getData('text/plain'); document.execCommand('insertText', false, t); });
  el.addEventListener('click', e => { if (editing) e.stopPropagation(); });
});

/* ---------- Thanh định dạng chữ ---------- */
const fmt = document.getElementById('fmt');
let lastEl = null;
function saveEl(el){
  if (!el) return;
  const id = el.dataset.e;
  EDITS.texts[id] = el.hasAttribute('data-count') || el.hasAttribute('data-slot') ? el.textContent : el.innerHTML;
  // dịch chuyển / phóng to do chế độ Bố cục lưu riêng ở EDITS.blocks → không chép vào styles
  const st = (el.getAttribute('style') || '').replace(/(^|;)\s*(translate|scale)\s*:[^;]*;?/g, '$1').trim();
  if (st !== (ORIG_STYLE[+id] || '').trim()) EDITS.styles[id] = st; else delete EDITS.styles[id];
  markDirty();
}
function updFmt(){
  fmt.classList.toggle('off', !lastEl);
  if (!lastEl) return;
  const cs = getComputedStyle(lastEl), fs = parseFloat(cs.fontSize);
  const lh = cs.lineHeight === 'normal' ? 1.2 : parseFloat(cs.lineHeight) / fs;
  fmt.querySelector('.fsv').textContent = Math.round(fs) + 'px';
  fmt.querySelector('.lhv').textContent = lh.toFixed(2);
  fmt.querySelectorAll('[data-f="al"]').forEach(b => b.classList.toggle('on', cs.textAlign === b.dataset.v || (b.dataset.v === 'left' && (cs.textAlign === 'start'))));
  ['bold','italic','underline'].forEach(c => { const b = fmt.querySelector(`[data-f="${c}"]`); try { b.classList.toggle('on', document.queryCommandState(c)); } catch(e){} });
}
document.addEventListener('selectionchange', () => {
  if (!editing) return;
  const sel = getSelection(); if (!sel.rangeCount) return;
  const n = sel.anchorNode; const pe = n && (n.nodeType === 1 ? n : n.parentElement);
  const el = pe && pe.closest('[data-e]');
  if (el && el.isContentEditable) { lastEl = el; updFmt(); }
});
function selInEl(){ const s = getSelection(); return s.rangeCount && !s.isCollapsed && lastEl && lastEl.contains(s.getRangeAt(0).commonAncestorContainer) ? s.getRangeAt(0) : null; }
function wrapSel(r, styler){
  const span = document.createElement('span'); styler(span, r);
  span.appendChild(r.extractContents()); r.insertNode(span);
  const s = getSelection(); s.removeAllRanges(); const nr = document.createRange(); nr.selectNodeContents(span); s.addRange(nr);
}
fmt.addEventListener('mousedown', e => { if (e.target.closest('button')) e.preventDefault(); });
fmt.addEventListener('click', e => {
  const b = e.target.closest('button'); if (!b || !lastEl) return;
  const f = b.dataset.f, v = b.dataset.v, el = lastEl, r = selInEl();
  if (document.activeElement !== el) el.focus({preventScroll:true});
  document.execCommand('styleWithCSS', false, true);
  const cs = getComputedStyle(el), fs = parseFloat(cs.fontSize);
  if (f === 'fs+' || f === 'fs-') {
    const step = (f === 'fs+' ? 1 : -1) * (fs >= 40 ? 4 : 2);
    if (r) { const base = parseFloat(getComputedStyle(r.startContainer.nodeType === 1 ? r.startContainer : r.startContainer.parentElement).fontSize); wrapSel(r, sp => sp.style.fontSize = Math.max(10, base + step) + 'px'); }
    else el.style.fontSize = Math.max(10, fs + step) + 'px';
  } else if (f === 'lh+' || f === 'lh-') {
    const lh = cs.lineHeight === 'normal' ? 1.2 : parseFloat(cs.lineHeight) / fs;
    el.style.lineHeight = Math.max(.8, Math.min(3, lh + (f === 'lh+' ? .1 : -.1))).toFixed(2);
  } else if (f === 'br') { document.execCommand('insertLineBreak');
  } else if (f === 'bold' || f === 'italic' || f === 'underline') {
    if (r) document.execCommand(f);
    else { const map = {bold:['fontWeight','800','400'], italic:['fontStyle','italic','normal'], underline:['textDecoration','underline','none']}[f];
      const on = f === 'bold' ? parseInt(cs.fontWeight) >= 600 : f === 'italic' ? cs.fontStyle === 'italic' : cs.textDecorationLine.includes('underline');
      el.style[map[0]] = on ? map[2] : map[1]; }
  } else if (f === 'c') {
    if (r) document.execCommand('foreColor', false, v); else el.style.color = v;
  } else if (f === 'hl') {
    if (r) wrapSel(r, sp => { sp.style.background = 'linear-gradient(transparent 55%, rgba(255,205,60,.55) 55%)'; sp.style.padding = '0 .08em'; });
    else toast('Hãy bôi đen phần chữ cần tô nền.');
  } else if (f === 'al') { el.style.textAlign = v; if (getComputedStyle(el).display.includes('flex')) el.style.justifyContent = {left:'flex-start',center:'center',right:'flex-end',justify:'space-between'}[v];
  } else if (f === 'up' || f === 'low' || f === 'none') {
    if (r && f !== 'none') { const t = r.toString(); document.execCommand('insertText', false, f === 'up' ? t.toLocaleUpperCase('vi') : t.toLocaleLowerCase('vi')); }
    else el.style.textTransform = f === 'up' ? 'uppercase' : f === 'low' ? 'lowercase' : 'none';
  } else if (f === 'undo' || f === 'redo') { document.execCommand(f);
  } else if (f === 'clear') {
    if (r) document.execCommand('removeFormat');
    else { const o = ORIG_STYLE[+el.dataset.e]; if (o) el.setAttribute('style', o); else el.removeAttribute('style'); }
  }
  saveEl(el); updFmt();
});

async function saveFile(){
  const json = JSON.stringify(EDITS).replace(/<\//g, '<\\/');
  const i = PRISTINE.indexOf(EDIT_TAG), j = PRISTINE.indexOf('</' + 'script>', i);
  if (i < 0 || j < 0) { toast('Không tìm thấy vùng lưu dữ liệu trong file.'); return; }
  const html = PRISTINE.slice(0, i + EDIT_TAG.length) + json + PRISTINE.slice(j);
  const name = decodeURIComponent((location.pathname.split('/').pop() || 'trinh-chieu.html'));
  // ghép lại dữ liệu video nhúng vào đúng thẻ dv-N (dùng mảng phần để khỏi tạo chuỗi khổng lồ)
  const parts = []; let last = 0; const re = /(<script[^>]*\bid="(dv-\d+)"[^>]*>)(<\/script>)/g; let m;
  while ((m = re.exec(html))) { parts.push(html.slice(last, m.index + m[1].length), DV[m[2]] || ''); last = m.index + m[1].length; }
  parts.push(html.slice(last));
  const blob = new Blob(parts, {type:'text/html'});
  if (window.showSaveFilePicker) {
    try {
      const h = await showSaveFilePicker({ suggestedName: name, types:[{description:'Trang trình chiếu HTML', accept:{'text/html':['.html']}}] });
      const w = await h.createWritable(); await w.write(blob); await w.close();
      dirty = false; ebar.classList.remove('dirty'); toast('Đã lưu file: <b>' + h.name + '</b>'); return;
    } catch(e) { if (e && e.name === 'AbortError') return; }
  }
  const aEl = document.createElement('a'); aEl.href = URL.createObjectURL(blob); aEl.download = name; document.body.appendChild(aEl); aEl.click(); aEl.remove();
  dirty = false; ebar.classList.remove('dirty'); toast('Đã tải xuống bản mới: <b>' + name + '</b> — dùng file này để trình chiếu.', 6000);
}
ebar.querySelector('.sv').onclick = saveFile;
ebar.querySelector('.ex').onclick = () => toggleEdit(false);
addEventListener('beforeunload', e => { if (dirty) { e.preventDefault(); e.returnValue = ''; } });

window.deck = { go: n => go(n - 1), get index(){ return cur + 1; } };
/* ---------- Start ---------- */
const startAt = Math.max(0, Math.min(slides.length-1, (parseInt(location.hash.slice(1)) || 1) - 1));
document.fonts && document.fonts.ready ? document.fonts.ready.then(() => go(startAt)) : go(startAt);
})();
