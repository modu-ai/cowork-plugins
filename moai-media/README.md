# moai-media

> AI 미디어 스튜디오 — 이미지·영상·음성 통합 생성 + **Day 3 한국 이커머스 광고 풀세트** (v2.3.0 신규)

[![버전](https://img.shields.io/badge/version-2.3.0-blue)](../CHANGELOG.md)
[![라이선스](https://img.shields.io/badge/license-MIT-green)](../LICENSE)
[![스킬](https://img.shields.io/badge/skills-13-success)](#스킬-카탈로그-13종)

## 개요

`moai-media`는 AI 크리에이터·마케터·이커머스 셀러를 위한 **미디어 생성 단일 창구**입니다.
카드뉴스·인스타 피드·숏폼 영상·팟캐스트·브랜드 캠페인부터 **이커머스 광고 풀세트**(무드보드·한글 타이포 5장·메인 영상·보조 컷 2개·채널별 변환·AI 표기·캔바 매직 레이어)까지 하나의 플러그인에서 해결합니다.

**v2.3.0부터** "모두의 커머스 3일 마스터 캠프" Day 3(광고 풀세트) 전용 신규 6스킬을 추가했습니다. 카테고리 매트릭스 기반 자동 라우팅(의류=Kling 3 / 뷰티=Veo 3 / 건강식품=Kling 3 / 생활용품=Seedance)으로 4명×5조 시차 호출(5분 간격)로 Higgsfield 동시 호출 비용 폭증을 방지합니다.

## 스킬 카탈로그 (13종)

### 범용 미디어 생성 (7) — v1.x 이전부터

| 스킬 | 한글명 | 백엔드 | 용도 |
|---|---|---|---|
| [`nano-banana`](skills/nano-banana/SKILL.md) | 나노바나나 | Gemini 3 Image Preview | **한국어 타이포 SOTA** 이미지 (카드뉴스·포스터·썸네일) |
| [`image-gen`](skills/image-gen/SKILL.md) | 이미지젠 | Gemini Image / fal.ai | 일반 이미지 생성 (시네마틱·제품 사진·배경) |
| [`video-gen`](skills/video-gen/SKILL.md) | 비디오젠 | fal.ai (Kling·Hailuo) + Higgsfield | 영상 생성 (숏폼·광고·제품 데모, 텍스트→영상·이미지→영상) |
| [`audio-gen`](skills/audio-gen/SKILL.md) | 오디오젠 | ElevenLabs MCP + Gemini | TTS·음성 합성·다국어 더빙·BGM·효과음 |
| [`speech-video`](skills/speech-video/SKILL.md) | 스피치비디오 | ElevenLabs + Higgsfield | 립싱크 영상 (말하는 머리·강의·팟캐스트 영상) |
| [`character-mgmt`](skills/character-mgmt/SKILL.md) | 캐릭터관리 | Higgsfield | 일관된 캐릭터 시리즈 관리 (브랜드 캐릭터·웹툰) |
| [`fal-gateway`](skills/fal-gateway/SKILL.md) | 팔게이트웨이 | fal.ai MCP | Flux·Recraft·Ideogram·Hailuo·Luma·Pika·MiniMax Music 등 1000+ 모델 통합 |

### Day 3 광고 풀세트 (6 신규) — V6 Day 3 산출물 ⑫~⑰ + 표기 (v2.3.0)

| 스킬 | V6 매핑 | 백엔드 | 산출물 |
|---|---|---|---|
| [`media-moodboard`](skills/media-moodboard/SKILL.md) | ⑫ Day3 S1 | 분석·검색 | 색 팔레트 3종 + 톤 키워드 5개 + 레퍼런스 이미지 5장 + 작업 카드 |
| [`media-gpt-image2-builder`](skills/media-gpt-image2-builder/SKILL.md) | ⑬ Day3 S2 | **GPT Image 2** | 한글 타이포 5장 세트 (Hero 1 + 인포 1 + 라이프 2 + CTA 1) — 8단계 자동 리라이팅 |
| [`media-model-router`](skills/media-model-router/SKILL.md) | ⑮⑯ Day3 S4 | Kling 3 / Veo 3 / Seedance | 카테고리 매트릭스 자동 라우팅 + 의심차단형 후크 + 메인 영상 5~10초 + 보조 영상 2컷 |
| [`media-channel-ad-packager`](skills/media-channel-ad-packager/SKILL.md) | ⑰ Day3 S6 | 후처리 | 메타 1:1·9:16 / 네이버 GFA / 카카오모먼트 1:1·16:9 채널 규격 자동 변환 + .zip 패키지 |
| [`media-ai-disclosure`](skills/media-ai-disclosure/SKILL.md) | Day3 S2~S7 | 후처리 자동 체인 | "AI 생성" 메타데이터·워터마크·캡션 3계층 부착 — 광고심의·소비자보호법 대응 |
| [`media-canva-magic-layer`](skills/media-canva-magic-layer/SKILL.md) | Day3 S7 보너스 | 가이드 | 합성 PNG → 카피만 분리 → 시즌 재사용 5단계 체크리스트 (GPT Image 2 재호출 ↓90%) |

> Day 3 신규 스킬은 PDF §6 + 부록 A·B·D 매핑입니다. `media-gpt-image2-builder` 8단계 프롬프트 구조와 `media-model-router` 카테고리 매트릭스는 강사·개발팀 내부용 `references/` 자료로 분리되어 있어 수강생 출력에 원문이 노출되지 않습니다 (REQ-MEDIA-013).

## 스킬 선택 가이드

### 이미지

| 상황 | 우선 스킬 |
|---|---|
| 한국어 대형 타이포그래피 (카드뉴스·포스터·썸네일) | **`nano-banana`** ⭐ |
| 이커머스 광고 한글 타이포 5장 세트 (Day 3) | **`media-gpt-image2-builder`** 🆕 |
| 디자인 방향성 수립 (색·톤·레퍼런스) | **`media-moodboard`** 🆕 |
| 시네마틱·제품 사진·배경 (텍스트 없음) | `image-gen` |
| 로고·벡터·브랜드 일관 컬러 | `fal-gateway` (Recraft V3) |
| 일관된 캐릭터 시리즈 | `character-mgmt` |

### 영상

| 상황 | 스킬 |
|---|---|
| 이커머스 광고 메인+보조 영상 (카테고리 자동 라우팅) | **`media-model-router`** 🆕 |
| 인스타 릴스·유튜브 쇼츠·틱톡 | `video-gen` (fal.ai Kling) |
| 브랜드 광고·제품 영상 | `video-gen` (Kling Pro 모드) |
| 말하는 머리·립싱크 강의 | `speech-video` (음성+영상 결합) |
| 시네마틱 영상 (Higgsfield DOP) | `video-gen` |

### 채널 변환 / 표기 / 재사용

| 상황 | 스킬 |
|---|---|
| 메타·네이버 GFA·카카오모먼트 광고 소재 패키징 | **`media-channel-ad-packager`** 🆕 |
| "AI 생성" 표기 자동 부착 (광고심의·소비자보호법) | **`media-ai-disclosure`** 🆕 (모든 미디어 산출물 자동 체인) |
| Canva 매직 레이어로 카피만 교체해 시즌 재사용 | **`media-canva-magic-layer`** 🆕 |

### 음성·음악

| 상황 | 스킬 |
|---|---|
| TTS·내레이션·다국어 더빙 | **`audio-gen`** (ElevenLabs MCP) |
| BGM·효과음·오리지널 음악 | `fal-gateway` (MiniMax Music, Stable Audio) |
| 립싱크 영상까지 한 번에 | `speech-video` |

## Day 3 광고 풀세트 표준 워크플로우

```
[10:10–10:25 S1]  media-moodboard               → 색 팔레트·톤·레퍼런스 5장 + 작업 카드
       ↓
[11:08–11:18 S2]  media-gpt-image2-builder      → Hero+인포+라이프 2+CTA = 5장 한글 타이포
       ↓                                         ↘ media-ai-disclosure 자동 체인
[14:08–14:20 S4]  media-model-router            → 카테고리 매트릭스 자동 라우팅
                  (Kling 3 / Veo 3 / Seedance)    → 메인 영상 5~10초 + 보조 영상 2컷
       ↓                                         ↘ media-ai-disclosure 자동 체인
[16:20–16:45 S6]  media-channel-ad-packager     → 메타·네이버 GFA·카카오 채널 규격 .zip
       ↓
[17:40–17:45 S7]  media-canva-magic-layer       → 카피만 교체해 시즌 재사용 가이드
```

## API 키 설정 (총 4개)

| 키 | 발급처 | 공유 대상 스킬 |
|---|---|---|
| `GEMINI_API_KEY` | [ai.google.dev](https://ai.google.dev/) | `nano-banana`, `image-gen`, `audio-gen`, `video-gen` |
| `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com/api-keys) | `media-gpt-image2-builder` 🆕 (GPT Image 2 호출) |
| `FAL_KEY` | [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys) | `fal-gateway`, `image-gen`, `video-gen` |
| `ELEVENLABS_API_KEY` | [elevenlabs.io](https://elevenlabs.io/app/settings/api-keys) | `audio-gen`, `speech-video` (ElevenLabs MCP) |
| `HIGGSFIELD_API_KEY` + `HIGGSFIELD_SECRET` | [higgsfield.ai](https://higgsfield.ai/) | `character-mgmt`, `video-gen`, `speech-video`, `media-model-router` 🆕 |

`/project init` 또는 `/project apikey`로 통합 등록. Day 3 캠프 운영 시 `moai-core:mcp-connector-setup`(v2.3.0+)에서 4커넥터(Drive·Notion·Higgsfield·OpenAI) 인증·트러블슈팅 일괄 가이드 제공.

## MCP 서버 자동 등록

`moai-media/.mcp.json`이 다음 MCP를 자동 등록합니다:

1. **fal-ai** (hosted HTTP MCP): `https://mcp.fal.ai/mcp` — Flux·Ideogram·Recraft·Kling·Hailuo·Luma·Pika·MiniMax Music
2. **elevenlabs** (local stdio MCP via `uvx elevenlabs-mcp`) — TTS·음성복제·다국어 더빙
3. **higgsfield** (local stdio MCP) — 시네마틱 이미지(Soul)·영상(DOP)·립싱크·캐릭터 관리 + Day 3 Kling 3·Veo 3·Seedance 2.0

플러그인 설치 시 자동 활성화. `nano-banana`·`image-gen`·`audio-gen`·`media-gpt-image2-builder`는 각 모델 API 직접 호출(MCP 불필요).

## 비용 폭증 방지 (Day 3 운영)

`media-model-router`는 Higgsfield 동시 호출 비용 폭증을 방지하기 위해 다음을 강제합니다:

- 4명×5조 = **20명 시차 호출** (5분 간격 = 총 100분 윈도우)
- 카테고리 매트릭스 라우팅으로 1조당 모델 분산
- Higgsfield 워크스페이스 사전 비용 충전 **1.5배** 권장 (PDF §6.9)

## 월 예상 비용 (한국 크리에이터 기준)

| 용도 | 월 예산 | 산출물 |
|---|---|---|
| 입문 (포트폴리오 1~2편/주) | **$10~15** | Nano Banana 2 위주, 영상 시안 소량 |
| 중급 (브랜드 3개, 주 3편) | **$45~60** | 이미지 500장 + 영상 20편 (Kling) + TTS 30분 |
| **Day 3 캠프 1회 (4명×5조 = 20명)** | **$150~250** | GPT Image 2 100장 + Kling/Veo/Seedance 40편 + 음성 |
| 고급 (에이전시 수준) | **$200+** | Kling Pro 영상 일 3~5편 + 4K 이미지 마스터 + 다채널 배포 |

## 사용 예시

```
"무드보드 만들어줘 — 비건 스킨케어, 따뜻한 톤"           # → media-moodboard
"광고 이미지 5장 만들어줘 — 무선이어폰, 직장인 타겟"     # → media-gpt-image2-builder
"광고 영상 만들어줘 — 의류 카테고리, 의심차단형 후크"    # → media-model-router (Kling 3 자동 선택)
"채널별 광고 소재 만들어줘 — 메타+네이버+카카오"         # → media-channel-ad-packager
"AI 생성 표기 달아줘 — 광고심의 대응"                    # → media-ai-disclosure
"카피만 교체해서 시즌 광고 재사용 가이드"                # → media-canva-magic-layer
```

## 관련 플러그인

- `moai-content` — 카드뉴스·블로그·랜딩페이지 기획 (`moai-media` 스킬을 호출하여 에셋 생성)
- `moai-commerce` — 13섹션 상세페이지 이미지 합성 + Day 3 V6 6도구 wrapper
- `moai-marketing` — `sns-content`(한국 3 + 글로벌 4채널), `campaign-planner`(중장기 캠페인, 상세페이지·이미지 책임은 moai-commerce/moai-media로 이관됨)
- `moai-core` — `mcp-connector-setup`(Day 1 셋업), `ai-slop-reviewer`(텍스트 산출물 검수)
- `moai-office` — PPT·Word·Excel·PDF 문서 생성

## 변경 이력

- **v2.3.0** (2026-05-12): Day 3 광고 풀세트 6스킬 신규 — `media-moodboard`·`media-gpt-image2-builder`·`media-model-router`·`media-channel-ad-packager`·`media-ai-disclosure`·`media-canva-magic-layer`. 총 7 → **13 스킬**. 카테고리 매트릭스 자동 라우팅(의류=Kling 3 / 뷰티=Veo 3 / 건강식품=Kling 3 / 생활용품=Seedance), 4명×5조 시차 호출(5분 간격), "AI 생성" 3계층 자동 표기, GPT Image 2 재호출 90% ↓ 캔바 매직 레이어 가이드 추가
- **v2.0.0** (2026-05-04): cowork v2.0.0 — Breaking change 없음(스킬 7종 그대로)
- **v1.8.0** (2026-05-02): 7스킬 카탈로그로 갱신
- **v1.6.0**: ElevenLabs·Kling·Ideogram 독립 SKILL 제거 → MCP·모델 ID로 통합
- **v1.5.0**: `image-gen`·`speech-video`·`character-mgmt` 추가
- **v1.1.0**: 독립 플러그인으로 분리, Google Nano Banana 재정의 반영

자세한 변경 내역: [CHANGELOG.md](../CHANGELOG.md)

## 라이선스

MIT · [CHANGELOG](../CHANGELOG.md) · [CLAUDE.local.md](../CLAUDE.local.md)
