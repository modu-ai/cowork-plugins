# moai-media

> AI 미디어 스튜디오 — 이미지·영상·음성 통합 생성 플러그인

[![버전](https://img.shields.io/badge/version-1.8.0-blue)](../CHANGELOG.md)
[![라이선스](https://img.shields.io/badge/license-MIT-green)](../LICENSE)

## 개요

`moai-media`는 AI 크리에이터·마케터를 위한 **미디어 생성 단일 창구**입니다.
카드뉴스·인스타 피드·숏폼 영상·팟캐스트·브랜드 캠페인에 필요한 이미지·영상·음성을
하나의 플러그인에서 해결합니다.

## 스킬 카탈로그 (7종)

| 스킬 | 한글명 | 백엔드 | 용도 |
|---|---|---|---|
| [`nano-banana`](skills/nano-banana/SKILL.md) | 나노바나나 | Gemini 3 Image Preview | **한국어 타이포 SOTA** 이미지 (카드뉴스·포스터·썸네일) |
| [`image-gen`](skills/image-gen/SKILL.md) | 이미지젠 | Gemini Image / fal.ai | 일반 이미지 생성 (시네마틱·제품 사진·배경) |
| [`video-gen`](skills/video-gen/SKILL.md) | 비디오젠 | fal.ai (Kling·Hailuo) + Higgsfield | 영상 생성 (숏폼·광고·제품 데모, 텍스트→영상·이미지→영상) |
| [`audio-gen`](skills/audio-gen/SKILL.md) | 오디오젠 | ElevenLabs MCP + Gemini | TTS·음성 합성·다국어 더빙·BGM·효과음 |
| [`speech-video`](skills/speech-video/SKILL.md) | 스피치비디오 | ElevenLabs + Higgsfield | 립싱크 영상 (말하는 머리·강의·팟캐스트 영상) |
| [`character-mgmt`](skills/character-mgmt/SKILL.md) | 캐릭터관리 | Higgsfield | 일관된 캐릭터 시리즈 관리 (브랜드 캐릭터·웹툰) |
| [`fal-gateway`](skills/fal-gateway/SKILL.md) | 팔게이트웨이 | fal.ai MCP | Flux·Recraft·Ideogram·Hailuo·Luma·Pika·MiniMax Music 등 1000+ 모델 통합 |

## 스킬 선택 가이드

### 이미지

| 상황 | 우선 스킬 |
|---|---|
| 한국어 대형 타이포그래피가 핵심 (카드뉴스·포스터·썸네일) | **`nano-banana`** ⭐ |
| 시네마틱·제품 사진·배경 (텍스트 없음) | `image-gen` |
| 로고·벡터·브랜드 일관 컬러 | `fal-gateway` (Recraft V3) |
| 오픈소스 Flux 선호 | `fal-gateway` (Flux 1.1 Pro) |
| 영문 타이포 특화 (대안) | `fal-gateway` (Ideogram v3) |
| 일관된 캐릭터 시리즈 | `character-mgmt` |

### 영상

| 상황 | 스킬 |
|---|---|
| 인스타 릴스·유튜브 쇼츠·틱톡 | **`video-gen`** (fal.ai Kling 백엔드) |
| 브랜드 광고·제품 영상 | **`video-gen`** (Kling Pro 모드) |
| 말하는 머리·립싱크 강의 | **`speech-video`** (음성+영상 결합) |
| 초저가 시안 대량 생성 | `fal-gateway` (Hailuo 2.3) |
| 시네마틱 영상 (Higgsfield) | `video-gen` (DOP 모델) |

### 음성·음악

| 상황 | 스킬 |
|---|---|
| TTS·내레이션·다국어 더빙 | **`audio-gen`** (ElevenLabs MCP) |
| BGM·효과음·오리지널 음악 | `fal-gateway` (MiniMax Music, Stable Audio) |
| 립싱크 영상까지 한 번에 | `speech-video` |

## API 키 설정 (총 4개)

| 키 | 발급처 | 공유 대상 스킬 |
|---|---|---|
| `GEMINI_API_KEY` | [ai.google.dev](https://ai.google.dev/) | `nano-banana`, `image-gen`, `audio-gen`, `video-gen` |
| `FAL_KEY` | [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys) | `fal-gateway`, `image-gen`, `video-gen` |
| `ELEVENLABS_API_KEY` | [elevenlabs.io](https://elevenlabs.io/app/settings/api-keys) | `audio-gen`, `speech-video` (ElevenLabs MCP 사용) |
| `HIGGSFIELD_API_KEY` + `HIGGSFIELD_SECRET` | [higgsfield.ai](https://higgsfield.ai/) | `character-mgmt`, `video-gen`, `speech-video` (Higgsfield MCP 사용) |

`/project init` 또는 `/project apikey`로 통합 등록.

## MCP 서버 자동 등록

`moai-media/.mcp.json`이 다음 3개 MCP를 자동 등록합니다:

1. **fal-ai** (hosted HTTP MCP): `https://mcp.fal.ai/mcp` — Flux·Ideogram·Recraft·Kling·Hailuo·Luma·Pika·MiniMax Music
2. **elevenlabs** (local stdio MCP via `uvx elevenlabs-mcp`) — TTS·음성복제·다국어 더빙
3. **higgsfield** (local stdio MCP) — 시네마틱 이미지(Soul)·영상(DOP)·립싱크·캐릭터 관리

플러그인 설치 시 자동 활성화. `nano-banana`·`image-gen`·`audio-gen`은 Gemini API 직접 호출(MCP 불필요).

> **참고**: ElevenLabs·Kling·Ideogram은 v1.6.0부터 **독립 SKILL이 아니라 MCP·모델 ID로 통합**되었습니다. 사용자 측 호출 방식이 달라졌으니, 기존 `moai-media:elevenlabs` 호출은 `audio-gen`으로, `moai-media:kling`은 `video-gen` 또는 `fal-gateway`로, `moai-media:ideogram`은 `nano-banana`(한국어 타이포 SOTA) 또는 `fal-gateway`(Ideogram v3 모델)로 대체하세요.

## 월 예상 비용 (한국 크리에이터 기준)

| 용도 | 월 예산 | 산출물 |
|---|---|---|
| 입문 (포트폴리오 1~2편/주) | **$10~15** | Nano Banana 2 위주, 영상 시안 소량 |
| 중급 (브랜드 3개, 주 3편) | **$45~60** | 이미지 500장 + 영상 20편 (Kling) + TTS 30분 |
| 고급 (에이전시 수준) | **$200+** | Kling Pro 영상 일 3~5편 + 4K 이미지 마스터 + 다채널 배포 |

## 관련 플러그인

- `moai-content` — 카드뉴스·블로그·랜딩페이지 기획 (`moai-media` 스킬을 호출하여 에셋 생성)
- `moai-commerce` — 13섹션 상세페이지 이미지 합성 (`detail-page-image` → `nano-banana`)
- `moai-marketing` — SNS 캠페인·광고 소재 기획
- `moai-office` — PPT·Word·Excel·PDF 문서 생성

## 변경 이력

- **v1.8.0** (2026-05-02): README 7스킬 카탈로그로 갱신, kling/ideogram/elevenlabs 스킬 표기 정리
- **v1.6.0**: ElevenLabs·Kling·Ideogram 독립 SKILL 제거 → MCP·모델 ID로 통합 (`audio-gen`/`video-gen`/`nano-banana` + `fal-gateway`)
- **v1.5.0**: `image-gen`·`speech-video`·`character-mgmt` 추가
- **v1.1.0**: 독립 플러그인으로 분리, Google Nano Banana 재정의 반영 (Imagen 4 → Gemini 3 Image Preview)

자세한 변경 내역: [CHANGELOG.md](../CHANGELOG.md)

## 라이선스

MIT · [CHANGELOG](../CHANGELOG.md) · [CLAUDE.local.md](../CLAUDE.local.md)
