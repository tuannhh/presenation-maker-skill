/* ---------- Ảnh chèn thêm (chế độ sửa): kéo-thả / dán / chọn tệp; di chuyển, đổi cỡ, xoay; sáng tối, bo góc, viền, bóng ---------- */
const ipan = document.getElementById('ipan');
const IMG_DEF = { r:0, b:100, rad:4, bw:0, bc:'#ffffff', sh:40, z:6 };
let selImg = null, imgDrag = null;
const stageK = () => stage.getBoundingClientRect().width / 1920;
function stagePt(e){ const r = stage.getBoundingClientRect(), k = r.width / 1920; return { x:(e.clientX - r.left) / k, y:(e.clientY - r.top) / k }; }

function imgApply(el){
  const d = EDITS.images[el.dataset.img]; if (!d) return;
  Object.assign(el.style, { left:d.x + 'px', top:d.y + 'px', width:d.w + 'px', height:d.h + 'px', zIndex:d.z });
  el.querySelector('.uin').style.transform = d.r ? `rotate(${d.r}deg)` : '';
  const im = el.querySelector('img');
  im.style.filter = d.b !== 100 ? `brightness(${d.b / 100})` : '';
  im.style.borderRadius = Math.round(d.rad / 100 * Math.min(d.w, d.h)) + 'px';
  im.style.border = d.bw > 0 ? `${d.bw}px solid ${d.bc}` : 'none';
  im.style.boxShadow = d.sh > 0 ? `0 ${(d.sh * .32).toFixed(1)}px ${(d.sh * 1.1).toFixed(1)}px rgba(8,22,60,${(.1 + d.sh / 260).toFixed(2)})` : 'none';
}
function imgMake(id){
  const d = EDITS.images[id], slide = slides[d.s]; if (!slide) return null;
  const el = document.createElement('div'); el.className = 'uimg'; el.dataset.img = id; el.dataset.a = 'zoom'; el.dataset.d = '350';
  el.innerHTML = '<div class="uin"><img alt="" draggable="false"><i class="h c1"></i><i class="h c2"></i><i class="h c3"></i><i class="h c4"></i><i class="h rt"></i></div>';
  el.querySelector('img').src = d.src;
  slide.appendChild(el); imgApply(el);
  el.addEventListener('pointerdown', imgDown);
  return el;
}
Object.keys(EDITS.images).forEach(imgMake);

function imgSelect(el){
  if (selImg && selImg !== el) selImg.classList.remove('sel');
  selImg = el; el.classList.add('sel'); document.body.classList.add('imgsel'); imgPanel();
  if (document.activeElement && document.activeElement.isContentEditable) document.activeElement.blur();
}
function imgDeselect(){ if (!selImg) return; selImg.classList.remove('sel'); selImg = null; document.body.classList.remove('imgsel'); }

function imgDown(e){
  if (!editing) return;
  e.preventDefault(); e.stopPropagation();
  const el = e.currentTarget; imgSelect(el);
  const d = EDITS.images[el.dataset.img], p = stagePt(e), cx = d.x + d.w / 2, cy = d.y + d.h / 2;
  const t = e.target.classList;
  imgDrag = { el, mode: t.contains('rt') ? 'rot' : t.contains('h') ? 'rs' : 'mv', p0:p, d0:{...d}, cx, cy,
    a0: Math.atan2(p.y - cy, p.x - cx), r0: Math.hypot(p.x - cx, p.y - cy) || 1, moved:false };
  el.setPointerCapture(e.pointerId);
  el.addEventListener('pointermove', imgMove); el.addEventListener('pointerup', imgUp); el.addEventListener('pointercancel', imgUp);
}
function imgMove(e){
  const g = imgDrag; if (!g) return;
  const d = EDITS.images[g.el.dataset.img], p = stagePt(e);
  if (g.mode === 'mv') { d.x = Math.round(g.d0.x + p.x - g.p0.x); d.y = Math.round(g.d0.y + p.y - g.p0.y); }
  else if (g.mode === 'rs') {
    const f = Math.hypot(p.x - g.cx, p.y - g.cy) / g.r0;
    d.w = Math.max(60, Math.round(g.d0.w * f)); d.h = Math.round(d.w * g.d0.h / g.d0.w);
    d.x = Math.round(g.cx - d.w / 2); d.y = Math.round(g.cy - d.h / 2);
  } else {
    let r = g.d0.r + (Math.atan2(p.y - g.cy, p.x - g.cx) - g.a0) * 180 / Math.PI;
    r = ((r + 540) % 360) - 180; if (e.shiftKey) r = Math.round(r / 15) * 15; else if (Math.abs(r) < 2) r = 0;
    d.r = Math.round(r);
  }
  g.moved = true; imgApply(g.el); imgPanel();
}
function imgUp(e){
  const g = imgDrag; if (!g) return; imgDrag = null;
  g.el.removeEventListener('pointermove', imgMove); g.el.removeEventListener('pointerup', imgUp); g.el.removeEventListener('pointercancel', imgUp);
  if (g.moved) markDirty();
}
document.addEventListener('pointerdown', e => { if (editing && selImg && !e.target.closest('.uimg,#ipan,#ebar')) imgDeselect(); });

