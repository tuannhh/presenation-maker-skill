# Bố cục v2 + v3 (components.css) + cấu hình deck.json

Mẫu chạy được: `reference/showcase.html` (33 trang; bố cục v3 ở trang 18–32). Mọi bố cục ở đây tự đổi màu/font theo theme. Bố cục gốc (thẻ lưới, video, slot, bộ đếm, khiên…) xem `patterns.md`.

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

Các trang `cover`, `sect`, `statement`, `thanks` dùng kiểu chuyển trang "lớn" (`motion.big`). Đặt kiểu riêng cho một trang bằng `data-tr` trên `<section>` (vd `data-tr="prezi"`, `cube`, `flip`, `zoomin`, `stack`, `parallax`, `swirl`); danh sách đủ ở `themes.md`.

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

## Bố cục v3: biểu đồ, sơ đồ, bố cục mới

Mẫu chạy được: trang 18–32 của `reference/showcase.html`. Số liệu ghi bằng biến CSS ngay trên phần tử (`style="--v:42"`), không cần JS. Màu chuỗi dữ liệu: `c-p1 … c-p6` (deck có ít phần hơn thì tự lấy màu tên của theme: xanh, đỏ, lục, tím, cam, lam ngọc). Khối nào cần dáng thẻ của theme (kính, viền đậm, gạch đầu báo…) thì thêm class `card`.

**Chú giải dùng chung**: `<div class="lgd"><span class="c-p1">Kế toán <b>46%</b></span>…</div>`. Ô màu tự vẽ theo `--c`; `.lgd.v` = xếp dọc, số căn phải.

### Biểu đồ

**Donut nhiều phần** (`--v` = phần trăm của đoạn, `--o` = tổng các đoạn đứng trước; `--sz` cỡ, `--sw` độ dày):
```html
<div class="dn" style="--sz:340px;--sw:20">
  <svg viewBox="0 0 120 120"><circle class="dn-trk" cx="60" cy="60" r="50"/>
    <circle class="dn-seg c-p1" style="--v:46;--o:0" cx="60" cy="60" r="50" pathLength="100" data-a="ring" data-d="500"/>
    <circle class="dn-seg c-p2" style="--v:27;--o:46" cx="60" cy="60" r="50" pathLength="100" data-a="ring" data-d="750"/></svg>
  <div class="dn-c"><b>1.250</b><small>tỷ đồng</small></div>
</div>
```
Mỗi đoạn mọc lần lượt nhờ `data-a="ring"` + trễ tăng dần.

**Thanh chồng 100%** (mỗi `<i>` có `--v`; đoạn dưới ~8% thì để trống chữ):
```html
<div class="sb" style="--lw:200px">
  <div class="sb-r"><div class="sb-l">Miền Bắc<small>520 tỷ</small></div>
    <div class="sb-t" data-a="mask" data-d="600"><i class="c-p1" style="--v:50">50%</i><i class="c-p2" style="--v:30">30%</i><i class="c-p3" style="--v:20">20%</i></div></div>
</div>
```
Dùng `data-a="mask"` (quét trái sang phải, chữ không bị méo). `--bh` = độ cao thanh.

**Phễu** (`--w` = độ rộng tầng, giảm dần; cột phải là tỷ lệ chuyển đổi):
```html
<div class="fn" style="--lw:250px">
  <div class="fn-s" style="--w:100%"><div class="fn-l">Lượt truy cập<small>Website</small></div><div class="fn-bw"><div class="fn-b" data-a="grow" data-d="300">48.000</div></div><div class="fn-r"></div></div>
  <div class="fn-s" style="--w:80%"><div class="fn-l">Dùng thử</div><div class="fn-bw"><div class="fn-b" data-a="grow" data-d="450">9.600</div></div><div class="fn-r">20%<small>chuyển đổi</small></div></div>
</div>
```
Tầng nổi bật: thêm `c-p3` lên `.fn-s`. `--bh` = độ cao tầng, `--tp` = độ vát.

**Thác nước (waterfall)**: `--b` = đáy, `--h` = chiều cao, cả hai tính theo % chiều cao biểu đồ (giá trị lớn nhất ≈ 95). `.tot` tổng (màu `--blue`), `.pos` tăng (xanh lá), `.neg` giảm (đỏ; `--b` = mức sau khi giảm). Đường nối nét đứt tự vẽ.
```html
<div class="wf">
  <div class="wf-c tot" style="--b:0;--h:96"><div class="wf-bar" data-a="bar" data-d="300"><span class="wf-v">1.250</span></div><div class="wf-l">Doanh thu</div></div>
  <div class="wf-c neg" style="--b:59;--h:37"><div class="wf-bar" data-a="bar" data-d="500"><span class="wf-v">−480</span></div><div class="wf-l">Giá vốn</div></div>
  <div class="wf-c tot" style="--b:0;--h:27"><div class="wf-bar" data-a="bar" data-d="700"><span class="wf-v">356</span></div><div class="wf-l">Lợi nhuận</div></div>
</div>
```
`.wf` tự giãn hết chỗ còn lại (`flex:1`); `--gap` = khoảng cách cột, `--bw` = độ rộng tối đa của cột.

