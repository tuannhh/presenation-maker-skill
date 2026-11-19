#!/usr/bin/env python3
"""Đóng gói deck thành 1 file HTML tự chứa (font + ảnh + logo + video nhúng base64), theo THEME.

Chạy:  <python của skill> build.py          (Windows: ~/.claude/skills/misa-html-deck/.venv/Scripts/python.exe
                                                 macOS/Linux: ~/.claude/skills/misa-html-deck/.venv/bin/python)
Cấu hình ở deck.json:
  title, output, theme (xem themes/themes.json), logo (đường dẫn hoặc null = không logo),
  parts [{name, color?}], videos {"<số trang>": "file.mp4"},
  tuỳ chọn ghi đè theme: bg, fonts {head, body, mono, script}, palette [...], colors {token: màu},
  motion ("calm" | "normal" | "lively" | "none" | {speed, blur, enter, big}), title_case ("upper"|"none"),
  shield (true/false: khiên chìm ở nền), logo_plate (true/false: nền trắng sau logo trên theme tối)
Thứ tự CSS: src/style.css → src/components.css → font + màu phần (sinh) → themes/<theme>.css → deck.json → src/custom.css
"""
import base64, html as _html, io, json, math, os, random, re, sys
from pathlib import Path
from PIL import Image
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

ROOT = Path(__file__).resolve().parent
SKILL = Path(os.environ.get("HTML_DECK_SKILL") or Path.home() / ".claude" / "skills" / "misa-html-deck")
SRC, AS, OUT = ROOT / "src", ROOT / "assets", ROOT / "dist"
OUT.mkdir(exist_ok=True)
CFG = json.loads((ROOT / "deck.json").read_text("utf-8"))

def first(rel, dirs):
    for d in dirs:
        p = Path(d) / rel
        if p.exists(): return p
    return None

THEME_DIRS = [ROOT / "themes", SKILL / "template" / "themes"]
FONT_DIRS = [ROOT / "assets" / "fonts", SKILL / "fonts"]
TPL_DIRS = [ROOT, SKILL / "template"]

# ---------- Theme ----------
REG = {}
for d in reversed(THEME_DIRS):
    f = Path(d) / "themes.json"
    if f.exists(): REG.update({k: v for k, v in json.loads(f.read_text("utf-8")).items() if not k.startswith("_")})
TNAME = CFG.get("theme", "misa-glass")
if TNAME not in REG: sys.exit(f"Không có theme '{TNAME}'. Có: {', '.join(REG)}")
T = REG[TNAME]
FONTSEL = {**T.get("fonts", {}), **(CFG.get("fonts") or {})}
BGKIND = CFG.get("bg") or T.get("bg", "blobs")
SHIELD = CFG.get("shield", T.get("shield", False))
PALETTE = CFG.get("palette") or T.get("palette") or ["#1557F0", "#E3263A", "#0B9A62", "#5A3FE6", "#DE8A00", "#0891B2"]
MOTION_PRESETS = {"calm": {"speed": 1.3}, "normal": {}, "lively": {"speed": 0.8}, "none": {"speed": 0.02, "enter": "cut", "big": "fade"}}
mcfg = CFG.get("motion")
MOTION = {**T.get("motion", {}), **(MOTION_PRESETS.get(mcfg, {}) if isinstance(mcfg, str) else (mcfg or {}))}
DARK = T.get("dark", False)

# ---------- Icon (Lucide-style, nét 2) — danh sách trong icons.json ----------
ICONS = json.loads(first("icons.json", TPL_DIRS).read_text("utf-8"))
def icon_svg(name):
    if name not in ICONS: sys.exit(f"Thiếu icon: {name} (thêm path SVG 24×24 vào icons.json)")
    return f'<svg class="i" aria-hidden="true"><use href="#i-{name}"/></svg>'

def b64(data, mime): return f"data:{mime};base64," + base64.b64encode(data).decode()

def webp(path, max_side, q=80):
    im = Image.open(path)
    im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=q, method=6)
    return buf.getvalue()

