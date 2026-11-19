# Cú pháp trang (src/slides.html)

Muốn xem mẫu đầy đủ thì mở `slides-example.html` (38 trang), tìm theo tên class. Bố cục v2 (agenda, KPI, ring, timeline, bảng giá, SWOT…) và các hiệu ứng mới ở `components.md`.

## Khung một trang

```html
<section class="slide" data-p="2" data-title="Tiêu đề hiển thị ở mục lục/ghi chú" data-k="Nhãn phụ">
  <span class="t-bar" data-a="grow"></span>
  <h2 class="t" data-a="up">Nhận diện tổng quan <span class="hl">chiêu thức</span></h2>
  <p class="s" data-a="up">Câu dẫn phụ (Inter, màu nhạt)</p>
  ... nội dung ...
</section>
```

**Thuộc tính của `<section>`:**
- `data-p`: số phần (1..n), khớp `deck.json.parts`. Dùng cho thanh tiến độ, màu nền và nền đổi tông theo phần.
- `data-title`: tên trang trong mục lục (G) và ghi chú (N).
- `data-nologo`: ẩn logo góc. Dùng cho bìa và trang kết, vì ở đó logo to đặt giữa.

**Các loại trang:**
- **Bìa:** `class="slide cover"`.
- **Trang phần:** `class="slide sect"`, gồm `.wm` (số chìm), `.num-badge`, `.stitle`, `.ssub` và mục lục phần `.toc .ti`.
- **Trang kết:** `class="slide cover closing"`. Không đánh số; có khiên SVG `.cshield` bao `.biglogo`.

**Lưu ý:**
- Tiêu đề `h2.t` dùng font tiêu đề của theme; viết HOA hay không tuỳ theme (`title_case` trong deck.json để ép).
- `.hl` là chữ nhấn màu theo phần.
- KHÔNG dùng nhãn `.kicker` ở góc trên trái (người dùng đã bỏ).
- Logo: `<img src="{{LOGO}}">`. Build tự thay bằng logo trong `deck.json`.

## Bố cục

**Khối dàn trang:**
- `row`: flex ngang. `col`: flex dọc. `grow`: flex 1. `mt-auto`: đẩy xuống đáy.
- Gap và margin chỉnh bằng `style`.

**Thẻ `card`:**
- Kèm màu: `c-p1` … `c-p6` (màu phần, đổi theo theme) hoặc `c-blue` / `c-red` / `c-amber` / `c-green` / `c-violet` (cố định, dùng khi màu mang nghĩa). Màu này áp cho icon, chip và viền nhấn bên trong.
- Biến thể: `q4`, `k4`, `w5`… là độ rộng theo lưới. Xem trang mẫu tương ứng.

**Chữ:**

| Class | Dùng cho |
|---|---|
| `h3`, `h4` | tiêu đề thẻ (Google Sans) |
| `p` | đoạn văn; thêm `sm` cho chữ nhỏ |
| `lbl` | nhãn chữ HOA giãn chữ |
| `chip` | viên thuốc nhỏ |
| `stepn` | nhãn "Bước/Kiểu 01" |
| `big` | số lớn |
| `ul.bul > li` | gạch đầu dòng |

**Thành phần khác:**
- **Hộp icon:** `<div class="ib sm">[[icon]]</div>`. Kích thước `sm` / `lg`; thêm `solid` để tô nền đặc.
- **Băng nhấn cuối trang:** `<div class="banner c-red">[[zap]] Câu kết</div>`.
- **Icon nổi trang trí:** `<div class="par" style="--dp:-18px;position:absolute;left:150px;top:200px"><div class="orb c-red float" data-a="pop">[[hook]]</div></div>`. Dùng ở bìa và trang kết; `--dp` là độ lệch parallax theo chuột.
- **Dòng nguồn trích dẫn:** `<div class="src">Nguồn: …</div>`. Mặc định nằm ở đáy trang; trên trang video thì nằm trên góc phải khung (`.vwrap ~ .src`).

## Icon

`[[ten-icon]]` được build thay bằng SVG kiểu Lucide. Danh sách ở `template/icons.json` (159 icon; thiếu thì thêm path SVG 24×24 kiểu Lucide vào file đó, hoặc tạo `icons.json` riêng trong dự án):

