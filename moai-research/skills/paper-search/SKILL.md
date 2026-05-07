---
name: paper-search
description: >
  학술 논문을 통합 검색합니다.
  '논문 찾아줘', '선행연구 조사', 'RISS 검색', 'KCI 논문', '문헌 검토'라고 요청할 때 사용하세요.
  RISS, KCI, DBpia, Google Scholar에서 논문을 검색하고 인용 정보를 정리합니다.
user-invocable: true
version: 2.1.0
---

# 논문 검색 (Paper Search)

## 개요

RISS, KCI, DBpia, Google Scholar 등 주요 학술 데이터베이스에서 논문을 통합 검색하고, 서지정보와 인용 형식을 체계적으로 정리하는 전문 스킬입니다. 선행연구 조사, 문헌 고찰, 참고문헌 정리를 지원합니다.

## 트리거 키워드

- 논문 검색, 논문 찾아줘, 문헌 검색
- 선행연구 조사, 문헌 고찰, 관련 연구 찾기
- RISS 검색, KCI 논문, DBpia
- 학술지, 학위논문, 연구 논문
- 참고문헌 정리, 인용 정보

## 워크플로우

### 1단계: API 키 확인

KCI 논문 검색 API 키가 필요합니다:

```
IF KCI_API_KEY 미설정:
  "KCI 논문 검색을 위해 API 키가 필요합니다.

   발급 방법 (간편):
   1. https://www.data.go.kr/data/3049042/openapi.do 접속
   2. 활용신청 → 자동승인 → 키 발급

   API 키를 입력해 주세요 (또는 '건너뛰기'로 웹검색만 사용):"

  → '건너뛰기' 시: RISS/DBpia/Google Scholar 웹검색으로 진행
  → 키 입력 시: ${CLAUDE_PLUGIN_DATA}/moai-credentials.env에 KCI_API_KEY 저장
```

### 2단계: 검색 전략 수립

- 핵심 키워드 추출 (한국어 + 영어 동시 검색)
- 검색 범위 결정 (국내/해외, 연도 필터)
- 분야 필터 (KCI 분류코드)
- 검색 소스 우선순위 결정

### 3단계: 통합 검색 실행

| 검색 소스 | URL | 검색 방법 | 특징 |
|----------|-----|----------|------|
| KCI | kci.go.kr | REST API (WebFetch) | 인용색인, 학술지 평가 (API 키 필요) |
| RISS | riss.kr | WebSearch | 학위논문, 해외 DB 연계 |
| DBpia | dbpia.co.kr | WebSearch | 전 분야 학술지 |
| Google Scholar | scholar.google.com | WebSearch | 글로벌 학술 검색 |

**KCI API 호출 예시 (키 있을 때):**
```
GET https://open.kci.go.kr/po/openapi/openApiSearch.kci
  ?apiCode=articleSearch
  &key={KCI_API_KEY}
  &title={검색어}
```

### 4단계: 검색 결과 정리

- 논문 목록 (제목, 저자, 학술지, 연도, 인용수)
- 핵심 논문 3-5편 선별 및 초록 요약
- 연구 동향 파악 (연도별 추세, 주요 연구자)
- 참고문헌 정리 (BibTeX, RIS, 텍스트 형식)

### 5단계: 후속 작업 제안

- "논문 작성" → moai-research:paper-writer 스킬 연계
- "참고문헌 포맷 변환" → APA/KCI/IEEE 포맷 자동 생성

## 사용 예시

```
"딥러닝 기반 이미지 분류 관련 논문을 찾아줘. 최근 5년 내로."
"자연어 처리 선행연구 조사해줘. 특히 트랜스포머 모델 관련."
"KCI 등재 학술지에서 '머신러닝' 키워드 논문 검색해줘."
"의료 영상 진령 관련 연구 동향 파악해줘."
```

## 출력 형식

- 논문 목록 테이블 (제목, 저자, 학술지, 연도, 인용수)
- 핵심 논문 요약 (초록 기반)
- 연구 동향 분석 (연도별 추세, 주요 연구자)
- 참고문헌 정리 (선택 포맷: BibTeX, RIS, 텍스트)

## 주의사항

- KCI API 키가 없는 경우, 웹검색으로 대체합니다. 웹검색은 API에 비해 결과 수와 정확도가 낮을 수 있습니다.
- KCI API 키는 data.go.kr에서 무료로 발급받을 수 있습니다 (활용신청 후 자동승인).
- 학술 DB 접근 권한에 따라 일부 논문의 전문 텍스트를 확인하지 못할 수 있습니다. 이 경우 서지정보만 제공됩니다.
- 논문 작성이 필요한 경우 paper-writer 스킬로 연계하여 참고문헌 인용 포맷을 자동 생성할 수 있습니다.

## 관련 스킬

- **moai-research:paper-writer** - 논문 작성 및 참고문헌 포맷팅
- **moai-research:grant-writer** - 연구비 신청서 선행연조사 섹션 작성
- **moai-data:data-visualizer** - 연구 동향 시각화 (연도별 추세 차트)

## API 발급 안내

**KCI API (한국연구재단 인용색인)**
- 발급처: https://www.data.go.kr/data/3049042/openapi.do
- 비용: 무료
- 한도: 1,000회/일
- 인증 방식: ServiceKey 파라미터