def img_file(name):
    return next((AS / "img" / f"{name}.{e}" for e in ("png", "jpg", "jpeg", "webp") if (AS / "img" / f"{name}.{e}").exists()), None)

# ---------- Compose ----------
slides = (SRC / "slides.html").read_text("utf-8")
css = (SRC / "style.css").read_text("utf-8")
comp = first("src/components.css", TPL_DIRS)
css += "\n" + (comp.read_text("utf-8") if comp else "")
js = (SRC / "app.js").read_text("utf-8")
_img = (SRC / "img.js").read_text("utf-8")
assert "window.deck = {" in js
js = js.replace("window.deck = {", _img + "\nwindow.deck = {", 1)
notes = json.loads((SRC / "notes.json").read_text("utf-8")) if (SRC / "notes.json").exists() else []
SECS = re.findall(r'<section class="slide([^"]*)"([^>]*)>', slides)
n_slides = len(SECS)
if len(notes) != n_slides:
    print(f"  (ghi chú: {len(notes)} mục / {n_slides} trang — tự bù/cắt cho khớp)")
notes = (notes + [""] * n_slides)[:n_slides]
TOTAL_NUMBERED = sum(1 for cls, _ in SECS if "closing" not in cls)

# Màu phần: deck.json parts[k].color, không có thì lấy palette của theme
part_cfg = CFG.get("parts", [])
n_parts = max(len(part_cfg), max([int(m) for m in re.findall(r'data-p="(\d+)"', slides)] or [1]))
PCOL = [None] + [(part_cfg[k - 1].get("color") if k <= len(part_cfg) else None) or PALETTE[(k - 1) % len(PALETTE)] for k in range(1, n_parts + 1)]
parts = [None]
for k, p in enumerate(part_cfg, 1):
    idx = [i + 1 for i, (cls, attrs) in enumerate(SECS) if f'data-p="{k}"' in attrs and "cover" not in cls]
    parts.append({"n": p["name"], "c": PCOL[k], "from": min(idx) if idx else 0, "to": max(idx) if idx else 0})
part_css = ""
for k in range(1, n_parts + 1):
    c, c2 = PCOL[k], PCOL[k % n_parts + 1] if n_parts > 1 else PALETTE[1 % len(PALETTE)]
    part_css += (f'.slide[data-p="{k}"],.c-p{k}{{--c:{c};--cs:color-mix(in srgb,{c} 12%,transparent)}}'
                 f'#stage[data-p="{k}"]{{--b1:color-mix(in srgb,{c} 30%,var(--bg));--b2:color-mix(in srgb,{c2} 20%,var(--bg));--b3:color-mix(in srgb,{c} 16%,var(--bg))}}\n')

used_icons = sorted(set(re.findall(r"\[\[([a-z0-9-]+)\]\]", slides)))
slides = re.sub(r"\[\[([a-z0-9-]+)\]\]", lambda m: icon_svg(m.group(1)), slides)
sprite = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + "".join(
    f'<symbol id="i-{n}" viewBox="0 0 24 24">{ICONS[n]}</symbol>' for n in used_icons) + "</defs></svg>"

# Ảnh minh hoạ trong thẻ (data-im) — dùng lại qua CSS, không lặp base64
used_imgs = sorted(set(re.findall(r'data-im="([a-z0-9_-]+)"', slides)))
img_css, total_img = [], 0
for name in used_imgs:
    p = img_file(name)
    if not p: print(f"  ! thiếu ảnh assets/img/{name}.png — thẻ ảnh sẽ trống"); continue
    W_, H_ = Image.open(p).size
    data = webp(p, 900, 82); total_img += len(data)
    img_css.append(f'.im[data-im="{name}"]{{--r:{W_/H_:.4f}}}.im[data-im="{name}"] .imt{{background-image:url({b64(data, "image/webp")})}}')
