#!/usr/bin/env bash
# One-time setup in the user's project. Installs Playwright + Chromium into $MOTION_DIR/node_modules.
set -e
MOTION_DIR="${1:-./motion}"
mkdir -p "$MOTION_DIR"/{clips,dist,out,work}
# Resolve to an absolute path straight away: with a relative MOTION_DIR the steps
# below that cd into the folder would write to $MOTION_DIR/$MOTION_DIR/package.json.
MOTION_DIR="$(cd "$MOTION_DIR" && pwd)"
missing=()
command -v node >/dev/null || missing+=("node (https://nodejs.org)")
command -v ffmpeg >/dev/null || missing+=("ffmpeg (macOS: brew install ffmpeg)")
command -v python3 >/dev/null || missing+=("python3")
if [ ${#missing[@]} -gt 0 ]; then echo "Missing: ${missing[*]}"; exit 1; fi
python3 -c "import numpy" 2>/dev/null || python3 -m pip install --user numpy || python3 -m pip install --break-system-packages numpy
if [ ! -d "$MOTION_DIR/node_modules/playwright" ]; then
  if [ ! -f "$MOTION_DIR/package.json" ]; then echo '{"private":true}' > "$MOTION_DIR/package.json"; fi
  (cd "$MOTION_DIR" && npm install --silent playwright && npx playwright install chromium)
fi
ffmpeg -hide_banner -encoders 2>/dev/null | grep -q prores_ks || echo "Note: your ffmpeg has no prores_ks encoder; transparent panel clips will fail."
echo "Ready. Clips go in $MOTION_DIR/clips, renders in $MOTION_DIR/out."
