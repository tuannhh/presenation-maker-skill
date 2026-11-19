#!/usr/bin/env python3
"""Dựng PPTX sửa được từ dữ liệu capture_pptx.mjs.
python make_pptx.py <capture_dir> <deck.html> <out.pptx>

- Mỗi trang: ảnh nền (đứng yên) + ảnh từng khối có hiệu ứng + text box PowerPoint cho mọi khối chữ (sửa được).
- Hiệu ứng vào: mỗi khối (ảnh + chữ trong nó) xuất hiện tự động theo đúng thứ tự/độ trễ của HTML
  (up/rise → Float In, zoom/pop → Zoom, grow/draw → Wipe từ trái, bar → Wipe từ dưới, còn lại → Fade).
- Chuyển trang: prezi/zoomin → Fly Through, cube → Cube, flip → Flip, swirl → Vortex, stack → Uncover, parallax/slide → Push, fade → Fade.
- Video nhúng → video PowerPoint (bấm để phát). Ghi chú người nói → Notes.
- Font: chép font tĩnh đúng độ đậm vào <out>_fonts/ — cài các font này trước khi mở PPTX.
"""
import sys, os, re, json, base64, io, copy
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.oxml.ns import qn
from lxml import etree

cap, deck, out = sys.argv[1:4]
D = json.load(open(os.path.join(cap, 'pptx.json'), encoding='utf-8'))
H = open(deck, encoding='utf-8').read()
PX = 6350  # 1px của sân khấu 1920×1080 = 6350 EMU (slide 13,333 × 7,5 in)
E = lambda v: Emu(int(round(v * PX)))

prs = Presentation()
prs.slide_width, prs.slide_height = Emu(1920 * PX), Emu(1080 * PX)
blank = prs.slide_layouts[6]

# ---------- ghi chú người nói + video nhúng (lấy từ chính file HTML) ----------
m = re.search(r'const NOTES = (\[.*?\]);\n', H, re.S)
NOTES = json.loads(m.group(1)) if m else []
vids = {int(k): v for k, v in re.findall(r'<script type="application/octet-stream" id="dv-(\d+)">([^<]*)</script>', H) if v.strip()}
m = re.search(r'<script id="deck-edits" type="application/json">(.*?)</script>', H, re.S)
if m:
    ed = json.loads(m.group(1).replace('<\\/', '</') or '{}')
    for si, v in (ed.get('videos') or {}).items():
        if v is None: vids.pop(int(si) + 1, None)
        elif v.startswith('data:'): vids[int(si) + 1] = v.split(',', 1)[1]

# ---------- font: tên họ + độ đậm → tên font PowerPoint ----------
WNAME = {100: 'Thin', 200: 'ExtraLight', 300: 'Light', 500: 'Medium', 600: 'SemiBold', 800: 'ExtraBold', 900: 'Black'}
USED = set()
def font_of(fam, w):
    w = int(round(w / 100) * 100); w = max(100, min(900, w))
    USED.add((fam, w))
    if w in (400, 700): return fam, w == 700
    return f'{fam} {WNAME[w]}', False

def rgba(c):
    m = re.match(r'rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)', c or '')
    if m: return tuple(int(float(x)) for x in m.groups()[:3]), float(m.group(4)) if m.group(4) else 1.0
    m = re.match(r'#([0-9a-f]{6})', c or '', re.I)
    if m: h = m.group(1); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)), 1.0
    return (0, 0, 0), 1.0

def grad_fill(css):
    """linear-gradient(...) của chữ tô gradient → <a:gradFill> cho run PowerPoint."""
    if not css or 'linear-gradient' not in css: return None
    body = css[css.index('linear-gradient(') + 16:]
    parts, depth, cur = [], 0, ''
    for ch in body:
        if ch == '(': depth += 1
        elif ch == ')':
            if depth == 0: break
            depth -= 1
        if ch == ',' and depth == 0: parts.append(cur.strip()); cur = ''
        else: cur += ch
    parts.append(cur.strip())
    ang = 180.0
    m = re.match(r'(-?[\d.]+)deg$', parts[0]); TO = {'to right': 90, 'to left': 270, 'to bottom': 180, 'to top': 0}
    if m: ang = float(m.group(1)); parts = parts[1:]
    elif parts[0] in TO: ang = TO[parts[0]]; parts = parts[1:]
    stops = []
    for i, ptxt in enumerate(parts):
        mc = re.match(r'(rgba?\([^)]*\)|#[0-9a-fA-F]{3,8})\s*([\d.]+%)?', ptxt)
        if not mc: continue
        (cr, cg, cb), _ = rgba(mc.group(1))
        pos = float(mc.group(2)[:-1]) if mc.group(2) else (100.0 * i / max(1, len(parts) - 1))
        stops.append((pos, '%02X%02X%02X' % (cr, cg, cb)))
    if len(stops) < 2: return None
    gs = ''.join(f'<a:gs pos="{int(p * 1000)}"><a:srgbClr val="{c}"/></a:gs>' for p, c in stops)
    return etree.fromstring(f'<a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" rotWithShape="1"><a:gsLst>{gs}</a:gsLst>'
                            f'<a:lin ang="{int(((ang - 90) % 360) * 60000)}" scaled="0"/></a:gradFill>')

