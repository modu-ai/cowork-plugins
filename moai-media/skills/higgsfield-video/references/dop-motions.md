# Higgsfield DOP — 카메라 무브먼트 카탈로그

DOP (Director of Photography) 모델이 지원하는 카메라 모션 ID와 권장 강도(strength).

## 모션 카테고리

### 1. 줌 (Zoom)

| 모션 ID | 효과 | 권장 strength | 적합 시점 |
|---|---|---|---|
| `slow_zoom_in` | 천천히 가까이 | 0.5-0.8 | 제품 클로즈업·발견 모먼트 |
| `slow_zoom_out` | 천천히 멀어짐 | 0.5-0.8 | 클라이맥스 후 여운 |
| `fast_zoom_in` | 빠르게 가까이 | 0.7-1.0 | 임팩트·놀람 |
| `fast_zoom_out` | 빠르게 멀어짐 | 0.7-1.0 | 반전·드라마틱 |
| `dolly_zoom` (히치콕 줌) | 줌+트랙 반대 | 0.6-0.9 | 긴장감·심리적 충격 |

### 2. 팬 (Pan)

| 모션 ID | 효과 | strength | 적합 |
|---|---|---|---|
| `pan_left` | 좌로 패닝 | 0.4-0.7 | 풍경 탐색·내러티브 |
| `pan_right` | 우로 패닝 | 0.4-0.7 | 같은 용도 |
| `pan_up` | 위로 | 0.5-0.7 | 건물·인물 풀샷 강조 |
| `pan_down` | 아래로 | 0.5-0.7 | 발견·디테일 노출 |

### 3. 트래킹 (Track)

| 모션 ID | 효과 | strength | 적합 |
|---|---|---|---|
| `track_in` | 정면 다가감 | 0.5-0.8 | 주제로 접근 |
| `track_out` | 정면 멀어짐 | 0.5-0.8 | 결말·여운 |
| `side_track_left` | 측면 좌로 이동 | 0.4-0.7 | 흐름·진행 |
| `side_track_right` | 측면 우로 이동 | 0.4-0.7 | 같은 용도 |
| `orbit_left` | 좌측 회전 | 0.6-0.9 | 제품 회전·360도 |
| `orbit_right` | 우측 회전 | 0.6-0.9 | 같은 용도 |
| `orbit_360` | 완전 360도 | 0.7-1.0 | 제품 전체 회전 |

### 4. 돌리·페데스탈 (Dolly/Pedestal)

| 모션 ID | 효과 | strength | 적합 |
|---|---|---|---|
| `dolly_in` | 카메라 자체 전진 | 0.5-0.8 | 줌과 다른 깊이감 |
| `dolly_out` | 카메라 후진 | 0.5-0.8 | 같은 용도 반대 |
| `pedestal_up` | 카메라 상승 | 0.5-0.7 | 풍경 펼침·신적 시점 |
| `pedestal_down` | 카메라 하강 | 0.5-0.7 | 사람 시점으로 |

### 5. 틸트 (Tilt)

| 모션 ID | 효과 | strength | 적합 |
|---|---|---|---|
| `tilt_up` | 카메라 위로 기울임 | 0.4-0.7 | 인물 풀샷·건물 |
| `tilt_down` | 아래로 | 0.4-0.7 | 발 아래·디테일 |

### 6. 특수 효과

| 모션 ID | 효과 | strength | 적합 |
|---|---|---|---|
| `bullet_time` | 매트릭스풍 정지+회전 | 0.7-1.0 | 액션·드라마틱 |
| `handheld` | 핸드헬드 흔들림 | 0.3-0.6 | 다큐멘터리·생동감 |
| `rotation_cw` | 시계 방향 회전 | 0.5-0.8 | 비현실·꿈 시퀀스 |
| `rotation_ccw` | 반시계 방향 | 0.5-0.8 | 같은 용도 |
| `vertigo` | 어지럼증 효과 | 0.6-0.9 | 심리·긴장 |

