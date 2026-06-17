---
title: "데이터 트랙"
weight: 80
description: "moai-data 세 스킬과 공공데이터 API를 조합해 보고서 수준의 데이터 분석을 자동화."
geekdocBreadcrumb: true
tags: [cookbook, data]
---

# 트랙 — 데이터 분석

> CSV·Excel을 Cowork에 던지고 나면 Pandas 콘솔이 열리는 것이 아니라 **보고서 수준의 결과물**이 나오는 흐름을 만듭니다. `moai-data` 세 스킬과 공공데이터 API를 조합하는 실전 트랙입니다.

## 왜 이 흐름인가

데이터 분석은 요리에 비유하면 이해하기 쉽습니다. 재료를 검수하고(썩은 부분 골라내기), 손질하고(씻고 썰기), 접시에 예쁘게 담고(플레이팅), 코스 요리로 조립하는 네 단계로 이어집니다. 이 순서가 바뀌면 썩은 재료를 접시에 담거나 날것을 그대로 내놓는 사고가 납니다. 데이터도 같습니다. 한 번도 살펴보지 않은 원본 CSV를 곧장 차트로 그리면, 빠진 값과 튀는 값이 그대로 그래프에 반영되어 잘못된 결론을 내리게 됩니다.

그래서 `moai-data` 세 스킬은 정해진 순서로 엮입니다. 먼저 `data-explorer`가 원본 데이터의 건강 상태를 진단합니다. 이때 자주 등장하는 말이 셋 있습니다. **결측값**은 재료에 빠진 부분(비어 있는 칸), **이상값**은 비정상적으로 크거나 작은 부품(평균에서 크게 벗어난 숫자), **IQR**(사분위수 범위)은 정상 범위를 상자로 그려놓은 기준선입니다. 이 진단 결과를 `data-visualizer`가 그래프로 옮기고, 마지막으로 `moai-office` 스킬이 보고서·PPT로 포장합니다. 탐색 없이 시각화부터 하면 "썩은 재료를 접시에 담는" 결과가 되므로, 반드시 탐색 → 정제 → 시각화 순서를 지킵니다.

```mermaid
flowchart LR
    A["원본 데이터<br/>(CSV·Excel)"] --> B["① 탐색<br/>data-explorer"]
    B --> C{"결측·이상<br/>발견?"}
    C -- 발견 --> D["② 정제·보완<br/>(수동 지시)"]
    C -- 없음 --> E
    D --> E["③ 시각화<br/>data-visualizer"]
    E --> F["④ 보고서·PPT 변환<br/>moai-office"]

    style A fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style B fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style D fill:#f6e6dc,stroke:#c47b2a,color:#09110f
    style E fill:#e6f0ef,stroke:#144a46,color:#09110f
    style F fill:#d6ebe7,stroke:#1c7c70,color:#09110f
```

```mermaid
flowchart TD
    RAW["원본 데이터<br/>CSV · Excel<br/>(결측값 · 이상값 포함)"]
    S1["① 탐색<br/>data-explorer"]
    CHK{"결측·이상<br/>발견?"}
    S2["② 정제 · 보완<br/>(수동 프롬프트)"]
    S3["③ 시각화<br/>data-visualizer"]
    S4["④ 보고서 · PPT 변환<br/>moai-office"]
    PUB["공공데이터 API<br/>(KOSIS · data.go.kr)"]

    RAW --> S1
    S1 --> CHK
    CHK -->|"발견"| S2
    CHK -->|"없음 (바로 시각화)"| S3
    S2 --> S3
    PUB -.->|"CPI·거시지표로 실질 매출 계산"| S3
    S3 --> S4
```

## 트랙 지도

