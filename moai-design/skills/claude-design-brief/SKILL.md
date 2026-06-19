---
name: claude-design-brief
description: |
  Claude Design용 6요소 브리프(Project·Audience·Pages·Tone·Reference·Constraints)를 자동으로 작성해 주는 스킬.
  자연어 한 줄 요청에서 시작해 누락된 요소를 차례로 채우고, AI 슬롭 회피 블록을 포함한 복붙용 프롬프트를 출력합니다.
  완성된 프롬프트는 claude.ai/design 채팅에 그대로 붙여 넣어 사용합니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "Claude Design 브리프 만들어 줘"
  - "클로드 디자인 프롬프트 작성"
  - "디자인 브리프 6요소"
  - "claude.ai/design에 넣을 프롬프트"
  - "디자인 요청 정리"
user-invocable: true
version: 2.27.0
---

# claude-design-brief — Claude Design 6요소 브리프 빌더

## 개요

Claude Design 사용자가 가장 자주 실패하는 지점은 **막연한 톤만 적은 채 프롬프트를 던지는 것**입니다. 이 스킬은 [docs-site 베스트 프랙티스](https://cowork.mo.ai.kr/claude-design/best-practices/)에서 정리한 6요소 템플릿을 자동으로 채워, **claude.ai/design 채팅에 그대로 붙여 넣을 수 있는 프롬프트**를 만들어 줍니다.

## 트리거 키워드

Claude Design 브리프, 클로드 디자인 프롬프트, 디자인 브리프 6요소, claude.ai/design 프롬프트, 디자인 요청 정리, 디자인 시안 프롬프트, design brief

## 6요소 템플릿

```
[ROLE]      [구체적 직업·연차·소속 — 선택]
[GOAL]      [한 문장 목표 — 사용자가 무엇을 X초 안에 할 수 있게]
[AUDIENCE]  [구체적 사용자 — 직책·산업·맥락]
[PAGES]     [필요한 페이지·섹션 목록 + 각 목적]
[TONE]      [형용사 3-5개]
[REFERENCE] [URL·스크린샷]
[CONSTRAINTS] [디바이스·시스템·제외 항목]

[AI SLOP 회피]
진부한 폰트(Inter·Roboto·Arial)·보라 그라데이션·천편일률 3-카드 그리드 금지.
우리 브랜드의 고유 비주얼로.
```

## 워크플로우

### 1단계 — 자연어 1줄 입력 수신

사용자가 다음 같은 한 줄을 입력합니다.

```
예시 입력:
- "마케팅 자동화 SaaS 가격 페이지"
- "10슬라이드 시드 피치덱"
- "헬스케어 웨어러블 랜딩"
- "어드민 대시보드 - KPI 5개·차트 2개"
- "결제 플로우 3페이지 와이어프레임"
```

### 2단계 — 누락 요소 보완

입력에서 추출된 요소를 확인하고, **6요소 중 누락된 항목**을 AskUserQuestion으로 차례로 보완합니다.

- 한 라운드에 최대 4개 질문
- 모든 항목에 "건너뜀(추측으로 채움)" 옵션 포함
- "Reference URL" 같은 자유 응답이 필요한 항목은 사용자가 직접 입력
- 사용자가 이미 명시한 요소는 다시 묻지 않음

#### 주요 질문 패턴

**ROLE 추천**:
```
어떤 디자인 관점이 가장 중요한가요?
- 정보 구조·내비게이션 (IA 시니어 아키텍트)
- 사용성·휴리스틱 (Baymard Institute 컨설턴트)
- 카피·마이크로카피 (Dropbox UX 라이터)
- 온보딩·활성화 (Intercom 프로덕트 디자이너)
- 접근성 (Level Access 컨설턴트)
- 데이터 시각화 (Tableau 디자이너)
- 폼 컨버전 (CXL Institute 옵티마이저)
- 디자인 시스템 (Figma 디자인 시스템 엔지니어)
- 일반 — 역할 부여 없이
```

**TONE 추천**:
```
다음 중 3-5개를 골라 주세요 (또는 직접 입력):
- 신뢰감 있는 · 데이터 중심 · 미니멀
- 활기찬 · 친근한 · 따뜻한
- 진중한 · 격식 있는 · 전문적
- 대범한 · 실험적 · 하이테크
- 부드러운 · 차분한 · 자연 친화적
```

**REFERENCE 안내**:
```
참고할 만한 사이트가 있나요? 다음을 적어 주세요:
- 자사 잘 만든 페이지 URL (가장 강한 시그널)
- 경쟁사 또는 동경하는 사이트 URL
- Dribbble · Behance 컬렉션
- 없으면 "건너뜀" 선택 — 추천 사이트를 제안해 드립니다
```

### 3단계 — 추측 보완

"건너뜀" 처리된 항목은 합리적 추측으로 채웁니다.

| 항목 | 추측 규칙 |
|---|---|
| ROLE | GOAL의 영역에 맞춰 자동 선택 (예: 가격 페이지 → "12년차 시니어 UX 아키텍트") |
| AUDIENCE | "일반 사용자" 대신 GOAL의 산업 맥락으로 (예: "B2B SaaS의 의사결정자") |
| PAGES | GOAL이 명시한 페이지만 (1-3개) |
| TONE | 미니멀·신뢰감·데이터 중심 (안전한 기본값) |
| REFERENCE | linear.app · stripe.com · 자사 도메인의 기존 페이지 |
| CONSTRAINTS | "데스크톱 우선·반응형 포함" 기본 |

### 4단계 — 프롬프트 합성

6요소를 결합해 복붙용 프롬프트를 생성합니다.

```
다음 프롬프트를 claude.ai/design 채팅에 그대로 복사·붙여넣기 하세요:

---
[ROLE]      12년차 시니어 UX 아키텍트 IDEO 출신.

[GOAL]      B2B 마케팅 자동화 SaaS의 가격 페이지에서 3티어 비교를
            10초 안에 의사결정 가능하게.

[AUDIENCE]  20-100명 스타트업의 그로스 리드·마케팅 매니저.

[PAGES]     Hero(가치 제안) · 3티어 가격 카드 · 비교표 · FAQ ·
            Sticky CTA.

[TONE]      신뢰감 있는, 데이터 중심, 미니멀, 약간의 활기.

[REFERENCE] linear.app/pricing, stripe.com/pricing 톤 참고.

[CONSTRAINTS] 데스크톱 우선, 기존 React 시스템, 결제 정보 입력 X.

[AI 슬롭 회피] 진부한 폰트(Inter·Roboto·Arial)·보라 그라데이션·
              천편일률 3-카드 그리드 금지. 우리 브랜드 고유 비주얼로.

[OUTPUTS]   1) Hero 시안, 2) 3티어 카드 시안, 3) 비교표,
            4) 의사결정 지원 마이크로카피.
---

내보낼 형식 권장: PPTX(발표용) · PDF(외부 발송) · Claude Code 핸드오프(코드 구현).
```

### 5단계 — 후속 안내

```
다음 단계 추천:
- 디자인 시스템 셋업이 안 됐다면 → moai-design:claude-design-system-prep
- 특정 영역(IA·접근성·온보딩)에 집중 → moai-design:claude-design-prompt-builder
- 결과 카피 검수 → moai-design:claude-design-slop-check
- 핸드오프 번들 분석 → moai-design:claude-design-handoff-reader
```

## 출력 형식

```
## Claude Design 브리프

### 입력 분석
- GOAL: [감지된 목표]
- 누락 요소: [보완한 항목 목록]

### 완성된 프롬프트 (복붙 가능)
```
[프롬프트 본문]
```

### 다음 단계
- [후속 스킬·내보내기 형식 제안]
```

## 사용 예시

### 예시 1 — 가격 페이지 (Pro 사용자, 자료 풍부)

```
사용자: "B2B 마케팅 자동화 SaaS 가격 페이지. 우리는 14-day trial,
         경쟁사는 30-day."

→ 누락 요소 보완: AUDIENCE만 보완 (나머지는 GOAL에서 추출)
→ AUDIENCE: "20-100명 스타트업의 그로스 리드" (보완)
→ 완성된 프롬프트 출력
```

### 예시 2 — 피치덱 (창업자, 자료 적음)

```
사용자: "10슬라이드 시드 피치덱"

→ 보완 필요: AUDIENCE · TONE · REFERENCE · CONSTRAINTS
→ AskUserQuestion 1라운드: AUDIENCE·TONE
→ AskUserQuestion 2라운드: REFERENCE·CONSTRAINTS
→ 완성된 프롬프트 출력
```

### 예시 3 — 와이어프레임 (PM, 명확한 PRD 있음)

```
사용자: "결제 플로우 3페이지 와이어프레임 - Cart, Address, Payment"

→ 보완 필요: AUDIENCE · TONE
→ ROLE 자동: "Baymard Institute UX 컨설턴트" (결제 영역 권장)
→ 완성된 프롬프트 출력
```

## 주의사항

### Do

- 한 번에 6요소 모두 채워 줍니다 — 사용자가 Claude Design에서 다시 헤매지 않게
- AI 슬롭 회피 블록을 **항상** 포함합니다
- ROLE은 GOAL 영역에 맞춰 추천 — 일반 역할보다 구체적 직업이 결과 분산 30-40% 감소
- REFERENCE URL은 **실물 1개가 사양서 3개보다** 강한 시그널

### Don't

- 사용자가 명시한 요소를 다시 묻지 않음
- "예쁘게" "좋게" 같은 모호한 톤 단어 자동 사용 금지
- 사용자가 모르는 디자인 도구 이름(Figma·Sketch 등) 강제 도입 금지
- 한 라운드에 5개 이상 질문 금지 (AskUserQuestion 한도 4개)

## 관련 스킬

| 스킬 | 사용 시점 |
|---|---|
| `moai-design:claude-design-system-prep` | 선행: 디자인 시스템이 아직 셋업 안 됐을 때 |
| `moai-design:claude-design-prompt-builder` | 대안: 특정 UX 영역(IA·접근성·온보딩 등)에 집중하고 싶을 때 |
| `moai-design:claude-design-slop-check` | 후속: 시안 결과 카피 검수 |
| `moai-design:claude-design-handoff-reader` | 후속: Claude Code 핸드오프 번들 분석 |
| `moai-content:landing-page` | 대안: 코드 기반 랜딩 페이지 직접 제작 |
| `moai-marketing:brand-identity` | 보조: 브랜드 정체성이 모호할 때 먼저 정리 |