/* Bảng chỉnh ảnh */
function imgPanel(){
  if (!selImg) return; const d = EDITS.images[selImg.dataset.img];
  ipan.querySelectorAll('[data-k]').forEach(inp => { if (document.activeElement !== inp) inp.value = d[inp.dataset.k]; });
  ipan.querySelector('[data-v="b"]').textContent = d.b + '%';
  ipan.querySelector('[data-v="rad"]').textContent = d.rad + '%';
  ipan.querySelector('[data-v="bw"]').textContent = d.bw + 'px';
  ipan.querySelector('[data-v="sh"]').textContent = d.sh;
  ipan.querySelector('[data-v="r"]').textContent = d.r + '°';
  ipan.querySelectorAll('[data-bc]').forEach(b => b.classList.toggle('on', b.dataset.bc.toLowerCase() === String(d.bc).toLowerCase()));
}
ipan.addEventListener('input', e => {
  const k = e.target.dataset.k; if (!k || !selImg) return;
  const d = EDITS.images[selImg.dataset.img]; d[k] = k === 'bc' ? e.target.value : +e.target.value;
  if (k === 'bc' && !d.bw) d.bw = 4;
  imgApply(selImg); imgPanel(); markDirty();
});
ipan.addEventListener('click', e => {
  const b = e.target.closest('button'); if (!b || !selImg) return;
  const id = selImg.dataset.img, d = EDITS.images[id];
  if (b.dataset.bc) { d.bc = b.dataset.bc; if (!d.bw) d.bw = 4; }
  else if (b.dataset.ia === 'front') d.z = Math.max(6, ...Object.values(EDITS.images).filter(o => o.s === d.s).map(o => o.z)) + 1;
  else if (b.dataset.ia === 'back') d.z = -1;
  else if (b.dataset.ia === 'reset') Object.assign(d, IMG_DEF);
  else if (b.dataset.ia === 'del') { const el = selImg; imgDeselect(); el.remove(); delete EDITS.images[id]; markDirty(); toast('Đã xoá ảnh.'); return; }
  imgApply(selImg); imgPanel(); markDirty();
});
/* Phím tắt khi đang chọn ảnh: Delete xoá, mũi tên dịch (Shift = 10px), Esc bỏ chọn */
function imgKey(e){
  const k = e.key, d = EDITS.images[selImg.dataset.img], st = e.shiftKey ? 10 : 2;
  if (k === 'Delete' || k === 'Backspace') { ipan.querySelector('[data-ia="del"]').click(); e.preventDefault(); return true; }
  if (k === 'Escape') { imgDeselect(); return true; }
  const mv = { ArrowLeft:[-st,0], ArrowRight:[st,0], ArrowUp:[0,-st], ArrowDown:[0,st] }[k];
  if (mv) { e.preventDefault(); d.x += mv[0]; d.y += mv[1]; imgApply(selImg); markDirty(); return true; }
  return false;
}

