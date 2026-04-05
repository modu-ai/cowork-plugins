# MoAI Core Protocol 11개 파일 인덱스

## 개요
MoAI-Cowork v9.0의 핵심 프로토콜 11개 파일이 설계 문서를 기반으로 완성되었습니다.
모든 파일은 한국어로 작성되었으며, 5계층 아키텍처와 Single-Skill Router + Generator 패턴을 반영합니다.

**생성 일자**: 2026-04-04
**버전**: v1.0.0
**총 크기**: 116KB
**총 단어 수**: 10,296 단어

---

## 11개 파일 목록

### 1. router.md — 자연어 → 하네스 매핑 프로토콜
**크기**: 5.0KB | **역할**: 사용자 요청 분석 및 하네스 자동 감지

사용자의 자연어 요청을 분석하여 적절한 하네스를 자동 선택하는 프로토콜.
- 자연어 파싱 (동사, 도메인 키워드, 문맥 신호)
- 의도 분류 알고리즘
- 키워드 매핑 테이블 (9가지 그룹)
- 모호성 해소 로직 (AskUserQuestion 4질문)
- 복합 요청 분기 (순차/병렬/의존)
- 라우팅 결정 트리
- 우선순위 랭킹
- 오류 처리 및 폴백

---

### 2. init-protocol.md — /moai init 전체 플로우
**크기**: 6.8KB | **역할**: 초기화 및 프로필 구축

6개 Phase로 구성된 초기화 프로세스:
- **Phase 0**: 글로벌 프로필 감지 (재사용/수정/신규)
- **Phase 1-A**: 언어 & 기본 프로필 (4질문)
- **Phase 1-B**: 회사/사업자 프로필 (3질문)
- **Phase 2**: 카테고리 선택 (2단계 분기)
- **Phase 3**: 하네스 선택 (multiSelect, 페이지네이션)
- **Phase 4**: 심층 맥락 수집 (하네스별 최대 4질문)
- **Phase 5**: 로캘 현지화 (한국=내장 데이터, 기타=웹검색 기반)
- **Phase 6**: 파일 생성 (모든 설정 저장)

--harness 옵션으로 Phase 2-3 스킵 가능.

---

### 3. context-collector.md — 맥락 수집 프로토콜
**크기**: 6.4KB | **역할**: 효율적 컨텍스트 수집

맥락 충분성 등급 (A/B/C), 모호성 감지, 반복 제한:
- **A등급** (필수): 이름, 언어, 국가, 역할 (프로필에서 즉시)
- **B등급** (핵심 80%): 하네스별 도메인 맥락
- **C등급** (보강): 팀 규모, 트렌드, 고충
- 모호성 감지 신호 5가지
- AskUserQuestion 재질문 전략
- 반복 제한: 하네스당 최대 7라운드
- 캐싱 및 TTL 관리
- 서브에이전트 제약 (AskUserQuestion 금지)

---

### 4. profile-manager.md — 글로벌 프로필 관리
**크기**: 8.3KB | **역할**: 프로필 저장소 및 CRUD

/mnt/.auto-memory/moai-profile.md 중심 프로필 관리:
- **프로필 스키마**: 7개 섹션 (User / Role&Industry / Company / Preferences / Context Depth 등)
- **Company Profile ★**: 사업자번호, 업종코드, 규모, 회계년도 등
- **CRUD 작업**: Create/Read/Update/Delete 상세 프로세스
- **MEMORY.md 인덱스**: 자동 동기화
- **버전 관리 및 백업**: 자동 스냅샷 저장
- **유효성 검증**: 스키마 + 일관성
- **마이그레이션**: 버전 업그레이드 프로세스
- **캐싱 및 최적화**

---

### 5. claudemd-generator.md — CLAUDE.md 생성 프로토콜
**크기**: 8.5KB | **역할**: 개인화된 CLAUDE.md 자동 생성

MoAI의 ID, 원칙, 참조 경로를 정의하는 CLAUDE.md 자동 생성:
- **기본 템플릿**: 헤더 + 아이덴티티 + 행동원칙(4개) + 참조경로 + 부팅프로토콜
- **자동 생성 로직**: 프로필 기반 렌더링
- **다국어 지원**: ko/en/ja/es 템플릿
- **생성 예시**: 한국어 전체 예시 포함
- **하네스별 규칙 참조**: 각 하네스의 규칙 내용
- **검증 및 업데이트**: 생성 후 자동 검증, 재생성 트리거

---

### 6. rules-generator.md — rules/ 파일 생성 프로토콜
**크기**: 9.8KB | **역할**: 행동 규칙 자동 생성