slides = re.sub(r'(<div class="im[^"]*" data-im="[a-z0-9_-]+"[^>]*>)(</div>)', r'\1<i class="imt"></i>\2', slides)
# Ảnh chụp tràn khung (data-ph) — nền cover, nét hơn (1920px)
used_ph = sorted(set(re.findall(r'data-ph="([a-z0-9_-]+)"', slides)))
for name in used_ph:
    p = img_file(name)
    if not p: print(f"  ! thiếu ảnh assets/img/{name}.jpg — khung ảnh sẽ trống"); continue
    data = webp(p, 1920, 80); total_img += len(data)
    img_css.append(f'[data-ph="{name}"]{{background-image:url({b64(data, "image/webp")})}}')

# Logo (tuỳ chọn)
LOGO_PATH = CFG.get("logo", "assets/logo-misa.png")
logo = webp(ROOT / LOGO_PATH, 1300, 90) if LOGO_PATH and (ROOT / LOGO_PATH).exists() else None
if LOGO_PATH and not logo: print(f"  ! không thấy logo {LOGO_PATH} — bỏ logo")
if not logo:
    slides = re.sub(r'<div class="biglogo"[^>]*>\s*<img[^>]*\{\{LOGO\}\}[^>]*>\s*</div>', "", slides)
    slides = re.sub(r'<img[^>]*\{\{LOGO\}\}[^>]*>', "", slides)

js = (js.replace("{{NOTES_JSON}}", json.dumps(notes, ensure_ascii=False)).replace("{{TOTAL_NUMBERED}}", str(TOTAL_NUMBERED))
        .replace("{{PARTS_JSON}}", json.dumps(parts, ensure_ascii=False)).replace("{{MOTION_JSON}}", json.dumps(MOTION)))

