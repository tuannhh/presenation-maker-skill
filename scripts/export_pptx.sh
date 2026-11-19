#!/bin/bash
# Xuất PPTX sửa được: chữ là text box PowerPoint, nền / hình / biểu đồ là ảnh, có hiệu ứng vào + chuyển trang.
# export_pptx.sh <deck.html> <thư-mục-ra> [ten_file.pptx]
set -e
D="$(cd "$(dirname "$0")" && pwd)"; . "$D/_env.sh"
DECK="$1"; OUT="$2"; NAME="${3:-$(basename "${DECK%.*}").pptx}"
CAP="$(mktemp -d)/pptx"
node "$D/capture_pptx.mjs" "$DECK" "$CAP"
mkdir -p "$OUT"
"$PY" "$D/make_pptx.py" "$CAP" "$DECK" "$OUT/$NAME"