.claude/rules/ 디렉토리의 규칙 파일들 자동 생성:
- **00-moai-core.md**: MoAI 기본 규칙 10개 항목 (항상 로드)
- **01-{harness-id}.md**: 선택된 각 하네스별 전문화 규칙
- **02-locale-{country}.md**: 현지 규제/문화 규칙 (필요시)
- **README.md**: 규칙 설명서
- **생성 로직**: 템플릿 기반 자동 렌더링
- **검증 및 갱신**: 규칙 파일 유효성, 재생성 트리거

---

### 7. evolution-protocol.md — 자기학습 진화 프로토콜
**크기**: 8.6KB | **역할**: 지속적 학습 및 개선

Self-Refine 사이클을 통한 자동 진화:
- **5단계 프로세스**: 반성 → 피드백 → 패턴 발견 → 규칙 업데이트 → 교차 도메인 학습
- **진화 로그**: self-refine-log.md (매 사이클 기록), rule-updates.md (규칙 변경), pattern-database.md (패턴)
- **롤백 메커니즘**: 조건기반 자동 롤백, 이력 관리
- **학습 속도 제어**: 극복보기 관리, 과도한 학습 방지
- **메트릭 추적**: feedback_score, completion_time, quality_score 등
- **대시보드**: 진화 진행 상황 시각화

---

### 8. execution-protocol.md — 하네스 실행 프로토콜
**크기**: 7.2KB | **역할**: 하네스 실행 및 산출물 생성

하네스 선택부터 산출물 생성까지의 전체 프로세스:
- **실행 전 준비**: 하네스 레퍼런스 로드 → 페르소나 채택
- **워크플로우 실행**: 하네스별 단계별 프로세스 (copywriting, sop-writer 예시)
- **산출물 생성**: .moai/projects/{id}/ 구조, 메타데이터 저장
- **공유**: computer:// 링크, 내보내기 옵션 (PDF/DOCX/HTML)
- **반성 수행**: 자동 평가 + 사용자 피드백 수집
- **실행 경로**: Quick/Interactive/Batch 모드
- **성능 최적화**: 캐싱, 병렬 처리

---

### 9. evaluation-protocol.md — 평가 프로토콜
**크기**: 7.5KB | **역할**: 산출물 품질 평가

5개 차원의 체계적 평가:
- **정확성** (20%): 사실/데이터 정확도 + 신뢰성 검증
- **완전성** (25%): 요구사항 충족도 + 깊이 평가
- **실용성** (25%): 실행 가능성 + 맥락 반영도
- **톤 적합성** (15%): 사용자 톤 일치도
- **현지화** (15%): 로케일 적합성
- **등급 매핑**: S(95-100) / A(85-94) / B(75-84) / C(65-74) / D(0-64)
- **자동 평가 엔진**: 각 차원별 점수 계산
- **개선 제안**: 자동 생성
- **피드백 루프**: 사용자 평가와 자동 평가 비교

---

### 10. diagnostic-protocol.md — 진단 프로토콜
**크기**: 8.2KB | **역할**: 환경 상태 진단 및 모니터링

/moai doctor와 /moai status 명령어:
- **/moai doctor**: 6단계 환경 체크
  - Phase 1: 파일 시스템 검사
  - Phase 2: 글로벌 프로필 검사
  - Phase 3: 하네스 설치 상태
  - Phase 4: 규칙 파일 검사
  - Phase 5: 진화 상태
  - Phase 6: auto-memory 접근
- **/moai status**: 간단한 현황 요약
- **건강 점수**: Health Score (95-100 HEALTHY ~ 0-59 CRITICAL)
- **성능 메트릭**: 응답속도, 캐시 히트율, 평가 평균 등
- **재설정 및 복구**: 부분/전체 초기화, 백업 복원
- **로깅 및 디버깅**: 로그 조회, DEBUG 모드

---

### 11. localization-protocol.md — 로케일 현지화 프로토콜
**크기**: 10KB | **역할**: 지역화 및 규제 적용

전세계 로케일 지원 (한국 내장 + 웹검색 동적 수집):
- **로케일 결정 흐름**: 한국(KR)=내장 데이터, 기타 전세계=웹검색 기반 실시간 수집
- **로케일 구성**: country, language, timezone, currency, date_format, number_format 등
- **웹검색 5개 카테고리**: 세법, 노동법, 데이터보호법, 비즈니스 관행, 형식 표준
- **하네스 실행 시 적용**: 화폐/날짜 표기, 법적 고지, 비즈니스 톤 현지화
- **규제 민감 하네스**: contract-review, accounting-tax, labor-hr 등 필수 참조
- **페르소나 적응**: 국가별 호칭 및 톤 자동 조정
- **Graceful Degradation**: 웹검색 실패 시 사용자 직접 입력, 한국은 오프라인 동작

