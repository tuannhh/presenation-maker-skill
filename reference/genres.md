# Thể loại bài trình chiếu: cấu trúc, bố cục, giọng văn

Mỗi mục là khung gợi ý, không phải luật cứng. Tên bố cục khớp với `components.md` (v2) và `patterns.md` (gốc). Quy tắc chung cho mọi thể loại:

- **Mỗi trang một ý.** Tiêu đề là một câu kết luận ("Doanh thu tăng 32% nhờ kênh số"), không phải nhãn ("Doanh thu").
- **≤ 6 dòng chữ, ≤ 12 từ mỗi dòng** trên một trang; phần còn lại cho vào ghi chú (`notes.json`).
- **Đổi nhịp bố cục**: không quá 2 trang liền cùng kiểu. Chèn `statement`, `quote`, `split` ảnh, trang phần để "thở".
- **Số liệu phải có so sánh** (với kỳ trước, mục tiêu, đối thủ) và một câu "vì thế nên…".
- Trang cuối luôn có hành động tiếp theo hoặc lời cảm ơn + liên hệ.

---

## 1. Đào tạo nội bộ / bài giảng / e-learning
**Theme:** `playful-edu` (vui, nhân viên trẻ, trẻ em), `misa-glass` (doanh nghiệp), `nature-green` (sức khoẻ, mầm non). **Motion:** normal.
**Khung (15–30 trang):** bìa → mục tiêu buổi học (`checks`) → `agenda` → mỗi bài: trang phần (`sect`) → khái niệm (thẻ `card` + `ib` icon, hoặc `split` ảnh) → ví dụ / tình huống (`ba` trước-sau, `quote`) → các bước làm (`proc`, `vtl`) → lỗi hay gặp (`mx` hoặc thẻ đỏ) → câu hỏi kiểm tra nhanh (`statement` "Bạn sẽ làm gì nếu…?") → tóm tắt (`checks`) → `thanks` + tài liệu tham khảo.
**Giọng:** gần gũi, "bạn", câu ngắn, ví dụ đời thường. Mỗi bài kết bằng 1 câu "nhớ được".
**Mẹo:** dùng `data-stagger` để hiện từng ý khi giảng; trang câu hỏi dùng `slot`/`data-type` để tạo bất ngờ.

## 2. Pitch gọi vốn (investor pitch)
**Theme:** `bold-pitch` (startup, mạnh mẽ) hoặc `clean-minimal` (nghiêm túc), `vivid-gradient` (consumer). **Motion:** lively.
**Khung (10–15 trang, chuẩn Sequoia):** bìa (1 câu tầm nhìn) → vấn đề (`statement` + `hero-num` quy mô nỗi đau) → giải pháp (`split` ảnh sản phẩm) → vì sao bây giờ (`tl` timeline xu hướng) → quy mô thị trường TAM/SAM/SOM (`ring` hoặc `pyr`) → sản phẩm/demo (video hoặc `photos`) → mô hình kinh doanh (`plans`) → traction (`kpis` + `lchart`) → cạnh tranh (`mx` 2×2 hoặc bảng `tbl`) → đội ngũ (`team`) → tài chính & kế hoạch (`cols` + `vtl`) → số vốn cần & dùng vào đâu (`hbars`) → `thanks` + liên hệ.
**Giọng:** tự tin, con số cụ thể, không tính từ sáo rỗng. Mỗi trang trả lời 1 câu hỏi nhà đầu tư sẽ hỏi.

## 3. Bán hàng / giới thiệu giải pháp cho khách
**Theme:** `misa-glass`, `clean-minimal`, hoặc theme màu thương hiệu khách (`palette`). **Motion:** normal.
**Khung (12–20 trang):** bìa (tên khách + giá trị) → khách đang gặp gì (`ba-before` hoặc thẻ đỏ) → chi phí của việc không thay đổi (`hero-num`) → giải pháp (`split`) → tính năng theo lợi ích (lưới `card` 3–6 thẻ) → cách hoạt động (`proc`) → kết quả khách hàng khác (`quote` + `kpis`) → so sánh (`tbl` hoặc `ba`) → bảng giá (`plans`) → lộ trình triển khai (`tl`) → bước tiếp theo (`checks`) → `thanks`.
**Giọng:** nói về khách trước, sản phẩm sau. "Anh/chị sẽ…" thay vì "Chúng tôi có…".

