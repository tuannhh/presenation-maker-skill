// Chụp nhanh mọi trang (trạng thái cuối hiệu ứng) và ghép thành 1 ảnh lưới để rà bằng mắt.
// node contact_sheet.mjs <deck.html> <ra.jpg> [cột=4] [rộng-ô=480]
// Dùng sau mỗi lần build: xem 1 ảnh là thấy trang nào tràn chữ, lệch, trống, sai màu.
import { writeFileSync } from 'node:fs';
import { openDeck, sleep } from './cdp.mjs';
const [file, outFile, colsArg, wArg] = process.argv.slice(2);
if (!file || !outFile) { console.log('node contact_sheet.mjs <deck.html> <ra.jpg> [cột=4] [rộng-ô=480]'); process.exit(1); }
const cols = +(colsArg || 4), cw = +(wArg || 480), ch = Math.round(cw * 9 / 16);
const d = await openDeck(file, { scale: 1 });
const n = await d.ev('document.querySelectorAll(".slide").length');
const shots = [];
for (let k = 1; k <= n; k++) {
  await d.ev(`deck.go(${k})`); await sleep(3400);
  await d.ev(`document.getAnimations().forEach(a=>{try{if(a.effect&&a.effect.getComputedTiming().iterations!==Infinity)a.finish()}catch(e){}})`);
  await sleep(250);
  const s = await d.send('Page.captureScreenshot', { format: 'jpeg', quality: 70 });
  shots.push(s.result.data); process.stdout.write(k + ' ');
}
// ghép trong chính trình duyệt (canvas) để không cần thư viện ảnh
const rows = Math.ceil(n / cols);
const data = await d.ev(`(async()=>{const S=${JSON.stringify(shots)};const c=document.createElement('canvas');c.width=${cols}*${cw}+${(cols + 1) * 10};c.height=${rows}*(${ch}+28)+10;const x=c.getContext('2d');x.fillStyle='#222';x.fillRect(0,0,c.width,c.height);
for(let i=0;i<S.length;i++){const im=new Image();im.src='data:image/jpeg;base64,'+S[i];await im.decode();const cx=10+(i%${cols})*(${cw}+10),cy=10+Math.floor(i/${cols})*(${ch}+28);x.drawImage(im,cx,cy,${cw},${ch});x.fillStyle='#fff';x.font='bold 16px sans-serif';x.fillText(String(i+1),cx,cy+${ch}+19);}
return c.toDataURL('image/jpeg',.82).split(',')[1]})()`);
writeFileSync(outFile, Buffer.from(data, 'base64'));
console.log(`\n=> ${outFile} (${n} trang)`);
d.close();
