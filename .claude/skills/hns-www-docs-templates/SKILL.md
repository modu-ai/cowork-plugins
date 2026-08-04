---
description: www 문서 템플릿 — _index(섹션 허브)/일반 문서/릴리스 노트 frontmatter+본문 골격. 버저닝 3축 규칙 포함.
metadata:
  version: "1.0.0"
  category: "reference"
triggers:
  keywords: ["템플릿", "frontmatter", "_index", "릴리스 노트", "버저닝"]
---

# www 문서 템플릿

## _index.md (섹션 허브)
```yaml
---
title: "섹션 제목"
weight: <정수, 낮을수록 위>
description: "검색/SEO용 한 줄"
geekdocBreadcrumb: true
geekdocCollapseSection: true|false
geekdocAnchor: false          # 홈은 false
geekdocNav: false             # 홈(전폭 랜딩)은 false
aliases: ["/old-url/"]
date: 2026-08-05
lastmod: 2026-08-05
ia_in_scope: true             # REQ-IA-024: 규약 적용 집합 (기계 식별)
---
```

## 일반 문서 (guide/cookbook/moai-agents)
동일 frontmatter + 본문 구조:
- **prose-first** (REQ-IA-018): why → when → how 서사. 표/목록은 보조만.
- **mermaid 최소 1개** (REQ-IA-019)
- DS HTML 클래스 (`cw-termlogo`, `cw-flow`, `cw-caps`) + 숏코드 적극 활용
- **이중 톤** (REQ-IA-021): 데스크탑 축은 비개발자 비유; CLI 축은 정확한 기술 용어를 친근한 산문으로
- **Sources 섹션** (REQ-IA-020): 페이지 끝 출처 블록

## 릴리스 노트 (releases/vX.Y.Z.md)
```yaml
---
title: "v1.2.0"
weight: <높을수록 최신이 위>
description: "..."
geekdocBreadcrumb: true
date: 2026-08-05
lastmod: 2026-08-05
---
```
본문: 메타(날짜·버전·`/plugin marketplace update moai-cowork`) → `## 하이라이트` → `## 무엇이 달라지나`(비교표) → 상세 섹션 → `## 사용자가 해야 할 일` → `## 버전`.
추가 시: `_index.md` 표 + `data/menu/main.yaml` 릴리스 섹션 + `hugo.toml params.version` 동기화.

## 버저닝 (3축 독립 — 자리 상한 100)
| 축 | 기록 위치 | 올리는 시점 |
|---|---|---|
| moai-cowork | `hugo.toml params.version` + `marketplace.json metadata.version` | 사이트·문서 구조 변경 시 |
| 플러그인 17종 | `plugin.json` + `marketplace.json` entry | 그 플러그인 수정 시 |
| 스킬 | `SKILL.md` frontmatter `version` | 그 스킬 수정 시 |

**plugin.json == marketplace.json 동기화 필수** (한쪽만 올리는 실수가 가장 흔함).