```mermaid
flowchart TD
    Raw[원본 데이터] --> Explore[① 데이터 탐색<br/>data-explorer]
    Explore -->|이상 없음| Visual[② 시각화<br/>data-visualizer]
    Explore -->|이상 발견| Clean[정제·보완]
    Clean --> Visual
    Visual --> Report[보고서 변환<br/>moai-office]

    Public[공공데이터 API] --> PublicData[③ public-data]
    PublicData --> Explore
```

## Part 1 — data-explorer

### 언제 쓰나

- 처음 받은 CSV·Excel의 품질을 빠르게 진단
- 결측값·이상값·중복 레코드 탐지
- 컬럼별 분포·상관관계 요약
- 1만 ~ 수십만 행 규모의 탐색

### 기본 프롬프트

{{< terminal title="claude — cowork" >}}
> D:/Input/customer-transactions-2026.csv를 분석해줘.
>
>   - 총 행수·결측률·중복 건수
>   - 수치형 컬럼 요약 통계 (평균·중앙값·표준편차·분위수)
>   - 범주형 컬럼 Top 10 빈도
>   - 이상값 탐지 (IQR 기준)
>   - 주요 상관관계 (Pearson > 0.5)
>   - 결과는 Markdown 리포트로, 90_Output/data-quality.md에 저장
{{< /terminal >}}

### 실전 팁

**큰 파일은 샘플링부터.** 500MB 이상 Excel은 탐색만 해도 5분 이상 걸립니다. "처음 1만 행만 샘플링해서" 지시하면 속도가 크게 개선됩니다.

**결측률 5% 기준.** SKILL.md 기본값은 결측률 10% 초과 컬럼에만 경고합니다. 더 보수적으로 보고 싶다면 "결측률 3% 초과 경고"를 명시하세요.

**범주형 변수 Top N.** 기본 10개. "Top 20까지" 지시 가능합니다.

## Part 2 — data-visualizer

### 언제 쓰나

- Markdown 리포트에 바로 넣을 수 있는 차트
- 인터랙티브 대시보드 (Chart.js HTML)
- Mermaid 다이어그램 (흐름도·시퀀스)
- PPT·Word로 옮길 수 있는 고정 이미지

### 기본 프롬프트

{{< terminal title="claude — cowork" >}}
> 방금 생성한 data-quality.md 분석 결과를 시각화해줘.

  - 월별 매출 추이: 선 그래프 (Chart.js HTML)
  - 카테고리별 매출 비중: 도넛 차트
  - 지역별 고객 분포: 막대 그래프
  - 모든 차트는 반응형, 다크 모드 지원
  - 저장: 90_Output/dashboards/YYYY-MM-DD.html
{{< /terminal >}}

### 차트 종류별 추천 표

| 의도 | 차트 | 이유 |
|---|---|---|
| 시간 추이 | 선 그래프 | 연속성 전달 최적 |
| 비율 | 도넛 | 파이보다 가독성 우수 |
| 순위 Top N | 막대 | 비교가 직관적 |
| 분포 | 히스토그램·박스플롯 | 분산·이상값 시각화 |
| 상관관계 | 산점도 + 추세선 | 관계의 강도·방향 |
| 프로세스 흐름 | Mermaid flowchart | 의사결정 시각화 |
| 상태 전이 | Mermaid stateDiagram | 라이프사이클 |

### PPT로 넘길 때

시각화 결과는 HTML이므로 그대로 PPT에 넣을 수 없습니다. 흐름:

1. `data-visualizer`로 HTML 대시보드 생성
2. Cowork에 "이 HTML 대시보드의 각 차트를 PNG로 캡처해줘" 지시
3. PNG를 `moai-office:pptx-designer`로 임베드

## Part 3 — public-data

### 언제 쓰나

- 공공데이터포털 (`data.go.kr`) API 조회
- KOSIS 통계청 데이터 조회
- 내부 데이터를 공공 지표와 비교
- KPI 대시보드에 거시 지표 추가

### 주요 API