**Đồng hồ (gauge)** (`--v` 0–100; bỏ `.gz-ndl` nếu chỉ cần cung):
```html
<div class="gz" style="--v:82;--sz:500px">
  <div class="gz-d"><svg viewBox="0 0 200 110"><path class="gz-trk" d="M20 100 A80 80 0 0 1 180 100" pathLength="100"/>
    <path class="gz-val" d="M20 100 A80 80 0 0 1 180 100" pathLength="100" data-a="ring" data-d="500"/></svg><div class="gz-ndl"></div></div>
  <div class="gz-mm"><span>0</span><span>100</span></div>
  <div class="gz-n"><b>82</b><small>mục tiêu: 80 điểm</small></div>
</div>
```
Kim tự quay từ 0 tới giá trị khi trang hiện.

**Waffle 10×10** (`--n` = số ô tô màu trên 100, lấp theo hàng từ trên xuống):
```html
<div class="wfl c-p1" style="--n:68;--sz:420px"><b data-a="fade" data-d="700"></b></div>
<div class="wfl-n">68<small>/100</small></div><div class="wfl-t">doanh nghiệp dùng từ 3 phân hệ</div>
```
`.wfl.dot` = ô tròn; `--g` = khe giữa các ô.

**Bản đồ nhiệt (heatmap)** (`--n` = số cột; mỗi ô `<i style="--v:0…1">`, chữ tự đổi sáng/tối theo độ đậm):
```html
<div class="hm c-p1" style="--n:3;--lw:220px" data-stagger="20" data-d0="400" data-sa="zoom">
  <span></span><span class="hm-h">T10</span><span class="hm-h">T11</span><span class="hm-h">T12</span>
  <span class="hm-l">Kế toán</span><i style="--v:.71">71</i><i style="--v:.82">82</i><i style="--v:.9">90</i>
</div>
<div class="hm-key">Thấp <i></i> Cao</div>
```
`--ch` = độ cao ô.

**Bảng so sánh** (`--n` phương án, `--lw` cột tiêu chí, `--hl` = số thứ tự cột nổi bật, bỏ đi nếu không cần):
```html
<div class="cpt c-p1" style="--n:3;--hl:1;--lw:520px" data-stagger="70" data-d0="350">
  <div class="cpt-r cpt-h"><div></div><div class="on"><span class="cpt-tag">Đề xuất</span><br>Gói A<small>6,5 triệu/năm</small></div><div>Gói B</div><div>Excel</div></div>
  <div class="cpt-r"><div>Hoá đơn điện tử</div><div><span class="cpt-y">[[check]]</span></div><div>Một phần</div><div><span class="cpt-x">[[x]]</span></div></div>
</div>
```
`.cpt-y` dấu có (xanh), `.cpt-x` dấu không (xám), ô chữ ghi thẳng. `--rh` = độ cao dòng tối thiểu.

### Sơ đồ

**Vòng lặp (cycle)** 3–6 bước: `--n` trên `.cyc`, `--i` (0 … n-1, bắt đầu ở đỉnh, chạy theo chiều kim đồng hồ) trên từng bước; mũi tên giữa các bước tự vẽ.
```html
<div class="cyc c-p3" style="--n:5;--h:680px;--ry:235px" data-stagger="150" data-d0="400" data-sa="pop">
  <div class="cyc-c"><div class="cyc-cn">Mỗi quý<small>một vòng</small></div></div>
  <div class="cyc-i" style="--i:0"><div class="cyc-b card"><div class="cyc-ic">[[database]]</div><div class="cyc-t">Thu thập</div><div class="cyc-d">Dữ liệu sử dụng</div></div></div>
  <div class="cyc-i" style="--i:1">…</div>
</div>
```
`--w/--h` = khung (mặc định 1300×700), `--rx/--ry` = bán kính ngang/dọc, `--bw` = độ rộng thẻ, `--cz` = cỡ vòng giữa. 3–4 bước có thể giảm `--rx`.

