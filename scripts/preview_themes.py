#!/usr/bin/env python3
"""Build bộ trang mẫu (reference/showcase.html hoặc slides của một dự án) ra MỌI theme để so sánh / cho người dùng chọn.

  python preview_themes.py <thư-mục-ra> [--slides <slides.html>] [--themes a,b,c] [--logo <ảnh>|none]

Kết quả: <thư-mục-ra>/<theme>.html cho từng theme + index.html (lưới xem trước, bấm để mở từng bản).
"""
import argparse, json, shutil, subprocess, sys, tempfile
from pathlib import Path

SK = Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("--slides", default=str(SK / "reference" / "showcase.html"))
ap.add_argument("--themes", default="")
ap.add_argument("--logo", default="assets/logo-misa.png")
a = ap.parse_args()
out = Path(a.out).resolve(); out.mkdir(parents=True, exist_ok=True)
reg = {k: v for k, v in json.loads((SK / "template" / "themes" / "themes.json").read_text("utf-8")).items() if not k.startswith("_")}
names = [t for t in a.themes.split(",") if t] or list(reg)
cards = []
with tempfile.TemporaryDirectory() as tmp:
    proj = Path(tmp) / "p"
    shutil.copytree(SK / "template", proj)
    shutil.copy(a.slides, proj / "src" / "slides.html")
    (proj / "src" / "notes.json").write_text("[]", "utf-8")
    for t in names:
        cfg = json.loads((proj / "deck.json").read_text("utf-8"))
        cfg.update(theme=t, output=f"{t}.html", title=f"Theme · {t}", logo=None if a.logo == "none" else a.logo)
        cfg["parts"] = [{"name": n} for n in ("Kết quả", "Tăng trưởng", "Chiến lược", "Kế hoạch")]
        (proj / "deck.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), "utf-8")
        r = subprocess.run([sys.executable, str(proj / "build.py")], capture_output=True, text=True, encoding="utf-8")
        if r.returncode: print(f"[{t}] LỖI:\n{r.stdout}\n{r.stderr}"); continue
        shutil.copy(proj / "dist" / f"{t}.html", out / f"{t}.html")
        print(f"[{t}] ok")
        cards.append(f'<a class="c" href="{t}.html" target="_blank"><div class="fr"><iframe src="{t}.html#1" loading="lazy" tabindex="-1"></iframe></div>'
                     f'<b>{t}</b><span>{reg[t].get("label", "")}</span></a>')
idx = """<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Chọn theme</title><style>
body{margin:0;padding:40px;font:15px/1.4 system-ui,sans-serif;background:#f3f4f7;color:#111}h1{margin:0 0 6px}p{margin:0 0 28px;color:#555}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:26px}
.c{display:block;background:#fff;border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;box-shadow:0 2px 10px rgba(0,0,0,.08)}
.c:hover{box-shadow:0 8px 28px rgba(0,0,0,.18)}.fr{position:relative;aspect-ratio:16/9;overflow:hidden;background:#ddd}
.fr iframe{position:absolute;left:0;top:0;width:1920px;height:1080px;border:0;transform-origin:0 0;pointer-events:none}
.c b{display:block;padding:14px 16px 2px;font-size:17px}.c span{display:block;padding:0 16px 16px;color:#666}
</style></head><body><h1>Chọn phong cách</h1><p>Bấm một ô để mở bản đầy đủ (→ / Space để chuyển trang, G để xem mục lục).</p><div class="g">""" + "".join(cards) + """</div>
<script>const fit=()=>document.querySelectorAll('.fr').forEach(f=>{f.firstChild.style.transform=`scale(${f.clientWidth/1920})`});addEventListener('resize',fit);fit();</script></body></html>"""
(out / "index.html").write_text(idx, "utf-8")
print(f"=> {out / 'index.html'}")
