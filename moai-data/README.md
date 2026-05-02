# moai-data

데이터 분석 플러그인 — CSV/Excel 탐색, 공공데이터 조회, 시각화, 대시보드.

3개 스킬로 데이터 수집부터 분석, 시각화까지 전 과정을 지원합니다. Mermaid, Chart.js 기반 차트 생성 후 moai-office로 PPT/Word 변환이 가능합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [data-explorer](./skills/data-explorer/) | CSV/Excel 프로파일링, 이상값 탐지, 상관 분석 | 1 | ✅ |
| [data-visualizer](./skills/data-visualizer/) | Mermaid/Chart.js 차트, HTML 대시보드, PPT/Word 변환 | 1 | ✅ |
| [public-data](./skills/public-data/) | 공공데이터포털, KOSIS 통계 실시간 조회 | 1 | ✅ |

## 커넥터

| 커넥터 | 활용 |
|--------|------|
| Airtable | 구조화된 데이터 조회/분석 |
| Google Sheets | 스프레드시트 분석, 결과 출력 |
| Google Drive | CSV/Excel 파일 저장/공유 |
| Notion | 분석 결과 보고서 발행 |

## API 키 (선택)

| 서비스 | 환경변수 | 발급처 |
|--------|---------|--------|
| 공공데이터포털 | DATA_GO_KR_API_KEY | [data.go.kr](https://www.data.go.kr/) |
| KOSIS 통계 | KOSIS_API_KEY | [kosis.kr/openapi](https://kosis.kr/openapi/) |

## 주요 워크플로우 체인

```
CSV → 시각화 보고서
  data-explorer(프로파일링) → data-visualizer(차트 HTML) → docx-generator → ai-slop-reviewer

공공데이터 → 정책 분석
  public-data(KOSIS/data.go.kr fetch) → data-explorer → data-visualizer

KPI 대시보드 + 임원 1pager
  data-explorer → data-visualizer(shadcn/ui 대시보드) → moai-bi/executive-summary

이상값 탐지 + 보고
  data-explorer(통계·상관) → docx-generator(이슈 보고)
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 재무제표 분석(K-IFRS) | `moai-finance/financial-statements` |
| 변동분석(예산 vs 실적) | `moai-finance/variance-analysis` |
| 마케팅 ROAS·KPI | `moai-marketing/performance-report` |
| 임원 1pager 요약 | `moai-bi/executive-summary` |
| 학술 데이터 검색 | `moai-research/paper-search` |

## 한국 데이터 환경 특화

- **공공데이터포털 + KOSIS** 직접 조회 (API 키 등록 시)
- **shadcn/ui 차트 스택** — Recharts·Chart.js·Tremor·ECharts 자동 선택
- **DART 공시 데이터 연동** — `moai-business`와 결합하면 실시간 기업 재무 분석
- **Pretendard 한국어 폰트** 차트·대시보드 기본 적용

## 사용 예시

```
이 CSV 첨부했어. 매출 이상 패턴 찾고 시각화 대시보드 만들어줘.
- 컬럼: 날짜, 지역, 카테고리, 매출액, 객수
- 결과: shadcn/ui 대시보드 HTML + 이상값 보고 docx
```

```
KOSIS에서 최근 5년 한국 가구당 월평균 소비지출 통계 가져와서
연령대별 추이 차트 만들어줘.
```

## 설치

Settings > Plugins > cowork-plugins에서 `moai-data` 선택

## 참고자료

| 항목 | URL | 용도 |
|------|-----|------|
| [공공데이터포털](https://www.data.go.kr/) | 공식 API | 공공데이터 조회 |
| [KOSIS OpenAPI](https://kosis.kr/openapi/) | 공식 API | 통계청 데이터 |
| [data-go-mcp-servers](https://github.com/Koomook/data-go-mcp-servers) | 오픈소스 | 공공데이터 MCP |
| [KOSIS 개발가이드](https://kosis.kr/openapi/file/openApi_manual_v1.0.pdf) | 공식 문서 | API 사용법 |
