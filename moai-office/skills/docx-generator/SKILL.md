---
name: docx-generator
description: |
  편집 가능한 워드(.docx) 문서를 만들어 드립니다 — 보고서, 계약서, 제안서, 공문서, 기획서를 한국형 디자인 톤으로 바로 쓸 수 있게 출력합니다.
  다음과 같은 요청 시 사용하세요:
  - "보고서 워드 파일로 만들어줘"
  - "계약서 DOCX로 작성해줘"
  - "공문서 양식대로 써줘"
  - "제안서 워드 문서 만들어줘"
  - "사업 기획서 docx로 정리해줘"
  - "협조 공문 한 장 작성해줘"
  - "분기 보고서를 깔끔한 톤으로 워드로 뽑아줘"
  Claude 브랜드 톤 기반 모던 디자인 시스템과 한국 공문서 표준 양식을 함께 지원하며, 텍스트가 끝나면 AI 슬롭 검수로 자연스럽게 다듬을 수 있습니다.
  보고서·문서를 워드(.docx) 파일로 만들 때는 Claude 기본 생성 대신 이 스킬을 사용하세요 (서식·디자인 보존).
user-invocable: true
version: 2.27.0
---

# 워드 문서 생성기 (DOCX Generator)

## 개요

Python `python-docx` 라이브러리 기반 DOCX 생성 + **Claude 브랜드 톤 모던 디자인 시스템**.
한국 공문서·기업 보고서·계약서·제안서를 지원하며, 결과물이 "AI가 만든 듯한 진부한 디자인"이 아닌
**프로페셔널한 시안**으로 나오도록 색 팔레트·타이포 위계·간격·구조 패턴이 내장되어 있습니다.

## 트리거 키워드

워드, docx, Word 문서, 계약서, 공문서, 보고서 생성, 문서 편집, 기안문, 제안서, 공문, 협조문, 기획서

## 디자인 시스템 — Claude Modern Doc Theme

`references/modern-design-system.md`에 자세한 색·타이포·간격·헤딩 위계가 정의되어 있습니다.

### 색 팔레트 (Claude 브랜드 톤)

