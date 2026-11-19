# Danh mục theme

Đổi theme = đổi `"theme"` trong `deck.json` rồi build lại; cùng một `slides.html` chạy được với mọi theme. Xem tận mắt cả 15 bản:

```bash
"$PY" $SK/scripts/preview_themes.py <thư-mục-ra> [--slides src/slides.html] [--themes a,b] [--logo none]
```

## Chọn nhanh

| Theme | Cảm giác | Hợp nhất cho | Font (tiêu đề / nội dung) | Nền | Nhịp |
|---|---|---|---|---|---|
| `misa-glass` (mặc định) | sáng, kính mờ xanh-trắng, mạch điện tử | bài nội bộ MISA, tuyên truyền, đào tạo doanh nghiệp, báo cáo | Google Sans / Inter | circuit + khiên ở trang kết | vừa, mềm |
| `midnight-tech` | navy tối, neon cyan | công nghệ, AI, bảo mật, dữ liệu, tech talk, hội thảo kỹ thuật | Space Grotesk / Inter | circuit (tối) | vừa |
| `clean-minimal` | trắng, chữ to, phẳng, Swiss | báo cáo điều hành, họp HĐQT, chiến lược, tài chính, tư vấn | Be Vietnam Pro / Inter | none | nhanh, gọn, không blur |
| `editorial` | giấy kem, chữ có chân, kẻ chỉ | báo cáo chuyên sâu, nghiên cứu, kể chuyện, case study, văn hoá | Playfair Display / Lora | paper (vân giấy) | chậm, fade |
| `playful-edu` | tươi, bo tròn, confetti | đào tạo, bài giảng, giáo dục, trẻ em, team building, sự kiện nội bộ | Baloo 2 / Nunito | confetti | nảy, vui |
| `bold-pitch` | neo-brutalism: viền đen dày, bóng cứng, màu rực | pitch gọi vốn, marketing, sáng tạo, startup, ra mắt chiến dịch | Oswald / Space Grotesk | dots | nhanh, zoom, wipe |
| `luxury-gold` | đen + vàng ánh kim, thanh lịch | gala, vinh danh, tất niên, kỷ niệm thành lập, tri ân khách hàng VIP | Cormorant Garamond / Montserrat (+ Dancing Script) | stars | chậm, sang |
| `nature-green` | xanh lá, be, sóng mềm | ESG, CSR, môi trường, sức khoẻ, nông nghiệp, thực phẩm, giáo dục mầm non | Lora / Be Vietnam Pro | waves | chậm, êm |
| `vivid-gradient` | nền tối, gradient tím-hồng-cyan rực, glass | ra mắt sản phẩm, sự kiện trẻ, âm nhạc, Gen Z, khởi động năm mới | Montserrat / Inter | mesh | vừa, zoom |
| `ava-lavender` | sáng, lavender tím-hồng, dải lụa, sóng chấm trắng, chữ gradient | sản phẩm AI, ra mắt chatbot/mascot, marketing, khán giả trẻ | Montserrat / Be Vietnam Pro (+ Dancing Script) | blobs + lụa + sóng chấm | vừa, mềm |
| `corporate-navy` | trắng + navy đậm + vàng đồng, kẻ chỉ mảnh, thẻ phẳng góc vuông | ngân hàng, tài chính, báo cáo thường niên, họp HĐQT/đại hội cổ đông, cơ quan nhà nước | Barlow / Roboto | grid rất nhạt + dải navy-vàng trên đỉnh | gọn, fade, không blur |
| `mono-keynote` | gần đen, chữ trắng rất to, mỗi trang một màu nhấn, nhiều khoảng trống | keynote sân khấu, ra mắt sản phẩm, tầm nhìn, diễn giả | Inter / Inter | none (vệt sáng sân khấu nhẹ) | chậm, fade |
| `sunset-warm` | kem ấm, san hô / cam / đào / hồng, bo tròn mềm, mặt trời kẻ sọc | nhân sự, văn hoá doanh nghiệp, cộng đồng, marketing, bán lẻ, F&B | Montserrat / Open Sans | blobs ấm + mặt trời | vừa, rise |
| `chalkboard` | bảng xanh rêu, khung gỗ, chữ phấn, phấn màu pastel, viền nét đứt | giảng dạy, lớp học, workshop, đào tạo, chia sẻ kiến thức | Baloo 2 / Nunito | mesh (bụi phấn) + hình vẽ phấn ở lề | vừa, không blur |
| `ocean-fresh` | sáng, xanh biển / ngọc / da trời, sóng mềm, thẻ kính trong | logistics, y tế, du lịch, nước & biển, SaaS | Barlow / Open Sans | waves + đường sóng mảnh | vừa, mềm |

