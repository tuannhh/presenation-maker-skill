---
name: misa-html-deck
description: Dựng bài trình chiếu thành MỘT file HTML tự chứa (font, ảnh, logo, video nhúng; chạy offline) có hiệu ứng chuyển động và chuyển trang kiểu Prezi, khối lập phương, lật thẻ. 15 theme (MISA glass, tối công nghệ, tối giản, tạp chí, vui nhộn, neo-brutalism, vàng-đen, thiên nhiên, gradient, AVA lavender, navy, keynote đen trắng, hoàng hôn, bảng phấn, biển xanh); hơn 40 bố cục gồm biểu đồ, sơ đồ, bento, chat, khung điện thoại/laptop; nhiều thể loại (đào tạo, pitch, bán hàng, báo cáo, ra mắt sản phẩm, gala, workshop, onboarding, tech talk, tuyên truyền). Có bút chiếu, chế độ sửa tại chỗ (sửa chữ/ảnh, kéo khối, đổi font, Ctrl+S lưu), xuất PDF, xuất PPTX sửa được có hiệu ứng, bỏ trang. Dùng khi người dùng muốn làm slide/deck/bài thuyết trình HTML, thiết kế lại PPTX hoặc nội dung thành slide, đổi phong cách deck, hoặc sửa/xuất PDF/xuất PPTX/bỏ trang một deck đã dựng bằng skill này.
---

# MISA HTML Deck (đa phong cách)

Khung đã chạy thật qua nhiều vòng góp ý. **Dùng lại khung, đừng viết lại từ đầu.** Một bộ `slides.html` build được ra mọi theme; đổi phong cách chỉ cần đổi `"theme"` trong `deck.json`.

```
template/   build.py · deck.json · icons.json (159 icon) · themes/{themes.json, <theme>.css}
            src/{slides.html, style.css, components.css, app.js, img.js, notes.json} · assets/{logo-misa.png, img/, video/}
fonts/      font dùng chung + fonts.json (đều có đủ dấu tiếng Việt)
reference/  themes.md · genres.md · components.md · patterns.md · lessons.md · showcase.html (33 trang v2 + v3) · slides-example.html (38 trang gốc)
scripts/    setup.sh · new_deck.sh · preview_themes.py · contact_sheet.mjs · check_layout.mjs · dump_pptx.py · gen_images.py
            compress_video.sh · capture_slides.mjs · export_pdf.sh · remove_slides.mjs
            capture_pptx.mjs · make_pptx.py · export_pptx.sh
```

**Môi trường** (`SK` = thư mục chứa file SKILL.md này, vd `~/.claude/skills/misa-html-deck`, `~/.codex/skills/misa-html-deck`, `~/.gemini/config/skills/misa-html-deck`, `~/.copilot/skills/misa-html-deck`):
- Python của skill (gọi là `$PY` bên dưới): macOS/Linux `$SK/.venv/bin/python`, Windows `$SK/.venv/Scripts/python.exe`. Chưa có thì chạy `bash $SK/scripts/setup.sh` (đặt `VENV_DIR=D:/...` để venv nằm ổ khác rồi nối vào `.venv`).
- Node ≥ 22 + Chrome/Edge cho các script `.mjs` (tự tìm theo hệ điều hành; đặt biến `CHROME` nếu ở chỗ khác).
- Trên Windows chạy script `.sh` bằng Git Bash: `bash $SK/scripts/<tên>.sh …`.

## Quy trình làm bài mới

1. **Chốt yêu cầu** (hỏi gọn nếu thiếu): nội dung/file nguồn, **thể loại & khán giả**, giữ nguyên chữ hay được biên tập, phong cách mong muốn, các phần lớn, video gắn trang nào, logo (MISA, logo khác, hay không logo).
2. **Chọn thể loại** → `reference/genres.md`: cấu trúc trang, bố cục nên dùng, giọng văn, theme gợi ý.
3. **Chọn theme** → `reference/themes.md`. Người dùng chưa rõ thì cho xem cả 15:
   `"$PY" $SK/scripts/preview_themes.py <thư-mục-ra>` → mở `<thư-mục-ra>/index.html` (lưới xem trước, bấm để xem bản đầy đủ). Thêm `--slides src/slides.html` để xem trước bằng chính nội dung của họ, `--themes a,b` để giới hạn, `--logo none` để bỏ logo.
