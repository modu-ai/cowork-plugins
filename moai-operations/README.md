# moai-operations

운영 플러그인 — 결재 프로세스, 정부조달(나라장터), SOP, 벤더 관리, 상태 보고.

업무 프로세스 표준화, 공급업체 리스크 관리, 프로젝트 현황 보고까지 운영 실무를 지원합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [process-manager](./skills/process-manager/) | 운영 매뉴얼, SOP, 조달 문서(구매 요청서/발주서), 회의록 작성 | 4 | ✅ |
| [vendor-manager](./skills/vendor-manager/) | 벤더 선정 기준, 공급업체 평가표, 계약 관리, 리스크 대응 계획 | 1 | ✅ |
| [status-reporter](./skills/status-reporter/) | 주간/월간/분기 보고서, OKR 현황, 마일스톤 진행률, KPI 대시보드 | 0 | ✅ |

## 사용 예시

```
IT 장비 구매 SOP 작성해줘. 100만원 이상은 팀장 결재, 500만원 이상은 임원 결재.
```

```
현재 거래 중인 벤더 5곳 리스크 평가 템플릿 만들어줘
```

```
이번 주 프로젝트 현황 보고서 작성해줘
```

## 주요 워크플로우 체인

```
SOP 표준화
  process-manager(절차 설계) → docx-generator(매뉴얼) → ai-slop-reviewer

벤더 평가·계약 관리
  vendor-manager(평가표·리스크 레지스터) → xlsx-creator(평가 매트릭스) → docx-generator

주간/월간 운영 보고
  status-reporter(KPI·OKR 진행률) → moai-bi/executive-summary → pptx-designer

정부조달(나라장터) 입찰 준비
  process-manager(입찰 서류) → moai-legal/compliance-check → docx-generator
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 주간 비즈니스 리뷰(WBR) | `moai-pm/weekly-report` |
| 임원 1pager 요약 | `moai-bi/executive-summary` |
| 결재·세금계산서 양식 | `moai-finance/close-management` |
| B2B 영업 제안서 | `moai-sales/proposal-writer` |

## 한국 운영 환경 특화

- **나라장터(g2b.go.kr)** 입찰 서류 양식 호환
- **결재선·전결규정** 한국 기업 표준(대표·임원·팀장 3단계)
- **회의록 한국식**: 일시·참석자·안건·결정사항·다음 단계
- **벤더 리스크 레지스터**: ESG·정보보안·재무·납기 4축 평가
- **KS 인증·ISO 9001** 품질경영 표준 양식

## 설치

Settings > Plugins > cowork-plugins에서 `moai-operations` 선택

## 참고자료

- [Anthropic 플러그인 가이드](https://code.claude.com/docs/en/plugins)
- [MoAI 마켓플레이스](https://github.com/modu-ai/cowork-plugins)
