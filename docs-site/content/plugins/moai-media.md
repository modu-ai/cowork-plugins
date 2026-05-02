---
title: "moai-media — 이미지·영상·음성"
weight: 50
description: "Nano Banana, fal.ai Gateway, Gemini Audio/Video Gen을 포함한 7개 AI 미디어 생성 스킬을 묶은 통합 플러그인입니다."
geekdocBreadcrumb: true
tags: ["moai-media"]
---

# moai-media

> AI 미디어 생성 전용 플러그인입니다. 카드뉴스 썸네일부터 숏폼 영상·내레이션까지 한 번에 만들 수 있습니다.

## 무엇을 하는 플러그인인가

`moai-media` (v1.6.0)는 이미지·영상·음성을 모두 한 플러그인 안에서 생성할 수 있도록 묶은 AI 미디어 스튜디오입니다. Google Gemini의 Nano Banana·Audio Gen·Video Gen 계열, 그리고 fal.ai Gateway를 통한 1000+ 모델 라우팅을 지원하며, **총 7개 스킬**이 통합되어 있습니다.

카드뉴스 슬라이드 이미지 일괄 생성, 한국어 타이포 포스터, 15초 숏폼 영상, 팟캐스트 내레이션까지 콘텐츠 제작에 필요한 멀티미디어를 한 번의 체인으로 처리할 수 있습니다.

본 플러그인은 MCP 서버를 번들합니다 (`fal-ai` hosted). API 키 등록 절차는 플러그인 루트의 `CONNECTORS.md`를 참고하세요.

## 설치

{{< tabs "install-media" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. `moai-core` 설치 후 `moai-media` 옆의 **+** 버튼을 눌러 설치합니다.
2. 아래 API 키를 `.moai/credentials.env`에 등록합니다.
{{< /tab >}}
{{< tab "수동" >}}
[GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-media)를 클론한 뒤 `~/.claude/plugins/`에 배치합니다.
{{< /tab >}}
{{< /tabs >}}

## 핵심 스킬 (7개)

| 스킬 | 모델·서비스 | 특화 |
|---|---|---|
| `nano-banana` | Google Gemini (nano-banana pro/flash) | 카드뉴스·인스타 이미지, 한국어 텍스트 렌더링 SOTA |
| `audio-gen` | Google Gemini (Audio-Gen) | 음성 생성, 배경음악, 효과음 제작 |
| `character-mgmt` | Gemini Vision + fal.ai | 캐릭터 디자인, 일관된 캐릭터 이미지 시리즈 |
| `image-gen` | Google Gemini (Image Gen) | 다양한 스타일 이미지 생성, 한국어 프롬프트 최적화 |
| `speech-video` | Gemini Audio + Video Gen | 음성 합성 + 영상 생성, 팟캐스트/강의용 |
| `video-gen` | Google Gemini (Video Gen) | 단순 영상 생성, 애니메이션, 제품 데모 |
| `fal-gateway` | fal.ai 통합 | Flux 1.1 Pro, Recraft V3, MiniMax 등 1000+ 모델 |

## 필수 API 키

{{< hint type="warning" >}}
이미지·영상·음성을 생성하려면 **API 키 설정이 필수**입니다. 프로젝트 루트 `.moai/credentials.env`에 저장하세요.
{{< /hint >}}

```bash
# .moai/credentials.env
GEMINI_API_KEY=...           # nano-banana, audio-gen, video-gen, speech-video, image-gen
FAL_KEY=...                  # fal-gateway
```

| 변수 | 용도 | 발급처 |
|---|---|---|
| `GEMINI_API_KEY` | Nano Banana·Audio Gen·Image Gen·Video Gen·Speech Video | [Google AI Studio](https://aistudio.google.com/) |
| `FAL_KEY` | fal Gateway (Flux 1.1, Recraft V3 등 1000+ 모델) | [fal.ai](https://fal.ai) |

## 대표 체인

**카드뉴스 전체 제작**

```text
moai-content:card-news → nano-banana → ai-slop-reviewer
```

**쇼핑몰 상세페이지 이미지**

```text
moai-content:product-detail → image-gen → ai-slop-reviewer
```

**캐릭터 기반 영상 콘텐츠**

```text
moai-content:copywriting → character-mgmt → speech-video
```

**팟캐스트 전체 제작**

```text
moai-content:media-production → audio-gen → speech-video → ai-slop-reviewer
```

## 비용 관리

- `nano-banana`는 비교적 저렴하며 반복 생성에 적합합니다.
- `video-gen`은 영상당 비용이 상대적으로 큽니다 — 스토리보드를 먼저 확정한 뒤 최종 생성을 권장합니다.
- `fal-gateway`는 단일 `FAL_KEY`로 다양한 모델을 사용할 수 있어 테스트 단계에서 유용합니다.

## 빠른 사용 예

```text
인스타 6슬라이드 카드뉴스에 쓸 이미지 6장을 3:4 비율로 만들어줘.
주제는 '프리랜서 3.3% 원천징수 쉽게 정리'.
```

```text
이 이미지로 15초짜리 인스타 릴스 영상 만들어줘.
```

## 다음 단계

- [`moai-content`](../moai-content/) — 슬라이드 카피·기획과 결합
- [Cowork 커넥터와 MCP](../../cowork/connectors-mcp/)

---

### Sources

- [modu-ai/cowork-plugins README](https://github.com/modu-ai/cowork-plugins)
- [moai-media 디렉터리](https://github.com/modu-ai/cowork-plugins/tree/main/moai-media)