**Trục – nan (hub & spoke)** 4–8 nhánh: `--n` trên `.hs`, `--i` trên từng `.hs-i`; đường nối nét đứt tự vẽ về tâm.
```html
<div class="hs c-p1" style="--n:6;--h:660px">
  <div class="hs-c" data-a="zoom" data-d="300"><div class="hs-cn">[[layers]]<b>AMIS</b><small>Dữ liệu dùng chung</small></div></div>
  <div class="hs-i" style="--i:0" data-a="pop" data-d="600"><div class="hs-b card"><span class="ib">[[calculator]]</span><div><div class="hs-t">Kế toán</div><div class="hs-d">Sổ sách, thuế</div></div></div></div>
</div>
```
`--rx/--ry` (mặc định 560/250), `--rot` xoay cả vòng (ví dụ 8 nhánh: `--rot:22.5deg`), `--cz` cỡ tâm, `--bw` độ rộng thẻ.

**Venn 3 vòng / 2 vòng** (`.vn.two`): các vòng `.vn-o` đặt TRƯỚC, nhãn sau. `.vn-x.ab/.ac/.bc` = nhãn vùng giao từng cặp, `.vn-c` = nhãn giữa.
```html
<div class="vn" style="--sz:700px">
  <div class="vn-o c-p1" data-a="zoom" data-d="300"><div class="vn-t">[[cpu]]<b>Công nghệ</b><small>Đám mây, AI</small></div></div>
  <div class="vn-o c-p2" data-a="zoom" data-d="450"><div class="vn-t"><b>Dữ liệu</b></div></div>
  <div class="vn-o c-p3" data-a="zoom" data-d="600"><div class="vn-t"><b>Con người</b></div></div>
  <div class="vn-x ab" data-a="fade" data-d="1000"><span>Tự động hoá</span></div>
  <div class="vn-c" data-a="pop" data-d="1400"><span>Chuyển đổi số</span></div>
</div>
```
Nhãn trong vùng giao hẹp nên ngắn, xuống dòng bằng `<br>`.

**Sơ đồ tổ chức / cây 3 cấp** (danh sách lồng nhau; cấp 3 tự xếp dọc; nhánh màu theo `c-pN` đặt trên `li` cấp 2):
```html
<div class="otr"><ul><li><div class="ot-n card" data-a="pop"><span class="ot-av">MT</span><div><b>Minh Tâm</b><small>Tổng giám đốc</small></div></div>
  <ul>
    <li class="c-p1"><div class="ot-n card" data-a="up" data-d="550"><span class="ot-av">HL</span><div><b>Khối Sản phẩm</b><small>Hải Linh</small></div></div>
      <ul><li><div class="ot-n card" data-a="left" data-d="900"><b>Kế toán số</b></div></li></ul></li>
  </ul></li></ul></div>
```
`.ot-av` nhận ảnh qua `style="background-image:url(…)"` hoặc chữ tắt. `--og` = khoảng cách giữa các cấp. Tối đa ~5 nhánh cấp 2 trên một trang.

**Kiến trúc tầng (layer stack)**:
```html
<div class="lyr" style="--lw:330px" data-stagger="120" data-d0="350" data-sa="left">
  <div class="ly-r c-p1"><div class="ly-l">[[smartphone]]<div>Kênh tương tác<small>Người dùng chạm vào</small></div></div>
    <div class="ly-b"><span class="ly-ch">[[monitor]] Web</span><span class="ly-ch">Ứng dụng di động</span></div></div>
</div>
```
`.ly-r.hi` = tầng nhấn mạnh (viền màu). `--rh` = độ cao tầng.

**Bản đồ định vị (2 trục)**: bong bóng `.pm-b` đặt bằng `--x`, `--y` (0–100, gốc ở góc trái dưới), cỡ `--s` (đường kính px). `.me` = vị trí của mình; nhãn mặc định dưới bong bóng, `.up` trên, `.r` phải, `.l` trái.
```html
<div class="pm c-p1" style="--w:1040px;--h:620px">
  <div class="pm-q q1">Cao cấp</div><div class="pm-q q2 on">Đáng tiền nhất</div><div class="pm-q q3">Cơ bản</div><div class="pm-q q4">Đắt, ít tính năng</div>
  <div class="pm-ax yh"><span>Đầy đủ tính năng ↑</span></div><div class="pm-ax yl"><span>↓ Cơ bản</span></div>
  <div class="pm-ax xl">← Giá thấp</div><div class="pm-ax xh">Giá cao →</div>
  <div class="pm-b me" style="--x:34;--y:76;--s:110" data-a="pop" data-d="500"><i>[[star]]</i><span>Chúng ta</span></div>
  <div class="pm-b c-p2" style="--x:74;--y:70;--s:84" data-a="pop" data-d="650"><i></i><span>Đối thủ A</span></div>
</div>
```
`.pm-q.on` = tô nền góc phần tư nổi bật (q1 phải trên, q2 trái trên, q3 trái dưới, q4 phải dưới).

