---
name: detail-page-planner
description: |
  한국 이커머스 상세페이지의 기획안(원 메시지·오프닝 유형·본문 뼈대·유통 채널 전략·사진 체크리스트)을 만들어 드립니다. 카피·코드·이미지를 만들기 전, 무엇을 어떤 구조와 톤으로 보여줄지 먼저 확정하는 단계입니다.
  다음과 같은 요청 시 사용하세요:
  - "상세페이지 기획해줘"
  - "상세페이지 구조 짜줘"
  - "이 제품 원 메시지 잡아줘"
  - "와디즈 펀딩 상세페이지 전략 세워줘"
  - "스마트스토어 상세페이지 사진 체크리스트 만들어줘"
  - "화장품 상세페이지 어떻게 구성할지 기획해줘"
  완성한 기획안은 moai-commerce:detail-page-copy(카피) → moai-content:product-detail(코드) → moai-commerce:detail-page-image(이미지)로 이어집니다.
  [책임 경계] vs 페어 스킬: 이 스킬=기획·전략, moai-commerce:detail-page-copy=13섹션 카피, moai-content:product-detail=코드, moai-content:landing-page=단독 랜딩 1페이지.
user-invocable: true
version: 2.27.0
---

# 상세페이지 기획자 (Detail Page Planner)

## 책임 경계

| 단계 | 스킬 | 산출물 |
|------|------|--------|
| 1. 기획·전략 (★ **본 스킬**) | `moai-content:detail-page-planner` | **Brief** (원 메시지·오프닝·본문 뼈대·채널·이미지 체크리스트) |
| 2. 카피 | `moai-commerce:detail-page-copy` | 13섹션 감정여정 JSON |
| 3. 코드 | `moai-content:product-detail` | shadcn/ui React 또는 HTML |
| 4. 이미지 | `moai-commerce:detail-page-image` | 1080×12720 합성 PNG |

**본 스킬은 1번만 담당** — 카피·코드·이미지는 위임. Brief가 후속 3개 스킬의 입력.

## 트리거 키워드

상세페이지 기획, 상세페이지 구조, 원 메시지, 오프닝 4유형, 본문 뼈대, 유통 채널 분기, 펀딩 vs 커머스, 카테고리 사진 체크리스트, 상세페이지 전략, 상폐 기획

## 5대 기획 모듈

### 모듈 1 — One Message 프레임워크 ★ 핵심

**원 메시지** = 상세페이지가 전달할 단 하나의 메시지. 모든 콘텐츠가 이걸 뒷받침해야 한다.

3단 정합 구조:
```
브랜드 컨셉  →  원 메시지  →  이미지·색·글 3요소
```

같은 제품이라도 **타깃에 따라 원 메시지 분기**:

```
원목 수납장 손잡이 예시:
  타깃 A "튼튼함 우선"  → "20kg를 견디는 손잡이"
  타깃 B "예쁨 우선"    → "방의 분위기를 바꾸는 손잡이"
  타깃 C "안전 우선"    → "아이가 매달려도 안전한 손잡이"
```

산출물: `[원 메시지 - 카피 - 설명글]` 세트

```yaml
one_message:
  brand_concept: "{브랜드가 추구하는 본질 한 문장}"
  message: "{원 메시지 한 문장}"
  copy: "{메시지를 강화하는 헤드라인 카피}"
  description: "{메시지를 풀어 설명하는 본문 도입글}"
```

색 체계:
- 브랜드 색 (전체 일관성)
- 상품페이지 컨셉 색 (각 페이지 분위기)
- 두 색을 분리해 운영

이미지 선택 기준:
- **사진 이미지**: 실제 보이는 특징 (텍스처·크기·색)
- **디자인 이미지**: 보이지 않는 특징·컨셉(작동 원리·라이프스타일)

자세한 카테고리별 사진은 → `references/photo-checklist.md`

---

### 모듈 2 — 오프닝 4유형 분기 ★ 핵심

UX 데이터 근거: **3초 = 스크롤 3번**. 어텐션 그래프상 "오프닝 > 본문 > 클로징" 순서로 우선순위.

#### 유형 진단 트리

