---
name: detail-page-copy
description: >
  [책임 경계] 카피 산출 (13섹션 감정여정 JSON + 마크다운 미리보기 — Hero→Pain→Problem→Story→Solution→How→Proof→Authority→Benefits→Risk→Compare→Filter→CTA) + V6 신규 모드 (`--mode diagnose`: 7단계 진단 점수 / `--mode copy`: 페르소나 2세트 카피, 비율 25/50/25 강제).
  페어 moai-content:product-detail과 명확히 구분 — 본 스킬은 카피, 페어는 코드 (shadcn/ui React 또는 HTML).
  체이닝 권장: detail-page-copy(카피) → product-detail(코드) 또는 detail-page-copy → detail-page-image(1080×12720 합성 PNG).
  한국 이커머스 상세페이지(상폐)를 위한 13섹션 감정여정 카피를 자동 생성하는 스킬입니다.
  "상세페이지 카피 써줘", "상폐 만들어줘", "이커머스 상세페이지 글 작성해줘", "쇼핑몰 상품 카피 만들어줘", "현재 상세페이지 진단해줘", "상세페이지 점수 매겨줘", "페르소나별 카피 2세트 만들어줘"처럼 말하면 됩니다.
  V6 ③ 상세페이지 도구 = MCP wrapper (SPEC-COMMERCE-V6-003 §5.3 인용).
  v2.4.0 강화: 좋은/피해야 할 예시 가이드 + PAS 카피 공식 매핑 + 혜택 언어 3단계 변환법 (자료 4 §8 광고 심리학 통합).
user-invocable: true
version: 2.4.0
---

# 상세페이지 카피 (Detail Page Copy)

## 개요

이커머스 고전환 상세페이지를 위한 카피 생성 전문 스킬입니다. **3가지 모드**를 지원합니다:

| 모드 | 플래그 | 설명 | 시연 시점 |
|------|--------|------|----------|
| 기본 (13섹션) | 없음 | 감정여정 13섹션 카피 전체 생성 (기존 하위 호환) | 기존 |
| 진단 | `--mode diagnose` | 현재 상세페이지 7단계 진단 점수 (V6 신규) | Day2 4교시 |
| 페르소나 카피 | `--mode copy` | ⑥⑦ 기반 카피 2세트 생성, 비율 25/50/25 강제 (V6 신규) | Day2 4교시 |

**V6 ↔ MCP 매핑** (SPEC-COMMERCE-V6-003 §5.3): V6 ③ 상세페이지 도구 wrapper.

**MCP 백엔드**: 본 스킬은 MoAI-Commerce MCP Phase 1 (SPEC-COMMERCE-MCP-002)의 ③ 상세페이지 도구를 호출합니다 (`--mode diagnose` 및 `--mode copy` 시). MCP 미출시 시점에는 강사 본인 워크스페이스 사전 녹화 영상 5분으로 시연 대체 (PDF §4 운영 노트 §S4 인용).

지원 카테고리: electronics / fashion / food / beauty / home / supplement / pet / kids / handmade / general

## 트리거 키워드

상세페이지, 상폐, 이커머스 상세페이지, 쇼핑몰 카피, 상품 상세, 제품 상세페이지, 상품 설명 페이지,
detail page, 상세 카피, 온라인 쇼핑몰 상품 페이지, 감정여정 카피, 13섹션 상세페이지,
상세페이지 진단, 상세페이지 점수, 7단계 진단, 페르소나 카피, 카피 2세트, 비율 가이드

---

## V6 신규 모드 워크플로우 (--mode diagnose / --mode copy)

### --mode diagnose: 7단계 진단 점수

현재 상세페이지 URL 또는 캡처 이미지를 입력하면 7단계 기준으로 진단 점수를 산출합니다.

**입력**: 현재 상세페이지 URL 또는 스크린샷 이미지

**7단계 진단 기준**:

