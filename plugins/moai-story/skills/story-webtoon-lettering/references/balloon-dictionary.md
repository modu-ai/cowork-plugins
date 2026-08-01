# 말풍선 사전 (세로 스크롤 웹툰용)

> **누가 읽나 — 이 스킬이다. 말풍선을 직접 그리지 않는다.** 장면 감정 → 아래에서 **이름 고르기** → 그 **영어 스니펫을 컷 프롬프트에 그대로 복붙.** 그림은 이미지 모델이 그린다. 해석·번역하지 말고 스니펫을 그대로 쓴다(이름이 곧 작동 토큰).

## 0. 원칙

- **이름이 형태를 강제** — 이름 속 형태 단어("Spike")는 프롬프트로 못 뺀다. 빼려면 그 단어 없는 이름을 쓴다.
- **과분류 금지** — 비슷한 건 큰 갈래로 수렴. 감정 라벨(Angry/Rage…)은 형태에 매핑하고 따로 항목을 만들지 않는다.
- **열림 원칙** — 사전은 바닥선(보장)이지 천장(규격)이 아니다. 모델이 더 나으면 자유 확장 가능, 판단은 사용자.
- **점선구름 = 소심한 혼잣말 전용** / 생각 기본형은 Fine Spike Aura.
- **클린 원고 역획득** — 완성본 → 말풍선 제거(원본 비율 유지)로 수정 안전망을 만든다.

## 1. 코어 (거의 모든 웹툰에 쓰임)

### 대사 / 생각
| 이름 | 복붙 스니펫 | 언제 |
|------|-------------|------|
| Normal Speech | `a normal speech balloon (smooth oval, small tail to mouth)` | 평범한 대사(기본) |
| Conversational/Soft | `a soft conversational speech balloon (smooth rounded oval)` | 부드러운 대화 |
| Hand-Drawn Rough | `a "Hand-Drawn Rough Outline" balloon (wobbly/sketchy uneven outline; TEXT clean sans-serif)` | 더듬·당황 (그 풍선만 거칠게) |
| Whisper | `a WHISPER balloon (dashed/dotted outline)` | 속삭임 |
| Double/Split | `a DOUBLE/SPLIT balloon (one character's line in two linked bubbles, tail on the 2nd to mouth)` | 한 화자 끊어 말하기 |
| Wobble ⭐ | `a "Wobble Balloon" (wavy/shaky trembling outline)` | 불안·떨리는 목소리 |
| Fine Spike Aura | `a "Fine Spike Aura" balloon (oval with a fine thin spiky aura outline, NO tail)` | 미묘한 긴장·깨달음(생각 기본형) |
| Fuzzy/Inner Shock | `a "Fuzzy/Inner Shock" balloon (oval with a thick fuzzy fur-like aura, NO tail)` | 강한 내면 충격 |
| Soft Cloud Thought | `a soft cloud thought balloon (cloud shape, dotted edge, small bubble tail)` | 소심한 혼잣말 |

### 외침 / 감정
| 이름 | 복붙 스니펫 | 언제 |
|------|-------------|------|
| Loud Shout/Scream | `a loud scream balloon (sharp spiky burst)` | 외침·비명 |
| Surprised/Shocked | `a "Surprised/Shocked" balloon (jagged burst outline)` | 놀람·경악 |
| Panic/Alarmed | `a "Panic/Alarmed" balloon (explosive jagged burst)` | 당황·다급 |
| Held-Back Spike | `a "Held-Back Spike" balloon (angular polygon body; the single SPIKE points toward the mouth and serves AS the tail — one spike, no separate tail)` | 억눌린·참는 톤 |
| Demonic/Menacing | `a "Demonic/Menacing" balloon (heavy black spiky/jagged outline)` | 불길·위협 |
| Crying ⭐ | `a "Crying Balloon" (drooping outline with tear-like drops)` | 울며 말하기 |
| Broken Voice ⭐ | `a "Broken Voice Balloon" (cracked outline)` | 감정 북받침·격해짐 |
| Dripping ⭐ | `a "Dripping Balloon" (melting/dripping outline)` | 충격·허탈 |
| Dry Voice ⭐ | `a "Dry Voice Balloon" (thin brittle angular outline)` | 시큰둥·비꼼(일상 코미디) |

