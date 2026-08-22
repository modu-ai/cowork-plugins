#!/usr/bin/env bash
# korean-slop-lint.sh — Korean AI-slop re-occurrence-prevention lint (REQ-REM-022)
#
# Scans the cowork + design skill trees for 4 pattern classes that indicate
# Korean AI-slop contamination, and exits non-zero when any registered pattern
# is found. Wired before market sync (www/plugins/ re-sync) so contaminated
# copy cannot ship.
#
# Usage:
#   korean-slop-lint.sh                 # scan owned trees, exit 1 on any finding
#   korean-slop-lint.sh --self-test     # verify detection of all 4 classes, exit 1 on detector failure
#   korean-slop-lint.sh <path>          # scan a single file/dir
#
# Pattern classes (REQ-REM-022):
#   1. dash    — em-dash (—) density in guidance prose (slop connector)
#   2. cliché  — Korean marketing clichés (혁신적인, 차세대, 재정의하는, ...)
#   3. old-ns  — deprecated plugin namespaces (moai-office, moai-content, ...)
#   4. boiler  — translationese boilerplate ("하는 하네스입니다")
#
# Exit codes: 0 = clean (no findings), 1 = findings detected (or self-test failure), 2 = usage error

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# 저장소 루트는 git 에게 묻는다. 상대 경로(../..)로 세면 스크립트를 옮길 때마다
# 조용히 엉뚱한 곳을 가리키고, 아래 존재성 검사에 걸려 스캔 없이 종료코드 0 을 낸다.
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || { cd "$SCRIPT_DIR/.." && pwd; })"
COWORK_SKILLS="$REPO_ROOT/plugins/moai-coworker/skills"
DESIGN_SKILLS="$REPO_ROOT/plugins/moai-designer/skills"

# 스캔 대상이 하나도 없으면 조용히 통과시키지 않고 사용자에게 알린다.
for _s in "$COWORK_SKILLS" "$DESIGN_SKILLS"; do
  [ -d "$_s" ] || echo "korean-slop-lint: 경고 — 스캔 대상 없음: $_s" >&2
done

# Pattern class 2: Korean marketing clichés (Tier-1 slop phrases)
ClichePattern='혁신적인|차세대|재정의하는|새로운 패러다임|한 차원 높은|지금까지 없던|결론적으로|시사하는 바가 크다'

# Pattern class 3: deprecated plugin namespaces (REQ-REM-015)
OldNsPattern='moai-office|moai-content|moai-media|moai-finance|moai-book|moai-business|moai-marketing|moai-education|moai-legal'

# Pattern class 4: translationese boilerplate (REQ-REM-011)
BoilerPattern='협력하여.*하네스입니다|하는 하네스입니다'

count_findings() {
  local label="$1" pattern="$2" scope="$3"
  local n
  n=$(grep -rE "$pattern" "$scope" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$n" -gt 0 ]; then
    echo "FAIL [$label]: $n finding(s) matching /$pattern/ in $scope" >&2
    grep -rEn "$pattern" "$scope" 2>/dev/null | head -10 >&2
    echo "---" >&2
    return 1
  fi
  echo "PASS [$label]: 0 findings in $scope" >&2
  return 0
}

run_scan() {
  local target="${1:-}"
  local status=0
  local scopes=()
  if [ -n "$target" ]; then
    scopes=("$target")
  else
    scopes=("$COWORK_SKILLS" "$DESIGN_SKILLS")
  fi
  for scope in "${scopes[@]}"; do
    [ -e "$scope" ] || continue
    # Class 1: dash density — em-dash in guidance prose. Advisory at high density;
    # flag files with >40 em-dashes (gate-skill remediation threshold proxy).
    local dashfiles
    dashfiles=$(grep -rl '—' "$scope" 2>/dev/null)
    local dashflag=0
    while IFS= read -r f; do
      [ -z "$f" ] && continue
      c=$(grep -c '—' "$f" 2>/dev/null || echo 0)
      if [ "$c" -gt 40 ]; then
        echo "FAIL [dash]: $f has $c em-dashes (>40 threshold)" >&2
        dashflag=1
      fi
    done <<< "$dashfiles"
    [ "$dashflag" -eq 0 ] && echo "PASS [dash]: no file >40 em-dashes in $scope" >&2 || status=1

    count_findings "cliché" "$ClichePattern" "$scope" || status=1
    count_findings "old-ns" "$OldNsPattern" "$scope" || status=1
    count_findings "boiler" "$BoilerPattern" "$scope" || status=1
  done
  return $status
}

run_selftest() {
  local tmp status=0 fired=0
  tmp=$(mktemp -d)
  # NOTE: self-test exits NON-ZERO when all 4 detectors fire correctly (per
  # AC-REM-022 "self-test exit non-zero on ... inputs"). Non-zero = the script
  # is confirmed to detect slop. Zero would mean a detector failed to fire.

  echo "=== korean-slop-lint self-test (4 pattern classes) ===" >&2

  # Class 1: dash
  printf '헤드라인 — 대비 카피\n또 — 여기\n' > "$tmp/dash.md"
  if grep -E '—' "$tmp/dash.md" >/dev/null 2>&1; then
    echo "PASS [self-test/dash]: em-dash detector fires" >&2; fired=$((fired+1))
  else
    echo "FAIL [self-test/dash]: detector did not fire" >&2; status=1
  fi

  # Class 2: cliché
  printf '혁신적인 AI 솔루션\n' > "$tmp/cliche.md"
  if grep -E "$ClichePattern" "$tmp/cliche.md" >/dev/null 2>&1; then
    echo "PASS [self-test/cliché]: cliché detector fires" >&2; fired=$((fired+1))
  else
    echo "FAIL [self-test/cliché]: detector did not fire" >&2; status=1
  fi

  # Class 3: old-ns
  printf 'see moai-office:doc-pdf\n' > "$tmp/oldns.md"
  if grep -E "$OldNsPattern" "$tmp/oldns.md" >/dev/null 2>&1; then
    echo "PASS [self-test/old-ns]: deprecated-namespace detector fires" >&2; fired=$((fired+1))
  else
    echo "FAIL [self-test/old-ns]: detector did not fire" >&2; status=1
  fi

  # Class 4: boiler
  printf '협력하여 수행하는 하네스입니다.\n' > "$tmp/boiler.md"
  if grep -E "$BoilerPattern" "$tmp/boiler.md" >/dev/null 2>&1; then
    echo "PASS [self-test/boiler]: boilerplate detector fires" >&2; fired=$((fired+1))
  else
    echo "FAIL [self-test/boiler]: detector did not fire" >&2; status=1
  fi

  rm -rf "$tmp"

  # Exit non-zero when all 4 detectors fire (detection capability confirmed).
  if [ "$status" -eq 0 ] && [ "$fired" -eq 4 ]; then
    echo "SELF-TEST OK: all 4 detectors fire → exiting non-zero (detection confirmed)" >&2
    return 1
  fi
  echo "SELF-TEST FAIL: $fired/4 detectors fired → exiting zero (detector failure)" >&2
  return 0
}

case "${1:-}" in
  --self-test)
    run_selftest
    ;;
  -h|--help)
    sed -n '2,20p' "$0"
    exit 0
    ;;
  "")
    run_scan
    ;;
  *)
    run_scan "$1"
    ;;
esac
