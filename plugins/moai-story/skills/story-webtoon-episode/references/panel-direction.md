# 컷 연출 — 프레임 연출 8종 + 인물 배치 5종 + 작성 위치 승격

> `story-webtoon-episode` Step 3에서 로드한다. 감정 정점 컷의 **프레임(테두리)을 연출**하거나 **인물이 컷 경계를 넘게** 배치하는 영어 프롬프트 카드셋. 영어 스니펫은 해석·번역하지 않고 그대로 컷 지시에 삽입한다. **감정 정점 컷에만** — 남발하면 대비가 죽는다.

## A. 감정 컷 프레임 연출 8종

컷 테두리 자체를 감정에 맞게 연출한다. **인물·말풍선은 온전하게, 프레임만** 연출한다. 위·아래 컷은 일반 테두리로 둬야 대비로 살아난다.

| 프레임 연출 | 프롬프트 지시(영어, 해당 컷에 삽입) | 감정·상황 |
|------|------|-----------|
| **Shattered**(깨진 유리) | `shattered comic panel frame, broken glass shards around the border` | 충격·절망 |
| Spiderweb(거미줄 금) | `spiderweb cracks spreading across the panel frame` | 충격(Shattered의 약한 변주) |
| **Darkness**(어둠 침식) | `dark shadow consuming the panel border, creeping inward` | 공포·불길·절망 |
| **Glitch**(글리치) | `glitching comic panel frame, pixel distortion, RGB split` | SF·오류·현실 붕괴 |
| **Breakout**(튀어나옴) | `character breaking out of the panel frame, breaking through the border` | 역동·돌파·강조 |
| **Torn/Aged paper**(낡은 종이) | `torn old aged paper comic panel, frayed edges` | 회상·과거(세피아 톤까지 자동으로 물듦) |
| **Ink/Watercolor**(번짐) | `watercolor / ink splash panel border, soft bleeding edges` | 아련·감성·꿈 |
| **Cherry blossom**(벚꽃) | `cherry blossom petals forming the panel border` | 따뜻·봄·추억 |

**★ 충격 클라이맥스 조합**(단일보다 강): `shattered comic panel frame, dramatic focus lines behind the character, blinding white flash`.

**감정 → 프레임 매핑:** 충격/절망 → Shattered·조합 / 공포·불길 → Darkness / SF·붕괴 → Glitch / 역동·돌파 → Breakout / 회상·과거 → Torn paper / 아련·감성·꿈 → Ink splash / 따뜻·봄 → Cherry blossom / 여운·감동 → 무경계(테두리를 흐리게, `soft feathered fade`).

## B. 컷 경계 넘는 인물 배치 5종

인물이 프레임을 넘는 레이아웃. 실측상 프레임 변형(A)보다 **인물이 컷을 넘는 쪽(B)이 더 안정적**이다.

| 배치 | 프롬프트 지시(영어) | 상황 |
|------|------|------|
| **부치누키**(세로 관통) | `a tall full-body character standing vertically across multiple stacked panels, breaking through the panel borders, dynamic first-appearance composition` | 첫 등장·존재감 |
| **오버레이**(배경 인물+작은 컷) | `a large character illustration as the background, with smaller comic panels layered on top, emotional and introspective atmosphere` | 회상·감정 몰입 |
| **경계 걸침**(두 컷 잇기) | `character standing on the border between two panels, straddling the gutter line, connecting the two scenes seamlessly` | 장면 전환·연결 |
| **부분 삐져나옴**(손·팔) | `character's hand and arm reaching out of the panel, breaking the border into the gutter, dynamic and tactile` | 순간 강조·긴박 |
| **전신+리액션 컷** | `one full-body character in the center surrounded by small reaction panels scattered around, energetic and expressive` | 일상·코미디·들뜬 감정 |

**상황 → 배치 매핑:** 첫 등장 → 부치누키 / 회상 → 오버레이 / 전환 → 경계 걸침 / 강조 → 부분 삐져나옴 / 일상·코미디 → 전신+리액션.

