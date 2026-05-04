---
title: "제품 개발 트랙"
weight: 70
description: "PRD · 로드맵 · UX 자동화 — strategy-planner → startup-launchpad → campaign-planner → landing-page → pptx-designer → ai-slop-reviewer"
geekdocBreadcrumb: true
---

# 제품 개발 트랙 — PRD · 로드맵 · UX 자동화

> 제품 매니저, UX 디자이너, 개발 매니저를 위한 트랙입니다. **제품 기획 → 로드맵 설계 → UX 디자인 → 발표 자료 생성** 5단계로 제품 개발 프로세스 전체를 자동화합니다. 기획단계부터 출시 전까지 제품 개발 전 주기를 커버합니다.

{{< hint type="note" >}}
이 트랙은 현재 **moai-business**(`strategy-planner`·`startup-launchpad`)와 **moai-marketing**(`campaign-planner`)·**moai-content**(`landing-page`)의 인접 스킬로 PRD·로드맵·UX 흐름을 구성합니다. 향후 제품 관리 전용 플러그인이 추가되면 본 페이지가 갱신됩니다.
{{< /hint >}}

## 트랙 개요

### 🎯 학습 목표

- 제품 요구사항 문서화(`strategy-planner`) 전문 스킬 활용법
- 제품 로드맵 관리(`startup-launchpad`) 기술
- UX 리서치 및 디자인(`campaign-planner`, `landing-page`) 프로세스
- 제품 발표 자료 생성(`pptx-designer`) 및 품질 관리(`ai-slop-reviewer`)
- 제품 개발의 완전 자동화 워크플로우

### 📋 준비물

```
[ ] spec-writer, roadmap-manager, ux-researcher, ux-designer, pptx-designer, ai-slop-reviewer 스킬 접근 권한
[ ] 제품 기획 템플릿 (PRD, 로드맵, UX 리서치 템플릿)
[ ] 사용자 데이터 및 시장 조사 자료
[ ] 디자인 가이드라인 (UI/UX 스타일 가이드)
[ ] 발표 자료 템플릿 (투자자, 내부, 고객용)
```

## Step 1 — 플러그인 스캐폴드 구축 (10분)

```bash
# 프로젝트 폴더 구조
D:/Projects/product-dev/
└── product-assistant/
    ├── .claude-plugin/
    │   └── plugin.json
    ├── templates/
    │   ├── prd/
    │   ├── roadmap/
    │   ├── ux-research/
    │   └── presentations/
    ├── research/
    │   ├── user-research/
    │   ├── market-analysis/
    │   └── competitive-analysis/
    ├── specifications/
    │   ├── features/
    │   ├── requirements/
    │   └── acceptance-criteria/
    ├── roadmap/
    │   ├── quarterly/
    │   └── annual/
    ├── designs/
    │   ├── wireframes/
    │   ├── mockups/
    │   └── prototypes/
    └── skills/
        ├── product-planner/
        ├── roadmapper/
        ├── ux-researcher/
        ├── ux-designer/
        ├── presenter/
        └── product-reviewer/
```

플러그인을 생성하는 명령어:

{{< terminal title="claude — cowork" >}}
> D:/Projects/product-dev/product-assistant/ 폴더에 플러그인을 생성해줘.

  - plugin.json에 name: "product-assistant", version: "1.0.0", description: "제품 개발 자동화 — PRD, 로드맵, UX 디자인, 발표 자료"
  - skills 배열은 일단 비워두고, 이후 스킬 추가 시 채워줘
{{< /terminal >}}

## Step 2 — 제품 기획 스킬 (20분)

첫 번째 스킬로 `strategy-planner`를 활용한 제품 요구사항 문서화 스킬을 만듭니다.