| 단계 | 진단 항목 | 배점 |
|------|----------|------|
| 1 | Hero — 10초 내 가치 전달 여부 | 15점 |
| 2 | Pain·Problem — 고객 공감 + 문제 정의 명확성 | 15점 |
| 3 | Solution·How — 솔루션 + 작동 방식 설명 | 15점 |
| 4 | Proof·Authority — 사회적 증거 + 전문성 근거 | 15점 |
| 5 | Benefits — 혜택 구체성 + 차별화 | 10점 |
| 6 | Risk·Compare·Filter — 리스크 제거 + 비교 + 타겟 필터 | 15점 |
| 7 | CTA — 긴급성 + 행동 유도 명확성 | 15점 |

**출력 형식** (--mode diagnose):

```json
{
  "mode": "diagnose",
  "url": "{진단 URL 또는 이미지}",
  "total_score": 67,
  "grade": "B",
  "stages": [
    {"stage": 1, "name": "Hero", "score": 12, "max": 15, "issue": "서브카피 없음", "suggestion": "10초 내 USP 한 줄 추가"},
    {"stage": 2, "name": "Pain·Problem", "score": 8, "max": 15, "issue": "고통점 묘사 추상적", "suggestion": "구체 상황 예시 추가"},
    {"stage": 3, "name": "Solution·How", "score": 13, "max": 15, "issue": "작동 방식 3단계 중 2단계만 있음", "suggestion": "3단계 완성"},
    {"stage": 4, "name": "Proof·Authority", "score": 10, "max": 15, "issue": "리뷰 인용 없음", "suggestion": "실제 구매 리뷰 3개 삽입"},
    {"stage": 5, "name": "Benefits", "score": 7, "max": 10, "issue": "혜택 4개 중 2개 중복", "suggestion": "중복 혜택 제거 후 차별화"},
    {"stage": 6, "name": "Risk·Compare·Filter", "score": 8, "max": 15, "issue": "보증 정책 미표기", "suggestion": "환불 정책 + 비추천 대상 추가"},
    {"stage": 7, "name": "CTA", "score": 9, "max": 15, "issue": "긴급성 요소 없음", "suggestion": "한정 수량 또는 마감일 추가"}
  ],
  "priority_fixes": ["stage4 리뷰 추가", "stage1 서브카피", "stage6 보증 정책"],
  "next_step": "--mode copy 로 개선된 카피 2세트 생성 권장"
}
```

---

### --mode copy: 페르소나 2세트 카피 (비율 25/50/25 강제)

⑥⑦ JTBD·페르소나와 현재 상세페이지를 입력받아 메인·보조 페르소나용 카피 2세트를 생성합니다.

**비율 가이드 강제 적용 (REQ-V6-011 HARD)**:
- 문제·공감 섹션: **25%** (Hero + Pain + Problem)
- 핵심·증명 섹션: **50%** (Solution + How + Proof + Authority + Benefits)
- FAQ·CTA 섹션: **25%** (Risk + Compare + Filter + CTA)

**입력 슬롯** (--mode copy):

| 항목 | 필수 여부 | 예시 |
|------|----------|------|
| ⑥ JTBD 결과 | 필수 | commerce-jtbd-persona --mode jtbd 산출물 |
| ⑦ 페르소나 3명 | 필수 | commerce-jtbd-persona --mode persona 산출물 |
| 현재 상세페이지 | 권장 | URL 또는 --mode diagnose 결과 (개선점 반영) |

**출력 형식** (--mode copy):

```json
{
  "mode": "copy",
  "ratio_guide": "25/50/25",
  "persona_sets": [
    {
      "persona": "메인 (박지연, 32세, 직장인)",
      "jtbd_focus": "F1 — 성분 안전성",
      "sections": {
        "problem_empathy_25pct": {
          "hero": {...},
          "pain": {...},
          "problem": {...}
        },
        "core_proof_50pct": {
          "solution": {...},
          "how": {...},
          "proof": {...},
          "authority": {...},
          "benefits": {...}
        },
        "faq_cta_25pct": {
          "risk": {...},
          "compare": {...},
          "filter": {...},
          "cta": {...}
        }
      }
    },
    {
      "persona": "보조1 (김수현, 27세, 대학원생)",
      "jtbd_focus": "E2 — 클린 라이프스타일",
      "sections": {"...": "..."}
    }
  ],
  "slop_review": {
    "status": "passed",
    "changes_made": 3,
    "notes": "ai-slop-reviewer 검수 완료"
  }
}
```