| API | 용도 | 비고 |
|---|---|---|
| DART OpenDART | 상장사 공시·재무제표 | API 키 필요 (무료) |
| 공공데이터포털 | 정부 데이터 3만+ | API 키 필요 (무료) |
| KOSIS | 통계청 공식 통계 | API 키 필요 (무료) |
| KIPRIS Plus | 특허·상표 검색 | API 키 필요 (월 무료 한도) |
| KCI | 학술지 인용 | API 키 필요 |
| 국가법령정보센터 | 법령·판례 | API 키 필요 |

### 왜 거시 지표가 필요한가

용돈을 떠올려 보면 됩니다. 10년 전 용돈 5만 원과 지금의 5만 원은 살 수 있는 것이 다릅니다. 그 사이 물가가 올랐기 때문입니다. 회사 매출도 마찬가지입니다. 매출이 10% 올랐다고 진짜로 10% 성장한 것은 아닐 수 있습니다. 같은 기간 물가가 8% 올랐다면, 겉으로는 10% 늘었어도 물가 상승분을 빼고 나면 진짜 성장은 2%에 불과합니다.

이렇게 겉으로 보이는 금액을 **명목 매출**, 물가 거품을 걷어낸 진짜 가치를 **실질 매출**이라 부릅니다. 물가 상승분을 빼고 진짜 성장률을 계산하는 작업을 **디플레이트**(deflate)라고 합니다. 이때 물가의 자로 쓰는 대표 지표가 **CPI**(소비자물가지수)입니다. `public-data`로 KOSIS에서 CPI를 가져오고, `data-visualizer`로 명목 매출과 실질 매출을 한 그래프에 겹쳐 그리면 "우리가 진짜로 성장하고 있는가"라는 질문에 처음으로 정직한 대답을 얻게 됩니다. 이것이 내부 데이터만으로는 볼 수 없는, 공공데이터와 결합해야만 보이는 시야입니다.

### 기본 프롬프트

{{< terminal title="claude — cowork" >}}
> KOSIS에서 "소비자물가지수 최근 24개월"을 조회해서
내 회사 매출 데이터(Q1-sales.xlsx)와 함께 분석해줘.

- CPI 원계열 데이터 확보
- 우리 매출 금액을 CPI로 디플레이트 (실질 매출)
- 실질 매출 그래프 + 명목 매출 그래프 비교
- 인플레이션 효과 제거 후 진짜 성장률 계산
- Word 보고서로 정리, 90_Output/real-growth.docx
{{< /terminal >}}

### API 키 관리

**절대 하드코딩 금지.** 프로젝트 폴더의 `.env` 또는 `credentials.env` 파일에 저장하고 `.gitignore`에 추가하세요.

```dotenv
# .env 예시
KOSIS_API_KEY=XXXXXXXXXXXXXXXX
DART_API_KEY=YYYYYYYYYYYYYYYY
DATA_GO_KR_KEY=ZZZZZZZZZZZZ
```

SKILL.md 본문에는 환경변수 참조만 넣습니다. 예: `.env`의 `KOSIS_API_KEY` 값 사용. 절대 프롬프트·로그에 키를 노출하지 마세요.

## 통합 시나리오 — "매출 분석 완성 파이프라인"

1. **탐색 — data-explorer** — Q1 매출 CSV의 품질 진단. 결측·이상·중복 체크.
2. **정제 — 수동 프롬프트** — 이상값·결측 처리 규칙을 Cowork에 지시하여 정제 버전 생성.
3. **거시 지표 결합 — public-data** — KOSIS에서 CPI·GDP·가계소비 지출 추이 확보.
4. **시각화 — data-visualizer** — 매출 추이 + 거시 지표 비교 차트 HTML 대시보드.
5. **PPT 변환 — pptx-designer** — 임원 보고용 7장 PPT. 차트는 PNG로 임베드.
6. **Word 요약 — docx-generator** — 경영진 3페이지 요약본. 핵심 수치 + 그래프 + 제언.

