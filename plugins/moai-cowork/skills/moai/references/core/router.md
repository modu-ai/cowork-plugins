# router.md — 자연어 → 하네스 매핑 프로토콜

## 개요
사용자의 자연어 요청을 분석하여 적절한 MoAI 하네스(skill)를 자동 감지하고 라우팅하는 프로토콜입니다.
의도 분류, 키워드 매핑, 모호성 해소를 통해 최적의 실행 경로를 결정합니다.

---

## 1. 요청 분석 단계

### 1.1 자연어 파싱
사용자 입력에서 다음을 추출합니다:
- **핵심 동사**: "작성", "분석", "계획", "검토", "자동화" 등
- **도메인 키워드**: 마케팅, 재무, 기술, 전략, 콘텐츠 등
- **문맥 신호**: 긴급성, 복잡도, 팀 규모, 기한 등
- **명시적 대상**: 산출물(문서, 이메일, 계획서 등)

### 1.2 의도 분류 알고리즘
- IF 사용자_요청 IN [콘텐츠_생성, 글쓰기, 블로그, SNS, 이메일] → copywriting, email-crafter, social-media
- IF 사용자_요청 IN [자동화, 워크플로우_최적화, 프로세스] → sop-writer, project-tracker, remote-work-ops
- IF 사용자_요청 IN [법규_검토, 규제, 컴플라이언스] → compliance, contract-review, regulatory
- IF 사용자_요청 IN [일정관리, 협업, 커뮤니케이션] → meeting-strategist, stakeholder-report

---

## 2. 키워드 매핑 테이블

| 키워드 그룹 | 예시 | 하네스 | 우선순위 |
|-----------|------|------|---------|
| 콘텐츠 창작 | 블로그, 글쓰기, SNS, 카피 | copywriting, newsletter, content-calendar | 1순위 |
| 이메일 | 이메일 작성, 제안서 | email-crafter, proposal-writer | 1순위 |
| 마케팅 | 캠페인, 퍼널, 광고, SEO | ad-campaign, growth-hacking, social-media | 1순위 |
| 재무/분석 | 예산, ROI, 수익 | financial-model, analytics-report, data-analysis | 1순위 |
| 전략/계획 | OKR, 로드맵, 분기 계획 | product-roadmap, market-research, business-model-canvas | 1순위 |
| 자동화/운영 | 반복작업, 프로세스, 파이프라인 | sop-writer, project-tracker, remote-work-ops | 1순위 |
| 법규/컴플라이언스 | 법규, 계약, 규제 | compliance, contract-review, regulatory | 1순위 |
| 기술/개발 | 코드, API, 아키텍처 | feature-spec, technical-writer, release-notes | 2순위 |
| 협업/일정 | 회의, 일정, 진척도 | meeting-strategist, stakeholder-report | 2순위 |

---

## 3. 모호성 해소 로직

### 3.1 감지 신호
- 여러 하네스가 동등한 점수 (예: content + email 동시 매칭)
- 도메인 신호 부재 (추상적/일반적 요청)
- 상충하는 키워드 (예: "마케팅 자동화 법규 검토")
- 첫 사용자 또는 프로필 불완전

### 3.2 AskUserQuestion 재질문
모호성 감지 시, 최대 **4개 질문**으로 확인합니다:
- Q1: 주요 작업 타입 (4옵션)
- Q2: 도메인 (4옵션)
- Q3: 산출물 형태 (3-4옵션)
- Q4: 긴급도/복잡도 (3옵션)

---

## 4. 복합 요청 분기 처리

### 4.1 순차 실행 (Sequential)
예: "캠페인 계획 → 이메일 초안 → 성과 분석"
- Phase 1: ad-campaign
- Phase 2: email-crafter
- Phase 3: analytics-report

### 4.2 병렬 실행 (Parallel)
예: "마케팅 전략 + 재무 예산 동시 필요"
- Track A: market-research
- Track B: financial-model
- 병합 및 통합 분석

### 4.3 의존적 실행 (Dependent)
예: "법규 검토 후 계약서 작성"
- Phase 1: compliance (제약사항 산출)
- Phase 2: contract-review (Phase 1 결과 참조)

---

## 5. 라우팅 결정 트리

```
사용자_요청_분석
├─ [콘텐츠&마케팅] 신호?
│  ├─ YES → 콘텐츠 타입 확인
│  └─ NO → 다음 분기
├─ [비즈니스&전략] 신호?
│  ├─ YES → 자동화/계획/분석 확인
│  └─ NO → 다음 분기
├─ [전문분야&규제] 신호?
│  ├─ YES → compliance, contract-review, regulatory
│  └─ NO → 다음 분기
└─ [라이프&커뮤니케이션] 신호?
   ├─ YES → meeting-strategist, travel-planner, event-organizer
   └─ NO → 일반 AskUserQuestion
```

---

## 6. 실행 순서 (Priority Ranking)

라우팅 후 최적 하네스 선택:

1. **프로필 기반 가중치**: 사용자 role/industry와 하네스 매칭
2. **요청 신선도**: 최근 선택한 하네스 선호 (학습 효과)
3. **완성도**: 필수 컨텍스트 충분 여부
4. **복잡도**: 요청 복잡도와 하네스 난이도 매칭

---

## 7. 확장성 및 커스터마이징

### 7.1 조직별 라우팅 규칙
`.moai/routing-rules.yaml`:
```yaml
tech_startup:
  high_priority: [feature-spec, ai-strategy, product-roadmap]
finance_corp:
  high_priority: [financial-model, compliance, accounting-tax]
```

### 7.2 사용자 선호도 학습
- 선택 이력 추적 (.moai/user-preferences.md)
- 실행 성공률 기반 가중치 조정
- 피드백 루프: 평점 → 가중치 재계산

---

## 8. 오류 처리 및 폴백

| 상황 | 조치 |
|-----|------|
| 하네스 미설치 | `/moai init --harness {name}` 제안 |
| 프로필 불완전 | `/moai init` 재실행 유도 |
| 모두 불확실 | 일반 AI 어시스턴트로 폴백 |
| 모호 (해소 불가) | 2회 재시도 후 다시 분류 |

---

## 9. 성능 메트릭

- **정확성**: 선택 하네스 = 사용자 예상 (%)
- **응답 속도**: 라우팅 결정 시간 (< 2초)
- **재질문 빈도**: 모호성 해소 시도 횟수
- **성공률**: 라우팅 후 작업 완료율