```text
> product-assistant/skills/product-planner/SKILL.md 파일을 생성해줘。

name: product-planner
description: 제품 요구사항 문서(PRD) 자동 생성. 시장 분석, 사용자 리서치, 기능 요구사항을 통합하여 전문 PRD를 생성.
  트리거 — "PRD 작성", "제품 기획", "요구사항 문서화", "/product plan"

본문 절차:
1. 제품 개요 수집 및 분석:
  - 제품 이름 및 목적 정의
  - 타겟 사용자 식별 (인구통계학적, 행동적 특성)
  - 핵심 가치 제안 (사용자가 얻는 이점)
  - 비전 및 목표 설정 (장기적 목표)
2. spec-writer 스킬 호출:
  - 시장 분석 (시장 규모, 성장성, 동향)
  - 사용자 리서치 (니즈, 고통점, 기대치)
  - 경쟁사 분석 (장점, 약점, 차별점)
  - 요구사항 정의 (필수, 선택, 제외)
3. PRD 구조 설계:
  - 제품 개요 (제품명, 비전, 목표)
  - 시장 분석 (목표 시장, 경쟁 환경)
  - 사용자 프로파일 (페르소나, 사용자 여정)
  - 기능 요구사항 (핵심 기능, 보조 기능)
  - 비기능 요구사항 (성능, 보안, 확장성)
  - 성공 지표 (KPI, OKR)
4. 요구사항 상세화:
  - 사용자 스토리 작성
  - 기능 명세서 작성
  - 비즈니스 규칙 정의
  - 제약 조건 식별
5. 출력 형식:
  - PRD 문서 (Markdown/Word)
  - 사용자 프로파일 문서
  - 시장 분석 보고서
  - 요구사항 추적 매트릭스
```

### 🧪 테스트 명령어

{{< terminal title="claude — cowork" >}}
> # SaaS 제품 PRD 작성해줘
# 제품명: AI 기반 프로젝트 관리 툴
# 타겟: 중소기업 프로젝트 매니저
# 핵심 가치: AI 자동화로 프로젝트 효율성 30% 향상
# 시장 분석, 사용자 리서치, 기능 요구사항 포함

# 모바일 앱 PRD 작성해줘
# 제품명: 개인 재무 관리 앱
# 타겟: 20-30대 직장인
# 핵심 기능: 지출 추적, 예산 관리, 투자 조언
# 사용자 경험 요구사항 명시
{{< /terminal >}}

## Step 3 — 로드맵 관리 스킬 (20분)

두 번째 스킬로 `startup-launchpad`를 활용해 제품 로드맵을 생성합니다.

```text
> product-assistant/skills/roadmapper/SKILL.md 파일을 생성해줘。

name: roadmapper
description: 제품 로드맵 자동 생성 및 관리. 분기별, 연간 로드맵을 수립하고 기간별 우선순위를 관리하여 제품 방향성 설정.
  트리거 — "로드맵 작성", "분기 계획", "기능 우선순위", "/product roadmap"

본문 절차:
1. 로드맵 요구사항 분석:
  - 기간 설정 (분기별, 반기별, 연간)
  - 목표 설정 (비즈니스 목적, 사용자 가치)
  - 제약 조건 (자원, 시간, 예산)
  - 위험 요소 식별
2. roadmap-manager 스킬 호출:
  - 기능 우선순위 결정 (MoSCoW 방법론 적용)
  - 마일스톤 설정 (주요 시점)
  - 자원 배분 (인력, 예산)
  - 위험 관리 (리스크 완화 계획)
3. 로드맵 구성 요소:
  - 분기별 목표 설정
  - 주요 기능 정의
  - 마일스톤 일정
  - 성과 지표 설정
  - 의존성 관리
4. 우선순위 결정 기준:
  - Must-have: 반드시 필요한 핵심 기능
  - Should-have: 중요한 보조 기능
  - Could-have: 좋을 수 있는 추가 기능
  - Won't-have: 제외할 기능
5. 출력 형식:
  - 분기별 로드맵 (시각화 차트)
  - 연간 로드맵 (타임라인)
  - 마일스톤 일정표
  - 우선순위 매트릭스
```

### 🧪 테스트 명령어

{{< terminal title="claude — cowork" >}}
> # SaaS 제품 분기별 로드맵 작성해줘
# 1분기: MVP 런칭 (핵심 기능 5개)
# 2분기: 사용자 경험 개선 (UI/UX 업데이트)
# 3분기: 고급 기능 추가 (자동화, 통합)
# 4분기: 시장 확장 (새로운 고객층)
# 기간별 우선순위, 마일스톤 포함

# 모바일 앱 연간 로드맵 작성해줃
# Q1: 기본 기능 완성 (지출 추적, 예산 관리)
# Q2: AI 기능 추가 (지출 분석, 예산 제안)
# Q3: 사회적 기능 (친구 비교, 목표 공유)
# Q4: 보안 기능 강화 (생체인식, 암호화)
# 의존성 관리, 위험 요소 고려
{{< /terminal >}}

## Step 4 — UX 리서치 스킬 (20분)

세 번째 스킬로 `campaign-planner`를 활용해 사용자 경험 리서치를 수행합니다.

