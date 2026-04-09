# moai-office

문서 생성 플러그인 — PPT 디자인(PPTX), Word(DOCX), Excel(XLSX), 한글(HWPX).

Pretendard+명조 기반 한국형 디자인과 OWPML 표준을 지원합니다. python-docx, python-hwpx, pptxgenjs, openpyxl 기반으로 편집 가능한 파일을 직접 생성합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [pptx-designer](./skills/pptx-designer/) | pptxgenjs 코드 생성. 발표자료, 보고서, 기안서, 피칭 덱 슬라이드 | 3 | ✅ |
| [hwpx-writer](./skills/hwpx-writer/) | python-hwpx + lxml 기반 OWPML HWPX 생성. 공문서, 기안서, 보고서 | 2 | ✅ |
| [docx-generator](./skills/docx-generator/) | python-docx 기반 보고서, 계약서, 공문서, 제안서 DOCX 생성 | 0 | ✅ |
| [xlsx-creator](./skills/xlsx-creator/) | openpyxl 기반 데이터 표, 차트, 수식, 조건부 서식 XLSX 생성 | 0 | ✅ |

## 에이전트

| 에이전트 | 모델 | 역할 |
|---------|:----:|------|
| document-generator | Sonnet | 500단어 이상 장문 비즈니스 문서 생성. moai-business, moai-legal 등에서 공유 호출 |
| format-converter | Sonnet | HWPX/PPTX/DOCX/XLSX 파일 형식 변환, 템플릿 기반 생성. 전 플러그인에서 공유 호출 |

## 스크립트

| 디렉토리 | 용도 |
|----------|------|
| scripts/docx/ | DOCX 생성 보조 스크립트 |
| scripts/hwpx/ | HWPX 생성 보조 스크립트 |
| scripts/pptx/ | PPTX 생성 보조 스크립트 |
| scripts/xlsx/ | XLSX 생성 보조 스크립트 |

## 사용 예시

```
2026년 상반기 성과 발표 PPT 12장 만들어줘. 깔끔한 미니멀 디자인.
```

```
행정기관 제출용 사업 제안서 한글(hwpx) 파일로 만들어줘
```

```
KPI 대시보드 엑셀로 만들어줘. 차트랑 조건부 서식 포함.
```

## 설치

Settings > Plugins > moai-cowork-plugins에서 `moai-office` 선택