> **★ 세로 스크롤에서 부치누키(세로 관통)는 원본(페이지형)보다 적합도가 오히려 높다.** 세로 스크롤은 위→아래로 길게 흐르므로 여러 컷을 세로로 관통하는 인물 배치가 자연스럽다 — 첫 등장·존재감 연출에 적극 활용한다.

## C. 작성 위치 승격 규칙 (실측)

배치·연출 지시를 컷 묘사 문장 **안에 한 줄로 묻으면 무시된다**(묘사 안 삽입 2회 연속 실패 → 페이지/컷 레벨로 승격 후 1회 성공).

- 승격 형식: 컷 지시 직후 **`★ 레이아웃:` 줄**로 별도로 쓴다.
  ```
  컷 7: 라이벌이 골목 끝에 처음 나타난다.
  ★ 레이아웃: a tall full-body character standing vertically across multiple stacked panels, breaking through the panel borders (부치누키 — 첫 등장)
  ```
- "굵은 검은 테두리·직사각" 전역 못박기는 **일반 컷에만** 한정한다(연출 컷과 충돌).
- 연출 컷은 "어느 테두리를 어떻게 넘는지" 구체적으로 쓴다(예: `character's body drawn on top of the frame lines, crossing OVER the border`).

## D. 남발 금지 원칙

- **감정 정점 컷 1개에만.** 위·아래 컷은 일반 테두리 유지 → 대비로 살아난다.
- **같은 구간에 A(프레임 연출)와 B(인물 배치)를 겹쳐 쓰지 않는다** — 이중 연출은 산만.
- 정적 구간은 직사각 기본 + 포인트 1~2개.

## E. 앵글 · 거리 · 시점 — 컷마다 따로 명시

컷 크기(높이)와 별개의 독립 레버다. 각 컷 지시에 셋을 **각각 따로** 적는다 — 묶어서 뭉뚱그리면 AI가 미디엄 수평만 반복한다.

- **거리**: 풀샷 · 미디엄 · 미디엄 클로즈업 · 클로즈업 · 익스트림 클로즈업. 한 씬에 **2~3종 혼합**(같은 거리만 반복 = 밋밋).
- **앵글**: 수평 · 부감(하이) · 앙각(로우) · 더치(기울임). **앵글은 감정 강도·인물 권력 관계와 일치시킨다** — 올려다보면(앙각) 압도, 내려다보면(부감) 위축.
- **시점**: 1인칭(POV·몰입) / 3인칭(객관·거리) / 관찰자(관계 전체가 보이는 와이드).

**감정 → 앵글 즉시 매핑:** 압도·위협 → 앙각 / 위축·고립 → 부감 / 불안·붕괴 → 더치 / 일상 → 수평.

## F. 180도 연속성 — 좌우 고정 (예방 규칙)

좌우 반전은 `story-webtoon-qc`의 결함 7종에 있지만, **프롬프트 단계에서 예방**하는 것이 싸다.

- **좌우 고정 명시**: 모든 대치·격돌·대화 컷에 `"A는 화면 왼쪽 / B는 화면 오른쪽"`을 적는다. 안 적으면 컷마다 좌우가 뒤집힌다(원본 실측: ep01 v1 반전 사례).
- **앵커 컷에서 확정**: 씬의 첫 와이드 컷에서 두 인물의 좌우 위치를 정하고, 이후 단독 클로즈업에서도 **시선 방향이 상대방 쪽**을 향하게 유지한다.
- 진행 방향·시선 방향은 씬 내내 일관. 의도적으로 어길 때는 `의도적 연출 — [이유]`를 컷 메모에 남긴다.

## 출처

- 프레임 연출 8종·인물 배치 5종·작성 위치 승격·앵글 체계·180도 규칙: aitoon-comic 연출 시스템(내부 자산 이식). 페이지형 전제(거터·왼→오)는 제거하고 세로 스크롤 맥락으로 조정.
- 원작 카피라이터: **조남경** (https://www.facebook.com/Bmisty)