## 4. Báo cáo kết quả quý / năm, họp điều hành
**Theme:** `clean-minimal` (HĐQT), `misa-glass` (nội bộ), `editorial` (báo cáo dài). **Motion:** calm.
**Khung (10–25 trang):** bìa → tóm tắt điều hành (`statement` 1 câu + `kpis` 3–4 số) → mỗi mảng: trang phần → số chính (`kpis`, `hbars`, `cols`, `lchart`) → giải thích nguyên nhân (thẻ hoặc `note`) → điều làm tốt / chưa tốt (`ba` hoặc `mx`) → rủi ro (`mx` SWOT) → kế hoạch kỳ tới (`vtl` + `checks`) → đề xuất cần quyết (`statement`) → `thanks`.
**Giọng:** kết luận trước, số liệu sau. Mọi biểu đồ có 1 câu takeaway ở tiêu đề. Ghi nguồn số liệu bằng `.src`.

## 5. Ra mắt sản phẩm / keynote
**Theme:** `vivid-gradient`, `midnight-tech` (sản phẩm số), `bold-pitch`. **Motion:** lively.
**Khung (12–25 trang):** bìa kịch tính → câu chuyện bối cảnh (`statement`) → vấn đề (`hero-num`) → "Giới thiệu…" (trang phần + `th-big` tên sản phẩm, hiệu ứng `slam`) → video demo → 3 điểm khác biệt (mỗi điểm 1 trang `split` ảnh) → thông số (`kpis` / `ring`) → khách dùng thử nói gì (`quote`) → giá & phiên bản (`plans`) → ngày ra mắt (`hero-num` hoặc `tl`) → `thanks` + QR/link.
**Giọng:** ngắn, nhiều khoảng trống, 1 câu mạnh mỗi trang. Dùng ảnh tràn và video nhiều hơn chữ.

## 6. Gala / vinh danh / tất niên / kỷ niệm
**Theme:** `luxury-gold` (trang trọng), `vivid-gradient` (trẻ, sôi động), `playful-edu` (gia đình, vui). **Motion:** calm (luxury) / lively (vivid).
**Khung:** bìa (tên sự kiện, chữ `script` cho lời chào) → chương trình (`agenda` hoặc `vtl`) → nhìn lại năm (`tl` + `photos`) → con số đáng nhớ (`kpis` / `hero-num`) → mỗi hạng mục giải: trang phần ("Giải thưởng …") → người đạt giải (`team` hoặc `split` ảnh chân dung + `quote` cảm nghĩ) → lời tri ân (`statement`) → video kỷ niệm → `thanks` + lời chúc.
**Giọng:** cảm xúc, trang trọng, tên người viết đầy đủ. Đọc lại tên người/chức danh 2 lần.
**Mẹo:** dùng `data-a="slam"` cho tên người đạt giải, `slot` để "quay số" công bố.

## 7. Workshop / hội thảo tương tác
**Theme:** `playful-edu`, `clean-minimal`, `nature-green`. **Motion:** normal.
**Khung:** bìa → mục tiêu + quy tắc (`checks`) → `agenda` có giờ → mỗi hoạt động: trang phần → đề bài (`statement`) → hướng dẫn từng bước (`proc`) → thời gian (`hero-num` "15 phút") → khung thảo luận (`mx` 2×2 trống để điền) → tổng kết (`checks`) → cam kết hành động → `thanks`.
**Giọng:** câu hỏi mở, động từ mệnh lệnh nhẹ ("Hãy thử…", "Thảo luận nhóm…").

