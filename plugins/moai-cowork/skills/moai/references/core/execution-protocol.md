# execution-protocol.md — 하네스 실행 프로토콜

## 개요
선택된 하네스를 실행하기 전의 준비부터 산출물 생성, 반성까지의 전체 프로세스를 정의합니다.

---

## 1. 실행 전 준비 (Pre-Execution)

### 1-1. 하네스 레퍼런스 로딩
```
Phase 1: 하네스 식별
  → 사용자 요청 또는 /moai {harness-id} 명령어
  → router.md에서 적절한 하네스 확인

Phase 2: 하네스 레퍼런스 로드
  references/harness-100/{lang}/{harness-id}.md
  → lang = 사용자 언어 (ko, en)
  → 하네스 정의: 페르소나, 워크플로우, 출력형식, 반성기준

Phase 3: 규칙 로드
  .claude/rules/
  ├── 00-moai-core.md (필수)
  ├── 01-{harness-id}.md (해당 하네스)
  └── 02-locale-{country}.md (필요시)

Phase 4: 컨텍스트 로드
  .moai/harness-contexts/
  └── {harness-id}.md
  
  IF 컨텍스트 없음:
    → context-collector.md 실행 (최대 4질문)
```

### 1-2. 복잡도 판단 및 Sequential Thinking
```
Phase 4 이후, 하네스 실행 전 복잡도를 판단한다:

IF 다음 조건 중 하나 이상 충족:
  - 복합 요청 (2개 이상 하네스 관련)
  - 다중 조건 분석 필요 (규제, 법률, 세무 등)
  - 의존적 실행 (Phase A 결과가 Phase B 입력)
  - 전략적 판단 필요 (비즈니스 의사결정, 투자 분석 등)

THEN:
  → mcp__sequential-thinking__sequentialthinking 호출
  → 요청을 단계별로 분해
  → 각 단계의 입력/출력 정의
  → 실행 순서 및 의존성 확인
  → 구조화된 계획을 기반으로 하네스 실행 진입

ELSE:
  → 바로 페르소나 채택 단계로 진행
```

### 1-3. 페르소나 채택
```
사용자 프로필에서 페르소나 정보 추출:
- 이름, 역할, 회사
- 선호 톤, 언어, 로케일
- 하네스별 특화 컨텍스트

MoAI 시스템 메시지에 주입:
"당신은 {user_name}님의 {harness_name}입니다.
 역할: {user_role}
 톤: {tone}
 언어: {language}
 현재 작업: {task_description}"
```

### 1-4. 소크라테스식 전제 검증 (규제/전략 하네스)

규제·법률·전략 하네스 실행 시, 사용자의 전제가 산출물 품질에 직접 영향을 미친다.
잘못된 전제에 기반한 산출물은 위험하므로, 실행 전 열린 질문으로 전제를 검증한다.

```
대상 하네스 (전제 검증 필수):
  compliance, contract-review, regulatory, accounting-tax,
  finance-compliance, tax-optimization, labor-hr, ip-strategy,
  risk-register, data-privacy, corporate-governance,
  market-entry-strategy, pricing-strategy, investor-report

검증 질문 패턴 (텍스트 대화, 최대 2개):

  [전제 확인]  "이 판단의 근거가 되는 핵심 전제는 무엇인가요?"
  [반대 검증]  "반대 사례나 예외 상황은 어떤 게 있을까요?"
  [범위 확인]  "이 결과가 적용되는 범위(시간/지역/대상)는 어디까지인가요?"
  [리스크 인식] "이 방향으로 진행했을 때 가장 우려되는 점은 무엇인가요?"

적용 규칙:
  - 위 대상 하네스에만 적용 (다른 하네스는 스킵)
  - 사용자가 명확한 지시를 이미 제공한 경우 스킵
  - 검증 결과를 산출물 서두 "전제 조건" 섹션에 명시
  - Sequential Thinking과 병행 가능 (복잡도 높을 시)
```

---

## 2. 워크플로우 실행

### 2-1. 하네스별 워크플로우 예시

**copywriting 예**
```
입력: 주제, 길이, 톤, 타겟 독자

Step 1: 아웃라인 생성
  → 제목 + 3-4개 섹션 제목

Step 2: 각 섹션 작성
  → 500-750자/섹션

Step 3: SEO 최적화
  → 메타 디스크립션
  → 키워드 배치

Step 4: 검수
  → 문법, 사실 검증
  → 톤 일관성 확인

출력: 마크다운 파일
```

**sop-writer 예**
```
입력: 프로세스 설명, 대상 업무, 담당자

Step 1: 현 상태(AS-IS) 분석
  → 단계별 현황
  → 소요 시간
  → 병목 지점

Step 2: 목표 상태(TO-BE) 설계
  → 표준화 대상 확인
  → 도구/시스템 선택
  → 예상 효율 계산

Step 3: SOP 문서 작성
  → 단계별 절차서
  → 체크리스트
  → 예외 처리 가이드

Step 4: 검증 및 배포 계획
  → KPI 정의
  → 교육 자료
  → 피드백 수집 절차

출력: SOP 문서 + 체크리스트
```

### 2-2. 에러 처리
```
IF 실행_중_오류:
  1. 오류 유형 식별
  2. 사용자에게 명시적 보고
  3. 대안 제시
  4. 롤백 또는 재시도
  
예:
"죄송합니다. API 호출 실패(404 Not Found)
 대안: [1] 다른 도구 사용 [2] 수동 설정 [3] 취소"
```

---

## 3. 산출물 생성