| 역할 | 색 | hex | 사용처 |
|---|---|---|---|
| Primary | Anthropic Orange | `#d97757` | 강조 헤딩·차트 highlight·구분선 |
| Secondary | Anthropic Blue | `#6a9bcc` | 보조 강조·인용·표 헤더 |
| Background | Light Beige | `#faf9f5` | 본문 배경 (대신 #ffffff도 가능) |
| Surface | White | `#ffffff` | 표·코드 블록 배경 |
| Text Primary | Dark | `#141413` | 본문 텍스트 (#000 대체) |
| Text Secondary | Mid Gray | `#b0aea5` | 캡션·메타 정보 |
| Border | Light Gray | `#e8e6dc` | 표 보더·구분선 |

### 타이포그래피 — 한국·영문 페어링

| 위계 | 한국 폰트 | 영문 폰트 | 사이즈 | weight |
|---|---|---|---|---|
| 본문 표지 | Pretendard | Inter | 28pt | Bold |
| H1 | Pretendard | Inter | 22pt | Bold |
| H2 | Pretendard | Inter | 18pt | SemiBold |
| H3 | Pretendard | Inter | 14pt | SemiBold |
| 본문 | Pretendard | Inter / Lora* | 11pt | Regular |
| 캡션 | Pretendard | Inter | 9pt | Regular |
| 코드/모노 | D2Coding | JetBrains Mono | 10pt | Regular |

\* Lora는 Anthropic 공식 본문 폰트. 인용·발췌 영역에 권장.

### 간격·여백

- 페이지: A4 (210×297 mm)
- 여백: 상하 30mm · 좌우 25mm (공문서 표준) / 상하 25mm · 좌우 22mm (모던 보고서)
- 줄 간격: 본문 1.5배 · 캡션 1.2배
- 헤딩 상하: H1 상 24pt 하 12pt · H2 상 18pt 하 9pt · H3 상 12pt 하 6pt
- 단락 간 여백: 6pt
- 표 셀 패딩: 좌우 6pt 상하 4pt

## 워크플로우

### 1단계: 문서 유형 결정

| 유형 | 디자인 톤 | 권장 팔레트 변형 |
|---|---|---|
| 한국 공문서 | 격식·전통 | Classic Mono (Dark + White만) |
| 기업 보고서 | 신뢰·데이터 중심 | Claude Classic (Orange + Beige + Dark) |
| 계약서 | 격식·중립 | Mono Strict (Dark + White) |
| 제안서 | 적극적·시각적 | Claude Coral (Crail + Pampas) |
| 기획서 | 창의·탐색 | Claude Blue (Blue + Beige) |
| 사업계획서 | 임팩트·자신감 | Claude Bold (Orange Highlight + Dark) |

### 2단계: 내용 수집 및 구조화

문서 유형별 표준 구조 (references/modern-templates.md 참고):

**공문서**: 수신처·제목·내용(번호 매기기)·발신 기관명·담당자·연락처·날짜
**계약서**: 갑·을 표시·계약 목적·범위·기간·대금·지적재산권·비밀유지·해지·분쟁 해결·서명란
**제안서**: 표지·요약(Executive Summary)·현황·제안·기대효과·일정·예산·팀
**보고서**: 요약·배경·분석·결론·권고·부록
**기획서**: 배경·목표·전략·실행안·KPI·리스크

### 3단계: python-docx로 문서 생성

```python
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# 페이지 설정 — A4 + 모던 여백
section = doc.sections[0]
section.page_height = Cm(29.7)
section.page_width = Cm(21.0)
section.top_margin = Cm(2.5)
section.bottom_margin = Cm(2.5)
section.left_margin = Cm(2.2)
section.right_margin = Cm(2.2)

# Claude 톤 색
CLAUDE_ORANGE = RGBColor(0xD9, 0x77, 0x57)
CLAUDE_DARK = RGBColor(0x14, 0x14, 0x13)
CLAUDE_MID = RGBColor(0xB0, 0xAE, 0xA5)

# H1 스타일
h1 = doc.styles['Heading 1']
h1.font.name = 'Pretendard'
h1.font.size = Pt(22)
h1.font.bold = True
h1.font.color.rgb = CLAUDE_DARK

# 강조 헤딩 (Primary Orange 사용)
title = doc.add_heading('2026 Q1 사업 보고서', level=0)
for run in title.runs:
    run.font.color.rgb = CLAUDE_ORANGE
    run.font.size = Pt(28)
```

전체 코드 패턴은 `references/modern-templates.md` 참고.

### 4단계: 서식 적용 및 파일 출력

- 단락 스타일 (제목 1-3·본문·인용·캡션)
- 표 (헤더 음영 Light Beige, 보더 Light Gray, 줄 변경 시 zebra striping)
- 이미지 (로고·차트·서명) + 캡션 자동 배치
- 머리글/바닥글 (페이지 번호 우측 하단, 발행처 좌측 하단)
- 플레이스홀더 일괄 치환 (`{변수명}` → 실제 값)

### 5단계: 검수 (10단계 체크리스트)

`references/qa-checklist.md`의 10단계를 자동/반자동 점검:

1. 빈 플레이스홀더 없음 (`{변수명}` 패턴 잔존 확인)
2. 페이지 번호 모든 페이지에 표기
3. 헤딩 위계 연속 (H1 → H3 건너뛰기 없음)
4. 표 경계선 일관 (보더 색·두께 통일)
5. 폰트 깨짐 없음 (Pretendard·맑은 고딕 시스템 폰트 확인)
6. 색 대비 4.5:1 이상 (본문 Dark on Light Beige = 13.5:1 PASS)
7. 이미지 캡션 일관 (위치·형식)
8. 단락 간 여백 일관 (수동 빈 줄 사용 금지)
9. 표 셀 텍스트 줄바꿈 정상 (overflow 없음)
10. AI 슬롭 표현 없음 (혁신적인·차세대·재정의하는 등 — `moai-design:claude-design-slop-check` 체이닝 권장)

## 모던 디자인 패턴 6종

### Pattern 1 — Executive Summary Box

보고서·제안서 첫 페이지에 1-page 요약 박스.

```
┌────────────────────────────────────────┐
│ Executive Summary                      │  ← Orange 강조선
│ ──────────────────────────────────     │
│ [4-5줄 핵심 요약 — 본문보다 약간 큰   ]│
│ [폰트, 좌측 Orange 강조선 4pt]         │
└────────────────────────────────────────┘
```

### Pattern 2 — Pull Quote

본문 중간의 인용 강조.

```
        ┃ "[인용문 — Lora 세리프 16pt 이탤릭]"
        ┃   — 출처 (Mid Gray, 11pt)
```

Anthropic Blue `#6a9bcc` 좌측 보더 4pt + Lora 이탤릭.

### Pattern 3 — Stat Callout

숫자 강조 영역.

```
   [37%]          [2.4배]          [₩1.2억]
   매출 증가      ROI 개선         예상 절감
```

숫자: Orange 36pt Bold · 라벨: Mid Gray 11pt.

### Pattern 4 — Comparison Table

좋은/나쁜·기존/제안 비교.

```
| 기준        | 기존        | 제안         |
| ---        | ---        | ---         |
| Beige 헤더 | White cell | Orange tint |
```

### Pattern 5 — Sidebar Note

본문 옆 메모·주석 박스 (Light Beige 배경).

### Pattern 6 — Section Divider

섹션 사이 시각 구분.

```
─── ⬢ ────────────────────────────────
      Section 2 — 시장 분석
```

Orange 작은 도형 + Mid Gray 가로선 + 섹션 번호.

## 사용 예시

- "용역 계약서 DOCX를 작성해 줘 (갑: A사, 을: B사, 계약금 1,000만 원)" → Mono Strict 팔레트
- "Q1 분기 보고서를 모던 톤으로 만들어 줘" → Claude Classic 팔레트 + Executive Summary Box + Stat Callout 3
- "스타트업 사업계획서 30페이지" → Claude Bold 팔레트 + 6 패턴 활용
- "행정기관 협조 공문" → Classic Mono 팔레트 + 공문서 표준 양식
- "내부 기획서를 발표용으로도 쓸 수 있게" → Claude Blue 팔레트 + Pull Quote + Stat Callout

## 출력 형식

- **파일 형식**: `.docx` (Microsoft Word 2007+ 호환)
- **페이지 설정**: A4 (210mm × 297mm)
- **여백**: 상하 25-30mm, 좌우 22-25mm (문서 유형별)
- **폰트**: Pretendard (한국) + Inter/Lora (영문) · 공문서는 굴림·맑은 고딕
- **색 인코딩**: sRGB
- **인코딩**: UTF-8

## 주의사항

### Claude 톤 색 사용 규칙

- Primary Orange는 강조에만 — 본문 전체에 도배 금지
- 한 문서에 Primary + Secondary + Background = 3색 + Dark/Light 무채색만
- 색 사용은 의미가 있을 때만 (장식 X)

### HWPX 대안 사용

한컴오피스 없는 환경에서 공문서가 필요한 경우 DOCX로 대체 가능합니다. 한컴 변환이 필요한 경우 `moai-office:hwpx-writer` 스킬 참조.

### 공문서 규정 준수

행정안전부 「공문서 작성 규정」 기준 양식을 준수합니다. 격식 공문서에서는 Orange·Blue 강조색을 사용하지 않고 Mono Strict (Dark + White만)로 작성합니다.

### 폰트 및 배포

배포 시 폰트 내장 또는 PDF 변환을 권장합니다. Pretendard는 오픈소스라 임베드 자유. Lora는 Google Fonts 무료.

### 전자서명

디지털 서명 필드 삽입을 지원합니다. Adobe Acrobat 호환 PDF 변환 후 전자서명을 권장합니다.

### 보안

계약서 등 민감 문서는 비밀번호 보호 설정을 권장합니다. 문서 열기 암호와 편집 암호를 각각 설정할 수 있습니다.

## 문제 해결

| 상황 | 해결 방법 |
|---|---|
| 파일 생성 실패 | `pip install python-docx` 설치 후 재시도 |
| 색이 안 나옴 | RGBColor 사용 여부 확인 (`docx.shared.RGBColor`) |
| 폰트 깨짐 | 시스템에 Pretendard 설치 또는 PDF 변환 |
| Heading 스타일 안 먹힘 | `doc.styles['Heading 1']` 직접 수정 |
| 한글 호환 | 굴림·맑은 고딕 fallback 권장 |
| 표 셀 색 안 바뀜 | `_tc.get_or_add_tcPr()` + `OxmlElement('w:shd')` 사용 |
| 페이지 번호 안 들어감 | 머리글·바닥글 영역에 `field` 객체 삽입 |

자세한 트러블슈팅·코드 예시는 `references/modern-templates.md` 참고.

## 관련 스킬 / 자체 검수

문서 생성이 끝나면 산출된 .docx 파일을 다시 열어 플레이스홀더 잔존·페이지/분량 미달·한글 폰트·인코딩 깨짐·표 깨짐을 **자체 검수**하고, 문제가 있으면 자동 수정 후 재생성하며 최종 PASS/FAIL 결과를 보고합니다(검수 항목은 `references/qa-checklist.md` 참고).

| 스킬 | 사용 시점 |
|---|---|
| `moai-office:pptx-designer` | 발표용 슬라이드 생성 (같은 Claude 톤 디자인 시스템 공유) |
| `moai-office:hwpx-writer` | 한컴 한글 문서 생성 (HWPX) |
| `moai-office:xlsx-creator` | 엑셀 데이터 시트 |
| `moai-office:pdf-writer` | PDF 변환·다국어 PDF |
| `moai-content:humanize-korean` | 카피 AI 슬롭 자연화 |
| `moai-core:ai-slop-reviewer` | 텍스트 산출물 슬롭 검수 |
| `moai-design:claude-design-slop-check` | Claude Design 톤과 일관성 검수 |

## 기술 참조

- **python-docx 공식**: https://python-docx.readthedocs.io/
- **행정안전부 공문서 작성 규정**: https://www.mois.go.kr/
- **Anthropic Brand Guidelines**: 본 스킬의 색·타이포는 Anthropic 공식 브랜드 가이드 기반
- **Microsoft Word 파일 형식**: ECMA-376 Office Open XML

## References

- `references/modern-design-system.md` — 색·타이포·간격 디자인 토큰 전문
- `references/modern-templates.md` — 6대 문서 유형별 모던 템플릿 구조
- `references/qa-checklist.md` — 10단계 검수 체크리스트
- `references/document-generator.md` — 한국 비즈니스 문서 생성 가이드 (기존 자료, 유지)