ALIGN = {'center': PP_ALIGN.CENTER, 'right': PP_ALIGN.RIGHT, 'end': PP_ALIGN.RIGHT, 'justify': PP_ALIGN.JUSTIFY}

def add_text(sl, t):
    b = t['box']; slack = 0 if t['nowrap'] else b['w'] * .03
    x, w = b['x'], b['w'] + slack
    if not t['nowrap'] and t['align'] == 'center': x -= slack / 2
    elif not t['nowrap'] and t['align'] in ('right', 'end'): x -= slack
    top = t['lineTop']; h = max(b['h'], t['lh'] * t['lines'])
    tb = sl.shapes.add_textbox(E(x), E(top), E(w), E(h))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = not t['nowrap']; tf.auto_size = MSO_AUTO_SIZE.NONE; tf.vertical_anchor = MSO_ANCHOR.TOP
    for pi, P in enumerate(t['paras']):
        para = P['runs']
        p = tf.paragraphs[0] if pi == 0 else tf.add_paragraph()
        p.alignment = ALIGN.get(t['align'], PP_ALIGN.LEFT)
        if P.get('ind', 0) > 1 and t['align'] in ('left', 'start', 'justify'): p._p.get_or_add_pPr().set('indent', str(int(P['ind'] * PX)))
        p.line_spacing = Pt(t['lh'] * .5); p.space_before = p.space_after = Pt(0)
        for r in para:
            if r.get('br'): p.add_line_break(); continue
            run = p.add_run(); run.text = r['t']
            f = run.font; name, bold = font_of(r['f'], r['fw'])
            f.name = name; f.bold = bold; f.italic = r['it']; f.size = Pt(r['fs'] * .5)
            if r['u']: f.underline = True
            (cr, cg, cb), a = rgba(r['c']); f.color.rgb = RGBColor(cr, cg, cb)
            rPr = run._r.get_or_add_rPr()
            gf = grad_fill(r.get('gr'))
            if gf is not None:
                sf = rPr.find(qn('a:solidFill')); sf.addprevious(gf); rPr.remove(sf); a = 1
            if a < .99:
                clr = rPr.find(qn('a:solidFill')).find(qn('a:srgbClr'))
                etree.SubElement(clr, qn('a:alpha')).set('val', str(int(a * 100000)))
            if abs(r['ls']) > .05: rPr.set('spc', str(int(round(r['ls'] * .5 * 100))))
            if r['tt'] == 'uppercase': rPr.set('cap', 'all')
            if r.get('sup'): rPr.set('baseline', '30000')
    return tb

# ---------- hiệu ứng vào (p:timing) ----------
NS = 'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
EFFECT = {'up': 'float', 'rise': 'float', 'slam': 'zoom', 'tilt': 'float', 'pop': 'zoom', 'zoom': 'zoom', 'spin': 'zoom', 'grow': 'wipeL',
          'draw': 'wipeL', 'ring': 'wipeL', 'bar': 'wipeB', 'blur': 'fade', 'fade': 'fade', 'left': 'wipeL', 'right': 'fade', 'wipe': 'wipeL'}
class Ids:
    def __init__(s): s.n = 2
    def __call__(s): s.n += 1; return s.n

