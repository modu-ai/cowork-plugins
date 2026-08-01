#!/usr/bin/env bash
# harness-builder / sync.sh — qmd incremental update (run before search)
# Usage: sync.sh [--quiet]
set -euo pipefail

QUIET=0
[ "${1:-}" = "--quiet" ] && QUIET=1
COLLECTION="${VAULT_QMD_COLLECTION:-moai-vault}"

if ! command -v qmd >/dev/null 2>&1; then
  exit 0
fi

[ $QUIET -eq 0 ] && echo "qmd update ($COLLECTION)..." >&2
qmd update -c "$COLLECTION" 2>&1 | tail -n 3 || true
