# Dùng chung cho các script: tìm python của venv (.venv/bin trên macOS/Linux, .venv/Scripts trên Windows)
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY=""
for c in "$SKILL_DIR/.venv/bin/python" "$SKILL_DIR/.venv/Scripts/python.exe"; do [ -x "$c" ] && { PY="$c"; break; }; done
if [ -z "$PY" ]; then PY="$(command -v python3 || command -v python || true)"; fi