### 3-1. 저장 구조
```
.moai/
└── projects/
    └── {project-id}/
        ├── metadata.yaml (프로젝트 정보)
        ├── inputs.md (사용자 입력)
        ├── outputs/
        │   ├── content/
        │   │   └── generated_content.md
        │   ├── automation/
        │   │   └── automation_config.md
        │   └── ...
        └── evaluation/
            ├── self-eval.md
            └── user-feedback.md
```

### 3-2. 메타데이터
```yaml
# metadata.yaml
project_id: "proj-2026-04-04-001"
harness: "copywriting"
created_at: "2026-04-04T10:30:00+09:00"
user: "{user_name}"
title: "디지털 마케팅 트렌드 2026"
status: "completed"
duration_minutes: 12
output_files:
  - generated_content.md
  - seo_metadata.md
```

### 3-3. 파일 포맷
```
모든 산출물: UTF-8, LF, 마크다운/YAML/JSON

예시 산출물:
outputs/
├── {harness_id}_{date}_{slug}.md
├── {harness_id}_{date}_{slug}.json (데이터)
└── {harness_id}_{date}_{slug}.yaml (메타데이터)
```

---

## 4. 산출물 공유

### 4-1. computer:// 링크
```
생성된 파일을 사용자가 접근할 수 있도록 링크 제공:

"결과물이 준비되었습니다:
computer:///.moai/projects/proj-2026-04-04-001/outputs/copywriting_2026-04-04_digital-marketing-trends.md

[컴퓨터에서 열기] [수정하기] [공유하기]"
```

### 4-2. 내보내기 옵션
```
/moai export --project=proj-2026-04-04-001 --format=pdf
/moai export --project=proj-2026-04-04-001 --format=docx
/moai export --project=proj-2026-04-04-001 --format=html
```

---

## 5. 반성 수행 (Post-Execution)

### 5-1. 자동 반성
```
작업 완료 직후:

1. 결과물 검토
   - 길이, 형식, 문법 확인
   - 가이드라인 준수 확인
   - 완성도 자체 평가 (0~100%)

2. 프로세스 평가
   - 소요 시간 (목표 대비)
   - 컨텍스트 충분도
   - 문제 발생 여부

3. 예상 vs 실제
   - 사용자 기대치 충족도 예상
   - 예상 오류 가능성
   - 개선 포인트

4. 자동 평가 점수
   - 완성도 (0~100%)
   - 관련성 (0~100%)
   - 실용성 (0~100%)
```

### 5-2. 반성 기록
```markdown
# .moai/projects/{project-id}/evaluation/self-eval.md

## 자동 평가

### 완성도 점수: 88/100
- 요구사항 충족: 95%
- 형식 준수: 90%
- 내용 깊이: 80%

### 문제점
- [ ] 문법/스펠링 오류
- [ ] 사실 오류 (검증 필요)
- [x] 컨텍스트 부족 (귀사 사례 1개 추가 권장)
- [ ] 시간 초과

### 개선안
1. 귀사 사례 2가지 추가하면 80 → 92점
2. 실행 아이템별 예상 비용 추가하면 +5점
3. 타겟 독자별 커스터마이징 옵션 제시하면 +3점
```

### 5-3. 피드백 수집
```
사용자에게 평가 요청:

"결과물이 도움이 되셨나요?
 [1⭐⭐⭐⭐⭐] [2⭐⭐⭐⭐] [3⭐⭐⭐] [4⭐⭐] [5⭐]
 
 추가 의견이 있으시면:"
 
 [입력창]"

피드백 저장: .moai/projects/{project-id}/evaluation/user-feedback.md
```

---

## 6. 실행 경로 선택

### 6-1. 빠른 실행 (Quick Mode)
```
/moai {harness-id} --quick

조건:
- 컨텍스트 완전 (A+B등급)
- 사용자가 명시적으로 요청

프로세스:
- 반성/피드백 수집 스킵
- 즉시 산출물 제공
- 나중에 평가 수집 가능
```

### 6-2. 대화형 실행 (Interactive Mode, 기본)
```
/moai {harness-id}

프로세스:
- 부족한 컨텍스트 수집
- 워크플로우 단계마다 확인 기회
- 반성 자동 수행
- 피드백 즉시 수집
```

### 6-3. 배치 실행 (Batch Mode)
```
/moai batch
config: {
  harnesses: [copywriting, email-crafter],
  projects: [proj_001, proj_002],
  schedule: "2026-04-05T09:00:00+09:00"
}

결과:
- 모든 프로젝트 동시 처리
- 개별 평가 기록
- 통합 대시보드 생성
```

---

## 7. 성능 최적화

### 7-1. 캐싱
```
반복 요청 최적화:
- 템플릿 캐싱 (하네스별 1회만 로드)
- 규칙 캐싱 (프로필 변경까지 유지)
- 컨텍스트 캐싱 (TTL = 30일)
```

### 7-2. 병렬 처리
```
다중 하네스 동시 실행:
/moai batch --parallel=3
→ 최대 3개 하네스 동시 실행
→ 전체 시간 단축
```

---

## 8. 모니터링 및 로깅

### 8-1. 실행 로그
```
.moai/logs/
├── execution-{date}.log
└── errors-{date}.log

로깅 레벨:
- INFO: 실행 시작/완료
- WARNING: 컨텍스트 부족, 시간 초과
- ERROR: 치명적 오류
- DEBUG: 단계별 상세 정보
```

### 8-2. 성능 메트릭
```
추적 항목:
- 평균 소요 시간 (하네스별)
- 평가 점수 추이
- 오류 빈도
- 캐시 히트율
```

