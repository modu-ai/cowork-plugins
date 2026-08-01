---
name: media-codex-image
description: |
  codex CLI의 내장 image_gen 도구로 **gpt-image-2** 이미지를 생성합니다 — ChatGPT OAuth 인증으로 **API 키 불필요**, ChatGPT Plus/Team/Enterprise 구독 한도로 동작합니다.

  다음과 같은 요청 시 사용하세요:
  - "codex로 이미지 만들어줘", "codex 이미지 생성", "codex image"
  - "gpt-image-2로 이미지 만들어줘", "GPT Image 2 생성"
  - "API 키 없이 이미지 생성해줘"
  - "로컬에서 이미지 생성", "ChatGPT 구독 한도로 이미지"
  - "/media-codex-image" (직접 호출)

  프롬프트가 복잡하거나 한국어 텍스트가 들어가면 `moai-media:media-gpt-image-2-prompt`(6-Block 프롬프트 빌더)로 먼저 프롬프트를 빌드한 뒤 이 스킬로 생성하세요. Higgsfield MCP가 연결돼 있지 않거나 로컬 개발·ChatGPT 구독 한도 재사용이 목적이면 이 스킬을 사용합니다 (프로덕션·CI·멱등은 `media-higgsfield-image` 권장).
version: "1.0.0"
---

# media-codex-image — codex CLI(gpt-image-2) 이미지 생성기

> moai-coworker | 로컬 이미지 생성 (codex CLI OAuth, API 키 불필요)

## 개요

`codex CLI`의 내장 `image_gen` 도구를 호출해 **gpt-image-2** 모델로 이미지를 생성합니다. 핵심은 **OpenAI REST API를 직접 호출하지 않고 `codex exec` 브릿지를 경유**한다는 점 — ChatGPT OAuth 세션 토큰(`~/.codex/auth.json`)을 이미지 생성 서비스로 라우팅해 **API 키(`sk-*`) 없이 ChatGPT 구독 한도**로 동작합니다.

특히 본 스킬은:

- **API 키 불필요** — `codex login` 1회 OAuth로 ChatGPT 구독(Plus/Team/Enterprise) 한도 사용. `OPENAI_API_KEY` 관리 부담 없음.
- **6-Block 프롬프트 연동** — `media-gpt-image-2-prompt`가 빌드한 OpenAI Cookbook 6-Block 프롬프트(Subject·Action·Scene·Composition·Lighting·Style&Text)를 그대로 codex에 전달.
- **한국어 verbatim 보장** — 이미지 내 한글 텍스트는 따옴표·ALL CAPS·verbatim 지시로 gpt-image-2의 95%+ 텍스트 렌더링 정확도 활용.
- **media-higgsfield-image 대체 경로** — 같은 gpt-image-2를 Higgsfield MCP 경로(`media-higgsfield-image`)로도 호출 가능. 백엔드 선택은 환경·비용 선호에 따라.

## 트리거 키워드

codex 이미지 codex image gpt-image-2 생성 GPT Image 2 API 키 없이 이미지 로컬 이미지 생성 ChatGPT 구독 한도 이미지 codex exec image_gen

## 핵심 인사이트 — OAuth 브릿지 (왜 codex exec인가)