```
제품이 시장에 처음 나왔는가?
├─ YES → 첫 만남형
└─ NO ↓
    제품 자체가 시각적으로 강한가? (예쁨·독특함)
    ├─ YES → 스타형
    └─ NO ↓
        타깃의 페인포인트가 명확한가?
        ├─ YES → 공감형
        └─ NO  → 매력형 (혜택·가성비 강조)
```

#### 유형별 인트로 3 step 템플릿

| 유형 | Step 1 | Step 2 | Step 3 | 예시 |
|---|---|---|---|---|
| **첫 만남형** | "이런 제품 본 적 있나요?" | 핵심 USP 정의 | 가치 예고 | 3 in 1 마우스 |
| **스타형** | 제품 시각 임팩트 | 제품명·디자인 강조 | 사용 장면 | 빨아 입는 수트 |
| **매력형** | 매력 포인트 1 | 매력 포인트 2 | "지금 결정해야 하는 이유" | (혜택·가성비) |
| **공감형** | "이런 고민 있죠?" | 페인포인트 구체화 | "이 제품이 해결" | (페인 해소) |

총 12개 작성 패턴. 직접 LLM 프롬프트에 인용 가능.

---

### 모듈 3 — 본문 4단계 + 3 미션 체크

#### 4단계 본문 기획 프로세스

```
[1] 인트로     → 모듈 2의 4유형 인트로 적용
[2] 요약 콘텐츠 → 한눈에 보는 USP 1~3개
[3] 소제목 뼈대 → 스캐너 + 검색 고객 동시 대응
[4] 시각 자료  → 모듈 1의 사진/디자인 분기
```

#### 3 미션 체크리스트 (본문 작성 전)

- [ ] **진짜 차별점**이 명확한가? (경쟁 제품 대비)
- [ ] 고객이 **갈아타게** 만드는 이유가 있는가?
- [ ] **생생한 간접 경험**이 들어 있는가? (사용 장면·후기·실측)

#### 본문 USP 정리 공식

```
본문 = 대표 USP 2~3개 + 좋은 제품 특징 2~3개 + 신뢰도/옵션 정보
```

#### "어려운 성분 → 사용자 시각 표현" 3단계 변환

```
[1] 성분 명사     → "히알루론산"
[2] 특징 키워드   → "수분 보유"
[3] 사용자 체감 문장 → "오후 4시에도 촉촉"
```

#### 한국 광고 심의 가드 (카테고리 분기)

- 화장품: 재생·치료·세포 등 의약품 표현 금지 → `references/category-beauty.md`
- 식품: 효능 단정 표현 주의 → `references/category-food.md`
- 패션·생활: 비교 우위 단정 주의

---

### 모듈 4 — 유통 채널 분기 ★ 차별화

펀딩 vs 커머스(오픈마켓)의 사용자 행태가 다르다 — UX 데이터 근거:
- 커머스 사용자는 **체류시간 1/3 단축**
- 스크롤 도달률 **2,000px 짧음**

#### 채널 분기 트리

| 채널 | 사용자 행태 | 본문 전략 |
|---|---|---|
| **펀딩(와디즈·텀블벅)** | 탐색형, 스토리 OK | 인트로 길게, 공감·사회 이슈 OK, 4유형 모두 가능 |
| **커머스(스마트스토어·쿠팡·카카오)** | 목적형, 즉시 판단 | **딴소리 제거**, 제품 특징 즉시 노출, 매력형/스타형 우선 |

#### 커머스 상세페이지 뼈대 템플릿

```
[1] 특징 (USP 즉시 노출)
[2] 차별점 (3 in 3, 경쟁 제품 비교)
[3] 후기 (실사용·평점·이미지)
[4] CTA (구매·찜·문의)
```

#### 4단계 타깃 재정의 프로세스

```
[1] 트렌드 파악         → 카테고리 시장 흐름
[2] 새 타깃 정의        → 구체 페르소나 1~2명
[3] 라이프스타일 매핑    → 일상 시나리오 5개
[4] 마케팅 플랜 일치    → 광고·SNS·검색 통합
```

---

### 모듈 5 — 카테고리별 사진 체크리스트

**9 카테고리 × 가까운/먼** 사진별 필수 항목 → `references/photo-checklist.md`

