# moai-media

> AI 이미지 프롬프트 빌더 + 음성 생성 — Higgsfield MCP·ElevenLabs MCP 통합 컴패니언 플러그인

[![버전](https://img.shields.io/badge/version-2.22.0-blue)](../CHANGELOG.md)
[![라이선스](https://img.shields.io/badge/license-MIT-green)](../LICENSE)
[![스킬](https://img.shields.io/badge/skills-6-success)](#스킬-카탈로그-6종)

## 개요

`moai-media`는 AI 이미지·음성 작업의 **프롬프트와 음성 합성 전담 플러그인**입니다.

- **이미지 프롬프트 빌더 3종** — OpenAI GPT-image-2 / Google Gemini 3 Pro Image / Midjourney v8.1 공식 가이드를 그대로 적용한 텍스트 프롬프트 빌더. ChatGPT·Google AI Studio·Discord에 복붙 가능한 형식으로 출력합니다.
- **음성 생성 1종** — ElevenLabs MCP 기반 TTS·보이스 클로닝·다국어 더빙·효과음 생성.

이미지·영상의 **실제 렌더링**은 별도 MCP가 담당합니다 (예: Higgsfield MCP의 Soul·DOP·캐릭터·말하는머리 등). 본 플러그인은 텍스트 프롬프트 산출과 음성 합성에 집중합니다.

## 스킬 카탈로그 (6종)

### 이미지 프롬프트 빌더 (3)

| 스킬 | 공식 가이드 | 산출물 |
|---|---|---|
| [`gpt-image-2-prompt`](skills/gpt-image-2-prompt/SKILL.md) | [OpenAI Cookbook](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide) | 6-Block 구조(Subject·Action·Scene·Composition·Lighting·Style&Text) + 편집 2-column 로직 + 텍스트 verbatim 다국어 |
| [`gemini-3-image-prompt`](skills/gemini-3-image-prompt/SKILL.md) | [Google AI for Developers](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image-preview) | 5-component 영문 문장 + Creative Director 어조 + 14 reference 슬롯 + Search Grounding + Thinking/Fast 모드 |
| [`midjourney-v8-prompt`](skills/midjourney-v8-prompt/SKILL.md) | [Midjourney Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List) | 키워드+`--파라미터` + `--sref`/`--oref`/`--cw`/`--p` 3대 reference + 6대 비용·동작 함정 자동 검사 |

> 본 3 스킬은 **프롬프트 텍스트만 산출**합니다. 실제 이미지 생성은 사용자가 ChatGPT·Google AI Studio·Discord `/imagine`(또는 alpha.midjourney.com)에서 직접 실행합니다.

### 이미지·영상 직접 생성 — Higgsfield (2) 🆕 v2.13.0

| 스킬 | 백엔드 | 용도 |
|---|---|---|
| [`higgsfield-image`](skills/higgsfield-image/SKILL.md) | Higgsfield MCP | AI 이미지 자연어 한 줄로 직접 생성 (공식 11 이미지 모델, 비동기 잡 폴링) |
| [`higgsfield-video`](skills/higgsfield-video/SKILL.md) | Higgsfield MCP | AI 영상 자연어 한 줄로 직접 생성 (공식 11 영상 모델 + UGC·언박싱·제품리뷰 등 6 프리셋) |

### 음성 생성 (1)

| 스킬 | 백엔드 | 용도 |
|---|---|---|
| [`audio-gen`](skills/audio-gen/SKILL.md) | ElevenLabs MCP | TTS·보이스 클로닝·다국어 더빙·효과음 생성 |

## 스킬 선택 가이드

| 상황 | 우선 스킬 |
|---|---|
| ChatGPT/OpenAI API에서 이미지를 만들 텍스트 프롬프트가 필요 | `gpt-image-2-prompt` |
| Google AI Studio/Gemini에서 이미지를 만들 텍스트 프롬프트가 필요 | `gemini-3-image-prompt` |
| Midjourney Discord 또는 alpha.midjourney.com에서 쓸 프롬프트가 필요 | `midjourney-v8-prompt` |
| 한국어·영어·다국어 TTS 음성 파일이 필요 | `audio-gen` |
| 보이스 클로닝(자기 목소리·캐릭터 목소리)이 필요 | `audio-gen` |
| 영상·콘텐츠용 효과음(SFX)이 필요 | `audio-gen` |

## MCP 통합 (역할 분리)

`moai-media` 자체는 ElevenLabs MCP 1개만 번들합니다. 이미지·영상 렌더링은 별도 MCP에 위임합니다.

| 영역 | 담당 |
|---|---|
| 이미지 텍스트 프롬프트 작성 | **`moai-media`** 빌더 3종 |
| 음성·TTS·더빙·효과음 합성 | **`moai-media:audio-gen`** (ElevenLabs MCP) |
| 이미지 실제 렌더링 | 사용자가 외부 도구(ChatGPT·Google AI Studio·Discord)에서 실행 |
| 영상·캐릭터·립싱크 시네마틱 | **Higgsfield MCP** (별도 설치, Soul·DOP·말하는머리·캐릭터) |

## API 키 설정 (1개)

| 키 | 발급처 | 대상 스킬 |
|---|---|---|
| `ELEVENLABS_API_KEY` | [elevenlabs.io](https://elevenlabs.io/app/settings/api-keys) | `audio-gen` |

이미지 프롬프트 빌더 3종은 **API 키 불필요**합니다 (텍스트 프롬프트만 생성).

```bash
# .moai/credentials.env
ELEVENLABS_API_KEY=sk_...
```

## MCP 서버 자동 등록

`moai-media/.mcp.json`이 다음 MCP를 자동 등록합니다:

1. **elevenlabs** (local stdio MCP via `uvx elevenlabs-mcp`) — TTS, 보이스 클로닝, 다국어 더빙, 효과음

사전 준비: `uv` 설치 (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## 대표 체인

**이미지 제작 (외부 도구로 연결)**

```text
moai-content:copywriting → gpt-image-2-prompt
                          (사용자가 ChatGPT에서 실행)
```

**나노바나나(Gemini 3 Image)로 한국어 타이포 카드뉴스**

```text
moai-content:card-news → gemini-3-image-prompt
                        (사용자가 Google AI Studio에서 실행)
```

**Midjourney 브랜드 비주얼**

```text
moai-content:copywriting → midjourney-v8-prompt
                          (사용자가 Discord /imagine에서 실행)
```

**유튜브 내레이션 음성**

```text
moai-content:blog → audio-gen (한국어 TTS) → 영상 편집기로 import
```

**다국어 더빙**

```text
audio-gen (원본 음성 업로드 → 영어·일본어·중국어 더빙 동시 산출)
```

## 사용 예시

```
"GPT 프롬프트 만들어줘 — 비건 스킨케어 제품샷, 따뜻한 조명"   # → gpt-image-2-prompt
"Gemini 프롬프트 만들어줘 — 카드뉴스 5장, 한국어 타이포"      # → gemini-3-image-prompt
"Midjourney 프롬프트 만들어줘 — 사이버펑크 도시 일러스트"     # → midjourney-v8-prompt
"한국어 내레이션 만들어줘 — 30초 분량, 차분한 여성 목소리"    # → audio-gen
"이 영어 영상을 한국어로 더빙해줘"                            # → audio-gen
```

## 관련 플러그인

- `moai-content` — 카드뉴스·블로그·랜딩페이지 기획 (본 플러그인 빌더와 페어)
- `moai-commerce` — 상세페이지 카피·구조
- `moai-marketing` — `sns-content`·`campaign-planner`
- `moai-core` — `mcp-connector-setup`·`ai-slop-reviewer`(텍스트 산출물 검수)
- `moai-office` — PPT·Word·Excel·PDF 문서 생성

## 변경 이력

자세한 변경 내역은 [CHANGELOG.md](../CHANGELOG.md)를 참고하세요.

## 라이선스

MIT · [CHANGELOG](../CHANGELOG.md)