---

## 설계 핵심 반영 사항

### 1. AskUserQuestion 제약 준수
- 1-4질문/호출 (최대 4질문)
- 2-4옵션/질문 (기본 4옵션, 필요시 3옵션)
- header 12자 이내 (예: "언어설정", "지역설정")
- "Other" 자동 추가

### 2. 5계층 아키텍처 구현
```
auto-memory (/mnt/.auto-memory/moai-profile.md)
    ↕ (profile-manager, context-collector)
플러그인 (skills/moai/references/core/)
    ↕ (router, init-protocol, rules-generator)
.claude/ (CLAUDE.md + rules/)
    ↕ (claudemd-generator, rules-generator)
.moai/ (프로젝트, 진화, 로케일)
    ↕ (execution-protocol, evolution-protocol, localization-protocol)
auto-memory 학습
```

### 3. Single-Skill Router + Generator 패턴
- **Router** (router.md): 요청 분석 및 하네스 감지
- **Generator** (규칙 + 프로토콜): 개인화된 산출물 생성
- **Self-Refine** (evolution-protocol): 자동 학습 및 개선

### 4. 서브에이전트 제약 준수
- AskUserQuestion 사용 금지 (부모가 처리)
- 부모 컨텍스트 참조만 허용
- 부모에게 컨텍스트 재수집 요청

### 5. 한국어 작성
- 모든 11개 파일 100% 한국어
- 변수/함수명은 영문 (기술 표준)
- 설명/예시는 한국어 또는 한영혼용

---

## 파일 간 의존성 관계

```
router.md
  ↓
init-protocol.md
  ↓
profile-manager.md
  ↓
context-collector.md
  ↓
claudemd-generator.md + rules-generator.md
  ↓
execution-protocol.md
  ↓
evaluation-protocol.md + evolution-protocol.md
  ↓
diagnostic-protocol.md
  
(병렬) localization-protocol.md (모든 프로토콜과 연동)
```

---

## 사용 시나리오

### 시나리오 1: 초기 사용자
1. **router.md** 읽고 요청 해석
2. **init-protocol.md** 실행 (Phase 0-6)
3. **profile-manager.md** 프로필 저장
4. **context-collector.md** 컨텍스트 수집
5. **execution-protocol.md** 첫 하네스 실행
6. **evaluation-protocol.md** 결과 평가
7. **evolution-protocol.md** 학습

### 시나리오 2: 기존 사용자 (새 하네스)
1. **router.md** 요청 분석
2. **init-protocol.md** Phase 3 (하네스 추가)
3. **context-collector.md** 새 하네스 컨텍스트
4. **rules-generator.md** 01-{new_harness}.md 생성
5. **execution-protocol.md** 하네스 실행

### 시나리오 3: 환경 점검
1. **diagnostic-protocol.md** /moai doctor 실행
2. 문제 발견 시 해당 프로토콜 참조
3. **profile-manager.md** 프로필 업데이트
4. **rules-generator.md** 규칙 재생성

### 시나리오 4: 국제화
1. **localization-protocol.md** 로케일 감지
2. **profile-manager.md** 국가정보 저장
3. **rules-generator.md** 02-locale-{country}.md 생성
4. **execution-protocol.md** 현지화된 실행

---

## 향후 확장 포인트

1. **하네스 추가**: init-protocol Phase 3, rules-generator 템플릿
2. **새 로케일 추가**: localization-protocol 참조, rules-generator 02-locale
3. **평가 개선**: evaluation-protocol 차원 추가
4. **자동화 고도화**: execution-protocol Batch 모드 확장
5. **AI 기반 진화**: evolution-protocol Self-Refine 고도화

---

## 버전 정보

- **문서 버전**: 1.0.0
- **MoAI 버전**: 0.1.0 (초기)
- **Cowork 플러그인**: v9.0
- **생성일**: 2026-04-04
- **언어**: 한국어 100%
- **총 크기**: 116KB (11개 파일)
- **총 단어수**: 10,296 단어

---

## 문서 수정 이력

| 날짜 | 변경 내용 |
|------|----------|
| 2026-04-05 | 전체 파일 감사: placeholder 하네스명 → 실제 harness-100 ID로 교체, `/moai install` 고스트 커맨드 제거, 하네스 레퍼런스 경로 수정, localization-protocol 설명 갱신 (전세계 웹검색 기반) |

---

## 문의 및 피드백

각 파일의 내용에 대한 구체적인 질문은 해당 파일을 참조하세요.
전체 아키텍처에 대한 질문은 설계 문서(MoAI-Cowork v9.0 설계)를 참조하세요.

