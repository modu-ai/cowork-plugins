#!/usr/bin/env bash
# validate-marketplace.sh — MoAI-Cowork-Plugins marketplace integrity gate
#
# PURPOSE
#   Consolidates the marketplace integrity rules from CLAUDE.local.md §1
#   (버저닝 정책 — version single-source-of-truth + SKILL.md frontmatter schema)
#   and §4-2 (푸시 전 체크리스트 — pre-push checklist) into ONE runnable gate.
#   Run it before any release commit/tag/push.
#
# USAGE
#   bash scripts/validate-marketplace.sh
#
#   Exits 0 only if ALL 6 checks pass; exits 1 if ANY check fails.
#   Each check prints [PASS]/[FAIL] + a one-line summary; failures list offenders.
#
# DEV-TOOL NOTE
#   This is a repository DEV TOOL — it is NOT shipped to users, NOT a plugin
#   component, and NOT a CHANGELOG-tracked artifact. It validates the workspace;
#   it never mutates it (no version bumps, no edits).
#
# PORTABILITY
#   POSIX-ish bash, compatible with macOS bash 3.2 and Linux. No mapfile, no
#   associative arrays. JSON parsing prefers python3 with a grep/awk fallback.

# Note: intentionally NOT using `set -e` — we want to run every check and
# accumulate failures rather than abort on the first non-zero command.
set -u

# ---- locate repo root (script lives in <root>/scripts/) ----
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT" || { echo "ERROR: cannot cd to repo root"; exit 1; }

# ---- colors (disabled when not a tty) ----
if [ -t 1 ]; then
  RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BOLD='\033[1m'; NC='\033[0m'
else
  RED=''; GREEN=''; YELLOW=''; BOLD=''; NC=''
fi

MARKETPLACE=".claude-plugin/marketplace.json"
PASS_COUNT=0
FAIL_COUNT=0

pass() { printf "${GREEN}[PASS]${NC} %s\n" "$1"; PASS_COUNT=$((PASS_COUNT + 1)); }
fail() { printf "${RED}[FAIL]${NC} %s\n" "$1"; FAIL_COUNT=$((FAIL_COUNT + 1)); }

have_python3=0
if command -v python3 >/dev/null 2>&1; then have_python3=1; fi

# Extract the top-level YAML frontmatter block (lines strictly between the
# first and second '---' delimiter) of a SKILL.md file.
fm_block() {
  awk '
    NR==1 && $0=="---" { infm=1; next }
    infm && $0=="---"  { exit }
    infm               { print }
  ' "$1"
}

# Extract top-level frontmatter keys (no leading whitespace, "key:" form).
fm_top_keys() {
  fm_block "$1" | grep -E '^[A-Za-z][A-Za-z0-9_-]*:' | sed -E 's/:.*//'
}

printf "${BOLD}=== MoAI-Cowork-Plugins Marketplace Validator ===${NC}\n"
printf "repo: %s\n\n" "$REPO_ROOT"

# Gather the SKILL.md and plugin.json file lists once (whitespace-safe enough:
# these paths contain no spaces by convention).
SKILL_FILES="$(find moai-*/skills -name SKILL.md -not -path '*/.git/*' 2>/dev/null | sort)"
PLUGIN_FILES="$(find . -path '*/.claude-plugin/plugin.json' -not -path '*/.git/*' 2>/dev/null | sort)"

