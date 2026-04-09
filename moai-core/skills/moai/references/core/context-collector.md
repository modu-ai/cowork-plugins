# context-collector.md — 맥락 수집 프로토콜

## 개요
하네스 실행에 필요한 사용자 맥락을 체계적으로 수집하는 프로토콜입니다.
맥락 충분성 등급, 심화 인터뷰, 모호성 감지, 반복 제한을 통해 효율적인 수집을 구현합니다.

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

**충족 조건**: /mnt/.auto-memory/moai-profile.md 로드 (CLAUDE.md 시스템 지침 참조)

---

### B등급 — 핵심 (80% 이상 충족 권장)
하네스별 도메인 맥락. **반드시 해당 하네스 레퍼런스의 "맥락 수집 질문" 섹션 참조**.

**질문 생성 규칙 (중요!)**:
```
1. 하네스 레퍼런스 로딩: Read("references/skills/{harness-id}.md")
2. "맥락 수집 질문 (AskUserQuestion)" 섹션의 필수 질문(Q1~Q4) 그대로 사용
3. 임의로 질문을 만들지 않는다
4. 옵션 예시도 레퍼런스 원본 그대로
```

**예시** (레퍼런스 기반):

**copywriting** (references/skills/copywriting.md):
- Q1. 콘텐츠 목적은? → 브랜드 인지 / 리드 생성 / 전환 유도 / 고객 유지
- Q2. 타겟 독자는? → B2B 의사결정자 / B2C 소비자 / 내부 직원 / 투자자
- Q3. 긴급도는? → 즉시 / 1주일 내 / 2주+ / 미정
- Q4. 선호 톤은? → 전문적 / 캐주얼 / 스토리텔링 / 데이터 중심

**market-research** (references/skills/market-research.md):
- Q1. 조사 대상은? → 특정 산업명/제품군
- Q2. 조사 목적은? → 신규 진입 / 경쟁 대응 / 투자 판단 / 전략 수립
- Q3. 지리 범위는? → 한국 / 아시아 / 글로벌
- Q4. 초점은? → 시장 규모 / 경쟁사 / 소비자 니즈 / 트렌드

**technical-writer** (references/skills/technical-writer.md):
- Q1. 문서 유형은? → API 가이드 / 사용자 매뉴얼 / 운영 가이드 / 제품 가이드
- Q2. 타깃 독자는? → 개발자 / 관리자 / 최종 사용자 / 조합
- Q3. 기술 스택은? → 웹 / 모바일 / 클라우드 / 데이터베이스 / 기타
- Q4. 문서 현황은? → 신규 / 기존 개선 / 마이그레이션 / 유지보수

---

### C등급 — 보강 (심화 인터뷰로 수집)
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
harness_ref = Read("references/skills/{harness-id}.md")
current_context = collect_user_context_from_profile()
missing_context = A등급 + 필수_B등급 - current_context

IF missing_context.empty():
  → 즉시 실행 (프로필 완전)
ELSE:
  → 질문 프롬프트 생성 (harness_ref의 맥락 수집 질문 사용)
```

### 2-2. 질문 생성 (AskUserQuestion)
```
# 하네스 레퍼런스에서 질문 추출
questions = extract_questions_from_harness_ref(harness_ref, section="맥락 수집 질문")
Q_count = min(len(questions), 4)

FOR each 질문 in questions[:Q_count]:
  options = 질문.options  # 레퍼런스에 정의된 옵션 그대로 사용
  user_response = AskUserQuestion(질문.text, options)
  context_store[질문.id] = user_response
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

### 2-4. 심화 인터뷰 (Deep Interview)

AskUserQuestion 옵션 선택 이후, 맥락 깊이를 B→C등급으로 향상시키기 위해
**텍스트 대화 기반** 열린 질문을 1-2개 수행한다.

```
IF sufficiency_score >= 60% AND sufficiency_score < 80%:
  → 심화 인터뷰 수행 (텍스트 대화)

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

하네스별 심화 질문 우선순위:
  - 전략/규제 하네스 (market-research, compliance 등): 동기 탐색 + 전제 확인
  - 콘텐츠 하네스 (copywriting, newsletter 등): 영향 범위 + 제약 발견
  - 기술 하네스 (technical-writer, feature-spec 등): 대안 탐색 + 제약 발견
  - 또는 하네스 레퍼런스의 "선택적 심화 질문" 섹션에서 택 2
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

IF resolution_attempts >= 2:
  → "일부 정보 불명확하지만 진행 가능합니다."
  → [계속] [저장 후 나중에]
```

---

## 5. 저장 및 추적

### 5-1. harness-contexts 파일 구조 (핵심!)

**기존 문제**: 15줄짜리 축약본만 생성됨
**개선**: 사용자 맥락 + 풀 하네스 레퍼런스 복사

```markdown
# {사용자 언어 하네스명} ({harness-id}) — 하네스 컨텍스트

## 사용자 맥락 (수집 결과)
- **하네스 ID**: {harness-id}
- **표시명**: {사용자 언어 하네스명}
- **카테고리**: {category}
- **설치일**: {YYYY-MM-DD}
- **충분성 등급**: {A/B/C}

### 수집된 답변
- **Q1**: {질문} → {답변}
- **Q2**: {질문} → {답변}
- **Q3**: {질문} → {답변}
- **Q4**: {질문} → {답변}

### 심화 맥락 (심화 인터뷰 결과)
- {열린 질문 1}: {사용자 답변 요약}
- {열린 질문 2}: {사용자 답변 요약}

### 활용 시나리오
- {구체적 시나리오 1}
- {구체적 시나리오 2}
- {구체적 시나리오 3}

---

## 하네스 레퍼런스 (원본)

{references/skills/{harness-id}.md 전체 내용 복사}
{축약 금지! 페르소나, 전문가 역할, 워크플로우, 산출물 형식 등 모두 포함}
```

**파일 최소 크기**: 80줄 이상
- 사용자 맥락 섹션: ~25줄
- 하네스 레퍼런스 원본: ~55줄 이상 (하네스별 상이)
- 15줄 축약본은 부적합 → 재생성 필요

### 5-2. 메타데이터 추적
```
context_metadata = {
  collected_date: timestamp,
  source: "profile" | "user_input" | "document_upload",
  confidence: 0.0 ~ 1.0,
  ttl_days: 30,
  last_used: timestamp,
  feedback_score: 0 ~ 10,
  refresh_needed: boolean,
  interview_depth: "step1_only" | "step1_step2" | "full_step123"
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
- **심화 인터뷰 깊이**: 평균 심화 질문 수
