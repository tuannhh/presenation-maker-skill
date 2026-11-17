# html-presentation-skill-claude

Skill cho **Claude Code**: dựng bài trình chiếu thành **một file HTML tự chứa** (font, ảnh, logo, video nhúng sẵn; mở offline trên máy bất kỳ), với **9 phong cách** và playbook cho **12 thể loại** bài.

## Tính năng

- **9 theme** đổi bằng một dòng trong `deck.json`: `misa-glass` (mặc định) · `midnight-tech` · `clean-minimal` · `editorial` · `playful-edu` · `bold-pitch` · `luxury-gold` · `nature-green` · `vivid-gradient`. Mỗi theme có font, bảng màu, nền động và nhịp hiệu ứng riêng. Tuỳ biến thêm: palette, font, nền, tốc độ hiệu ứng, logo — hoặc tự tạo theme mới.
- **Thư viện bố cục**: agenda, statement, KPI đếm số, vòng %, thanh ngang, cột, đường, timeline ngang/dọc, quy trình, trích dẫn, ảnh tràn nửa trang, đội ngũ, bảng giá, trước/sau, SWOT, kim tự tháp, khối mã, cảm ơn… cộng 38 trang mẫu gốc. 159 icon.
- **Playbook theo thể loại** (`reference/genres.md`): đào tạo, pitch gọi vốn, bán hàng, báo cáo, ra mắt sản phẩm, gala/vinh danh, workshop, đề xuất dự án, onboarding, case study, tech talk, tuyên truyền.
- **Hiệu ứng chuyển động** khi vào trang và chuyển trang (theo theme).
- **Điều khiển bằng bút chiếu.** Ở trang video: next lần 1 hiện khung, lần 2 phát toàn màn hình có tiếng, lần 3 sang trang.
- **Chế độ sửa tại chỗ** (phím **E**): sửa/định dạng chữ, chèn/kéo/xoay/chỉnh ảnh, gắn video; **Ctrl+S** lưu file mới.
- **Script kèm theo**: đọc PPTX, xem trước mọi theme, chụp contact sheet để rà nhanh, rà lỗi bố cục, sinh ảnh minh hoạ (Gemini/Vertex AI), nén video, xuất PDF có link video, bỏ trang trên file đã tự sửa.

Bộ khung lấy từ một bài thật ("Xu hướng lừa đảo và cách phòng tránh", MISA, 11/2026) đã qua nhiều vòng góp ý; các góp ý được ghi thành quy tắc trong `reference/lessons.md`.

## Cài đặt

macOS / Linux:
```bash
git clone https://github.com/tuannhh/html-presentation-skill-claude.git ~/.claude/skills/misa-html-deck
bash ~/.claude/skills/misa-html-deck/scripts/setup.sh
```

Windows (Git Bash):
```bash
git clone https://github.com/tuannhh/html-presentation-skill-claude.git ~/.claude/skills/misa-html-deck
VENV_DIR=D:/venvs/misa-html-deck bash ~/.claude/skills/misa-html-deck/scripts/setup.sh
```
(`VENV_DIR` tuỳ chọn: đặt venv ở ổ khác rồi nối vào `.venv` bằng junction.)

**Yêu cầu:** Python 3.10+; Node ≥ 22 và Chrome hoặc Edge (xuất PDF, contact sheet, rà bố cục); ffmpeg (nén video).

## Dùng

Trong Claude Code, gọi `/misa-html-deck` hoặc nói tự nhiên, ví dụ: *"làm bài pitch gọi vốn 12 trang phong cách bold"*, *"chuyển file PPTX này thành slide HTML kiểu tạp chí"*. Quy trình chi tiết ở `SKILL.md`.

Xem trước 9 theme:
```bash
~/.claude/skills/misa-html-deck/.venv/Scripts/python.exe ~/.claude/skills/misa-html-deck/scripts/preview_themes.py ./theme-preview
```
(macOS/Linux: `.venv/bin/python`.) Mở `theme-preview/index.html`.

Sinh ảnh minh hoạ cần một file service account Google Cloud có quyền Vertex AI, đặt đường dẫn vào biến `MISA_GEMINI_SA`. **Không commit file khoá vào repo.**

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `template/` | khung dự án: `build.py`, `deck.json`, `icons.json`, `themes/` (9 theme), `src/`, `assets/` |
| `fonts/` | font dùng chung + `fonts.json` (đủ dấu tiếng Việt) |
| `reference/` | `themes.md`, `genres.md`, `components.md`, `patterns.md`, `lessons.md`, `showcase.html` (18 trang v2), `slides-example.html` (38 trang gốc) |
| `scripts/` | các script tiện ích kể trên |

## Lưu ý bản quyền

- `fonts/` có **Google Sans** (bản quyền của Google, không phải font mã nguồn mở). Các font còn lại (Inter, Be Vietnam Pro, Playfair Display, Lora, Montserrat, Nunito, Baloo 2, JetBrains Mono, Space Grotesk, Cormorant Garamond, Lexend, Oswald, Dancing Script) dùng giấy phép SIL OFL.
- `template/assets/logo-misa.png` là nhãn hiệu MISA.

Vì hai lý do trên, repo nên để **private**. Muốn công khai thì bỏ Google Sans (theme `misa-glass` đổi `fonts.head` sang font mở, ví dụ `be-vietnam-pro`) và bỏ logo.
