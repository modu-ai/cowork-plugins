---
name: patent-search
description: >
  특허를 검색하고 분석합니다.
  '특허 찾아줘', 'KIPRIS 검색', '선행기술 조사', '특허 출원 현황'이라고 요청할 때 사용하세요.
  KIPRIS Plus API로 특허/실용신안/디자인/상표를 검색하고 서지정보를 정리합니다.
user-invocable: true
---

# 특허 검색 (Patent Search)

## 개요

KIPRIS Plus(한국지식재산보호원) API를 활용하여 특허, 실용신안, 디자인, 상표를 검색하고 서지정보를 체계적으로 정리하는 전문 스킬입니다. 선행기술 조사, 출원 현황 파악, 기술 동향 분석을 지원합니다.

## 트리거 키워드

- 특허 검색, 특허 찾아줘, 특허 조사
- KIPRIS 검색, 한국 특허
- 선행기술 조사, prior art search
- 특허 출원 현황, 등록 특허
- 실용신안, 디자인권, 상표 검색

## 워크플로우

### 1단계: API 키 확인 (필수)

KIPRIS Plus API 키가 필요합니다:

```
IF KIPRIS_API_KEY 미설정:
  "특허 검색을 위해 KIPRIS Plus API 키가 필요합니다.

   발급 방법:
   1. https://plus.kipris.or.kr/ 접속 → 회원가입
   2. 마이페이지 → 인증키 발급
   3. 또는 https://www.data.go.kr/data/15065437/openapi.do 에서 활용신청 (무료)

   API 키를 입력해 주세요:"

  → 사용자가 키 입력
  → ${CLAUDE_PLUGIN_DATA}/moai-credentials.env에 KIPRIS_API_KEY 저장
  → Step 2로 진행
```

### 2단계: 검색 전략 수립

- 핵심 키워드 추출 (한국어 + 영어 동시 검색)
- IPC 분류코드 매핑 (국제특허분류)
- 검색 범위 결정 (국내/해외, 연도, 상태: 출원/등록/공개)
- 출원인/발명자 필터

### 3단계: KIPRIS API 검색

**API 기본 정보**
- Base URL: http://plus.kipris.or.kr/openapi/rest/
- 인증: ServiceKey 파라미터 (KIPRIS_API_KEY)
- 응답 형식: XML

**주요 검색 API**

| API | 설명 | 파라미터 |
|-----|------|----------|
| 검색 | 출원/등록 특허 검색 | keyword, ipc, applicant, inventor |
| 출원정보 | 출원번호 기본 정보 | applicationNumber |
| 청구항 | 청구항 텍스트 | applicationNumber |
| 인용 | 인용 특허 정보 | applicationNumber |

**검색 API 호출 예시:**
```
GET http://plus.kipris.or.kr/openapi/rest/patentSearchInfo
  ?ServiceKey={KIPRIS_API_KEY}
  &keyword={검색어}
  &ipc={IPC코드}
  &year={연도}
```

### 4단계: 검색 결과 정리

- 특허 목록 (출원번호, 제목, 출원인, 발명자, 출원일, 등록일, 상태)
- 핵심 청구항 요약 (독립항 중심)
- IPC/CPC 분류별 기술 분포
- 출원인별 경쟁 현황 (상위 10개)
- 연도별 출원 추이

### 5단계: 후속 작업 제안

- "선행기술 조사" → moai-research:patent-analyzer 스킬 연계
- "특허 맵 분석" → moai-research:patent-analyzer 스킬 연계
- "출원서 작성" → moai-research:patent-analyzer 스킬 연계
- "FTO 분석" → moai-research:patent-analyzer 스킬 연계

## 사용 예시

```
"딥러닝 기반 이미지 분류 관련 특허를 검색해줘."
"삼성전자의 반도체 관련 등록특허를 찾아줘."
"최근 5년간 배터리 기술 출원 현황을 조사해줘."
"자율주행 선행기술을 조사해줘. LiDAR 관련 특허야."
```

## 출력 형식

- 특허 목록 테이블 (출원번호, 제목, 출원인, 출원일, 상태)
- 핵심 특허 요약 (청구항 기반)
- IPC 분류별 기술 분포
- 출원인별 경쟁 현황
- 연도별 출원 추이 (데이터)

## 주의사항

- KIPRIS Plus API 키가 없는 경우 검색을 진행할 수 없습니다. API 키는 KIPRIS 또는 data.go.kr에서 무료로 발급받을 수 있습니다.
- KIPRIS API는 1,000회/월 무료 호출이 가능합니다. 초과 시 유료 요금제가 적용됩니다.
- 일부 특허는 전문 텍스트를 확인하지 못할 수 있습니다. 이 경우 서지정보와 청구항 요약만 제공됩니다.
- 선행기술 조사, FTO 분석, 출원서 작성이 필요한 경우 patent-analyzer 스킬로 연계합니다.

## 관련 스킬

- **moai-research:patent-analyzer** - 선행기술 조사, FTO 분석, 출원서 작성
- **moai-research:grant-writer** - 연구비 신청서 선행기술 섹션 작성
- **moai-data:data-visualizer** - 특허 동향 시각화 (연도별 추이, IPC 분포 차트)

## KIPRIS Plus API 안내

**발급처**
- KIPRIS: https://plus.kipris.or.kr/ (회원가입 후 인증키 발급)
- data.go.kr: https://www.data.go.kr/data/15065437/openapi.do (활용신청 후 자동승인)

**API 스펙**
- 비용: 무료 (1,000회/월)
- 인증: ServiceKey 파라미터
- 응답 형식: XML
- 개발가이드: https://plus.kipris.or.kr/portal/bbs/view.do?nttId=1060&bbsId=B0000001

**IPC 분류코드**
- A部: 생활필수품 (농업, 식품, 의약)
- B부: 처리조작, 운수 (분리, 혼합, 운수)
- C부: 화학, 야금
- D부: 섬유, 종이
- E부: 고정구조물 (건축, 광산)
- F부: 기계공학, 조명, 가열
- G부: 물리학 (전기, 통신, 컴퓨터)
- H부: 전기
