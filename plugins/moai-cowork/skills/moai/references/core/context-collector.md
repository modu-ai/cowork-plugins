# context-collector.md — 맥락 수집 프로토콜

## 개요
하네스 실행에 필요한 사용자 맥락을 체계적으로 수집하는 프로토콜입니다.
맥락 충분성 등급, 모호성 감지, 반복 제한을 통해 효율적인 수집을 구현합니다.

---

## 1. 맥락 충분성 등급

### A등급 — 필수 (즉시 충족 가능)
프로필 재사용으로 즉시 획득:
- 사용자 이름
- 선호 언어
- 국가
- 역할 (Job title)
- 산업
- 타임존

**충족 조건**: /mnt/.auto-memory/moai-profile.md 로드

---

### B등급 — 핵심 (80% 이상 충족 권장)
하네스별 도메인 맥락:

**copywriting**:
- 주요 콘텐츠 형식 (블로그/이메일/SNS/광고)
- 타겟 독자/청중
- 톤&스타일 (공식/캐주얼/기술적)
- 발행 채널 (웹/이메일/SNS)

**financial-model**:
- 분석 범위 (회사 전체/부서/프로젝트)
- 주요 KPI (수익/비용/ROI/현금흐름)
- 시간 단위 (월/분기/연)
- 비교 기준 (이전 기간/목표/경쟁사)

**sop-writer**:
- 자동화 대상 프로세스
- 현재 반복 주기 (일/주/월)
- 예상 효율 개선도
- 우선 영역

**ad-campaign**:
- 캠페인 목표 (인식/전환/유지)
- 타겟 고객 세그먼트
- 예산 규모
- 경쟁 환경

---

### C등급 — 보강 (완성도 향상용)
추가 컨텍스트:
- 팀 규모
- 업무 일정/마감
- 최근 트렌드/시장 변화
- 주요 과제/고충
- 기술 스택
- 예산 제약

---

## 2. 맥락 수집 플로우

### 2-1. 초기 평가
```
harn_contexts = load_harness_contexts(selected_harness)
current_context = collect_user_context_from_profile()
missing_context = A등급 + 필수_B등급 - current_context

IF missing_context.empty():
  → 즉시 실행 (프로필 완전)
ELSE:
  → 질문 프롬프트 생성
```

### 2-2. 질문 생성 (AskUserQuestion)
```
Q_count = min(len(missing_context), 4)
질문들 = generate_questions(missing_context, Q_count)

FOR each 질문 in 질문들:
  options = generate_options(질문, default_3_to_4)
  user_response = AskUserQuestion(질문, options)
  context_store[질문_id] = user_response
```

### 2-3. 모호성 감지
질문 응답 후:
```
IF response == "기타" OR response_confidence < 0.7:
  → 모호성 신호 감지
  → follow_up_question = generate_clarification(질문)
  → follow_up_response = AskUserQuestion(follow_up)
  → context_store[질문_id] = [response, follow_up_response]
```

### 2-4. 소크라테스식 심화 질문 (Socratic Deepening)

AskUserQuestion 옵션 선택 이후, 맥락 깊이를 B→C등급으로 향상시키기 위해
**텍스트 대화 기반** 열린 질문을 1-2개 수행한다.

```
IF sufficiency_score >= 60% AND sufficiency_score < 80%:
  → 소크라테스식 심화 질문 수행 (텍스트 대화)

목적별 질문 패턴:

  [동기 탐색] "이 작업이 필요하게 된 배경은 무엇인가요?"
  [전제 확인] "그렇게 판단하신 근거는 무엇인가요?"
  [대안 탐색] "다른 접근 방식도 고려해 보셨나요?"
  [영향 범위] "이 결과물이 누구에게 어떤 영향을 줄까요?"
  [제약 발견] "이 작업에서 꼭 피해야 할 것이 있나요?"

적용 규칙:
  - AskUserQuestion이 아닌 일반 텍스트 대화로 수행
  - 질문은 최대 2개 (사용자 피로 방지)
  - 답변을 요약하여 확인: "정리하면 ~이라는 뜻이 맞으시죠?"
  - 사용자가 "빨리 진행해" 또는 간단히 답하면 즉시 실행으로 전환
  - 응답 내용을 context_store에 저장
```