```text
> product-assistant/skills/ux-researcher/SKILL.md 파일을 생성해줘。

name: ux-researcher
description: 사용자 경험 리서치 자동 수행. 사용자 인터뷰, 설문조사, 경쟁사 분석을 통합하여 UX 인사이트 도출.
  트리거 — "UX 리서치", "사용자 조사", "경쟁사 분석", "/product research"

본문 절차:
1. 리서치 계획 수립:
  - 연구 질문 정의 (사용자 행동, 니즈, 고통점)
  - 대상 사용자 정의 (인구통계, 행동 특성)
  - 리서치 방법 결정 (정성적, 정량적)
  - 데이터 수집 계획
2. ux-researcher 스킬 호출:
  - 사용자 인터뷰 스크립트 생성
  - 설문조사 질문 설계
  - 경쟁사 분석 수행
  - 데이터 분석 및 인사이트 도출
3. 리서치 방법 적용:
  - 정성적 리서치: 사용자 인터뷰, 포커스 그룹, 관찰법
  - 정량적 리서치: 설문조사, 데이터 분석, A/B 테스트
  - 경쟁사 분석: 기능 비교, UX 평가, 차별점 분석
4. 데이터 분석 기법:
  - 데이터 코딩 및 테마 추출
  - 통계 분석 (설문조사 결과)
  - 사용자 여정 맵핑
  - 고통점 기회점 분석
5. 출력 형식:
  - 리서치 보고서
  - 사용자 인사이트 요약
  - 기회점 및 제안사항
  - UX 권장안
```

### 🧪 테스트 명령어

{{< terminal title="claude — cowork" >}}
> # SaaS 프로젝트 관리 툴 UX 리서치 수행해줘
# 연구 대상: 중소기업 프로젝트 매니저 10명
# 연구 질문: 현재 사용하는 도구의 문제점, 개선점
# 정성적/정량적 리서치 결합, 인사이트 도출

# 모바일 재무 관리 앱 경쟁사 분석해줘
# 경쟁 대상: 복지락, 토스, 네이버 페이
# 기능 비교, UX 평가, 사용자 리뷰 분석
# 차별화 기회점 식별
{{< /terminal >}}

## Step 5 — UX 디자인 스킬 (20분)

네 번째 스킬로 `landing-page`를 활용해 사용자 경험 디자인을 생성합니다.

```text
product-assistant/skills/ux-designer/SKILL.md 파일을 생성해줃。

name: ux-designer
description: UX 디자인 자동 생성. 와이어프레임, 프로토타입, 디자인 시스템을 생성하여 사용자 경험을 설계.
  트리거 — "UX 디자인", "와이어프레임", "프로토타입", "/product design"

본문 절차:
1. 디자인 요구사항 분석:
   - 사용자 요구사항 정의
   - 기술 제약 조건 확인
   - 디자인 가이드라인 참조
   - 디바이스별 요구사항
2. ux-designer 스킬 호출:
   - 와이어프레임 생성 (저충실도)
   - 인터랙션 디자인 (사용자 흐름)
   - 시각 디자인 (색상, 타이포그래피)
   - 디자인 시스템 구축
3. 디자인 단계별 생성:
   - Phase 1: 와이어프레임 (구조 레이아웃)
   - Phase 2: 인터랙션 디자인 (사용자 상호작용)
   - Phase 3: 시각 디자인 (UI 요소)
   - Phase 4: 디자인 시스템 (일관성 유지)
4. 디자인 원칙 적용:
   - 사용자 중심 디자인
   - 접근성 (WCAG 기준)
   - 일관성 디자인
   - 반응형 디자인
5. 출력 형식:
   - 와이어프레임 이미지
   - 인터랙션 프로토타입
   - 디자인 가이드라인
   - 디자인 시스템 문서
```

### 🧪 테스트 명령어

{{< terminal title="claude — cowork" >}}
> # SaaS 프로젝트 관리 툴 와이어프레임 생성해줘
# 주요 화면: 대시보드, 프로젝트 목록, 상세 보기
# 사용자 흐름: 로그인 → 대시보드 → 프로젝트 선택 → 상세 보기
# 반응형 디자인, 모바일/데스크톱 최적화

# 모바일 재무 관리 앱 프로토타입 생성해줘
# 주요 화면: 메인, 지출 추적, 예산 관리, 투자
# 인터랙션: 탭 네비게이션, 스와이프, 제스처
# 디자인 시스템: 색상, 타이포그래피, 아이콘
{{< /terminal >}}

## Step 6 — 발표 자료 생성 스킬 (15분)

다섯 번째 스킬로 `pptx-designer`를 활용해 제품 발표 자료를 생성합니다.

