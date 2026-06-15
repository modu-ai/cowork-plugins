# diagnostic-protocol.md — 진단 프로토콜

## 개요
cowork 플러그인 환경과 프로젝트 설정 상태를 진단하고 문제를 식별하는 프로토콜입니다.
`/project doctor`와 `/project status` 명령어로 실행됩니다.

> `/project init`은 더 이상 별도 동작이 아니며, 맨 명령 `/project`(초기화 기본 동작)의 **레거시 별칭**입니다.

---

## 1. /project doctor — 환경 체크

### 1-1. 진단 구성

```
/project doctor
```

### 1-2. 체크리스트

```
┌─ cowork 플러그인 환경 진단 ──────────────────────┐
│
│ [Phase 1] 파일 시스템 검사
│ ├─ ./CLAUDE.md 존재: ✓
│ ├─ .moai/ 디렉토리: ✓
│ ├─ .moai/credentials.env: ✓ (프로젝트 격리)
│ ├─ skills/project/references/: ✓ (core + templates 포함)
│ └─ 27개 플러그인 / 173 스킬 설치 상태: ✓
│
│ [Phase 2] 프로젝트 CLAUDE.md 검사
│ ├─ CLAUDE.md 라인 수: 178 / 200 (한도 내 ✓)
│ ├─ HARD 규칙 포함(office 우선): ✓
│ ├─ HARD 규칙 포함(ai-slop 후처리): ✓
│ ├─ 스킬 체인 블록 포함: ✓ (6개 체인)
│ └─ 레거시 전역 변수 흔적: 없음 ✓
│   (v1.3.0에서 글로벌 프로필 시스템 제거됨)
│
│ [Phase 3] 설치 플러그인 + 스킬 체인 상태
│ ├─ moai-core: ✓ (project, ai-slop-reviewer, feedback)
│ ├─ 화이트리스트 대조: 27개 플러그인 일치 ✓
│ ├─ 설계된 스킬 체인: 6개
│ └─ ai-slop-reviewer 체인 말미 포함율: 100%
│
│ [Phase 4] API 키 / 커넥터 상태
│ ├─ .moai/credentials.env 로드: ✓
│ ├─ MCP 커넥터 등록: higgsfield ✓ / elevenlabs ✓
│ └─ 누락 키: 0개
│
│ [Phase 5] 시스템 지침 검사
│ ├─ ./CLAUDE.md 로드: ✓
│ └─ 에이전트 오케스트레이터 모델 활성: ✓
│
│ ═════════════════════════════════════════════
│ 전체 진단: ✓ HEALTHY (건강함)
│ 조치 필요: 0개
│ ═════════════════════════════════════════════
└─────────────────────────────────────────────────┘
```

### 1-3. 진단 항목별 상세

**파일 시스템 검사**
```
FOR each critical_file in [
  ./CLAUDE.md,
  .moai/config.json
]:
  IF file.exists AND file.size > 0:
    status = "✓"
  ELSE:
    status = "✗"
    remediation = suggest_fix()
```

**CLAUDE.md 유효성**
```
- "프로젝트 개요" 섹션 존재 여부
- HARD 규칙(office 우선 / ai-slop 후처리) 포함 여부
- "프로젝트 워크플로우" 스킬 체인 블록 존재 여부
- 라인 수 한도(200) 준수 여부

completeness_score = (충족_항목 / 전체_항목) * 100
```

**플러그인 인벤토리 검사 (27 화이트리스트)**
```
installed = scan_installed_plugins()
FOR each plugin in installed:
  IF plugin in WHITELIST_27:
    check_plugin_json()       # plugin.json 유효성·버전
    check_skills_present()    # skills/*/SKILL.md 존재
  ELSE:
    warn("화이트리스트 밖 플러그인: " + plugin)
```

**스킬 체인 정의 유효성**
```
FOR each chain in CLAUDE.md "프로젝트 워크플로우":
  validate_skill_names()      # 각 스킬이 설치된 플러그인에 실재하는지
  check_aislop_tail()         # 텍스트 산출물 체인 말미에 ai-slop-reviewer 포함
```

---

## 2. /project status — 현황 요약

### 2-1. 간단한 상태 확인

```
/project status
```

### 2-2. 출력 예시

