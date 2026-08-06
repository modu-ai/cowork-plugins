---
name: doc-hwp
description: |
  아래아한글(.hwpx) 문서를 만들어 드립니다 — 한컴오피스에서 열리는 공문서·기안서·품의서·보고서를 작성하고, 기존 HWP 파일을 HWPX로 변환합니다.
  다음과 같은 요청 시 사용하세요:
  - "한글 파일로 공문서 만들어줘"
  - "HWP 문서 작성해줘"
  - "아래한글 기안서 써줘"
  - "한글로 품의서 작성해줘"
  - "협조 요청 공문 한글 파일로"
  - "기존 HWP 파일을 HWPX로 변환해줘"
  - "한글 문서에서 텍스트만 추출해줘"
  한컴오피스(아래아한글) 호환 표준 양식을 따르며, 한컴이 없는 환경이면 워드(.docx) 생성으로 대체할 수 있습니다.
  아래아한글(.hwpx) 문서를 만들 때는 Claude 기본 생성 대신 이 스킬을 사용하세요.
  [책임 경계] vs moai-officer:doc-docx: 이 스킬=한컴 .hwpx 한글 파일, 저 스킬=MS 워드 .docx 파일.
version: "1.0.0"
---

# 한글 문서 작성자 (HWPX Writer)

## 개요

HWPX 형식의 문서를 생성합니다. HWPX는 OWPML(Open Word Processor Markup Language) XML을 담은 ZIP이므로, `python-hwpx` 라이브러리가 있으면 그 API로(경로 A), 없으면 Python stdlib `zipfile`로 XML을 직접 조립해(경로 B) 만듭니다. 한컴오피스(Hwp)와 호환되는 공문서·기안서·보고서를 작성하고, 기존 HWP 파일을 HWPX로 변환하거나 텍스트를 추출할 수 있습니다.

## 트리거 키워드

한글, hwpx, 아래한글, 한컴, 공문서, 기안서, HWP 변환, 한글 문서 생성, HWPX 편집

## 워크플로우

### 1단계: 문서 요구사항 분석

사용자 요청 분석 후 작업 유형 결정:

- **신규 HWPX 생성**: 공문서, 기안서, 보고서, 회의록
- **HWP → HWPX 변환**: 구버전 한글 파일 최신 포맷 변환
- **텍스트 추출**: 기존 HWPX에서 내용 추출
- **양식 채우기**: 템플릿 레이아웃 보존 후 내용만 수정

### 2단계: 서식 결정 + 생성 경로 결정

**서식 결정 (공문·기안문·품의서 등 정형 문서일 때 필수)**: `references/kr-official-forms.md`를 로드해 두문·본문·결문 구조, 문서번호, 시행일자(`YYYY. M. D.`), 수신·경유, 항목 번호체계(`1.→가.→1)→가)`), `붙임 n부. 끝.`, 발신명의, 결재란·전결 표기를 서식대로 적용합니다. 구체 레이아웃(여백·폰트·플레이스홀더)은 `references/templates/` 아래 템플릿(공문 gonmun·보고서 report·회의록 minutes·제안서 proposal, 공통 base)을 사용합니다.

**생성 경로 결정 (두 경로 중 택1)**

- **경로 A — python-hwpx가 환경에 있으면 사용** (있으면 편리, 없으면 경로 B):
  ```bash
  python -c "import hwpx" 2>/dev/null && echo "python-hwpx 사용 가능" || echo "경로 B(직접 XML 조립) 사용"
  # 없고 설치 가능하면: pip install python-hwpx lxml  (HWP 바이너리 처리 시 olefile 추가)
  ```
- **경로 B — 라이브러리 없이 ZIP+XML 직접 조립** (기본 경로): HWPX는 OWPML(XML) 파일들을 담은 ZIP이므로
  Python stdlib `zipfile`만으로 조립할 수 있습니다. 3단계 인라인 코드를 그대로 실행합니다.

### 3단계: 문서 생성

**경로 A (python-hwpx 있을 때):**

```python
from hwpx import HwpxDocument

hwp = HwpxDocument.new()
# 단락 추가·표 삽입·서식 적용은 python-hwpx API(add_paragraph, add_table 등)로 수행
hwp.save("output.hwpx")
```

**경로 B (stdlib만, 기본 경로):** HWPX = ZIP(`mimetype` + `version.xml` + `Contents/content.hpf` +
`Contents/section0.xml` 등)을 `zipfile`로 직접 씁니다. 최소 골격:

