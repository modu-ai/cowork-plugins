---
name: hwpx-writer
description: >
  한글(HWPX) 문서를 생성하고 편집합니다. "한글 파일로 공문서 만들어줘", "HWP 문서 작성해줘", "아래한글 기안서 써줘"라고 요청할 때 사용하세요. OWPML 기반 python-hwpx로 공문서, 기안서, 보고서를 HWPX 형식으로 생성하고 기존 HWP 파일을 변환합니다.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "active"
  updated: "2026-04-09"
---

# 한글 문서 작성자 (hwpx-writer)

> moai-office v1.0.0 | python-hwpx 실행 모듈

## 참조 자료

- 작성 가이드: `references/guide.md`
- OWPML 스펙: `references/owpml-spec.md`

## 의존성

- `python-hwpx` — HWPX 생성 라이브러리 (권장, `pip install python-hwpx`)
- `olefile` — HWP(바이너리) 텍스트 추출 (선택, `pip install olefile`)
- 미설치 시 내장 XML 폴백으로 동작하나, 한글 호환성이 제한될 수 있음
- GitHub: https://github.com/airmang/python-hwpx

## 안정 기능 vs 제한 기능

| 기능 | 상태 | 비고 |
|------|------|------|
| 단락 추가 | 안정 | 기본 기능 |
| 볼드/이탤릭/밑줄 | 안정 | lxml 패치 자동 적용 |
| 테이블 | 안정 | 행/열 제한 없음 |
| 머리글/바닥글 | 안정 | |
| 각주/미주 | 안정 | |
| 북마크 | 안정 | |
| 텍스트 치환 | 안정 | |
| 도형 (선/사각/타원) | 제한 | 한글에서 오류 경고 발생 가능 |
| 이미지 삽입 | 제한 | 불완전한 pic 요소 생성 |
| 다단 설정 | 제한 | 한글에서 오류 경고 발생 가능 |

## 실행 스크립트

- `${CLAUDE_SKILL_DIR}/scripts/create_hwpx.py` — HWPX 생성 (python-hwpx 기반)
- `${CLAUDE_SKILL_DIR}/scripts/extract_text.py` — 텍스트 추출
- `${CLAUDE_SKILL_DIR}/scripts/extract_hwp.py` — HWP 변환
- `${CLAUDE_SKILL_DIR}/scripts/pack.py` — HWPX 패킹
- `${CLAUDE_SKILL_DIR}/scripts/unpack.py` — HWPX 언패킹
- `${CLAUDE_SKILL_DIR}/scripts/validate.py` — HWPX 검증

## 실행 규칙

1. 사용자 한글 문서 요청 수신
2. `references/guide.md` 로드 → python-hwpx 방법론 확인
3. `references/owpml-spec.md` 참조 → OWPML 구조 검증
4. 적절한 스크립트 실행 → HWPX 생성/편집
5. `--deepthink` 또는 복잡한 문서 구조 → `mcp__sequential-thinking__sequentialthinking` 호출
6. 결과물 생성 후 사용자 검토 요청

## 트리거 키워드

한글, hwpx, 아래한글, 한컴, 공문서, 기안서, HWP 변환, 한글 문서 생성

## 사용 예시

- "공문서 양식으로 협조 요청 한글 파일을 만들어줘"
- "기존 HWP 파일을 HWPX로 변환해줘"
- "아래한글 기안서 형식으로 품의서를 작성해줘"
- "HWPX 파일에서 텍스트를 추출해줘"
- "한글 문서 내용이 올바른 OWPML 구조인지 검증해줘"

## 문제 해결

| 상황 | 해결 방법 |
|------|-----------|
| 파일 생성 실패 | python-hwpx 및 lxml 설치 여부 확인: `pip install python-hwpx lxml`. 설치 후 재시도하세요 |
| HWPX 라이브러리 미설치 | `pip install python-hwpx` 실행 후 `references/guide.md`의 설치 가이드를 참조하세요 |
| HWP 변환 오류 | HWP 파일 버전(2010/2014/2018 등)을 확인하세요. 구버전은 변환 제한이 있을 수 있습니다 |
| OWPML 구조 오류 | validate.py 스크립트로 검증 후 오류 내용을 공유해 주시면 수정을 도와드립니다 |
| 폰트 깨짐 | 한컴 전용 폰트(HY헤드라인, HY견고딕 등)는 한컴오피스 설치 환경에서만 정상 표시됩니다 |

## 이 스킬을 사용하지 말아야 할 때

- **DOCX(Word) 문서 생성** → moai-office:docx-generator 스킬이 더 적합합니다
- **엑셀(XLSX) 문서 생성** → moai-office:xlsx-creator 스킬을 사용하세요
- **PPT 발표자료 생성** → moai-office:pptx-designer 스킬을 사용하세요
- **한컴오피스 미설치 환경에서 최종 편집** → DOCX로 작성 후 한컴 변환을 고려하거나 docx-generator 스킬을 사용하세요