```
프로젝트 현황
═════════════════════════════════════════════════

프로젝트:
  CLAUDE.md: ✓ (프로젝트 개요 + 워크플로우 포함)
  스킬 체인: 6개 설계됨

설치된 플러그인 (27개 중):
  ✓ moai-core (project, ai-slop-reviewer, feedback ...)
  ✓ moai-content (copywriting, landing-page ...)
  ✓ moai-office (docx-generator, pptx-designer ...)
  ... (총 27 플러그인 / 173 스킬)

API 키 / 커넥터:
  ✓ higgsfield (이미지·영상)
  ✓ elevenlabs (음성)
  누락: 0개

다음 권장 조치:
  1. 없음 — 환경 정상

═════════════════════════════════════════════════
```

### 2-3. 상세 보기 옵션

```
/project status --detailed
/project status --plugins
/project status --export=json
```

---

## 3. 문제 감지 및 진단

### 3-1. 자동 감지 규칙

```
IF CLAUDE.md_없음 OR "프로젝트 개요"_섹션_부재:
  ERROR: "프로젝트가 초기화되지 않았습니다. /project 실행 필요"

IF 설치_플러그인 == 0:
  ERROR: "설치된 cowork 플러그인이 없습니다. 마켓플레이스 설치 필요"

IF 화이트리스트_밖_플러그인_감지:
  WARNING: "27 화이트리스트 밖 플러그인이 있습니다. /project catalog 확인"

IF 스킬_체인_내_미설치_스킬_참조:
  WARNING: "스킬 체인이 미설치 스킬을 참조합니다. /project catalog 확인"

IF 커넥터_API_키_누락:
  INFO: "일부 커넥터 키가 없습니다. /project apikey 로 등록"

IF CLAUDE.md_로드_실패:
  ERROR: "시스템 지침 로드 실패. ./CLAUDE.md 확인 필요"
```

### 3-2. 진단 레포트 생성

```
/project doctor --report

출력:
doctor-report-YYYY-MM-DD-HHMM.md 생성됨
├── 진단 결과 요약
├── 발견된 문제 목록
├── 각 문제별 해결 방안
└── 권장 조치 우선순위
```

---

## 4. 진단 메트릭

### 4-1. 추적 메트릭

```
진단 대시보드:

환경 상태:
  └─ CLAUDE.md 유효성: ✓
  └─ 플러그인 인벤토리: 27/27 일치 ✓

설정 상태:
  └─ 스킬 체인 유효성: 6/6 ✓
  └─ 커넥터 키 완비율: 100% (목표: 100%) ✓

안정성:
  └─ 미설치 스킬 참조: 0개 (목표: 0) ✓
  └─ 화이트리스트 밖 플러그인: 0개 (목표: 0) ✓
```

---

## 5. 재설정 및 복구

### 5-1. 부분 재설정

```
# CLAUDE.md만 재생성 (스킬 체인 재설계)
/project

# 커넥터 키만 재등록
/project apikey
```

### 5-2. 전체 재설정

```
# CLAUDE.md를 처음부터 다시 작성 (Phase 1 인터뷰 재실행)
/project

주의: 기존 CLAUDE.md 본문이 갱신됩니다.

초기화 후:
1. Phase 1 인터뷰 응답
2. 스킬 체인 재설계
3. CLAUDE.md 본문 재작성
```

---

## 6. 로깅 및 디버깅

### 6-1. 디버그 모드

```
/project --debug {command}

출력:
[DEBUG] CLAUDE.md 로드 중...
[DEBUG] 플러그인 인벤토리 스캔 중...
[DEBUG] 스킬 체인 정의 검증 중...
[DEBUG] 커넥터 키 점검 중...
...
```

---

## 7. 건강 점수

### 7-1. 계산 방식

```
Health Score = Σ(component_score × weight)

Components:
  CLAUDE.md 유효성: 30% × (충족_항목 / 전체_항목)
  플러그인 인벤토리: 25% × (일치_플러그인 / 27)
  스킬 체인 유효성: 25% × (유효_체인 / 전체_체인)
  커넥터 키 완비: 20% × (등록_키 / 필요_키)

예:
  CLAUDE.md:   100 × 0.30 = 30.0
  플러그인:    100 × 0.25 = 25.0
  스킬 체인:   100 × 0.25 = 25.0
  커넥터:      100 × 0.20 = 20.0
  ────────────────────────
  Health Score = 100 (HEALTHY)
```

### 7-2. 상태 레벨

```
95-100: ✓ HEALTHY (건강함)
80-94: ⚠ CAUTION (주의)
60-79: ⚠ WARNING (경고)
0-59: ✗ CRITICAL (심각)
```
