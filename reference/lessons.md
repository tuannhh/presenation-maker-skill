# Bài học từ góp ý thật (bài lừa đảo, 11/2026)

Những điều sếp, người dùng đã yêu cầu sửa. Mặc định làm đúng ngay từ đầu.

- Mục **Chữ**, **Video và bút chiếu**, **Bộ đếm**, **Chế độ sửa**, **Xuất PDF** và **Quy tắc chung** áp dụng cho MỌI theme.
- Mục **Thẩm mỹ MISA** chỉ là quy tắc của theme `misa-glass` (bài nội bộ MISA). Theme khác có font, màu, nền riêng (`themes.md`); đừng ép các quy tắc đó lên theme khác, trừ khi người dùng muốn.

## Quy tắc chung cho mọi theme (rút ra khi làm 9 theme)

- **Hỏi phong cách trước, đừng mặc định.** Chưa rõ thì cho xem `preview_themes.py` và để người dùng chọn.
- **Theme tối**: logo màu phải có nền sáng (`logo_plate`), không thì chìm. Ảnh minh hoạ nền trắng trên theme tối vẫn đặt trong thẻ trắng bo góc, trông như "ảnh in".
- **Chữ trên nền màu đặc** (gói nổi bật, banner, nút số) dễ trùng màu với nền ở theme lạ. Luôn xem contact sheet của trang bảng giá, banner, badge.
- **Font phải đủ dấu tiếng Việt.** Mọi font trong `fonts/` đã kiểm tra; font mới thì xem dòng "thiếu N ký tự" khi build.
- **Hiệu ứng vừa phải theo khán giả**: lãnh đạo/báo cáo → `calm`; sự kiện trẻ, pitch → `lively`; in/chiếu máy yếu → `none`.
- **Không đặt CSS `opacity` lên phần tử có `data-a`** (fade của WAAPI ghi đè, phần tử thành đậm đặc).
- **Kiểm tra bằng contact sheet sau mỗi lần build**, không chỉ xem vài trang đầu.

## Thẩm mỹ MISA (theme misa-glass)

- **Font:**
  - Tiêu đề dùng Google Sans, VIẾT HOA, đậm (700–900).
  - Nội dung dùng Inter.
  - Phân cấp chính/phụ rõ: tiêu đề đậm, điểm nhấn đậm và có màu, chữ phụ nhạt hơn.
- **Tông màu mặc định:** SÁNG, kiểu glass xanh-trắng.
  - Tiêu đề navy `#0B1A4A`, nhấn xanh `#1557F0`, phụ đỏ/cam/xanh lá/tím theo phần.
  - Các sếp chê nền tối (navy) là "tối quá". Chỉ làm tối khi được yêu cầu.
- **Nền:**
  - Đơn giản, chuyển động CHẬM và THƯA (mạch vi điện tử mờ).
  - KHÔNG dùng lưới tổ ong (rối mắt).
  - KHÔNG có đường quét chạy ngang (chóng mặt).
  - KHÔNG có các ô vuông chip trắng.
- **Logo MISA:** ở góc trên phải mọi trang. Riêng trang bìa và trang kết thì logo to, đặt giữa.
- **Trang kết:** khiên (shield) SVG chuyển động bao quanh logo. Không dùng vòng tròn lan toả.
- **Nhãn góc trên trái** (kiểu "PHẦN 2 · CẬN CẢNH"): người dùng đã BỎ. Không thêm.

## Chữ

- **Không để dòng cuối của tiêu đề chỉ có 1 từ** (mồ côi). Dùng `&nbsp;` hoặc viết lại cho cân.
- **Không để chữ tràn khỏi thẻ/shape.** Luôn chạy `check_layout.mjs` và xem bằng mắt.
- **Icon không được đè lên chữ.**
- **Giữ nguyên nội dung gốc** khi người dùng yêu cầu. Chỉ đổi cách trình bày.

## Ảnh

