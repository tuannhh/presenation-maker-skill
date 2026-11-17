#!/bin/bash
# Xuất PDF (không hiệu ứng) + thư mục video/ để bấm mở video từ PDF.
# export_pdf.sh <deck.html> <thư-mục-ra> "<Tiêu đề PDF>"
set -e
D="$(cd "$(dirname "$0")" && pwd)"; PY="$D/../.venv/bin/python"; [ -x "$PY" ] || PY=python3
DECK="$1"; OUT="$2"; TITLE="${3:-Bài trình bày}"
SH="$(mktemp -d)/shots"
node "$D/capture_slides.mjs" "$DECK" "$SH" 1.5
mkdir -p "$OUT"
"$PY" "$D/make_pdf.py" "$SH" "$DECK" "$OUT" "$TITLE"
echo "Ảnh chụp từng trang: $SH (xem nhanh trước khi gửi)"
