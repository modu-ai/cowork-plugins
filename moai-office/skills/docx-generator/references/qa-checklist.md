# DOCX QA Checklist — 10단계 검수

DOCX 결과물 출력 직전 다음 10단계를 점검합니다. 자동 검수 + 시각 검수가 함께 진행됩니다.

## 자동 검수 (코드 레벨)

### 1. 빈 플레이스홀더 잔존 확인

```python
import re
from docx import Document

doc = Document('output.docx')
remaining = []
for p in doc.paragraphs:
    matches = re.findall(r'\{[^}]+\}', p.text)
    if matches:
        remaining.append((p.text[:50], matches))

if remaining:
    print(f"⚠️ 미치환 플레이스홀더 {len(remaining)}건")
    for text, vars in remaining[:5]:
        print(f"  - {text}... → {vars}")
```

### 2. 페이지 번호 모든 페이지 표기

```python
for section in doc.sections:
    footer = section.footer
    has_page_num = any('PAGE' in p.text or 'page' in str(p._p.xml).lower()
                        for p in footer.paragraphs)
    if not has_page_num:
        print(f"⚠️ Section {doc.sections.index(section)} 페이지 번호 누락")
```

### 3. 헤딩 위계 연속성 (H1 → H3 건너뛰기 금지)

```python
levels = []
for p in doc.paragraphs:
    if p.style.name.startswith('Heading'):
        level = int(p.style.name.split()[-1])
        levels.append(level)

for i, (prev, curr) in enumerate(zip(levels, levels[1:])):
    if curr - prev > 1:
        print(f"⚠️ 헤딩 위계 건너뜀: H{prev} → H{curr} (위치 {i+1})")
```

### 4. 표 보더 일관성

```python
for i, table in enumerate(doc.tables):
    borders = set()
    for row in table.rows:
        for cell in row.cells:
            tc = cell._tc
            tcPr = tc.tcPr
            if tcPr is not None:
                # 보더 색·두께 수집
                borders.add(str(tcPr.xml))
    if len(borders) > 3:
        print(f"⚠️ 표 {i}의 보더 스타일이 일관되지 않음 ({len(borders)} 종)")
```

### 5. 폰트 일관성 (Pretendard 등 외 다른 폰트 사용 확인)

```python
allowed_fonts = {'Pretendard', '맑은 고딕', '굴림', 'Inter', 'Lora',
                 'D2Coding', 'JetBrains Mono'}
used_fonts = set()
for p in doc.paragraphs:
    for run in p.runs:
        if run.font.name:
            used_fonts.add(run.font.name)

unexpected = used_fonts - allowed_fonts
if unexpected:
    print(f"⚠️ 예상 외 폰트 사용: {unexpected}")
```

## 시각 검수 (사람·도구 레벨)

### 6. 색 대비 4.5:1 이상

본문 텍스트와 배경의 명암 대비 확인:

| 조합 | 대비 비율 | WCAG AA |
|---|---|---|
| Dark `#141413` on White `#ffffff` | 18.4:1 | ✅ PASS |
| Dark `#141413` on Light Beige `#faf9f5` | 13.5:1 | ✅ PASS |
| Orange `#d97757` on White | 3.7:1 | ⚠️ 본문 NG (헤딩에만) |
| Mid Gray `#b0aea5` on White | 2.3:1 | ❌ FAIL (캡션이라도 권장 X) |

캡션에는 Mid Gray 대신 **Dark 0.7 투명도** 또는 **#6e6e6e** 권장.

### 7. 이미지 캡션 일관성

- 모든 이미지 아래에 캡션 (그림 1: ..., Figure 1: ...)
- 캡션 정렬 (가운데 또는 좌측 통일)
- 캡션 폰트 (9pt Mid Gray) 통일

### 8. 단락 간 여백 일관성

- 빈 줄(엔터) 사용 금지 — 단락 간 여백은 `space_after`로 처리
- 본문 단락 간 6pt
- 헤딩 위·아래 12·6pt

```python
for p in doc.paragraphs:
    if not p.text.strip() and not p.style.name.startswith('Heading'):
        print(f"⚠️ 빈 단락 발견 — space_after로 대체 권장")
```

### 9. 표 셀 텍스트 줄바꿈 정상

- 셀 안에서 자연스럽게 줄바꿈
- overflow로 셀이 잘리지 않음
- 표 너비가 페이지 너비를 초과하지 않음

수동 확인 또는 LibreOffice CLI로 변환 후 PDF 시각 확인:
```bash
libreoffice --headless --convert-to pdf output.docx
```

### 10. AI 슬롭 표현 없음

본문에 다음 진부 표현이 있으면 검출:

**한국어 Tier 1 (거의 항상 슬롭)**:
- "혁신적인", "차세대", "재정의하는"
- "새로운 패러다임", "AI 기반의"
- "한 차원 높은", "지금까지 없던"

**영문 Tier 1**:
- "Reimagine your X"
- "Unleash your X" / "Unleash the power of"
- "Empower your team"
- "Transform the way you X"

```python
SLOP_PATTERNS_KO = [
    r'혁신적인?', r'차세대', r'재정의(하는|된)',
    r'새로운\s*패러다임', r'AI\s*기반의?',
    r'한\s*차원\s*높은', r'지금까지\s*없던',
]
SLOP_PATTERNS_EN = [
    r'Reimagine\s+your', r'Unleash\s+(your|the\s+power)',
    r'Empower\s+(your|teams?)', r'Transform\s+the\s+way',
]

for p in doc.paragraphs:
    text = p.text
    for pat in SLOP_PATTERNS_KO + SLOP_PATTERNS_EN:
        if re.search(pat, text, re.IGNORECASE):
            print(f"⚠️ AI 슬롭 의심: '{re.search(pat, text).group()}' in '{text[:50]}...'")
```

권장: 후속으로 `moai-design:claude-design-slop-check` 또는 `moai-content:humanize-korean` 스킬 호출.

---

## 자동 검수 통합 스크립트

전체 10단계를 한 번에 실행:

```python
def qa_docx(filepath: str) -> dict:
    """DOCX 10단계 검수 — passed·warnings 보고."""
    doc = Document(filepath)
    report = {'passed': [], 'warnings': [], 'errors': []}

    # 1. 플레이스홀더
    # 2. 페이지 번호
    # 3. 헤딩 위계
    # 4. 표 보더
    # 5. 폰트
    # 6. 색 대비 (수동 권장)
    # 7. 캡션 일관성
    # 8. 빈 단락
    # 9. 표 overflow (수동)
    # 10. AI 슬롭

    # ... (위 코드 통합)
    return report
```

## 통과 기준

| 항목 | 통과 |
|---|---|
| 1. 빈 플레이스홀더 | 0건 (필수) |
| 2. 페이지 번호 | 모든 페이지 (필수) |
| 3. 헤딩 위계 | 건너뛰기 0건 (필수) |
| 4. 표 보더 | 일관 (권장) |
| 5. 폰트 | 화이트리스트 내 (권장) |
| 6. 색 대비 | 4.5:1 이상 (필수) |
| 7. 캡션 | 모든 이미지 (필수) |
| 8. 빈 단락 | 0건 (권장) |
| 9. 표 overflow | 없음 (필수) |
| 10. AI 슬롭 | 0건 또는 의도된 사용 (권장) |

**필수 6개 모두 통과 시 출력**. 권장 4개 중 1개 이상 실패 시 사용자 확인.
