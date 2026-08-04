---
description: www 디자인 시스템 규칙 SSOT — 이모지 금지·Lucide 아이콘·4종 폰트·WCAG 대비·mermaid 팔레트. CLAUDE.local.md(gitignored)를 하네스가 읽을 수 있게 인라인.
metadata:
  version: "1.0.0"
  category: "reference"
triggers:
  keywords: ["DS 규칙", "이모지", "대비", "mermaid 색", "폰트", "Lucide"]
---

# DS 규칙 (www 온라인 문서)

> CLAUDE.local.md(gitignored 개인 파일)의 DS 규칙을 하네스가 읽을 수 있게 인라인한 참조. 진실원은 `www/design-system/handoff/`.

## 이모지 — 금지
`www/content/**`, `www/layouts/**`, `www/data/**`에 이모지(`✅❌⚠️🚀💡🟢🟡🔴⭐` 등) 사용 금지. **Lucide 아이콘만.**
예외: `→←↑↓↔` 활자 화살표, `①②③` 원문자, `⌘`.

## 아이콘 — Lucide만
`{{< icon name size class >}}`. 24×24 / `fill="none"` / `stroke-width="2"` / `stroke="currentColor"`. 색은 `tone-primary|success|warning|error|muted|teal|amber` 클래스. 인라인 `<svg>` 직접 삽입 금지.

## 폰트 — 4종 전부 CDN
- **MaruBuri** (제목 h1~h4, 600/700만) — 부리체, **상한 700** (800·900 없음)
- **Pretendard Variable** (본문)
- **Inter** (숫자·영문 지표)
- **JetBrains Mono** (코드·eyebrow·칩·kbd)
금지: OTF/TTF 셀프호스팅, NeoDunggeunmo(둥근모), GowunBatang, Goorm Sans Code.

## CSS 구조
geekdoc `main.scss`/`mobile.scss`/`custom.css`는 **로드하지 않음**. 순서 고정: `moai-ds-tokens` → `moai-ds-base` → `moai-ds` → `moai-ds-docs` → `moai-ds-mascot` → **`moai-ds-v2`(최종 확정 레이어)**. 새 `!important` 추가 금지 (v2에서 소유권 명시).

## 색 대비 — WCAG AA 4.5:1
`cd www && python3 scripts/check-contrast.py` (exit 1 = 미달). 반투명 배경 위 글자 특히 위험 — 인라인 코드는 `--color-primary-active #265240` (최악 6.51:1).

## mermaid 팔레트 (고정)
그린 `#e8f1ec`/`#d6e7de`/`#3d7d5f`/`#265240`, 무채색 `#e6e6e6`/`#d1d1d1`/`#757575`, 경고 `#fbf0dc`/`#c47b2a`, 위험 `#f5dcd7`/`#c44a3a`. **주황·퍼플·마젠타 금지** (Anthropic 브랜드색 `#D97757` 포함 — 정체성 훼손). `foot.html`이 런타임 자동 치환.

## 검증
로컬 `http://localhost:1414/` (Hugo dev). 색 변경 시 `check-contrast.py`. 최소 5페이지 육안 확인.
