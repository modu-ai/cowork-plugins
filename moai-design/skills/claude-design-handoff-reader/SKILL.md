---
name: claude-design-handoff-reader
description: |
  Claude Code 핸드오프 번들(README + design-tokens.json + components.json + layout-hierarchy.json + chat-history.md)을 분석해 요약 보고서와 Claude Code에 넘길 짧은 지시 1줄을 자동 생성합니다.
  핸드오프 번들 구조를 한눈에 파악하고, 컴포넌트 트리·토큰·디자인 결정 맥락을 정리합니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "Claude Design 핸드오프 번들 분석"
  - "handoff 번들 요약"
  - "핸드오프 번들 읽어 줘"
  - "디자인 토큰 추출"
  - "Claude Code 핸드오프 준비"
user-invocable: true
version: 2.27.0
---

# claude-design-handoff-reader — 핸드오프 번들 분석

## 개요

[내보내기·핸드오프 페이지](https://cowork.mo.ai.kr/claude-design/export-handoff/)에서 정리한 대로, Claude Design은 핸드오프 시 README·design-tokens.json·components.json·layout-hierarchy.json·chat-history.md를 포함한 번들을 만듭니다. 이 스킬은 그 번들을 분석해 **사람이 5분 안에 핸드오프 상태를 파악**할 수 있는 요약 보고서와 **Claude Code에 그대로 붙여 넣을 수 있는 지시 1줄**을 만들어 줍니다.

## 트리거 키워드

Claude Design 핸드오프, handoff 번들, design-tokens 분석, components.json, Claude Code 인계, 디자인 토큰 추출

## 입력

다음 중 하나:

| 입력 | 형태 |
|---|---|
| ZIP archive | `./handoff-bundle.zip` |
| 디렉토리 | `./handoff-bundle/` |
| URL | Claude Design Export 시 제공된 번들 URL |

## 워크플로우

### 1단계 — 번들 구조 검증

```
handoff-bundle/
├── README.md
├── design-tokens.json
├── components.json
├── layout-hierarchy.json
├── chat-history.md
└── assets/
```

위 파일들의 존재를 확인합니다. 누락된 파일이 있으면 보고하고 가능한 만큼만 분석합니다.

| 파일 | 누락 시 영향 |
|---|---|
| README.md | 의도 파악 어려움 — 코드만 보고 추측 |
| design-tokens.json | 토큰 그대로 사용 불가 — Claude Code가 다시 추론 |
| components.json | 컴포넌트 트리 추론 — 매핑 정확도 떨어짐 |
| layout-hierarchy.json | 반응형 패턴 추론 |
| chat-history.md | 디자인 결정 맥락 손실 |

### 2단계 — 각 파일 분석

#### README.md 분석

- 프로젝트 목표·범위
- 컴포넌트 매핑 가이드
- 의도된 사용자 플로우
- 알려진 제약·미완성 부분

#### design-tokens.json 분석

```
- 색 토큰 N개 (primary·secondary·semantic 구분)
- 타이포 N개 (family·size·weight 스케일)
- 간격 N개 (spacing scale)
- 모서리·그림자·전환 등
- 시맨틱 매핑 정확도 (예: primary/500 → #2a8a8c)
```

#### components.json 분석

```
- 사용된 컴포넌트 N개
- 컴포넌트 트리 (depth·중첩)
- variants·states 명시 여부
- 기존 코드베이스 컴포넌트와 매칭 가능성
```

#### layout-hierarchy.json 분석

```
- 페이지 수
- 반응형 변형 정의 여부 (mobile·tablet·desktop)
- 그리드·간격 일관성
- 인터랙티브 요소 (호버·클릭·드래그) 목록
```

#### chat-history.md 분석

```
- 주요 디자인 결정과 이유 추출
- 사용자가 명시한 제약·우선순위
- 거부된 대안 (왜 안 했는가)
- 미해결 질문
```

### 3단계 — 요약 보고서 생성

```markdown
# 핸드오프 번들 분석 — [프로젝트명]

## 한눈에 보기

| 항목 | 내용 |
|---|---|
| 페이지 수 | N |
| 컴포넌트 수 | N (그중 기존 코드와 매칭 가능: M) |
| 디자인 토큰 | 색 N·타이포 N·간격 N |
| 인터랙티브 요소 | N (호버·클릭·드래그) |
| 반응형 정의 | mobile·tablet·desktop 모두 / 일부 / 없음 |
| 엣지 상태 | empty·error·loading 정의 여부 |

## 디자인 토큰 요약

### 색
- primary/500: #[hex] (기존 토큰과 일치 / 새로움)
- ...

### 타이포
- Display: [폰트] [size]
- ...

## 컴포넌트 트리

```
Page
├─ Hero
│  ├─ Headline (h1)
│  ├─ Subheadline (h2)
│  └─ CTA Button (primary, large)
├─ FeatureGrid (3-col)
│  ├─ FeatureCard × 6
│  └─ ...
└─ Footer
```

## 디자인 결정 맥락 (chat-history.md에서 추출)

1. 사이드바 대신 탭 선택 — 이유: 사용자가 모든 섹션 동시 인지 필요
2. 흰 배경 + 단일 강조색 — 이유: 기존 마케팅 사이트 톤 유지
3. ...

## 미해결 질문

- [ ] 결제 페이지의 카드 위젯이 기존 ChargeCard와 호환되는가?
- [ ] 다크 모드 변형이 정의되어 있지 않음
- [ ] ...

## 구현 우선순위 (추천)

1. P0: Hero · CTA (전환 핵심)
2. P1: FeatureGrid (스크롤 다음 영역)
3. P2: Footer · 보조 페이지
4. P3: 다크 모드 변형 (정의 후 추가)

## Claude Code 핸드오프 지시 (복붙용)

```
이 핸드오프 번들을 받아 프로덕션 코드로 구현해 줘.
번들 URL: [URL]
기존 디자인 시스템 토큰을 그대로 사용. 컴포넌트는 우리 React 라이브러리
([ChargeCard·FeatureGrid·CTA 등 매칭 컴포넌트])로 매핑. 결과를 로컬에서
미리보기 가능하게 (npm run dev). chat-history.md의 디자인 결정 맥락을
존중. 다크 모드는 정의 후 별도 라운드로.
```
```

### 4단계 — 후속 권장

#### 두 경로 분기

| 경로 | 사용 시점 | 본 스킬의 역할 |
|---|---|---|
| **Claude Code 빌드 경로** (1차 목적) | 프로덕션 코드로 구현해야 할 때 | 번들 분석 + Claude Code 1줄 지시 자동 생성 (아래 워크플로우) |
| **Canva 마케팅 후속 경로** (Anthropic ↔ Canva 공식 파트너십) | 마케팅 팀이 SNS·이벤트·광고 변형을 후속 편집해야 할 때 | 본 스킬의 분석은 참고용. 실제 Canva export는 Claude Design 캔버스의 Export → Canva 메뉴에서 직접 실행 |

두 경로를 동시에 진행하면 디자인이 두 도구에서 동시에 변형되어 일관성이 깨집니다. **한 시안에서 한 경로만** 운영하세요.

```
## 다음 단계 (Claude Code 빌드 경로)

1. 위 Claude Code 핸드오프 지시를 복사
2. Claude Code 터미널 또는 Web에서 붙여넣기
3. 첫 빌드 후 로컬 미리보기 확인
4. 코드와 디자인 차이가 있으면:
   - 작은 차이: Claude Code에서 수정 지시
   - 큰 차이: Claude Design으로 돌아가 재디자인 → 새 핸드오프

## 주의

- 핸드오프 후 디자인을 또 수정하지 마세요 — 코드와 어긋납니다
- 큰 디자인 변경은 새 핸드오프 번들 작성 후 부분 인계
- 마케팅 후속(Canva 경로)이 필요하면 핸드오프 번들과 별개로 Claude Design 캔버스에서 직접 Export → Canva
```

## 사용 예시

### 예시 1 — 완전한 번들

```
입력: ./handoff-bundle/ (5개 파일 모두 존재)

결과:
- 페이지 4개, 컴포넌트 18개 (기존 매칭 14)
- 색 8개, 타이포 5개, 간격 8개
- 디자인 결정 5개 추출
- 미해결 질문 3개
- Claude Code 지시 1줄 생성
```

### 예시 2 — 부분 번들 (chat-history.md 누락)

```
입력: ./handoff-bundle/ (chat-history.md 없음)

결과:
- 다른 파일 정상 분석
- chat-history.md 누락 경고 — 디자인 의도가 코드로만 추론됨
- Claude Code 지시는 생성 (맥락이 약해진 점 명시)
- 후속 권장: Claude Design 채팅 화면을 캡처해 별도 참고 자료로
```

### 예시 3 — ZIP 압축 번들

```
입력: ./handoff-bundle.zip

처리:
1. unzip으로 ./handoff-bundle/ 추출
2. 위 예시 1·2와 동일 절차
3. 분석 후 ZIP 원본은 백업 용도로 보존
```

## 출력 형식

```
## 핸드오프 번들 분석 결과

### 번들 상태
- 위치: [경로]
- 포함 파일: [목록]
- 누락 파일: [있다면]

### 한눈에 보기 테이블
[페이지·컴포넌트·토큰·인터랙티브·반응형·엣지]

### 디자인 토큰 요약
[색·타이포·간격]

### 컴포넌트 트리
[ASCII 트리]

### 디자인 결정 맥락
[chat-history에서 추출한 결정 5-10개]

### 미해결 질문
[체크리스트]

### 구현 우선순위
[P0-P3]

### Claude Code 지시 (복붙용)
[1단락 지시문]
```

## 주의사항

### Do

- 모든 5개 파일을 가능한 한 분석
- 컴포넌트 이름이 기존 코드와 매칭되는지 명시 — Claude Code의 결과 품질을 결정
- 디자인 결정 맥락을 압축 — 5-10개로 추출
- 미해결 질문을 분리 — 구현 시작 전 결정 필요

### Don't

- 번들 분석을 핸드오프 절차의 대체로 쓰지 말 것 — 항상 Claude Code에 번들을 직접 인계
- 디자인 토큰을 임의로 변경 금지 — Claude Code가 그대로 사용해야 일관성
- chat-history.md의 결정 맥락을 임의 해석 금지 — 인용 형태로 보존

## 관련 스킬

| 스킬 | 사용 시점 |
|---|---|
| `moai-design:claude-design-brief` | 선행: 핸드오프할 시안 자체를 만들 때 |
| `moai-design:claude-design-system-prep` | 선행: 디자인 시스템 셋업 |
| `moai-core:project` | 후속: Claude Code 작업 폴더 초기화 |
| `moai-product:spec-writer` | 보조: 핸드오프 후 코드 SPEC 작성 |