**ai-slop-reviewer 자동 체이닝 (HARD)**: `--mode copy` 산출물은 모든 카피 생성 이후 `moai-core:ai-slop-reviewer`를 자동 체인합니다.

---

## 기존 모드 (13섹션, 하위 호환 유지)

**플래그 없이 호출 시 기존 13섹션 감정여정 카피 모드가 실행됩니다.** 기존 워크플로우, 출력 형식, ai-slop-reviewer 체이닝 모두 동일하게 유지됩니다.

---

## 카피 품질 가이드 (자료 1 §3 + 자료 4 §8, v2.4.0 신규)

### 좋은 예시 vs 피해야 할 예시 (자료 1 §3 상세페이지 체크리스트)

#### ✅ 좋은 예시
```
"하루 종일 피곤하고 집중력이 떨어지시나요?
많은 직장인들이 같은 고민을 하고 있습니다.
100% 자연 성분으로 만든 저희 에너지 드링크는
카페인 부작용 없이 6시간 동안 지속되는 활력을 선사합니다."
```
→ **문제 제시 + 공감 + 해결책 + 차별점**을 간결하게 포함. 7단계 구조 1·2·3 단계가 한 흐름.

#### ❌ 피해야 할 예시
```
"최고 품질의 에너지 드링크입니다.
맛있고 효과적입니다.
많은 분들이 구매하셨습니다.
빨리 구매하세요."
```
→ **구체적 증명과 차별점 없이 추상적 문구만 나열**. 7단계 중 어느 단계도 명확히 수행하지 못함.

### PAS 카피 공식 매핑 (자료 4 §8)

7단계 구조와 PAS(Problem-Agitate-Solution) 카피 공식의 매핑:

| 7단계 | PAS 매핑 | 심리 전략 |
|------|----------|----------|
| 1. 문제 인식 | **P (Problem)** | 타겟이 이미 인식하는 문제를 그들의 언어로 정확히 묘사. 제품 얘기 금지 |
| 2. 공감 | **A (Agitate)** | 문제를 더 크고 아프게 만듦. "지금 해결 안 하면 어떻게 되는가". **손실 회피 편향** 작동 |
| 3. 핵심 메시지 | **S (Solution) 도입** | 해결책 제시. 기능이 아닌 혜택으로 |
| 4. 증명 | **S 강화** | 사회적 증거로 마무리. 통계·리뷰·전문가 |
| 5. 사용법/혜택 | 가치 방정식 적용 | (얻는 것 - 잃는 것) × 신뢰 |
| 6. FAQ/반론 처리 | 제로 리스크 편향 | "30일 환불 보장" 등 |
| 7. 구매 유도 | 손실 회피 + 앵커링 | 마감·할인·증가 가격 대비 |

### 혜택 언어 3단계 변환법 (자료 4 §8)

대부분의 카피가 1단계(기능)에서 멈춤. 3단계까지 가야 정체성 구매 동기 작동.

| 단계 | 변환 결과 | 예시 (방수 소재) |
|------|----------|-----------------|
| **1단계 — 기능의 직접 결과** | 제품 → 무엇을 할 수 있나 | 방수 소재 → **비에 안 젖는다** |
| **2단계 — 결과의 변화** | 결과 → 일상에서 무엇이 바뀌나 | 비에 안 젖는다 → **우산 챙기는 걱정이 사라진다** |
| **3단계 — 변화의 감정 (정체성)** | 변화 → 어떤 사람이 되는 느낌 | 걱정이 사라진다 → **비 오는 날도 가볍게 나가는 사람이 된 느낌** |

> **고객 후기에서 언어를 훔쳐라**: "허리 통증이 사라졌어요"보다 "아침에 일어날 때 더 이상 인상 안 쓰게 됐어요"가 더 강한 혜택 언어. 고객이 실제로 쓴 말이 가장 공명이 강함.

### 카피 작성 체크리스트 (7단계 통합)

각 단계 카피 생성 후 자체 검수:

