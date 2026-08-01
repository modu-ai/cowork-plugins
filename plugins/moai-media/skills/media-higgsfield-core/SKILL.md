---
name: media-higgsfield-core
description: |
  Higgsfield MCP 이미지·영상 생성의 공유 코어. media-higgsfield-image / media-higgsfield-video가
  로드하는 SSOT(single source of truth)로, 호출 스키마·라이브 카탈로그 조회 프로토콜·공통 크래프트
  규칙(R1–R5)·인터뷰 슬롯·잡 수명주기를 정의합니다.
  다음과 같은 상황에서 로드됩니다:
  - media-higgsfield-image 또는 media-higgsfield-video가 호출 계약을 참조할 때
  - Higgsfield 모델의 파라미터를 하드코딩하지 않고 런타임 조회해야 할 때
  - namespace(mcp__higgsfield__ vs mcp__claude_ai_higgsfield__)를 런타임 해석해야 할 때
  이 스킬은 단독 실행 스킬이 아니라 두 소비 스킬이 참조하는 공유 코어입니다.
version: "1.0.0"
---

# Higgsfield 코어 (media-higgsfield-core)

> `moai-media` | 이미지·영상 스킬의 공유 SSOT (참조 전용 코어)

## 개요

이 스킬은 `media-higgsfield-image`와 `media-higgsfield-video`가 공통으로 참조하는 코어다. 두 소비 스킬은 호출 계약·조회 순서·공통 규칙을 여기서 가져온다. **핵심 설계 원칙: 파라미터(모델 id·enum·aspect·duration·media role·비용)는 절대 하드코딩하지 않고 런타임에 `models_explore`로 조회한다. 프롬프트 크래프트만 정적으로 큐레이션하고 출처를 단다.**

이 설계가 필요한 이유는 두 축이 서로 다른 진실원을 갖기 때문이다:

| 축 | 진실원 | 스킬이 얻는 방법 |
|---|---|---|
| 파라미터 | 라이브 MCP | `models_explore` / `show_marketing_studio` / `presets_show` / `get_cost` (호출 시점) |
| 프롬프트 크래프트 | 모델 벤더 공식 문서 | 계열별 `prompt-craft/*.md` (저술 시점 고정, 출처·Evidence tier 표기) |

## 코어 참조 파일

| 파일 | 역할 |
|---|---|
| `references/call-schema.md` | 중첩 `params{}` 형태 계약, `medias[].role/.value` 규칙, namespace 런타임 해석, 존재하지 않는 파라미터 안티패턴 |
| `references/catalog-protocol.md` | `models_explore` 등 라이브 조회 도구와 표준 순서(REQ-010), 범위 밖 모델 폴백 |
| `references/universal-rules.md` | R1–R5 벤더 교차 공통 규칙 |
| `references/interview-schema.md` | 크래프트 파일이 소비하는 수집 슬롯 |
| `references/job-lifecycle.md` | `get_cost` 프리플라이트, `credits` 규칙, `adjustments` 리드백, 폴링·오류 분류, 잔액 정지 |

## 오케스트레이션 계약 (REQ-010 흐름)

소비 스킬은 다음 순서를 따른다:

1. **의도 → 후보 좁히기** — 사용자 요청에서 계열 후보를 추린다(크래프트 노트 참조). 후보를 좁힐 뿐 파라미터를 단정하지 않는다.
2. **라이브 조회** — `models_explore(action:'get')`로 실제 제약을 가져온다. Marketing Studio 계열이면 `show_marketing_studio`.
3. **비용 프리플라이트** — `get_cost: true`로 `credits` 확인(크레딧 0). `adjustments` 확보.
4. **생성** — 조회된 값으로만 호출.
5. **폴링·리드백** — `job_status`로 `completed`까지, `adjustments`를 사용자에게 보고.

## namespace 런타임 해석

Higgsfield 도구의 namespace 접두사는 등록 방식에 따라 `mcp__higgsfield__` 또는 `mcp__claude_ai_higgsfield__`다. 스킬은 호출 직전 실제 노출된 namespace를 런타임에 확인하고 그 접두사를 쓴다. 어느 하나를 유일 정답으로 하드코딩하지 않는다. 상세는 `references/call-schema.md` §3.

## 인터뷰 경계

이 스킬(및 서브에이전트)은 사용자에게 직접 질문하지 않는다. 수집할 슬롯을 문서화할 뿐이며, 실제 질문은 오케스트레이터가 진행한다. 슬롯이 비면 구조화된 blocker 보고를 반환한다. 상세는 `references/interview-schema.md`.

## 관련 스킬

| 스킬 | 관계 |
|---|---|
| `moai-media:media-higgsfield-image` | 소비: 이미지 생성 |
| `moai-media:media-higgsfield-video` | 소비: 영상 생성 |
| `moai-media:media-higgsfield-identity` | 소비: Soul·Element 일관성 참조 |
| `moai-media:media-higgsfield-assets` | 소비: 3D·오디오·영상 분석·후처리 |
| `moai-media:media-higgsfield-explainer` | 소비: 블록 조립형 설명 영상 |
| `moai-media:media-higgsfield-product` | 소비: 제품 촬영 10모드 |
| `moai-designer:design-brand-visual` | 소비(교차 플러그인): 브랜드 정합 비주얼 |
| `moai-story:story-*` | 소비(교차 플러그인): 작화·콘티·표지·캐릭터 |

## 출처

- [Higgsfield Skills (공식 agent 문서)](https://github.com/higgsfield-ai/skills)
- [Higgsfield MCP](https://higgsfield.ai/mcp)
- 라이브 카탈로그 스냅샷: `.moai/specs/SPEC-MOC-HIGGSFIELD-PROMPT-001/mcp-catalog-snapshot.md` (plan 단계 증거 기준선, 런타임 계약 아님)