def effect_xml(ids, spid, kind, delay, dur, first):
    node = 'afterEffect' if first else 'withEffect'
    tgt = f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
    setv = (f'<p:set><p:cBhvr><p:cTn id="{ids()}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>{tgt}'
            '<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>')
    fade = f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{ids()}" dur="{dur}"/>{tgt}</p:cBhvr></p:animEffect>'
    def anim(attr, a, b):
        return (f'<p:anim calcmode="lin" valueType="num"><p:cBhvr additive="base"><p:cTn id="{ids()}" dur="{dur}" fill="hold"/>{tgt}'
                f'<p:attrNameLst><p:attrName>{attr}</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst><p:tav tm="0"><p:val><p:strVal val="{a}"/></p:val></p:tav>'
                f'<p:tav tm="100000"><p:val><p:strVal val="{b}"/></p:val></p:tav></p:tavLst></p:anim>')
    if kind == 'float':  pid, sub, body = 42, 0, setv + fade + anim('ppt_x', '#ppt_x', '#ppt_x') + anim('ppt_y', '#ppt_y+.1', '#ppt_y')
    elif kind == 'zoom': pid, sub, body = 53, 16, setv + anim('ppt_w', '0', '#ppt_w') + anim('ppt_h', '0', '#ppt_h') + fade
    elif kind == 'wipeL': pid, sub, body = 22, 8, setv + f'<p:animEffect transition="in" filter="wipe(left)"><p:cBhvr><p:cTn id="{ids()}" dur="{dur}"/>{tgt}</p:cBhvr></p:animEffect>'
    elif kind == 'wipeB': pid, sub, body = 22, 4, setv + f'<p:animEffect transition="in" filter="wipe(up)"><p:cBhvr><p:cTn id="{ids()}" dur="{dur}"/>{tgt}</p:cBhvr></p:animEffect>'
    else: pid, sub, body = 10, 0, setv + fade
    return (f'<p:par><p:cTn id="{ids()}" presetID="{pid}" presetClass="entr" presetSubtype="{sub}" fill="hold" grpId="0" nodeType="{node}">'
            f'<p:stCondLst><p:cond delay="{int(delay)}"/></p:stCondLst><p:childTnLst>{body}</p:childTnLst></p:cTn></p:par>')

def add_timing(sl, items, text_ids, old=None):
    # old = p:timing python-pptx tạo cho video (nút phát media) → gộp vào cây hiệu ứng, vì mỗi trang chỉ được có 1 p:timing
    if not items:
        if old is not None: sl._element.append(old)
        return
    ids = Ids()
    effs = ''.join(effect_xml(ids, sp, k, dl, du, i == 0) for i, (sp, k, dl, du) in enumerate(sorted(items, key=lambda x: x[2])))
    bld = ''.join(f'<p:bldP spid="{s}" grpId="0"/>' for s in text_ids)
    xml = (f'<p:timing {NS}><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
           '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
           f'<p:par><p:cTn id="{ids()}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>'
           f'<p:par><p:cTn id="{ids()}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>{effs}</p:childTnLst></p:cTn></p:par>'
           '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn>'
           '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
           '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
           f'</p:childTnLst></p:cTn></p:par></p:tnLst>{"<p:bldLst>" + bld + "</p:bldLst>" if bld else ""}</p:timing>')
    tm = etree.fromstring(xml)
    if old is not None:
        root = tm.find('.//' + qn('p:cTn')).find(qn('p:childTnLst'))
        for v in old.iter(qn('p:video')):
            for c in v.iter(qn('p:cTn')): c.set('id', str(ids()))
            root.append(v)
    sl._element.append(tm)

# ---------- chuyển trang ----------
P14 = 'xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main"'
def tr_xml(name, dur):
    base = {'fade': '<p:fade/>', 'slide': '<p:push dir="l"/>', 'parallax': '<p:push dir="l"/>', 'rise': '<p:push dir="u"/>',
            'zoom': '<p:zoom/>', 'circle': '<p:circle/>', 'wipe': '<p:wipe dir="r"/>', 'stack': '<p:pull dir="l"/>'}
    p14 = {'prezi': '<p14:flythrough/>', 'zoomin': '<p14:flythrough/>', 'cube': '<p14:prism/>', 'flip': '<p14:flip dir="l"/>', 'swirl': '<p14:vortex dir="r"/>'}
    if name == 'cut': return None
    if name in p14:
        return (f'<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" {NS} {P14}>'
                f'<mc:Choice Requires="p14"><p:transition spd="slow" p14:dur="{dur}">{p14[name]}</p:transition></mc:Choice>'
                '<mc:Fallback><p:transition spd="slow"><p:fade/></p:transition></mc:Fallback></mc:AlternateContent>')
    return (f'<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" {NS} {P14}>'
            f'<mc:Choice Requires="p14"><p:transition spd="slow" p14:dur="{dur}">{base.get(name, base["fade"])}</p:transition></mc:Choice>'
            f'<mc:Fallback><p:transition spd="slow">{base.get(name, base["fade"])}</p:transition></mc:Fallback></mc:AlternateContent>')

