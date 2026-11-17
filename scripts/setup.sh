#!/bin/bash
# Cài môi trường Python riêng cho skill (một lần).
set -e
D="$(cd "$(dirname "$0")/.." && pwd)"
[ -x "$D/.venv/bin/python" ] || python3 -m venv "$D/.venv"
"$D/.venv/bin/pip" install -q --upgrade pip
"$D/.venv/bin/pip" install -q pillow fonttools brotli python-pptx requests google-auth
echo "OK: $D/.venv/bin/python"
command -v node >/dev/null && node -e 'if(typeof WebSocket!=="function"){console.log("Cần Node ≥ 22 cho xuất PDF/rà bố cục");process.exit(1)}' && echo "Node OK"
[ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ] && echo "Chrome OK" || echo "Thiếu Google Chrome (cần cho xuất PDF/rà bố cục; đặt biến CHROME nếu ở chỗ khác)"
