# Midjourney v8.1 — Cost Traps & Common Pitfalls

V8.1의 새 파라미터는 강력하지만 비용이 곱연산으로 늘어납니다. 다음 함정 6종을 항상 검사하세요.

## Trap 1 — `--hd` + `--q 4` = 16x

각각 4x 비용 → 조합 시 **16배 GPU 시간**.

### 검사
프롬프트 출력 전에 `--hd`와 `--q 4`가 모두 있는지 확인. 본 스킬은 이를 자동 검사하여 한국어 해설에 경고 표시:

```
⚠️ 비용 경고: --hd + --q 4 조합 = 16x GPU 시간
   1차 탐색은 둘 다 제거, 최종 production에서만 활성화 권장.
```

### 권장

| 단계 | 파라미터 |
|---|---|
| 1차 탐색 (variation 8장) | 기본 (1x) |
| 컨셉 확정 후 정제 (4장) | `--q 4` (4x) |
| 최종 production (1-2장) | `--hd --q 4` (16x) |

## Trap 2 — `--cw 100` (default) 상속 함정

`--oref`를 쓰면 `--cw` 기본값 100이 적용됨. Reference 이미지의 **조명·스타일·자세까지 상속**되어 새 프롬프트의 조명·환경 지시가 무시될 수 있습니다.

### 검사
`--oref`가 있는데 `--cw`가 명시되지 않은 프롬프트는 자동으로 다음 경고:

```
⚠️ --cw 함정: default 100으로 reference의 조명·스타일까지 상속됩니다.
   얼굴만 가져오려면 --cw 20~40 권장.
   의상까지 가져오려면 --cw 50~70.
```

### 권장 매트릭스

| 사용 케이스 | --cw |
|---|---|
| 캐릭터 얼굴만, 새 의상·새 환경 | 20-40 |
| 캐릭터 얼굴 + 의상, 새 환경 | 50-70 |
| 캐릭터 전체 (모든 디테일 복제) | 80-100 |

## Trap 3 — `--sref random` 재현 불가

`--sref random`은 호출 후 자동으로 실제 코드로 변환되지만, 사용자가 그 코드를 확인·저장하지 않으면 다음 generation에서 같은 스타일을 재현할 수 없습니다.

### 검사
`--sref random` 발견 시:

```
⚠️ --sref random: 결과 이미지가 마음에 들면 변환된 실제 sref 코드를
   Discord 응답에서 확인해 저장하세요. 그렇지 않으면 같은 스타일
   재현이 불가능합니다.
```

## Trap 4 — V6 옵션 잔존 (`--cref`)

V8에서 `--cref`는 deprecated. 자동으로 `--oref`로 대체되지만, 사용자가 V6 가이드를 보고 `--cref`를 입력하면 본 스킬이 다음을 출력:

```
⚠️ --cref는 V7·V8에서 deprecated. 자동으로 --oref로 변환했습니다.
   --cw 파라미터는 그대로 유효합니다 (default 100 함정 주의).
```

## Trap 5 — `--oref` 비호환 모드

`--oref`는 다음 모드와 비호환:

- Fast Mode
- Draft Mode
- Conversational Mode
- `--q 4`

### 검사
`--oref` + `--q 4` 또는 Fast/Draft/Conv 모드 인디케이터가 함께 있으면 경고:

```
⚠️ --oref는 --q 4 / Fast Mode / Draft Mode / Conversational Mode와
   비호환입니다. 둘 중 하나만 사용하세요.
```

## Trap 6 — Personalization 학습 부족

`--p PROFILE_ID`를 사용했는데 해당 프로파일의 ratings가 40 미만이면 효과가 미미하거나 무시됩니다.

### 권장 단계

| Ratings | 권장 |
|---|---|
| 0-39 | `--p` 사용 안 함, 표준 프롬프트로 |
| 40-199 | `--p` 사용 가능하지만 효과 일관성 부족 |
| 200+ | stable, production 가능 |
| 2000+ | 최대 개선 |

## 추가 함정 — Relax Mode

V8 Alpha 초기 출시(2026.03.17)에는 Relax Mode가 없어 모든 generation이 Fast 또는 paid GPU 시간을 소비했습니다. V8.1에서 점진적으로 Relax 추가 중. 비용 민감 워크플로우는:

```
사전 확인: alpha.midjourney.com 또는 Discord settings에서 Relax 가용 여부 체크
```

## 안전한 디폴트 (본 스킬이 자동 적용)

라운드 정보가 충분하지 않을 때 본 스킬이 기본으로 적용하는 파라미터:

```
--ar [Round 3에서 받은 값] --style raw --s 200
```

`--hd`·`--q 4`·`--sref`·`--oref`·`--p`는 사용자가 명시적으로 요청했을 때만 추가됩니다.

## 출처

- [Midjourney Documentation — Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List)
- [Midjourney Documentation — Style Reference](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference)
- [Midjourney Documentation — Omni Reference](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference)
- [AI Tools DevPro — Midjourney v8 Specs Manual](https://aitoolsdevpro.com/ai-tools/midjourney-guide/)
