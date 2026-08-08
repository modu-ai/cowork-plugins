# 미디어 크리에이터 (moai-media)

미디어 생성 전담 AI 코워커입니다. 이미지·영상·오디오 생성(media-* 13종) 스킬과 Higgsfield 이미지·영상·3D·설명영상·제품촬영·캐릭터 일관성, ElevenLabs TTS/보이스클로닝 MCP 연동, GPT-image-2·Gemini 3·Midjourney v8 프롬프트 빌더를 하나의 플러그인으로 제공합니다. 슬래시 명령을 외울 필요 없이 자연어로 요청하면 매칭되는 스킬이 자동 호출됩니다.

> **분리 안내**: 본 플러그인의 미디어 생성 스킬들은 `moai-marketer`에서 분리되었습니다(카피·캠페인·콘텐츠 스킬은 moai-marketer에 잔류). 신규 호출은 `moai-media:<스킬명>` 네임스페이스를 사용하세요.

**이런 분께 추천**: 콘텐츠 크리에이터 · 마케터 · 디자이너 · 1인 브랜드

## 설치

```
claude plugin marketplace add modu-ai/moai-cowork
claude plugin install moai-media@moai-cowork
```

또는 Claude Code 세션 안에서:

```
/plugin marketplace add modu-ai/moai-cowork
/plugin install moai-media
```

## 스킬 13종

호출 형식: `/moai-media:<스킬명>` — 예: `/moai-media:media-higgsfield-image`. 자연어 요청("표지 이미지 만들어줘", "TTS 성우 더빙 생성")으로도 자동 매칭됩니다.

### Higgsfield 계열 (7종)

| 스킬 | 역할 |
|------|------|
| `media-higgsfield-core` | (공유 코어) 호출 계약·라이브 카탈로그 조회·비용 프리플라이트 SSOT. 단독 호출용 아님 |
| `media-higgsfield-image` | Higgsfield MCP 기반 AI 이미지 생성 (자연어 한 줄) |
| `media-higgsfield-video` | Higgsfield MCP 기반 AI 영상 생성 (자연어 한 줄) |
| `media-higgsfield-identity` | 캐릭터·인물 일관성 참조 — Soul 학습 / Element 생성 판정 |
| `media-higgsfield-assets` | 3D 메시(GLB)·리깅·오디오·바이럴 예측·업스케일/리프레임/누끼 |
| `media-higgsfield-explainer` | 10초 블록 조립형 내레이션 설명 영상 (1~10분) |
| `media-higgsfield-product` | 브랜드·제품 비주얼 10모드 판정과 생성 |

### 그 밖의 생성·프롬프트 (6종)

| 스킬 | 역할 |
|------|------|
| `media-audio-gen` | ElevenLabs MCP 기반 TTS(32개국어)·보이스 클로닝·더빙·효과음 |
| `media-gpt-image-2-prompt` | OpenAI GPT-image-2 전용 6-Block 이미지 프롬프트 빌더 |
| `media-gemini-3-image-prompt` | Gemini 3 Pro Image(Nano Banana Pro) 전용 5-component 프롬프트 빌더 |
| `media-midjourney-v8-prompt` | Midjourney v8.1 전용 키워드+파라미터 프롬프트 빌더 |
| `media-codex-image` | codex CLI 내장 image_gen으로 gpt-image-2 생성(API 키 불필요) |
| `media-notebooklm-slide-prompt` | 강연 마크다운 → NotebookLM 슬라이드 데크 + 슬라이드별 이미지 프롬프트 |
| `media-asset-production` | (구명칭 호환 스텁 — 종수 미포함) 두 개의 스킬로 분리됨 — 신규 호출은 분리 스킬 사용 |

## MCP 연동 2종

플러그인 루트 `.mcp.json`에 2개 MCP 서버가 선언되어 있습니다. 자격증명은 **환경변수 또는 OAuth 로그인으로만** 설정하세요(파일에 키를 적지 않습니다).

| 서버 | 역할 | 인증 방법 |
|------|------|-----------|
| `higgsfield` | AI 영상·이미지 생성 (media-higgsfield-* 사용) | Higgsfield 계정 토큰 (mcp.higgsfield.ai) |
| `ElevenLabs` | TTS·보이스 클로닝·더빙·효과음 (media-audio-gen 전용) | `ELEVENLABS_API_KEY` 환경변수 (elevenlabs.io에서 발급) + `uv` 사전 설치 |

- 생성 작업은 크레딧이 소모되므로 각 스킬이 **사전 크레딧 고지 + 사용자 확인** 후에만 실행합니다
- MCP 미연결 시 프롬프트 온리 모드(생성 프롬프트만 산출)로 자동 전환됩니다

## 에이전트 2종

| 에이전트 | 등급 | 역할 |
|----------|------|------|
| `media-producer` | worker | 이미지·영상·오디오 생성 산출물을 만드는 실무 에이전트. 목표 이해 → 계획 → media-* 스킬 선택 → 실행 → 검증의 에이전트 루프로 동작. 저작권/초상권 준수·크레딧 사전 고지·카피/전략은 marketer·토큰은 designer로 인계를 HARD 가드레일로 준수 |
| `media-brand-auditor` | read-only audit | 미디어 산출물·프롬프트를 회의적으로 검증하는 감사 에이전트 — 브랜드/스타일 정합, 저작권·라이선스 위험, 프롬프트 인젝션/불쾌 콘텐츠 위험, 프롬프트 엔지니어링 품질. 증거 기반 PASS/FAIL 판정만 반환하며 파일을 수정하지 않음 |

## 라이선스

Apache-2.0 · © 2026 modu-ai (email@mo.ai.kr) — 산출물은 이용자 소유([LICENSE-OUTPUT.md](../../LICENSE-OUTPUT.md))