tmp_media = []
for s in D['slides']:
    sl = prs.slides.add_slide(blank)
    pre = os.path.join(cap, s['pre'])
    sl.shapes.add_picture(pre + '-bg.jpg', 0, 0, prs.slide_width, prs.slide_height).name = 'Nền'
    items, text_ids, gshape = [], [], {}
    for g in s['groups']:
        if g.get('skip'): continue
        c = g['clip']
        pic = sl.shapes.add_picture(f"{pre}-g{g['i']:02d}.png", E(c['x']), E(c['y']), E(c['w']), E(c['h']))
        pic.name = f"Khối {g['i'] + 1}"
        gshape[g['i']] = g
        items.append((pic.shape_id, EFFECT.get(g['kind'], 'fade'), g['delay'], int(min(1200, max(300, g['dur'])))))
    for t in s['texts']:
        tb = add_text(sl, t)
        g = gshape.get(t['g'])
        if g is not None:
            items.append((tb.shape_id, EFFECT.get(g['kind'], 'fade'), g['delay'], int(min(1200, max(300, g['dur'])))))
            text_ids.append(tb.shape_id)
    if s.get('video') and s['k'] in vids:
        v = s['video']; mp4 = os.path.join(cap, f"{s['pre']}-video.mp4")
        open(mp4, 'wb').write(base64.b64decode(vids[s['k']]))
        poster = os.path.join(cap, f"{s['pre']}-poster.jpg")
        if os.path.exists(poster): os.remove(poster)
        # ảnh bìa video: khung hình ở giây 1 (ffmpeg); không có ffmpeg thì cắt từ ảnh nền
        import shutil, subprocess
        ff = os.environ.get('FFMPEG') or shutil.which('ffmpeg')
        if ff: subprocess.run([ff, '-y', '-loglevel', 'error', '-ss', '1', '-i', mp4, '-frames:v', '1', '-q:v', '3', poster])
        if not os.path.exists(poster):
            from PIL import Image
            Image.open(pre + '-bg.jpg').crop((int(v['x']), int(v['y']), int(v['x'] + v['w']), int(v['y'] + v['h']))).save(poster, quality=90)
        sl.shapes.add_movie(mp4, E(v['x']), E(v['y']), E(v['w']), E(v['h']), poster_frame_image=poster, mime_type='video/mp4')
    # chuyển trang (đặt trước p:timing)
    old = sl._element.find(qn('p:timing'))
    if old is not None: sl._element.remove(old)
    x = tr_xml(s.get('tr') or 'fade', 1400 if s.get('tr') in ('prezi', 'zoomin', 'cube') else 900)
    if x is not None and s['k'] > 1: sl._element.append(etree.fromstring(x))
    add_timing(sl, items, text_ids, old)
    note = NOTES[s['k'] - 1] if s['k'] - 1 < len(NOTES) else ''
    if note:
        sl.notes_slide.notes_text_frame.text = re.sub(r'<[^>]+>', '', note) if isinstance(note, str) else str(note)
prs.core_properties.title = re.search(r'<title>(.*?)</title>', H).group(1) if '<title>' in H else ''
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
prs.save(out)

# ---------- font tĩnh đúng độ đậm ----------
SK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fdir = os.path.splitext(out)[0] + '_fonts'; os.makedirs(fdir, exist_ok=True)
FREG = json.load(open(os.path.join(SK, 'fonts', 'fonts.json'), encoding='utf-8'))
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
made = []
for fam, w in sorted(USED):
    spec = next((v for k, v in FREG.items() if k != '_doc' and v['family'] == fam), None)
    if not spec: continue
    files = spec['files']
    static = next((f for f, ww in files if str(ww) == str(w)), None)
    dst = os.path.join(fdir, f"{fam.replace(' ', '')}-{WNAME.get(w, 'Bold' if w == 700 else 'Regular')}.ttf")
    try:
        if static: import shutil; shutil.copy(os.path.join(SK, 'fonts', static), dst)
        else:
            vf = next((f for f, ww in files if isinstance(ww, str) and ' ' in ww), None)
            if not vf: continue
            f = TTFont(os.path.join(SK, 'fonts', vf))
            pin = {'wght': w}
            for a in f['fvar'].axes:
                if a.axisTag != 'wght': pin[a.axisTag] = 100 if a.axisTag == 'wdth' else a.defaultValue
            inst = instancer.instantiateVariableFont(f, pin, updateFontNames=True)
            inst.save(dst)
        made.append(os.path.basename(dst))
    except Exception as e:
        print('  ! không tạo được font', fam, w, e)
n_txt = sum(len(s['texts']) for s in D['slides']); n_g = sum(len(s['groups']) for s in D['slides'])
print(f"=> {out}  ({os.path.getsize(out) / 1048576:.1f} MB) · {len(D['slides'])} trang · {n_txt} khối chữ sửa được · {n_g} khối có hiệu ứng")
print(f"Font cần cài trước khi mở (đã chép vào {fdir}): " + ', '.join(made))
