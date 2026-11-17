# html-presentation-skill-claude

Skill cho **Claude Code**: dựng bài trình chiếu thành **một file HTML tự chứa** (font, ảnh, logo, video nhúng sẵn; mở offline trên máy bất kỳ).

## Tính năng

- **Hiệu ứng chuyển động** khi vào trang.
- **Điều khiển bằng bút chiếu.** Ở trang video:
  - next lần 1: hiện khung video;
  - next lần 2: phát toàn màn hình, có tiếng;
  - next lần 3: sang trang.
- **Chế độ sửa tại chỗ** (phím **E**), không cần người kỹ thuật:
  - sửa và định dạng chữ;
  - chèn, kéo, xoay, chỉnh ảnh;
  - gắn video;
  - **Ctrl+S** lưu thành file mới.
- **Kèm script:**
  - đọc PPTX;
  - sinh ảnh minh hoạ (Gemini / Vertex AI);
  - nén video;
  - rà lỗi bố cục tự động;
  - xuất PDF có link mở video;
  - bỏ trang trên file người dùng đã tự sửa (giữ nguyên các chỗ sửa).

Bộ khung lấy từ một bài thật ("Xu hướng lừa đảo và cách phòng tránh", MISA, 11/2026) đã qua nhiều vòng góp ý. Các góp ý được ghi thành quy tắc trong `reference/lessons.md`.

## Cài đặt

```bash
git clone https://github.com/tuannhh/html-presentation-skill-claude.git ~/.claude/skills/misa-html-deck
~/.claude/skills/misa-html-deck/scripts/setup.sh
```

**Yêu cầu:**
- macOS hoặc Linux, Python 3.10+;
- Node ≥ 22 và Google Chrome (dùng cho xuất PDF và rà bố cục);
- ffmpeg (dùng để nén video).

## Dùng

Trong Claude Code, gọi `/misa-html-deck` hoặc nói tự nhiên, ví dụ: *"làm bài trình chiếu HTML từ file PPTX này"*. Quy trình chi tiết ở `SKILL.md`.

Sinh ảnh minh hoạ cần một file service account Google Cloud có quyền Vertex AI. Đặt đường dẫn file vào biến `MISA_GEMINI_SA`. **Không commit file khoá vào repo.**

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `template/` | khung dự án: `build.py`, `deck.json`, `src/`, `assets/` |
| `reference/` | 38 trang mẫu (thư viện bố cục), cú pháp trang, bài học từ góp ý |
| `scripts/` | các script tiện ích kể trên |

## Lưu ý bản quyền

- `template/assets/fonts/` có font **Google Sans** (bản quyền của Google, không phải font mã nguồn mở) và **Inter** (OFL).
- `template/assets/logo-misa.png` là nhãn hiệu MISA.

Vì hai lý do trên, repo nên để **private**. Muốn công khai thì thay Google Sans bằng font mở (ví dụ Plus Jakarta Sans) và bỏ logo.
