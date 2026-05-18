# GPT-image-2 — Parameter Cheatsheet

ChatGPT 웹 UI에서는 일부 파라미터가 자동 결정되지만, OpenAI API (`images.generate`, `images.edit`)에서는 명시적으로 지정합니다.

## quality

| 값 | 비용/장 (1024) | 적용 |
|---|---|---|
| `low` | ~$0.01 | 프리뷰, 대량 A/B, 인터널 탐색 |
| `medium` (권장) | 중간 | 대부분의 production, SNS 콘텐츠 |
| `high` | ~$0.04-0.41 | 브랜드 캠페인, 광고 메인 컷, 고해상도 인쇄 |

권장: 1차 탐색은 `low`, 컨셉 확정 후 `medium`/`high`.

## size

| 값 | 픽셀 | 용도 |
|---|---|---|
| `512x512` | 작음 | 빠른 프리뷰, 썸네일 |
| `1024x1024` (권장) | 표준 | SNS, 카드뉴스, 일반 |
| `1024x1536` | 세로 | 9:16 인스타 릴스 (정확히는 `768x1344` 권장) |
| `1536x1024` | 가로 | 16:9 유튜브 썸네일 |
| `2048x2048` | 2K | 고해상도 production |
| 약 4K | experimental | OpenAI가 unstable로 분류 (2K 초과는 실험적) |

권장 매핑:

| 화면비 | size | 메모 |
|---|---|---|
| 1:1 | `1024x1024` 또는 `2048x2048` | 가장 안정 |
| 16:9 | `1536x864` | 유튜브 |
| 9:16 | `768x1344` | 릴스·쇼츠 |
| 4:5 | `1024x1280` | 인스타 피드 |

## background (편집 전용)

| 값 | 동작 |
|---|---|
| `auto` (권장) | 입력 이미지에 맞춰 결정 |
| `opaque` | 단색 배경 유지 |
| `transparent` | 알파 채널 PNG 출력 (로고·아이콘에 유용) |

## moderation

| 값 | 동작 |
|---|---|
| `auto` (권장) | OpenAI 기본 필터 |
| `low` | 덜 제한적 (성인용·민감 콘텐츠 일부 허용, 단 정책 위반은 여전히 차단) |

## n (배치 생성)

- 1-10 권장. 동일 프롬프트로 여러 변형이 필요할 때 `n=4` 호출이 `n=1`을 4회 호출하는 것보다 효율적.

## 참조 이미지 (편집 모드)

- 최대 16개 입력 이미지 (`file_id` 또는 URL).
- 각 이미지에 label을 붙이고 프롬프트에서 "Image 1: ... Image 2: ..." 형식으로 참조.

## API 호출 예 (Python)

```python
client.images.generate(
    model="gpt-image-2",
    prompt="<6-Block 단락>",
    size="1024x1024",
    quality="medium",
    moderation="auto",
    n=1,
)
```

편집:

```python
client.images.edit(
    model="gpt-image-2",
    image=[base_image, ref_jacket, ref_boots],
    prompt="<Change/Preserve/Constraints 단락>",
    background="auto",
    size="1024x1024",
)
```

## 비용 최적화 (Cookbook 권장)

1. 프리뷰는 `size=512` 또는 `1024` + `quality=low`로 생성.
2. 확정 후에만 `size=2048` + `quality=high`로 재생성.
3. 4K는 OpenAI가 experimental로 분류 — 일반 production은 2K까지.
4. 변형이 필요하면 `n=N` 한 번 호출.

## 출처

- [OpenAI Cookbook — image-gen-models-prompting-guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)
- [Framia — GPT Image 2 API Best Practices 2026](https://framia.pro/page/en-US/news/gpt-image-2-api-best-practices)
- [CometAPI — How to Use GPT Image 2](https://www.cometapi.com/how-to-use-and-prompt-gpt-image-2/)
