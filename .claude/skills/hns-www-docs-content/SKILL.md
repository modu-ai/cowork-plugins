---
description: www 문서 멀티모달 콘텐츠 가이드 — mermaid(직접)/SVG(직접)/Higgsfield(Skill 위임) 선택 기준 + 위임 계약. REQ-IA-019 per-page mermaid.
metadata:
  version: "1.0.0"
  category: "reference"
triggers:
  keywords: ["mermaid", "svg", "인포그래픽", "higgsfield", "다이어그램", "이미지"]
---

# 멀티모달 콘텐츠 (mermaid · SVG · Higgsfield)

## 선택 기준
| 콘텐츠 종류 | 방식 | 이유 |
|---|---|---|
| 구조/플로우/시퀀스/상태 다이어그램 | **mermaid 직접** | `foot.html`이 DS 팔레트 자동 적용 |
| 정확한 숫자/라벨/한국어 인포그래픽 | **인라인 SVG 직접** | AI 래스터는 한국어 텍스트 부정확 |
| 히어로/장식/실사/로고 | **Higgsfield Skill() 위임** | 디자인 정합 이미지 |

## mermaid — 직접 작성
` ```mermaid ` 코드블록 직접 삽입. 패턴: `flowchart`(개념), `sequenceDiagram`(절차), `stateDiagram`(라이프사이클), `journey`.
- **REQ-IA-019**: 모든 in-scope 페이지(`ia_in_scope: true`)는 최소 1개 mermaid 포함
- 라벨에 이모지 금지 (ASCII `[v] [x] *` 만)
- 팔레트: `foot.html` 자동 치환 — 작성자가 색 하드코딩 금지

## SVG — 직접 저작
<<<<<<< HEAD
`plugins/moai-officer/skills/doc-html-slide/references/inline-svg-infographics.md` 패턴 참조.
=======
`plugins/moai-officer/skills/office-html-slide/references/inline-svg-infographics.md` 패턴 참조.
>>>>>>> origin/main
- `font-family`: Pretendard / Noto Sans KR
- `text-anchor`, `dominant-baseline` 명시
- viewBox 16:9(1280×720) 또는 1:1(1080×1080)
- 패턴: KPI 카드 · 막대/도넛 차트 · 타임라인 · 비교 카드

## Higgsfield — Skill() 위임
히어로/장식/로고는 Skill()로 위임 (내부적으로 `media-higgsfield-core`에 실행 위임 — REQ-010: `models_explore`→`get_cost`→`generate`→`poll`):
- 로고 → `Skill("moai-designer:design-logo")` (recraft_v4_1 벡터)
- 히어로/OG/목업 → `Skill("moai-designer:design-brand-visual")`
- 일반 이미지 → `Skill("moai-media:media-higgsfield-image")`
- 영상 → `Skill("moai-media:media-higgsfield-video")`

## 하이브리드 오버레이 (정확한 한국어 숫자 필요 시)
Higgsfield 래스터 이미지 + SVG 텍스트 레이어를 겹쳐라. AI 래스터는 한국어 텍스트를 정확히 렌더링하지 못한다 (`image-backend-policy.md` 강제).
