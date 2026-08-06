---
name: design-system-prep
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
version: "1.1.0"
---

# design-system-prep — 디자인 시스템 자산 합성

## 개요

[docs-site 디자인 시스템 페이지](https://cowork.mo.ai.kr/claude-design/design-system/)에서 정리한 대로, Claude Design 결과 품질을 가장 크게 좌우하는 것은 **디자인 시스템 셋업**입니다. 이 스킬은 흩어진 브랜드 자산을 분석해 Claude Design이 한 번에 흡수할 수 있는 **DESIGN.md**로 합성합니다.

> **네이티브 경로와의 관계 (2026-06 업데이트)**: Claude Design은 이제 GitHub repo·디자인 파일·업로드에서 디자인 시스템을 직접 import하고, 출력을 등록된 시스템에 대조해 자가 수정합니다. Claude Code 터미널에서는 `/design-sync`로 코드베이스 디자인 시스템을 바로 보낼 수도 있습니다. 깔끔한 코드 repo가 있으면 그 네이티브 경로가 가장 빠릅니다. 이 스킬은 **자산이 흩어져 있거나, 깔끔한 코드 repo가 없거나, `design-system-library`의 큐레이션된 토큰을 출발점으로 쓰고 싶을 때** DESIGN.md로 합성해 네이티브 경로를 보완합니다(대체가 아니라 보완).

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
| **디자인 시스템 라이브러리** | `moai-designer:design-system-library`의 75개 시스템 (claude · clickhouse · clay 등) | 토큰(색·타이포·radius·spacing) + 컴포넌트 매핑 — DESIGN.md 합성의 즉시 소스 |

> **우선 순위 (v2.21.0+)**: 사용자가 특정 브랜드 무드를 지정하거나 결과물 성격에 맞는 시스템이 필요하면, 별도 자산 수집 전 **`design-system-library`의 75개 시스템에서 먼저 선택**합니다. `design-system-prep`는 선택된 `systems/<name>.md` 토큰을 DESIGN.md 합성의 1차 소스로 사용합니다. 외부 자산(웹사이트 URL·Figma 등)은 라이브러리 시스템에 대한 보강 자료로만 활용합니다.

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

**라이브러리 시스템 선택 우선 경로 (v2.21.0+)**: 1단계에서 브랜드 무드만 지정된 경우, `moai-designer:design-system-library`의 `systems/registry.md`에서 매칭되는 시스템을 선택하고 `systems/<name>.md`의 YAML 토큰을 DESIGN.md의 Color palette · Typography · Spacing 섹션에 직접 반영합니다. 이 경로는 자산 분석(2단계)을 생략하거나 보강으로만 사용하므로 가장 빠릅니다.

먼저 각 섹션을 원천 자산에서 **어떻게 도출하는지** 정리합니다. DESIGN.md는 관측된 자산에서 값을 뽑아 채우는 문서이므로, 각 섹션은 다음 규칙으로 채웁니다.

| # | 섹션 | 원천 자산에서 도출하는 법 |
|---|---|---|
| 1 | Brand voice & personality | About·랜딩 카피·PPTX 문구를 읽어 형용사 추출. 불명확하면 `moai-coworker:collab-brand-identity` 선행 후 AskUserQuestion으로 확정 |
| 2 | Color palette | 이미지·스크린샷 비전 분석 + CSS/Tailwind 토큰 파싱으로 hex 수집 → 50–950 스케일 보간, 상태색·시그니처 자산 분리. 각 색에 **출처 표기** |
| 3 | Typography | `@font-face`·CSS·Figma 텍스트 스타일에서 family/weight/size 추출. 한국어면 letter-spacing 규칙 부여, 제목↔본문 굵기 대비 관찰 |
| 4 | Spacing/Radius/Shadow/Motion | Tailwind config·CSS 변수에서 스케일 추출. 없으면 4px 베이스 표준 스캐폴드 제시 |
| 5 | Token 3-layer mapping | 2~4에서 확정한 값을 DTCG/CSS/semantic 3계층으로 요약. **실제 변환은 `moai-designer:design-tokens-transformer`에 위임** |
| 6 | FROZEN Rules | 스타일 가이드 PDF·브랜드 규정에서 금지 항목 추출. 없으면 사용자 질의(임의 창작 금지). WCAG 대비는 팔레트에서 자동 계산 |
| 7 | Voice & copy patterns | 실제 카피 코퍼스에서 선호/금지 어휘·격식체·이모지 빈도 관찰. `moai-marketer:content-copywriting` 보조 |
| 8 | Component recipes | 코드 repo 컴포넌트·라이브 DOM에서 자주 쓰는 패턴을 **토큰 변수 참조형 CSS 스니펫**으로 축약 |
| 9 | Asset index | 로고·이미지를 변형별 분류(가로/정사각/마스코트/화이트 녹아웃)하고 용도 지정 |
| 10 | Upload guide | 2~9 산출물을 업로드 순서로 정렬. 자동/수동 경로는 **`moai-designer:design-sync-upload`에 위임** |

원칙: 관측된 자산에서 **도출**하되, 자산에 없는 값을 추측으로 채우지 않는다 — 불명확한 항목은 사용자에게 질의하거나 "미확정"으로 남긴다.

다음 10-섹션 구조로 DESIGN.md를 작성합니다.

```markdown
# [브랜드명] Design System

## 1. Brand voice & personality
[형용사 5-7개 + 한 문단 — 브랜드 성격]

## 2. Color palette
### Primary scale (50–950)
- primary/500: #RRGGBB — [의미]  (예: 600=라이트 주색, 500=다크 주색 명시)
- 50·100 … 900·950 (11단계 휘도 스케일)
### Secondary · Accent
- [보조·강조색]: #RRGGBB
### Semantic
- success · warning · error · info: #RRGGBB
### Signature asset
- [시그니처 그라디언트·패턴 등 브랜드 코어 자산] 예: linear-gradient(135deg, #A 0%, #B 100%)

## 3. Typography
- family: Display/Heading/Body/Mono [폰트 이름]
- weight: [사용 굵기 — 예 400/700/900]
- size / lineHeight: [스케일]
- Letter-spacing rules: display −0.05em · body −0.025em · caption 0 (한국어 자간)
- Weight-contrast pattern: [한 문장 안에서 굵기 대비로 핵심어를 강조하는 규칙]

## 4. Spacing / Radius / Shadow / Motion
- Spacing: 4px 베이스 — 4·8·12·16·24·32·48·64
- Radius: none/sm/md/lg/xl/full
- Shadow: sm/md/lg (+ 시그니처 글로우)
- Motion: duration(fast/normal/slow) + easing(default/bounce/smooth)

## 5. Token 3-layer mapping
- L1 DTCG SSOT: `$value`/`$type`/`$description` (provenance 기록)
- L2 CSS vars: `--color-*`·`--tracking-*`·`--space-*` …
- L3 semantic roles: `--base-*` (shadcn) + `.dark` 전환
> 변환·검증은 `moai-designer:design-tokens-transformer`로 수행

## 6. FROZEN Rules
- 금지 규칙: [소스가 선언한 것만 — 예: 특정 색/그라디언트/폰트 금지]
- Letter-spacing: [자간 규칙 준수 조건]
- WCAG contrast: 본문 ≥ 4.5:1(AA), 큰 텍스트 ≥ 3:1 (팔레트에서 자동 계산)
- Illustration/mascot policy: [허용/금지 영역 — 예: 정서 화면 허용, 데이터·결제 화면 금지]

## 7. Voice & copy patterns
- 선호 어휘 / 금지 어휘(AI 슬롭·진부 표현)
- 격식 레지스터: [존댓말·반말·친근체 정책]
- 이모지 정책: [사용/금지]

## 8. Component recipes
- Primary CTA / Card / Sticky nav / Empty state / Section eyebrow
  — 토큰 변수 참조형 CSS 스니펫(아래 예시 참조)

## 9. Asset index
| 변형 | 용도 |
|---|---|
| 가로형(horizontal) | 헤더·네비 |
| 정사각(square) | 파비콘·앱 아이콘·소셜 |
| 마스코트(mascot) | 히어로·엠프티·404 (정서 영역) |
| 화이트 녹아웃(-WH) | 어두운/그라디언트 배경 위 |

## 10. Upload guide
- 업로드 순서: DESIGN.md → 토큰 → 로고 변형 → 참고 자산
- 자동/수동 이중 경로 → `moai-designer:design-sync-upload`
- Published 토글: 업로드 후 분석 대기 → 테스트 프롬프트 → 일치 시 ON
```

**섹션 8 — Component recipes 스니펫 (예시, 토큰 변수 참조형)**

```css
/* Primary CTA — pill + 시그니처 배경 */
padding: var(--space-3) var(--space-6); border-radius: var(--radius-full);
background: var(--gradient-signature); color: var(--fg-on-primary);
font-weight: var(--fw-bold); letter-spacing: var(--tracking-body);
/* hover: box-shadow: var(--shadow-signature) */

/* Card — surface */
background: var(--color-surface); border-radius: var(--radius-lg);
padding: var(--space-6); border: 1px solid var(--border-1);
box-shadow: var(--shadow-sm);
/* hover: translateY(-2px) + var(--shadow-md) */

/* Sticky nav (glassy) */
position: sticky; top: 0; backdrop-filter: blur(12px);
background: color-mix(in srgb, var(--color-bg) 85%, transparent);
border-bottom: 1px solid var(--border-1);

/* Empty state */
/* 일러스트/마스코트(정책 허용 영역) + 위트 카피 + CTA, text-align: center */

/* Section eyebrow */
font-family: var(--font-mono); font-size: var(--text-xs); font-weight: var(--fw-semibold);
color: var(--color-primary); letter-spacing: 0.08em; text-transform: uppercase;
```

스니펫은 하드코딩 값 대신 **토큰 변수**(`var(--…)`)를 참조한다 — 브랜드 값은 5번 3계층 매핑에서 주입되고, 레시피는 구조·패턴만 고정한다.

### 4단계 — 자산 정리 가이드 동봉

DESIGN.md와 함께 **claude.ai/design에 무엇을 어떻게 올릴지** 가이드를 제공합니다. 업로드는 자동(DesignSync MCP)·수동 두 경로가 있으며 실제 실행은 `moai-designer:design-sync-upload`가 담당합니다 — 여기서는 그 스킬이 소비할 우선순위·주의사항만 정리합니다.

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
- DESIGN.md (자동 합성, 10섹션)
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
| `moai-designer:design-tokens-transformer` | 후속: 5번 3계층 토큰 생성·검증 |
| `moai-designer:design-sync-upload` | 후속: 10번 자동/수동 업로드 실행 |
| `moai-designer:design-brief` | 후속: 시스템 셋업 후 첫 시안 작성 |
| `moai-designer:design-prompt-builder` | 후속: 특정 영역 디자인 |
| `moai-coworker:collab-brand-identity` | 선행: 브랜드 정체성이 모호할 때 |
| `moai-marketer:content-copywriting` | 보조: voice·copy 패턴 정리 |
| `moai-officer:doc-pptx` | 보조: 잘 만든 자사 PPTX가 없으면 |