| 카테고리 | 가까운 (Close) | 먼 (Wide) |
|---|---|---|
| 패션 | 원단 클로즈업·부자재·디자인 디테일 | 전신 착장·코디 룩 |
| 푸드 | 단면·원물·조리예 | 식탁 컨텍스트 |
| 뷰티 | 제형·발색·흡수 | 사용 장면·전후 |
| B2B/SaaS | UI 캡처·데이터 시각화 | 화면 전체·팀 사용 장면 |
| 구독 | 박스 개봉·내용물 클로즈업 | 월별 큐레이션·생활 컷 |
| 베이비/키즈 | 안전 인증·소재 | 연령별 사용 시나리오 |
| 디지털 콘텐츠 | UI 미리보기·강의 캡처 | 학습 환경·결과물 |
| 펫 | 사료 알갱이·성분표 | 반려동물 사용 장면 |
| 여행 | 객실·메뉴 디테일 | 풍경·동선·체험 컷 |

추가 4종 (스포츠/명품 등)은 photo-checklist.md 참조.

#### 사진 없이 상세페이지 기획 5단계 (사진 촬영 전)

```
[1] 원 메시지 결정 (모듈 1)
[2] 특징 3~5개 추출
[3] 각 특징별 사진 종류 결정 (가까운/먼/디자인)
[4] 사진 vs gif 결정
[5] 흐름 짜기 (PowerPoint 워크플로우)
```

---

## 워크플로우 (전체 흐름)

```
사용자 요청 입력
  ↓
[Step 1] 카테고리 진단 (패션/푸드/테크/뷰티/리빙/기타)
  ↓
[Step 2] 채널 진단 (펀딩 vs 커머스) → 모듈 4 분기
  ↓
[Step 3] 모듈 1: One Message 잡기
  ↓
[Step 4] 모듈 2: 오프닝 유형 진단 + 3 step 인트로 작성
  ↓
[Step 5] 모듈 3: 본문 4단계 뼈대 + 3 미션 체크 + 광고 심의 가드 적용
  ↓
[Step 6] 모듈 5: 카테고리별 사진 체크리스트
  ↓
[Step 7] Brief 산출 (YAML/Markdown) → 후속 스킬 입력
```

## Brief 산출 형식

```yaml
brief:
  category: "{패션|푸드|테크|뷰티|리빙}"
  channel: "{펀딩|커머스}"

  one_message:
    brand_concept: "..."
    message: "..."
    copy: "..."
    description: "..."

  opening:
    type: "{첫 만남형|스타형|매력형|공감형}"
    step1: "..."
    step2: "..."
    step3: "..."

  body_skeleton:
    intro: "(모듈 2 적용)"
    summary_usp: ["...", "...", "..."]
    sub_headings: ["...", "...", "..."]
    visual_notes: "(사진/디자인 분기)"

  three_missions:
    real_differentiation: true
    switch_motivation: true
    vivid_indirect_experience: true

  channel_strategy:
    funding_or_commerce: "..."
    body_template: "..."
    target_redefinition:
      trend: "..."
      persona: "..."
      lifestyle: "..."
      marketing_plan: "..."

  photo_checklist:
    close_shots: [...]
    wide_shots: [...]
    gif_or_static: "..."

  ad_compliance_warnings:
    - "..."
```

후속 스킬 호출:
```
1. brief 산출 후 → moai-commerce:detail-page-copy "Brief: <yaml>"
2. 카피 JSON 산출 후 → moai-content:product-detail "Brief + Copy"
3. 코드 산출 후 → moai-commerce:detail-page-image "Brief + Copy + Code"
```

## 사용 예시

### 예시 1 — 자연어 한 줄

```
"신규 비건 비누 상세페이지 기획해줘. 와디즈 펀딩으로 출시 예정."
```

→ Step 1: 카테고리 = 뷰티 (비누) → `references/category-beauty.md` 자동 로드
→ Step 2: 채널 = 펀딩 → 인트로 길게 OK, 공감형/스타형 우선
→ Step 3: One Message — "5가지 식물 추출물로 만든 24시간 보습 비누"
→ Step 4: 오프닝 = 공감형 ("건성 피부 한겨울 가려움" → 페인포인트 → 식물 추출물 해결)
→ Step 5-6: 본문 4단계 + 사진 체크리스트
→ Step 7: Brief YAML 산출

### 예시 2 — 채널·카테고리 미정

```
"화장품 상세페이지 기획"
```

→ AskUserQuestion 1라운드:
   - Q1: 카테고리 세부 (스킨케어·메이크업·헤어 등)
   - Q2: 채널 (펀딩/커머스)