4. **Tạo dự án**: `bash $SK/scripts/new_deck.sh <thư-mục> <theme>` rồi sửa `deck.json` (title, output, parts, videos, logo, palette…; xem `reference/components.md` › deck.json).
5. **Đọc nội dung**: PPTX → `"$PY" $SK/scripts/dump_pptx.py file.pptx > dump.txt`. Ghi chú thuyết trình → `src/notes.json` (mảng, mỗi trang 1 chuỗi).
6. **Dựng trang** trong `src/slides.html` (mỗi trang 1 `<section class="slide">`):
   - Bố cục v2 (agenda, statement, KPI, ring, hbars, cột, đường, timeline, process, quote, split ảnh, team, bảng giá, trước/sau, SWOT, roadmap, code, cảm ơn…): `reference/components.md` + mẫu sống `reference/showcase.html`.
   - Bố cục v3 (donut, thanh chồng 100%, phễu, waterfall, gauge, waffle, heatmap, bảng so sánh, vòng lặp, hub & spoke, Venn, sơ đồ tổ chức, kiến trúc tầng, bản đồ định vị, bento, chat, khung điện thoại/laptop): cùng `components.md` (mục "Bố cục v3"), mẫu ở trang 18–32 của showcase.
   - Bố cục gốc (thẻ lưới, video, bộ đếm, slot, khiên…): `reference/patterns.md` + `reference/slides-example.html`.
   - Đa dạng bố cục, mỗi trang một ý chính. Dùng màu theo phần `c-p1..c-p6` (lấy từ palette của theme) để màu tự đổi khi đổi theme.
7. **Ảnh** (nếu cần): `jobs.json` → `MISA_GEMINI_SA=<file service account> "$PY" $SK/scripts/gen_images.py jobs.json assets/img`. **Phong cách prompt theo theme** ở `themes.md`. Ảnh minh hoạ dùng `data-im`, ảnh chụp/tràn trang dùng `data-ph`.
8. **Video**: `bash $SK/scripts/compress_video.sh vào.mov assets/video/v1.mp4 [crf]`, khai báo `"videos": {"5": "v1.mp4"}`.
9. **Build**: `"$PY" build.py` → `dist/<output>`. Build in ra theme/nền/font đang dùng, báo thiếu ảnh/icon/ký tự.
10. **Kiểm tra** (bắt buộc trước khi giao):
    - `node $SK/scripts/contact_sheet.mjs dist/<file>.html dist/sheet.jpg 4` rồi **xem ảnh** → thấy ngay trang tràn chữ, lệch, trống, sai màu.
    - `node $SK/scripts/check_layout.mjs dist/<file>.html`: tiêu đề mồ côi, chữ tràn thẻ, icon đè chữ.
    - Trang video: thử luồng bút chiếu (PageDown 2 lần, PageUp đóng video).
11. **Giao**: đường dẫn, dung lượng, theme đã dùng, cách dùng (→/Space/bút chiếu, F toàn màn hình, N ghi chú, G mục lục, E sửa, M trong chế độ sửa để kéo/xoá khối, Ctrl+S lưu).

## Việc thường gặp sau khi giao

- **Đổi phong cách**: đổi `"theme"` (và nếu cần `palette`, `fonts`, `bg`, `motion`) trong `deck.json` rồi build lại. Không phải viết lại slides.
- **Sửa theo góp ý**: sửa `src/*` rồi build lại. Đừng sửa file trong `dist/`.
- **Người dùng đã tự sửa (E + Ctrl+S) rồi gửi lại file**: chỉnh sửa nằm trong `<script id="deck-edits">`. **Làm trên chính file đó**, không build lại từ src. Bỏ trang: `node $SK/scripts/remove_slides.mjs vào.html ra.html 32,36` (lưu ra file MỚI).
- **Xuất PDF**: `bash $SK/scripts/export_pdf.sh <deck.html> "<thư-mục-ra>" "<Tiêu đề>"`. PDF không phát video tại chỗ: phải gửi kèm thư mục `video/`. Xem lại ảnh chụp trước khi giao.
- **Xuất PPTX sửa được**: `bash $SK/scripts/export_pptx.sh <deck.html> "<thư-mục-ra>" [ten.pptx]`. Chữ thành text box PowerPoint sửa được (đúng font, cỡ, màu, cả chữ gradient); nền, icon, biểu đồ, ảnh thành hình; mỗi khối vào bằng hiệu ứng PowerPoint gần nhất theo đúng thứ tự và độ trễ như HTML; chuyển trang ánh xạ sang transition PowerPoint; video nhúng kèm ảnh bìa; ghi chú thuyết trình vào Notes. Font tĩnh cần cài nằm ở `<ten>_fonts/`: dặn người nhận cài trước khi mở. Giới hạn: biểu đồ và sơ đồ là ảnh (sửa số phải sửa trong HTML rồi xuất lại); hiệu ứng lặp (nhấp nháy, xoay vòng) không giữ.
- **Theme riêng cho khách/thương hiệu khác**: tạo `<dự-án>/themes/<tên>.css` + `<dự-án>/themes/themes.json` (build ưu tiên thư mục dự án). Cách làm ở `themes.md` › Tạo theme mới.

