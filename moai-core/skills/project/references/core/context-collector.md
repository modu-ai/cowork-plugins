# context-collector.md — 맥락 수집 프로토콜

## 개요
이 프로젝트의 스킬 체인 실행에 필요한 사용자 맥락을 체계적으로 수집하는 프로토콜입니다.
맥락 충분성 등급, 심화 인터뷰, 모호성 감지, 반복 제한을 통해 효율적인 수집을 구현합니다.

---

## 1. 맥락 충분성 등급

### A등급 — 필수 (프로젝트 CLAUDE.md에서 즉시 획득)
프로젝트 CLAUDE.md의 "프로젝트 개요" 섹션에서 읽어옴:
- 프로젝트 목적 (`{project_purpose}`)
- 주요 산출물 (`{primary_deliverables}`)
- 대상 독자·고객 (`{audience}`)
- 톤·형식 제약 (`{tone_constraints}`)
- 설치 플러그인 (`{installed_plugins}`)

**충족 조건**: `./CLAUDE.md` 로드 (Cowork 세션 시작 시 자동).
v1.3.0부터 **글로벌 프로필은 사용하지 않는다**. 프로젝트 CLAUDE.md가 유일한 맥락 소스.

---

### B등급 — 핵심 (80% 이상 충족 권장)
산출물별 도메인 맥락. 선택한 스킬(또는 스킬 체인)에 맞춰 **Phase 1 인터뷰 + 필요 시 추가 AskUserQuestion**으로 수집한다.

**질문 생성 규칙 (중요!)**:
```
1. 선택한 스킬(또는 스킬 체인)이 무엇을 만드는지 파악 (산출물 유형)
2. Phase 1 인터뷰 답변과 CLAUDE.md 프로젝트 개요에서 이미 알고 있는 맥락은 재질문하지 않는다
3. 부족한 도메인 맥락만 AskUserQuestion으로 보강
4. 질문 횟수: 필요한 맥락이 부족할 때 자연스럽게 질문. 형식과 횟수는 상황에 맞게 판단.
   (이미 맥락이 충분하면 생략 가능)
```

<!-- "최대 4질문" 하드 리밋 제거: Claude가 상황에 맞게 질문 수를 판단. 과잉 질문도, 무조건 4개 채우기도 불필요. -->

**예시** (산출물 유형별 질문 템플릿):

**카피·콘텐츠 작성 (copywriting)**:
- Q1. 콘텐츠 목적은? → 브랜드 인지 / 리드 생성 / 전환 유도 / 고객 유지
- Q2. 타겟 독자는? → B2B 의사결정자 / B2C 소비자 / 내부 직원 / 투자자
- Q3. 긴급도는? → 즉시 / 1주일 내 / 2주+ / 미정
- Q4. 선호 톤은? → 전문적 / 캐주얼 / 스토리텔링 / 데이터 중심

**시장조사 (market-research)**:
- Q1. 조사 대상은? → 특정 산업명/제품군
- Q2. 조사 목적은? → 신규 진입 / 경쟁 대응 / 투자 판단 / 전략 수립
- Q3. 지리 범위는? → 한국 / 아시아 / 글로벌
- Q4. 초점은? → 시장 규모 / 경쟁사 / 소비자 니즈 / 트렌드

**기술 문서 (technical-writer)**:
- Q1. 문서 유형은? → API 가이드 / 사용자 매뉴얼 / 운영 가이드 / 제품 가이드
- Q2. 타깃 독자는? → 개발자 / 관리자 / 최종 사용자 / 조합
- Q3. 기술 스택은? → 웹 / 모바일 / 클라우드 / 데이터베이스 / 기타
- Q4. 문서 현황은? → 신규 / 기존 개선 / 마이그레이션 / 유지보수

위 3개 세트는 어디까지나 예시 템플릿이다. 실제 질문은 선택한 스킬의 산출물 유형에 맞춰 구성한다.

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
context = (CLAUDE.md "프로젝트 개요") + (Phase 1 인터뷰 답변)
missing_context = A등급 + 필수_B등급 - context

IF missing_context.empty():
  → 즉시 실행 (맥락 충분)