→ 답변 후 Step 1-7 진행

### 예시 3 — Brief만 받아서 후속 위임

```
"이 Brief로 카피랑 코드까지 다 만들어줘"
+ 첨부: 작성된 Brief YAML
```

→ Step 0: Brief 검증 (모듈 1-5 항목 누락 확인)
→ Brief 완성 후: moai-commerce:detail-page-copy → product-detail → moai-commerce:detail-page-image 순차 위임

## 페어 스킬과의 관계

### 본 스킬을 사용하지 않는 경우 (페어 위임)

- "상세페이지 카피 만들어줘" → `moai-commerce:detail-page-copy` (13섹션 JSON)
- "상세페이지 코드 만들어줘" → `moai-content:product-detail` (shadcn/ui 컴포넌트)
- "상세페이지 이미지 합성해줘" → `moai-commerce:detail-page-image` (1080×12720 PNG)
- "랜딩 페이지 만들어줘" → `moai-content:landing-page` (단독 전환 1페이지)

### 본 스킬을 사용하는 경우

- 위 페어 호출 **이전** 단계 — 무엇을 어떤 구조로 어떤 톤으로 만들지를 먼저 확정해야 할 때
- 카테고리·채널·타깃이 모호해서 한 번에 카피·코드로 가기 어려운 경우
- 와디즈/커머스 베스트 프랙티스를 일관 적용하고 싶을 때

## References (분리 자료) — 9 카테고리 커버

### 공통

- `references/photo-checklist.md` — **9 카테고리별** 사진 체크리스트 + 사진 없이 기획 5단계
- `references/copy-patterns.md` — 저관여/고관여 언어 + 가격 13전략 + 카피 100개 raw 예시

### 카테고리 분기 (9종)

| # | references | 적용 |
|---|---|---|
| 1 | `category-fashion.md` | 의류·가방·신발·잡화 — 페르소나 5단계 + 컬러/폰트 |
| 2 | `category-food.md` | 식품·음료·농수산물 — 목적/탐색형 + 식품 심의 + 4 스토리텔링 |
| 3 | `category-beauty.md` | 스킨케어·메이크업·헤어·바디 — 본문 4단계 + 화장품법 + 성분 변환 |
| 4 | `category-b2b-saas.md` | SaaS·솔루션·B2B 제품 — 가격 페이지·기능 비교·데모 CTA·복수 의사결정자 |
| 5 | `category-subscription.md` | 구독 박스·정기 배송·멤버십 — LTV·첫 회 할인·이탈 방지 |
| 6 | `category-baby-kids.md` | 유아·아동용품 — 안전 인증·연령 분기·부모 페인포인트 |
| 7 | `category-digital-content.md` | 강의·e북·뉴스레터·소프트웨어 — 무형 상품·체험 데모·구매 후 흐름 |
| 8 | `category-pet.md` | 반려동물 사료·용품·서비스 — 보호자 신뢰·안전 성분 |
| 9 | `category-travel.md` | 여행·호텔·액티비티 — 무형 경험·계절 분기·예약 흐름 |
| 10 | `category-sports-leisure.md` | 캠핑·러닝·자전거·골프 — 활동 시나리오·기능 사양 |
| 11 | `category-luxury.md` | 명품·하이엔드 — 격식 톤·여백·간결·정통성 |

기타 카테고리(자동차·부동산·금융·의료기기 등)는 별도 도메인 스킬 권장.

## 제한

- **이 스킬은 코드·카피·이미지를 직접 산출하지 않음** — Brief 산출만. 후속 페어 스킬 호출 필수.
- 한국 시장 특화 (와디즈·스마트스토어·쿠팡·카카오 규격). 글로벌 시장은 별도 가이드 필요.
- 광고 심의 가드는 2024 시점 기준 — 변경될 수 있으므로 카테고리별 references/ 정기 업데이트 필요.

## 관련

- before: 사용자 자연어 발화 → 본 스킬 자동 호출
- after: moai-commerce:detail-page-copy → product-detail → moai-commerce:detail-page-image 순차 체이닝
- alternative: 빠른 단일 카피만 → moai-commerce:detail-page-copy 직접
- 가이드: `moai-foundation-cc` (Claude Code 스킬 작성), `.claude/rules/moai/development/skill-authoring.md`
