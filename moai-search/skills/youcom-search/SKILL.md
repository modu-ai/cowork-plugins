---
name: youcom-search
description: |
  You.com Search API로 실시간 웹 검색 결과를 제공합니다.
  다음과 같은 요청 시 사용하세요:
  - "검색해줘", "웹검색", "온라인 검색"
  - "~ 관련 정보 찾아줘", "~について検索して"
  - "최근 ~ 뉴스 알려줘", "~ 관련 최신动向 파악해줘"
  핵심 검색 결과를 제목·URL·스니펫·날짜 형식으로 정리합니다.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "draft"
  updated: "2026-07-14"
---

# 웹 검색 (You.com Search)

## 개요

You.com Search API를 사용하여 실시간 웹 검색 결과를 제공하는 전문 스킬입니다.
 DuckDuckGo·Tavily·Google 등 기존 웹검색과 달리 You.com은 API 키 하나면 바로 사용 가능하며,
 매일 100회 무료 검색(무료 티어)이 가능합니다.

## 트리거 키워드

- 검색해줘, 웹검색, 온라인 검색
- "~ 관련 정보 찾아줘", "~ 알아봐줘"
- "~ 뉴스", "~ 최신 소식"
- "~ 동향 파악해줘", "~ 트렌드"

## 워크플로우

### 1단계: API 키 확인

You.com Search API 키가 필요합니다:

```
IF YOU_SEARCH_API_KEY 미설정:
  "You.com Search API 키가 필요합니다.

   발급 방법:
   1. https://api.you.com 접속 → 회원가입
   2. API 키 발급 (매일 100회 무료 검색)

   API 키를 입력해 주세요:"

  → 키 입력 시: ${CLAUDE_PLUGIN_DATA}/moai-credentials.env에 YOU_SEARCH_API_KEY 저장
  → Step 2로 진행
```

### 2단계: 검색 쿼리 구성

- 사용자의 자연어 질문을 핵심 검색어로 변환
- 한국어 + 영어 동시 검색 권장 (결과 풍부)
- 불용어 제거, 키워드 조합

### 3단계: API 호출

```
POST https://ydc-index.io/v1/search
Headers:
  X-API-Key: ${YOU_SEARCH_API_KEY}
  Content-Type: application/json
Body:
  {
    "query": "{검색어}",
    "count": 10
  }
```

> ⚠️ 엔드포인트 URL과 파라미터는 [공식 OpenAPI 문서](https://you.com/specs/openapi_search_v1.yaml)를 기준으로 확인하세요.

### 4단계: 결과 파싱

- 각 결과에서 제목·URL·설명(스니펫)·페이지 날짜 추출
- Markdown 테이블 형태로 정리
- 결과 없음 시 안내 메시지 반환

### 5단계: 후속 작업 제안

- "자세히 알아봐줘" → 관련 URL 내용을 moai-search:jina-crawler로 크롤링
- "논문 찾아줘" → moai-research:paper-search로 연계
- "통계 보여줘" → moai-public-data:public-data로 연계

## 출력 형식

- 검색 결과 Markdown 테이블 (제목, URL, 스니펫, 날짜)
- 결과 수 표시
- 필요시 관련 스킬 연계 제안

## 사용 예시

```
"生成式 AI 관련 최신 뉴스 검색해줘."
"半导体供应链 最近 新闻 教えて"
"2025년 AI 규제 동향 파악해줘."
```

## 주의사항

- 무료 티어: 매일 100회. 초과 시 `429 Too Many Requests` 발생
- API 키는 ${CLAUDE_PLUGIN_DATA}/moai-credentials.env에 저장하며 절대 코드에 하드코딩하지 않음
- 검색 결과가 없으면 "검색 결과가 없습니다" 반환

## 관련 스킬

- **moai-research:paper-search** — 학술 논문 검색 (RISS/KCI/DBpia)
- **moai-public-data:public-data** — 공공 데이터포털/KOSIS 통계 조회
- **moai-content:content-writer** — 블로그·기사 작성

## API 발급 안내

**You.com Search API**
- 발급처: https://api.you.com
- 비용: 무료 (매일 100회), 유료 플랜 available
- 인증: `X-API-Key` 요청 헤더
- 문서: https://you.com/specs/openapi_search_v1.yaml