이 여섯 단계는 식당의 코스 요리 완성에 비유하면 흐름이 보입니다. 재료를 검수하고(①탐색), 불량 재료를 골라내고(②정제), 시장 시세표를 받아옵니다(③거시 지표 — CPI로 실질 매출을 계산하는 것은 "물가 상승분을 빼고 진짜 늘었는지 보는" 작업입니다). 요리를 완성하고(④시각화), 고급 접시에 담아 내고(⑤PPT, 임원용), 마지막으로 한 페이지 요약 카드를 만듭니다(⑥Word). 중요한 점은 각 단계의 산출물이 곧 다음 단계의 재료가 된다는 것입니다. 아래 그래프에서 화살표를 따라가며 데이터가 어떻게 가공되며 흘러가는지 확인해 보세요.

```mermaid
flowchart LR
    S1["① 탐색<br/>data-explorer"] --> S2["② 정제<br/>수동 지시"]
    S2 --> S3["③ 거시 지표 결합<br/>public-data (CPI)"]
    S3 --> S4["④ 시각화<br/>data-visualizer"]
    S4 --> S5["⑤ PPT 변환<br/>pptx-designer"]
    S5 --> S6["⑥ Word 요약<br/>docx-generator"]

    S3 -.->|물가 거품 제거| S4

    style S1 fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style S2 fill:#f6e6dc,stroke:#c47b2a,color:#09110f
    style S3 fill:#e6f0ef,stroke:#144a46,color:#09110f
    style S4 fill:#e6f0ef,stroke:#144a46,color:#09110f
    style S5 fill:#d6ebe7,stroke:#1c7c70,color:#09110f
    style S6 fill:#d6ebe7,stroke:#1c7c70,color:#09110f
```

## 자주 걸리는 지점

### CSV 인코딩 문제

한국어 CSV는 EUC-KR·CP949·UTF-8 세 가지가 공존합니다. Cowork가 자동 감지하지만 깨진 결과가 보이면 "인코딩은 CP949로 시도해줘"라고 명시하세요.

### 일자 컬럼이 문자열로 읽힘

원인은 공백·한글 요일·슬래시·점 혼용. 프롬프트에 "날짜 컬럼은 `date_col` 이며 `YYYY-MM-DD` 또는 `YYYY/MM/DD` 둘 다 허용, 공백 제거 후 파싱"이라고 명시.

### 차트가 너무 많음

"대시보드에 차트 최대 6개"로 상한을 두세요. 넘치면 별도 상세 페이지로 분리 지시.

### 공공 API 제한 초과

일부 API는 호출당 건수·일일 한도가 있습니다. 한 번에 수천 건 요청하면 차단됩니다. SKILL.md에 "요청은 100건 단위로 배치, 배치 간 2초 지연" 규칙 명시.

## 보안·윤리

### 민감 데이터는 격리

고객 개인정보·금융 거래는 별도 암호화 폴더에서만 작업. 분석 스킬(`data-explorer`·`data-visualizer`)의 입력 프롬프트에 민감 데이터가 노출되지 않도록 명시.

### 익명화·가명화

고객 이름·이메일·전화는 해시·마스킹 처리 후 분석 대상에 포함. "이메일은 도메인만 유지, 로컬파트는 마스킹" 같은 구체적 규칙을 지시.

### 저작권·출처

공공데이터는 대부분 CC-BY 또는 공공누리. 보고서 발행 시 출처를 명기하세요.

## 다음 읽을거리

- [트랙 — 문서](../track-documents/)
- [트랙 — 마케팅](../track-marketing/)
- [보고서 자동화](../report-automation/)

---

### Sources
- [공공데이터포털](https://www.data.go.kr/)
- [KOSIS OpenAPI](https://kosis.kr/openapi/index/index.jsp)
- [modu-ai/cowork-plugins — moai-data](https://github.com/modu-ai/cowork-plugins/tree/main/moai-data)
