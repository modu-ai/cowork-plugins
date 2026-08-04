---
description: www 빌드/검증 레시피 — hugo 빌드 + WCAG 대비(check-contrast.py) + 내부 링크(check-links.mjs). /harness:www-docs verify 게이트.
metadata:
  version: "1.0.0"
  category: "verify"
triggers:
  keywords: ["verify", "빌드", "대비 검사", "check-contrast", "hugo", "check-links"]
---

# www 검증 레시피

## 3-in-1 검증 (design-goal-check.sh와 동일 계약)
```bash
cd www
hugo --logLevel error              # 빌드 (exit 0 = 오류 없음)
python3 scripts/check-contrast.py  # WCAG AA 4.5:1 대비 (exit 1 = 미달)
node scripts/check-links.mjs       # 내부 링크 (exit !=0 = 깨진 링크)
```

## 병렬 실행 (agent-common-protocol § Parallel Execution)
3개는 **독립 읽기** → 한 턴에 병렬 Bash로 실행. 각 exit 코드로 PASS/FAIL 판정.

## PASS 기준 (must-pass)
- `hugo` exit 0
- `check-contrast.py` exit 0
- `check-links.mjs` exit 0

## FAIL 시 복구
- **hugo 오류**: frontmatter YAML / 숏코드 문법 / 마크다운 문법 수정
- **대비 미달**: 색 조합 수정 (`!important` 대신 `moai-ds-v2.css`에서 소유권 명시). 새 표면은 `check-contrast.py`의 `PAIRS`에 한 줄 추가.
- **깨진 링크**: `aliases` 추가 또는 실제 페이지 경로로 수정

## 로컬 확인
`http://localhost:1414/` (Hugo dev server). 색 변경 시 `check-contrast.py` 병행. 최소 5페이지 육안: `/` · `/getting-started/quick-start/` · `/guide/cowork/intro/` · `/plugins/` · `/releases/`.

## data SSOT 재생성 (sync 시)
플러그인/스킬/에이전트 변경 후 `data/agent_teams.json`은 반드시 스크립트로 재생성:
```bash
python3 www/scripts/gen-agent-teams.py   # marketplace.json + frontmatter → agent_teams.json
```
직접 편집 금지 (드리프트).