```text
product-assistant/skills/presenter/SKILL.md 파일을 생성해줃。

name: presenter
description: 제품 발표 자료 자동 생성. PRD, 로드맵, UX 디자인을 통합하여 투자자, 내부, 고객용 발표 자료 제작.
  트리거 — "발표 자료", "피칭 데크", "프로덕트 데모", "/product present"

본문 절차:
1. 발표 목적 및 대상 분석:
   - 발조 유형 (투자 유치, 내부 보고, 고객 데모)
   - 대상 구성 (투자자, 경영진, 개발팀, 고객)
   - 발조 시간 (15분, 30분, 60분)
   - 핵심 메시지 정의
2. pptx-designer 스킬 호출:
   - 템플릿 선택 (투자자, 내부, 고객용)
   - 콘텐츠 구조 설계
   - 시각화 요소 생성
   - 브랜딩 적용
3. 발표 자료 구조:
   - 소개 (제품 비전, 시장 기회)
   - 문제 정의 (사용자 고통점)
   - 솔루션 (제품 개요, 핵심 기능)
   - 시장 분석 (경쟁 환경, 차별점)
   - 로드맵 (개발 계획, 마일스톤)
   - UX 디자인 (사용자 경험)
   - 재무 모델 (수익 모델, 예측)
   - 팀 소개 (핵심 인력)
4. 시각화 요소:
   - 제품 소개 이미지
   - 시장 규모 그래프
   - 사용자 여정 맵
   - 로드맵 타임라인
   - 재무 예측 차트
5. 출력 형식:
   - PPTX 발표 자료
   - PDF 버전 (공유용)
   - 발표 메모 스크립트
   - Q&A 준비 자료
```

### 🧪 테스트 명령어

{{< terminal title="claude — cowork" >}}
> # 투자자용 제품 피칭 데크 생성해줘
# 슬라이드 12장: 소개, 문제, 솔루션, 시장, 경쟁, 로드맵, UX, 팀, 재무, 요청사항
# 전문적인 디자인, 데이터 기반의 설득력 있는 내용

# 내부용 개발 계획 발표 자료 생성해줘
# 슬라이드 15장: 제품 비전, 요구사항, 기능 명세, 개발 일정, 자원 배분, 위험 관리
# 개발팀을 위한 기술적 내용 포함
{{< /terminal >}}

## Step 7 — 품질 검수 스킬 (15분)

여섯 번째 스킬로 `ai-slop-reviewer`를 활용해 제품 문서를 검수합니다.

```text
product-assistant/skills/product-reviewer/SKILL.md 파일을 생성해줃。

name: product-reviewer
description: 제품 문서 최종 검수 및 전문성 강화. PRD, 로드맵, UX 디자인, 발표 자료의 완성도를 높이고 일관성을 검증.
  트리거 — "제품 검수", "최종 검토", "문서 완성", "/product final"

본문 절차:
1. ai-slop-reviewer 스킬 호출:
   - 일관성 검사 (PRD vs 로드맵 vs UX vs 발표 자료)
   - 전문성 검증 (제품 관련 용어, 개념)
   - 완전성 검토 (필요한 섹션 포함 여부)
   - 명확성 평가 (모호한 표현 제거)
2. 검수 항목 상세:
   - PRD 검수: 요구사항 명확성, 검증 가능성
   - 로드맵 검수: 현실성, 우선순위 타당성
   - UX 검수: 사용자 경험 일관성, 접근성
   - 발표 자료 검수: 설득력, 전문성
3. 품질 기준 적용:
   - 일관성: 모든 문서 간의 정보 일치
   - 완전성: 필요한 모든 정보 포함
   - 명확성: 모호하지 않은 표현
   - 전문성: 산업 표준 준수
4. 개선 적용:
   - 모호한 표현 명확화
   - 불일치 정보 통일
   - 누락된 정보 추가
   - 전문 용어 정확성 강화
5. 출력 형식:
   - 최종 검수 완료 문서
   - 검수 보고서
   - 개선 사항 리스트
   - 품질 등급 평가
```

### 🧪 테스트 명령어

{{< terminal title="claude — cowork" >}}
> # 전체 제품 문서 검수해줘
# PRD, 로드맵, UX 디자인, 발표 자료의 일관성 검증
# 전문성, 완전성, 명확성 평가

# 투자자용 발표 자료 최종 검수해줘
# 설득력 있는 내용, 전문적인 표현, 일관성 검증
# 투자자 의사결정에 도움이 되는 수준으로 완성
{{< /terminal >}}

## Step 8 — 체인 연결 및 자동화 (15분)

