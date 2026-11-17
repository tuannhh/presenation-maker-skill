// Helper: mở 1 file HTML trong Chrome headless và điều khiển qua DevTools Protocol (Node ≥22 có sẵn WebSocket)
import { spawn } from 'node:child_process';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
export const sleep = ms => new Promise(r => setTimeout(r, ms));
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
export async function openDeck(file, { scale = 1, hash = '#1', port = 9300 + Math.floor(Math.random() * 500) } = {}) {
  const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${mkdtempSync(tmpdir() + '/cdp-')}`,
    '--hide-scrollbars', '--mute-audio', '--window-size=1920,1080', '--no-first-run', 'about:blank'], { stdio: 'ignore' });
  let tgt;
  for (let i = 0; i < 60 && !tgt; i++) { await sleep(300); try { tgt = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find(t => t.type === 'page'); } catch {} }
  if (!tgt) { chrome.kill(); throw new Error('Không mở được Chrome headless'); }
  const ws = new WebSocket(tgt.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const pend = new Map();
  ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } };
  const send = (method, params = {}) => new Promise(r => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async expr => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); if (r.result?.exceptionDetails) throw new Error(r.result.exceptionDetails.exception?.description || 'JS error'); return r.result?.result?.value; };
  await send('Emulation.setDeviceMetricsOverride', { width: 1920, height: 1080, deviceScaleFactor: scale, mobile: false });
  await send('Page.enable');
  await send('Page.navigate', { url: 'file://' + resolve(file) + hash });
  // chờ app sẵn sàng + video nhúng nạp xong (tối đa ~60s)
  for (let i = 0; i < 120; i++) { await sleep(500); try { if (await ev(`!!window.deck && document.querySelectorAll('.vframe video').length >= document.querySelectorAll('script[id^="dv-"]').length`)) break; } catch {} }
  await sleep(1200);
  await ev(`(()=>{const s=document.createElement('style');s.textContent='#help,#toast,#ebar,#fmt,#ipan,#jump{display:none!important}*{cursor:none!important}';document.head.appendChild(s);})()`);
  const close = () => { try { ws.close(); } catch {} chrome.kill(); };
  return { send, ev, close };
}
// hiện slide k (1-based) ở trạng thái cuối của hiệu ứng
export async function showSlide(d, k, wait = 4200) {
  await d.ev(`deck.go(${k})`); await sleep(wait);
  await d.ev(`document.getAnimations().forEach(a=>{try{if(a.effect&&a.effect.getComputedTiming().iterations!==Infinity)a.finish()}catch(e){}})`);
  await sleep(400);
}
