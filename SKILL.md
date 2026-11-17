---
name: misa-html-deck
description: Dựng bài trình chiếu thành MỘT file HTML tự chứa kiểu MISA (font, ảnh, logo, video nhúng base64; chạy offline trên máy khác), có hiệu ứng chuyển động "wow", điều khiển bằng bút chiếu (video: next lần 1 hiện khung, next lần 2 phát toàn màn hình có tiếng), chế độ sửa tại chỗ (phím E: sửa chữ, định dạng, chèn/xoay/chỉnh ảnh, gắn video; Ctrl+S lưu file mới), xuất PDF có link mở video, bỏ trang trên file người dùng đã sửa. Dùng khi người dùng muốn thiết kế lại PPTX/nội dung thành slide HTML, "làm deck HTML", "slide trình chiếu 1 file", "bài thuyết trình như bài lừa đảo", sửa/xuất PDF/bỏ trang một deck đã dựng bằng skill này.
---

# MISA HTML Deck

Bộ khung đã chạy thật (bài "Xu hướng lừa đảo và cách phòng tránh", 11/2026), đã qua nhiều vòng góp ý của sếp. **Dùng lại khung, đừng viết lại từ đầu.**

```
template/      khung dự án: build.py, deck.json, src/{slides.html, style.css, app.js, img.js, notes.json}, assets/{fonts, logo-misa.png, img/, video/}
reference/     slides-example.html (38 trang mẫu = thư viện bố cục), patterns.md (cú pháp trang), lessons.md (bài học từ góp ý — ĐỌC TRƯỚC KHI THIẾT KẾ)
scripts/       setup.sh · new_deck.sh · dump_pptx.py · gen_images.py · compress_video.sh · check_layout.mjs · export_pdf.sh · remove_slides.mjs
```
`SK=~/.claude/skills/misa-html-deck`, Python: `$SK/.venv/bin/python` (chưa có thì chạy `$SK/scripts/setup.sh`). Node ≥ 22 + Google Chrome cho các script `.mjs`.

## Quy trình làm bài mới

1. **Chốt yêu cầu** (hỏi gọn nếu thiếu): file nguồn, giữ nguyên nội dung hay được biên tập, tông màu (mặc định: sáng, glass xanh-trắng), các phần lớn (tên + màu), video nào gắn vào trang nào, có cần nguồn trích dẫn trên trang video không.
2. **Tạo dự án**: `$SK/scripts/new_deck.sh <thư-mục>` rồi sửa `deck.json` (title, output, parts, videos).
3. **Đọc nội dung**: PPTX → `$SK/.venv/bin/python $SK/scripts/dump_pptx.py file.pptx > dump.txt` (chữ, vị trí, ghi chú). Giữ nguyên câu chữ gốc nếu người dùng yêu cầu; ghi chú thuyết trình → `src/notes.json` (mảng, mỗi trang 1 chuỗi; build tự bù cho trang kết).
4. **Dựng trang** trong `src/slides.html`: mỗi trang 1 `<section class="slide">`. Chọn bố cục từ `reference/slides-example.html` (bìa, mục lục, trang phần, thẻ số liệu, lưới thẻ, quy trình bước, biểu đồ cột, so sánh, video, trang kết có khiên). Cú pháp ở `reference/patterns.md`. Đa dạng bố cục, mỗi trang một điểm nhấn.
5. **Ảnh minh hoạ** (nếu cần): viết `jobs.json` → `MISA_GEMINI_SA=<file service account .json> $SK/.venv/bin/python $SK/scripts/gen_images.py jobs.json assets/img` (Gemini qua Vertex, model `gemini-3-pro-image`; đường dẫn file khoá hỏi người dùng hoặc xem bộ nhớ dự án). Prompt chuẩn ở `lessons.md`. Dùng `<div class="im" data-im="ten_anh">`: ảnh nền trắng đặt trong thẻ trắng bo góc, **không tách nền**.
6. **Video**: nén `$SK/scripts/compress_video.sh vào.mov assets/video/v1.mp4 [crf]` (CRF 25 mặc định; video dài/nặng dùng 27; luôn H.264 + AAC, ≤1080p). Khai báo `"videos": {"5": "v1.mp4"}` (số trang 1-based) và đặt khung `.vwrap > .vframe` ở trang đó.
7. **Build**: `$SK/.venv/bin/python build.py` → `dist/<output>`. Font tự cắt theo ký tự dùng; build báo thiếu ảnh/icon.
8. **Kiểm tra** (bắt buộc trước khi giao):
   - `node $SK/scripts/check_layout.mjs dist/<file>.html`: tiêu đề mồ côi 1 từ, chữ tràn thẻ, icon đè chữ.
   - Xem bằng mắt từng trang (preview server hoặc `capture_slides.mjs` rồi ghép ảnh xem nhanh).
   - Thử luồng bút chiếu trên trang video (PageDown: lần 1 phát toàn màn hình, lần 2 sang trang; PageUp đóng video).
   - Video lớn: thử cả Safari nếu người dùng chiếu bằng Mac.