## 8. Đề xuất dự án / xin phê duyệt
**Theme:** `clean-minimal`, `misa-glass`, `editorial`. **Motion:** calm.
**Khung (8–15 trang):** bìa → đề xuất trong 1 câu + số tiền/thời gian (`statement`) → bối cảnh & vấn đề (`kpis` hoặc `hbars`) → phương án (`mx` hoặc `tbl` so sánh 2–3 phương án) → phương án chọn (`split`) → lợi ích đo được (`kpis`, `ring`) → chi phí & ROI (`cols`, `tbl`) → kế hoạch (`tl`) → rủi ro & cách giảm (`mx`) → nhân sự (`team`) → điều cần phê duyệt (`checks`) → `thanks`.
**Giọng:** chính xác, có số, có phương án dự phòng. Trang 2 phải đủ để người duyệt quyết.

## 9. Onboarding nhân sự / văn hoá công ty
**Theme:** `playful-edu`, `misa-glass`, `nature-green`. **Motion:** normal.
**Khung:** chào mừng (`cover` + `script`) → câu chuyện công ty (`tl`) → sứ mệnh/giá trị (`statement` + lưới `card` icon) → sơ đồ tổ chức (`team` / `pyr`) → tuần đầu tiên (`vtl`) → công cụ & quy trình (`proc`, `checks`) → quyền lợi (`card` + `ib`) → ai hỗ trợ bạn (`team`) → FAQ (`mx`) → `thanks` + liên hệ.
**Giọng:** ấm áp, "chào mừng bạn", tránh thuật ngữ nội bộ chưa giải thích.

## 10. Kể chuyện / case study / truyền cảm hứng
**Theme:** `editorial`, `nature-green`, `luxury-gold`. **Motion:** calm.
**Khung (cấu trúc 3 hồi):** bìa → nhân vật & bối cảnh (`split` ảnh) → thách thức (`hero-num` hoặc `statement`) → bước ngoặt (`quote`) → hành trình (`vtl` / `tl`) → kết quả (`kpis`, `ba`) → bài học (`checks`) → thông điệp (`statement`) → `thanks`.
**Giọng:** kể chuyện, chi tiết cụ thể (tên, nơi, thời gian), trích lời thật.

## 11. Tech talk / chia sẻ kỹ thuật
**Theme:** `midnight-tech`, `clean-minimal`. **Motion:** normal.
**Khung:** bìa → "Hôm nay bạn sẽ biết…" (`checks`) → vấn đề (`statement` + số đo hiệu năng `kpis`) → kiến trúc cũ/mới (`ba` hoặc `split` sơ đồ) → giải thích từng phần (`proc`, `code` khối mã) → benchmark (`cols`, `hbars`, `lchart`) → bài học / cạm bẫy (`mx`) → roadmap (`vtl`) → `thanks` + repo/link.
**Giọng:** chính xác, ví dụ code ngắn (≤ 12 dòng/khối), luôn kèm con số đo được.
**Mẹo:** `.code` có tô màu bằng span `.k .s .n .c .f`; font mono tự nhúng khi có dùng.

## 12. Tuyên truyền / cảnh báo / nâng cao nhận thức (như bài lừa đảo)
**Theme:** `misa-glass` (đã kiểm chứng), `midnight-tech` (an ninh mạng). **Motion:** normal.
**Khung:** bìa → con số gây sốc (`hero-num` / bộ đếm `data-live`) → video thật → các kiểu thủ đoạn (trang phần + thẻ lưới, `slot`) → dấu hiệu nhận biết (`checks`, `ib` icon) → cách phòng tránh (`proc`) → làm gì khi đã bị (`vtl`) → thông điệp nhớ (`statement`) → trang kết có khiên.
**Giọng:** cụ thể, ví dụ thật, kêu gọi hành động rõ. Xem `lessons.md` (rút từ bài thật).
