---
name: design-handoff-reader
description: |
  Claude Design → Claude Code 핸드오프 번들(공식 구성: README + 디자인 파일 + chat)을 방어적으로 분석해 요약 보고서와 Claude Code에 넘길 짧은 지시 1줄을 자동 생성합니다.
  README를 source of truth로 먼저 파싱하고, 토큰/컴포넌트 JSON은 있으면 사용·없으면 코드(HTML/CSS)에서 유도하는 best-effort 방식입니다(하드 5-파일 요구 없음).

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "Claude Design 핸드오프 번들 분석"
  - "handoff 번들 요약"
  - "핸드오프 번들 읽어 줘"
  - "디자인 토큰 추출"
  - "Claude Code 핸드오프 준비"
version: "1.1.1"
---

# design-handoff-reader — 핸드오프 번들 분석

## 개요

Claude Design의 **Export → "Handoff to Claude Code"**(로컬 터미널 또는 Claude Code Web)는 프로젝트의 **디자인 파일 + chat + README** 3요소를 담은 번들을 만듭니다(공식 확인 사실). Anthropic은 디자인을 "code under the hood(HTML/CSS/JS)"로 규정하며, 구조화된 DTCG JSON 형식은 **공식 규격이 아닙니다**. 이 스킬은 그 번들을 방어적으로 분석해 **사람이 5분 안에 핸드오프 상태를 파악**할 수 있는 요약 보고서와 **Claude Code에 그대로 붙여 넣을 수 있는 지시 1줄**을 생성합니다.

> **공식 규격 vs 추론 (anti-hallucination — docs 03 §5.4)**: 공식 문서가 보장하는 것은 3요소 triad(디자인 파일 + chat + README)뿐입니다. `design-tokens.json`/`tokens.json`, `components.json`, `layout-hierarchy.json`, `chat-history.md` 같은 **구체 파일명은 MoAI 작업 가정이며 Anthropic 문서화 규격이 아닙니다**. 따라서 하드 5-파일 존재 검사를 하지 않고, 존재하는 것만 best-effort로 파싱하며 없으면 코드(HTML/CSS)에서 유도합니다.

> **핸드오프 방향 + 진입 모드 (2026-06)**: 번들은 Claude Design 캔버스의 **Export → Handoff to Claude Code**(local/web)에서 생성됩니다. 반대 방향(코드→디자인)은 Claude Code 터미널의 `/design-sync`로 코드베이스 디자인 시스템을 Claude Design에 import — 핸드오프는 양방향입니다. 두 진입 모드를 지원합니다: (1) **.zip 다운로드**(확정 오프라인 컨테이너), (2) **붙여넣기 프롬프트 + 번들 URL**(실제 메인 흐름 — Claude Code가 URL을 fetch).

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

### 1단계 — README 우선 파싱 + 방어적 glob (graceful degradation)

**하드 5-파일 존재 검사를 하지 않습니다.** 정확한 번들 형식이 공식 미문서화이므로 다음 순서로 방어적으로 처리합니다.

1. **README 우선 (source of truth)**: 번들에서 README를 **먼저** 읽어 구조·의도를 파악합니다. Anthropic이 "모델에게 디자인 해석 지침을 주도록" 설계한 유일한 공식 문서화 요소입니다. `README.md`가 일반적이나 확장자 없는 `README`도 수용합니다.
2. **선택적 best-effort glob (하드 요구 금지)**: 아래 파일들을 **있으면 사용, 없어도 실패하지 않는** 입력으로 discover합니다. 파일명은 추론이므로 변형을 모두 수용합니다.

| 개념 | 수용 파일명 (추론 — 공식 규격 아님) | 없을 때 fallback |
|---|---|---|
| 디자인 토큰 | `design-tokens.json` **또는** `tokens.json` (둘 다 수용) | CSS custom properties / standalone HTML에서 토큰 유도 |
| 컴포넌트 | `components.json` | HTML DOM 구조에서 컴포넌트 트리 추론 |
| 레이아웃 | `layout-hierarchy.json` | HTML/CSS에서 반응형 패턴 추론 |
| chat 맥락 | `chat-history.md` (또는 README 내 chat 요약) | 코드 주석·README에서 결정 맥락 유도 |
| 자산 | `assets/` | 없으면 생략 |

3. **파일명 분열 정규화**: 토큰 파일이 `design-tokens.json`이든 `tokens.json`이든 수용하고, `.moai/design/` 출력 시 한 이름(`tokens.json`)으로 정규화합니다(`design-workflow`과 정합).
4. **version gating 완화**: 알 수 없거나 없는 bundle version은 **hard-reject하지 않고** best-effort 파싱 + 경고로 처리합니다(공식 version-stamp 증거 없음 — `supported_bundle_versions`는 MoAI 내부 placeholder).
5. **2개 진입 모드**: **.zip 다운로드**(unzip 후 위 절차) + **붙여넣기 프롬프트 + 번들 URL**(Claude Code가 URL fetch 후 컨텍스트에 로드된 것을 분석).

### 2단계 — 존재하는 파일 분석 (best-effort)

> 아래 파일별 분석은 **해당 파일이 존재할 때만** 수행합니다. 없으면 1단계 표의 fallback(코드/HTML 유도)으로 대체하며, 누락 자체는 실패가 아닙니다.

#### README (source of truth) 분석

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

- README를 먼저 파싱(source of truth) 후, 존재하는 파일만 best-effort 분석 (하드 5-파일 요구 없음)
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
| `moai-designer:design-brief` | 선행: 핸드오프할 시안 자체를 만들 때 |
| `moai-designer:design-system-prep` | 선행: 디자인 시스템 셋업 |
| `moai-pm:project` | 후속: Claude Code 작업 폴더 초기화 |
| `moai-coworker:collab-spec` | 보조: 핸드오프 후 코드 SPEC 작성 |
