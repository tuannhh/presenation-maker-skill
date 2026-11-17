# Bố cục v2 (components.css) + cấu hình deck.json

Mẫu chạy được: `reference/showcase.html` (18 trang). Mọi bố cục ở đây tự đổi màu/font theo theme. Bố cục gốc (thẻ lưới, video, slot, bộ đếm, khiên…) xem `patterns.md`.

## Màu và chữ tiện ích

- **Màu theo phần**: `c-p1 … c-p6` trên bất kỳ khối nào → đặt `--c` cho khối đó (icon, chip, viền, số). `.hl` = chữ nhấn màu theo `data-p` của trang. Màu cố định có nghĩa: `c-blue c-red c-green c-violet c-amber`.
- `.eyebrow` (nhãn nhỏ HOA giãn chữ, màu `--c`), `.note` (hộp ghi chú viền trái), `.divider`, `.tc` / `.tr` (căn giữa/phải), `.mono` (font code), `.script` (chữ viết tay của theme, ví dụ luxury-gold).

## Hiệu ứng

`data-a` (kiểu) · `data-d` (trễ ms) · `data-t` (thời lượng ms). Tốc độ chung nhân với `motion.speed` của theme.

| Nhóm | Kiểu |
|---|---|
| Vào cơ bản | `up down left right fade pop zoom flip` |
| Mới | `rise` (lên xa, mềm) · `slam` (đập mạnh, cho số/tiêu đề lớn) · `tilt` (nghiêng 3D) · `blur` (mờ → rõ) · `wipe` (quét từ trái) · `spin` (xoay vào) |
| Đặc biệt | `grow` (thanh ngang, `.t-bar`, `.hb-f`, `.tl-line`) · `bar` (cột mọc từ đáy) · `mask` (băng chữ) · `draw` (nét SVG) · `ring` (vòng tròn %) |

**Xuất hiện lần lượt**: đặt trên khối cha thay vì ghi `data-a/data-d` cho từng con:
```html
<div class="agenda" data-stagger="110" data-d0="350" data-sa="up">…con…</div>
```
`data-stagger` = khoảng cách giữa các con (ms), `data-d0` = trễ của con đầu, `data-sa` = kiểu (mặc định `up`). Con nào đã có `data-a`/`data-d` thì giữ nguyên.

**Số đếm**: `<span data-count="4.7" data-dec="1">4,7</span>` (định dạng vi-VN, `data-dec` = số chữ số thập phân). **Bộ đếm thời gian thực**: `<b data-live="14e9">0</b>` (giá trị = số lượng mỗi ngày).

⚠ Không đặt CSS `opacity` trên phần tử có `data-a` (fade ghi đè). Cần mờ thì dùng `fill-opacity`/rgba.

## Trang đặc biệt (class trên `<section>`)

| Class | Dùng cho | Nội dung |
|---|---|---|
| `cover` | bìa | `.biglogo`, `.ck` (nhãn), `h1.ttl` (dòng `.g` là gradient), `.sub`, `.by`, `.orb` trang trí |
| `sect` | trang phần | `.wm` (số chìm), `.num-badge`, `.stitle`, `.ssub`, `.toc .ti` hoặc `.im` |
| `statement` | 1 câu thông điệp lớn giữa trang | `.st-k` (eyebrow), `.st-big`, `.st-sub` |
| `split` (+`rev` đảo bên) | ảnh tràn nửa trái + nội dung | `.sp-media.ph[data-ph]`, `.sp-body` |
| `thanks closing` | cảm ơn / Q&A | `.th-big`, `.th-sub`, `.th-contact` (chip), `.qa-mark` |
| `cover closing` | trang kết có logo + khiên (misa-glass) | xem `patterns.md` |

Các trang `cover`, `sect`, `statement`, `thanks` dùng kiểu chuyển trang "lớn" (`motion.big`).

## Bố cục nội dung

**Agenda**
```html
<div class="agenda" data-stagger="110" data-d0="350">
  <div class="ag-item c-p1"><div class="ag-n">01</div><div><div class="ag-t">Tiêu đề</div><div class="ag-d">Mô tả ngắn</div></div></div>
</div>
```
Thêm `.on` (mục đang nói) / `.dim` (mục khác) để dùng lại agenda làm trang chuyển phần.

**Số lớn**: `<div class="hero-num c-p2" data-a="slam">68<small>%</small></div>`

**KPI** (`--n` = số cột):
```html
<div class="kpis" style="--n:4" data-stagger="120" data-d0="400">
  <div class="kpi c-p1"><div class="kpi-l">Doanh thu</div><div class="kpi-v"><span data-count="1250">1.250</span><small>tỷ</small></div>
    <div class="kpi-d up">[[arrow-up]] 32%</div><div class="kpi-n">Vượt kế hoạch 8%</div></div>
</div>
```
`.kpi-d.down` cho giảm.

**Vòng tròn %**
```html
<div class="ring" style="--v:86;--sz:340px;--sw:14"><svg viewBox="0 0 120 120"><circle class="trk" cx="60" cy="60" r="52"/>
  <circle class="val" cx="60" cy="60" r="52" pathLength="100" data-a="ring" data-d="700"/></svg>
  <div class="ring-n"><div><span data-count="86">86</span>%<small>hoàn thành</small></div></div></div>
```

