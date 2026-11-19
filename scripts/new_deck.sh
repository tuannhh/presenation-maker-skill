#!/bin/bash
# Tạo dự án deck mới từ khung mẫu.   new_deck.sh <thư-mục-dự-án> [theme]
# Xem danh sách theme: reference/themes.md  (hoặc template/themes/themes.json)
set -e
. "$(dirname "$0")/_env.sh"
T="$1"; TH="${2:-misa-glass}"
[ -n "$T" ] || { echo "Cần đường dẫn thư mục dự án"; exit 1; }
[ -f "$SKILL_DIR/template/themes/$TH.css" ] || { echo "Không có theme '$TH'. Có: $(cd "$SKILL_DIR/template/themes" && ls *.css | sed 's/\.css//' | tr '\n' ' ')"; exit 1; }
[ -e "$T" ] && [ "$(ls -A "$T" 2>/dev/null)" ] && { echo "Thư mục $T đã có nội dung — chọn thư mục khác"; exit 1; }
mkdir -p "$T"; cp -R "$SKILL_DIR/template/." "$T/"
rm -rf "$T/themes" "$T/dist" "$T/assets/fonts"   # theme & font dùng chung lấy từ skill; muốn tùy biến thì tạo lại $T/themes/<tên>.css
"$PY" - "$T/deck.json" "$TH" <<'PY'
import json,sys; p,th=sys.argv[1],sys.argv[2]
c=json.load(open(p,encoding="utf-8")); c["theme"]=th
open(p,"w",encoding="utf-8").write(json.dumps(c,ensure_ascii=False,indent=1))
PY
echo "Đã tạo $T (theme: $TH). Build thử:"
echo "  \"$PY\" \"$T/build.py\""