# =====================================================================
# CHECK 1 — Version consistency across all sync points
#   marketplace.json metadata.version
#   + every moai-*/.claude-plugin/plugin.json version
#   + every moai-*/skills/*/SKILL.md frontmatter version
#   All MUST be identical.
# =====================================================================
{
  versions_file="$(mktemp 2>/dev/null || echo /tmp/vmp_versions.$$)"
  : > "$versions_file"

  # marketplace.json metadata.version
  if [ "$have_python3" -eq 1 ]; then
    mp_ver="$(python3 -c "import json,sys; print(json.load(open('$MARKETPLACE')).get('metadata',{}).get('version',''))" 2>/dev/null)"
  else
    # fallback: first version under the metadata block
    mp_ver="$(grep -A20 '"metadata"' "$MARKETPLACE" | grep '"version"' | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')"
  fi
  [ -n "$mp_ver" ] && echo "$mp_ver" >> "$versions_file"

  # plugin.json versions (top-level "version")
  for pf in $PLUGIN_FILES; do
    pv="$(grep '"version"' "$pf" | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')"
    [ -n "$pv" ] && echo "$pv" >> "$versions_file"
  done

  # SKILL.md frontmatter versions
  for sf in $SKILL_FILES; do
    sv="$(fm_block "$sf" | grep -E '^version:' | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')"
    [ -n "$sv" ] && echo "$sv" >> "$versions_file"
  done

  distinct="$(sort -u "$versions_file")"
  distinct_count="$(echo "$distinct" | grep -c .)"
  total_points="$(grep -c . "$versions_file")"

  if [ "$distinct_count" -eq 1 ] && [ -n "$distinct" ]; then
    pass "Version consistency: all $total_points sync points = $distinct (marketplace=$mp_ver)"
  else
    fail "Version consistency: $distinct_count distinct values across $total_points sync points"
    echo "       distinct values found:"
    echo "$distinct" | sed 's/^/         - /'
  fi
  rm -f "$versions_file"
}

# =====================================================================
# CHECK 2 — No top-level 'metadata:' block in any SKILL.md frontmatter
# =====================================================================
{
  offenders=""
  for sf in $SKILL_FILES; do
    if fm_block "$sf" | grep -qE '^metadata:'; then
      offenders="$offenders $sf"
    fi
  done
  if [ -z "$offenders" ]; then
    pass "No 'metadata:' block: 0 offenders across SKILL.md frontmatter"
  else
    n="$(echo $offenders | wc -w | tr -d ' ')"
    fail "Found 'metadata:' block in $n SKILL.md file(s)"
    for o in $offenders; do echo "         - $o"; done
  fi
}

# =====================================================================
# CHECK 3 — Every SKILL.md has a 'version:' frontmatter field
# =====================================================================
{
  missing=""
  total=0
  for sf in $SKILL_FILES; do
    total=$((total + 1))
    if ! fm_block "$sf" | grep -qE '^version:'; then
      missing="$missing $sf"
    fi
  done
  if [ -z "$missing" ]; then
    pass "All SKILL.md have version: field ($total/$total)"
  else
    n="$(echo $missing | wc -w | tr -d ' ')"
    fail "$n of $total SKILL.md missing 'version:' field"
    for m in $missing; do echo "         - $m"; done
  fi
}

# =====================================================================
# CHECK 4 — marketplace plugins[] count == plugin.json file count
# =====================================================================
{
  plugin_file_count="$(echo "$PLUGIN_FILES" | grep -c .)"
  if [ "$have_python3" -eq 1 ]; then
    mp_plugins_count="$(python3 -c "import json; print(len(json.load(open('$MARKETPLACE')).get('plugins',[])))" 2>/dev/null)"
  else
    # fallback: count "source" entries inside the plugins array (best-effort)
    mp_plugins_count="$(grep -c '"source"' "$MARKETPLACE")"
  fi
  if [ -n "$mp_plugins_count" ] && [ "$mp_plugins_count" = "$plugin_file_count" ]; then
    pass "plugins[] count matches: marketplace=$mp_plugins_count, plugin.json files=$plugin_file_count"
  else
    fail "plugins[] count mismatch: marketplace=$mp_plugins_count, plugin.json files=$plugin_file_count"
    # Surface which plugin dirs are missing from / extra in marketplace, when python3 is available.
    if [ "$have_python3" -eq 1 ]; then
      python3 - "$MARKETPLACE" <<'PY' 2>/dev/null
import json, os, sys, glob
mp = json.load(open(sys.argv[1]))
mp_paths = set()
for p in mp.get('plugins', []):
    src = p.get('source') or p.get('name') or ''
    mp_paths.add(os.path.normpath(src.lstrip('./')))
disk = set(os.path.normpath(os.path.dirname(os.path.dirname(f)))
           for f in glob.glob('moai-*/.claude-plugin/plugin.json'))
only_disk = sorted(disk - mp_paths)
only_mp   = sorted(mp_paths - disk)
for d in only_disk:
    print(f"         - on disk but NOT in marketplace: {d}")
for d in only_mp:
    print(f"         - in marketplace but NO plugin.json on disk: {d}")
PY
    fi
  fi
}