### 2-5. 충분성 재평가
```
updated_context = context_store + previous_context
sufficiency_score = evaluate_context_completeness(
  missing_context,
  updated_context
)

IF sufficiency_score >= 80%:
  → Phase 완료, 실행 시작
ELSE IF sufficiency_score >= 60%:
  → 경고: "일부 정보 부재, 진행하시겠습니까?"
  → 선택: [계속] [추가 정보]
ELSE:
  → 부족: "필수 정보를 모두 입력해주세요."
  → 재질문
```

---

## 3. 반복 제한 및 방지

### 3-1. 최대 반복 횟수
```
max_rounds_per_harness = 7회

LOOP for round in 1..7:
  remaining_context = identify_missing_context()
  IF remaining_context.empty():
    break  (충족)
  
  questions = generate_questions(remaining_context, max_4)
  FOR q in questions:
    response = AskUserQuestion(q)
    store_context(q, response)
  
  sufficiency = evaluate()
  IF sufficiency >= 80% or round >= 7:
    break

IF round >= 7 and sufficiency < 60%:
  warn("충분한 정보 없이 진행합니다. 정확도가 낮을 수 있습니다.")
```

### 3-2. 반복 방지 (캐싱)
```
context_cache = load_from_profile()
FOR each harness:
  IF context_cache[harness] exists and age < 30days:
    reuse(context_cache[harness])
    skip_collection()
  ELSE:
    collect_context(harness)
```

### 3-3. 피드백 루프
실행 후 평가:
```
evaluation = get_user_feedback_or_auto_eval()
IF evaluation_score >= 8/10:
  → 컨텍스트 충분 (캐시 유지, TTL = 90days)
ELSE IF evaluation_score >= 5/10:
  → 컨텍스트 부분 적용 (TTL = 30days)
ELSE:
  → 컨텍스트 갱신 필요 (TTL = 7days, 재수집 권장)
```

---

## 4. 모호성 감지 규칙

### 4-1. 신호 패턴
```
[신호 1] 다중 선택 (1 이상의 "기타")
[신호 2] 저신뢰도 응답 (예: "음... 잘 모르겠어요")
[신호 3] 상충하는 답변 (예: Q1="매일" vs Q2="월 1회")
[신호 4] 도메인 키워드 부재 (너무 일반적인 답변)
[신호 5] 프로필 불일치 (역할과 요청이 불일치)
```

### 4-2. 해소 전략
```
IF signal_count <= 1:
  → 단순 follow_up (1질문)
  
ELSE IF signal_count >= 2:
  → 다중 follow_up (최대 2질문)
  → 또는 수동 입력 제안

IF mobo_resolution_attempts >= 2:
  → "일부 정보 불명확하지만 진행 가능합니다."
  → [계속] [저장 후 나중에]
```

---

## 5. 저장 및 추적

### 5-1. 저장 구조
```
.moai/
├── context-log.md
│   ├── collection_date: YYYY-MM-DD HH:MM
│   ├── harness_id: {harness}
│   ├── rounds_taken: 3
│   ├── sufficiency_score: 85%
│   ├── contexts_collected:
│   │   ├── q1: {answer}
│   │   ├── q2: {answer}
│   │   └── ...
│   └── evaluation_after_exec: 8/10
│
└── harness-contexts/
    ├── copywriting.md (B등급 메타데이터)
    ├── financial-model.md
    └── ...
```

### 5-2. 메타데이터 추적
```
context_metadata = {
  collected_date: timestamp,
  source: "profile" | "user_input",
  confidence: 0.0 ~ 1.0,
  ttl_days: 30,
  last_used: timestamp,
  feedback_score: 0 ~ 10,
  refresh_needed: boolean
}
```

---

## 6. 컨텍스트 갱신 트리거

자동 갱신 요청:
- 프로필 변경 후 (회사, 역할, 산업)
- TTL 만료 시
- 평가 점수 < 5/10
- 사용자 명시적 요청 (`/moai refresh-context`)

---

## 7. 서브에이전트 제약

서브에이전트(nested skills)에서:
- **금지**: AskUserQuestion 직접 호출
- **대신**: 부모 에이전트 컨텍스트 참조
- **필요시**: 부모에게 컨텍스트 재수집 요청

```
# 서브에이전트 내부
IF context_missing():
  return error("Parent context required")
  # 부모 에이전트가 처리
```

---

## 8. 성능 메트릭

추적 메트릭:
- **수집 효율**: 라운드당 획득 정보량
- **충분성률**: 첫 라운드에 A+B등급 달성 %
- **재질문율**: 평균 재질문 횟수
- **만족도**: 사용자 평가 평균
- **캐시 히트율**: 프로필 재사용 %