Gợi ý theo khán giả: lãnh đạo cấp cao → `clean-minimal` / `editorial` / `corporate-navy`; ngân hàng, tài chính, cơ quan nhà nước → `corporate-navy`; nhân viên nội bộ → `misa-glass` / `playful-edu` / `sunset-warm`; học viên, lớp học, workshop → `chalkboard` / `playful-edu`; nhà đầu tư → `bold-pitch` / `clean-minimal`; dev/kỹ sư → `midnight-tech`; khán giả sân khấu lớn → `mono-keynote`; người trẻ, sản phẩm AI → `ava-lavender` / `vivid-gradient`; khách hàng y tế, logistics, du lịch → `ocean-fresh`; khách mời sự kiện → `luxury-gold` / `vivid-gradient`.

Theme tối (`midnight-tech`, `luxury-gold`, `vivid-gradient`, `mono-keynote`, `chalkboard`) tự đặt logo trên nền sáng bo góc (`logo_plate`). Logo đã có bản trắng thì đặt `"logo_plate": false`.

## Màu phần (palette)

Mỗi theme có 6 màu cho `data-p` 1..6, dùng qua `c-p1..c-p6` (thẻ, chip, icon, cột…) và `.hl` (chữ nhấn theo phần của trang). Màu cố định `c-blue c-red c-green c-violet c-amber` vẫn dùng được nhưng KHÔNG đổi theo theme — chỉ dùng khi màu mang nghĩa (đỏ = xấu, xanh lá = tốt, như SWOT).

| Theme | p1 | p2 | p3 | p4 | p5 | p6 |
|---|---|---|---|---|---|---|
| misa-glass | #1557F0 | #E3263A | #0B9A62 | #5A3FE6 | #DE8A00 | #0891B2 |
| midnight-tech | #4D8BFF | #2EE6F6 | #18D48F | #A08CFF | #FFB224 | #FF4D6A |
| clean-minimal | #2448F5 | #E5484D | #12A150 | #7C5CFF | #E08A00 | #0E7490 |
| editorial | #B3261E | #1F3A5F | #2F6B4F | #6B4C8A | #B86E00 | #3D5A6C |
| playful-edu | #3B82F6 | #F97316 | #22C55E | #A855F7 | #EAB308 | #EC4899 |
| bold-pitch | #2B59FF | #FF5A36 | #00A86B | #8B5CF6 | #F5B700 | #FF4FA3 |
| luxury-gold | #D4AF37 | #E2B8A0 | #8FCFB2 | #B9A4E8 | #F0C987 | #9EC5F0 |
| nature-green | #2F7D4F | #C2643A | #3A7CA5 | #7D8F2E | #B5884B | #6B5B95 |
| vivid-gradient | #8B6CFF | #FF4D9D | #22D3EE | #FFB547 | #3DDC97 | #5B8CFF |
| ava-lavender | #7B3FF2 | #E0367F | #4B5CFF | #0A9BB0 | #D9720F | #11996C |
| corporate-navy | #1B4B8F | #A8741A | #1F7A55 | #8C2A3C | #4E5D7E | #13707E |
| mono-keynote | #4C9BFF | #FF6B3D | #3FD68F | #B78CFF | #FFC23D | #FF5A8A |
| sunset-warm | #E8572F | #D93A6E | #1E8C86 | #8E4DB0 | #C96F0E | #3E6FB0 |
| chalkboard | #F7DC6F | #F5A3C0 | #9FD3F5 | #A8E6B8 | #F8B878 | #C9B3F2 |
| ocean-fresh | #0A78BE | #0E9A9A | #3B5FD9 | #E5594B | #C98307 | #0F9A6A |

Thương hiệu khách có màu riêng: giữ theme, ghi đè `"palette": ["#...", ...]` trong `deck.json`.

## Phong cách ảnh minh hoạ theo theme

Ghép `<chủ thể cụ thể, ẩn dụ nội dung trang>. ` + đuôi prompt dưới đây. Luôn kết thúc bằng `absolutely no text, no letters, no numbers, no logos, no watermark`. Ảnh minh hoạ (`data-im`) dùng nền trắng phẳng; ảnh tràn (`data-ph`) là ảnh chụp/cảnh, tỉ lệ 16:9 hoặc 4:5.

