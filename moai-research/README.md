# moai-research

연구/특허 플러그인 — 논문 검색, 학술 논문 작성, 특허 분석/출원, 연구비 신청.

5개 스킬로 연구 기획부터 논문 출판, 특허 출원, 연구비 확보까지 R&D 전과정을 지원합니다. RISS, KCI, KIPRIS 등 주요 학술/특허 DB를 활용합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [paper-search](./skills/paper-search/) | RISS/KCI/DBpia/Google Scholar 논문 통합 검색 | 1 | ✅ |
| [paper-writer](./skills/paper-writer/) | 학술 논문 구조화 작성 (APA/KCI/IEEE 포맷) | 1 | ✅ |
| [patent-search](./skills/patent-search/) | KIPRIS Plus 특허/실용신안/디자인/상표 검색 | 1 | ✅ |
| [patent-analyzer](./skills/patent-analyzer/) | 특허 맵, 선행기술 조사, FTO 분석 | 1 | ✅ |
| [grant-writer](./skills/grant-writer/) | NRF/IITP/KIAT 연구비 신청서 작성 | 1 | ✅ |

## API 키 (선택)

| 서비스 | 환경변수 | 발급처 |
|--------|---------|--------|
| KIPRIS Plus | KIPRIS_API_KEY | [plus.kipris.or.kr](https://plus.kipris.or.kr/) |
| KCI 논문 | KCI_API_KEY | [data.go.kr](https://www.data.go.kr/data/3049042/openapi.do) |

## 주요 워크플로우 체인

```
학술 논문 풀 사이클
  paper-search(통합 검색) → paper-writer(KCI/IEEE 포맷) → docx-generator → ai-slop-reviewer

특허 출원 준비
  patent-search(KIPRIS 선행기술) → patent-analyzer(FTO·특허맵) → docx-generator(출원 문서)

연구비 신청서
  grant-writer(NRF/IITP/KIAT 양식) → docx-generator → ai-slop-reviewer

논문 + 특허 통합 R&D 보고
  paper-search → patent-search → grant-writer → docx-generator
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 강의 커리큘럼 설계 | `moai-education/curriculum-designer` |
| 데이터 분석·시각화 | `moai-data/data-explorer` |
| 정부 지원사업(창업·중기부) | `moai-business/kr-gov-grant` |
| PRD·R&D 기획 | `moai-product/spec-writer` |
| 법률 IP 포트폴리오 전략 | `moai-legal/legal-risk` |

## 한국 연구·특허 환경 특화

- **KIPRIS Plus API**: 특허·실용신안·디자인·상표 통합 검색 (`KIPRIS_API_KEY` 필요)
- **KCI·RISS·DBpia**: 한국 학술지·학위논문 통합 검색
- **NRF/IITP/KIAT/KISA** 4대 R&D 기관 양식 호환
- **APA·KCI·IEEE 한국형** 인용 스타일 자동 적용
- **특허 한국 분류**: IPC·CPC·F-Term·KIPRIS 분류 통합

## 설치

Settings > Plugins > cowork-plugins에서 `moai-research` 선택

## 참고자료

| 항목 | URL | 용도 |
|------|-----|------|
| [KIPRIS Plus](https://plus.kipris.or.kr/) | 공식 API | 특허/실용신안 검색 |
| [KIPRIS 개발가이드](https://plus.kipris.or.kr/portal/bbs/view.do?nttId=1060&bbsId=B0000001) | 공식 문서 | API 사용법 |
| [KCI 논문정보 API](https://www.data.go.kr/data/3049042/openapi.do) | data.go.kr | 학술 논문 검색 |
| [KCI Open API](https://www.kci.go.kr/kciportal/po/openapi/openApiConnView.kci) | 공식 | 논문 직접 검색 |
| [RISS](https://www.riss.kr/) | 공식 | 학위논문/학술정보 |
| [DBpia](https://www.dbpia.co.kr/) | 민간 | 학술지 논문 플랫폼 |
