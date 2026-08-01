---
id: SPEC-MOC-PLUGIN-STORY-001
title: "moai-story 플러그인 신설 + 패밀리 v4 재배치"
version: "0.1.0"
status: in-progress
created: 2026-07-06
updated: 2026-07-07
author: GOOS
priority: P1
phase: "v4.0.0"
module: "plugins/moai-story"
lifecycle: spec-anchored
tags: "plugin,story,higgsfield,cowork,v4"
depends_on: ["SPEC-MOC-FAMILY-DRIFT-001"]
---

# DESIGN DOCUMENT

## 1. Architecture Overview

### 1.1 Plugin Family v4 Structure

```
plugins/
├── moai-cowork/          # v4.0.0 (171 skills, 8 MCP)
│   ├── .claude-plugin/plugin.json
│   ├── .mcp.json
│   └── skills/
│       ├── content-*     # 콘텐츠 마케팅 (잔존)
│       ├── marketing-*   # 마케팅 (잔존)
│       └── ...           # 실무자 용도 스킬 171종
│
├── moai-story/           # v0.1.0 (21 skills, 1 MCP) 🆕
│   ├── .claude-plugin/plugin.json
│   ├── .mcp.json
│   └── skills/
│       ├── book-*        # 이관 8종
│       └── story-*       # 신규 13종
│
├── moai-design/          # v0.x (unchanged)
└── moai-code/            # v3.x (unchanged)
```

### 1.2 청중 분리 모델

| 청중 | 플러그인 | 진입점 | 주요 용도 |
|------|----------|--------|----------|
| 작가·콘텐츠 비즈니스 | moai-story | `/story:*` + 자연어 | 출판·웹툰·웹소설·시나리오·콘티 |
| 비개발 실무자 | moai-cowork | `/project` + 자연어 | 사업·마케팅·법무·재무·HR·교육 |
| 디자이너 | moai-design | `/design:*` | 브랜드·토큰·UI 디자인 |
| 개발자 | moai-code | `/moai:*` | 개발 워크플로우 |

---

## 2. moai-story Plugin Design

### 2.1 Identity

```yaml
# plugins/moai-story/.claude-plugin/plugin.json
{
  "name": "story",
  "displayName": "MoAI Story",
  "version": "0.1.0",
  "description": "작가와 콘텐츠 비즈니스를 위한 플러그인 — 출판 기획·집필부터 웹툰·웹소설·드라마/영화 시나리오·광고/영상 콘티까지. Higgsfield 최신 모델로 캐릭터 일관성 작화·콘티·프리비즈를 생성.",
  "category": "작가·콘텐츠",
  "author": "modu-ai"
}
```

### 2.2 MCP Configuration

```json
// plugins/moai-story/.mcp.json (canonical — §4.1과 단일 형식)
{
  "mcpServers": {
    "higgsfield": {
      "type": "url",
      "url": "https://mcp.higgsfield.ai/mcp",
      "timeout": 120000,
      "headers": { "User-Agent": "MoAI-Story/0.1.0" }
    }
  }
}
```

**설계 결정**:
- OAuth 인증: Claude 커넥터에서 Higgsfield 계정 1회 인증
- API 키 불필요: 자격증명은 Higgsfield 서버 보관
- Timeout 120초: 생성형 작업 대응
- `type: "url"` + `headers.User-Agent`: §4.1 canonical shape와 동일 (3개 변형 금지, 단일 형식만 사용)

### 2.3 Directory Structure

```
plugins/moai-story/
├── .claude-plugin/
│   ├── plugin.json
│   └── claude-plugin-manifest.json  # 자동 생성
├── .mcp.json
├── .claudeignore
└── skills/
    ├── story-project/
    │   ├── SKILL.md
    │   └── skill.yaml
    ├── story-webtoon-planner/
    ├── story-webtoon-episode/
    ├── story-webtoon-art/
    ├── story-webnovel-writer/
    ├── story-synopsis/
    ├── story-screenplay/
    ├── story-conti/
    ├── story-ad-conti/
    ├── story-character-sheet/
    ├── story-cover-art/
    ├── story-previz/
    ├── story-ip-pitch/
    ├── book-concept-planner/      # 이관
    ├── book-target-reader/        # 이관
    ├── book-outline-designer/    # 이관
    ├── book-chapter-writer/       # 이관
    ├── book-revision-coach/       # 이관
    ├── book-author-bio/           # 이관
    ├── book-proposal-writer/      # 이관
    └── book-publisher-matcher/    # 이관
```

