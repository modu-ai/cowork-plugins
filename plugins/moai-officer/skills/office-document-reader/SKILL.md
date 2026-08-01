---
name: office-document-reader
description: |
  한국 공문서(HWP 3.0/5.x·HWPX·HWPML·PDF·XLSX·DOCX)를 마크다운으로 파싱해 드립니다 — 표 완벽 재현, 신구대조표, 양식 필드 추출/자동 채우기, 문서 비교, DRM 배포용 문서 복호화, OCR 연동까지. kordoc MCP의 8개 도구를 호출하므로 별도 설치·API 키가 필요 없습니다(Node.js 18+ 권장).
  다음과 같은 요청 시 사용하세요:
  - "이 HWP 파일 읽어줘", "HWP 문서 내용 알려줘", "한글 파일 텍스트 추출"
  - "공문서 PDF 마크다운으로 변환", "PDF 표 그대로 가져와줘"
  - "두 문서 신구대조표 만들어줘", "개정판 달라진 부분 비교"
  - "신청서 양식 자동 채우기", "공문서 빈칸 채워줘", "양식 필드 추출"
  - "판결문 HWP 텍스트 추출", "엑셀 양식 파싱", "워드 문서 읽어줘"
  - "배포용 HWP 잠금 해제", "DRM 문서 읽기", "스캔 PDF 텍스트화(OCR)"
  본 스킬은 "읽기(파싱)" 전담입니다. 문서 "생성(쓰기)"은 office-pdf-writer·office-hwpx-writer·office-docx-generator·office-xlsx-creator를 사용하세요.
version: "1.0.0"
---

# 한국 공문서 파서 (office-document-reader)

## 역할

관공서·법원·기업에서 쏟아지는 한국 공문서를 마크다운으로 파싱하는 전문가. HWP 3.0(구버전)·HWP 5.x·HWPX·HWPML·PDF·XLSX·DOCX를 지원하며, 표 구조·양식·서식을 보존해 AI가 바로 읽고 분석할 수 있게 만듭니다. 단순 텍스트 추출을 넘어 신구대조표·양식 자동 채우기·DRM 복호화·OCR까지 공문서 처리 전 과정을 자동화합니다.

