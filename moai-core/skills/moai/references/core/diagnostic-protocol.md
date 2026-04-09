# diagnostic-protocol.md — 진단 프로토콜

## 개요
MoAI 환경과 프로필 상태를 진단하고 문제를 식별하는 프로토콜입니다.
/moai doctor와 /moai status 명령어로 실행됩니다.

---

## 1. /moai doctor — 환경 체크

### 1-1. 진단 구성

```bash
/moai doctor
```

### 1-2. 체크리스트

```
┌─ MoAI 환경 진단 (v0.2.0) ────────────────────────┐
│
│ [Phase 1] 파일 시스템 검사
│ ├─ .claude/CLAUDE.md 존재: ✓
│ ├─ .moai/ 디렉토리: ✓
│ ├─ skills/moai/references/: ✓ (core 포함)
│ └─ skills/moai/references/skills/: ✓ (84개 스킬)
│
│ [Phase 2] 글로벌 프로필 검사
│ ├─ /mnt/.auto-memory/moai-profile.md: ✓
│ ├─ 프로필 유효성: ✓ (schema v1.0 호환)
│ ├─ 필수 필드 완성도: 100% (A등급)
│ ├─ 권장 필드 완성도: 85% (B등급)
│ └─ 마지막 업데이트: 2026-04-04 (신선함)
│
│ [Phase 3] 하네스 설치 상태
│ ├─ copywriting: ✓ (설치됨)
│ ├─ email-crafter: ✓ (설치됨)
│ ├─ sop-writer: ✗ (미설치)
│ │  └─ 설치 권장: /moai init --harness=sop-writer
│ └─ 설치된 하네스: 2/84
│
│ [Phase 4] 시스템 지침 검사
│ ├─ .claude/CLAUDE.md 로드: ✓
│ ├─ v0.2.0 아키텍처 적용: ✓
│ └─ 에이전트 디렉터 모델 활성: ✓
│
│ [Phase 5] 진화 상태
│ ├─ evolution 로그: ✓ (4개 기록)
│ ├─ 마지막 자기학습: 2026-04-04 10:30
│ ├─ 평가 평균: 8.2/10
│ ├─ 활성 패턴: 3개
│ └─ 권장사항: 규칙 강화 필요 없음
│
│ [Phase 6] auto-memory 접근
│ ├─ MEMORY.md 접근: ✓
│ ├─ 인덱스 동기화: ✓
│ └─ 백업 상태: ✓ (최근 백업: 2026-04-04)
│
│ ═════════════════════════════════════════════
│ 전체 진단: ✓ HEALTHY (건강함)
│ 조치 필요: 1개 (sop-writer 설치)
│ 성능: 96%
│ ═════════════════════════════════════════════
└─────────────────────────────────────────────────┘
```

### 1-3. 진단 항목별 상세

**파일 시스템 검사**
```
FOR each critical_file in [
  .claude/CLAUDE.md,
  .claude/rules/00-moai-core.md,
  .moai/evolution/self-refine-log.md
]:
  IF file.exists AND file.size > 0:
    status = "✓"
  ELSE:
    status = "✗"
    remediation = suggest_fix()
```

**프로필 유효성**
```
schema_validation(moai_profile.yaml)
  → required fields check
  → data type validation
  → enum values validation
  → consistency check (country vs company_country)
  
completeness_score = (filled_fields / total_fields) * 100
```

**하네스 상태**
```
FOR each harness in installed_harnesses:
  check_reference_files()
  check_context_file()
  check_rule_file()
  validate_config()
```

---

## 2. /moai status — 현황 요약

### 2-1. 간단한 상태 확인

```bash
/moai status
```

### 2-2. 출력 예시

```
MoAI 현황 ({user_name})
═════════════════════════════════════════════════

프로필:
  이름: {user_name}
  역할: {user_role}
  회사: {company_name}
  국가: 한국 (KRW)
  프로필 완성도: 95% (A+)

설치된 하네스 (84개 중):
  ✓ copywriting (마지막 사용: 2026-04-04 10:30)
  ✓ email-crafter (마지막 사용: 2026-04-02 14:15)
  ○ sop-writer (미설치, 추천됨)

진화 상태:
  총 작업 수: 12개
  평가 평균: 8.2/10
  지난 주 개선율: +5%
  활성 규칙 개선안: 2개

컨텍스트:
  수집 라운드: 3회
  충분성 등급: 85% (B등급)
  마지막 갱신: 2026-04-04 09:00
  컨텍스트 신선도: 양호

다음 권장 조치:
  1. sop-writer 설치
  2. 월간 프로필 검토 (2026-04-11 예정)

═════════════════════════════════════════════════
```

### 2-3. 상세 보기 옵션