---

## 3. Skill Catalog Design

### 3.1 Naming Convention

- **접두어**: `story-` (신규 13종) / `book-` (이관 8종, 유지)
- **형식**: `<카테고리>-<기능>` (cowork 패턴 따름)
- **예시**: `story-webtoon-planner`, `book-concept-planner`

### 3.2 Migrated Skills (8)

| 스킬 | 기능 | 체인 위치 |
|------|------|----------|
| book-concept-planner | 도서 컨셉 기획 | 체인 시작 |
| book-target-reader | 타겟 독자 설정 | 2단계 |
| book-outline-designer | 목차 구조 설계 | 3단계 |
| book-chapter-writer | 장 집필 | 4단계 |
| book-revision-coach | 퇴고 지도 | 5단계 (폴백 있음) |
| book-author-bio | 저자 소개 | 독립 |
| book-proposal-writer | 출판 제안서 | 독립 |
| book-publisher-matcher | 출판사 매칭 | 체인 종단 |

### 3.3 New Skills (13)

#### 3.3.1 Entry Point (1)

| 스킬 | 기능 | Higgsfield |
|------|------|:---:|
| story-project | 작품 유형 파악 → 장르 파이프라인 라우팅 | — |

**라우팅 로직**:
```
사용자 입력 → 유형 분류 → 파이프라인 라우팅
- "소설/출판" → book-* 체인
- "웹툰" → story-webtoon-planner → story-webtoon-episode → story-webtoon-art
- "웹소설" → story-webnovel-writer
- "시나리오" → story-synopsis → story-screenplay
- "콘티" → story-conti
- "광고 콘티" → story-ad-conti
```

#### 3.3.2 Webtoon (3)

| 스킬 | 기능 | Higgsfield |
|------|------|:---:|
| story-webtoon-planner | 세계관·캐릭터·시즌/회차·플랫폼 문법 | — |
| story-webtoon-episode | 컷 분할·대사·연출·말칸 배치 | — |
| story-webtoon-art | 패널 이미지, 캐릭터 일관성 | ✅ AI Anime Generator + Soul ID |

#### 3.3.3 Web Novel (1)

| 스킬 | 기능 | Higgsfield |
|------|------|:---:|
| story-webnovel-writer | 연재 집필, 플랫폼 문법, 절단 설계 | — |

**플랫폼 문법**:
- 문피아: 장르별 태그, 등록 인기 순위
- 카카오페이지: 추천 태그, 연재 주차, 절단 클리프행어

#### 3.3.4 Screenplay (2)

| 스킬 | 기능 | Higgsfield |
|------|------|:---:|
| story-synopsis | 로그라인·기획의도·인물·회차/막 구성 | — |
| story-screenplay | 씬 넘버·지문·대사, 표준 포맷 | — |

**표준 포맷**:
- 한국 방송 작가 협회 포맷
- 영화 시나리오 표준 ( scene heading, action, character, dialogue, transition )

#### 3.3.5 Continuity (2)

| 스킬 | 기능 | Higgsfield |
|------|------|:---:|
| story-conti | 씬 → 프레임 시퀀스 | ✅ Popcorn (8프레임) + Shots (9앵글) |
| story-ad-conti | 제품/브랜드 광고 스토리보드 | ✅ Marketing Studio · Ads 2.0 · Seedance 2.0 |

#### 3.3.6 Character/Cover (2)

| 스킬 | 기능 | Higgsfield |
|------|------|:---:|
| story-character-sheet | 설정 + 비주얼 + Soul ID 훈련 가이드 | ✅ Soul ID |
| story-cover-art | 표지/일러스트, 인쇄 해상도 | ✅ Soul 2.0 + 업스케일 |