---

## 조합 가이드

### 단일 모션 (자연스러움 우선)

```
motions: [
  { id: "slow_zoom_in", strength: 0.6 }
]
```

→ 한 가지 효과만 적용. 가장 자연스러움.

### 2개 조합 (드라마틱)

```
motions: [
  { id: "slow_zoom_in", strength: 0.5 },
  { id: "tilt_up", strength: 0.3 }
]
```

→ 줌인하면서 살짝 위로. 인물 강조에 적합.

### 3개 조합 (영화적)

```
motions: [
  { id: "track_in", strength: 0.6 },
  { id: "tilt_down", strength: 0.3 },
  { id: "slow_zoom_in", strength: 0.4 }
]
```

→ 카메라가 다가가며 살짝 내려보고 줌인. 발견 모먼트.

**주의**: 모션 4개 이상은 결과가 흐트러집니다. 최대 3개 권장.

---

## 사용 시나리오별 추천

### 제품 광고 영상

```
1. orbit_360 (strength 0.8) — 제품 전체 노출
2. 이어서 slow_zoom_in (0.5) — 디테일 클로즈업
```

### 인물 인터뷰·다큐

```
handheld (0.4) — 약간의 생동감
```

### 부동산·공간 영상

```
pedestal_up (0.5) + pan_right (0.4) — 공간 펼침
```

### 음식·요리 영상

```
slow_zoom_in (0.6) — 음식에 집중
또는 orbit_left (0.6) — 회전 노출
```

### 발견·언박싱 모먼트

```
tilt_down (0.5) + slow_zoom_in (0.4) — 위에서 천천히
```

### 액션·드라마틱

```
bullet_time (0.9) — 매트릭스풍
또는 dolly_zoom (0.7) — 히치콕 효과
```

### 풍경 영상

```
pan_right (0.6) — 풍경 탐색
또는 pedestal_up (0.5) + pan_left (0.4)
```

---

## strength 가이드

| 값 | 효과 | 시점 |
|---|---|---|
| 0.1-0.3 | 매우 미세함 | 자연스러운 배경 효과 |
| 0.4-0.6 | 보통 | 일반 광고·내러티브 (★ 권장) |
| 0.7-0.9 | 강함 | 드라마틱·임팩트 |
| 1.0 | 최대 | 거의 사용 안 함 — 과함 |

**자연스러움 우선**: 처음에는 0.5로 시작 후 결과 보고 조정.

---

## 호출 예시

```javascript
// 단일 모션
mcp__higgsfield__generate_video_dop({
  input_image_url: "https://...",
  prompt: "A leather wallet on dark wood, warm light",
  motions: [
    { id: "slow_zoom_in", strength: 0.6 }
  ]
})

// 2개 조합
mcp__higgsfield__generate_video_dop({
  input_image_url: "https://...",
  prompt: "Modern office interior, daylight from window",
  motions: [
    { id: "track_in", strength: 0.5 },
    { id: "pan_right", strength: 0.4 }
  ]
})

// 3개 조합 (영화적)
mcp__higgsfield__generate_video_dop({
  input_image_url: "https://...",
  prompt: "Founder at desk, contemplating",
  motions: [
    { id: "dolly_in", strength: 0.5 },
    { id: "tilt_down", strength: 0.3 },
    { id: "slow_zoom_in", strength: 0.4 }
  ]
})
```

---

## 주의

- 모션 ID는 Higgsfield 업데이트에 따라 변할 수 있음. 호출 실패 시 [공식 페이지](https://higgsfield.ai/mcp)에서 최신 목록 확인
- 정확한 UUID 형식 모션 ID를 사용하는 경우도 있음 (커뮤니티 MCP 구현)
- DOP는 기본 generate_video보다 1.2-1.5배 비쌈 (카메라 워크 계산 추가)