| Theme | Đuôi prompt cho `data-im` (minh hoạ) | Gợi ý cho `data-ph` (ảnh tràn) |
|---|---|---|
| misa-glass | Soft 3D clay illustration, glossy rounded shapes, bright cheerful pastel palette dominated by sky blue, white and light mint with small coral-red accents, single centered subject with generous empty margin, isolated on a pure flat white background (#FFFFFF), soft contact shadow, premium product-render quality | ảnh văn phòng sáng, người thật, tông xanh-trắng |
| midnight-tech | Isometric 3D render, dark navy glass and brushed metal with glowing cyan and electric blue edge lights, holographic UI fragments, single centered subject, isolated on a pure flat white background (#FFFFFF), crisp studio lighting | phòng server, màn hình code, ánh neon xanh, chụp tối |
| clean-minimal | Minimal flat vector illustration, geometric shapes, limited palette of one strong blue with light grey and black, lots of negative space, single centered subject, isolated on a pure flat white background (#FFFFFF) | ảnh kiến trúc tối giản, nhiều khoảng trống, đen trắng hoặc ít màu |
| editorial | Elegant editorial illustration in the style of a vintage engraving with muted watercolor washes, cream, deep red and navy ink, fine line hatching, single subject, isolated on a pure flat white background (#FFFFFF) | ảnh phóng sự, ánh sáng tự nhiên, hạt film, tông ấm |
| playful-edu | Cute 3D cartoon illustration, chunky rounded shapes, saturated candy colors (blue, orange, green, purple, yellow), friendly expressive characters, single centered subject, isolated on a pure flat white background (#FFFFFF), soft shadow | ảnh lớp học, trẻ em, hoạt động nhóm, màu tươi |
| bold-pitch | Bold flat illustration with thick black outlines and hard offset shadow, neo-brutalist poster style, saturated blue, orange-red and yellow, single subject, isolated on a pure flat white background (#FFFFFF) | ảnh sản phẩm/nhân vật nền màu trơn, tương phản mạnh |
| luxury-gold | Luxurious 3D render of polished gold and black onyx, soft caustic reflections, elegant minimal composition, single centered object, isolated on a pure flat white background (#FFFFFF), studio product lighting | ảnh sân khấu, đèn vàng ấm, bokeh, tối và sang |
| nature-green | Soft watercolor and gouache botanical illustration, sage green, terracotta and warm beige, organic shapes, gentle texture, single subject, isolated on a pure flat white background (#FFFFFF) | ảnh thiên nhiên, cánh đồng, lá cây, ánh nắng sớm |
| vivid-gradient | Glossy 3D abstract render, iridescent chrome and glass with vivid violet, hot pink and cyan gradients, dreamy lighting, single centered object, isolated on a pure flat white background (#FFFFFF) | ảnh concert/đám đông, ánh đèn màu, chuyển động |
| ava-lavender | Soft glossy 3D render, rounded friendly shapes, pastel lavender, pink and periwinkle blue with white highlights, dreamy soft lighting, single centered subject with generous empty margin, isolated on a pure flat white background (#FFFFFF), soft contact shadow | ảnh người trẻ dùng điện thoại/laptop, ánh sáng tím-hồng dịu |
| corporate-navy | Clean corporate 3D render, matte navy blue and white materials with small brushed-gold accents, precise geometric forms, single centered subject, isolated on a pure flat white background (#FFFFFF), soft studio lighting | ảnh toà nhà văn phòng, phòng họp, bắt tay, tông navy-xám, trang trọng |
| mono-keynote | Minimal dramatic product render, matte black and graphite with one glowing accent light, high contrast studio lighting, single centered object, isolated on a pure flat white background (#FFFFFF) | ảnh sân khấu tối, một luồng đèn, diễn giả bóng đen, nhiều khoảng tối |
| sunset-warm | Warm friendly 3D illustration, soft rounded shapes, coral, peach, orange and rose palette, cozy golden-hour lighting, single centered subject, isolated on a pure flat white background (#FFFFFF), soft shadow | ảnh con người, đồng nghiệp cười, cộng đồng, nắng chiều ấm |
| chalkboard | Hand-drawn chalk illustration look, simple outlined doodle with soft pastel chalk fills (yellow, pink, light blue), playful classroom style, single subject, isolated on a pure flat white background (#FFFFFF) | ảnh lớp học, bàn học, sách vở, người học tập trung |
| ocean-fresh | Clean glossy 3D render, translucent glass and water-like materials in aqua, teal and sky blue with white, fresh airy lighting, single centered subject, isolated on a pure flat white background (#FFFFFF), soft shadow | ảnh biển, cảng, tàu hàng, bệnh viện sáng sủa, bầu trời trong |

Ảnh minh hoạ luôn đặt nguyên nền trắng trên thẻ bo góc (`.im`), KHÔNG tách nền.

## Tuỳ biến nhanh trong deck.json (không cần theme mới)

```json
{
  "theme": "clean-minimal",
  "palette": ["#0F766E", "#DC2626", "#2563EB", "#9333EA"],
  "fonts": {"head": "montserrat", "body": "inter"},
  "bg": "grid",
  "motion": "calm",
  "title_case": "none",
  "colors": {"ink": "#0B1F33"},
  "logo": "assets/logo-khach.png"
}
```

- `fonts`: khoá trong `fonts/fonts.json`: `google-sans inter be-vietnam-pro montserrat playfair lora cormorant nunito baloo space-grotesk oswald lexend barlow roboto open-sans jetbrains-mono dancing-script`. Có `mono` (khối code) và `script` (chữ viết tay, class `.script`).
- `bg`: `circuit blobs dots grid paper mesh waves stars confetti none`.
- `motion`: `"calm"` (chậm 1.3×), `"normal"`, `"lively"` (nhanh 0.8×), `"none"` (gần như không hiệu ứng, cho máy yếu/in) hoặc object `{speed, blur, enter, big}`; `enter` (trang thường) và `big` (bìa, trang phần, statement, cảm ơn) nhận mọi kiểu dưới đây.
  - Một lớp (chỉ trang mới chuyển động): `slide fade zoom rise cut`, `circle wipe` (hợp trang lớn).
  - Hai lớp (trang cũ và mới cùng chuyển động): `prezi` (lùi xa, lướt sang trang mới, zoom vào; hướng đổi theo số trang), `cube` (khối lập phương xoay), `flip` (lật thẻ), `zoomin` (bay xuyên vào trang), `stack` (rút thẻ trên cùng ra), `parallax` (đẩy có chiều sâu), `swirl` (xoáy).
  - `mix`: luân phiên các kiểu hai lớp theo số trang.
  - Riêng một trang: `<section class="slide" data-tr="cube">` (ghi đè `enter`/`big`).
  - Gợi ý: bài sự kiện, ra mắt sản phẩm dùng `{"enter":"prezi","big":"zoomin"}`; báo cáo, đào tạo giữ `slide`/`fade` và chỉ đặt `data-tr` cho vài trang chuyển phần.
- `title_case`: `"upper"` hoặc `"none"` (tiêu đề `.t` có viết HOA hay không).
- `colors`: ghi đè token bất kỳ (bỏ dấu `--`).
- `logo`: đường dẫn ảnh, hoặc `null` để bỏ logo hoàn toàn.
- `shield`: bật/tắt khiên SVG quanh logo ở trang kết (mặc định chỉ bật ở misa-glass).

## Tạo theme mới

1. Trong dự án: tạo `themes/themes.json` với một mục mới (build gộp với danh mục của skill, dự án được ưu tiên):

```json
{ "brand-x": { "label": "Brand X — …", "fonts": {"head": "montserrat", "body": "inter"},
  "bg": "blobs", "dark": false, "palette": ["#..", "#..", "#..", "#.."],
  "motion": {"speed": 1, "blur": true, "enter": "slide", "big": "circle"} } }
```

2. Tạo `themes/brand-x.css`. Bắt đầu bằng `:root{…}` đổi token, chép một theme gần giống làm mẫu:
   - nền: `--bg`, `#stage{background:…}`; chữ: `--ink` (tiêu đề), `--text` (nội dung), `--muted`, `--line`;
   - thẻ: `--surface`, `--surface2`, `--cardbg`, `--cardline`, `--shadow`, `--shadow-lg`, `--radius`, `--rsm`, `--blur`;
   - nhấn: `--blue` (màu chính), `--accent2`, `--g1`/`--g2` (gradient chữ bìa), `--hi`, `--onc` (chữ trên nền màu đặc);
   - kiểu tiêu đề: `--tt` (`uppercase`/`none`).
3. Rồi mới chỉnh chi tiết riêng: `.card`, `.t`, `.hl`, `.t-bar`, `.cover .ttl`, `.sect .stitle`, `.banner`, `.kpi`, `.plan.feat`… (xem `bold-pitch.css`, `editorial.css` để thấy cách "đổi tính cách" bằng viền, bóng, chữ nghiêng).
4. Font mới: thả file `.ttf/.woff2` vào `assets/fonts/` của dự án, chép `$SK/fonts/fonts.json` vào cùng chỗ rồi thêm mục mới `{"family": "…", "files": [["Ten.ttf", "400"], ["Ten-Bold.ttf", "700"]]}` (font variable: `[["Ten[wght].ttf", "300 800"]]`). File `fonts.json` của dự án thay hẳn bản của skill, còn file font cũ vẫn được tìm ở thư mục skill. Kiểm tra font có đủ dấu tiếng Việt (build báo "thiếu N ký tự").
5. `"$PY" $SK/scripts/preview_themes.py out --slides src/slides.html --themes brand-x` hoặc build + `contact_sheet.mjs` → xem từng trang: chữ trên nền màu, badge, bảng, code, trang tối/sáng.

Lỗi hay gặp khi làm theme: chữ trên nền màu đặc bị trùng màu (`--onc`), selector `.plan.feat *` / `.x *` đè màu con (tăng độ ưu tiên bằng `.slide …`), theme tối quên `--surface` tối khiến thẻ trắng loá.
