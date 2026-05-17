# Midjourney v8.1 — Parameter Cheatsheet

공식 [Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List) 기반.

## --ar (Aspect Ratio)

| 값 | 용도 |
|---|---|
| `--ar 1:1` (default) | SNS 정사각 |
| `--ar 16:9` | 와이드, 유튜브 |
| `--ar 9:16` | 릴스·쇼츠 |
| `--ar 4:5` | 인스타 피드 |
| `--ar 3:2` | 사진 표준 |
| `--ar 2:3` | 책 표지 |

극단 비율(`--ar 1:4` 등)은 V6 이후 일부만 지원. 확인 필요.

## --style

| 값 | 동작 |
|---|---|
| (생략, default) | 모델 자체 스타일 개입 |
| `--style raw` | 자연·photographic, 모델 개입 최소 |
| `--style cute` (V6 잔존) | 가끔 동작, V8에서 deprecation 진행 중 |

권장: 사진 작업은 `--style raw`, 일러스트는 생략.

## --hd (V8 신규)

- Native 2K 해상도 출력.
- **비용 4x**.
- `--q 4`와 조합 시 곱연산 (16x).

## --q (Quality)

| 값 | 동작 | 비용 |
|---|---|---|
| `--q 1` | 빠름, 거친 디테일 | 1x |
| `--q 2` (default) | 표준 | 1x |
| `--q 4` (V8 신규) | extra coherence | 4x |

## --s / --stylize

| 값 | 동작 |
|---|---|
| `--s 0` | 프롬프트만 충실 |
| `--s 100` (default) | 균형 |
| `--s 250` | 약간 스타일 강조 |
| `--s 500` | 강한 스타일 |
| `--s 1000` | 최대 모델 개입 (V8 권장 상한) |

## --sref (Style Reference)

```
--sref CODE                 # 라이브러리 코드
--sref https://...          # 이미지 URL
--sref CODE1 CODE2 CODE3    # 다중 (공백 구분)
--sref random               # 무작위 → 결과 후 실제 코드 확인 필수
```

| 동반 옵션 | 동작 |
|---|---|
| `--sw 0~1000` | sref 영향력 (default 100) |
| `--sv 1~7` | sref version (default 7) |

`--sv` 표:

| 버전 | 특징 |
|---|---|
| `--sv 1`~`--sv 5` | 구버전 |
| `--sv 6` | V7 중반 default |
| `--sv 7` (V8 default) | 4x 빠름, 4x 저렴, `--hd`·`--p`·`--stylize`·`--exp` 지원 |

**비용 4x**.

## --oref (Omni Reference, V7+ replaces --cref)

```
--oref https://image-url.jpg
```

| 동반 | 동작 |
|---|---|
| `--cw 0~100` | character weight (default 100) |

`--cw` 함정:

| 값 | 동작 |
|---|---|
| `--cw 0` | 얼굴만 가져옴, 옷·조명 무시 |
| `--cw 20~40` (권장) | 얼굴 + 약간의 형태 |
| `--cw 50~70` | 얼굴 + 의상 + 자세 |
| `--cw 100` (default ⚠️) | 모든 디테일 (조명·스타일 포함, 새 프롬프트와 충돌 위험) |

**비호환**:
- Fast Mode
- Draft Mode
- Conversational Mode
- `--q 4`

**비용 2x**.

## --p / --profile (Personalization)

```
--p                        # default moodboard
--p PROFILE_ID             # 특정 프로파일
--profile PROFILE_ID       # 동일
```

설정 단계:
- 40 ratings → 시작 가능
- 200 ratings → stable
- 2000 ratings → 최대 개선

V8 신규:
- 여러 named profile 동시 활성화
- 5x 빠른 setup

## --no (Negative)

```
--no people, --no text, --no watermark
```

여러 키워드 콤마 구분.

## --c / --chaos

```
--c 0~100   # 결과 다양성 (default 0)
```

시안용. 50 이상은 매우 다양한 결과.

## --weird / --w

```
--w 0~3000   # 비정상·실험적 결과
```

기괴함을 의도할 때.

## Deprecated · 비호환 옵션 (V8)

| 옵션 | 상태 | 대체 |
|---|---|---|
| `--cref` | deprecated | `--oref` |
| `--cw` (V6 형식) | 동작 | `--oref --cw` |
| `--niji 6` | V8에서도 일부 동작 | `--p` 또는 `--sref`로 대체 |
| `--v 7` | 자동 v8 라우팅 | 생략 |

## 비용 빠른 계산

| 조합 | 멀티플라이어 |
|---|---|
| 기본 (`--ar`만) | 1x |
| `--style raw` | 1x |
| `--hd` | 4x |
| `--q 4` | 4x |
| `--sref` (URL 또는 CODE) | 4x |
| `--oref` | 2x |
| `--p` | 1x |
| `--hd --q 4` | 16x |
| `--hd --q 4 --sref` | 64x ⚠️ |
| `--hd --q 4 --sref --oref` | 128x ⚠️⚠️ |

비용 민감 시 Relax Mode 가용 여부 확인 (V8 Alpha 초기 미지원, V8.1에서 추가).

## 출처

- [Midjourney Documentation — Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List)
- [Midjourney Documentation — Style Reference](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference)
- [Midjourney Documentation — Omni Reference](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference)