### Bố cục

**Bento** (`--n` cột; `.w2/.w3` rộng 2/3 cột, `.h2` cao 2 hàng; ô chữ/số `.bt.card`, ô ảnh `.bt-ph`):
```html
<div class="bento" style="--n:4" data-stagger="100" data-d0="350" data-sa="zoom">
  <div class="bt card solid w2 h2 c-p1"><div class="bt-k">Người dùng</div><div class="bt-v">1,2<small>triệu</small></div><div class="bt-d">Tăng 38%</div></div>
  <div class="bt-ph h2" data-ph="ten_anh"><div class="cap">Chú thích ảnh</div></div>
  <div class="bt card c-p3"><div class="bt-k">Uptime</div><div class="bt-v" style="font-size:72px">99,9<small>%</small></div></div>
</div>
```
`.bt.solid` = nền màu `--c`. Mục chữ trong ô: `.bt-k` (nhãn), `.bt-v` (số lớn, tự dồn xuống đáy), `.bt-t` (tiêu đề), `.bt-d` (mô tả). Lưới tự chia đều chiều cao còn lại: 3 hàng là vừa, ô nhỏ chỉ nên 1 số hoặc 1 dòng mô tả.

**Hội thoại (chat)**: `.cv-m` = khách (trái), `.cv-m.me` = nhân viên/AI (phải, nền `--c`); `.cv-typing` = ba chấm đang gõ.
```html
<div class="cv c-p1" data-stagger="350" data-d0="400">
  <div class="cv-m"><div class="cv-av">NL</div><div><div class="cv-n">Chị Ngọc Lan <time>09:41</time></div><div class="cv-bb">Hoá đơn bị sai mã số thuế?</div></div></div>
  <div class="cv-m me"><div class="cv-av">[[bot]]</div><div><div class="cv-n">Trợ lý AMIS <time>09:41</time></div><div class="cv-bb">Em đã tìm thấy <b>hoá đơn 0001234</b>…</div></div></div>
  <div class="cv-m me"><div class="cv-av">[[bot]]</div><div><div class="cv-bb cv-typing"><i></i><i></i><i></i></div></div></div>
</div>
```
`.cv-av` nhận ảnh đại diện qua `style="background-image:url(…)"`.

**Khung thiết bị**: điện thoại `.dv-phone` (`--w` = rộng, cao tự tính 9:19), laptop `.dv-lap` (`--w`, màn 16:10, đế tự vẽ, cần chừa thêm ~7% mỗi bên). Màn hình `.dv-scr[data-ph]` = ảnh chụp màn hình (phủ kín, căn đỉnh), hoặc `.dv-scr.ui` chứa HTML tự dựng (dùng lại được donut, chú giải…).
```html
<div class="dv-phone" data-a="rise" style="--w:300px"><div class="dv-scr" data-ph="app_home"></div></div>
<div class="dv-lap" data-a="rise" style="--w:860px"><div class="dv-scr" data-ph="web_dashboard"></div></div>
```
Điện thoại cao gấp ~2,1 lần bề rộng: trang có tiêu đề thì `--w` ≤ 310px; laptop `--w` ≤ 900px.

⚠ Các sơ đồ định vị bằng `left/top` + hàm lượng giác CSS, KHÔNG bằng `transform`, nên đặt `data-a` thẳng lên `.cyc-i`, `.hs-i`, `.pm-b`, `.vn-o` được. Không đặt `opacity` lên phần tử có `data-a`.

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
  "logo_plate": true,
  "font_picker": ["inter", "montserrat", "barlow", "roboto", "google-sans", "open-sans"]
}
```

Chỉ `title`, `output`, `theme`, `parts` là cần; các khoá còn lại ghi đè theme (giải thích ở `themes.md`). `parts[].color` ghi đè màu một phần. `logo: null` = không logo. `fonts` nhận khoá trong `fonts/fonts.json` (vd `barlow`, `roboto`, `open-sans`, `google-sans`, `inter`, `montserrat`). `font_picker`: các font nhúng sẵn để người dùng đổi trong chế độ sửa (nút Aa Font); bỏ trống = 6 font trên, `false` = tắt (file nhẹ hơn ~0,6 MB).

## Thứ tự ưu tiên file

`src/style.css`, `src/app.js`, `src/img.js`, `src/slides.html` lấy từ thư mục dự án (`new_deck.sh` đã chép sẵn). Theme (`themes/`), font (`assets/fonts/` → `$SK/fonts/`), `src/components.css` và `icons.json` tìm ở dự án trước rồi mới tới skill. Muốn chỉnh CSS riêng cho 1 bài mà không đụng theme: tạo `src/custom.css` (nạp sau cùng).
