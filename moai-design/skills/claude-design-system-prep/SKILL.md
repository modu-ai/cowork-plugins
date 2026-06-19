---
name: claude-design-system-prep
description: |
  브랜드 자산(로고·색·타이포·기존 사이트·PPTX 등)을 분석해 Claude Design 업로드용 DESIGN.md를 자동으로 합성합니다.
  Claude Design 디자인 시스템 셋업의 가장 흔한 실패(자산이 흩어져 있고 정리가 안 된 채 업로드)를 해결합니다.
  결과는 그대로 claude.ai/design 온보딩에 업로드하면 됩니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "Claude Design용 디자인 시스템 자료 정리"
  - "브랜드 자산을 DESIGN.md로 합성"
  - "디자인 시스템 자산 업로드 준비"
  - "claude.ai/design 디자인 시스템 셋업 준비"
  - "DESIGN.md 만들어 줘"
user-invocable: true
version: 2.27.0
---

# claude-design-system-prep — 디자인 시스템 자산 합성

## 개요

[docs-site 디자인 시스템 페이지](https://cowork.mo.ai.kr/claude-design/design-system/)에서 정리한 대로, Claude Design 결과 품질을 가장 크게 좌우하는 것은 **디자인 시스템 셋업**입니다. 이 스킬은 흩어진 브랜드 자산을 분석해 Claude Design이 한 번에 흡수할 수 있는 **DESIGN.md**로 합성합니다.

## 트리거 키워드

Claude Design 디자인 시스템, 디자인 시스템 자산, DESIGN.md, 브랜드 자산 합성, 디자인 시스템 셋업, claude.ai/design 시스템

## 입력 — 자산 5종

다음 중 가능한 만큼 제공합니다 (한 가지만 있어도 시작 가능).

| 자산 유형 | 형태 | Claude가 추출하는 것 |
|---|---|---|
| **코드** | GitHub repo URL · 로컬 UI 패키지 디렉토리 | React·Vue·Svelte 컴포넌트, CSS 토큰, Tailwind 설정 |
| **디자인 파일** | Figma `.fig`, Sketch, 컴포넌트 스크린샷 PNG | 색 팔레트, 타이포 스케일, 컴포넌트 라이브러리 |
| **브랜드 자산** | 로고 SVG·PNG, 색 팔레트 이미지, 스타일 가이드 PDF | 색·타이포·로고 사용 규칙 |
| **실물** | 운영 중 웹사이트 URL, PPTX 덱, 잘 만든 마케팅 페이지 | 실제 컴포넌트·간격·voice |
| **사전 빌트인** | Apple · Linear · Stripe 시스템 (오픈 라이선스) | 시작점 |
| **디자인 시스템 라이브러리** | `moai-design:design-system-library`의 75개 시스템 (claude · clickhouse · clay 등) | 토큰(색·타이포·radius·spacing) + 컴포넌트 매핑 — DESIGN.md 합성의 즉시 소스 |

> **우선 순위 (v2.21.0+)**: 사용자가 특정 브랜드 무드를 지정하거나 결과물 성격에 맞는 시스템이 필요하면, 별도 자산 수집 전 **`design-system-library`의 75개 시스템에서 먼저 선택**합니다. `claude-design-system-prep`는 선택된 `systems/<name>.md` 토큰을 DESIGN.md 합성의 1차 소스로 사용합니다. 외부 자산(웹사이트 URL·Figma 등)은 라이브러리 시스템에 대한 보강 자료로만 활용합니다.

## 워크플로우

### 1단계 — 자산 수집

사용자에게 자산 유형을 묻고 입력을 받습니다. AskUserQuestion 1라운드.

```
가지고 있는 자산을 모두 알려 주세요 (복수 선택):
- 우리 웹사이트 URL
- 로고·이미지 파일
- 잘 만든 자사 페이지 (PPTX·PDF·캡처)
- GitHub repo (UI 컴포넌트)
- Figma 파일
- 사전 빌트인에서 시작
```

선택 후 각 자산의 경로·URL을 차례로 수집합니다.

### 2단계 — 자산 분석

| 자산 | 처리 방법 |
|---|---|
| 웹사이트 URL | WebFetch로 라이브 페이지 분석 — 색·폰트·컴포넌트 패턴 추출 |
| 이미지 파일 | 비전 분석으로 색 팔레트·로고 형태 추출 |
| PPTX·PDF | 텍스트·이미지·배경 색 분석 |
| GitHub repo URL | `package.json` · `tailwind.config.*` · UI 디렉토리 분석 |
| 로컬 폴더 | `ls` · `Read`로 파일 구조 분석 |

### 3단계 — DESIGN.md 합성

**라이브러리 시스템 선택 우선 경로 (v2.21.0+)**: 1단계에서 브랜드 무드만 지정된 경우, `moai-design:design-system-library`의 `systems/registry.md`에서 매칭되는 시스템을 선택하고 `systems/<name>.md`의 YAML 토큰을 DESIGN.md의 Color palette · Typography · Spacing 섹션에 직접 반영합니다. 이 경로는 자산 분석(2단계)을 생략하거나 보강으로만 사용하므로 가장 빠릅니다.

다음 구조로 DESIGN.md를 작성합니다.

```markdown
# [브랜드명] Design System

## Brand voice & personality

[추출한 voice — 형용사 5-7개, 한 문단 요약]

## Color palette

### Primary
- primary/500: #[hex] — [의미]
- primary/600 ~ 100/900 스케일

### Secondary · Accent
[보조·강조색]

### Semantic
- success · warning · error · info

## Typography

- Display: [폰트 이름] [weight] [사이즈 범위]
- Heading: [폰트 이름]
- Body: [폰트 이름]
- Mono: [폰트 이름]

## Spacing scale

[Tailwind 또는 디자인 토큰 기반 — 4·8·12·16·24·32·48·64 등]

## Components

### Existing in our codebase
- Button (variants: primary, secondary, ghost)
- Card (variants: default, elevated, bordered)
- ...

### Layout patterns
- Hero with [구조]
- Feature grid (3-col, 6-card)
- ...

## Voice & copy patterns

- 어조: [존댓말·반말 정책]
- 금기어: [회피할 표현 — AI 슬롭, 진부 표현]
- 권장 패턴: [회사 고유 표현]

## Reference

- 자사 잘 만든 페이지: [URL]
- 경쟁사 참고: [URL]
- 디자인 영감: [Dribbble/Behance]

## Constraints

- [모바일·데스크톱 정책]
- [접근성 기준 — WCAG 등]
- [폰트 라이선스 메모]
- [회피 톤·콘셉트]
```

### 4단계 — 자산 정리 가이드 동봉

DESIGN.md와 함께 **claude.ai/design에 무엇을 어떻게 올릴지** 가이드를 제공합니다.

```markdown
## Claude Design 업로드 가이드

### 업로드 우선순위

1. `DESIGN.md` (이 파일) — 가장 먼저
2. [GitHub repo 또는 UI 패키지 디렉토리]
3. [잘 만든 자사 사이트 URL] — 웹 캡처 도구로
4. [경쟁사 참고 URL] — 톤 비교용
5. 로고 파일 (SVG 우선)

### 업로드 시 주의

- 모노레포 전체 X → UI 패키지 디렉토리만
- 고객 데이터·매출 박힌 PPTX는 익명화 후 업로드
- 폰트 파일은 라이선스 확인 후 업로드

### Published 토글

1. 위 자산 업로드 후 5-15분 대기 (분석 시간)
2. UI 키트 검토 후 테스트 프롬프트 실행:
   - "마케팅 랜딩 페이지를 디자인해 줘"
   - "사이드바와 3개 콘텐츠 섹션이 있는 설정 페이지"
3. 결과가 브랜드와 일치하면 → Published 토글 ON
4. 어긋나면 → Remix 또는 자산 추가 업로드 후 재시도
```

### 5단계 — 결과 저장

- 사용자가 지정한 경로 또는 기본 `./design-system-prep/` 디렉토리에 저장
- `DESIGN.md` + `UPLOAD-GUIDE.md` + 정리된 자산 사본
- 사용자가 그대로 폴더를 Claude Design에 업로드 가능

## 출력 형식

```
## 디자인 시스템 자산 합성 완료

### 분석한 자산
- [URL 또는 파일 경로 목록]

### 생성된 파일
- ./design-system-prep/DESIGN.md  (XX줄)
- ./design-system-prep/UPLOAD-GUIDE.md

### 추출 요약
- Primary: #[hex] (출처: [자산])
- Typography: [폰트] (출처: [자산])
- Components 인식: N개
- Voice: [한 문단]

### 다음 단계
1. claude.ai/design 진입 → Organization settings → Design systems
2. 위 폴더 업로드 → 5-15분 대기
3. 테스트 프롬프트로 검증
4. Published 토글 ON
```

## 사용 예시

### 예시 1 — 운영 중 SaaS 회사

```
입력 자산:
- 자사 웹사이트: https://example.com
- GitHub repo: github.com/example/web-ui
- 로고: ./brand/logo.svg
- 잘 만든 PPTX 덱: ./decks/q4-report.pptx

결과:
- DESIGN.md (자동 합성, 6섹션)
- 자산 정리 폴더
- 추출된 색 5개, 폰트 3개, 컴포넌트 12개
```

### 예시 2 — 초기 스타트업 (자산 적음)

```
입력 자산:
- 로고: ./logo.png
- 색 팔레트 이미지: ./colors.png
- 영감 사이트: linear.app

결과:
- DESIGN.md (Linear 기반 + 로고·색 커스터마이즈)
- UPLOAD-GUIDE.md
- 후속 권장: Linear 사전 빌트인에서 시작 → 우리 색·로고로 Remix
```

### 예시 3 — 자산 없음 (사전 빌트인 활용)

```
입력: "자산 없음 — Linear 톤으로 시작하고 싶다"

결과:
- DESIGN.md (Linear 시스템 기반 시작점)
- 자체 브랜드 점진 정의 가이드
- 권장: Claude Design에서 사전 빌트인 Linear 선택 후
  3-5개 프로젝트 진행하며 자사 시스템 점진 추출
```

## 주의사항

### Do

- 자산이 부족해도 시작 — 사전 빌트인 + 부분 자산 조합 가능
- DESIGN.md를 **사람이 읽을 수 있는 형식**으로 — Claude도 사람도 이해
- 폰트는 **이름 + 라이선스 메모** 함께 — 핸드오프 시 분쟁 방지
- WebFetch로 라이브 사이트 분석 시 robots.txt·이용 약관 확인

### Don't

- 모노레포 전체 분석 시도 금지 — 5분+ 지연 + 시스템 추출 어긋남
- 민감 자산(고객 데이터·매출이 박힌 PPTX) 그대로 업로드 금지 → 익명화
- "AI가 알아서" 추측만으로 DESIGN.md 채우기 금지 — 사용자 확인 필요
- 폰트 라이선스 모른 채 자산에 포함 금지

## 관련 스킬

| 스킬 | 사용 시점 |
|---|---|
| `moai-design:claude-design-brief` | 후속: 시스템 셋업 후 첫 시안 작성 |
| `moai-design:claude-design-prompt-builder` | 후속: 특정 영역 디자인 |
| `moai-marketing:brand-identity` | 선행: 브랜드 정체성이 모호할 때 |
| `moai-content:copywriting` | 보조: voice·copy 패턴 정리 |
| `moai-office:pptx-designer` | 보조: 잘 만든 자사 PPTX가 없으면 |
