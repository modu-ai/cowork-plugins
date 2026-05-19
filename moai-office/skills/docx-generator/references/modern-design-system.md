# Modern Design System — Claude Brand Theme

Anthropic 공식 브랜드 톤을 기반으로 한 한국 비즈니스 문서용 모던 디자인 시스템입니다.

## 1. 색 팔레트

### 1-1. Core (Claude Modern Doc)

| 토큰 | 이름 | hex | 용도 |
|---|---|---|---|
| `--cm-primary` | Anthropic Orange | `#d97757` | 강조 헤딩·차트 highlight·구분선 |
| `--cm-secondary` | Anthropic Blue | `#6a9bcc` | 보조 강조·인용·표 헤더 |
| `--cm-tertiary` | Anthropic Green | `#788c5d` | 성공·완료·체크 표시 |
| `--cm-coral` | Crail (Product UI) | `#c15f3c` | 적극적 톤·CTA 강조 |
| `--cm-bg` | Light Beige | `#faf9f5` | 본문 배경 (대신 #ffffff도 가능) |
| `--cm-surface` | White | `#ffffff` | 표·코드 블록 배경 |
| `--cm-ink` | Dark | `#141413` | 본문 텍스트 (#000 대체) |
| `--cm-mid` | Mid Gray | `#b0aea5` | 캡션·메타 정보 |
| `--cm-border` | Light Gray | `#e8e6dc` | 표 보더·구분선 |
| `--cm-pampas` | Pampas | `#f4f3ee` | 보조 배경 (sidebar·callout) |

### 1-2. Semantic

| 토큰 | hex | 용도 |
|---|---|---|
| `--cm-success` | `#788c5d` | 성공·완료 |
| `--cm-warning` | `#d9a557` | 주의·검토 필요 |
| `--cm-danger` | `#c44a3a` | 경고·오류·중요 |
| `--cm-info` | `#6a9bcc` | 정보·참고 |

### 1-3. 색 사용 규칙

- 한 문서에 **Primary + Secondary + Background = 3색** + Dark/Light 무채색만
- Primary Orange는 **강조에만** — 본문 전체 도배 금지
- 격식 공문서·계약서는 **Mono Strict** (Dark + White만)
- 명암 대비 **4.5:1 이상** 필수 (본문 Dark on Light Beige = 13.5:1)
- 의미 있는 색만 — 장식 X

## 2. 타이포그래피

### 2-1. 페어링

| 위계 | 한국 | 영문 | 사이즈 | weight | 줄 간격 |
|---|---|---|---|---|---|
| 표지 제목 | Pretendard | Inter | 28pt | Bold | 1.2 |
| H1 | Pretendard | Inter | 22pt | Bold | 1.3 |
| H2 | Pretendard | Inter | 18pt | SemiBold | 1.35 |
| H3 | Pretendard | Inter | 14pt | SemiBold | 1.4 |
| 본문 | Pretendard | Inter | 11pt | Regular | 1.5 |
| 본문 강조 | Pretendard | Inter | 11pt | SemiBold | 1.5 |
| 인용 (Pull Quote) | Pretendard | Lora | 16pt | Regular Italic | 1.4 |
| 캡션 | Pretendard | Inter | 9pt | Regular | 1.2 |
| 표 헤더 | Pretendard | Inter | 10pt | SemiBold | 1.2 |
| 표 본문 | Pretendard | Inter | 10pt | Regular | 1.3 |
| 코드/모노 | D2Coding | JetBrains Mono | 10pt | Regular | 1.4 |

### 2-2. 한국 폰트 우선순위

1. **Pretendard** (오픈소스, 한·영 통일) — 권장 1순위
2. **맑은 고딕** (Windows 기본) — fallback
3. **굴림** (공문서 전통) — 한국 공문서에서만
4. **본문 한글 Serif가 필요할 때**: Noto Serif KR

### 2-3. 폰트 사용 규칙

- 한 문서에 **최대 3개 폰트** (Heading·Body·Mono)
- 한국어 본문에 **영문 Serif (Lora) 단독 사용 금지** — 한국 폰트와 페어
- 굴림은 공문서 외에는 사용 금지 (가독성 떨어짐)
- 폰트 사이즈 단위는 **pt 통일** (px 혼용 금지)

## 3. 간격 (Spacing Scale)

### 3-1. 페이지 여백

| 문서 유형 | 상·하 | 좌·우 |
|---|---|---|
| 한국 공문서 | 30mm | 25mm |
| 모던 보고서 | 25mm | 22mm |
| 모던 제안서 | 22mm | 20mm |
| 컴팩트 (다단 가능) | 20mm | 18mm |

### 3-2. 단락·헤딩 간격

| 항목 | 위 | 아래 |
|---|---|---|
| H1 | 24pt | 12pt |
| H2 | 18pt | 9pt |
| H3 | 12pt | 6pt |
| 본문 단락 | 0 | 6pt |
| 표 위·아래 | 12pt | 12pt |
| 이미지 위·아래 | 12pt | 12pt |
| 캡션 (이미지·표 아래) | 4pt | 12pt |

### 3-3. 표·셀

| 항목 | 값 |
|---|---|
| 셀 패딩 좌우 | 6pt |
| 셀 패딩 상하 | 4pt |
| 보더 두께 | 0.5pt |
| 헤더 행 높이 | 24pt |
| 본문 행 최소 높이 | 20pt |

## 4. 헤딩 위계

```
표지 제목 (28pt Bold, Orange)
  └─ H1 (22pt Bold, Dark)
       └─ H2 (18pt SemiBold, Dark)
            └─ H3 (14pt SemiBold, Mid Gray)
                 └─ 본문 (11pt Regular, Dark)
```

**규칙**:
- H1 → H3 건너뛰기 금지
- H1은 페이지당 1개 (다음 페이지에서 시작 권장)
- 표지 제목과 H1 동시 사용 금지

## 5. 색·타이포 조합 — 좋은 예 / 나쁜 예

### 좋은 예

```
H1 (Pretendard Bold 22pt, Dark) + Orange 좌측 강조선 4pt
본문 (Pretendard Regular 11pt, Dark) 1.5 줄간격
Pull Quote (Lora Italic 16pt, Dark) + Blue 좌측 보더 4pt
표 헤더 (Pretendard SemiBold 10pt, White on Beige)
표 본문 (Pretendard Regular 10pt, Dark on White, zebra Light Beige)
```

### 나쁜 예 — AI 슬롭 패턴

- 모든 헤딩에 Orange 채워 사용 (강조 의미 상실)
- Inter + 맑은 고딕 혼용 (한국 폰트 통일성 깨짐)
- 본문 굴림 12pt 사용 (모던 보고서에 부적합)
- 색 4개 이상 동시 사용 (시각적 노이즈)
- 헤딩 H2 → H4 건너뛰기 (위계 깨짐)
- 표 보더 두께 1pt + 색 Orange (시선 분산)

## 6. 디자인 토큰 export (JSON)

`docx-generator`는 다음 형식의 토큰을 인식합니다.

```json
{
  "color": {
    "primary": "#d97757",
    "secondary": "#6a9bcc",
    "background": "#faf9f5",
    "ink": "#141413",
    "mid": "#b0aea5",
    "border": "#e8e6dc"
  },
  "font": {
    "heading_ko": "Pretendard",
    "heading_en": "Inter",
    "body_ko": "Pretendard",
    "body_en": "Inter",
    "serif": "Lora",
    "mono": "D2Coding"
  },
  "size": {
    "h1": 22,
    "h2": 18,
    "h3": 14,
    "body": 11,
    "caption": 9
  },
  "margin": {
    "top_mm": 25,
    "bottom_mm": 25,
    "left_mm": 22,
    "right_mm": 22
  }
}
```

`docx-generator`에 `--tokens design.json` 옵션으로 전달하면 토큰을 일괄 적용합니다.

---

## Sources

- Anthropic 공식 브랜드 가이드 — Orange #d97757, Light #faf9f5, Dark #141413
- Mobbin Claude UI 분석 — Crail #c15f3c, Pampas #f4f3ee
- 한국 출판·디자인 표준 — Pretendard 가이드라인
- WCAG 2.1 AA 색 대비 — 4.5:1 최소 기준