- **Ảnh AI:** đặt nguyên ảnh nền trắng trên thẻ trắng bo 4 góc. KHÔNG tách nền tự động (đã lỗi, người dùng không chấp nhận).
- **Prompt chuẩn cho misa-glass** (Gemini `gemini-3-pro-image`, tỉ lệ 4:3 hoặc 1:1). Theme khác: lấy đuôi prompt ở `themes.md` › Phong cách ảnh.

  > `<chủ thể cụ thể, ẩn dụ của nội dung trang>`. Soft 3D clay illustration, glossy rounded shapes, bright cheerful pastel palette dominated by sky blue, white and light mint with small coral-red accents, single centered subject with generous empty margin, isolated on a pure flat white background (#FFFFFF), soft contact shadow, premium product-render quality, absolutely no text, no letters, no numbers, no logos, no watermark

## Video và bút chiếu

- **Bút chiếu phải luôn next được.** Luồng ở trang video:
  1. Tới trang: video CHƯA chạy, chỉ hiện khung hình đầu + nút play.
  2. Next lần 2: phát TOÀN MÀN HÌNH, đủ tiếng.
  3. Next lần 3: tắt video và sang trang.
  4. Back khi đang phát: chỉ đóng video. Video hết thì tự đóng.
- **Nén video:** H.264 CRF 25, video dài/nặng dùng CRF 27; ≤1080p; AAC. Ví dụ: video 310 MB còn 61 MB mà vẫn nét.
- **Nhúng base64 nhưng giải mã theo khúc thành Blob.** Data URL vài chục MB làm Safari không phát được (đã gặp).
- **Ghi nguồn video** (ví dụ "Nguồn: Hiếu PC"): đặt góc trên phải khung video, ngang hàng tiêu đề, cỡ 21px.
- **Nặng file:** 5 video khoảng 100 MB thì file HTML khoảng 130 MB. Báo người dùng mở file sớm vài giây.

## Bộ đếm "từ lúc mở slide…"

- Chỉ con số đỏ chạy. Chữ xám bên cạnh phải ĐỨNG YÊN, nên số cần độ rộng cố định và tabular-nums.

## Chế độ sửa (người dùng tự sửa không cần người kỹ thuật)

- **Mở và lưu:**
  - Phím E bật/tắt chế độ sửa.
  - Ctrl+S lưu thành file mới. Hướng dẫn người dùng trình chiếu bằng file vừa lưu.
- **Định dạng chữ** (thanh dưới đáy):
  - Cỡ chữ, dãn dòng, xuống dòng.
  - B/I/U, màu nhấn, tô nền.
  - Căn trái/giữa/phải/đều; VIẾT HOA/thường.
- **Ảnh chèn thêm:**
  - Kéo-thả, Ctrl+V hoặc nút "Chèn ảnh".
  - Kéo để di chuyển, kéo góc để đổi cỡ, kéo nút trên để xoay.
  - Chỉnh sáng/tối, bo góc, viền + màu, đổ bóng, lên trên/ra sau chữ.
- **Video:** bấm hoặc kéo-thả file vào khung video.
- **Bố cục** (phím M hoặc nút "✥ Bố cục" trên thanh sửa; M lần nữa quay lại sửa chữ):
  - Bấm vào bất kỳ chữ / hình / thẻ nào để chọn (viền tím). Bấm trúng phần nhỏ bên trong thì nhấn Q (hoặc Alt+bấm) để chọn khối lớn hơn chứa nó.
  - Kéo để di chuyển; mũi tên dịch từng chút (Shift = 10px); + / − phóng to, thu nhỏ; Delete xoá.
  - "Về chỗ cũ" trả khối về vị trí và cỡ ban đầu; "Hiện lại khối đã xoá" lấy lại mọi khối đã xoá trên trang đang xem.
  - Lưu trong `EDITS.blocks["trang:thứ tự"] = {x, y, sc, del}` (CSS `translate`/`scale`, không đụng hiệu ứng vào). Khối đánh số theo DOM gốc của từng trang → sửa `slides.html` rồi build lại thì chỉnh sửa bố cục cũ có thể lệch khối; khi người dùng đã tự sửa, làm tiếp trên chính file của họ.

## Xuất PDF

- Không có hiệu ứng. Chụp từng trang ở trạng thái cuối, nét 1.5×.
- PDF không phát video tại chỗ. Gắn link tương đối tới `video/video-trang-NN.mp4` và phải gửi kèm thư mục `video/`.