모든 스킬을 체인으로 연결하고 실제 제품 개발 프로세스에 적용합니다.

### 🔗 체인 설정

```text
# 제품 기획 체인
"AI 프로젝트 관리 툴 PRD 작성해줘" → product-planner → ux-researcher → ux-designer → product-reviewer

# 로드맵 체인
"분기별 로드맵 작성해줘" → product-planner → roadmapper → presenter → product-reviewer

# 발표 자료 체인
"투자자용 피칭 데크 만들어줘" → product-planner → ux-researcher → ux-designer → presenter → product-reviewer
```

### ⏰ 스케줄링 설정

{{< terminal title="claude — cowork" >}}
/schedule

매월 1일 10:00에 product-assistant의 roadmapper 스킬을 실행해줘.
분기 초 (1/4/7/10월 1일)에 product-planner 자동 실행.

실패 시 Slack #product-alerts 채널로 오류 알림 전송.
{{< /terminal >}}

## 성공 검증 체크리스트

```
[ ] product-planner 실행 → PRD 생성 확인
[ ] roadmapper 실행 → 로드맵 생성 확인
[ ] ux-researcher 실행 → 사용자 리서치 확인
[ ] ux-designer 실행 → UX 디자인 생성 확인
[ ] presenter 실행 → 발표 자료 생성 확인
[ ] product-reviewer 실행 → 품질 검수 확인
[ ] 체인 연결 → 6개 스킬 연속 실행 테스트 성공
[ ] 실제 제품 테스트 → 실제 제품 아이디어로 테스트 완료
```

## 자주 발생하는 문제 해결

### 🚨 요구사항 불명확

**원인:** 사용자 요구사항이 모호하거나 구체적이지 않을 경우

**해결:** 구체화된 요구사항 수집 시스템
```text
# 요구사항 구체화 프로세스
1. 사용자 인터뷰 통해 요구사항 심층 탐색
2. 사용자 스토리 작성 (사용자가 원하는 행동)
3. 인수 기준 정의 (검증 가능한 조건)
4. 우선순위 부여 (MoSCoW 방법론)
```

### 🎨 디자인 일관성 부족

**원인:** 여러 디자너 작업 시 일관성 유지 어려움

**해결:** 디자인 시스템 표준화
```text
# 디자인 시스템 요소
1. 컬러 팔레트 (주색, 보조색, 중성색)
2. 타이포그래피 (제목, 본문, 버튼 글씨체)
3. 인터랙션 패턴 (버튼, 폼, 네비게이션)
4 컴포넌트 라이브러리 (버튼, 카드, 모달)
```

### 📊 정보 과다 또는 부족

**원인:** 발표 자료에 불필요한 정보 과다 또는 핵심 정보 누락

**해결:** 정보 필터링 및 구조화 시스템
```text
# 정보 필터링 기준
1: 핵심 메시지 (1개 이상의 메시지)
2: 지원 데이터 (핵심 메시지 증빙)
3: 세부 정보 (참고용 추가 정보)
4: 제외 항목 (필요 없는 정보)
```

## 확장 아이디어

### 🎯 고급 활용

1. **실시간 제품 개선 시스템**:
   ```text
   # 사용자 피드백 분석 체인
   "사용자 피드백 분석" → feedback-analyzer → improvement-suggestions → roadmap-update
   ```

2. **자동 테스트 케이스 생성**:
   ```text
   # 테스트 케이스 생성 체인
   "기능 테스트 케이스 작성" → requirement-analyzer → test-generator → quality-check
   ```

3. **시장 변화 대응 시스템**:
   ```text
   # 시장 변화 모니터링 체인
   "시장 동향 모니터링" → market-trend-analysis → competitive-response → strategy-update
   ```

## 관련 자료

- [spec-writer 제품 요구사항 작성 가이드](../../../plugins/moai-core/)
- [roadmap-manager 로드맵 관리](../../../plugins/moai-core/)
- [ux-researcher 사용자 리서치](../../../plugins/moai-marketing/)
- [ux-designer UX 디자인](../../../plugins/moai-marketing/)
- [pptx-designer 발표 자료 생성](../../../plugins/moai-office/)

---

### Sources
- [modu-ai/cowork-plugins — moai-core](https://github.com/modu-ai/cowork-plugins/tree/main/moai-core)
- [Nielsen Norman Group UX 리서치 가이드](https://www.nngroup.com/)
- [Marty Cagan Inspired Product Management](https://www.svpg.com/)
- [Google Material Design 가이드](https://material.io/)