/* Đưa ảnh vào: nén về tối đa 1920px (webp, Safari không có webp thì jpeg/png) */
function imgFileData(file){
  return new Promise((res, rej) => {
    const fr = new FileReader();
    fr.onerror = rej;
    fr.onload = () => {
      const raw = fr.result;
      if (/svg|gif/.test(file.type)) { const im = new Image(); im.onload = () => res({ src:raw, w:im.naturalWidth || 800, h:im.naturalHeight || 600 }); im.onerror = rej; im.src = raw; return; }
      const im = new Image();
      im.onerror = rej;
      im.onload = () => {
        const W = im.naturalWidth, H = im.naturalHeight, s = Math.min(1, 1920 / Math.max(W, H));
        const c = document.createElement('canvas'); c.width = Math.round(W * s); c.height = Math.round(H * s);
        c.getContext('2d').drawImage(im, 0, 0, c.width, c.height);
        let out = c.toDataURL('image/webp', .86);
        if (!out.startsWith('data:image/webp')) out = file.type === 'image/png' ? c.toDataURL('image/png') : c.toDataURL('image/jpeg', .88);
        if (out.length > raw.length && s === 1) out = raw;
        res({ src:out, w:c.width, h:c.height });
      };
      im.src = raw;
    };
    fr.readAsDataURL(file);
  });
}
async function imgInsert(files, at){
  const list = [...files].filter(f => /^image\//.test(f.type));
  if (!list.length) return false;
  if (!editing) toggleEdit(true);
  let i = 0;
  for (const f of list) {
    try {
      const { src, w, h } = await imgFileData(f);
      const W = Math.min(720, w), H = Math.round(W * h / w);
      const sc = H > 760 ? 760 / H : 1, ww = Math.round(W * sc), hh = Math.round(H * sc);
      const c = at || { x:960, y:560 };
      const id = 'i' + Date.now().toString(36) + Math.random().toString(36).slice(2, 5);
      EDITS.images[id] = { s:cur, src, x:Math.round(c.x - ww / 2 + i * 30), y:Math.round(c.y - hh / 2 + i * 30), w:ww, h:hh, ...IMG_DEF,
        z: Math.max(5, ...Object.values(EDITS.images).filter(o => o.s === cur).map(o => o.z)) + 1 };
      const el = imgMake(id); el._a = el.animate(KF.pop, {duration:450, easing:SPRING, fill:'both'}); imgSelect(el); i++;
    } catch(err) { toast('Không đọc được ảnh: ' + esc(f.name)); }
  }
  if (i) { markDirty(); toast(`Đã chèn ${i} ảnh — kéo để di chuyển, kéo góc để đổi cỡ, kéo nút tròn phía trên để xoay.`, 5000); }
  return true;
}
stage.addEventListener('dragover', e => { if ([...(e.dataTransfer.items || [])].some(it => it.kind === 'file' && /^image\//.test(it.type)) && !e.target.closest('.vframe')) { e.preventDefault(); stage.classList.add('imgdrop'); } });
stage.addEventListener('dragleave', e => { if (e.target === stage || !stage.contains(e.relatedTarget)) stage.classList.remove('imgdrop'); });
stage.addEventListener('drop', e => {
  stage.classList.remove('imgdrop');
  if (e.target.closest('.vframe')) return;
  const fs = e.dataTransfer && e.dataTransfer.files; if (!fs || !fs.length) return;
  e.preventDefault(); imgInsert(fs, stagePt(e));
});
document.addEventListener('paste', e => {
  if (!editing) return;
  const fs = [...(e.clipboardData && e.clipboardData.files || [])].filter(f => /^image\//.test(f.type));
  if (fs.length) { e.preventDefault(); imgInsert(fs); }
});
const imgPick = document.createElement('input'); imgPick.type = 'file'; imgPick.accept = 'image/*'; imgPick.multiple = true; imgPick.hidden = true; document.body.appendChild(imgPick);
imgPick.addEventListener('change', () => { imgInsert(imgPick.files); imgPick.value = ''; });
ebar.querySelector('.ad').onclick = () => imgPick.click();

/* ---------- Chế độ Bố cục (trong chế độ sửa, phím M): chọn bất kỳ khối chữ / hình / thẻ nào để kéo di chuyển, phóng to-thu nhỏ hoặc xoá.
   Lưu ở EDITS.blocks["trang:thứ tự"] = {x, y, sc, del}. Dùng thuộc tính CSS translate/scale (không đụng transform của hiệu ứng vào). ---------- */
const bpan = document.getElementById('bpan');
let blkMode = false, selBlk = null, blkDrag = null, hovBlk = null;
const blkEl = key => stage.querySelector(`[data-b="${key}"]`);
function blkApply(el){
  const d = EDITS.blocks[el.dataset.b];
  el.style.translate = d && (d.x || d.y) ? `${d.x || 0}px ${d.y || 0}px` : '';
  el.style.scale = d && d.sc && d.sc !== 1 ? String(d.sc) : '';
  el.classList.toggle('xdel', !!(d && d.del));
}
Object.keys(EDITS.blocks).forEach(k => { const el = blkEl(k); if (el) blkApply(el); });
function blkClean(key){ const d = EDITS.blocks[key]; if (d && !d.x && !d.y && (!d.sc || d.sc === 1) && !d.del) delete EDITS.blocks[key]; }
function blkName(el){
  const t = (el.innerText || '').trim().replace(/\s+/g, ' ');
  if (t) return '“' + (t.length > 34 ? t.slice(0, 34) + '…' : t) + '”';
  if (el.matches('svg,.i')) return 'biểu tượng';
  if (el.matches('img,[data-ph],[data-im],.im,.ph') || getComputedStyle(el).backgroundImage !== 'none') return 'hình ảnh';
  return 'khối';
}
function blkPanel(){
  if (!bpan) return;
  bpan.querySelector('.bn').textContent = selBlk ? blkName(selBlk) : 'Bấm vào chữ / hình / thẻ để chọn';
  const d = selBlk && EDITS.blocks[selBlk.dataset.b];
  bpan.querySelector('.bsc').textContent = Math.round(((d && d.sc) || 1) * 100) + '%';
  bpan.querySelectorAll('[data-ba]:not([data-ba="restore"]):not([data-ba="off"])').forEach(b => b.disabled = !selBlk);
  const nDel = Object.entries(EDITS.blocks).filter(([k, v]) => v.del && +k.split(':')[0] === cur).length;
  const rb = bpan.querySelector('[data-ba="restore"]'); rb.disabled = !nDel; rb.textContent = nDel ? `Hiện lại ${nDel} khối đã xoá` : 'Hiện lại khối đã xoá';
}
function blkSelect(el){
  if (selBlk) selBlk.classList.remove('bsel');
  selBlk = el; if (el) el.classList.add('bsel');
  blkPanel();
}
function blkToggle(on){
  blkMode = on === undefined ? !blkMode : on;
  document.body.classList.toggle('blkmode', blkMode);
  if (!blkMode) { blkSelect(null); if (hovBlk) { hovBlk.classList.remove('bhov'); hovBlk = null; } }
  else { imgDeselect(); if (document.activeElement && document.activeElement.isContentEditable) document.activeElement.blur(); lastEl = null; updFmt(); }
  EDITABLE.forEach(el => { if (editing && !blkMode) { el.contentEditable = 'true'; el.spellcheck = false; } else el.removeAttribute('contenteditable'); });
  const mb = ebar.querySelector('.mb'); if (mb) mb.classList.toggle('on', blkMode);
  if (blkMode) { blkPanel(); toast('Bố cục: bấm để chọn khối · kéo để di chuyển · <b>Q</b> chọn khối lớn hơn · <b>Delete</b> xoá · <b>M</b> quay lại sửa chữ', 6000); }
}
/* khối nằm dưới con trỏ, trong trang đang xem */
function blkAt(t){
  const s = slides[cur]; if (!s || !t || !s.contains(t)) return null;
  const el = t.closest('[data-b]'); return el && s.contains(el) ? el : null;
}
document.addEventListener('pointerdown', e => {
  if (!editing || !blkMode || e.button !== 0) return;
  if (e.target.closest('#ebar,#bpan,#fmt,#ipan,#toast,.uimg')) return;
  const el = blkAt(e.target);
  e.preventDefault(); e.stopPropagation();
  if (!el) { blkSelect(null); return; }
  const tgt = e.altKey && el.parentElement && el.parentElement.closest('[data-b]') ? el.parentElement.closest('[data-b]') : el;
  if (!(selBlk && selBlk.contains(e.target) && !e.altKey)) blkSelect(tgt);
  const key = selBlk.dataset.b, d = EDITS.blocks[key] || {};
  blkDrag = { el: selBlk, key, p0: stagePt(e), x0: d.x || 0, y0: d.y || 0, moved: false };
}, true);
addEventListener('pointermove', e => {
  if (!editing || !blkMode) return;
  if (blkDrag) {
    const p = stagePt(e), g = blkDrag, dx = p.x - g.p0.x, dy = p.y - g.p0.y;
    if (!g.moved && Math.hypot(dx, dy) < 4) return;
    g.moved = true;
    const d = EDITS.blocks[g.key] || (EDITS.blocks[g.key] = {});
    d.x = Math.round(g.x0 + dx); d.y = Math.round(g.y0 + dy); blkApply(g.el);
    return;
  }
  const el = blkAt(e.target);
  if (el !== hovBlk) { if (hovBlk) hovBlk.classList.remove('bhov'); hovBlk = el; if (el) el.classList.add('bhov'); }
});
addEventListener('pointerup', () => { if (!blkDrag) return; const g = blkDrag; blkDrag = null; if (g.moved) { blkClean(g.key); markDirty(); } });
/* chặn bấm-chuyển-trang, mở link, mở khung video khi đang ở chế độ Bố cục */
document.addEventListener('click', e => { if (editing && blkMode && slides[cur] && slides[cur].contains(e.target)) { e.preventDefault(); e.stopPropagation(); } }, true);
function blkDo(a){
  if (a === 'off') { blkToggle(false); return; }
  if (a === 'restore') {
    Object.entries(EDITS.blocks).forEach(([k, v]) => { if (v.del && +k.split(':')[0] === cur) { v.del = false; blkClean(k); const el = blkEl(k); if (el) blkApply(el); } });
    markDirty(); blkPanel(); return;
  }
  if (!selBlk) return;
  const key = selBlk.dataset.b, d = EDITS.blocks[key] || (EDITS.blocks[key] = {});
  if (a === 'up') { const p = selBlk.parentElement && selBlk.parentElement.closest('[data-b]'); if (p && slides[cur].contains(p)) blkSelect(p); blkClean(key); return; }
  if (a === 'big' || a === 'small') d.sc = Math.max(.2, Math.min(4, Math.round(((d.sc || 1) * (a === 'big' ? 1.1 : 1 / 1.1)) * 100) / 100));
  else if (a === 'reset') { delete d.x; delete d.y; delete d.sc; }
  else if (a === 'del') { d.del = true; blkApply(selBlk); blkSelect(null); blkClean(key); markDirty(); toast('Đã xoá khối. Bấm <b>Hiện lại khối đã xoá</b> nếu cần lấy lại.'); return; }
  blkApply(selBlk); blkClean(key); markDirty(); blkPanel();
}
if (bpan) {
  bpan.addEventListener('mousedown', e => e.preventDefault());
  bpan.addEventListener('click', e => { const b = e.target.closest('[data-ba]'); if (b) blkDo(b.dataset.ba); });
}
const mbtn = ebar.querySelector('.mb'); if (mbtn) mbtn.onclick = () => blkToggle();
/* Phím khi ở chế độ Bố cục: mũi tên dịch khối đang chọn (Shift = 10px), Delete xoá, Q khối lớn hơn, +/− phóng to/thu nhỏ, Esc bỏ chọn */
function blkKey(e){
  const k = e.key;
  if (selBlk && !slides[cur].contains(selBlk)) blkSelect(null);
  if (k === 'Escape') { if (selBlk) { blkSelect(null); return true; } blkToggle(false); return true; }
  if (!selBlk) return false;
  if (k === 'Delete' || k === 'Backspace') { e.preventDefault(); blkDo('del'); return true; }
  if (k === 'q' || k === 'Q') { blkDo('up'); return true; }
  if (k === '+' || k === '=') { blkDo('big'); return true; }
  if (k === '-' || k === '_') { blkDo('small'); return true; }
  const st = e.shiftKey ? 10 : 2, mv = { ArrowLeft:[-st,0], ArrowRight:[st,0], ArrowUp:[0,-st], ArrowDown:[0,st] }[k];
  if (mv) { e.preventDefault(); const key = selBlk.dataset.b, d = EDITS.blocks[key] || (EDITS.blocks[key] = {}); d.x = (d.x || 0) + mv[0]; d.y = (d.y || 0) + mv[1]; blkApply(selBlk); blkClean(key); markDirty(); return true; }
  return false;
}