```bash
/moai status --detailed
/moai status --harness=copywriting
/moai status --evolution
/moai status --export=json
```

---

## 3. 문제 감지 및 진단

### 3-1. 자동 감지 규칙

```
IF 프로필_완성도 < 60%:
  WARNING: "프로필이 불완전합니다. /moai init --reset 권장"

IF 하네스_설치 == 0:
  ERROR: "설치된 하네스가 없습니다. /moai init 실행 필요"

IF evolution_평가_평균 < 5:
  WARNING: "평가가 낮습니다. /moai evolution --suggest 확인"

IF 컨텍스트_TTL > 30days:
  INFO: "컨텍스트 갱신 시간입니다. /moai refresh-context 권장"

IF CLAUDE.md_로드_실패:
  ERROR: "시스템 지침 로드 실패. .claude/CLAUDE.md 확인 필요"
```

### 3-2. 진단 레포트 생성

```bash
/moai doctor --report

출력:
doctor-report-2026-04-04-1030.md 생성됨
├── 진단 결과 요약
├── 발견된 문제 5개
├── 각 문제별 해결 방안
├── 성능 메트릭
└── 권장 조치 우선순위
```

---

## 4. 성능 메트릭

### 4-1. 추적 메트릭

```
성능 대시보드:

시스템 성능:
  └─ 응답 속도: 1.2초 (목표: < 2초) ✓
  └─ 캐시 히트율: 78% (목표: > 70%) ✓

작업 성능:
  └─ 평균 평가: 8.2/10 (목표: > 7.5) ✓
  └─ 완료율: 100% (목표: > 95%) ✓

학습 성능:
  └─ 규칙 개선: 12회 (월간)
  └─ 롤백율: 8% (목표: < 10%) ✓

안정성:
  └─ 에러율: 2% (목표: < 5%) ✓
  └─ 평균 운영시간: 99.8% (목표: > 99%) ✓
```

### 4-2. 트렌드 분석

```bash
/moai status --trend=30days

출력:
평가 점수 추이 (최근 30일):
│
8.5│                    ●
8.0│          ●    ●    ●    ●
7.5│    ●    ●    ●    ●    ●
7.0│         
6.5│
────┴─────────────────────────
   1주   2주   3주   4주
   
트렌드: ↑ 상향 (+0.5점)
```

---

## 5. 재설정 및 복구

### 5-1. 부분 재설정

```bash
# 프로필만 초기화
/moai profile --reset

# 규칙만 초기화 (프로필은 유지)
/moai rules --reset

# 하네스 컨텍스트만 초기화
/moai context --reset
```

### 5-2. 전체 재설정

```bash
/moai reset --confirm

주의: 모든 진화 기록이 삭제됩니다.
백업이 자동 생성됩니다: .moai/backups/reset-2026-04-04/

초기화 후:
1. /moai init 재실행
2. 하네스 재설치
3. 컨텍스트 재수집
```

### 5-3. 복구

```bash
# 특정 시점으로 복구
/moai restore --backup=2026-04-01

# 백업 목록 조회
/moai backups --list

출력:
Available backups:
  1. 2026-04-04_reset (Latest)
  2. 2026-04-03_auto
  3. 2026-04-02_auto
  4. 2026-04-01_auto
```

---

## 6. 로깅 및 디버깅

### 6-1. 로그 조회

```bash
/moai logs --level=ERROR
/moai logs --harness=copywriting
/moai logs --after=2026-04-04T09:00:00+09:00
```

### 6-2. 디버그 모드

```bash
/moai --debug {command}

출력:
[DEBUG] 프로필 로드 중...
[DEBUG] 규칙 파일 검증 중...
[DEBUG] 하네스 context 로드 중...
[DEBUG] router 실행 중...
...
```

---

## 7. 건강 점수

### 7-1. 계산 방식

```
Health Score = Σ(component_score × weight)

Components:
  프로필 완성도: 20% × (현재/목표)
  하네스 상태: 25% × (설치수/권장수)
  진화 상태: 20% × (평가_평균 / 10)
  규칙 유효성: 15% × (유효_규칙수 / 전체_규칙수)
  시스템 안정성: 20% × (가용성 / 100)

예:
  프로필: 95 × 0.20 = 19.0
  하네스: 80 × 0.25 = 20.0
  진화: 82 × 0.20 = 16.4
  규칙: 100 × 0.15 = 15.0
  안정성: 99.8 × 0.20 = 19.96
  ────────────────────────
  Health Score = 90.36 (HEALTHY)
```

### 7-2. 상태 레벨

```
95-100: ✓ HEALTHY (건강함)
80-94: ⚠ CAUTION (주의)
60-79: ⚠ WARNING (경고)
0-59: ✗ CRITICAL (심각)
```