```python
import zipfile

# section0.xml — OWPML 본문(단락·표). 실제로는 <hp:p> 단락, <hp:tbl> 표를 필요한 만큼 채웁니다.
section = """<?xml version="1.0" encoding="UTF-8"?>
<hs:sec xmlns:hs="http://www.hancom.co.kr/hwpml/2011/section"
        xmlns:hp="http://www.hancom.co.kr/hwpml/2011/paragraph">
  <hp:p><hp:run><hp:t>여기에 본문 단락 텍스트</hp:t></hp:run></hp:p>
</hs:sec>"""

with zipfile.ZipFile("output.hwpx", "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("mimetype", "application/hwp+zip")           # 반드시 첫 엔트리
    z.writestr("version.xml", '<?xml version="1.0"?><hv:HCFVersion xmlns:hv="http://www.hancom.co.kr/hwpml/2011/version"/>')
    z.writestr("Contents/section0.xml", section)
    # 실제 배포용은 header.xml(글꼴·문단모양)·content.hpf(패키지 매니페스트)를 함께 채웁니다.
```

> 경로 B는 최소 골격입니다. 서식·표·머리글 등 복잡한 문서는 python-hwpx(경로 A) 사용을 권장하며,
> 라이브러리가 없으면 위 XML을 OWPML 스펙에 맞춰 단락·표 요소를 확장해 조립합니다.

### 4단계: OWPML 구조 검증

생성한 HWPX가 OWPML 스펙을 준수하는지 stdlib로 직접 검증합니다 — ZIP 무결성·필수 XML well-formed 여부를 확인합니다:

```python
import zipfile, xml.etree.ElementTree as ET

with zipfile.ZipFile("output.hwpx") as z:
    assert z.testzip() is None, "ZIP 손상"
    names = z.namelist()
    assert "mimetype" in names and "Contents/section0.xml" in names, "필수 엔트리 누락"
    ET.fromstring(z.read("Contents/section0.xml"))   # XML well-formed 검증 (실패 시 ParseError)
print("OWPML 기본 구조 OK — 한컴오피스에서 최종 열림 여부는 사용자가 확인")
```

## 사용 예시

- "공문서 양식으로 협조 요청 한글 파일을 만들어줘"
- "기존 HWP 파일을 HWPX로 변환해줘"
- "아래한글 기안서 형식으로 품의서를 작성해줘"
- "HWPX 파일에서 텍스트를 추출해줘"
- "한글 문서 내용이 올바른 OWPML 구조인지 검증해줘"

## 출력 형식

- **파일 형식**: `.hwpx` (한컴오피스 2010+ 표준)
- **표준**: OWPML 1.5 (Open Word Processor Markup Language)
- **압축**: ZIP 기반 (XML + 리소스 파일)
- **한글 호환**: 한컴오피스 2014, 2018, 2020에서 정상 열림

## 주의사항

### 안정 기능 vs 제한 기능

| 기능 | 상태 | 비고 |
|------|------|------|
| 단락 추가 | 안정 | 기본 기능 |
| 볼드/이탤릭/밑줄 | 안정 | lxml 패치 자동 적용 |
| 테이블 | 안정 | 행/열 제한 없음 |
| 머리글/바닥글 | 안정 | - |
| 각주/미주 | 안정 | - |
| 북마크 | 안정 | - |
| 텍스트 치환 | 안정 | - |
| 도형 (선/사각/타원) | 제한 | 한글에서 오류 경고 발생 가능 |
| 이미지 삽입 | 제한 | 불완전한 pic 요소 생성 |
| 다단 설정 | 제한 | 한글에서 오류 경고 발생 가능 |

### 한컴오피스 환경

HWPX 파일은 한컴오피스에서 최적으로 열립니다. 한컴오피스가 설치되지 않은 환경에서는 `moai-officer:doc-docx` 스킬 사용을 권장합니다.

### 폰트 호환성

한컴 전용 폰트(HY헤드라인, HY견고딕 등)는 한컴오피스 설치 환경에서만 정상 표시됩니다. 배포 시 폰트 내장 또는 PDF 변환을 권장합니다.

### HWP 변환 제한

HWP 파일 버전(2010/2014/2018 등)에 따라 변환 제한이 있을 수 있습니다. 구버전 HWP는 텍스트 추출만 가능할 수 있습니다.

