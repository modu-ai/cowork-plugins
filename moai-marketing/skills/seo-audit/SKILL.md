---
name: seo-audit
description: >
  네이버·구글·AI 검색(GEO) 통합 SEO 감사 및 최적화 전략을 수립합니다.
  'SEO 감사해줘', '네이버 상위 노출 전략 짜줘', '키워드 분석해줘',
  '구글 검색 최적화해줘', 'GEO 전략 만들어줘', 'C-Rank 개선 방법 알려줘'라고 요청하세요.
  온페이지·기술 SEO, 키워드 전략, AI 검색 최적화 보고서를 생성합니다.
user-invocable: true
version: 2.5.0
---

# SEO 감사 (SEO Audit)

## 개요

네이버·구글 양대 검색엔진과 ChatGPT·Perplexity 등 AI 검색(GEO)까지 포괄하는 통합 SEO 감사 및 최적화 전략을 제공합니다.

2026년 핵심 트렌드인 네이버 스마트블록·C-Rank 전문성, 구글 AI Overview, GEO(생성형 검색 최적화)를 반영합니다.

## 트리거 키워드

SEO 감사, 검색최적화, 키워드 분석, 네이버 SEO, 구글 SEO, 온페이지 SEO, 백링크, 검색 순위, C-Rank, DIA, GEO, AI 검색 최적화, 상위노출

## 워크플로우

### 1단계: 감사 범위 확인

대상 URL / 도메인 수집, 목표 플랫폼 선택(네이버/구글/AI 검색(GEO)/전체), 주요 타겟 키워드 3~5개 확인을 수행합니다.

### 2단계: 네이버 SEO 감사 (C-Rank + D.I.A.)

**C-Rank 평가 항목:** 주제 집중도(단일 주제 전문성), 콘텐츠 발행 일관성 및 발행 주기, 사용자 반응 지표(공감, 댓글, 스크랩, 체류시간), VIEW 통합 노출 여부를 확인합니다.

**D.I.A. / D.I.A.+ 평가 항목:** 제목-본문 키워드 적합도, 경험 기반 정보 포함 여부, 글의 구조, 검색 의도(Query Intent) 부합도, AI 생성 콘텐츠 패널티 리스크를 평가합니다.

**2026년 네이버 최신 변화 체크:** 스마트블록 노출 구조, AI 콘텐츠 탐지 패널티 리스크, 네이버TV 영상 콘텐츠 연동 여부, 로컬 SEO(지역 특화 키워드) 대응을 확인합니다.

### 3단계: 구글 SEO 감사 (Core Web Vitals + E-E-A-T)

**기술 SEO:** Core Web Vitals(LCP < 2.5s, FID < 100ms, CLS < 0.1), 모바일 친화성(Mobile-First Index), 사이트맵·robots.txt 설정, HTTPS 보안 인증을 확인합니다.

**콘텐츠 SEO (E-E-A-T):** Experience(경험) · Expertise(전문성) · Authoritativeness(권위) · Trustworthiness(신뢰성), 구조화 데이터(Schema.org) 마크업을 평가합니다.

### 4단계: GEO 감사 (생성형 AI 검색 최적화) — 2026 신규

**AI 검색 엔진 크롤러 접근성:** GPTBot, ClaudeBot, PerplexityBot robots.txt 차단 여부, llms.txt 파일 존재 여부를 확인합니다.

**AI 인용 최적화:** FAQ, HowTo, Article 스키마 마크업, 명확한 답변형 문단 구조, 신뢰할 수 있는 데이터·출처 포함 여부를 확인합니다.

**2026년 GEO 지표:** Perplexity·Google AIO 인용 여부, ChatGPT·Gemini 브랜드 언급을 확인합니다.

### 5단계: 감사 보고서 생성

종합 점수(네이버 SEO, 구글 SEO, GEO 준비도), 즉시 개선 항목(Quick Wins), 중기 개선 항목(3개월), 장기 전략(6개월+), 경쟁사 SEO 비교, 추천 키워드 목록을 포함한 보고서를 생성합니다.

## 사용 예시

**예시 1**: "우리 블로그 네이버 SEO 감사해줘. URL은 xxx.tistory.com"
→ C-Rank 진단 → D.I.A. 체크 → 개선 우선순위 → 액션 플랜

**예시 2**: "이커머스 사이트 구글 SEO + GEO 전략 만들어줘"
→ Core Web Vitals → E-E-A-T → GEO 준비도 → 통합 최적화 로드맵

## 출력 형식

- 네이버 / 구글 / GEO 통합 SEO 감사 보고서
- 개선 우선순위별 액션 플랜
- 추천 키워드 목록 (검색량·경쟁도·의도 분류)
- 기술 SEO 체크리스트

## 주의사항

| 상황 | 대응 |
|------|------|
| URL 접근이 불가한 경우 | 사용자에게 주요 페이지 내용 공유 요청. 텍스트 기반으로 분석 진행 |
| 키워드 검색량 데이터가 없는 경우 | 네이버 광고 플랫폼·Google Keyword Planner 사용 안내. 추정 기반 제안 |
| 사이트 구조 정보가 없는 경우 | 핵심 페이지 URL 2~3개와 업종 정보로 일반 가이드라인 제공 |

## 관련 스킬

| 스킬 | 사용 시점 |
|------|----------|
| `moai-marketing:sns-content` | SNS 콘텐츠 작성이나 브랜드 전략 |
| `moai-marketing:campaign-planner` | 마케팅 캠페인 기획이나 광고 집행 |