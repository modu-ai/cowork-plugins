# moai-search

웹 검색 전담 플러그인 — You.com Search API.

You.com Search API로 실시간 웹 검색 결과를 제공합니다. 매일 100회 무료 검색 가능하며, API 키 하나면 바로 사용할 수 있습니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [youcom-search](./skills/youcom-search/) | You.com Search API 웹 검색 | 0 | ✅ |

## API 키 (필수)

| 서비스 | 환경변수 | 발급처 |
|--------|---------|--------|
| You.com Search | YOU_SEARCH_API_KEY | [api.you.com](https://api.you.com) |

## 주요 워크플로우 체인

```
일반 정보 검색
  youcom-search(검색) → youcom-search(심화 검색) → moai-content:content-writer

논문 선행연구
  youcom-search(웹검색) → moai-research:paper-search(학술 DB)

实时 뉴스 분석
  youcom-search(최신 뉴스) → moai-data:data-visualizer(시각화)
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 학술 논문 검색 | `moai-research:paper-search` |
| 공공 데이터/통계 조회 | `moai-public-data:public-data` |
|DFFF|网页正文 内容抓取|`moai-content:web-content`|

## 설치

Settings > Plugins > cowork-plugins에서 `moai-search` 선택

## 참고자료

| 항목 | URL | 용도 |
|------|-----|------|
| [You.com Search API](https://you.com/specs/openapi_search_v1.yaml) | 공식 문서 | API 스펙 |
| [You.com API 가입](https://api.you.com) | 발급처 | API 키 발급 |