#### 3.3.7 Previz/Business (2)

| 스킬 | 기능 | Higgsfield |
|------|------|:---:|
| story-previz | 카메라 무빙 지정 숏 | ✅ DoP + Cinema Studio 3.5 |
| story-ip-pitch | 피칭 문서, 판권/2차 저작 제안 | — |

---

## 4. Higgsfield Integration Architecture

### 4.1 MCP Server Specification (canonical — 모든 .mcp.json 참조는 본 형식으로 단일 통일)

```json
{
  "mcpServers": {
    "higgsfield": {
      "type": "url",
      "url": "https://mcp.higgsfield.ai/mcp",
      "timeout": 120000,
      "headers": {
        "User-Agent": "MoAI-Story/0.1.0"
      }
    }
  }
}
```

### 4.2 Authentication Flow

```
1. 사용자: Claude Code settings → MCP Servers → Higgsfield OAuth
2. Higgsfield: Access token 발급
3. MCP 호출: Authorization: Bearer {access_token}
4. Token 만료 시: Claude Code 자동 갱신
```

### 4.3 Model Routing Table

| 용도 | Higgsfield 모델 | 도구명 | 파라미터 |
|------|-----------------|--------|----------|
| 웹툰 패널 생성 | AI Anime Generator | `generate_anime_panel` | style, character_id, composition |
| 캐릭터 일관성 | Soul ID | `train_character` | images, name, preserve_pose |
| 콘티 8프레임 | Popcorn | `generate_continuity` | scene_description, style |
| 멀티 앵글 탐색 | Shots | `generate_multi_angle` | image_url, grid_size |
| 광고 콘티 | Marketing Studio | `generate_ad_storyboard` | product_url, format |
| 시네마틱 프리비즈 | DoP | `generate_previz` | shot_description, camera_preset |
| 표지/일러스트 | Soul 2.0 | `generate_cover_art` | concept, style, resolution |

### 4.4 Fallback Strategy

**MCP 미연결 시**:

1. 스킬이 MCP 호출 감지
2. "Higgsfield MCP에 연결할 수 없습니다. 프롬프트 온리 모드로 동작합니다." 안내
3. 완성 프롬프트 출력
4. "Higgsfield 웹(https://higgsfield.ai)에 위 프롬프트를 붙여넣으세요." 안내

### 4.5 Credit Estimate Template

```markdown
## 크레딧 안내

이 작업은 Higgsfield 크레딧을 소모합니다:
- 패널 1개: 약 2 크레딧
- 캐릭터 훈련 20장: 약 10 크레딧
- 시네마틱 숏 1개: 약 20~50 크레딧

진행하시겠습니까? (Y/n)
```

---

## 5. Migration Strategy

### 5.1 cowork v4.0.0 Breaking Changes

**변경 사항**:
- book-* 8스킬 제거 (179 → 171)
- higgsfield MCP 제거 (9 → 8)

**사용자 영향**:
- 기존 book-* 스킬 사용자: story 설치 필요
- Higgsfield 사용자: story 설치 후 재인증 필요

### 5.2 Migration Guide

```markdown
# Cowork v4.0.0 마이그레이션 가이드

## 변경 사항

v4.0.0에서 publication/creative skills (book-*)가 moai-story 플러그인으로 이관되었습니다.

## 영향 받는 스킬

- book-concept-planner
- book-target-reader
- book-outline-designer
- book-chapter-writer
- book-revision-coach
- book-author-bio
- book-proposal-writer
- book-publisher-matcher

## 마이그레이션 절차

### 1. moai-story 설치

```
/plugin install story
```

### 2. Higgsfield 인증 (생성형 스킬 사용 시)

1. Claude Code → Settings → MCP Servers
2. Higgsfield OAuth 연결
3. 계정 인증 완료

### 3. 기존 워크플로우

book-* 스킬은 story 플러그인에서 동일하게 사용 가능합니다.

## 롤백

v4.0.0 이하로 롤백:
```
claude plugin install modu-ai/claude@3.0.0
```
```

