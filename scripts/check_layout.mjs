// Rà lỗi bố cục từng trang: tiêu đề có dòng cuối chỉ 1 từ, chữ tràn khỏi khung/thẻ, icon đè chữ.
// node check_layout.mjs <deck.html>
import { openDeck, showSlide } from './cdp.mjs';
const d = await openDeck(process.argv[2]);
const n = await d.ev('document.querySelectorAll(".slide").length');
let bad = 0;
for (let k = 1; k <= n; k++) {
  await showSlide(d, k, 2600);
  const r = await d.ev(`(()=>{
    const s=document.querySelectorAll('.slide')[${k-1}], out=[];
    const lines=el=>{const rg=document.createRange();const w=[];const tw=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let t;while(t=tw.nextNode()){const re=/\\S+/g;let m;while(m=re.exec(t.data)){rg.setStart(t,m.index);rg.setEnd(t,m.index+m[0].length);const b=rg.getClientRects()[0];if(b)w.push([Math.round(b.top),m[0]]);}}const L={};w.forEach(([y,x])=>{const key=Object.keys(L).find(q=>Math.abs(q-y)<8)||y;(L[key]=L[key]||[]).push(x)});return Object.values(L)};
    s.querySelectorAll('h1,h2,h3,.t,.h3,.h4,.ttl,.sub,.lbl,.big').forEach(el=>{const L=lines(el);if(L.length>1&&L[L.length-1].length===1)out.push('mồ côi: "'+el.textContent.trim().slice(0,50)+'" → "'+L[L.length-1][0]+'"')});
    s.querySelectorAll('*').forEach(el=>{if(!el.childNodes.length||el.closest('svg'))return;const hasT=[...el.childNodes].some(c=>c.nodeType===3&&c.textContent.trim());if(!hasT)return;
      const cs=getComputedStyle(el);if(cs.overflow!=='visible'||cs.textOverflow==='ellipsis'){const eb=el.getBoundingClientRect();const rg=document.createRange();for(const c of el.childNodes){if(c.nodeType!==3||!c.textContent.trim())continue;rg.selectNodeContents(c);for(const b of rg.getClientRects()){if(b.right>eb.right+2||b.left<eb.left-2||b.bottom>eb.bottom+2){out.push('chữ bị cắt: "'+el.textContent.trim().slice(0,40)+'"');break}}}}
      const box=el.closest('.card,[class*="card"],.chip,.pill');if(box&&box!==el){const a=el.getBoundingClientRect(),b=box.getBoundingClientRect();if(a.right>b.right+2||a.bottom>b.bottom+2||a.left<b.left-2)out.push('ra ngoài thẻ: "'+el.textContent.trim().slice(0,40)+'"')}});
    // tràn xuống vùng chân trang (thanh tiến độ ở ~y=1000 trên khung 1080)
    s.querySelectorAll('.card,.banner,.vframe,.im,.toc,.bars').forEach(el=>{const b=el.getBoundingClientRect();if(b.height&&b.bottom>1004&&!s.classList.contains('cover'))out.push('tràn xuống chân trang: '+(el.className.split(' ')[0])+' "'+el.textContent.trim().slice(0,30)+'" (đáy '+Math.round(b.bottom)+'px)')});
    // nhãn ngắn bị xuống dòng
    s.querySelectorAll('.chip,.lbl,.stepn,.tag,.ck').forEach(el=>{if(!el.textContent.trim())return;const L=lines(el);if(L.length>1)out.push('nhãn bị xuống dòng: "'+el.textContent.trim().slice(0,30)+'"')});
    const txt=[...s.querySelectorAll('*')].filter(e=>[...e.childNodes].some(c=>c.nodeType===3&&c.textContent.trim())).map(e=>e.getBoundingClientRect());
    s.querySelectorAll('svg.i').forEach(ic=>{const a=ic.getBoundingClientRect();if(!a.width)return;if(txt.some(b=>a.left<b.right-3&&a.right>b.left+3&&a.top<b.bottom-3&&a.bottom>b.top+3&&!(b.left<=a.left&&b.right>=a.right&&b.top<=a.top&&b.bottom>=a.bottom)))out.push('icon đè chữ')});
    return [...new Set(out)];
  })()`);
  if (r.length) { bad++; console.log(`Trang ${k}:`); r.forEach(x => console.log('   -', x)); }
}
console.log(bad ? `\n${bad} trang cần xem lại (kiểm tra bằng mắt — có thể là ngắt dòng cố ý)` : 'Không phát hiện lỗi bố cục.');
d.close();
