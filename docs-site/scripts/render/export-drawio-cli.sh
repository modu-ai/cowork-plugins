#!/usr/bin/env bash
# draw.io desktop CLI 로 .drawio → SVG 일괄 변환
# 사용: bash export-drawio-cli.sh
set -u
DIAGRAMS_DIR="/Users/goos/MoAI/MoAI-Cowork-Plugins/docs-site/static/diagrams"

# draw.io 바이너리 탐지
DRAWIO=""
for cand in "/Applications/draw.io.app/Contents/MacOS/draw.io" "$(brew --prefix 2>/dev/null)/bin/drawio" "/opt/homebrew/bin/drawio" "/usr/local/bin/drawio"; do
  [ -x "$cand" ] && DRAWIO="$cand" && break
done
if [ -z "$DRAWIO" ]; then echo "❌ draw.io 바이너리 없음 (brew install --cask drawio)"; exit 1; fi
echo "사용: $DRAWIO"

ok=0; fail=0
for f in "$DIAGRAMS_DIR"/*.drawio; do
  slug=$(basename "$f" .drawio)
  out="$DIAGRAMS_DIR/$slug.svg"
  # -x export, -f format, -o output. Electron headless 안정화 플래그.
  if "$DRAWIO" -x -f svg -o "$out" "$f" --no-sandbox --disable-gpu 2>/tmp/drawio-err.log; then
    if [ -s "$out" ]; then echo "  ✓ $slug ($(wc -c < "$out" | tr -d ' ') bytes)"; ok=$((ok+1));
    else echo "  ❌ $slug: 출력 없음"; fail=$((fail+1)); fi
  else
    echo "  ❌ $slug: $(head -1 /tmp/drawio-err.log)"; fail=$((fail+1))
  fi
done
echo "성공 $ok / 실패 $fail"