### 특수 / 매체(기본)
| 이름 | 복붙 스니펫 | 언제 |
|------|-------------|------|
| Narration Box | `a NARRATION BOX (rectangular caption box, no tail; add "with a visible rectangular border" for a boxed edge)` | 나레이션·자막 |
| Telephone/Electronic | `a TELEPHONE/ELECTRONIC balloon (rectangular with a zig-zag electronic outline)` | 전화 너머 목소리 |

## 2. 확장 (장르별 — 필요할 때 꺼내 씀)

> ★ 매체는 모델 기준 "실제 기기 아이콘"으로 나온다(전화기·라디오·TV 모양). 이게 표준 형태.

### 디지털·전자
| 이름 | 스니펫 | 언제 |
|------|--------|------|
| Chat Message | `a chat message bubble (app-style rounded rectangle with tail)` | 메신저·문자 |
| Notification | `a notification bubble (small rounded rect with an alert mark)` | 앱 알림 |
| Glitch | `a "Glitch Balloon" (broken digital/glitch edges)` | 깨진 신호·오류 |
| Pixel | `a "Pixel Balloon" (blocky pixelated outline)` | 레트로 게임·디지털 |
| Hologram | `a "Hologram Balloon" (translucent layered, glowing outline)` | 홀로그램·투사 음성 |
| Static | `a "Static Balloon" (noisy broken outline)` | 잡음·신호 불량 |
| Recording Playback | `a recording-playback balloon (playback bar / waveform box)` | 녹음 재생 |
| Electric | `a "Electric Balloon" (lightning jagged burst)` | 전기·충격·에너지 |
| Spark | `a "Spark Balloon" (oval with small spark/star accents)` | 번뜩임·흥분 |

### 매체·음성 기기 (모델 = 기기 아이콘)
| 이름 | 스니펫 | 언제 |
|------|--------|------|
| Phone | `a phone balloon (rounded rect with a handset tail / phone device look)` | 전화 통화 |
| Radio | `a "Radio Balloon" (old radio-device shaped)` | 라디오 송출 |
| TV | `a "TV Balloon" (TV-screen shaped box)` | TV 음성 |
| Speaker/Megaphone | `a megaphone balloon (megaphone cone + balloon)` / `a speaker-device balloon` | 확성·방송 |
| Intercom | `a "Intercom Balloon" (intercom panel with UI marks)` | 인터폰·PA |
| Robot | `a "Robot Balloon" (angular mechanical frame)` | 로봇 음성 |
| AI Assistant | `a "AI Assistant Balloon" (clean rounded UI bubble + AI mark)` | AI·챗봇 |
| Synth Voice | `a "Synth Voice Balloon" (geometric waveform edge)` | 합성·기계 음성 |

### 환경 / 액션
| 이름 | 스니펫 | 언제 |
|------|--------|------|
| Underwater | `an "Underwater Balloon" (wavy bubbly outline)` | 물속·먹먹한 음성 |
| Echo | `an "Echo Balloon" (concentric repeated outlines)` | 메아리·울림 |
| Frozen | `a "Frozen Balloon" (icy angular frost edge)` | 차가움·얼어붙음 |
| Fire | `a "Fire Balloon" (flame-shaped outline)` | 분노·열정 |
| Wind | `a "Wind Balloon" (stretched flowing outline)` | 바람에 실린 음성 |
| Metal | `a "Metal Balloon" (hard beveled metal polygon)` | 금속·기계·냉정 |