## 문제 해결

| 상황 | 해결 방법 |
|------|-----------|
| 파일 생성 실패 (경로 A) | python-hwpx·lxml 설치 여부 확인(`pip install python-hwpx lxml`) 후 재시도, 또는 3단계 경로 B(stdlib zipfile 조립)로 전환 |
| HWPX 라이브러리 미설치 | python-hwpx가 없으면 3단계 경로 B(라이브러리 없이 ZIP+XML 직접 조립)를 사용하세요 — 설치는 선택입니다 |
| HWP 변환 오류 | HWP 파일 버전(2010/2014/2018 등)을 확인하세요. 구버전은 변환 제한이 있을 수 있습니다 |
| OWPML 구조 오류 | 4단계 인라인 검증 코드(zipfile + ElementTree)로 ZIP 무결성·XML well-formed를 확인하고, 오류 내용을 공유해 주시면 수정을 도와드립니다 |
| 폰트 깨짐 | 한컴 전용 폰트(HY헤드라인, HY견고딕 등)는 한컴오피스 설치 환경에서만 정상 표시됩니다 |
| 한글에서 열리지 않음 | OWPML 네임스페이스를 확인하고 xml 헤더가 올바른지 검증하세요 |

## 관련 스킬 / 자체 검수

한글 문서 생성이 끝나면 산출된 .hwpx 파일을 다시 열어 플레이스홀더 잔존·OWPML 구조·한글 인코딩 깨짐·표 깨짐을 **자체 검수**하고, 문제가 있으면 자동 수정 후 재생성하며 최종 PASS/FAIL 결과를 보고합니다.

- `moai-officer:doc-docx` - DOCX(Word) 문서 생성
- `moai-officer:doc-pptx` - 발표용 PPT 슬라이드 생성
- `moai-officer:doc-xlsx` - 엑셀 데이터 시트 생성

## 기술 참조

- **python-hwpx GitHub**: https://github.com/airmang/python-hwpx
- **OWPML 스펙**: 한글과컴퓨터 OWPML 1.5 명세서
- **한컴오피스 API**: HwpObject 프로그래밍 가이드


## 한국어 카피 품질 게이트 (필수)

본 스킬이 산출하는 한국어 텍스트는 배포 전 의무 게이트를 통과합니다:

1. `moai-coworker:ai-slop-reviewer` — 1차 일반 AI 슬롭 검수 (금지어, 구조 패턴, 리듬)
2. `moai-writer:korean-humanize` — 2차 한국어 정밀 윤문 (40+ 패턴 SSOT, 의미 불변)

두 게이트는 대시 대비 헤드라인·조사·체언 종결 조각문·"A에서 B로" 전환 공식 S1 패턴을 잡아냅니다. 게이트 통과 없이 산출물을 바로 배포하지 않습니다.
> **정형 서식 보호** — 이 스킬의 산출물은 정형 문서다. 슬롭 검수는 금지어 치환만 수행하고, 구조(개조식·항목 번호 체계·두문/본문/결문)는 재작성하지 않는다.


## 상세 레퍼런스

| 파일 | 로드 조건 |
|------|-----------|
| references/kr-official-forms.md | 공문·기안문·품의서 등 정형 문서 작성 시 (워크플로우 2단계 필수 — 두문/본문/결문·항목 번호체계·붙임/끝.·결재란·전결 표기 SSOT) |
| references/guide.md | HWPX 생성 전반의 상세 가이드가 필요할 때 (라이브러리 활용·문서 조립 절차) |
| references/owpml-spec.md | HWPX 편집 시 OWPML XML 네임스페이스·섹션 파일 구조 등 스펙 참조가 필요할 때 |
| references/format-converter.md | HWPX·PPTX·DOCX·XLSX 형식 간 변환·템플릿 기반 문서 생성 에이전트가 필요할 때 |
| references/templates/base.md | 모든 HWPX 템플릿의 공통 페이지·폰트·스타일 기본값이 필요할 때 |
| references/templates/gonmun.md | 공문서(시행문) 생성 시 (「행정 효율과 협업 촉진에 관한 규정」 별지 서식 기반 레이아웃) |
| references/templates/report.md | 보고서 HWPX 생성 시 |
| references/templates/minutes.md | 회의록 HWPX 생성 시 |
| references/templates/proposal.md | 제안서 HWPX 생성 시 |