OpenAI의 모든 인증 경로를 테스트한 결과 (참고: [wjb127/codex-image](https://github.com/wjb127/codex-image) MIT):

| 방식 | 동작 | 비고 |
|---|---|---|
| `OPENAI_API_KEY` → REST API | ✅ | 표준이지만 API 키 관리 부담 |
| **OAuth 토큰 → REST API 직접** | ❌ **401** | OAuth 토큰은 세션 토큰이지 API 키가 아님 |
| **OAuth 토큰 → `codex exec` → `image_gen`** | ✅ **본 스킬** | codex exec 내부 브릿지가 OAuth를 이미지 생성 서비스로 라우팅 |

```
codex login (최초 1회)
  → OAuth 토큰이 ~/.codex/auth.json에 저장
    → codex exec가 토큰을 자동 읽기
      → 내장 image_gen 도구가 OAuth로 인증
        → gpt-image-2가 이미지 생성
          → 프로젝트 디렉토리에 저장
```

> **주의**: OAuth 토큰으로 OpenAI REST API를 직접 호출하면 HTTP 401. 반드시 `codex exec` 브릿지를 거쳐야 합니다.

## 전제 — codex CLI 설치 + 로그인

| 요구사항 | 명령 | 비고 |
|---|---|---|
| **codex CLI** | `npm install -g @openai/codex` | 이미지 생성 엔진 |
| **codex login** | `codex login` | ChatGPT로 최초 1회 OAuth |

```bash
# 설치·인증 확인
codex --version          # OpenAI Codex v0.1xx.x
codex login status       # "Logged in using ChatGPT"
```

> Cowork 환경에서 Bash가 제한되면 codex CLI 호출이 차단될 수 있습니다. 이 스킬은 **로컬 Claude Code(터미널) 또는 Bash 허용 Cowork 환경**에서 동작합니다. Bash 제한 시 사용자에게 codex 명령어를 안내만 하고 수동 실행을 유도하세요.

## 워크플로우

```
1. 컨텍스트 수집 — 주제·화면비·품질·출력 경로·장수
   (복잡한 프롬프트/한국어 텍스트 → media-gpt-image-2-prompt로 6-Block 프롬프트 빌드 선행)
    ↓
2. 인자 조립 — --size · --quality · --out · -n + 프롬프트
    ↓
3. codex exec 호출 — image_gen 도구가 gpt-image-2로 생성
    ↓
4. 이미지 수집 — ~/.codex/generated_images/<session>/ → --out 디렉토리로 복사
    ↓
5. 출력 — 타임스탬프 파일명(codex-image-YYYYMMDD-HHMMSS.png) + 인라인 표시
```

## 옵션

| 플래그 | 값 | 기본값 | 설명 |
|---|---|---|---|
| `--size` | `1024x1024` · `1024x1536` · `1536x1024` · `auto` | `1024x1024` | 이미지 크기 (정사각·세로·가로) |
| `--quality` | `low` · `medium` · `high` · `auto` | `auto` | 생성 품질 (높을수록 느리고 비쌈) |
| `--out` | 디렉토리 경로 | 프로젝트 루트 | 저장 위치 |
| `-n` | 1–10 | `1` | 생성 장수 |

## 호출 패턴

### 기본 — 자연어 한 줄

```bash
codex exec "Use \$imagegen to create a 1024x1024 image: a red apple on white background, studio lighting. Save to ./apple.png"
```

### 고품질 + 특정 폴더

```bash
codex exec "Use \$imagegen. Generate a 1536x1024 aerial view of jeju island coastline, golden hour. quality high, save to ./public/images/jeju.png"
```

### 여러 변형

```bash
# -n 3 처럼 루프 — codex exec를 3회 호출하거나 한 턴에 3장 지시
codex exec "Use \$imagegen. Create 3 logo variations for a tech startup, minimal, geometric. size 1024x1024, save to ./logos/"
```

### 구조화 출력 + 파이프라인 통합

```bash
codex exec --json --output-last-message ./last.txt \
  "Generate a 1536x1024 productivity-visual hero, save under output/imagegen/hero.png"
```

### 한국어 텍스트 이미지 (verbatim 보장) ★

gpt-image-2의 한국어 렌더링 정확도를 극대화하려면 **따옴표 + verbatim 지시 + 폰트 무게·색·위치** 명시:

```bash
codex exec "Use \$imagegen. Text (verbatim, 한글): '2026년 분기 실적'. Typography: bold sans 한글, 검정, 상단 중앙. Require verbatim rendering, no extra characters. quality high, size 1536x1024, save to ./slide-q1.png"
```

> 한국어 텍스트 정확도 규칙은 `moai-media:media-gpt-image-2-prompt`의 `references/text-rendering.md`와 동일한 원칙을 따릅니다.

## 6-Block 프롬프트 체이닝 (권장)

복잡한 장면이나 에디토리얼 품질이 필요하면 `media-gpt-image-2-prompt`로 먼저 프롬프트를 빌드하세요:

```
사용자 자연어 → moai-media:media-gpt-image-2-prompt (6-Block 프롬프트 빌드)
                    ↓ 산출: 6-Block 자연어 단락
              moai-media:media-codex-image (해당 프롬프트로 codex exec 호출 → gpt-image-2 생성)
```

이 흐름은 `media-higgsfield-image` 경로와 동일한 프롬프트 SSOT를 공유합니다 — 같은 프롬프트로 Higgsfield(GPT Image 2) 또는 codex(gpt-image-2) 백엔드를 선택해 생성할 수 있습니다.

## 백엔드 선택 — higgsfield vs codex

같은 gpt-image-2·Nano Banana Pro 모델을两条 경로로 호출 가능. 환경·비용·목적에 따라 선택:

| 기준 | `media-higgsfield-image` (Higgsfield MCP) | `media-codex-image` (codex CLI) |
|---|---|---|
| 인증 | Higgsfield API 키 (MCP) | ChatGPT OAuth (API 키 불필요) |
| 비용 | Higgsfield 크레딧 | ChatGPT 구독 한도 |
| 적합 | 프로덕션·CI·멱등·무인 자동화 | 로컬 개발·구독 한도 재사용·API 키 회피 |
| 모델 범위 | 11종(Soul·Nano Banana Pro·GPT Image 2·Seedream 등) | gpt-image-2 단일 |
| MCP 의존 | 필요 (`moai-coworker/.mcp.json`) | 불필요 (codex CLI 별도 설치) |

상세 백엔드 정책은 [`moai-officer:office-html-slide` references/image-backend-policy.md](../../../moai-coworker/skills/office-html-slide/references/image-backend-policy.md) 참조.

## 출력

이미지는 타임스탬프 파일명으로 저장돼 덮어쓰기를 방지합니다:

```
codex-image-20260619-143052.png        # 단일
codex-image-20260619-143052-1.png      # 복수: 첫 번째
codex-image-20260619-143052-2.png      # 복수: 두 번째
```

생성된 이미지는 Claude Code에서 즉시 확인할 수 있도록 인라인으로 표시합니다.

## 프롬프트 팁

gpt-image-2는 reasoning-driven 모델로 **art-director 어조의 자연어 단락**이 키워드 나열보다 우수합니다 (OpenAI Cookbook 권장).

- **구조**: Scene/backdrop → Subject → Details → Constraints
- **조명 구체화**: "warm golden hour side light" > "good lighting"
- **카메라 언어**: "shallow depth of field", "aerial view", "close-up macro"
- **스타일 명시**: "photorealistic", "oil painting style", "3D render", "concept art"
- **무드/품질**: "serene", "8K detail", "ultra detailed"
- **네거티브 프롬프트 미지원** — gpt-image-2는 부정 지시 대신 긍정 묘사로 회피

상세 6-Block 구조는 `media-gpt-image-2-prompt`의 `references/prompt-blocks.md` 참조.

## 주의사항

- **Bash 의존** — codex CLI는 터미널 도구. Claude Code 메인 세션 또는 Bash 허용 환경에서만 동작. Bash 제한 Cowork에서는 codex 명령어 안내만 하고 수동 실행 유도.
- **구독 한도 소모** — 이미지 생성 턴은 일반 턴 대비 한도를 3~5배 빨리 소모 (OpenAI 공식). 대량 생성 시 주의.
- **투명 배경 미지원** — gpt-image-2는 투명 PNG 불가. 투명 필요 시 크로마키 폴백.
- **승인 정책** — `--dangerously-bapprovals-and-sandbox`는 CI/샌드박스만. 로컬은 `-s workspace-write`로 범위 제한 권장.
- **텍스트/레이아웃 중심 슬라이드** — HTML/CSS 코드 경로 우선 (imagegen "When not to use" 권고). 인포그래픽 숫자·라벨은 인라인 SVG가 정확.

## 비용

이미지 생성 비용은 ChatGPT 구독(Plus/Team/Enterprise) 한도로 청구:

| 크기 | 품질 | 대략적 비용 |
|---|---|---|
| `1024x1024` | `low` | ~$0.02 |
| `1024x1024` | `high` | ~$0.04 |
| `1024x1536` | `high` | ~$0.06 |

> 현재 gpt-image-2 요금은 OpenAI 프라이싱 페이지 확인.

## 보안

- **API 키 저장/전송 없음** — OAuth only
- **텔레메트리 없음** — 추적·에러 리포팅 없음
- **이미지 로컬 저장** — 프로젝트 디렉토리에만, 외부 업로드 없음
- **단일 외부 연결** — codex CLI를 통한 `api.openai.com`만

## 문제 해결

| 문제 | 해결 |
|---|---|
| `NOT_FOUND` (codex 없음) | `npm install -g @openai/codex` |
| 인증 만료 | `codex login` 재실행 |
| Trust 오류 | 프로젝트를 `~/.codex/config.toml` 신뢰 목록 추가 또는 `--skip-git-repo-check` |
| 타임아웃 (>2분) | `--quality low`로 속도 향상 |
| 401 on REST API | 예상 동작 — OAuth 토큰은 REST 직접 호출 불가. `codex exec` 사용. |
| `image_gen` 도구 없음 | `npm update -g @openai/codex` |

## 관련 스킬

| 스킬 | 관계 | 설명 |
|---|---|---|
| media-gpt-image-2-prompt | before | 6-Block 프롬프트 빌더 — 복잡한 장면·한국어 텍스트 시 선행 |
| media-higgsfield-image | alternative | Higgsfield MCP 경로 (API 키, 프로덕션/CI). 같은 gpt-image-2·Nano Banana Pro 모델 |
| media-gemini-3-image-prompt | sibling | Gemini 어조 프롬프트 (Nano Banana Pro) |

## 출처

1차 (공식):
- [OpenAI Codex CLI — GitHub](https://github.com/openai/codex) — codex CLI 공식, `image_gen` 내장 도구
- [OpenAI Cookbook — GPT Image Generation Models Prompting Guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide) — 6-Block 프롬프트 구조

참고 스킬 (MIT):
- [wjb127/codex-image](https://github.com/wjb127/codex-image) — Claude Code 스킬, OAuth 브릿지 패턴·옵션·출력 파일명 규약 참고. 본 스킬은 wjb127의 핵심 인사이트(OAuth→REST 401, codex exec 브릿지)를 채택하고 moai-coworker 정책(6-Block 체이닝·한국어 verbatim·higgsfield 백엔드 선택)으로 확장했습니다.
