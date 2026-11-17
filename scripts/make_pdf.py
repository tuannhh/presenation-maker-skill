#!/usr/bin/env python3
"""Ghép ảnh slide thành PDF 16:9 (960x540pt) + tách video nhúng ra thư mục video/ + gắn link bấm mở video.
python make_pdf.py <shots_dir> <deck.html> <out_dir> "<Tiêu đề>" [ten_file.pdf]
Video lấy từ chính file HTML (thẻ dv-N = video nhúng lúc build, và video người dùng gắn trong deck-edits)."""
import base64, glob, json, os, re, sys
from PIL import Image
shots, deck, out_dir, title = sys.argv[1:5]
pdf_name = sys.argv[5] if len(sys.argv) > 5 else re.sub(r'[\\/:*?"<>|]', '', title) + '.pdf'
os.makedirs(os.path.join(out_dir, 'video'), exist_ok=True)
h = open(deck, encoding='utf-8').read()
vids = {int(n): base64.b64decode(b) for n, b in re.findall(r'<script type="application/octet-stream" id="dv-(\d+)">([^<]*)</script>', h) if b.strip()}
m = re.search(r'<script id="deck-edits" type="application/json">(.*?)</script>', h, re.S)
if m:
    ed = json.loads(m.group(1).replace('<\\/', '</') or '{}')
    for si, v in (ed.get('videos') or {}).items():
        if v is None: vids.pop(int(si) + 1, None)
        elif v.startswith('data:'): vids[int(si) + 1] = base64.b64decode(v.split(',', 1)[1])
VIDEO = {}
for n, data in sorted(vids.items()):
    rel = f'video/video-trang-{n:02d}.mp4'; open(os.path.join(out_dir, rel), 'wb').write(data); VIDEO[n] = rel
links = {l['page']: l for l in json.load(open(os.path.join(shots, 'links.json')))} if os.path.exists(os.path.join(shots, 'links.json')) else {}
files = sorted(glob.glob(os.path.join(shots, 's*.jpg')))
PW, PH, K = 960, 540, 0.5
objs = []
def add(b): objs.append(b if isinstance(b, bytes) else b.encode('latin-1')); return len(objs)
def pdfstr(s): return '<FEFF' + s.encode('utf-16-be').hex().upper() + '>'
catalog = add(''); pages = add(''); kids = []
for f in files:
    i = int(re.search(r's(\d+)\.jpg$', f).group(1))
    data = open(f, 'rb').read(); w, hh = Image.open(f).size
    img = add(f'<< /Type /XObject /Subtype /Image /Width {w} /Height {hh} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length {len(data)} >>\nstream\n'.encode() + data + b'\nendstream')
    cs = f'q {PW} 0 0 {PH} 0 0 cm /Im0 Do Q'.encode()
    cont = add(f'<< /Length {len(cs)} >>\nstream\n'.encode() + cs + b'\nendstream')
    annots = ''
    if i in links and i in VIDEO:
        l = links[i]; x1, x2 = l['x'] * K, (l['x'] + l['w']) * K; y1, y2 = PH - (l['y'] + l['h']) * K, PH - l['y'] * K
        a = add(f'<< /Type /Annot /Subtype /Link /Rect [{x1:.1f} {y1:.1f} {x2:.1f} {y2:.1f}] /Border [0 0 0] /H /O /Contents {pdfstr("Bấm để mở video")} /A << /S /URI /URI ({VIDEO[i]}) >> >>')
        annots = f' /Annots [{a} 0 R]'
    kids.append(add(f'<< /Type /Page /Parent {pages} 0 R /MediaBox [0 0 {PW} {PH}] /Resources << /XObject << /Im0 {img} 0 R >> >> /Contents {cont} 0 R{annots} >>'))
objs[pages - 1] = f'<< /Type /Pages /Kids [{" ".join(f"{k} 0 R" for k in kids)}] /Count {len(kids)} >>'.encode()
objs[catalog - 1] = f'<< /Type /Catalog /Pages {pages} 0 R /ViewerPreferences << /DisplayDocTitle true >> >>'.encode()
info = add(f'<< /Title {pdfstr(title)} /Author {pdfstr("MISA")} >>')
buf = bytearray(b'%PDF-1.6\n%\xe2\xe3\xcf\xd3\n'); offs = []
for n, b in enumerate(objs, 1): offs.append(len(buf)); buf += f'{n} 0 obj\n'.encode() + b + b'\nendobj\n'
x = len(buf)
buf += f'xref\n0 {len(objs)+1}\n0000000000 65535 f \n'.encode() + b''.join(f'{o:010d} 00000 n \n'.encode() for o in offs)
buf += f'trailer\n<< /Size {len(objs)+1} /Root {catalog} 0 R /Info {info} 0 R >>\nstartxref\n{x}\n%%EOF\n'.encode()
out = os.path.join(out_dir, pdf_name); open(out, 'wb').write(buf)
print(f'{out}: {len(kids)} trang, {len(buf)/1048576:.1f} MB; video: {", ".join(f"trang {n}" for n in VIDEO) or "không"}')
if not VIDEO: os.rmdir(os.path.join(out_dir, 'video'))
