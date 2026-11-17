#!/bin/bash
# Tạo dự án deck mới từ khung mẫu.   new_deck.sh <thư-mục-dự-án>
set -e
D="$(cd "$(dirname "$0")/.." && pwd)"; T="$1"
[ -n "$T" ] || { echo "Cần đường dẫn thư mục dự án"; exit 1; }
[ -e "$T" ] && [ "$(ls -A "$T" 2>/dev/null)" ] && { echo "Thư mục $T đã có nội dung — chọn thư mục khác"; exit 1; }
mkdir -p "$T"; cp -R "$D/template/." "$T/"
echo "Đã tạo $T. Build thử:  $D/.venv/bin/python $T/build.py"