### 장식 / 판타지
| 이름 | 스니펫 | 언제 |
|------|--------|------|
| Ornate | `an "Ornate Balloon" (decorative ornate border)` | 우아·연극적 |
| Scroll | `a "Scroll Balloon" (parchment scroll shape)` | 사극·고풍·판타지 |
| Glass | `a "Glass Balloon" (thin sharp cracked-glass outline)` | 깨질 듯·연약 |
| Poison | `a "Poison Balloon" (bubbling uneven toxic outline)` | 독설·사악 |
| Magic | `a "Magic Balloon" (ornate sparkly outline)` | 마법·주문 |
| Star | `a "Star Balloon" (star-shaped body)` | 밝은 흥분 |
| Gem | `a "Gem Balloon" (faceted jewel shape)` | 화려·마법 |
| Flower | `a "Flower Balloon" (floral petal edge)` | 사랑스러움·로맨스 |
| Calligraphy | `a "Calligraphy Balloon" (brush-calligraphic frame)` | 시적·역사극 |
| Void | `a "Void Balloon" (black-filled body, white text)` | 공허·냉랭·불길 |

## 3. 꼬리 규칙

- **꼬리:** 있으면 화자 입 쪽. 한 컷에 여러 풍선이면 각자 입 쪽.
- **꼬리 없는 타입:** 생각(Aura·구름), 전자/전화, 나레이션 박스.
- **예외:** Held-Back Spike는 스파이크가 곧 꼬리(별도 꼬리 금지).

## 4. 위치 거동 — 세로 스크롤 기준 (전면 신규 작성)

페이지형 만화의 "거터(칸 사이 흰 공간) 걸침" 개념은 세로 웹툰에 그대로 쓰지 않는다. 세로 웹툰은 **위→아래 연속 스크롤 + 컷 사이 세로 여백 띠**가 기준이다.

- **컷 안 고정(contained)** — `keep this balloon inside the panel` : 대사가 그 컷의 사건에 묶일 때.
- **여백 띠 활용(스크롤 전환)** — 컷과 컷 사이 세로 빈 띠에 나레이션/독백을 얹어 장면을 넘긴다. `place this narration in the vertical gap band between panels` : 시간·장소 전환의 호흡.
- **여백 띠 침범 금지(원칙)** — 말풍선이 **아래 컷의 그림 영역을 덮어** 스크롤 리듬을 깨뜨리면 안 된다. 큰 외침이라도 여백 띠 안에서 키우고, 다음 컷 그림 위로 흘러내리지 않게 한다. `do NOT let the balloon spill over into the next panel's artwork`.
- **1화면 동시 노출 상한** — 모바일 세로 뷰포트 한 화면(스크롤 한 눈)에 **말풍선은 2~3개를 넘기지 않게** 배치한다. 한 화면에 대사가 몰리면 읽기 순서가 무너진다. 대사가 많으면 컷을 세로로 더 쪼개 여러 화면에 나눈다.
- **읽기 순서** — 세로 웹툰은 기본 위→아래. 한 컷/한 화면에 2풍선이면 순서를 명시: `top balloon FIRST, bottom balloon SECOND`, 각자 꼬리 입 쪽.

## 5. 큰 글씨 배분

내용 많은 대사가 작게 눌려 안 보이는 문제를 막는다. 컷 감정으로 강도를 자동 배분한다.

- **기본:** 말풍선·나레이션 박스를 넉넉히, 글자가 그 안을 꽉 채우게. → 일반 대사·나레이션.
- **감정 강조:** 외침·Panic·충격·절규는 글자를 특히 크고 굵고 또렷하게.
- **작게 유지(예외):** 속삭임·독백·조용한 여운은 큰 글씨 미적용(점선/작은 풍선으로 차별, 연출 보존).
- **세로형 절제:** 말풍선을 무리하게 키워 **다음 컷 그림·여백 띠를 덮지 않는다.** 이미 크게 잡힌 컷에는 글자 크기만 맞춰 이중 강조를 피한다.

## 6. 부록 — 수렴 / 제외

- **수렴:** Cave Echo → Echo · Smoke·Dream → Soft Cloud · Slime → Dripping.
- **제외:** Speed(풍선 형태 아님 — 화살표/속도선의 클린 효과로 처리).
- **손글씨체:** 본문 금지 — 효과음·특수 요소에만. 서체 규칙은 `korean-lettering.md`.

## 출처

- 핵심 자산: aitoon 연출·기획 시스템(내부 자산 이식, 세로 스크롤·한국 플랫폼 맥락으로 조정).
- 원작 카피라이터: **조남경** (https://www.facebook.com/Bmisty)
