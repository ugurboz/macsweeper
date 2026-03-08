#!/usr/bin/env bash
set -euo pipefail

# Build a distributable macOS .app from the current source tree.
# Usage:
#   ./scripts/build_macos.sh
# Optional env vars:
#   APP_NAME="MacSweeper Pro"
#   ICON_PATH="assets/macsweeper.icns"

APP_NAME="${APP_NAME:-MacSweeper Pro}"
ICON_PATH="${ICON_PATH:-assets/macsweeper.icns}"

cd "$(dirname "$0")/.."

if ! command -v pyinstaller >/dev/null 2>&1; then
  echo "[build] pyinstaller not found, installing..."
  /usr/local/bin/python3 -m pip install pyinstaller
fi

echo "[build] cleaning old artifacts"
rm -rf build dist "${APP_NAME}.spec"

echo "[build] creating app bundle: ${APP_NAME}"
pyinstaller \
  --noconfirm \
  --windowed \
  --name "${APP_NAME}" \
  --icon "${ICON_PATH}" \
  --add-data "ui/web:ui/web" \
  --collect-all webview \
  --collect-all PIL \
  main.py

echo "[build] done"
echo "[build] app path: dist/${APP_NAME}.app"