### 5.3 Version Policy

**3점 동기화 (D1 정정 — NFR-STORY-003 / DRIFT-001 D14 정합)**:
- plugin.json version = 모든 스킬 SKILL.md version (marketplace plugin entry는 `version` 필드 미기재; marketplace catalog `metadata.version`만 3.0.0 → 4.0.0 승격)
- 검증: `grep '"version":"4.0.0"' plugins/moai-cowork/.claude-plugin/plugin.json` (1건) + `grep -c '"version":"4.0.0"' plugins/moai-cowork/skills/*/SKILL.md` (171건) + `jq '.plugins[].version' .claude-plugin/marketplace.json` (모두 null) + `jq '.metadata.version' .claude-plugin/marketplace.json` ("4.0.0")

**semver 준수**:
- breaking change: 메이저 범프 (4.0.0)
- feature 추가: 마이너 범프 (4.1.0)
- 버그 수정: 패치 범프 (4.0.1)

---

## 6. Documentation Structure

### 6.1 www Docs

```
www/
├── plugins/
│   ├── index.md              # 4 플러그인 개요
│   ├── migration.md          # v4.0.0 마이그레이션 가이드
│   ├── higgsfield-setup.md    # Higgsfield OAuth 설정
│   └── story/
│       ├── user-guide.md     # moai-story 사용자 가이드
│       └── skill-reference.md # 21 스킬 레퍼런스
└── CHANGELOG.md               # v4.0.0 릴리스 노트
```

### 6.2 Plugin CHANGELOG

```markdown
# MoAI Cowork v4.0.0

## Breaking Changes

- publication/creative skills (book-*)가 moai-story 플러그인으로 이관되었습니다.
- higgsfield MCP 연동이 moai-story로 이관되었습니다.

## Migration

`/plugin install story`로 moai-story를 설치하세요.

## Fixes

- 3점 동기화 HARD 규칙 준수
```

---

## 7. Risk Mitigation

### 7.1 Higgsfield Rate Limit

**위험**: Rate limit 미문서화

**완화**:
- 방어적 재시도 안내를 스킬 본문에 의무화
- "서버 과부하 시 잠시 대기 후 재시도하세요." 안내

### 7.2 Higgsfield Tool Surface Change

**위험**: 도구 표면 변경으로 모델 탐색 실패

**완화**:
- 모델명 하드코딩 대신 "용도 기술 → 도구 탐색" 방식으로 서술
- 스킬 본문: "웹툰 패널 생성 기능을 찾아 실행합니다."

### 7.3 Third-Party Model Supply

**위험**: 서드파티 모델 수급 변동 (예: Sora 2 중단설)

**완화**:
- 라우팅 표에서 1순위 배제
- 대안 안내: "현재 Higgsfield 권장 모델: ..."

---

## 8. Future Considerations

### 8.1 Reserved: Self-hosted MCP

Higgsfield 공식 호스티드 MCP가 부적합해질 때의 전환 경로:

1. 공식 SDK 기반 자체 벤더링
2. 구축·유지보수 사용자 부담
3. 사용자 유료 API 키 필요

현재는 **문서화만** — 구현하지 않음.

### 8.2 Reserved: Cowork Split

`claude plugin details` 실측 후 스킬 목록 토큰 비용이 1% 예산을 초과할 경우 분할 재판단:

- 콘텐츠 마케팅 (content-*, marketing-*)
- 실무자 (일반 비개발)
- 분할 기준: 청중 + 토큰 비용

현재는 **분할 없음** — 공식 문서상 기술적 근거 부족.

---

## 9. References

- [05-family-redesign-v2.md](../../../docs/plugin-family-design/05-family-redesign-v2.md) — 설계 정본
- [00-ecosystem-architecture.md](../../../docs/plugin-family-design/00-ecosystem-architecture.md) — 생태계 아키텍처
- Higgsfield Official: https://higgsfield.ai/mcp
- Claude Code Plugins: https://code.claude.com/docs/en/plugins
