# MISA HTML Deck

**Tiếng Việt** · [English](#english)

## Giới thiệu

**MISA HTML Deck** là một skill cho trợ lý lập trình AI (Claude Code, OpenAI Codex, Google Antigravity, GitHub Copilot trong VS Code). Bạn đưa nội dung: một file PPTX cũ, dàn ý, tài liệu, hay chỉ vài dòng mô tả. Skill dựng thành bài trình chiếu hoàn chỉnh trong **một file HTML duy nhất**: font, ảnh, logo, video đều nhúng sẵn, gửi qua email hay chép USB là mở được trên máy bất kỳ, không cần mạng, không cần cài PowerPoint.

Bài trình chiếu có hiệu ứng vào trang và chuyển trang sinh động kiểu Prezi, chạy bằng bút chiếu như PowerPoint, có 15 phong cách và hơn 40 bố cục (biểu đồ, sơ đồ, timeline, bảng giá, khung điện thoại…). Sau khi dựng, người trình bày tự sửa chữ, ảnh, font, vị trí khối ngay trong trình duyệt (phím **E**) mà không phải đụng vào mã. Khi cần gửi đi, xuất ra **PDF** để in hoặc **PPTX sửa được** vẫn giữ hiệu ứng khi trình chiếu.

Skill được đúc kết từ các bài trình bày thật của MISA qua nhiều vòng góp ý. Mỗi lỗi từng gặp (chữ xuống dòng xấu, chữ tràn khung, màu tương phản kém…) đều được ghi thành quy tắc để không lặp lại.

## Tính năng

- **15 theme** đổi bằng một dòng trong `deck.json`: `misa-glass` (mặc định) · `midnight-tech` · `clean-minimal` · `editorial` · `playful-edu` · `bold-pitch` · `luxury-gold` · `nature-green` · `vivid-gradient` · `ava-lavender` · `corporate-navy` · `mono-keynote` · `sunset-warm` · `chalkboard` · `ocean-fresh`. Mỗi theme có font, bảng màu, nền động và nhịp hiệu ứng riêng. Tuỳ biến thêm: palette, font, nền, tốc độ hiệu ứng, logo — hoặc tự tạo theme mới.
- **Biểu đồ, sơ đồ, bố cục v3**: donut, thanh chồng 100%, phễu, waterfall, gauge, waffle, heatmap, bảng so sánh, vòng lặp, hub & spoke, Venn, sơ đồ tổ chức, kiến trúc tầng, bản đồ định vị, bento, khung chat, khung điện thoại/laptop. Tất cả tự đổi màu, font theo theme.
- **Thư viện bố cục**: agenda, statement, KPI đếm số, vòng %, thanh ngang, cột, đường, timeline ngang/dọc, quy trình, trích dẫn, ảnh tràn nửa trang, đội ngũ, bảng giá, trước/sau, SWOT, kim tự tháp, khối mã, cảm ơn… cộng 38 trang mẫu gốc. 159 icon.
- **Playbook theo thể loại** (`reference/genres.md`): đào tạo, pitch gọi vốn, bán hàng, báo cáo, ra mắt sản phẩm, gala/vinh danh, workshop, đề xuất dự án, onboarding, case study, tech talk, tuyên truyền.
- **Hiệu ứng chuyển động** khi vào trang và chuyển trang (theo theme). Chuyển trang hai lớp kiểu Prezi (lùi xa, lướt, zoom vào), khối lập phương, lật thẻ, rút thẻ, chiều sâu, xoáy; đặt cho cả bài hoặc từng trang (`data-tr`).
- **Điều khiển bằng bút chiếu.** Ở trang video: next lần 1 hiện khung, lần 2 phát toàn màn hình có tiếng, lần 3 sang trang.
- **Chế độ sửa tại chỗ** (phím **E**): sửa/định dạng chữ, chèn/kéo/xoay/chỉnh ảnh, gắn video; rê chuột vào chữ / hình rồi kéo ô **✥** để di chuyển ngay khi đang sửa; nút **Aa Font** đổi font cả bài (Inter, Montserrat, Barlow, Roboto, Google Sans, Open Sans), ô Font trên thanh định dạng đổi font từng khối chữ; **chế độ Bố cục** (phím **M**) để kéo di chuyển, phóng to/thu nhỏ hoặc xoá bất kỳ cụm chữ, hình, thẻ nào có sẵn trên trang; **Ctrl+S** lưu file mới.
- **Script kèm theo**: đọc PPTX, xem trước mọi theme, chụp contact sheet để rà nhanh, rà lỗi bố cục, sinh ảnh minh hoạ (Gemini/Vertex AI), nén video, xuất PDF có link video, xuất PPTX (chữ sửa được, giữ hiệu ứng vào và chuyển trang), bỏ trang trên file đã tự sửa.

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

### Dùng với công cụ AI khác

Skill theo chuẩn mở Agent Skills (thư mục có `SKILL.md`), nên chạy được ở mọi công cụ đọc chuẩn này. Chỉ đổi thư mục clone, rồi chạy `setup.sh` trong thư mục đó:

| Công cụ | Thư mục cài cho mọi dự án | Hoặc riêng một dự án |
|---|---|---|
| Claude Code | `~/.claude/skills/misa-html-deck` | `.claude/skills/misa-html-deck` |
| OpenAI Codex (CLI, app, VS Code extension) | `~/.codex/skills/misa-html-deck` | `.agents/skills/misa-html-deck` |
| Google Antigravity | `~/.gemini/config/skills/misa-html-deck` (bản cũ: `~/.gemini/antigravity/skills/`) | `.agents/skills/misa-html-deck` |
| VS Code + GitHub Copilot | `~/.copilot/skills/misa-html-deck` (Copilot cũng đọc `~/.claude/skills`) | `.github/skills/misa-html-deck` |

Ví dụ với Codex:
```bash
git clone https://github.com/tuannhh/html-presentation-skill-claude.git ~/.codex/skills/misa-html-deck
bash ~/.codex/skills/misa-html-deck/scripts/setup.sh
```
Đã cài cho Claude Code thì không cần clone lần nữa: tạo liên kết (Windows: `mklink /J`, macOS/Linux: `ln -s`) từ thư mục của công cụ kia tới `~/.claude/skills/misa-html-deck`.

Công cụ chạy skill phải được chạy lệnh shell (bash, Python, Node) và ghi file. Khởi động lại công cụ sau khi cài để nó nhận skill.

**Yêu cầu:** Python 3.10+; Node ≥ 22 và Chrome hoặc Edge (xuất PDF, contact sheet, rà bố cục); ffmpeg (nén video, ảnh bìa video khi xuất PPTX); python-pptx (xuất PPTX, có sẵn sau `setup.sh`).

## Dùng

Trong Claude Code, gọi `/misa-html-deck` hoặc nói tự nhiên, ví dụ: *"làm bài pitch gọi vốn 12 trang phong cách bold"*, *"chuyển file PPTX này thành slide HTML kiểu tạp chí"*. Quy trình chi tiết ở `SKILL.md`.

Xem trước 15 theme:
```bash
~/.claude/skills/misa-html-deck/.venv/Scripts/python.exe ~/.claude/skills/misa-html-deck/scripts/preview_themes.py ./theme-preview
```
(macOS/Linux: `.venv/bin/python`.) Mở `theme-preview/index.html`.

Sinh ảnh minh hoạ cần một file service account Google Cloud có quyền Vertex AI, đặt đường dẫn vào biến `MISA_GEMINI_SA`. **Không commit file khoá vào repo.**

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `template/` | khung dự án: `build.py`, `deck.json`, `icons.json`, `themes/` (15 theme), `src/`, `assets/` |
| `fonts/` | font dùng chung + `fonts.json` (đủ dấu tiếng Việt) |
| `reference/` | `themes.md`, `genres.md`, `components.md`, `patterns.md`, `lessons.md`, `showcase.html` (33 trang v2 + v3), `slides-example.html` (38 trang gốc) |
| `scripts/` | các script tiện ích kể trên |

## Lưu ý bản quyền

- `fonts/` có **Google Sans** (bản quyền của Google, không phải font mã nguồn mở). Các font còn lại (Inter, Be Vietnam Pro, Playfair Display, Lora, Montserrat, Nunito, Baloo 2, JetBrains Mono, Space Grotesk, Cormorant Garamond, Lexend, Oswald, Dancing Script, Barlow, Roboto, Open Sans) dùng giấy phép SIL OFL.
- `template/assets/logo-misa.png` là nhãn hiệu MISA.

Vì hai lý do trên, repo nên để **private**. Muốn công khai thì bỏ Google Sans (theme `misa-glass` đổi `fonts.head` sang font mở, ví dụ `be-vietnam-pro`) và bỏ logo.

---

## English

### Introduction

**MISA HTML Deck** is an agent skill for AI coding assistants (Claude Code, OpenAI Codex, Google Antigravity, GitHub Copilot in VS Code). Give it your content: an old PPTX, an outline, a document, or a few lines of description. It builds a finished presentation as **one self-contained HTML file**, with fonts, images, logo and videos embedded. Email it or copy it to a USB stick and it opens on any computer, offline, with no PowerPoint needed.

Decks come with lively entrance animations and Prezi-style slide transitions, work with a presentation clicker just like PowerPoint, and offer 15 visual styles and more than 40 layouts (charts, diagrams, timelines, pricing tables, phone mockups…). Once built, presenters edit text, images, fonts and block positions right in the browser (press **E**) without touching code. When it is time to share, export to **PDF** for printing or to an **editable PPTX** that keeps the animations when presenting.

The skill was distilled from real MISA presentations through many rounds of feedback. Every problem met along the way (awkward line breaks, overflowing text, low contrast…) became a rule so it does not happen again.

### Features

- **15 themes**, switched with one line in `deck.json`: corporate glass, dark tech, minimal, editorial magazine, playful education, neo-brutalist pitch, black and gold luxury, nature, vivid gradient, lavender, corporate navy, black and white keynote, warm sunset, chalkboard, ocean. Each has its own fonts, palette, animated background and motion pace; palette, fonts, background and logo can all be customised.
- **40+ layouts**: donut, stacked bar, funnel, waterfall, gauge, waffle and heatmap charts; cycle, hub and spoke, Venn, org chart and layered architecture diagrams; bento grids, chat bubbles, phone and laptop frames; agenda, KPI counters, timelines, processes, quotes, team, pricing, before/after, SWOT, pyramid, code blocks. 159 icons.
- **Playbooks for 12 genres**: training, investor pitch, sales, quarterly/annual report, product launch, gala and awards, workshop, project proposal, onboarding, case study, tech talk, awareness campaign.
- **Motion**: entrance animations per block; two-layer transitions (Prezi-style zoom-out/pan/zoom-in, cube, card flip, fly-through, card stack, parallax, swirl), set for the whole deck or per slide.
- **Clicker-friendly**, including video slides (first click shows the frame, second plays full screen with sound).
- **In-browser edit mode** (**E**): edit and format text, insert, move, rotate and crop images, attach videos, drag any block, change the deck font (Inter, Montserrat, Barlow, Roboto, Google Sans, Open Sans) or a single block's font, layout mode (**M**) to move, resize or delete anything, **Ctrl+S** to save a new file.
- **Export**: PDF without animations (with links to the videos); editable PPTX where all text stays editable in PowerPoint, entrance effects follow the HTML order, transitions are mapped to the closest PowerPoint ones, videos and speaker notes are included.
- **Helper scripts**: read PPTX content, preview all themes, contact sheets, automatic layout checks, AI image generation (Gemini / Vertex AI), video compression, removing slides from an edited file.

### Install

Clone into your tool's skills folder, then run `setup.sh` from that folder (on Windows use Git Bash). Restart the tool afterwards.

| Tool | All projects | One project |
|---|---|---|
| Claude Code | `~/.claude/skills/misa-html-deck` | `.claude/skills/misa-html-deck` |
| OpenAI Codex | `~/.codex/skills/misa-html-deck` | `.agents/skills/misa-html-deck` |
| Google Antigravity | `~/.gemini/config/skills/misa-html-deck` | `.agents/skills/misa-html-deck` |
| VS Code + GitHub Copilot | `~/.copilot/skills/misa-html-deck` | `.github/skills/misa-html-deck` |

```bash
git clone https://github.com/tuannhh/html-presentation-skill-claude.git ~/.claude/skills/misa-html-deck
bash ~/.claude/skills/misa-html-deck/scripts/setup.sh
```

**Requirements:** Python 3.10+; Node 22+ and Chrome or Edge (PDF/PPTX export, contact sheets, layout checks); ffmpeg (video compression, video posters in PPTX). The assistant must be allowed to run shell commands and write files.

### Usage

Ask in plain language, for example *"make a 12-slide investor pitch in a bold style"* or *"turn this PPTX into an HTML deck in magazine style"*, or call `/misa-html-deck` in Claude Code. The full workflow is in `SKILL.md` (written in Vietnamese; the assistant reads it for you).

### Licensing notes

`fonts/` includes **Google Sans** (proprietary to Google); all other fonts are SIL OFL. `template/assets/logo-misa.png` is a MISA trademark. Keep the repository **private**, or remove Google Sans and the logo before making it public.
