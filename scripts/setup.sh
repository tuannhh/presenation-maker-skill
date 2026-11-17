#!/bin/bash
# Cài môi trường Python riêng cho skill (một lần). Chạy được trên macOS, Linux, Windows (Git Bash).
#   setup.sh                 → tạo <skill>/.venv
#   VENV_DIR=D:/venvs/deck setup.sh → tạo venv ở chỗ khác rồi nối vào <skill>/.venv (Windows: junction)
set -e
D="$(cd "$(dirname "$0")/.." && pwd)"
SYS_PY="$(command -v python3 || command -v python || true)"
[ -n "$SYS_PY" ] || { echo "Cần Python 3.10+"; exit 1; }
find_py(){ for c in "$D/.venv/bin/python" "$D/.venv/Scripts/python.exe"; do [ -x "$c" ] && { echo "$c"; return; }; done; }
PY="$(find_py)"
if [ -z "$PY" ]; then
  if [ -n "$VENV_DIR" ]; then
    "$SYS_PY" -m venv "$VENV_DIR"
    case "$(uname -s)" in
      MINGW*|MSYS*|CYGWIN*) cmd //c mklink //J "$(cygpath -w "$D/.venv")" "$(cygpath -w "$VENV_DIR")" >/dev/null ;;
      *) ln -s "$VENV_DIR" "$D/.venv" ;;
    esac
  else
    "$SYS_PY" -m venv "$D/.venv"
  fi
  PY="$(find_py)"
fi
"$PY" -m pip install -q --upgrade pip
"$PY" -m pip install -q pillow fonttools brotli python-pptx requests google-auth
echo "OK: $PY"
command -v node >/dev/null && node -e 'if(typeof WebSocket!=="function"){console.log("Cần Node ≥ 22 cho xuất PDF/rà bố cục");process.exit(1)}' && echo "Node OK" || echo "Thiếu Node ≥ 22 (cần cho xuất PDF/rà bố cục)"
node "$D/scripts/cdp.mjs" --which 2>/dev/null || true