# ---------- Nền ----------
def circuit_svg():
    rg = random.Random(11); W, H = 1920, 1080; base = []; pulses = []; pads = []
    def route(x, y, dx, dy, n):
        pts = [(x, y)]
        for k in range(n):
            if k % 2 == 0:
                L = rg.choice([70, 110, 150, 200, 260]); x, y = x + dx * L, y + dy * L
            else:
                d = rg.choice([30, 50, 70]) * rg.choice([-1, 1])
                if dx: x, y = x + dx * abs(d), y + d
                else: x, y = x + d, y + dy * abs(d)
            pts.append((x, y))
        return pts
    starts = [(0, rg.uniform(60, 1020), 1, 0) for _ in range(9)] + [(W, rg.uniform(60, 1020), -1, 0) for _ in range(9)]
    starts += [(rg.uniform(80, 1840), 0, 0, 1) for _ in range(5)] + [(rg.uniform(80, 1840), H, 0, -1) for _ in range(5)]
    for idx, (x, y, dx, dy) in enumerate(starts):
        pts = route(x, y, dx, dy, rg.choice([3, 4, 5]))
        d = "M" + " L".join(f"{a:.0f} {b:.0f}" for a, b in pts)
        base.append(f'<path d="{d}"/>')
        ex, ey = pts[-1]; pads.append(f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="5"/>')
        if rg.random() < .3:
            mx, my = pts[len(pts) // 2]; pads.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="3.5"/>')
        if idx in (0, 4, 9, 13, 18, 23):
            pulses.append(f'<path pathLength="1000" d="{d}" style="animation-duration:{rg.uniform(16,24):.1f}s;animation-delay:{-rg.uniform(0,20):.1f}s"/>')
    return (f'<svg class="circ" viewBox="0 0 {W} {H}" preserveAspectRatio="none">'
            f'<g class="cb">{"".join(base)}</g><g class="cp">{"".join(pads)}</g>'
            f'<g class="cg">{"".join(pulses)}</g><g class="cl">{"".join(pulses)}</g></svg>')

def waves_svg():
    def wave(y0, amp, cls):
        d = f"M0 {y0}"
        for i in range(8):  # 8 nửa chu kỳ × 480px = 3840px, lặp liền khi trượt 1920px
            x0 = i * 480; s = -1 if i % 2 == 0 else 1
            d += f" C{x0+160} {y0+s*amp} {x0+320} {y0+s*amp} {x0+480} {y0}"
        return f'<path class="{cls}" d="{d} L3840 420 L0 420 Z"/>'
    return f'<div class="waves"><svg viewBox="0 0 3840 420" preserveAspectRatio="none">{wave(170,60,"w3")}{wave(230,46,"w2")}{wave(300,36,"w1")}</svg></div>'

def stars_html():
    rg = random.Random(5)
    return '<div class="stars">' + "".join(
        f'<i style="left:{rg.uniform(0,1920):.0f}px;top:{rg.uniform(0,1080):.0f}px;animation-duration:{rg.uniform(2.5,6.5):.1f}s;animation-delay:{-rg.uniform(0,6):.1f}s;{"width:2px;height:2px;" if rg.random()<.6 else ""}"></i>'
        for _ in range(90)) + "</div>"

def confetti_html():
    rg = random.Random(3); out = []
    while len(out) < 26:
        x, y = rg.uniform(20, 1880), rg.uniform(20, 1040)
        if 360 < x < 1560 and 230 < y < 860 and rg.random() < .85: continue  # tránh vùng nội dung
        sz = rg.uniform(14, 30); k = PALETTE[len(out) % len(PALETTE)]; cls = rg.choice(["cc", "cr", "ct", "cs"])
        out.append(f'<i class="{cls}" style="--k:{k};background:{k};left:{x:.0f}px;top:{y:.0f}px;width:{sz:.0f}px;height:{sz:.0f}px;'
                   f'transform:rotate({rg.uniform(0,90):.0f}deg);animation-duration:{rg.uniform(6,11):.1f}s;animation-delay:{-rg.uniform(0,10):.1f}s"></i>')
    return '<div class="confetti">' + "".join(out) + "</div>"

LAYERS = {"circuit": circuit_svg, "dots": lambda: '<div class="dots"></div>', "grid": lambda: '<div class="gridl"></div>',
          "paper": lambda: '<div class="paper"></div>', "mesh": lambda: '<div class="grain"></div>', "waves": waves_svg,
          "stars": stars_html, "confetti": confetti_html, "blobs": lambda: "", "none": lambda: ""}
if BGKIND not in LAYERS: sys.exit(f"bg '{BGKIND}' không hợp lệ. Chọn: {', '.join(LAYERS)}")
SH = 'M410 60 L720 170 V430 C720 640 590 790 410 870 C230 790 100 640 100 430 V170 Z'
SH2 = 'M410 110 L672 203 V430 C672 610 562 738 410 808 C258 738 148 610 148 430 V203 Z'
rnd = random.Random(7)
ptc = "".join(f'<i style="left:{rnd.uniform(0,1920):.0f}px;animation-duration:{rnd.uniform(30,45):.1f}s;animation-delay:{-rnd.uniform(0,40):.1f}s;{"width:2px;height:2px;" if rnd.random()<.5 else ""}"></i>' for _ in range(10))
BG = (f'<div id="bg" class="bg-{BGKIND}"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div><div class="glow"></div>'
      f'{LAYERS[BGKIND]()}'
      + (f'<svg class="bshield" viewBox="0 0 820 920"><circle class="ring" cx="410" cy="450" r="400"/><circle class="ring r2" cx="410" cy="450" r="440"/>'
         f'<path class="o" d="{SH}"/><path class="o" d="{SH2}" style="opacity:.6"/><path class="flow" pathLength="1000" d="{SH}" style="stroke-dasharray:70 930"/>'
         f'<path d="M300 450 L385 535 L540 360" class="o" style="stroke-width:6;opacity:.7"/></svg>' if SHIELD else "")
      + (f'<div class="ptc">{ptc}</div>' if BGKIND == "circuit" else "") + '<div class="vig"></div></div>')

title = CFG["title"]
LOGO_DIV = '<div id="logo"><img src="{{LOGO}}" alt="logo"></div>' if logo else ""
html_body = f"""<div id="stage" data-p="1">
{BG}
{LOGO_DIV}
{slides}
<div id="foot"><div class="parts"></div><div class="pg"></div></div>
</div>
<div id="ov"></div><div id="jump"></div>
<div id="help"><kbd>→</kbd><kbd>Space</kbd> tiếp · <kbd>←</kbd> lùi · <kbd>F</kbd> toàn màn hình · <kbd>N</kbd> ghi chú · <kbd>G</kbd> mục lục · <kbd>E</kbd> sửa nội dung · gõ số + <kbd>Enter</kbd> nhảy trang</div>
<div id="ebar"><span class="dot"></span><b>Chế độ chỉnh sửa</b><span>Bấm chữ để sửa · rê chuột vào chữ/hình rồi kéo <kbd>✥</kbd> để di chuyển · kéo-thả hoặc Ctrl+V ảnh để chèn · <kbd>M</kbd> chọn cụm, phóng to, xoá · <kbd>←</kbd><kbd>→</kbd> đổi trang</span><span class="st">Có thay đổi chưa lưu</span><button class="mb" title="Chọn chữ / hình / thẻ để kéo di chuyển, phóng to-thu nhỏ hoặc xoá (phím M)">✥ Bố cục (M)</button><button class="fb" title="Đổi font chữ cho cả bài">Aa Font</button><button class="ad">🖼 Chèn ảnh</button><button class="sv">Lưu file (Ctrl+S)</button><button class="ex">Thoát (E)</button></div>
<div id="fmt" class="off"><div class="g"><button data-f="fs-" title="Chữ nhỏ hơn">A−</button><span class="fsv" title="Cỡ chữ">–</span><button data-f="fs+" title="Chữ to hơn">A+</button></div><div class="g"><button data-f="lh-" title="Giảm dãn dòng">↕−</button><span class="lhv" title="Dãn dòng">–</span><button data-f="lh+" title="Tăng dãn dòng">↕+</button></div><div class="g"><button data-f="br" title="Xuống dòng (Enter)">↵ Xuống dòng</button></div><div class="g"><select class="ffs" title="Font của khối chữ này"><option value="">Font: theo bài</option></select></div><div class="g"><button data-f="bold" title="In đậm (Ctrl+B)"><b>B</b></button><button data-f="italic" title="In nghiêng (Ctrl+I)"><i>I</i></button><button data-f="underline" title="Gạch chân (Ctrl+U)"><u>U</u></button></div><div class="g cl">{''.join(f'<button data-f="c" data-v="{c}" title="Màu nhấn" style="--sw:{c}"></button>' for c in PALETTE[:5])}<button data-f="c" data-v="var(--ink)" title="Màu chữ mặc định" style="--sw:var(--ink)"></button><button data-f="hl" title="Tô nền vàng nhấn mạnh" class="hlb">▇</button></div><div class="g"><button data-f="al" data-v="left" title="Căn trái"><svg viewBox="0 0 24 24"><path d="M3 6h18M3 10h12M3 14h18M3 18h12"/></svg></button><button data-f="al" data-v="center" title="Căn giữa"><svg viewBox="0 0 24 24"><path d="M3 6h18M6 10h12M3 14h18M6 18h12"/></svg></button><button data-f="al" data-v="right" title="Căn phải"><svg viewBox="0 0 24 24"><path d="M3 6h18M9 10h12M3 14h18M9 18h12"/></svg></button><button data-f="al" data-v="justify" title="Căn đều 2 bên"><svg viewBox="0 0 24 24"><path d="M3 6h18M3 10h18M3 14h18M3 18h18"/></svg></button></div><div class="g"><button data-f="up" title="VIẾT HOA">AA</button><button data-f="low" title="viết thường">aa</button><button data-f="none" title="Giữ nguyên như khi gõ">Aa</button></div><div class="g"><button data-f="undo" title="Hoàn tác (Ctrl+Z)">↶</button><button data-f="redo" title="Làm lại">↷</button><button data-f="clear" title="Xoá định dạng">⌫ Định dạng</button></div><span class="tip">Bấm vào một đoạn chữ để định dạng</span></div><div id="ipan"><div class="g"><span class="l">Sáng / tối</span><input type="range" data-k="b" min="30" max="170" step="1"><span class="v" data-v="b"></span></div><div class="g"><span class="l">Bo góc</span><input type="range" data-k="rad" min="0" max="50" step="1"><span class="v" data-v="rad"></span></div><div class="g"><span class="l">Viền</span><input type="range" data-k="bw" min="0" max="24" step="1"><span class="v" data-v="bw"></span><button data-bc="#ffffff" title="Trắng" style="--sw:#ffffff"></button><button data-bc="#0B1A4A" title="Xanh đen" style="--sw:#0B1A4A"></button><button data-bc="#1557F0" title="Xanh dương" style="--sw:#1557F0"></button><button data-bc="#E3263A" title="Đỏ" style="--sw:#E3263A"></button><button data-bc="#DE8A00" title="Cam" style="--sw:#DE8A00"></button><label class="cp" title="Chọn màu viền khác"><input type="color" data-k="bc"></label></div><div class="g"><span class="l">Đổ bóng</span><input type="range" data-k="sh" min="0" max="100" step="1"><span class="v" data-v="sh"></span></div><div class="g"><span class="l">Xoay</span><input type="range" data-k="r" min="-180" max="180" step="1"><span class="v" data-v="r"></span></div><div class="g"><button data-ia="front" title="Đưa ảnh lên trên cùng">Lên trên</button><button data-ia="back" title="Đưa ảnh ra sau chữ">Ra sau chữ</button><button data-ia="reset" title="Bỏ xoay, sáng tối, viền… về mặc định">Đặt lại</button><button data-ia="del" class="del" title="Xoá ảnh (Delete)">Xoá</button></div></div><div id="bpan"><div class="g"><span class="l">Bố cục</span><span class="bn"></span></div><div class="g"><button data-ba="up" title="Chọn khối lớn hơn chứa khối này (Q · hoặc Alt+bấm)">⤴ Khối lớn hơn</button></div><div class="g"><button data-ba="small" title="Thu nhỏ (−)">−</button><span class="bsc v">100%</span><button data-ba="big" title="Phóng to (+)">+</button></div><div class="g"><button data-ba="reset" title="Đưa khối về vị trí, kích thước ban đầu">Về chỗ cũ</button><button data-ba="del" class="del" title="Xoá khối (Delete)">Xoá</button></div><div class="g"><button data-ba="restore" title="Hiện lại các khối đã xoá trên trang này">Hiện lại khối đã xoá</button><button data-ba="off" title="Quay lại sửa chữ (M)">✎ Sửa chữ</button></div></div><div id="fpan"><div class="g"><span class="l">Tiêu đề</span><span class="fo" data-r="head"></span></div><div class="g"><span class="l">Nội dung</span><span class="fo" data-r="body"></span></div><div class="g"><button class="fx" title="Đóng">✕</button></div></div><div id="toast"></div>
"""

# ---------- CSS theme + ghi đè ----------
tcss = first(f"{TNAME}.css", THEME_DIRS)
theme_css = tcss.read_text("utf-8") if tcss else ""
over = []
if CFG.get("colors"): over.append(":root{" + ";".join(f"--{k.lstrip('-')}:{v}" for k, v in CFG["colors"].items()) + "}")
if CFG.get("title_case"): over.append(f":root{{--tt:{'uppercase' if CFG['title_case'] == 'upper' else 'none'}}}")
if logo and T.get("logo_plate") and CFG.get("logo_plate", True):
    over.append("#logo img{background:#fff;border-radius:14px;padding:8px 14px;box-sizing:border-box}"
                ".biglogo img{background:#fff;border-radius:34px;padding:26px 40px;box-sizing:border-box;box-shadow:0 30px 60px -30px rgba(0,0,0,.6)}")
custom = SRC / "custom.css"

# ---------- Font: chọn theo theme, cắt theo đúng ký tự dùng ----------
FREG = json.loads(first("fonts.json", FONT_DIRS).read_text("utf-8"))
text_for_glyphs = re.sub(r"<[^>]+>", " ", html_body) + js + css + theme_css + "".join(notes) + title
text_for_glyphs = _html.unescape(text_for_glyphs)
USED = set(_html.unescape(re.sub(r"<[^>]+>", " ", html_body)) + title)
chars = set(text_for_glyphs) | set("0123456789.,:;!?%+-–—…“”‘’\"'()/·→←▶◀ ") | set("абвгдеёжзийклмнопрстуфхцчшщъыьэюяіАВЕКМНОРСТХ")
chars |= set(chr(c) for c in range(0x20, 0x7F))
unicodes = sorted(ord(c) for c in chars if ord(c) >= 0x20)

def subset_font(path, label, axes=None):
    f = TTFont(path, lazy=False)
    if axes and "fvar" in f:
        have = {a.axisTag: (a.minValue, a.maxValue) for a in f["fvar"].axes}
        lim = {k: (v if isinstance(v, (int, float)) else (max(v[0], have[k][0]), min(v[1], have[k][1]))) for k, v in axes.items() if k in have}
        f = instancer.instantiateVariableFont(f, lim)
        b = io.BytesIO(); f.save(b); b.seek(0); f = TTFont(b, lazy=False)
    cmap = f.getBestCmap()
    missing = [chr(u) for u in unicodes if u not in cmap and u > 0x7F]
    opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["*"]; opts.name_IDs = ["*"]; opts.notdef_outline = True
    sub = subset.Subsetter(opts); sub.populate(unicodes=unicodes); sub.subset(f)
    buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
    miss = [c for c in missing if c in USED and c not in "↕↵↶↷⌫▇▶◀🖼✕←→✎✥⤴"]  # chỉ báo ký tự có trên trang (bỏ qua ký tự giao diện/dự phòng)
    print(f"  {label}: {len(buf.getvalue())//1024} KB" + (f"  (thiếu {len(miss)} ký tự: {''.join(miss[:30])})" if miss else ""))
    return buf.getvalue()

import logging; logging.getLogger("fontTools").setLevel(logging.ERROR)
print(f"Theme: {TNAME} · nền: {BGKIND} · font: " + ", ".join(f"{k}={v}" for k, v in FONTSEL.items()))
face_css, done = [], set()
# mono/script chỉ nhúng khi trang có dùng (class code/mono/script hoặc var(--mono)/var(--script))
NEED = {"head": True, "body": True,
        "mono": bool(re.search(r'class="[^"]*\b(code|mono)\b|var\(--mono\)', slides)),
        "script": bool(re.search(r'class="[^"]*\bscript\b|var\(--script\)', slides))}
def embed_font(key):
    if key in done: return
    if key not in FREG: sys.exit(f"Font '{key}' không có trong fonts.json")
    done.add(key); spec = FREG[key]
    for style, files in (("normal", spec["files"]), ("italic", spec.get("italic", []))):
        for fn, w in files:
            p = first(fn, FONT_DIRS)
            if not p: sys.exit(f"Thiếu file font {fn} (đặt vào {SKILL / 'fonts'})")
            data = subset_font(p, f"{spec['family']} {w}{' italic' if style == 'italic' else ''}", spec.get("axes"))
            face_css.append(f'@font-face{{font-family:"{spec["family"]}";src:url({b64(data, "font/woff2")}) format("woff2");font-weight:{w};font-style:{style};font-display:block}}')
for role, key in FONTSEL.items():
    if key and NEED.get(role, True): embed_font(key)
# Bộ đổi font trong chế độ sửa (nút "Aa Font"): nhúng sẵn các font cho người dùng chọn.
# deck.json "font_picker": [khoá fonts.json…] để đổi danh sách, false để tắt (file nhẹ hơn ~0,5 MB).
DEF_PICK = ["inter", "montserrat", "barlow", "roboto", "google-sans", "open-sans"]
PICK = CFG.get("font_picker", DEF_PICK)
PICK = [k for k in (PICK or []) if k in FREG]
if PICK: print("Font cho người dùng chọn: " + ", ".join(FREG[k]["family"] for k in PICK))
for key in PICK: embed_font(key)
fam = lambda k: f'"{FREG[k]["family"]}"' if k and k in FREG else None
head, body = fam(FONTSEL.get("head")) or '"Inter"', fam(FONTSEL.get("body")) or '"Inter"'
font_vars = (f':root{{--gs:{head},{body},system-ui,sans-serif;--in:{body},system-ui,sans-serif;'
             f'--mono:{fam(FONTSEL.get("mono")) or "ui-monospace"},Consolas,monospace;--script:{fam(FONTSEL.get("script")) or head},cursive}}')
js = js.replace("{{FONTS_JSON}}", json.dumps({"choices": [FREG[k]["family"] for k in PICK],
                                              "head": head.strip('"'), "body": body.strip('"')}, ensure_ascii=False))

css_all = "\n".join([css, "\n".join(face_css), font_vars, part_css, f"/* theme: {TNAME} */", theme_css, "\n".join(over),
                     custom.read_text("utf-8") if custom.exists() else "", "".join(img_css)])
# Chặn text-wrap:balance (theme / custom.css): nó chia chữ thành các dòng bằng nhau, dòng trên bị hụt
# mà người sửa chữ không kéo từ lên được. Đổi thành pretty (lấp đầy dòng, chỉ tránh từ mồ côi).
_n_bal = len(re.findall(r"text-wrap(-style)?\s*:\s*balance", re.sub(r"/\*.*?\*/", "", css_all, flags=re.S)))
if _n_bal:
    css_all = re.sub(r"text-wrap(-style)?\s*:\s*balance", r"text-wrap\1:pretty", css_all)
    print(f"  ! {_n_bal} chỗ text-wrap:balance trong theme/custom.css — đã đổi thành pretty (ngắt dòng cố ý thì dùng <br>)")

# Video nhúng sẵn: số trang -> file đã nén
VMAP = {int(k): v for k, v in CFG.get("videos", {}).items()}
VIDS = "".join(f'<script type="application/octet-stream" id="dv-{n}">{base64.b64encode((AS/"video"/f).read_bytes()).decode()}</script>\n' for n, f in VMAP.items() if (AS/"video"/f).exists())
for n, f in VMAP.items():
    if not (AS / "video" / f).exists(): print(f"  ! thiếu video assets/video/{f} (trang {n})")
if VMAP: print("Video nhúng:", {n: f"{(AS/'video'/f).stat().st_size/1048576:.1f} MB" for n, f in VMAP.items() if (AS/'video'/f).exists()})
html = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>{css_all}</style>
</head><body class="theme-{TNAME}{' dark' if DARK else ''}">
{sprite}
{html_body}
<div id="vfs"></div>
<script id="deck-edits" type="application/json">{{}}</script>
{VIDS}
<script>{js}</script>
</body></html>"""
if logo: html = html.replace("{{LOGO}}", b64(logo, "image/webp"))
left = re.findall(r"\{\{[A-Z_]+\}\}", html)
assert not left, left

out = OUT / CFG.get("output", "deck.html")
out.write_text(html, "utf-8")
print(f"Trang: {n_slides} ({TOTAL_NUMBERED} đánh số) · Ảnh: {len(used_imgs)} minh hoạ + {len(used_ph)} ảnh chụp, {total_img//1024} KB · "
      f"Logo {len(logo)//1024 if logo else 0} KB · Icon: {len(used_icons)}")
print(f"=> {out}  ({out.stat().st_size/1024/1024:.2f} MB)")