activity alert-triangle arrow-down arrow-left arrow-right arrow-up arrow-up-right atom award ban bank banknote bar-chart bell book-open bookmark bot brain briefcase building cake calculator calendar camera car cart cast check check-circle check-square chevrons-right circle-dot clipboard clock cloud code coffee coins compass cpu credit-card crosshair crown database dollar download droplet eye eye-off factory file-text filter flag flame flask folder gamepad gem gift git-branch globe grad hand handshake headphones heart heart-pulse help home hook hourglass id-card image infinity info key landmark laptop layers leaf life-buoy lightbulb line-chart link list-checks lock mail map map-pin megaphone message message-square mic minus monitor moon mountain mouse-pointer music package palette party pen percent phone pie-chart pill plane play plus puzzle qr quote receipt refresh repeat rocket scale scan-face school search send server settings share shield shield-alert shield-check sliders smartphone smile sparkles sprout star stethoscope store sun tag target thumbs-up ticket timer toggle trending-down trending-up trophy truck user user-check user-plus users video wallet wand wifi wrench x x-circle zap

## Ảnh minh hoạ

```html
<div class="im float" data-im="money_industry" data-a="zoom" data-d="300" style="width:330px;height:300px"></div>
```

- Ảnh lấy từ file `assets/img/money_industry.png` (cũng nhận jpg hoặc webp). Build nén sang webp 900px.
- Ảnh hiện trên thẻ trắng bo góc và tự giữ đúng tỉ lệ (`--r`).
- `float` cho ảnh trôi nhẹ lên xuống.

## Hiệu ứng (đặt trên phần tử bất kỳ)

- `data-a`: kiểu hiệu ứng. Có `up` · `down` · `left` · `right` · `fade` · `pop` · `zoom` · `flip` · `grow` (cho `.t-bar`) · `bar` (cột biểu đồ, mọc từ đáy) · `mask` · `draw` (nét SVG), và mới: `rise` · `slam` · `tilt` · `blur` · `wipe` · `spin` · `ring`. Cho cả nhóm xuất hiện lần lượt: `data-stagger` (xem `components.md`).
- `data-d`: thời điểm bắt đầu (ms). Bỏ trống thì tự xếp lần lượt, mỗi phần tử cách nhau ~90ms. Nên rải 300→1200ms trong một trang.
- `data-t`: thời lượng (ms).

## Thành phần động

| Thành phần | Mã mẫu | Ghi chú |
|---|---|---|
| Số đếm lên | `<span data-count="14">14</span>` | Số lẻ: `data-count="4.7" data-dec="1"` |
| Ô số quay kiểu máy đánh bạc | `<div class="slot" data-slot="2" data-d="500">2</div>` | |
| Chữ gõ từng ký tự | `<span class="url" data-type>amazon.com</span>` | |
| Đèn bật theo thời gian | `<div class="light" data-light="700">[[hand]]</div>` | |
| Bộ đếm chạy theo thời gian thực | `<b data-live="14e9">0</b>` | Giá trị = số lượng mỗi ngày (mặc định 14 tỷ/ngày). Số có độ rộng cố định để chữ bên cạnh đứng yên. |
| Biểu đồ cột | `<div class="bars"><div class="bar in" data-a="bar" style="height:56%"></div>…</div>` | |

## Khung video

```html
<div class="vwrap"><div class="vframe" data-a="zoom" data-d="250"><div class="vno">01</div><div class="play">[[play]]</div><div class="hint">Bấm hoặc kéo-thả video vào khung để phát · Ctrl+S để lưu video vào file</div><input type="file" accept="video/*" hidden></div></div>
<div class="src" data-a="fade" data-d="600">Nguồn: …</div>   <!-- nếu cần -->
```

- Gắn video bằng `deck.json.videos` (`{"<số trang>": "v1.mp4"}`, file đặt trong `assets/video/`).
- Khung không có video thì bút chiếu next sang trang bình thường, người dùng tự gắn video bằng phím E.

## Chống chữ mồ côi / tràn

- Dùng `&nbsp;` giữa 2 từ cuối tiêu đề, hoặc giữa các cụm không được tách ("14&nbsp;tỷ", "Hình&nbsp;thức&nbsp;1").
- CSS dùng `text-wrap-style: pretty` (lấp đầy dòng, tránh mồ côi). **Không dùng `text-wrap: balance`**: build tự đổi thành pretty. Tiêu đề dài hơn khung ≤ 10% tự co chữ cho vừa 1 dòng. Ngắt dòng cố ý thì dùng `<br>`.
- Kiểm tra bằng `scripts/check_layout.mjs`. Riêng ngắt dòng cố ý, script sẽ báo nhưng không phải lỗi.
