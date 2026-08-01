# 모두의클로드 플러그인 — 4-plugin 재설계 계획 (확정)

## Context

goos.kim "플러그인=AI 직원" 발상의 최종 귀결 — **4-plugin (코워커·디자이너·코더·PM)**. 디자이너를 코워커에서 분리하여 전문성 명확화. 비개발자 한국 타깃.

**4개 AI 직원 플러그인** (한글 displayName):
| 플러그인 | 한글명 | 역할 | 스킬 |
|---|---|---|---|
| `moai-coworker` | **코워커** | 실무 + 글쓰기 작가/IP 통합 (올인원 동료) | cowork(172) + story(21) = ~193 |
| `moai-designer` | **디자이너** | 디자인 전담 (브랜드·시스템·Claude Design 핸드오프) | design(12) |
| `moai-coder` | **코더** | 개발 (SPEC DDD/TDD·품질 게이트) | code(28) |
| `moai-pm` | **PM** | 프로젝트 초기화 허브 (`/project --cowork`·`--designer`·`--code`) | project 라우터 + init 스킬 |

**컨셉**: 코워커는 실무+작가 모자 교체, 디자이너·코더는 전문 분리, PM은 셋업 허브. story(작가/IP)는 코워커에 흡수(별도 플러그인 X).

---

## 아키텍처

```
moai-coworker (코워커, ~193스킬)        ← 실무 + 글쓰기 작가 올인원
  내부 역할 라벨: 실무 / 글쓰기 작가(IP·출판·웹툰·시나리오)
  자연어 → 역할 자동 감지 → 스킬 체인
  (cowork + story 스킬 본문 통합 보존)

moai-designer (디자이너, 12스킬)        ← 디자인 전담
  브랜드·디자인시스템·Claude Design 핸드오프·GAN 루프

moai-coder (코더, 28스킬)               ← 개발 전담
  SPEC plan/run/sync + commands/agents (정본 MoAI-ADK 패턴)

moai-pm (PM)                            ← 프로젝트 초기화 허브
  /project --cowork     →  코워커 체인 init (8-Phase → CLAUDE.md)
  /project --designer   →  디자이너 브랜드 컨텍스트 셋업
  /project --code       →  코더 개발 환경 셋업 (.claude/.moai/CLAUDE.md/MCP 정본 패리티)
  project 라우터 스킬 (cowork에서 이관)
```

---

## Phase 1 — 4-plugin 생성·통합

| M | 작업 | 상세 | 의존성 |
|---|---|---|---|
| M1.1 | `moai-coworker` 스캐폴드 | cowork + story 스킬 통합 (본문 보존). plugin.json (name=moai-coworker, displayName="코워커"). 내부 역할 라벨 2종(실무/글쓰기 작가) | STORY-001 완료 후 |
| M1.2 | `moai-designer` 개명 | moai-design → moai-designer (name·displayName="디자이너") | M1.1 후 |
| M1.3 | `moai-coder` 개명 | moai-code → moai-coder (name·displayName="코더"). commands/agents 유지 | M1.1 후 |
| M1.4 | `moai-pm` 스캐폴드 | 신규. project 라우터 스킬(cowork 이관). plugin.json (name=moai-pm, displayName="PM") | M1.1 후 |
| M1.5 | plugin.json name 정합 | 4-plugin name 필드 marketplace와 일치 (근본 버그 해소) | M1.1-M1.4 |
| M1.6 | marketplace.json 4-plugin 재구성 | moai-coworker·moai-designer·moai-coder·moai-pm 선언. 한글 displayName·카테고리·"이런 분께 추천" | M1.5 |

---

## Phase 2 — PM /project 스킬 (사용자 핵심 요구)

| M | 작업 | 상세 |
|---|---|---|
| M2.1 | `/project --cowork` 스킬 | 코워커 체인 init. 8-Phase(인터뷰→인벤토리→체인설계→CLAUDE.md). 실무/작가 역할 맥락 주입 |
| M2.2 | `/project --designer` 스킬 | 디자이너 브랜드 컨텍스트 셋업 (.moai/project/brand/ + DESIGN.md) |
| M2.3 | `/project --code` 스킬 | 코더 개발 환경 셋업. 정본 `internal/template/templates/` 패리티 (.claude/.moai/CLAUDE.md/.mcp.json) |
| M2.4 | PM 라우터 스킬 | 자연어 + `--cowork`/`--designer`/`--code` 플래그 분기 |
| M2.5 | PM README | /project 사용법, 비개발자 가이드 |

---

## Phase 3 — 역할 라벨 + 비개발자 UX

| M | 작업 |
|---|---|
| M3.1 | 코워커 역할 라벨 2종(실무/글쓰기 작가) 자동 교체 ("[작가 모자 착용]") |
| M3.2 | 진입 UX (시스템이 먼저 말 + 자기소개 2문장 + 3단 progressive disclosure) |
| M3.3 | 비개발자 설치 가이드 (4플러그인 한 줄 블록 + 그림 5장) |
| M3.4 | README 재작성 (4개, 한글 페르소나 정체성) |

---

## Phase 4 — 검증

| M | 작업 |
|---|---|
| M4.1 | `/plugin install moai-coworker` (및 designer/coder/pm) 성공 (근본 버그 해소) |
| M4.2 | `/project --cowork`/`--designer`/`--code` → 각 셋업 산출물 생성 |
| M4.3 | 코워커 자연어 → 실무/작가 역할 자동 분기 |
| M4.4 | 디자이너·코더 전문 진입 |

---

## 의존성 · 순서

1. **STORY-001 병렬 세션 완료 대기** — 4-plugin v4.0.0(cowork/code/design/story) 안정화. 그 위에 재구성: story→coworker 흡수, design→designer·code→coder 개명, pm 신규
2. **Phase 1 → 2 → 3 → 4**
3. **M1.5 name 정합** = 근본 버그 해소 (모든 설치 가이드 전제)

> 스킬 본문은 전부 보존(재작성 아님). 변경은 플러그인 래핑(name·displayName·통합·개명) + PM 신규.

---

## 핸드오프 지침 (다음 세션)

다음 세션은 **STORY-001 완료 확인 후 Phase 1 M1.1(coworker 통합)** 부터. 상세는 memory + 본 plan.

재개 조건:
1. 병렬 STORY-001 완료 (`git log` 커밋 종료, 4-plugin v4.0.0 안정)
2. cowork/design/code/story 스킬 재실측
3. M1.1 — moai-coworker(cowork+story 통합) → M1.2 designer · M1.3 coder 개명 → M1.4 pm 신규 → M1.5 name 정합 → M1.6 marketplace 4-plugin