- [ ] **1·2단계** (25%): 고객 문제를 그들의 언어로 정확히 묘사 + 공감
- [ ] **3·4·5단계** (50%): 차별점 강조 + 구체적 증명(데이터·후기·성분) + 혜택 3단계 변환
- [ ] **6·7단계** (25%): 예상 질문 답변 + CTA 명확 + 긴급성·앵커링
- [ ] **PAS 흐름** 확인 (Problem 명확 → Agitate 강화 → Solution 도출)
- [ ] **혜택 언어 3단계** 변환 완료 (기능 → 변화 → 감정)
- [ ] **금지 표현 회피**: "최고 품질·맛있고 효과적·빨리 구매" 등 추상 문구 ❌
- [ ] **구체적 증거** 포함: 100% 자연 성분, 6시간 지속, 92% 만족 등 ✅

---

## 필요 입력 정보 (기존 모드)

orchestrator가 사용자에게 다음 정보를 사전 수집합니다 (스킬 호출 전 AskUserQuestion 활용):

| 항목 | 필수 여부 | 예시 |
|------|----------|------|
| 상품명 | 필수 | "스마트워치 X200" |
| 카테고리 | 권장 | electronics, fashion, food, beauty, home, supplement, pet, kids, handmade, general |
| 핵심 USP | 필수 | "30시간 배터리 + ANC + IPX5 방수" |
| 타겟 고객 | 권장 | "20~40대 직장인, 운동 즐기는 분" |
| 가격대 | 선택 | "12만 9천원" |
| 브랜드 톤 | 선택 | "신뢰감 있고 전문적" / "젊고 활발하게" |
| 판매 채널 | 선택 | 쿠팡 / 스마트스토어 / 자사몰 / 범용 |
| 보증/AS 정책 | 선택 | "1년 무상 A/S" |

## 워크플로우

### 1단계: 상품 DNA 분석

입력된 상품 정보에서 다음을 추출합니다:

```
ProductDNA:
  physical:
    form: 상품 형태
    colors: 대표 색상
    material: 소재
    signature_angle: 대표 각도/뷰
  positioning:
    tier: mass / premium_indie / luxury
    tone: 어조 앵커 (신뢰/흥미/따뜻함/혁신)
    brand_archetype: 브랜드 원형
  palette:
    primary: 대표 색상
    background: 배경 색상
```

### 2단계: 카테고리 브리프 적용

카테고리별 비주얼·카피 원칙을 적용합니다 (`references/category-briefs.md` 참조):
- **electronics**: 정밀·혁신 어조, 스펙 중심, 기술 신뢰감
- **fashion**: 감성·라이프스타일, 여백 활용, 에디토리얼 톤
- **food**: 따뜻함·풍성함, 식감·향 묘사, 수제·자연 키워드
- **beauty**: 광채·클린뷰티, 성분 강조, 뷰티 루틴 연계
- **home**: 아늑함·의도적 삶, 인테리어 맥락, 감성 라이프스타일
- **supplement**: 신뢰·과학적 근거, 성분 명확화, 안전 보증
- **general**: 깔끔·범용, 제품 중심, 모던 미니멀

### 3단계: 13섹션 카피 생성

`references/13-sections.md`의 각 섹션 규칙을 따라 카피를 작성합니다:

#### 섹션별 카피 요소

| # | 섹션 | 핵심 요소 |
|---|------|----------|
| 1 | **Hero** | 메인 헤드라인 (10초 내 가치 전달) + 서브카피 + CTA 버튼 문구 + 긴급성 뱃지 |
| 2 | **Pain** | 공감 헤드라인 + 고통점 4가지 (불릿) + 감정 연결 문구 |
| 3 | **Problem** | 반전 훅 헤드라인 + 근본 원인 3가지 (번호) + 전환 문구 |
| 4 | **Story** | Before 상태 묘사 + 전환점 레이블 + After 상태 + 증거 수치 |
| 5 | **Solution** | 상품명 + 한 줄 솔루션 + 타겟 핏 태그라인 |
| 6 | **How** | 작동 방식 3단계 (제목 + 짧은 설명) + 결과 하이라이트 |
| 7 | **Proof** | 통계 3개 + 리뷰어 인용 3개 + 에디토리얼 톤 소개 |
| 8 | **Authority** | 창업자/전문가 인용 + 이름 + 직함 + 자격 |
| 9 | **Benefits** | 혜택 6가지 (아이콘 + 레이블) + 보너스 항목 + 총 가치 표현 |
| 10 | **Risk** | 보증 헤드라인 + FAQ 5개 (Q&A) + 공식 문구 |
| 11 | **Compare** | Without 포인트 3개 vs With 포인트 3개 |
| 12 | **Filter** | 추천 대상 3개 + 비추천 대상 3개 |
| 13 | **CTA** | 최종 헤드라인 + 긴급성 카피 + 가격/혜택 표현 + CTA 버튼 + 마감 태그라인 |