ELSE:
  → 부족분만 AskUserQuestion으로 보강
```

### 2-2. 질문 생성 (AskUserQuestion)
```
# 선택한 스킬(체인)의 산출물 유형에 맞는 도메인 질문 구성
questions = build_domain_questions(selected_skill_chain)

# CLAUDE.md 프로젝트 개요 / Phase 1 답변으로 이미 충족된 질문은 스킵
missing_questions = [q for q in questions if not already_known(q)]

FOR each 질문 in missing_questions:
  options = 질문.options  # 산출물 유형에 맞는 옵션 제시
  user_response = AskUserQuestion(질문.text, options)
  context_store[질문.id] = user_response

# 질문 횟수는 필요한 맥락에 따라 자율 판단 (최소화 지향)
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

산출물 유형별 심화 질문 우선순위:
  - 전략/규제 산출물 (시장조사, 컴플라이언스 등): 동기 탐색 + 전제 확인
  - 콘텐츠 산출물 (카피, 뉴스레터 등): 영향 범위 + 제약 발견
  - 기술 산출물 (기술 문서, 사양서 등): 대안 탐색 + 제약 발견
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
max_rounds = 7회  (산출물 체인 단위)

LOOP for round in 1..7:
  remaining_context = identify_missing_context()
  IF remaining_context.empty():
    break  (충족)

  questions = generate_questions(remaining_context)  # 필요한 만큼만
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
# CLAUDE.md 프로젝트 개요 + 현재 세션에서 이미 수집한 맥락을 우선 재사용
context_cache = load_from_claude_md_and_session()
FOR each deliverable_chain:
  IF context_cache[chain] exists in this session:
    reuse(context_cache[chain])
    skip_collection()
  ELSE:
    collect_context(chain)
```

### 3-3. 피드백 루프
실행 후 평가:
```
evaluation = get_user_feedback_or_auto_eval()
IF evaluation_score >= 8/10:
  → 컨텍스트 충분 (현재 세션 재사용)
ELSE IF evaluation_score >= 5/10:
  → 컨텍스트 부분 적용
ELSE:
  → 컨텍스트 갱신 필요 (재수집 권장)
```

---

## 4. 모호성 감지 규칙

### 4-1. 신호 패턴
```
[신호 1] 다중 선택 (1 이상의 "기타")
[신호 2] 저신뢰도 응답 (예: "음... 잘 모르겠어요")
[신호 3] 상충하는 답변 (예: Q1="매일" vs Q2="월 1회")
[신호 4] 도메인 키워드 부재 (너무 일반적인 답변)
[신호 5] 산출물 목적과 요청 불일치
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

### 5-1. 수집된 맥락의 저장 위치

수집된 맥락은 **Phase 6에서 CLAUDE.md 본문(프로젝트 개요·스킬 체인 섹션)에 기록**되며,
별도의 컨텍스트 파일이나 글로벌 프로필을 만들지 않는다.

- 인터뷰 답변 → CLAUDE.md "프로젝트 개요"에 반영
- 산출물별 스킬 체인 → CLAUDE.md "프로젝트 워크플로우" 섹션에 기록
- 현재 세션 내에서는 context_store에 임시 보관, 세션 종료 후에는 CLAUDE.md가 단일 소스

### 5-2. 메타데이터 추적
```
context_metadata = {
  collected_date: timestamp,
  source: "claude_md" | "user_input" | "document_upload",
  confidence: 0.0 ~ 1.0,
  last_used: timestamp,
  feedback_score: 0 ~ 10,
  interview_depth: "step1_only" | "step1_step2" | "full_step123"
}
```

---

## 6. 컨텍스트 갱신 트리거

다음 경우에 맥락을 갱신한다:
- 사용자가 CLAUDE.md를 직접 수정한 경우
- 새 산출물 유형(스킬 체인)을 추가하는 경우
- 평가 점수 < 5/10
- 사용자가 명시적으로 재수집을 요청한 경우

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
- **캐시 히트율**: 세션 내 맥락 재사용 %
- **심화 인터뷰 깊이**: 평균 심화 질문 수
