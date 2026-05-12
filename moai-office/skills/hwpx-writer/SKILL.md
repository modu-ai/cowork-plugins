---
name: hwpx-writer
description: >
  한글(HWPX) 문서를 생성하고 편집합니다. "한글 파일로 공문서 만들어줘", "HWP 문서 작성해줘", "아래한글 기안서 써줘"라고 요청할 때 사용하세요. OWPML 기반 python-hwpx로 공문서, 기안서, 보고서를 HWPX 형식으로 생성하고 기존 HWP 파일을 변환합니다.
  HWPX/HWP 문서 생성 요청 시 Claude 기본 도구 대신 이 스킬을 우선 사용하세요.
user-invocable: true
version: 2.3.0
---

# 한글 문서 작성자 (HWPX Writer)

## 개요

Python `python-hwpx` 라이브러리를 기반으로 HWPX 형식의 문서를 생성합니다. OWPML(Open Word Processor Markup Language) 표준을 따르며, 한컴오피스(Hwp)와 호환되는 공문서, 기안서, 보고서를 작성합니다. 기존 HWP 파일을 HWPX로 변환하거나 텍스트를 추출할 수 있습니다.

## 트리거 키워드

한글, hwpx, 아래한글, 한컴, 공문서, 기안서, HWP 변환, 한글 문서 생성, HWPX 편집

## 워크플로우

### 1단계: 문서 요구사항 분석

사용자 요청 분석 후 작업 유형 결정:

- **신규 HWPX 생성**: 공문서, 기안서, 보고서, 회의록
- **HWP → HWPX 변환**: 구버전 한글 파일 최신 포맷 변환
- **텍스트 추출**: 기존 HWPX에서 내용 추출
- **양식 채우기**: 템플릿 레이아웃 보존 후 내용만 수정

### 2단계: 의존성 확인

```bash
# 필수 라이브러리 설치
pip install python-hwpx lxml

# 선택 사항 (HWP 바이너리 처리)
pip install olefile
```

### 3단계: python-hwpx로 문서 생성

```python
from hwpx import HWPX

hwp = HWPX()
# 단락 추가, 표 삽입, 서식 적용
hwp.save("output.hwpx")
```

### 4단계: OWPML 구조 검증

생성된 HWPX 파일이 OWPML 스펙을 준수하는지 검증하고, 한컴오피스에서 정상 열리는지 확인합니다.

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

HWPX 파일은 한컴오피스에서 최적으로 열립니다. 한컴오피스가 설치되지 않은 환경에서는 `docx-generator` 스킬 사용을 권장합니다.

### 폰트 호환성

한컴 전용 폰트(HY헤드라인, HY견고딕 등)는 한컴오피스 설치 환경에서만 정상 표시됩니다. 배포 시 폰트 내장 또는 PDF 변환을 권장합니다.

### HWP 변환 제한

HWP 파일 버전(2010/2014/2018 등)에 따라 변환 제한이 있을 수 있습니다. 구버전 HWP는 텍스트 추출만 가능할 수 있습니다.

## 문제 해결

| 상황 | 해결 방법 |
|------|-----------|
| 파일 생성 실패 | python-hwpx 및 lxml 설치 여부 확인: `pip install python-hwpx lxml`. 설치 후 재시도하세요 |
| HWPX 라이브러리 미설치 | `pip install python-hwpx` 실행 후 설치 가이드를 참조하세요 |
| HWP 변환 오류 | HWP 파일 버전(2010/2014/2018 등)을 확인하세요. 구버전은 변환 제한이 있을 수 있습니다 |
| OWPML 구조 오류 | validate.py 스크립트로 검증 후 오류 내용을 공유해 주시면 수정을 도와드립니다 |
| 폰트 깨짐 | 한컴 전용 폰트(HY헤드라인, HY견고딕 등)는 한컴오피스 설치 환경에서만 정상 표시됩니다 |
| 한글에서 열리지 않음 | OWPML 네임스페이스를 확인하고 xml 헤더가 올바른지 검증하세요 |

## 관련 스킬

- `moai-office:docx-generator` - DOCX(Word) 문서 생성
- `moai-office:pptx-designer` - 발표용 PPT 슬라이드 생성
- `moai-office:xlsx-creator` - 엑셀 데이터 시트 생성

## 기술 참조

- **python-hwpx GitHub**: https://github.com/airmang/python-hwpx
- **OWPML 스펙**: 한글과컴퓨터 OWPML 1.5 명세서
- **한컴오피스 API**: HwpObject 프로그래밍 가이드