### 4단계: ai-slop-reviewer 자동 체이닝 (HARD)

**모든 텍스트 카피 산출 직전에 `moai-core:ai-slop-reviewer`를 호출합니다.**

검수 항목:
- AI 특유 반복 표현 ("물론입니다", "훌륭한", "혁신적인" 등) 제거
- 과도한 형용사 클리셰 정제
- 한국어 이커머스 자연 어체로 조정
- 마케팅 과장 문구 사실 기반으로 수정

## 출력 형식

### 카피 JSON 구조

```json
{
  "product": {
    "name": "상품명",
    "category": "electronics",
    "usp": "핵심 USP",
    "target": "타겟 고객",
    "price": "가격대",
    "tier": "premium_indie"
  },
  "sections": [
    {
      "id": "hero",
      "label": "Hero (긴급성 헤더)",
      "headline": "메인 헤드라인",
      "subheadline": "서브카피",
      "cta": "CTA 버튼 문구",
      "badge": "긴급성 뱃지 문구"
    },
    {
      "id": "pain",
      "label": "Pain (공감)",
      "headline": "공감 헤드라인",
      "bullets": ["고통점1", "고통점2", "고통점3", "고통점4"],
      "bridge": "감정 연결 문구"
    },
    {
      "id": "problem",
      "label": "Problem (문제 정의)",
      "hook": "반전 훅 헤드라인",
      "causes": ["원인1", "원인2", "원인3"],
      "transition": "전환 문구"
    },
    {
      "id": "story",
      "label": "Story (Before→After)",
      "before": "Before 상태 묘사",
      "turning_point": "전환점 레이블",
      "after": "After 상태 묘사",
      "stat": "증거 수치"
    },
    {
      "id": "solution",
      "label": "Solution (솔루션 소개)",
      "product_name": "상품명",
      "one_liner": "한 줄 솔루션",
      "tagline": "타겟 핏 태그라인"
    },
    {
      "id": "how",
      "label": "How It Works (작동 방식)",
      "steps": [
        {"title": "1단계 제목", "desc": "설명"},
        {"title": "2단계 제목", "desc": "설명"},
        {"title": "3단계 제목", "desc": "설명"}
      ],
      "result": "결과 하이라이트"
    },
    {
      "id": "proof",
      "label": "Social Proof (사회적 증거)",
      "stats": ["통계1", "통계2", "통계3"],
      "reviews": [
        {"quote": "리뷰 인용", "reviewer": "리뷰어명"},
        {"quote": "리뷰 인용", "reviewer": "리뷰어명"},
        {"quote": "리뷰 인용", "reviewer": "리뷰어명"}
      ]
    },
    {
      "id": "authority",
      "label": "Authority (권위/전문성)",
      "quote": "전문가 인용",
      "name": "이름",
      "title": "직함",
      "credentials": "자격/경력"
    },
    {
      "id": "benefits",
      "label": "Benefits (혜택)",
      "items": [
        {"label": "혜택1", "desc": "설명"},
        {"label": "혜택2", "desc": "설명"},
        {"label": "혜택3", "desc": "설명"},
        {"label": "혜택4", "desc": "설명"},
        {"label": "혜택5", "desc": "설명"},
        {"label": "혜택6", "desc": "설명"}
      ],
      "bonus": "보너스 항목",
      "total_value": "총 가치 표현"
    },
    {
      "id": "risk",
      "label": "Risk Removal (리스크 제거)",
      "guarantee_headline": "보증 헤드라인",
      "faqs": [
        {"q": "질문1", "a": "답변1"},
        {"q": "질문2", "a": "답변2"},
        {"q": "질문3", "a": "답변3"},
        {"q": "질문4", "a": "답변4"},
        {"q": "질문5", "a": "답변5"}
      ]
    },
    {
      "id": "compare",
      "label": "Before/After Final (최종 대비)",
      "without": ["포인트1", "포인트2", "포인트3"],
      "with": ["포인트1", "포인트2", "포인트3"]
    },
    {
      "id": "filter",
      "label": "Target Filter (타겟 필터)",
      "recommend": ["추천 대상1", "추천 대상2", "추천 대상3"],
      "not_recommend": ["비추천 대상1", "비추천 대상2", "비추천 대상3"]
    },
    {
      "id": "cta",
      "label": "Final CTA (최종 CTA)",
      "headline": "최종 헤드라인",
      "urgency": "긴급성 카피",
      "price_display": "가격/혜택 표현",
      "cta_button": "CTA 버튼 문구",
      "closing": "마감 태그라인"
    }
  ],
  "slop_review": {
    "status": "passed",
    "changes_made": 0,
    "notes": "ai-slop-reviewer 검수 결과"
  }
}
```

