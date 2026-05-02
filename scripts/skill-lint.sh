#!/usr/bin/env bash
# skill-lint.sh — SKILL.md frontmatter and structure validation
# Usage: ./scripts/skill-lint.sh [skill-path]
#   skill-path: specific SKILL.md file or directory (default: all skills)

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0
WARNINGS=0
CHECKED=0

lint_skill() {
  local file="$1"
  local relpath="${file#$PWD/}"

  CHECKED=$((CHECKED + 1))

  # 1. Check file exists
  if [ ! -f "$file" ]; then
    echo -e "${RED}FAIL${NC} $relpath: file not found"
    ERRORS=$((ERRORS + 1))
    return
  fi

  # 2. Check YAML frontmatter exists
  if ! head -1 "$file" | grep -q '^---$'; then
    echo -e "${RED}FAIL${NC} $relpath: missing YAML frontmatter opening '---'"
    ERRORS=$((ERRORS + 1))
    return
  fi

  # 3. Extract frontmatter
  local fm_start fm_end
  fm_start=1
  fm_end=$(awk '/^---$/{n++; if(n==2) print NR; }' "$file")
  if [ -z "$fm_end" ]; then
    echo -e "${RED}FAIL${NC} $relpath: missing YAML frontmatter closing '---'"
    ERRORS=$((ERRORS + 1))
    return
  fi

  # 4. Check required fields: name
  if ! sed -n "${fm_start},${fm_end}p" "$file" | grep -q '^name:'; then
    echo -e "${RED}FAIL${NC} $relpath: missing required field 'name'"
    ERRORS=$((ERRORS + 1))
  fi

  # 5. Check required fields: description
  if ! sed -n "${fm_start},${fm_end}p" "$file" | grep -q '^description:'; then
    echo -e "${RED}FAIL${NC} $relpath: missing required field 'description'"
    ERRORS=$((ERRORS + 1))
  fi

  # 6. Check FORBIDDEN: metadata block
  if sed -n "${fm_start},${fm_end}p" "$file" | grep -q '^metadata:'; then
    echo -e "${RED}FAIL${NC} $relpath: forbidden 'metadata:' block (v1.3.0 policy)"
    ERRORS=$((ERRORS + 1))
  fi

  # 7. Check FORBIDDEN: keywords field
  if sed -n "${fm_start},${fm_end}p" "$file" | grep -q '^keywords:'; then
    echo -e "${RED}FAIL${NC} $relpath: forbidden 'keywords:' field (non-standard)"
    ERRORS=$((ERRORS + 1))
  fi

  # 8. Check name format (lowercase, hyphens only)
  local skill_name
  skill_name=$(sed -n "${fm_start},${fm_end}p" "$file" | grep '^name:' | sed 's/^name: *//' | tr -d '"' | tr -d "'")
  if [ -n "$skill_name" ]; then
    if ! echo "$skill_name" | grep -qE '^[a-z][a-z0-9-]*$'; then
      echo -e "${YELLOW}WARN${NC} $relpath: name '$skill_name' should be lowercase with hyphens only"
      WARNINGS=$((WARNINGS + 1))
    fi
  fi

  # 9. Check description length (at least 50 chars)
  local desc_len
  desc_len=$(sed -n "${fm_start},${fm_end}p" "$file" | grep -A 50 '^description:' | tail -n +2 | head -20 | grep -v '^[a-z]*:' | grep -v '^$' | wc -c)
  if [ "$desc_len" -lt 50 ]; then
    echo -e "${YELLOW}WARN${NC} $relpath: description may be too short (${desc_len} chars, recommend 50+)"
    WARNINGS=$((WARNINGS + 1))
  fi

  # 10. Check body sections (required: overview/개요, trigger/트리거, workflow/워크플로우)
  local body
  body=$(sed -n "$((fm_end + 1)),\$p" "$file")
  if ! echo "$body" | grep -qiE '(^#.*개요|^#.*overview)'; then
    echo -e "${YELLOW}WARN${NC} $relpath: missing '개요/Overview' section"
    WARNINGS=$((WARNINGS + 1))
  fi
  if ! echo "$body" | grep -qiE '(트리거|trigger)'; then
    echo -e "${YELLOW}WARN${NC} $relpath: missing '트리거 키워드' section"
    WARNINGS=$((WARNINGS + 1))
  fi
  if ! echo "$body" | grep -qiE '(워크플로우|workflow)'; then
    echo -e "${YELLOW}WARN${NC} $relpath: missing '워크플로우' section"
    WARNINGS=$((WARNINGS + 1))
  fi

  # 11. Check usage examples (at least 1)
  if ! echo "$body" | grep -qiE '(예시|example)'; then
    echo -e "${YELLOW}WARN${NC} $relpath: no usage examples found"
    WARNINGS=$((WARNINGS + 1))
  fi

  # 12. Check version banner (forbidden in body)
  if echo "$body" | grep -qE '^> v[0-9]+\.[0-9]+\.[0-9]+ \|'; then
    echo -e "${RED}FAIL${NC} $relpath: version banner in body is forbidden (v1.3.0 policy)"
    ERRORS=$((ERRORS + 1))
  fi

  echo -e "${GREEN}PASS${NC} $relpath"
}

# Main
echo "=== SKILL.md Lint ==="
echo ""

if [ $# -gt 0 ]; then
  target="$1"
  if [ -d "$target" ]; then
    files=$(find "$target" -name "SKILL.md" -not -path "*/.git/*")
  else
    files="$target"
  fi
else
  files=$(find moai-*/skills -name "SKILL.md" -not -path "*/.git/*")
fi

for f in $files; do
  lint_skill "$f"
done

echo ""
echo "=== Summary ==="
echo "Checked: $CHECKED"
echo -e "Errors: ${RED}$ERRORS${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"

if [ "$ERRORS" -gt 0 ]; then
  exit 1
fi
exit 0
