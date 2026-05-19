# PPTX QA Checklist — 자동·시각 검수

PPTX 출력 직전 다음을 점검합니다.

## 자동 검수 (코드 레벨)

### 1. 빈 플레이스홀더 잔존

```javascript
import PptxGenJS from "pptxgenjs";
import fs from "fs";

const placeholderPattern = /\{[^}]+\}/g;
slides.forEach((slide, i) => {
  slide.objects.forEach(obj => {
    if (obj.text && placeholderPattern.test(obj.text)) {
      console.warn(`⚠️ Slide ${i+1}: 미치환 플레이스홀더 ${obj.text}`);
    }
  });
});
```

### 2. 텍스트 overflow (슬라이드 영역 초과)

기준: 16:9 (1920×1080 = 13.33×7.5 inch)

```javascript
// 텍스트 박스 좌표·크기 검증
slides.forEach((slide, i) => {
  slide.objects.forEach(obj => {
    if (obj.options && obj.options.text) {
      const x = obj.options.x;
      const y = obj.options.y;
      const w = obj.options.w;
      const h = obj.options.h;
      if (x + w > 13.33 || y + h > 7.5) {
        console.warn(`⚠️ Slide ${i+1}: 텍스트 박스가 슬라이드 영역 초과`);
      }
    }
  });
});
```

### 3. 색 대비 4.5:1 이상

| 조합 | 대비 비율 | 통과 |
|---|---|---|
| Dark `#141413` on Beige `#faf9f5` | 13.5:1 | ✅ |
| Dark `#141413` on White `#ffffff` | 18.4:1 | ✅ |
| Orange `#d97757` on Beige | 3.0:1 | ❌ 본문 NG (헤딩 large text는 OK) |
| Orange on White | 3.7:1 | ⚠️ 24pt 이상만 |
| Mid Gray `#b0aea5` on White | 2.3:1 | ❌ 본문 NG (캡션 회피) |
| Crail `#c15f3c` on Pampas `#f4f3ee` | 4.1:1 | ⚠️ 큰 텍스트만 |

본문(20pt 미만) 텍스트는 반드시 Ink Dark 사용. 강조색은 헤딩(24pt+)에만.

### 4. 폰트 화이트리스트

```javascript
const ALLOWED_FONTS = [
  'Pretendard', '맑은 고딕', 'Inter', 'Lora',
  'D2Coding', 'JetBrains Mono', 'Poppins', 'Georgia'
];

slides.forEach((slide, i) => {
  slide.objects.forEach(obj => {
    if (obj.options && obj.options.fontFace) {
      if (!ALLOWED_FONTS.includes(obj.options.fontFace)) {
        console.warn(`⚠️ Slide ${i+1}: 비표준 폰트 ${obj.options.fontFace}`);
      }
    }
  });
});
```

### 5. 슬라이드 마스터 일관 적용

- 모든 슬라이드가 `masterName` 지정
- 페이지 번호·로고·푸터 동일 위치
- 배경색 일관

---

## 시각 검수 (PDF/JPEG 변환 후)

### 6. LibreOffice CLI로 변환

```bash
# PPTX → PDF
libreoffice --headless --convert-to pdf output.pptx

# PPTX → JPEG (각 슬라이드)
libreoffice --headless --convert-to jpg output.pptx

# 또는 모든 슬라이드를 한 PDF로
unoconv -f pdf output.pptx
```

### 7. 시각 검수 항목

| 항목 | 확인 |
|---|---|
| 색 일관성 | 모든 슬라이드가 같은 팔레트 |
| 텍스트 정렬 | 헤딩·본문·캡션 정렬 통일 |
| 여백 일관 | 슬라이드 간 여백 동일 |
| 페이지 번호 | 모든 슬라이드에 |
| 아이콘 일관 | Outline vs Filled 통일 |
| 사진 비율 | 정사각·정원 통일 |
| 한국 폰트 | 한국 본문에 영문 폰트 단독 X |
| 차트 색 | 팔레트 색만 사용 |
| 표·그리드 | 칸 정렬 정확 |
| 다크/라이트 | 사용한 팔레트 톤과 일치 |

### 8. AI 슬롭 카피 검출

`moai-design:claude-design-slop-check` 또는 `moai-content:humanize-korean` 체이닝.

영문 Tier 1 슬롭 — 발견 시 수정 권장:
- "Reimagine your X"
- "Unleash your X"
- "Empower your team"
- "Transform the way you X"

한국어 Tier 1 슬롭:
- "혁신적인 X"
- "차세대 X"
- "재정의하는 X"
- "한 차원 높은 X"

### 9. 청중·톤 적합성 (사람 검수)

- 임원 발표에 캐주얼 톤 사용 X
- 격식 공문서에 강조색 남발 X
- 마케팅에 흑백만 사용 X
- 청중 연령·전문성에 맞는 폰트 사이즈 (50대 청중은 본문 24pt+)

### 10. 발표 환경 시뮬레이션

- 프로젝터 색 출력 (저채도화 가능)
- 회의실 거리 (32-40 ft) 가독성 — 본문 18pt+
- 영상 회의(Zoom·Meet) 화면 캡처 화질
- 인쇄 출력 (필요 시 — 검은색 본문 권장)

---

## 자동 검수 통합 스크립트

```javascript
// qa-runner.js
import PptxGenJS from "pptxgenjs";

function qaPPTX(slides) {
  const report = { passed: [], warnings: [], errors: [] };

  // 1. 플레이스홀더
  // 2. 텍스트 overflow
  // 3. 색 대비
  // 4. 폰트 화이트리스트
  // 5. 마스터 일관

  return report;
}

// 사용
const slides = pptx.slides;
const report = qaPPTX(slides);
console.log(`✅ Passed: ${report.passed.length}`);
console.log(`⚠️ Warnings: ${report.warnings.length}`);
console.log(`❌ Errors: ${report.errors.length}`);
```

## 통과 기준

| 항목 | 통과 |
|---|---|
| 1. 플레이스홀더 | 0건 (필수) |
| 2. Overflow | 0건 (필수) |
| 3. 색 대비 | 4.5:1 이상 (필수) |
| 4. 폰트 | 화이트리스트 내 (권장) |
| 5. 마스터 일관 | 100% (필수) |
| 6. 시각 검수 (PDF) | 사람 OK (필수) |
| 7. 시각 검수 (항목) | 9/10 이상 (권장) |
| 8. AI 슬롭 | 0건 또는 의도된 사용 (권장) |
| 9. 청중·톤 | 사람 OK (필수) |
| 10. 발표 환경 | 시뮬레이션 OK (권장) |

**필수 5개 모두 통과 시 출력**. 권장 5개 중 1개 이상 실패 시 사용자 확인.

---

## 시각 검수 도구

| 도구 | 용도 |
|---|---|
| LibreOffice CLI | PPTX → PDF/JPEG 변환 |
| ImageMagick | 슬라이드 이미지 색·대비 분석 |
| 색 대비 계산기 | https://webaim.org/resources/contrastchecker/ |
| WCAG 색 시뮬레이터 | 색맹·약시 시각 시뮬레이션 |
| Claude Code subagent | 슬라이드 이미지 LLM 검수 (Anthropic 공식 패턴) |

Claude Code subagent 검수 예시:

```
이미지를 Claude에게 첨부하고:
"이 슬라이드를 검수해 줘. 다음을 확인:
1. 텍스트가 슬라이드 밖으로 잘리지 않았는가
2. 색 대비가 충분한가
3. 텍스트 정렬이 어긋나지 않았는가
4. AI 슬롭 표현이 없는가"
```