### 마크다운 미리보기

JSON 출력 후, 사용자 확인용 마크다운 미리보기를 섹션별로 제공합니다.

## codex CLI 선택적 백엔드

`codex` CLI가 설치되어 있고 OAuth 세션이 활성화된 경우, 분석 단계에서 보조적으로 활용할 수 있습니다.
설치되지 않은 경우 Claude 자체로 카피를 완전히 생성합니다. 두 경우 모두 품질 차이 없습니다.

확인 명령: `codex --version` (없으면 Claude 단독 실행)

## 사용 예시

- "무선 이어폰 상세페이지 카피 써줘 — ANC 탑재, 30시간 배터리, 직장인 타겟"
- "비건 스킨케어 세트 상폐 만들어줘 — 카테고리 beauty"
- "수제 원목 도마 이커머스 상세페이지 — handmade 카테고리, 프리미엄 톤"
- "반려견 유산균 상세페이지 카피 — 수의사 추천 포인트 있음"

## 합격 기준 (V6 강화 모드)

PDF §5.5 ⑧ 합격 기준:

**--mode diagnose**:
- 7단계 모두 점수 산출
- 단계별 개선 제안 1줄 이상
- 우선순위 수정 항목 3개 명시

**--mode copy**:
- 7단계 모두 포함 (섹션 누락 없음)
- 메인·보조 페르소나용 각 1세트 = 총 2세트
- 비율 25/50/25 준수 (문제·공감 / 핵심·증명 / FAQ·CTA)
- ai-slop-reviewer 검수 흔적 (slop_review 블록)

## 관련 스킬

체이닝 (V6): `commerce-jtbd-persona --mode persona` → **detail-page-copy --mode diagnose** → **detail-page-copy --mode copy** → `commerce-product-naming`

- `commerce-jtbd-persona` — ⑥⑦ JTBD·페르소나 (--mode copy 입력)
- `moai-commerce:detail-page-image` — 생성된 카피를 기반으로 13섹션 이미지 합성
- `moai-commerce:marketplace-coupang` — 쿠팡 정책 적용 최적화
- `moai-commerce:marketplace-naver` — 스마트스토어/오픈마켓 최적화
- `moai-content:copywriting` — 일반 광고 카피
- `moai-content:product-detail` — shadcn/ui 기반 웹 상세페이지
- `moai-core:ai-slop-reviewer` — 텍스트 검수 (이 스킬에서 자동 호출)

## 이 스킬을 사용하지 말아야 할 때

- 랜딩 페이지(마케팅 원페이지): `moai-content:landing-page` 사용
- 블로그 포스팅: `moai-content:blog` 사용
- SNS 콘텐츠: `moai-content:social-media` 사용
- 이미지 합성만 필요할 때: `moai-commerce:detail-page-image` 직접 사용