## Kiến trúc (khi cần sửa sâu)

- **Sân khấu** 1920×1080, co giãn vừa màn hình. Hiệu ứng vào trang bằng WAAPI theo `data-a`/`data-d`/`data-t`; nhịp độ, blur, kiểu chuyển trang lấy từ `motion` của theme (`MOTION` trong `app.js`). Riêng từng trang: `<section data-tr="prezi">`. Kiểu hai lớp (trang cũ và mới cùng chuyển động): `prezi cube flip zoomin stack parallax swirl`; `mix` luân phiên các kiểu này. Xem `reference/themes.md`.
- **CSS ghép theo thứ tự**: `style.css` (khung + giao diện MISA glass mặc định) → `components.css` (bố cục v2, lớp nền) → `@font-face` + biến font (`--gs` tiêu đề, `--in` nội dung, `--mono`, `--script`) → màu phần (sinh từ palette) → `themes/<theme>.css` → ghi đè `deck.json.colors` → `src/custom.css` (nếu có).
- **Token theme** (khai trong `:root` của theme): `--ink --text --mute --line --blue --surface --surface2 --cardbg --cardline --onc --accent2 --hi --g1 --g2 --radius --rsm --blur --tt --srcc`. Theme chỉ cần đổi token + vài chi tiết riêng.
- **Nền** (`bg`): `circuit · blobs · dots · grid · paper · mesh · waves · stars · confetti · none`, sinh trong `build.py` (`LAYERS`).
- **Font**: `fonts/fonts.json` là sổ đăng ký; build cắt font theo đúng ký tự dùng và nhúng WOFF2. Font mono/script chỉ nhúng khi trang có dùng. Đổi font khi build: `deck.json` `"fonts": {"head": "roboto", "body": "open-sans"}`. Đổi font khi trình chiếu: chế độ sửa có nút **Aa Font** (font tiêu đề / nội dung cho cả bài, lưu `EDITS.fonts`) và ô chọn font trên thanh định dạng (riêng một khối chữ). Build nhúng sẵn 6 font để chọn: Inter, Montserrat, Barlow, Roboto, Google Sans, Open Sans (khoảng 0,6 MB). Đổi danh sách bằng `"font_picker": [khoá…]`, tắt bằng `"font_picker": false`.
- **Ngắt dòng:** `text-wrap-style: pretty`, cấm `balance` (build tự đổi). Tiêu đề vượt khung ≤ 10% tự co cho vừa 1 dòng (`fitText`).
- **Chế độ sửa, tay kéo ✥, ảnh chèn, Bố cục (M), video base64 → Blob** (`app.js`, `img.js`). Mọi chỉnh sửa nằm trong `<script id="deck-edits">`: `texts`, `styles` (theo số khối chữ `data-e`), `images`, `videos`, `blocks` (theo `data-b="trang:thứ tự"`). Không dùng data: URL cho video (Safari không nạp được chuỗi lớn).
- **Không đặt CSS `opacity` lên phần tử có `data-a`**: hiệu ứng fade của WAAPI sẽ ghi đè. Muốn mờ thì dùng `fill-opacity`, màu rgba hoặc bọc thêm 1 lớp.

## Bảo mật

File service account Gemini chứa private key: chỉ dùng cục bộ qua đường dẫn. Không in nội dung, không chép vào dự án/HTML, không gửi đi đâu.