# =====================================================================
# CHECK 5 — Phantom skill-ref in sub-agents
#   For every moai-*/agents/*.md, extract moai-<plugin>:<skill> colon-refs
#   and assert each referenced <plugin>/skills/<skill>/ directory exists.
#   (Phase 6 audit, made permanent.)
# =====================================================================
{
  agent_files="$(find moai-* -path '*/agents/*.md' -not -path '*/.git/*' 2>/dev/null | sort)"
  agent_count="$(echo "$agent_files" | grep -c .)"
  phantoms=""
  refs_checked=0
  for af in $agent_files; do
    [ -n "$af" ] || continue
    # extract distinct colon-refs of the form moai-<plugin>:<skill>
    refs="$(grep -oE 'moai-[a-z0-9-]+:[a-z0-9-]+' "$af" 2>/dev/null | sort -u)"
    for ref in $refs; do
      plugin="${ref%%:*}"
      skill="${ref#*:}"
      refs_checked=$((refs_checked + 1))
      if [ ! -d "$plugin/skills/$skill" ]; then
        phantoms="$phantoms ${af}::${ref}"
      fi
    done
  done
  if [ -z "$phantoms" ]; then
    pass "No phantom skill-refs: $refs_checked colon-ref(s) across $agent_count agent file(s) all resolve"
  else
    n="$(echo $phantoms | wc -w | tr -d ' ')"
    fail "$n phantom skill-ref(s) found in sub-agents"
    for p in $phantoms; do
      af="${p%%::*}"; ref="${p#*::}"
      echo "         - $af references $ref (missing ${ref%%:*}/skills/${ref#*:}/)"
    done
  fi
}

# =====================================================================
# CHECK 6 — SKILL.md frontmatter allowed-keys
#   Top-level frontmatter keys must be within {name, description,
#   user-invocable, version}. Inspect only the block between the first
#   two '---' lines and only top-level (no leading whitespace) keys.
# =====================================================================
{
  offenders=""
  for sf in $SKILL_FILES; do
    bad="$(fm_top_keys "$sf" | grep -vxE 'name|description|user-invocable|version' | tr '\n' ',' | sed 's/,$//')"
    if [ -n "$bad" ]; then
      offenders="$offenders ${sf}::${bad}"
    fi
  done
  if [ -z "$offenders" ]; then
    pass "Frontmatter allowed-keys: all SKILL.md within {name,description,user-invocable,version}"
  else
    n="$(echo $offenders | wc -w | tr -d ' ')"
    fail "$n SKILL.md with disallowed top-level frontmatter key(s)"
    for o in $offenders; do
      sf="${o%%::*}"; keys="${o#*::}"
      echo "         - $sf has disallowed key(s): $keys"
    done
  fi
}

# =====================================================================
# Summary
# =====================================================================
TOTAL=$((PASS_COUNT + FAIL_COUNT))
printf "\n${BOLD}=== Summary: %d/%d checks passed ===${NC}\n" "$PASS_COUNT" "$TOTAL"

if [ "$FAIL_COUNT" -gt 0 ]; then
  printf "${RED}Validation FAILED (%d check(s) failed).${NC}\n" "$FAIL_COUNT"
  exit 1
fi
printf "${GREEN}Validation PASSED.${NC}\n"
exit 0