9. **Giao**: đường dẫn file, dung lượng, cách dùng (→/Space/bút chiếu, F toàn màn hình, N ghi chú, G mục lục, E sửa, Ctrl+S lưu), lưu ý mở file sớm vài giây khi có video nặng.

## Việc thường gặp sau khi giao

- **Sửa theo góp ý**: sửa `src/*` rồi build lại. Đừng sửa thẳng file trong `dist/`.
- **Người dùng đã tự sửa (E + Ctrl+S) rồi gửi lại file**: chỉnh sửa nằm trong `<script id="deck-edits">` (texts/styles theo chỉ số khối chữ, videos theo chỉ số trang, images theo trang). **Làm trên chính file đó**, không build lại từ src (sẽ mất chỉnh sửa của họ).
  - Bỏ trang: `node $SK/scripts/remove_slides.mjs vào.html ra.html 32,36`. Script tự đánh lại chỉ số chỉnh sửa, ghi chú, tổng số trang, video. Lưu ra file MỚI cạnh file gốc.
- **Xuất PDF**: `$SK/scripts/export_pdf.sh <deck.html> "<thư-mục-ra>" "<Tiêu đề>"`.
  - Chụp từng trang ở trạng thái cuối hiệu ứng, nét gấp rưỡi Full HD. Trang có bộ đếm chạy được chờ khoảng 1 phút cho số đủ dài.
  - Ghép PDF 16:9, tách video nhúng ra `video/video-trang-NN.mp4` và gắn link tương đối trên khung video.
  - Nói rõ với người dùng: PDF không phát video tại chỗ; phải gửi kèm cả thư mục `video/`; muốn 1 file duy nhất thì dùng link online.
  - Xem lại ảnh chụp trước khi giao.

## Kiến trúc khung (khi cần sửa sâu)

- **Sân khấu**: 1920×1080, co giãn vừa màn hình (`fit()`).
- **Hiệu ứng vào trang**: chạy bằng WAAPI theo `data-a` (kiểu), `data-d` (trễ, ms), `data-t` (thời lượng). Easing spring dùng `linear()`.
- **Khung trang**: `#foot` (thanh tiến độ các phần + số trang) do build tự tính từ `data-p` và `deck.json.parts`. Trang `.closing` không đánh số.
- **Chế độ sửa** (`app.js`):
  - `PRISTINE` = HTML gốc chụp lúc mở (dữ liệu video `dv-N` tách riêng để không nhân đôi bộ nhớ).
  - Khối sửa được = `EDITABLE` (duyệt cây theo thứ tự, gắn `data-e`).
  - Ctrl+S ghi `EDITS` vào thẻ `deck-edits`, rồi lưu bằng showSaveFilePicker (không có thì tải xuống).
- **Thanh định dạng `#fmt`**: dùng execCommand; kiểu khối lưu ở `EDITS.styles`.
- **Ảnh chèn** (`img.js`, build ghép vào trước `window.deck`): lưu ở `EDITS.images`, bảng chỉnh `#ipan`.
- **Video**: `<script type="application/octet-stream" id="dv-N">` base64. Lúc chạy, `b64Blob()` giải mã theo khúc thành Blob URL (**không dùng data: URL**: Safari không nạp được chuỗi data: vài chục MB). `#vfs` là lớp phủ toàn màn hình.
- **Theme**: khối "LIGHT · GLASS BLUE" cuối `style.css` ghi đè các token (`--ink`, `--blue`, `--cardbg`…). Đổi tông thì sửa khối này. Các khối tối phía trên là lớp nền cũ, giữ nguyên.
- **Nền**: mạch vi điện tử SVG sinh trong `build.py` (`circuit_svg()`), chuyển động chậm, thưa.

## Bảo mật

File service account Gemini chứa private key: chỉ dùng cục bộ qua đường dẫn. Không in nội dung, không chép vào dự án/HTML, không gửi đi đâu.
