# Midjourney v8.1 — Style/Omni/Personalization Deep Dive

`--sref`·`--oref`·`--p` 3대 reference 시스템 상세 가이드.

## 1. --sref (Style Reference)

이미지의 **스타일·미학·색감·매체**를 새 프롬프트에 입히는 옵션.

### 사용법

```
--sref CODE                 # 라이브러리 코드 (숫자)
--sref https://image.jpg    # URL
--sref CODE1 CODE2 CODE3    # 다중 (공백 구분, 가중치 자동 평균)
--sref random               # 무작위
```

### --sw (Style Weight)

| 값 | 동작 |
|---|---|
| `--sw 0` | sref 거의 무시 |
| `--sw 100` (default) | 균형 |
| `--sw 300` | 강한 스타일 전이 |
| `--sw 1000` | 최대 — 새 프롬프트가 거의 무시될 수 있음 |

### --sv (Style Version)

V8 default는 `--sv 7`. 이전 버전을 명시적으로 쓰려면 추가.

| 버전 | 사용 시점 |
|---|---|
| `--sv 4` | 2025.06.16 이전 sref 결과 재현 |
| `--sv 6` | V7 중반 결과 재현 |
| `--sv 7` (default) | V8 권장. 4x 빠름·저렴, `--hd`·`--p`·`--stylize`·`--exp` 지원 |

### 자주 쓰이는 패턴

```
--sref 1234567890 --sw 200          # 단일 코드, 강한 영향
--sref URL --sw 100 --sv 7          # 사용자 이미지 reference
--sref CODE1 CODE2 --sw 150         # 다중 평균
--sref random                       # 탐색 → 결과 후 실제 코드 확인
```

### 비용

- 4x cost (per Midjourney 공식).
- `--hd` + `--q 4` + `--sref` 조합 = 16x × 4x = 64x ⚠️.

### 일반적 실패와 대응

| 증상 | 원인 | 대응 |
|---|---|---|
| 새 프롬프트 무시 | `--sw` 너무 높음 | `--sw` 100-200으로 낮춤 |
| 스타일 약함 | `--sw` 너무 낮음 | `--sw` 300-500 |
| 색감만 변동 | 단일 sref | 다중 sref 또는 sref + 텍스트 키워드 보강 |

## 2. --oref (Omni Reference, V6 --cref 대체)

이미지의 **캐릭터·객체·차량·생물**을 새 프롬프트에 등장시키는 옵션. V8에서는 인간 캐릭터를 일관되게 시리즈로 만드는 표준 도구.

### 사용법

```
--oref https://image.jpg
```

### --cw (Character Weight)

**가장 중요한 함정**.

| 값 | 가져오는 항목 |
|---|---|
| `--cw 0` | 얼굴만 (의상·조명·스타일 무시) |
| `--cw 20~40` (얼굴 중심 권장) | 얼굴 + 약간의 형태 |
| `--cw 50~70` (의상 포함) | 얼굴 + 의상 + 기본 자세 |
| `--cw 100` (default ⚠️) | 거의 모든 디테일 (조명·스타일·자세) |

**Default 100은 함정**. 새 프롬프트에서 다른 조명·환경을 지정해도 reference 이미지의 조명·미학을 상속하므로 결과가 충돌함. 일반 권장: `--cw 30~60`.

### 비호환

| 모드/옵션 | 비호환 이유 |
|---|---|
| Fast Mode | 처리 시간 부족 |
| Draft Mode | 품질 보장 안 됨 |
| Conversational Mode | 입력 형식 충돌 |
| `--q 4` | 비호환 명시 |

### 편집 (Editor) 사용

`--oref` 이미지를 Editor에 로드해 추가 편집할 때는 프롬프트에서 `--oref`·`--cw` 파라미터를 제거해야 함.

### 비용

- 2x cost.

### 자주 쓰이는 패턴

```
# 캐릭터 일관성 시리즈 (광고 5장)
--oref https://character.jpg --cw 50

# 얼굴만 등장 (의상은 새 프롬프트로)
--oref https://character.jpg --cw 25

# 가상 캐릭터 다양한 포즈 시리즈
--oref https://character.jpg --cw 60 --s 300
```

## 3. --p / --profile (Personalization & Moodboards)

사용자의 취향을 학습한 프로파일을 자동 적용. `--sref`보다 추상적·통합적인 스타일.

### 단계

| Ratings | 상태 |
|---|---|
| 0-39 | setup 진행 중 (사용 불가) |
| 40 | 시작 가능 |
| 200 | stable (권장 시작점) |
| 2000 | 최대 개선 |

### 사용법

```
--p                        # default moodboard 사용
--p PROFILE_ID             # 특정 named profile
--profile PROFILE_ID       # 동일
--p PROFILE_ID --sref CODE # sref와 함께 (시너지)
```

### V8 신규

- 여러 named profile 동시 활성화 가능
- 5x 빠른 setup
- V7 프로파일이 V8.1과 호환됨 (Global Profile 지원)

### 자주 쓰이는 패턴

```
# 개인 디폴트 스타일 유지
--ar 1:1 --p

# 브랜드 전용 프로파일 + 캐릭터 일관성
--p BRAND_PROFILE_ID --oref https://hero.jpg --cw 40
```

## 4. Combination Cheatsheet

### 광고 캠페인 (캐릭터 시리즈 5장)

```
[prompt] --ar 4:5 --style raw --p BRAND_PROFILE --oref CHARACTER_URL --cw 50 --s 300
```

### 시네마틱 풍경 (16:9 와이드)

```
[prompt] --ar 16:9 --style raw --hd --q 4 --sref MOOD_CODE --sw 200 --s 400
```

### 빠른 탐색 (저비용)

```
[prompt] --ar 1:1 --style raw --s 200
```

### 일러스트 시리즈

```
[prompt] --ar 1:1 --sref ART_CODE --sw 300 --s 500
```

## 출처

- [Midjourney Documentation — Style Reference](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference)
- [Midjourney Documentation — Omni Reference](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference)
- [Midjourney Documentation — Character Reference (deprecated)](https://docs.midjourney.com/hc/en-us/articles/32162917505293-Character-Reference)
- [Prompting Systems — How to use Midjourney --cref/--oref](https://prompting.systems/blog/how-to-use-midjourney-cref-for-consistent-characters)