> 본 스킬은 [`chrisryugj/kordoc`](https://github.com/chrisryugj/kordoc) (MIT, 949★) MCP 서버를 호출합니다. rhwp(MIT)·OpenDataLoader(Apache-2.0)·pdfjs(Apache-2.0)·cfb(Apache-2.0)·JSZip(MIT) OSS를 포함합니다.

## 지원 도구 (kordoc MCP 8개)

| 도구 | 설명 |
| --- | --- |
| `parse_document` | HWP/HWPX/HWPML/PDF/XLSX/DOCX → 마크다운 (메타데이터 포함). 메인 파싱 도구. |
| `detect_format` | 매직 바이트로 포맷 감지(`hwpx`·`hwp`·`hwpml`·`pdf`·`xlsx`·`docx`·`unknown`). 확장자 오용 의심 시 먼저 호출. |
| `parse_metadata` | 메타데이터(제목·작성자·생성일 등)만 빠르게 추출. 전문 파싱 전 사전 확인에 적합. |
| `parse_pages` | 특정 페이지 범위만 파싱(`"1-3"`, `[1, 5, 10]`). 대형 PDF 부분 조회 시 필수. |
| `parse_table` | N번째 테이블만 추출. 표만 필요할 때 전체 파싱 회피. |
| `compare_documents` | 두 문서 비교(신구대조표). HWP↔HWPX 크로스 포맷 지원, 표는 셀 단위 diff. |
| `parse_form` | 양식 필드를 JSON으로 추출(라벨-값 쌍). 공문서 양식 분석·자동화 시작점. |
| `fill_form` | 양식 템플릿에 값 자동 채우기. HWPX 원본 서식(글꼴·크기·정렬) 100% 보존 모드(`hwpx-preserve`) 지원. 체크박스(`□`→`☑`), 괄호 빈칸(`( )`→`(3)`), 어노테이션 채움 지원. |

## 워크플로우

### Step 1 — 포맷 확인 (필요 시)

사용자가 파일을 전달하면 확장자가 확실하지 않은 경우 `detect_format`으로 실제 포맷을 확인합니다. HWP 바이너리인데 HWPML(XML)인 경우 등이 흔한 케이스입니다.

```
IF 확장자 != 실제 포맷 (예: .hwp인데 HWPML XML):
  detect_format로 실제 포맷 감지 → 그 포맷에 맞는 도구로 파싱
```

### Step 2 — 목적에 따른 도구 선택

| 목적 | 도구 | 비고 |
| --- | --- | --- |
| 전체 문서를 마크다운으로 | `parse_document` | 기본 경로. 메타데이터 자동 포함. |
| 제목·작성자만 빠르게 | `parse_metadata` | 전체 파싱 전 사전 확인. |
| 특정 페이지만 (대형 PDF) | `parse_pages` | `pages: "1-3"` 또는 `[1, 5, 10]`. |
| 표만 추출 | `parse_table` | N번째 테이블만. |
| 두 문서 비교 (신구대조표) | `compare_documents` | 크로스 포맷(HWP↔HWPX) 지원. |
| 양식 필드 JSON 추출 | `parse_form` | 라벨-값 매핑. |
| 양식 자동 채우기 | `fill_form` | `hwpx-preserve` 모드로 서식 보존. |

### Step 3 — 결과 정리

- 파싱된 마크다운을 그대로 제공하거나, 필요 섹션만 발췌해 요약.
- 표는 GFM(표준 마크다운 테이블)로 재현; 병합 셀(`colspan`/`rowspan`)이 복잡하면 HTML `<table>`로 출력해 구조 보존.
- `warnings`(`스킵된 요소`, `숨김 텍스트`, `IMAGE_BASED_PDF`)가 있으면 반드시 사용자에게 알림.
- 이미지 기반 PDF(스캔 문서)는 OCR 연동 안내(`IMAGE_BASED_PDF` 에러 코드).

## CLI 대체 옵션

MCP 호출이 불가능한 환경에서는 kordoc CLI를 직접 사용할 수 있습니다. `parse_form`·`fill_form`·`compare_documents`는 CLI에서도 동일하게 동작합니다.

```bash
# 단일 파일 파싱 → 터미널 출력
npx kordoc 사업계획서.hwpx

# 파일로 저장
npx kordoc 보고서.hwp -o 보고서.md

# 일괄 변환
npx kordoc *.pdf -d ./변환결과/

# JSON(구조화 데이터 + 메타데이터)
npx kordoc 검토서.hwpx --format json

# 페이지 범위
npx kordoc 보고서.hwpx --pages 1-3

# 양식 채우기
npx kordoc fill 신청서.hwpx -f '성명=홍길동,주소=서울' -o 결과.hwpx
npx kordoc fill 신청서.hwpx -j values.json -o 결과.hwpx
npx kordoc fill 신청서.hwpx --dry-run        # 필드 목록만 확인

# 폴더 감시 (자동 변환)
npx kordoc watch ./수신함 -d ./변환결과 --webhook https://...
```

> CLI는 MCP 서버와 동일한 엔진을 사용하므로 결과 품질이 동일합니다. 단, AI 에이전트 연동이 필요 없는 단발성 변환·배치 작업에 적합합니다.

## 주요 활용 시나리오

### 1. 공문서·판결문 텍스트 추출
HWP 3.0(구버전 판결문)·HWP 5.x·HWPX 공문서를 마크다운으로 변환해 AI가 읽고 요약·검색할 수 있게 만듭니다. 구버전 한컴 문서(`"HWP Document File V3.00"` 시그니처)도 상용조합형(johab) → 유니코드 변환으로 지원합니다.

### 2. 표 완벽 재현
선 없는 PDF·복잡하게 병합된 HWP 표도 구조를 분석해 정확한 마크다운 테이블로 복원합니다. 선 기반 감지 + 클러스터 기반 fallback + 한국 공문서 key-value 패턴 인식을 단계적으로 적용합니다.

### 3. 신구대조표 자동 생성
개정 전·후 두 문서를 비교해 추가·삭제·수정·변경 없음을 블록 단위로 표시합니다. 표는 셀 단위 diff를 제공합니다. HWP와 HWPX 간 크로스 포맷 비교도 지원합니다.

### 4. 양식 자동 채우기
공문서 양식 템플릿(신청서·보고서)에 값을 넣으면 라벨-값 매핑·체크박스·괄호 빈칸·어노테이션을 자동으로 채웁니다. `hwpx-preserve` 모드는 원본 서식(글꼴·크기·정렬)을 100% 보존합니다.

### 5. DRM 배포용 문서 복호화
관공서에서 배포용으로 잠근 HWP/HWPX 파일을 자동 텍스트 추출합니다. HWPX DRM은 한컴 오피스 COM API(fallback), HWP 5.x 배포용은 AES-128 ECB 복호화(rhwp 알고리즘 포팅)로 처리합니다. Windows + 한컴 오피스 환경에서 별도 설정 없이 동작합니다.

### 6. OCR (이미지 기반 PDF)
스캔 문서·사진 PDF는 `IMAGE_BASED_PDF` 에러 코드와 함께 OCR 연동 안내가 나갑니다. Tesseract·Claude Vision 등 프로바이더를 직접 연결해 텍스트를 추출합니다.

## 응답 컴팩트 규칙

- 파일명 + 감지된 포맷
- 주요 섹션 헤딩(필요 시 첫 3-5개만)
- 표는 마크다운 테이블로 재현(너무 크면 상위 5-10행만 + "전체 N행" 표시)
- `warnings`는 사용자에게 반드시 노출(스킵된 요소, 숨김 텍스트, 이미지 PDF 등)
- 대형 문서(50페이지 이상)는 처음에 `parse_metadata`로 메타데이터만 먼저 보여주고 전체 파싱 여부를 확인

## 책임 분담 (중요)

본 스킬은 **"읽기(파싱)"** 전담입니다. **"생성(쓰기)"**은 아래 페어 스킬을 사용하세요.

| 작업 | 스킬 | 비고 |
| --- | --- | --- |
| HWP/HWPX 문서 **생성**(기안서·품의서·공문) | `moai-officer:office-hwpx-writer` | 한컴오피스 호환 .hwpx 파일 작성 |
| 워드(.docx) 문서 **생성** | `moai-officer:office-docx-generator` | 보고서·계약서·제안서 |
| PDF **생성** | `moai-officer:office-pdf-writer` | weasyprint 엔진, CJK 폰트 임베딩 |
| 엑셀(.xlsx) **생성** | `moai-officer:office-xlsx-creator` | KPI 대시보드·매출 분석표 |
| HWP/HWPX/PDF **읽기·파싱** | **`moai-officer:office-document-reader` (본 스킬)** | kordoc MCP |

예외: `fill_form`은 기존 양식 템플릿의 빈칸을 채우는 동작이므로 본 스킬이 담당합니다(새 문서를 생성하지 않음).

## 이 스킬을 사용하지 말아야 할 때

- **새 문서를 처음부터 작성** → `moai-officer:office-pdf-writer` / `office-hwpx-writer` / `office-docx-generator` / `office-xlsx-creator`
- **HTML·Markdown을 PDF로 변환** → `moai-officer:office-pdf-writer` (weasyprint 엔진)
- **AI 슬롭 제거·윤문** → `moai-writer:korean-spell-check` / `humanize-korean`
- **DART 공시·사업보고서 첨부 PDF 마크다운화** → dart MCP(`get_attachments(mode=extract)`)가 내부적으로 kordoc을 사용하므로 공시 컨텍스트에서는 dart MCP 우선
- **파일 인코딩만 변경**(UTF-8 변환 등) → 일반적인 텍스트 변환 도구 사용

## Prerequisites

사용자 측 필수 시크릿 **없음**. API 키 발급 불필요.

- **Node.js 18+** (사전 설치 권장). MCP 서버가 `npx -y kordoc mcp`로 실행됩니다.
- 첫 실행 시 npm 캐시에 kordoc 패키지가 다운로드됩니다(약 10-30초, 이후 캐시 적중).
- Windows에서 한컴 오피스가 설치된 환경이면 DRM 배포용 HWP/HWPX COM fallback이 추가로 동작합니다(선택).
- `IMAGE_BASED_PDF`(스캔 문서) 파싱은 OCR 프로바이더(Tesseract·Claude Vision 등)를 별도 연결해야 합니다.

## Failure modes

- `ENCRYPTED` — DRM 배포용 문서 + Windows 한컴 오피스 미설치 → COM fallback 불가. 원본 파일 그대로 또는 한컴에서 열어 재저장 안내.
- `ZIP_BOMB` — 악성/손상 ZIP 기반 포맷(HWPX·XLSX·DOCX). 처리 중단.
- `IMAGE_BASED_PDF` — 스캔/사진 PDF로 텍스트 레이어 없음. OCR 연동 필요.
- `UNSUPPORTED_FORMAT` — 지원하지 않는 포맷. 지원 포맷: HWP 3.0/5.x, HWPX, HWPML, PDF, XLSX, DOCX.
- `PARSE_WARNING` — 부분 파싱 실패(개별 페이지). 전체 중단 없이 warnings로 노출.

## 관련 스킬 체이닝

- **after**: `moai-writer:korean-spell-check` — 파싱된 텍스트 맞춤법·문체 교정
- **after**: `moai-analyst:office-data-explorer` — 파싱된 표 데이터 분석
- **after**: `moai-officer:office-pdf-writer` — 파싱된 내용으로 새 PDF 생성
- **after**: `moai-officer:office-hwpx-writer` — 파싱된 내용으로 새 한글 문서 생성
- **after**: `moai-officer:office-docx-generator` — 파싱된 내용으로 새 워드 문서 생성
- **after**: `moai-analyst:office-data-visualizer` — 파싱된 표 데이터 차트 시각화
- **pair**: `moai-officer:office-mcp-connector-setup` — kordoc MCP 사전 준비 가이드

## Done when

- 파일 포맷을 감지하고(detect_format 또는 확장자 기반) 적절한 파싱 도구를 선택했다.
- 요청 목적(전체 파싱·페이지 범위·표 추출·문서 비교·양식 추출·양식 채우기)에 맞는 도구를 호출했다.
- 파싱 결과(마크다운 또는 JSON)를 사용자에게 제공하고, warnings가 있으면 노출했다.
- "읽기 vs 생성" 책임 분담을 지켰다(생성 요청은 writer 스킬로 라우팅).