**Thanh ngang** (`--lw` = độ rộng nhãn; `.hi` = thanh nổi bật):
```html
<div class="hbars" style="--lw:280px">
  <div class="hb hi"><div class="hb-l">Nhãn</div><div class="hb-t"><div class="hb-f" data-a="grow" data-d="500" style="--v:72%"></div></div><div class="hb-v">72%</div></div>
</div>
```

**Cột** (`.dim` = cột phụ):
```html
<div class="cols-wrap"><div class="cols">
  <div class="colw dim"><div class="colv">240</div><div class="colb" data-a="bar" data-d="450" style="height:48%"></div><div class="coll">Q1</div></div>
</div></div>
```

**Đường** (SVG tự vẽ, viewBox 700×400): `svg.lchart` gồm `line.gl` (lưới), `path.ar` (vùng tô), `path.ln2` (đường so sánh, nét đứt), `path.ln` (`data-a="draw"`), `circle.pt` (`data-a="pop"`), `text.tv` (giá trị), `text` (nhãn trục). Xem trang 7 của showcase.

**Timeline ngang** (mốc so le trên/dưới):
```html
<div class="tl"><span class="tl-line" data-a="grow" data-d="300" data-t="1800"></span>
  <div class="tl-item" data-a="up" data-d="500"><div class="tl-top"><div class="tl-date">T2</div><div class="tl-t">Sự kiện</div></div><span class="tl-dot"></span><div class="tl-bot"></div></div>
  <div class="tl-item" data-a="up" data-d="750"><div class="tl-top"></div><span class="tl-dot"></span><div class="tl-bot"><div class="tl-date">T5</div><div class="tl-t">Sự kiện</div><div class="tl-d">Mô tả</div></div></div>
</div>
```

**Timeline dọc / roadmap** (`.done` = đã xong): `.vtl > .vtl-item > .vtl-date + .vtl-t + .vtl-d`.

**Quy trình bước**: `.proc > .pstep > .pn (số) + .pt (tên) + .pd (mô tả)`; mũi tên giữa các bước tự có.

**Trích dẫn**: `.quote > .qt-mark + .qt-text + .qt-by > .qt-av (chữ tắt hoặc <img>) + div > .qt-n + .qt-r`.

**Đội ngũ** (`--n` cột): `.team > .person.c-pN > .av + .pn (tên) + .pr (vai trò) + .pd`.

**Bảng giá** (`--n` cột; `.feat` = gói nổi bật):
```html
<div class="plans" style="--n:3">
  <div class="plan feat" data-a="up" data-d="480"><div class="plan-badge">Phổ biến</div><div class="plan-n">Tên gói</div>
    <div class="plan-p">6,5<small> triệu/năm</small></div><ul class="bul"><li>…</li></ul><div class="plan-cta">Đăng ký</div></div>
</div>
```

**Trước / sau**: `.ba > .ba-pane.ba-before + .ba-arrow + .ba-pane.ba-after`, mỗi pane có `.ba-h` + `ul.bul`.

**Ma trận 2×2 / SWOT**: `.mx > .mx-c.c-green > .mx-k (chữ chìm S/W/O/T) + .mx-h + ul.bul`.

**Checklist**: `.checks > .chk > span.bx [[check]] + span`; `.chk.no` cho mục gạch bỏ.

**Ảnh**: `<div class="ph" data-ph="ten_anh"><div class="cap">Chú thích</div></div>` (ảnh phủ kín khối, file `assets/img/ten_anh.jpg|png|webp`, nén 1920px). `.ph.duo` = ảnh đơn sắc nhuộm màu phần; `.ph.flat` = không bo góc. Lưới ảnh: `.photos` (1 lớn + 4 nhỏ) hoặc `.photos.even` (3 cột đều).

**Kim tự tháp**: `.pyr > .lv.c-pN` (đặt `style="width:…px"` tăng dần từ trên xuống).

**Khối mã**: `<pre class="code">` với `span.k` (từ khoá) `.s` (chuỗi) `.n` (số) `.c` (chú thích) `.f` (hàm).

## deck.json

```json
{
  "title": "Tiêu đề tab trình duyệt",
  "output": "Ten_file.html",
  "theme": "misa-glass",
  "logo": "assets/logo-misa.png",
  "parts": [{"name": "Phần 1"}, {"name": "Phần 2", "color": "#E3263A"}],
  "videos": {"5": "v1.mp4"},
  "palette": ["#...", "#..."],
  "fonts": {"head": "…", "body": "…", "mono": "…", "script": "…"},
  "bg": "circuit",
  "shield": true,
  "motion": "calm",
  "title_case": "upper",
  "colors": {"ink": "#0B1A4A"},
  "logo_plate": true
}
```

Chỉ `title`, `output`, `theme`, `parts` là cần; các khoá còn lại ghi đè theme (giải thích ở `themes.md`). `parts[].color` ghi đè màu một phần. `logo: null` = không logo.

## Thứ tự ưu tiên file

`src/style.css`, `src/app.js`, `src/img.js`, `src/slides.html` lấy từ thư mục dự án (`new_deck.sh` đã chép sẵn). Theme (`themes/`), font (`assets/fonts/` → `$SK/fonts/`), `src/components.css` và `icons.json` tìm ở dự án trước rồi mới tới skill. Muốn chỉnh CSS riêng cho 1 bài mà không đụng theme: tạo `src/custom.css` (nạp sau cùng).
