# moai-office

문서 생성 플러그인 — PPT 디자인(PPTX), Word(DOCX), Excel(XLSX), 한글(HWPX), **다국어 PDF**.

Pretendard+명조 기반 한국형 디자인과 OWPML 표준을 지원합니다. python-docx, python-hwpx, pptxgenjs, openpyxl, PyMuPDF 기반으로 편집 가능한 파일을 직접 생성합니다. PDF는 Noto Sans CJK 폰트 자동 다운로드로 한·중·일·영 깨짐을 근본 해결합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [pptx-designer](./skills/pptx-designer/) | pptxgenjs 코드 생성. 발표자료, 보고서, 기안서, 피칭 덱 슬라이드 | 3 | ✅ |
| [hwpx-writer](./skills/hwpx-writer/) | python-hwpx + lxml 기반 OWPML HWPX 생성. 공문서, 기안서, 보고서 | 2 | ✅ |
| [docx-generator](./skills/docx-generator/) | python-docx 기반 보고서, 계약서, 공문서, 제안서 DOCX 생성 | 0 | ✅ |
| [xlsx-creator](./skills/xlsx-creator/) | openpyxl 기반 데이터 표, 차트, 수식, 조건부 서식 XLSX 생성 | 0 | ✅ |
| [pdf-writer](./skills/pdf-writer/) | PyMuPDF + Noto Sans CJK 자동 다운로드. 한·중·일·영 다국어 PDF 생성 (Markdown/JSON/HTML/Text 입력) | 1 | ✅ |

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

Settings > Plugins > cowork-plugins에서 `moai-office` 선택

## 오픈소스 및 의존성

| 패키지 | 용도 | 설치 | 라이센스 |
|--------|------|------|---------|
| [python-hwpx](https://github.com/airmang/python-hwpx) | HWPX 생성/편집/양식채우기 | `pip install python-hwpx` | Custom |
| [openpyxl](https://openpyxl.readthedocs.io/) | Excel(XLSX) 생성 | `pip install openpyxl` | MIT |
| [python-pptx](https://python-pptx.readthedocs.io/) | PPT 이미지 삽입 | `pip install python-pptx` | MIT |
| [olefile](https://olefile.readthedocs.io/) | HWP 바이너리 추출 | `pip install olefile` | BSD |
| [lxml](https://lxml.de/) | XML 파싱 (python-hwpx 의존) | 자동 설치 | BSD |
| [pptxgenjs](https://gitbrent.github.io/PptxGenJS/) | PPT 슬라이드 생성 | npm/인라인 | MIT |
| [Deno](https://deno.land/) | DOCX TypeScript 스크립트 | 별도 설치 | MIT |
| [PyMuPDF](https://pymupdf.readthedocs.io/) | PDF 생성/렌더링/폰트 임베딩 | `pip install pymupdf` | AGPL/Commercial |
| [Noto Sans CJK](https://github.com/notofonts/noto-cjk) | PDF 한·중·일·영 폰트 (자동 다운로드) | `download_fonts.py` | SIL OFL 1.1 |

### 참고 문서
- [한컴테크 HWPX 포맷 구조](https://tech.hancom.com/hwpxformat/)
- [OWPML 스펙 (KS X 6101)](https://www.hancom.com/support/downloadCenter/hwpOwpml)
- [python-hwpx GitHub](https://github.com/airmang/python-hwpx)
- [hwpx-skill (양식 채우기)](https://github.com/airmang/hwpx-skill)
