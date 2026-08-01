#!/usr/bin/env bash
# harness-builder / qmd-search.sh — native wrapper
# qmd hybrid search (BM25 + semantic + LLM rerank) with ripgrep fallback.
# Usage: qmd-search.sh <query> [TOP_N]
set -euo pipefail

QUERY="${1:-}"
TOP="${2:-${VAULT_SEARCH_TOP:-10}}"
COLLECTION="${VAULT_QMD_COLLECTION:-moai-vault}"
MIN_VECTORS="${VAULT_QMD_MIN_VECTORS:-1000}"

if [ -z "$QUERY" ]; then
  cat >&2 <<EOF
Usage: qmd-search.sh <query> [TOP_N]

Env:
  VAULT_QMD_COLLECTION   qmd collection (default moai-vault)
  VAULT_SEARCH_TOP       result count (default 10)
  VAULT_QMD_MIN_VECTORS  min vectors for qmd use (default 1000)
  MOAI_OBSIDIAN_VAULT    vault path for ripgrep fallback
EOF
  exit 1
fi

# Layer 1 — qmd hybrid (priority)
if command -v qmd >/dev/null 2>&1; then
  VECTORS=$(qmd status 2>&1 | grep -E "^[[:space:]]*Vectors:" | grep -oE "[0-9]+" | head -1 || echo 0)
  if [ "${VECTORS:-0}" -ge "$MIN_VECTORS" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    [ -x "$SCRIPT_DIR/sync.sh" ] && bash "$SCRIPT_DIR/sync.sh" --quiet || true
    echo "## qmd hybrid search: \"$QUERY\" (collection: $COLLECTION, vectors: $VECTORS)"
    echo ""
    qmd query "$QUERY" -c "$COLLECTION" -n "$TOP" --files 2>&1 | sed -E 's/\x1b\[[0-9;]*[a-zA-Z]//g'
    exit 0
  fi
fi

# Fallback — ripgrep over the vault
VAULT="${MOAI_OBSIDIAN_VAULT:-$HOME}"
echo "## ripgrep fallback search: \"$QUERY\" (vault: $VAULT)"
echo ""
if command -v rg >/dev/null 2>&1; then
  rg -i "$QUERY" "$VAULT" -n --color never 2>/dev/null | head -n "$TOP" || echo "(ripgrep 매치 없음)"
else
  grep -rni "$QUERY" "$VAULT" 2>/dev/null | head -n "$TOP" || echo "(grep 매치 없음)"
fi
